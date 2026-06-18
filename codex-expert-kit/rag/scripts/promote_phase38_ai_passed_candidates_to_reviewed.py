"""Promote remaining Phase 38 ai_passed candidates into formal reviewed knowledge.

This is a narrow Phase 32/38 maintenance script. It only converts candidates
that are already accepted_for_draft and still sit in workflow.queue_group
ai_passed. It never creates approved/default-guidance/hard-gate knowledge.
"""

from __future__ import annotations

import importlib.util
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


TASK_ID = "CEK-TA-341"
TODAY = date(2026, 6, 11).isoformat()
SCRIPT_DIR = Path(__file__).resolve().parent
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_ai_passed_to_reviewed_promotion_report.json", start_file=__file__
)


def load_phase38_promoter() -> Any:
    path = SCRIPT_DIR / "promote_phase38_accepted_candidates_to_reviewed.py"
    spec = importlib.util.spec_from_file_location("phase38_promoter", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load promoter script: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.AUDIT_TASK_ID = TASK_ID
    module.TODAY = TODAY
    return module


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


def workflow_group(candidate: dict[str, Any]) -> str:
    workflow = candidate.get("workflow") if isinstance(candidate.get("workflow"), dict) else {}
    return str(workflow.get("queue_group") or "")


def main() -> int:
    promoter = load_phase38_promoter()
    promoted: list[dict[str, Any]] = []
    skipped = Counter()
    touched_candidates: list[str] = []

    for candidate_path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        candidate = read_json(candidate_path)
        if workflow_group(candidate) != "ai_passed":
            skipped["not_ai_passed"] += 1
            continue

        reason = promoter.validate_candidate_for_promotion(candidate)
        if reason:
            skipped[reason] += 1
            continue

        item = promoter.candidate_to_knowledge(candidate)
        item["metadata"]["classification_notes"] = (
            "Phase 38 ai_passed residual candidate promoted by CEK-TA-341; "
            "formal reviewed/caveat_only only, not approved/default guidance/hard gate. "
            + str(item["metadata"].get("classification_notes", ""))
        )
        item["machine_gate"]["default_guidance"] = "caveat_only"
        item["machine_gate"]["reason"] = (
            "CEK-TA-341 将 Phase 38 ai_passed 候选沉淀为 formal reviewed；"
            "仅可审计检索，不可作为 approved 默认指导或 hard gate。"
        )
        item["review"]["default_guidance_allowed"] = False
        item["review"]["approval_status"] = "not_requested"
        item["review"]["ai_audit"]["approved_allowed"] = False
        item["review"]["ai_audit"]["default_guidance_allowed"] = False
        item["review"]["ai_audit"]["hard_gate_allowed"] = False
        item["phase38_conversion"]["promoted_by_task"] = TASK_ID

        knowledge_path = promoter.write_knowledge(item)
        promoter.update_candidate_backlink(candidate, item, knowledge_path)
        write_json(candidate_path, candidate)
        touched_candidates.append(rel(candidate_path))
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
                "default_guidance_allowed": False,
                "approved_allowed": False,
                "hard_gate_allowed": False,
            }
        )

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    by_partition = Counter(item["partition_id"] for item in promoted)
    report = {
        "report_id": "phase38_ai_passed_to_reviewed_promotion_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "input_scope": "Phase 38 candidates with workflow.queue_group == ai_passed",
        "promoted_count": len(promoted),
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "by_partition": dict(sorted(by_partition.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
