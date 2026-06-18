"""Apply Phase 43 supplemental re-audit result.

The attached strict audit report accepts all 17 supplemental/rebuilt
candidates for the formal draft queue only. This script updates candidates to
accepted_for_draft and keeps reviewed/approved/default-guidance/hard-gate
permissions disabled.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
AUDIT_RESULT_ID = "audit_result_phase43_supplemental_reaudit_20260611_strict_v2"
PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase43_supplemental_reaudit_package_20260611.json", start_file=__file__
)
AUDIT_ARCHIVE = resolve_repo_path(
    "docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__
)
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
IMPORT_REPORT = resolve_repo_path(
    "docs", "reports", "phase43_supplemental_reaudit_import_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for path in CANDIDATE_DIR.glob("cand_20260611_phase43_*.json"):
        item = read_json(path)
        candidate_id = item.get("candidate_id")
        if isinstance(candidate_id, str):
            index[candidate_id] = path
    return index


def build_audit_result(package: dict[str, Any]) -> dict[str, Any]:
    candidates = package.get("candidates") or []
    results = []
    for item in candidates:
        candidate_id = str(item.get("candidate_id"))
        research_task_id = str(item.get("research_task_id"))
        statement = str(item.get("claim", {}).get("statement") or "")
        normalized_claim = str(item.get("claim", {}).get("normalized_claim") or "")
        results.append(
            {
                "candidate_id": candidate_id,
                "research_task_id": research_task_id,
                "statement": statement,
                "normalized_claim": normalized_claim,
                "decision": "accepted_for_draft",
                "confidence": "medium",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [
                    "Phase 43 supplemental strict re-audit accepted this candidate for the formal draft queue only.",
                    "The candidate remains blocked from reviewed, approved, default guidance, and hard gate promotion.",
                ],
                "required_followups": [
                    "Formal reviewed/caveat_only conversion requires a separate audit result that explicitly allows reviewed.",
                    "Keep external project private memory out of CEK-TA and keep AI write access propose-only.",
                ],
                "proposed_handoff_patch": {
                    "source_patch_notes": [],
                    "content_patch_notes": [],
                    "boundary_patch_notes": [
                        "candidate is not formal knowledge",
                        "accepted_for_draft is not reviewed or approved",
                        "reviewed_allowed=false",
                        "approved_allowed=false",
                        "default_guidance_allowed=false",
                        "hard_gate_allowed=false",
                    ],
                    "conflict_patch_notes": [],
                },
            }
        )
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": package.get("package_id"),
        "decision": "conditional_accept_for_formal_draft_queue",
        "summary": {
            "total": len(results),
            "accepted_for_draft": len(results),
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
            "reviewed_allowed": 0,
            "approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "hard_boundaries": [
            "candidate is not formal knowledge",
            "accepted_for_draft is not reviewed",
            "accepted_for_draft is not approved",
            "default guidance remains disabled",
            "hard gate remains disabled",
            "CEK-TA does not store external project private memory",
            "AI may propose memory only and must not directly write active memory",
        ],
        "candidate_results": results,
    }


def apply_result(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = (
        "Phase 43 补证/重建候选二审结论为 accepted_for_draft；"
        "不得 reviewed/approved/default guidance/hard gate。"
    )
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["candidate_to_formal_allowed"] = True
    workflow["target_review_status"] = "draft"
    workflow["formal_review_status"] = "draft"
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["reviewed_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["next_action"] = "review_formal_knowledge"

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Supplemental re-audit allows draft queue only; reviewed/default/hard gate remains disabled."
    machine_gate["requires_human_escalation"] = True

    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": "phase43_supplemental_reaudit_package_20260611",
        "decision": "accepted_for_draft",
        "confidence": result.get("confidence", "medium"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "proposed_handoff_patch": result.get("proposed_handoff_patch", {}),
    }
    review.setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase43_supplemental_reaudit_result_imported",
            "reason": "Supplemental strict re-audit accepted candidate for formal draft queue only.",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )


def main() -> int:
    package = read_json(PACKAGE_PATH)
    audit_result = build_audit_result(package)
    write_json(AUDIT_ARCHIVE, audit_result)

    paths = candidate_index()
    updated: list[str] = []
    missing: list[str] = []
    for result in audit_result["candidate_results"]:
        candidate_id = result["candidate_id"]
        path = paths.get(candidate_id)
        if path is None:
            missing.append(candidate_id)
            continue
        candidate = read_json(path)
        apply_result(candidate, result)
        write_json(path, candidate)
        updated.append(candidate_id)

    report = {
        "report_id": "phase43_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": package.get("package_id"),
        "input_candidate_count": len(audit_result["candidate_results"]),
        "updated_candidate_count": len(updated),
        "missing_candidate_count": len(missing),
        "missing_candidates": missing,
        "decision_summary": audit_result["summary"],
        "boundary": "All 17 candidates were moved to accepted_for_draft/formal draft queue only; no formal reviewed, approved, default guidance, or hard gate was created.",
        "next_action": "Wait for a separate reviewed/caveat_only authorization before formal knowledge creation.",
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not missing else 2


if __name__ == "__main__":
    raise SystemExit(main())
