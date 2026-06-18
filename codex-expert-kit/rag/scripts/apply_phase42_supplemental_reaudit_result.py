"""Apply Phase 42 supplemental re-audit result to candidate workflow only."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase42_needs_evidence_supplemental_reaudit_20260611_strict_v2"
EXPECTED_PACKAGE_ID = "phase42_needs_evidence_supplemental_reaudit_package_20260611"
LOCAL_AUDIT_PATH = resolve_repo_path(
    "docs",
    "audit",
    "audit_result_phase42_needs_evidence_supplemental_reaudit_20260611_strict_v2.json",
    start_file=__file__,
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase42_supplemental_reaudit_import_report.json", start_file=__file__
)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_audit_result(source: Path) -> Path:
    LOCAL_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if source.resolve() != LOCAL_AUDIT_PATH.resolve():
        shutil.copy2(source, LOCAL_AUDIT_PATH)
    return LOCAL_AUDIT_PATH


def candidate_index() -> dict[str, Path]:
    indexed: dict[str, Path] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase42_*.json")):
        payload = read_json(path)
        candidate_id = payload.get("candidate_id")
        if isinstance(candidate_id, str):
            indexed[candidate_id] = path
    return indexed


def append_unique(log: list[Any], entry: dict[str, Any], keys: tuple[str, ...]) -> None:
    for existing in log:
        if isinstance(existing, dict) and all(existing.get(key) == entry.get(key) for key in keys):
            return
    log.append(entry)


def ai_audit_payload(audit: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    patch = result.get("proposed_handoff_patch") or {}
    return {
        "audit_result_id": audit["audit_result_id"],
        "package_id": audit["package_id"],
        "auditor": audit.get("auditor"),
        "audited_at": audit.get("audited_at"),
        "decision": result.get("decision"),
        "confidence": result.get("confidence"),
        "reviewed_allowed": bool(result.get("reviewed_allowed")),
        "approved_allowed": bool(result.get("approved_allowed")),
        "default_guidance_allowed": bool(result.get("default_guidance_allowed")),
        "hard_gate_allowed": bool(result.get("hard_gate_allowed")),
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "source_audit": result.get("source_audit", {}),
        "conflict_audit": result.get("conflict_audit", {}),
        "scope_audit": result.get("scope_audit", {}),
        "classification_audit": result.get("classification_audit", {}),
        "source_patch_notes": patch.get("source_patch_notes", []),
        "content_patch_notes": patch.get("content_patch_notes", []),
        "boundary_patch_notes": patch.get("boundary_patch_notes", []),
        "conflict_patch_notes": patch.get("conflict_patch_notes", []),
        "boundary": "Accepted for formal draft queue only; not reviewed, approved, default guidance or hard gate.",
    }


def patch_candidate(candidate: dict[str, Any], audit: dict[str, Any], result: dict[str, Any]) -> str:
    decision = str(result.get("decision"))
    if decision != "accepted_for_draft":
        raise ValueError(f"Phase 42 supplemental import only supports accepted_for_draft, got {decision}")

    status = candidate.setdefault("status", {})
    review = candidate.setdefault("review", {})
    workflow = candidate.setdefault("workflow", {})
    conversion_target = candidate.setdefault("conversion_target", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log

    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["updated_at"] = TODAY
    status["decision_reason"] = (
        "Phase 42 二审结论为 accepted_for_draft；只允许进入 formal draft queue，"
        "不得视为 reviewed/approved/default guidance/hard gate。"
    )

    review["ai_audit"] = ai_audit_payload(audit, result)
    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    review["supplement_status"] = "accepted_for_draft_after_reaudit"

    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["ai_audit_result_id"] = audit["audit_result_id"]
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["next_action"] = "review_formal_knowledge"

    conversion_target["target_review_status"] = "draft"
    conversion_target["default_guidance_allowed"] = False
    conversion_target["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Accepted for draft queue only; reviewed/approved/default guidance requires later governance."
    machine_gate["requires_human_escalation"] = True

    append_unique(
        audit_log,
        {
            "at": TODAY,
            "actor": audit.get("auditor", "external_ai"),
            "action": "phase42_supplemental_reaudit_result_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": audit["audit_result_id"],
        },
        ("action", "audit_result_id"),
    )
    return decision


def run(audit_path: Path) -> dict[str, Any]:
    local_audit = copy_audit_result(audit_path)
    audit = read_json(local_audit)
    if audit.get("audit_result_id") != EXPECTED_AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != EXPECTED_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")

    indexed = candidate_index()
    updated: list[dict[str, str]] = []
    missing: list[str] = []
    decisions: dict[str, int] = {}

    for result in audit.get("candidate_results", []):
        if not isinstance(result, dict):
            continue
        candidate_id = str(result.get("candidate_id", ""))
        path = indexed.get(candidate_id)
        if path is None:
            missing.append(candidate_id)
            continue
        candidate = read_json(path)
        decision = patch_candidate(candidate, audit, result)
        write_json(path, candidate)
        decisions[decision] = decisions.get(decision, 0) + 1
        updated.append({"candidate_id": candidate_id, "decision": decision, "path": str(path)})

    report = {
        "report_id": "phase42_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_id": audit["audit_result_id"],
        "source_audit_result_path": str(local_audit),
        "package_id": audit["package_id"],
        "candidate_result_count": len(audit.get("candidate_results", [])),
        "updated_count": len(updated),
        "missing_count": len(missing),
        "decision_counts": decisions,
        "updated_candidates": updated,
        "missing_candidates": missing,
        "formal_knowledge_created": 0,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "This import moves candidates to formal draft queue only. No formal reviewed knowledge is created.",
        "next_action": "Prepare a separate formal reviewed/caveat_only conversion package for all 28 accepted Phase 42 candidates.",
        "gate_status": "pass" if not missing else "fail",
    }
    write_json(REPORT_PATH, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_result", help="Path to Phase 42 supplemental re-audit result JSON.")
    args = parser.parse_args()
    audit_path = Path(args.audit_result)
    if not audit_path.is_absolute():
        audit_path = resolve_repo_path(*audit_path.parts, start_file=__file__)
    report = run(audit_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
