"""Apply Phase 37 Data Engineering first audit result to candidates.

The audit result may move candidates to accepted_for_draft or
needs_more_evidence. This script never creates formal reviewed knowledge,
approved knowledge, default guidance, or hard gates.
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
EXPECTED_PACKAGE_ID = "phase37_data_engineering_candidate_audit_package_20260611"
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1"
SCHEMA_PATCHED_AUDIT_RESULT_ID = f"{EXPECTED_AUDIT_RESULT_ID}_schema_patched"
PARTITION = "KB_02_DATA_ENGINEERING"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_audit_import_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_input_path() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return resolve_repo_path("docs", "audit", f"{EXPECTED_AUDIT_RESULT_ID}.json", start_file=__file__)


def audit_archive_path(audit_result_id: str) -> Path:
    return resolve_repo_path("docs", "audit", f"{audit_result_id}.json", start_file=__file__)


def validate_audit_result(audit: dict[str, Any]) -> None:
    if audit.get("audit_result_id") not in {EXPECTED_AUDIT_RESULT_ID, SCHEMA_PATCHED_AUDIT_RESULT_ID}:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != EXPECTED_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    results = audit.get("candidate_results")
    if not isinstance(results, list) or len(results) != 12:
        raise ValueError("candidate_results must contain 12 items.")
    allowed_decisions = {"accepted_for_draft", "needs_more_evidence", "rejected", "blocked"}
    seen: set[str] = set()
    for result in results:
        if result.get("decision") not in allowed_decisions:
            raise ValueError(f"{result.get('candidate_id')}: invalid decision {result.get('decision')}")
        if result.get("confidence") not in {"low", "medium", "high"}:
            raise ValueError(f"{result.get('candidate_id')}: invalid confidence {result.get('confidence')}")
        if result.get("reviewed_allowed") is not False:
            raise ValueError(f"{result.get('candidate_id')}: reviewed_allowed must be false in first audit.")
        if result.get("approved_allowed") is not False:
            raise ValueError(f"{result.get('candidate_id')}: approved_allowed must be false.")
        if result.get("default_guidance_allowed") is not False:
            raise ValueError(f"{result.get('candidate_id')}: default_guidance_allowed must be false.")
        if result.get("hard_gate_allowed") is not False:
            raise ValueError(f"{result.get('candidate_id')}: hard_gate_allowed must be false.")
        candidate_id = str(result.get("candidate_id"))
        if candidate_id in seen:
            raise ValueError(f"duplicate candidate_id: {candidate_id}")
        seen.add(candidate_id)


def candidate_path(candidate_id: str) -> Path:
    return CANDIDATE_DIR / f"{candidate_id}.json"


def patch_candidate(payload: dict[str, Any], result: dict[str, Any], audit_result_id: str) -> dict[str, Any]:
    decision = str(result["decision"])
    status = payload.setdefault("status", {})
    workflow = payload.setdefault("workflow", {})
    review = payload.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log

    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": audit_result_id,
        "package_id": EXPECTED_PACKAGE_ID,
        "auditor": result.get("auditor", "external_ai_strict_audit"),
        "audited_at": TODAY,
        "decision": decision,
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": result.get("patch_notes", []),
        "source_assessment": result.get("source_assessment", {}),
        "classification_assessment": result.get("classification_assessment", {}),
        "boundary_assessment": result.get("boundary_assessment", {}),
        "boundary": "accepted_for_draft is not reviewed or approved; this audit does not allow default guidance or hard gate.",
    }

    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"Phase 37 Data Engineering 首轮严格审计结论为 {decision}；"
        "不允许 reviewed/approved/default guidance/hard gate。"
    )

    workflow["ai_audit_result_id"] = audit_result_id
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["formalization_allowed"] = False

    machine_gate = payload.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Phase 37 Data Engineering first audit does not allow default guidance; formal reviewed requires a later reviewed-preparation gate."
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True

    conversion = payload.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft" if decision == "accepted_for_draft" else "blocked"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    if decision == "accepted_for_draft":
        status["review_status"] = "accepted"
        status["ingestion_decision"] = "accepted_for_draft"
        workflow["stage"] = "ai_audited"
        workflow["queue_group"] = "ai_passed"
        workflow["next_action"] = "export_reviewed_preparation_audit_package"
    elif decision == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "supplement_sources_and_export_reaudit_package"
    elif decision == "rejected":
        status["review_status"] = "rejected"
        status["ingestion_decision"] = "rejected"
        workflow["stage"] = "rejected"
        workflow["queue_group"] = "rejected"
        workflow["next_action"] = "none"
    else:
        status["review_status"] = "blocked"
        status["ingestion_decision"] = "blocked"
        workflow["stage"] = "blocked"
        workflow["queue_group"] = "pending"
        workflow["next_action"] = "manual_review"

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase37_data_engineering_first_audit_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": audit_result_id,
            "patch_notes": result.get("patch_notes", []),
        }
    )
    return payload


def decision_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"total": len(results), "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0}
    for result in results:
        decision = str(result.get("decision"))
        if decision in counts:
            counts[decision] += 1
    return counts


def main() -> None:
    source_path = resolve_input_path()
    audit = read_json(source_path)
    validate_audit_result(audit)
    audit_result_id = str(audit["audit_result_id"])
    archive_path = audit_archive_path(audit_result_id)
    write_json(archive_path, audit)

    updated: list[dict[str, Any]] = []
    for result in audit["candidate_results"]:
        cid = str(result["candidate_id"])
        path = candidate_path(cid)
        if not path.exists():
            raise FileNotFoundError(path)
        payload = patch_candidate(read_json(path), result, audit_result_id)
        write_json(path, payload)
        updated.append(
            {
                "candidate_id": cid,
                "research_task_id": result.get("research_task_id"),
                "decision": result.get("decision"),
                "path": str(path),
                "patch_note_count": len(result.get("patch_notes", [])),
            }
        )

    counts = decision_counts(audit["candidate_results"])
    report = {
        "report_id": "phase37_data_engineering_audit_import_report",
        "generated_at": TODAY,
        "audit_result_id": audit_result_id,
        "original_audit_result_id": EXPECTED_AUDIT_RESULT_ID if audit_result_id == SCHEMA_PATCHED_AUDIT_RESULT_ID else None,
        "package_id": EXPECTED_PACKAGE_ID,
        "source_path": str(source_path),
        "archive_path": str(archive_path),
        "updated_count": len(updated),
        "decision_counts": counts,
        "updated": updated,
        "next_action": (
            "All 12 candidates are accepted_for_draft. Export a reviewed/caveat_only preparation audit package "
            "before creating any formal reviewed knowledge."
            if counts["needs_more_evidence"] == 0 and counts["rejected"] == 0 and counts["blocked"] == 0
            else "Supplement or manually review non-accepted candidates before reviewed preparation."
        ),
        "boundary": "No formal reviewed knowledge, approved knowledge, default guidance, or hard gate was created.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"updated_count": len(updated), "decision_counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
