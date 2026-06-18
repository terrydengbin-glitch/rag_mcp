"""Apply Phase 41 P41-A05-R1 third-audit result.

The third audit is delivered as an external report. This script archives a
structured audit result, updates only the candidate lifecycle state to
accepted_for_draft, and keeps reviewed/approved/default-guidance/hard-gate
permissions disabled.
"""

from __future__ import annotations

import argparse
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
AUDIT_RESULT_ID = "audit_result_phase41_a05_r1_third_audit_20260610_strict_v3"
SOURCE_PACKAGE_ID = "phase41_a05_r1_third_audit_package_20260610"
CANDIDATE_ID = "cand_20260610_phase41_p41_a05_model_selection_business_cost_latency_explainability_calibration_governance_001"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase41_a05_r1_third_audit_import_report.json", start_file=__file__
)
REMAINING_FOLLOWUP_PATH = resolve_repo_path(
    "docs", "reports", "phase41_candidate_remaining_evidence_followups.json", start_file=__file__
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_report_text_path", type=Path)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def validate_report_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    required_markers = [
        "P41-A05-R1",
        "accepted_for_draft",
        "不得 reviewed",
        "不得 approved",
        "不得 default guidance",
        "不得 hard gate",
    ]
    missing = [marker for marker in required_markers if marker not in text]
    if missing:
        raise ValueError(f"Audit report text misses required markers: {missing}")
    return text


def build_audit_result(report_text_path: Path) -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_date": TODAY,
        "decision": "accepted_for_draft",
        "scope": "P41-A05-R1 single-candidate third audit",
        "input_report_path": str(report_text_path),
        "candidate_id": CANDIDATE_ID,
        "research_task_id": "P41-A05-R1",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "hard_boundaries": [
            "accepted_for_draft is not reviewed.",
            "accepted_for_draft is not approved.",
            "default guidance remains disabled.",
            "hard gate remains disabled.",
            "Business cost must not define Trading PnL, fee, slippage, fill model, or execution body.",
            "Latency/SLO only covers AI scorer serving and audit-service response, not trading execution latency.",
        ],
        "source_dimensions_accepted": {
            "latency_slo": [
                "scikit-learn computational performance",
                "scikit-learn prediction latency example",
                "Google SRE implementing SLOs",
            ],
            "explainability_boundary": [
                "SHAP causal interpretation boundary",
            ],
            "calibration_quality": [
                "scikit-learn probability calibration",
                "scikit-learn CalibrationDisplay / reliability diagram",
                "scikit-learn Brier score loss",
            ],
            "business_cost": [
                "scikit-learn threshold tuning",
                "scikit-learn cost-sensitive threshold",
            ],
            "governance_complexity": [
                "NIST AI RMF",
                "MLflow Model Registry",
                "Phase41 runtime contract",
            ],
        },
        "formal_draft_schema_recommendation": {
            "schema_version": "phase41_model_selection_comparison_v1",
            "required_sections": [
                "business_cost",
                "latency_slo",
                "explainability_boundary",
                "calibration_quality",
                "governance_complexity",
            ],
            "required_tests": [
                "no_trading_body_test",
                "latency_scope_test",
                "explainability_not_causality_test",
                "calibration_gate_test",
                "accepted_only_permission_test",
            ],
        },
        "decision_reason": (
            "P41-A05-R1 has supplemented direct latency/SLO, explainability-boundary, "
            "and calibration-quality evidence. It may enter formal draft queue only."
        ),
    }


def enforce_safety(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "P41-A05-R1 third audit accepted for draft only; reviewed, approved, default guidance, and hard gate remain disabled."

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False


def apply_result(candidate: dict[str, Any], audit_result: dict[str, Any]) -> None:
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Unexpected candidate_id")
    if candidate.get("research_task_id") != "P41-A05-R1":
        raise ValueError("Unexpected research_task_id")

    enforce_safety(candidate)
    candidate.setdefault("status", {}).update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Phase 41 三审允许进入 formal draft 准备队列；不是 reviewed、approved 或默认指导。",
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
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_third_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = []
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": CANDIDATE_ID,
        "research_task_id": "P41-A05-R1",
        "decision": "accepted_for_draft",
        "reason": audit_result["decision_reason"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "hard_boundaries": audit_result["hard_boundaries"],
        "formal_draft_schema_recommendation": audit_result["formal_draft_schema_recommendation"],
        "import_policy": "third audit may route candidate only; formal reviewed/approved creation is blocked.",
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_a05_r1_third_audit_accepted_for_draft",
                "reason": "三审通过进入 formal draft 准备队列；不能直接 reviewed/approved/default guidance/hard gate。",
            }
        )

    trace = candidate.setdefault("phase41_trace", {})
    trace["third_audit_result"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "decision": "accepted_for_draft",
        "source_dimensions_accepted": audit_result["source_dimensions_accepted"],
        "formal_draft_schema_recommendation": audit_result["formal_draft_schema_recommendation"],
        "boundary": "accepted_for_draft only; no reviewed/approved/default guidance/hard gate.",
    }


def write_remaining_followups() -> None:
    payload = {
        "report_id": "phase41_candidate_remaining_evidence_followups",
        "generated_at": TODAY,
        "source_audit_result_id": AUDIT_RESULT_ID,
        "remaining_count": 0,
        "items": [],
        "boundary": "All Phase 41 P0-Core candidates are now accepted_for_draft or rejected source artifacts; none are reviewed, approved, default guidance, or hard gate enabled.",
    }
    write_json(REMAINING_FOLLOWUP_PATH, payload)


def main() -> None:
    args = parse_args()
    validate_report_text(args.audit_report_text_path)
    audit_result = build_audit_result(args.audit_report_text_path)
    write_json(AUDIT_RESULT_PATH, audit_result)

    candidate = read_json(CANDIDATE_PATH)
    apply_result(candidate, audit_result)
    write_json(CANDIDATE_PATH, candidate)
    write_remaining_followups()

    report = {
        "report_id": "phase41_a05_r1_third_audit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-326",
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_RESULT_PATH),
        "updated_candidate": repo_rel(CANDIDATE_PATH),
        "decision_counts": {"accepted_for_draft": 1},
        "remaining_needs_more_evidence": 0,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "remaining_followups": repo_rel(REMAINING_FOLLOWUP_PATH),
        "status_boundary": "三审只允许 accepted_for_draft；未生成 formal reviewed。",
        "next_action": "如需进入正式知识库，需要单独执行 formal draft/reviewed 转换任务和运行时联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
