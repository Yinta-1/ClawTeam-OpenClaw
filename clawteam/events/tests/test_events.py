"""Tests for ClawTeam Event Tracking System (SpectrAI-inspired)."""

import json
import os
import tempfile
import threading
import time
import unittest
from pathlib import Path

# Set up test data directory before imports
_temp_dir = tempfile.mkdtemp()
os.environ["CLAWTEAM_DATA_DIR"] = _temp_dir

from clawteam.events.models import (
    EventType,
    EventSeverity,
    EventCategory,
    ClawTeamEvent,
    create_team_event,
    create_task_event,
    create_agent_event,
    create_session_event,
    create_message_event,
    create_alert_event,
    create_usage_event,
)
from clawteam.events.tracker import EventTracker
from clawteam.events.api import EventAPI


class TestEventModels(unittest.TestCase):
    """Test event model definitions."""

    def test_event_type_values(self):
        """Test that all event types are defined."""
        expected_types = [
            "team_created",
            "team_destroyed",
            "member_joined",
            "member_left",
            "member_alive",
            "task_created",
            "task_status_changed",
            "task_assigned",
            "task_completed",
            "task_blocked",
            "agent_spawned",
            "agent_terminated",
            "agent_idle",
            "agent_active",
            "turn_complete",
            "session_started",
            "session_ended",
            "message_sent",
            "message_received",
            "inbox_notification",
            "alert_triggered",
            "alert_acknowledged",
            "alert_resolved",
            "usage_recorded",
            "command_executed",
            "error_occurred",
        ]
        actual_types = [e.value for e in EventType]
        for expected in expected_types:
            self.assertIn(expected, actual_types)

    def test_event_severity_values(self):
        """Test severity levels."""
        self.assertEqual(EventSeverity.DEBUG.value, "debug")
        self.assertEqual(EventSeverity.INFO.value, "info")
        self.assertEqual(EventSeverity.WARNING.value, "warning")
        self.assertEqual(EventSeverity.ERROR.value, "error")
        self.assertEqual(EventSeverity.CRITICAL.value, "critical")

    def test_event_category_values(self):
        """Test event categories."""
        self.assertEqual(EventCategory.TEAM.value, "team")
        self.assertEqual(EventCategory.TASK.value, "task")
        self.assertEqual(EventCategory.AGENT.value, "agent")
        self.assertEqual(EventCategory.SESSION.value, "session")
        self.assertEqual(EventCategory.MESSAGE.value, "message")
        self.assertEqual(EventCategory.ALERT.value, "alert")
        self.assertEqual(EventCategory.USAGE.value, "usage")
        self.assertEqual(EventCategory.SYSTEM.value, "system")

    def test_clawteam_event_creation(self):
        """Test basic event creation."""
        event = ClawTeamEvent(
            event_type=EventType.TASK_CREATED,
            category=EventCategory.TASK,
            team_name="test-team",
            agent_name="worker-1",
            message="Task created",
            data={"task_id": "task-123"},
        )

        self.assertEqual(event.event_type, EventType.TASK_CREATED)
        self.assertEqual(event.category, EventCategory.TASK)
        self.assertEqual(event.team_name, "test-team")
        self.assertEqual(event.agent_name, "worker-1")
        self.assertEqual(event.message, "Task created")
        self.assertEqual(event.data["task_id"], "task-123")
        self.assertIsNotNone(event.id)
        self.assertIsNotNone(event.timestamp)

    def test_clawteam_event_to_dict(self):
        """Test event serialization to dict."""
        event = ClawTeamEvent(
            event_type=EventType.AGENT_SPAWNED,
            category=EventCategory.AGENT,
            agent_name="worker-1",
            session_id="sess-123",
            message="Agent spawned",
        )

        d = event.to_dict()

        self.assertIsInstance(d, dict)
        self.assertEqual(d["event_type"], "agent_spawned")
        self.assertEqual(d["category"], "agent")
        self.assertEqual(d["agent_name"], "worker-1")
        self.assertEqual(d["session_id"], "sess-123")
        self.assertEqual(d["message"], "Agent spawned")

    def test_factory_create_team_event(self):
        """Test team event factory function."""
        event = create_team_event(
            EventType.MEMBER_JOINED,
            team_name="my-team",
            agent_name="worker-1",
            message="Worker joined the team",
        )

        self.assertEqual(event.event_type, EventType.MEMBER_JOINED)
        self.assertEqual(event.category, EventCategory.TEAM)
        self.assertEqual(event.team_name, "my-team")
        self.assertEqual(event.agent_name, "worker-1")

    def test_factory_create_task_event(self):
        """Test task event factory function."""
        event = create_task_event(
            EventType.TASK_COMPLETED,
            task_id="task-456",
            team_name="my-team",
            message="Task completed successfully",
        )

        self.assertEqual(event.event_type, EventType.TASK_COMPLETED)
        self.assertEqual(event.category, EventCategory.TASK)
        self.assertEqual(event.task_id, "task-456")

    def test_factory_create_agent_event(self):
        """Test agent event factory function."""
        event = create_agent_event(
            EventType.TURN_COMPLETE,
            agent_name="worker-1",
            session_id="sess-789",
            duration_ms=1500.0,
            message="Turn completed in 1500ms",
        )

        self.assertEqual(event.event_type, EventType.TURN_COMPLETE)
        self.assertEqual(event.category, EventCategory.AGENT)
        self.assertEqual(event.duration_ms, 1500.0)

    def test_factory_create_session_event(self):
        """Test session event factory function."""
        event = create_session_event(
            EventType.SESSION_STARTED,
            session_id="sess-123",
            agent_name="worker-1",
            team_name="my-team",
        )

        self.assertEqual(event.event_type, EventType.SESSION_STARTED)
        self.assertEqual(event.category, EventCategory.SESSION)
        self.assertEqual(event.session_id, "sess-123")

    def test_factory_create_message_event(self):
        """Test message event factory function."""
        event = create_message_event(
            EventType.MESSAGE_SENT,
            team_name="my-team",
            sender="worker-1",
            recipient="worker-2",
            message="Hello!",
        )

        self.assertEqual(event.event_type, EventType.MESSAGE_SENT)
        self.assertEqual(event.category, EventCategory.MESSAGE)

    def test_factory_create_alert_event(self):
        """Test alert event factory function."""
        event = create_alert_event(
            EventType.ALERT_TRIGGERED,
            team_name="my-team",
            message="High memory usage detected",
            severity=EventSeverity.WARNING,
        )

        self.assertEqual(event.event_type, EventType.ALERT_TRIGGERED)
        self.assertEqual(event.category, EventCategory.ALERT)
        self.assertEqual(event.severity, EventSeverity.WARNING)

    def test_factory_create_usage_event(self):
        """Test usage event factory function."""
        event = create_usage_event(
            team_name="my-team",
            session_id="sess-123",
            input_tokens=1000,
            output_tokens=500,
            estimated_cost=0.05,
        )

        self.assertEqual(event.event_type, EventType.USAGE_RECORDED)
        self.assertEqual(event.category, EventCategory.USAGE)
        self.assertEqual(event.data["input_tokens"], 1000)
        self.assertEqual(event.data["output_tokens"], 500)


