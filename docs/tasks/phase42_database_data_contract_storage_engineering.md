# Phase 42: Database / Data Contract / Storage Engineering for Trading AI

## Phase 目标

为外接交易 AI、LLM gating/scoring、RAG 检索和审计工作流补齐数据库、数据契约、存储、审计日志、向量库、备份恢复和数据生命周期治理知识。

本 Phase 的重点不是立刻引入真实数据库，而是把后续外接项目开发 AI 必须掌握的数据库工程知识拆成可采集、可审计、可检索、可复用的正式知识分支。

核心原则：

```text
1. PostgreSQL 可作为 canonical store，但 Vector DB 只能作为 retrieval index，不能作为事实主库。
2. LLM audit 可以写审计结果表，但不能写 final_gate 决策表。
3. score、final_gate、feedback、outcome、label、dataset、model、prompt、RAG index 必须可追踪、可回放、可审计。
4. 决策时点可见性、防泄漏、版本绑定和审计追踪优先于“单纯建表”。
5. 数据库/存储知识只能指导 AI Engineering 与 Project Integration，不把 K 线、fill model、仓位、风控本体混入本分支。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-342 | P0 | done | 创建 Phase 42 任务卡并登记任务索引 | `docs/tasks/phase42_database_data_contract_storage_engineering.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-340 |
| CEK-TA-343 | P0 | done | 定义 Database / Data Contract / Storage Engineering 知识范围、L3 专题和跨分支边界 | `docs/research/phase42_database_storage_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-342 |
| CEK-TA-344 | P0 | done | 定义交易 AI 数据库核心表、主键、索引、时间字段、版本字段、审计字段和 append-only 边界契约 | `docs/contracts/phase42_database_storage_contract.md` | CEK-TA-343 |
| CEK-TA-345 | P0 | done | 定义 RAG 文档、chunk、embedding、vector index、citation 和 source provenance 存储契约 | `docs/contracts/phase42_rag_vector_storage_contract.md` | CEK-TA-344 |
| CEK-TA-346 | P0 | done | 创建 34 条 Phase 42 知识点采集矩阵和 ResearchIngestionTask 队列 | `docs/research/phase42_database_storage_collection_matrix.md`、`docs/research/phase42_research_task_queue.md` | CEK-TA-345 |
| CEK-TA-347 | P0 | done | 导出 Phase 42 知识范围审计 JSON，先审计边界、专题、表结构和知识点数量 | `docs/audit/phase42_database_storage_scope_for_audit.json` | CEK-TA-346 |
| CEK-TA-348 | P1 | done | 联网采集 P0 来源，生成候选知识包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase42_p0_candidate_research.md`、`docs/reports/phase42_candidate_generation_report.md`、`docs/reports/phase42_candidate_quality_gate.json` | CEK-TA-347 |
| CEK-TA-349 | P1 | done | 导出 Phase 42 候选 AI 审计包，等待按 Phase 32 工作流处理 accepted、needs_more_evidence、rejected | `docs/audit/phase42_candidate_audit_package_20260611.json`、`docs/reports/phase42_candidate_audit_package_quality_gate.json` | CEK-TA-348 |
| CEK-TA-350 | P1 | done | 按审计结果补证、回写、沉淀 formal reviewed/caveat_only 知识并重建索引和 Vue3 fixture | `docs/audit/audit_result_phase42_candidate_audit_package_20260611_strict_v1.json`、`docs/reports/phase42_candidate_audit_import_report.json`、`docs/audit/phase42_needs_evidence_supplemental_reaudit_package_20260611.json`、`docs/research/phase42_needs_evidence_supplemental_research.md`、`docs/audit/audit_result_phase42_needs_evidence_supplemental_reaudit_20260611_strict_v2.json`、`docs/reports/phase42_supplemental_reaudit_import_report.json`、`docs/reports/phase42_candidates_to_reviewed_promotion_report.json`、`codex-expert-kit/rag/scripts/apply_phase42_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/promote_phase42_accepted_candidates_to_reviewed.py`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts` | CEK-TA-349 |
| CEK-TA-351 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按数据库存储子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase42_runtime_linkage.py`、`docs/reports/phase42_runtime_linkage_validation_report.json` | CEK-TA-350 |
| CEK-TA-352 | P1 | done | 生成 Phase 42 P0 验收报告，明确 P1 6 条仍需继续采集 | `docs/reports/phase42_database_storage_engineering_report.md` | CEK-TA-351 |
| CEK-TA-353 | P1 | done | 联网采集 Phase 42 P1 6 条来源，生成候选知识包并运行来源、冲突、乱码和污染门禁 | `codex-expert-kit/rag/scripts/generate_phase42_p1_candidates.py`、`codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/`、`docs/research/phase42_p1_candidate_research.md`、`docs/reports/phase42_p1_candidate_generation_report.md`、`docs/reports/phase42_p1_candidate_quality_gate.json` | CEK-TA-352 |
| CEK-TA-354 | P1 | done | 导出 Phase 42 P1 6 条候选 AI 审计包，等待外部 AI/人工严格审计 | `codex-expert-kit/rag/scripts/export_phase42_p1_candidate_audit_package.py`、`docs/audit/phase42_p1_candidate_audit_package_20260611.json`、`docs/reports/phase42_p1_candidate_audit_package_quality_gate.json` | CEK-TA-353 |
| CEK-TA-355 | P1 | done | 按 Phase 32 工作流处理 P1 审计结果、补证、回写并沉淀 6 条 formal reviewed/caveat_only 知识；不创建 approved、default guidance 或 hard gate | `codex-expert-kit/rag/scripts/apply_phase42_p1_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase42_p1_p003_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase42_p1_reviewed_preparation_result.py`、`docs/audit/audit_result_phase42_p1_candidate_audit_package_20260611_strict_v1.json`、`docs/reports/phase42_p1_audit_import_report.json`、`docs/research/phase42_p1_p003_supplemental_research.md`、`docs/audit/audit_result_phase42_p1_p003_supplemental_reaudit_20260611_strict_v2.json`、`docs/reports/phase42_p1_p003_supplemental_reaudit_import_report.json`、`docs/audit/phase42_p1_reviewed_preparation_audit_package_20260611.json`、`docs/audit/audit_result_phase42_p1_reviewed_preparation_20260611_strict_v1.json`、`docs/reports/phase42_p1_reviewed_preparation_import_report.json`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`ui/src/data/knowledgeTreeNodes.ts` | CEK-TA-354 |
| CEK-TA-356 | P1 | done | 验证 MCP/SearchLab/KnowledgeTree 能按 Phase 42 P1 子板块检索、引用、阻断和降级 | `codex-expert-kit/rag/scripts/validate_phase42_runtime_linkage.py`、`docs/reports/phase42_runtime_linkage_validation_report.json` | CEK-TA-355 |
| CEK-TA-357 | P1 | done | 生成 Phase 42 全量验收报告并更新 Phase 状态为 done | `docs/reports/phase42_database_storage_engineering_report.md` | CEK-TA-356 |

