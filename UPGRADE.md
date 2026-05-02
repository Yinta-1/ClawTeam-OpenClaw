# ClawTeam 升级计划 v0.5.0

> 基于 SpectrAI 架构灵感，实现真正的多 Agent 协作框架

---

## 📊 升级进度总览

| 项目 | 任务 | 状态 | 负责人 | 备注 |
|------|------|------|--------|------|
| P26 | Parent-Child 生命周期管理 | ✅ **已完成** | arch-p27 | cb52d4e |
| P27 | turn_complete 事件驱动 | 🔄 进行中 | arch-p27 | 集成到 lifecycle |
| P28 | 工具注册增强 | 🔄 进行中 | arch-p28 | registry.py 已修改 |
| P29 | 协作增强 | 🔄 进行中 | arch-p29 | collaboration/ 已创建 |
| P30-P33 | 多模态支持 | 🔄 进行中 | arch-p30-33 | specs 文档已创建 |
| P34 | Dashboard 监控面板 | 🔄 进行中 | arch-dashboard | dashboard.py 已创建 |
| P35 | 事件追踪系统 | 🔄 进行中 | arch-events | events/ 已创建 |
| P36 | 实时 SSE 推送 | 🔄 进行中 | arch-realtime | server.py 已修改 |
| P37 | 组件集成测试 | ⬜ 待开始 | arch-integrator | 未开始 |

---

## ✅ 已完成功能（v0.4.0）

### 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| **MailboxManager** | `clawteam/team/mailbox.py` | Agent 间消息传递，Transport 抽象 |
| **P2P Transport** | `clawteam/transport/p2p.py` | ZeroMQ PUSH/PULL + 文件回退 |
| **RoleStore** | `clawteam/team/roles.py` | 动态角色分配（developer/reviewer/tester/architect/coordinator） |
| **BaseTaskStore** | `clawteam/store/base.py` | 任务存储抽象，文件锁并发控制 |
| **WebSocketManager** | `clawteam/board/websocket.py` | WebSocket 连接管理 |
| **Board Server** | `clawteam/board/server.py` | HTTP API + SSE 实时推送 |
| **Transport 抽象** | `clawteam/transport/base.py` | File/P2P/Redis/ClaimedMessage |
| **生命周期管理** | `clawteam/team/lifecycle.py` | Agent 生命周期状态机 |
| **审计日志** | `clawteam/audit/` | 操作审计追溯 |
| **告警系统** | `clawteam/alerts/` | 四级告警机制 |
| **记忆系统** | `clawteam/memory/` | 分层记忆存储 |
| **技能引擎** | `clawteam/skill/` | Skill 自动创建和执行 |

### CLI 命令

```bash
# 团队管理
clawteam team create <team>           # 创建团队
clawteam team status <team>           # 团队状态
clawteam team members <team>          # 列出成员

# 消息传递
clawteam inbox send <team> <to> <msg> # 发送消息
clawteam inbox peek <team>           # 查看消息
clawteam inbox receive <team>        # 接收消息

# 任务管理
clawteam task create <team> <subject> # 创建任务
clawteam task list <team>            # 列出任务
clawteam task update <team> <id> --status completed  # 更新状态

# 角色管理
clawteam role assign <team> <agent> <role>  # 分配角色

# Agent Spawn
clawteam spawn <backend> --team <team> --agent-name <name>  # 生成 Agent

# 生命周期
clawteam lifecycle on-exit --team <team> --agent <name>  # 退出时清理
```

---

## 🔄 进行中功能（v0.5.0）

### P26: Parent-Child 生命周期管理 ✅

**commit**: `cb52d4e feat(lifecycle): implement Parent-Child lifecycle management (P26)`

新增功能：
- `ParentChildRegistry` - 追踪父子关系
- `parentToAgents: Map[parentSessionId, Set[agentId]]`
- `cleanupChildAgents(sessionId)` - 级联终止
- 5 个新 CLI 命令：
  - `terminate-children`
  - `terminate-tree`
  - `list-children`
  - `show-parent`
  - `register-child`
- `--parent` flag for spawn command

### P28: 工具注册增强 🔄

**修改文件**: `clawteam/tools/registry.py`

目标：
- 增强工具注册表
- 支持动态工具发现
- MCP 工具集成

### P29: 协作增强 🔄

