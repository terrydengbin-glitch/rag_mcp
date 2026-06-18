"""Import Phase 42 P1 audit result and prepare P42-P1-003 re-audit.

The first P1 audit allows five candidates to move to accepted_for_draft and
keeps P42-P1-003 in needs_more_evidence. This script does not create formal
knowledge, reviewed knowledge, approved knowledge, default guidance, or hard
gate rules.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", "audit_result_phase42_p1_candidate_audit_package_20260611_strict_v1.json", start_file=__file__
)
IMPORT_REPORT_PATH = resolve_repo_path("docs", "reports", "phase42_p1_audit_import_report.json", start_file=__file__)
SUPPLEMENT_RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase42_p1_p003_supplemental_research.md", start_file=__file__
)
SUPPLEMENT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase42_p1_p003_supplemental_reaudit_package_20260611.json", start_file=__file__
)
SUPPLEMENT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase42_p1_p003_supplemental_reaudit_package_report.json", start_file=__file__
)

AUDIT_RESULT_ID = "audit_result_phase42_p1_candidate_audit_package_20260611_strict_v1"
PACKAGE_ID = "phase42_p1_candidate_audit_package_20260611"
SUPPLEMENT_PACKAGE_ID = "phase42_p1_p003_supplemental_reaudit_package_20260611"

TASK_TO_CANDIDATE = {
    "P42-P1-001": "cand_20260611_phase42_p42_p1_001_pgvector_vs_qdrant_selection_boundary_001",
    "P42-P1-002": "cand_20260611_phase42_p42_p1_002_hnsw_vs_ivfflat_selection_boundary_001",
    "P42-P1-003": "cand_20260611_phase42_p42_p1_003_qdrant_payload_index_metadata_filter_rule_001",
    "P42-P1-004": "cand_20260611_phase42_p42_p1_004_feast_adoption_boundary_after_offline_online_parity_pressure_001",
    "P42-P1-005": "cand_20260611_phase42_p42_p1_005_mlflow_registry_adoption_boundary_after_release_manifest_complexity_001",
    "P42-P1-006": "cand_20260611_phase42_p42_p1_006_rls_pgaudit_adoption_boundary_001",
}

DECISIONS = {
    "P42-P1-001": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "pgvector 和 Qdrant 官方来源足以支持工具选型边界。",
            "候选保留 vector index 不能替代 canonical source of truth 的边界。",
        ],
        "patch_notes": [
            "formal draft 必须增加 VectorStoreSelectionDecision schema。",
            "保留 vector index != canonical store、vector hit != approved knowledge、vector similarity != citation resolved。",
        ],
    },
    "P42-P1-002": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "pgvector 文档支持 HNSW 与 IVFFlat 的 latency、recall、memory、build-time tradeoff。",
            "候选没有把 HNSW 或 IVFFlat 写成默认最佳。",
        ],
        "patch_notes": [
            "formal draft 必须要求 VectorIndexBenchmarkReport。",
            "选择必须绑定 workload benchmark，不能按流行度默认选择。",
        ],
    },
    "P42-P1-003": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reasons": [
            "Qdrant 来源支持 payload index 与 filtering。",
            "formal_knowledge_id、source provenance、version metadata 属于 CEK-TA formal index/citation resolver 语义，不能只由 Qdrant 文档支撑。",
        ],
        "patch_notes": [
            "补充 Phase42 RAG / Vector Storage Contract。",
            "补充 CitationResolver / FormalKnowledgeLink 相关内部契约。",
            "拆分 Qdrant 工具能力与 CEK-TA provenance contract。",
        ],
    },
    "P42-P1-004": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "Feast 文档支持 point-in-time joins 与 feature retrieval 边界。",
            "候选将 Feast 写成条件基础设施，不是默认依赖。",
        ],
        "patch_notes": [
            "formal draft 必须增加 FeastAdoptionDecision schema。",
            "Feature store 不能绕过 decision-time feature contract。",
        ],
    },
    "P42-P1-005": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "MLflow Model Registry 文档支持 registered model、version、alias、tag、metadata。",
            "候选保留 MLflow complement release manifest 而不是替代 release approval 的边界。",
        ],
        "patch_notes": [
            "formal draft 必须增加 MLflowRegistryAdoptionDecision schema。",
            "MLflow alias 不等于 production permission 或 final gate。",
        ],
    },
    "P42-P1-006": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "PostgreSQL RLS 与 pgAudit 来源足以支持条件引入边界。",
            "候选未直接启用 RLS/pgAudit，也未改变真实数据库权限。",
        ],
        "patch_notes": [
            "formal draft 必须增加 RlsPgAuditAdoptionDecision schema。",
            "必须要求 policy design、performance review、log-retention plan 和 rollback plan。",
        ],
    },
}

SUPPLEMENTAL_SOURCES = [
    {
        "source_id": "src_phase42_rag_vector_storage_contract",
        "source_title": "Phase 42 RAG / Vector Storage 契约",
        "source_url": "docs/contracts/phase42_rag_vector_storage_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "phase42",
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["内部契约只证明 CEK-TA 项目治理语义，不替代 Qdrant 官方工具能力说明。"],
        "evidence_summary": (
            "契约定义 rag_document、rag_chunk、embedding_record、vector_index_manifest、citation_result；"
            "要求检索结果回链 source document、chunk、formal knowledge id、source_uri、license 和版本。"
        ),
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_phase41_citation_resolver_contract",
        "source_title": "Phase 41 Hybrid Scoring Runtime Contract: citation resolver",
        "source_url": "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "phase41",
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["该契约用于 CEK-TA hybrid scoring runtime，不证明 Qdrant 本身具备 CEK-TA citation resolver。"],
        "evidence_summary": (
            "契约定义 rag_citation_response、citation_resolution_status、unsupported_claim detector；"
            "当 citation unresolved/no_source/conflict/stale/out_of_scope 时必须降级或阻断。"
        ),
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_external_ai_active_retrieval_protocol",
        "source_title": "外部项目 AI 主动检索协议",
        "source_url": "docs/contracts/external_ai_active_retrieval_protocol.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "phase35",
        "reliability": "high",
        "score": 82,
        "relevance": "medium",
        "freshness": "stable",
        "limitations": ["该协议定义外部项目 AI 检索和引用要求，不替代具体 vector DB 文档。"],
        "evidence_summary": "协议要求外部项目 AI 在专业判断前主动检索 CEK-TA，并输出 citation、knowledge_id、review_status 与边界说明。",
        "quoted_excerpt_allowed": False,
    },
]


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must be a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_path(candidate_id: str) -> Path:
    paths = list(CANDIDATE_DIR.glob(f"{candidate_id}.json"))
    if not paths:
        raise FileNotFoundError(candidate_id)
    return paths[0]


def append_unique(items: list[Any], entry: dict[str, Any], key: str) -> None:
    value = entry.get(key)
    for item in items:
        if isinstance(item, dict) and item.get(key) == value:
            return
    items.append(entry)


def build_audit_result() -> dict[str, Any]:
    candidate_results: list[dict[str, Any]] = []
    for research_task_id, candidate_id in TASK_TO_CANDIDATE.items():
        decision = DECISIONS[research_task_id]
        candidate_results.append(
            {
                "candidate_id": candidate_id,
                "research_task_id": research_task_id,
                "decision": decision["decision"],
                "confidence": decision["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": decision["reasons"],
                "source_audit": {
                    "status": "warning" if decision["decision"] == "needs_more_evidence" else "pass",
                    "notes": decision["reasons"],
                },
                "conflict_audit": {
                    "status": "pass",
                    "notes": ["未发现与 Phase 42 P0 formal reviewed 知识的直接冲突。"],
                },
                "scope_audit": {
                    "status": "pass",
                    "notes": [
                        "分类保持在 AI Engineering / Database Storage Engineering。",
                        "未混入 K 线、fill model、仓位、止损止盈或实盘执行本体。",
                    ],
                },
                "classification_audit": {
                    "status": "pass",
                    "notes": ["canonical_node_id 属于 kt.ai_engineering.database_storage_engineering.*。"],
                },
                "required_followups": decision["patch_notes"] if decision["decision"] == "needs_more_evidence" else [],
                "proposed_handoff_patch": {
                    "source_patch_notes": decision["patch_notes"],
                    "content_patch_notes": decision["patch_notes"],
                    "boundary_patch_notes": [
                        "不得创建真实数据库、执行迁移、启用工具或改变 MCP/API 写权限。",
                        "不得进入 reviewed、approved、default guidance 或 hard gate。",
                    ],
                    "conflict_patch_notes": [
                        "P1 工具能力只能作为条件增强项，不能覆盖 P0 canonical store 和 deterministic final gate 边界。"
                    ],
                },
            }
        )

    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit_transcribed_by_codex",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_draft": 5,
            "needs_more_evidence": 1,
            "rejected": 0,
            "blocked": 0,
            "reviewed_allowed": 0,
            "approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "hard_boundaries": [
            "accepted_for_draft 不是 reviewed 或 approved。",
            "本报告不允许创建正式 reviewed 知识。",
            "本报告不允许 default guidance 或 hard gate。",
            "P1 工具能力不能写成默认依赖。",
        ],
        "candidate_results": candidate_results,
    }


def patch_candidate(candidate: dict[str, Any], audit_result: dict[str, Any], result: dict[str, Any]) -> None:
    decision = str(result["decision"])
    status = candidate.setdefault("status", {})
    review = candidate.setdefault("review", {})
    workflow = candidate.setdefault("workflow", {})
    machine_gate = candidate.setdefault("machine_gate", {})
    conversion_target = candidate.setdefault("conversion_target", {})

    review["ai_audit"] = {
        "audit_result_id": audit_result["audit_result_id"],
        "package_id": audit_result["package_id"],
        "auditor": audit_result["auditor"],
        "audited_at": audit_result["audited_at"],
        "decision": decision,
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "source_audit": result.get("source_audit", {}),
        "conflict_audit": result.get("conflict_audit", {}),
        "scope_audit": result.get("scope_audit", {}),
        "classification_audit": result.get("classification_audit", {}),
        "proposed_handoff_patch": result.get("proposed_handoff_patch", {}),
        "boundary": "Phase 42 P1 first audit does not allow reviewed, approved, default guidance or hard gate.",
    }
    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        append_unique(
            audit_log,
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase42_p1_audit_result_imported",
                "reason": f"external audit decision={decision}",
                "audit_result_id": audit_result["audit_result_id"],
            },
            "action",
        )

    status["updated_at"] = TODAY
    status["decision_reason"] = f"Phase 42 P1 严格审计结论为 {decision}；不得 reviewed/approved/default guidance/hard gate。"
    workflow["ai_audit_result_id"] = audit_result["audit_result_id"]
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Phase 42 P1 candidate audit does not allow default guidance; formal reviewed requires later reviewed gate."
    machine_gate["requires_human_escalation"] = True
    conversion_target["target_review_status"] = "draft" if decision == "accepted_for_draft" else "blocked"
    conversion_target["default_guidance_allowed"] = False
    conversion_target["hard_gate_allowed"] = False

    if decision == "accepted_for_draft":
        status["review_status"] = "accepted"
        status["ingestion_decision"] = "accepted_for_draft"
        workflow["stage"] = "ai_audited"
        workflow["queue_group"] = "ai_passed"
        workflow["next_action"] = "prepare_formal_draft_after_separate_reviewed_gate"
    elif decision == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "supplement_sources_and_export_reaudit_package"
    else:
        status["review_status"] = "rejected"
        status["ingestion_decision"] = "rejected"
        workflow["stage"] = "rejected"
        workflow["queue_group"] = "rejected"
        workflow["next_action"] = "none"


def supplement_p003(candidate: dict[str, Any]) -> None:
    source_refs = candidate.setdefault("source_refs", [])
    if not isinstance(source_refs, list):
        raise ValueError("source_refs must be a list.")
    for source in SUPPLEMENTAL_SOURCES:
        append_unique(source_refs, source, "source_id")

    claim = candidate.setdefault("claim", {})
    claim["statement"] = (
        "Qdrant payload indexes should be created for metadata fields repeatedly used in filtered retrieval; "
        "CEK-TA RAG results must separately preserve source provenance, formal_knowledge_id, citation resolution status and version metadata through CEK-TA contracts."
    )
    claim["evidence_summary"] = (
        str(claim.get("evidence_summary", ""))
        + "；CEK-TA Phase 42 RAG/vector 契约定义 source、chunk、formal knowledge id、version metadata 与 citation_result 回链。"
        + "；Phase 41 citation resolver 契约定义 citation_resolution_status 和 unsupported claim 降级/阻断语义。"
    )
    claim["interpretation_notes"] = (
        "本条拆分两层语义：Qdrant 文档只支撑 payload index/filtering 工具能力；"
        "formal_knowledge_id、citation status、source/version provenance 由 CEK-TA 内部契约约束。"
    )

    quality = candidate.setdefault("source_quality", {})
    quality["primary_source_count"] = len([s for s in source_refs if s.get("source_type") in {"official_doc", "internal_contract"}])
    quality["supporting_source_count"] = max(0, len(source_refs) - int(quality["primary_source_count"]))
    quality["low_reliability_source_count"] = len([s for s in source_refs if s.get("reliability") == "low"])
    quality["score"] = max(int(quality.get("score", 0)), 86)
    quality["limitations"] = [
        "Qdrant 来源支持 payload index/filtering；formal_knowledge_id、citation resolver 和 source provenance 由 CEK-TA 内部契约补足。",
        "本候选仍需二审确认补证是否足以升级 accepted_for_draft。",
    ]

    review = candidate.setdefault("review", {})
    review["supplement_status"] = "ready_for_reaudit"
    review["supplemental_evidence"] = {
        "supplemented_at": TODAY,
        "reason": "补充 CEK-TA formal index、citation resolver 和 RAG/vector storage 内部契约证据。",
        "verified_source_ids": [source["source_id"] for source in SUPPLEMENTAL_SOURCES],
        "claim_split": [
            "Qdrant payload index/filtering = 工具能力。",
            "formal_knowledge_id/citation/source version = CEK-TA provenance contract。",
        ],
        "expected_reaudit_decision": "accepted_for_draft 或继续 needs_more_evidence。",
    }
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        append_unique(
            audit_log,
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase42_p1_p003_supplemented",
                "reason": "按审计报告补充 CEK-TA RAG/vector、citation resolver 和主动检索协议来源。",
                "source_ids": [source["source_id"] for source in SUPPLEMENTAL_SOURCES],
            },
            "action",
        )

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["updated_at"] = TODAY
    status["decision_reason"] = "已补齐 CEK-TA provenance/citation/internal contract 证据，等待 P42-P1-003 二审。"
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "export_ai_audit"


def build_supplement_package(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": SUPPLEMENT_PACKAGE_ID,
        "package_type": "candidate_ai_reaudit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "source_audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": PACKAGE_ID,
        "phase": "42",
        "title": "Phase 42 P1 P42-P1-003 补证后二审包",
        "purpose": "请只审计 P42-P1-003 在补充 CEK-TA formal index / citation resolver / RAG vector storage 内部契约后，是否可升级为 accepted_for_draft。",
        "strict_boundaries": [
            "本包不能创建 reviewed、approved、default guidance 或 hard gate。",
            "accepted_for_draft 只表示可进入后续 formal draft/reviewed 准备，不等于 reviewed 或 approved。",
            "Qdrant payload index 只能证明工具能力；formal_knowledge_id/citation status/source version 属于 CEK-TA provenance contract。",
            "Vector DB 仍只能作为 retrieval index，不能成为 canonical store。",
        ],
        "audit_instructions": [
            "检查补充的 CEK-TA 内部契约是否足以覆盖 formal_knowledge_id、citation_resolution_status、source/version metadata。",
            "检查 claim 是否已经拆分 Qdrant 工具能力与 CEK-TA provenance contract。",
            "检查是否仍存在来源不足、claim 过强、默认指导越权或 Trading Engineering 污染。",
            "输出 decision 只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": SUPPLEMENT_PACKAGE_ID,
            "summary": {
                "total": 1,
                "accepted_for_draft": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
                "reviewed_allowed": 0,
                "approved_allowed": 0,
                "default_guidance_allowed": 0,
                "hard_gate_allowed": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P42-P1-003",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "high | medium | low",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "proposed_handoff_patch": {
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                    },
                }
            ],
        },
        "candidate_count": 1,
        "candidates": [candidate],
    }


def write_supplement_research(candidate: dict[str, Any]) -> None:
    source_ids = [source["source_id"] for source in SUPPLEMENTAL_SOURCES]
    lines = [
        "# Phase 42 P1 P42-P1-003 补证记录",
        "",
        "## 补证对象",
        "",
        f"- research_task_id: `{candidate.get('research_task_id')}`",
        f"- candidate_id: `{candidate.get('candidate_id')}`",
        "- 原审计结论：`needs_more_evidence`",
        "",
        "## 补证原因",
        "",
        "Qdrant 官方文档可以支撑 payload index 和 metadata filtering，但不能单独支撑 CEK-TA 的 `formal_knowledge_id`、`citation_resolution_status`、source version 和 formal index 回链语义。",
        "",
        "## 新增来源",
        "",
    ]
    for source in SUPPLEMENTAL_SOURCES:
        lines.append(f"- `{source['source_id']}`：{source['source_title']}，{source['source_url']}")
    lines.extend(
        [
            "",
            "## Claim 拆分",
            "",
            "```text",
            "Qdrant payload index/filtering = 工具能力。",
            "formal_knowledge_id/citation/source version = CEK-TA provenance contract。",
            "```",
            "",
            "## 边界",
            "",
            "本轮补证不代表 accepted、reviewed、approved、default guidance 或 hard gate。二审通过后仍只能进入 accepted_for_draft，后续 formal reviewed/caveat_only 需要另一个 gate。",
            "",
            "## verified_source_ids",
            "",
            "```text",
            "\n".join(source_ids),
            "```",
            "",
        ]
    )
    SUPPLEMENT_RESEARCH_PATH.write_text("\n".join(lines), encoding="utf-8")


def run() -> dict[str, Any]:
    audit_result = build_audit_result()
    write_json(AUDIT_RESULT_PATH, audit_result)

    updated: list[dict[str, str]] = []
    decision_counts: dict[str, int] = {}
    supplemented: list[str] = []
    for result in audit_result["candidate_results"]:
        candidate_id = str(result["candidate_id"])
        path = candidate_path(candidate_id)
        candidate = read_json(path)
        patch_candidate(candidate, audit_result, result)
        if result["research_task_id"] == "P42-P1-003":
            supplement_p003(candidate)
            write_json(SUPPLEMENT_PACKAGE_PATH, build_supplement_package(candidate))
            write_supplement_research(candidate)
            supplemented.append(candidate_id)
        write_json(path, candidate)
        decision = str(result["decision"])
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
        updated.append({"candidate_id": candidate_id, "research_task_id": str(result["research_task_id"]), "decision": decision})

    supplement_report = {
        "report_id": "phase42_p1_p003_supplemental_reaudit_package_report",
        "generated_at": TODAY,
        "audit_package_path": str(SUPPLEMENT_PACKAGE_PATH),
        "research_report_path": str(SUPPLEMENT_RESEARCH_PATH),
        "supplemented_candidate_ids": supplemented,
        "formal_knowledge_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "gate_status": "pass" if supplemented else "fail",
    }
    write_json(SUPPLEMENT_REPORT_PATH, supplement_report)

    report = {
        "report_id": "phase42_p1_audit_import_report",
        "generated_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_audit_result_path": str(AUDIT_RESULT_PATH),
        "package_id": PACKAGE_ID,
        "candidate_result_count": len(audit_result["candidate_results"]),
        "updated_count": len(updated),
        "decision_counts": decision_counts,
        "updated_candidates": updated,
        "supplemental_reaudit_package_path": str(SUPPLEMENT_PACKAGE_PATH),
        "formal_knowledge_created": 0,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "This import only updates candidate workflow and prepares one re-audit package. No formal reviewed knowledge is created.",
        "next_action": "等待 P42-P1-003 二审结果；5 条 accepted_for_draft 仍需后续 reviewed/caveat_only gate 才能正式沉淀。",
        "gate_status": "pass" if len(updated) == 6 and supplemented else "fail",
    }
    write_json(IMPORT_REPORT_PATH, report)
    return report


def main() -> int:
    report = run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
