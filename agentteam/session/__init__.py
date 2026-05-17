"""Cross-session awareness module for AgentTeam.

This module provides session registry and cross-session communication capabilities,
inspired by SpectrAI's supervisorPrompt.ts awareness layer.

Key components:
- SessionRegistry: Central registry for all active sessions
- CrossSessionBus: Message bus for cross-session communication
"""

from agentteam.session.cross_session import (
    CrossSessionBus,
    CrossSessionMessage,
    NotificationType,
    get_cross_session_bus,
)
from agentteam.session.registry import (
    SessionInfo,
    SessionRegistry,
    SessionStatus,
    get_session_registry,
)

__all__ = [
    "SessionRegistry",
    "SessionInfo",
    "SessionStatus",
    "get_session_registry",
    "CrossSessionBus",
    "CrossSessionMessage",
    "NotificationType",
    "get_cross_session_bus",
]
