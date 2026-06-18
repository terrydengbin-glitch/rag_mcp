# Phase 42 Database / Data Contract / Storage Engineering 采集矩阵

## 采集目标

本矩阵把 Phase 42 的数据库、数据契约、审计日志、向量检索存储、迁移、备份恢复和生命周期治理知识拆成 34 条可联网采集、可审计、可入库的候选知识点。

本矩阵只定义知识采集范围，不创建真实数据库，不执行迁移。

## 分区与节点

```text
primary_partition: KB_AI_26_DATABASE_STORAGE
primary_l2_node: kt.ai_engineering.database_storage_engineering
review_target: formal reviewed / caveat_only
approved_allowed: false
default_guidance_allowed: false
hard_gate_allowed: false
```

## P0 知识点

| Topic ID | 优先级 | canonical node | claim_type | storage_role | 知识点 | 期望来源 | 最少来源数 | 边界 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P42-P0-001 | P0 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | storage_boundary_rule | canonical_store | canonical records must live in PostgreSQL, not vector DB | official_doc, framework_doc, engineering_article | 3 | 不把 Vector DB 当事实主库 |
| P42-P0-002 | P0 | `kt.ai_engineering.database_storage_engineering.runtime_observability_trace` | traceability_rule | audit_ledger | every scoring/gating decision must have audit_trace_id | official_doc, governance_framework, engineering_article | 3 | 不允许无 trace 决策 |
| P42-P0-003 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append_only_rule | audit_ledger | final_gate decision must be append-only | official_doc, security_standard, governance_framework | 3 | LLM 不能写 final_gate |
| P42-P0-004 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append_only_rule | audit_ledger | score_result must be versioned append-only | official_doc, engineering_article, governance_framework | 3 | raw score 不能直接 gate |
| P42-P0-005 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | leakage_boundary_rule | manifest_store | trade_candidate snapshot must contain only decision-time visible fields | official_doc, research_paper, engineering_article | 3 | 不保存未来结果 |
| P42-P0-006 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | leakage_boundary_rule | manifest_store | outcome must be isolated from input features | official_doc, research_paper, engineering_article | 3 | 防标签泄漏 |
| P42-P0-007 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | data_contract_rule | manifest_store | feedback/outcome/label must be separated | official_doc, governance_framework, engineering_article | 3 | 不合并成一个结果字段 |
| P42-P0-008 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | label_lineage_rule | manifest_store | labels must record label_policy_version and label_source | official_doc, governance_framework, engineering_article | 3 | 不允许无来源标签 |
| P42-P0-009 | P0 | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | version_binding_rule | registry | model_version/prompt_version/rag_index_version must be recorded together | official_doc, governance_framework, engineering_article | 3 | 不允许不可回放发布 |
| P42-P0-010 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | citation_storage_rule | vector_index | LLM audit output must bind citations/source/version | official_doc, standard_doc, engineering_article | 3 | 无来源必须降级 |
| P42-P0-011 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | provenance_rule | vector_index | vector search result must link back to source document and formal knowledge id | official_doc, framework_doc, engineering_article | 3 | 向量命中不等于 approved |
| P42-P0-012 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | chunk_storage_rule | vector_index | RAG chunks must store source_uri/license/hash/chunk_version | official_doc, framework_doc, legal_policy | 3 | 不保存超版权长引用 |
| P42-P0-013 | P0 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | embedding_version_rule | vector_index | embedding_model_version must be stored with vector records | official_doc, framework_doc, engineering_article | 3 | embedding 版本变化需重建 |
| P42-P0-014 | P0 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | constraint_rule | canonical_store | PostgreSQL constraints must enforce high-value invariants | official_doc, engineering_article | 2 | 不只靠应用层 if |
| P42-P0-015 | P0 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | idempotency_rule | canonical_store | high-value tables must use unique constraints and idempotency keys | official_doc, engineering_article | 2 | 防重复写入 |
| P42-P0-016 | P0 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | migration_rule | canonical_store | Alembic migration must be reviewed and reversible | official_doc, engineering_article | 2 | 不执行不可逆迁移 |
| P42-P0-017 | P0 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | migration_rule | canonical_store | autogenerate migration must not be auto-applied | official_doc, engineering_article | 2 | autogenerate 只辅助 |
| P42-P0-018 | P0 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | compatibility_rule | canonical_store | schema_version change must trigger compatibility check | official_doc, engineering_article, governance_framework | 3 | 不破坏旧数据回放 |
| P42-P0-019 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | time_semantics_rule | manifest_store | event_time/decision_time/ingestion_time/label_time must be separated | official_doc, research_paper, engineering_article | 3 | 不混用业务时间 |
| P42-P0-020 | P0 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | point_in_time_rule | feature_store | point-in-time correctness is required for training datasets | official_doc, research_paper, framework_doc | 3 | 防训练/评估泄漏 |
| P42-P0-021 | P0 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | feature_manifest_rule | feature_store | feature_snapshot_manifest must store feature_schema_hash | official_doc, framework_doc, engineering_article | 3 | 不允许无 schema hash |
| P42-P0-022 | P0 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | dataset_manifest_rule | manifest_store | dataset_snapshot_manifest must store dataset_hash | official_doc, governance_framework, engineering_article | 3 | 数据集必须可复现 |
| P42-P0-023 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | ledger_schema_rule | audit_ledger | final_gate ledger must store actor/reason/before_after/trace_id | security_standard, governance_framework, engineering_article | 3 | 不允许无责任主体 |
| P42-P0-024 | P0 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | tamper_evidence_rule | audit_ledger | audit ledger must support row_hash/prev_hash or equivalent tamper evidence | security_standard, engineering_article | 2 | 不允许覆盖审计事件 |
| P42-P0-025 | P0 | `kt.ai_engineering.database_storage_engineering.data_lifecycle_retention` | lifecycle_rule | backup_restore | delete/retention policy must not break audit replay | official_doc, governance_framework, security_standard | 3 | 删除不能断链 |
| P42-P0-026 | P0 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | secret_boundary_rule | canonical_store | database credentials/secrets/private account fields must not be stored in business tables | security_standard, official_doc | 2 | 不保存密钥 |
| P42-P0-027 | P0 | `kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery` | backup_restore_rule | backup_restore | backup restore must be tested, not only configured | official_doc, security_standard, engineering_article | 3 | restore drill 必须有证据 |
| P42-P0-028 | P0 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | permission_audit_rule | canonical_store | DB permissions and write actions must be auditable | security_standard, official_doc, governance_framework | 3 | 写动作必须可追踪 |

