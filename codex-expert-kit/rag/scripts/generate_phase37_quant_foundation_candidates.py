"""Generate Phase 37 Quant Foundation candidate knowledge and audit package.

This script only writes candidate/audit artifacts. It does not create formal
reviewed knowledge, does not approve knowledge, and does not enable default
guidance.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
PHASE = "37"
PARTITION = "KB_01_QUANT_FOUNDATION"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path(
    "docs", "research", "phase37_quant_foundation_candidate_research.md", start_file=__file__
)
TREE_MAPPING_REPORT = resolve_repo_path(
    "docs", "reports", "phase37_trading_tree_mapping_report.md", start_file=__file__
)
COLLECTION_REPORT = resolve_repo_path(
    "docs", "reports", "phase37_trading_collection_report.md", start_file=__file__
)
QUALITY_GATE = resolve_repo_path(
    "docs", "reports", "phase37_quant_foundation_candidate_quality_gate.json", start_file=__file__
)
AUDIT_PACKAGE = resolve_repo_path(
    "docs", "audit", "phase37_quant_foundation_candidate_audit_package_20260611.json", start_file=__file__
)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "cfa_trade_strategy_execution": {
        "source_title": "Trade Strategy and Execution",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
        "source_type": "professional_body",
        "publisher": "CFA Institute",
        "published_at": "2026-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute explains that execution strategy must consider urgency, order size, market conditions, expected costs, risk, and trader objectives.",
        "limitations": ["Professional learning material; it supports execution/cost/risk framing, not any specific strategy edge."],
    },
    "cfa_market_risk": {
        "source_title": "Measuring and Managing Market Risk",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/measuring-managing-market-risk",
        "source_type": "professional_body",
        "publisher": "CFA Institute",
        "published_at": "2026-01-01",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute frames market-risk management around risk measurement, limits, stress, and portfolio exposure.",
        "limitations": ["Market-risk overview; it does not define a trading strategy's full validation protocol."],
    },
    "morgan_stanley_expected_value": {
        "source_title": "The Practicalities and Psychology of Expected Value",
        "source_url": "https://www.morganstanley.com/im/en-us/financial-advisor/insights/consilient-observer/probabilities-and-payoffs.html",
        "source_type": "professional_article",
        "publisher": "Morgan Stanley Investment Management",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "evidence_summary": "The article explains expected value through probabilities and payoffs, supporting the separation of win probability from payoff magnitude.",
        "limitations": ["Investment education article; use only for EV framing, not a trading-system validation claim."],
    },
    "investopedia_expected_value": {
        "source_title": "Expected Value",
        "source_url": "https://www.investopedia.com/terms/e/expected-value.asp",
        "source_type": "financial_education",
        "publisher": "Investopedia",
        "published_at": None,
        "reliability": "medium",
        "score": 72,
        "freshness": "stable",
        "evidence_summary": "Defines expected value as a probability-weighted outcome concept.",
        "limitations": ["Educational source; not sufficient alone for professional knowledge approval."],
    },
    "investopedia_risk_reward": {
        "source_title": "Risk/Reward Ratio",
        "source_url": "https://www.investopedia.com/terms/r/riskrewardratio.asp",
        "source_type": "financial_education",
        "publisher": "Investopedia",
        "published_at": None,
        "reliability": "medium",
        "score": 72,
        "freshness": "stable",
        "evidence_summary": "Defines risk/reward ratio as potential reward relative to potential risk.",
        "limitations": ["Educational source; does not validate a strategy by itself."],
    },
    "investopedia_profit_loss_myth": {
        "source_title": "The Myth of Profit/Loss Ratios",
        "source_url": "https://www.investopedia.com/articles/forex/07/profit_loss.asp",
        "source_type": "financial_education",
        "publisher": "Investopedia",
        "published_at": None,
        "reliability": "medium",
        "score": 71,
        "freshness": "stable",
        "evidence_summary": "Explains why judging a system from a single ratio or win/loss view can be misleading without context.",
        "limitations": ["Educational article; should be paired with stronger risk, cost, and validation sources."],
    },
    "investopedia_position_sizing": {
        "source_title": "Position Sizing: Definition, Strategies, Importance in Trading",
        "source_url": "https://www.investopedia.com/terms/p/positionsizing.asp",
        "source_type": "financial_education",
        "publisher": "Investopedia",
        "published_at": None,
        "reliability": "medium",
        "score": 72,
        "freshness": "stable",
        "evidence_summary": "Describes position sizing as determining how much capital to allocate to a trade in relation to risk.",
        "limitations": ["Educational source; project-level risk limits must be defined separately."],
    },
    "trademetria_r_multiple": {
        "source_title": "What Are R-Multiples? The Key Metric Every Trader Should Know",
        "source_url": "https://trademetria.com/blog/what-are-r-multiples-the-key-metric-every-trader-should-know/",
        "source_type": "trading_journal_article",
        "publisher": "Trademetria",
        "published_at": None,
        "reliability": "medium",
        "score": 70,
        "freshness": "stable",
        "evidence_summary": "Explains R-multiple as expressing trade outcomes relative to initial risk.",
        "limitations": ["Vendor education article; use as supporting source, not sole authority."],
    },
    "crosstrade_r_multiple": {
        "source_title": "R-Multiple",
        "source_url": "https://crosstrade.io/learn/performance-metrics/r-multiple",
        "source_type": "trading_education",
        "publisher": "CrossTrade",
        "published_at": None,
        "reliability": "medium",
        "score": 68,
        "freshness": "stable",
        "evidence_summary": "Explains trade outcomes in risk-unit terms and supports comparing trades across different dollar sizes.",
        "limitations": ["Educational vendor source; requires professional audit before formal guidance."],
    },
    "crosstrade_win_rate_expectancy": {
        "source_title": "Win Rate vs Expectancy",
        "source_url": "https://crosstrade.io/learn/performance-metrics/win-rate-vs-expectancy",
        "source_type": "trading_education",
        "publisher": "CrossTrade",
        "published_at": None,
        "reliability": "medium",
        "score": 68,
        "freshness": "stable",
        "evidence_summary": "Contrasts win rate with expectancy, supporting the rule that win rate is insufficient without payoff and cost context.",
        "limitations": ["Educational vendor source; needs stronger supporting evidence for formalization."],
    },
    "sec_margin_accounts": {
        "source_title": "Understanding Margin Accounts",
        "source_url": "https://www.sec.gov/investor/alerts/ib_marginaccounts.pdf",
        "source_type": "regulatory_guidance",
        "publisher": "U.S. Securities and Exchange Commission",
        "published_at": None,
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "SEC investor guidance explains margin risks, including amplified losses and obligations beyond deposited cash.",
        "limitations": ["U.S. securities margin guidance; crypto/futures/CFD venues may differ."],
    },
    "finra_margin_rule_2264": {
        "source_title": "FINRA Rule 2264 Margin Disclosure Statement",
        "source_url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2264",
        "source_type": "regulatory_rule",
        "publisher": "FINRA",
        "published_at": None,
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA margin disclosure requires warning customers about margin risks and possible loss amplification.",
        "limitations": ["U.S. broker-dealer rule; use for leverage-risk boundary, not universal venue implementation."],
    },
    "finra_intraday_margin": {
        "source_title": "Understanding the New Intraday Margin Requirements",
        "source_url": "https://www.finra.org/investors/insights/intraday-margin-requirements",
        "source_type": "regulatory_guidance",
        "publisher": "FINRA",
        "published_at": "2025-11-21",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA explains intraday margin requirements for trading activity and why intraday exposure can create margin obligations.",
        "limitations": ["U.S. margin context; exchange, broker, and asset rules may differ."],
    },
    "finra_day_trading_risk": {
        "source_title": "FINRA Rule 2270 Day-Trading Risk Disclosure Statement",
        "source_url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270",
        "source_type": "regulatory_rule",
        "publisher": "FINRA",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA requires day-trading risk disclosure, supporting the rule that frequent trading requires explicit risk and suitability boundaries.",
        "limitations": ["U.S. day-trading regulatory source; does not define a universal frequency threshold."],
    },
    "cftc_virtual_currency_risk": {
        "source_title": "Understand the Risks of Virtual Currency Trading",
        "source_url": "https://www.cftc.gov/LearnAndProtect/AdvisoriesAndArticles/understand_risks_of_virtual_currency.html",
        "source_type": "regulatory_guidance",
        "publisher": "U.S. Commodity Futures Trading Commission",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "CFTC warns that virtual-currency trading involves high volatility, leverage and fraud risks.",
        "limitations": ["Crypto-focused risk advisory; use only for risk-boundary support."],
    },
    "bailey_pbo": {
        "source_title": "The Probability of Backtest Overfitting",
        "source_url": "https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf",
        "source_type": "research_paper",
        "publisher": "Bailey et al.",
        "published_at": "2014-01-01",
        "reliability": "high",
        "score": 89,
        "freshness": "stable",
        "evidence_summary": "The paper proposes a framework for estimating the probability that backtest selection is overfit.",
        "limitations": ["Supports overfitting risk assessment; it is not a complete validation process by itself."],
    },
    "bailey_statistical_overfitting": {
        "source_title": "The Probability of Backtest Overfitting",
        "source_url": "https://sdm.lbl.gov/oapapers/ssrn-id2507040-bailey.pdf",
        "source_type": "research_paper",
        "publisher": "Bailey et al.",
        "published_at": "2015-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "The paper discusses selection bias and statistical overfitting in investment strategy research.",
        "limitations": ["Research framing; project implementation still needs data and validation contracts."],
    },
    "portfolio_optimization_backtesting_dangers": {
        "source_title": "Dangers of Backtesting",
        "source_url": "https://portfoliooptimizationbook.com/book/8.3-dangers-backtesting.html",
        "source_type": "book",
        "publisher": "Portfolio Optimization Book",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "stable",
        "evidence_summary": "Discusses backtesting dangers such as overfitting, data-snooping and unrealistic assumptions.",
        "limitations": ["Book chapter summary; should be audited alongside primary papers."],
    },
}


TOPICS: list[dict[str, Any]] = [
    {
        "task_id": "P37-A-Q01",
        "slug": "expected_value_definition",
        "knowledge_slug": "quant_foundation.expected_value_definition.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "foundation",
        "claim_type": "definition",
        "statement": "交易期望值必须同时表达结果概率和结果幅度；只描述胜率或只描述盈亏比，都不足以说明一个交易决策是否有正期望。",
        "evidence_summary": "Expected value sources support probability-weighted payoff framing; win-rate and P/L ratio sources support the boundary that single metrics are insufficient.",
        "sources": ["morgan_stanley_expected_value", "investopedia_expected_value", "crosstrade_win_rate_expectancy"],
        "applies_when": ["定义交易系统的基础评价指标", "评审 gating/scoring 是否理解胜率、收益幅度和成本的关系"],
        "not_applicable_when": ["用户要求具体买卖点、仓位、杠杆或实盘执行建议", "没有概率或结果分布数据，只是在记录单笔交易事实"],
    },
    {
        "task_id": "P37-A-Q02",
        "slug": "r_multiple_definition",
        "knowledge_slug": "quant_foundation.r_multiple_definition.v1",
        "canonical_node_id": "kt.quant_foundation.position_sizing",
        "subdomain": "position_sizing",
        "claim_type": "definition",
        "statement": "R multiple 应把交易结果表达为初始风险单位的倍数；它可用于跨不同金额交易比较质量，但不能替代交易成本、滑点、样本外和风控审计。",
        "evidence_summary": "R-multiple education sources support risk-unit normalization; professional execution and risk sources require costs and risk boundaries.",
        "sources": ["trademetria_r_multiple", "crosstrade_r_multiple", "cfa_trade_strategy_execution", "cfa_market_risk"],
        "applies_when": ["复盘交易结果", "比较不同名义金额交易的风险归一化表现", "为 AI 训练提供交易质量标签候选维度"],
        "not_applicable_when": ["没有明确初始风险单位", "要判断实盘是否允许下单", "需要计算具体仓位或止损距离"],
    },
    {
        "task_id": "P37-A-Q03",
        "slug": "risk_reward_boundary",
        "knowledge_slug": "quant_foundation.risk_reward_boundary.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "risk_reward",
        "claim_type": "methodological_constraint",
        "statement": "风险收益比只能描述潜在收益相对潜在风险的静态关系；没有胜率、成本、样本外验证和执行可达性时，不得把高 R/R 描述成策略优势。",
        "evidence_summary": "Risk/reward and profit/loss ratio sources support ratio definition and pitfalls; CFA execution source supports cost and execution-context boundaries.",
        "sources": ["investopedia_risk_reward", "investopedia_profit_loss_myth", "cfa_trade_strategy_execution", "crosstrade_win_rate_expectancy"],
        "applies_when": ["评审交易计划中的风险收益表达", "训练 AI 避免把高 R/R 当作独立优势"],
        "not_applicable_when": ["用户已经给出经审计的完整策略验证报告", "问题只是在解释数学比例，不涉及交易结论"],
    },
    {
        "task_id": "P37-A-Q04",
        "slug": "cost_adjusted_expectancy_required",
        "knowledge_slug": "quant_foundation.cost_adjusted_expectancy_required.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "cost",
        "claim_type": "audit_gate",
        "statement": "交易期望值、回测收益或 scoring 标签在用于比较策略质量前，必须显式说明手续费、点差、滑点、市场冲击和执行失败等成本假设；缺失成本假设时只能视为未完成证据。",
        "evidence_summary": "CFA execution material supports explicit execution cost and market condition considerations; P/L pitfalls support not judging performance from incomplete ratios.",
        "sources": ["cfa_trade_strategy_execution", "investopedia_profit_loss_myth", "portfolio_optimization_backtesting_dangers"],
        "applies_when": ["生成策略评价、回测审计、AI 训练标签或 scoring 特征", "需要比较不同策略、模型或交易过滤器"],
        "not_applicable_when": ["只是定义字段名，不评价策略质量", "成本由外部项目事实库另行提供且当前任务只保存引用"],
    },
    {
        "task_id": "P37-A-Q05",
        "slug": "win_rate_not_enough",
        "knowledge_slug": "quant_foundation.win_rate_not_enough.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "foundation",
        "claim_type": "anti_pattern",
        "statement": "胜率不能单独证明交易系统质量；低胜率高收益幅度或高胜率大亏损尾部都可能改变期望值，必须结合 payoff、成本、回撤和样本外表现解释。",
        "evidence_summary": "Win-rate versus expectancy and EV sources support probability/payoff separation; risk and backtest sources support drawdown and validation boundaries.",
        "sources": ["crosstrade_win_rate_expectancy", "morgan_stanley_expected_value", "investopedia_profit_loss_myth", "bailey_pbo"],
        "applies_when": ["评审交易系统报告", "训练 AI 识别只看胜率的坏例", "构建交易质量 scoring rubric"],
        "not_applicable_when": ["问题只是在统计已发生交易中盈利交易数量", "没有收益幅度、成本或风险数据时不能输出质量结论"],
    },
    {
        "task_id": "P37-A-Q06",
        "slug": "position_sizing_requires_risk_unit",
        "knowledge_slug": "quant_foundation.position_sizing_requires_risk_unit.v1",
        "canonical_node_id": "kt.quant_foundation.position_sizing",
        "subdomain": "position_sizing",
        "claim_type": "procedure_boundary",
        "statement": "仓位 sizing 必须先定义账户风险预算、单笔风险单位、止损或失效边界和最大暴露；没有风险单位时，AI 只能提示缺字段，不能推导仓位。",
        "evidence_summary": "Position sizing and R-multiple sources support risk-unit framing; regulatory margin sources support exposure and loss-amplification boundary.",
        "sources": ["investopedia_position_sizing", "trademetria_r_multiple", "sec_margin_accounts", "cfa_market_risk"],
        "applies_when": ["设计交易计划 schema", "检查 AI 是否错误生成仓位", "把交易事实转为训练样本前检查 risk fields"],
        "not_applicable_when": ["用户明确要求交易建议或真实仓位计算", "没有账户事实或项目级风险预算", "实盘 broker margin 规则未接入"],
    },
    {
        "task_id": "P37-A-Q07",
        "slug": "leverage_amplifies_drawdown",
        "knowledge_slug": "quant_foundation.leverage_amplifies_drawdown.v1",
        "canonical_node_id": "kt.quant_foundation.position_sizing",
        "subdomain": "position_sizing",
        "claim_type": "risk_boundary_rule",
        "statement": "杠杆和保证金会放大收益与亏损，并可能触发追加保证金、强平或超过初始资金的损失；任何使用杠杆的交易质量评价都必须单独展示杠杆、保证金和回撤边界。",
        "evidence_summary": "SEC, FINRA and CFTC sources directly support leverage/margin risk and loss-amplification boundaries.",
        "sources": ["sec_margin_accounts", "finra_margin_rule_2264", "cftc_virtual_currency_risk", "cfa_market_risk"],
        "applies_when": ["审计杠杆交易、保证金交易、合约或高波动资产交易评价", "构建风险标签或交易质量评分"],
        "not_applicable_when": ["完全无杠杆的现货交易且没有借贷、保证金或衍生品暴露", "需要给出具体杠杆倍数建议"],
    },
    {
        "task_id": "P37-A-Q08",
        "slug": "signal_decision_execution_separation",
        "knowledge_slug": "quant_foundation.signal_decision_execution_separation.v1",
        "canonical_node_id": "kt.quant_foundation.signal_flow",
        "subdomain": "signal_flow",
        "claim_type": "architecture_rule",
        "statement": "市场信号、交易决策、订单意图、成交回报和交易结果必须分层记录；一个信号只能作为候选输入，不能直接等同于下单许可或实盘执行结果。",
        "evidence_summary": "CFA execution material distinguishes investment objective, trading strategy and execution; day-trading risk sources support explicit risk boundaries before frequent execution.",
        "sources": ["cfa_trade_strategy_execution", "finra_day_trading_risk", "cfa_market_risk"],
        "applies_when": ["设计交易系统事件流", "审计 AI gating/scoring 是否把信号误当执行许可", "构建数据 schema 或训练样本链路"],
        "not_applicable_when": ["只是在解释某个静态指标定义", "用户要求具体下单、撤单或仓位调整"],
    },
    {
        "task_id": "P37-A-Q09",
        "slug": "trade_frequency_vs_quality_boundary",
        "knowledge_slug": "quant_foundation.trade_frequency_vs_quality_boundary.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "cost",
        "claim_type": "risk_boundary_rule",
        "statement": "交易频率不能单独代表交易质量；频率上升通常会放大成本、保证金、执行失败和行为风险，因此必须结合成本模型、账户约束和样本外表现评价。",
        "evidence_summary": "FINRA day-trading and intraday margin sources support frequency and margin risk; CFA execution source supports cost and execution-context evaluation.",
        "sources": ["finra_day_trading_risk", "finra_intraday_margin", "cfa_trade_strategy_execution", "portfolio_optimization_backtesting_dangers"],
        "applies_when": ["评审高频、日内或高周转策略", "训练 AI 避免把更多交易等同于更高质量"],
        "not_applicable_when": ["仅统计成交笔数不做质量判断", "项目已有外部交易成本和账户约束事实且当前任务只引用"],
    },
    {
        "task_id": "P37-A-Q10",
        "slug": "edge_requires_out_of_sample_evidence",
        "knowledge_slug": "quant_foundation.edge_requires_out_of_sample_evidence.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "foundation",
        "claim_type": "audit_gate",
        "statement": "任何交易 edge、过滤器或模型改进声称，在进入默认指导或实盘前都必须提供样本外、walk-forward、shadow/paper 或等价的独立验证证据；仅靠样本内回测不能证明可复用优势。",
        "evidence_summary": "Backtest overfitting and data-snooping sources support independent validation requirements; CFA execution source supports not ignoring cost/execution context.",
        "sources": ["bailey_pbo", "bailey_statistical_overfitting", "portfolio_optimization_backtesting_dangers", "cfa_trade_strategy_execution"],
        "applies_when": ["评审策略 edge、模型分数提升、过滤器收益或交易质量提升声明", "决定候选是否可转 reviewed/approved"],
        "not_applicable_when": ["候选只声明研究假设，不声称 edge", "还处于候选知识审计阶段，不能进入默认指导"],
    },
    {
        "task_id": "P37-A-Q11",
        "slug": "sample_size_and_regime_caveat",
        "knowledge_slug": "quant_foundation.sample_size_and_regime_caveat.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "foundation",
        "claim_type": "methodological_constraint",
        "statement": "交易系统评价必须声明样本数量、样本时期、市场状态和资产范围；样本过小或只覆盖单一 regime 时，不得泛化为跨市场、跨周期或跨状态规则。",
        "evidence_summary": "EV and overfitting sources support uncertainty around small or selected samples; backtesting danger sources support regime and data-snooping caveats.",
        "sources": ["morgan_stanley_expected_value", "bailey_pbo", "portfolio_optimization_backtesting_dangers"],
        "applies_when": ["写策略报告、交易复盘、AI 训练标签说明或 RAG 知识卡", "判断规则是否可跨市场复用"],
        "not_applicable_when": ["只是在记录单笔交易", "外部项目已提供明确的样本和 regime 边界且当前知识只保存引用"],
    },
    {
        "task_id": "P37-A-Q12",
        "slug": "no_profit_claim_without_costs",
        "knowledge_slug": "quant_foundation.no_profit_claim_without_costs.v1",
        "canonical_node_id": "kt.quant_foundation",
        "subdomain": "cost",
        "claim_type": "default_guidance_block",
        "statement": "没有手续费、点差、滑点、市场冲击、成交失败和数据偏差说明时，不得把交易结果描述为可复用盈利能力；最多只能描述为未完成成本审计的研究观察。",
        "evidence_summary": "CFA execution and backtesting danger sources support costs and assumptions; overfitting sources support blocking unvalidated profit claims.",
        "sources": ["cfa_trade_strategy_execution", "portfolio_optimization_backtesting_dangers", "bailey_statistical_overfitting", "investopedia_profit_loss_myth"],
        "applies_when": ["审计策略收益、AI scoring 改进、交易复盘结论或营销式收益表述", "判断候选知识是否可作为默认指导"],
        "not_applicable_when": ["只是在记录原始成交事实", "已有独立成本审计和样本外验证且当前任务只引用报告编号"],
    },
]


PRIMARY_SOURCE_TYPES = {
    "professional_body",
    "professional_article",
    "regulatory_guidance",
    "regulatory_rule",
    "research_paper",
    "book",
}


def source_ref(source_key: str, idx: int) -> dict[str, Any]:
    raw = SOURCE_CATALOG[source_key]
    return {
        "source_id": f"src_{idx:03d}",
        "source_title": raw["source_title"],
        "source_url": raw["source_url"],
        "source_type": raw["source_type"],
        "publisher": raw["publisher"],
        "published_at": raw["published_at"],
        "accessed_at": TODAY,
        "version": None,
        "reliability": raw["reliability"],
        "score": raw["score"],
        "relevance": "high",
        "freshness": raw["freshness"],
        "limitations": raw["limitations"],
        "evidence_summary": raw["evidence_summary"],
        "quoted_excerpt_allowed": False,
    }


def proposed_knowledge_id(topic: dict[str, Any]) -> str:
    return f"kb_01_quant_foundation.{topic['slug']}.v1"


def candidate_id(topic: dict[str, Any]) -> str:
    return f"cand_20260611_phase37_{topic['slug']}_001"


def normalized_claim(topic: dict[str, Any]) -> str:
    return f"phase37_{topic['slug']}_requires_source_backed_boundary"


def build_candidate(topic: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, index + 1) for index, key in enumerate(topic["sources"])]
    reliability_scores = [int(ref["score"]) for ref in refs]
    primary_count = sum(1 for ref in refs if ref["source_type"] in PRIMARY_SOURCE_TYPES)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": candidate_id(topic),
        "research_task_id": topic["task_id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "pending_ai_audit",
            "decision_reason": "Phase 37 首批 Trading Engineering 候选知识，必须先经过外部 AI/人工审计；不代表 reviewed、approved 或默认指导。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": topic["canonical_node_id"],
            "canonical_node_id": topic["canonical_node_id"],
            "tree_path": "CEK-TA / Trading Engineering / Quant Foundation",
            "related_nodes": [
                "kt.trading_engineering",
                "kt.ai_engineering",
                "kt.ai_engineering.llm_training",
            ],
            "partition_id": PARTITION,
            "domain": "quant_trading",
            "subdomain": topic["subdomain"],
            "rule_type": topic["claim_type"],
            "claim_type": topic["claim_type"],
            "used_for": [
                "trading_knowledge_audit",
                "ai_trader_project_design",
                "trade_quality_scoring_context",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "本候选主归属 Trading Engineering / Quant Foundation；AI Engineering 只能通过 knowledge_refs 引用，不得复制交易规则本体。",
        },
        "claim": {
            "claim_id": f"claim_{topic['task_id'].lower().replace('-', '_')}",
            "statement": topic["statement"],
            "normalized_claim": normalized_claim(topic),
            "evidence_summary": topic["evidence_summary"],
            "interpretation_notes": "本候选只定义交易专业知识边界，不输出买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
            "claim_strength": "medium_high" if primary_count >= 2 else "medium",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "trading_ai_support_layer",
            "applies_when": topic["applies_when"],
            "not_applicable_when": topic["not_applicable_when"]
            + [
                "需要具体交易策略参数、账户事实、交易所配置、密钥或实盘权限时，应由外接项目事实层处理。",
                "AI Engineering 只能引用本规则，不得把本规则改写为模型训练、MCP 或 RAG 本体规则。",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，而不是某个项目私有策略。",
                "所有交易结论都必须保留市场、样本、成本、执行和验证边界。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "首批候选以公开专业资料、监管资料、论文和教育资料为来源，仍需要外部 AI/人工严格审计。",
                "部分来源是教育或供应商文章，只能作为 supporting evidence，不能单独支撑 approved。",
                "本候选不提供任何投资建议或实盘执行许可。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high" if primary_count >= 2 else "medium_high",
            "score": round(sum(reliability_scores) / len(reliability_scores)),
            "score_version": "phase37_source_scoring_v1",
            "primary_source_count": primary_count,
            "supporting_source_count": len(refs) - primary_count,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [] if primary_count >= 1 else ["missing_primary_source"],
            "limitations": [
                "正式入库前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "监管资料按地区适用，不能自动泛化到所有市场或交易所。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": ["Phase 36/38/40/41 AI Engineering 知识边界", "现有 KB_01_QUANT_FOUNDATION formal 知识"],
            "conflicts": [],
            "resolution_summary": "未发现与现有正式知识的直接冲突；与 AI Engineering 中 risk/reward、cost、label 相关知识属于 owner/reference 边界互补。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检索 Trading Engineering 规则本体。",
                "用于审计交易项目方案中是否缺少成本、风险、样本和验证边界。",
                "用于辅助外接项目设计 schema、label、reason code 和 review checklist。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得绕过外接项目事实、风控 hard gate 或人工治理流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate/proposed only; external audit is required before formal reviewed conversion.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
        },
        "review": {
            "confidence": "medium_high" if primary_count >= 2 else "medium",
            "freshness": "mixed",
            "reviewer": "codex_research_ingestion",
            "reviewed_at": None,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 claim？",
                "是否需要补充更强的一手来源、交易所规则、教材或论文？",
                "是否存在与现有 Trading Engineering formal 知识的重叠，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 37 P37-A Quant Foundation 队列生成首批 Trading Engineering 候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录公开专业资料、监管资料、论文和教育资料的来源摘要。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "classified",
                    "reason": f"归类到 {PARTITION} / {topic['canonical_node_id']} / {topic['subdomain']}。",
                },
            ],
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、元数据和摘要，不保存长段原文。",
            "reuse_risk": "low",
        },
        "conversion_target": {
            "proposed_knowledge_id": proposed_knowledge_id(topic),
            "target_schema": "cek_ta_knowledge_item_schema_v1_1",
            "target_review_status": "draft",
            "target_machine_gate": "deny_until_audit",
            "skill_candidate": False,
            "eval_case_candidate": True,
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending_audit",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "next_action": "external_ai_or_human_audit",
        },
    }


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def load_existing_formal_ids() -> set[str]:
    if not KNOWLEDGE_DIR.exists():
        return set()
    ids: set[str] = set()
    for path in KNOWLEDGE_DIR.glob("*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        knowledge_id = raw.get("knowledge_id")
        if isinstance(knowledge_id, str):
            ids.add(knowledge_id)
    return ids


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    expected_ids = {topic["task_id"] for topic in TOPICS}
    seen_ids = {str(item.get("research_task_id")) for item in candidates}
    formal_ids = load_existing_formal_ids()

    for item in candidates:
        candidate = str(item.get("candidate_id"))
        source_refs = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in source_refs if isinstance(src, dict)}
        proposed_id = str(item.get("conversion_target", {}).get("proposed_knowledge_id", ""))
        not_applicable = " ".join(item.get("applicability", {}).get("not_applicable_when", []))
        policy_text = json.dumps(item.get("llm_usage_policy", {}), ensure_ascii=False)

        if item.get("research_task_id") not in expected_ids:
            failures.append({"candidate_id": candidate, "failure": "unexpected_research_task_id"})
        if not str(item.get("classification", {}).get("canonical_node_id", "")).startswith("kt.quant_foundation"):
            failures.append({"candidate_id": candidate, "failure": "wrong_canonical_node"})
        if item.get("classification", {}).get("partition_id") != PARTITION:
            failures.append({"candidate_id": candidate, "failure": "wrong_partition"})
        if len(source_refs) < 3:
            failures.append({"candidate_id": candidate, "failure": "source_refs_lt_3"})
        if not (source_types & PRIMARY_SOURCE_TYPES):
            failures.append({"candidate_id": candidate, "failure": "missing_primary_source_type"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": candidate, "failure": "not_proposed_candidate"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate, "failure": "default_guidance_allowed_not_false"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate, "failure": "machine_gate_not_deny"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": candidate, "failure": "unsafe_conflict_status"})
        if proposed_id in formal_ids:
            failures.append({"candidate_id": candidate, "failure": "proposed_knowledge_id_already_exists"})
        if "AI Engineering" not in not_applicable:
            failures.append({"candidate_id": candidate, "failure": "missing_ai_engineering_reference_boundary"})
        if "不得生成买卖点" not in policy_text:
            failures.append({"candidate_id": candidate, "failure": "missing_no_trade_advice_policy"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate, "failure": "mojibake_marker_detected"})

    for missing in sorted(expected_ids - seen_ids):
        failures.append({"research_task_id": missing, "failure": "missing_candidate"})

    return {
        "report_id": "phase37_quant_foundation_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 37 P37-A Quant Foundation candidate package",
        "planned_total": len(TOPICS),
        "candidate_count": len(candidates),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not formal reviewed or approved; external audit is required before any conversion.",
    }


def build_audit_package(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": "phase37_quant_foundation_candidate_audit_package_20260611",
        "package_type": "candidate_ai_audit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": PHASE,
        "title": "Phase 37 Trading Engineering / Quant Foundation 首批候选知识审计包",
        "purpose": "严格审计 12 条 Quant Foundation 候选知识，判断是否可进入 accepted_for_draft、needs_more_evidence 或 rejected。",
        "strict_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 reviewed，也不是 approved。",
            "本包不得创建 approved、default guidance 或 hard gate。",
            "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "AI Engineering 只能引用 Trading Engineering 规则，不得复制或改写交易规则本体。",
            "交易 edge、收益、胜率、R/R、成本和仓位相关 claim 必须保留样本、市场、执行和验证边界。",
        ],
        "audit_instructions": [
            "必须搜索相关的专业网站、资料、案例和数据，对审计报告进行严格审计。",
            "逐条检查来源是否足以支撑 claim，不能让教育类来源单独支撑强规则。",
            "检查是否存在与现有正式知识冲突、重复或需要合并的地方。",
            "检查是否清楚声明适用范围、不适用场景、假设、限制和 AI 使用边界。",
            "检查是否有中文乱码、mock/test 污染、项目私有策略参数或实盘敏感信息。",
            "输出只能是 accepted_for_draft、needs_more_evidence 或 rejected；不得输出 approved。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": "phase37_quant_foundation_candidate_audit_package_20260611",
            "summary": {
                "total": 12,
                "accepted_for_draft": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": ["string"],
                    "source_assessment": {
                        "source_count": 0,
                        "missing_sources": ["string"],
                        "weak_sources": ["string"],
                        "recommended_extra_sources": ["string"],
                    },
                    "classification_assessment": {
                        "correct_partition": True,
                        "expected_partition": PARTITION,
                        "correct_tree_node": True,
                        "notes": "string",
                    },
                    "boundary_assessment": {
                        "no_trade_advice": True,
                        "ai_reference_only": True,
                        "requires_external_project_facts": True,
                    },
                }
            ],
        },
        "quality_gate": quality,
        "candidates": candidates,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_candidate_files(candidates: list[dict[str, Any]]) -> None:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    for item in candidates:
        path = CAND_DIR / f"{item['candidate_id']}.json"
        write_json(path, item)


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    rows = [
        "| 任务 | 候选 | 节点 | 来源数 | 主来源数 | 状态 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in candidates:
        primary_count = item["source_quality"]["primary_source_count"]
        rows.append(
            f"| {item['research_task_id']} | `{item['conversion_target']['proposed_knowledge_id']}` | "
            f"`{item['classification']['canonical_node_id']}` | {len(item['source_refs'])} | {primary_count} | candidate_ready |"
        )
    content = f"""# Phase 37 Quant Foundation 候选研究记录

