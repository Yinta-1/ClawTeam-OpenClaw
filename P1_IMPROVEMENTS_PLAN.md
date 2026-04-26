# ClawTeam P1 Engineering Improvements — Implementation Plan

> **交给 spai 执行，完成后由楚灵审核。**
> 每个任务包含：上下文、实现要点、文件位置、验收标准。
> 
> **重要**：spai 工作目录是 `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw`
> 所有文件路径都是相对于这个目录的绝对路径。

---

## 任务 1：智能任务路由（Intelligent Task Routing）

### 背景
当前任务分配是手动指定 `--owner`。智能路由根据 Agent 历史表现、负载、技能匹配自动分配任务。

### 实现思路
1. **Agent 能力档案**：记录每个 Agent 的历史任务类型、成功率、平均评分
2. **负载感知**：记录每个 Agent 当前正在执行的任务数
3. **匹配算法**：基于任务主题关键词 + Agent 能力档案 + 负载，计算最佳匹配
4. **CLI 命令**：`clawteam task route <team> --subject "xxx" --description "xxx"` 自动推荐最佳 Agent

### 需要新建的文件

#### 1. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\team\router.py` — 路由引擎

```python
"""Intelligent task routing for ClawTeam multi-agent teams.

Routes tasks to the best-matched agent based on:
- Historical performance (success rate, quality scores)
- Current workload (number of in-progress tasks)
- Skill/topic matching (keyword-based)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from clawteam.fileutil import atomic_write_text
from clawteam.paths import ensure_within_root, validate_identifier
from clawteam.team.models import TaskItem, TaskStatus, get_data_dir


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _router_root(team_name: str) -> Path:
    d = ensure_within_root(get_data_dir() / "router", validate_identifier(team_name, "team name"))
    d.mkdir(parents=True, exist_ok=True)
    return d


# Simple keyword extraction for topic matching
_TOPIC_KEYWORDS = re.compile(r'[a-zA-Z]{3,}|[\u4e00-\u9fff]+')


def _extract_keywords(text: str) -> set[str]:
    """Extract keywords from text for topic matching."""
    return set(_TOPIC_KEYWORDS.findall(text.lower()))


@dataclass
class AgentProfile:
    """Profile of an agent's capabilities and performance."""
    
    name: str
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_score: float = 0.0
    score_count: int = 0
    topics: dict[str, int] = field(default_factory=dict)  # keyword -> count
    current_load: int = 0  # number of in-progress tasks
    
    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.5  # default for new agents
        return self.completed_tasks / self.total_tasks
    
    @property
    def avg_score(self) -> float:
        if self.score_count == 0:
            return 5.0  # default for new agents
        return self.total_score / self.score_count
    
    def update_from_task(self, task: TaskItem) -> None:
        """Update profile from a completed task."""
        if task.owner != self.name:
            return
        
        self.total_tasks += 1
        if task.status == TaskStatus.completed:
            self.completed_tasks += 1
        else:
            self.failed_tasks += 1
        
        # Extract topics from subject and description
        keywords = _extract_keywords(task.subject + " " + task.description)
        for kw in keywords:
            self.topics[kw] = self.topics.get(kw, 0) + 1
        
        # Update scores if available
        if task.scores:
            for score in task.scores:
                self.total_score += score.total
                self.score_count += 1


@dataclass
class RouteCandidate:
    """A candidate agent for task assignment."""
    
    name: str
    match_score: float  # 0-100, higher is better
    success_rate: float
    avg_score: float
    current_load: int
    matching_topics: list[str] = field(default_factory=list)


class TaskRouter:
    """Intelligent task router based on agent profiles and task characteristics."""
    
    def __init__(self, team_name: str):
        self.team_name = team_name
        self._profiles: dict[str, AgentProfile] = {}
    
    def load_profiles(self) -> None:
        """Load agent profiles from disk."""
        path = _router_root(self.team_name) / "profiles.json"
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            for name, profile_data in data.items():
                self._profiles[name] = AgentProfile(**profile_data)
    
    def save_profiles(self) -> None:
        """Save agent profiles to disk."""
        path = _router_root(self.team_name) / "profiles.json"
        data = {name: {
            "name": p.name,
            "total_tasks": p.total_tasks,
            "completed_tasks": p.completed_tasks,
            "failed_tasks": p.failed_tasks,
            "total_score": p.total_score,
            "score_count": p.score_count,
            "topics": p.topics,
            "current_load": p.current_load,
        } for name, p in self._profiles.items()}
        atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2))
    
    def update_profile(self, task: TaskItem) -> None:
        """Update profile for an agent based on a completed task."""
        if not task.owner:
            return
        
        if task.owner not in self._profiles:
            self._profiles[task.owner] = AgentProfile(name=task.owner)
        
        self._profiles[task.owner].update_from_task(task)
        self.save_profiles()
    
    def update_load(self, team_name: str) -> None:
        """Update current load for all agents from task store."""
        from clawteam.store.file import FileTaskStore
        
        store = FileTaskStore(team_name)
        in_progress = store.list_tasks(status=TaskStatus.in_progress)
        
        # Reset all loads
        for profile in self._profiles.values():
            profile.current_load = 0
        
        # Count in-progress tasks per agent
        for task in in_progress:
            if task.owner and task.owner in self._profiles:
                self._profiles[task.owner].current_load += 1
        
        self.save_profiles()
    
    def route(self, subject: str, description: str, candidates: list[str] | None = None) -> RouteCandidate | None:
        """Find the best agent for a task.
        
        Args:
            subject: Task subject
            description: Task description
            candidates: Optional list of candidate agent names. If None, use all known agents.
        
        Returns:
            RouteCandidate with match score, or None if no candidates available.
        """
        task_keywords = _extract_keywords(subject + " " + description)
        if not task_keywords:
            task_keywords = {"general"}
        
        if candidates:
            profiles = {n: p for n, p in self._profiles.items() if n in candidates}
        else:
            profiles = self._profiles
        
        if not profiles:
            return None
        
        candidates_list = []
        for name, profile in profiles.items():
            # Calculate topic match score (0-50)
            matching_topics = task_keywords & set(profile.topics.keys())
            topic_match = len(matching_topics) / max(len(task_keywords), 1) * 50
            
            # Calculate success rate score (0-30)
            success_score = profile.success_rate * 30
            
            # Calculate quality score (0-20)
            quality_score = min(profile.avg_score / 10, 1.0) * 20
            
            # Load penalty (reduce score for busy agents)
            load_penalty = min(profile.current_load * 5, 15)
            
            total_score = topic_match + success_score + quality_score - load_penalty
            
            candidates_list.append(RouteCandidate(
                name=name,
                match_score=round(total_score, 2),
                success_rate=profile.success_rate,
                avg_score=profile.avg_score,
                current_load=profile.current_load,
                matching_topics=list(matching_topics),
            ))
        
        # Sort by match score descending
        candidates_list.sort(key=lambda c: c.match_score, reverse=True)
        return candidates_list[0] if candidates_list else None
    
    def get_all_candidates(self, subject: str, description: str, candidates: list[str] | None = None) -> list[RouteCandidate]:
        """Get all candidates sorted by match score."""
        task_keywords = _extract_keywords(subject + " " + description)
        if not task_keywords:
            task_keywords = {"general"}
        
        if candidates:
            profiles = {n: p for n, p in self._profiles.items() if n in candidates}
        else:
            profiles = self._profiles
        
        result = []
        for name, profile in profiles.items():
            matching_topics = task_keywords & set(profile.topics.keys())
            topic_match = len(matching_topics) / max(len(task_keywords), 1) * 50
            success_score = profile.success_rate * 30
            quality_score = min(profile.avg_score / 10, 1.0) * 20
            load_penalty = min(profile.current_load * 5, 15)
            total_score = topic_match + success_score + quality_score - load_penalty
            
            result.append(RouteCandidate(
                name=name,
                match_score=round(total_score, 2),
                success_rate=profile.success_rate,
                avg_score=profile.avg_score,
                current_load=profile.current_load,
                matching_topics=list(matching_topics),
            ))
        
        result.sort(key=lambda c: c.match_score, reverse=True)
        return result


# Convenience function
def get_router(team_name: str) -> TaskRouter:
    """Get a TaskRouter instance with profiles loaded."""
    router = TaskRouter(team_name)
    router.load_profiles()
    return router
```

