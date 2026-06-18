"""Supplement Phase 41 P0-Extended/P1 needs-more-evidence candidates.

The output is a focused reaudit package for the six candidates that the strict
audit marked as needs_more_evidence. The script preserves candidate status and
does not create formal reviewed/approved knowledge.
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
TASK_ID = "CEK-TA-332"
SOURCE_AUDIT_RESULT_ID = "audit_result_phase41_extended_p1_candidate_audit_package_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase41_extended_p1_candidate_audit_package_20260610"
REAUDIT_PACKAGE_ID = "phase41_extended_p1_supplemental_reaudit_package_20260610"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase41_extended_p1_supplemental_evidence_report.json", start_file=__file__)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{REAUDIT_PACKAGE_ID}.json", start_file=__file__)
RESEARCH_PATH = resolve_repo_path("docs", "research", "phase41_extended_p1_supplemental_research.md", start_file=__file__)


SOURCE_LIBRARY: dict[str, dict[str, Any]] = {
    "src_shap_causal_warning": {
        "source_id": "src_shap_causal_warning",
        "source_title": "Be careful when interpreting predictive models in search of causal insights - SHAP documentation",
        "source_url": "https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html",
        "source_type": "official_doc",
        "publisher": "SHAP",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 attribution 不是因果证据，不证明任何交易特征稳定有效。"],
        "evidence_summary": "SHAP 文档专门提醒预测模型解释不应被直接当作因果洞察。",
        "quoted_excerpt_allowed": False,
    },
    "src_phase41_runtime_contract": {
        "source_id": "src_phase41_runtime_contract",
        "source_title": "CEK-TA Phase 41 Hybrid Scoring Runtime Contract",
        "source_url": "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "draft",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约只证明 CEK-TA 字段和权限边界，不替代外部专业来源。"],
        "evidence_summary": "契约明确 top_features 只能用于审计和 debug，不能作为因果结论或 final gate 权限。",
        "quoted_excerpt_allowed": False,
    },
    "src_phase41_training_data_contract": {
        "source_id": "src_phase41_training_data_contract",
        "source_title": "CEK-TA Phase 41 Tabular and Qwen3 Training Data Contract",
        "source_url": "docs/contracts/phase41_tabular_llm_training_data_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "draft",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["内部契约只定义数据隔离和样本池字段，不证明模型效果。"],
        "evidence_summary": "契约要求 gold/eval 样本不得进入训练池，并定义 split、feature、label 和审计样本隔离规则。",
        "quoted_excerpt_allowed": False,
    },
    "src_ohem_paper": {
        "source_id": "src_ohem_paper",
        "source_title": "Training Region-based Object Detectors with Online Hard Example Mining",
        "source_url": "https://arxiv.org/abs/1604.03540",
        "source_type": "research_paper",
        "publisher": "arXiv",
        "published_at": "2016-04-12",
        "accessed_at": TODAY,
        "version": None,
        "reliability": "medium",
        "score": 78,
        "relevance": "medium",
        "freshness": "stable",
        "limitations": ["来源来自计算机视觉 hard example mining 场景，只能支撑采样增强概念，不能直接证明交易 scorer 效果。"],
        "evidence_summary": "论文提出 online hard example mining，用于选择困难样本改善训练；迁移到交易时必须作为复核采样增强并保留偏差控制。",
        "quoted_excerpt_allowed": False,
    },
    "src_active_learning_survey": {
        "source_id": "src_active_learning_survey",
        "source_title": "An Active Learning Approach with Uncertainty, Representativeness, and Diversity",
        "source_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4144157/",
        "source_type": "research_paper",
        "publisher": "NIH / PMC",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "medium",
        "score": 80,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["支撑 active learning 采样原则，不证明 hard-example mining 可以提高交易质量。"],
        "evidence_summary": "论文讨论不确定性、代表性和多样性采样，支撑 active learning 需要防止采样偏差。",
        "quoted_excerpt_allowed": False,
    },
    "src_google_rag_finetune_guide": {
        "source_id": "src_google_rag_finetune_guide",
        "source_title": "To tune or not to tune: A guide to leveraging your data with LLMs",
        "source_url": "https://cloud.google.com/blog/products/ai-machine-learning/to-tune-or-not-to-tune-a-guide-to-leveraging-your-data-with-llms",
        "source_type": "engineering_article",
        "publisher": "Google Cloud",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["工程指南支撑方法选择，不替代 CEK-TA 的审计数据集和 RAG 评测契约。"],
        "evidence_summary": "Google Cloud 指南比较 prompt、RAG 和 fine-tuning 的适用问题，支撑先建立检索、提示和评测基线再决定训练权重。",
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
        "limitations": ["支撑 RAG pipeline 检索和生成评估，不定义交易发布治理。"],
        "evidence_summary": "Promptfoo 文档要求同时评估 document retrieval 和 LLM output generation。",
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
        "limitations": ["支撑模型 shadow testing，不证明 paper/replay 与实盘成交等价。"],
        "evidence_summary": "SageMaker shadow tests 将请求副本路由到 shadow variant，用于候选与生产变体比较。",
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
        "limitations": ["支撑 shadow 环境比较，不等同于实盘交易证明。"],
        "evidence_summary": "Microsoft playbook 将 shadow testing 描述为复制生产流量到候选环境并比较差异。",
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
        "limitations": ["Trading Engineering 来源，只能作为 paper/replay 非等价提示，不定义 Phase 41 交易本体。"],
        "evidence_summary": "QuantConnect 说明 paper trading 使用实时数据、虚拟资金和模拟 fills。",
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
        "limitations": ["仅作为 fill/cost/execution 假设引用边界，不把 fill model 本体写入 AI Engineering。"],
        "evidence_summary": "QuantConnect 文档说明 fill models 决定成交价格和数量，并可结合 spread/slippage 模拟成交。",
        "quoted_excerpt_allowed": False,
    },
    "src_nist_least_privilege": {
        "source_id": "src_nist_least_privilege",
        "source_title": "Least Privilege - NIST CSRC Glossary",
        "source_url": "https://csrc.nist.gov/glossary/term/least_privilege",
        "source_type": "security_standard",
        "publisher": "NIST",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["安全原则来源，不定义 CEK-TA MCP tool schema。"],
        "evidence_summary": "NIST least privilege 原则支撑外部项目只获得必要只读权限和最小路径访问。",
        "quoted_excerpt_allowed": False,
    },
    "src_owasp_llm_top10": {
        "source_id": "src_owasp_llm_top10",
        "source_title": "OWASP Top 10 for LLM Applications",
        "source_url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "source_type": "security_standard",
        "publisher": "OWASP",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": ["支撑 LLM 应用安全边界，不替代本项目 MCP 权限契约。"],
        "evidence_summary": "OWASP LLM 风险框架支撑 tool 权限、提示注入和数据边界需要显式控制。",
        "quoted_excerpt_allowed": False,
    },
    "src_google_sre_slo": {
        "source_id": "src_google_sre_slo",
        "source_title": "Service Level Objectives - Google SRE Book",
        "source_url": "https://sre.google/sre-book/service-level-objectives/",
        "source_type": "book",
        "publisher": "Google SRE",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["支撑 SLO/预算思想，不定义交易系统放行策略。"],
        "evidence_summary": "Google SRE SLO 来源支撑以明确目标、指标和预算管理服务可靠性。",
        "quoted_excerpt_allowed": False,
    },
    "src_google_sre_overload": {
        "source_id": "src_google_sre_overload",
        "source_title": "Handling Overload - Google SRE Book",
        "source_url": "https://sre.google/sre-book/handling-overload/",
        "source_type": "book",
        "publisher": "Google SRE",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["支撑过载和降级处理，不授权交易自动放行。"],
        "evidence_summary": "Google SRE overload 来源支撑请求过载时需要降级、拒绝或保护系统可用性。",
        "quoted_excerpt_allowed": False,
    },
    "src_fca_algo_trading_review": {
        "source_id": "src_fca_algo_trading_review",
        "source_title": "Algorithmic Trading Compliance in Wholesale Markets",
        "source_url": "https://www.fca.org.uk/publication/multi-firm-reviews/algorithmic-trading-compliance-wholesale-markets.pdf",
        "source_type": "regulator_review",
        "publisher": "FCA",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["监管综述支撑算法交易控制和治理，不定义本项目具体阈值。"],
        "evidence_summary": "FCA 综述强调算法交易需要治理、测试、变更控制、监控和 kill switch 等控制。",
        "quoted_excerpt_allowed": False,
    },
    "src_sec_knight_capital": {
        "source_id": "src_sec_knight_capital",
        "source_title": "SEC Charges Knight Capital With Violations of Market Access Rule",
        "source_url": "https://www.sec.gov/newsroom/press-releases/2013-222",
        "source_type": "regulator_release",
        "publisher": "SEC",
        "published_at": "2013-10-16",
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "limitations": ["事故监管来源用于说明自动化交易控制缺失风险，不证明某个模型有效。"],
        "evidence_summary": "SEC Knight Capital 案例说明自动化交易系统缺乏充分控制、审查和保护会造成重大损失。",
        "quoted_excerpt_allowed": False,
    },
}


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "P41-A07": {
        "candidate_file": "cand_20260610_phase41_p41_a07_feature_attribution_top_features_final_gate_001.json",
        "source_ids": ["src_shap_causal_warning", "src_phase41_runtime_contract"],
        "claim_patch": "feature attribution、SHAP、permutation importance 和 top_features 只能作为模型调试与审计线索；不得声明因果关系，不得作为交易规则证据，也不得作为 deterministic final gate 的直接放行或阻断依据。",
        "supplemental_notes": [
            "SHAP 官方 causal-warning 来源直接支撑 attribution 不能被当作因果洞察。",
            "Phase 41 runtime contract 明确 top_features 只能用于审计和 debug，不能作为 final gate 权限。",
        ],
        "remaining_boundary": "causal_claim_allowed=false；final_gate_decision_allowed=false；任何 attribution 结论进入交易解释时必须带非因果、非交易规则证据说明。",
        "extra_trace": {"causal_claim_allowed": False, "final_gate_decision_allowed": False},
    },
    "P41-B06": {
        "candidate_file": "cand_20260610_phase41_p41_b06_active_learning_hard_example_mining_gold_eval_001.json",
        "source_ids": ["src_active_learning_survey", "src_ohem_paper", "src_phase41_training_data_contract"],
        "claim_patch": "active learning 或 hard-example mining 只能作为复核采样增强；必须同时保留 random_control_sample、stratified_sample、sampling_bias_review 和 no_gold_eval_contamination 标记，不能污染 gold/eval 池或替代正式评估。",
        "supplemental_notes": [
            "active learning 来源支撑不确定性、代表性和多样性采样需要共同考虑。",
            "OHEM 来源只支撑 hard-example mining 概念，不直接证明交易样本有效，因此必须保留迁移限制。",
            "Phase 41 training data contract 明确 gold/eval 隔离和样本池边界。",
        ],
        "remaining_boundary": "hard-example mining 是采样增强，不是性能保证；gold/eval 池污染时必须阻断训练或重新切分。",
        "extra_trace": {
            "required_sampling_controls": [
                "active_learning_sample",
                "random_control_sample",
                "stratified_sample",
                "sampling_bias_review",
                "no_gold_eval_contamination",
            ]
        },
    },
    "P41-E07": {
        "candidate_file": "cand_20260610_phase41_p41_e07_rag_first_prompt_sft_lora_001.json",
        "source_ids": ["src_google_rag_finetune_guide", "src_promptfoo_rag_eval", "src_phase41_runtime_contract"],
        "claim_patch": "外接项目应先建立 RAG、prompt 和 eval baseline；只有在 schema、citation、reason code 或审计流程稳定性仍持续失败，并且评测能证明提示/检索修正不足时，才进入 SFT/LoRA 权重训练。",
        "supplemental_notes": [
            "Google Cloud 指南支撑 prompt、RAG 与 fine-tuning 应按问题类型选择。",
            "Promptfoo RAG evaluation 来源支撑先评估 retrieval 与 generation，再判断是否需要模型训练。",
            "Phase 41 runtime contract 将 Qwen3 限定为 audit assistant，不允许训练交易概率或 final gate 权限。",
        ],
        "remaining_boundary": "SFT/LoRA 只能训练格式、reason code、引用习惯和审计流程；不得训练交易概率、买卖点或 final gate 决策。",
        "extra_trace": {"rag_prompt_eval_baseline_required": True, "sft_lora_requires_persistent_eval_failure": True},
    },
    "P41-F04": {
        "candidate_file": "cand_20260610_phase41_p41_f04_champion_challenger_offline_shadow_paper_soft_gate_champion_paper_replay_fill_cost_execution_phase_37_ai_engineering_001.json",
        "source_ids": [
            "src_aws_sagemaker_shadow_tests",
            "src_microsoft_shadow_testing",
            "src_quantconnect_paper_trading",
            "src_quantconnect_trade_fills",
            "src_phase41_runtime_contract",
        ],
        "claim_patch": "champion/challenger 晋级必须按 offline_eval、shadow_eval、paper_or_replay_eval、soft_gate_eval、canary_plan 和 owner_approval_ref 分阶段记录；paper/replay 只提供模拟证据，必须声明与 live execution、fill、fee、slippage、latency 的非等价边界。",
        "supplemental_notes": [
            "AWS 与 Microsoft 来源支撑 shadow testing 的候选/生产对照方式。",
            "QuantConnect paper trading 与 trade fills 来源支撑 paper/fill 假设和实盘非等价边界。",
            "Phase 41 runtime contract 要求 AI Engineering 只读取 Trading refs，不定义 fill/cost/execution 本体。",
        ],
        "remaining_boundary": "AI Engineering 只管理晋级证据和引用字段；fill model、手续费、滑点、market impact、订单状态机和执行延迟本体归 Phase 37 / Trading Engineering。",
        "extra_trace": {
            "promotion_stages": [
                "offline_eval",
                "shadow_eval",
                "paper_or_replay_eval",
                "soft_gate_eval",
                "canary_plan",
                "owner_approval_ref",
            ],
            "paper_replay_live_equivalence_claim_allowed": False,
        },
    },
    "P41-F07": {
        "candidate_file": "cand_20260610_phase41_p41_f07_cek_ta_resolver_001.json",
        "source_ids": ["src_nist_least_privilege", "src_owasp_llm_top10", "src_phase41_runtime_contract"],
        "claim_patch": "任何平台接入必须保留 CEK-TA 知识检索只读、路径 resolver、最小权限和可移植配置边界；外部项目不得通过 MCP/adapter 直接写 CEK-TA，不得绕过 allowed_paths/forbidden_paths 或把本机绝对路径写成运行时依赖。",
        "supplemental_notes": [
            "NIST least privilege 支撑最小权限访问原则。",
            "OWASP LLM Top 10 支撑 LLM tool 安全、提示注入和数据边界需要显式控制。",
            "Phase 41 runtime contract 明确 MCP/SearchLab 只读正式知识索引。",
        ],
        "remaining_boundary": "read_only=true；no_write_back_to_cek_ta=true；所有运行时路径必须来自 resolver 或显式环境变量。",
        "extra_trace": {
            "read_only": True,
            "no_write_back_to_cek_ta": True,
            "required_fields": ["resolver_version", "allowed_paths", "forbidden_paths", "portable_config_ref"],
        },
    },
    "P41-F08": {
        "candidate_file": "cand_20260610_phase41_p41_f08_hybrid_scoring_runtime_scorer_calibrator_rag_qwen3_final_gate_latency_budget_timeout_fallback_fail_to_review_fail_closed_001.json",
        "source_ids": [
            "src_google_sre_slo",
            "src_google_sre_overload",
            "src_fca_algo_trading_review",
            "src_sec_knight_capital",
            "src_phase41_runtime_contract",
        ],
        "claim_patch": "hybrid scoring runtime 必须为 scorer、calibrator、RAG、Qwen3 audit 和 final gate 分别定义 latency_budget_ms、timeout_ms、fallback_action、fail_to_review 或 fail_closed 策略；任何组件故障不得默认 allow，paper/live 下 final_gate_timeout 必须 fail_closed。",
        "supplemental_notes": [
            "Google SRE 来源支撑 SLO、延迟预算、过载保护和降级思路。",
            "FCA 算法交易治理和 SEC Knight Capital 案例支撑自动化交易控制、测试、监控和 kill switch 的必要性。",
            "Phase 41 runtime contract 已定义 latency/fallback schema 和 fail-closed 硬规则。",
        ],
        "remaining_boundary": "fallback 只能路由到 human review、safe degradation、rule baseline 或 fail_closed；不得在缺少 final-gate policy 时自动 allow/block。",
        "extra_trace": {
            "required_runtime_fields": [
                "latency_budget_ms",
                "timeout_ms",
                "fallback_action",
                "fail_closed_or_fail_to_review",
                "kill_switch_ref",
            ]
        },
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


def append_unique(items: list[Any], values: list[Any]) -> list[Any]:
    merged = list(items)
    for value in values:
        if value not in merged:
            merged.append(value)
    return merged


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


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    audit_log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def enforce_candidate_safety(candidate: dict[str, Any]) -> None:
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
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False


def update_source_quality(candidate: dict[str, Any]) -> None:
    source_refs = candidate.get("source_refs") or []
    primary_count = sum(
        1
        for source in source_refs
        if source.get("source_type")
        in {"official_doc", "paper", "research_paper", "governance_framework", "security_standard", "regulator_release", "regulator_review", "book", "internal_contract"}
    )
    low_count = sum(1 for source in source_refs if source.get("reliability") == "low")
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high" if primary_count >= 4 and low_count == 0 else "medium"
    quality["score"] = max(int(quality.get("score") or 0), 88 if primary_count >= 4 else 84)
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
    applicability["limitations"] = append_unique(list(applicability.get("limitations") or []), [supplement["remaining_boundary"]])

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已按 Phase 41 P0-Extended/P1 严格审计意见补充 claim-specific 来源、内部契约和边界说明；等待外部二审。"
    status["updated_at"] = TODAY

    enforce_candidate_safety(candidate)

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none"
    conflict["approval_allowed"] = False
    conflict["resolution_summary"] = "补证后未发现直接理论冲突；仍需二审确认来源充分性和 AI/Trading 分支边界。"
    conflict["checked_against"] = append_unique(
        list(conflict.get("checked_against") or []),
        [
            "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
            "docs/contracts/phase41_tabular_llm_training_data_contract.md",
            "docs/research/phase41_hybrid_scoring_qwen3_scope.md",
            "docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md",
        ],
    )

    trace = candidate.setdefault("phase41_trace", {})
    trace["supplemental_evidence_ready"] = True
    trace["supplemental_evidence_added_at"] = TODAY
    trace["supplemental_task_id"] = TASK_ID
    trace["supplemental_source_ids"] = supplement["source_ids"]
    trace["supplemental_constraints"] = supplement.get("extra_trace", {})
    trace["related_contracts"] = append_unique(
        list(trace.get("related_contracts") or []),
        [
            "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
            "docs/contracts/phase41_tabular_llm_training_data_contract.md",
        ],
    )

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_supplemental_evidence"
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = [
        "请二审确认补证后是否 accepted_for_draft；如果仍不足，请返回 needs_more_evidence 或 rejected。",
        "即使二审通过，本条仍只能进入 formal reviewed draft 准备流程，不得直接 approved、default guidance 或 hard gate。",
    ]
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
    append_audit_log(candidate, "phase41_extended_p1_supplemental_evidence_ready", "按严格审计意见补证并准备二审。")
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
        "gate_id": "phase41_extended_p1_supplemental_reaudit_quality_gate",
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
        "phase": "41",
        "task_id": TASK_ID,
        "source_audit_result_id": SOURCE_AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "title": "Phase 41 P0-Extended/P1 needs_more_evidence 补证后二审包",
        "purpose": "只审计 6 条已补证候选，判断是否可进入 accepted_for_draft。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "二审可以给出 accepted_for_draft，但不得直接给 approved。",
            "reviewed_allowed=true 只表示可由 Codex 后续生成 formal reviewed draft，不等于 approved。",
            "approved_allowed、default_guidance_allowed、hard_gate_allowed 必须保持 false。",
            "Trading Engineering 的 K 线、fill model、订单状态机、实盘风控和交易执行本体不得混入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "确认补证是否充分、字段契约是否足够、AI/Trading 边界是否正确、是否仍需补来源或应拒绝。",
            "focus_checks": [
                "新增来源是否直接支撑该 claim，而不是只支撑通用 ML 概念。",
                "内部 CEK-TA 契约是否只作为字段、权限和工作流证据，不替代外部专业来源。",
                "是否误把交易规则、成本模型、market regime、fill/slippage 本体写入 AI Engineering。",
                "是否保持 default_guidance_allowed=false 和 hard_gate_allowed=false。",
                "若 accepted_for_draft，请给出 required_patch_notes 以便 Codex 后续转 formal reviewed draft。",
            ],
            "required_output_schema": {
                "audit_result_id": "audit_result_phase41_extended_p1_supplemental_reaudit_20260610_strict_v2",
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


def render_research(touched: list[dict[str, Any]]) -> str:
    lines = [
        "# Phase 41 P0-Extended/P1 补证采集记录",
        "",
        f"生成日期：{TODAY}",
        f"对应任务：{TASK_ID}",
        "",
        "## 补证范围",
        "",
        "本次只处理严格审计标记为 `needs_more_evidence` 的 6 条候选：P41-A07、P41-B06、P41-E07、P41-F04、P41-F07、P41-F08。",
        "",
        "## 采集原则",
        "",
        "1. 外部来源支撑通用方法、平台治理、安全或监管控制。",
        "2. CEK-TA 内部契约只支撑字段、状态流、权限和 AI/Trading 分支边界。",
        "3. 补证后仍保持 candidate 状态，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 补证结果",
        "",
    ]
    for item in touched:
        lines.extend(
            [
                f"### {item['research_task_id']}",
                "",
                f"- 候选：`{item['candidate_id']}`",
                f"- 文件：`{item['path']}`",
                f"- 新增来源：{', '.join(item['added_source_ids']) if item['added_source_ids'] else '无新增，来源已存在'}",
                f"- 当前来源数量：{item['total_source_count']}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


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
        "report_id": "phase41_extended_p1_supplemental_evidence_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "scope": "Phase 41 P0-Extended/P1 needs_more_evidence supplemental evidence",
        "source_audit_result_id": SOURCE_AUDIT_RESULT_ID,
        "touched_count": len(touched),
        "touched_candidates": touched,
        "quality_gate": gate,
        "audit_package_path": repo_rel(AUDIT_PACKAGE_PATH),
        "research_path": repo_rel(RESEARCH_PATH),
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_allowed_count": 0,
        "hard_gate_allowed_count": 0,
        "boundary": "补证后仍是 candidate；不创建 formal reviewed、approved、default guidance 或 hard gate。",
    }
    write_json(REPORT_PATH, report)
    write_json(AUDIT_PACKAGE_PATH, build_audit_package(supplemented, report))
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text(render_research(touched), encoding="utf-8")

    print(
        json.dumps(
            {
                "ok": gate["gate_status"] == "pass",
                "report": repo_rel(REPORT_PATH),
                "audit_package": repo_rel(AUDIT_PACKAGE_PATH),
                "candidate_count": len(supplemented),
            },
            ensure_ascii=False,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
