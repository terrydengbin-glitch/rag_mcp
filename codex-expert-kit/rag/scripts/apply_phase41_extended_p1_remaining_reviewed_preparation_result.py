"""Apply Phase 41 remaining reviewed-preparation audit result.

This task imports the strict reaudit for the 13 remaining Phase 41
P0-Extended/P1 candidates. It converts only the 12 decisions with
reviewed_allowed=true into formal reviewed/caveat_only knowledge. The single
P41-A06 needs_more_evidence item is metadata-normalized but remains blocked
from formal reviewed, approved, default guidance, and hard gate.
"""

from __future__ import annotations

import argparse
import importlib.util
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


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-336"
AUDIT_RESULT_ID = "audit_result_phase41_extended_p1_remaining_reviewed_preparation_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase41_extended_p1_remaining_reviewed_preparation_audit_package_20260610"
EXPECTED_TOTAL = 13
EXPECTED_PROMOTED = 12
EXPECTED_NEEDS_MORE = 1
A06_CANDIDATE_ID = "cand_20260610_phase41_p41_a06_baseline_001"
A06_NORMALIZED_CLAIM = "phase41.ensemble_after_single_model_baseline_insufficient.v1"
A06_KNOWLEDGE_ID = "kb_ai_hybrid_scoring.phase41.ensemble_after_single_model_baseline_insufficient.v1"

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_SCRIPT = SCRIPT_DIR / "apply_phase41_reviewed_preparation_result.py"
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT_COPY_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase41_extended_p1_remaining_reviewed_preparation_import_report.json", start_file=__file__
)
A06_FOLLOWUP_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase41_a06_metadata_slug_followup_report.json", start_file=__file__
)


def load_base_module():
    spec = importlib.util.spec_from_file_location("phase41_reviewed_preparation_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load base script: {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.TODAY = TODAY
    module.TASK_ID = TASK_ID
    module.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    module.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "audit_result_path",
        type=Path,
        nargs="?",
        default=resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__),
    )
    return parser.parse_args()


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


def validate_audit_result(audit_result: dict[str, Any]) -> None:
    if audit_result.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit_result.get('audit_result_id')}")
    if audit_result.get("source_package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected source_package_id: {audit_result.get('source_package_id')}")
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != EXPECTED_TOTAL:
        raise ValueError(f"Expected {EXPECTED_TOTAL} decisions")
    accepted = 0
    needs_more = 0
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError("Decision entries must be JSON objects")
        if decision.get("approved_allowed") is not False:
            raise ValueError(f"{decision.get('candidate_id')}: approved_allowed must be false")
        if decision.get("default_guidance_allowed") is not False:
            raise ValueError(f"{decision.get('candidate_id')}: default_guidance_allowed must be false")
        if decision.get("hard_gate_allowed") is not False:
            raise ValueError(f"{decision.get('candidate_id')}: hard_gate_allowed must be false")
        if decision.get("decision") == "accepted_for_draft":
            accepted += 1
            if decision.get("reviewed_allowed") is not True:
                raise ValueError(f"{decision.get('candidate_id')}: accepted_for_draft must have reviewed_allowed=true")
        elif decision.get("decision") == "needs_more_evidence":
            needs_more += 1
            if decision.get("reviewed_allowed") is not False:
                raise ValueError(f"{decision.get('candidate_id')}: needs_more_evidence must have reviewed_allowed=false")
            if decision.get("candidate_id") != A06_CANDIDATE_ID:
                raise ValueError("Only P41-A06 is expected to remain needs_more_evidence")
        else:
            raise ValueError(f"{decision.get('candidate_id')}: unsupported decision {decision.get('decision')}")
    if accepted != EXPECTED_PROMOTED or needs_more != EXPECTED_NEEDS_MORE:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} accepted and {EXPECTED_NEEDS_MORE} needs_more, got {accepted}/{needs_more}")


def load_candidates_by_id() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_p41_*.json")):
        candidate = read_json(path)
        candidate_id = candidate.get("candidate_id")
        if isinstance(candidate_id, str):
            candidates[candidate_id] = (path, candidate)
    return candidates


