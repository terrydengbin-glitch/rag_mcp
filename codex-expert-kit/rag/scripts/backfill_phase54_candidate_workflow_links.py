"""Backfill historical candidate workflow and formal review backlinks."""

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
REPORT_PATH = resolve_repo_path("docs", "reports", "phase54_candidate_workflow_backfill_report.json", start_file=__file__)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


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
        payload = load_json(path)
        item_id = payload.get(key)
        if isinstance(item_id, str) and item_id:
            items[item_id] = (path, payload)
    return items


def candidate_review_status(candidate: dict[str, Any]) -> str:
    for path in (
        ("status", "review_status"),
        ("review", "review_status"),
    ):
        value = deep_get(candidate, path)
        if isinstance(value, str) and value:
            return value
    return "candidate_ready"


def candidate_decision(candidate: dict[str, Any]) -> str:
    for path in (
        ("status", "ingestion_decision"),
        ("review", "ai_audit", "decision"),
        ("workflow", "stage"),
    ):
        value = deep_get(candidate, path)
        if isinstance(value, str) and value:
            return value
    return candidate_review_status(candidate)


def infer_next_action(candidate: dict[str, Any], workflow: dict[str, Any]) -> str:
    queue_group = workflow.get("queue_group")
    stage = workflow.get("stage")
    status = candidate_review_status(candidate)
    decision = candidate_decision(candidate)
    if queue_group == "formalized" or stage == "formalized_reviewed" or status in {"formalized", "reviewed"}:
        return "none"
    if status == "rejected" or decision == "rejected":
        return "archive_or_rebuild_if_needed"
    if status == "needs_more_evidence" or decision == "needs_more_evidence":
        return "collect_more_evidence"
    if decision in {"accepted_for_draft", "accepted", "ai_passed"}:
        return "prepare_reviewed_caveat_only_audit"
    return "external_ai_audit"


def audit_result_id_from_candidate(candidate: dict[str, Any]) -> str | None:
    direct = deep_get(candidate, ("review", "ai_audit", "audit_result_id"))
    if isinstance(direct, str) and direct:
        return direct
    audit_log = deep_get(candidate, ("review", "audit_log"), [])
    if isinstance(audit_log, list):
        for entry in reversed(audit_log):
            if isinstance(entry, dict) and isinstance(entry.get("audit_result_id"), str) and entry["audit_result_id"]:
                return entry["audit_result_id"]
    return None


def build_candidate_lookup(candidates: dict[str, tuple[Path, dict[str, Any]]]) -> dict[str, str]:
    by_formal: dict[str, str] = {}
    for candidate_id, (_, candidate) in candidates.items():
        possible_ids = [
            deep_get(candidate, ("workflow", "formal_knowledge_id")),
            deep_get(candidate, ("workflow", "conversion_target", "proposed_knowledge_id")),
            deep_get(candidate, ("conversion_target", "proposed_knowledge_id")),
            deep_get(candidate, ("proposed_knowledge_id",)),
        ]
        for value in possible_ids:
            if isinstance(value, str) and value:
                by_formal.setdefault(value, candidate_id)
    return by_formal