class TestEventTracker(unittest.TestCase):
    """Test event tracker functionality."""

    def setUp(self):
        """Set up test tracker with temporary database."""
        self.db_path = Path(_temp_dir) / "test_events.db"
        self.tracker = EventTracker(str(self.db_path))

    def tearDown(self):
        """Clean up tracker and database."""
        self.tracker.close()
        # Delete database file to isolate tests
        if self.db_path.exists():
            self.db_path.unlink()

    def test_track_single_event(self):
        """Test tracking a single event."""
        event = create_team_event(
            EventType.TEAM_CREATED,
            team_name="test-team",
            message="Team created",
        )

        self.tracker.track(event)

        # Query the event
        events = self.tracker.query(team_name="test-team")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "team_created")
        self.assertEqual(events[0]["team_name"], "test-team")

    def test_track_multiple_events(self):
        """Test tracking multiple events."""
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="team-a"),
            create_team_event(EventType.MEMBER_JOINED, team_name="team-a", agent_name="worker-1"),
            create_task_event(EventType.TASK_CREATED, task_id="task-1", team_name="team-a"),
        ]

        self.tracker.track_batch(events)

        # Query all events
        all_events = self.tracker.query(team_name="team-a")
        self.assertEqual(len(all_events), 3)

    def test_query_by_event_type(self):
        """Test querying by event type."""
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="team-a"),
            create_team_event(EventType.MEMBER_JOINED, team_name="team-a"),
            create_team_event(EventType.MEMBER_JOINED, team_name="team-b"),
        ]
        self.tracker.track_batch(events)

        # Query by event type
        joined_events = self.tracker.query(event_types=["member_joined"])
        self.assertEqual(len(joined_events), 2)

    def test_query_by_category(self):
        """Test querying by category."""
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="team-a"),
            create_task_event(EventType.TASK_CREATED, task_id="task-1"),
            create_agent_event(EventType.TURN_COMPLETE, agent_name="worker-1"),
        ]
        self.tracker.track_batch(events)

        # Query by category
        task_events = self.tracker.query(categories=["task"])
        self.assertEqual(len(task_events), 1)
        self.assertEqual(task_events[0]["category"], "task")

    def test_query_with_limit_offset(self):
        """Test query pagination."""
        # Create 10 events
        events = [create_team_event(EventType.TEAM_CREATED, team_name=f"team-{i}") for i in range(10)]
        self.tracker.track_batch(events)

        # Get first 5
        first_page = self.tracker.query(limit=5, offset=0)
        self.assertEqual(len(first_page), 5)

        # Get next 5
        second_page = self.tracker.query(limit=5, offset=5)
        self.assertEqual(len(second_page), 5)

    def test_get_events_for_dashboard(self):
        """Test getting dashboard events."""
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="dash-team"),
            create_agent_event(EventType.TURN_COMPLETE, agent_name="worker-1", team_name="dash-team"),
            create_task_event(EventType.TASK_COMPLETED, task_id="task-1", team_name="dash-team"),
        ]
        self.tracker.track_batch(events)

        dashboard = self.tracker.get_events_for_dashboard("dash-team")
        self.assertEqual(len(dashboard), 3)

    def test_get_agent_timeline(self):
        """Test getting agent timeline."""
        events = [
            create_agent_event(EventType.AGENT_SPAWNED, agent_name="worker-1"),
            create_agent_event(EventType.TURN_COMPLETE, agent_name="worker-1", duration_ms=100.0),
            create_agent_event(EventType.TURN_COMPLETE, agent_name="worker-1", duration_ms=200.0),
            create_agent_event(EventType.AGENT_TERMINATED, agent_name="worker-1"),
        ]
        self.tracker.track_batch(events)

        timeline = self.tracker.get_agent_timeline("worker-1")
        self.assertEqual(len(timeline), 4)

    def test_get_task_events(self):
        """Test getting task event history."""
        events = [
            create_task_event(EventType.TASK_CREATED, task_id="task-123"),
            create_task_event(EventType.TASK_ASSIGNED, task_id="task-123", agent_name="worker-1"),
            create_task_event(EventType.TASK_COMPLETED, task_id="task-123"),
        ]
        self.tracker.track_batch(events)

        history = self.tracker.get_task_events("task-123")
        self.assertEqual(len(history), 3)

    def test_get_event_stats(self):
        """Test getting event statistics."""
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="stats-team"),
            create_team_event(EventType.MEMBER_JOINED, team_name="stats-team"),
            create_team_event(EventType.MEMBER_JOINED, team_name="stats-team"),
            create_task_event(EventType.TASK_CREATED, task_id="task-1"),
        ]
        self.tracker.track_batch(events)

        stats = self.tracker.get_event_stats(team_name="stats-team")

        self.assertEqual(stats["total_events"], 3)
        self.assertIn("by_category", stats)
        self.assertIn("by_type", stats)
        self.assertIn("by_severity", stats)
        self.assertEqual(stats["by_category"].get("team"), 3)
        self.assertEqual(stats["by_type"].get("member_joined"), 2)

    def test_clear_old_events(self):
        """Test clearing old events."""
        # Create some events
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="old-team"),
        ]
        self.tracker.track_batch(events)

        # Clear events older than 0 days (should clear all)
        deleted = self.tracker.clear_old_events(days=0)
        self.assertGreaterEqual(deleted, 1)

        # Verify no events remain
        remaining = self.tracker.query(team_name="old-team")
        self.assertEqual(len(remaining), 0)

    def test_thread_safety(self):
        """Test thread-safe event tracking."""
        events = []
        for i in range(50):
            events.append(
                create_team_event(
                    EventType.TEAM_CREATED,
                    team_name="thread-test",
                    agent_name=f"worker-{i}",
                )
            )

        def track_batch(batch):
            self.tracker.track_batch(batch)

        threads = []
        for i in range(5):
            t = threading.Thread(target=track_batch, args=(events[i * 10 : (i + 1) * 10],))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        # All events should be tracked
        tracked = self.tracker.query(team_name="thread-test")
        self.assertEqual(len(tracked), 50)


