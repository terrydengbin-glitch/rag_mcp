"""Apply the Phase 40 P0-Core strict audit result to candidate files.

The strict audit result can route candidates into draft-ready,
needs-more-evidence, and rejected queues, but it does not authorize
formal reviewed/approved knowledge or default guidance.
"""

from __future__ import annotations

import argparse
import copy
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
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase40_p0_core_continuous_learning_20260610_strict_v1"
EXPECTED_SOURCE_PACKAGE_ID = "phase40_candidate_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_COPY_PATH = resolve_repo_path(
    "docs", "audit", f"{EXPECTED_AUDIT_RESULT_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_p0_core_audit_import_report.json", start_file=__file__
)

REBUILT_CANDIDATES = {
    "P40-C10": {
        "research_task_id": "P40-C10-R1",
        "candidate_id": "cand_20260610_phase40_p40_c10_retraining_trigger_audit_record_001",
        "normalized_claim": "phase40.retraining_trigger_audit_record.v1",
        "proposed_knowledge_id": "kb_ai_feedback_governance.phase40.retraining_trigger_audit_record.v1",
        "search_direction": "retraining trigger audit record dataset version approval",
        "evidence_summary": (
            "重建候选：再训练触发必须记录触发原因、样本窗口、数据版本和审批状态；"
            "需要补充 MLflow、TFDV、NIST 与 CEK-TA retraining trigger contract 后重新审计。"
        ),
    },
    "P40-C11": {
        "research_task_id": "P40-C11-R1",
        "candidate_id": "cand_20260610_phase40_p40_c11_retrain_recalibration_threshold_reliability_001",
        "normalized_claim": "phase40.retrain_recalibration_threshold_reliability.v1",
        "proposed_knowledge_id": (
            "kb_ai_feedback_governance.phase40.retrain_recalibration_threshold_reliability.v1"
        ),
        "search_direction": "retrain recalibration threshold reliability brier ece grouped calibration",
        "evidence_summary": (
            "重建候选：每次再训练后必须重新校准概率、阈值和分组可靠性；"
            "需要保留校准、Brier、TFDV 和分组可靠性证据后重新审计。"
        ),
    },
    "P40-C18": {
        "research_task_id": "P40-C18-R1",
        "candidate_id": "cand_20260610_phase40_p40_c18_feedback_loop_label_provenance_001",
        "normalized_claim": "phase40.feedback_loop_label_provenance.v1",
        "proposed_knowledge_id": "kb_ai_feedback_governance.phase40.feedback_loop_label_provenance.v1",
        "search_direction": "feedback loop label provenance self training model generated labels",
        "evidence_summary": (
            "重建候选：自标注、模型生成标签和选择性日志必须标注来源，避免反馈回路污染；"
            "需要补充 self-training、model-generated labels 与 feedback-loop contamination 证据后重新审计。"
        ),
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "audit_result_path",
        type=Path,
        help="Path to phase40_candidate_audit_result_20260610_strict_v1.json",
    )
    return parser.parse_args()


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase40_*.json")):
        candidate = read_json(path)
        task_id = candidate.get("research_task_id")
        if isinstance(task_id, str):
            candidates[task_id] = (path, candidate)
    return candidates


def decision_by_task(audit_result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for decision in audit_result.get("decisions", []):
        if not isinstance(decision, dict):
            continue
        task_id = decision.get("research_task_id")
        if isinstance(task_id, str):
            decisions[task_id] = decision
    return decisions


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    review = candidate.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def enforce_candidate_safety(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False

    conversion_target = candidate.setdefault("conversion_target", {})
    conversion_target["default_guidance_allowed"] = False
    conversion_target["hard_gate_allowed"] = False
    conversion_target.setdefault("target_review_status", "draft")

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = (
        "candidate only; external audit does not allow reviewed, approved, default guidance, or hard gate."
    )

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False

    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False


def apply_ai_audit(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "source_package_id": EXPECTED_SOURCE_PACKAGE_ID,
        "candidate_id": decision.get("candidate_id"),
        "research_task_id": decision.get("research_task_id"),
        "decision": decision.get("decision"),
        "reason": decision.get("reason"),
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
        "reviewed_allowed": bool(decision.get("reviewed_allowed")),
        "approved_allowed": bool(decision.get("approved_allowed")),
        "default_guidance_allowed": bool(decision.get("default_guidance_allowed")),
        "hard_gate_allowed": bool(decision.get("hard_gate_allowed")),
        "import_policy": (
            "strict audit result may route candidates only; formal reviewed/approved creation is blocked."
        ),
    }
    followups = decision.get("required_followups", [])
    if isinstance(followups, list):
        review["open_questions"] = followups


def mark_accepted_for_draft(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": (
                "外部严格审计允许进入 formal draft 准备队列；不是 reviewed、approved 或默认指导。"
            ),
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
            "ai_audit_result_id": EXPECTED_AUDIT_RESULT_ID,
            "next_action": "prepare_formal_draft_after_codex_patch_review",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(
        candidate,
        "phase40_strict_audit_accepted_for_draft",
        "候选进入 formal draft 准备队列；直接 reviewed/approved 被审计结果禁止。",
    )


def mark_needs_more_evidence(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "外部严格审计要求补充更贴近 claim 的来源、实例或 CEK-TA 契约后再二审。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": EXPECTED_AUDIT_RESULT_ID,
            "next_action": "supplement_sources_and_export_reaudit_package",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase40_strict_audit_needs_more_evidence", "需补证后二审。")


def mark_rejected(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "rejected",
            "ingestion_decision": "reject",
            "decision_reason": "外部严格审计发现空 slug 结构污染风险，原候选禁止进入 formal draft。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "rejected",
            "queue_group": "rejected",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": EXPECTED_AUDIT_RESULT_ID,
            "next_action": "rebuilt_candidate_created",
        }
    )
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "potential"
    conflict["resolution_summary"] = "候选含空 slug，可能污染 formal index；已按审计建议创建重建候选。"
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase40_strict_audit_rejected", "空 slug 污染风险，原件归档。")


def rebuild_candidate(old_candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    task_id = old_candidate["research_task_id"]
    meta = REBUILT_CANDIDATES[task_id]
    rebuilt = copy.deepcopy(old_candidate)
    rebuilt["candidate_id"] = meta["candidate_id"]
    rebuilt["research_task_id"] = meta["research_task_id"]

    claim = rebuilt.setdefault("claim", {})
    claim["normalized_claim"] = meta["normalized_claim"]
    claim["evidence_summary"] = meta["evidence_summary"]

    conversion_target = rebuilt.setdefault("conversion_target", {})
    conversion_target["proposed_knowledge_id"] = meta["proposed_knowledge_id"]
    conversion_target["target_review_status"] = "draft"

    status = rebuilt.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "ready_for_reaudit",
            "decision_reason": "由 rejected 空 slug 候选重建；需补充审计要求的来源后再二审。",
            "created_at": TODAY,
            "updated_at": TODAY,
        }
    )

    phase_trace = rebuilt.setdefault("phase40_trace", {})
    phase_trace["search_direction"] = meta["search_direction"]
    phase_trace["rebuilt_from_candidate_id"] = old_candidate.get("candidate_id")
    phase_trace["rebuilt_reason"] = "fix_empty_slug_metadata_pollution"

    enforce_candidate_safety(rebuilt)
    rebuilt_conflict = rebuilt.setdefault("conflict_audit", {})
    rebuilt_conflict["conflict_status"] = "potential"
    rebuilt_conflict["resolution_summary"] = (
        "原候选存在空 slug 污染风险；重建候选已修复 ID，但仍需补证和二审。"
    )
    workflow = rebuilt.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": EXPECTED_AUDIT_RESULT_ID,
            "next_action": "supplement_sources_and_export_reaudit_package",
            "parent_rejected_candidate_id": old_candidate.get("candidate_id"),
        }
    )

    review = rebuilt.setdefault("review", {})
    review["reviewer"] = "codex_rebuild_after_external_audit"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "source_package_id": EXPECTED_SOURCE_PACKAGE_ID,
        "decision": "rebuilt_needs_more_evidence",
        "parent_decision": decision.get("decision"),
        "parent_candidate_id": old_candidate.get("candidate_id"),
        "required_followups": decision.get("required_followups", []),
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }
    review["open_questions"] = decision.get("required_followups", [])
    append_audit_log(
        rebuilt,
        "phase40_rebuilt_from_rejected_empty_slug",
        "修复 candidate_id、normalized_claim 和 proposed_knowledge_id 后进入补证队列。",
    )
    return rebuilt


