"""Validate the Phase 32 candidate-to-reviewed workflow gates."""

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


CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase32_candidate_to_reviewed_quality_gate.json", start_file=__file__)


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def load_items(root: Path, key: str) -> dict[str, tuple[Path, dict[str, Any]]]:
    items: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(root.glob("**/*.json")):
        payload = read_json(path)
        item_id = payload.get(key)
        if isinstance(item_id, str):
            items[item_id] = (path, payload)
    return items


def main() -> int:
    failures: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    candidates = load_items(CANDIDATE_ROOT, "candidate_id")
    knowledge = load_items(KNOWLEDGE_ROOT, "knowledge_id")
    knowledge_by_candidate = {
        str(deep_get(payload, ("review", "source_candidate_id"))): (knowledge_id, path, payload)
        for knowledge_id, (path, payload) in knowledge.items()
        if deep_get(payload, ("review", "source_candidate_id"))
    }

    for candidate_id, (path, candidate) in candidates.items():
        workflow = candidate.get("workflow")
        if not isinstance(workflow, dict):
            failures.append({"id": candidate_id, "path": rel(path), "reason": "candidate_missing_workflow"})
            continue
        for field in ("stage", "queue_group", "hidden_from_default_queue", "next_action"):
            if field not in workflow:
                failures.append({"id": candidate_id, "path": rel(path), "reason": f"workflow_missing_{field}"})
        if workflow.get("queue_group") == "formalized":
            formal_id = workflow.get("formal_knowledge_id")
            formal = knowledge.get(str(formal_id)) if formal_id else None
            if formal is None:
                failures.append({"id": candidate_id, "path": rel(path), "reason": "formalized_candidate_missing_formal_knowledge"})
                continue
            review = formal[1].get("review", {})
            if review.get("source_candidate_id") != candidate_id:
                failures.append({"id": candidate_id, "path": rel(formal[0]), "reason": "formal_knowledge_source_candidate_mismatch"})
            if not review.get("ai_audit_result_id"):
                failures.append({"id": candidate_id, "path": rel(formal[0]), "reason": "formal_knowledge_missing_ai_audit_result_id"})
        elif candidate_id in knowledge_by_candidate:
            warnings.append({"id": candidate_id, "path": rel(path), "reason": "candidate_has_formal_backlink_but_not_formalized"})

    for knowledge_id, (path, item) in knowledge.items():
        review = item.get("review", {})
        review_status = review.get("review_status")
        conflict_status = deep_get(
            item,
            ("conflict_audit", "conflict_status"),
            deep_get(item, ("metadata", "conflict_status"), "none"),
        )
        source_evidence = item.get("source_evidence", [])
        if review_status in {"reviewed", "approved"}:
            if not isinstance(source_evidence, list) or not source_evidence:
                failures.append({"id": knowledge_id, "path": rel(path), "reason": "reviewed_or_approved_missing_source_evidence"})
            if conflict_status in {"confirmed", "unchecked"}:
                failures.append({"id": knowledge_id, "path": rel(path), "reason": f"unsafe_conflict_status_{conflict_status}"})
            if not review.get("source_candidate_id") and review.get("ai_audit"):
                failures.append({"id": knowledge_id, "path": rel(path), "reason": "ai_audited_reviewed_missing_source_candidate_id"})
            if review_status == "reviewed" and review.get("default_guidance_allowed") is True:
                failures.append({"id": knowledge_id, "path": rel(path), "reason": "reviewed_item_default_guidance_allowed_true"})
        if review_status == "approved" and review.get("approval_status") != "approved":
            failures.append({"id": knowledge_id, "path": rel(path), "reason": "approved_without_approval_status"})

    if not INDEX_PATH.exists():
        failures.append({"id": "knowledge_items_index", "path": rel(INDEX_PATH), "reason": "knowledge_items_index_missing"})

    report = {
        "report_id": "phase32_candidate_to_reviewed_quality_gate",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "candidate_count": len(candidates),
        "knowledge_count": len(knowledge),
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "reviewed is not approved; default guidance requires explicit approval.",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
