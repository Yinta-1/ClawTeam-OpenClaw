"""ClawTeam - Framework-agnostic multi-agent coordination CLI."""

__version__ = "0.3.0+openclaw1"

from clawteam.audit import (
    AuditEvent,
    AuditEventType,
    get_audit_summary,
    log_audit_event,
    read_audit_log,
)
from clawteam.team import (
    InboxWatcher,
    LifecycleManager,
    MailboxManager,
    PlanManager,
    TeamManager,
)

__all__ = [
    # Audit module
    "AuditEvent",
    "AuditEventType",
    "get_audit_summary",
    "log_audit_event",
    "read_audit_log",
    # Team module
    "TeamManager",
    "MailboxManager",
    "PlanManager",
    "LifecycleManager",
    "InboxWatcher",
]