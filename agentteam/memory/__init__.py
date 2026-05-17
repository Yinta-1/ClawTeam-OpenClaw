"""AgentTeam 记忆模块 - 提供记忆存储与检索能力。

借鉴 Hermes Agent 的 MemoryProvider 架构。
核心概念：
- 记忆 Provider 抽象基类（MemoryProvider）
- FTS5 全文检索提供者（可选）
- L1-L4 分层记忆系统
- 记忆同步与检索接口
"""

from agentteam.memory.fts5_provider import FTS5MemoryProvider
from agentteam.memory.layered import (
    L1WorkingMemory,
    L2SessionMemory,
    L3CrossSessionMemory,
    L4KnowledgeBase,
    LayeredMemoryProvider,
    MemoryEntry,
)
from agentteam.memory.provider import MemoryProvider

__all__ = [
    "MemoryProvider",
    "FTS5MemoryProvider",
    "LayeredMemoryProvider",
    "L1WorkingMemory",
    "L2SessionMemory",
    "L3CrossSessionMemory",
    "L4KnowledgeBase",
    "MemoryEntry",
]
