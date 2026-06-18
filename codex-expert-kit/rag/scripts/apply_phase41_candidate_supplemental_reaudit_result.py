"""Apply Phase 41 supplemental reaudit result.

This import handles the second audit round for the Phase 41 supplemental
reaudit package. It may route candidates to accepted_for_draft or
needs_more_evidence, but it must not create reviewed/approved knowledge or
enable default guidance/hard gate permissions.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
AUDIT_RESULT_ID = "audit_result_phase41_candidate_supplemental_reaudit_20260610_strict_v2"
SOURCE_PACKAGE_ID = "phase41_candidate_supplemental_reaudit_package_20260610"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT_COPY_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase41_candidate_supplemental_reaudit_import_report.json", start_file=__file__)
REMAINING_FOLLOWUP_PATH = resolve_repo_path(
    "docs", "reports", "phase41_candidate_remaining_evidence_followups.json", start_file=__file__
)

EXPECTED_CANDIDATES = {
    "cand_20260610_phase41_p41_a05_model_selection_business_cost_latency_explainability_calibration_governance_001",
    "cand_20260610_phase41_p41_b01_bad_trade_false_allow_class_weight_sample_weight_001",
    "cand_20260610_phase41_p41_b03_time_aware_split_no_random_shuffle_001",
    "cand_20260610_phase41_p41_c03_threshold_policy_false_allow_false_block_review_capacity_001",
    "cand_20260610_phase41_p41_d02_offline_online_feature_parity_default_guidance_block_001",
    "cand_20260610_phase41_p41_e03_qwen3_rag_abstain_needs_human_review_001",
    "cand_20260610_phase41_p41_e09_rag_context_qwen3_prompt_injection_guard_citation_resolver_unsupported_claim_detector_schema_validation_001",
    "cand_20260610_phase41_p41_f02_composite_release_manifest_scorer_calibrator_threshold_qwen3_prompt_rag_index_reason_taxonomy_rollback_target_001",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_result_path", type=Path)
    return parser.parse_args()


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


def validate_audit_result(audit_result: dict[str, Any]) -> None:
    if audit_result.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError("Unexpected audit_result_id")
    if audit_result.get("source_package_id") != SOURCE_PACKAGE_ID:
        raise ValueError("Unexpected source_package_id")
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list):
        raise ValueError("decisions must be a list")

    candidate_ids = {item.get("candidate_id") for item in decisions if isinstance(item, dict)}
    missing = sorted(EXPECTED_CANDIDATES - candidate_ids)
    unexpected = sorted(candidate_ids - EXPECTED_CANDIDATES)
    if missing:
        raise ValueError(f"Missing candidate decisions: {missing}")
    if unexpected:
        raise ValueError(f"Unexpected candidate decisions: {unexpected}")

    allowed_decisions = {"accepted_for_draft", "needs_more_evidence", "rejected"}
    bad_decisions = [
        item.get("candidate_id")
        for item in decisions
        if isinstance(item, dict) and item.get("decision") not in allowed_decisions
    ]
    if bad_decisions:
        raise ValueError(f"Unexpected decisions: {bad_decisions}")

    forbidden = [
        item.get("candidate_id")
        for item in decisions
        if isinstance(item, dict)
        and (
            item.get("reviewed_allowed")
            or item.get("approved_allowed")
            or item.get("default_guidance_allowed")
            or item.get("hard_gate_allowed")
        )
    ]
    if forbidden:
        raise ValueError(f"Audit result unexpectedly allowed reviewed/approved/default/hard gate: {forbidden}")


def load_candidates_by_id() -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_*.json")):
        candidate = read_json(path)
        candidate_id = candidate.get("candidate_id")
        if isinstance(candidate_id, str):
            result[candidate_id] = (path, candidate)
    return result


def enforce_safety(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False

    conversion = candidate.setdefault("conversion_target", {})
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conversion["target_review_status"] = "draft"

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "candidate only; Phase 41 supplemental reaudit does not allow reviewed, approved, default guidance, or hard gate."

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def apply_review_payload(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_supplemental_reaudit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": decision.get("candidate_id"),
        "research_task_id": decision.get("research_task_id"),
        "decision": decision.get("decision"),
        "reason": decision.get("reason"),
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "import_policy": "supplemental audit result may route candidates only; formal reviewed/approved creation is blocked.",
    }
    followups = decision.get("required_followups", [])
    review["open_questions"] = followups if isinstance(followups, list) else []

    trace = candidate.setdefault("phase41_trace", {})
    trace["supplemental_reaudit_patch_notes"] = {
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
    }
    trace["supplemental_reaudit_result_id"] = AUDIT_RESULT_ID

    limitations = candidate.setdefault("applicability", {}).setdefault("limitations", [])
    for note in decision.get("boundary_patch_notes", []) or []:
        if isinstance(note, str) and note not in limitations:
            limitations.append(note)


def mark_accepted(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_safety(candidate)
    candidate.setdefault("status", {}).update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Phase 41 二审允许进入 formal draft 准备队列；不是 reviewed、approved 或默认指导。",
            "updated_at": TODAY,
        }
    )
    candidate.setdefault("workflow", {}).update(
        {
            "stage": "ai_audited",
            "queue_group": "ai_passed",
            "formal_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
            "formal_review_status": "draft",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "prepare_formal_draft_after_codex_patch_review",
        }
    )
    apply_review_payload(candidate, decision)
    append_audit_log(candidate, "phase41_supplemental_reaudit_accepted_for_draft", "二审通过进入 formal draft 准备队列；不能直接 reviewed/approved。")


def mark_needs_more_evidence(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_safety(candidate)
    candidate.setdefault("status", {}).update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "Phase 41 二审要求继续补充 claim-specific 来源或拆分 claim 后再审。",
            "updated_at": TODAY,
        }
    )
    candidate.setdefault("workflow", {}).update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "supplement_sources_or_split_claim_then_export_reaudit_package",
        }
    )
    apply_review_payload(candidate, decision)
    append_audit_log(candidate, "phase41_supplemental_reaudit_needs_more_evidence", "二审仍要求补证或拆分 claim。")


def mark_rejected(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_safety(candidate)
    candidate.setdefault("status", {}).update(
        {
            "review_status": "rejected",
            "ingestion_decision": "reject",
            "decision_reason": "Phase 41 二审拒绝该候选进入 formal draft。",
            "updated_at": TODAY,
        }
    )
    candidate.setdefault("workflow", {}).update(
        {
            "stage": "rejected",
            "queue_group": "rejected",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "none",
        }
    )
    apply_review_payload(candidate, decision)
    append_audit_log(candidate, "phase41_supplemental_reaudit_rejected", "二审拒绝该候选。")


def apply_decision(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    decision_value = decision.get("decision")
    if decision_value == "accepted_for_draft":
        mark_accepted(candidate, decision)
    elif decision_value == "needs_more_evidence":
        mark_needs_more_evidence(candidate, decision)
    elif decision_value == "rejected":
        mark_rejected(candidate, decision)
    else:
        raise ValueError(f"Unsupported decision: {decision_value}")


def collect_remaining_followups(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    remaining: list[dict[str, Any]] = []
    for decision in decisions:
        if decision.get("decision") == "needs_more_evidence":
            remaining.append(
                {
                    "candidate_id": decision.get("candidate_id"),
                    "research_task_id": decision.get("research_task_id"),
                    "reason": decision.get("reason"),
                    "source_patch_notes": decision.get("source_patch_notes", []),
                    "content_patch_notes": decision.get("content_patch_notes", []),
                    "boundary_patch_notes": decision.get("boundary_patch_notes", []),
                    "required_followups": decision.get("required_followups", []),
                }
            )
    return remaining


def main() -> None:
    args = parse_args()
    audit_result = read_json(args.audit_result_path)
    validate_audit_result(audit_result)

    AUDIT_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.audit_result_path, AUDIT_COPY_PATH)

    candidates = load_candidates_by_id()
    updated_paths: list[str] = []
    decisions = [item for item in audit_result["decisions"] if isinstance(item, dict)]
    counts: Counter[str] = Counter()

    for decision in decisions:
        candidate_id = str(decision["candidate_id"])
        if candidate_id not in candidates:
            raise ValueError(f"Candidate file not found for {candidate_id}")
        path, candidate = candidates[candidate_id]
        apply_decision(candidate, decision)
        write_json(path, candidate)
        updated_paths.append(repo_rel(path))
        counts[str(decision.get("decision"))] += 1

    remaining = collect_remaining_followups(decisions)
    write_json(
        REMAINING_FOLLOWUP_PATH,
        {
            "report_id": "phase41_candidate_remaining_evidence_followups",
            "generated_at": TODAY,
            "source_audit_result_id": AUDIT_RESULT_ID,
            "remaining_count": len(remaining),
            "items": remaining,
            "boundary": "remaining candidates are not reviewed, approved, default guidance, or hard gate enabled.",
        },
    )

    report = {
        "report_id": "phase41_candidate_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-326",
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_COPY_PATH),
        "decision_counts": dict(counts),
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "updated_candidates": updated_paths,
        "remaining_followups": repo_rel(REMAINING_FOLLOWUP_PATH),
        "status_boundary": "本次二审 reviewed_allowed_count=0；只回写候选状态，不生成 formal reviewed。",
        "next_action": "继续为 P41-A05-R1 补充 latency、explainability、calibration quality 证据，或拆分 claim 后再审。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
