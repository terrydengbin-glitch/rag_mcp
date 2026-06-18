"""Apply Phase 40 Batch D/E strict audit result to candidate files.

The audit result can route candidates into draft-ready or needs-more-evidence
queues, but it does not authorize formal reviewed/approved knowledge or default
guidance.
"""

from __future__ import annotations

import argparse
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


TODAY = date(2026, 6, 10).isoformat()
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase40_extended_p1_batch_de_20260610_strict_v1"
EXPECTED_SOURCE_PACKAGE_ID = "phase40_extended_p1_candidate_audit_package_20260610"
EXPECTED_TASKS = {f"P40-E{i:02d}" for i in range(1, 13)} | {f"P40-P{i:02d}" for i in range(1, 7)}

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT_COPY_PATH = resolve_repo_path("docs", "audit", f"{EXPECTED_AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase40_extended_p1_audit_import_report.json", start_file=__file__)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_result_path", type=Path)
    return parser.parse_args()


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase40_*.json")):
        candidate = read_json(path)
        task_id = candidate.get("research_task_id")
        if isinstance(task_id, str) and task_id in EXPECTED_TASKS:
            candidates[task_id] = (path, candidate)
    return candidates


def decision_by_task(audit_result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for decision in audit_result.get("decisions", []):
        if not isinstance(decision, dict):
            continue
        task_id = decision.get("research_task_id")
        if isinstance(task_id, str):
            decisions[task_id] = decision
    return decisions


def validate_audit_result(audit_result: dict[str, Any]) -> None:
    if audit_result.get("audit_result_id") != EXPECTED_AUDIT_RESULT_ID:
        raise ValueError("Unexpected audit_result_id")
    if audit_result.get("source_package_id") != EXPECTED_SOURCE_PACKAGE_ID:
        raise ValueError("Unexpected source_package_id")
    decisions = decision_by_task(audit_result)
    missing = sorted(EXPECTED_TASKS - set(decisions))
    unexpected = sorted(set(decisions) - EXPECTED_TASKS)
    if missing:
        raise ValueError(f"Missing audit decisions: {missing}")
    if unexpected:
        raise ValueError(f"Unexpected audit decisions: {unexpected}")
    forbidden = [
        item.get("candidate_id")
        for item in decisions.values()
        if item.get("reviewed_allowed")
        or item.get("approved_allowed")
        or item.get("default_guidance_allowed")
        or item.get("hard_gate_allowed")
    ]
    if forbidden:
        raise ValueError(f"Audit result unexpectedly allowed reviewed/approved/default/hard gate: {forbidden}")


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    review = candidate.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def enforce_candidate_safety(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False

    conversion_target = candidate.setdefault("conversion_target", {})
    conversion_target["default_guidance_allowed"] = False
    conversion_target["hard_gate_allowed"] = False
    conversion_target.setdefault("target_review_status", "draft")

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "candidate only; Batch D/E strict audit does not allow reviewed, approved, default guidance, or hard gate."

    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False


def apply_patch_notes(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    phase_trace = candidate.setdefault("phase40_trace", {})
    phase_trace["audit_patch_notes"] = {
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
    }
    limitations = candidate.setdefault("applicability", {}).setdefault("limitations", [])
    if isinstance(limitations, list):
        for note in decision.get("boundary_patch_notes", []) or []:
            if isinstance(note, str) and note not in limitations:
                limitations.append(note)


def apply_ai_audit(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "source_package_id": EXPECTED_SOURCE_PACKAGE_ID,
        "candidate_id": decision.get("candidate_id"),
        "research_task_id": decision.get("research_task_id"),
        "decision": decision.get("decision"),
        "reason": decision.get("reason"),
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "import_policy": "strict audit result may route candidates only; formal reviewed/approved creation is blocked.",
    }
    followups = decision.get("required_followups", [])
    if isinstance(followups, list):
        review["open_questions"] = followups
    apply_patch_notes(candidate, decision)


def mark_accepted_for_draft(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Batch D/E 严格审计允许进入 formal draft 准备队列；不是 reviewed、approved 或默认指导。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "ai_audited",
            "queue_group": "ai_passed",
            "formal_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
            "formal_review_status": "draft",
            "ai_audit_result_id": EXPECTED_AUDIT_RESULT_ID,
            "next_action": "prepare_formal_draft_after_codex_patch_review",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase40_extended_p1_audit_accepted_for_draft", "候选进入 formal draft 准备队列；不能直接 reviewed/approved。")


def mark_needs_more_evidence(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "Batch D/E 严格审计要求补充 claim-specific 来源、实例或 CEK-TA 契约后再二审。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": EXPECTED_AUDIT_RESULT_ID,
            "next_action": "supplement_sources_and_export_reaudit_package",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase40_extended_p1_audit_needs_more_evidence", "需补证后重新审计。")


def main() -> int:
    args = parse_args()
    audit_result = read_json(args.audit_result_path)
    validate_audit_result(audit_result)
    write_json(AUDIT_COPY_PATH, audit_result)

    candidates = load_candidates()
    decisions = decision_by_task(audit_result)
    touched: list[str] = []
    counts: Counter[str] = Counter()
    needs_more_evidence: list[dict[str, Any]] = []

    for task_id, decision in sorted(decisions.items()):
        if task_id not in candidates:
            raise ValueError(f"Candidate for {task_id} not found")
        path, candidate = candidates[task_id]
        if candidate.get("candidate_id") != decision.get("candidate_id"):
            raise ValueError(f"Candidate ID mismatch for {task_id}")
        decision_value = decision.get("decision")
        if decision_value == "accepted_for_draft":
            mark_accepted_for_draft(candidate, decision)
            counts["accepted_for_draft"] += 1
        elif decision_value == "needs_more_evidence":
            mark_needs_more_evidence(candidate, decision)
            counts["needs_more_evidence"] += 1
            needs_more_evidence.append(
                {
                    "research_task_id": task_id,
                    "candidate_id": candidate.get("candidate_id"),
                    "reason": decision.get("reason"),
                    "required_followups": decision.get("required_followups", []),
                    "source_patch_notes": decision.get("source_patch_notes", []),
                }
            )
        elif decision_value == "rejected":
            enforce_candidate_safety(candidate)
            candidate.setdefault("status", {}).update(
                {
                    "review_status": "rejected",
                    "ingestion_decision": "reject",
                    "decision_reason": str(decision.get("reason") or "Batch D/E 严格审计拒绝。"),
                    "updated_at": TODAY,
                }
            )
            apply_ai_audit(candidate, decision)
            counts["rejected"] += 1
        else:
            raise ValueError(f"Unsupported decision {decision_value!r} for {task_id}")
        write_json(path, candidate)
        touched.append(repo_rel(path))

    report = {
        "report_id": "phase40_extended_p1_audit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-312",
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "source_package_id": EXPECTED_SOURCE_PACKAGE_ID,
        "input_audit_result_path": str(args.audit_result_path),
        "canonical_audit_result_path": repo_rel(AUDIT_COPY_PATH),
        "decision_counts": dict(counts),
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_allowed_count": 0,
        "hard_gate_allowed_count": 0,
        "needs_more_evidence": needs_more_evidence,
        "touched_candidates": touched,
        "next_steps": [
            "为 5 条 needs_more_evidence 候选补充 claim-specific 来源和 CEK-TA 契约字段。",
            "导出 Batch D/E 补证二审 JSON。",
            "只有二审明确 reviewed_allowed=true 后，才能创建 formal reviewed knowledge。",
        ],
        "boundary": "accepted_for_draft is not reviewed or approved; all Batch D/E candidates remain blocked from default guidance and hard gate.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"ok": True, "report": repo_rel(REPORT_PATH), "counts": dict(counts)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