#### 2. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\cli\commands.py` — 添加路由命令

在 `task_app` 下添加：

```python
@task_app.command("route")
def task_route(
    team: str = typer.Argument(...),
    subject: str = typer.Option(..., "--subject", "-s"),
    description: str = typer.Option("", "--description", "-d"),
    candidates: str = typer.Option(None, "--candidates", "-c", help="Comma-separated list of agent names"),
):
    """Find the best agent for a task using intelligent routing."""
    from clawteam.team.router import get_router
    
    router = get_router(team)
    router.update_load(team)
    
    cand_list = [c.strip() for c in candidates.split(",")] if candidates else None
    
    # Get all candidates
    all_candidates = router.get_all_candidates(subject, description, cand_list)
    
    if not all_candidates:
        console.print("[yellow]No agents available for routing.[/yellow]")
        return
    
    best = all_candidates[0]
    
    def _human(_data):
        console.print(f"[bold]Task Route — '{subject}'[/bold]")
        console.print(f"  [green]Recommended: {best.name}[/green] (score: {best.match_score})")
        console.print(f"  Success rate: {best.success_rate:.0%}  Avg score: {best.avg_score:.1f}/10  Load: {best.current_load}")
        if best.matching_topics:
            console.print(f"  Matching topics: {', '.join(best.matching_topics[:5])}")
        
        if len(all_candidates) > 1:
            console.print()
            console.print("[dim]Other candidates:[/dim]")
            for c in all_candidates[1:]:
                console.print(f"  {c.name}: score={c.match_score} (success={c.success_rate:.0%}, load={c.current_load})")
    
    _output({
        "best": best.__dict__,
        "all_candidates": [c.__dict__ for c in all_candidates],
    }, _human)
```

