# Phase 43 Project Memory Contract

## 契约目标

本契约定义外接项目可复用的项目记忆数据模型。CEK-TA 只提供通用 schema 和治理规则；外接项目自行决定是否落库、落在哪个数据库、如何接入自己的权限系统。

## MemoryItem v0.1

```json
{
  "memory_id": "mem_...",
  "project_id": "project_...",
  "memory_type": "goal | task | decision | artifact | lesson | boundary",
  "title": "string",
  "summary": "string",
  "content": "string",
  "source": {
    "source_type": "conversation | task_card | audit_report | build_log | code_diff | user_instruction | external_doc",
    "source_event_id": "string",
    "source_artifact_ref": "string",
    "source_hash": "string",
    "source_trust": "low | medium | high"
  },
  "relations": {
    "related_task_ids": [],
    "related_decision_ids": [],
    "related_artifact_ids": [],
    "supersedes": []
  },
  "lifecycle": {
    "status": "proposed | active | superseded | deprecated | rejected",
    "valid_from": "datetime",
    "valid_to": null,
    "created_at": "datetime",
    "updated_at": "datetime"
  },
  "review": {
    "review_status": "unreviewed | reviewed | approved",
    "reviewer": "human | rule | ai_assisted",
    "reviewed_at": null
  },
  "write_policy": {
    "write_origin": "human_confirmed | ai_proposed | rule_extracted | audit_imported",
    "requires_review": true,
    "auto_promote_allowed": false
  },
  "security": {
    "visibility": "private | project | team",
    "contains_private_data": false,
    "sanitized": true,
    "untrusted_input": false,
    "poisoning_risk": "low | medium | high",
    "secret_scan_status": "passed | failed | not_run",
    "allowed_agents": []
  },
  "retrieval": {
    "retrievable": true,
    "include_by_default": false,
    "top_k_scope": "project | task | agent",
    "last_used_at": null
  },
  "integrity": {
    "memory_hash": "string",
    "previous_version_id": "string | null",
    "snapshot_id": "string | null",
    "rollback_allowed": true,
    "last_integrity_check_at": "datetime | null"
  }
}
```

## 6 类 MemoryType

| memory_type | 说明 | 典型来源 |
| --- | --- | --- |
| goal | 项目目标、阶段目标、验收目标 | 用户指令、任务卡、审计结论 |
| task | 当前任务、待办、阻塞、延期计划 | 任务卡、项目管理文档、用户指令 |
| decision | 架构、技术选型、治理和边界决策 | 设计文档、审计报告、用户确认 |
| artifact | 重要交付物、报告、接口、配置和版本 | 代码差异、报告、发布记录 |
| lesson | 错误复盘、失败原因、修复方式、预防规则 | 事故记录、构建失败、审计反馈 |
| boundary | 禁止事项、权限边界、私有数据边界、调用边界 | AGENTS、契约、用户规则 |

## 不作为 MemoryItem 的内容

| 内容 | 处理方式 |
| --- | --- |
| process | 进入 append-only `memory_events`，不作为长期记忆事实 |
| future_plan | 并入 `task`，使用 `todo / blocked / deferred` 等状态 |
| error | 并入 `lesson`，记录 `error_cause / fix / prevention` |
| 普通对话 | 默认不写长期记忆，必要时进入短期 event log |
| 临时 debug | 不写长期记忆，除非形成复盘 lesson |

## 生命周期

```text
event_logged -> proposed -> reviewed -> active
active -> superseded
active -> deprecated
proposed -> rejected
deprecated -> archived
```

规则：

```text
1. AI 只能创建 proposed memory。
2. active 必须由人工、规则引擎或受控审核流程设置。
3. 不允许静默覆盖 active memory，必须通过 supersede 关系替换。
4. deprecated memory 只能作为历史参考，不得作为当前事实默认注入。
5. rejected memory 不得被检索作为建议依据。
6. auto_promote_allowed 默认 false，除非外接项目另有人工确认的规则。
```

## 推荐逻辑表

```text
memory_items
memory_events
memory_links
```

`memory_items` 是 canonical store；`memory_events` 是 append-only 审计账本；`memory_links` 记录记忆与任务、决策、产物和替代关系。

## 存储边界

```text
1. PostgreSQL JSONB 可作为 v0.1 默认 canonical memory store。
2. pgvector 只作为可选 semantic retrieval index，不是事实源。
3. 第三方 memory engine 只能作为 adapter，不替代 MemoryItem 契约。
4. CEK-TA 本仓库不创建外接项目生产表。
```