生成日期：{TODAY}

## 范围

本文件记录 Phase 37 首批 `P37-A` Quant Foundation 12 条候选知识的来源选择、分类和边界。所有条目仍是 candidate，不是 formal reviewed，不是 approved，不进入默认指导。

## 来源原则

```text
1. 优先使用专业机构、监管机构、论文、教材或官方资料。
2. 教育类和供应商资料只能作为 supporting source。
3. R/R、胜率、R multiple、仓位、成本、杠杆等规则必须写明适用边界和不适用场景。
4. 不输出买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 候选清单

{chr(10).join(rows)}

## 下游

```text
docs/audit/phase37_quant_foundation_candidate_audit_package_20260611.json
```
"""
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text(content, encoding="utf-8")


def write_tree_mapping_report(candidates: list[dict[str, Any]]) -> None:
    nodes = sorted({item["classification"]["canonical_node_id"] for item in candidates})
    rows = [
        "| 节点 | 候选数 | 说明 |",
        "| --- | ---: | --- |",
    ]
    for node in nodes:
        count = sum(1 for item in candidates if item["classification"]["canonical_node_id"] == node)
        rows.append(f"| `{node}` | {count} | Phase 37 首批 Quant Foundation 候选挂载节点 |")
    content = f"""# Phase 37 Trading 分支知识树映射检查报告

生成日期：{TODAY}

## 结论

首批 P37-A Quant Foundation 候选均归属 `KB_01_QUANT_FOUNDATION`，主节点挂载在 `kt.quant_foundation` 或其现有 Level 3 子节点。当前不修改 `knowledge_tree.md`，原因是现有树已包含 Quant Foundation、Signal Flow、Position Sizing，并且 `kt.quant_foundation.item_mapping.allowed_subdomains` 已覆盖 foundation、signal_flow、sizing、risk_reward、cost。

## 映射统计

{chr(10).join(rows)}

## 边界

```text
1. K 线、fill model、订单状态机、实盘风控本体不放入 Quant Foundation。
2. AI Engineering 只能引用这些 Trading Engineering 规则。
3. 后续如 UI 需要更细的 L3 导航，可单独新增 EV / Risk Reward / Cost 子节点任务。
```
"""
    TREE_MAPPING_REPORT.parent.mkdir(parents=True, exist_ok=True)
    TREE_MAPPING_REPORT.write_text(content, encoding="utf-8")


def write_collection_report(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> None:
    content = f"""# Phase 37 Trading Engineering 首批候选采集报告

生成日期：{TODAY}

## 本批范围

```text
分支：Trading Engineering
分区：KB_01_QUANT_FOUNDATION
批次：P37-A Quant Foundation
候选数：{len(candidates)}
质量门禁：{quality['gate_status']}
```

## 已完成任务

```text
CEK-TA-191 跨分支引用契约
CEK-TA-192 ResearchIngestionTask 队列
CEK-TA-193 知识树映射检查
CEK-TA-194 首批候选知识包
CEK-TA-195 候选审计包和质量门禁
```

## 交付物

```text
codex-expert-kit/rag/candidates/KB_01_QUANT_FOUNDATION/
docs/research/phase37_quant_foundation_candidate_research.md
docs/reports/phase37_trading_tree_mapping_report.md
docs/reports/phase37_quant_foundation_candidate_quality_gate.json
docs/audit/phase37_quant_foundation_candidate_audit_package_20260611.json
```

## 停止点

当前已到外部 AI/人工审计点。下一步必须先审计 `phase37_quant_foundation_candidate_audit_package_20260611.json`，再决定 accepted_for_draft、needs_more_evidence 或 rejected。
"""
    COLLECTION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    COLLECTION_REPORT.write_text(content, encoding="utf-8")


def main() -> None:
    candidates = [build_candidate(topic) for topic in TOPICS]
    write_candidate_files(candidates)
    quality = quality_gate(candidates)
    write_json(QUALITY_GATE, quality)
    write_json(AUDIT_PACKAGE, build_audit_package(candidates, quality))
    write_research_report(candidates)
    write_tree_mapping_report(candidates)
    write_collection_report(candidates, quality)
    if quality["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {quality['failures']}")
    print(
        json.dumps(
            {
                "generated": len(candidates),
                "candidate_dir": str(CAND_DIR),
                "audit_package": str(AUDIT_PACKAGE),
                "quality_gate": quality["gate_status"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