#### 3. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\store\file.py` — 集成路由更新

在 `update()` 方法中，任务状态变为 `completed` 时自动更新路由档案：

```python
# 在 update() 方法中，状态变更成功后添加：
if old_status != TaskStatus.completed and task.status == TaskStatus.completed:
    try:
        from clawteam.team.router import get_router
        router = get_router(self.team_name)
        router.update_profile(task)
    except Exception:
        pass  # Don't fail task completion if routing update fails
```

### 验收标准
- [ ] `TaskRouter` 类创建并可用
- [ ] `clawteam task route` 命令可用
- [ ] 任务完成时自动更新 Agent 档案
- [ ] 路由推荐基于历史表现 + 负载 + 技能匹配
- [ ] 测试文件 `tests/test_router.py` 通过（至少 15 项测试）

---

## 任务 2：审计日志（Audit Logging）

### 背景
当前事件日志（`evt-*.json`）格式不统一，缺少安全审计所需的完整操作记录。审计日志记录所有关键操作：谁在什么时间做了什么。

### 实现思路
1. 统一审计日志格式：`{data_dir}/audit/{team}/audit-{timestamp}-{id}.json`
2. 记录所有关键操作：任务创建/完成、Agent 生成/退出、消息发送、配置变更
3. 支持按操作类型/Agent/时间查询
4. 不可篡改（追加写入，不修改历史）

### 需要新建的文件

#### 1. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\team\audit.py` — 审计日志模块

