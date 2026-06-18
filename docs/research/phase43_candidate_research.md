# Phase 43 Candidate Research

## 来源目录

- `langchain_memory`: LangChain Docs: Memory overview - https://docs.langchain.com/oss/python/concepts/memory
- `langchain_long_term`: LangChain Docs: Long-term memory - https://docs.langchain.com/oss/python/langchain/long-term-memory
- `letta_blocks`: Letta Docs: Memory blocks - https://docs.letta.com/guides/core-concepts/memory/memory-blocks/
- `letta_archival`: Letta Docs: Archival memory - https://docs.letta.com/guides/core-concepts/memory/archival-memory/
- `mem0_oss`: Mem0 Docs: Open Source Overview - https://docs.mem0.ai/open-source/overview
- `mem0_types`: Mem0 Docs: Memory Types - https://docs.mem0.ai/core-concepts/memory-types
- `graphiti`: Graphiti GitHub: Real-Time Knowledge Graphs for AI Agents - https://github.com/getzep/graphiti
- `zep_paper`: Zep: A Temporal Knowledge Graph Architecture for Agent Memory - https://arxiv.org/html/2501.13956v1
- `owasp_memory_guard`: OWASP Agent Memory Guard - https://owasp.org/www-project-agent-memory-guard/
- `owasp_ai_agent`: OWASP AI Agent Security Cheat Sheet - https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- `unit42_memory_poisoning`: Unit 42: Indirect prompt injection poisons AI long-term memory - https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/
- `postgres_jsonb`: PostgreSQL Documentation: JSON Types - https://www.postgresql.org/docs/current/datatype-json.html
- `pgvector`: pgvector: Open-source vector similarity search for Postgres - https://github.com/pgvector/pgvector
- `aws_mcp_security`: AWS Security Blog: Secure AI agent access patterns using MCP - https://aws.amazon.com/blogs/security/secure-ai-agent-access-patterns-to-aws-resources-using-model-context-protocol/

## 候选知识点

### P43-P0-001 RAG Knowledge 与 Project Memory 必须分离

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_boundary`
- role: `boundary`
- acceptance_gate: 明确区分专业知识、项目事实和临时上下文
- candidate_id: `cand_20260611_phase43_p43_p0_001_rag_knowledge_project_memory_001`

### P43-P0-002 Project Memory 不能污染 CEK-TA 通用专业知识库

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_boundary`
- role: `boundary`
- acceptance_gate: 明确禁止私有项目事实进入通用知识
- candidate_id: `cand_20260611_phase43_p43_p0_002_project_memory_cek_ta_002`

### P43-P0-003 CEK-TA 只定义 Memory Contract，不保存外接项目私有记忆

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_boundary`
- role: `boundary`
- acceptance_gate: 明确责任边界和不存储边界
- candidate_id: `cand_20260611_phase43_p43_p0_003_cek_ta_memory_contract_003`

### P43-P0-004 外接 AI IDE 应同时查询 CEK-TA MCP 与 Project Memory MCP

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_boundary`
- role: `boundary`
- acceptance_gate: 明确双 MCP 查询和引用边界
- candidate_id: `cand_20260611_phase43_p43_p0_004_ai_ide_cek_ta_mcp_project_memory_mcp_004`

### P43-P0-005 第一版 MemoryType 应压缩为 6 类

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `schema`
- acceptance_gate: 6 类可覆盖目标、任务、决策、产物、经验、边界
- candidate_id: `cand_20260611_phase43_p43_p0_005_memorytype_6_005`

### P43-P0-006 process 不应作为长期 MemoryItem

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_event_log`
- role: `lifecycle`
- acceptance_gate: process 进入 append-only event log
- candidate_id: `cand_20260611_phase43_p43_p0_006_process_memoryitem_006`

### P43-P0-007 future_plan 应并入 task 状态

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `lifecycle`
- acceptance_gate: future_plan 不单独成类
- candidate_id: `cand_20260611_phase43_p43_p0_007_future_plan_task_007`

### P43-P0-008 error 应并入 lesson 并记录复盘字段

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `lifecycle`
- acceptance_gate: error_cause/fix/prevention 完整
- candidate_id: `cand_20260611_phase43_p43_p0_008_error_lesson_008`

### P43-P0-009 MemoryItem 必须有来源、hash、trust 和 write_origin

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `schema`
- acceptance_gate: source_type/source_event/source_hash/source_trust/write_origin 必填
- candidate_id: `cand_20260611_phase43_p43_p0_009_memoryitem_hash_trust_write_origin_009`

### P43-P0-010 MemoryItem 必须支持 supersede

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `lifecycle`
- acceptance_gate: 不允许静默覆盖
- candidate_id: `cand_20260611_phase43_p43_p0_010_memoryitem_supersede_010`

### P43-P0-011 deprecated memory 不能作为当前事实

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `lifecycle`
- acceptance_gate: deprecated 只用于历史审计
- candidate_id: `cand_20260611_phase43_p43_p0_011_deprecated_memory_011`

### P43-P0-012 AI 只能 propose memory

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_write_gate`
- role: `write_gate`
- acceptance_gate: active 必须受控审核
- candidate_id: `cand_20260611_phase43_p43_p0_012_ai_propose_memory_012`

