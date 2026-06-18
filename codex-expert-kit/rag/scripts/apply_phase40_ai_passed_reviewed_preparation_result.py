"""Apply Phase 40 reviewed-preparation audit result.

This imports the CEK-TA-316 audit result for Phase 40 ai_passed candidates.
Candidates with reviewed_allowed=true are written as formal reviewed knowledge
with caveat_only machine gates. Candidates that still need evidence are moved
back to the needs_more_evidence queue. Nothing is approved, default-guidance
enabled, or hard-gate enabled by this script.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
CORE_DIR = Path(__file__).resolve().parents[2] / "core"
for path in (SCRIPT_DIR, CORE_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from path_resolver import resolve_repo_path  # noqa: E402
import apply_phase40_supplemental_reaudit_result as base  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-316"
AUDIT_RESULT_ID = "audit_result_phase40_ai_passed_reviewed_preparation_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase40_ai_passed_reviewed_preparation_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_ai_passed_reviewed_preparation_import_report.json", start_file=__file__
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


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dedupe(values: list[Any]) -> list[str]:
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


def decision_patch(decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "reason": str(decision.get("reason", "")),
        "required_followups": dedupe(
            as_list(decision.get("content_patch_notes"))
            + as_list(decision.get("boundary_patch_notes"))
            + as_list(decision.get("required_followups"))
        ),
    }


def load_candidates_by_id() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase40_*.json")):
        candidate = read_json(path)
        candidate_id = candidate.get("candidate_id")
        if isinstance(candidate_id, str):
            candidates[candidate_id] = (path, candidate)
    return candidates


def validate_audit_result(audit_result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if audit_result.get("audit_result_id") != AUDIT_RESULT_ID:
        errors.append(f"audit_result_id mismatch: {audit_result.get('audit_result_id')}")
    if audit_result.get("source_package_id") != SOURCE_PACKAGE_ID:
        errors.append(f"source_package_id mismatch: {audit_result.get('source_package_id')}")
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list):
        errors.append("decisions must be a list")
        return errors
    if len(decisions) != 23:
        errors.append(f"expected 23 decisions, got {len(decisions)}")
    for decision in decisions:
        if not isinstance(decision, dict):
            errors.append("decision entry must be object")
            continue
        if decision.get("approved_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: approved_allowed must be false")
        if decision.get("default_guidance_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: default_guidance_allowed must be false")
        if decision.get("hard_gate_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: hard_gate_allowed must be false")
        if decision.get("decision") == "accepted_for_draft" and decision.get("reviewed_allowed") is not True:
            errors.append(f"{decision.get('candidate_id')}: accepted_for_draft must have reviewed_allowed=true")
        if decision.get("decision") == "needs_more_evidence" and decision.get("reviewed_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: needs_more_evidence must have reviewed_allowed=false")
    return errors


def validate_accepted_candidate(candidate: dict[str, Any], decision: dict[str, Any]) -> str | None:
    candidate_id = str(candidate.get("candidate_id", ""))
    if not str(candidate.get("research_task_id", "")).startswith("P40-"):
        return "not_phase40"
    if candidate_id != decision.get("candidate_id"):
        return "candidate_id_mismatch"
    if base.deep_get(candidate, ("workflow", "queue_group")) not in {"ai_passed", "formalized"}:
        return "not_ai_passed_or_formalized_queue"
    if base.deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "not_accepted_for_draft"
    if not base.deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_knowledge_id"
    if not str(base.deep_get(candidate, ("classification", "canonical_node_id"), "")).startswith(
        "kt.ai_feedback_governance."
    ):
        return "wrong_node"
    if not as_list(candidate.get("source_refs")):
        return "missing_sources"
    if base.deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if base.deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    return None


def apply_full_audit_notes(item: dict[str, Any], decision: dict[str, Any]) -> None:
    audit = item.setdefault("review", {}).setdefault("ai_audit", {})
    audit.update(
        {
            "audit_result_id": AUDIT_RESULT_ID,
            "source_package_id": SOURCE_PACKAGE_ID,
            "decision": decision.get("decision"),
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "allowed_next_stage": "formal_reviewed_knowledge",
            "reason": decision.get("reason", ""),
            "source_patch_notes": as_list(decision.get("source_patch_notes")),
            "content_patch_notes": as_list(decision.get("content_patch_notes")),
            "boundary_patch_notes": as_list(decision.get("boundary_patch_notes")),
            "conflict_patch_notes": as_list(decision.get("conflict_patch_notes")),
            "required_followups": as_list(decision.get("required_followups")),
        }
    )
    item.setdefault("phase40_conversion", {})["reviewed_allowed"] = True
    item.setdefault("phase40_conversion", {})["approved_allowed"] = False


def mark_needs_more_evidence(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = str(decision.get("reason", "二审仍要求补充证据。"))
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_review_status": "blocked",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
            "next_action": "supplement_evidence_then_reaudit",
            "default_guidance_allowed": False,
        }
    )

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "二审仍为 needs_more_evidence；不能生成 formal reviewed 或默认指导。"
    machine_gate["requires_human_escalation"] = True

    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["open_questions"] = dedupe(
        as_list(review.get("open_questions"))
        + as_list(decision.get("source_patch_notes"))
        + as_list(decision.get("content_patch_notes"))
        + as_list(decision.get("boundary_patch_notes"))
        + as_list(decision.get("required_followups"))
    )
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": decision.get("candidate_id"),
        "research_task_id": decision.get("research_task_id"),
        "decision": "needs_more_evidence",
        "reason": decision.get("reason", ""),
        "source_patch_notes": as_list(decision.get("source_patch_notes")),
        "content_patch_notes": as_list(decision.get("content_patch_notes")),
        "boundary_patch_notes": as_list(decision.get("boundary_patch_notes")),
        "conflict_patch_notes": as_list(decision.get("conflict_patch_notes")),
        "required_followups": as_list(decision.get("required_followups")),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase40_reviewed_preparation_needs_more_evidence",
                "reason": f"{TASK_ID}: 二审仍需补证，保持 candidate，不生成 formal reviewed。",
            }
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply Phase 40 reviewed-preparation audit result.")
    parser.add_argument(
        "--input",
        type=Path,
        default=AUDIT_RESULT_PATH,
        help="Path to external audit result JSON. Defaults to docs/audit copy.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input
    if not input_path.exists():
        raise FileNotFoundError(input_path)

    audit_result = read_json(input_path)
    errors = validate_audit_result(audit_result)
    if errors:
        raise ValueError("Invalid audit result: " + "; ".join(errors))

    write_json(AUDIT_RESULT_PATH, audit_result)

    base.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    base.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID
    base.AUDIT_TASK_ID = TASK_ID
    base.REPORT_PATH = REPORT_PATH
    base.AUDIT_RESULT_PATH = AUDIT_RESULT_PATH

    candidates_by_id = load_candidates_by_id()
    promoted: list[dict[str, Any]] = []
    needs_more_evidence: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    skipped = Counter()
    by_node = Counter()

    for decision in audit_result["decisions"]:
        candidate_id = str(decision.get("candidate_id", ""))
        if candidate_id not in candidates_by_id:
            skipped["missing_candidate"] += 1
            continue
        candidate_path, candidate = candidates_by_id[candidate_id]
        decision_name = decision.get("decision")

        if decision_name == "accepted_for_draft" and decision.get("reviewed_allowed") is True:
            reason = validate_accepted_candidate(candidate, decision)
            if reason:
                skipped[reason] += 1
                continue
            patch = decision_patch(decision)
            item = base.candidate_to_knowledge(candidate, patch)
            apply_full_audit_notes(item, decision)
            knowledge_path = base.write_knowledge(item)
            base.update_candidate(candidate, item, knowledge_path)
            base.write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            promoted.append(
                {
                    "candidate_id": candidate_id,
                    "research_task_id": candidate.get("research_task_id"),
                    "knowledge_id": item["knowledge_id"],
                    "knowledge_path": rel(knowledge_path),
                    "canonical_node_id": item["metadata"]["canonical_node_id"],
                    "partition_id": item["metadata"]["partition_id"],
                    "review_status": "reviewed",
                    "machine_gate": "caveat_only",
                }
            )
            by_node[item["metadata"]["canonical_node_id"]] += 1
            continue

        if decision_name == "needs_more_evidence":
            mark_needs_more_evidence(candidate, decision)
            base.write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            needs_more_evidence.append(
                {
                    "candidate_id": candidate_id,
                    "research_task_id": candidate.get("research_task_id"),
                    "formal_knowledge_id": decision.get("formal_knowledge_id")
                    or base.deep_get(candidate, ("workflow", "formal_knowledge_id")),
                    "reason": decision.get("reason", ""),
                    "required_followups": as_list(decision.get("required_followups")),
                }
            )
            continue

        skipped[f"unsupported_decision_{decision_name}"] += 1

    expected_promoted = audit_result.get("batch_summary", {}).get("reviewed_allowed_count", 18)
    expected_needs = audit_result.get("batch_summary", {}).get("needs_more_evidence_count", 5)
    if len(promoted) != expected_promoted or len(needs_more_evidence) != expected_needs:
        raise ValueError(
            f"Unexpected import counts: promoted={len(promoted)} expected={expected_promoted}; "
            f"needs={len(needs_more_evidence)} expected={expected_needs}; skipped={dict(skipped)}"
        )

    report = {
        "report_id": "phase40_ai_passed_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "input_audit_result_path": str(input_path),
        "repository_audit_result_path": rel(AUDIT_RESULT_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more_evidence),
        "rejected_count": 0,
        "approved_count": 0,
        "default_guidance_allowed_count": 0,
        "hard_gate_allowed_count": 0,
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "needs_more_evidence": needs_more_evidence,
        "touched_candidates": sorted(set(touched_candidates)),
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate. needs_more_evidence candidates remain candidate-only.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