## 上游输入

```text
1. Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展。
2. Phase 38 AI 模型平台与交易 Gating/Scoring POC 知识扩展。
3. Phase 40 AI Continuous Learning 与再训练闭环。
4. Phase 41 Hybrid Scoring 与 Qwen3 审计助手知识扩展。
5. Phase 32 候选到 reviewed 知识的批量审计工作流。
6. codex-expert-kit/rag/knowledge_tree.md
7. codex-expert-kit/rag/knowledge_item_schema.md
8. codex-expert-kit/rag/indexes/knowledge_items.json
9. AGENTS.md 中数据库/存储规范、路径 resolver 规范和 UTF-8 规范。
```

## 下游输出

```text
1. 外接交易 AI 项目可复用的数据库、数据契约和存储工程知识。
2. AI Engineering 下 Database / Data Contract / Storage Engineering 子分支。
3. 表结构、迁移、索引、审计日志、向量库、RAG 存储、备份恢复和生命周期治理知识卡。
4. MCP/SearchLab/KnowledgeTree/Vue3 可检索、可审计、可引用的 formal reviewed 知识。
5. 后续项目数据库设计、迁移和审计日志实现的 AI IDE 主动检索依据。
```

## 建议 L3 专题

Phase 42 默认挂在 `kt.ai_engineering.database_storage_engineering`，并按必要程度引用 `kt.rag_engineering`、`kt.project_support` 和 `kt.knowledge_governance`。

