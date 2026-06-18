# Phase 42 P0 候选知识来源采集记录

生成日期：2026-06-11

## 结论

本轮按 Phase 42 P0 矩阵生成候选知识 28 条，跳过已存在候选 0 条；当前 P0 规划总数为 28 条。

本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。

## 主要来源族

| 来源族 | 用途 |
| --- | --- |
| PostgreSQL 官方文档 | constraints、MVCC、transaction isolation、backup/PITR 和 canonical store 关系库边界 |
| Alembic 官方文档 | migration、autogenerate candidate migration、review 和 rollback 边界 |
| Feast 官方文档 | point-in-time joins、feature store、offline/online feature parity |
| MLflow / DVC | model registry、版本、alias/tag、dataset hash 和可复现数据管理 |
| pgvector / Qdrant | vector index、HNSW/IVFFlat、payload index、metadata filter 和 source provenance |
| NIST / OWASP | log management、audit trail、append-only、防篡改、权限和安全监控 |
| OpenTelemetry | request/trace context propagation，用于 audit_trace_id 和跨服务追踪 |

## P0 主题

| topic_id | canonical_node_id | claim_type | storage_role | 来源数 |
| --- | --- | --- | --- | ---: |
| P42-P0-001 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | storage_boundary_rule | canonical_store | 4 |
| P42-P0-002 | `kt.ai_engineering.database_storage_engineering.runtime_observability_trace` | traceability_rule | audit_ledger | 3 |
| P42-P0-003 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append_only_rule | audit_ledger | 3 |
| P42-P0-004 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | append_only_rule | audit_ledger | 3 |
| P42-P0-005 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | leakage_boundary_rule | manifest_store | 3 |
| P42-P0-006 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | leakage_boundary_rule | manifest_store | 3 |
| P42-P0-007 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | data_contract_rule | manifest_store | 3 |
| P42-P0-008 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | label_lineage_rule | manifest_store | 3 |
| P42-P0-009 | `kt.ai_engineering.database_storage_engineering.model_registry_release_storage` | version_binding_rule | registry | 3 |
| P42-P0-010 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | citation_storage_rule | vector_index | 3 |
| P42-P0-011 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | provenance_rule | vector_index | 3 |
| P42-P0-012 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | chunk_storage_rule | vector_index | 3 |
| P42-P0-013 | `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage` | embedding_version_rule | vector_index | 3 |
| P42-P0-014 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | constraint_rule | canonical_store | 2 |
| P42-P0-015 | `kt.ai_engineering.database_storage_engineering.relational_core_schema` | idempotency_rule | canonical_store | 2 |
| P42-P0-016 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | migration_rule | canonical_store | 2 |
| P42-P0-017 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | migration_rule | canonical_store | 2 |
| P42-P0-018 | `kt.ai_engineering.database_storage_engineering.migration_versioning` | compatibility_rule | canonical_store | 3 |
| P42-P0-019 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | time_semantics_rule | manifest_store | 3 |
| P42-P0-020 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | point_in_time_rule | feature_store | 3 |
| P42-P0-021 | `kt.ai_engineering.database_storage_engineering.feature_store_storage` | feature_manifest_rule | feature_store | 3 |
| P42-P0-022 | `kt.ai_engineering.database_storage_engineering.data_contract_lineage` | dataset_manifest_rule | manifest_store | 3 |
| P42-P0-023 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | ledger_schema_rule | audit_ledger | 3 |
| P42-P0-024 | `kt.ai_engineering.database_storage_engineering.audit_log_ledger` | tamper_evidence_rule | audit_ledger | 2 |
| P42-P0-025 | `kt.ai_engineering.database_storage_engineering.data_lifecycle_retention` | lifecycle_rule | backup_restore | 3 |
| P42-P0-026 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | secret_boundary_rule | canonical_store | 2 |
| P42-P0-027 | `kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery` | backup_restore_rule | backup_restore | 3 |
| P42-P0-028 | `kt.ai_engineering.database_storage_engineering.security_privacy_access_control` | permission_audit_rule | canonical_store | 3 |

## 边界

本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值、买卖点、仓位或交易所执行适配器本体知识。这些内容仍归 Trading Engineering。

本轮没有创建真实数据库、没有执行 migration、没有改变 MCP/SearchLab 写权限。