class TestEventAPI(unittest.TestCase):
    """Test EventAPI functionality."""

    def setUp(self):
        """Set up test API with temporary database."""
        self.db_path = Path(_temp_dir) / "test_api_events.db"
        self.tracker = EventTracker(str(self.db_path))
        self.api = EventAPI(self.tracker)

    def tearDown(self):
        """Clean up tracker and database."""
        self.tracker.close()
        # Delete database file to isolate tests
        if self.db_path.exists():
            self.db_path.unlink()

    def test_record_event(self):
        """Test recording an event via API."""
        event = create_team_event(
            EventType.TEAM_CREATED,
            team_name="api-team",
            message="Test event",
        )

        result = self.api.record_event(event)

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["event_id"])

    def test_record_team_created(self):
        """Test recording team creation via API."""
        result = self.api.record_team_created(
            team_name="new-team",
            agent_name="creator",
            message="Team created by API",
        )

        self.assertTrue(result["success"])

        # Verify event was stored
        events = self.tracker.query(team_name="new-team")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "team_created")

    def test_record_turn_complete(self):
        """Test recording turn_complete event (SpectrAI-inspired)."""
        result = self.api.record_turn_complete(
            agent_name="worker-1",
            session_id="sess-123",
            team_name="spectrai-team",
            duration_ms=1500.0,
            message="Turn completed",
        )

        self.assertTrue(result["success"])

        # Verify event
        events = self.tracker.query(agent_name="worker-1")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "turn_complete")
        self.assertEqual(events[0]["duration_ms"], 1500.0)

    def test_record_agent_spawned(self):
        """Test recording agent spawn event."""
        result = self.api.record_agent_spawned(
            agent_name="worker-1",
            agent_id="agent-abc123",
            team_name="spawn-team",
            session_id="sess-456",
        )

        self.assertTrue(result["success"])

        events = self.tracker.query(agent_name="worker-1")
        self.assertEqual(events[0]["event_type"], "agent_spawned")

    def test_get_events(self):
        """Test getting events via API."""
        # Track some events
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="query-team"),
            create_team_event(EventType.MEMBER_JOINED, team_name="query-team"),
        ]
        self.tracker.track_batch(events)

        # Get via API
        result = self.api.get_events(team_name="query-team", limit=10)

        self.assertEqual(result["count"], 2)
        self.assertEqual(len(result["events"]), 2)
        self.assertTrue(result["has_more"] is False or result["count"] < result["limit"])

    def test_get_stats(self):
        """Test getting statistics via API."""
        events = [
            create_team_event(EventType.TEAM_CREATED, team_name="stats-team"),
            create_agent_event(EventType.TURN_COMPLETE, agent_name="worker-1"),
        ]
        self.tracker.track_batch(events)

        stats = self.api.get_stats(team_name="stats-team")

        self.assertIn("total_events", stats)
        self.assertIn("by_category", stats)
        self.assertIn("by_type", stats)