| L3 专题 | canonical node | 说明 |
| --- | --- | --- |
| Relational Core Schema | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | 交易 AI 核心关系表、主键、外键、约束、JSONB 边界 |
| Data Contract Lineage | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | decision_time、event_time、label_time、schema hash、dataset hash、lineage |
| Migration Versioning | `kt.ai_engineering.database_storage_engineering.migration_versioning` | Alembic、migration review、rollback、兼容性检查 |
| Indexing Query Performance | `kt.ai_engineering.database_storage_engineering.indexing_query_performance` | 查询模式、复合索引、分区、分页、慢查询审计 |
| Audit Log Ledger | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append-only ledger、trace_id、actor、reason、row_hash/prev_hash |
| Feature Store Storage | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | offline/online feature parity、feature snapshot、feature manifest |
| Vector Store Retrieval Storage | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | pgvector/Qdrant、embedding version、payload metadata、source provenance |
| Model Registry Release Storage | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | model release manifest、scorer/calibrator/prompt/RAG index 版本绑定 |
| Runtime Observability Trace | `kt.ai_engineering.database_storage_engineering.runtime_observability_trace` | request_id、audit_trace_id、latency、fallback、error record |
| Data Lifecycle Retention | `kt.ai_engineering.database_storage_engineering.data_lifecycle_retention` | 保留、归档、删除、冷存储、不破坏审计回放 |
| Security Privacy Access Control | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | secret 不入业务表、权限、RLS、脱敏、PII/private field 边界 |
| Backup Restore Disaster Recovery | `kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery` | backup、restore drill、RPO/RTO、演练记录 |

## 知识点规划

首批规划 34 条：P0 28 条，P1 6 条。当前 34 条均已完成 formal reviewed/caveat_only 沉淀；不创建 approved、default guidance 或 hard gate。Phase 42 全量验收报告见 `docs/reports/phase42_database_storage_engineering_report.md`。

### P0：28 条

```text
1. P42-P0-001：canonical records must live in PostgreSQL, not vector DB。
2. P42-P0-002：every scoring/gating decision must have audit_trace_id。
3. P42-P0-003：final_gate decision must be append-only。
4. P42-P0-004：score_result must be versioned append-only。
5. P42-P0-005：trade_candidate snapshot must contain only decision-time visible fields。
6. P42-P0-006：outcome must be isolated from input features。
7. P42-P0-007：feedback/outcome/label must be separated。
8. P42-P0-008：labels must record label_policy_version and label_source。
9. P42-P0-009：model_version/prompt_version/rag_index_version must be recorded together。
10. P42-P0-010：LLM audit output must bind citations/source/version。
11. P42-P0-011：vector search result must link back to source document and formal knowledge id。
12. P42-P0-012：RAG chunks must store source_uri/license/hash/chunk_version。
13. P42-P0-013：embedding_model_version must be stored with vector records。
14. P42-P0-014：PostgreSQL constraints must enforce high-value invariants。
15. P42-P0-015：high-value tables must use unique constraints and idempotency keys。
16. P42-P0-016：Alembic migration must be reviewed and reversible。
17. P42-P0-017：autogenerate migration must not be auto-applied。
18. P42-P0-018：schema_version change must trigger compatibility check。
19. P42-P0-019：event_time/decision_time/ingestion_time/label_time must be separated。
20. P42-P0-020：point-in-time correctness is required for training datasets。
21. P42-P0-021：feature_snapshot_manifest must store feature_schema_hash。
22. P42-P0-022：dataset_snapshot_manifest must store dataset_hash。
23. P42-P0-023：final_gate ledger must store actor/reason/before_after/trace_id。
24. P42-P0-024：audit ledger must support row_hash/prev_hash or equivalent tamper evidence。
25. P42-P0-025：delete/retention policy must not break audit replay。
26. P42-P0-026：database credentials/secrets/private account fields must not be stored in business tables。
27. P42-P0-027：backup restore must be tested, not only configured。
28. P42-P0-028：DB permissions and write actions must be auditable。
```

### P1：6 条

```text
29. P42-P1-001：pgvector vs Qdrant selection boundary。
30. P42-P1-002：HNSW vs IVFFlat selection boundary。
31. P42-P1-003：Qdrant payload index / metadata filter rule。
32. P42-P1-004：Feast adoption boundary after offline/online parity pressure。
33. P42-P1-005：MLflow registry adoption boundary after release manifest complexity。
34. P42-P1-006：RLS / pgAudit adoption boundary。
```

## 输入契约

Phase 42 的采集任务必须至少包含：

