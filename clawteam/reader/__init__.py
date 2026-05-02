"""Output reader system for multi-provider support."""

from __future__ import annotations

from clawteam.reader.jsonl_parser import ClaudeJsonlReader
from clawteam.reader.manager import OutputReaderManager
from clawteam.reader.types import (
    BaseOutputReader,
    OutputEvent,
    OutputEventType,
    ReaderState,
    TokenUsage,
)

__all__ = [
    "OutputEvent",
    "TokenUsage",
    "ReaderState",
    "OutputEventType",
    "BaseOutputReader",
    "OutputReaderManager",
    "ClaudeJsonlReader",
]
