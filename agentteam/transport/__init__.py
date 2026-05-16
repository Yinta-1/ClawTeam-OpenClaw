"""Pluggable transport backends for message delivery."""

from __future__ import annotations

from agentteam.transport.base import Transport


def get_transport(name: str, team_name: str, **kwargs) -> Transport:
    """Factory: create a transport by name.

    Supported transports:
    - "file": FileTransport (default, local filesystem)
    - "p2p": P2PTransport (ZeroMQ + file fallback)
    - "redis": RedisTransport (Redis-backed, cross-machine)

    Args:
        name: Transport name ("file", "p2p", "redis").
        team_name: Team name for the transport.
        **kwargs: Additional arguments passed to transport constructor.

    Returns:
        Transport instance.
    """
    if name == "p2p":
        from agentteam.transport.p2p import P2PTransport

        return P2PTransport(team_name, **kwargs)
    if name == "redis":
        from agentteam.transport.redis import RedisTransport

        return RedisTransport(team_name, **kwargs)
    # Default to FileTransport
    from agentteam.transport.file import FileTransport

    return FileTransport(team_name)


__all__ = ["Transport", "get_transport"]
