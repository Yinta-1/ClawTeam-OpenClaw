"""Tests for the audit logging module."""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from clawteam.utils.audit import (
    AuditEvent,
    AuditEventType,
    AuditLogger,
    _now_iso,
    _audit_root,
)


class TestAuditEvent:
    """Test AuditEvent model and validation."""
    
    def test_audit_event_creation(self):
        """Test basic AuditEvent creation with required fields."""
        event = AuditEvent(
            type=AuditEventType.TASK_CREATED,
            team="test-team",
            actor="test-user",
            message="Task created",
            details={"task_id": "123"}
        )
        assert event.type == AuditEventType.TASK_CREATED
        assert event.team == "test-team"
        assert event.actor == "test-user"
        assert event.message == "Task created"
        assert event.details == {"task_id": "123"}
        assert event.timestamp is not None
        
    def test_audit_event_timestamp_format(self):
        """Test that timestamp is in ISO format with timezone."""
        event = AuditEvent(
            type=AuditEventType.TASK_COMPLETED,
            team="test-team",
            actor="test-user",
            message="Task completed"
        )
        # Should be ISO format with timezone info
        dt = datetime.fromisoformat(event.timestamp.replace('Z', '+00:00'))
        assert dt.tzinfo is not None
        
    def test_audit_event_validation_team_name(self):
        """Test team name validation."""
        with pytest.raises(ValueError, match="Invalid team name"):
            AuditEvent(
                type=AuditEventType.TASK_CREATED,
                team="invalid team name!",  # contains spaces and special chars
                actor="test-user",
                message="Task created"
            )
            
    def test_audit_event_validation_actor(self):
        """Test actor validation."""
        with pytest.raises(ValueError, match="Actor must be a non-empty string"):
            AuditEvent(
                type=AuditEventType.TASK_CREATED,
                team="valid-team",
                actor="",  # empty actor
                message="Task created"
            )
            
    def test_audit_event_optional_fields(self):
        """Test that optional fields can be omitted."""
        event = AuditEvent(
            type=AuditEventType.SYSTEM_EVENT,
            team="test-team",
            actor="system",
            message="System started"
        )
        assert event.details is None


