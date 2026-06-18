"""Apply Phase 60 P1 reviewed/caveat_only preparation audit result.

This materializes exactly three accepted P1 candidates as formal
reviewed/caveat_only knowledge and keeps three candidates in needs_more_evidence.
It never creates approved knowledge, default guidance, hard gates, live
permission, trading advice, or risk-threshold advice.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-18"
TASK_ID = "CEK-TA-586"
AUDIT_RESULT_ID = "audit_result_phase60_p1_reviewed_preparation_20260618_strict_v1"
PACKAGE_ID = "phase60_p1_reviewed_preparation_audit_package_20260617"
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)


ACCEPTED_TARGETS: dict[str, dict[str, Any]] = {
    "P60-P1-01": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_p1_fix_broker_certification_required_001.json"),
        "knowledge_id": "kb_phase60_live_execution.adapter_certification.fix_broker_certification_required.v1",
        "knowledge_path": ("KB_06_LIVE_EXECUTION", "kb_phase60_live_execution.adapter_certification.fix_broker_certification_required.v1.json"),
    },
    "P60-P1-03": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_p1_paper_account_reset_trace_required_001.json"),
        "knowledge_id": "kb_phase60_live_execution.paper_account_state.reset_trace_required.v1",
        "knowledge_path": ("KB_06_LIVE_EXECUTION", "kb_phase60_live_execution.paper_account_state.reset_trace_required.v1.json"),
        "alias_of": "kb_phase60_replay_simulation.paper_trading_not_live_required.v1",
    },
    "P60-P1-04": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_p1_realtime_sim_health_monitor_required_001.json"),
        "knowledge_id": "kb_phase60_live_execution.environment_health.monitor_required.v1",
        "knowledge_path": ("KB_06_LIVE_EXECUTION", "kb_phase60_live_execution.environment_health.monitor_required.v1.json"),
    },
}

NEEDS_MORE_EVIDENCE_TARGETS: dict[str, dict[str, Any]] = {
    "P60-P1-02": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_p1_replay_scenario_library_versioned_001.json"),
    },
    "P60-P1-05": {
        "candidate_path": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_p1_live_canary_rollback_owner_required_001.json"),
    },
    "P60-P1-06": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_p1_environment_drift_monitor_required_001.json"),
    },
}


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


def load_base_module() -> Any:
    path = Path(__file__).with_name("apply_phase60_reviewed_preparation_result.py")
    spec = importlib.util.spec_from_file_location("phase60_apply_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.TODAY = TODAY
    module.TASK_ID = TASK_ID
    module.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    module.PACKAGE_ID = PACKAGE_ID
    return module


def audit_item_map() -> dict[str, dict[str, Any]]:
    audit = read_json(AUDIT_PATH)
    return {str(item["research_task_id"]): item for item in audit.get("candidate_results", [])}


def enrich_target(task_id: str, target: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(target)
    enriched["confidence"] = item.get("confidence", "medium")
    enriched["required_followups"] = item.get("required_followups", [])
    enriched["patch_notes"] = item.get("patch_notes", {})
    return enriched


def validate_report(created: list[str], needs_more: list[str]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    for path_text in created:
        item = read_json(repo_path(*path_text.split("/")))
        kid = str(item.get("knowledge_id", ""))
        gate = item.get("machine_gate", {})
        review = item.get("review", {})
        if review.get("review_status") != "reviewed":
            failures.append({"knowledge_id": kid, "path": path_text, "reason": "formal_not_reviewed"})
        if gate.get("default_guidance") != "caveat_only":
            failures.append({"knowledge_id": kid, "path": path_text, "reason": "default_guidance_not_caveat_only"})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append({"knowledge_id": kid, "path": path_text, "reason": f"{field}_not_false"})
    for path_text in needs_more:
        item = read_json(repo_path(*path_text.split("/")))
        cid = str(item.get("candidate_id", ""))
        if item.get("status", {}).get("review_status") != "needs_more_evidence":
            failures.append({"candidate_id": cid, "path": path_text, "reason": "candidate_not_needs_more_evidence"})
    return failures


def main() -> int:
    base = load_base_module()
    items = audit_item_map()
    created: list[str] = []
    formalized_candidates: list[str] = []
    needs_more_evidence: list[str] = []

    for task_id, base_target in ACCEPTED_TARGETS.items():
        item = items[task_id]
        if item.get("decision") != "accepted_for_reviewed_caveat_only":
            raise ValueError(f"{task_id} is not accepted_for_reviewed_caveat_only")
        target = enrich_target(task_id, base_target, item)
        cpath = base.candidate_path(target["candidate_path"])
        kpath = base.knowledge_path(target["knowledge_path"])
        candidate = read_json(cpath)
        formal = base.build_formal(candidate, target)
        write_json(kpath, formal)
        write_json(cpath, base.update_formalized_candidate(candidate, target))
        created.append(rel(kpath))
        formalized_candidates.append(rel(cpath))

    for task_id, base_target in NEEDS_MORE_EVIDENCE_TARGETS.items():
        item = items[task_id]
        if item.get("decision") != "needs_more_evidence":
            raise ValueError(f"{task_id} is not needs_more_evidence")
        target = enrich_target(task_id, base_target, item)
        cpath = base.candidate_path(target["candidate_path"])
        candidate = read_json(cpath)
        write_json(cpath, base.update_needs_more_evidence_candidate(candidate, task_id, target))
        needs_more_evidence.append(rel(cpath))

    failures = validate_report(created, needs_more_evidence)
    report = {
        "schema_version": "phase60_p1_reviewed_preparation_import_report.v1",
        "task_id": TASK_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": rel(AUDIT_PATH),
        "created_formal_knowledge_count": len(created),
        "created_formal_knowledge": created,
        "formalized_candidates": formalized_candidates,
        "needs_more_evidence_count": len(needs_more_evidence),
        "needs_more_evidence_candidates": needs_more_evidence,
        "failure_count": len(failures),
        "failures": failures,
        "boundary": {
            "review_status": "reviewed_for_accepted_items",
            "review_mode": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "task_completion_status": "partial_pending_supplemental_evidence",
        "next_action": "Rebuild index and fixtures, then supplement P60-P1-02/P1-05/P1-06 evidence.",
        "gate_status": "pass" if not failures else "fail",
    }
    report_path = repo_path("docs", "reports", "phase60_p1_reviewed_preparation_import_report.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
