# Phase 43 External Project AI Memory Layer 范围方案

## 目标

Phase 43 为使用 CEK-TA 的外接 AI 项目定义项目记忆层知识体系。它解决的是外接 AI IDE / Agent 如何记住项目目标、任务、决策、产物、经验、边界和错误复盘，并在后续开发中可检索、可审计、可回滚、可迁移。

本 Phase 不给 CEK-TA 自己保存项目进度记忆，也不保存任何外接项目的私有事实。CEK-TA 只沉淀通用 Memory Contract、schema、MCP/API 契约、写入门禁、检索预算、安全治理和 adapter 选型知识。

## 上游

```text
1. Phase 35 外部项目 AI 主动检索协议。
2. Phase 36/38/40/41 AI Engineering 知识分支。
3. Phase 42 Database / Storage Engineering。
4. Phase 32 候选到 reviewed 知识审计工作流。
5. AGENTS.md 的路径、UTF-8、MCP/API、数据库/存储和知识治理规范。
```

## 下游

```text
1. 外接项目可实现自己的 Project Memory MCP/API。
2. 外接项目 AI IDE 可以同时查询 CEK-TA 专业知识和项目记忆。
3. CEK-TA SearchLab / MCP / 知识树可以检索本分支的专业知识。
4. 后续 Phase 43 候选知识采集、审计、formal reviewed 沉淀。
```

## 知识树归属

```text
L1: kt.ai_engineering
L2: kt.ai_engineering.external_project_memory
partition: KB_AI_27_PROJECT_MEMORY
```

## L3 专题

| L3 | canonical_node_id | 职责 |
| --- | --- | --- |
| Memory Boundary | `kt.ai_engineering.external_project_memory.memory_boundary` | 区分 CEK-TA 专业知识、外接项目记忆、私有项目事实和临时上下文 |
| Memory MCP API Contract | `kt.ai_engineering.external_project_memory.memory_mcp_api_contract` | 定义 Project Memory MCP/API 最小权限工具集、读写边界、错误结构和审计事件 |
| Memory Schema Lifecycle | `kt.ai_engineering.external_project_memory.memory_schema_lifecycle` | 定义 MemoryItem、memory_type、状态机、supersede 和 review |
| Memory Event Log | `kt.ai_engineering.external_project_memory.memory_event_log` | 定义 append-only event log、source_event_id、trace_id 和审计追踪 |
| Memory Write Gate | `kt.ai_engineering.external_project_memory.memory_write_gate` | 定义 AI propose only、来源检查、脱敏、冲突检查和写入审批 |
| Memory Retrieval Context | `kt.ai_engineering.external_project_memory.memory_retrieval_context` | 定义 project_id、visibility、status、top-k、token budget 和默认注入范围 |
| Memory Security Governance | `kt.ai_engineering.external_project_memory.memory_security_governance` | 定义 prompt injection、memory poisoning、secret scan、rollback 和完整性 |
| Memory Retention Privacy | `kt.ai_engineering.external_project_memory.memory_retention_privacy` | 定义 retention、deletion、export、privacy minimization、tombstone 和生命周期证据 |
| Memory Adapter Selection | `kt.ai_engineering.external_project_memory.memory_adapter_selection` | 定义 PostgreSQL JSONB、pgvector、LangGraph、Letta、Mem0、Zep/Graphiti 的 adapter 边界 |
| Memory Evaluation Regression | `kt.ai_engineering.external_project_memory.memory_evaluation_regression` | 定义 retrieval regression、stale memory、permission、poisoning 和 rollback 测试 |

## 核心边界

```text
1. Project Memory 是项目状态，不是 CEK-TA 专业知识。
2. CEK-TA 不保存外接项目私有目标、任务、错误、决策或产物。
3. AI 只能 propose memory，不能直接写 active memory。
4. 不能把所有聊天自动写入长期记忆。
5. vector hit 不是事实源，只能作为召回索引。
6. 第三方 memory engine 只能作为 adapter，不能替代 CEK-TA Memory Contract。
7. Memory 不能决定交易、不能替代 deterministic final gate、不能产生买卖点或仓位建议。
```

## 参考来源方向

| 来源 | 用途 |
| --- | --- |
| LangChain / LangGraph long-term memory 文档 | 区分 thread memory、long-term memory、memory store 和 agent recall |
| Letta memory blocks / archival memory 文档 | 参考核心记忆块、归档记忆和 agent 可编辑记忆边界 |
| Mem0 open-source 文档 | 参考用户/agent/session 维度的长期记忆接口和 adapter 形态 |
| Zep / Graphiti 项目与论文 | 参考时序知识图谱和 episode 到 entity/relationship 的记忆建模 |
| PostgreSQL JSONB 与 pgvector 文档 | 参考 canonical store 与可选向量索引分离 |
| OWASP Agent Memory Guard | 参考 agent memory 的敏感数据、注入和治理要求 |
| Unit42 memory poisoning 案例 | 参考间接 prompt injection 污染长期记忆的风险 |

## 首批知识点数量

```text
P0-Core: 22 条
P0-Extended: 4 条
P1: 3 条
合计: 29 条
```

## 不进入本 Phase 的内容

```text
1. 不实现外接项目生产数据库。
2. 不实现 Project Memory MCP server。
3. 不绑定单一第三方 memory 平台。
4. 不保存任何外接项目私有项目记忆。
5. 不创建 approved/default guidance。
6. 不把记忆用作交易执行或风控 final gate。
```
