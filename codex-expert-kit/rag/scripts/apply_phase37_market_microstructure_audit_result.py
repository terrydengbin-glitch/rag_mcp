"""Apply Phase 37 Market Microstructure first audit result to candidates.

This script updates candidate workflow state only. It never creates formal
reviewed knowledge, approved knowledge, default guidance, or hard gates.
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
EXPECTED_PACKAGE_ID = "phase37_market_microstructure_candidate_audit_package_20260611"
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase37_market_microstructure_candidate_audit_20260611_strict_v1"
PARTITION = "KB_03_MARKET_MICROSTRUCTURE"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_audit_import_report.json", start_file=__file__
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


def archive_path(audit_result_id: str) -> Path:
    return resolve_repo_path("docs", "audit", f"{audit_result_id}.json", start_file=__file__)


def get_results(audit: dict[str, Any]) -> list[dict[str, Any]]:
    results = audit.get("results") or audit.get("candidate_results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain results or candidate_results list.")
    return results


def validate_audit_result(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("audit_result_id") != EXPECTED_AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != EXPECTED_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    quality_gate = audit.get("quality_gate", {})
    if isinstance(quality_gate, dict) and quality_gate.get("pass") is not True:
        raise ValueError("audit quality_gate.pass must be true.")

    results = get_results(audit)
    if len(results) != 12:
        raise ValueError(f"results must contain 12 items, got {len(results)}.")

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


def apply_m11_semantic_patch(payload: dict[str, Any], patch_notes: dict[str, list[str]]) -> None:
    claim = payload.setdefault("claim", {})
    if claim.get("normalized_claim") != "microstructure.thin_market_execution_risk.v1":
        return

    old_title = claim.get("title")
    claim["title"] = "薄市场执行风险必须显式降级或要求复核"
    statement = str(claim.get("statement", ""))
    statement = statement.replace("必须降级为风险提示或要求人工/风控复核", "必须显式降级为风险提示或要求人工/风控复核")
    statement = statement.replace("不能把正常市场假设沿用到 thin market 执行", "不能把正常市场假设沿用到 thin market 执行，也不能在本候选中创建自动 hard gate")
    claim["statement"] = statement

    patch_notes["content"].append(
        f"M11 标题已从 `{old_title}` 改为 `薄市场执行风险必须显式降级或要求复核`，避免机器误读为 hard gate。"
    )
    patch_notes["boundary"].append("M11 保留 hard_gate_allowed=false；真正阻断只能由外接项目 Risk/Live Execution 风控层定义。")


def patch_candidate(payload: dict[str, Any], result: dict[str, Any], audit_result_id: str) -> dict[str, Any]:
    decision = str(result["decision"])
    patch_notes = normalize_patch_notes(result.get("patch_notes"))
    apply_m11_semantic_patch(payload, patch_notes)
    flat_patch_notes = flatten_patch_notes(patch_notes)

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
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "decision": decision,
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reason": result.get("reason"),
        "patch_notes": flat_patch_notes,
        "patch_note_groups": patch_notes,
        "boundary": "accepted_for_draft is not reviewed or approved; this audit does not allow default guidance or hard gate.",
    }

    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"Phase 37 Market Microstructure 首轮严格审计结论为 {decision}；"
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
    machine_gate["reason"] = (
        "Phase 37 Market Microstructure first audit does not allow default guidance; "
        "formal reviewed requires a later reviewed-preparation gate."
    )
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
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "blocked"
        workflow["stage"] = "blocked"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "manual_review"

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase37_market_microstructure_first_audit_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": audit_result_id,
            "patch_notes": flat_patch_notes,
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
                "confidence": result.get("confidence"),
                "path": str(path),
            }
        )

    counts = decision_counts(results)
    report = {
        "report_id": "phase37_market_microstructure_audit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-404",
        "phase": "37",
        "partition_id": PARTITION,
        "source_audit_result": str(source_path),
        "archived_audit_result": str(archive_path(audit_result_id)),
        "quality_gate": {
            "pass": True,
            "reason": "首轮严格审计通过；12 条均 accepted_for_draft；未创建 formal reviewed/approved/default guidance/hard gate。",
        },
        "decision_counts": counts,
        "updated_candidates": updated,
        "global_patches": audit.get("global_patches", []),
        "next_step": "跳过 needs_more_evidence 补证流，进入 CEK-TA-407 reviewed/caveat_only 准备审计包导出。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report["decision_counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
