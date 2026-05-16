"""ClawTeam Tracker Module — 文件追踪和Token统计"""

from __future__ import annotations

from agentteam.tracker.change_attribution import ActiveSession, ChangeAttributor, ChangeRecord
from agentteam.tracker.diff_tracker import DiffEntry, DiffTracker, FileSnapshot
from agentteam.tracker.file_tracker import (
    FileChange,
    FileChangeTracker,
    FileChangeTrackerConfig,
    get_file_change_tracker,
    get_recent_file_changes,
    track_file_change,
)
from agentteam.tracker.file_watcher import ChangeType, FileWatcher, WatchEvent, watch_directory
from agentteam.tracker.token_stats import (
    DailyUsage,
    ProviderUsageStats,
    SessionUsage,
    TrendAnalysis,
    UsageEstimator,
    UsageSummary,
    accumulate_usage,
    estimate_tokens,
    get_provider_stats,
    get_usage_estimator,
    get_usage_summary,
    get_usage_trend,
    mark_session_ended,
    record_request,
)

__all__ = [
    # File watcher
    "FileWatcher",
    "WatchEvent",
    "ChangeType",
    "watch_directory",
    # Change attribution
    "ChangeRecord",
    "ChangeAttributor",
    "ActiveSession",
    # Diff tracker
    "DiffTracker",
    "DiffEntry",
    "FileSnapshot",
    # File change tracker
    "FileChange",
    "FileChangeTracker",
    "FileChangeTrackerConfig",
    "get_file_change_tracker",
    "track_file_change",
    "get_recent_file_changes",
    # Token stats
    "UsageEstimator",
    "UsageSummary",
    "DailyUsage",
    "SessionUsage",
    "TrendAnalysis",
    "ProviderUsageStats",
    "get_usage_estimator",
    "estimate_tokens",
    "accumulate_usage",
    "get_usage_summary",
    "get_usage_trend",
    "get_provider_stats",
    "record_request",
    "mark_session_ended",
]
