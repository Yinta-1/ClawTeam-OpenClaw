"""Task store compatibility shim.

This module preserves the historic ``agentteam.team.tasks`` import path while
delegating the implementation to :mod:`agentteam.store`.
"""

from __future__ import annotations

from agentteam.store.base import BaseTaskStore, TaskLockError
from agentteam.store.file import FileTaskStore

TaskStore = FileTaskStore

__all__ = ["BaseTaskStore", "TaskLockError", "TaskStore"]
