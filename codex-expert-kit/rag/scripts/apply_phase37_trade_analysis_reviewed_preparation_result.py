"""Apply Phase 37 Trade Analysis reviewed-preparation audit result.

The reviewed-preparation audit rejected formal reviewed conversion for all
12 Trade Analysis candidates because the package did not include inline CEK-TA
schema contracts. This script archives that audit result and moves the
candidates back to the ``needs_more_evidence`` queue without creating formal
knowledge, approved guidance, default guidance, hard gates, or risk-threshold
advice.
"""

from __future__ import annotations

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


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-446"
AUDIT_RESULT_ID = "audit_result_phase37_trade_analysis_reviewed_preparation_20260612_strict_v1"
SOURCE_PACKAGE_ID = "phase37_trade_analysis_reviewed_preparation_audit_package_20260612"
PARTITION_ID = "KB_07_TRADE_ANALYSIS"
EXPECTED_TOTAL = 12

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_trade_analysis_reviewed_preparation_import_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_root() -> Path:
    return resolve_repo_path(start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(repo_root()).as_posix()


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [item.strip() for item in as_list(value) if isinstance(item, str) and item.strip()]


def dedupe_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = value.strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def patch_groups(result: dict[str, Any]) -> dict[str, list[str]]:
    raw = result.get("patch_notes")
    groups = {"source": [], "content": [], "boundary": [], "conflict": []}
    if isinstance(raw, dict):
        for key in groups:
            groups[key] = string_list(raw.get(key))
    elif isinstance(raw, list):
        groups["content"] = string_list(raw)
    return groups


def archive_audit_result(source_path: Path) -> dict[str, Any]:
    payload = read_json(source_path)
    if payload.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {payload.get('audit_result_id')}")
    if payload.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {payload.get('package_id')}")
    AUDIT_RESULT_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != AUDIT_RESULT_ARCHIVE_PATH.resolve():
        shutil.copyfile(source_path, AUDIT_RESULT_ARCHIVE_PATH)
    else:
        write_json(AUDIT_RESULT_ARCHIVE_PATH, payload)
    return payload


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260612_phase37_trade_analysis_*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            candidates[task_id] = (path, candidate)
    return candidates


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    results = audit.get("candidate_results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain candidate_results list.")
    if len(results) != EXPECTED_TOTAL:
        raise ValueError(f"expected {EXPECTED_TOTAL} results, got {len(results)}")
    counts = Counter(str(item.get("decision")) for item in results if isinstance(item, dict))
    if counts.get("needs_more_evidence", 0) != EXPECTED_TOTAL:
        raise ValueError(f"expected all results to be needs_more_evidence, got {dict(counts)}")
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("candidate_results must contain objects.")
        cid = result.get("candidate_id")
        if result.get("reviewed_allowed") is not False:
            raise ValueError(f"{cid}: reviewed_allowed must be false.")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if result.get(field) is not False:
                raise ValueError(f"{cid}: {field} must be false.")
    return results


def update_candidate(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    patches = patch_groups(result)
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = "reviewed-preparation 审计未通过：缺 CEK-TA Trade Analysis 内部契约/schema 正文或 schema_extract。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "reviewed_preparation_needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formalization_allowed": False,
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "supplement_trade_analysis_contract_schema_then_reaudit",
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }
    )

    conversion = candidate.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        blockers = as_list(conversion.get("formalization_blockers"))
        blockers.append("requires_trade_analysis_contract_schema_inline_evidence")
        conversion.update(
            {
                "target_review_status": "blocked_until_supplemented",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "formalization_blockers": dedupe_strings(blockers),
            }
        )

    review = candidate.setdefault("review", {})
    review["reviewed_preparation_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": patches,
        "schema_contract_assessment": result.get("schema_contract_assessment", {}),
    }
    review["open_questions"] = dedupe_strings(
        as_list(review.get("open_questions"))
        + as_list(result.get("required_followups"))
        + patches["source"]
        + patches["content"]
        + patches["boundary"]
        + patches["conflict"]
    )
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_trade_analysis_reviewed_preparation_needs_more_evidence",
                "reason": status["decision_reason"],
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate.update(
        {
            "default_guidance": "deny",
            "reason": "reviewed-preparation 审计未通过；补 Trade Analysis 内部契约/schema 前不得 formal reviewed、approved、default guidance、hard gate 或风险阈值建议。",
            "requires_human_escalation": True,
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }
    )


def main() -> int:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit = archive_audit_result(source_path)
    results = validate_audit(audit)
    candidates = load_candidates()

    updated: list[dict[str, Any]] = []
    failures: list[str] = []
    for result in sorted(results, key=lambda item: str(item.get("research_task_id", ""))):
        task_id = str(result.get("research_task_id", ""))
        entry = candidates.get(task_id)
        if not entry:
            failures.append(f"{task_id}: candidate not found")
            continue
        path, candidate = entry
        update_candidate(candidate, result)
        write_json(path, candidate)
        updated.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": task_id,
                "candidate_path": rel(path),
                "decision": "needs_more_evidence",
                "required_followups": result.get("required_followups", []),
            }
        )

    if failures:
        raise SystemExit(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))

    report = {
        "report_id": "phase37_trade_analysis_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "archive_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "source_quality_gate_pass": bool(audit.get("quality_gate", {}).get("pass", False)),
        "source_quality_gate_reason": audit.get("quality_gate", {}).get("reason"),
        "decision_counts": dict(Counter(str(item.get("decision")) for item in results)),
        "updated_count": len(updated),
        "needs_more_evidence_count": len(updated),
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "risk_threshold_advice_enabled": 0,
        "updated": updated,
        "boundary": "12 条 Trade Analysis 候选保持 draft 方向但不得 formal reviewed；补内部契约/schema 后再审。",
        "next_action": "CEK-TA-447: 补 Trade Analysis 内部契约/schema 并导出补证再审包。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
