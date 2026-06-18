# Phase 42 ResearchIngestionTask 队列

## 队列目标

本队列承接 `phase42_database_storage_collection_matrix.md`，用于后续联网采集、候选知识生成、AI 审计包导出和 formal reviewed/caveat_only 沉淀。

统一边界：

```text
1. 本队列只采集数据库/数据契约/存储工程知识。
2. 不创建真实数据库，不执行迁移。
3. 不采集 K 线、fill model、仓位、止损止盈、实盘执行本体。
4. 不把 reviewed 自动升级 approved/default guidance/hard gate。
```

## P0 队列

| Research Task ID | Topic ID | 优先级 | canonical node | claim_type | storage_role | 查询目标 | source_types | min_sources | acceptance_gate | forbidden_claims | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P42-RT-001 | P42-P0-001 | P0 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | storage_boundary_rule | canonical_store | 搜索 canonical store、vector DB 事实主库边界、PostgreSQL 作为事实存储与向量索引分离 | official_doc, framework_doc, engineering_article | 3 | 必须证明 canonical records 与 retrieval index 分离 | 不得让 Vector DB 作为唯一事实来源 | todo |
| P42-RT-002 | P42-P0-002 | P0 | `kt.ai_engineering.database_storage_engineering.runtime_observability_trace` | traceability_rule | audit_ledger | 搜索 audit trace、decision logging、request id、交易 AI scoring/gating 决策追踪 | official_doc, governance_framework, engineering_article | 3 | 必须要求 scoring/gating 决策带 audit_trace_id | 不允许无 trace 决策 | todo |
| P42-RT-003 | P42-P0-003 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append_only_rule | audit_ledger | 搜索 append-only ledger、audit log、final decision record、防篡改日志 | official_doc, security_standard, governance_framework | 3 | 必须要求 final_gate append-only | 不允许 LLM 写 final_gate | todo |
| P42-RT-004 | P42-P0-004 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append_only_rule | audit_ledger | 搜索 score result versioning、model output logging、append-only decision evidence | official_doc, engineering_article, governance_framework | 3 | 必须要求 score_result 带版本且 append-only | 不允许 raw score 直接 gate | todo |
| P42-RT-005 | P42-P0-005 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | leakage_boundary_rule | manifest_store | 搜索 decision-time feature availability、snapshot isolation、point-in-time feature 可见性 | official_doc, research_paper, engineering_article | 3 | 必须阻断未来字段进入 trade_candidate | 不采集具体交易信号 | todo |
| P42-RT-006 | P42-P0-006 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | leakage_boundary_rule | manifest_store | 搜索 outcome leakage、label leakage、post-event data leakage | official_doc, research_paper, engineering_article | 3 | 必须要求 outcome 与 feature 隔离 | 不允许 outcome 反写特征 | todo |
| P42-RT-007 | P42-P0-007 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | data_contract_rule | manifest_store | 搜索 feedback/outcome/label separation、ML data contract、label governance | official_doc, governance_framework, engineering_article | 3 | 必须分离 feedback、outcome、label | 不合并成单一结果字段 | todo |
| P42-RT-008 | P42-P0-008 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | label_lineage_rule | manifest_store | 搜索 label policy version、label source、label lineage、dataset governance | official_doc, governance_framework, engineering_article | 3 | 标签必须记录 policy version 和 source | 不允许无来源标签 | todo |
| P42-RT-009 | P42-P0-009 | P0 | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | version_binding_rule | registry | 搜索 model registry、prompt version、RAG index version、release manifest 绑定 | official_doc, governance_framework, engineering_article | 3 | 必须绑定 model/prompt/rag index 版本 | 不允许不可回放发布 | todo |
| P42-RT-010 | P42-P0-010 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | citation_storage_rule | vector_index | 搜索 LLM audit citation、source grounding、RAG source versioning | official_doc, standard_doc, engineering_article | 3 | LLM audit 必须绑定 citation/source/version | 无来源不得默认指导 | todo |
| P42-RT-011 | P42-P0-011 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | provenance_rule | vector_index | 搜索 vector search source provenance、metadata payload、formal knowledge 回链 | official_doc, framework_doc, engineering_article | 3 | vector hit 必须回链 source 和 formal knowledge id | 向量命中不等于 approved | todo |
| P42-RT-012 | P42-P0-012 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | chunk_storage_rule | vector_index | 搜索 RAG chunk metadata、source_uri、license、hash、chunk version | official_doc, framework_doc, legal_policy | 3 | chunk 必须保存 source/license/hash/version | 不保存超版权长引用 | todo |
| P42-RT-013 | P42-P0-013 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | embedding_version_rule | vector_index | 搜索 embedding model version、index rebuild、vector metadata versioning | official_doc, framework_doc, engineering_article | 3 | embedding 必须保存 model version | 不允许版本不明索引 | todo |
| P42-RT-014 | P42-P0-014 | P0 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | constraint_rule | canonical_store | 搜索 PostgreSQL constraints、unique/check/foreign key、高价值不变量 | official_doc, engineering_article | 2 | 必须用数据库约束保护核心不变量 | 不只靠应用层 if | todo |
| P42-RT-015 | P42-P0-015 | P0 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | idempotency_rule | canonical_store | 搜索 idempotency key、unique constraint、防重复写入 | official_doc, engineering_article | 2 | 必须给高价值表唯一键或幂等键 | 不允许重复 gate 事件 | todo |
| P42-RT-016 | P42-P0-016 | P0 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | migration_rule | canonical_store | 搜索 Alembic migration、reversible migration、migration review | official_doc, engineering_article | 2 | migration 必须 review 且可回滚 | 不执行不可逆迁移 | todo |
| P42-RT-017 | P42-P0-017 | P0 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | migration_rule | canonical_store | 搜索 Alembic autogenerate caveats、manual review、schema diff 风险 | official_doc, engineering_article | 2 | autogenerate 只能辅助 | 不自动应用 | todo |
| P42-RT-018 | P42-P0-018 | P0 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | compatibility_rule | canonical_store | 搜索 schema compatibility、backward compatibility、migration rollout | official_doc, engineering_article, governance_framework | 3 | schema_version 变更需兼容性检查 | 不破坏回放 | todo |
| P42-RT-019 | P42-P0-019 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | time_semantics_rule | manifest_store | 搜索 event time、decision time、ingestion time、label time 分离 | official_doc, research_paper, engineering_article | 3 | 必须区分四类时间 | 不混用业务时间 | todo |
| P42-RT-020 | P42-P0-020 | P0 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | point_in_time_rule | feature_store | 搜索 point-in-time correctness、feature store training dataset、防泄漏 join | official_doc, research_paper, framework_doc | 3 | 训练数据必须 point-in-time correct | 不允许未来特征 | todo |
| P42-RT-021 | P42-P0-021 | P0 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | feature_manifest_rule | feature_store | 搜索 feature schema hash、feature manifest、feature lineage | official_doc, framework_doc, engineering_article | 3 | feature snapshot 必须带 schema hash | 不允许 schema 不明 | todo |
| P42-RT-022 | P42-P0-022 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | dataset_manifest_rule | manifest_store | 搜索 dataset hash、dataset snapshot、reproducible dataset、data versioning | official_doc, governance_framework, engineering_article | 3 | dataset manifest 必须带 dataset_hash | 不允许不可复现训练集 | todo |
| P42-RT-023 | P42-P0-023 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | ledger_schema_rule | audit_ledger | 搜索 audit log actor/reason/before-after/trace id、approval trail | security_standard, governance_framework, engineering_article | 3 | final_gate ledger 必须记录 actor/reason/before_after/trace_id | 不允许无责任主体 | todo |
| P42-RT-024 | P42-P0-024 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | tamper_evidence_rule | audit_ledger | 搜索 tamper-evident logs、hash chain、row_hash/prev_hash | security_standard, engineering_article | 2 | audit ledger 需要防篡改证据 | 不覆盖审计事件 | todo |
| P42-RT-025 | P42-P0-025 | P0 | `kt.ai_engineering.database_storage_engineering.data_lifecycle_retention` | lifecycle_rule | backup_restore | 搜索 retention policy、archive、delete、audit replay continuity | official_doc, governance_framework, security_standard | 3 | 删除/归档不得破坏审计回放 | 不允许断链 | todo |
| P42-RT-026 | P42-P0-026 | P0 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | secret_boundary_rule | canonical_store | 搜索 secret management、PII redaction、database credential storage anti-pattern | security_standard, official_doc | 2 | 密钥和私有账户字段不得入业务表 | 不保存 secret | todo |
| P42-RT-027 | P42-P0-027 | P0 | `kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery` | backup_restore_rule | backup_restore | 搜索 backup restore drill、RPO/RTO、disaster recovery verification | official_doc, security_standard, engineering_article | 3 | backup 必须有 restore drill | 不把配置等同恢复能力 | todo |
| P42-RT-028 | P42-P0-028 | P0 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | permission_audit_rule | canonical_store | 搜索 database permission audit、least privilege、write action audit | security_standard, official_doc, governance_framework | 3 | DB 权限和写动作必须可审计 | 不给 MCP 默认写权限 | todo |

