"""ClawTeam - Framework-agnostic multi-agent coordination CLI."""

__version__ = "0.3.0+openclaw1"

from clawteam.alerts import (
    Alert,
    AlertType,
    acknowledge_alert,
    check_agent_failure_rates,
    check_task_timeouts,
    create_alert,
)
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
    # Alerts module
    "Alert",
    "AlertType",
    "create_alert",
    "acknowledge_alert",
    "check_task_timeouts",
    "check_agent_failure_rates",
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