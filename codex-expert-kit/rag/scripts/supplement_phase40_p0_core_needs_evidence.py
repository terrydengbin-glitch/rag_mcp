"""Supplement Phase 40 P0-Core needs-more-evidence candidates and export reaudit package."""

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
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase40_p0_core_supplemental_evidence_report.json", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase40_p0_core_supplemental_reaudit_package_20260610.json", start_file=__file__
)

SOURCE_LIBRARY: dict[str, dict[str, Any]] = {
    "src_cek_ta_phase40_feedback_dataset_contract": {
        "source_id": "src_cek_ta_phase40_feedback_dataset_contract",
        "source_title": "CEK-TA Phase 40 Feedback Dataset Contract",
        "source_url": "docs/contracts/phase40_feedback_dataset_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": "2026-06-10",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约只定义 CEK-TA 项目边界，需要外部来源共同支撑通用方法。"],
        "evidence_summary": (
            "定义 FeedbackRecord、LabelUpdateRecord、DatasetVersionManifest 和 AuditTraceRecord；"
            "明确所有候选都要记录、标签不能只看 PnL、反馈记录不能直接成为训练真值。"
        ),
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase40_drift_retraining_contract": {
        "source_id": "src_cek_ta_phase40_drift_retraining_contract",
        "source_title": "CEK-TA Phase 40 Drift Retraining Recalibration Contract",
        "source_url": "docs/contracts/phase40_drift_retraining_recalibration_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": "2026-06-10",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约用于交易 AI 的工程边界，不替代外部 ML 监控来源。"],
        "evidence_summary": (
            "定义 feature、label、score、calibration、strategy、symbol/regime、execution cost 等漂移类型；"
            "强调漂移报警不是再训练命令，再训练触发不是上线许可。"
        ),
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase40_champion_release_contract": {
        "source_id": "src_cek_ta_phase40_champion_release_contract",
        "source_title": "CEK-TA Phase 40 Champion Challenger Release Contract",
        "source_url": "docs/contracts/phase40_champion_challenger_release_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": "2026-06-10",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约定义交易 AI 发布阶段，不替代真实交易环境的验证数据。"],
        "evidence_summary": (
            "定义 champion/challenger、shadow/paper/canary、ReleaseManifest、RollbackPlan 和 HumanApprovalRecord；"
            "明确 shadow/paper/canary 是发布证据，不是自动上线许可。"
        ),
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase38_training_eval_contract": {
        "source_id": "src_cek_ta_phase38_training_eval_contract",
        "source_title": "CEK-TA Phase 38 Training Data and Eval Contract",
        "source_url": "docs/contracts/phase38_training_data_and_eval_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": "2026-06-10",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部训练评估契约需要外部模型评估和结构化输出来源共同支撑。"],
        "evidence_summary": "定义交易 LLM gating/scoring 的训练数据、评估集、泄漏控制和指标边界。",
        "quoted_excerpt_allowed": False,
    },
    "src_cek_ta_phase38_rag_reason_taxonomy_contract": {
        "source_id": "src_cek_ta_phase38_rag_reason_taxonomy_contract",
        "source_title": "CEK-TA Phase 38 RAG Citation and Reason Taxonomy Contract",
        "source_url": "docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": "2026-06-10",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部 reason code 契约只约束 CEK-TA 输出格式。"],
        "evidence_summary": "定义 RAG 引用、reason code、unsupported claim 和 no-source abstain 的输出约束。",
        "quoted_excerpt_allowed": False,
    },
    "src_tfdv_get_started": {
        "source_id": "src_tfdv_get_started",
        "source_title": "Get started with TensorFlow Data Validation",
        "source_url": "https://www.tensorflow.org/tfx/data_validation/get_started",
        "source_type": "official_doc",
        "publisher": "TensorFlow",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["TFDV 支撑数据 schema、skew 和 drift 检查，不直接定义交易标签或阈值。"],
        "evidence_summary": "TFDV 支持 schema、训练/服务 skew 和不同训练数据日期之间的 drift 检查。",
        "quoted_excerpt_allowed": False,
    },
    "src_nist_ai_rmf_core": {
        "source_id": "src_nist_ai_rmf_core",
        "source_title": "AI RMF Core | NIST AI Resource Center",
        "source_url": "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/",
        "source_type": "governance_framework",
        "publisher": "NIST",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["NIST AI RMF 是治理框架，不替代项目内部审批记录。"],
        "evidence_summary": "NIST AI RMF Core 包含 govern、map、measure、manage 四类风险治理活动。",
        "quoted_excerpt_allowed": False,
    },
    "src_outcome_bias_replication": {
        "source_id": "src_outcome_bias_replication",
        "source_title": "Outcomes Affect Evaluations of Decision Quality: Replication and Extensions",
        "source_url": "https://rips-irsp.com/articles/10.5334/irsp.751",
        "source_type": "paper",
        "publisher": "International Review of Social Psychology",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["心理学决策研究，不是交易系统论文；用于支撑 outcome 与 decision quality 需要分离。"],
        "evidence_summary": "研究 outcome bias：人会因为结果好坏而偏置地评价相同决策质量。",
        "quoted_excerpt_allowed": False,
    },
    "src_concrete_problems_ai_safety": {
        "source_id": "src_concrete_problems_ai_safety",
        "source_title": "Concrete Problems in AI Safety",
        "source_url": "https://arxiv.org/abs/1606.06565",
        "source_type": "paper",
        "publisher": "arXiv",
        "published_at": "2016-06-21",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["通用 AI safety 论文，不直接定义交易标签 taxonomy。"],
        "evidence_summary": "将 reward hacking、distributional shift、scalable supervision 等列为实际 AI safety 问题。",
        "quoted_excerpt_allowed": False,
    },
    "src_deepmind_specification_gaming": {
        "source_id": "src_deepmind_specification_gaming",
        "source_title": "Specification gaming: the flip side of AI ingenuity",
        "source_url": "https://deepmind.google/blog/specification-gaming-the-flip-side-of-ai-ingenuity/",
        "source_type": "engineering_article",
        "publisher": "Google DeepMind",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["工程文章，适合支撑代理优化指标可能偏离意图，不是交易标签规范。"],
        "evidence_summary": "说明模型可能满足目标的字面定义，却没有达成人类真正想要的行为。",
        "quoted_excerpt_allowed": False,
    },
    "src_google_data_cards_playbook": {
        "source_id": "src_google_data_cards_playbook",
        "source_title": "The Data Cards Playbook",
        "source_url": "https://sites.research.google/datacardsplaybook/",
        "source_type": "framework_doc",
        "publisher": "Google Research",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "medium",
        "freshness": "stable",
        "limitations": ["数据文档框架，不直接定义交易标签枚举。"],
        "evidence_summary": "Data Cards 是面向 ML 数据集生命周期的结构化透明文档，可支撑标签、来源和数据集事实记录。",
        "quoted_excerpt_allowed": False,
    },
    "src_tfx_fairness_indicators": {
        "source_id": "src_tfx_fairness_indicators",
        "source_title": "Fairness Indicators | TFX",
        "source_url": "https://www.tensorflow.org/tfx/guide/fairness_indicators",
        "source_type": "official_doc",
        "publisher": "TensorFlow",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": ["公平性切片评估文档，不直接定义交易 regime 或 execution cost。"],
        "evidence_summary": "支持在大规模数据和模型中按切片计算常见评估指标，适合支撑分组/切片监控思想。",
        "quoted_excerpt_allowed": False,
    },
    "src_whylabs_segmenting_data": {
        "source_id": "src_whylabs_segmenting_data",
        "source_title": "Segmenting Data | WhyLabs Documentation",
        "source_url": "https://docs.whylabs.ai/docs/usecases-segmenting-data/",
        "source_type": "official_doc",
        "publisher": "WhyLabs",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["通用 ML segment monitoring，不直接解释交易 execution cost 本体。"],
        "evidence_summary": "说明 whylogs/WhyLabs 支持将 profiling 数据按 segment 记录和监控。",
        "quoted_excerpt_allowed": False,
    },
    "src_whylabs_monitor_manager": {
        "source_id": "src_whylabs_monitor_manager",
        "source_title": "Monitor Manager Overview | WhyLabs Documentation",
        "source_url": "https://docs.whylabs.ai/docs/monitor-manager/",
        "source_type": "official_doc",
        "publisher": "WhyLabs",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["通用监控文档，不给出交易策略版本或成本模型定义。"],
        "evidence_summary": "覆盖 data drift、data quality、concept/label drift、model performance 和按 segments 监控。",
        "quoted_excerpt_allowed": False,
    },
    "src_obp_docs": {
        "source_id": "src_obp_docs",
        "source_title": "Open Bandit Pipeline Documentation",
        "source_url": "https://zr-obp.readthedocs.io/en/latest/",
        "source_type": "official_doc",
        "publisher": "Open Bandit Pipeline",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": ["OPE 文档来自推荐/广告场景，不等同交易 paper/replay。"],
        "evidence_summary": "提供 logged bandit feedback 与 off-policy evaluation 工具，适合支撑未执行候选的反事实评估边界。",
        "quoted_excerpt_allowed": False,
    },
    "src_logged_bandit_feedback": {
        "source_id": "src_logged_bandit_feedback",
        "source_title": "Off-Policy Evaluation and Learning from Logged Bandit Feedback",
        "source_url": "https://arxiv.org/abs/1808.00232",
        "source_type": "paper",
        "publisher": "arXiv",
        "published_at": "2018-08-01",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "medium",
        "freshness": "stable",
        "limitations": ["logged bandit 论文不直接证明交易 paper/slippage/fill 假设。"],
        "evidence_summary": "说明从历史策略记录的 action-context feedback 学习和评估新策略存在统计挑战。",
        "quoted_excerpt_allowed": False,
    },
    "src_google_sre_canarying": {
        "source_id": "src_google_sre_canarying",
        "source_title": "Canary Release: Deployment Safety and Efficiency",
        "source_url": "https://sre.google/workbook/canarying-releases/",
        "source_type": "official_doc",
        "publisher": "Google SRE",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["软件发布实践来源，不直接定义交易 capital/risk limits。"],
        "evidence_summary": "说明 canary release 用小流量暴露新版本以获得安全信心并降低发布风险。",
        "quoted_excerpt_allowed": False,
    },
    "src_mlflow_tracking": {
        "source_id": "src_mlflow_tracking",
        "source_title": "ML Experiment Tracking | MLflow",
        "source_url": "https://mlflow.org/docs/latest/ml/tracking/",
        "source_type": "official_doc",
        "publisher": "MLflow",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["实验追踪文档不定义 CEK-TA 审批状态。"],
        "evidence_summary": "MLflow Tracking 用于记录参数、代码版本、指标和输出文件，支撑再训练触发与训练运行审计。",
        "quoted_excerpt_allowed": False,
    },
    "src_mlflow_dataset_tracking": {
        "source_id": "src_mlflow_dataset_tracking",
        "source_title": "MLflow Dataset Tracking",
        "source_url": "https://mlflow.org/docs/latest/ml/dataset/",
        "source_type": "official_doc",
        "publisher": "MLflow",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["数据集追踪文档不规定交易标签策略。"],
        "evidence_summary": "说明 MLflow 可追踪、版本化和管理训练、验证、评估数据集，并保留数据到模型预测的 lineage。",
        "quoted_excerpt_allowed": False,
    },
    "src_sklearn_calibration_curve_example": {
        "source_id": "src_sklearn_calibration_curve_example",
        "source_title": "Probability Calibration curves | scikit-learn",
        "source_url": "https://scikit-learn.org/stable/auto_examples/calibration/plot_calibration_curve.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["校准曲线文档不定义交易阈值策略。"],
        "evidence_summary": "展示用 calibration curves / reliability diagrams 评估预测概率校准情况。",
        "quoted_excerpt_allowed": False,
    },
    "src_sklearn_brier_score": {
        "source_id": "src_sklearn_brier_score",
        "source_title": "brier_score_loss | scikit-learn",
        "source_url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["Brier 分数是概率预测指标，不直接决定交易阈值。"],
        "evidence_summary": "定义 Brier score loss，可用于衡量概率预测质量。",
        "quoted_excerpt_allowed": False,
    },
    "src_openai_structured_outputs": {
        "source_id": "src_openai_structured_outputs",
        "source_title": "Structured model outputs | OpenAI API",
        "source_url": "https://developers.openai.com/api/docs/guides/structured-outputs",
        "source_type": "official_doc",
        "publisher": "OpenAI",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["结构化输出约束 schema，不证明模型事实正确。"],
        "evidence_summary": "Structured Outputs 用 JSON Schema 约束模型响应结构，适合支撑 schema_valid_rate 门禁。",
        "quoted_excerpt_allowed": False,
    },
    "src_ragas_faithfulness": {
        "source_id": "src_ragas_faithfulness",
        "source_title": "Faithfulness | Ragas",
        "source_url": "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/",
        "source_type": "official_doc",
        "publisher": "Ragas",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "medium",
        "score": 78,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["RAG 评估指标不是交易策略有效性证据。"],
        "evidence_summary": "Faithfulness 衡量回答是否与检索上下文事实一致，适合支撑 citation/unsupported claim 评估。",
        "quoted_excerpt_allowed": False,
    },
    "src_hf_trl_sft_trainer": {
        "source_id": "src_hf_trl_sft_trainer",
        "source_title": "SFT Trainer | Hugging Face TRL",
        "source_url": "https://huggingface.co/docs/trl/en/sft_trainer",
        "source_type": "official_doc",
        "publisher": "Hugging Face",
        "published_at": None,
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": ["SFT 工具文档说明如何训练，不说明何时应该训练。"],
        "evidence_summary": "TRL 提供 SFTTrainer 进行监督微调，适合作为可选 SFT/LoRA 实施来源。",
        "quoted_excerpt_allowed": False,
    },
}

SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "P40-C04": {
        "source_ids": [
            "src_cek_ta_phase40_feedback_dataset_contract",
            "src_outcome_bias_replication",
            "src_concrete_problems_ai_safety",
            "src_google_data_cards_playbook",
        ],
        "claim_patch": (
            "PnL-only label 只能描述结果，不能充分代表交易决策质量；标签必须分离结果、过程、规则合规、"
            "风控合规、执行质量和人工复核结论。"
        ),
        "supplemental_notes": [
            "CEK-TA contract 提供 label_schema_v1：good_loss、bad_win、rule_violation、risk_violation、execution_quality、human_review_outcome。",
            "outcome bias 支撑结果好坏会扭曲决策质量评价。",
            "Concrete Problems in AI Safety 支撑单一代理目标可能诱发 reward hacking 或目标错配。",
            "Data Cards 支撑数据集和标签来源需要结构化记录。"
        ],
        "remaining_boundary": "AI Engineering 只定义标签治理，不定义交易风控阈值、执行质量公式或 fill/cost 模型。",
    },
    "P40-C05": {
        "source_ids": [
            "src_cek_ta_phase40_feedback_dataset_contract",
            "src_outcome_bias_replication",
            "src_deepmind_specification_gaming",
            "src_concrete_problems_ai_safety",
        ],
        "claim_patch": (
            "亏损不必然代表坏决策，盈利也不必然代表好决策；good_loss/bad_win 必须由人审规则、"
            "决策时证据、规则合规和执行上下文共同判定。"
        ),
        "supplemental_notes": [
            "outcome bias 直接支撑结果与决策质量需要分离。",
            "specification gaming/reward hacking 支撑只优化表面结果会产生错误激励。",
            "CEK-TA contract 要求 HumanReviewRecord 与 label provenance。"
        ],
        "remaining_boundary": "good_loss/bad_win 不能转化为买卖信号或实盘阈值。",
    },
    "P40-C08": {
        "source_ids": [
            "src_cek_ta_phase40_drift_retraining_contract",
            "src_whylabs_segmenting_data",
            "src_whylabs_monitor_manager",
            "src_tfx_fairness_indicators",
        ],
        "claim_patch": (
            "交易 AI 漂移监控应按 AI monitoring slice 记录 strategy_version_ref、symbol_group、"
            "regime_label_ref 和 execution_cost_ref；这些字段是切片维度和引用，不是交易规则本体。"
        ),
        "supplemental_notes": [
            "WhyLabs 支撑按 segment 记录和监控数据、label/concept drift 与模型性能。",
            "TFX/Fairness Indicators 支撑按 slice 计算模型指标。",
            "CEK-TA drift contract 明确 execution_cost_drift 需要 Trading Engineering 引用。"
        ],
        "remaining_boundary": "不得在 AI Engineering 内定义 market regime 规则、成本模型、成交假设或执行参数。",
    },
    "P40-C10-R1": {
        "source_ids": [
            "src_cek_ta_phase40_drift_retraining_contract",
            "src_mlflow_tracking",
            "src_mlflow_dataset_tracking",
            "src_nist_ai_rmf_core",
        ],
        "claim_patch": (
            "再训练触发必须形成 RetrainingTriggerDecision，记录 trigger_type、触发证据、样本窗口、"
            "dataset_version、目标模型角色、reason_codes、reviewer 和 approval_ref。"
        ),
        "supplemental_notes": [
            "MLflow Tracking 支撑参数、代码版本、指标和产物记录。",
            "MLflow Dataset Tracking 支撑训练、验证、评估数据 lineage。",
            "NIST AI RMF Core 支撑 govern/map/measure/manage 风险治理链路。",
            "CEK-TA retraining contract 明确触发不是上线许可。"
        ],
        "remaining_boundary": "再训练触发只允许 candidate training request，不允许自动替换 champion 或启用 hard gate。",
    },
    "P40-C11-R1": {
        "source_ids": [
            "src_cek_ta_phase40_drift_retraining_contract",
            "src_sklearn_calibration_curve_example",
            "src_sklearn_brier_score",
            "src_tfdv_get_started",
        ],
        "claim_patch": (
            "再训练后必须重新生成 RecalibrationReport 和 ThresholdStabilityReport，至少覆盖 Brier、"
            "calibration curve/reliability diagram、关键切片可靠性和阈值压力。"
        ),
        "supplemental_notes": [
            "scikit-learn calibration curve 支撑概率可靠性图。",
            "Brier score 支撑概率预测质量评估。",
            "TFDV 支撑数据 skew/drift 与 schema 检查。",
            "CEK-TA contract 明确再训练后必须重新校准。"
        ],
        "remaining_boundary": "概率校准和阈值稳定性报告不能直接给出交易仓位、止损或执行参数。",
    },
    "P40-C13": {
        "source_ids": [
            "src_cek_ta_phase40_champion_release_contract",
            "src_google_sre_canarying",
            "src_obp_docs",
            "src_logged_bandit_feedback",
        ],
        "claim_patch": (
            "challenger promotion gate 应拆成 offline_eval、shadow_eval、paper_or_replay_eval、"
            "soft_gate_eval 与 canary_plan；每阶段只提供证据，不自动上线。"
        ),
        "supplemental_notes": [
            "Google SRE canary 支撑小流量验证发布风险。",
            "OBP/OPE 支撑用 logged feedback 评估反事实策略存在统计挑战。",
            "CEK-TA release contract 定义 shadow/paper/canary 的边界和审批。"
        ],
        "remaining_boundary": "paper/replay 的成交、滑点、成本假设必须引用 Trading Engineering。",
    },
    "P40-C17": {
        "source_ids": [
            "src_cek_ta_phase38_training_eval_contract",
            "src_cek_ta_phase38_rag_reason_taxonomy_contract",
            "src_openai_structured_outputs",
            "src_ragas_faithfulness",
            "src_hf_trl_sft_trainer",
        ],
        "claim_patch": (
            "SFT/LoRA 触发必须由 eval 证明 schema_valid_rate、citation_resolved_rate、"
            "reason_code_consistency 或 unsupported_claim_rate 长期失败；优先 RAG/prompt 修复。"
        ),
        "supplemental_notes": [
            "OpenAI Structured Outputs 支撑 schema 有机器约束。",
            "Ragas faithfulness 支撑回答与检索上下文一致性评估。",
            "Hugging Face TRL SFTTrainer 只作为训练工具来源，不作为触发条件来源。",
            "CEK-TA reason taxonomy contract 约束 reason code 和 citation。"
        ],
        "remaining_boundary": "SFT/LoRA 不能作为事实来源，也不能赋予 LLM final gate 权限。",
    },
    "P40-C18-R1": {
        "source_ids": [
            "src_cek_ta_phase40_feedback_dataset_contract",
            "src_concrete_problems_ai_safety",
            "src_deepmind_specification_gaming",
            "src_logged_bandit_feedback",
            "src_google_data_cards_playbook",
        ],
        "claim_patch": (
            "自标注、模型生成标签和选择性日志必须记录 label_source、labeler_type、"
            "behavior_policy_ref、human_review_ref 和 provenance，避免反馈回路污染。"
        ),
        "supplemental_notes": [
            "reward hacking/specification gaming 支撑代理目标可能偏离真实意图。",
            "logged bandit feedback 支撑历史策略记录与新策略评估之间存在偏差和 OPE 风险。",
            "Data Cards 支撑数据与标签来源透明记录。",
            "CEK-TA contract 禁止 FeedbackRecord 直接成为训练真值。"
        ],
        "remaining_boundary": "候选只定义标签来源治理，不定义具体交易标签真值或项目私有 label。"
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
    source_refs = candidate.setdefault("source_refs", [])
    existing_ids = {source.get("source_id") for source in source_refs if isinstance(source, dict)}
    added: list[dict[str, Any]] = []
    for source_id in source_ids:
        if source_id in existing_ids:
            continue
        source = SOURCE_LIBRARY[source_id]
        copied = dict(source)
        source_refs.append(copied)
        added.append(copied)
        existing_ids.add(source_id)
    return added


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
    quality["overall_reliability"] = "high" if primary_count >= 3 and low_count == 0 else "medium"
    quality["score"] = max(int(quality.get("score") or 0), 86 if primary_count >= 3 else 82)
    quality["score_version"] = "1.1.0"
    quality["primary_source_count"] = primary_count
    quality["supporting_source_count"] = max(0, len(source_refs) - primary_count)
    quality["low_reliability_source_count"] = low_count
    quality["limitations"] = list(
        dict.fromkeys(
            list(quality.get("limitations") or [])
            + ["补证后仍需外部 AI/人工二审确认 claim-specific 充分性，不能直接转 reviewed。"]
        )
    )


def candidate_key(candidate: dict[str, Any]) -> str:
    task_id = str(candidate.get("research_task_id"))
    if task_id in SUPPLEMENTS:
        return task_id
    return task_id.replace("-R1", "")


def supplement_candidate(path: Path, candidate: dict[str, Any]) -> dict[str, Any] | None:
    key = candidate_key(candidate)
    supplement = SUPPLEMENTS.get(key)
    if not supplement:
        return None

    added_sources = merge_sources(candidate, supplement["source_ids"])
    claim = candidate.setdefault("claim", {})
    original_statement = claim.get("statement")
    claim["statement"] = supplement["claim_patch"]
    claim["evidence_summary"] = "；".join(
        source["evidence_summary"] for source in candidate.get("source_refs", [])[-min(4, len(candidate.get("source_refs", []))):]
    )
    claim["claim_strength"] = "medium"

    applicability = candidate.setdefault("applicability", {})
    limitations = applicability.setdefault("limitations", [])
    if isinstance(limitations, list):
        limitations.append(supplement["remaining_boundary"])
        applicability["limitations"] = list(dict.fromkeys(limitations))

    candidate.setdefault("phase40_trace", {})["supplemental_evidence_ready"] = True
    candidate["phase40_trace"]["supplemental_evidence_added_at"] = TODAY

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已按严格审计意见补充来源、边界和二审说明；等待外部二审。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["next_action"] = "export_ai_audit"

    conversion = candidate.setdefault("conversion_target", {})
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conversion["target_review_status"] = "draft"

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "supplemented candidate awaiting reaudit; not reviewed, approved, default guidance, or hard gate."

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["conflict_status"] = "potential" if str(candidate.get("research_task_id", "")).endswith("-R1") else "none"
    conflict["resolution_summary"] = (
        "补证后未发现直接理论冲突；仍需二审确认来源充分性和跨分支边界。"
    )

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_supplemental_evidence"
    review["reviewed_at"] = TODAY
    review["open_questions"] = ["请二审确认补证后是否可进入 formal reviewed draft，且不得进入 approved/default guidance。"]
    review.setdefault("ai_audit", {})["supplemental_evidence"] = {
        "status": "ready_for_reaudit",
        "added_at": TODAY,
        "previous_statement": original_statement,
        "patched_statement": supplement["claim_patch"],
        "added_source_ids": [source["source_id"] for source in added_sources],
        "all_supplemental_source_ids": supplement["source_ids"],
        "supplemental_notes": supplement["supplemental_notes"],
        "remaining_boundary": supplement["remaining_boundary"],
        "reaudit_request": (
            "请判断补证后是否 accepted_for_draft；如果仍不足，请只返回 needs_more_evidence 或 rejected。"
        ),
    }
    update_source_quality(candidate)
    append_audit_log(candidate, "phase40_supplemental_evidence_ready", "按严格审计意见补证并准备二审。")
    write_json(path, candidate)
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "path": repo_rel(path),
        "added_source_ids": [source["source_id"] for source in added_sources],
        "total_source_count": len(candidate.get("source_refs") or []),
    }


