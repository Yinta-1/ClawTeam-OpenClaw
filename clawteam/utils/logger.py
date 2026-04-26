"""Structured logging utilities for ClawTeam.

Provides JSON-formatted logging with trace_id support and per-module
log level configuration via CLAWTEAM_LOG_LEVEL environment variable.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

# Trace ID context variable for request tracking
_trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)


def get_trace_id() -> str | None:
    """Get the current trace ID from context."""
    return _trace_id_var.get()


def set_trace_id(trace_id: str | None) -> None:
    """Set the trace ID for the current context."""
    _trace_id_var.set(trace_id)


class JSONFormatter(logging.Formatter):
    """JSON log formatter that includes trace_id."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add trace_id if present
        trace_id = get_trace_id()
        if trace_id:
            log_data["trace_id"] = trace_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        for key in ("task_id", "team_name", "agent_name"):
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        return json.dumps(log_data, ensure_ascii=False, default=str)


class StructuredLogger:
    """Structured logger with JSON output and trace_id support."""

    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if args:
            msg = msg % args
        self._logger.debug(msg, extra=kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if args:
            msg = msg % args
        self._logger.info(msg, extra=kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if args:
            msg = msg % args
        self._logger.warning(msg, extra=kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if args:
            msg = msg % args
        self._logger.error(msg, extra=kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if args:
            msg = msg % args
        self._logger.critical(msg, extra=kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if args:
            msg = msg % args
        self._logger.exception(msg, extra=kwargs)


def get_logger(name: str) -> StructuredLogger:
    """Get a structured logger for the given module name.

    Configures the logger with:
    - JSON formatter
    - Rotating file handler (10MB, 5 backups)
    - Per-module log level from CLAWTEAM_LOG_LEVEL env var
    """
    logger = StructuredLogger(name)

    # Only configure once
    if logger._logger.handlers:
        return logger

    # Get log level from environment
    log_level_str = os.environ.get("CLAWTEAM_LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Set level
    logger._logger.setLevel(log_level)

    # Create console handler with JSON formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(JSONFormatter())
    logger._logger.addHandler(console_handler)

    # Create file handler with rotation
    try:
        from clawteam.paths import get_data_dir

        data_dir = get_data_dir()
        log_dir = data_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "clawteam.log"

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(JSONFormatter())
        logger._logger.addHandler(file_handler)
    except Exception:
        # If file logging fails, continue with console only
        pass

    return logger


def init_logging() -> None:
    """Initialize logging for the application.

    Call this once at application startup to configure root logging.
    """
    log_level_str = os.environ.get("CLAWTEAM_LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Add JSON formatter to root logger
    if not root_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(JSONFormatter())
        root_logger.addHandler(console_handler)
