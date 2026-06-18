# Phase 42 P1 候选知识联网采集记录

本文件记录 Phase 42 P1 6 条数据库/存储增强知识候选的来源、边界和审计状态。

## 全局边界

```text
1. P1 候选不创建真实数据库，不执行迁移，不启用 RLS/pgAudit，不引入外部服务依赖。
2. 候选不能作为 reviewed、approved、default guidance 或 hard gate。
3. 具体交易规则、K 线、fill model、仓位、止损止盈和实盘执行仍归 Trading Engineering。
```

## P42-P1-001 - phase42.pgvector_vs_qdrant_selection_boundary.v1

- statement: pgvector and Qdrant selection must be a storage-boundary decision: pgvector is suitable when vector retrieval should stay close to PostgreSQL metadata and transactional governance, while Qdrant is suitable when a dedicated vector service with payload filtering and operational scaling is justified; neither may replace the canonical source of truth.
- canonical_node_id: `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage`
- proposed_knowledge_id: `kb_ai_database_storage.phase42.pgvector_vs_qdrant_selection_boundary.v1`
- sources:
  - pgvector: Open-source vector similarity search for Postgres：https://github.com/pgvector/pgvector；pgvector documents vector storage and HNSW/IVFFlat indexes inside PostgreSQL, preserving SQL adjacency with relational metadata.
  - Qdrant Documentation: Indexing：https://qdrant.tech/documentation/manage-data/indexing/；Qdrant documents vector indexes and payload indexes, emphasizing combined vector and traditional indexing for filtered search.
  - Qdrant GitHub Repository：https://github.com/qdrant/qdrant；Qdrant describes itself as a vector similarity search engine and vector database with payload management and filtering support.

## P42-P1-002 - phase42.hnsw_vs_ivfflat_selection_boundary.v1

- statement: HNSW and IVFFlat selection must be based on measured latency, recall, memory, build-time and update-pattern tradeoffs; index type must not be selected by default without a benchmark tied to the retrieval workload.
- canonical_node_id: `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage`
- proposed_knowledge_id: `kb_ai_database_storage.phase42.hnsw_vs_ivfflat_selection_boundary.v1`
- sources:
  - pgvector: Open-source vector similarity search for Postgres：https://github.com/pgvector/pgvector；pgvector documents vector storage and HNSW/IVFFlat indexes inside PostgreSQL, preserving SQL adjacency with relational metadata.
  - Qdrant Documentation: Indexing：https://qdrant.tech/documentation/manage-data/indexing/；Qdrant documents vector indexes and payload indexes, emphasizing combined vector and traditional indexing for filtered search.
  - Qdrant Documentation: Search：https://qdrant.tech/documentation/search/search/；Qdrant search documentation recommends payload indexes for fields used in filtered vector search.

## P42-P1-003 - phase42.qdrant_payload_index_metadata_filter_rule.v1

- statement: Qdrant payload indexes should be created for metadata fields that are repeatedly used in filtered retrieval, and every filtered RAG query must preserve source provenance, formal_knowledge_id and version metadata.
- canonical_node_id: `kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage`
- proposed_knowledge_id: `kb_ai_database_storage.phase42.qdrant_payload_index_metadata_filter_rule.v1`
- sources:
  - Qdrant Documentation: Indexing：https://qdrant.tech/documentation/manage-data/indexing/；Qdrant documents vector indexes and payload indexes, emphasizing combined vector and traditional indexing for filtered search.
  - Qdrant Documentation: Search：https://qdrant.tech/documentation/search/search/；Qdrant search documentation recommends payload indexes for fields used in filtered vector search.
  - Qdrant Documentation: Filtering：https://qdrant.tech/documentation/search/filtering/；Qdrant filtering documentation explains payload conditions, nested object filters and metadata-based retrieval constraints.

## P42-P1-004 - phase42.feast_adoption_boundary_after_offline_online_parity_pressure.v1

- statement: Feast should be introduced only when offline/online feature parity, point-in-time retrieval, feature reuse and serving latency create enough pressure to justify a feature store; simpler manifest-based pipelines remain acceptable before that threshold.
- canonical_node_id: `kt.ai_engineering.database_storage_engineering.feature_store_storage`
- proposed_knowledge_id: `kb_ai_database_storage.phase42.feast_adoption_boundary_after_offline_online_parity_pressure.v1`
- sources:
  - Feast Documentation: Introduction：https://docs.feast.dev/；Feast describes an open-source feature store for defining, managing, validating and serving features for production AI/ML.
  - Feast Documentation: Point-in-time joins：https://docs.feast.dev/getting-started/concepts/point-in-time-joins；Feast documents point-in-time correct joins that reproduce feature state at a specific past timestamp.
  - Feast Documentation: Feature retrieval：https://docs.feast.dev/getting-started/concepts/feature-retrieval；Feast feature retrieval covers historical features for training and online features for low-latency serving.

## P42-P1-005 - phase42.mlflow_registry_adoption_boundary_after_release_manifest_complexity.v1

- statement: MLflow Model Registry should be introduced when model versions, aliases, tags, metadata, release manifests and deployment organization exceed simple file-based release tracking; it must complement, not replace, scorer/calibrator/prompt/RAG index version binding.
- canonical_node_id: `kt.ai_engineering.database_storage_engineering.model_registry_release_storage`
- proposed_knowledge_id: `kb_ai_database_storage.phase42.mlflow_registry_adoption_boundary_after_release_manifest_complexity.v1`
- sources:
  - MLflow Model Registry：https://mlflow.org/docs/latest/ml/model-registry/；MLflow Model Registry documents registered models, versions, aliases, tags and model metadata.
  - MLflow Model Registry Workflows：https://mlflow.org/docs/latest/ml/model-registry/workflow/；MLflow workflow documentation covers registering models, managing versions, applying aliases and organizing releases.
  - DVC: Data Version Control：https://dvc.org/；DVC describes data and ML artifact versioning patterns that complement model registry release manifests.

## P42-P1-006 - phase42.rls_pgaudit_adoption_boundary.v1

- statement: PostgreSQL RLS and pgAudit should be adopted when row-level access boundaries, tenant/project isolation or audit-grade database activity tracing are required; they require explicit policy design, performance review and log-retention planning before production use.
- canonical_node_id: `kt.ai_engineering.database_storage_engineering.security_privacy_access_control`
- proposed_knowledge_id: `kb_ai_database_storage.phase42.rls_pgaudit_adoption_boundary.v1`
- sources:
  - PostgreSQL 18 Documentation: Row Security Policies：https://www.postgresql.org/docs/current/ddl-rowsecurity.html；PostgreSQL row security policies restrict which rows users can access or modify through table policies.
  - PostgreSQL 18 Documentation: CREATE POLICY：https://www.postgresql.org/docs/current/sql-createpolicy.html；CREATE POLICY defines row-level security policies and requires row-level security to be enabled on the table.
  - PostgreSQL Audit Extension：https://pgaudit.org/；pgAudit provides detailed session and object audit logging via the PostgreSQL logging facility.
  - pgAudit GitHub Repository：https://github.com/pgaudit/pgaudit；pgAudit documents audit logging intended to support government, financial or ISO certification audit needs.
  - AWS Documentation: Using pgAudit to log database activity：https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.pgaudit.html；AWS documents using pgAudit on RDS PostgreSQL to track changes, users and database/table activity for audit requirements.

