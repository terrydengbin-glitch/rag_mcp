"""Export P41-A06 reviewed/caveat_only preparation audit package.

This script is intentionally non-promotional. P41-A06 has passed the third
audit only as accepted_for_draft. The next valid step is to ask for explicit
reviewed/caveat_only permission before creating any formal knowledge item.
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
TASK_ID = "CEK-TA-339"
CANDIDATE_ID = "cand_20260610_phase41_p41_a06_baseline_001"
RESEARCH_TASK_ID = "P41-A06"
PACKAGE_ID = "phase41_a06_reviewed_preparation_audit_package_20260611"
TARGET_KNOWLEDGE_ID = "kb_ai_hybrid_scoring.phase41.ensemble_after_single_model_baseline_insufficient.v1"
TARGET_NORMALIZED_CLAIM = "phase41.ensemble_after_single_model_baseline_insufficient.v1"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
FORMAL_INDEX_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "indexes",
    "knowledge_items.json",
    start_file=__file__,
)
PACKAGE_PATH = resolve_repo_path(
    "docs",
    "audit",
    f"{PACKAGE_ID}.json",
    start_file=__file__,
)
REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase41_a06_reviewed_preparation_gap_report.json",
    start_file=__file__,
)


def read_json(path: Path) -> dict[str, Any] | list[Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def source_count(candidate: dict[str, Any]) -> int:
    return len(as_list(candidate.get("source_refs")))


def source_ids(candidate: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for item in as_list(candidate.get("source_refs")):
        if isinstance(item, dict) and isinstance(item.get("source_id"), str):
            ids.append(item["source_id"])
    return ids


def formal_index_has_target() -> bool:
    if not FORMAL_INDEX_PATH.exists():
        return False
    payload = read_json(FORMAL_INDEX_PATH)
    if isinstance(payload, dict):
        items = payload.get("items")
    else:
        items = payload
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain an items array")
    for item in items:
        if isinstance(item, dict) and item.get("knowledge_id") == TARGET_KNOWLEDGE_ID:
            return True
    return False


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    status = as_dict(candidate.get("status"))
    workflow = as_dict(candidate.get("workflow"))
    conversion = as_dict(candidate.get("conversion_target"))
    claim = as_dict(candidate.get("claim"))
    machine_gate = as_dict(candidate.get("machine_gate"))

    if candidate.get("candidate_id") != CANDIDATE_ID:
        errors.append("candidate_id 不匹配。")
    if candidate.get("research_task_id") != RESEARCH_TASK_ID:
        errors.append("research_task_id 不匹配。")
    if status.get("ingestion_decision") != "accepted_for_draft":
        errors.append("候选必须先处于 accepted_for_draft。")
    if status.get("review_status") != "accepted":
        errors.append("候选 review_status 必须是 accepted。")
    if workflow.get("formal_knowledge_id") != TARGET_KNOWLEDGE_ID:
        errors.append("workflow.formal_knowledge_id 与目标知识 ID 不一致。")
    if conversion.get("proposed_knowledge_id") != TARGET_KNOWLEDGE_ID:
        errors.append("conversion_target.proposed_knowledge_id 与目标知识 ID 不一致。")
    if claim.get("normalized_claim") != TARGET_NORMALIZED_CLAIM:
        errors.append("claim.normalized_claim 与三审修复后的 slug 不一致。")
    if source_count(candidate) < 5:
        errors.append("来源数量不足，不能请求 reviewed/caveat_only。")
    if machine_gate.get("default_guidance") not in {"deny", "caveat_only"}:
        errors.append("machine_gate.default_guidance 必须保持 deny 或 caveat_only。")
    if formal_index_has_target():
        errors.append("正式 knowledge_items.json 已存在目标知识 ID，本任务不能重复创建正式知识。")
    return errors


def build_candidate_view(candidate: dict[str, Any]) -> dict[str, Any]:
    status = as_dict(candidate.get("status"))
    workflow = as_dict(candidate.get("workflow"))
    conversion = as_dict(candidate.get("conversion_target"))
    review = as_dict(candidate.get("review"))
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "current_status": {
            "review_status": status.get("review_status"),
            "ingestion_decision": status.get("ingestion_decision"),
            "decision_reason": status.get("decision_reason"),
            "workflow_stage": workflow.get("stage"),
            "queue_group": workflow.get("queue_group"),
            "formal_review_status": workflow.get("formal_review_status"),
        },
        "conversion_target": {
            "proposed_knowledge_id": conversion.get("proposed_knowledge_id"),
            "formal_knowledge_id": workflow.get("formal_knowledge_id"),
            "target_review_status_requested": "reviewed",
            "machine_gate_requested": "caveat_only",
        },
        "classification": candidate.get("classification"),
        "claim": candidate.get("claim"),
        "applicability": candidate.get("applicability"),
        "llm_usage_policy": candidate.get("llm_usage_policy"),
        "source_refs": candidate.get("source_refs"),
        "source_summary": {
            "source_count": source_count(candidate),
            "source_ids": source_ids(candidate),
        },
        "conflict_audit": candidate.get("conflict_audit"),
        "machine_gate": candidate.get("machine_gate"),
        "review_snapshot": {
            "reviewed_allowed": review.get("reviewed_allowed", False),
            "approved_allowed": review.get("approved_allowed", False),
            "default_guidance_allowed": review.get("default_guidance_allowed", False),
            "hard_gate_allowed": review.get("hard_gate_allowed", False),
            "open_questions": review.get("open_questions", []),
        },
    }


def build_package(candidate: dict[str, Any], validation_errors: list[str]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "task_id": TASK_ID,
        "created_at": TODAY,
        "purpose": "请求外部 AI/人工审计确认 P41-A06 是否可以从 accepted_for_draft 进入 formal reviewed/caveat_only。不得授权 approved、default guidance 或 hard gate。",
        "source_candidate_path": repo_rel(CANDIDATE_PATH),
        "target_knowledge_id": TARGET_KNOWLEDGE_ID,
        "hard_boundaries": {
            "create_formal_knowledge_in_this_package": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trading_execution_allowed": False,
            "qwen_as_numeric_scorer_allowed": False,
            "ensemble_as_final_gate_allowed": False,
        },
        "allowed_audit_decisions": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
        ],
        "decision_semantics": {
            "accepted_for_reviewed_caveat_only": "允许 Codex 后续另起任务创建 formal knowledge，review.review_status=reviewed，machine_gate.default_guidance=caveat_only；仍不得 approved/default/hard gate。",
            "needs_more_evidence": "仍需补充来源、边界、冲突或契约，不得创建 formal knowledge。",
            "rejected": "不应继续作为 Phase 41 reviewed 候选。",
        },
        "audit_questions": [
            "single-model baseline comparison 是否足以支持 ensemble 只能作为增强候选，而非默认优先模型？",
            "auditability impact report 是否覆盖模型版本、校准器、threshold policy、trace、解释边界和回滚目标？",
            "该知识是否只属于 AI Engineering / numeric scoring / model family selection，不混入 K 线、fill model、仓位或实盘风控本体？",
            "来源是否足以支撑 reviewed/caveat_only，而不是 approved/default guidance/hard gate？",
            "是否仍保持 ensemble 输出只能作为 scorer signal 或 review-priority signal？",
        ],
        "expected_output_schema": {
            "candidate_id": "string",
            "research_task_id": "string",
            "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected",
            "reviewed_allowed": "boolean",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "reason": "string",
            "source_patch_notes": ["string"],
            "content_patch_notes": ["string"],
            "boundary_patch_notes": ["string"],
            "conflict_patch_notes": ["string"],
            "required_followups": ["string"],
        },
        "preflight_validation": {
            "passed": len(validation_errors) == 0,
            "errors": validation_errors,
        },
        "candidates": [build_candidate_view(candidate)],
    }


def build_report(candidate: dict[str, Any], validation_errors: list[str]) -> dict[str, Any]:
    return {
        "task_id": TASK_ID,
        "created_at": TODAY,
        "candidate_id": CANDIDATE_ID,
        "target_knowledge_id": TARGET_KNOWLEDGE_ID,
        "formal_index_has_target": formal_index_has_target(),
        "candidate_ingestion_decision": as_dict(candidate.get("status")).get("ingestion_decision"),
        "candidate_queue_group": as_dict(candidate.get("workflow")).get("queue_group"),
        "source_count": source_count(candidate),
        "validation_passed": len(validation_errors) == 0,
        "validation_errors": validation_errors,
        "next_action": (
            "将 docs/audit/phase41_a06_reviewed_preparation_audit_package_20260611.json 交给外部 AI/人工复审；"
            "只有返回 reviewed_allowed=true 且仍保持 approved/default/hard=false 后，才能另起任务创建 formal reviewed/caveat_only。"
        ),
        "deliverables": {
            "audit_package": repo_rel(PACKAGE_PATH),
            "gap_report": repo_rel(REPORT_PATH),
            "source_candidate": repo_rel(CANDIDATE_PATH),
        },
    }


def main() -> int:
    candidate_payload = read_json(CANDIDATE_PATH)
    if not isinstance(candidate_payload, dict):
        raise ValueError("Candidate file must contain a JSON object")

    validation_errors = validate_candidate(candidate_payload)
    package = build_package(candidate_payload, validation_errors)
    report = build_report(candidate_payload, validation_errors)
    write_json(PACKAGE_PATH, package)
    write_json(REPORT_PATH, report)

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not validation_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
