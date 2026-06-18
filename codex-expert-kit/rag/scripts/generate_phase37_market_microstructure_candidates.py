"""Generate Phase 37 Market Microstructure candidate knowledge.

This script writes candidate and audit-support artifacts only. It does not
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
TASK_ID = "CEK-TA-402"
PARTITION = "KB_03_MARKET_MICROSTRUCTURE"
TREE_NODE = "kt.market_microstructure"
TREE_PATH = "CEK-TA / Trading Engineering / Market Microstructure"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path(
    "docs", "research", "phase37_market_microstructure_candidate_research.md", start_file=__file__
)
GENERATION_REPORT = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_candidate_generation_report.md", start_file=__file__
)
QUALITY_GATE = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_candidate_quality_gate.json", start_file=__file__
)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "cfa_trade_strategy": {
        "source_title": "Trade Strategy and Execution",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
        "source_type": "professional_curriculum",
        "publisher": "CFA Institute",
        "published_at": "2026-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute frames trading decisions around liquidity needs, market conditions, execution risk, opportunity cost, market impact and trade cost analysis.",
        "limitations": ["Professional curriculum source; it supports execution and cost boundaries, not any profitable microstructure signal."],
    },
    "cfa_trading_costs": {
        "source_title": "Trading Costs and Electronic Markets",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
        "source_type": "professional_curriculum",
        "publisher": "CFA Institute",
        "published_at": "2026-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute explains explicit and implicit trading costs, transaction cost estimation, electronic trading, speed needs, market monitoring and systemic-risk caveats.",
        "limitations": ["Supports cost, speed and execution-quality context; it does not define exchange-specific order-book fields."],
    },
    "databento_mbo": {
        "source_title": "Market by order (MBO)",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/mbo",
        "source_type": "official_data_vendor_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento MBO provides every order book event across every price level keyed by order ID, including adds, cancels, modifies, trades and fills; it is commonly called L3 data.",
        "limitations": ["Vendor-specific schema; use as concrete data-model evidence, not universal market behavior."],
    },
    "databento_mbp10": {
        "source_title": "Market by price (MBP-10)",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/mbp-10",
        "source_type": "official_data_vendor_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento MBP-10 provides order-book events across the top ten price levels, with trade events and aggregate market depth by price; it is commonly called L2 data.",
        "limitations": ["Top-of-book/depth limitation must be declared; vendor-specific fields cannot be assumed for all feeds."],
    },
    "databento_trades": {
        "source_title": "Trades schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/trades",
        "source_type": "official_data_vendor_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento trades records include a side field for the side that initiates the trade, with bid/ask/none semantics depending on availability.",
        "limitations": ["Aggressor classification is feed- and venue-dependent; absence or ambiguity must be handled explicitly."],
    },
    "nasdaq_totalview": {
        "source_title": "Nasdaq TotalView",
        "source_url": "https://www.nasdaq.com/solutions/data/equities/nasdaq-totalview",
        "source_type": "official_exchange_data_doc",
        "publisher": "Nasdaq",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Nasdaq describes TotalView as complete depth-of-book for displayed orders across Nasdaq, NYSE and regional securities.",
        "limitations": ["Exchange/data-product specific; not a universal guarantee of hidden liquidity, off-book trades or all venues."],
    },
    "nasdaq_itch_spec": {
        "source_title": "Nasdaq TotalView-ITCH 5.0 specification",
        "source_url": "https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf",
        "source_type": "official_exchange_spec",
        "publisher": "Nasdaq Trader",
        "published_at": "2024-01-01",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Nasdaq TotalView-ITCH tracks full order depth through order-level messages that add, execute, cancel, delete and replace customer orders.",
        "limitations": ["Specific to Nasdaq ITCH feed semantics and not directly transferable to all exchanges."],
    },
    "binance_funding_rate": {
        "source_title": "Get Funding Rate History",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History",
        "source_type": "official_exchange_api_doc",
        "publisher": "Binance Open Platform",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance futures API returns symbol-level fundingRate, fundingTime and markPrice with request limits and time-window semantics.",
        "limitations": ["Crypto perpetuals specific; funding fields must not be generalized to spot, equities or all derivatives."],
    },
    "binance_open_interest": {
        "source_title": "Open Interest",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Open-Interest",
        "source_type": "official_exchange_api_doc",
        "publisher": "Binance Open Platform",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance futures API exposes present open interest for a specific symbol.",
        "limitations": ["Single-exchange open interest must be timestamped and cannot represent total market positioning by itself."],
    },
    "brunnermeier_pedersen": {
        "source_title": "Market Liquidity and Funding Liquidity",
        "source_url": "https://www.nber.org/system/files/working_papers/w12939/w12939.pdf",
        "source_type": "academic_paper",
        "publisher": "NBER",
        "published_at": "2007-02-01",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "Brunnermeier and Pedersen model how market liquidity and funding liquidity can reinforce each other and can dry up under stress.",
        "limitations": ["Theoretical liquidity-stress source; does not define a trading signal or venue-specific field."],
    },
    "ecb_liquidity": {
        "source_title": "Gauging the interplay between market liquidity and funding liquidity",
        "source_url": "https://www.ecb.europa.eu/press/financial-stability-publications/fsr/special/html/ecb.fsrart202305_01~830184261b.en.html",
        "source_type": "central_bank_research",
        "publisher": "European Central Bank",
        "published_at": "2023-05-31",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "evidence_summary": "ECB defines market liquidity as the ability to rapidly execute large transactions at low cost and limited price impact, and distinguishes it from funding liquidity.",
        "limitations": ["Macro/financial-stability framing; use for liquidity definitions and stress caveats."],
    },
    "almgren_chriss": {
        "source_title": "Optimal Liquidation",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=53501",
        "source_type": "academic_paper",
        "publisher": "SSRN / Applied Mathematical Finance",
        "published_at": "2000-12-01",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "Almgren and Chriss model optimal execution as a trade-off between transaction costs, market impact and volatility risk.",
        "limitations": ["Optimal-execution model assumptions must be stated; not a default live trading permission."],
    },
    "esma_rts25": {
        "source_title": "Commission Delegated Regulation RTS 25 clock synchronisation",
        "source_url": "https://ec.europa.eu/finance/securities/docs/isd/mifid/rts/160607-rts-25_en.pdf",
        "source_type": "regulatory_standard",
        "publisher": "European Commission / ESMA",
        "published_at": "2016-06-07",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "RTS 25 requires trading venues and participants to synchronise business clocks and timestamp reportable events with an accurate time source.",
        "limitations": ["EU regulatory context; use as strong timing/clock-sync boundary evidence, not universal global law."],
    },
    "sec_15c3_5": {
        "source_title": "Responses to Frequently Asked Questions Concerning Risk Management Controls for Brokers or Dealers with Market Access",
        "source_url": "https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0",
        "source_type": "regulatory_guidance",
        "publisher": "U.S. Securities and Exchange Commission",
        "published_at": "2013-04-15",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "SEC Rule 15c3-5 guidance requires risk management controls and supervisory procedures for market access to be reviewed regularly for effectiveness.",
        "limitations": ["Broker-dealer market-access regulation; use as risk-control context rather than microstructure signal proof."],
    },
    "overcharts_volume_delta": {
        "source_title": "Volume Delta",
        "source_url": "https://www.overcharts.com/en/helpcenter/docs/volume-delta/",
        "source_type": "trading_platform_doc",
        "publisher": "Overcharts",
        "published_at": None,
        "reliability": "medium",
        "score": 70,
        "freshness": "time_sensitive",
        "evidence_summary": "Overcharts defines Volume Delta as ASK sizes minus BID sizes over a chart resolution, where ask-side hits indicate buyer aggressor and bid-side hits indicate seller aggressor.",
        "limitations": ["Platform-specific indicator documentation; supporting evidence only, not universal CVD truth."],
    },
}


CANDIDATES: list[dict[str, Any]] = [
    {
        "task": "P37-D-M01",
        "slug": "spread_liquidity_context_required",
        "title": "价差信号必须声明流动性上下文",
        "claim": "Bid-ask spread、盘口价差或价差收窄/扩大信号，必须同时声明市场、品种、交易时段、数据源、成交量和流动性状态；不得把单一价差变化解释为通用交易方向。",
        "subdomain": "spread_liquidity",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy", "ecb_liquidity", "nasdaq_totalview"],
        "applies": ["审计价差、流动性、报价质量或执行成本相关指标", "把价差特征用于交易候选评分或交易质量复盘"],
        "not_applies": ["需要直接生成买卖方向、仓位、杠杆或止损止盈参数", "数据源没有 bid/ask、深度、时间戳或交易时段信息"],
    },
    {
        "task": "P37-D-M02",
        "slug": "order_book_depth_boundary",
        "title": "盘口深度必须声明 L2/L3 和可见性边界",
        "claim": "Order book depth 只能描述可见订单簿的深度和变动，必须声明是 L2 aggregate depth、L3 market-by-order、top-of-book 还是完整深度；不得把可见深度等同于全部市场流动性。",
        "subdomain": "order_book_depth",
        "sources": ["databento_mbo", "databento_mbp10", "nasdaq_totalview", "nasdaq_itch_spec"],
        "applies": ["解析 L2/L3 盘口、队列、深度或 DOM 特征", "设计盘口特征、执行仿真或流动性审计"],
        "not_applies": ["只拥有 OHLCV 数据而无 order book feed", "需要断言隐藏流动性、暗池或全市场真实深度"],
    },
    {
        "task": "P37-D-M03",
        "slug": "trade_prints_aggressor_caveat",
        "title": "逐笔成交 aggressor 方向必须保留数据源语义",
        "claim": "Trade prints 的买卖主动方、bid/ask hit 或 aggressor side 必须按数据源字段定义解释；缺失、推断或 venue 规则不一致时，不能把 trade side 当成确定订单流事实。",
        "subdomain": "trade_prints",
        "sources": ["databento_trades", "nasdaq_itch_spec", "databento_mbo", "cfa_trading_costs"],
        "applies": ["使用逐笔成交、tape、aggressor side、trade side 或成交方向特征", "审计订单流、成交量 delta 或交易行为标签"],
        "not_applies": ["数据源没有 aggressor 字段且未声明推断规则", "跨交易所直接合并 trade side 而未做字段映射"],
    },
    {
        "task": "P37-D-M04",
        "slug": "order_flow_proxy_boundary",
        "title": "订单流代理指标不能替代真实订单簿事实",
        "claim": "Order flow proxy、imbalance、signed volume 或 OFI 类指标必须声明输入数据、采样窗口、方向推断和归一化方式；代理指标不能替代真实订单、取消、修改和成交事件事实。",
        "subdomain": "order_flow",
        "sources": ["databento_mbo", "databento_mbp10", "databento_trades", "cfa_trading_costs"],
        "applies": ["构造 order flow proxy、OFI、signed volume 或 imbalance 特征", "把订单流代理接入 AI scoring 或交易复盘"],
        "not_applies": ["需要重建真实队列位置但只有聚合或 OHLCV 数据", "没有声明采样窗口、重采样规则和方向推断方法"],
    },
    {
        "task": "P37-D-M05",
        "slug": "cvd_interpretation_caveat",
        "title": "CVD 只能作为订单流代理，不能单独定义趋势结论",
        "claim": "Cumulative Volume Delta 或 Volume Delta 只能作为指定数据源和采样规则下的订单流代理；CVD 背离、上升或下降不得单独证明趋势、反转或交易优势。",
        "subdomain": "order_flow",
        "sources": ["overcharts_volume_delta", "databento_trades", "databento_mbo", "cfa_trade_strategy"],
        "applies": ["审计 CVD、Volume Delta、bid/ask volume 或主动成交量解释", "把 CVD 作为交易候选的辅助上下文"],
        "not_applies": ["缺少逐笔成交或 bid/ask 归属数据", "把 CVD 直接当成买卖点、止损止盈、仓位或最终交易许可"],
    },
    {
        "task": "P37-D-M06",
        "slug": "funding_open_interest_context_required",
        "title": "资金费率和持仓量必须声明衍生品上下文",
        "claim": "Funding rate、open interest、合约持仓量和永续合约定位指标必须声明交易所、合约类型、时间戳、结算机制和样本范围；不得把单所资金费率或 OI 当成全市场方向事实。",
        "subdomain": "derivatives_flow",
        "sources": ["binance_funding_rate", "binance_open_interest", "brunnermeier_pedersen", "ecb_liquidity"],
        "applies": ["分析永续合约资金费率、OI、杠杆拥挤和流动性压力", "把衍生品流指标作为交易候选背景特征"],
        "not_applies": ["现货、股票或无 funding/OI 机制的市场", "没有合约规格、结算时间和交易所覆盖说明"],
    },
    {
        "task": "P37-D-M07",
        "slug": "liquidity_regime_required",
        "title": "流动性状态必须按 regime 标注",
        "claim": "Microstructure 特征必须区分 normal、thin、stressed、event-driven、rollover 或 session-specific liquidity regime；不得把正常时段的盘口特征直接外推到压力、休市前后或低流动性时段。",
        "subdomain": "liquidity_regime",
        "sources": ["ecb_liquidity", "brunnermeier_pedersen", "cfa_trade_strategy", "cfa_trading_costs"],
        "applies": ["审计盘口、成交、滑点、市场影响或订单流特征的 regime 适用范围", "把流动性状态作为 backtest、replay 或 live execution 输入"],
        "not_applies": ["没有交易时段、事件日、交易量或报价可用性信息", "需要证明某个 regime 下必然盈利"],
    },
    {
        "task": "P37-D-M08",
        "slug": "market_impact_cost_required",
        "title": "市场影响成本必须进入微观结构解释边界",
        "claim": "使用盘口深度、订单流或短周期信号评估交易候选时，必须考虑订单规模、执行速度、流动性、临时/永久市场影响和机会成本；不得只看理论信号而忽略执行带来的价格冲击。",
        "subdomain": "market_impact",
        "sources": ["almgren_chriss", "cfa_trading_costs", "cfa_trade_strategy", "ecb_liquidity"],
        "applies": ["高周转、短周期、大单、薄市场或盘口驱动策略", "把 microstructure signal 接入回测、回放、模拟或交易质量复盘"],
        "not_applies": ["只做理论研究且不评估可执行性", "需要直接给出执行算法、下单拆分或最优执行参数"],
    },
    {
        "task": "P37-D-M09",
        "slug": "high_frequency_signal_latency_boundary",
        "title": "高频微观结构信号必须声明延迟和时钟同步边界",
        "claim": "高频盘口、成交、订单流和微观结构信号必须声明数据延迟、处理延迟、时钟同步、事件顺序和可执行窗口；无法证明时间一致性时，不能用于声称实时交易优势。",
        "subdomain": "latency_timing",
        "sources": ["esma_rts25", "cfa_trading_costs", "databento_mbo", "nasdaq_itch_spec"],
        "applies": ["毫秒/微秒级 market data、order book replay、event-driven execution 或 HFT 特征", "审计 signal timestamp、decision timestamp 和 execution timestamp 的一致性"],
        "not_applies": ["日线或低频研究不涉及事件级顺序", "没有可靠时钟、接收时间、处理时间和交易所事件时间字段"],
    },
    {
        "task": "P37-D-M10",
        "slug": "slippage_regime_caveat",
        "title": "滑点必须按流动性和执行 regime 建模",
        "claim": "Slippage 不应使用固定常数覆盖所有品种、时段和订单类型；微观结构相关滑点必须按流动性、价差、深度、订单规模、波动、延迟和执行方式分层建模或审计。",
        "subdomain": "slippage",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy", "almgren_chriss", "ecb_liquidity"],
        "applies": ["回测、回放、模拟盘、纸面交易或实盘复盘中的滑点假设", "把 short-horizon signal 转成可执行交易候选"],
        "not_applies": ["只研究理论指标不涉及成交", "缺少订单类型、订单规模、成交规则或市场数据粒度"],
    },
    {
        "task": "P37-D-M11",
        "slug": "thin_market_execution_risk",
        "title": "薄市场执行风险必须显式阻断或降级",
        "claim": "在薄市场、低深度、宽价差、事件冲击或流动性枯竭场景下，微观结构信号必须降级为风险提示或要求人工/风控复核；不能把正常市场假设沿用到 thin market 执行。",
        "subdomain": "thin_market",
        "sources": ["ecb_liquidity", "brunnermeier_pedersen", "cfa_trade_strategy", "sec_15c3_5"],
        "applies": ["低流动性品种、盘前盘后、重大事件、市场压力或异常价差状态", "设计 final gate 前的风险提示、降级或人工复核规则"],
        "not_applies": ["没有行情质量、深度、成交量或事件上下文", "把风险提示直接写成自动交易许可"],
    },
    {
        "task": "P37-D-M12",
        "slug": "microstructure_feature_not_universal",
        "title": "微观结构特征不得跨市场无条件泛化",
        "claim": "盘口、订单流、CVD、funding、OI、深度、滑点和市场影响特征不能跨资产、交易所、数据源、交易时段和 market regime 无条件泛化；每个特征必须声明适用市场、数据契约和验证范围。",
        "subdomain": "feature_boundary",
        "sources": ["databento_mbo", "binance_funding_rate", "cfa_trading_costs", "almgren_chriss", "esma_rts25"],
        "applies": ["把微观结构特征用于策略工程、AI scoring、RAG 解释或交易质量复盘", "审计跨市场、跨交易所、跨数据供应商迁移的特征声明"],
        "not_applies": ["只做单市场描述且不迁移", "需要证明某个 microstructure feature 在所有市场长期有效"],
    },
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def source_refs(source_keys: list[str]) -> list[dict[str, Any]]:
    refs = []
    for index, key in enumerate(source_keys, start=1):
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
    source_items = source_refs(spec["sources"])
    normalized_claim = f"microstructure.{spec['slug']}.v1"
    candidate_id = f"cand_{TODAY.replace('-', '')}_phase37_market_microstructure_{slugify(spec['slug'])}_001"
    tree_node_id = TREE_NODE if spec["subdomain"] != "order_flow" else "kt.market_microstructure.order_flow"
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": candidate_id,
        "research_task_id": spec["task"],
        "status": {
            "review_status": "sourced",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Market Microstructure 候选生成完成；等待外部 AI/人工严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": tree_node_id,
            "canonical_node_id": tree_node_id,
            "tree_path": TREE_PATH if tree_node_id == TREE_NODE else f"{TREE_PATH} / Order Flow",
            "related_nodes": [
                "kt.trading_engineering",
                "kt.market_microstructure",
                "kt.trading_engineering.data_engineering",
                "kt.kline_strategy",
                "kt.backtest",
                "kt.replay_simulation",
                "kt.live_execution",
                "kt.risk_management",
                "kt.ai_engineering.llm_training",
            ],
            "partition_id": PARTITION,
            "domain": "market_microstructure",
            "subdomain": spec["subdomain"],
            "rule_type": "trading_microstructure_boundary_rule",
            "claim_type": "methodological_constraint",
            "used_for": [
                "market_microstructure_audit",
                "strategy_design_audit",
                "execution_cost_boundary",
                "ai_trader_project_gap_audit",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "本候选主归属 Trading Engineering / Market Microstructure。AI Engineering 只能引用本规则，不得把盘口、订单流、滑点、funding/OI 或市场影响本体改写为模型训练规则。",
        },
        "claim": {
            "claim_id": f"claim_{spec['task'].lower().replace('-', '_')}",
            "title": spec["title"],
            "statement": spec["claim"],
            "normalized_claim": normalized_claim,
            "evidence_summary": "；".join(item["evidence_summary"] for item in source_items[:3]),
            "interpretation_notes": "本候选只定义市场微观结构解释、数据和执行边界，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_market_specific_mapping",
            "asset": "general",
            "timeframe": "event_to_intraday",
            "data_granularity": "order_book_trades_or_derivatives_market_data",
            "project_type": "trading_ai_support_layer",
            "applies_when": spec["applies"],
            "not_applicable_when": spec["not_applies"]
            + [
                "需要具体买卖点、仓位、杠杆、止损止盈价格、交易所私有配置、账户事实或实盘权限时，应由外接项目事实层、执行层和风控层处理。",
                "AI Engineering 只能引用本规则，不得把本规则改写为 LLM 训练、MCP、RAG 或模型部署本体规则。",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含任何外接项目私有策略参数。",
                "微观结构结论必须保留市场、交易所、数据源、时间戳、粒度、执行和验证边界。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "官方文档和平台文档只能支撑数据字段、接口语义和工程边界，不能证明交易优势。",
                "论文或专业机构资料支持方法边界，不能替代具体交易所、数据供应商或外接项目契约。",
                "本候选不提供任何投资建议或实盘执行许可。",
            ],
        },
        "source_refs": source_items,
        "source_quality": {
            "overall_reliability": "medium_high",
            "score": round(sum(item["score"] for item in source_items) / len(source_items), 1),
            "score_version": "phase37_market_microstructure_source_scoring_v1",
            "primary_source_count": sum(1 for item in source_items if item["reliability"] == "high"),
            "supporting_source_count": sum(1 for item in source_items if item["reliability"] != "high"),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式入库前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "供应商、交易平台和交易所接口文档只可作为数据语义与工程边界证据，不能单独证明信号有效。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "Phase 36/38/40/41 AI Engineering 知识边界",
                "现有 Trading Engineering formal 知识",
                "Phase 37 Trading 与 AI 跨分支引用契约",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与可见正式知识的直接冲突；本候选只定义 Trading Engineering 市场微观结构规则本体，AI Engineering 只能引用。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检索 Trading Engineering 市场微观结构边界。",
                "用于审计交易项目方案中是否缺少盘口、订单流、流动性、滑点、延迟、市场影响和数据源边界。",
                "用于辅助外接项目设计数据契约、特征边界、审计清单和 reason code。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
                "不得把候选知识当作 reviewed、approved、default guidance 或 hard gate。",
                "不得绕过外接项目事实层、数据契约、执行适配器、风控 hard gate 或人工治理流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 37 Market Microstructure candidate only; formal reviewed requires later reviewed-preparation gate.",
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
            "reviewer": "codex_pre_audit_generation",
            "reviewed_at": TODAY,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 claim？",
                "是否需要补充更强的一手论文、监管材料、交易所规范或数据供应商字段级证据？",
                "是否存在与现有 Data Engineering、Backtest、Replay、Live Execution、Risk Management 或 AI Engineering formal 知识的重叠，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 37 P37-D Market Microstructure 队列生成 Trading Engineering 候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录专业机构、监管、交易所/API、数据供应商和论文来源摘要。",
                },
            ],
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending_ai_audit",
            "current_task_id": TASK_ID,
            "next_action": "export_candidate_audit_package",
            "next_allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
            "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formalization_allowed": False,
            "conversion_target": {
                "proposed_knowledge_id": f"kb_03_market_microstructure.{spec['slug']}.v1",
                "target_review_status": "draft_only_after_external_audit",
                "target_default_guidance": "deny",
            },
        },
        "contribution": {
            "origin": "codex_research_ingestion_phase37",
            "private_data_removed": True,
            "contains_account_facts": False,
            "contains_secret": False,
            "contains_project_private_strategy": False,
        },
    }


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    cid = candidate.get("candidate_id", "<missing>")
    if candidate.get("classification", {}).get("partition_id") != PARTITION:
        errors.append(f"{cid}: partition mismatch")
    if candidate.get("status", {}).get("ingestion_decision") != "candidate_ready":
        errors.append(f"{cid}: ingestion_decision must be candidate_ready")
    if len(candidate.get("source_refs", [])) < 3:
        errors.append(f"{cid}: source_refs < 3")
    if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
        errors.append(f"{cid}: default guidance must be deny")
    if candidate.get("machine_gate", {}).get("approved_allowed") is not False:
        errors.append(f"{cid}: approved_allowed must be false")
    if candidate.get("machine_gate", {}).get("hard_gate_allowed") is not False:
        errors.append(f"{cid}: hard_gate_allowed must be false")
    return errors


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_research_report(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> None:
    lines = [
        "# Phase 37 Market Microstructure 候选知识采集记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 范围",
        "",
        "本批覆盖 Phase 37 D 组 Market Microstructure 12 条 P0 候选知识。候选只做审计准备，不创建 formal reviewed，不进入 approved/default/hard gate。",
        "",
        "## 来源原则",
        "",
        "- 优先使用 CFA Institute、SEC/ESMA/ECB 等专业机构或监管来源、交易所/API 官方文档、数据供应商字段级文档和学术论文。",
        "- 供应商、平台和教育资料只作为 supporting evidence，不单独证明交易优势。",
        "- 微观结构特征必须声明数据源、交易所、市场、时间戳、粒度、执行和 regime 边界。",
        "",
        "## 采集结果",
        "",
        f"- 候选数量：{len(candidates)}",
        f"- 质量门禁：{'pass' if quality['quality_gate']['pass'] else 'fail'}",
        f"- 最少来源数：{quality['source_count_min']}",
        "",
    ]
    for item in candidates:
        lines.extend(
            [
                f"### {item['research_task_id']} {item['claim']['title']}",
                "",
                f"- candidate_id: `{item['candidate_id']}`",
                f"- normalized_claim: `{item['claim']['normalized_claim']}`",
                f"- tree_node_id: `{item['classification']['tree_node_id']}`",
                f"- 来源数：{len(item['source_refs'])}",
                f"- statement: {item['claim']['statement']}",
                "",
                "主要来源：",
            ]
        )
        for source in item["source_refs"]:
            lines.append(f"- {source['source_title']}：{source['source_url']}")
        lines.append("")
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [make_candidate(spec) for spec in CANDIDATES]
    errors: list[str] = []
    for candidate in candidates:
        errors.extend(validate_candidate(candidate))
        write_json(CAND_DIR / f"{candidate['candidate_id']}.json", candidate)

    quality = {
        "quality_gate": {"pass": not errors, "errors": errors},
        "phase": PHASE,
        "task_id": TASK_ID,
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
        "task_id": TASK_ID,
        "generated_at": TODAY,
        "scope": "Market Microstructure D group",
        "partition_id": PARTITION,
        "candidate_count": len(candidates),
        "candidate_ids": [item["candidate_id"] for item in candidates],
        "status": "pass" if not errors else "fail",
        "notes": [
            "Candidates are not formal reviewed knowledge.",
            "External strict audit must decide accepted_for_draft / needs_more_evidence / rejected.",
            "Market Microstructure belongs to Trading Engineering; AI Engineering may only reference it.",
        ],
    }
    write_json(QUALITY_GATE, quality)
    write_json(GENERATION_REPORT.with_suffix(".json"), generation)
    GENERATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    GENERATION_REPORT.write_text(
        "\n".join(
            [
                "# Phase 37 Market Microstructure 候选生成报告",
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
