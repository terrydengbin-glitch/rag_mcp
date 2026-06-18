"""Apply Phase 37 Backtest first audit result to candidates.

The first audit may only move candidates to ``accepted_for_draft``,
``needs_more_evidence``, ``rejected`` or ``blocked``. It never creates formal
reviewed knowledge, approved knowledge, default guidance, or hard gates.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
EXPECTED_PACKAGE_ID = "phase37_backtest_candidate_audit_package_20260611"
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase37_backtest_candidate_audit_20260611_strict_v1"
PARTITION = "KB_04_BACKTEST"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_backtest_audit_import_report.json", start_file=__file__)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_input_path() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()
    return resolve_repo_path("docs", "audit", f"{EXPECTED_AUDIT_RESULT_ID}.json", start_file=__file__)


def archive_path(audit_result_id: str) -> Path:
    return resolve_repo_path("docs", "audit", f"{audit_result_id}.json", start_file=__file__)


def get_results(audit: dict[str, Any]) -> list[dict[str, Any]]:
    results = audit.get("candidate_results") or audit.get("results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain candidate_results or results list.")
    return results


def validate_audit_result(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("audit_result_id") != EXPECTED_AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != EXPECTED_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    gate = audit.get("quality_gate", {})
    if isinstance(gate, dict) and gate.get("pass") is not True:
        raise ValueError("audit quality_gate.pass must be true.")

    results = get_results(audit)
    if len(results) != 12:
        raise ValueError(f"candidate_results must contain 12 items, got {len(results)}.")
    allowed_decisions = {"accepted_for_draft", "needs_more_evidence", "rejected", "blocked"}
    allowed_confidence = {"low", "medium", "medium_high", "high"}
    seen: set[str] = set()
    for result in results:
        cid = str(result.get("candidate_id"))
        if cid in seen:
            raise ValueError(f"duplicate candidate_id: {cid}")
        seen.add(cid)
        if result.get("decision") not in allowed_decisions:
            raise ValueError(f"{cid}: invalid decision {result.get('decision')}")
        if result.get("confidence") not in allowed_confidence:
            raise ValueError(f"{cid}: invalid confidence {result.get('confidence')}")
        if result.get("reviewed_allowed") is not False:
            raise ValueError(f"{cid}: reviewed_allowed must be false in first audit.")
        if result.get("approved_allowed") is not False:
            raise ValueError(f"{cid}: approved_allowed must be false.")
        if result.get("default_guidance_allowed") is not False:
            raise ValueError(f"{cid}: default_guidance_allowed must be false.")
        if result.get("hard_gate_allowed") is not False:
            raise ValueError(f"{cid}: hard_gate_allowed must be false.")
    return results


def candidate_path(candidate_id: str) -> Path:
    return CANDIDATE_DIR / f"{candidate_id}.json"


def normalize_patch_notes(value: Any) -> dict[str, list[str]]:
    notes = {"source": [], "content": [], "boundary": [], "conflict": []}
    if isinstance(value, dict):
        for key in notes:
            raw = value.get(key, [])
            if isinstance(raw, list):
                notes[key] = [str(item) for item in raw]
            elif raw:
                notes[key] = [str(raw)]
    elif isinstance(value, list):
        notes["content"] = [str(item) for item in value]
    elif value:
        notes["content"] = [str(value)]
    return notes


def flatten_patch_notes(groups: dict[str, list[str]]) -> list[str]:
    flattened: list[str] = []
    for group_name in ("source", "content", "boundary", "conflict"):
        for note in groups.get(group_name, []):
            flattened.append(f"{group_name}: {note}")
    return flattened


def apply_semantic_patch(payload: dict[str, Any], patch_notes: dict[str, list[str]]) -> None:
    normalized_claim = str(payload.get("claim", {}).get("normalized_claim", ""))
    if normalized_claim not in {"backtest.lookahead_bias_block.v1", "backtest.data_leakage_block.v1"}:
        return
    claim = payload.setdefault("claim", {})
    statement = str(claim.get("statement", ""))
    if "不得作为策略有效性证据" not in statement:
        statement = statement.rstrip("。") + "；本候选中的 block/阻断仅表示该回测证据失效，不表示可创建自动 hard gate。"
        claim["statement"] = statement
    patch_notes["content"].append("已把 block/阻断语义限定为 evidence invalidation：该回测不得作为策略有效性证据。")
    patch_notes["boundary"].append("保留 hard_gate_allowed=false；真正 hard gate 只能由后续 Risk/Live Execution 治理任务定义。")


def patch_candidate(payload: dict[str, Any], result: dict[str, Any], audit_result_id: str) -> dict[str, Any]:
    decision = str(result["decision"])
    patch_notes = normalize_patch_notes(result.get("patch_notes"))
    apply_semantic_patch(payload, patch_notes)
    flat_patch_notes = flatten_patch_notes(patch_notes)

    status = payload.setdefault("status", {})
    workflow = payload.setdefault("workflow", {})
    review = payload.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log = [
        item
        for item in audit_log
        if not (isinstance(item, dict) and item.get("audit_result_id") == audit_result_id)
    ]
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
        "patch_notes": flat_patch_notes,
        "patch_note_groups": patch_notes,
        "source_assessment": result.get("source_assessment", {}),
        "classification_assessment": result.get("classification_assessment", {}),
        "boundary_assessment": result.get("boundary_assessment", {}),
        "boundary": "accepted_for_draft is not reviewed or approved; this audit does not allow default guidance or hard gate.",
    }

    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"Phase 37 Backtest 首轮严格审计结论为 {decision}；"
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
    machine_gate["reason"] = "Phase 37 Backtest first audit does not allow default guidance; formal reviewed requires a later reviewed-preparation gate."
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False

    conversion = workflow.setdefault("conversion_target", {})
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
            "action": "phase37_backtest_first_audit_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": audit_result_id,
            "patch_notes": flat_patch_notes,
        }
    )
    return payload


def decision_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(str(result.get("decision")) for result in results)
    return {
        "total": len(results),
        "accepted_for_draft": counter.get("accepted_for_draft", 0),
        "needs_more_evidence": counter.get("needs_more_evidence", 0),
        "rejected": counter.get("rejected", 0),
        "blocked": counter.get("blocked", 0),
    }


def main() -> None:
    source_path = resolve_input_path()
    audit = read_json(source_path)
    results = validate_audit_result(audit)
    audit_result_id = str(audit["audit_result_id"])
    write_json(archive_path(audit_result_id), audit)

    updated: list[dict[str, Any]] = []
    for result in results:
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
            }
        )

    report = {
        "report_id": "phase37_backtest_audit_import_report",
        "generated_at": TODAY,
        "audit_result_id": audit_result_id,
        "source_path": str(source_path),
        "archive_path": str(archive_path(audit_result_id)),
        "partition_id": PARTITION,
        "decision_counts": decision_counts(results),
        "updated_candidates": updated,
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "next_step": "如果 needs_more_evidence 为 0，则跳过补证链路，导出 reviewed/caveat_only 准备审计包。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report["decision_counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
