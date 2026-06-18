"""Apply Phase 43 formal draft reviewed/caveat_only audit result.

This script consumes the external audit conclusion for the 29 Phase 43 formal
draft knowledge items. It promotes only those items to formal reviewed with
machine_gate.default_guidance=caveat_only. It never creates approved knowledge,
default guidance allow, hard gate, real project memory, database migrations, or
vendor activation.
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
TASK_ID = "CEK-TA-368"
AUDIT_RESULT_ID = "audit_result_phase43_formal_draft_reviewed_preparation_20260611_strict_v1"
PACKAGE_ID = "phase43_formal_draft_reviewed_audit_package_20260611"
KNOWLEDGE_DIR = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "knowledge",
    "KB_AI_27_PROJECT_MEMORY",
    start_file=__file__,
)
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    start_file=__file__,
)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs",
    "audit",
    f"{AUDIT_RESULT_ID}.json",
    start_file=__file__,
)
REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase43_formal_draft_reviewed_import_report.json",
    start_file=__file__,
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


def phase43_knowledge_files() -> list[Path]:
    return sorted(KNOWLEDGE_DIR.glob("kb_ai_project_memory.phase43.*.json"))


def phase43_knowledge_items() -> list[tuple[Path, dict[str, Any]]]:
    result: list[tuple[Path, dict[str, Any]]] = []
    for path in phase43_knowledge_files():
        item = read_json(path)
        if str(item.get("knowledge_id", "")).startswith("kb_ai_project_memory.phase43."):
            result.append((path, item))
    return result


def audit_result_payload(items: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    knowledge_results = []
    node_counts = Counter()
    for path, item in items:
        metadata = item.get("metadata", {}) if isinstance(item.get("metadata"), dict) else {}
        review = item.get("review", {}) if isinstance(item.get("review"), dict) else {}
        node_id = str(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")
        node_counts[node_id] += 1
        knowledge_results.append(
            {
                "knowledge_id": item.get("knowledge_id"),
                "knowledge_path": rel(path),
                "source_candidate_id": review.get("source_candidate_id"),
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [
                    "Phase 43 formal draft reviewed/caveat_only preparation audit passed.",
                    "Item remains within kt.ai_engineering.external_project_memory.* and does not store external project private memory.",
                    "Item is usable as reviewed/caveat_only reference only, not approved/default guidance/hard gate.",
                ],
                "required_followups": [
                    "Keep default_guidance_allowed=false and visible_in_default_guidance_queue=false.",
                    "Run MCP/SearchLab/KnowledgeTree linkage validation after conversion.",
                ],
            }
        )
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_audit",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "phase": "43",
        "task_id": TASK_ID,
        "decision": "conditional_accept_for_formal_reviewed_caveat_only_preparation",
        "summary": {
            "total": len(items),
            "accepted_for_reviewed_caveat_only": len(items),
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
            "reviewed_allowed": len(items),
            "approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "node_counts": dict(sorted(node_counts.items())),
        "hard_boundaries": {
            "create_approved": False,
            "create_default_guidance_allow": False,
            "enable_hard_gate": False,
            "store_external_project_private_memory": False,
            "create_real_database": False,
            "execute_migration": False,
            "enable_memory_vendor": False,
            "change_mcp_or_api_write_permissions": False,
            "generate_trading_execution_advice": False,
        },
        "required_formal_defaults": {
            "target_review_status": "reviewed",
            "review_mode": "caveat_only",
            "machine_gate.default_guidance": "caveat_only",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        },
        "knowledge_results": knowledge_results,
    }


def replace_text(value: str) -> str:
    replacements = {
        "Phase 43 formal draft only；用于外接项目 AI Memory Layer 契约审计。不得保存外接项目私有记忆，不得进入 reviewed/approved/default guidance/hard gate。": (
            "Phase 43 formal reviewed/caveat_only 知识；用于外接项目 AI Memory Layer 契约审计。不得保存外接项目私有记忆，不得进入 approved/default guidance/hard gate。"
        ),
        "Phase 43 formal draft only；尚未 reviewed/approved，不得作为默认指导或 hard gate。": (
            "Phase 43 formal reviewed/caveat_only；不是 approved，不得作为默认指导或 hard gate。"
        ),
        "review.review_status 必须保持 draft，直到单独 reviewed/caveat_only 审计通过。": (
            "review.review_status 必须为 reviewed，review_mode 必须为 caveat_only；approved/default guidance/hard gate 仍需单独人工治理。"
        ),
        "machine_gate.default_guidance 必须为 deny。": "machine_gate.default_guidance 必须为 caveat_only，且 default_guidance_allowed 必须为 false。",
        "必须同时返回 review_status=draft、machine_gate=deny、source_evidence 和适用边界。": (
            "必须同时返回 review_status=reviewed、review_mode=caveat_only、machine_gate=caveat_only、source_evidence 和适用边界。"
        ),
        "不得把 draft 当作 reviewed、approved 或默认指导。": "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
        "不得把 candidate 当作 reviewed/approved 默认指导。": "不得把 reviewed/caveat_only 当作 approved 默认指导。",
        "本条是 formal draft，不是 reviewed/approved。": "本条是 formal reviewed/caveat_only，不是 approved。",
        "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充实例。": (
            "本条已通过 reviewed/caveat_only 准备审计；后续 approved/default guidance/hard gate 仍需单独人工治理。"
        ),
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def patch_text_tree(value: Any) -> Any:
    if isinstance(value, str):
        return replace_text(value)
    if isinstance(value, list):
        return [patch_text_tree(item) for item in value]
    if isinstance(value, dict):
        return {key: patch_text_tree(item) for key, item in value.items()}
    return value


def promote_item(item: dict[str, Any]) -> dict[str, Any]:
    item = patch_text_tree(item)
    review = item.setdefault("review", {})
    review.update(
        {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "confidence": review.get("confidence", "medium"),
            "freshness": review.get("freshness", "time_sensitive"),
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approval_status": "not_requested",
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        }
    )
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "auditor": "external_ai_audit",
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": [
            "Phase 43 formal draft reviewed/caveat_only preparation audit passed for this item.",
            "Formal reviewed knowledge remains caveat_only and cannot become approved/default guidance/hard gate without separate governance.",
        ],
    }
    machine_gate = item.setdefault("machine_gate", {})
    machine_gate.update(
        {
            "default_guidance": "caveat_only",
            "reason": (
                "CEK-TA-368 按 Phase 43 formal draft reviewed-preparation 审计结果沉淀为 "
                "formal reviewed/caveat_only；不可作为 approved 默认指导或 hard gate。"
            ),
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_disabled_until_human_approval",
                "hard_gate_disabled",
                "external_project_private_memory_not_allowed",
                "production_memory_store_changes_require_separate_task",
            ],
            "checked_at": TODAY,
        "gate_version": "1.0.0",
        }
    )
    conflict = item.setdefault("conflict_audit", {})
    conflict.update(
        {
            "conflict_status": conflict.get("conflict_status", "none"),
            "resolution_summary": (
                "Phase 43 reviewed/caveat_only conversion passed; formal reviewed knowledge is searchable and citable, "
                "but not approved, not default guidance, not hard gate, and not external project private memory."
            ),
            "default_recommendation": "caveat_only_until_human_approval",
        }
    )
    source_quality = item.setdefault("source_quality", {})
    limitations = source_quality.get("limitations")
    if not isinstance(limitations, list):
        limitations = []
    caveat = "Phase 43 formal reviewed/caveat_only；不是 approved，不得作为默认指导或 hard gate。"
    if caveat not in limitations:
        limitations.append(caveat)
    source_quality["limitations"] = [
        replace_text(str(entry)) if isinstance(entry, str) else entry
        for entry in limitations
        if "formal draft only" not in str(entry)
    ]
    content = item.setdefault("content", {})
    risk_notes = content.get("risk_notes")
    if isinstance(risk_notes, list):
        extra = "本条为 formal reviewed/caveat_only，不是 approved；不得进入默认指导或 hard gate。"
        if extra not in risk_notes:
            risk_notes.append(extra)
    llm_usage = item.setdefault("llm_usage_policy", {})
    not_allowed = llm_usage.get("not_allowed")
    if isinstance(not_allowed, list):
        extra = "不得把 reviewed/caveat_only 当作 approved、default guidance 或 hard gate。"
        if extra not in not_allowed:
            not_allowed.append(extra)
    item["updated_at"] = TODAY
    history = item.setdefault("version_history", [])
    if isinstance(history, list):
        history.append(
            {
                "version": "v1",
                "created_at": TODAY,
                "actor": "codex",
                "change": "Promoted Phase 43 formal draft to formal reviewed/caveat_only after external audit.",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
    item["phase43_conversion"] = {
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": PACKAGE_ID,
        "review_status": "reviewed",
        "review_mode": "caveat_only",
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "external_project_private_memory_allowed": False,
        "production_database_changes_allowed": False,
        "vendor_activation_allowed": False,
        "trading_execution_allowed": False,
    }
    return item


def load_candidates_by_id() -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("*.json")):
        candidate = read_json(path)
        candidate_id = str(candidate.get("candidate_id", ""))
        if candidate_id:
            result[candidate_id] = (path, candidate)
    return result


def update_candidate(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Formal reviewed/caveat_only created from Phase 43 reviewed preparation audit.",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item.get("knowledge_id"),
            "formal_review_status": "reviewed",
            "formal_review_mode": "caveat_only",
            "formal_knowledge_path": rel(knowledge_path),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "none",
        }
    )
    review = candidate.setdefault("review", {})
    ai_audit = review.setdefault("ai_audit", {})
    if isinstance(ai_audit, dict):
        ai_audit.update(
            {
                "audit_result_id": AUDIT_RESULT_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "formal_knowledge_id": item.get("knowledge_id"),
            }
        )
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "formal_reviewed_caveat_only_created",
                "reason": "Phase 43 formal draft reviewed preparation audit accepted this item.",
                "audit_result_id": AUDIT_RESULT_ID,
                "knowledge_id": item.get("knowledge_id"),
            }
        )
    return candidate


def main() -> int:
    items = phase43_knowledge_items()
    if len(items) != 29:
        raise ValueError(f"Expected 29 Phase 43 formal knowledge items, got {len(items)}.")
    audit_payload = audit_result_payload(items)
    write_json(AUDIT_RESULT_PATH, audit_payload)

    candidates = load_candidates_by_id()
    promoted: list[dict[str, Any]] = []
    skipped: Counter[str] = Counter()
    for path, item in items:
        review = item.get("review", {}) if isinstance(item.get("review"), dict) else {}
        if review.get("review_status") not in {"draft", "reviewed"}:
            skipped["unexpected_review_status"] += 1
            continue
        if review.get("approval_status") not in {"not_requested", None}:
            skipped["approval_status_not_allowed"] += 1
            continue
        source_candidate_id = str(review.get("source_candidate_id", ""))
        item = promote_item(item)
        write_json(path, item)
        candidate_path = None
        if source_candidate_id in candidates:
            candidate_path, candidate = candidates[source_candidate_id]
            candidate = update_candidate(candidate, item, path)
            write_json(candidate_path, candidate)
        promoted.append(
            {
                "knowledge_id": item.get("knowledge_id"),
                "knowledge_path": rel(path),
                "source_candidate_id": source_candidate_id,
                "candidate_path": rel(candidate_path) if candidate_path else None,
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )

    report = {
        "report_id": "phase43_formal_draft_reviewed_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "input_package_id": PACKAGE_ID,
        "promoted_count": len(promoted),
        "skipped": dict(skipped),
        "promoted": promoted,
        "boundary": (
            "formal reviewed/caveat_only only; no approved/default guidance/hard gate; "
            "no external project private memory, database migration, or vendor activation."
        ),
        "next_action": "Run Phase 43 MCP/SearchLab/KnowledgeTree linkage validation.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == 29 and not skipped else 1


if __name__ == "__main__":
    raise SystemExit(main())