### P43-P0-013 长期记忆写入必须通过完整安全门禁

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_write_gate`
- role: `write_gate`
- acceptance_gate: source/secret/prompt_injection/poisoning/visibility/conflict/untrusted 检查齐全
- candidate_id: `cand_20260611_phase43_p43_p0_013__013`

### P43-P0-014 不能把所有聊天自动写入长期记忆

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_write_gate`
- role: `write_gate`
- acceptance_gate: 明确长期记忆筛选条件
- candidate_id: `cand_20260611_phase43_p43_p0_014__014`

### P43-P0-015 长期记忆写入白名单

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_write_gate`
- role: `write_gate`
- acceptance_gate: 用户明确记住、目标变化、架构决策、复盘和审计结论才适合保存
- candidate_id: `cand_20260611_phase43_p43_p0_015__015`

### P43-P0-016 长期记忆写入黑名单

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_write_gate`
- role: `write_gate`
- acceptance_gate: 普通对话、debug、推断和短期日志不进长期记忆
- candidate_id: `cand_20260611_phase43_p43_p0_016__016`

### P43-P0-017 Project Memory MCP/API 必须使用最小权限工具集

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_mcp_api_contract`
- role: `mcp_api`
- acceptance_gate: 写入类工具必须经过 write gate，不允许 direct_write_active_memory
- candidate_id: `cand_20260611_phase43_p43_p0_017_project_memory_mcp_api_017`

### P43-P0-018 Memory retention / deletion / export policy 必须显式定义

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_retention_privacy`
- role: `retention_privacy`
- acceptance_gate: 不能无限期保留所有项目记忆，必须支持 tombstone/export
- candidate_id: `cand_20260611_phase43_p43_p0_018_memory_retention_deletion_export_policy_018`

### P43-P0-019 Memory conflict resolution 必须可审计

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_schema_lifecycle`
- role: `conflict_resolution`
- acceptance_gate: conflict_status/conflict_reason/resolver/resolution_event_id 完整
- candidate_id: `cand_20260611_phase43_p43_p0_019_memory_conflict_resolution_019`

### P43-P0-020 长期记忆必须防 prompt injection / memory poisoning

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_security_governance`
- role: `security`
- acceptance_gate: 中毒风险、外部输入和审计链明确
- candidate_id: `cand_20260611_phase43_p43_p0_020_prompt_injection_memory_poisoning_020`

### P43-P0-021 MemoryItem 必须可回滚、可完整性校验

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_security_governance`
- role: `integrity`
- acceptance_gate: memory_hash、source_hash、previous_version、snapshot、rollback event 明确
- candidate_id: `cand_20260611_phase43_p43_p0_021_memoryitem_021`

### P43-P0-022 PostgreSQL JSONB 是 v0.1 canonical store 推荐基线

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_adapter_selection`
- role: `storage_baseline`
- acceptance_gate: canonical store 与 semantic index 分离
- candidate_id: `cand_20260611_phase43_p43_p0_022_postgresql_jsonb_v0_1_canonical_store_022`

### P43-P0E-001 Memory recall 必须受范围和预算限制

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_retrieval_context`
- role: `retrieval`
- acceptance_gate: project_id/visibility/status/top-k/token budget 明确
- candidate_id: `cand_20260611_phase43_p43_p0e_001_memory_recall_023`

### P43-P0E-002 默认上下文只注入关键记忆

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_retrieval_context`
- role: `retrieval`
- acceptance_gate: 默认只注入 goal/task/boundary/relevant lesson
- candidate_id: `cand_20260611_phase43_p43_p0e_002__024`

### P43-P0E-003 长日志、审计历史和 deprecated memory 必须显式请求

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_retrieval_context`
- role: `retrieval`
- acceptance_gate: 默认不注入历史噪声
- candidate_id: `cand_20260611_phase43_p43_p0e_003_deprecated_memory_025`

### P43-P0E-004 Memory quality 必须做回归测试

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_evaluation_regression`
- role: `evaluation`
- acceptance_gate: retrieval/stale/poisoning/permission 测试齐全
- candidate_id: `cand_20260611_phase43_p43_p0e_004_memory_quality_026`

### P43-P1-001 第三方 memory engine 只能作为 adapter

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_adapter_selection`
- role: `adapter`
- acceptance_gate: 不替代核心契约
- candidate_id: `cand_20260611_phase43_p43_p1_001_memory_engine_adapter_027`

### P43-P1-002 pgvector 是可选 semantic index

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_adapter_selection`
- role: `adapter`
- acceptance_gate: pgvector 不是事实源，也不是默认必须启用
- candidate_id: `cand_20260611_phase43_p43_p1_002_pgvector_semantic_index_028`

### P43-P1-003 Adapter portability test 必须验证可迁移性

- canonical_node_id: `kt.ai_engineering.external_project_memory.memory_evaluation_regression`
- role: `evaluation`
- acceptance_gate: 第三方 memory engine 可迁移回 CEK-TA Memory Contract
- candidate_id: `cand_20260611_phase43_p43_p1_003_adapter_portability_test_029`

