"""Apply Phase 41 P41-A06 third-audit result.

The third audit allows P41-A06 to move from needs_more_evidence to
accepted_for_draft only. It must not create formal reviewed knowledge and must
not enable approved, default guidance, or hard gate.
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
TASK_ID = "CEK-TA-338"
CANDIDATE_ID = "cand_20260610_phase41_p41_a06_baseline_001"
RESEARCH_TASK_ID = "P41-A06"
SOURCE_PACKAGE_ID = "phase41_a06_single_model_baseline_third_audit_package_20260611"
AUDIT_RESULT_ID = "audit_result_phase41_a06_single_model_baseline_third_audit_20260611_strict_v3"
NORMALIZED_CLAIM = "phase41.ensemble_after_single_model_baseline_insufficient.v1"
PROPOSED_KNOWLEDGE_ID = "kb_ai_hybrid_scoring.phase41.ensemble_after_single_model_baseline_insufficient.v1"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs",
    "audit",
    "audit_result_phase41_a06_single_model_baseline_third_audit_20260611_strict_v3.json",
    start_file=__file__,
)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase41_a06_third_audit_import_report.json",
    start_file=__file__,
)


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


def build_audit_result() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "generated_at": TODAY,
        "auditor": "external_ai_audit",
        "task_id": TASK_ID,
        "phase": "41",
        "decision_scope": "candidate_state_only",
        "candidate_count": 1,
        "results": [
            {
                "candidate_id": CANDIDATE_ID,
                "research_task_id": RESEARCH_TASK_ID,
                "decision": "accepted_for_draft",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reason": (
                    "P41-A06 已修复 metadata/slug 一致性，并补齐 single-model baseline comparison、"
                    "ensemble enhancement、ensemble validation complexity、auditability impact report、"
                    "final gate boundary 五个维度证据；可进入 accepted_for_draft。"
                ),
                "source_patch_notes": [
                    "保留补证后的 5 个证据维度。",
                    "formal draft 前去重 scikit-learn ensemble 相关 source_refs。"
                ],
                "content_patch_notes": [
                    "只能表述为：只有当单模型 baseline 不足，且 ensemble 不破坏可审计性时，ensemble 才能作为增强候选。",
                    "不得表述为 ensemble 默认优于单模型或应默认采用。"
                ],
                "boundary_patch_notes": [
                    "ensemble 输出只能作为 scorer signal 或 review-priority signal。",
                    "不得作为交易执行许可、买卖点、仓位建议、allow/block/reduce_size 或 deterministic final gate decision。",
                    "不得进入 reviewed、approved、default guidance 或 hard gate。"
                ],
                "conflict_patch_notes": [
                    "metadata/slug 已统一到 phase41.ensemble_after_single_model_baseline_insufficient.v1。",
                    "继续保持 candidate 到 formal reviewed 的后续人工/Codex 治理边界。"
                ],
                "required_followups": [
                    "prepare_formal_reviewed_caveat_only_draft_in_next_task",
                    "run_phase41_final_runtime_validation_after_formalization"
                ],
            }
        ],
        "hard_boundaries": {
            "creates_formal_reviewed": False,
            "creates_approved": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }


def dedupe_sources(candidate: dict[str, Any]) -> dict[str, int]:
    refs = candidate.get("source_refs")
    if not isinstance(refs, list):
        return {"before": 0, "after": 0, "removed": 0}

    before = len(refs)
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        key = (str(ref.get("source_id") or ""), str(ref.get("source_url") or ""))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(ref)
    candidate["source_refs"] = deduped
    return {"before": before, "after": len(deduped), "removed": before - len(deduped)}


def apply_result(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError(f"Unexpected candidate_id: {candidate.get('candidate_id')}")
    if candidate.get("research_task_id") != RESEARCH_TASK_ID:
        raise ValueError(f"Unexpected research_task_id: {candidate.get('research_task_id')}")

    item = result["results"][0]
    if item["decision"] != "accepted_for_draft":
        raise ValueError("This importer only handles accepted_for_draft for P41-A06.")
    for field in ("reviewed_allowed", "approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
        if item.get(field) is not False:
            raise ValueError(f"Unsafe audit result: {field} must be false")

    dedupe_report = dedupe_sources(candidate)
    candidate["normalized_claim"] = NORMALIZED_CLAIM
    candidate.setdefault("claim", {})["normalized_claim"] = NORMALIZED_CLAIM
    candidate.setdefault("conversion_target", {})["proposed_knowledge_id"] = PROPOSED_KNOWLEDGE_ID
    candidate.setdefault("_audit_export_meta", {})["proposed_knowledge_id"] = PROPOSED_KNOWLEDGE_ID
    candidate["_audit_export_meta"]["normalized_claim"] = NORMALIZED_CLAIM
    candidate["_audit_export_meta"]["accepted_for_draft_at"] = TODAY

    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = item["reason"]
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["formal_knowledge_id"] = PROPOSED_KNOWLEDGE_ID
    workflow["formal_review_status"] = "draft"
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["next_action"] = "prepare_formal_reviewed_caveat_only_draft"
    workflow["default_guidance_allowed"] = False

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Candidate accepted_for_draft only; formal reviewed/default guidance/hard gate are not allowed by third audit."
    machine_gate["requires_human_escalation"] = True

    review = candidate.setdefault("review", {})
    review["review_status"] = "accepted_for_draft"
    review["reviewer"] = "external_ai_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["open_questions"] = [
        "prepare_formal_reviewed_caveat_only_draft_in_next_task",
        "do_not_enable_default_guidance",
        "do_not_enable_hard_gate",
    ]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": CANDIDATE_ID,
        "research_task_id": RESEARCH_TASK_ID,
        "decision": "accepted_for_draft",
        "reason": item["reason"],
        "source_patch_notes": item["source_patch_notes"],
        "content_patch_notes": item["content_patch_notes"],
        "boundary_patch_notes": item["boundary_patch_notes"],
        "conflict_patch_notes": item["conflict_patch_notes"],
        "required_followups": item["required_followups"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_a06_third_audit_accepted_for_draft_imported",
                "reason": "CEK-TA-338: 三审通过，只升级为 accepted_for_draft，不创建 reviewed/approved/default/hard gate。",
            }
        )

    trace = candidate.setdefault("phase41_trace", {})
    trace["third_audit_result"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "decision": "accepted_for_draft",
        "imported_at": TODAY,
        "source_dedupe": dedupe_report,
        "boundary": "accepted_for_draft only; not reviewed, approved, default guidance, or hard gate.",
    }

    return dedupe_report


def main() -> int:
    audit_result = build_audit_result()
    candidate = read_json(CANDIDATE_PATH)
    dedupe_report = apply_result(candidate, audit_result)

    write_json(AUDIT_RESULT_PATH, audit_result)
    write_json(CANDIDATE_PATH, candidate)

    report = {
        "report_id": "phase41_a06_third_audit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_id": CANDIDATE_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "decision": "accepted_for_draft",
        "candidate_path": repo_rel(CANDIDATE_PATH),
        "audit_result_path": repo_rel(AUDIT_RESULT_PATH),
        "source_dedupe": dedupe_report,
        "status": candidate.get("status"),
        "workflow": candidate.get("workflow"),
        "gate": {
            "formal_reviewed_created": False,
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "machine_gate_default_guidance": candidate.get("machine_gate", {}).get("default_guidance"),
        },
        "next_action": "后续另开任务将 accepted_for_draft 候选沉淀为 formal reviewed/caveat_only，并运行 Phase 41 全量联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