def main() -> int:
    generated_at = utc_now()
    candidates = load_items(CANDIDATE_ROOT, "candidate_id")
    knowledge = load_items(KNOWLEDGE_ROOT, "knowledge_id")
    candidate_by_formal = build_candidate_lookup(candidates)

    updated_candidates: list[dict[str, Any]] = []
    updated_formal: list[dict[str, Any]] = []
    manual_required: list[dict[str, Any]] = []

    for candidate_id, (path, candidate) in candidates.items():
        workflow = candidate.setdefault("workflow", {})
        if not isinstance(workflow, dict):
            manual_required.append({"candidate_id": candidate_id, "path": rel(path), "reason": "workflow_not_object"})
            continue
        before = json.loads(json.dumps(workflow, ensure_ascii=False))
        changed_fields: list[str] = []

        formal_id = workflow.get("formal_knowledge_id")
        if not isinstance(formal_id, str) or not formal_id:
            for value in (
                deep_get(candidate, ("conversion_target", "proposed_knowledge_id")),
                deep_get(candidate, ("workflow", "conversion_target", "proposed_knowledge_id")),
            ):
                if isinstance(value, str) and value in knowledge:
                    workflow["formal_knowledge_id"] = value
                    formal_id = value
                    changed_fields.append("workflow.formal_knowledge_id")
                    break

        if "stage" not in workflow:
            if isinstance(formal_id, str) and formal_id in knowledge:
                workflow["stage"] = "formalized_reviewed"
            elif candidate_decision(candidate) in {"accepted_for_draft", "accepted", "ai_passed"}:
                workflow["stage"] = "accepted_for_draft"
            else:
                workflow["stage"] = candidate_review_status(candidate)
            changed_fields.append("workflow.stage")

        if "queue_group" not in workflow:
            if isinstance(formal_id, str) and formal_id in knowledge:
                workflow["queue_group"] = "formalized"
            elif candidate_review_status(candidate) == "rejected":
                workflow["queue_group"] = "rejected"
            elif candidate_review_status(candidate) == "needs_more_evidence":
                workflow["queue_group"] = "needs_more_evidence"
            elif candidate_decision(candidate) in {"accepted_for_draft", "accepted", "ai_passed"}:
                workflow["queue_group"] = "ai_passed"
            else:
                workflow["queue_group"] = "pending"
            changed_fields.append("workflow.queue_group")

        if "hidden_from_default_queue" not in workflow:
            workflow["hidden_from_default_queue"] = True
            changed_fields.append("workflow.hidden_from_default_queue")

        if "next_action" not in workflow:
            workflow["next_action"] = infer_next_action(candidate, workflow)
            changed_fields.append("workflow.next_action")

        if isinstance(formal_id, str) and formal_id in knowledge:
            formal_path, formal = knowledge[formal_id]
            if "formal_knowledge_path" not in workflow:
                workflow["formal_knowledge_path"] = rel(formal_path)
                changed_fields.append("workflow.formal_knowledge_path")
            if workflow.get("queue_group") != "formalized":
                workflow["queue_group"] = "formalized"
                changed_fields.append("workflow.queue_group")
            if workflow.get("stage") != "formalized_reviewed":
                workflow["stage"] = "formalized_reviewed"
                changed_fields.append("workflow.stage")
            if workflow.get("next_action") != "none":
                workflow["next_action"] = "none"
                changed_fields.append("workflow.next_action")

        if changed_fields:
            path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            updated_candidates.append(
                {
                    "candidate_id": candidate_id,
                    "path": rel(path),
                    "fields": sorted(set(changed_fields)),
                    "workflow_before": before,
                    "workflow_after": workflow,
                }
            )

    for knowledge_id, (path, item) in knowledge.items():
        review = item.setdefault("review", {})
        if not isinstance(review, dict):
            manual_required.append({"knowledge_id": knowledge_id, "path": rel(path), "reason": "review_not_object"})
            continue
        before = dict(review)
        changed_fields: list[str] = []

        candidate_id = review.get("source_candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id:
            metadata_candidate_id = deep_get(item, ("metadata", "source_candidate_id"))
            if isinstance(metadata_candidate_id, str) and metadata_candidate_id in candidates:
                review["source_candidate_id"] = metadata_candidate_id
                candidate_id = metadata_candidate_id
                changed_fields.append("review.source_candidate_id")
            elif knowledge_id in candidate_by_formal:
                review["source_candidate_id"] = candidate_by_formal[knowledge_id]
                candidate_id = candidate_by_formal[knowledge_id]
                changed_fields.append("review.source_candidate_id")

        if not isinstance(review.get("ai_audit_result_id"), str) or not review.get("ai_audit_result_id"):
            ai_audit_id = deep_get(item, ("review", "ai_audit", "audit_result_id"))
            if isinstance(ai_audit_id, str) and ai_audit_id:
                review["ai_audit_result_id"] = ai_audit_id
                changed_fields.append("review.ai_audit_result_id")
            elif isinstance(candidate_id, str) and candidate_id in candidates:
                candidate_audit_id = audit_result_id_from_candidate(candidates[candidate_id][1])
                if candidate_audit_id:
                    review["ai_audit_result_id"] = candidate_audit_id
                    changed_fields.append("review.ai_audit_result_id")

        if isinstance(candidate_id, str) and candidate_id in candidates:
            candidate_path, candidate = candidates[candidate_id]
            workflow = candidate.setdefault("workflow", {})
            if isinstance(workflow, dict):
                changed_candidate_fields: list[str] = []
                if workflow.get("formal_knowledge_id") != knowledge_id:
                    workflow["formal_knowledge_id"] = knowledge_id
                    changed_candidate_fields.append("workflow.formal_knowledge_id")
                if workflow.get("formal_knowledge_path") != rel(path):
                    workflow["formal_knowledge_path"] = rel(path)
                    changed_candidate_fields.append("workflow.formal_knowledge_path")
                if workflow.get("stage") != "formalized_reviewed":
                    workflow["stage"] = "formalized_reviewed"
                    changed_candidate_fields.append("workflow.stage")
                if workflow.get("queue_group") != "formalized":
                    workflow["queue_group"] = "formalized"
                    changed_candidate_fields.append("workflow.queue_group")
                if workflow.get("hidden_from_default_queue") is not True:
                    workflow["hidden_from_default_queue"] = True
                    changed_candidate_fields.append("workflow.hidden_from_default_queue")
                if workflow.get("next_action") != "none":
                    workflow["next_action"] = "none"
                    changed_candidate_fields.append("workflow.next_action")
                if changed_candidate_fields:
                    candidate_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                    updated_candidates.append(
                        {
                            "candidate_id": candidate_id,
                            "path": rel(candidate_path),
                            "fields": sorted(set(changed_candidate_fields)),
                            "workflow_after": workflow,
                            "linked_from_knowledge_id": knowledge_id,
                        }
                    )

        if changed_fields:
            path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            updated_formal.append(
                {
                    "knowledge_id": knowledge_id,
                    "path": rel(path),
                    "fields": sorted(set(changed_fields)),
                    "review_before": before,
                    "review_after": review,
                }
            )

    report = {
        "report_id": "phase54_candidate_workflow_backfill_report",
        "generated_at": generated_at,
        "task_id": "CEK-TA-530",
        "candidate_count": len(candidates),
        "formal_knowledge_count": len(knowledge),
        "formalized_candidate_count": sum(
            1
            for _, candidate in candidates.values()
            if deep_get(candidate, ("workflow", "queue_group")) == "formalized"
            or candidate_review_status(candidate) in {"formalized", "reviewed"}
        ),
        "updated_candidate_count": len(updated_candidates),
        "updated_formal_count": len(updated_formal),
        "manual_required_count": len(manual_required),
        "updated_candidates": updated_candidates,
        "updated_formal_items": updated_formal,
        "manual_required": manual_required,
        "boundary": {
            "candidate_deleted": False,
            "formal_review_status_changed": False,
            "approved_or_default_or_hard_gate_enabled": False,
        },
        "status": "pass" if not manual_required else "manual_required",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "candidate_count": len(candidates),
                "formal_knowledge_count": len(knowledge),
                "updated_candidate_count": len(updated_candidates),
                "updated_formal_count": len(updated_formal),
                "manual_required_count": len(manual_required),
                "status": report["status"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
