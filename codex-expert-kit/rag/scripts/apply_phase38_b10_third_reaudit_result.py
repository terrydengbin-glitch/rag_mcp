"""Import Phase 38 B10 third re-audit result.

B10 is accepted for the formal draft queue only. This script applies the
third-audit boundary patches, deduplicates source refs, and keeps B10 out of
reviewed, approved, default-guidance, and hard-gate use.
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
AUDIT_RESULT_ID = "audit_result_phase38_b10_bayesian_calibration_third_reaudit_20260610_strict_v3"
SOURCE_PACKAGE_ID = "phase38_b10_bayesian_calibration_third_audit_package_20260610"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    "cand_20260610_phase38_p38_b10_conformal_bayesian_calibration_001.json",
    start_file=__file__,
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_b10_bayesian_calibration_third_reaudit_import_report.json", start_file=__file__
)


ACCEPTED_REASON = (
    "B10 三审通过：PMLR calibrated regression 支撑 Bayesian/probabilistic uncertainty calibration，"
    "AAAI Bayesian Binning into Quantiles 支撑 Bayesian classifier probability calibration。"
)

FINAL_DRAFT_TITLE = "Conformal / Bayesian Calibration as an Uncertainty Enhancement Layer"
FINAL_DRAFT_STATEMENT = (
    "Conformal and Bayesian/probabilistic calibration methods may improve uncertainty or probability quality "
    "under explicit assumptions and sufficient calibration data, but they are enhancement layers only; they must "
    "not replace deterministic final gate, threshold governance, shadow/paper evaluation, or human review."
)


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


def canonicalize_sources(candidate: dict[str, Any]) -> dict[str, Any]:
    refs = candidate.get("source_refs", [])
    if not isinstance(refs, list):
        return {"removed_duplicate_source_ids": [], "governance_source_ids": []}

    seen_urls: set[str] = set()
    deduped: list[dict[str, Any]] = []
    removed: list[str] = []
    governance: list[str] = []
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        url = str(ref.get("source_url", "")).strip()
        source_id = str(ref.get("source_id", ""))
        if url and url in seen_urls:
            removed.append(source_id)
            continue
        if url:
            seen_urls.add(url)
        if source_id == "src_nist_ai_rmf":
            ref["relevance"] = "medium"
            ref["method_level_evidence"] = False
            ref["governance_support_only"] = True
            governance.append(source_id)
        else:
            ref["method_level_evidence"] = True
        deduped.append(ref)

    candidate["source_refs"] = deduped
    quality = candidate.setdefault("source_quality", {})
    quality["primary_source_count"] = len(
        [
            ref
            for ref in deduped
            if ref.get("reliability") == "high" and ref.get("method_level_evidence") is True
        ]
    )
    quality["governance_source_count"] = len(governance)
    quality["supporting_source_count"] = max(len(deduped) - int(quality["primary_source_count"]), 0)
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score", 0) or 0), 88)
    limitations = quality.setdefault("limitations", [])
    for note in [
        "三审要求 formal draft 去重 canonical source；相同 scikit-learn calibration URL 不重复计入 primary_source_count。",
        "NIST AI RMF 仅作为 governance source，不作为 method-level calibration evidence。",
    ]:
        if isinstance(limitations, list) and note not in limitations:
            limitations.append(note)
    return {"removed_duplicate_source_ids": removed, "governance_source_ids": governance}


def block_default(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    candidate["reviewed_allowed"] = False
    candidate["approved_allowed"] = False
    candidate["default_guidance_allowed"] = False
    candidate["hard_gate_allowed"] = False
    candidate["draft_conversion_allowed"] = True


def update_candidate(candidate: dict[str, Any], source_patch: dict[str, Any]) -> None:
    if candidate.get("research_task_id") != "P38-B10":
        raise ValueError(f"Unexpected candidate: {candidate.get('research_task_id')}")

    block_default(candidate)
    claim = candidate.setdefault("claim", {})
    claim["statement"] = "conformal / Bayesian calibration 只能作为不确定性增强层"
    claim["evidence_summary"] = FINAL_DRAFT_STATEMENT
    claim["interpretation_notes"] = (
        "formal draft 内部必须拆成 Conformal uncertainty layer 与 Bayesian/probabilistic calibration layer；"
        "Bayesian confidence 不等于 trading truth，calibration_output 不等于 final_gate_decision。"
    )
    claim["claim_strength"] = "medium"
    candidate["formal_draft_title"] = FINAL_DRAFT_TITLE
    candidate["calibration_governance_fields"] = {
        "calibration_set_id": "required",
        "calibration_set_hash": "required",
        "calibration_holdout_policy": "independent_from_scorer_training",
        "calibration_method_family": [
            "probability",
            "conformal",
            "bayesian_classifier",
            "bayesian_regression_uncertainty",
        ],
        "calibration_target": [
            "probability",
            "coverage",
            "credible_interval",
            "review_uncertainty",
        ],
        "calibration_metric": [
            "Brier",
            "ECE",
            "reliability_curve",
            "coverage_error",
            "interval_coverage",
        ],
        "threshold_policy_version": "required",
        "final_gate_policy_version": "required",
    }
    candidate["formal_draft_assumptions_and_caveats"] = {
        "conformal": [
            "coverage guarantee depends on assumptions such as exchangeability or validated distributional conditions.",
            "under distribution shift or sparse calibration data, output must be caveat/review signal only.",
        ],
        "bayesian_probabilistic_uncertainty": [
            "requires representative calibration data.",
            "Bayesian uncertainty estimates may still be inaccurate under model misspecification or approximate inference.",
        ],
        "classifier_probability_calibration": [
            "must be evaluated on holdout or cross-validation predictions.",
            "calibration may improve probability reliability but does not imply trading profitability.",
        ],
    }
    candidate["formal_draft_forbidden_outputs"] = [
        "allow",
        "block",
        "reduce_size",
        "open_position",
        "close_position",
        "hard_gate_decision",
    ]
    candidate["formal_draft_required_tests"] = [
        "calibration_independence_test",
        "final_gate_boundary_test",
        "bayesian_claim_scope_test",
        "sparse_slice_fallback_test",
        "source_dedup_test",
    ]

    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = (
        f"{ACCEPTED_REASON} 仅进入 formal draft 队列，不是 reviewed、approved、default guidance 或 hard gate。"
    )
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["formal_knowledge_id"] = candidate.get("conversion_target", {}).get("proposed_knowledge_id")
    workflow["formal_review_status"] = "draft"
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["next_action"] = "apply_ai_audit_patch"

    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_third_reaudit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = [
        "formal draft 内部是否拆成 conformal 和 Bayesian/probabilistic 两个小节。",
        "formal draft 是否需要将 Bayesian calibration 另拆候选；三审建议暂可保留合并 claim。",
    ]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "notes": ACCEPTED_REASON,
        "source_patch_notes": [
            "去重 scikit-learn calibration canonical source。",
            "NIST AI RMF 保留为 governance source，不计为 method-level calibration evidence。",
        ],
        "content_patch_notes": [
            "formal draft 标题建议：Conformal / Bayesian Calibration as an Uncertainty Enhancement Layer。",
            "formal draft 内部拆成 conformal uncertainty layer 和 Bayesian/probabilistic calibration layer。",
        ],
        "boundary_patch_notes": [
            "calibration_output != final_gate_decision",
            "uncertainty_score != trade_allow",
            "Bayesian confidence != trading truth",
            "conformal set != execution permission",
        ],
        "required_tests": candidate["formal_draft_required_tests"],
        "source_patch": source_patch,
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "b10_third_reaudit_accepted_for_draft",
                "reason": ACCEPTED_REASON,
            }
        )


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    source_patch = canonicalize_sources(candidate)
    update_candidate(candidate, source_patch)
    write_json(CANDIDATE_PATH, candidate)

    decision = {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "reason": ACCEPTED_REASON,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "source_patch": source_patch,
    }
    audit_result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_third_reaudit_imported_by_codex",
        "overall_decision": "accepted_for_formal_draft_queue",
        "decision_summary": {
            "accepted_for_draft": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "direct_reviewed_allowed": 0,
            "direct_approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "decisions": [decision],
    }
    write_json(AUDIT_PATH, audit_result)

    report = {
        "report_id": "phase38_b10_bayesian_calibration_third_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_path": rel(AUDIT_PATH),
        "candidate_path": rel(CANDIDATE_PATH),
        "decision_summary": audit_result["decision_summary"],
        "source_patch": source_patch,
        "formal_reviewed_created": False,
        "approved_created": False,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "next_task": "B10 可在后续单独治理任务中转换 formal reviewed，但不得自动 approved。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
