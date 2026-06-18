"""Apply Phase 42 P1 reviewed-preparation audit result.

This task consumes the external reviewed/caveat_only preparation audit for the
six Phase 42 P1 database/storage engineering candidates. It creates formal
reviewed/caveat_only knowledge only for entries explicitly allowed by the audit.
It never creates approved, default guidance, hard gate, or production database
changes.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402

import promote_phase42_accepted_candidates_to_reviewed as base  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-355"
base.TASK_ID = TASK_ID

AUDIT_RESULT_PATH = resolve_repo_path(
    "docs",
    "audit",
    "audit_result_phase42_p1_reviewed_preparation_20260611_strict_v1.json",
    start_file=__file__,
)
REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase42_p1_reviewed_preparation_import_report.json",
    start_file=__file__,
)
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    start_file=__file__,
)


AUDIT_DECISIONS: dict[str, dict[str, Any]] = {
    "P42-P1-001": {
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "summary": "pgvector/Qdrant 只作为 vector retrieval storage 选择边界；vector store 不能替代 canonical store。",
    },
    "P42-P1-002": {
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "summary": "HNSW/IVFFlat 选择必须绑定 workload benchmark，不存在默认最佳索引。",
    },
    "P42-P1-003": {
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "summary": "Qdrant payload index 是工具过滤能力，formal knowledge/citation 语义必须由 CEK-TA provenance 契约解析。",
    },
    "P42-P1-004": {
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "summary": "Feast 只在 offline/online parity、point-in-time retrieval、feature reuse 和 serving latency 压力足够时作为条件基础设施。",
    },
    "P42-P1-005": {
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "summary": "MLflow Registry 可补充版本、alias、tag 和 metadata，但不能替代 composite release manifest 或发布审批。",
    },
    "P42-P1-006": {
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "summary": "RLS/pgAudit 只作为条件安全增强项，生产启用必须另有 policy、性能、保留期和安全审批。",
    },
}


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": "audit_result_phase42_p1_reviewed_preparation_20260611_strict_v1",
        "created_at": TODAY,
        "phase": "Phase 42",
        "task_id": TASK_ID,
        "input_package": "docs/audit/phase42_p1_reviewed_preparation_audit_package_20260611.json",
        "scope": "Phase 42 P1 accepted_for_draft candidates reviewed/caveat_only preparation audit",
        "quality_gate": "pass",
        "package_decision": "conditional_accept_for_formal_reviewed_caveat_only_preparation",
        "summary": {
            "candidate_count": len(AUDIT_DECISIONS),
            "accepted_for_reviewed_caveat_only": len(AUDIT_DECISIONS),
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
            "reviewed_allowed": len(AUDIT_DECISIONS),
            "approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "hard_boundaries": {
            "create_approved": False,
            "create_default_guidance": False,
            "enable_hard_gate": False,
            "create_real_database": False,
            "execute_migration": False,
            "enable_qdrant_feast_mlflow_rls_pgaudit": False,
            "change_mcp_or_api_write_permissions": False,
            "generate_trading_execution_advice": False,
        },
        "required_formal_defaults": {
            "target_review_status": "reviewed",
            "review_mode": "caveat_only",
            "machine_gate.default_guidance": "caveat_only",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        },
        "items": [
            {
                "research_task_id": task_id,
                "decision": decision["decision"],
                "reviewed_allowed": decision["reviewed_allowed"],
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "summary": decision["summary"],
            }
            for task_id, decision in sorted(AUDIT_DECISIONS.items())
        ],
    }


def load_p1_candidates() -> list[tuple[Path, dict[str, Any]]]:
    candidates: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase42_p42_p1_*.json")):
        candidates.append((path, base.read_json(path)))
    return candidates


def task_id_for(candidate: dict[str, Any]) -> str:
    return str(candidate.get("research_task_id", ""))


def main() -> int:
    audit_payload = audit_result_payload()
    base.write_json(AUDIT_RESULT_PATH, audit_payload)

    promoted: list[dict[str, Any]] = []
    skipped: Counter[str] = Counter()
    touched_candidates: list[str] = []

    for candidate_path, candidate in load_p1_candidates():
        research_task_id = task_id_for(candidate)
        decision = AUDIT_DECISIONS.get(research_task_id)
        if not decision:
            skipped["not_in_audit_result"] += 1
            continue
        if decision.get("decision") != "accepted_for_reviewed_caveat_only" or decision.get("reviewed_allowed") is not True:
            skipped["reviewed_not_allowed"] += 1
            continue

        reason = base.validate_candidate_for_promotion(candidate)
        if reason:
            skipped[reason] += 1
            continue

        review = candidate.setdefault("review", {})
        ai_audit = review.setdefault("ai_audit", {})
        if isinstance(ai_audit, dict):
            ai_audit.update(
                {
                    "audit_result_id": audit_payload["audit_result_id"],
                    "decision": "accepted_for_reviewed_caveat_only",
                    "allowed_next_stage": "formal_reviewed_knowledge",
                    "reviewed_allowed": True,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                }
            )

        workflow = candidate.setdefault("workflow", {})
        workflow.update(
            {
                "reviewed_preparation_audit_result_id": audit_payload["audit_result_id"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
        )

        item = base.candidate_to_knowledge(candidate)
        item["review"]["ai_audit"]["decision"] = "accepted_for_reviewed_caveat_only"
        item["review"]["ai_audit"]["audit_result_id"] = audit_payload["audit_result_id"]
        item["machine_gate"]["reason"] = (
            "CEK-TA-355 按 Phase 42 P1 reviewed-preparation 审计结果沉淀为 formal reviewed/caveat_only；"
            "不可作为 approved 默认指导或 hard gate。"
        )
        item["phase42_conversion"]["promoted_by_task"] = TASK_ID
        item["phase42_conversion"]["reviewed_preparation_audit_result_id"] = audit_payload["audit_result_id"]

        knowledge_path = base.write_knowledge(item)
        base.update_candidate_backlink(candidate, item, knowledge_path)
        base.write_json(candidate_path, candidate)
        touched_candidates.append(base.rel(candidate_path))
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": research_task_id,
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": base.rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
        )

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase42_p1_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_path": base.rel(AUDIT_RESULT_PATH),
        "input_scope": "Phase 42 P1 six accepted_for_draft candidates with reviewed_allowed=true",
        "promoted_count": len(promoted),
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "formal_knowledge_created": len(promoted),
        "reviewed_created": len(promoted),
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate; no production database changes.",
    }
    base.write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