class TestEventIntegration(unittest.TestCase):
    """Integration tests for event tracking system."""

    def setUp(self):
        """Set up test environment."""
        self.db_path = Path(_temp_dir) / "test_integration.db"
        self.tracker = EventTracker(str(self.db_path))

    def tearDown(self):
        """Clean up tracker and database."""
        self.tracker.close()
        # Delete database file to isolate tests
        if self.db_path.exists():
            self.db_path.unlink()

    def test_full_agent_lifecycle(self):
        """Test tracking a complete agent lifecycle."""
        agent_name = "lifecycle-agent"
        team_name = "lifecycle-team"
        session_id = "lifecycle-session"

        # Spawn event
        spawn_event = create_agent_event(
            EventType.AGENT_SPAWNED,
            agent_name=agent_name,
            agent_id="agent-lifecycle",
            team_name=team_name,
            session_id=session_id,
        )
        self.tracker.track(spawn_event)

        # Turn complete events
        for i in range(3):
            turn_event = create_agent_event(
                EventType.TURN_COMPLETE,
                agent_name=agent_name,
                session_id=session_id,
                team_name=team_name,
                duration_ms=1000.0 + (i * 100),
            )
            self.tracker.track(turn_event)

        # Session end event
        end_event = create_session_event(
            EventType.SESSION_ENDED,
            session_id=session_id,
            agent_name=agent_name,
            team_name=team_name,
        )
        self.tracker.track(end_event)

        # Terminate event
        term_event = create_agent_event(
            EventType.AGENT_TERMINATED,
            agent_name=agent_name,
            agent_id="agent-lifecycle",
            team_name=team_name,
        )
        self.tracker.track(term_event)

        # Query agent timeline
        timeline = self.tracker.get_agent_timeline(agent_name)
        self.assertEqual(len(timeline), 6)  # spawn + 3 turns + session end + terminate

        # Verify sequence
        event_types = [e["event_type"] for e in timeline]
        self.assertEqual(event_types[0], "agent_spawned")
        self.assertEqual(event_types[1], "turn_complete")
        self.assertEqual(event_types[-1], "agent_terminated")

    def test_full_task_lifecycle(self):
        """Test tracking a complete task lifecycle."""
        task_id = "task-lifecycle-123"
        team_name = "task-team"

        # Create task
        self.tracker.track(
            create_task_event(
                EventType.TASK_CREATED,
                task_id=task_id,
                team_name=team_name,
            )
        )

        # Assign task
        self.tracker.track(
            create_task_event(
                EventType.TASK_ASSIGNED,
                task_id=task_id,
                team_name=team_name,
                agent_name="worker-1",
            )
        )

        # Update status
        self.tracker.track(
            create_task_event(
                EventType.TASK_STATUS_CHANGED,
                task_id=task_id,
                team_name=team_name,
                data={"from": "pending", "to": "in_progress"},
            )
        )

        # Complete task
        self.tracker.track(
            create_task_event(
                EventType.TASK_COMPLETED,
                task_id=task_id,
                team_name=team_name,
                agent_name="worker-1",
            )
        )

        # Query task history
        history = self.tracker.get_task_events(task_id)
        self.assertEqual(len(history), 4)

        # Verify sequence
        event_types = [e["event_type"] for e in history]
        self.assertIn("task_created", event_types)
        self.assertIn("task_completed", event_types)


if __name__ == "__main__":
    unittest.main()