```text
knowledge_topic_id
target_canonical_node_id
priority: P0 | P1
claim_type
storage_role: canonical_store | audit_ledger | vector_index | manifest_store | feature_store | registry | backup_restore
expected_sources
source_types
applicability
not_applicable_when
related_phase38_items
related_phase40_items
related_phase41_items
runtime_consumer: MCP | SearchLab | external_ai_ide | Vue3 | training_project
acceptance_gate
```

外接项目调用 Phase 42 知识时，应至少提供：

```text
project_adapter_id
task_type
requested_decision: schema_design | migration | indexing | audit_log | vector_store | lifecycle | backup_restore
data_domain
decision_time_available_fields
schema_version
dataset_hash
model_version
prompt_version
rag_index_version
audit_trace_id
storage_backend
write_permission_scope
```

## 输出契约

RAG/MCP 返回 Phase 42 知识时必须包含：

```text
knowledge_id
canonical_node_id
review_status
machine_gate.default_guidance
claim_type
storage_role
llm_usage_policy
source_evidence
conflict_status
freshness
applicability
not_applicable_when
required_runtime_fields
recommended_next_action
```

涉及数据库实现建议时必须区分：

```text
canonical_store_advice:
  table_role
  primary_key
  unique_key
  required_time_fields
  required_version_fields
  audit_fields
  append_only_required

retrieval_index_advice:
  vector_backend
  embedding_model_version
  payload_metadata
  source_document_link
  index_version
  rebuild_policy

governance_advice:
  migration_review
  rollback_plan
  backup_restore_drill
  retention_policy
  access_control
```

## 边界范围

本 Phase 包含：

```text
1. 交易 AI 项目的数据库、数据契约、存储、审计日志、向量检索存储和生命周期治理知识。
2. PostgreSQL、Alembic、pgvector/Qdrant、Feast、MLflow、RLS/pgAudit 等技术的专业边界知识。
3. table/schema/index/migration/audit/backup/vector storage 的知识卡采集、审计和 formal reviewed 沉淀。
4. MCP/SearchLab/KnowledgeTree/Vue3 对新知识的只读检索和审计展示对齐。
```

本 Phase 不包含：

```text
1. 不直接创建生产数据库。
2. 不执行不可逆迁移。
3. 不改外部项目真实数据库。
4. 不训练模型。
5. 不设计具体交易策略。
6. 不把 K 线、fill model、风控本体塞进本分支。
7. 不让向量库成为事实主库。
8. 不允许 LLM 输出直接写 final_gate。
9. 不允许无 migration 手改 schema。
10. 不允许没有 audit_trace_id 的交易 AI 决策入库。
11. 不把 candidate/reviewed 自动升级为 approved/default guidance/hard gate。
```

## 涉及组件

```text
docs/research/
docs/contracts/
docs/audit/
docs/reports/
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/
codex-expert-kit/api/
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
ui/src/data/knowledgeTreeNodes.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
```

## 涉及数据结构

```text
KnowledgeItem v1.1
ResearchIngestionTask
CandidateKnowledge
AI audit package
AI audit result
knowledge_items.json
trade_candidate
score_result
calibration_result
llm_audit_result
final_gate_ledger
feedback_event
outcome_event
label_event
feature_snapshot_manifest
dataset_snapshot_manifest
rag_document
rag_chunk
vector_index_manifest
model_release_manifest
audit_trace
migration_history
incident_freeze
```

## 涉及数据库/存储

本 Phase 会定义数据库/存储知识，但默认不直接引入或部署数据库。

最小表骨架知识范围：

```text
trade_candidate
score_result
calibration_result
llm_audit_result
final_gate_ledger
feedback_event
outcome_event
label_event
feature_snapshot_manifest
dataset_snapshot_manifest
rag_document
rag_chunk
vector_index_manifest
model_release_manifest
audit_trace
migration_history
incident_freeze
```

append-only 建议范围：

```text
final_gate_ledger
score_result
llm_audit_result
feedback_event
outcome_event
label_event
```

允许 update 的范围必须限定为：

```text
manifest 状态
处理状态
归档状态
非审计性 metadata
```

## 实施步骤