def load_target_candidates() -> list[tuple[Path, dict[str, Any]]]:
    targets: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase40_*.json")):
        candidate = read_json(path)
        if candidate.get("workflow", {}).get("queue_group") == "needs_more_evidence":
            if str(candidate.get("research_task_id")) in SUPPLEMENTS:
                targets.append((path, candidate))
    return targets


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id"))
        source_refs = candidate.get("source_refs") or []
        ai_audit = candidate.get("review", {}).get("ai_audit", {})
        if len(source_refs) < 4:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_4"})
        if ai_audit.get("supplemental_evidence", {}).get("status") != "ready_for_reaudit":
            failures.append({"candidate_id": candidate_id, "failure": "missing_supplemental_evidence_status"})
        if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_not_denied"})
        if candidate.get("conversion_target", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "conversion_default_guidance_not_false"})
        if candidate.get("workflow", {}).get("visible_in_default_guidance_queue") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "visible_default_queue_not_false"})
    return {
        "gate_id": "phase40_p0_core_supplemental_reaudit_quality_gate",
        "generated_at": TODAY,
        "candidate_count": len(candidates),
        "expected_count": len(SUPPLEMENTS),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures and len(candidates) == len(SUPPLEMENTS) else "fail",
    }


def build_audit_package(candidates: list[dict[str, Any]], report: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": "phase40_p0_core_supplemental_reaudit_package_20260610",
        "package_type": "candidate_ai_reaudit_package",
        "generated_at": TODAY,
        "phase": "40",
        "source_audit_result_id": "audit_result_phase40_p0_core_continuous_learning_20260610_strict_v1",
        "source_package_id": "phase40_candidate_audit_package_20260610",
        "title": "Phase 40 P0-Core needs_more_evidence 补证后二审包",
        "purpose": "只审计 8 条已补证候选，判断是否可进入 formal draft/reviewed 准备链路。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "二审可以给出 accepted_for_draft，但不得直接给 approved。",
            "reviewed_allowed=true 只表示可由 Codex 后续生成 formal reviewed draft，不等于 approved。",
            "所有 hard_gate_allowed 必须为 false，除非另有人工治理任务。",
            "Trading Engineering 规则本体仍不得混入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "确认补证是否充分、边界是否正确、是否仍需要补来源或应拒绝。",
            "focus_checks": [
                "补充来源是否直接支撑 claim，而不是只支撑通用 ML 概念。",
                "内部 CEK-TA 契约是否只作为边界和工作流证据，不替代外部专业来源。",
                "是否误把交易规则、成本模型、market regime 定义写入 AI Engineering。",
                "是否保持 default_guidance_allowed=false 和 hard_gate_allowed=false。",
                "若 accepted_for_draft，请明确 required_patch_notes 以便 Codex 转 formal reviewed draft。",
            ],
            "required_output_schema": {
                "audit_result_id": "audit_result_phase40_p0_core_supplemental_reaudit_20260610_v1",
                "source_package_id": "phase40_p0_core_supplemental_reaudit_package_20260610",
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
                },
            },
        },
        "quality_gate": report["quality_gate"],
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def main() -> int:
    targets = load_target_candidates()
    touched: list[dict[str, Any]] = []
    supplemented: list[dict[str, Any]] = []
    for path, candidate in targets:
        result = supplement_candidate(path, candidate)
        if result:
            touched.append(result)
            supplemented.append(read_json(path))

    gate = quality_gate(supplemented)
    report = {
        "report_id": "phase40_p0_core_supplemental_evidence_report",
        "generated_at": TODAY,
        "scope": "Phase 40 P0-Core needs_more_evidence supplemental evidence",
        "touched_count": len(touched),
        "touched_candidates": touched,
        "quality_gate": gate,
        "audit_package_path": repo_rel(AUDIT_PACKAGE_PATH),
        "boundary": "补证后仍是 candidate；不创建 formal reviewed、approved、default guidance 或 hard gate。",
    }
    write_json(REPORT_PATH, report)
    write_json(AUDIT_PACKAGE_PATH, build_audit_package(supplemented, report))
    print(json.dumps({"ok": gate["gate_status"] == "pass", "report": repo_rel(REPORT_PATH), "audit_package": repo_rel(AUDIT_PACKAGE_PATH), "candidate_count": len(supplemented)}, ensure_ascii=True))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