```python
"""Audit logging for ClawTeam multi-agent teams.

Records all critical operations with immutable, append-only logs.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from clawteam.fileutil import atomic_write_text
from clawteam.paths import ensure_within_root, validate_identifier
from clawteam.team.models import get_data_dir


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _audit_root(team_name: str) -> Path:
    d = ensure_within_root(get_data_dir() / "audit", validate_identifier(team_name, "team name"))
    d.mkdir(parents=True, exist_ok=True)
    return d


class AuditAction(str, Enum):
    """Types of auditable actions."""
    task_created = "task.created"
    task_updated = "task.updated"
    task_completed = "task.completed"
    task_deleted = "task.deleted"
    agent_spawned = "agent.spawned"
    agent_exited = "agent.exited"
    agent_shutdown = "agent.shutdown"
    message_sent = "message.sent"
    message_received = "message.received"
    config_changed = "config.changed"
    review_submitted = "review.submitted"
    drift_detected = "drift.detected"
    cost_reported = "cost.reported"
    snapshot_created = "snapshot.created"
    snapshot_restored = "snapshot.restored"


class AuditEntry(BaseModel):
    """A single audit log entry."""
    model_config = {"populate_by_name": True}
    
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    timestamp: str = Field(default_factory=_now_iso)
    team: str = ""
    actor: str = ""  # who performed the action (agent name or "system")
    action: AuditAction = Field(default=AuditAction.task_created, alias="action")
    target: str = ""  # what was affected (task id, agent name, etc.)
    details: dict[str, Any] = Field(default_factory=dict)
    result: str = "success"  # success/failure


def write_audit(
    team: str,
    action: AuditAction,
    actor: str,
    target: str,
    details: dict[str, Any] | None = None,
    result: str = "success",
) -> AuditEntry:
    """Write an audit log entry. Append-only, never modifies existing entries."""
    entry = AuditEntry(
        team=team,
        actor=actor,
        action=action,
        target=target,
        details=details or {},
        result=result,
    )
    
    path = _audit_root(team) / f"audit-{entry.timestamp.replace(':', '-').replace('+', 'p')}-{entry.id}.json"
    atomic_write_text(path, entry.model_dump_json(indent=2, by_alias=True))
    
    return entry


def query_audit(
    team: str,
    action: AuditAction | None = None,
    actor: str = "",
    target: str = "",
    limit: int = 50,
) -> list[AuditEntry]:
    """Query audit log entries with filters."""
    root = _audit_root(team)
    entries = []
    for f in sorted(root.glob("audit-*.json"), reverse=True)[:limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            entry = AuditEntry.model_validate(data)
            if action and entry.action != action:
                continue
            if actor and entry.actor != actor:
                continue
            if target and entry.target != target:
                continue
            entries.append(entry)
        except Exception:
            continue
    return entries


def query_audit_range(
    team: str,
    since: str = "",
    until: str = "",
    action: AuditAction | None = None,
    limit: int = 100,
) -> list[AuditEntry]:
    """Query audit log entries within a time range."""
    root = _audit_root(team)
    entries = []
    for f in sorted(root.glob("audit-*.json"), reverse=True):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            entry = AuditEntry.model_validate(data)
            
            # Time range filter
            if since and entry.timestamp < since:
                continue
            if until and entry.timestamp > until:
                continue
            
            # Action filter
            if action and entry.action != action:
                continue
            
            entries.append(entry)
            if len(entries) >= limit:
                break
        except Exception:
            continue
    return entries
```

#### 2. 集成到现有操作

在以下位置添加审计日志调用：

| 位置 | 审计操作 | 内容 |
|------|----------|------|
| `store/file.py` `create()` | `task.created` | 任务创建 |
| `store/file.py` `update()` | `task.updated` | 任务状态变更 |
| `store/file.py` `update()` completed | `task.completed` | 任务完成 |
| `mailbox.py` `send()` | `message.sent` | 消息发送 |
| `mailbox.py` `receive()` | `message.received` | 消息接收 |
| `spawn/*.py` `spawn()` | `agent.spawned` | Agent 生成 |
| `team/lifecycle.py` `on-exit` | `agent.exited` | Agent 退出 |
| `team/lifecycle.py` `request-shutdown` | `agent.shutdown` | 关机请求 |
| `costs.py` `report()` | `cost.reported` | 成本上报 |
| `drift.py` `detect_drift()` | `drift.detected` | 漂移检测 |
| `team/snapshot.py` `create()` | `snapshot.created` | 快照创建 |
| `team/snapshot.py` `restore()` | `snapshot.restored` | 快照恢复 |
| `cli/commands.py` `review submit` | `review.submitted` | 评审提交 |

#### 3. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\cli\commands.py` — 添加审计查询命令

在 `app` 下添加新的 typer 子应用：

