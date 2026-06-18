"""Apply Phase 41 reviewed-preparation supplemental re-audit result.

This imports the focused P41-B05/P41-D03 supplemental audit result, converts
only accepted_for_draft + reviewed_allowed=true candidates into formal
reviewed knowledge, and keeps approved/default-guidance/hard-gate disabled.
"""

from __future__ import annotations

import argparse
import json
import shutil
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
import apply_phase41_reviewed_preparation_result as base  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-326"
AUDIT_RESULT_ID = "audit_result_phase41_reviewed_preparation_supplemental_reaudit_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase41_reviewed_preparation_supplemental_reaudit_package_20260610"
EXPECTED_COUNT = 2
TARGET_RESEARCH_TASKS = {"P41-B05", "P41-D03"}

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_COPY_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase41_reviewed_preparation_supplemental_reaudit_import_report.json", start_file=__file__
)
REMAINING_FOLLOWUP_PATH = resolve_repo_path(
    "docs", "reports", "phase41_reviewed_preparation_remaining_followups.json", start_file=__file__
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "audit_result_path",
        nargs="?",
        type=Path,
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


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


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
    if len(decisions) != EXPECTED_COUNT:
        errors.append(f"expected {EXPECTED_COUNT} decisions, got {len(decisions)}")
    seen_tasks: set[str] = set()
    for decision in decisions:
        if not isinstance(decision, dict):
            errors.append("decision entry must be object")
            continue
        task_id = str(decision.get("research_task_id", ""))
        seen_tasks.add(task_id)
        if task_id not in TARGET_RESEARCH_TASKS:
            errors.append(f"{decision.get('candidate_id')}: unexpected research_task_id={task_id}")
        if decision.get("decision") != "accepted_for_draft":
            errors.append(f"{decision.get('candidate_id')}: supplemental result must be accepted_for_draft")
        if decision.get("reviewed_allowed") is not True:
            errors.append(f"{decision.get('candidate_id')}: reviewed_allowed must be true")
        if decision.get("approved_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: approved_allowed must be false")
        if decision.get("default_guidance_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: default_guidance_allowed must be false")
        if decision.get("hard_gate_allowed") is not False:
            errors.append(f"{decision.get('candidate_id')}: hard_gate_allowed must be false")
    missing = TARGET_RESEARCH_TASKS - seen_tasks
    if missing:
        errors.append(f"missing decisions for {sorted(missing)}")
    return errors


def load_candidates_by_id() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_p41_*.json")):
        candidate = read_json(path)
        candidate_id = candidate.get("candidate_id")
        if isinstance(candidate_id, str):
            candidates[candidate_id] = (path, candidate)
    return candidates


def validate_candidate_for_reviewed(candidate: dict[str, Any], decision: dict[str, Any]) -> str | None:
    candidate_id = str(candidate.get("candidate_id", ""))
    if candidate_id != decision.get("candidate_id"):
        return "candidate_id_mismatch"
    if candidate.get("research_task_id") not in TARGET_RESEARCH_TASKS:
        return "not_target_research_task"
    if deep_get(candidate, ("workflow", "queue_group")) != "needs_more_evidence":
        return "not_needs_more_evidence_queue"
    if deep_get(candidate, ("status", "ingestion_decision")) != "needs_more_evidence":
        return "not_currently_needs_more_evidence"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_knowledge_id"
    if not str(deep_get(candidate, ("classification", "canonical_node_id"), "")).startswith("kt.ai_engineering."):
        return "wrong_node"
    sources = as_list(candidate.get("source_refs"))
    if not sources:
        return "missing_sources"
    source_ids = {str(source.get("source_id")) for source in sources if isinstance(source, dict)}
    if candidate.get("research_task_id") == "P41-B05" and "src_phase41_training_dataset_manifest_contract" not in source_ids:
        return "missing_training_dataset_manifest_contract"
    if candidate.get("research_task_id") == "P41-D03" and "src_phase41_feature_lineage_record_contract" not in source_ids:
        return "missing_feature_lineage_record_contract"
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {"none", "resolved"}:
        return "unsafe_conflict"
    return None


def patch_base_constants() -> None:
    base.TODAY = TODAY
    base.TASK_ID = TASK_ID
    base.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    base.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID
    base.EXPECTED_COUNT = EXPECTED_COUNT
    base.AUDIT_COPY_PATH = AUDIT_COPY_PATH
    base.REPORT_PATH = REPORT_PATH
    base.REMAINING_FOLLOWUP_PATH = REMAINING_FOLLOWUP_PATH


def main() -> int:
    args = parse_args()
    patch_base_constants()
    audit_result = read_json(args.audit_result_path)
    errors = validate_audit_result(audit_result)
    if errors:
        raise ValueError("; ".join(errors))

    AUDIT_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if args.audit_result_path.resolve() != AUDIT_COPY_PATH.resolve():
        shutil.copyfile(args.audit_result_path, AUDIT_COPY_PATH)

    candidates = load_candidates_by_id()
    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    skipped = Counter()

    for decision in audit_result["decisions"]:
        candidate_id = str(decision.get("candidate_id", ""))
        if candidate_id not in candidates:
            skipped["candidate_file_not_found"] += 1
            continue
        candidate_path, candidate = candidates[candidate_id]
        reason = validate_candidate_for_reviewed(candidate, decision)
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
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
        )

    if len(promoted) != EXPECTED_COUNT:
        raise ValueError(f"Expected {EXPECTED_COUNT} promotions, got {len(promoted)}; skipped={dict(skipped)}")

    write_json(
        REMAINING_FOLLOWUP_PATH,
        {
            "report_id": "phase41_reviewed_preparation_remaining_followups",
            "generated_at": TODAY,
            "audit_result_id": AUDIT_RESULT_ID,
            "remaining_count": 0,
            "items": [],
            "boundary": "Phase 41 reviewed-preparation supplemental items have been formalized as reviewed/caveat_only; no approved/default guidance/hard gate.",
        },
    )

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    by_partition = Counter(item["partition_id"] for item in promoted)
    report = {
        "report_id": "phase41_reviewed_preparation_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_COPY_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "by_node": dict(sorted(by_node.items())),
        "by_partition": dict(sorted(by_partition.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "remaining_followups": repo_rel(REMAINING_FOLLOWUP_PATH),
        "skipped": dict(skipped),
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate.",
        "next_action": "重建 knowledge_items/UI fixture，并执行 MCP/SearchLab/KnowledgeTree 联动验证。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
