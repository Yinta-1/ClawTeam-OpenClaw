"""Collaboration enhancements for AgentTeam multi-agent coordination.

This module provides enhanced collaboration features:
- Presence status management
- Shared context board
- Activity feed
- @mention support
"""

from agentteam.collaboration.activity_feed import ActivityEntry, ActivityFeed, ActivityType
from agentteam.collaboration.context_board import ContextBoard, ContextCategory, ContextEntry
from agentteam.collaboration.mentions import Mention, MentionParser
from agentteam.collaboration.presence import PresenceManager, PresenceStatus

__all__ = [
    "PresenceStatus",
    "PresenceManager",
    "ContextBoard",
    "ContextEntry",
    "ContextCategory",
    "ActivityFeed",
    "ActivityEntry",
    "ActivityType",
    "MentionParser",
    "Mention",
]