```python
audit_app = typer.Typer(help="Audit log — query immutable operation history")
app.add_typer(audit_app, name="audit")


@audit_app.command("query")
def audit_query(
    team: str = typer.Argument(...),
    action: str = typer.Option(None, "--action", "-a", help="Filter by action type"),
    actor: str = typer.Option(None, "--actor", "-u", help="Filter by actor (agent name)"),
    target: str = typer.Option(None, "--target", "-t", help="Filter by target (task id, agent name)"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max entries to show"),
):
    """Query audit logs for a team."""
    from clawteam.team.audit import query_audit, AuditAction
    
    act = AuditAction(action) if action else None
    entries = query_audit(team, action=act, actor=actor, target=target, limit=limit)
    
    def _human(_data):
        if not entries:
            console.print("[dim]No audit entries found.[/dim]")
            return
        
        from rich.table import Table
        table = Table(title=f"Audit Log — Team '{team}'")
        table.add_column("Time", style="dim")
        table.add_column("Action", style="cyan")
        table.add_column("Actor", style="blue")
        table.add_column("Target", style="magenta")
        table.add_column("Result", justify="center")
        
        for e in entries:
            result_icon = "[green]*[/green]" if e.result == "success" else "[red]![/red]"
            table.add_row(
                e.timestamp[:19],
                e.action.value,
                e.actor or "-",
                e.target[:30],
                result_icon,
            )
        console.print(table)
        console.print(f"\n[dim]{len(entries)} entry(ies)[/dim]")
    
    _output([e.model_dump(by_alias=True) for e in entries], _human)
```

### 验收标准
- [ ] `audit.py` 模块创建并可用
- [ ] 所有关键操作自动记录审计日志
- [ ] 支持按操作类型/Actor/目标查询
- [ ] CLI `clawteam audit query` 命令可用
- [ ] 日志追加写入，不修改历史
- [ ] 测试文件 `tests/test_audit.py` 通过（至少 10 项测试）

---

## 任务 3：告警机制增强（Enhanced Alerting）

### 背景
当前告警仅支持漂移检测。需要增强为：任务超时、Agent 异常、质量退化等自动告警。

### 实现思路
1. **告警规则**：可配置的告警条件（超时、失败率、质量下降）
2. **告警通知**：通知 Leader 或指定 Agent
3. **告警历史**：记录所有告警，支持查询和确认

### 需要新建的文件

#### 1. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\team\alerts.py` — 告警引擎

