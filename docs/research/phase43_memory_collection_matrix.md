# Phase 43 Memory Knowledge Collection Matrix

## 采集目标

本矩阵定义 Phase 43 首批 29 条外接项目 AI Memory Layer 知识点。采集完成后先进入 candidate，再走 Phase 32 审计工作流，不直接进入 approved/default guidance。

## 优先级统计

```text
P0-Core: 22
P0-Extended: 4
P1: 3
Total: 29
```

| topic_id | priority | title | canonical_node_id | role | expected_sources | acceptance_gate |
| --- | --- | --- | --- | --- | --- | --- |
| P43-P0-001 | P0 | RAG Knowledge 与 Project Memory 必须分离 | `kt.ai_engineering.external_project_memory.memory_boundary` | boundary | LangChain memory concepts, CEK-TA RAG contract, memory security references | 明确区分专业知识、项目事实和临时上下文 |
| P43-P0-002 | P0 | Project Memory 不能污染 CEK-TA 通用专业知识库 | `kt.ai_engineering.external_project_memory.memory_boundary` | boundary | CEK-TA governance, RAG source governance, memory poisoning references | 明确禁止私有项目事实进入通用知识 |
| P43-P0-003 | P0 | CEK-TA 只定义 Memory Contract，不保存外接项目私有记忆 | `kt.ai_engineering.external_project_memory.memory_boundary` | boundary | CEK-TA integration docs, data privacy references | 明确责任边界和不存储边界 |
| P43-P0-004 | P0 | 外接 AI IDE 应同时查询 CEK-TA MCP 与 Project Memory MCP | `kt.ai_engineering.external_project_memory.memory_boundary` | boundary | MCP contract, agent memory docs, RAG retrieval docs | 明确双 MCP 查询和引用边界 |
| P43-P0-005 | P0 | 第一版 MemoryType 应压缩为 6 类 | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | schema | LangGraph memory docs, Letta memory blocks, Mem0 docs | 6 类可覆盖目标、任务、决策、产物、经验、边界 |
| P43-P0-006 | P0 | process 不应作为长期 MemoryItem | `kt.ai_engineering.external_project_memory.memory_event_log` | lifecycle | event sourcing references, LangChain memory concepts | process 进入 append-only event log |
| P43-P0-007 | P0 | future_plan 应并入 task 状态 | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | lifecycle | task management references, agent memory docs | future_plan 不单独成类 |
| P43-P0-008 | P0 | error 应并入 lesson 并记录复盘字段 | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | lifecycle | incident/postmortem references, memory docs | error_cause/fix/prevention 完整 |
| P43-P0-009 | P0 | MemoryItem 必须有来源、hash、trust 和 write_origin | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | schema | RAG citation docs, audit log references | source_type/source_event/source_hash/source_trust/write_origin 必填 |
| P43-P0-010 | P0 | MemoryItem 必须支持 supersede | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | lifecycle | data versioning, audit log references | 不允许静默覆盖 |
| P43-P0-011 | P0 | deprecated memory 不能作为当前事实 | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | lifecycle | lifecycle governance, RAG freshness references | deprecated 只用于历史审计 |
| P43-P0-012 | P0 | AI 只能 propose memory | `kt.ai_engineering.external_project_memory.memory_write_gate` | write_gate | LangGraph memory docs, Letta agent memory controls, OWASP references | active 必须受控审核 |
| P43-P0-013 | P0 | 长期记忆写入必须通过完整安全门禁 | `kt.ai_engineering.external_project_memory.memory_write_gate` | write_gate | OWASP, Unit42, privacy/security references | source/secret/prompt_injection/poisoning/visibility/conflict/untrusted 检查齐全 |
| P43-P0-014 | P0 | 不能把所有聊天自动写入长期记忆 | `kt.ai_engineering.external_project_memory.memory_write_gate` | write_gate | memory management docs, privacy references | 明确长期记忆筛选条件 |
| P43-P0-015 | P0 | 长期记忆写入白名单 | `kt.ai_engineering.external_project_memory.memory_write_gate` | write_gate | memory docs, incident review references | 用户明确记住、目标变化、架构决策、复盘和审计结论才适合保存 |
| P43-P0-016 | P0 | 长期记忆写入黑名单 | `kt.ai_engineering.external_project_memory.memory_write_gate` | write_gate | memory docs, data minimization references | 普通对话、debug、推断和短期日志不进长期记忆 |
| P43-P0-017 | P0 | Project Memory MCP/API 必须使用最小权限工具集 | `kt.ai_engineering.external_project_memory.memory_mcp_api_contract` | mcp_api | MCP/API design references, OWASP references | 写入类工具必须经过 write gate，不允许 direct_write_active_memory |
| P43-P0-018 | P0 | Memory retention / deletion / export policy 必须显式定义 | `kt.ai_engineering.external_project_memory.memory_retention_privacy` | retention_privacy | privacy minimization, data lifecycle, audit references | 不能无限期保留所有项目记忆，必须支持 tombstone/export |
| P43-P0-019 | P0 | Memory conflict resolution 必须可审计 | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | conflict_resolution | audit log, data governance references | conflict_status/conflict_reason/resolver/resolution_event_id 完整 |
| P43-P0-020 | P0 | 长期记忆必须防 prompt injection / memory poisoning | `kt.ai_engineering.external_project_memory.memory_security_governance` | security | OWASP Agent Memory Guard, Unit42 case, prompt injection references | 中毒风险、外部输入和审计链明确 |
| P43-P0-021 | P0 | MemoryItem 必须可回滚、可完整性校验 | `kt.ai_engineering.external_project_memory.memory_security_governance` | integrity | audit ledger, integrity, rollback references | memory_hash、source_hash、previous_version、snapshot、rollback event 明确 |
| P43-P0-022 | P0 | PostgreSQL JSONB 是 v0.1 canonical store 推荐基线 | `kt.ai_engineering.external_project_memory.memory_adapter_selection` | storage_baseline | PostgreSQL JSONB docs, LangGraph JSON memory docs | canonical store 与 semantic index 分离 |
| P43-P0E-001 | P0E | Memory recall 必须受范围和预算限制 | `kt.ai_engineering.external_project_memory.memory_retrieval_context` | retrieval | LangChain/LangGraph retrieval docs, RAG budget references | project_id/visibility/status/top-k/token budget 明确 |
| P43-P0E-002 | P0E | 默认上下文只注入关键记忆 | `kt.ai_engineering.external_project_memory.memory_retrieval_context` | retrieval | agent context docs, RAG context selection docs | 默认只注入 goal/task/boundary/relevant lesson |
| P43-P0E-003 | P0E | 长日志、审计历史和 deprecated memory 必须显式请求 | `kt.ai_engineering.external_project_memory.memory_retrieval_context` | retrieval | audit log, RAG retrieval docs | 默认不注入历史噪声 |
| P43-P0E-004 | P0E | Memory quality 必须做回归测试 | `kt.ai_engineering.external_project_memory.memory_evaluation_regression` | evaluation | RAG eval, security regression, permission testing references | retrieval/stale/poisoning/permission 测试齐全 |
| P43-P1-001 | P1 | 第三方 memory engine 只能作为 adapter | `kt.ai_engineering.external_project_memory.memory_adapter_selection` | adapter | LangGraph, Letta, Mem0, Zep/Graphiti docs | 不替代核心契约 |
| P43-P1-002 | P1 | pgvector 是可选 semantic index | `kt.ai_engineering.external_project_memory.memory_adapter_selection` | adapter | pgvector docs, PostgreSQL docs | pgvector 不是事实源，也不是默认必须启用 |
| P43-P1-003 | P1 | Adapter portability test 必须验证可迁移性 | `kt.ai_engineering.external_project_memory.memory_evaluation_regression` | evaluation | adapter portability, migration test references | 第三方 memory engine 可迁移回 CEK-TA Memory Contract |
