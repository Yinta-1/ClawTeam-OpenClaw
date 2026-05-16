"""Team coordination layer for multi-agent collaboration."""

from agentteam.team.lifecycle import LifecycleManager
from agentteam.team.mailbox import MailboxManager
from agentteam.team.manager import TeamManager
from agentteam.team.plan import PlanManager
from agentteam.team.watcher import InboxWatcher


def __getattr__(name: str):
    # Lazy import to avoid circular dependency with agentteam.store
    if name == "TaskStore":
        from agentteam.team.tasks import TaskStore

        return TaskStore
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "TeamManager",
    "MailboxManager",
    "TaskStore",
    "PlanManager",
    "LifecycleManager",
    "InboxWatcher",
]