```text
1. 建立 Phase 42 任务卡和索引。
2. 输出知识范围、L3 专题和跨分支边界。
3. 输出数据库核心表、RAG/vector storage、migration、audit ledger、lifecycle 契约。
4. 创建 34 条知识点采集矩阵和 ResearchIngestionTask 队列。
5. 导出知识范围审计 JSON，由外部 AI/人工先审计边界和数量。
6. 联网采集 P0 来源，生成候选知识包。
7. 导出候选 AI 审计包并运行质量门禁。
8. 按审计结果补证、回写、沉淀 formal reviewed/caveat_only。
9. 重建 knowledge_items.json 和 Vue3 fixture。
10. 验证 MCP/SearchLab/KnowledgeTree 检索、引用、阻断和降级。
11. 生成 Phase 42 验收报告。
```

## Definition of Done

```text
1. Phase 42 任务卡存在并登记到 docs/index_tasks.md 和 docs/tasks/README.md。
2. 上游 Phase 38/40/41 的边界已引用。
3. 任务卡明确输入、输出、契约、边界、存储、DoD 和测试。
4. 知识点规划明确 P0 28 条、P1 6 条。
5. 明确 PostgreSQL/关系库为 canonical store 的边界，Vector DB 只做 retrieval index。
6. 明确 LLM audit 不能写 final_gate，final_gate 必须 deterministic。
7. 明确所有交易 AI 决策必须带 audit_trace_id、版本绑定和可回放依据。
8. 明确本 Phase 不引入真实生产数据库，不执行不可逆迁移。
9. 涉及中文文档时以 UTF-8 读取和写入，无乱码。
```

## 测试与验收

```text
文档验收：
  - docs/index_tasks.md 能找到 Phase 42 和 CEK-TA-342 至 CEK-TA-352。
  - docs/tasks/README.md 能找到 Phase 42 任务卡。
  - docs/tasks/phase42_database_data_contract_storage_engineering.md 包含任务卡必备章节。

知识验收：
  - 后续知识候选必须有来源、适用范围、不适用场景、冲突状态和 review_status。
  - 不允许无来源或未消解冲突知识进入 reviewed。
  - 不允许 candidate/reviewed 自动升级 approved。
  - 不允许把数据库工程知识写成交易策略、买卖点、仓位或实盘执行建议。

运行时验收：
  - 后续 formal reviewed 入库后，MCP/SearchLab/KnowledgeTree 能按 canonical node 检索。
  - no-hit、无来源、冲突未消解时必须降级或阻断默认指导。

编码验收：
  - PowerShell 使用 UTF-8 读取检查。
  - 运行乱码门禁脚本或等效 UTF-8 检查。
```

## 风险与回滚

| 风险 | 影响 | 处理 |
| --- | --- | --- |
| 把 Phase 42 误解为真实数据库实施 | 可能提前引入外部依赖和迁移风险 | 本 Phase 只做知识、契约和候选采集，真实实施另开 Phase |
| Vector DB 被当事实主库 | 来源、审计和回放断链 | 强制 canonical store 与 retrieval index 分离 |
| LLM audit 写入 final_gate | 语言模型绕过 deterministic gate | 明确 LLM 只能写 audit result，final_gate 只接受 deterministic policy |
| 数据库知识混入 Trading 本体 | 知识树分类污染 | K 线、fill model、风控本体只引用，不归入 Phase 42 |
| 来源不足或技术版本过期 | 知识无法 reviewed | 保持 candidate 或 needs_more_evidence，不入正式索引 |
| 任务后续实现硬编码路径 | 外部项目无法迁移复用 | 所有脚本继续使用 resolver 或显式环境变量 |

回滚方式：

```text
1. 若任务卡分类不合适，回滚 docs/index_tasks.md、docs/tasks/README.md 和本任务卡新增内容。
2. 若后续候选生成有误，只回滚候选和审计包，不删除已审计正式知识。
3. 若 knowledge_tree 节点错误，先恢复上一个 knowledge_tree 版本并重建索引。
```

## 需要开发者确认的问题

```text
1. 是否确认 Phase 42 新增 AI Engineering 下数据库/数据契约/存储工程子分支。
2. 是否接受首批 34 条作为 Phase 42 知识点范围。
3. 是否确认本 Phase 只做知识采集和契约，不直接引入真实数据库实现。
4. 是否后续需要另起“外接项目数据库落地实施 Phase”，用于真实 PostgreSQL/Alembic/schema 代码。
```

## 状态更新要求

完成每个任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase42_database_data_contract_storage_engineering.md
```

如果新增契约、研究、审计或报告文档，还必须更新：

```text
docs/index_tasks.md 的文档入口
相关 Phase 报告
```
