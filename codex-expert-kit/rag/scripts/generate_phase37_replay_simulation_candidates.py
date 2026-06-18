"""Generate Phase 37 Replay / Simulation candidate knowledge.

This script creates candidate and audit-support artifacts only. It does not
create formal reviewed knowledge, approve knowledge, enable default guidance,
or create hard gates.
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
TASK_ID = "CEK-TA-424"
PHASE = "37"
PARTITION = "KB_05_REPLAY_SIMULATION"
TREE_NODE = "kt.replay_simulation"
TREE_PATH = "CEK-TA / Trading Engineering / Replay Simulation"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase37_replay_simulation_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase37_replay_simulation_candidate_generation_report.md", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase37_replay_simulation_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "quantconnect_fills": {
        "source_title": "Trade Fills - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
        "source_type": "framework_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect explains that fill models determine fill price and quantity, may incorporate spread costs, and work with slippage models.",
        "limitations": ["Platform-specific implementation semantics; external projects must map their own fill model."],
    },
    "quantconnect_slippage": {
        "source_title": "Slippage Models - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts",
        "source_type": "framework_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect defines slippage as the difference between expected and actual fill price and models it to make backtests more realistic.",
        "limitations": ["Platform-specific; supports concept and modeling boundary, not universal parameter values."],
    },
    "quantconnect_fees": {
        "source_title": "Transaction Fees - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/transaction-fees/key-concepts",
        "source_type": "framework_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect fee models simulate brokerage transaction fees so replay/backtest results include cost assumptions.",
        "limitations": ["Platform-specific; external projects must use their brokerage/exchange fee schedule."],
    },
    "quantconnect_brokerage": {
        "source_title": "Reality Modelling - Brokerage Models",
        "source_url": "https://www.quantconnect.com/docs/v1/algorithm-reference/reality-modelling",
        "source_type": "framework_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect brokerage models set fees, fill models, slippage models and validate whether orders can be submitted to a brokerage model.",
        "limitations": ["Older platform documentation; use as implementation pattern, not CEK-TA mandatory tooling."],
    },
    "backtrader_order_execution": {
        "source_title": "Orders - Creation/Execution",
        "source_url": "https://www.backtrader.com/docu/order-creation-execution/order-creation-execution/",
        "source_type": "framework_doc",
        "publisher": "Backtrader",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "stable",
        "evidence_summary": "Backtrader documents broker order execution assumptions, including that the current data bar has already happened and cannot be used to execute an order unless special cheat modes are used.",
        "limitations": ["Framework-specific semantics; useful for event-clock and same-bar ambiguity boundaries."],
    },
    "backtrader_slippage": {
        "source_title": "Broker - Slippage",
        "source_url": "https://www.backtrader.com/docu/slippage/slippage/",
        "source_type": "framework_doc",
        "publisher": "Backtrader",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "stable",
        "evidence_summary": "Backtrader broker supports slippage configuration such as percentage/fixed slippage and open-price slippage handling.",
        "limitations": ["Framework-specific; does not define universal market slippage."],
    },
    "backtrader_cheat_open": {
        "source_title": "Broker - Cheat-On-Open",
        "source_url": "https://www.backtrader.com/docu/cerebro/cheat-on-open/cheat-on-open/",
        "source_type": "framework_doc",
        "publisher": "Backtrader",
        "reliability": "medium",
        "score": 74,
        "freshness": "stable",
        "evidence_summary": "Backtrader documents cheat-on-open behavior as a deliberate simulation mode that changes when orders can be issued relative to the open.",
        "limitations": ["Use only as evidence that event timing modes must be declared."],
    },
    "hftbacktest_order_fill": {
        "source_title": "Order Fill",
        "source_url": "https://hftbacktest.readthedocs.io/en/latest/order_fill.html",
        "source_type": "framework_doc",
        "publisher": "HftBacktest",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "HftBacktest distinguishes no-partial-fill and partial-fill exchange simulations and warns that market-data replay cannot alter the market.",
        "limitations": ["Framework-specific; strong support for replay/fill-model caveats, not a universal exchange simulator."],
    },
    "hftbacktest_latency": {
        "source_title": "Latency Models",
        "source_url": "https://hftbacktest.readthedocs.io/en/latest/latency_models.html",
        "source_type": "framework_doc",
        "publisher": "HftBacktest",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "HftBacktest provides order latency models and discusses interpolation from actual latency data for more realistic replay.",
        "limitations": ["Framework-specific; supports latency-model requirement, not default latency values."],
    },
    "hftbacktest_project": {
        "source_title": "hftbacktest project",
        "source_url": "https://github.com/nkaz001/hftbacktest",
        "source_type": "official_repo",
        "publisher": "HftBacktest",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "The project focuses on feed/order latencies and queue position for market replay-based backtesting with order-book and trade tick data.",
        "limitations": ["Project-level summary; use with detailed docs for reviewed claims."],
    },
    "ibkr_tws_api": {
        "source_title": "TWS API Documentation",
        "source_url": "https://www.interactivebrokers.com/campus/ibkr-api-page/trader-workstation-api/",
        "source_type": "official_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR documents TWS API connectivity for retrieving and sending data and orders, supporting the need to distinguish simulated and broker/API behavior.",
        "limitations": ["Broker-specific; supports adapter boundary, not a universal exchange rule."],
    },
    "ibkr_order_types": {
        "source_title": "Order Types",
        "source_url": "https://www.interactivebrokers.com/campus/ibkr-api-page/order-types/",
        "source_type": "official_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR documents available order types and order fields, supporting the need to map simulated orders to broker-supported orders.",
        "limitations": ["Broker-specific order semantics."],
    },
    "fix_execution_report": {
        "source_title": "Execution Report <8> message - FIX 4.4",
        "source_url": "https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html",
        "source_type": "standard_doc",
        "publisher": "OnixS FIX Dictionary",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "stable",
        "evidence_summary": "FIX Execution Report confirms receipt, changes, order status, fills, rejects and fees calculations, supporting order-state and fill-event trace boundaries.",
        "limitations": ["FIX dictionary mirror; useful for status semantics, not venue-specific implementation."],
    },
    "fix_ordstatus": {
        "source_title": "OrdStatus <39> field - FIX 4.4",
        "source_url": "https://www.onixs.biz/fix-dictionary/4.4/tagnum_39.html",
        "source_type": "standard_doc",
        "publisher": "OnixS FIX Dictionary",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "stable",
        "evidence_summary": "FIX OrdStatus values include new, partially filled, filled, canceled, rejected, pending cancel and expired states.",
        "limitations": ["Status vocabulary support only; venue adapters still need native mapping."],
    },
    "binance_filters": {
        "source_title": "Filters",
        "source_url": "https://developers.binance.com/docs/binance-spot-api-docs/filters",
        "source_type": "exchange_rule",
        "publisher": "Binance Open Platform",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance official filters define LOT_SIZE, MIN_NOTIONAL and NOTIONAL constraints for acceptable order quantity and notional values.",
        "limitations": ["Crypto venue-specific; use as example that exchange constraints must be simulated per venue."],
    },
    "cme_matching": {
        "source_title": "Matching Algorithm Overview",
        "source_url": "https://www.cmegroup.com/education/matching-algorithm-overview",
        "source_type": "exchange_rule",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "stable",
        "evidence_summary": "CME describes matching algorithms such as allocation, FIFO, pro-rata and configurable variants, supporting venue-specific execution-rule modeling.",
        "limitations": ["Educational overview; specific products require current rulebook/session mapping."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P37-F-R01",
        "slug": "event_clock_required",
        "title": "Replay 必须声明事件时钟",
        "statement": "Replay / Simulation 必须声明事件时钟、撮合时点、信号生成时点和订单提交时点；未声明事件顺序的模拟结果不能作为执行质量或策略可交易性的证据。",
        "subdomain": "event_clock",
        "claim_type": "simulation_timing_boundary",
        "sources": ["backtrader_order_execution", "backtrader_cheat_open", "hftbacktest_latency", "quantconnect_fills"],
    },
    {
        "task": "P37-F-R02",
        "slug": "ohlc_same_bar_tp_sl_ordering_required",
        "title": "OHLC 同根 K TP/SL 必须声明成交顺序假设",
        "statement": "仅有 OHLC bar 时，同一根 K 内同时触达止盈和止损不能声称真实先后顺序；系统必须显式声明 conservative、optimistic、next-bar 或 tick-replay 等处理假设。",
        "subdomain": "ohlc_same_bar",
        "claim_type": "fill_ordering_boundary",
        "sources": ["backtrader_order_execution", "backtrader_cheat_open", "quantconnect_fills", "hftbacktest_order_fill"],
    },
    {
        "task": "P37-F-R03",
        "slug": "fill_model_assumption_required",
        "title": "Fill model 假设必须显式记录",
        "statement": "Simulation 中的 market、limit、stop、stop-limit 和 auction 成交必须绑定 fill model 假设，包括价格来源、数量可得性、spread、滑点、队列/流动性限制和适用市场。",
        "subdomain": "fill_model",
        "claim_type": "execution_assumption_contract",
        "sources": ["quantconnect_fills", "quantconnect_slippage", "hftbacktest_order_fill", "cme_matching"],
    },
    {
        "task": "P37-F-R04",
        "slug": "partial_fill_policy_required",
        "title": "部分成交策略必须定义",
        "statement": "Replay / Simulation 必须定义 partial fill、no fill、残量、超时、取消和后续状态更新策略；不能默认所有订单都完整成交。",
        "subdomain": "partial_fill",
        "claim_type": "execution_state_contract",
        "sources": ["hftbacktest_order_fill", "fix_execution_report", "fix_ordstatus", "quantconnect_fills"],
    },
    {
        "task": "P37-F-R05",
        "slug": "latency_model_required",
        "title": "延迟模型必须定义",
        "statement": "Simulation 必须声明行情延迟、决策延迟、订单发送延迟、交易所确认延迟和回报延迟；没有延迟模型的高频或盘中执行模拟只能作为粗略研究。",
        "subdomain": "latency",
        "claim_type": "latency_boundary_rule",
        "sources": ["hftbacktest_latency", "hftbacktest_project", "ibkr_tws_api", "quantconnect_slippage"],
    },
    {
        "task": "P37-F-R06",
        "slug": "paper_trading_not_equal_live",
        "title": "Paper trading 不等于实盘",
        "statement": "Paper trading、模拟盘或沙盒执行只能验证系统流程和部分执行假设，不能等同于真实成交、真实滑点、真实拒单、真实延迟或真实风控表现。",
        "subdomain": "paper_trading",
        "claim_type": "simulation_live_boundary",
        "sources": ["ibkr_tws_api", "ibkr_order_types", "quantconnect_brokerage", "hftbacktest_order_fill"],
    },
    {
        "task": "P37-F-R07",
        "slug": "exchange_rule_simulation_required",
        "title": "交易所规则必须进入模拟约束",
        "statement": "Replay / Simulation 若声称接近实盘，必须按市场和品种映射交易所/经纪商规则，包括交易时段、撮合算法、订单类型、最小数量、价格步长、涨跌停/暂停和拒单条件。",
        "subdomain": "exchange_rules",
        "claim_type": "venue_rule_mapping_contract",
        "sources": ["cme_matching", "binance_filters", "ibkr_order_types", "quantconnect_brokerage"],
    },
    {
        "task": "P37-F-R08",
        "slug": "minimum_order_size_required",
        "title": "最小下单量和最小名义金额必须模拟",
        "statement": "Simulation 必须校验交易所或经纪商的最小数量、步长、最小名义金额、价格精度和订单类型限制；未通过约束的订单应被模拟为拒单或不可提交。",
        "subdomain": "exchange_constraints",
        "claim_type": "order_constraint_contract",
        "sources": ["binance_filters", "ibkr_order_types", "quantconnect_brokerage", "fix_execution_report"],
    },
    {
        "task": "P37-F-R09",
        "slug": "order_reject_and_cancel_policy_required",
        "title": "拒单和撤单策略必须定义",
        "statement": "Replay / Simulation 必须定义订单拒绝、撤单、撤改单、过期、pending 状态和回报缺失的处理；不能只模拟 filled 状态。",
        "subdomain": "order_lifecycle",
        "claim_type": "order_state_contract",
        "sources": ["fix_execution_report", "fix_ordstatus", "ibkr_tws_api", "quantconnect_brokerage"],
    },
    {
        "task": "P37-F-R10",
        "slug": "simulation_live_gap_report_required",
        "title": "模拟盘与实盘差异必须出 gap report",
        "statement": "从 simulation / paper 进入 live 前，必须记录成交价格、成交数量、延迟、拒单、滑点、费用、订单状态和风控触发的模拟-实盘差异报告。",
        "subdomain": "simulation_live_gap",
        "claim_type": "audit_report_contract",
        "sources": ["quantconnect_fills", "quantconnect_slippage", "fix_execution_report", "ibkr_tws_api"],
    },
    {
        "task": "P37-F-R11",
        "slug": "tick_replay_vs_ohlc_boundary",
        "title": "Tick replay 与 OHLC replay 边界必须区分",
        "statement": "Tick/order-book replay 可以提供比 OHLC replay 更细的路径和队列信息，但仍不能改变历史市场；OHLC replay 不能伪装成 tick 级成交真实性。",
        "subdomain": "tick_replay",
        "claim_type": "data_granularity_boundary",
        "sources": ["hftbacktest_order_fill", "hftbacktest_project", "backtrader_order_execution", "quantconnect_fills"],
    },
    {
        "task": "P37-F-R12",
        "slug": "execution_cost_consistency_required",
        "title": "执行成本在 backtest、replay、paper、live 间必须一致可追踪",
        "statement": "Backtest、Replay、Paper 和 Live 的费用、spread、滑点、market impact 与 fill 假设必须有版本化映射；成本口径不一致时不能直接比较表现。",
        "subdomain": "execution_cost",
        "claim_type": "cost_consistency_contract",
        "sources": ["quantconnect_fees", "quantconnect_slippage", "quantconnect_fills", "fix_execution_report"],
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slug_id(slug: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", slug.lower()).strip("_")


def source_refs(keys: list[str]) -> list[dict[str, Any]]:
    refs = []
    for idx, key in enumerate(keys, start=1):
        source = dict(SOURCES[key])
        source.update(
            {
                "source_id": f"src_{idx:03d}",
                "accessed_at": TODAY,
                "version": None,
                "relevance": "high" if idx <= 2 else "medium_high",
                "quoted_excerpt_allowed": False,
            }
        )
        refs.append(source)
    return refs


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = source_refs(item["sources"])
    source_score = round(sum(float(source["score"]) for source in refs) / len(refs), 2)
    evidence_summary = "；".join(source["evidence_summary"] for source in refs[:3])
    slug = slug_id(item["slug"])
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": f"cand_{TODAY.replace('-', '')}_phase37_replay_simulation_{slug}_001",
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Replay / Simulation 候选已完成来源采集，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": TREE_NODE,
            "canonical_node_id": TREE_NODE,
            "tree_path": TREE_PATH,
            "related_nodes": [
                "kt.trading_engineering",
                "kt.trading_engineering.backtest",
                "kt.trading_engineering.data_engineering",
                "kt.market_microstructure",
                "kt.live_execution",
                "kt.risk_management",
                "kt.ai_engineering.llm_training",
            ],
            "partition_id": PARTITION,
            "domain": "replay_simulation",
            "subdomain": item["subdomain"],
            "rule_type": "replay_simulation_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "replay_review",
                "simulation_audit",
                "paper_trading_readiness_review",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "本候选主归属 Trading Engineering / Replay Simulation。AI Engineering 只能引用本规则，不得把成交模拟、交易所规则或执行假设改写为模型训练本体规则。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"replay.{slug}.v1",
            "evidence_summary": evidence_summary,
            "interpretation_notes": "本候选只定义 replay/simulation 的事件、成交、延迟、交易所规则、订单状态和模拟-实盘差异边界，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_venue_specific_mapping",
            "asset": "general",
            "timeframe": "historical_replay_or_paper_simulation",
            "data_granularity": "ohlc_tick_quote_order_book_and_order_events",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "审计 replay、simulation、paper trading、fill model、latency model 或交易所规则模拟",
                "把模拟成交结果用于 AI scoring、paper/live 前置评估、回测复核或执行质量研究",
            ],
            "not_applicable_when": [
                "需要直接生成买卖点、仓位、杠杆、止损止盈或实盘执行建议",
                "问题属于 live execution 真实订单路由、账户同步或 risk hard gate，应由对应分支处理",
                "没有市场、交易所、品种、数据粒度、事件时钟或订单状态来源",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含任何外接项目私有策略参数。",
                "模拟结果必须保留事件时钟、成交模型、成本、延迟、订单状态、交易所规则和数据粒度边界。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "平台和框架文档只能支持实现模式，不能证明任何特定策略可实盘盈利。",
                "交易所或经纪商规则具有市场、品种、时间和版本差异，外接项目必须映射自己的 venue/rulebook。",
                "本候选不提供任何投资建议、订单建议或实盘许可。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "medium_high",
            "score": source_score,
            "score_version": "phase37_replay_simulation_source_scoring_v1",
            "primary_source_count": len([source for source in refs if source["reliability"] in {"high", "medium_high"}]),
            "supporting_source_count": len(refs),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": ["本批候选大量使用平台/框架/交易所文档，审计时必须防止把具体平台实现泛化为通用交易所真理。"],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "KB_04_BACKTEST",
                "KB_03_MARKET_MICROSTRUCTURE",
                "KB_06_LIVE_EXECUTION",
                "KB_07_RISK_MANAGEMENT",
                "KB_AI_ENGINEERING",
            ],
            "resolution_summary": "未发现与当前可见 CEK-TA formal knowledge 直接冲突；候选不会进入默认指导，仍需外部严格审计。",
            "approval_allowed": True,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计 replay/simulation 时声明事件时钟、成交模型、延迟、成本和交易所规则边界",
                "用于审计模拟盘、回放、paper trading 和 backtest-to-live gap 报告",
                "用于阻止 AI 把模拟成交当作真实成交或实盘许可",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈参数或实盘订单",
                "不得据此声称某个策略可盈利或可实盘",
                "不得把某个框架或交易所的实现细节写成所有市场通用规则",
            ],
            "requires_context": [
                "market",
                "venue",
                "instrument",
                "data_granularity",
                "event_clock",
                "order_type",
                "fill_model_version",
                "latency_model_version",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; pending external strict audit; not formal reviewed; no default guidance.",
            "requires_human_escalation": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "conversion_target": {
            "proposed_knowledge_id": f"kb_05_replay_simulation.{slug}.v1",
            "target_review_status": "candidate_only_pending_external_audit",
            "default_guidance_after_conversion": "deny_until_reviewed_caveat_only_audit",
            "formalization_blockers": ["requires_external_strict_audit"],
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
        },
        "workflow": {
            "phase": PHASE,
            "task_id": TASK_ID,
            "stage": "pending_external_audit",
            "next_allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
        },
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings = [
        "本批只是 Replay / Simulation candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
        "成交模型、延迟模型和交易所规则必须按市场/交易所/品种映射，不得泛化为统一实盘真理。",
    ]
    if len(candidates) != 12:
        failures.append(f"expected 12 candidates, got {len(candidates)}")
    expected_tasks = {f"P37-F-R{idx:02d}" for idx in range(1, 13)}
    actual_tasks = {candidate.get("research_task_id") for candidate in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research task set: {sorted(actual_tasks ^ expected_tasks)}")
    for candidate in candidates:
        cid = candidate.get("candidate_id", "<unknown>")
        if candidate.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition mismatch")
        if candidate.get("classification", {}).get("canonical_node_id") != TREE_NODE:
            failures.append(f"{cid}: canonical_node_id mismatch")
        if candidate.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if candidate.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default_guidance must be deny")
        if candidate.get("machine_gate", {}).get("approved_allowed") is not False:
            failures.append(f"{cid}: approved_allowed must be false")
        if candidate.get("machine_gate", {}).get("hard_gate_allowed") is not False:
            failures.append(f"{cid}: hard_gate_allowed must be false")
        if len(candidate.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        blob = json.dumps(candidate, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase37_replay_simulation_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": 12,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }


def write_research_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    lines = [
        "# Phase 37 Replay / Simulation Candidate Research",
        "",
        f"- generated_at: {TODAY}",
        f"- task_id: {TASK_ID}",
        f"- partition: {PARTITION}",
        f"- candidate_count: {len(candidates)}",
        f"- gate_status: {gate['gate_status']}",
        "",
        "## 来源种子",
        "",
    ]
    for key, source in SOURCES.items():
        lines.append(f"- `{key}`: {source['source_title']} ({source['publisher']}) - {source['source_url']}")
    lines.extend(["", "## 候选知识点", ""])
    for candidate in candidates:
        lines.append(f"- `{candidate['research_task_id']}` `{candidate['claim']['normalized_claim']}`: {candidate['claim']['statement']}")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 本批候选只处理 replay/simulation 规则本体，不处理实盘下单权限、账户事实、仓位建议或策略收益声明。",
            "- 候选不得直接进入 reviewed、approved、default guidance 或 hard gate。",
        ]
    )
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [build_candidate(item) for item in ITEMS]
    for candidate in candidates:
        slug = candidate["claim"]["normalized_claim"].split(".")[1]
        path = CAND_DIR / f"cand_{TODAY.replace('-', '')}_phase37_replay_simulation_{slug}_001.json"
        write_json(path, candidate)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_research_report(candidates, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase37_replay_simulation_candidate_generation",
            "generated_at": TODAY,
            "task_id": TASK_ID,
            "partition_id": PARTITION,
            "candidate_count": len(candidates),
            "candidate_dir": str(CAND_DIR),
            "quality_gate": gate,
            "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "quality_gate": str(QUALITY_GATE)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
