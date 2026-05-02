"""Collaboration enhancements for ClawTeam multi-agent coordination.

This module provides enhanced collaboration features:
- Presence status management
- Shared context board
- Activity feed
- @mention support
"""

from clawteam.collaboration.activity_feed import ActivityEntry, ActivityFeed, ActivityType
from clawteam.collaboration.context_board import ContextBoard, ContextCategory, ContextEntry
from clawteam.collaboration.mentions import Mention, MentionParser
from clawteam.collaboration.presence import PresenceManager, PresenceStatus

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
