"""Apply Phase 40 reviewed-preparation supplemental third audit result.

This imports the CEK-TA-328 result for five Phase 40 candidates that were
supplemented by CEK-TA-317. The output is formal reviewed knowledge with
caveat_only machine gates. Nothing is approved, default-guidance enabled, or
hard-gate enabled by this script.
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
import apply_phase40_supplemental_reaudit_result as base  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-328"
AUDIT_RESULT_ID = "audit_result_phase40_reviewed_preparation_supplemental_reaudit_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase40_reviewed_preparation_supplemental_reaudit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_reviewed_preparation_supplemental_reaudit_import_report.json", start_file=__file__
)


REVIEW_PATCHES: dict[str, dict[str, Any]] = {
    "P40-C01": {
        "candidate_id": "cand_20260610_phase40_p40_c01_allow_block_skip_human_review_001",
        "reason": "logged bandit / OPE / FeedbackRecord contract 已补足，可支撑 allow、block、skip、human_review 和 error 全候选记录。",
        "required_followups": [
            "保留 candidate_id、decision_time、action_taken、final_gate_decision、policy_version、outcome_ref、counterfactual_status。",
            "log_every_candidate != execute_every_candidate。",
            "blocked/skipped outcome 不是直接可观测事实，不得把反事实 opportunity 写成真实 PnL。",
        ],
    },
    "P40-C02": {
        "candidate_id": "cand_20260610_phase40_p40_c02_feedback_record_scorer_llm_final_gate_001",
        "reason": "point-in-time / decision-time feature 来源已补足，可支撑 FeedbackRecord 同链路保存 scorer、LLM、final gate 和 outcome refs。",
        "required_followups": [
            "固定 decision_time_feature_frame_ref、feature_available_time_policy、numeric_scorer_output_ref、llm_audit_output_ref、deterministic_final_gate_decision_ref。",
            "post-trade outcome 只能作为观察窗口后的结果引用，不得混入 scorer 或 final gate 的 decision-time input。",
            "LLM audit output 只是审计辅助；final_gate_decision 必须来自 deterministic final gate。",
        ],
    },
    "P40-C07": {
        "candidate_id": "cand_20260610_phase40_p40_c07_feature_drift_label_drift_score_distribution_drift_calibration_drift_001",
        "reason": "calibration curve / reliability diagram 来源已补足，可支撑 calibration drift 独立监控。",
        "required_followups": [
            "formal reviewed 内容必须拆分 feature_drift、label_or_target_drift、score_distribution_drift、calibration_drift。",
            "calibration drift 至少记录 reference_window、current_window、minimum_slice_n、Brier/ECE 或 calibration curve / reliability diagram 证据。",
            "drift alert 只能触发 investigation / review / collect_more_evidence / retraining_review，不能作为 hard gate、自动再训练命令或实盘交易动作。",
        ],
    },
    "P40-C12": {
        "candidate_id": "cand_20260610_phase40_p40_c12_threshold_policy_001",
        "reason": "cost-sensitive threshold、human review budget、queue capacity 和 owner approval contract 已补足。",
        "required_followups": [
            "threshold policy 必须绑定 threshold_policy_version、cost_matrix_version、calibrator_version、review_budget_policy_ref、review_queue_capacity_snapshot_ref、owner_approval_ref。",
            "review budget 或 queue capacity 超限时只能进入 freeze_threshold_change、safe_mode、owner_review 或 collect_more_evidence。",
            "review budget 超限不能自动 allow 或自动 block；threshold policy 不是 final gate policy。",
        ],
    },
    "P40-C15": {
        "candidate_id": "cand_20260610_phase40_p40_c15_release_manifest_rollback_target_kill_switch_001",
        "reason": "release manifest、rollback、kill switch、secret scan、rollback drill 和 human approval 证据已补足。",
        "required_followups": [
            "release manifest 必须记录 release_manifest_id、rollback_target、kill_switch_policy_ref、secret_scan_status、rollback_drill_status、kill_switch_tested_at、human_approval_record_ref。",
            "缺任一关键控制必须 block_release。",
            "release manifest 不得包含私有策略正文、账号密钥或交易执行规则本体；kill switch 具体实现归 Trading Engineering 或外接项目 owner。",
        ],
    },
}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def load_candidate(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_candidate(candidate: dict[str, Any], patch: dict[str, Any]) -> str | None:
    if candidate.get("candidate_id") != patch["candidate_id"]:
        return "candidate_id_mismatch"
    if str(candidate.get("research_task_id")) not in REVIEW_PATCHES:
        return "not_in_scope"
    if base.deep_get(candidate, ("workflow", "queue_group")) != "needs_more_evidence":
        return "not_needs_more_evidence_queue"
    if base.deep_get(candidate, ("status", "ingestion_decision")) != "ready_for_reaudit":
        return "not_ready_for_reaudit"
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


def build_audit_result(promoted_candidates: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = []
    for candidate in promoted_candidates:
        task_id = str(candidate["research_task_id"])
        patch = REVIEW_PATCHES[task_id]
        decisions.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": task_id,
                "decision": "accepted_for_draft",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reason": patch["reason"],
                "source_patch_notes": [],
                "content_patch_notes": patch["required_followups"],
                "boundary_patch_notes": [
                    "reviewed_allowed=true 只表示允许 Codex 生成 formal reviewed draft。",
                    "不得解释为已经 approved、可进入 default guidance 或可用于 hard gate。",
                    "Trading Engineering 的 K 线、fill model、订单状态机、实盘风控和交易执行本体不得混入 AI Engineering。",
                ],
                "conflict_patch_notes": [
                    "未发现 misrouted_to_trading；AI Engineering 只记录引用、发布门禁和审计证据。"
                ],
                "required_followups": patch["required_followups"],
            }
        )
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "decision": "conditional_accept_for_formal_reviewed_preparation",
        "decisions": decisions,
        "batch_summary": {
            "accepted_for_draft_count": len(decisions),
            "reviewed_allowed_count": len(decisions),
            "needs_more_evidence_count": 0,
            "rejected_count": 0,
            "approved_allowed_count": 0,
            "default_guidance_allowed_count": 0,
            "hard_gate_allowed_count": 0,
            "misrouted_to_trading_count": 0,
        },
        "boundary": "5 candidates may become formal reviewed + caveat_only; none may become approved/default guidance/hard gate.",
    }


def apply_audit_notes(item: dict[str, Any], patch: dict[str, Any]) -> None:
    item.setdefault("metadata", {})["classification_notes"] = (
        "Phase 40 formal reviewed knowledge；三审允许 reviewed，但不是 approved/default guidance/hard gate。"
    )
    item.setdefault("machine_gate", {})["reason"] = (
        "Phase 40 三审允许转 formal reviewed；可审计检索，但尚未人工 approved，不能默认指导或 hard gate。"
    )
    review = item.setdefault("review", {})
    review["ai_audit_result_id"] = AUDIT_RESULT_ID
    review["default_guidance_allowed"] = False
    review["approval_status"] = "not_requested"
    review["open_questions"] = patch["required_followups"]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_draft",
        "reviewed_allowed": True,
        "allowed_next_stage": "formal_reviewed_knowledge",
        "reason": patch["reason"],
        "source_patch_notes": [],
        "content_patch_notes": patch["required_followups"],
        "boundary_patch_notes": [
            "reviewed 不等于 approved。",
            "default_guidance_allowed=false。",
            "hard_gate_allowed=false。",
        ],
        "default_guidance_allowed": False,
        "approved_allowed": False,
        "hard_gate_allowed": False,
    }
    item.setdefault("phase40_conversion", {})["promoted_by_task"] = TASK_ID
    item.setdefault("phase40_conversion", {})["reviewed_allowed"] = True
    item.setdefault("phase40_conversion", {})["approved_allowed"] = False


def update_candidate_after_base(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, patch: dict[str, Any]) -> None:
    candidate.setdefault("status", {})["decision_reason"] = (
        "三审 accepted_for_draft 且 reviewed_allowed=true；已生成 formal reviewed knowledge。"
    )
    candidate.setdefault("status", {})["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval",
            "default_guidance_allowed": False,
            "knowledge_path": rel(knowledge_path),
        }
    )
    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": "accepted_for_draft",
        "reason": patch["reason"],
        "content_patch_notes": patch["required_followups"],
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "allowed_next_stage": "formal_reviewed_knowledge",
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase40_reviewed_preparation_supplemental_reaudit_formalized",
                "reason": f"{TASK_ID}: 三审通过，formal reviewed knowledge written to {rel(knowledge_path)}.",
            }
        )


def main() -> int:
    base.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    base.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID
    base.AUDIT_TASK_ID = TASK_ID
    base.AUDIT_RESULT_PATH = AUDIT_RESULT_PATH
    base.REPORT_PATH = REPORT_PATH

    promoted: list[dict[str, Any]] = []
    promoted_candidates: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    by_node = Counter()
    skipped = Counter()

    for task_id, patch in REVIEW_PATCHES.items():
        candidate_path = CANDIDATE_DIR / f"{patch['candidate_id']}.json"
        if not candidate_path.exists():
            skipped["missing_candidate"] += 1
            continue
        candidate = load_candidate(candidate_path)
        reason = validate_candidate(candidate, patch)
        if reason:
            skipped[reason] += 1
            continue
        item = base.candidate_to_knowledge(candidate, patch)
        apply_audit_notes(item, patch)
        knowledge_path = base.write_knowledge(item)
        base.update_candidate(candidate, item, knowledge_path)
        update_candidate_after_base(candidate, item, knowledge_path, patch)
        write_json(candidate_path, candidate)
        touched_candidates.append(rel(candidate_path))
        promoted_candidates.append(candidate)
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": task_id,
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )
        by_node[item["metadata"]["canonical_node_id"]] += 1

    if len(promoted) != len(REVIEW_PATCHES):
        raise ValueError(f"Expected {len(REVIEW_PATCHES)} promotions, got {len(promoted)}; skipped={dict(skipped)}")

    audit_result = build_audit_result(promoted_candidates)
    write_json(AUDIT_RESULT_PATH, audit_result)

    report = {
        "report_id": "phase40_reviewed_preparation_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "promoted_count": len(promoted),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_count": 0,
        "default_guidance_allowed_count": 0,
        "hard_gate_allowed_count": 0,
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