def fix_a06_metadata_slug(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.setdefault("claim", {})
    if isinstance(claim, dict):
        claim["normalized_claim"] = A06_NORMALIZED_CLAIM
    candidate["normalized_claim"] = A06_NORMALIZED_CLAIM

    conversion = candidate.setdefault("conversion_target", {})
    conversion["proposed_knowledge_id"] = A06_KNOWLEDGE_ID
    conversion["target_review_status"] = "blocked"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    workflow = candidate.setdefault("workflow", {})
    workflow["formal_knowledge_id"] = A06_KNOWLEDGE_ID
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["formal_review_status"] = "blocked"
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["hidden_from_default_queue"] = False
    workflow["visible_in_default_guidance_queue"] = False
    workflow["next_action"] = "supplement_baseline_comparison_and_auditability_report_then_reaudit"
    workflow["default_guidance_allowed"] = False

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = str(decision.get("reason", "P41-A06 metadata/slug conflict requires reaudit."))
    status["updated_at"] = TODAY

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "P41-A06 reviewed-preparation 再审计发现 metadata/slug 冲突；修复并补充报告前不得 formal reviewed。"
    machine_gate["requires_human_escalation"] = True

    audit_export_meta = candidate.setdefault("_audit_export_meta", {})
    audit_export_meta["proposed_knowledge_id"] = A06_KNOWLEDGE_ID
    audit_export_meta["normalized_claim"] = A06_NORMALIZED_CLAIM
    audit_export_meta["formal_index_has_target"] = False
    audit_export_meta["current_reviewed_allowed"] = False
    audit_export_meta["metadata_slug_fixed_at"] = TODAY
    audit_export_meta["required_next_decision"] = "补充 single-model baseline comparison report 和 auditability impact report 后再审。"

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
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
                "action": "phase41_a06_metadata_slug_normalized_but_blocked",
                "reason": f"{TASK_ID}: 统一 formal_knowledge_id / proposed_knowledge_id / normalized_claim；仍需补证再审。",
            }
        )
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "normalized_claim": A06_NORMALIZED_CLAIM,
        "proposed_knowledge_id": A06_KNOWLEDGE_ID,
        "formal_knowledge_id": workflow.get("formal_knowledge_id"),
        "status": status.get("ingestion_decision"),
        "reviewed_allowed": False,
        "required_followups": as_list(decision.get("required_followups")),
    }


def main() -> int:
    args = parse_args()
    base = load_base_module()
    audit_result = read_json(args.audit_result_path)
    validate_audit_result(audit_result)
    if args.audit_result_path.resolve() != AUDIT_COPY_PATH.resolve():
        AUDIT_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.audit_result_path, AUDIT_COPY_PATH)

    candidates = load_candidates_by_id()
    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    needs_more: list[dict[str, Any]] = []
    skipped = Counter()

    for decision in audit_result["decisions"]:
        candidate_id = str(decision["candidate_id"])
        if candidate_id not in candidates:
            skipped["candidate_file_not_found"] += 1
            continue
        candidate_path, candidate = candidates[candidate_id]
        if decision["decision"] == "accepted_for_draft":
            reason = base.validate_candidate_for_reviewed(candidate, decision)
            if reason:
                skipped[reason] += 1
                continue
            item = base.candidate_to_knowledge(candidate, decision)
            knowledge_path = base.write_knowledge(item)
            base.update_candidate_backlink(candidate, item, knowledge_path, decision)
            write_json(candidate_path, candidate)
            touched_candidates.append(repo_rel(candidate_path))
            written_knowledge_paths.append(repo_rel(knowledge_path))
            promoted.append(
                {
                    "candidate_id": candidate_id,
                    "research_task_id": candidate.get("research_task_id"),
                    "knowledge_id": item["knowledge_id"],
                    "knowledge_path": repo_rel(knowledge_path),
                    "canonical_node_id": item["metadata"]["canonical_node_id"],
                    "partition_id": item["metadata"]["partition_id"],
                    "review_status": "reviewed",
                    "machine_gate": "caveat_only",
                }
            )
        else:
            followup = fix_a06_metadata_slug(candidate, decision)
            write_json(candidate_path, candidate)
            touched_candidates.append(repo_rel(candidate_path))
            needs_more.append(followup)

    if len(promoted) != EXPECTED_PROMOTED:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} promotions, got {len(promoted)}; skipped={dict(skipped)}")
    if len(needs_more) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"Expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {len(needs_more)}")

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    by_partition = Counter(item["partition_id"] for item in promoted)
    followup_report = {
        "report_id": "phase41_a06_metadata_slug_followup_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "items": needs_more,
        "boundary": "P41-A06 已统一 metadata/slug，但仍是 candidate needs_more_evidence；没有 formal reviewed、approved、default guidance 或 hard gate。",
        "next_action": "补充 single-model baseline comparison report 和 auditability impact report 后导出 P41-A06 单条再审包。",
    }
    write_json(A06_FOLLOWUP_REPORT_PATH, followup_report)

    report = {
        "report_id": "phase41_extended_p1_remaining_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_COPY_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "by_node": dict(sorted(by_node.items())),
        "by_partition": dict(sorted(by_partition.items())),
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "a06_followup_report": repo_rel(A06_FOLLOWUP_REPORT_PATH),
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "skipped": dict(skipped),
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate. P41-A06 remains blocked.",
        "next_action": "重建 knowledge_items/UI fixture，并执行 Phase 41 40 条运行时联动验证；P41-A06 补证后单独再审。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
