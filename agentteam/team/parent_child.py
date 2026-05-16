"""Parent-Child lifecycle management for ClawTeam agents.

Tracks the hierarchical relationship between parent and child agents.
When a parent agent exits, all its children (and descendants) are cleaned up.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from agentteam.fileutil import atomic_write_text, file_locked
from agentteam.paths import ensure_within_root, validate_identifier
from agentteam.team.models import get_data_dir


def _parent_child_path(team_name: str) -> Path:
    return ensure_within_root(
        get_data_dir() / "teams",
        validate_identifier(team_name, "team name"),
        "parent_child.json",
    )


def _load_registry(team_name: str) -> dict[str, dict]:
    path = _parent_child_path(team_name)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def _save_registry(team_name: str, data: dict) -> None:
    atomic_write_text(_parent_child_path(team_name), json.dumps(data, indent=2))


class ParentChildRegistry:
    """Registry tracking parent-child relationships between agents.

    Each agent can have zero or one parent (parent_agent).
    An agent can have zero or more children (child_agents).
    """

    @staticmethod
    def register(
        team_name: str,
        child_agent: str,
        parent_agent: str,
    ) -> None:
        """Register a child agent under a parent agent.

        Creates the parent entry if it doesn't exist.
        Appends the child to the parent's child list.
        Sets the child entry's parent.
        """
        validate_identifier(team_name, "team name")
        validate_identifier(child_agent, "child agent name")
        validate_identifier(parent_agent, "parent agent name")

        path = _parent_child_path(team_name)
        with file_locked(path):
            registry = _load_registry(team_name)

            # Ensure parent entry exists
            if parent_agent not in registry:
                registry[parent_agent] = {
                    "agent_name": parent_agent,
                    "parent": None,
                    "children": [],
                    "registered_at": time.time(),
                }

            # Add child to parent's children list (dedup)
            parent_entry = registry[parent_agent]
            if child_agent not in parent_entry["children"]:
                parent_entry["children"].append(child_agent)
                parent_entry["registered_at"] = time.time()

            # Set child's parent
            registry[child_agent] = {
                "agent_name": child_agent,
                "parent": parent_agent,
                "children": [],
                "registered_at": time.time(),
            }

            _save_registry(team_name, registry)

    @staticmethod
    def unregister(team_name: str, agent_name: str) -> list[str]:
        """Unregister an agent and return its child agents that were also unregistered.

        Does NOT recursively remove descendants — use terminate_tree() for that.
        Returns list of child agents that were removed (direct children only).
        """
        validate_identifier(team_name, "team name")
        validate_identifier(agent_name, "agent name")

        path = _parent_child_path(team_name)
        with file_locked(path):
            registry = _load_registry(team_name)
            if agent_name not in registry:
                return []

            entry = registry.pop(agent_name, {})
            children_removed: list[str] = []

            # Remove this agent from its parent's children list
            if entry.get("parent"):
                parent_name = entry["parent"]
                if parent_name in registry:
                    parent_entry = registry[parent_name]
                    if agent_name in parent_entry["children"]:
                        parent_entry["children"].remove(agent_name)

            # Remove this agent's children entries (they now have no parent)
            for child_name in entry.get("children", []):
                if child_name in registry:
                    child_entry = registry.pop(child_name)
                    # Grandchildren keep their parent (now orphaned from this branch)
                    # but their parent field still points to the removed agent
                    children_removed.append(child_name)

            _save_registry(team_name, registry)
            return children_removed

    @staticmethod
    def get_children(team_name: str, agent_name: str) -> list[str]:
        """Return the list of direct child agents for a given agent."""
        validate_identifier(team_name, "team name")
        validate_identifier(agent_name, "agent name")
        registry = _load_registry(team_name)
        if agent_name not in registry:
            return []
        return list(registry[agent_name].get("children", []))

    @staticmethod
    def get_parent(team_name: str, agent_name: str) -> str | None:
        """Return the parent agent name, or None if no parent."""
        validate_identifier(team_name, "team name")
        validate_identifier(agent_name, "agent name")
        registry = _load_registry(team_name)
        if agent_name not in registry:
            return None
        return registry[agent_name].get("parent")

    @staticmethod
    def get_descendants(team_name: str, agent_name: str) -> list[str]:
        """Return all descendants (children, grandchildren, etc.) of an agent."""
        validate_identifier(team_name, "team name")
        validate_identifier(agent_name, "agent name")
        registry = _load_registry(team_name)
        if agent_name not in registry:
            return []

        descendants: list[str] = []
        queue = list(registry[agent_name].get("children", []))
        while queue:
            child = queue.pop(0)
            descendants.append(child)
            if child in registry:
                queue.extend(registry[child].get("children", []))
        return descendants

    @staticmethod
    def get_ancestors(team_name: str, agent_name: str) -> list[str]:
        """Return all ancestors (parent, grandparent, etc.) of an agent, oldest first."""
        validate_identifier(team_name, "team name")
        validate_identifier(agent_name, "agent name")
        registry = _load_registry(team_name)
        ancestors: list[str] = []
        current = agent_name
        visited: set[str] = set()
        while True:
            if current not in registry:
                break
            parent = registry[current].get("parent")
            if not parent or parent in visited:
                break
            ancestors.append(parent)
            visited.add(parent)
            current = parent
        return ancestors

    @staticmethod
    def list_all(team_name: str) -> dict[str, dict]:
        """Return the full parent-child registry for a team."""
        validate_identifier(team_name, "team name")
        return _load_registry(team_name)

    @staticmethod
    def terminate_tree(
        team_name: str,
        root_agent: str,
        spawn_registry: "ParentChildRegistry | None" = None,
    ) -> list[str]:
        """Terminate an entire tree of agents, bottom-up.

        Returns list of all terminated agent names (root first, leaves last for cleanup order).

        Note: This only removes registry entries; actual process termination
        must be done by the caller via spawn registry + backend.
        """
        validate_identifier(team_name, "team name")
        validate_identifier(root_agent, "root agent name")

        from agentteam.spawn.registry import unregister_agent

        terminated: list[str] = []
        # Get all descendants first (they need to be terminated before the root)
        descendants = ParentChildRegistry.get_descendants(team_name, root_agent)
        # Reverse so leaves are terminated first
        descendants.reverse()

        # Terminate each descendant
        for agent in descendants:
            # Remove from spawn registry
            unregister_agent(team_name, agent)
            terminated.append(agent)

        # Unregister root from parent-child registry
        ParentChildRegistry.unregister(team_name, root_agent)
        # Remove from spawn registry
        unregister_agent(team_name, root_agent)
        terminated.append(root_agent)

        return terminated
