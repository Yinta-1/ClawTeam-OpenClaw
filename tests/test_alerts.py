"""Tests for the alerts module."""

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from clawteam.alerts import (
    Alert,
    AlertType,
    AlertSeverity,
    create_alert,
    get_alert,
    list_alerts,
    acknowledge_alert,
)


@pytest.fixture
def temp_team_dir():
    """Create a temporary team directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["CLAWTEAM_DATA_DIR"] = tmpdir
        yield "test-team"
        os.environ.pop("CLAWTEAM_DATA_DIR", None)


def test_create_alert(temp_team_dir):
    """Test creating a basic alert."""
    team = temp_team_dir
    alert_id = create_alert(
        team=team,
        event_type=AlertType.TASK_TIMEOUT,
        severity=AlertSeverity.HIGH,
        message="Test alert message",
        source="test-source",
        details={"test": "value"},
    )
    
    # Retrieve the created alert
    alert = get_alert(team, alert_id)
    assert isinstance(alert, Alert)
    assert alert.event_type == AlertType.TASK_TIMEOUT
    assert alert.severity == AlertSeverity.HIGH
    assert alert.message == "Test alert message"
    assert alert.source == "test-source"
    assert alert.details == {"test": "value"}
    assert not alert.acknowledged
    assert alert.team == team
    
    # Verify alert was saved to disk
    alerts_root = Path(os.environ["CLAWTEAM_DATA_DIR"]) / "alerts" / team
    alert_files = list(alerts_root.glob("alert-*.json"))
    assert len(alert_files) == 1


def test_get_alert(temp_team_dir):
    """Test retrieving an alert by ID."""
    team = temp_team_dir
    alert_id = create_alert(
        team=team,
        event_type=AlertType.AGENT_FAILURE_RATE_HIGH,
        severity=AlertSeverity.MEDIUM,
        message="Agent failure rate too high",
        source="test-source",
        details={"agent": "backend-dev", "failure_rate": 0.8},
    )
    
    retrieved_alert = get_alert(team, alert_id)
    assert retrieved_alert is not None
    assert retrieved_alert.alert_id == alert_id
    assert retrieved_alert.event_type == AlertType.AGENT_FAILURE_RATE_HIGH
    assert retrieved_alert.severity == AlertSeverity.MEDIUM
    assert retrieved_alert.message == "Agent failure rate too high"


def test_list_alerts(temp_team_dir):
    """Test listing alerts."""
    team = temp_team_dir
    
    # Create multiple alerts
    alert_id1 = create_alert(
        team, 
        AlertType.TASK_TIMEOUT, 
        AlertSeverity.HIGH, 
        "Timeout alert 1",
        "source1", 
        details={"message": "Timeout 1"}
    )
    alert_id2 = create_alert(
        team, 
        AlertType.AGENT_FAILURE_RATE_HIGH, 
        AlertSeverity.MEDIUM, 
        "Failure alert 1",
        "source2", 
        details={"message": "Failure 1"}
    )
    
    # Acknowledge one alert
    acknowledge_alert(team, alert_id2, "test-user")
    
    # Test unfiltered list
    all_alerts = list_alerts(team)
    assert len(all_alerts) == 2
    
    # Test acknowledged filter
    acknowledged_alerts = [a for a in all_alerts if a.acknowledged]
    assert len(acknowledged_alerts) == 1
    assert acknowledged_alerts[0].alert_id == alert_id2
    
    unacknowledged_alerts = [a for a in all_alerts if not a.acknowledged]
    assert len(unacknowledged_alerts) == 1


def test_acknowledge_alert(temp_team_dir):
    """Test acknowledging an alert."""
    team = temp_team_dir
    alert_id = create_alert(
        team, 
        AlertType.TASK_TIMEOUT, 
        AlertSeverity.HIGH, 
        "Test alert",
        "test-source", 
        details={"message": "Test alert"}
    )
    
    # Get the alert to verify initially unacknowledged
    alert = get_alert(team, alert_id)
    assert not alert.acknowledged
    assert alert.acknowledged_by is None
    assert alert.acknowledged_at is None
    
    # Acknowledge the alert
    acknowledge_alert(team, alert_id, "test-user")
    
    # Verify acknowledgment
    updated_alert = get_alert(team, alert_id)
    assert updated_alert.acknowledged
    assert updated_alert.acknowledged_by == "test-user"
    assert updated_alert.acknowledged_at is not None


def test_alert_serialization(temp_team_dir):
    """Test that alerts can be serialized correctly."""
    team = temp_team_dir
    alert_id = create_alert(
        team=team,
        event_type=AlertType.CONFIGURATION_ERROR,
        severity=AlertSeverity.LOW,
        message="Test serialization",
        source="test-source",
        details={"key": "value"},
    )
    
    alert = get_alert(team, alert_id)
    
    # Serialize to JSON
    json_str = alert.to_json()
    data = json.loads(json_str)
    
    # Check key fields
    assert data["event_type"] == "configuration_error"
    assert data["severity"] == "low"
    assert data["message"] == "Test serialization"
    assert data["team"] == team
    assert data["details"]["key"] == "value"