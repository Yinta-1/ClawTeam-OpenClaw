"""Audit logging for ClawTeam operations.

Records all significant events in append-only JSONL files.
Each team has its own audit log directory.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Iterator, Optional

from clawteam.fileutil import atomic_write_text
from clawteam.paths import ensure_within_root, validate_identifier


def _now_iso() -> str:
    """Get current UTC time in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def _audit_root(team_name: str) -> Path:
    """Get the audit log root directory for a team."""
    from clawteam.team.models import get_data_dir
    d = ensure_within_root(get_data_dir() / "audit", validate_identifier(team_name, "team name"))
    d.mkdir(parents=True, exist_ok=True)
    return d


class AuditEventType(str, Enum):
    """Types of audit events."""
    TASK_CREATED = "TASK_CREATED"
    TASK_ASSIGNED = "TASK_ASSIGNED"
    TASK_COMPLETED = "TASK_COMPLETED"
    TASK_FAILED = "TASK_FAILED"
    TASK_REVIEWED = "TASK_REVIEWED"
    AGENT_STARTED = "AGENT_STARTED"
    AGENT_STOPPED = "AGENT_STOPPED"
    SYSTEM_EVENT = "SYSTEM_EVENT"
    CONFIG_CHANGED = "CONFIG_CHANGED"
    TEAM_CREATED = "TEAM_CREATED"
    TEAM_MODIFIED = "TEAM_MODIFIED"


@dataclass
class AuditEvent:
    """An audit log event."""
    
    type: AuditEventType
    team: str
    actor: str  # agent name, user ID, or "system"
    message: str
    details: dict | None = None
    timestamp: str | None = None
    
    def __post_init__(self):
        """Validate and set defaults after initialization."""
        # Validate team name
        validate_identifier(self.team, "team name")
        
        # Validate actor
        if not self.actor or not isinstance(self.actor, str):
            raise ValueError("Actor must be a non-empty string")
            
        # Set timestamp if not provided
        if self.timestamp is None:
            self.timestamp = _now_iso()
            
    def to_json(self) -> str:
        """Serialize to JSON line."""
        data = {
            "type": self.type.value,
            "team": self.team,
            "actor": self.actor,
            "message": self.message,
            "timestamp": self.timestamp,
        }
        if self.details is not None:
            data["details"] = self.details
        return json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    
    @classmethod
    def from_json(cls, json_str: str) -> AuditEvent:
        """Deserialize from JSON line."""
        data = json.loads(json_str)
        return cls(
            type=AuditEventType(data["type"]),
            team=data["team"],
            actor=data["actor"],
            message=data["message"],
            details=data.get("details"),
            timestamp=data["timestamp"]
        )


class AuditLogger:
    """Audit logger for a specific team."""
    
    def __init__(self, team_name: str):
        self.team_name = team_name
        self._root = _audit_root(team_name)
        
    def log_event(self, event: AuditEvent) -> None:
        """Log an audit event (append-only)."""
        if event.team != self.team_name:
            raise ValueError(f"Event team '{event.team}' does not match logger team '{self.team_name}'")
            
        # Find the current log file (most recent)
        log_files = sorted(self._root.glob("*.jsonl"))
        if log_files:
            current_file = log_files[-1]
        else:
            # Create new log file with timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            current_file = self._root / f"audit_{timestamp}.jsonl"
            
        # Append to the file
        with open(current_file, "a", encoding="utf-8") as f:
            f.write(event.to_json() + "\n")
            
    def get_events(
        self,
        event_type: AuditEventType | None = None,
        since: str | None = None,
        limit: int | None = None
    ) -> Iterator[AuditEvent]:
        """Get audit events with optional filtering."""
        log_files = sorted(self._root.glob("*.jsonl"))
        
        count = 0
        for log_file in reversed(log_files):  # Most recent first
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    
                # Process lines in reverse order (most recent first within file)
                for line in reversed(lines):
                    if line.strip():
                        try:
                            event = AuditEvent.from_json(line.strip())
                            
                            # Apply filters
                            if event_type is not None and event.type != event_type:
                                continue
                                
                            if since is not None and event.timestamp < since:
                                continue
                                
                            yield event
                            count += 1
                            
                            if limit is not None and count >= limit:
                                return
                                
                        except (json.JSONDecodeError, ValueError):
                            # Skip malformed lines
                            continue
                            
            except FileNotFoundError:
                # File might have been rotated/deleted
                continue


def cli_audit_log(team: str, event_type: str, actor: str, message: str, details: str | None = None) -> None:
    """CLI command to log an audit event."""
    from rich.console import Console
    
    console = Console()
    
    # Parse details if provided
    parsed_details = None
    if details:
        try:
            parsed_details = json.loads(details)
        except json.JSONDecodeError:
            console.print(f"[red]Invalid JSON for details: {details}[/red]")
            return
            
    # Create and log event
    try:
        event = AuditEvent(
            type=AuditEventType(event_type),
            team=team,
            actor=actor,
            message=message,
            details=parsed_details
        )
        logger = AuditLogger(team)
        logger.log_event(event)
        console.print(f"[green]* Logged audit event for team '{team}'[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")


def cli_audit_list(team: str, event_type: str | None = None, limit: int = 50) -> None:
    """CLI command to list audit events."""
    from rich.console import Console
    from rich.table import Table
    
    console = Console()
    
    try:
        logger = AuditLogger(team)
        type_filter = AuditEventType(event_type) if event_type else None
        
        table = Table(title=f"Audit Events for Team '{team}'")
        table.add_column("Timestamp", style="dim")
        table.add_column("Type")
        table.add_column("Actor")
        table.add_column("Message")
        
        events_shown = 0
        for event in logger.get_events(event_type=type_filter, limit=limit):
            table.add_row(
                event.timestamp,
                event.type.value,
                event.actor,
                event.message[:80] + "..." if len(event.message) > 80 else event.message
            )
            events_shown += 1
            
        if events_shown == 0:
            console.print(f"[yellow]No audit events found for team '{team}'[/yellow]")
        else:
            console.print(table)
            
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")