```python
"""Alert system for ClawTeam multi-agent teams.

Monitors team health and triggers alerts for:
- Task timeout (in_progress too long)
- Agent failure rate (too many failures)
- Quality degradation (scores dropping)
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from clawteam.fileutil import atomic_write_text
from clawteam.paths import ensure_within_root, validate_identifier
from clawteam.team.models import TaskItem, TaskStatus, get_data_dir


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _alerts_root(team_name: str) -> Path:
    d = ensure_within_root(get_data_dir() / "alerts", validate_identifier(team_name, "team name"))
    d.mkdir(parents=True, exist_ok=True)
    return d


class AlertSeverity(str, Enum):
    """Alert severity levels."""
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class AlertType(str, Enum):
    """Types of alerts."""
    task_timeout = "task.timeout"
    agent_failure = "agent.failure"
    quality_drop = "quality.drop"
    budget_exceeded = "budget.exceeded"
    drift_critical = "drift.critical"
    zombie_agent = "agent.zombie"


class AlertEntry(BaseModel):
    """A single alert entry."""
    model_config = {"populate_by_name": True}
    
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    timestamp: str = Field(default_factory=_now_iso)
    team: str = ""
    type: AlertType = AlertType.task_timeout
    severity: AlertSeverity = AlertSeverity.warning
    source: str = ""  # what triggered the alert (task id, agent name)
    message: str = ""
    details: dict[str, Any] = Field(default_factory=dict)
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_at: str = ""


def write_alert(
    team: str,
    alert_type: AlertType,
    severity: AlertSeverity,
    source: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> AlertEntry:
    """Write an alert entry."""
    entry = AlertEntry(
        team=team,
        type=alert_type,
        severity=severity,
        source=source,
        message=message,
        details=details or {},
    )
    
    path = _alerts_root(team) / f"alert-{entry.timestamp.replace(':', '-').replace('+', 'p')}-{entry.id}.json"
    atomic_write_text(path, entry.model_dump_json(indent=2, by_alias=True))
    
    return entry


def query_alerts(
    team: str,
    severity: AlertSeverity | None = None,
    alert_type: AlertType | None = None,
    unacked: bool = False,
    limit: int = 50,
) -> list[AlertEntry]:
    """Query alert entries with filters."""
    root = _alerts_root(team)
    entries = []
    for f in sorted(root.glob("alert-*.json"), reverse=True)[:limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            entry = AlertEntry.model_validate(data)
            if severity and entry.severity != severity:
                continue
            if alert_type and entry.type != alert_type:
                continue
            if unacked and entry.acknowledged:
                continue
            entries.append(entry)
        except Exception:
            continue
    return entries


def check_task_timeouts(team: str, timeout_minutes: int = 60) -> list[AlertEntry]:
    """Check for tasks that have been in_progress too long."""
    from clawteam.store.file import FileTaskStore
    
    store = FileTaskStore(team)
    tasks = store.list_tasks(status=TaskStatus.in_progress)
    
    now = datetime.now(timezone.utc)
    alerts = []
    
    for task in tasks:
        if not task.started_at:
            continue
        
        try:
            started = datetime.fromisoformat(task.started_at)
            if started.tzinfo is None:
                started = started.replace(tzinfo=timezone.utc)
            
            elapsed = (now - started).total_seconds() / 60
            if elapsed > timeout_minutes:
                severity = AlertSeverity.warning if elapsed < timeout_minutes * 2 else AlertSeverity.error
                alert = write_alert(
                    team=team,
                    alert_type=AlertType.task_timeout,
                    severity=severity,
                    source=task.id,
                    message=f"Task '{task.subject}' has been in progress for {elapsed:.0f} minutes (threshold: {timeout_minutes})",
                    details={"elapsed_minutes": elapsed, "threshold_minutes": timeout_minutes},
                )
                alerts.append(alert)
        except (ValueError, TypeError):
            continue
    
    return alerts


def check_agent_failures(team: str, failure_threshold: int = 3) -> list[AlertEntry]:
    """Check for agents with too many consecutive failures."""
    from clawteam.store.file import FileTaskStore
    
    store = FileTaskStore(team)
    tasks = store.list_tasks()
    
    # Count failures per agent
    failures: dict[str, int] = {}
    for task in tasks:
        if task.status == "blocked" and task.owner:  # blocked often means failure
            failures[task.owner] = failures.get(task.owner, 0) + 1
    
    alerts = []
    for agent, count in failures.items():
        if count >= failure_threshold:
            alert = write_alert(
                team=team,
                alert_type=AlertType.agent_failure,
                severity=AlertSeverity.error,
                source=agent,
                message=f"Agent '{agent}' has {count} blocked tasks (threshold: {failure_threshold})",
                details={"failure_count": count, "threshold": failure_threshold},
            )
            alerts.append(alert)
    
    return alerts


def run_health_checks(team: str) -> list[AlertEntry]:
    """Run all health checks and return any alerts triggered."""
    alerts = []
    alerts.extend(check_task_timeouts(team))
    alerts.extend(check_agent_failures(team))
    return alerts
```

#### 2. `C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw\clawteam\cli\commands.py` — 添加告警命令

