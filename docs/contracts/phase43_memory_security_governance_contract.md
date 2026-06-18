# Phase 43 Memory Security Governance Contract

## 目标

长期项目记忆一旦被污染，会持续影响外接 AI IDE / Agent 的后续行为。因此记忆层必须把安全治理作为写入、检索和回滚的核心契约。

## 风险类型

| 风险 | 说明 |
| --- | --- |
| memory poisoning | 不可信输入被写入长期记忆，后续持续误导 AI |
| indirect prompt injection | 外部网页、文档或工具输出诱导 AI 修改长期规则 |
| secret persistence | 密钥、账户、私有订单字段被写入长期记忆 |
| stale memory | 已过期目标、任务或决策继续被当作当前事实 |
| visibility leak | private 记忆被 team 或其他 agent 检索 |
| vector false positive | 向量相似命中被误当作事实 |

## 写入安全门禁

```text
1. untrusted_input=true 的候选不得自动 active。
2. 外部网页、日志、模型输出、工具输出默认视为 untrusted。
3. secret scan 必须早于持久化 active memory。
4. 与 active boundary 冲突的候选必须进入 conflict_review。
5. 高 poisoning_risk 候选只能 rejected 或人工复核。
6. 每次状态变更必须写入 memory_events。
```

## 检索安全门禁

```text
1. 检索必须按 project_id 和 visibility_scope 过滤。
2. private 记忆不得跨项目、跨团队、跨 agent 泄露。
3. deprecated 和 rejected 默认不返回。
4. untrusted 记忆默认只作为审计线索，不作为事实注入。
5. 召回结果必须携带 source_refs、status、review_status、freshness。
```

## 完整性与回滚

每条 MemoryItem 必须支持：

```text
source_hash
content_hash
previous_version_id
supersedes
rollback_allowed
audit_event_id
```

回滚规则：

```text
1. 不删除历史，只创建 rollback 或 supersede event。
2. active -> deprecated / superseded 必须有原因。
3. 回滚后必须重新计算检索索引。
4. 回滚报告必须能说明影响范围。
```

## 第三方 adapter 安全边界

```text
1. LangGraph、Letta、Mem0、Zep/Graphiti 等只能作为 adapter。
2. adapter 生成或召回的记忆仍需通过本地 write gate 和 retrieval policy。
3. 不允许把 vendor 内部状态直接视为 CEK-TA MemoryItem。
4. vendor lock-in 风险必须在外接项目设计中显式记录。
```

## 审计要求

```text
1. 每个写入事件必须有 trace_id。
2. 每个 active memory 必须能追到来源和审核记录。
3. 每个检索响应必须能解释为什么返回、为什么阻断。
4. 每次安全阻断必须生成可读 audit_event。
5. 定期运行 stale memory、permission、poisoning 和 rollback 回归测试。
```
