"""Apply Phase 38 P0-Core supplemental re-audit result.

The re-audit accepts seven supplemented candidates for the formal draft queue
and keeps G04-R1 in needs-more-evidence after fixing default-guidance metadata.
It does not create reviewed or approved knowledge.
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


TODAY = date(2026, 6, 10).isoformat()
AUDIT_RESULT_ID = "audit_result_phase38_p0_core_supplemental_reaudit_20260610_strict_v2"
SOURCE_PACKAGE_ID = "phase38_p0_core_supplemental_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_p0_core_supplemental_reaudit_import_report.json", start_file=__file__
)

ACCEPTED_TASKS = {
    "P38-D03": "补齐 formal index / citation resolver 契约，可进入 formal draft。",
    "P38-D04": "补齐 RAG faithfulness、OWASP 和 no-hit policy，可进入 formal draft。",
    "P38-D05": "补齐 unsupported_claims routing；draft 中需避免写成自动 hard block。",
    "P38-D06": "补齐 JSON Schema enum、Structured Outputs 和 reason taxonomy，可进入 formal draft。",
    "P38-E01": "已修正 offline eval 反事实边界，可进入 formal draft。",
    "P38-G01": "作为 CEK-TA 内部主动检索协议可进入 formal draft，不得写成通用行业强制规则。",
    "P38-G03": "补齐 machine_gate / review_status 契约，可进入 formal draft。",
}

G04_TASK = "P38-G04-R1"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    indexed: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        item = read_json(path)
        task_id = item.get("research_task_id")
        if isinstance(task_id, str):
            indexed[task_id] = (path, item)
    return indexed


def ensure_default_guidance_block(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    audit = review.setdefault("ai_audit", {})
    if isinstance(audit, dict):
        audit["default_guidance_allowed"] = False
    conversion = candidate.setdefault("conversion_target", {})
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False


def append_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    review = candidate.setdefault("review", {})
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def mark_accepted(candidate: dict[str, Any], reason: str) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": f"补证二审通过：{reason} 仅进入 formal draft 队列，不是 reviewed、approved 或 default guidance。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "ai_audited",
            "queue_group": "ai_passed",
            "formal_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
            "formal_review_status": "draft",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "next_action": "apply_ai_audit_patch",
        }
    )
    ensure_default_guidance_block(candidate)
    review = candidate.setdefault("review", {})
    review["reviewed_at"] = TODAY
    review["reviewer"] = "external_ai_reaudit_plus_codex_import"
    review["open_questions"] = ["进入 formal draft 转换时必须保留二审 patch notes 和 default_guidance=false。"]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "default_guidance_allowed": False,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "hard_gate_allowed": False,
        "notes": reason,
    }
    append_log(candidate, "supplemental_reaudit_accepted_for_draft", reason)
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "notes": reason,
        "default_guidance_allowed": False,
    }


def keep_g04_needs_more_evidence(candidate: dict[str, Any]) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "hold_for_metadata_clarification",
            "decision_reason": "二审确认空 slug 已修复，但仍需澄清 approval_allowed、draft_conversion_allowed 和 default guidance 元数据。",
            "updated_at": TODAY,
        }
    )
    candidate["parent_rejected_candidate_id"] = "cand_20260610_phase38_p38_g04__001"
    candidate["replacement_reason"] = "fix_empty_slug"
    candidate["draft_conversion_allowed"] = True
    candidate["default_guidance_allowed"] = False
    candidate["context_budget_policy_version"] = "phase38_context_budget_policy_v1"
    candidate["field_whitelist_version"] = "phase38_default_knowledge_pack_fields_v1"
    candidate["top_k"] = 5
    candidate["token_budget"] = 4000
    candidate["detail_expansion_policy"] = "explicit_request_required"
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["draft_conversion_allowed"] = True
    conflict["resolution_summary"] = (
        "原空 slug 已修复；本候选仍不得 approved/default guidance，等待二审后续确认是否进入 formal draft。"
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "next_action": "metadata_clarification_then_reaudit",
        }
    )
    ensure_default_guidance_block(candidate)
    review = candidate.setdefault("review", {})
    review["reviewed_at"] = TODAY
    review["reviewer"] = "external_ai_reaudit_plus_codex_import"
    review["open_questions"] = [
        "确认 draft_conversion_allowed=true 与 approval_allowed=false 的状态语义。",
        "确认 context_budget_policy_version、field_whitelist_version、top_k、token_budget 和 detail_expansion_policy 是否满足二审要求。",
    ]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "allowed_next_stage": "metadata_clarification_queue",
        "default_guidance_allowed": False,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "hard_gate_allowed": False,
        "notes": "G04-R1 空 slug 已修复，但 approval_allowed=false 与 hidden/default guidance 元数据需澄清。",
    }
    append_log(candidate, "supplemental_reaudit_needs_metadata_clarification", "G04-R1 保留补证队列。")
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": "needs_more_evidence",
        "allowed_next_stage": "metadata_clarification_queue",
        "notes": "空 slug 已修复；仍需元数据澄清，不进入 formal draft。",
        "default_guidance_allowed": False,
    }


def main() -> int:
    indexed = load_candidates()
    expected = set(ACCEPTED_TASKS) | {G04_TASK}
    missing = sorted(task_id for task_id in expected if task_id not in indexed)
    if missing:
        raise SystemExit(f"Missing candidates: {missing}")

    decisions: list[dict[str, Any]] = []
    touched: list[str] = []
    for task_id, reason in ACCEPTED_TASKS.items():
        path, candidate = indexed[task_id]
        decisions.append(mark_accepted(candidate, reason))
        write_json(path, candidate)
        touched.append(rel(path))

    g04_path, g04 = indexed[G04_TASK]
    decisions.append(keep_g04_needs_more_evidence(g04))
    write_json(g04_path, g04)
    touched.append(rel(g04_path))

    audit_result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_reaudit_imported_by_codex",
        "overall_decision": "conditional_accept_for_formal_draft_queue",
        "decision_summary": {
            "accepted_for_draft": 7,
            "needs_more_evidence": 1,
            "rejected": 0,
            "default_guidance_allowed": 0,
            "direct_reviewed_allowed": 0,
            "direct_approved_allowed": 0,
        },
        "global_patch": {
            "hidden_from_default_queue": "true for the supplemental scope to avoid default guidance ambiguity",
            "default_guidance_allowed": False,
            "accepted_for_draft_is_reviewed": False,
            "accepted_for_draft_is_approved": False,
        },
        "decisions": decisions,
    }
    write_json(AUDIT_PATH, audit_result)

    report = {
        "report_id": "phase38_p0_core_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_path": rel(AUDIT_PATH),
        "candidate_count": len(decisions),
        "touched_files": touched,
        "decision_summary": audit_result["decision_summary"],
        "g04_r1_status": "needs_more_evidence_metadata_clarification",
        "formal_reviewed_created": False,
        "approved_created": False,
        "default_guidance_enabled": False,
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
