# Phase 43 Project Memory MCP/API Contract

## 契约目标

定义外接项目 Project Memory MCP/API 的最小能力。默认只读，写入必须受控；任何写入都要产生审计事件。

## 通用输入字段

```text
project_id
agent_id
task_id
trace_id
visibility_scope
request_reason
```

## 通用输出字段

```text
status
memory_items
blocked_items
warnings
source_refs
audit_event_id
error
```

## Tool: search_memory

用途：按项目、任务、类型和可见性检索可用记忆。

输入：

```text
project_id
query
memory_type
visibility_scope
status
top_k
token_budget
include_deprecated=false
```

输出：

```text
memory_items
retrieval_reason
blocked_items
source_refs
warnings
```

权限：只读。

边界：默认只返回 `active/reviewed` 且可见性通过的记忆；deprecated、full audit history、process log 必须显式请求。

## Tool: get_memory

用途：按 ID 读取单条记忆和审计链。

输入：

```text
project_id
memory_id
include_audit_trace=false
```

输出：

```text
memory_item
audit_trace
visibility_result
warnings
```

权限：只读。

## Tool: propose_memory

用途：让 AI 或工具提交候选记忆。

输入：

```text
project_id
memory_type
title
summary
content
source
relations
security
proposed_by
```

输出：

```text
memory_candidate_id
status=proposed
review_required=true
write_gate_result
audit_event_id
```

权限：受控写入，只能写 proposed。

## Tool: update_memory_status

用途：由人工、规则或受控流程更新记忆状态。

输入：

```text
project_id
memory_id
target_status
review_record
reason
```

输出：

```text
updated_memory_item
audit_event_id
```

权限：受控写入。

## Tool: supersede_memory

用途：替代旧记忆，不允许静默覆盖。

输入：

```text
project_id
old_memory_id
new_memory_candidate
reason
```

输出：

```text
supersede_relation
new_memory_candidate_id
audit_event_id
```

权限：受控写入。

## Tool: list_current_goals

用途：列出当前项目或任务相关目标。

输入：

```text
project_id
task_id
top_k
```

输出：

```text
goals
warnings
```

权限：只读。

## Tool: list_active_tasks

用途：列出当前 active / blocked / deferred 任务记忆。

输入：

```text
project_id
status
owner_agent
top_k
```

输出：

```text
tasks
warnings
```

权限：只读。

## Tool: list_relevant_lessons

用途：按当前任务、错误类型或风险场景读取相关 lesson。

输入：

```text
project_id
task_id
risk_type
top_k
token_budget
```

输出：

```text
lessons
retrieval_reason
warnings
```

权限：只读。

## Tool: list_boundaries

用途：读取当前项目或任务必须遵守的 active boundary。

输入：

```text
project_id
task_id
visibility_scope
```

输出：

```text
boundaries
blocked_items
warnings
```

权限：只读。

## Admin Tool: export_memory

用途：导出项目记忆，用于迁移、审计或备份。

权限：管理工具，必须记录 audit_event。

## Admin Tool: run_memory_integrity_check

用途：校验 memory_hash、source_hash、previous_version_id、snapshot_id 和索引一致性。

权限：管理工具，只读检查。

## Admin Tool: run_memory_regression_tests

用途：运行 retrieval、stale memory、permission、poisoning 和 rollback 回归测试。

权限：管理工具，只读检查。

## Admin Tool: rollback_memory_snapshot

用途：回滚到指定 snapshot，不删除历史，只写 rollback event。

权限：高风险管理工具，必须人工确认。

## 错误结构

```json
{
  "error_code": "MEMORY_NOT_FOUND | VISIBILITY_DENIED | WRITE_GATE_FAILED | CONFLICT_DETECTED | TOKEN_BUDGET_EXCEEDED | INVALID_STATUS_TRANSITION",
  "message": "中文错误说明",
  "retryable": false,
  "safe_next_action": "string",
  "audit_event_id": "string"
}
```

## 禁止事项

```text
1. 不允许 Project Memory MCP 直接写 active memory。
2. 不允许 Memory MCP 修改 CEK-TA 专业知识库。
3. 不允许 memory item 直接影响交易 final gate。
4. 不允许返回未脱敏 secret 或私有账户字段。
5. 不允许把向量召回命中当作事实结论。
6. 不允许 direct_write_active_memory。
7. 不允许 delete_memory_without_tombstone。
8. 不允许 cross_project_search_without_permission。
9. 不允许 write_vendor_memory_without_local_write_gate。
```
