"""Apply Phase 40 Batch D/E supplemental reaudit and write reviewed knowledge.

The external supplemental reaudit accepted five Phase 40 Batch D/E candidates
for formal reviewed preparation. This script records the audit result, writes
formal reviewed KnowledgeItem v1.1 files, and keeps approved/default-guidance/
hard-gate disabled.
"""

from __future__ import annotations

import json
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
import apply_phase40_supplemental_reaudit_result as base  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-314"
AUDIT_RESULT_ID = "audit_result_phase40_extended_p1_supplemental_reaudit_20260610_strict_v2"
SOURCE_PACKAGE_ID = "phase40_extended_p1_supplemental_reaudit_package_20260610"

AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_extended_p1_supplemental_reaudit_to_reviewed_report.json", start_file=__file__
)

ACCEPTED_TASKS = ["P40-E06", "P40-E07", "P40-E11", "P40-E12", "P40-P05"]

REVIEW_PATCHES: dict[str, dict[str, Any]] = {
    "P40-E06": {
        "reason": "补证已覆盖 false allow/block、calibration、人审压力、execution_cost_ref；二审允许进入 formal reviewed preparation。",
        "required_followups": [
            "formal reviewed 内容必须固定 champion_challenger_risk_metric_set_version。",
            "false_allow_rate、false_block_rate、false_allow_cost_ref、false_block_cost_ref 必须可追踪。",
            "calibration metrics 至少覆盖 Brier、ECE 或 reliability curve。",
            "execution_cost_ref 必须是 Phase 37 或外接项目引用，不在 AI Engineering 定义交易成本本体。",
            "insufficient_data_policy 必须降级为 warn_only 或 human_review。",
        ],
    },
    "P40-E07": {
        "reason": "shadow、paper、replay 的非实盘等价边界已补足；二审允许进入 formal reviewed preparation。",
        "required_followups": [
            "shadow_result_gap 必须声明只比较候选输出，不改变真实交易决策。",
            "paper/replay 必须记录 fill_cost_assumption_ref、replay_engine_version、market_data_replay_policy_ref、latency_assumption_ref 和 execution_gap_report。",
            "paper/replay 结果必须带 non_equivalence_caveat_required=true。",
            "fill/cost/latency 假设本体必须路由 Trading Engineering。",
        ],
    },
    "P40-E11": {
        "reason": "faithfulness、grounding 和 citation 来源足够支撑 confidence 不能替代 evidence；二审允许进入 formal reviewed preparation。",
        "required_followups": [
            "必须记录 source_evidence_refs、citation_resolver_version、citation_resolution_status 和 unsupported_claims。",
            "grounding_status 必须区分 grounded、partially_grounded、unsupported、no_source。",
            "no_source_abstain_policy 必须降级为 neutral、abstain 或 human_review。",
            "model_confidence 只能作为风险信号，不能替代来源证据或默认指导。",
        ],
    },
    "P40-E12": {
        "reason": "dashboard 分面和 decision-cost contract 已补足；二审允许进入 formal reviewed preparation。",
        "required_followups": [
            "continuous_learning_dashboard_metric_schema_version 必须固定为 v1 或后续显式迁移版本。",
            "看板必须分面展示 drift、calibration、decision_cost、false_allow_block、human_review_load_cost、release_rollback_status 和 insufficient_data。",
            "allowed_next_actions 只能是 investigate、collect_more_evidence、retraining_review、release_freeze 或 rollback_review。",
            "forbidden_next_actions 必须包含 auto_retrain、auto_promote、auto_hard_gate、auto_trade。",
        ],
    },
    "P40-P05": {
        "reason": "组合发布与组合回滚契约已补足；二审允许进入 formal reviewed preparation。",
        "required_followups": [
            "CompositeReleaseUnit 必须记录 numeric_model_version、calibrator_version、prompt_version、rag_index_version、threshold_policy_version、final_gate_policy_version、code_version_hash、dataset_hash 和 approval_ref。",
            "CompositeRollbackTarget 必须记录每个组件的目标版本、rollback_reason 和 owner_approval_ref。",
            "partial_rollback_forbidden 必须为 true，禁止只回滚模型而保留事故版本 prompt、RAG 或 threshold。",
            "threshold/final-gate rollback 必须由 deterministic final-gate owner 审批。",
        ],
    },
}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def build_audit_result(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    decisions = []
    for candidate in candidates:
        task_id = str(candidate.get("research_task_id"))
        patch = REVIEW_PATCHES[task_id]
        decisions.append(
            {
                "candidate_id": candidate.get("candidate_id"),
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
                    "只允许后续生成 formal reviewed knowledge，不得直接 approved。",
                    "default_guidance_allowed=false；hard_gate_allowed=false。",
                    "Trading Engineering 本体必须保持引用边界。",
                ],
                "conflict_patch_notes": [
                    "二审未发现 misrouted_to_trading；AI Engineering 只保留引用字段和治理规则。"
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
            "accepted_count": len(decisions),
            "needs_more_evidence_count": 0,
            "rejected_count": 0,
            "misrouted_to_trading_count": 0,
            "reviewed_allowed_count": len(decisions),
            "approved_allowed_count": 0,
            "default_guidance_allowed_count": 0,
            "hard_gate_allowed_count": 0,
        },
        "boundary": "reviewed_allowed=true only authorizes Codex to write formal reviewed knowledge; it is not approved/default guidance.",
    }


def main() -> int:
    base.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    base.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID
    base.AUDIT_TASK_ID = TASK_ID
    base.ACCEPTED_TASKS = ACCEPTED_TASKS
    base.REVIEW_PATCHES = REVIEW_PATCHES
    base.AUDIT_RESULT_PATH = AUDIT_RESULT_PATH
    base.REPORT_PATH = REPORT_PATH
    base.build_audit_result = build_audit_result

    promoted: list[dict[str, Any]] = []
    skipped = Counter()
    touched_candidates: list[str] = []
    accepted_candidates: list[dict[str, Any]] = []

    for candidate_path, candidate in base.load_candidates():
        reason = base.validate_candidate(candidate)
        if reason:
            skipped[reason] += 1
            continue
        task_id = str(candidate["research_task_id"])
        item = base.candidate_to_knowledge(candidate, REVIEW_PATCHES[task_id])
        knowledge_path = base.write_knowledge(item)
        base.update_candidate(candidate, item, knowledge_path)
        base.write_json(candidate_path, candidate)
        touched_candidates.append(base.rel(candidate_path))
        accepted_candidates.append(candidate)
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": task_id,
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": base.rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )

    if len(promoted) != len(ACCEPTED_TASKS):
        raise ValueError(f"Expected {len(ACCEPTED_TASKS)} promotions, got {len(promoted)}; skipped={dict(skipped)}")

    audit_result = build_audit_result(accepted_candidates)
    write_json(AUDIT_RESULT_PATH, audit_result)

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase40_extended_p1_supplemental_reaudit_to_reviewed_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "promoted_count": len(promoted),
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
