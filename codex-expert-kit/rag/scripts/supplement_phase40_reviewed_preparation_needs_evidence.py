"""Supplement Phase 40 reviewed-preparation needs-more-evidence candidates.

This script updates only candidate audit artifacts and exports a third-review
package. It does not create formal reviewed knowledge, approved knowledge,
default guidance, or hard gates.
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


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-317"
AUDIT_RESULT_ID = "audit_result_phase40_ai_passed_reviewed_preparation_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase40_ai_passed_reviewed_preparation_audit_package_20260610"
REAUDIT_PACKAGE_ID = "phase40_reviewed_preparation_supplemental_reaudit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_reviewed_preparation_supplemental_evidence_report.json", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", f"{REAUDIT_PACKAGE_ID}.json", start_file=__file__
)


def source(
    source_id: str,
    title: str,
    url: str,
    source_type: str,
    publisher: str,
    score: int,
    relevance: str,
    summary: str,
    limitations: list[str] | None = None,
    published_at: str | None = None,
    reliability: str = "high",
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "source_title": title,
        "source_url": url,
        "source_type": source_type,
        "publisher": publisher,
        "published_at": published_at,
        "accessed_at": TODAY,
        "version": None,
        "reliability": reliability,
        "score": score,
        "relevance": relevance,
        "freshness": "time_sensitive" if source_type in {"official_doc", "governance_framework"} else "stable",
        "limitations": limitations or [],
        "evidence_summary": summary,
        "quoted_excerpt_allowed": False,
    }


SOURCE_LIBRARY: dict[str, dict[str, Any]] = {
    "src_vowpal_wabbit_contextual_bandit": source(
        "src_vowpal_wabbit_contextual_bandit",
        "Contextual Bandits - Vowpal Wabbit documentation",
        "https://vowpalwabbit.org/docs/vowpal_wabbit/python/latest/examples/contextual_bandit.html",
        "official_doc",
        "Vowpal Wabbit",
        86,
        "high",
        "Vowpal Wabbit contextual bandit examples use logged action, cost, probability and feature columns, supporting the need to retain chosen-action and logging-policy evidence.",
        ["支撑 logged bandit 字段结构，不直接定义交易执行或收益。"],
    ),
    "src_open_bandit_pipeline_docs": source(
        "src_open_bandit_pipeline_docs",
        "Open Bandit Pipeline documentation",
        "https://zr-obp.readthedocs.io/en/latest/",
        "official_doc",
        "Open Bandit Pipeline",
        84,
        "high",
        "Open Bandit Pipeline documents logged bandit feedback and off-policy evaluation for realistic and reproducible evaluation.",
        ["OPE 来源来自推荐/广告场景，交易执行质量仍需 Trading Engineering 引用。"],
    ),
    "src_doubly_robust_policy_evaluation": source(
        "src_doubly_robust_policy_evaluation",
        "Doubly Robust Policy Evaluation and Learning",
        "https://arxiv.org/abs/1103.4601",
        "paper",
        "arXiv",
        86,
        "high",
        "The paper frames contextual-bandit policy evaluation around historic data with contexts, actions, observed rewards, and a past policy.",
        ["支撑反事实/OPE 数据需求，不证明任何交易模型可盈利。"],
        published_at="2011-03-23",
    ),
    "src_feast_point_in_time_joins": source(
        "src_feast_point_in_time_joins",
        "Point-in-time joins - Feast documentation",
        "https://docs.feast.dev/getting-started/concepts/point-in-time-joins",
        "official_doc",
        "Feast",
        88,
        "high",
        "Feast documents point-in-time joins that reproduce feature state at a specific time in the past and help avoid future feature leakage.",
        ["支撑 feature availability，不定义交易标签或后验收益。"],
    ),
    "src_tecton_training_data": source(
        "src_tecton_training_data",
        "Construct Training Data - Tecton documentation",
        "https://docs.tecton.ai/docs/reading-feature-data/reading-feature-data-for-training/constructing-training-data",
        "official_doc",
        "Tecton",
        84,
        "medium",
        "Tecton training-data construction uses training events with keys and timestamps before requesting feature data.",
        ["支撑训练事件时间戳，不替代 CEK-TA FeedbackRecord 字段契约。"],
    ),
    "src_databricks_point_in_time": source(
        "src_databricks_point_in_time",
        "Point-in-time feature joins - Azure Databricks",
        "https://docs.azure.cn/en-us/databricks/machine-learning/feature-store/time-series",
        "official_doc",
        "Databricks",
        84,
        "medium",
        "Databricks documents point-in-time correctness to create training data that reflects feature values available when a label was observed.",
        ["支撑防 leakage 原则，不定义交易项目私有 schema。"],
    ),
    "src_sklearn_calibration": source(
        "src_sklearn_calibration",
        "Probability calibration - scikit-learn documentation",
        "https://scikit-learn.org/stable/modules/calibration.html",
        "official_doc",
        "scikit-learn",
        88,
        "high",
        "scikit-learn documents probability calibration for classifier probabilities and the need to improve poorly calibrated probability estimates.",
        ["支撑概率校准，不证明交易阈值或收益。"],
    ),
    "src_sklearn_calibration_curve_example": source(
        "src_sklearn_calibration_curve_example",
        "Probability Calibration curves - scikit-learn",
        "https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html",
        "official_doc",
        "scikit-learn",
        88,
        "high",
        "scikit-learn describes calibration curves, also known as reliability diagrams, for visualizing probability calibration.",
        ["支撑 calibration drift 度量，不定义漂移后的自动交易动作。"],
    ),
    "src_sklearn_calibration_display": source(
        "src_sklearn_calibration_display",
        "CalibrationDisplay - scikit-learn API reference",
        "https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibrationDisplay.html",
        "official_doc",
        "scikit-learn",
        86,
        "high",
        "CalibrationDisplay plots average predicted probability per bin against the fraction of positive classes.",
        ["API 文档来源，需结合 CEK-TA drift contract 解释交易 AI 动作边界。"],
    ),
    "src_aws_augmented_ai_human_review": source(
        "src_aws_augmented_ai_human_review",
        "Using Amazon Augmented AI for Human Review",
        "https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-use-augmented-ai-a2i-human-review-loops.html",
        "official_doc",
        "AWS",
        84,
        "medium",
        "Amazon A2I documents human review loops for ML applications, including low-confidence outputs and tabular data review.",
        ["支撑 human review loop，不定义交易阈值成本矩阵。"],
    ),
    "src_aws_augmented_ai_create_workflow": source(
        "src_aws_augmented_ai_create_workflow",
        "Create a Human Review Workflow - Amazon SageMaker AI",
        "https://docs.aws.amazon.com/sagemaker/latest/dg/a2i-create-flow-definition.html",
        "official_doc",
        "AWS",
        84,
        "medium",
        "Amazon A2I documents creating a human review workflow and configuring a private work team.",
        ["支撑工作流与 workforce 配置，不替代 CEK-TA review budget contract。"],
    ),
    "src_google_sre_canarying": source(
        "src_google_sre_canarying",
        "Canary Release: Deployment Safety and Efficiency",
        "https://sre.google/workbook/canarying-releases/",
        "official_doc",
        "Google SRE",
        88,
        "high",
        "Google SRE describes canarying as exposing changes to a small portion of traffic to reduce deployment risk before broader rollout.",
        ["软件发布来源，不定义交易 capital limit 或订单控制本体。"],
    ),
    "src_github_secret_scanning": source(
        "src_github_secret_scanning",
        "Secret scanning - GitHub Docs",
        "https://docs.github.com/code-security/secret-scanning/about-secret-scanning",
        "official_doc",
        "GitHub",
        86,
        "high",
        "GitHub secret scanning detects hardcoded credentials such as API keys, passwords and tokens in repository history and branches.",
        ["支撑发布前 secret scan，不允许在知识库保存密钥正文。"],
    ),
    "src_nist_ai_rmf_manage": source(
        "src_nist_ai_rmf_manage",
        "Manage - NIST AI RMF Playbook",
        "https://airc.nist.gov/airmf-resources/playbook/manage/",
        "governance_framework",
        "NIST",
        88,
        "high",
        "NIST AI RMF Manage covers post-deployment monitoring, override, decommissioning, incident response, recovery and change management.",
        ["治理框架来源，不替代项目级 release manifest。"],
    ),
    "src_fca_algo_trading_controls": source(
        "src_fca_algo_trading_controls",
        "Algorithmic Trading Compliance in Wholesale Markets",
        "https://www.fca.org.uk/publication/multi-firm-reviews/algorithmic-trading-compliance-wholesale-markets.pdf",
        "governance_framework",
        "FCA",
        86,
        "medium",
        "FCA algorithmic trading review discusses risk controls including kill functionality, control inventories, testing and governance.",
        ["监管来源用于 kill functionality 边界，不定义本项目交易执行实现。"],
        published_at="2018-02-12",
    ),
    "src_cek_ta_phase40_feedback_dataset_contract": source(
        "src_cek_ta_phase40_feedback_dataset_contract",
        "CEK-TA Phase 40 Feedback Dataset Contract",
        "docs/contracts/phase40_feedback_dataset_contract.md",
        "internal_contract",
        "CEK-TA",
        90,
        "high",
        "Defines FeedbackRecord fields and requires allow, block, skip, human_review and error candidates to be logged.",
        ["内部契约定义 CEK-TA 字段，需要外部专业来源共同支撑。"],
        published_at=TODAY,
    ),
    "src_cek_ta_phase40_drift_retraining_contract": source(
        "src_cek_ta_phase40_drift_retraining_contract",
        "CEK-TA Phase 40 Drift Retraining Recalibration Contract",
        "docs/contracts/phase40_drift_retraining_recalibration_contract.md",
        "internal_contract",
        "CEK-TA",
        90,
        "high",
        "Defines DriftReport, RecalibrationReport and ThresholdStabilityReport, including calibration drift and threshold pressure.",
        ["内部契约约束 CEK-TA 工作流，不替代外部 calibration 来源。"],
        published_at=TODAY,
    ),
    "src_cek_ta_phase40_review_budget_threshold_policy_contract": source(
        "src_cek_ta_phase40_review_budget_threshold_policy_contract",
        "CEK-TA Phase 40 Review Budget Threshold Policy Contract",
        "docs/contracts/phase40_review_budget_threshold_policy_contract.md",
        "internal_contract",
        "CEK-TA",
        90,
        "high",
        "Defines ReviewBudgetPolicy, ReviewQueueCapacitySnapshot, ThresholdPolicyReviewBudgetBinding and overflow boundaries.",
        ["内部契约支撑预算/队列字段，不替代外部 human-review workflow 来源。"],
        published_at=TODAY,
    ),
    "src_cek_ta_phase40_champion_release_contract": source(
        "src_cek_ta_phase40_champion_release_contract",
        "CEK-TA Phase 40 Champion Challenger Release Contract",
        "docs/contracts/phase40_champion_challenger_release_contract.md",
        "internal_contract",
        "CEK-TA",
        90,
        "high",
        "Defines ReleaseManifest, RollbackPlan, HumanApprovalRecord and release blockers for rollback and kill switch.",
        ["内部发布契约不替代真实部署验证。"],
        published_at=TODAY,
    ),
    "src_cek_ta_phase40_release_manifest_kill_switch_contract": source(
        "src_cek_ta_phase40_release_manifest_kill_switch_contract",
        "CEK-TA Phase 40 Release Manifest Kill Switch Contract",
        "docs/contracts/phase40_release_manifest_kill_switch_contract.md",
        "internal_contract",
        "CEK-TA",
        90,
        "high",
        "Defines ReleaseSafetyChecklist, KillSwitchPolicy, RollbackDrillRecord and SecretScanResult fields.",
        ["内部契约只定义安全发布字段和阻断规则。"],
        published_at=TODAY,
    ),
}


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "P40-C01": {
        "candidate_file": "cand_20260610_phase40_p40_c01_allow_block_skip_human_review_001.json",
        "source_ids": [
            "src_vowpal_wabbit_contextual_bandit",
            "src_open_bandit_pipeline_docs",
            "src_doubly_robust_policy_evaluation",
            "src_cek_ta_phase40_feedback_dataset_contract",
        ],
        "claim_patch": (
            "交易 AI gating/scoring 的 FeedbackRecord 必须记录 allow、block、skip、human_review 和 error "
            "全候选，并保留 candidate_id、decision_time、action_taken、final_gate_decision、policy_version、"
            "outcome_ref 与 counterfactual_status；blocked/skipped 候选的结果只能标记为未执行或反事实，不得解释为扩大实盘执行。"
        ),
        "supplemental_notes": [
            "Vowpal Wabbit 和 Open Bandit Pipeline 支撑 logged action / probability / cost / feedback 的 OPE 数据需求。",
            "Doubly Robust Policy Evaluation 论文支撑用历史 context、action、reward 和 past policy 评估新策略。",
            "CEK-TA Feedback Dataset Contract 明确所有候选决策类型都要记录。",
        ],
        "remaining_boundary": "log_every_candidate 不等于 execute_every_candidate；blocked/skipped outcome 仍是未执行或反事实状态。",
    },
    "P40-C02": {
        "candidate_file": "cand_20260610_phase40_p40_c02_feedback_record_scorer_llm_final_gate_001.json",
        "source_ids": [
            "src_feast_point_in_time_joins",
            "src_tecton_training_data",
            "src_databricks_point_in_time",
            "src_cek_ta_phase40_feedback_dataset_contract",
        ],
        "claim_patch": (
            "FeedbackRecord 必须保存决策时可用的 feature frame、numeric scorer 输出、LLM audit 输出、"
            "deterministic final gate 决策、版本号和后验 outcome_ref；post-trade outcome 只能作为观察窗口后的结果引用，"
            "不得混入 scorer 或 final gate 的决策时输入。"
        ),
        "supplemental_notes": [
            "Feast point-in-time joins 支撑按历史时间点复现 feature state，避免未来信息泄漏。",
            "Tecton 和 Databricks 来源支撑以 training events / timestamps 构造 point-in-time correct 数据。",
            "CEK-TA Feedback Dataset Contract 定义 scorer、LLM audit、final gate、outcome 和版本回链字段。",
        ],
        "remaining_boundary": "LLM audit output 只能作为审计辅助；final_gate_decision 必须来自 deterministic final gate。",
    },
    "P40-C07": {
        "candidate_file": "cand_20260610_phase40_p40_c07_feature_drift_label_drift_score_distribution_drift_calibration_drift_001.json",
        "source_ids": [
            "src_sklearn_calibration",
            "src_sklearn_calibration_curve_example",
            "src_sklearn_calibration_display",
            "src_cek_ta_phase40_drift_retraining_contract",
        ],
        "claim_patch": (
            "feature drift、label_or_target drift、score_distribution drift 和 calibration drift 必须分开监控；"
            "calibration drift 至少记录 reference_window、current_window、minimum_slice_n、Brier/ECE 或 "
            "calibration curve/reliability diagram 证据，并且 drift alert 只能触发 investigation、review 或 retraining_review。"
        ),
        "supplemental_notes": [
            "scikit-learn probability calibration 和 calibration curves 支撑概率校准与 reliability diagram。",
            "CalibrationDisplay 支撑按 bin 比较平均预测概率与正类比例。",
            "CEK-TA drift contract 定义 calibration_drift 与再训练/再校准触发边界。",
        ],
        "remaining_boundary": "drift alert 不是 hard gate、再训练命令或实盘交易动作。",
    },
    "P40-C12": {
        "candidate_file": "cand_20260610_phase40_p40_c12_threshold_policy_001.json",
        "source_ids": [
            "src_aws_augmented_ai_human_review",
            "src_aws_augmented_ai_create_workflow",
            "src_cek_ta_phase40_review_budget_threshold_policy_contract",
            "src_cek_ta_phase40_drift_retraining_contract",
        ],
        "claim_patch": (
            "threshold policy 必须绑定 cost_matrix_version、calibrator_version、review_budget_policy_ref、"
            "review_queue_capacity_snapshot_ref 和 owner_approval_ref；review budget 或 queue capacity 超限时只能进入 "
            "freeze_threshold_change、safe_mode、owner_review 或 collect_more_evidence，不能自动 allow 或自动 block。"
        ),
        "supplemental_notes": [
            "Amazon A2I 来源支撑 ML 应用中的 human review workflow 和 work team 配置。",
            "CEK-TA Review Budget Threshold Policy Contract 定义预算、队列容量和 overflow policy。",
            "CEK-TA drift/retraining contract 已定义 ThresholdStabilityReport 和 review_queue_pressure。",
        ],
        "remaining_boundary": "人审预算是治理约束，不是交易收益、买卖点、实盘风控阈值或自动放宽阈值的许可。",
    },
    "P40-C15": {
        "candidate_file": "cand_20260610_phase40_p40_c15_release_manifest_rollback_target_kill_switch_001.json",
        "source_ids": [
            "src_google_sre_canarying",
            "src_github_secret_scanning",
            "src_nist_ai_rmf_manage",
            "src_fca_algo_trading_controls",
            "src_cek_ta_phase40_champion_release_contract",
            "src_cek_ta_phase40_release_manifest_kill_switch_contract",
        ],
        "claim_patch": (
            "每次影响交易 AI gating/scoring 决策链路的发布都必须有 release manifest、rollback target、"
            "kill_switch_policy_ref、secret_scan_status、rollback_drill_status、kill_switch_tested_at 和 "
            "human_approval_record_ref；缺任一关键控制必须 block_release。"
        ),
        "supplemental_notes": [
            "Google SRE canarying 支撑小范围发布以降低部署风险。",
            "GitHub secret scanning 支撑发布前检查硬编码凭证和 token。",
            "NIST AI RMF Manage 支撑部署后监控、响应、恢复和变更管理。",
            "FCA 算法交易来源支撑 kill functionality 和风险控制清单。",
            "CEK-TA release/kill-switch contract 定义发布安全字段和阻断规则。",
        ],
        "remaining_boundary": "release manifest 不得包含私有策略正文、账号密钥或交易执行规则本体；订单撤单和实盘控制由 Trading Engineering 或外接项目实现。",
    },
}


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


def append_unique(values: list[Any], additions: list[Any]) -> list[Any]:
    result = list(values)
    for value in additions:
        if value not in result:
            result.append(value)
    return result


def merge_sources(candidate: dict[str, Any], source_ids: list[str]) -> list[dict[str, Any]]:
    refs = candidate.setdefault("source_refs", [])
    existing_refs = {ref.get("source_id"): ref for ref in refs if isinstance(ref, dict)}
    added: list[dict[str, Any]] = []
    for source_id in source_ids:
        if source_id in existing_refs:
            existing_refs[source_id].update(dict(SOURCE_LIBRARY[source_id]))
            continue
        source_ref = dict(SOURCE_LIBRARY[source_id])
        refs.append(source_ref)
        added.append(source_ref)
        existing_refs[source_id] = source_ref
    return added


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    audit_log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def update_source_quality(candidate: dict[str, Any]) -> None:
    source_refs = candidate.get("source_refs") or []
    primary_types = {"official_doc", "paper", "governance_framework", "internal_contract"}
    primary_count = sum(1 for ref in source_refs if isinstance(ref, dict) and ref.get("source_type") in primary_types)
    low_count = sum(1 for ref in source_refs if isinstance(ref, dict) and ref.get("reliability") == "low")
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high" if primary_count >= 5 and low_count == 0 else "medium"
    quality["score"] = max(int(quality.get("score") or 0), 88 if primary_count >= 5 else 85)
    quality["score_version"] = "1.1.0"
    quality["primary_source_count"] = primary_count
    quality["supporting_source_count"] = max(0, len(source_refs) - primary_count)
    quality["low_reliability_source_count"] = low_count
    quality["limitations"] = append_unique(
        list(quality.get("limitations") or []),
        ["补证后仍需外部 AI/人工三审确认 claim-specific 充分性，不能直接转 reviewed 或 approved。"],
    )


def supplement_candidate(path: Path, supplement: dict[str, Any]) -> dict[str, Any]:
    candidate = read_json(path)
    added_sources = merge_sources(candidate, supplement["source_ids"])

    claim = candidate.setdefault("claim", {})
    previous_statement = claim.get("statement")
    claim["statement"] = supplement["claim_patch"]
    claim["claim_strength"] = "medium"
    claim["evidence_summary"] = "；".join(
        ref["evidence_summary"] for ref in candidate.get("source_refs", [])[-min(5, len(candidate.get("source_refs", []))):]
    )

    applicability = candidate.setdefault("applicability", {})
    applicability["limitations"] = append_unique(
        list(applicability.get("limitations") or []),
        [supplement["remaining_boundary"]],
    )

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已按 reviewed preparation 二审意见补充来源、契约字段和边界说明；等待外部三审。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "default_guidance_allowed": False,
            "next_action": "export_ai_audit",
        }
    )

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "supplemented candidate awaiting third review; not reviewed, approved, default guidance, or hard gate."

    new_contracts = [
        "docs/contracts/phase40_review_budget_threshold_policy_contract.md",
        "docs/contracts/phase40_release_manifest_kill_switch_contract.md",
    ]
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none"
    conflict["approval_allowed"] = False
    conflict["checked_against"] = append_unique(list(conflict.get("checked_against") or []), new_contracts)
    conflict["resolution_summary"] = "补证后未发现直接理论冲突；仍需三审确认来源充分性和 AI/Trading 分支边界。"

    phase40_trace = candidate.setdefault("phase40_trace", {})
    phase40_trace["supplemental_evidence_ready"] = True
    phase40_trace["supplemental_evidence_added_at"] = TODAY
    phase40_trace["supplemental_task_id"] = TASK_ID
    phase40_trace["related_contracts"] = append_unique(list(phase40_trace.get("related_contracts") or []), new_contracts)
    phase40_trace["audit_patch_notes"] = {
        "source_ids_added_or_confirmed": supplement["source_ids"],
        "remaining_boundary": supplement["remaining_boundary"],
    }

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_supplemental_evidence"
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = [
        "请三审确认补证后是否 accepted_for_draft；如果仍不足，请返回 needs_more_evidence 或 rejected。",
        "即使三审通过，本条仍只能进入 formal reviewed draft，不得直接 approved、default guidance 或 hard gate。",
    ]
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False

    ai_audit = review.setdefault("ai_audit", {})
    ai_audit["supplemental_evidence"] = {
        "status": "ready_for_reaudit",
        "added_at": TODAY,
        "task_id": TASK_ID,
        "previous_statement": previous_statement,
        "patched_statement": supplement["claim_patch"],
        "added_source_ids": [ref["source_id"] for ref in added_sources],
        "all_supplemental_source_ids": supplement["source_ids"],
        "supplemental_notes": supplement["supplemental_notes"],
        "remaining_boundary": supplement["remaining_boundary"],
        "reaudit_request": "请判断补证后是否 accepted_for_draft；不得直接 reviewed/approved/default/hard gate。",
    }

    update_source_quality(candidate)
    append_audit_log(
        candidate,
        "phase40_reviewed_preparation_supplemental_evidence_ready",
        "按 CEK-TA-317 补充来源和契约，并准备三审。",
    )
    write_json(path, candidate)
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "path": repo_rel(path),
        "added_source_ids": [ref["source_id"] for ref in added_sources],
        "total_source_count": len(candidate.get("source_refs") or []),
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id"))
        refs = candidate.get("source_refs") or []
        supplemental = candidate.get("review", {}).get("ai_audit", {}).get("supplemental_evidence", {})
        if len(refs) < 6:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_6"})
        if supplemental.get("status") != "ready_for_reaudit":
            failures.append({"candidate_id": candidate_id, "failure": "missing_supplemental_evidence_status"})
        if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_not_denied"})
        if candidate.get("conversion_target", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "conversion_default_guidance_not_false"})
        if candidate.get("conversion_target", {}).get("hard_gate_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "conversion_hard_gate_not_false"})
        if candidate.get("workflow", {}).get("visible_in_default_guidance_queue") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "visible_default_queue_not_false"})
        if candidate.get("workflow", {}).get("formal_knowledge_id") is not None:
            failures.append({"candidate_id": candidate_id, "failure": "formal_knowledge_created_too_early"})
        if candidate.get("review", {}).get("reviewed_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "reviewed_allowed_not_false_before_third_review"})
    return {
        "gate_id": "phase40_reviewed_preparation_supplemental_reaudit_quality_gate",
        "generated_at": TODAY,
        "candidate_count": len(candidates),
        "expected_count": len(SUPPLEMENTS),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures and len(candidates) == len(SUPPLEMENTS) else "fail",
    }


def build_audit_package(candidates: list[dict[str, Any]], report: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": REAUDIT_PACKAGE_ID,
        "package_type": "candidate_ai_reaudit_package",
        "generated_at": TODAY,
        "phase": "40",
        "task_id": TASK_ID,
        "source_audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "title": "Phase 40 reviewed preparation needs_more_evidence 补证后三审包",
        "purpose": "只审计 5 条已补证候选，判断是否可进入 accepted_for_draft，供后续 Codex 生成 formal reviewed draft。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "三审可以给出 accepted_for_draft，但不得直接给 approved。",
            "reviewed_allowed=true 只表示可由 Codex 后续生成 formal reviewed draft，不等于 approved。",
            "approved_allowed、default_guidance_allowed、hard_gate_allowed 必须保持 false。",
            "Trading Engineering 的 K 线、fill model、订单状态机、实盘风控和交易执行本体不得混入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "确认补证是否充分、字段契约是否足够、边界是否正确、是否仍需补来源或应拒绝。",
            "focus_checks": [
                "新增来源是否直接支撑该 claim，而不是只支撑通用 ML 概念。",
                "内部 CEK-TA 契约是否只作为字段和工作流证据，不替代外部专业来源。",
                "是否误把交易规则、成本模型、market regime、fill/slippage 本体写入 AI Engineering。",
                "是否保持 candidate/reviewed/approved 状态边界。",
                "是否保持 default_guidance_allowed=false 和 hard_gate_allowed=false。",
                "若 accepted_for_draft，请给出 required_patch_notes 以便 Codex 后续转 formal reviewed draft。",
            ],
            "required_output_schema": {
                "audit_result_id": "audit_result_phase40_reviewed_preparation_supplemental_reaudit_20260610_v1",
                "source_package_id": REAUDIT_PACKAGE_ID,
                "decisions": [
                    {
                        "candidate_id": "string",
                        "research_task_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
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
                    }
                ],
                "batch_summary": {
                    "accepted_count": 0,
                    "needs_more_evidence_count": 0,
                    "rejected_count": 0,
                    "misrouted_to_trading_count": 0,
                    "reviewed_allowed_count": 0,
                    "approved_allowed_count": 0,
                    "default_guidance_allowed_count": 0,
                    "hard_gate_allowed_count": 0,
                },
            },
        },
        "quality_gate": report["quality_gate"],
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def main() -> int:
    touched: list[dict[str, Any]] = []
    supplemented: list[dict[str, Any]] = []

    for task_id, supplement in SUPPLEMENTS.items():
        path = CANDIDATE_DIR / supplement["candidate_file"]
        if not path.exists():
            raise FileNotFoundError(f"Missing candidate for {task_id}: {path}")
        touched.append(supplement_candidate(path, supplement))
        supplemented.append(read_json(path))

    gate = quality_gate(supplemented)
    report = {
        "report_id": "phase40_reviewed_preparation_supplemental_evidence_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "scope": "Phase 40 reviewed-preparation 5 needs_more_evidence supplemental evidence",
        "source_audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "touched_count": len(touched),
        "touched_candidates": touched,
        "new_contracts": [
            "docs/contracts/phase40_review_budget_threshold_policy_contract.md",
            "docs/contracts/phase40_release_manifest_kill_switch_contract.md",
        ],
        "research_record": "docs/research/phase40_reviewed_preparation_supplemental_research.md",
        "quality_gate": gate,
        "audit_package_path": repo_rel(AUDIT_PACKAGE_PATH),
        "boundary": "补证后仍是 candidate；不创建 formal reviewed、approved、default guidance 或 hard gate。",
    }
    write_json(REPORT_PATH, report)
    write_json(AUDIT_PACKAGE_PATH, build_audit_package(supplemented, report))

    print(
        json.dumps(
            {
                "ok": gate["gate_status"] == "pass",
                "report": repo_rel(REPORT_PATH),
                "audit_package": repo_rel(AUDIT_PACKAGE_PATH),
                "candidate_count": len(supplemented),
                "failure_count": gate["failure_count"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
