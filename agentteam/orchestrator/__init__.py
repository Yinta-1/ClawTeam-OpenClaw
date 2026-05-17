"""Orchestrator module for AgentTeam multi-agent teams.

This module provides:
- Provider selection with intelligent routing
- Automatic fallback when providers are unavailable
- Quota/limit detection and management
- Task orchestration and coordination
"""

from agentteam.orchestrator.provider_selector import (
    FallbackChain,
    ProviderInfo,
    ProviderSelector,
    ProviderStatus,
    QuotaInfo,
    SelectionResult,
)

__all__ = [
    "ProviderSelector",
    "ProviderInfo",
    "ProviderStatus",
    "QuotaInfo",
    "SelectionResult",
    "FallbackChain",
]