class TestAuditLogger:
    """Test AuditLogger functionality."""
    
    def setup_method(self):
        """Set up temporary directory for each test."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_data_dir = os.environ.get('CLAWTEAM_DATA_DIR')
        os.environ['CLAWTEAM_DATA_DIR'] = self.temp_dir
        
    def teardown_method(self):
        """Clean up temporary directory."""
        if self.original_data_dir is not None:
            os.environ['CLAWTEAM_DATA_DIR'] = self.original_data_dir
        else:
            os.environ.pop('CLAWTEAM_DATA_DIR', None)
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        
    def test_audit_root_creation(self):
        """Test that audit root directory is created properly."""
        team_name = "test-team"
        root = _audit_root(team_name)
        assert root.exists()
        assert root.is_dir()
        # Use os.path.sep for cross-platform compatibility
        expected_suffix = f"audit{os.path.sep}{team_name}"
        assert str(root).endswith(expected_suffix)
        
    def test_log_event_basic(self):
        """Test basic event logging functionality."""
        logger = AuditLogger("test-team")
        event = AuditEvent(
            type=AuditEventType.TASK_CREATED,
            team="test-team",
            actor="test-user",
            message="Test task created",
            details={"task_id": "test-123"}
        )
        
        # Log the event
        logger.log_event(event)
        
        # Check that file was created
        audit_files = list(_audit_root("test-team").glob("*.jsonl"))
        assert len(audit_files) == 1
        
        # Read and verify content
        with open(audit_files[0], 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 1
            logged_event = json.loads(lines[0])
            assert logged_event['type'] == 'TASK_CREATED'
            assert logged_event['team'] == 'test-team'
            assert logged_event['actor'] == 'test-user'
            assert logged_event['message'] == 'Test task created'
            assert logged_event['details'] == {'task_id': 'test-123'}
            
    def test_log_event_append_only(self):
        """Test that events are appended to existing files, not overwritten."""
        logger = AuditLogger("test-team")
        
        # Log first event
        event1 = AuditEvent(
            type=AuditEventType.TASK_CREATED,
            team="test-team",
            actor="user1",
            message="First task"
        )
        logger.log_event(event1)
        
        # Log second event
        event2 = AuditEvent(
            type=AuditEventType.TASK_COMPLETED,
            team="test-team",
            actor="user2",
            message="Second task"
        )
        logger.log_event(event2)
        
        # Check that both events are in the same file
        audit_files = list(_audit_root("test-team").glob("*.jsonl"))
        assert len(audit_files) == 1
        
        with open(audit_files[0], 'r', encoding='utf-8') as f:
            lines = f.readlines()
            assert len(lines) == 2
            event1_data = json.loads(lines[0])
            event2_data = json.loads(lines[1])
            assert event1_data['message'] == 'First task'
            assert event2_data['message'] == 'Second task'
            
    def test_get_events_all(self):
        """Test retrieving all events for a team."""
        logger = AuditLogger("test-team")
        
        # Log multiple events
        events = []
        for i in range(3):
            event = AuditEvent(
                type=AuditEventType.TASK_CREATED,
                team="test-team",
                actor=f"user{i}",
                message=f"Task {i}"
            )
            logger.log_event(event)
            events.append(event)
            
        # Retrieve all events
        retrieved_events = list(logger.get_events())
        assert len(retrieved_events) == 3
        
        # Verify order (should be reverse chronological - newest first)
        for i, retrieved in enumerate(retrieved_events):
            expected_index = 2 - i  # newest first: Task 2, Task 1, Task 0
            assert retrieved.message == f"Task {expected_index}"
            assert retrieved.actor == f"user{expected_index}"
            
    def test_get_events_by_type(self):
        """Test filtering events by type."""
        logger = AuditLogger("test-team")
        
        # Log different types of events
        task_created = AuditEvent(
            type=AuditEventType.TASK_CREATED,
            team="test-team",
            actor="user1",
            message="Task created"
        )
        task_completed = AuditEvent(
            type=AuditEventType.TASK_COMPLETED,
            team="test-team",
            actor="user2",
            message="Task completed"
        )
        system_event = AuditEvent(
            type=AuditEventType.SYSTEM_EVENT,
            team="test-team",
            actor="system",
            message="System event"
        )
        
        logger.log_event(task_created)
        logger.log_event(task_completed)
        logger.log_event(system_event)
        
        # Get only TASK_CREATED events
        created_events = list(logger.get_events(event_type=AuditEventType.TASK_CREATED))
        assert len(created_events) == 1
        assert created_events[0].type == AuditEventType.TASK_CREATED
        assert created_events[0].message == "Task created"
        
        # Get only SYSTEM_EVENT events
        system_events = list(logger.get_events(event_type=AuditEventType.SYSTEM_EVENT))
        assert len(system_events) == 1
        assert system_events[0].type == AuditEventType.SYSTEM_EVENT
        
    def test_get_events_since_timestamp(self):
        """Test filtering events by timestamp."""
        logger = AuditLogger("test-team")
        
        # Log events at different times
        with patch('clawteam.utils.audit._now_iso') as mock_now:
            # First event
            mock_now.return_value = "2023-01-01T10:00:00+00:00"
            event1 = AuditEvent(
                type=AuditEventType.TASK_CREATED,
                team="test-team",
                actor="user1",
                message="Early task"
            )
            logger.log_event(event1)
            
            # Second event
            mock_now.return_value = "2023-01-01T11:00:00+00:00"
            event2 = AuditEvent(
                type=AuditEventType.TASK_COMPLETED,
                team="test-team",
                actor="user2",
                message="Later task"
            )
            logger.log_event(event2)
            
        # Get events since 10:30 AM
        since_timestamp = "2023-01-01T10:30:00+00:00"
        recent_events = list(logger.get_events(since=since_timestamp))
        assert len(recent_events) == 1
        assert recent_events[0].message == "Later task"
        
    def test_multiple_teams_isolation(self):
        """Test that audit logs are isolated between teams."""
        team1_logger = AuditLogger("team1")
        team2_logger = AuditLogger("team2")
        
        # Log events for both teams
        team1_event = AuditEvent(
            type=AuditEventType.TASK_CREATED,
            team="team1",
            actor="user1",
            message="Team1 task"
        )
        team2_event = AuditEvent(
            type=AuditEventType.TASK_CREATED,
            team="team2",
            actor="user2",
            message="Team2 task"
        )
        
        team1_logger.log_event(team1_event)
        team2_logger.log_event(team2_event)
        
        # Verify isolation
        team1_events = list(team1_logger.get_events())
        team2_events = list(team2_logger.get_events())
        
        assert len(team1_events) == 1
        assert len(team2_events) == 1
        assert team1_events[0].message == "Team1 task"
        assert team2_events[0].message == "Team2 task"
        
    def test_cli_command_integration(self):
        """Test CLI command functionality (mocked)."""
        from clawteam.utils.audit import cli_audit_log, cli_audit_list
        
        # Mock console output
        with patch('rich.console.Console') as mock_console:
            mock_console_instance = MagicMock()
            mock_console.return_value = mock_console_instance
            
            # Test log command
            cli_audit_log("test-team", "TASK_CREATED", "test-user", "CLI test message")
            mock_console_instance.print.assert_called_with("[green]* Logged audit event for team 'test-team'[/green]")
            
            # Test list command
            cli_audit_list("test-team")
            # Should have called print at least once for the header or events
            assert mock_console_instance.print.call_count >= 1


def test_now_iso_format():
    """Test that _now_iso returns proper ISO format with timezone."""
    timestamp = _now_iso()
    # Should be able to parse it back
    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    assert dt.tzinfo is not None
    # Should be roughly current time
    now = datetime.now(timezone.utc)
    diff = abs((dt - now).total_seconds())
    assert diff < 5  # within 5 seconds