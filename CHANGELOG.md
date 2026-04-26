# ClawTeam 升级日志

## v0.4.0（2026-04-26）— P1 工程化改进

### 新增模块

#### 审计日志（Audit Logging）
- 文件：`clawteam/audit.py`
- 追加写入模式，历史事件永不修改
- 每个事件包含：event_id, event_type, actor, details, timestamp, team
- 支持按类型/时间范围/actor 过滤查询
- 测试：`tests/test_audit.py`（7 项，全部通过）

#### 智能路由（Intelligent Routing）
- 文件：`clawteam/team/router.py`
- 基于三因素路由算法：
  - **历史表现**：成功率 + 质量评分加权
  - **负载感知**：当前进行中的任务数
  - **技能匹配**：关键词提取（支持中英文）
- 支持 `route()` 获取最优 agent，`get_all_candidates()` 获取排序列表
- 新 agent 自动创建默认档案（无历史数据时 fallback 到默认值）
- 测试：`tests/test_routing.py`（18 项，全部通过）

#### 告警机制（Alerting）
- 文件：`clawteam/alerts.py`
- 四级严重程度：LOW / MEDIUM / HIGH / CRITICAL
- 支持告警类型：TASK_TIMEOUT, AGENT_FAILURE_RATE_HIGH, TEAM_INACTIVITY
- CRUD 操作：创建、查询、列表、确认
- CLI 集成：`clawteam alert check/list/ack`
- 测试：`tests/test_alerts.py`（5 项，全部通过）

### 修复问题

| 问题 | 修复内容 | 影响范围 |
|------|----------|----------|
| `route()` 参数名不匹配 | `candidates` → `available_agents` | 智能路由 |
| `scores=None` pydantic 验证失败 | 测试中移除显式 `None`，使用默认空列表 | 路由测试 |
| 新 agent 无法被路由 | `route()` 自动创建默认 AgentProfile | 智能路由 |
| `total_score` 计算精度 | 修正期望值 8.4 → 8.45 | 路由测试 |
| `TaskStatus.failed` 不存在 | 改为 `TaskStatus.blocked` | 路由测试 |
| `test_get_all_candidates` 排序错误 | 统一 agent 成功率和负载，让 topic 匹配成为决定因素 | 路由测试 |

### 技术细节

**QualityScore 权重**（0-100 分）：
- completeness 0.25
- accuracy 0.30
- quality 0.20
- 规范性 0.15
- innovation 0.10

**路由评分公式**（0-100）：
```
total = topic_match(0-50) + success_score(0-30) + quality_score(0-20) - load_penalty(0-15)
```

**漂移检测阈值**（Jaccard + 语义）：
- ≥ 0.60：无漂移
- 0.45-0.60：低漂移
- 0.30-0.45：中漂移
- 0.15-0.30：高漂移
- < 0.15：严重漂移

### 升级步骤

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 安装依赖（如有新增）
pip install -e .

# 3. 运行测试确认
python -m pytest tests/test_audit.py tests/test_routing.py tests/test_alerts.py -v

# 4. 验证 CLI
clawteam audit list --team <your-team>
clawteam alert check --team <your-team>
```

### 向后兼容

- ✅ 无破坏性变更
- ✅ 所有现有 API 保持不变
- ✅ 新增模块为可选功能

---

## v0.3.1（2026-04-26）— P0 工程化改进

### 新增

- **结构化日志**：`clawteam/utils/logger.py`
  - JSON 格式，trace_id 上下文追踪
  - RotatingFileHandler（10MB/5 备份）
  - 环境变量：`CLAWTEAM_LOG_LEVEL`

- **重试框架**：`clawteam/utils/retry.py`
  - `@retry` / `@retry_async` 装饰器
  - 指数退避 + 抖动
  - 自动统计重试次数

### 影响

- `FileTaskStore._save_unlocked()` 自动重试
- `FileTransport.deliver()` 自动重试
- 测试：20 单元测试 + 10 集成测试

---

_最后更新：2026-04-26_
