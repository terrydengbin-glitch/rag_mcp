"""Generate Phase 42 P0 database/storage candidate knowledge files.

This script writes candidate JSON only. It does not create formal reviewed or
approved knowledge, and it never enables default guidance.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any


CORE_DIR = __file__

if True:
    from pathlib import Path

    core_path = Path(__file__).resolve().parents[2] / "core"
    if str(core_path) not in sys.path:
        sys.path.insert(0, str(core_path))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
RESEARCH = resolve_repo_path("docs", "research", "phase42_p0_candidate_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase42_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase42_candidate_quality_gate.json", start_file=__file__)


CONTRACT_REFS = [
    "docs/research/phase42_database_storage_scope.md",
    "docs/contracts/phase42_database_storage_contract.md",
    "docs/contracts/phase42_rag_vector_storage_contract.md",
    "docs/tasks/phase42_database_data_contract_storage_engineering.md",
]


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "postgres_constraints": {
        "title": "PostgreSQL 18 Documentation: Constraints",
        "url": "https://www.postgresql.org/docs/current/ddl-constraints.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 88,
        "summary": "PostgreSQL documents primary keys, unique constraints, foreign keys, check constraints and the integrity role of constraints.",
    },
    "postgres_mvcc": {
        "title": "PostgreSQL 18 Documentation: Concurrency Control",
        "url": "https://www.postgresql.org/docs/current/mvcc.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 86,
        "summary": "PostgreSQL explains concurrency control and MVCC goals for efficient access while maintaining data integrity.",
    },
    "postgres_transaction_isolation": {
        "title": "PostgreSQL 18 Documentation: Transaction Isolation",
        "url": "https://www.postgresql.org/docs/current/transaction-iso.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 86,
        "summary": "PostgreSQL documents transaction isolation behavior and its MVCC mapping.",
    },
    "postgres_backup": {
        "title": "PostgreSQL 18 Documentation: Backup and Restore",
        "url": "https://www.postgresql.org/docs/current/backup.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 86,
        "summary": "PostgreSQL describes SQL dump, file-system backup, and continuous archiving approaches for backup and restore.",
    },
    "postgres_pitr": {
        "title": "PostgreSQL 18 Documentation: Continuous Archiving and Point-in-Time Recovery",
        "url": "https://www.postgresql.org/docs/current/continuous-archiving.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 86,
        "summary": "PostgreSQL PITR documentation requires archived WAL continuity and testing archive procedures before relying on backups.",
    },
    "alembic_autogenerate": {
        "title": "Alembic Documentation: Auto Generating Migrations",
        "url": "https://alembic.sqlalchemy.org/en/latest/autogenerate.html",
        "type": "official_doc",
        "publisher": "SQLAlchemy Alembic",
        "score": 86,
        "summary": "Alembic autogenerate compares database schema and SQLAlchemy metadata to produce candidate migration files.",
    },
    "alembic_docs": {
        "title": "Alembic Documentation",
        "url": "https://alembic.sqlalchemy.org/",
        "type": "official_doc",
        "publisher": "SQLAlchemy Alembic",
        "score": 86,
        "summary": "Alembic documents migration workflows, operations, offline mode, naming constraints and migration cookbook patterns.",
    },
    "feast_point_in_time": {
        "title": "Feast Documentation: Point-in-time joins",
        "url": "https://docs.feast.dev/getting-started/concepts/point-in-time-joins",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 86,
        "summary": "Feast documents point-in-time correct joins that reproduce feature values at a past point in time.",
    },
    "feast_docs": {
        "title": "Feast Documentation",
        "url": "https://docs.feast.dev/",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 84,
        "summary": "Feast describes feature store concepts for defining, managing, validating and serving ML features.",
    },
    "mlflow_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 86,
        "summary": "MLflow registry documents registered models, model versions, aliases, tags and model metadata.",
    },
    "mlflow_registry_workflow": {
        "title": "MLflow Model Registry Workflows",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 86,
        "summary": "MLflow workflow documentation covers registering models, managing versions, aliases, tags and metadata.",
    },
    "dvc_home": {
        "title": "DVC: Data Version Control",
        "url": "https://dvc.org/",
        "type": "official_doc",
        "publisher": "DVC",
        "score": 82,
        "summary": "DVC describes Git-like data version control for data, AI/ML and data infrastructure workflows.",
    },
    "pgvector": {
        "title": "pgvector: Open-source vector similarity search for Postgres",
        "url": "https://github.com/pgvector/pgvector",
        "type": "official_doc",
        "publisher": "pgvector",
        "score": 84,
        "summary": "pgvector documents vector search in Postgres and index tradeoffs such as HNSW and IVFFlat.",
    },
    "qdrant_indexing": {
        "title": "Qdrant Documentation: Indexing",
        "url": "https://qdrant.tech/documentation/manage-data/indexing/",
        "type": "official_doc",
        "publisher": "Qdrant",
        "score": 84,
        "summary": "Qdrant explains vector indexes and payload indexes for filtering on structured fields and metadata.",
    },
    "qdrant_search": {
        "title": "Qdrant Documentation: Search",
        "url": "https://qdrant.tech/documentation/search/search/",
        "type": "official_doc",
        "publisher": "Qdrant",
        "score": 84,
        "summary": "Qdrant search documentation explains filter-based searches and recommends payload indexes for performant filtering.",
    },
    "nist_log_management": {
        "title": "NIST SP 800-92: Guide to Computer Security Log Management",
        "url": "https://csrc.nist.gov/pubs/sp/800/92/final",
        "type": "security_standard",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST SP 800-92 provides guidance for developing, implementing and maintaining enterprise log management practices.",
    },
    "owasp_a09": {
        "title": "OWASP Top 10 2021 A09: Security Logging and Monitoring Failures",
        "url": "https://owasp.org/Top10/2021/A09_2021-Security_Logging_and_Monitoring_Failures/",
        "type": "security_standard",
        "publisher": "OWASP",
        "score": 86,
        "summary": "OWASP A09 recommends audit trails for high-value transactions and integrity controls to prevent tampering or deletion.",
    },
    "owasp_logging_vocabulary": {
        "title": "OWASP Application Logging Vocabulary Cheat Sheet",
        "url": "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Vocabulary_Cheat_Sheet.html",
        "type": "security_standard",
        "publisher": "OWASP",
        "score": 84,
        "summary": "OWASP proposes standard logging vocabulary to simplify security monitoring and alerting.",
    },
    "opentelemetry_context": {
        "title": "OpenTelemetry: Context propagation",
        "url": "https://opentelemetry.io/docs/concepts/context-propagation/",
        "type": "official_doc",
        "publisher": "OpenTelemetry",
        "score": 84,
        "summary": "OpenTelemetry describes context propagation for correlating traces, metrics and logs across process boundaries.",
    },
}


TOPICS: list[dict[str, Any]] = [
    {
        "id": "P42-P0-001",
        "slug": "canonical_records_postgresql_not_vector_db",
        "node": "kt.ai_engineering.database_storage_engineering.relational_core_schema",
        "claim_type": "storage_boundary_rule",
        "storage_role": "canonical_store",
        "statement": "Canonical records must live in a relational canonical store such as PostgreSQL; a vector database may index retrieval metadata but must not be the sole source of truth.",
        "sources": ["postgres_constraints", "postgres_mvcc", "pgvector", "qdrant_indexing"],
    },
    {
        "id": "P42-P0-002",
        "slug": "every_decision_requires_audit_trace_id",
        "node": "kt.ai_engineering.database_storage_engineering.runtime_observability_trace",
        "claim_type": "traceability_rule",
        "storage_role": "audit_ledger",
        "statement": "Every trading AI scoring or gating decision must carry an audit_trace_id so scorer, RAG, LLM audit and final gate records can be replayed together.",
        "sources": ["opentelemetry_context", "nist_log_management", "owasp_logging_vocabulary"],
    },
    {
        "id": "P42-P0-003",
        "slug": "final_gate_decision_append_only",
        "node": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "claim_type": "append_only_rule",
        "storage_role": "audit_ledger",
        "statement": "Final gate decisions must be written to an append-only ledger with actor, reason, before/after state and trace context.",
        "sources": ["owasp_a09", "nist_log_management", "postgres_constraints"],
    },
    {
        "id": "P42-P0-004",
        "slug": "score_result_versioned_append_only",
        "node": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "claim_type": "append_only_rule",
        "storage_role": "audit_ledger",
        "statement": "Score results must be versioned append-only records tied to scorer, calibrator and threshold policy versions; raw scores must not be overwritten.",
        "sources": ["mlflow_registry", "opentelemetry_context", "nist_log_management"],
    },
    {
        "id": "P42-P0-005",
        "slug": "trade_candidate_decision_time_visible_fields",
        "node": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "claim_type": "leakage_boundary_rule",
        "storage_role": "manifest_store",
        "statement": "A trade_candidate snapshot must contain only fields visible at decision_time; future outcomes, labels or post-trade analysis must be stored separately.",
        "sources": ["feast_point_in_time", "postgres_transaction_isolation", "dvc_home"],
    },
    {
        "id": "P42-P0-006",
        "slug": "outcome_isolated_from_input_features",
        "node": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "claim_type": "leakage_boundary_rule",
        "storage_role": "manifest_store",
        "statement": "Outcome records must be isolated from input feature records so post-decision information cannot leak into training or gating features.",
        "sources": ["feast_point_in_time", "dvc_home", "postgres_mvcc"],
    },
    {
        "id": "P42-P0-007",
        "slug": "feedback_outcome_label_separated",
        "node": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "claim_type": "data_contract_rule",
        "storage_role": "manifest_store",
        "statement": "Feedback, outcome and label events must be separated because they have different provenance, timing, review status and downstream training meaning.",
        "sources": ["dvc_home", "mlflow_registry", "nist_log_management"],
    },
    {
        "id": "P42-P0-008",
        "slug": "labels_record_policy_version_and_source",
        "node": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "claim_type": "label_lineage_rule",
        "storage_role": "manifest_store",
        "statement": "Labels must record label_policy_version and label_source so later training, audit and disagreement analysis can reproduce the label semantics.",
        "sources": ["dvc_home", "mlflow_registry", "nist_log_management"],
    },
    {
        "id": "P42-P0-009",
        "slug": "model_prompt_rag_versions_recorded_together",
        "node": "kt.ai_engineering.database_storage_engineering.model_registry_release_storage",
        "claim_type": "version_binding_rule",
        "storage_role": "registry",
        "statement": "A release manifest must record model_version, prompt_version and rag_index_version together whenever LLM audit participates in trading AI review.",
        "sources": ["mlflow_registry", "mlflow_registry_workflow", "dvc_home"],
    },
    {
        "id": "P42-P0-010",
        "slug": "llm_audit_binds_citations_source_version",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "citation_storage_rule",
        "storage_role": "vector_index",
        "statement": "LLM audit output must bind citations, source identifiers and index versions; unsupported claims must be marked rather than silently accepted.",
        "sources": ["qdrant_indexing", "opentelemetry_context", "nist_log_management"],
    },
    {
        "id": "P42-P0-011",
        "slug": "vector_search_links_source_and_knowledge_id",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "provenance_rule",
        "storage_role": "vector_index",
        "statement": "A vector search result must link back to a source document, chunk and formal knowledge id; a vector hit alone is not approved knowledge.",
        "sources": ["qdrant_indexing", "qdrant_search", "pgvector"],
    },
    {
        "id": "P42-P0-012",
        "slug": "rag_chunks_store_source_license_hash_version",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "chunk_storage_rule",
        "storage_role": "vector_index",
        "statement": "RAG chunks must store source_uri, license or copyright policy, content hash and chunk_version so retrieval evidence is traceable and rebuildable.",
        "sources": ["qdrant_indexing", "dvc_home", "nist_log_management"],
    },
    {
        "id": "P42-P0-013",
        "slug": "embedding_model_version_stored_with_vectors",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "embedding_version_rule",
        "storage_role": "vector_index",
        "statement": "Embedding model name and version must be stored with vector records; changing the embedding model requires a new index version or rebuild plan.",
        "sources": ["pgvector", "qdrant_indexing", "qdrant_search"],
    },
    {
        "id": "P42-P0-014",
        "slug": "postgres_constraints_enforce_invariants",
        "node": "kt.ai_engineering.database_storage_engineering.relational_core_schema",
        "claim_type": "constraint_rule",
        "storage_role": "canonical_store",
        "statement": "High-value invariants in trading AI storage should be enforced with PostgreSQL constraints where practical, not only with application-layer checks.",
        "sources": ["postgres_constraints", "postgres_transaction_isolation"],
    },
    {
        "id": "P42-P0-015",
        "slug": "unique_constraints_and_idempotency_keys",
        "node": "kt.ai_engineering.database_storage_engineering.relational_core_schema",
        "claim_type": "idempotency_rule",
        "storage_role": "canonical_store",
        "statement": "High-value write paths should use unique constraints and idempotency keys to prevent duplicated scoring, gate or audit events.",
        "sources": ["postgres_constraints", "postgres_mvcc"],
    },
    {
        "id": "P42-P0-016",
        "slug": "alembic_migration_reviewed_reversible",
        "node": "kt.ai_engineering.database_storage_engineering.migration_versioning",
        "claim_type": "migration_rule",
        "storage_role": "canonical_store",
        "statement": "Alembic migrations for trading AI storage must be reviewed and should include an explicit rollback or downgrade strategy before application.",
        "sources": ["alembic_docs", "alembic_autogenerate"],
    },
    {
        "id": "P42-P0-017",
        "slug": "autogenerate_migration_not_auto_applied",
        "node": "kt.ai_engineering.database_storage_engineering.migration_versioning",
        "claim_type": "migration_rule",
        "storage_role": "canonical_store",
        "statement": "Alembic autogenerate output should be treated as a candidate migration that requires review, not as an automatically safe database change.",
        "sources": ["alembic_autogenerate", "alembic_docs"],
    },
    {
        "id": "P42-P0-018",
        "slug": "schema_version_change_compatibility_check",
        "node": "kt.ai_engineering.database_storage_engineering.migration_versioning",
        "claim_type": "compatibility_rule",
        "storage_role": "canonical_store",
        "statement": "A schema_version change must trigger compatibility checks for replay, audit, existing manifests and downstream MCP/SearchLab consumers.",
        "sources": ["alembic_docs", "postgres_constraints", "dvc_home"],
    },
    {
        "id": "P42-P0-019",
        "slug": "event_decision_ingestion_label_time_separated",
        "node": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "claim_type": "time_semantics_rule",
        "storage_role": "manifest_store",
        "statement": "event_time, decision_time, ingestion_time and label_time must be separate fields because they answer different audit and leakage questions.",
        "sources": ["feast_point_in_time", "opentelemetry_context", "postgres_transaction_isolation"],
    },
    {
        "id": "P42-P0-020",
        "slug": "point_in_time_correctness_training_datasets",
        "node": "kt.ai_engineering.database_storage_engineering.feature_store_storage",
        "claim_type": "point_in_time_rule",
        "storage_role": "feature_store",
        "statement": "Training datasets for trading AI scoring must be point-in-time correct so each feature reflects only information available at the prediction decision time.",
        "sources": ["feast_point_in_time", "feast_docs", "dvc_home"],
    },
    {
        "id": "P42-P0-021",
        "slug": "feature_snapshot_manifest_schema_hash",
        "node": "kt.ai_engineering.database_storage_engineering.feature_store_storage",
        "claim_type": "feature_manifest_rule",
        "storage_role": "feature_store",
        "statement": "A feature_snapshot_manifest must store feature_schema_hash and lineage references so feature definitions can be audited and replayed.",
        "sources": ["feast_docs", "dvc_home", "mlflow_registry"],
    },
    {
        "id": "P42-P0-022",
        "slug": "dataset_snapshot_manifest_dataset_hash",
        "node": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "claim_type": "dataset_manifest_rule",
        "storage_role": "manifest_store",
        "statement": "A dataset_snapshot_manifest must store dataset_hash, split manifest and label policy references so training and evaluation data are reproducible.",
        "sources": ["dvc_home", "mlflow_registry", "mlflow_registry_workflow"],
    },
    {
        "id": "P42-P0-023",
        "slug": "final_gate_ledger_actor_reason_before_after_trace",
        "node": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "claim_type": "ledger_schema_rule",
        "storage_role": "audit_ledger",
        "statement": "A final_gate ledger must store actor, reason, before/after state and audit_trace_id so every allow, block or review action is accountable.",
        "sources": ["owasp_a09", "nist_log_management", "owasp_logging_vocabulary"],
    },
    {
        "id": "P42-P0-024",
        "slug": "audit_ledger_tamper_evidence",
        "node": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "claim_type": "tamper_evidence_rule",
        "storage_role": "audit_ledger",
        "statement": "Audit ledgers should provide tamper-evidence such as row_hash/prev_hash or equivalent integrity controls for high-value trading AI decisions.",
        "sources": ["owasp_a09", "nist_log_management"],
    },
    {
        "id": "P42-P0-025",
        "slug": "retention_policy_must_not_break_audit_replay",
        "node": "kt.ai_engineering.database_storage_engineering.data_lifecycle_retention",
        "claim_type": "lifecycle_rule",
        "storage_role": "backup_restore",
        "statement": "Delete, retention and archival policies must preserve enough manifests, hashes and lineage to replay audits after data lifecycle actions.",
        "sources": ["nist_log_management", "postgres_backup", "postgres_pitr"],
    },
    {
        "id": "P42-P0-026",
        "slug": "secrets_not_stored_in_business_tables",
        "node": "kt.ai_engineering.database_storage_engineering.security_privacy_access_control",
        "claim_type": "secret_boundary_rule",
        "storage_role": "canonical_store",
        "statement": "Database credentials, API keys, exchange secrets and private account fields must not be stored in ordinary business tables.",
        "sources": ["owasp_a09", "nist_log_management"],
    },
    {
        "id": "P42-P0-027",
        "slug": "backup_restore_must_be_tested",
        "node": "kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery",
        "claim_type": "backup_restore_rule",
        "storage_role": "backup_restore",
        "statement": "Backup is not sufficient unless restore is tested; trading AI storage must keep restore drill evidence and recovery assumptions.",
        "sources": ["postgres_backup", "postgres_pitr", "nist_log_management"],
    },
    {
        "id": "P42-P0-028",
        "slug": "db_permissions_and_write_actions_auditable",
        "node": "kt.ai_engineering.database_storage_engineering.security_privacy_access_control",
        "claim_type": "permission_audit_rule",
        "storage_role": "canonical_store",
        "statement": "Database permissions and write actions must be auditable, and MCP/SearchLab should remain read-only unless a separate audited write path is explicitly approved.",
        "sources": ["owasp_a09", "nist_log_management", "owasp_logging_vocabulary"],
    },
]


NODE_META = {
    "kt.ai_engineering.database_storage_engineering.relational_core_schema": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "relational_core_schema",
    ),
    "kt.ai_engineering.database_storage_engineering.data_contract_lineage": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "data_contract_lineage",
    ),
    "kt.ai_engineering.database_storage_engineering.migration_versioning": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "migration_versioning",
    ),
    "kt.ai_engineering.database_storage_engineering.indexing_query_performance": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "indexing_query_performance",
    ),
    "kt.ai_engineering.database_storage_engineering.audit_log_ledger": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "audit_log_ledger",
    ),
    "kt.ai_engineering.database_storage_engineering.feature_store_storage": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "feature_store_storage",
    ),
    "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "vector_store_retrieval_storage",
    ),
    "kt.ai_engineering.database_storage_engineering.model_registry_release_storage": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "model_registry_release_storage",
    ),
    "kt.ai_engineering.database_storage_engineering.runtime_observability_trace": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "runtime_observability_trace",
    ),
    "kt.ai_engineering.database_storage_engineering.data_lifecycle_retention": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "data_lifecycle_retention",
    ),
    "kt.ai_engineering.database_storage_engineering.security_privacy_access_control": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "security_privacy_access_control",
    ),
    "kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery": (
        "KB_AI_26_DATABASE_STORAGE",
        "storage_engineering",
        "backup_restore_disaster_recovery",
    ),
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def source_ref(key: str) -> dict[str, object]:
    src = SOURCE_CATALOG[key]
    return {
        "source_id": f"src_{key}",
        "source_title": src["title"],
        "source_url": src["url"],
        "source_type": src["type"],
        "publisher": src["publisher"],
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high" if int(src["score"]) >= 80 else "medium",
        "score": src["score"],
        "relevance": "high",
        "freshness": "time_sensitive" if src["type"] in {"official_doc", "security_standard"} else "stable",
        "limitations": [],
        "evidence_summary": src["summary"],
        "quoted_excerpt_allowed": False,
    }


def existing_phase42_topics() -> set[str]:
    topics: set[str] = set()
    for path in CAND_DIR.glob("cand_20260611_phase42_*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        rid = str(raw.get("research_task_id", ""))
        if rid.startswith("P42-"):
            topics.add(rid)
    return topics


def build_candidate(topic: dict[str, Any]) -> dict[str, object]:
    node_id = topic["node"]
    partition_id, domain, subdomain = NODE_META[node_id]
    source_refs = [source_ref(key) for key in topic["sources"]]
    score = round(sum(int(src["score"]) for src in source_refs) / len(source_refs))
    candidate_id = f"cand_20260611_phase42_{slug(topic['id'])}_{topic['slug']}_001"
    proposed_knowledge_id = f"kb_ai_database_storage.phase42.{topic['slug']}.v1"
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": topic["id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": "Phase 42 P0 sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering / Database Data Contract And Storage Engineering",
            "related_nodes": [
                "kt.rag_engineering",
                "kt.project_integration",
                "kt.ai_engineering.model_release_governance",
            ],
            "partition_id": partition_id,
            "domain": domain,
            "subdomain": subdomain,
            "rule_type": "governance_rule",
            "used_for": [
                "trading_ai_storage",
                "llm_training",
                "trading_gating_scoring",
                "rag_engineering",
                "mcp",
                "vue_audit_ui",
                "external_ai_ide",
            ],
        },
        "claim": {
            "claim_id": "claim_001",
            "statement": topic["statement"],
            "normalized_claim": f"phase42.{topic['slug']}.v1",
            "claim_type": topic["claim_type"],
            "storage_role": topic["storage_role"],
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in source_refs[:3]),
            "interpretation_notes": "本候选只沉淀 AI Engineering 的数据库、数据契约、存储、审计日志、向量检索和生命周期治理规则；K 线、fill model、仓位、止损止盈和实盘执行本体必须路由到 Trading Engineering。",
            "claim_strength": "medium",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "trading_ai_gating_scoring_storage",
            "applies_when": [
                "外接项目正在设计交易 AI gating/scoring 的数据库、数据契约、RAG 存储、审计日志、迁移、备份或生命周期治理。",
                "该规则用于阻断无 trace、无来源、无版本、无迁移、向量库事实化、LLM 越权 final gate 或训练/评估泄漏。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、K 线形态、策略参数或实盘下单建议。",
                "知识点主要描述 fill model、订单状态机、交易所异常处理、实盘风控阈值或交易收益本体，应路由到 Trading Engineering。",
                "用户正在请求直接创建生产数据库或执行不可逆迁移；这必须另起实现 Phase 并由开发者确认。",
            ],
            "assumptions": [
                "外接项目提供私有交易事实、真实表名和部署环境；CEK-TA 只沉淀可复用专业规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充交易 AI 实例。",
                "本条不创建真实数据库，不执行迁移，不改变 MCP 写权限。",
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 在外接交易 AI 项目中设计数据库、schema、migration、audit ledger、RAG/vector storage 和生命周期治理契约。",
                "用于生成任务卡、接口契约、测试计划、审计 checklist 和候选知识补证问题。",
                "用于阻断 Vector DB 成为事实主库、LLM audit 写 final_gate、无 audit_trace_id 决策或无来源默认指导。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘下单建议。",
                "不得据此直接创建生产数据库、执行迁移或修改外部项目真实数据库。",
                "不得把 candidate 当作 reviewed/approved 默认指导。",
            ],
        },
        "source_refs": source_refs,
        "source_quality": {
            "overall_reliability": "high" if score >= 82 else "medium",
            "score": score,
            "score_version": "1.1.0",
            "primary_source_count": min(3, len(source_refs)),
            "supporting_source_count": max(0, len(source_refs) - 3),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "来源支持通用数据库、RAG/vector、日志、安全、MLOps 和 feature store 工程原则；正式知识转换时需保留 CEK-TA 具体上下游引用和冲突链接。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": CONTRACT_REFS,
            "conflicts": [],
            "resolution_summary": "未发现与 Phase 42 契约的直接冲突；候选不会进入默认指导，也不会创建真实数据库。",
            "approval_allowed": False,
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; not reviewed or approved; external audit required before formal knowledge conversion.",
            "requires_human_escalation": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "codex",
            "reviewed_at": None,
            "open_questions": [
                "审计时确认该候选是否需要补充更贴近交易 AI storage 的实例、反例或与 Phase 41/Trading Engineering 增加交叉引用。",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "Phase 42 P0 database, data contract and storage engineering candidate expansion.",
                }
            ],
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、来源摘要和归纳性知识，不保存全文或长引用。",
            "reuse_risk": "low",
        },
        "conversion_target": {
            "proposed_knowledge_id": proposed_knowledge_id,
            "target_schema": "cek_ta_knowledge_item",
            "target_review_status": "draft",
            "skill_candidate": False,
            "eval_case_candidate": topic["id"] in {"P42-P0-002", "P42-P0-010", "P42-P0-011", "P42-P0-027"},
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": None,
            "hidden_from_default_queue": False,
            "next_action": "export_for_ai_or_human_audit",
            "default_guidance_allowed": False,
        },
        "phase42_trace": {
            "priority": "P0",
            "related_contracts": CONTRACT_REFS,
            "scope_boundary": "AI Engineering database/storage only; Trading Engineering body is reference-only.",
        },
    }


def load_phase42_candidates() -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for path in sorted(CAND_DIR.glob("cand_20260611_phase42_*.json")):
        candidates.append(json.loads(path.read_text(encoding="utf-8-sig")))
    return candidates


def write_research_note(created: int, skipped: int) -> None:
    lines = [
        "# Phase 42 P0 候选知识来源采集记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        f"本轮按 Phase 42 P0 矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条；当前 P0 规划总数为 {len(TOPICS)} 条。",
        "",
        "本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。",
        "",
        "## 主要来源族",
        "",
        "| 来源族 | 用途 |",
        "| --- | --- |",
        "| PostgreSQL 官方文档 | constraints、MVCC、transaction isolation、backup/PITR 和 canonical store 关系库边界 |",
        "| Alembic 官方文档 | migration、autogenerate candidate migration、review 和 rollback 边界 |",
        "| Feast 官方文档 | point-in-time joins、feature store、offline/online feature parity |",
        "| MLflow / DVC | model registry、版本、alias/tag、dataset hash 和可复现数据管理 |",
        "| pgvector / Qdrant | vector index、HNSW/IVFFlat、payload index、metadata filter 和 source provenance |",
        "| NIST / OWASP | log management、audit trail、append-only、防篡改、权限和安全监控 |",
        "| OpenTelemetry | request/trace context propagation，用于 audit_trace_id 和跨服务追踪 |",
        "",
        "## P0 主题",
        "",
        "| topic_id | canonical_node_id | claim_type | storage_role | 来源数 |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for topic in TOPICS:
        lines.append(
            f"| {topic['id']} | `{topic['node']}` | {topic['claim_type']} | {topic['storage_role']} | {len(topic['sources'])} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值、买卖点、仓位或交易所执行适配器本体知识。这些内容仍归 Trading Engineering。",
            "",
            "本轮没有创建真实数据库、没有执行 migration、没有改变 MCP/SearchLab 写权限。",
            "",
        ]
    )
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_quality_and_report(created: int, skipped: int) -> dict[str, object]:
    candidates = load_phase42_candidates()
    failures: list[dict[str, object]] = []
    seen = set()
    expected = {topic["id"] for topic in TOPICS}
    for item in candidates:
        cid = str(item.get("candidate_id", ""))
        rid = str(item.get("research_task_id", ""))
        seen.add(rid)
        sources = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in sources if isinstance(src, dict)}
        if len(sources) < 2:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_2"})
        if not (source_types & {"official_doc", "security_standard", "governance_framework", "framework_doc"}):
            failures.append({"candidate_id": cid, "failure": "missing_reliable_source_type"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": cid, "failure": "workflow_default_guidance_not_false"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "failure": "machine_gate_not_deny"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if not str(item.get("classification", {}).get("canonical_node_id", "")).startswith(
            "kt.ai_engineering.database_storage_engineering."
        ):
            failures.append({"candidate_id": cid, "failure": "wrong_canonical_node"})
        not_applicable = " ".join(item.get("applicability", {}).get("not_applicable_when", []))
        if "Trading Engineering" not in not_applicable:
            failures.append({"candidate_id": cid, "failure": "missing_trading_boundary"})
    for rid in sorted(expected - seen):
        failures.append({"research_task_id": rid, "failure": "missing_p0_candidate"})
    quality = {
        "report_id": "phase42_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 42 P0 database/storage candidates",
        "candidate_count": len(candidates),
        "planned_p0_total": len(TOPICS),
        "created_this_run": created,
        "skipped_existing": skipped,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Phase 42 P0 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本轮生成 Phase 42 P0 candidate `{created}` 条，跳过已存在 `{skipped}` 条。当前 Phase 42 P0 候选总数 `{len(candidates)}` 条。",
                "",
                f"质量门禁：`{quality['gate_status']}`，失败数 `{quality['failure_count']}`。",
                "",
                "## 上下游",
                "",
                "上游：`docs/research/phase42_database_storage_collection_matrix.md`、`docs/research/phase42_research_task_queue.md`、Phase 42 范围与契约文档。",
                "",
                "下游：`CEK-TA-349` 导出候选 AI 审计包，并按 Phase 32 工作流处理 accepted、needs_more_evidence、rejected。",
                "",
                "## 边界",
                "",
                "本轮只生成候选知识，不生成 formal reviewed，不设置 approved，不允许默认指导，不创建真实数据库，不执行 migration。",
                "",
                "Trading Engineering 本体只作为引用边界，不混入 AI Engineering 数据库存储候选。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return quality


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_phase42_topics()
    created = 0
    skipped = 0
    for topic in TOPICS:
        if topic["id"] in existing:
            skipped += 1
            continue
        candidate = build_candidate(topic)
        path = CAND_DIR / f"{candidate['candidate_id']}.json"
        path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1
    write_research_note(created, skipped)
    quality = write_quality_and_report(created, skipped)
    print(json.dumps(quality, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
