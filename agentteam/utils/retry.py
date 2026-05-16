"""Retry utilities with exponential backoff and jitter.

Provides a ``@retry`` decorator and async variant for wrapping functions
that may fail transiently (file I/O, network calls, lock acquisition).
"""

from __future__ import annotations

import asyncio
import random
import time
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, TypeVar

from agentteam.utils.logger import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


@dataclass
class RetryConfig:
    """Configuration for retry behaviour."""

    max_retries: int = 3
    """Maximum number of retry attempts."""

    base_delay: float = 0.5
    """Base delay in seconds for exponential backoff."""

    max_delay: float = 30.0
    """Maximum delay cap in seconds."""

    jitter: bool = True
    """Enable random jitter to prevent thundering herd."""

    retryable_exceptions: tuple[type[Exception], ...] = (
        OSError,
        IOError,
        TimeoutError,
        ConnectionError,
    )
    """Exception types that trigger a retry."""

    # Statistics
    success_count: int = field(default=0, init=False, repr=False)
    fail_count: int = field(default=0, init=False, repr=False)

    def record_success(self) -> None:
        self.success_count += 1

    def record_failure(self) -> None:
        self.fail_count += 1

    def get_stats(self) -> dict[str, int]:
        return {
            "success_count": self.success_count,
            "fail_count": self.fail_count,
            "total_attempts": self.success_count + self.fail_count,
        }


def _calculate_delay(config: RetryConfig, attempt: int) -> float:
    """Calculate delay with exponential backoff and optional jitter."""
    delay = min(config.base_delay * (2**attempt), config.max_delay)
    if config.jitter:
        delay = random.uniform(0, delay)
    return delay


def retry(
    func: Callable[..., T] | None = None,
    *,
    config: RetryConfig | None = None,
    on_retry: Callable[[Exception, int, float], None] | None = None,
) -> Callable[..., T] | Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator that retries a function on transient failures.

    Usage::

        @retry
        def flaky_operation():
            ...

        @retry(config=RetryConfig(max_retries=5))
        def another_operation():
            ...
    """
    cfg = config or RetryConfig()

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(cfg.max_retries + 1):
                try:
                    result = fn(*args, **kwargs)
                    cfg.record_success()
                    return result
                except cfg.retryable_exceptions as exc:
                    last_exception = exc
                    if attempt < cfg.max_retries:
                        delay = _calculate_delay(cfg, attempt)
                        logger.warning(
                            "Retry attempt %d/%d for %s: %s (waiting %.2fs)",
                            attempt + 1,
                            cfg.max_retries,
                            fn.__name__,
                            exc,
                            delay,
                        )
                        if on_retry:
                            on_retry(exc, attempt, delay)
                        time.sleep(delay)
                    else:
                        logger.error(
                            "All %d retry attempts exhausted for %s: %s",
                            cfg.max_retries,
                            fn.__name__,
                            exc,
                        )
                        cfg.record_failure()

            raise last_exception  # type: ignore[misc]

        # Attach config for inspection
        wrapper.retry_config = cfg  # type: ignore[attr-defined]
        return wrapper

    # Support both @retry and @retry()
    if func is not None:
        return decorator(func)
    return decorator


def retry_async(
    func: Callable[..., T] | None = None,
    *,
    config: RetryConfig | None = None,
    on_retry: Callable[[Exception, int, float], None] | None = None,
) -> Callable[..., T] | Callable[[Callable[..., T]], Callable[..., T]]:
    """Async decorator that retries an async function on transient failures.

    Usage::

        @retry_async
        async def flaky_async_operation():
            ...

        @retry_async(config=RetryConfig(max_retries=5))
        async def another_async_operation():
            ...
    """
    cfg = config or RetryConfig()

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None

            for attempt in range(cfg.max_retries + 1):
                try:
                    result = await fn(*args, **kwargs)
                    cfg.record_success()
                    return result
                except cfg.retryable_exceptions as exc:
                    last_exception = exc
                    if attempt < cfg.max_retries:
                        delay = _calculate_delay(cfg, attempt)
                        logger.warning(
                            "Async retry attempt %d/%d for %s: %s (waiting %.2fs)",
                            attempt + 1,
                            cfg.max_retries,
                            fn.__name__,
                            exc,
                            delay,
                        )
                        if on_retry:
                            on_retry(exc, attempt, delay)
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            "All %d async retry attempts exhausted for %s: %s",
                            cfg.max_retries,
                            fn.__name__,
                            exc,
                        )
                        cfg.record_failure()

            raise last_exception  # type: ignore[misc]

        # Attach config for inspection
        wrapper.retry_config = cfg  # type: ignore[attr-defined]
        return wrapper

    # Support both @retry_async and @retry_async()
    if func is not None:
        return decorator(func)
    return decorator