**新增目录**: `clawteam/collaboration/`

目标功能：
- Activity Feed（活动流）
- Presence（在线状态）
- Mentions（@提及）
- Context Board（上下文面板）

### P30-P33: 多模态支持 🔄

**文档**: `docs/superpowers/specs/P30-P33-multimodal-support-design.md`

目标：
- 音频输入/输出
- 视觉理解
- 文件处理
- 截图/屏幕捕获

### P34: Dashboard 监控面板 🔄

**新增文件**:
- `clawteam/api/monitor.py`
- `clawteam/board/dashboard.py`

目标：
- 实时会话监控
- Token 使用统计
- 风险评估

### P35: 事件追踪系统 🔄

**新增目录**: `clawteam/events/`

目标：
- 40+ 事件类型
- SQLite 持久化
- 事件查询 API

### P36: 实时 SSE 推送 🔄

**修改文件**:
- `clawteam/board/server.py`
- `clawteam/board/static/index.html`

目标：
- Server-Sent Events
- 实时日志推送
- 前端 Dashboard 集成

---

## 📋 待开始功能

### P37: 组件集成测试

**负责人**: arch-integrator

目标：
- 验证 P26-P36 各组件能协同工作
- 端到端测试
- 性能基准测试

### 新增功能规划（基于 SpectrAI Agent Teams）

| 功能 | 描述 | 优先级 |
|------|------|--------|
| **SharedTaskList DB** | SQLite 持久化任务队列（替代 JSON 文件） | P1 |
| **TeamBus MCP 工具** | team_message_role / team_broadcast 等 5 个 MCP 工具 | P1 |
| **团队数据库表** | teams / roles / instances / members / tasks / messages 6 张表 | P2 |
| **TaskKanban 可视化** | 看板视图展示任务流转 | P2 |
| **TeamMessageFlow** | 对话流展示成员通信 | P3 |

---

## 🏗️ 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    ClawTeam Framework                        │
├─────────────────────────────────────────────────────────────┤
│  CLI Layer                                                   │
│  ├── team create/list/status                                 │
│  ├── inbox send/peek/receive                                 │
│  ├── task create/list/update                                │
│  ├── role assign/list                                       │
│  └── lifecycle on-exit/terminate-children                   │
├─────────────────────────────────────────────────────────────┤
│  Core Layer                                                  │
│  ├── MailboxManager (Transport abstraction)                   │
│  │   ├── FileTransport (default)                            │
│  │   ├── P2PTransport (ZeroMQ PUSH/PULL)                   │
│  │   └── RedisTransport (optional)                          │
│  ├── RoleStore (dynamic role assignment)                    │
│  ├── BaseTaskStore (task storage)                          │
│  └── LifecycleManager (state machine)                       │
├─────────────────────────────────────────────────────────────┤
│  Agent Layer                                                 │
│  ├── AgentManager (spawn/monitor/terminate)                 │
│  ├── ParentChildRegistry (hierarchical lifecycle)            │
│  └── AgentRegistry (agent registration)                     │
├─────────────────────────────────────────────────────────────┤
│  Integration Layer                                           │
│  ├── OpenClaw SDK Backend (sessions.create/send)            │
│  ├── MCP Tools (team operations)                           │
│  └── WebSocket Manager (real-time updates)                  │
├─────────────────────────────────────────────────────────────┤
│  Storage Layer                                               │
│  ├── SQLite Database (optional)                             │
│  ├── File System (JSON tasks/messages)                     │
│  └── LanceDB (vector memory)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 相关文档

- [README.md](README.md) - 项目概述
- [RELEASE_NOTES.md](RELEASE_NOTES.md) - 发布说明
- [CHANGELOG.md](CHANGELOG.md) - 变更日志
- [CLAWTEAM_API.md](docs/CLAWTEAM_API.md) - API 文档
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构设计

---

## 🤝 贡献者

- **arch-p27**: Parent-Child 生命周期管理
- **arch-p28**: 工具注册增强
- **arch-p29**: 协作增强
- **arch-p30-33**: 多模态支持
- **arch-dashboard**: Dashboard 监控面板
- **arch-events**: 事件追踪系统
- **arch-realtime**: 实时 SSE 推送
- **arch-integrator**: 组件集成测试

---

_Last updated: 2026-05-03_
