# ClawTeam-OpenClaw P0 工程化改进计划

## 概述
针对 ClawTeam-OpenClaw 多 Agent 协作 CLI 框架的工程化短板，实施三项 P0 级改进：结构化日志系统、Peer Review 机制、自动重试策略。

## 现状分析
- **日志**: 仅 2 个模块使用 logging（workspace/manager.py, spawn/__init__.py），大部分模块无日志
- **错误处理**: 有 330 处 try/except/raise，但缺乏统一策略和重试机制
- **输出**: CLI 使用 rich console.print，但内部模块无统一输出方式
- **无日志轮转、无结构化日志、无 trace_id**
- **无 Peer Review 机制**
- **无自动重试策略**

---

## 改进项

### 1. 结构化日志系统 (Logging)
**优先级**: P0 | **负责人**: 后端工程师

**现状问题**:
- 仅 2 个模块使用 `logging.getLogger`，大部分模块无日志
- 无结构化输出（JSON 格式）
- 无日志轮转，日志文件会无限增长
- 无请求追踪 ID（trace_id），无法关联同一操作的日志
- 无 per-module 日志级别配置

**改进方案**:
- 创建 `clawteam/utils/logger.py`，实现结构化日志工具
  - `StructuredLogger` 类，支持 JSON 格式输出
  - `RotatingFileHandler` 日志轮转（10MB/文件，保留5个）
  - `trace_id` 请求追踪（通过 contextvars 实现）
  - `get_logger(name)` 工厂函数，统一日志获取
  - per-module 日志级别配置（通过 CLAWTEAM_LOG_LEVEL 环境变量）
- 在核心模块中集成日志：
  - `clawteam/team/manager.py` - 团队操作日志
  - `clawteam/team/tasks.py` - 任务操作日志
  - `clawteam/team/mailbox.py` - 消息传递日志
  - `clawteam/spawn/__init__.py` - Agent 生成日志
  - `clawteam/transport/file.py` - 传输操作日志
  - `clawteam/store/file.py` - 存储操作日志
- 更新 `clawteam/cli/commands.py` 添加日志初始化

**交付物**:
- `clawteam/utils/__init__.py` - utils 包初始化
- `clawteam/utils/logger.py` - 结构化日志工具
- 更新上述 6 个核心模块的日志调用
- 更新 CLI 命令添加日志初始化

---

### 2. Peer Review 机制
**优先级**: P0 | **负责人**: 架构师

**现状问题**:
- 无代码审查流程
- 无 review 模板和检查清单
- 无 review 记录追踪

**改进方案**:
- 创建 `clawteam/models/review.py`，实现 ReviewReport 数据模型（pydantic v2）
  - `ReviewReport` 模型：reviewer、reviewee、review_date、status、scores、comments
  - `ReviewChecklist` 模型：代码风格、类型注解、错误处理、性能、安全
  - `ReviewScore` 模型：5 维度评分（completeness、accuracy、codeQuality、adherence、innovation）
- 创建 `clawteam/review/CHECKLIST.md` - 审查检查清单
- 创建 `clawteam/review/TEMPLATE.md` - 审查报告模板
- 创建 `scripts/run_review.py` - 自动化审查脚本
  - 检查类型注解完整性
  - 检查 pydantic v2 兼容性
  - 检查错误处理覆盖
  - 生成审查报告
- 创建 `.github/workflows/review.yml` - CI 审查流程

**交付物**:
- `clawteam/models/review.py` - Review 数据模型
- `clawteam/review/CHECKLIST.md` - 审查检查清单
- `clawteam/review/TEMPLATE.md` - 审查报告模板
- `scripts/run_review.py` - 自动化审查脚本
- `.github/workflows/review.yml` - CI 审查流程

---

### 3. 自动重试策略
**优先级**: P0 | **负责人**: 后端工程师

**现状问题**:
- 无重试机制，文件操作和网络请求失败后直接抛出异常
- 无指数退避策略
- 无重试统计和监控

**改进方案**:
- 创建 `clawteam/utils/retry.py`，实现重试工具
  - `RetryConfig` 配置类（最大重试次数、退避策略、可重试异常列表）
  - `@retry` 装饰器，支持指数退避和抖动
  - `retry_async` 异步版本装饰器
  - 重试统计（成功/失败计数）
- 在核心模块中集成重试：
  - `clawteam/store/file.py` - 文件存储操作重试
  - `clawteam/transport/file.py` - 文件传输操作重试
  - `clawteam/team/tasks.py` - 任务锁操作重试
- 更新 `clawteam/config.py` 添加重试配置项

**交付物**:
- `clawteam/utils/retry.py` - 重试工具模块
- 更新 `clawteam/store/file.py` 集成重试
- 更新 `clawteam/transport/file.py` 集成重试
- 更新 `clawteam/team/tasks.py` 集成重试
- 更新 `clawteam/config.py` 添加重试配置项

---

## 执行顺序
1. **日志系统** → 2. **Peer Review** → 3. **自动重试**
每个任务完成后运行对应测试。

## 技术要求
- pydantic v2 + type hints
- 无破坏性变更（向后兼容）
- 代码风格一致（PEP 8 + ruff 格式化）
- 完成后提交 git commit

## 测试要求
- 每个改进项必须有对应的单元测试
- 测试覆盖率不低于 80%
- 集成测试验证端到端流程