## P1 队列

| Research Task ID | Topic ID | 优先级 | canonical node | claim_type | storage_role | 查询目标 | source_types | min_sources | acceptance_gate | forbidden_claims | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P42-RT-029 | P42-P1-001 | P1 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | backend_selection_rule | vector_index | 搜索 pgvector vs Qdrant 选型边界、运维、过滤、扩展、审计 | official_doc, framework_doc, engineering_article | 3 | 必须按规模、filter、延迟和运维边界选择 | 不预设唯一答案 | todo |
| P42-RT-030 | P42-P1-002 | P1 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | index_selection_rule | vector_index | 搜索 HNSW vs IVFFlat、召回、延迟、内存、重建成本 | official_doc, framework_doc, engineering_article | 3 | 必须评估召回/延迟/内存/重建 | 不只看速度 | todo |
| P42-RT-031 | P42-P1-003 | P1 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | metadata_filter_rule | vector_index | 搜索 Qdrant payload index、metadata filter、review_status/machine_gate filter | official_doc, framework_doc | 2 | 必须支持 metadata 过滤 | 不绕过 machine_gate | todo |
| P42-RT-032 | P42-P1-004 | P1 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | platform_boundary_rule | feature_store | 搜索 Feast 引入条件、offline/online parity、feature registry | official_doc, engineering_article | 2 | 明确 Feast 条件引入 | POC 不强制引入 | todo |
| P42-RT-033 | P42-P1-005 | P1 | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | platform_boundary_rule | registry | 搜索 MLflow registry、model versioning、artifact lineage、release manifest | official_doc, engineering_article | 2 | 明确 MLflow 条件引入 | 不默认引入服务 | todo |
| P42-RT-034 | P42-P1-006 | P1 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | platform_boundary_rule | canonical_store | 搜索 PostgreSQL RLS、pgAudit、审计扩展和权限治理边界 | official_doc, security_standard | 2 | 明确 RLS/pgAudit 条件引入 | 不替代应用权限审计 | todo |

## 执行顺序

```text
1. 先采集 P0-001 至 P0-013：canonical store、trace、append-only、time/label leakage、RAG/vector provenance。
2. 再采集 P0-014 至 P0-028：constraint、idempotency、migration、manifest、ledger、retention、security、backup。
3. 最后采集 P1-001 至 P1-006：pgvector/Qdrant、HNSW/IVFFlat、Feast、MLflow、RLS/pgAudit 条件引入。
```
