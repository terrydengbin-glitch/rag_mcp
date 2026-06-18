"""Apply Phase 60 P1 candidate strict audit result.

This moves six P1 candidates to accepted_for_draft only. It does not create
formal reviewed knowledge, approved guidance, default guidance, or hard gates.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-584"
AUDIT_RESULT_ID = "audit_result_phase60_p1_candidate_20260617_strict_v1"
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain JSON object")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_paths() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for partition in ("KB_05_REPLAY_SIMULATION", "KB_06_LIVE_EXECUTION", "KB_07_RISK_MANAGEMENT"):
        base = repo_path("codex-expert-kit", "rag", "candidates", partition)
        for path in base.glob("cand_20260617_phase60_p1_*.json"):
            item = read_json(path)
            cid = str(item.get("candidate_id", ""))
            if cid:
                result[cid] = path
    return result


def merge_list(existing: Any, additions: list[str]) -> list[str]:
    out: list[str] = []
    if isinstance(existing, list):
        out.extend(str(item) for item in existing)
    for item in additions:
        if item not in out:
            out.append(item)
    return out


def apply_result(candidate: dict[str, Any], audit_item: dict[str, Any], global_patch: list[str]) -> dict[str, Any]:
    candidate.setdefault("status", {})
    candidate["status"].update(
        {
            "review_status": "accepted_for_draft",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Phase 60 P1 strict audit accepted this candidate for draft only; reviewed/approved/default/hard gate are not allowed.",
            "updated_at": TODAY,
        }
    )

    candidate.setdefault("workflow", {})
    candidate["workflow"].update(
        {
            "stage": "accepted_for_draft",
            "queue_group": "ai_passed",
            "hidden_from_default_queue": True,
            "next_action": "export_reviewed_preparation_audit_package",
            "formal_knowledge_id": None,
            "formal_review_status": None,
        }
    )

    candidate.setdefault("review", {})
    candidate["review"].update(
        {
            "review_status": "accepted_for_draft",
            "reviewed_by": "external_ai_strict_audit",
            "reviewed_at": TODAY,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "notes": "Accepted for draft only. Requires reviewed-preparation audit before formal reviewed/caveat_only.",
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": "phase60_p1_candidate_audit_package_20260617",
                "decision": audit_item["decision"],
                "confidence": audit_item.get("confidence"),
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_followups": audit_item.get("required_followups", []),
                "patch_notes": audit_item.get("patch_notes", {}),
                "global_required_patch": global_patch,
            },
        }
    )

    candidate.setdefault("conflict_audit", {})
    candidate["conflict_audit"].update(
        {
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "resolution_summary": "Phase 60 P1 candidate audit accepted this item for draft only; reviewed/approved/default guidance/hard gate remain forbidden.",
        }
    )

    candidate.setdefault("machine_gate", {})
    candidate["machine_gate"].update(
        {
            "default_guidance": "deny",
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "requires_human_escalation": True,
            "reason": "accepted_for_draft only; reviewed-preparation audit required before formal reviewed/caveat_only.",
        }
    )

    candidate.setdefault("conversion_target", {})
    candidate["conversion_target"].update(
        {
            "target_review_status": "accepted_for_draft_pending_reviewed_preparation",
            "default_guidance_target": "deny",
            "hard_gate_target": "deny",
        }
    )

    candidate.setdefault("content", {})
    required_fields = candidate["content"].get("required_fields_or_contract", [])
    candidate["content"]["required_fields_or_contract"] = merge_list(required_fields, audit_item.get("field_patches", []))
    risk_notes = candidate["content"].get("risk_notes", [])
    candidate["content"]["risk_notes"] = merge_list(
        risk_notes,
        [
            "Phase 60 P1 只能作为增强治理证据，不替代 P0 EnvironmentManifest / PromotionDecision / GapReport。",
            "certification、scenario、paper reset、health、canary、drift 结果不得解释为 live-ready、收益证明、交易许可或 hard gate。",
        ],
    )

    candidate.setdefault("audit_log", []).append(
        {
            "event": "strict_ai_audit_imported",
            "at": TODAY,
            "by": "codex",
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": audit_item["decision"],
            "notes": "Candidate moved to accepted_for_draft only; no formal reviewed knowledge created.",
        }
    )
    return candidate


def validate(candidates: list[dict[str, Any]], paths: list[Path]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    for candidate, path in zip(candidates, paths, strict=True):
        cid = str(candidate.get("candidate_id", ""))
        if candidate.get("status", {}).get("review_status") != "accepted_for_draft":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "not_accepted_for_draft"})
        if candidate.get("workflow", {}).get("queue_group") != "ai_passed":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "not_ai_passed"})
        if candidate.get("conflict_audit", {}).get("approval_allowed") is not False:
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "approval_allowed_not_false"})
        gate = candidate.get("machine_gate", {})
        for field in ("reviewed_allowed", "approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append({"candidate_id": cid, "path": rel(path), "reason": f"{field}_not_false"})
    return failures


def main() -> int:
    audit = read_json(AUDIT_PATH)
    path_by_id = candidate_paths()
    updated: list[dict[str, Any]] = []
    paths: list[Path] = []
    missing: list[str] = []
    global_patch = [str(item) for item in audit.get("global_required_patch", [])]

    for item in audit.get("candidate_results", []):
        cid = str(item["candidate_id"])
        path = path_by_id.get(cid)
        if path is None:
            missing.append(cid)
            continue
        candidate = read_json(path)
        updated_candidate = apply_result(candidate, item, global_patch)
        write_json(path, updated_candidate)
        updated.append(updated_candidate)
        paths.append(path)

    failures = validate(updated, paths)
    for cid in missing:
        failures.append({"candidate_id": cid, "path": "", "reason": "candidate_file_missing"})

    report = {
        "report_id": "phase60_p1_candidate_audit_import_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "candidate_count": len(updated),
        "accepted_for_draft_count": sum(1 for item in updated if item.get("status", {}).get("review_status") == "accepted_for_draft"),
        "failure_count": len(failures),
        "failures": failures,
        "updated_paths": [rel(path) for path in paths],
        "next_action": "Export Phase 60 P1 reviewed/caveat_only preparation audit package.",
        "gate_status": "pass" if not failures else "fail",
    }
    report_path = repo_path("docs", "reports", "phase60_p1_candidate_audit_import_report.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