```python
alert_app = typer.Typer(help="Alert system — monitor team health")
app.add_typer(alert_app, name="alert")


@alert_app.command("check")
def alert_check(
    team: str = typer.Argument(...),
    timeout_minutes: int = typer.Option(60, "--timeout", "-t", help="Task timeout threshold in minutes"),
):
    """Run health checks and trigger alerts."""
    from clawteam.team.alerts import run_health_checks
    
    alerts = run_health_checks(team)
    
    def _human(_data):
        if not alerts:
            console.print("[green]* All health checks passed.[/green]")
        else:
            console.print(f"[yellow]{len(alerts)} alert(s) triggered:[/yellow]")
            for a in alerts:
                severity_icon = {"info": "[dim]i[/dim]", "warning": "[yellow]![/yellow]", "error": "[red]!![/red]", "critical": "[red bold]!!![/red bold]"}.get(a.severity.value, "!")
                console.print(f"  {severity_icon} [{a.severity.value}] {a.message}")
    
    _output([a.model_dump(by_alias=True) for a in alerts], _human)


@alert_app.command("list")
def alert_list(
    team: str = typer.Argument(...),
    severity: str = typer.Option(None, "--severity", "-s", help="Filter by severity"),
    unacked: bool = typer.Option(False, "--unacked", "-u", help="Show only unacknowledged alerts"),
    limit: int = typer.Option(50, "--limit", "-n"),
):
    """List all alerts for a team."""
    from clawteam.team.alerts import query_alerts, AlertSeverity
    
    sev = AlertSeverity(severity) if severity else None
    alerts = query_alerts(team, severity=sev, unacked=unacked, limit=limit)
    
    def _human(_data):
        if not alerts:
            console.print("[dim]No alerts found.[/dim]")
            return
        
        from rich.table import Table
        table = Table(title=f"Alerts — Team '{team}'")
        table.add_column("Time", style="dim")
        table.add_column("Type", style="cyan")
        table.add_column("Severity")
        table.add_column("Source", style="magenta")
        table.add_column("Message")
        table.add_column("Ack", justify="center")
        
        for a in alerts:
            ack_icon = "*" if a.acknowledged else "-"
            severity_icon = {"info": "[dim]i[/dim]", "warning": "[yellow]![/yellow]", "error": "[red]!![/red]", "critical": "[red bold]!!![/red bold]"}.get(a.severity.value, "!")
            table.add_row(
                a.timestamp[:19],
                a.type.value,
                f"{severity_icon} {a.severity.value}",
                a.source[:20],
                a.message[:40],
                ack_icon,
            )
        console.print(table)
        console.print(f"\n[dim]{len(alerts)} alert(s)[/dim]")
    
    _output([a.model_dump(by_alias=True) for a in alerts], _human)


@alert_app.command("ack")
def alert_ack(
    team: str = typer.Argument(...),
    alert_id: str = typer.Argument(...),
    by: str = typer.Option("leader", "--by", "-b", help="Who is acknowledging"),
):
    """Acknowledge an alert."""
    from clawteam.team.alerts import query_alerts, write_alert
    
    alerts = query_alerts(team, limit=200)
    target = None
    for a in alerts:
        if a.id == alert_id:
            target = a
            break
    
    if not target:
        console.print(f"[red]Alert '{alert_id}' not found.[/red]")
        raise typer.Exit(1)
    
    # Write a new entry with acknowledged flag
    # (In production, you'd update the existing file, but for append-only, we write a new ack entry)
    target.acknowledged = True
    target.acknowledged_by = by
    target.acknowledged_at = _now_iso()
    
    # Update the original file
    from clawteam.paths import ensure_within_root, validate_identifier
    from clawteam.team.models import get_data_dir
    from clawteam.fileutil import atomic_write_text
    
    root = ensure_within_root(get_data_dir() / "alerts", validate_identifier(team, "team name"))
    for f in root.glob(f"alert-*-{alert_id}.json"):
        atomic_write_text(f, target.model_dump_json(indent=2, by_alias=True))
        break
    
    def _human(_data):
        console.print(f"[green]* Acknowledged alert '{alert_id}' by {by}[/green]")
    
    _output({"alert_id": alert_id, "acknowledged": True, "by": by}, _human)
```

### 验收标准
- [ ] `alerts.py` 模块创建并可用
- [ ] 任务超时自动告警（可配置阈值）
- [ ] Agent 失败率告警
- [ ] CLI `clawteam alert check/list/ack` 命令可用
- [ ] 测试文件 `tests/test_alerts.py` 通过（至少 10 项测试）

---

## 执行顺序建议

1. **先做任务 2（审计日志）** — 基础能力，其他任务可复用
2. **再做任务 1（智能路由）** — 需要审计日志记录路由决策
3. **最后做任务 3（告警机制）** — 独立模块，最后集成

每个任务完成后运行测试：
```bash
cd C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw
C:\Users\31683\miniconda3\python.exe -m pytest tests/test_<task_name>.py -v
```

---

## 审核清单（楚灵用）

完成后我会检查：
- [ ] 所有测试通过
- [ ] 代码风格一致（pydantic v2 + type hints）
- [ ] CLI 命令可用且输出正确
- [ ] 审计日志追加写入，不修改历史
- [ ] 路由算法合理（历史表现 + 负载 + 技能匹配）
- [ ] 告警可配置（超时阈值、失败率阈值）
- [ ] 无破坏性变更（向后兼容）
- [ ] 文档更新（内联注释 + README 如有变更）

---

_计划创建时间：2026-04-26 20:08 GMT+8_
_执行者：spai_
_审核者：楚灵_
_工作目录：C:\Users\31683\.openclaw\workspace\ClawTeam-OpenClaw_
