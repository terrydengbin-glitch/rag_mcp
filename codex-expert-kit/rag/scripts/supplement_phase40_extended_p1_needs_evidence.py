"""Supplement Phase 40 Batch D/E needs-more-evidence candidates and export reaudit package."""

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
TASK_ID = "CEK-TA-313"
AUDIT_RESULT_ID = "audit_result_phase40_extended_p1_batch_de_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase40_extended_p1_candidate_audit_package_20260610"
REAUDIT_PACKAGE_ID = "phase40_extended_p1_supplemental_reaudit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_extended_p1_supplemental_evidence_report.json", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase40_extended_p1_supplemental_reaudit_package_20260610.json", start_file=__file__
)


SOURCE_LIBRARY: dict[str, dict[str, Any]] = {
    "src_cek_ta_phase40_decision_cost_dashboard_contract": {
        "source_id": "src_cek_ta_phase40_decision_cost_dashboard_contract",
        "source_title": "CEK-TA Phase 40 Decision Cost Dashboard Metric Contract",
        "source_url": "docs/contracts/phase40_decision_cost_dashboard_metric_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "draft",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约定义 CEK-TA 字段和边界，需要外部来源共同支撑通用方法。"],
        "evidence_summary": "定义 DecisionCostMetricSet、ContinuousLearningDashboardSnapshot、false allow/block、人审成本和看板硬门。",
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase40_composite_release_artifact_contract": {
        "source_id": "src_cek_ta_phase40_composite_release_artifact_contract",
        "source_title": "CEK-TA Phase 40 Composite Release Artifact Contract",
        "source_url": "docs/contracts/phase40_composite_release_artifact_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "draft",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约定义组合发布和组合回滚字段，不替代外部 MLOps 生命周期来源。"],
        "evidence_summary": "定义 CompositeReleaseUnit、CompositeArtifactReleaseManifest、CompositeRollbackTarget 和组件级 rollback 硬门。",
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase40_champion_release_contract": {
        "source_id": "src_cek_ta_phase40_champion_release_contract",
        "source_title": "CEK-TA Phase 40 Champion Challenger Release Contract",
        "source_url": "docs/contracts/phase40_champion_challenger_release_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "draft",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约定义交易 AI 发布阶段，不替代真实交易环境验证数据。"],
        "evidence_summary": "定义 champion/challenger、shadow/paper/canary、ReleaseManifest、RollbackPlan 和 HumanApprovalRecord。",
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase40_drift_retraining_contract": {
        "source_id": "src_cek_ta_phase40_drift_retraining_contract",
        "source_title": "CEK-TA Phase 40 Drift Retraining Recalibration Contract",
        "source_url": "docs/contracts/phase40_drift_retraining_recalibration_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "draft",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约用于交易 AI 的漂移和阈值边界，不定义 Trading Engineering 本体。"],
        "evidence_summary": "定义 DriftReport、RetrainingTriggerDecision、RecalibrationReport、ThresholdStabilityReport 和 execution-cost 引用边界。",
        "quoted_excerpt_allowed": False,
    },
    "src_sklearn_cost_sensitive_threshold": {
        "source_id": "src_sklearn_cost_sensitive_threshold",
        "source_title": "Post-tuning the decision threshold for cost-sensitive learning",
        "source_url": "https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑成本敏感阈值调优思想，不定义交易收益、回撤或实盘成本。"],
        "evidence_summary": "scikit-learn 示例用 TunedThresholdClassifierCV 选择能最小化业务成本的决策阈值。",
        "quoted_excerpt_allowed": False,
    },
    "src_sklearn_calibration": {
        "source_id": "src_sklearn_calibration",
        "source_title": "Probability calibration - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/calibration.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑概率校准，不证明交易模型可盈利。"],
        "evidence_summary": "scikit-learn 文档说明分类器概率可能需要校准，校准模块用于改进概率预测。",
        "quoted_excerpt_allowed": False,
    },
    "src_arize_monitoring_metrics": {
        "source_id": "src_arize_monitoring_metrics",
        "source_title": "Best Practices for Monitors - Arize AX Docs",
        "source_url": "https://arize.com/docs/ax/machine-learning/machine-learning/how-to-ml/monitors/choosing-your-metrics",
        "source_type": "official_doc",
        "publisher": "Arize AI",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 ML 监控指标和自定义指标，不定义 CEK-TA 的人工审批流。"],
        "evidence_summary": "Arize 监控文档覆盖 performance、drift、data quality、custom metrics，并列出 FPR/FNR 等指标。",
        "quoted_excerpt_allowed": False,
    },
    "src_evidently_data_drift": {
        "source_id": "src_evidently_data_drift",
        "source_title": "Data Drift - Evidently Documentation",
        "source_url": "https://docs.evidentlyai.com/metrics/preset_data_drift",
        "source_type": "official_doc",
        "publisher": "Evidently AI",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": ["支撑数据漂移监控，不定义 false allow/block 成本。"],
        "evidence_summary": "Evidently DataDriftPreset 用于比较参考数据与当前数据的分布变化。",
        "quoted_excerpt_allowed": False,
    },
    "src_aws_sagemaker_shadow_tests": {
        "source_id": "src_aws_sagemaker_shadow_tests",
        "source_title": "Shadow tests - Amazon SageMaker AI",
        "source_url": "https://docs.aws.amazon.com/sagemaker/latest/dg/shadow-tests.html",
        "source_type": "official_doc",
        "publisher": "AWS",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑模型服务 shadow testing，不定义交易 paper/replay 的成交假设。"],
        "evidence_summary": "SageMaker shadow tests 将实时请求副本路由给 shadow variant，用于和生产变体比较。",
        "quoted_excerpt_allowed": False,
    },
    "src_microsoft_shadow_testing": {
        "source_id": "src_microsoft_shadow_testing",
        "source_title": "Shadow Testing - Microsoft Engineering Fundamentals Playbook",
        "source_url": "https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/",
        "source_type": "official_doc",
        "publisher": "Microsoft",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["支撑 shadow 环境比较，不等同于实盘交易环境证明。"],
        "evidence_summary": "Microsoft playbook 将 shadow testing 描述为复制生产流量到候选环境并比较差异。",
        "quoted_excerpt_allowed": False,
    },
    "src_quantconnect_trade_fills": {
        "source_id": "src_quantconnect_trade_fills",
        "source_title": "Trade Fills - QuantConnect Documentation",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
        "source_type": "official_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["Trading Engineering 来源，只能作为 fill/cost/latency 引用，不应把本体搬进 AI Engineering。"],
        "evidence_summary": "QuantConnect 文档说明 fill models 决定成交价格和数量，并可结合 spread/slippage 模拟成交。",
        "quoted_excerpt_allowed": False,
    },
    "src_quantconnect_paper_trading": {
        "source_id": "src_quantconnect_paper_trading",
        "source_title": "QuantConnect Paper Trading",
        "source_url": "https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading",
        "source_type": "official_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["说明 paper trading 使用模拟成交，不证明实盘等价。"],
        "evidence_summary": "QuantConnect 说明 paper trading 使用实时数据但以虚拟资金和模拟 fills 执行。",
        "quoted_excerpt_allowed": False,
    },
    "src_ibkr_paper_trading_limitations": {
        "source_id": "src_ibkr_paper_trading_limitations",
        "source_title": "About Paper Trading Accounts - IBKR Guides",
        "source_url": "https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm",
        "source_type": "official_doc",
        "publisher": "Interactive Brokers",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["经纪商 paper account 限制来源，不定义 CEK-TA 回放引擎。"],
        "evidence_summary": "IBKR 指出 paper trading account 是 simulator，可能与 production account 存在差异。",
        "quoted_excerpt_allowed": False,
    },
    "src_ragas_faithfulness": {
        "source_id": "src_ragas_faithfulness",
        "source_title": "Faithfulness - Ragas",
        "source_url": "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/",
        "source_type": "official_doc",
        "publisher": "Ragas",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "medium",
        "score": 78,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["RAG faithfulness 指标不证明交易知识正确性，只支撑回答与检索上下文一致性。"],
        "evidence_summary": "Ragas Faithfulness 衡量 response 是否与 retrieved context 事实一致。",
        "quoted_excerpt_allowed": False,
    },
    "src_arize_phoenix_faithfulness": {
        "source_id": "src_arize_phoenix_faithfulness",
        "source_title": "Faithfulness - Phoenix Arize AI",
        "source_url": "https://arize.com/docs/phoenix/evaluation/pre-built-metrics/faithfulness",
        "source_type": "official_doc",
        "publisher": "Arize AI",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 hallucination/groundedness 检查，不替代人工来源审计。"],
        "evidence_summary": "Phoenix Faithfulness evaluator 检查 LLM response 是否被上下文支持、是否出现不支持或矛盾内容。",
        "quoted_excerpt_allowed": False,
    },
    "src_google_grounding_check": {
        "source_id": "src_google_grounding_check",
        "source_title": "Check grounding with RAG - Google Cloud",
        "source_url": "https://docs.cloud.google.com/generative-ai-app-builder/docs/check-grounding",
        "source_type": "official_doc",
        "publisher": "Google Cloud",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 grounding/citation，不证明交易规则本体。"],
        "evidence_summary": "Google Cloud grounding check 返回 support score，并包含支持回答 claim 的 citations。",
        "quoted_excerpt_allowed": False,
    },
    "src_promptfoo_context_faithfulness": {
        "source_id": "src_promptfoo_context_faithfulness",
        "source_title": "Context faithfulness - Promptfoo",
        "source_url": "https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/context-faithfulness/",
        "source_type": "official_doc",
        "publisher": "Promptfoo",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 claim 是否被上下文支持，不定义 CEK-TA citation resolver schema。"],
        "evidence_summary": "Promptfoo context faithfulness 检查模型回答是否只包含检索上下文支持的 claims。",
        "quoted_excerpt_allowed": False,
    },
    "src_promptfoo_rag_eval": {
        "source_id": "src_promptfoo_rag_eval",
        "source_title": "Evaluating RAG pipelines - Promptfoo",
        "source_url": "https://www.promptfoo.dev/docs/guides/evaluate-rag/",
        "source_type": "official_doc",
        "publisher": "Promptfoo",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 RAG pipeline 检索/生成评估，不定义交易发布治理。"],
        "evidence_summary": "Promptfoo 文档要求同时评估 document retrieval 和 LLM output generation。",
        "quoted_excerpt_allowed": False,
    },
    "src_mlflow_model_registry": {
        "source_id": "src_mlflow_model_registry",
        "source_title": "MLflow Model Registry",
        "source_url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "source_type": "official_doc",
        "publisher": "MLflow",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑模型版本和生命周期管理，不直接覆盖 prompt/RAG/threshold 组合回滚。"],
        "evidence_summary": "MLflow Model Registry 提供模型 lineage、versioning、aliases、metadata tagging 和 annotations。",
        "quoted_excerpt_allowed": False,
    },
    "src_mlflow_model_registry_workflow": {
        "source_id": "src_mlflow_model_registry_workflow",
        "source_title": "Model Registry Workflows - MLflow",
        "source_url": "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
        "source_type": "official_doc",
        "publisher": "MLflow",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": ["支撑模型注册、版本和 alias 工作流，不直接管理 RAG 索引和 prompt。"],
        "evidence_summary": "MLflow workflow 文档覆盖模型注册、版本管理、aliases 和 tags。",
        "quoted_excerpt_allowed": False,
    },
    "src_nist_ai_rmf_manage": {
        "source_id": "src_nist_ai_rmf_manage",
        "source_title": "Manage - NIST AI RMF Playbook",
        "source_url": "https://airc.nist.gov/airmf-resources/playbook/manage/",
        "source_type": "governance_framework",
        "publisher": "NIST",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["治理框架来源，不替代项目内 release/rollback manifest。"],
        "evidence_summary": "NIST AI RMF Manage 强调部署后监控、响应、恢复、变更管理和 decommission。",
        "quoted_excerpt_allowed": False,
    },
}


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "P40-E06": {
        "candidate_file": "cand_20260610_phase40_p40_e06_challenger_risk_metrics_001.json",
        "source_ids": [
            "src_cek_ta_phase40_decision_cost_dashboard_contract",
            "src_cek_ta_phase40_champion_release_contract",
            "src_cek_ta_phase40_drift_retraining_contract",
            "src_sklearn_cost_sensitive_threshold",
            "src_sklearn_calibration",
            "src_arize_monitoring_metrics",
        ],
        "claim_patch": (
            "champion/challenger 比较必须包含 AI decision-cost 风险切片，至少记录 false_allow_rate、"
            "false_block_rate、false_allow_cost、false_block_cost、calibration 指标、人审压力和 Trading Engineering "
            "execution_cost_ref；不得只用平均收益或平均分数决定 challenger 是否进入下一阶段。"
        ),
        "supplemental_notes": [
            "scikit-learn cost-sensitive threshold 示例直接支撑按业务成本而非单一平均指标选择阈值。",
            "scikit-learn calibration 支撑概率分数需要校准，不应把高分直接等同可上线。",
            "Arize 监控来源支撑 FPR/FNR、performance、drift 和 custom metrics。",
            "CEK-TA decision-cost 契约定义 false allow/block、人审成本、tail loss/drawdown proxy ref 和 execution_cost_ref。",
        ],
        "remaining_boundary": "Trading PnL、drawdown、fee、slippage、fill 和 execution-cost 本体必须引用 Trading Engineering 或外接项目事实。",
    },
    "P40-E07": {
        "candidate_file": "cand_20260610_phase40_p40_e07_shadow_paper_execution_gap_001.json",
        "source_ids": [
            "src_aws_sagemaker_shadow_tests",
            "src_microsoft_shadow_testing",
            "src_quantconnect_trade_fills",
            "src_quantconnect_paper_trading",
            "src_ibkr_paper_trading_limitations",
            "src_cek_ta_phase40_champion_release_contract",
        ],
        "claim_patch": (
            "shadow、paper 和 replay 结果必须分别声明与真实执行环境的差异：shadow 只比较候选输出，"
            "paper/replay 必须记录 fill_cost_assumption_ref、replay_engine_version、market_data_replay_policy_ref "
            "和 execution_gap_report；任何 paper/replay 结果都不得宣称等同实盘。"
        ),
        "supplemental_notes": [
            "AWS/Microsoft 来源支撑 shadow testing 复制生产请求或流量并比较候选环境。",
            "QuantConnect paper trading 明确使用模拟 fills；IBKR 说明 paper account 作为 simulator 可能与 production 存在差异。",
            "QuantConnect trade fills 来源支撑 fill model、spread/slippage 对成交模拟的重要性。",
            "CEK-TA release contract 明确 shadow/paper/canary 是发布证据，不是自动上线许可。",
        ],
        "remaining_boundary": "AI Engineering 只要求引用 fill/cost/latency 假设；fill model、market impact、手续费、滑点和订单状态机由 Trading Engineering 管理。",
    },
    "P40-E11": {
        "candidate_file": "cand_20260610_phase40_p40_e11_confidence_not_evidence_001.json",
        "source_ids": [
            "src_ragas_faithfulness",
            "src_arize_phoenix_faithfulness",
            "src_google_grounding_check",
            "src_promptfoo_context_faithfulness",
            "src_promptfoo_rag_eval",
        ],
        "claim_patch": (
            "高置信模型输出只能作为风险信号，不能替代来源证据；RAG/LLM 审计输出必须记录 "
            "source_evidence_refs、citation_resolver_version、unsupported_claims、grounding_status 和 "
            "no_source_abstain_policy，否则不得进入默认指导或发布证据。"
        ),
        "supplemental_notes": [
            "Ragas、Arize Phoenix 和 Promptfoo faithfulness 来源直接支撑回答/claim 必须被检索上下文支持。",
            "Google grounding check 来源支撑 support score 与 claim citation。",
            "Promptfoo RAG evaluation 来源支撑同时评估 retrieval 和 generation。",
        ],
        "remaining_boundary": "confidence、probability 或 LLM 自评不得替代 citation、source evidence、人工审计或 formal knowledge 状态。",
    },
    "P40-E12": {
        "candidate_file": "cand_20260610_phase40_p40_e12_continuous_learning_dashboard_001.json",
        "source_ids": [
            "src_cek_ta_phase40_decision_cost_dashboard_contract",
            "src_arize_monitoring_metrics",
            "src_evidently_data_drift",
            "src_sklearn_cost_sensitive_threshold",
            "src_sklearn_calibration",
        ],
        "claim_patch": (
            "持续学习看板必须分面展示 drift、calibration、decision cost、false allow/block、"
            "human review cost、release/rollback 状态和 insufficient_data；这些指标只能触发 investigate、"
            "collect_more_evidence、retraining_review、release_freeze 或 rollback_review，不能自动 hard gate。"
        ),
        "supplemental_notes": [
            "Arize 监控来源支撑 performance、drift、data quality、custom metrics 和 FPR/FNR。",
            "Evidently 支撑数据漂移监控。",
            "scikit-learn calibration 和 cost-sensitive threshold 支撑校准与成本敏感决策。",
            "CEK-TA dashboard metric contract 定义 decision cost、人审成本和看板输出 schema。",
        ],
        "remaining_boundary": "dashboard metrics 是观测和审计信号，不是自动再训练、上线、交易或 hard gate 命令。",
    },
    "P40-P05": {
        "candidate_file": "cand_20260610_phase40_p40_p05_composite_artifact_rollback_001.json",
        "source_ids": [
            "src_cek_ta_phase40_composite_release_artifact_contract",
            "src_cek_ta_phase40_champion_release_contract",
            "src_mlflow_model_registry",
            "src_mlflow_model_registry_workflow",
            "src_promptfoo_rag_eval",
            "src_nist_ai_rmf_manage",
        ],
        "claim_patch": (
            "发布治理必须把 numeric_model_version、calibrator_version、prompt_version、rag_index_version、"
            "threshold_policy_version、final_gate_policy_version 和 code_version_hash 作为 CompositeReleaseUnit 管理；"
            "回滚必须有 CompositeRollbackTarget，禁止只回滚模型却继续使用事故版本 prompt、RAG 索引或阈值策略。"
        ),
        "supplemental_notes": [
            "MLflow 来源支撑模型 lifecycle、lineage、versioning、aliases 和 tags。",
            "Promptfoo RAG evaluation 支撑 RAG package 需要独立回归评估。",
            "NIST AI RMF Manage 支撑部署后监控、响应、恢复和变更管理。",
            "CEK-TA composite contract 明确模型、prompt、RAG、threshold 和 final gate policy 的组合发布与组合回滚字段。",
        ],
        "remaining_boundary": "threshold/final-gate rollback 仍必须由 deterministic final-gate owner 和人工审批记录管理。",
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


def merge_sources(candidate: dict[str, Any], source_ids: list[str]) -> list[dict[str, Any]]:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    added: list[dict[str, Any]] = []
    for source_id in source_ids:
        if source_id in existing:
            continue
        source = dict(SOURCE_LIBRARY[source_id])
        refs.append(source)
        added.append(source)
        existing.add(source_id)
    return added


def append_unique(items: list[Any], values: list[Any]) -> list[Any]:
    merged = list(items)
    for value in values:
        if value not in merged:
            merged.append(value)
    return merged


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    review = candidate.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def update_source_quality(candidate: dict[str, Any]) -> None:
    source_refs = candidate.get("source_refs") or []
    primary_count = sum(
        1
        for source in source_refs
        if source.get("source_type") in {"official_doc", "paper", "governance_framework", "internal_contract"}
    )
    low_count = sum(1 for source in source_refs if source.get("reliability") == "low")
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high" if primary_count >= 5 and low_count == 0 else "medium"
    quality["score"] = max(int(quality.get("score") or 0), 88 if primary_count >= 5 else 84)
    quality["score_version"] = "1.1.0"
    quality["primary_source_count"] = primary_count
    quality["supporting_source_count"] = max(0, len(source_refs) - primary_count)
    quality["low_reliability_source_count"] = low_count
    quality["limitations"] = append_unique(
        list(quality.get("limitations") or []),
        ["补证后仍需外部 AI/人工二审确认 claim-specific 充分性，不能直接转 reviewed 或 approved。"],
    )


def supplement_candidate(path: Path, supplement: dict[str, Any]) -> dict[str, Any]:
    candidate = read_json(path)
    added_sources = merge_sources(candidate, supplement["source_ids"])

    claim = candidate.setdefault("claim", {})
    previous_statement = claim.get("statement")
    claim["statement"] = supplement["claim_patch"]
    claim["claim_strength"] = "medium"
    claim["evidence_summary"] = "；".join(source["evidence_summary"] for source in candidate.get("source_refs", [])[-4:])

    applicability = candidate.setdefault("applicability", {})
    applicability["limitations"] = append_unique(
        list(applicability.get("limitations") or []), [supplement["remaining_boundary"]]
    )

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已按 Batch D/E 严格审计意见补充 claim-specific 来源、内部契约和边界说明；等待外部二审。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
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
    machine_gate["reason"] = "supplemented candidate awaiting reaudit; not reviewed, approved, default guidance, or hard gate."

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none"
    conflict["approval_allowed"] = False
    conflict["resolution_summary"] = "补证后未发现直接理论冲突；仍需二审确认来源充分性和 AI/Trading 分支边界。"
    checked_against = list(conflict.get("checked_against") or [])
    conflict["checked_against"] = append_unique(
        checked_against,
        [
            "docs/contracts/phase40_decision_cost_dashboard_metric_contract.md",
            "docs/contracts/phase40_composite_release_artifact_contract.md",
        ],
    )

    phase40_trace = candidate.setdefault("phase40_trace", {})
    phase40_trace["supplemental_evidence_ready"] = True
    phase40_trace["supplemental_evidence_added_at"] = TODAY
    phase40_trace["supplemental_task_id"] = TASK_ID
    phase40_trace["related_contracts"] = append_unique(
        list(phase40_trace.get("related_contracts") or []),
        [
            "docs/contracts/phase40_decision_cost_dashboard_metric_contract.md",
            "docs/contracts/phase40_composite_release_artifact_contract.md",
        ],
    )

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_supplemental_evidence"
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = [
        "请二审确认补证后是否 accepted_for_draft；如果仍不足，请返回 needs_more_evidence 或 rejected。",
        "即使二审通过，本条仍只能进入 formal reviewed draft，不得直接 approved、default guidance 或 hard gate。",
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
        "added_source_ids": [source["source_id"] for source in added_sources],
        "all_supplemental_source_ids": supplement["source_ids"],
        "supplemental_notes": supplement["supplemental_notes"],
        "remaining_boundary": supplement["remaining_boundary"],
        "reaudit_request": "请判断补证后是否 accepted_for_draft；不得直接 reviewed/approved/default/hard gate。",
    }

    update_source_quality(candidate)
    append_audit_log(candidate, "phase40_extended_p1_supplemental_evidence_ready", "按 Batch D/E 严格审计意见补证并准备二审。")
    write_json(path, candidate)
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "path": repo_rel(path),
        "added_source_ids": [source["source_id"] for source in added_sources],
        "total_source_count": len(candidate.get("source_refs") or []),
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id"))
        source_refs = candidate.get("source_refs") or []
        supplemental = candidate.get("review", {}).get("ai_audit", {}).get("supplemental_evidence", {})
        if len(source_refs) < 5:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_5"})
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
    return {
        "gate_id": "phase40_extended_p1_supplemental_reaudit_quality_gate",
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
        "title": "Phase 40 Batch D/E needs_more_evidence 补证后二审包",
        "purpose": "只审计 5 条已补证候选，判断是否可进入 accepted_for_draft。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "二审可以给出 accepted_for_draft，但不得直接给 approved。",
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
                "是否保持 default_guidance_allowed=false 和 hard_gate_allowed=false。",
                "若 accepted_for_draft，请给出 required_patch_notes 以便 Codex 后续转 formal reviewed draft。",
            ],
            "required_output_schema": {
                "audit_result_id": "audit_result_phase40_extended_p1_supplemental_reaudit_20260610_v1",
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
        result = supplement_candidate(path, supplement)
        touched.append(result)
        supplemented.append(read_json(path))

    gate = quality_gate(supplemented)
    report = {
        "report_id": "phase40_extended_p1_supplemental_evidence_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "scope": "Phase 40 Batch D/E needs_more_evidence supplemental evidence",
        "source_audit_result_id": AUDIT_RESULT_ID,
        "touched_count": len(touched),
        "touched_candidates": touched,
        "new_contracts": [
            "docs/contracts/phase40_decision_cost_dashboard_metric_contract.md",
            "docs/contracts/phase40_composite_release_artifact_contract.md",
        ],
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
            },
            ensure_ascii=True,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