def validate_audit_result(audit_result: dict[str, Any]) -> None:
    if audit_result.get("audit_result_id") != EXPECTED_AUDIT_RESULT_ID:
        raise ValueError("Unexpected audit_result_id")
    if audit_result.get("source_package_id") != EXPECTED_SOURCE_PACKAGE_ID:
        raise ValueError("Unexpected source_package_id")
    decisions = decision_by_task(audit_result)
    missing = [f"P40-C{i:02d}" for i in range(1, 19) if f"P40-C{i:02d}" not in decisions]
    if missing:
        raise ValueError(f"Missing audit decisions: {missing}")


def main() -> int:
    args = parse_args()
    audit_result = read_json(args.audit_result_path)
    validate_audit_result(audit_result)
    write_json(AUDIT_COPY_PATH, audit_result)

    candidates = load_candidates()
    decisions = decision_by_task(audit_result)

    touched: list[str] = []
    rebuilt_paths: list[str] = []
    counts = {"accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "rebuilt": 0}

    for task_id, decision in sorted(decisions.items()):
        if task_id not in candidates:
            raise ValueError(f"Candidate for {task_id} not found")
        path, candidate = candidates[task_id]
        if candidate.get("candidate_id") != decision.get("candidate_id"):
            raise ValueError(f"Candidate ID mismatch for {task_id}")

        decision_value = decision.get("decision")
        if decision_value == "accepted_for_draft":
            mark_accepted_for_draft(candidate, decision)
            counts["accepted_for_draft"] += 1
        elif decision_value == "needs_more_evidence":
            mark_needs_more_evidence(candidate, decision)
            counts["needs_more_evidence"] += 1
        elif decision_value == "rejected":
            mark_rejected(candidate, decision)
            counts["rejected"] += 1
            if task_id in REBUILT_CANDIDATES:
                rebuilt = rebuild_candidate(candidate, decision)
                rebuilt_path = CANDIDATE_DIR / f"{rebuilt['candidate_id']}.json"
                write_json(rebuilt_path, rebuilt)
                rebuilt_paths.append(repo_rel(rebuilt_path))
                counts["rebuilt"] += 1
        else:
            raise ValueError(f"Unsupported decision {decision_value!r} for {task_id}")

        write_json(path, candidate)
        touched.append(repo_rel(path))

    report = {
        "report_id": "phase40_p0_core_audit_import_report",
        "generated_at": TODAY,
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "source_package_id": EXPECTED_SOURCE_PACKAGE_ID,
        "input_audit_result_path": str(args.audit_result_path),
        "canonical_audit_result_path": repo_rel(AUDIT_COPY_PATH),
        "decision_counts": counts,
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_allowed_count": 0,
        "hard_gate_allowed_count": 0,
        "formal_creation_blocked_reason": (
            "The strict audit result sets reviewed_allowed=false for every decision; "
            "accepted_for_draft is routed to draft preparation only."
        ),
        "touched_candidates": touched,
        "rebuilt_candidates": rebuilt_paths,
        "next_steps": [
            "对 needs_more_evidence 与 rebuilt 候选补充来源和实例。",
            "导出二审 JSON。",
            "二审允许 reviewed 后再创建 formal reviewed knowledge 并重建 knowledge_items.json。",
        ],
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"ok": True, "report": repo_rel(REPORT_PATH), "counts": counts}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
