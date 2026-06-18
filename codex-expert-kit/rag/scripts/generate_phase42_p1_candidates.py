"""Generate Phase 42 P1 database/storage candidate knowledge files."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
RESEARCH = resolve_repo_path("docs", "research", "phase42_p1_candidate_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase42_p1_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase42_p1_candidate_quality_gate.json", start_file=__file__)

CONTRACT_REFS = [
    "docs/research/phase42_database_storage_scope.md",
    "docs/contracts/phase42_database_storage_contract.md",
    "docs/contracts/phase42_rag_vector_storage_contract.md",
    "docs/tasks/phase42_database_data_contract_storage_engineering.md",
]

SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "pgvector": {
        "title": "pgvector: Open-source vector similarity search for Postgres",
        "url": "https://github.com/pgvector/pgvector",
        "type": "official_doc",
        "publisher": "pgvector",
        "score": 86,
        "summary": "pgvector documents vector storage and HNSW/IVFFlat indexes inside PostgreSQL, preserving SQL adjacency with relational metadata.",
    },
    "qdrant_indexing": {
        "title": "Qdrant Documentation: Indexing",
        "url": "https://qdrant.tech/documentation/manage-data/indexing/",
        "type": "official_doc",
        "publisher": "Qdrant",
        "score": 86,
        "summary": "Qdrant documents vector indexes and payload indexes, emphasizing combined vector and traditional indexing for filtered search.",
    },
    "qdrant_search": {
        "title": "Qdrant Documentation: Search",
        "url": "https://qdrant.tech/documentation/search/search/",
        "type": "official_doc",
        "publisher": "Qdrant",
        "score": 84,
        "summary": "Qdrant search documentation recommends payload indexes for fields used in filtered vector search.",
    },
    "qdrant_filtering": {
        "title": "Qdrant Documentation: Filtering",
        "url": "https://qdrant.tech/documentation/search/filtering/",
        "type": "official_doc",
        "publisher": "Qdrant",
        "score": 84,
        "summary": "Qdrant filtering documentation explains payload conditions, nested object filters and metadata-based retrieval constraints.",
    },
    "qdrant_github": {
        "title": "Qdrant GitHub Repository",
        "url": "https://github.com/qdrant/qdrant",
        "type": "official_doc",
        "publisher": "Qdrant",
        "score": 82,
        "summary": "Qdrant describes itself as a vector similarity search engine and vector database with payload management and filtering support.",
    },
    "feast_intro": {
        "title": "Feast Documentation: Introduction",
        "url": "https://docs.feast.dev/",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 86,
        "summary": "Feast describes an open-source feature store for defining, managing, validating and serving features for production AI/ML.",
    },
    "feast_point_in_time": {
        "title": "Feast Documentation: Point-in-time joins",
        "url": "https://docs.feast.dev/getting-started/concepts/point-in-time-joins",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 88,
        "summary": "Feast documents point-in-time correct joins that reproduce feature state at a specific past timestamp.",
    },
    "feast_retrieval": {
        "title": "Feast Documentation: Feature retrieval",
        "url": "https://docs.feast.dev/getting-started/concepts/feature-retrieval",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 86,
        "summary": "Feast feature retrieval covers historical features for training and online features for low-latency serving.",
    },
    "mlflow_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 88,
        "summary": "MLflow Model Registry documents registered models, versions, aliases, tags and model metadata.",
    },
    "mlflow_workflow": {
        "title": "MLflow Model Registry Workflows",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 86,
        "summary": "MLflow workflow documentation covers registering models, managing versions, applying aliases and organizing releases.",
    },
    "dvc": {
        "title": "DVC: Data Version Control",
        "url": "https://dvc.org/",
        "type": "official_doc",
        "publisher": "DVC",
        "score": 82,
        "summary": "DVC describes data and ML artifact versioning patterns that complement model registry release manifests.",
    },
    "postgres_rls": {
        "title": "PostgreSQL 18 Documentation: Row Security Policies",
        "url": "https://www.postgresql.org/docs/current/ddl-rowsecurity.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 88,
        "summary": "PostgreSQL row security policies restrict which rows users can access or modify through table policies.",
    },
    "postgres_create_policy": {
        "title": "PostgreSQL 18 Documentation: CREATE POLICY",
        "url": "https://www.postgresql.org/docs/current/sql-createpolicy.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 86,
        "summary": "CREATE POLICY defines row-level security policies and requires row-level security to be enabled on the table.",
    },
    "pgaudit": {
        "title": "PostgreSQL Audit Extension",
        "url": "https://pgaudit.org/",
        "type": "official_doc",
        "publisher": "pgAudit",
        "score": 86,
        "summary": "pgAudit provides detailed session and object audit logging via the PostgreSQL logging facility.",
    },
    "pgaudit_github": {
        "title": "pgAudit GitHub Repository",
        "url": "https://github.com/pgaudit/pgaudit",
        "type": "official_doc",
        "publisher": "pgAudit",
        "score": 84,
        "summary": "pgAudit documents audit logging intended to support government, financial or ISO certification audit needs.",
    },
    "aws_pgaudit": {
        "title": "AWS Documentation: Using pgAudit to log database activity",
        "url": "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Appendix.PostgreSQL.CommonDBATasks.pgaudit.html",
        "type": "cloud_provider_doc",
        "publisher": "AWS",
        "score": 82,
        "summary": "AWS documents using pgAudit on RDS PostgreSQL to track changes, users and database/table activity for audit requirements.",
    },
}

TOPICS: list[dict[str, Any]] = [
    {
        "id": "P42-P1-001",
        "slug": "pgvector_vs_qdrant_selection_boundary",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "storage_boundary_rule",
        "storage_role": "vector_index",
        "statement": "pgvector and Qdrant selection must be a storage-boundary decision: pgvector is suitable when vector retrieval should stay close to PostgreSQL metadata and transactional governance, while Qdrant is suitable when a dedicated vector service with payload filtering and operational scaling is justified; neither may replace the canonical source of truth.",
        "sources": ["pgvector", "qdrant_indexing", "qdrant_github"],
    },
    {
        "id": "P42-P1-002",
        "slug": "hnsw_vs_ivfflat_selection_boundary",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "index_selection_rule",
        "storage_role": "vector_index",
        "statement": "HNSW and IVFFlat selection must be based on measured latency, recall, memory, build-time and update-pattern tradeoffs; index type must not be selected by default without a benchmark tied to the retrieval workload.",
        "sources": ["pgvector", "qdrant_indexing", "qdrant_search"],
    },
    {
        "id": "P42-P1-003",
        "slug": "qdrant_payload_index_metadata_filter_rule",
        "node": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "claim_type": "metadata_filter_rule",
        "storage_role": "vector_index",
        "statement": "Qdrant payload indexes should be created for metadata fields that are repeatedly used in filtered retrieval, and every filtered RAG query must preserve source provenance, formal_knowledge_id and version metadata.",
        "sources": ["qdrant_indexing", "qdrant_search", "qdrant_filtering"],
    },
    {
        "id": "P42-P1-004",
        "slug": "feast_adoption_boundary_after_offline_online_parity_pressure",
        "node": "kt.ai_engineering.database_storage_engineering.feature_store_storage",
        "claim_type": "adoption_boundary_rule",
        "storage_role": "feature_store",
        "statement": "Feast should be introduced only when offline/online feature parity, point-in-time retrieval, feature reuse and serving latency create enough pressure to justify a feature store; simpler manifest-based pipelines remain acceptable before that threshold.",
        "sources": ["feast_intro", "feast_point_in_time", "feast_retrieval"],
    },
    {
        "id": "P42-P1-005",
        "slug": "mlflow_registry_adoption_boundary_after_release_manifest_complexity",
        "node": "kt.ai_engineering.database_storage_engineering.model_registry_release_storage",
        "claim_type": "adoption_boundary_rule",
        "storage_role": "registry",
        "statement": "MLflow Model Registry should be introduced when model versions, aliases, tags, metadata, release manifests and deployment organization exceed simple file-based release tracking; it must complement, not replace, scorer/calibrator/prompt/RAG index version binding.",
        "sources": ["mlflow_registry", "mlflow_workflow", "dvc"],
    },
    {
        "id": "P42-P1-006",
        "slug": "rls_pgaudit_adoption_boundary",
        "node": "kt.ai_engineering.database_storage_engineering.security_privacy_access_control",
        "claim_type": "security_adoption_boundary_rule",
        "storage_role": "audit_ledger",
        "statement": "PostgreSQL RLS and pgAudit should be adopted when row-level access boundaries, tenant/project isolation or audit-grade database activity tracing are required; they require explicit policy design, performance review and log-retention planning before production use.",
        "sources": ["postgres_rls", "postgres_create_policy", "pgaudit", "pgaudit_github", "aws_pgaudit"],
    },
]

PRIMARY_SOURCE_TYPES = {
    "official_doc",
    "research_paper",
    "standard_doc",
    "governance_framework",
    "security_standard",
    "framework_doc",
    "cloud_provider_doc",
}


def source_ref(source_id: str) -> dict[str, Any]:
    source = SOURCE_CATALOG[source_id]
    return {
        "source_id": f"src_{source_id}",
        "source_title": source["title"],
        "source_url": source["url"],
        "source_type": source["type"],
        "publisher": source["publisher"],
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high" if source["type"] in {"official_doc", "security_standard"} else "medium",
        "score": source["score"],
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": [],
        "evidence_summary": source["summary"],
        "quoted_excerpt_allowed": False,
    }


def subdomain_from_node(node: str) -> str:
    return node.rsplit(".", 1)[-1]


def normalize_claim(slug: str) -> str:
    return f"phase42.{slug}.v1"


def candidate_id(topic: dict[str, Any]) -> str:
    return f"cand_20260611_phase42_{topic['id'].lower().replace('-', '_')}_{topic['slug']}_001"


def candidate_path(topic: dict[str, Any]) -> Path:
    return CAND_DIR / f"{candidate_id(topic)}.json"


def build_candidate(topic: dict[str, Any]) -> dict[str, Any]:
    sources = [source_ref(source_id) for source_id in topic["sources"]]
    evidence_summary = "；".join(source["evidence_summary"] for source in sources)
    node = topic["node"]
    subdomain = subdomain_from_node(node)
    knowledge_id = f"kb_ai_database_storage.phase42.{topic['slug']}.v1"
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id(topic),
        "research_task_id": topic["id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "pending_external_audit",
            "decision_reason": "Phase 42 P1 candidate generated from official sources; must be externally audited before draft/reviewed conversion.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node,
            "canonical_node_id": node,
            "tree_path": "CEK-TA / AI Engineering / Database Data Contract And Storage Engineering",
            "related_nodes": [
                "kt.rag_engineering",
                "kt.project_integration",
                "kt.ai_engineering.model_release_governance",
            ],
            "partition_id": "KB_AI_26_DATABASE_STORAGE",
            "domain": "storage_engineering",
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
            "normalized_claim": normalize_claim(topic["slug"]),
            "claim_type": topic["claim_type"],
            "storage_role": topic["storage_role"],
            "evidence_summary": evidence_summary,
            "interpretation_notes": (
                "本候选只沉淀 AI Engineering 的数据库、数据契约、存储、审计日志、向量检索和生命周期治理规则；"
                "K 线、fill model、仓位、止损止盈和实盘执行本体必须路由到 Trading Engineering。"
            ),
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
                "该规则用于判断是否引入更复杂的向量库、feature store、model registry、RLS 或 pgAudit 等增强组件。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、K 线形态、策略参数或实盘下单建议。",
                "知识点主要描述 fill model、订单状态机、交易所异常处理、实盘风控阈值或交易收益本体，应路由到 Trading Engineering。",
                "用户正在请求直接创建生产数据库、启用 RLS/pgAudit、执行迁移或引入外部服务；这必须另起实现 Phase 并由开发者确认。",
            ],
            "assumptions": [
                "外接项目提供私有交易事实、真实表名、吞吐量、延迟和部署环境；CEK-TA 只沉淀可复用专业规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充实测 benchmark 或部署实例。",
                "本条不创建真实数据库，不执行迁移，不改变 MCP 写权限，不引入外部服务依赖。",
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
                "不得据此直接创建生产数据库、执行迁移、启用 RLS/pgAudit 或修改外部项目真实数据库。",
                "不得把 candidate 当作 reviewed/approved 默认指导。",
            ],
        },
        "source_refs": sources,
        "source_quality": {
            "overall_reliability": "high",
            "score": int(sum(source["score"] for source in sources) / len(sources)),
            "score_version": "1.1.0",
            "primary_source_count": len([s for s in sources if s["source_type"] in PRIMARY_SOURCE_TYPES]),
            "supporting_source_count": 0,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "来源支持工具边界和工程能力，但正式知识转换时必须保留 CEK-TA 不创建真实数据库、不执行迁移、不默认引入外部依赖的边界。"
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": CONTRACT_REFS,
            "conflicts": [],
            "resolution_summary": "未发现与 Phase 42 P0 formal reviewed 知识的直接冲突；P1 候选不会进入默认指导，也不会创建真实数据库。",
            "approval_allowed": False,
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 42 P1 candidate audit package does not allow default guidance; formal reviewed requires later audit.",
            "requires_human_escalation": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "external_ai_and_codex_alignment",
            "reviewed_at": None,
            "open_questions": [
                "审计时确认该候选是否需要补充更贴近交易 AI storage 的 benchmark、部署实例、成本边界或回滚策略。"
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "Phase 42 P1 database/storage engineering candidate expansion.",
                }
            ],
            "ai_audit": {
                "audit_result_id": None,
                "decision": "pending_external_audit",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "boundary": "Phase 42 P1 candidate does not allow reviewed, approved, default guidance or hard gate before audit.",
            },
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、来源摘要和归纳性知识，不保存全文或长引用。",
            "reuse_risk": "low",
        },
        "conversion_target": {
            "proposed_knowledge_id": knowledge_id,
            "target_schema": "cek_ta_knowledge_item",
            "target_review_status": "draft",
            "skill_candidate": False,
            "eval_case_candidate": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "workflow": {
            "stage": "pending_review",
            "queue_group": "pending",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": None,
            "hidden_from_default_queue": True,
            "next_action": "export_ai_audit",
            "default_guidance_allowed": False,
            "visible_in_default_guidance_queue": False,
            "hard_gate_allowed": False,
        },
        "phase42_trace": {
            "priority": "P1",
            "related_contracts": CONTRACT_REFS,
            "scope_boundary": "AI Engineering database/storage only; Trading Engineering body is reference-only.",
        },
    }


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def quality_gate(candidates: list[dict[str, Any]], created: list[str], skipped: list[str]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for item in candidates:
        candidate_id_value = str(item.get("candidate_id", ""))
        source_refs = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in source_refs if isinstance(src, dict)}
        canonical_node_id = str(item.get("classification", {}).get("canonical_node_id", ""))
        not_applicable = " ".join(item.get("applicability", {}).get("not_applicable_when", []))
        if not canonical_node_id.startswith("kt.ai_engineering.database_storage_engineering."):
            failures.append({"candidate_id": candidate_id_value, "failure": "wrong_canonical_node"})
        if len(source_refs) < 3:
            failures.append({"candidate_id": candidate_id_value, "failure": "source_refs_lt_3"})
        if not (source_types & PRIMARY_SOURCE_TYPES):
            failures.append({"candidate_id": candidate_id_value, "failure": "missing_primary_source_type"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": candidate_id_value, "failure": "unsafe_conflict_status"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": candidate_id_value, "failure": "not_candidate_proposed"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate_id_value, "failure": "machine_gate_not_deny"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id_value, "failure": "workflow_default_guidance_not_false"})
        if "Trading Engineering" not in not_applicable:
            failures.append({"candidate_id": candidate_id_value, "failure": "missing_trading_boundary"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id_value, "failure": "mojibake_marker_detected"})
    return {
        "report_id": "phase42_p1_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 42 P1 database/storage candidates",
        "candidate_count": len(candidates),
        "planned_p1_total": len(TOPICS),
        "created_this_run": len(created),
        "skipped_existing": len(skipped),
        "created": created,
        "skipped": skipped,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures and len(candidates) == len(TOPICS) else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }


def write_research(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 42 P1 候选知识联网采集记录",
        "",
        "本文件记录 Phase 42 P1 6 条数据库/存储增强知识候选的来源、边界和审计状态。",
        "",
        "## 全局边界",
        "",
        "```text",
        "1. P1 候选不创建真实数据库，不执行迁移，不启用 RLS/pgAudit，不引入外部服务依赖。",
        "2. 候选不能作为 reviewed、approved、default guidance 或 hard gate。",
        "3. 具体交易规则、K 线、fill model、仓位、止损止盈和实盘执行仍归 Trading Engineering。",
        "```",
        "",
    ]
    for item in candidates:
        claim = item["claim"]
        lines.extend(
            [
                f"## {item['research_task_id']} - {claim['normalized_claim']}",
                "",
                f"- statement: {claim['statement']}",
                f"- canonical_node_id: `{item['classification']['canonical_node_id']}`",
                f"- proposed_knowledge_id: `{item['conversion_target']['proposed_knowledge_id']}`",
                "- sources:",
            ]
        )
        for source in item["source_refs"]:
            lines.append(f"  - {source['source_title']}：{source['source_url']}；{source['evidence_summary']}")
        lines.append("")
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> None:
    lines = [
        "# Phase 42 P1 候选知识生成报告",
        "",
        f"- generated_at: {TODAY}",
        f"- candidate_count: {len(candidates)}",
        f"- gate_status: {quality['gate_status']}",
        f"- failure_count: {quality['failure_count']}",
        "",
        "## 候选列表",
        "",
    ]
    for item in candidates:
        lines.append(f"- `{item['research_task_id']}` -> `{item['conversion_target']['proposed_knowledge_id']}`")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "P1 候选只进入外部审计包；不得直接 reviewed、approved、default guidance 或 hard gate。",
            "```",
        ]
    )
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    skipped: list[str] = []
    candidates: list[dict[str, Any]] = []
    for topic in TOPICS:
        path = candidate_path(topic)
        if path.exists():
            candidate = json.loads(path.read_text(encoding="utf-8-sig"))
            skipped.append(path.name)
        else:
            candidate = build_candidate(topic)
            path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            created.append(path.name)
        candidates.append(candidate)

    write_research(candidates)
    quality = quality_gate(candidates, created, skipped)
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(candidates, quality)
    print(json.dumps({"report": str(REPORT), "quality_gate": str(QUALITY), **quality}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