## P1 知识点

| Topic ID | 优先级 | canonical node | claim_type | storage_role | 知识点 | 期望来源 | 最少来源数 | 边界 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P42-P1-001 | P1 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | backend_selection_rule | vector_index | pgvector vs Qdrant selection boundary | official_doc, framework_doc, engineering_article | 3 | 不预设唯一答案 |
| P42-P1-002 | P1 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | index_selection_rule | vector_index | HNSW vs IVFFlat selection boundary | official_doc, framework_doc, engineering_article | 3 | 必须评估召回/延迟/内存 |
| P42-P1-003 | P1 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | metadata_filter_rule | vector_index | Qdrant payload index / metadata filter rule | official_doc, framework_doc | 2 | 必须过滤 machine_gate/conflict |
| P42-P1-004 | P1 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | platform_boundary_rule | feature_store | Feast adoption boundary after offline/online parity pressure | official_doc, engineering_article | 2 | POC 不强制引入 |
| P42-P1-005 | P1 | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | platform_boundary_rule | registry | MLflow registry adoption boundary after release manifest complexity | official_doc, engineering_article | 2 | 不默认引入服务 |
| P42-P1-006 | P1 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | platform_boundary_rule | canonical_store | RLS / pgAudit adoption boundary | official_doc, security_standard | 2 | 不替代应用权限审计 |

## 接受门禁

```text
1. 每条候选必须至少有 expected_sources 中的最少来源数。
2. 必须说明 applicability 和 not_applicable_when。
3. 必须声明不生成交易建议、买卖点、仓位、止损止盈或实盘执行。
4. 必须声明 reviewed/caveat_only 不等于 approved/default guidance。
5. 如涉及真实数据库实现，必须降级为 implementation_followup，不在本 Phase 直接执行。
```
