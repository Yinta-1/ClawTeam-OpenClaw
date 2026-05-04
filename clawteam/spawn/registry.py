"""
Agent Registry - golutra-style agent configuration registry.

Inspired by golutra's TerminalDefaultMemberConfig, this module provides
a registry of known agent types with their default commands and configurations.

Usage:
    from clawteam.spawn.registry import get_registry, resolve_agent_config
    
    # List all known agent types
    agents = get_registry("my-team")
    
    # Get config for specific agent type
    config = resolve_agent_config("claude-code")
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

# golutra-style agent configuration
@dataclass
class AgentConfig:
    """Configuration for a known agent type."""
    id: str                          # Unique identifier (e.g., "claude-code")
    name: str                        # Display name (e.g., "Claude Code")
    terminal_type: str               # Terminal type (e.g., "claude")
    default_command: str             # Default command to launch
    unlimited_access_flag: Optional[str] = None  # Flag for unlimited access
    resume_command_template: Optional[str] = None  # Template for resuming sessions
    post_ready_steps: list[str] = None  # Steps to execute after ready
    
    def __post_init__(self):
        if self.post_ready_steps is None:
            self.post_ready_steps = []


# Built-in agent configurations (golutra-style)
BUILTIN_AGENTS: dict[str, AgentConfig] = {
    "claude-code": AgentConfig(
        id="claude-code",
        name="Claude Code",
        terminal_type="claude",
        default_command="claude",
        unlimited_access_flag="--dangerously-skip-permissions",
        resume_command_template=None,
        post_ready_steps=["AI_ONBOARDING"],
    ),
    "codex": AgentConfig(
        id="codex",
        name="Codex CLI",
        terminal_type="codex",
        default_command="codex",
        unlimited_access_flag="--dangerously-skip-permissions",
        resume_command_template="codex --resume {session_id}",
        post_ready_steps=[],
    ),
    "gemini": AgentConfig(
        id="gemini",
        name="Gemini CLI",
        terminal_type="gemini",
        default_command="gemini",
        unlimited_access_flag=None,
        resume_command_template=None,
        post_ready_steps=[],
    ),
    "opencode": AgentConfig(
        id="opencode",
        name="OpenCode",
        terminal_type="opencode",
        default_command="opencode",
        unlimited_access_flag="--dangerously-skip-permissions",
        resume_command_template=None,
        post_ready_steps=[],
    ),
    "qwen": AgentConfig(
        id="qwen",
        name="Qwen Code",
        terminal_type="qwen",
        default_command="qwen",
        unlimited_access_flag="--dangerously-skip-permissions",
        resume_command_template=None,
        post_ready_steps=[],
    ),
    "openclaw": AgentConfig(
        id="openclaw",
        name="OpenClaw",
        terminal_type="openclaw",
        default_command="openclaw",
        unlimited_access_flag=None,
        resume_command_template=None,
        post_ready_steps=[],
    ),
}


def resolve_agent_config(agent_id: str) -> Optional[AgentConfig]:
    """Resolve agent configuration by ID.
    
    Args:
        agent_id: Agent identifier (e.g., "claude-code", "openclaw")
        
    Returns:
        AgentConfig if found, None otherwise
    """
    return BUILTIN_AGENTS.get(agent_id)


def list_agent_types() -> list[AgentConfig]:
    """List all built-in agent configurations.
    
    Returns:
        List of AgentConfig objects
    """
    return list(BUILTIN_AGENTS.values())


def get_registry(team_name: str) -> dict[str, dict]:
    """Get team agent registry.
    
    Args:
        team_name: Team name
        
    Returns:
        Dictionary of agent configurations for the team
    """
    from clawteam.config import DATA_DIR
    
    registry_path = DATA_DIR / "teams" / team_name / "agents.json"
    if registry_path.exists():
        try:
            return json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def register_agent(team_name: str, agent_name: str, config: dict) -> None:
    """Register an agent in the team registry.
    
    Args:
        team_name: Team name
        agent_name: Agent name
        config: Agent configuration dict
    """
    from clawteam.config import DATA_DIR
    
    registry_path = DATA_DIR / "teams" / team_name / "agents.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    
    registry = {}
    if registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    
    registry[agent_name] = config
    registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


# golutra's post-ready step constants (for reference)
POST_READY_STEP_AI_ONBOARDING = "AI_ONBOARDING"
POST_READY_STEP_WAIT_FOR_PATTERN = "WAIT_FOR_PATTERN"
POST_READY_STEP_EXTRACT_SESSION = "EXTRACT_SESSION_ID"


__all__ = [
    "AgentConfig",
    "BUILTIN_AGENTS",
    "resolve_agent_config",
    "list_agent_types",
    "get_registry",
    "register_agent",
]
