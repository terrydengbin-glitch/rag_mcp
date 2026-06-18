"""Generate Phase 37 Kline / Strategy Engineering candidate knowledge.

This script only writes candidate and audit-support artifacts. It does not
create formal reviewed knowledge, does not approve knowledge, and does not
enable default guidance or hard gates.
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
PARTITION = "KB_02_KLINE_STRATEGY"
TREE_PATH = "CEK-TA / Trading Engineering / Kline Strategy"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path(
    "docs", "research", "phase37_kline_strategy_candidate_research.md", start_file=__file__
)
GENERATION_REPORT = resolve_repo_path(
    "docs", "reports", "phase37_kline_strategy_candidate_generation_report.md", start_file=__file__
)
QUALITY_GATE = resolve_repo_path(
    "docs", "reports", "phase37_kline_strategy_candidate_quality_gate.json", start_file=__file__
)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "lo_mamaysky_wang": {
        "source_title": "Foundations of Technical Analysis: Computational Algorithms, Statistical Inference, and Empirical Implementation",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=228099",
        "source_type": "peer_reviewed_paper",
        "publisher": "SSRN / Journal of Finance",
        "published_at": "2000-08-01",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "Lo, Mamaysky and Wang formalize technical pattern recognition and emphasize statistical inference and empirical implementation for technical-analysis claims.",
        "limitations": ["Supports technical-analysis methodology and validation boundaries, not any universal profitable K-line rule."],
    },
    "sullivan_timmermann_white": {
        "source_title": "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=65140",
        "source_type": "peer_reviewed_paper",
        "publisher": "SSRN / Journal of Finance",
        "published_at": "1999-10-01",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "The paper evaluates technical trading rules while accounting for data-snooping bias across a universe of rules.",
        "limitations": ["Supports multiple-testing and validation boundaries; does not define individual K-line entries or exits."],
    },
    "white_reality_check": {
        "source_title": "A Reality Check for Data Snooping",
        "source_url": "https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152",
        "source_type": "peer_reviewed_paper",
        "publisher": "Econometrica / Wiley",
        "published_at": "2000-09-01",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "White defines data snooping as reusing the same data for inference or model selection and provides a reality-check framework.",
        "limitations": ["Supports research validation boundaries, not trade execution decisions."],
    },
    "cfa_technical_analysis": {
        "source_title": "Technical Analysis",
        "source_url": "https://rpc.cfainstitute.org/sites/default/files/-/media/documents/book/rf-lit-review/2016/rflrv11n11.pdf",
        "source_type": "professional_literature_review",
        "publisher": "CFA Institute Research Foundation",
        "published_at": "2016-11-01",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "evidence_summary": "CFA Institute discusses technical analysis, trend, support/resistance, indicators, oscillators, volume and risk-management context.",
        "limitations": ["Professional overview; formal candidates still need explicit market, timeframe, data and validation boundaries."],
    },
    "fidelity_indicators": {
        "source_title": "Understanding Indicators in Technical Analysis",
        "source_url": "https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/learning-center/Understanding-Indicators-TA.pdf",
        "source_type": "brokerage_education_reference",
        "publisher": "Fidelity Investments",
        "published_at": None,
        "reliability": "medium_high",
        "score": 78,
        "freshness": "stable",
        "evidence_summary": "Fidelity categorizes trend, momentum, volume and volatility indicators and frames them as tools requiring context and risk management.",
        "limitations": ["Educational source; should be supporting evidence, not sole proof for formal reviewed knowledge."],
    },
    "ta_lib_home": {
        "source_title": "TA-Lib Technical Analysis Library",
        "source_url": "https://ta-lib.org/",
        "source_type": "technical_library_official_doc",
        "publisher": "TA-Lib",
        "published_at": None,
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "TA-Lib documents a large catalog of technical indicators, including RSI, ATR, moving averages and candlestick pattern recognition.",
        "limitations": ["Library catalog source; it documents implementation availability, not trading edge or default thresholds."],
    },
    "ta_lib_python": {
        "source_title": "TA-Lib Python wrapper documentation",
        "source_url": "https://ta-lib.github.io/ta-lib-python/",
        "source_type": "technical_library_doc",
        "publisher": "TA-Lib Python",
        "published_at": None,
        "reliability": "medium_high",
        "score": 76,
        "freshness": "time_sensitive",
        "evidence_summary": "TA-Lib Python documents common indicators and market-data inputs used by trading software developers.",
        "limitations": ["Wrapper documentation; should not be interpreted as strategy validation evidence."],
    },
    "tradingview_other_timeframes": {
        "source_title": "Other timeframes and data",
        "source_url": "https://www.tradingview.com/pine-script-docs/concepts/other-timeframes-and-data/",
        "source_type": "trading_platform_official_doc",
        "publisher": "TradingView",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "TradingView documents higher/lower timeframe data requests and behavior differences between historical and realtime bars.",
        "limitations": ["Pine Script-specific implementation source; use for multi-timeframe/repainting caveats, not universal platform requirements."],
    },
    "tradingview_repainting": {
        "source_title": "Repainting",
        "source_url": "https://www.tradingview.com/pine-script-docs/concepts/repainting/",
        "source_type": "trading_platform_official_doc",
        "publisher": "TradingView",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "TradingView explains repainting and historical versus realtime behavior for script calculations.",
        "limitations": ["Platform-specific; supports the need to document bar confirmation and realtime/historical semantics."],
    },
    "quantconnect_periods": {
        "source_title": "Periods",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/key-concepts/time-modeling/periods",
        "source_type": "trading_engine_official_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect states that bars have start and end times and are passed to algorithms at end time to avoid unavailable-bar lookahead.",
        "limitations": ["LEAN-specific time model; external projects must map equivalent bar availability semantics."],
    },
    "quantconnect_consolidators": {
        "source_title": "Time Period Consolidators",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/consolidating-data/consolidator-types/time-period-consolidators",
        "source_type": "trading_engine_official_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect documents time-period consolidators for aggregating data into multiple resolutions.",
        "limitations": ["LEAN-specific implementation; supports multi-timeframe aggregation concepts only."],
    },
    "backtrader_brackets": {
        "source_title": "Orders - Brackets",
        "source_url": "https://www.backtrader.com/docu/order-creation-execution/bracket/bracket/",
        "source_type": "backtesting_framework_doc",
        "publisher": "Backtrader",
        "published_at": None,
        "reliability": "medium",
        "score": 72,
        "freshness": "stable",
        "evidence_summary": "Backtrader describes bracket orders with main order, stop-side order and limit-side order submitted together.",
        "limitations": ["Framework-specific order model; use for entry/exit dependency examples, not live-exchange guarantees."],
    },
    "backtrader_stop": {
        "source_title": "Stop Trading",
        "source_url": "https://www.backtrader.com/blog/posts/2018-02-01-stop-trading/stop-trading/",
        "source_type": "backtesting_framework_doc",
        "publisher": "Backtrader",
        "published_at": "2018-02-01",
        "reliability": "medium",
        "score": 70,
        "freshness": "stable",
        "evidence_summary": "Backtrader discusses stop-based strategy mechanisms for limiting losses or securing profits.",
        "limitations": ["Framework education source; does not define a universal stop-loss rule."],
    },
}


CANDIDATES: list[dict[str, Any]] = [
    {
        "task": "P37-C-K01",
        "slug": "trend_structure_boundary",
        "subdomain": "market_structure",
        "tree_node_id": "kt.kline_strategy.market_structure",
        "title": "趋势结构必须声明识别规则和失效条件",
        "statement": "K线趋势结构不能只凭主观看图命名；必须声明 higher high/lower low、区间、突破、回撤、支撑阻力或失效条件的识别规则，并说明市场、周期和样本边界。",
        "applies_when": ["设计趋势、区间、突破、回撤或反转类 K 线策略", "把趋势结构作为标签、过滤器或交易复盘字段"],
        "not_applicable_when": ["只做成交撮合、订单状态机或数据库迁移", "已有更细粒度订单流证据且不使用 K 线结构"],
        "sources": ["cfa_technical_analysis", "lo_mamaysky_wang", "fidelity_indicators", "white_reality_check"],
    },
    {
        "task": "P37-C-K02",
        "slug": "market_structure_requires_timeframe",
        "subdomain": "market_structure",
        "tree_node_id": "kt.kline_strategy.market_structure",
        "title": "市场结构判断必须绑定时间周期和 bar 可用时点",
        "statement": "市场结构、趋势、支撑阻力和突破判断必须绑定时间周期、bar start/end、bar confirmation 和数据可用时点；不得把未确认的高周期 K 线当成已知事实。",
        "applies_when": ["多周期结构过滤", "高周期条件与低周期入场组合", "把 K 线结构输入 AI scoring 或回测"],
        "not_applicable_when": ["只处理纯 tick 级事件流且不聚合 K 线", "只展示图表且不进入策略、训练或审计"],
        "sources": ["quantconnect_periods", "tradingview_other_timeframes", "tradingview_repainting", "cfa_technical_analysis"],
    },
    {
        "task": "P37-C-K03",
        "slug": "entry_signal_not_equal_trade_decision",
        "subdomain": "entry_exit",
        "tree_node_id": "kt.kline_strategy.entry_exit",
        "title": "入场信号不等于完整交易决策",
        "statement": "K线形态、指标交叉或突破信号只能作为候选入场条件；完整交易决策还必须经过成本、滑点、风险、止损、止盈、仓位、样本外和执行边界检查。",
        "applies_when": ["把 K 线/指标信号接入策略引擎", "用 AI 解释或评分交易候选", "审计策略报告中的入场逻辑"],
        "not_applicable_when": ["只研究单个指标公式而不产生交易候选", "外接项目已经有独立 final gate 且本知识只作为引用"],
        "sources": ["sullivan_timmermann_white", "white_reality_check", "cfa_technical_analysis", "backtrader_brackets"],
    },
    {
        "task": "P37-C-K04",
        "slug": "stop_loss_requires_invalidation_logic",
        "subdomain": "entry_exit",
        "tree_node_id": "kt.kline_strategy.entry_exit",
        "title": "止损必须对应交易假设失效逻辑",
        "statement": "止损不能只写成固定点数或随意百分比；必须说明其与入场假设、结构失效、波动范围、数据粒度和执行模型之间的关系。",
        "applies_when": ["设计结构止损、ATR 止损、固定 R 止损或回测止损规则", "审计策略是否把止损作为风险边界"],
        "not_applicable_when": ["只讨论账户级 kill switch 或日亏损风控", "止损由交易所强制规则定义且策略不控制"],
        "sources": ["backtrader_stop", "backtrader_brackets", "cfa_technical_analysis", "quantconnect_periods"],
    },
    {
        "task": "P37-C-K05",
        "slug": "take_profit_requires_reachability_check",
        "subdomain": "entry_exit",
        "tree_node_id": "kt.kline_strategy.entry_exit",
        "title": "止盈目标必须有可达性和执行边界检查",
        "statement": "止盈目标不能只按理想 R 倍数或图形目标声明；必须检查目标在样本、波动、流动性、bar 粒度、fill model、滑点和成本下是否可达。",
        "applies_when": ["设计固定 R、结构位、通道、ATR 或分批止盈", "比较计划止盈与实际成交复盘"],
        "not_applicable_when": ["只定义回测指标而不使用出场规则", "只做风险预算且不定义具体 exit"],
        "sources": ["backtrader_brackets", "backtrader_stop", "quantconnect_periods", "cfa_technical_analysis"],
    },
    {
        "task": "P37-C-K06",
        "slug": "multi_timeframe_context_required",
        "subdomain": "multi_timeframe",
        "tree_node_id": "kt.kline_strategy.market_structure",
        "title": "多周期策略必须声明周期同步和确认语义",
        "statement": "多周期 K 线策略必须说明高低周期数据如何同步、何时确认、是否可能 repaint、如何避免未来数据泄漏，以及每个周期在决策中的职责。",
        "applies_when": ["高周期过滤低周期入场", "多周期指标或结构共振", "把多周期特征输入 AI scoring"],
        "not_applicable_when": ["单一周期策略且不引用其他周期数据", "纯订单簿策略不使用 K 线聚合"],
        "sources": ["tradingview_other_timeframes", "tradingview_repainting", "quantconnect_consolidators", "quantconnect_periods"],
    },
    {
        "task": "P37-C-K07",
        "slug": "indicator_lag_boundary",
        "subdomain": "indicators",
        "tree_node_id": "kt.kline_strategy.indicators",
        "title": "技术指标必须声明滞后、窗口和确认边界",
        "statement": "移动平均、振荡器、波动率和成交量类指标都必须声明输入窗口、计算时点、确认规则和滞后边界；不得把指标输出解释为实时无延迟事实。",
        "applies_when": ["使用 MA、MACD、RSI、ATR、OBV 或成交量指标", "把指标作为模型特征、交易信号或复盘 reason code"],
        "not_applicable_when": ["指标只用于静态教学展示", "使用订单簿实时特征且不依赖技术指标"],
        "sources": ["ta_lib_home", "ta_lib_python", "fidelity_indicators", "tradingview_repainting"],
    },
    {
        "task": "P37-C-K08",
        "slug": "atr_volatility_context_required",
        "subdomain": "indicators",
        "tree_node_id": "kt.kline_strategy.indicators",
        "title": "ATR 和波动率指标必须绑定品种、周期和用途",
        "statement": "ATR 等波动率指标只能说明历史区间波动或止损/仓位/过滤的候选上下文；必须声明品种、周期、窗口和用途，不能直接声称价格方向或交易胜率。",
        "applies_when": ["用 ATR 设定止损、过滤波动状态、归一化目标或构造训练特征", "审计策略是否把波动率误写成方向预测"],
        "not_applicable_when": ["讨论期权隐含波动率定价本体", "只处理账户级风险限额而不使用 K 线波动指标"],
        "sources": ["ta_lib_home", "ta_lib_python", "fidelity_indicators", "cfa_technical_analysis"],
    },
    {
        "task": "P37-C-K09",
        "slug": "rsi_threshold_not_universal",
        "subdomain": "indicators",
        "tree_node_id": "kt.kline_strategy.indicators",
        "title": "RSI 阈值不能被写成跨市场通用规则",
        "statement": "RSI 的超买/超卖阈值只能作为带市场、周期、窗口、趋势状态和验证边界的候选解释；不得把 70/30 等阈值写成跨市场通用买卖规则。",
        "applies_when": ["使用 RSI 或其他振荡器作为策略条件", "审计 AI 是否把指标阈值直接改写成买卖建议"],
        "not_applicable_when": ["只描述 RSI 公式且不产生交易结论", "已经由外部研究给出明确市场和样本边界但仍需保留 caveat"],
        "sources": ["ta_lib_home", "fidelity_indicators", "cfa_technical_analysis", "sullivan_timmermann_white"],
    },
    {
        "task": "P37-C-K10",
        "slug": "volume_confirmation_boundary",
        "subdomain": "indicators",
        "tree_node_id": "kt.kline_strategy.indicators",
        "title": "成交量确认必须绑定数据源、市场机制和样本边界",
        "statement": "成交量确认只能在声明市场机制、成交量定义、数据源、周期和验证样本后使用；不同交易所、现货/合约、聚合商和缺失数据会改变成交量含义。",
        "applies_when": ["用成交量确认突破、反转或趋势", "把成交量指标作为 AI 特征或复盘原因"],
        "not_applicable_when": ["无可靠成交量数据或仅有报价数据", "使用去中心化或聚合成交量且未定义口径"],
        "sources": ["cfa_technical_analysis", "fidelity_indicators", "lo_mamaysky_wang", "white_reality_check"],
    },
    {
        "task": "P37-C-K11",
        "slug": "signal_generalization_forbidden_without_market_scope",
        "subdomain": "signal_boundary",
        "tree_node_id": "kt.kline_strategy",
        "title": "信号泛化必须先声明市场、样本和验证范围",
        "statement": "任何 K 线形态、指标、结构或组合信号都不得被描述为跨市场、跨周期、跨样本的通用规律；必须声明训练/研究样本、样本外、成本和冲突边界。",
        "applies_when": ["沉淀 K 线或指标信号知识", "审计策略报告、AI 解释或交易候选 reason code"],
        "not_applicable_when": ["只做公式实现文档且不声明有效性", "已有 formal approved 边界规则且本候选作为补充来源"],
        "sources": ["lo_mamaysky_wang", "sullivan_timmermann_white", "white_reality_check", "cfa_technical_analysis"],
    },
    {
        "task": "P37-C-K12",
        "slug": "strategy_rule_version_required",
        "subdomain": "strategy_rule_contract",
        "tree_node_id": "kt.kline_strategy",
        "title": "策略规则必须有版本、参数和数据依赖清单",
        "statement": "K线策略规则进入回测、模拟、AI 训练或实盘候选前，必须记录 strategy_rule_version、参数、数据版本、周期、信号计算版本和变更原因，避免复现实验和审计断链。",
        "applies_when": ["策略进入回测、回放、模拟盘、AI 训练或人工审计", "比较不同策略版本或参数搜索结果"],
        "not_applicable_when": ["一次性图表观察且不沉淀为知识或策略", "只处理下游订单执行日志而无策略规则"],
        "sources": ["sullivan_timmermann_white", "white_reality_check", "quantconnect_periods", "lo_mamaysky_wang"],
    },
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")


def make_source_refs(keys: list[str]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for index, key in enumerate(keys, start=1):
        source = dict(SOURCE_CATALOG[key])
        source.update(
            {
                "source_id": f"src_{index:03d}",
                "accessed_at": TODAY,
                "version": None,
                "relevance": "high" if index <= 2 else "medium_high",
                "quoted_excerpt_allowed": False,
            }
        )
        refs.append(source)
    return refs


def make_candidate(spec: dict[str, Any]) -> dict[str, Any]:
    source_refs = make_source_refs(spec["sources"])
    source_score = round(sum(source["score"] for source in source_refs) / len(source_refs), 2)
    slug = spec["slug"]
    normalized_claim = f"kline_strategy.{slug}.v1"
    candidate_id = f"cand_{TODAY.replace('-', '')}_phase{PHASE}_kline_strategy_{slug}_001"
    proposed_knowledge_id = f"kb_02_kline_strategy.{slug}.v1"
    related_nodes = [
        "kt.trading_engineering",
        "kt.kline_strategy",
        "kt.trading_engineering.data_engineering",
        "kt.ai_engineering.llm_training",
    ]
    if spec["tree_node_id"] not in related_nodes:
        related_nodes.append(spec["tree_node_id"])

    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": candidate_id,
        "research_task_id": spec["task"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Kline / Strategy Engineering 候选已采集，等待外部 AI/人工严格审计；不得直接 reviewed、approved、default guidance 或 hard gate。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": spec["tree_node_id"],
            "canonical_node_id": spec["tree_node_id"],
            "tree_path": f"{TREE_PATH} / {spec['tree_node_id'].split('.')[-1].replace('_', ' ').title()}" if spec["tree_node_id"] != "kt.kline_strategy" else TREE_PATH,
            "related_nodes": related_nodes,
            "partition_id": PARTITION,
            "domain": "kline_strategy",
            "subdomain": spec["subdomain"],
            "rule_type": "trading_method_boundary_rule",
            "claim_type": "methodological_constraint",
            "used_for": [
                "strategy_design_audit",
                "kline_signal_boundary",
                "ai_trader_project_gap_audit",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "本候选主归属 KB_02_KLINE_STRATEGY / Trading Engineering / Kline Strategy。历史 Phase 37 范围文档曾使用 KB_03_STRATEGY_ENGINEERING 旧称；运行时以 knowledge_tree 和 schema 的 KB_02_KLINE_STRATEGY 为准。",
        },
        "claim": {
            "claim_id": f"claim_{spec['task'].lower().replace('-', '_')}",
            "statement": spec["statement"],
            "normalized_claim": normalized_claim,
            "evidence_summary": "; ".join(source["evidence_summary"] for source in source_refs[:3]),
            "interpretation_notes": "本候选只定义 K线/策略工程方法边界，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "kline",
            "project_type": "trading_ai_support_layer",
            "applies_when": spec["applies_when"],
            "not_applicable_when": spec["not_applicable_when"]
            + [
                "需要具体买卖点、仓位、杠杆、止损止盈价格、交易所私有配置、账户事实或实盘权限时，应由外接项目事实层和风控层处理。",
                "AI Engineering 只能引用本规则，不得把本规则改写为 LLM 训练、MCP、RAG 或模型部署本体规则。",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，而不是某个项目私有交易系统配置。",
                "所有 K线/策略工程结论必须保留市场、周期、数据、成本、样本和验证边界。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "本批来源包含论文、专业机构综述、交易平台文档和技术库文档，仍需要外部 AI/人工严格审计来源强度。",
                "平台/框架文档只能支撑工程边界和例子，不能替代具体交易所、数据供应商或外接项目策略契约。",
                "本候选不提供任何投资建议或实盘执行许可。",
            ],
        },
        "source_refs": source_refs,
        "source_quality": {
            "overall_reliability": "medium_high",
            "score": source_score,
            "score_version": "phase37_kline_strategy_source_scoring_v1",
            "primary_source_count": len([s for s in source_refs if s["source_type"] in {"peer_reviewed_paper", "professional_literature_review"}]),
            "supporting_source_count": len([s for s in source_refs if s["source_type"] not in {"peer_reviewed_paper", "professional_literature_review"}]),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式入库前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "教育、平台和框架文档只能作为 supporting evidence，不能单独证明交易信号有效性。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "Phase 36/38/40/41 AI Engineering 知识边界",
                "现有 KB_02_KLINE_STRATEGY formal 知识",
                "Phase 37 Trading 与 AI 跨分支引用契约",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与可见正式知识的直接冲突；本候选只定义 Trading Engineering K线/策略工程规则本体，AI Engineering 只能引用。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检索 Trading Engineering K线/策略工程边界。",
                "用于审计交易项目方案中是否缺少周期、样本、成本、验证和执行边界。",
                "用于辅助外接项目设计策略规则、信号版本、审计清单和 reason code。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
                "不得把候选知识当作 reviewed、approved、default guidance 或 hard gate。",
                "不得绕过外接项目事实层、数据契约、风控 hard gate 或人工治理流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 37 Kline / Strategy Engineering candidate is awaiting strict external audit; formal reviewed requires a later reviewed-preparation gate.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "review": {
            "confidence": "medium_high",
            "freshness": "mixed",
            "reviewer": "codex_initial_research",
            "reviewed_at": TODAY,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 claim？",
                "是否需要补充更强的一手论文、专业协会资料、交易平台或回测框架资料？",
                "是否存在与现有 Kline Strategy、Backtest、Replay 或 AI Engineering formal 知识的重叠，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 37 P37-C Kline / Strategy Engineering 队列生成 Trading Engineering 候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录论文、专业机构综述、交易平台文档、技术指标库和回测框架来源摘要。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "classified",
                    "reason": f"归类到 {PARTITION} / {spec['tree_node_id']} / {spec['subdomain']}。",
                },
            ],
        },
        "workflow": {
            "stage": "candidate_ready",
            "next_allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
            "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formal_knowledge_id": None,
            "conversion_target": {
                "proposed_knowledge_id": proposed_knowledge_id,
                "target_review_status": "draft_preparation_only",
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            },
        },
        "contribution": {
            "source": "phase37_research_ingestion",
            "private_data_removed": True,
            "project_private_fields": [],
            "external_project_backflow": False,
        },
    }


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if candidate["status"]["ingestion_decision"] != "candidate_ready":
        errors.append(f"{candidate['candidate_id']}: ingestion_decision must be candidate_ready")
    if candidate["classification"]["partition_id"] != PARTITION:
        errors.append(f"{candidate['candidate_id']}: partition mismatch")
    if len(candidate["source_refs"]) < 3:
        errors.append(f"{candidate['candidate_id']}: source_count < 3")
    if candidate["machine_gate"]["default_guidance"] != "deny":
        errors.append(f"{candidate['candidate_id']}: default guidance must be denied")
    if any(token in candidate["claim"]["statement"] for token in ["买入", "卖出", "开多", "开空", "加杠杆"]):
        errors.append(f"{candidate['candidate_id']}: potential trade instruction wording")
    return errors


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_research_report(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> None:
    lines = [
        "# Phase 37 Kline / Strategy Engineering 候选研究记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 范围",
        "",
        "本批只覆盖 Phase 37 C 组 Kline / Strategy Engineering 12 条候选知识。候选归入运行时知识树和 schema 的 `KB_02_KLINE_STRATEGY`，不是正式知识，不进入默认指导。",
        "",
        "历史范围文件中 `KB_03_STRATEGY_ENGINEERING` 属旧命名；当前 `knowledge_tree.md` 和 `metadata_schema.md` 的正式分区为 `KB_02_KLINE_STRATEGY`。",
        "",
        "## 候选清单",
        "",
        "| research_task_id | candidate_id | tree_node_id | source_count | statement |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for item in candidates:
        lines.append(
            f"| {item['research_task_id']} | `{item['candidate_id']}` | `{item['classification']['tree_node_id']}` | {len(item['source_refs'])} | {item['claim']['statement']} |"
        )
    lines.extend(
        [
            "",
            "## 来源矩阵",
            "",
            "| source_key | title | publisher | type | reliability | role |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for key, source in SOURCE_CATALOG.items():
        lines.append(
            f"| `{key}` | {source['source_title']} | {source['publisher']} | {source['source_type']} | {source['reliability']} | {source['evidence_summary']} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "1. 本批不生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "2. 本批不创建 reviewed、approved、default guidance 或 hard gate。",
            "3. 平台/框架文档只作为工程语义和例子，不作为交易有效性证明。",
            "4. AI Engineering 只能通过 `knowledge_refs` 引用本批规则，不得复制为模型训练或 RAG/MCP 本体规则。",
            "",
            "## 质量门禁摘要",
            "",
            "```json",
            json.dumps(quality, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [make_candidate(spec) for spec in CANDIDATES]
    errors: list[str] = []
    for candidate in candidates:
        errors.extend(validate_candidate(candidate))
        file_name = f"{candidate['candidate_id']}.json"
        write_json(CAND_DIR / file_name, candidate)

    quality = {
        "quality_gate": {"pass": not errors, "errors": errors},
        "phase": PHASE,
        "task_id": "CEK-TA-394",
        "generated_at": TODAY,
        "partition_id": PARTITION,
        "candidate_count": len(candidates),
        "candidate_ready_count": sum(1 for item in candidates if item["status"]["ingestion_decision"] == "candidate_ready"),
        "source_count_min": min(len(item["source_refs"]) for item in candidates),
        "source_count_max": max(len(item["source_refs"]) for item in candidates),
        "default_guidance_denied_count": sum(1 for item in candidates if item["machine_gate"]["default_guidance"] == "deny"),
        "tree_nodes": sorted({item["classification"]["tree_node_id"] for item in candidates}),
        "outputs": {
            "candidate_dir": str(CAND_DIR),
            "research_report": str(RESEARCH_REPORT),
            "generation_report": str(GENERATION_REPORT),
            "quality_gate": str(QUALITY_GATE),
        },
    }

    generation = {
        "phase": PHASE,
        "task_id": "CEK-TA-394",
        "generated_at": TODAY,
        "scope": "Kline / Strategy Engineering C group",
        "partition_id": PARTITION,
        "candidate_count": len(candidates),
        "candidate_ids": [item["candidate_id"] for item in candidates],
        "status": "pass" if not errors else "fail",
        "notes": [
            "Candidates are not formal reviewed knowledge.",
            "Runtime partition follows KB_02_KLINE_STRATEGY because knowledge_tree.md and metadata_schema.md use that partition.",
            "External strict audit must decide accepted_for_draft / needs_more_evidence / rejected.",
        ],
    }

    write_json(QUALITY_GATE, quality)
    write_json(GENERATION_REPORT.with_suffix(".json"), generation)
    GENERATION_REPORT.write_text(
        "\n".join(
            [
                "# Phase 37 Kline / Strategy Engineering 候选生成报告",
                "",
                f"生成日期：{TODAY}",
                "",
                f"- 候选数量：{len(candidates)}",
                f"- 分区：`{PARTITION}`",
                f"- 质量门禁：{'pass' if not errors else 'fail'}",
                f"- 候选目录：`{CAND_DIR}`",
                f"- 研究记录：`{RESEARCH_REPORT}`",
                f"- 质量门禁：`{QUALITY_GATE}`",
                "",
                "本任务只生成候选知识，不创建 formal reviewed，不进入 approved/default/hard gate。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_research_report(candidates, quality)

    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
