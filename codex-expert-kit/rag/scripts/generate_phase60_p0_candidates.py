"""Generate Phase 60 P0 sandbox / replay / paper trading candidates."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"


SOURCES: dict[str, dict[str, Any]] = {
    "nautilus_arch": {
        "source_title": "Architecture",
        "source_url": "https://nautilustrader.io/docs/latest/concepts/architecture/",
        "source_type": "framework_doc",
        "publisher": "NautilusTrader",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "NautilusTrader documents environment contexts for backtest, sandbox and live, including different data/execution contexts while sharing core runtime components.",
        "limitations": ["Framework-specific; use as environment taxonomy and implementation pattern, not a universal requirement."],
        "source_id": "src_nautilus_arch",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "nautilus_overview": {
        "source_title": "Overview",
        "source_url": "https://nautilustrader.io/docs/latest/concepts/overview/",
        "source_type": "framework_doc",
        "publisher": "NautilusTrader",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "NautilusTrader describes a deterministic event-driven runtime for research and live execution, with shared architecture and execution semantics across environments.",
        "limitations": ["Framework-specific; does not prove live profitability or broker-specific equivalence."],
        "source_id": "src_nautilus_overview",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "quantconnect_paper": {
        "source_title": "QuantConnect Paper Trading",
        "source_url": "https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading",
        "source_type": "framework_doc",
        "publisher": "QuantConnect",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect documents paper trading as real-time data with fictional capital where orders are not routed to an exchange and fills are simulated.",
        "limitations": ["Platform-specific paper brokerage behavior; not a universal broker guarantee."],
        "source_id": "src_quantconnect_paper",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "hftbacktest_order_fill": {
        "source_title": "HftBacktest Order Fill",
        "source_url": "https://hftbacktest.readthedocs.io/en/latest/order_fill.html",
        "source_type": "framework_doc",
        "publisher": "HftBacktest",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "HftBacktest discusses market-data replay and fill assumptions, including the critical no-market-impact limitation for replay-based backtesting.",
        "limitations": ["Framework-specific; use to support replay caveats and fill assumption disclosure."],
        "source_id": "src_hftbacktest_order_fill",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "alpaca_paper": {
        "source_title": "Paper Trading",
        "source_url": "https://docs.alpaca.markets/us/docs/paper-trading",
        "source_type": "official_doc",
        "publisher": "Alpaca",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Alpaca documents paper trading limitations such as market impact, information leakage, latency slippage, queue position, price improvement, regulatory fees and dividends.",
        "limitations": ["Broker-specific limitations; useful as paper/live gap examples, not exhaustive for all brokers."],
        "source_id": "src_alpaca_paper",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "ibkr_paper": {
        "source_title": "About Paper Trading Accounts",
        "source_url": "https://www.ibkrguides.com/clientportal/aboutpapertradingaccounts.htm",
        "source_type": "official_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR documents that paper trading accounts simulate most aspects of production accounts but can differ because they are simulators.",
        "limitations": ["IBKR-specific; does not define all paper trading behavior."],
        "source_id": "src_ibkr_paper",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "binance_testnet": {
        "source_title": "General Info",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/general-info",
        "source_type": "official_doc",
        "publisher": "Binance Open Platform",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance USD-M Futures documentation provides testnet REST and WebSocket base URLs and states that most endpoints can be used in the testnet platform.",
        "limitations": ["Binance USD-M Futures-specific endpoint behavior; not a universal exchange testnet rule."],
        "source_id": "src_binance_testnet",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "coinbase_sandbox": {
        "source_title": "Advanced Trade API Sandbox",
        "source_url": "https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/sandbox",
        "source_type": "official_doc",
        "publisher": "Coinbase Developer Platform",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Coinbase documents a sandbox endpoint where Accounts and Orders responses are mocked but have the same format as production.",
        "limitations": ["Static mocked sandbox; useful for API contract testing, not market behavior."],
        "source_id": "src_coinbase_sandbox",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "fix_exec_report": {
        "source_title": "Execution Report <8> message - FIX 4.4",
        "source_url": "https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html",
        "source_type": "standard_doc",
        "publisher": "OnixS FIX Dictionary",
        "reliability": "high",
        "score": 84,
        "freshness": "stable",
        "evidence_summary": "FIX Execution Report is used to confirm order receipt or changes, relay order status, fills, rejects and post-trade fee calculations.",
        "limitations": ["FIX-specific standard; REST/WebSocket broker states still require adapter mapping."],
        "source_id": "src_fix_exec_report",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "phase60_env_contract": {
        "source_title": "Phase 60 Sandbox / Replay / Paper Environment Contract",
        "source_url": "docs/contracts/phase60_sandbox_replay_paper_environment_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 88,
        "freshness": "current",
        "evidence_summary": "CEK-TA internal contract defining EnvironmentManifest fields, owner boundaries and machine gate restrictions.",
        "limitations": ["Internal CEK-TA schema; reviewed status requires external audit."],
        "source_id": "src_phase60_env_contract",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "phase60_gap_contract": {
        "source_title": "Phase 60 Environment Promotion Decision and Gap Report Contract",
        "source_url": "docs/contracts/phase60_environment_promotion_gap_report_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 88,
        "freshness": "current",
        "evidence_summary": "CEK-TA internal contract defining promotion decisions, gap report fields, required evidence and hard boundaries.",
        "limitations": ["Internal CEK-TA schema; reviewed status requires external audit."],
        "source_id": "src_phase60_gap_contract",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
}


CANDIDATES: list[dict[str, Any]] = [
    {
        "task": "P60-A01",
        "candidate_id": "cand_20260617_phase60_environment_taxonomy_required_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_environment_taxonomy_required_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "environment_taxonomy",
        "rule_type": "environment_governance_rule",
        "claim_type": "taxonomy_boundary",
        "title": "sandbox、testnet、replay、paper 和 live canary 必须显式区分",
        "statement": "交易系统测试链条必须显式声明当前环境类型；static API sandbox、exchange testnet、historical replay、realtime simulation、paper trading、live canary 和 live 不能混用同一语义。",
        "normalized": "phase60.environment_taxonomy_required.v1",
        "sources": ["nautilus_arch", "nautilus_overview", "phase60_env_contract"],
        "proposed_id": "kb_phase60_replay_simulation.environment_taxonomy_required.v1",
        "used_for": ["sandbox_review", "paper_trading_readiness", "environment_governance"],
    },
    {
        "task": "P60-A02",
        "candidate_id": "cand_20260617_phase60_static_api_sandbox_contract_only_001",
        "file": "KB_06_LIVE_EXECUTION/cand_20260617_phase60_static_api_sandbox_contract_only_001.json",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution",
        "subdomain": "api_sandbox",
        "rule_type": "api_contract_boundary_rule",
        "claim_type": "mocked_response_boundary",
        "title": "static API sandbox 只能验证接口契约，不能证明市场行为",
        "statement": "如果 sandbox 返回 mocked response，它只能验证 API 字段、请求/响应格式、鉴权和错误结构；不得作为真实成交、真实账户、真实流动性或策略收益证据。",
        "normalized": "phase60.static_api_sandbox_contract_only.v1",
        "sources": ["coinbase_sandbox", "phase60_env_contract"],
        "proposed_id": "kb_phase60_live_execution.static_api_sandbox_contract_only.v1",
        "used_for": ["api_contract_review", "adapter_review", "sandbox_boundary_audit"],
    },
    {
        "task": "P60-A03",
        "candidate_id": "cand_20260617_phase60_testnet_endpoint_isolation_required_001",
        "file": "KB_06_LIVE_EXECUTION/cand_20260617_phase60_testnet_endpoint_isolation_required_001.json",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution",
        "subdomain": "testnet_endpoint_isolation",
        "rule_type": "execution_environment_boundary_rule",
        "claim_type": "endpoint_isolation_constraint",
        "title": "testnet / demo endpoint 必须与生产 endpoint 隔离",
        "statement": "测试网或 demo trading 必须显式记录 endpoint、API key scope、账户 scope 和数据源；testnet 订单、余额和成交不得写成生产环境事实。",
        "normalized": "phase60.testnet_endpoint_isolation_required.v1",
        "sources": ["binance_testnet", "phase60_env_contract"],
        "proposed_id": "kb_phase60_live_execution.testnet_endpoint_isolation_required.v1",
        "used_for": ["testnet_review", "adapter_review", "credential_scope_audit"],
    },
    {
        "task": "P60-A04",
        "candidate_id": "cand_20260617_phase60_paper_trading_not_live_required_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_paper_trading_not_live_required_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "paper_trading_boundary",
        "rule_type": "paper_trading_boundary_rule",
        "claim_type": "simulation_not_live_constraint",
        "title": "paper trading 不等于 live trading",
        "statement": "Paper trading 使用实时行情和虚拟资金演练端到端链条，但成交、费用、队列、延迟、market impact、账户和监管费用可能与 live 不同；paper 盈亏不得作为 live-ready 证据。",
        "normalized": "phase60.paper_trading_not_live_required.v1",
        "sources": ["quantconnect_paper", "alpaca_paper", "ibkr_paper", "phase60_env_contract"],
        "proposed_id": "kb_phase60_replay_simulation.paper_trading_not_live_required.v1",
        "used_for": ["paper_trading_review", "live_readiness_audit", "gap_report_review"],
    },
    {
        "task": "P60-A05",
        "candidate_id": "cand_20260617_phase60_replay_market_impact_assumption_required_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_replay_market_impact_assumption_required_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "market_impact_assumption",
        "rule_type": "replay_boundary_rule",
        "claim_type": "market_impact_constraint",
        "title": "historical replay 必须声明 no-market-impact 与 fill 假设",
        "statement": "历史回放必须声明数据粒度、事件时钟、fill model、latency model、fee model 和 market impact 假设；market-data replay 的成交不能默认证明真实队列位置、真实冲击或 live 可成交性。",
        "normalized": "phase60.replay_market_impact_assumption_required.v1",
        "sources": ["hftbacktest_order_fill", "nautilus_arch", "phase60_env_contract"],
        "proposed_id": "kb_phase60_replay_simulation.replay_market_impact_assumption_required.v1",
        "used_for": ["historical_replay_review", "fill_model_audit", "live_gap_review"],
    },
    {
        "task": "P60-A06",
        "candidate_id": "cand_20260617_phase60_environment_manifest_required_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_environment_manifest_required_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "environment_manifest",
        "rule_type": "environment_manifest_rule",
        "claim_type": "audit_contract_required",
        "title": "沙盒、回放、模拟盘和 live canary 必须有 environment manifest",
        "statement": "任何用于推进测试链条的 sandbox、testnet、replay、paper trading 或 live canary 都必须保存 environment_manifest，记录环境类型、数据、时钟、adapter、账户、成交、费用、延迟、market impact、订单状态、风控和审计 trace。",
        "normalized": "phase60.environment_manifest_required.v1",
        "sources": ["phase60_env_contract", "nautilus_arch", "quantconnect_paper", "alpaca_paper"],
        "proposed_id": "kb_phase60_replay_simulation.environment_manifest_required.v1",
        "used_for": ["environment_governance", "promotion_review", "audit_trace_review"],
    },
    {
        "task": "P60-A07",
        "candidate_id": "cand_20260617_phase60_environment_promotion_evidence_required_001",
        "file": "KB_07_RISK_MANAGEMENT/cand_20260617_phase60_environment_promotion_evidence_required_001.json",
        "partition": "KB_07_RISK_MANAGEMENT",
        "tree_node": "kt.risk_management",
        "subdomain": "environment_promotion_gate",
        "rule_type": "promotion_governance_rule",
        "claim_type": "evidence_gate_constraint",
        "title": "环境晋级必须有证据门槛和人工复核",
        "statement": "从 sandbox、testnet、replay、paper trading 或 live canary 推进到下一环境前，必须引用 manifest、gap report、reconciliation、risk review 和人工复核；promotion decision 不是实盘许可。",
        "normalized": "phase60.environment_promotion_evidence_required.v1",
        "sources": ["phase60_gap_contract", "phase60_env_contract", "alpaca_paper", "ibkr_paper"],
        "proposed_id": "kb_phase60_risk_management.environment_promotion_evidence_required.v1",
        "used_for": ["promotion_review", "risk_review", "governance_audit"],
    },
    {
        "task": "P60-A08",
        "candidate_id": "cand_20260617_phase60_sandbox_paper_live_gap_report_required_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_sandbox_paper_live_gap_report_required_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "environment_gap_report",
        "rule_type": "gap_report_rule",
        "claim_type": "audit_report_required",
        "title": "sandbox / paper / live 差异必须输出标准 gap report",
        "statement": "比较 sandbox、testnet、replay、paper trading、live canary 或 live 前，必须输出 gap report，覆盖数据、时钟、成交、费用、滑点、延迟、market impact、订单状态、风控和账户差异。",
        "normalized": "phase60.sandbox_paper_live_gap_report_required.v1",
        "sources": ["phase60_gap_contract", "alpaca_paper", "hftbacktest_order_fill", "fix_exec_report"],
        "proposed_id": "kb_phase60_replay_simulation.sandbox_paper_live_gap_report_required.v1",
        "used_for": ["gap_report_review", "paper_live_reconciliation", "simulation_audit"],
    },
    {
        "task": "P60-A09",
        "candidate_id": "cand_20260617_phase60_order_lifecycle_mapping_required_001",
        "file": "KB_06_LIVE_EXECUTION/cand_20260617_phase60_order_lifecycle_mapping_required_001.json",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution",
        "subdomain": "order_lifecycle_mapping",
        "rule_type": "order_state_mapping_rule",
        "claim_type": "execution_state_contract_required",
        "title": "订单生命周期必须跨 sandbox、paper 和 live 统一映射",
        "statement": "跨 sandbox、testnet、paper 和 live 比较订单行为时，必须把 API/broker/FIX 状态映射到统一订单生命周期，至少覆盖接收、确认、部分成交、完全成交、撤单、拒单、过期、改单和费用事件。",
        "normalized": "phase60.order_lifecycle_mapping_required.v1",
        "sources": ["fix_exec_report", "coinbase_sandbox", "binance_testnet", "phase60_env_contract"],
        "proposed_id": "kb_phase60_live_execution.order_lifecycle_mapping_required.v1",
        "used_for": ["order_state_audit", "adapter_contract_review", "paper_live_reconciliation"],
    },
    {
        "task": "P60-A10",
        "candidate_id": "cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001",
        "file": "KB_07_RISK_MANAGEMENT/cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json",
        "partition": "KB_07_RISK_MANAGEMENT",
        "tree_node": "kt.risk_management",
        "subdomain": "risk_rehearsal_boundary",
        "rule_type": "risk_boundary_rule",
        "claim_type": "not_hard_gate_constraint",
        "title": "sandbox 风控演练不等于 live hard gate",
        "statement": "Sandbox、testnet、replay 或 paper 中的 risk rehearsal 只能验证字段、策略链条和审计流程；它不能替代 live risk owner 的真实风控政策、拒单、停机、解锁或 hard gate。",
        "normalized": "phase60.sandbox_risk_rehearsal_not_hard_gate.v1",
        "sources": ["phase60_gap_contract", "phase60_env_contract", "nautilus_arch"],
        "proposed_id": "kb_phase60_risk_management.sandbox_risk_rehearsal_not_hard_gate.v1",
        "used_for": ["risk_rehearsal_review", "promotion_review", "live_readiness_audit"],
    },
]


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_payload(spec: dict[str, Any]) -> dict[str, Any]:
    sources = [SOURCES[key] for key in spec["sources"]]
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": spec["candidate_id"],
        "research_task_id": spec["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": "Phase 60 P0 候选已完成来源采集和契约对齐，等待外部 AI/人工严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": spec["tree_node"],
            "canonical_node_id": spec["tree_node"],
            "tree_path": f"CEK-TA / Trading Engineering / {spec['tree_node'].split('.')[-1].replace('_', ' ').title()}",
            "related_nodes": [
                "kt.trading_engineering",
                "kt.replay_simulation",
                "kt.live_execution",
                "kt.risk_management",
                "kt.data_engineering",
                "kt.market_microstructure",
                "kt.ai_engineering",
            ],
            "partition_id": spec["partition"],
            "domain": spec["tree_node"].split(".")[-1],
            "subdomain": spec["subdomain"],
            "rule_type": spec["rule_type"],
            "claim_type": spec["claim_type"],
            "used_for": spec["used_for"] + ["external_project_rag_retrieval"],
            "classification_notes": "本候选属于 Trading Engineering 的环境治理知识。AI Engineering 只能引用 manifest、gap report 和 reason code 做审计解释，不得拥有交易执行、阈值或 hard gate。",
        },
        "claim": {
            "claim_id": f"claim_{spec['task'].lower().replace('-', '_')}",
            "title": spec["title"],
            "statement": spec["statement"],
            "normalized_claim": spec["normalized"],
            "evidence_summary": "；".join(source["evidence_summary"] for source in sources[:3]),
            "interpretation_notes": "本候选只定义 sandbox / testnet / replay / paper / live canary 环境边界、证据和审计流程，不输出买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_platform_or_venue_specific_mapping",
            "asset": "general",
            "timeframe": "testing_replay_paper_or_live_canary_environment",
            "data_granularity": "mocked_response_historical_realtime_order_event_or_fill_event",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目设计 sandbox、testnet、historical replay、realtime simulation、paper trading 或 live canary 流程",
                "需要审计测试环境、模拟成交、订单生命周期、风控 rehearsal 或 paper/live 差异",
                "需要把回测、回放、模拟盘和实盘等效链条落实到环境证据",
            ],
            "not_applicable_when": [
                "需要直接生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议",
                "问题属于真实 live order routing、账户同步、真实保证金或 broker truth，应由 Live Execution / Risk owner 处理",
                "没有平台、交易所、券商、API 版本、数据来源或环境类型证据",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含任何外接项目私有策略参数。",
                "每个环境都需要显式记录环境事实、模拟假设、owner 和审计 trace。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "平台、交易所、broker 和框架文档只能作为 implementation pattern 或 supporting source。",
                "sandbox、testnet、paper trading 和 replay 的结果不能单独证明策略收益或实盘可行性。",
                "本候选不提供投资建议、订单建议、风险阈值或实盘许可。",
            ],
        },
        "source_refs": sources,
        "source_quality": {
            "overall_reliability": "high",
            "source_count": len(sources),
            "primary_source_count": len([s for s in sources if s["source_type"] in {"official_doc", "framework_doc", "standard_doc", "internal_contract"}]),
            "limitations": [
                "外部来源具有平台、broker、exchange、asset class 或 API 版本边界。",
                "内部契约需要外部 AI/人工审计后才能用于 formal reviewed/caveat_only。",
            ],
            "needs_more_evidence": False,
        },
        "conflict_audit": {
            "conflict_status": "none",
            "known_conflicts": [],
            "potential_conflicts": [
                "可能与 Phase 58 environment equivalence manifest、Phase 37 replay/simulation、Phase 45 order/risk knowledge 重叠，正式转换前必须做重复和 owner 边界检查。"
            ],
            "resolution_summary": "未发现与当前 CEK-TA formal knowledge 的直接冲突；候选只允许进入外部审计队列。",
            "approval_allowed": True,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒外接项目区分 sandbox、testnet、replay、paper、live canary 和 live 环境",
                "用于审计 environment_manifest、promotion_decision 和 gap_report 是否齐全",
                "用于阻止 AI 把 paper 盈亏、sandbox 响应或 replay 成交泛化为 live-ready 证据",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或风险阈值",
                "不得据此授权实盘、自动拒单、自动停机或 hard gate",
                "不得把任何平台 sandbox/paper 行为泛化为所有市场",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "requires_human_escalation": True,
            "reason": "candidate_ready only; external audit required before accepted_for_draft or reviewed/caveat_only.",
        },
        "conversion_target": {
            "proposed_knowledge_id": spec["proposed_id"],
            "target_partition": spec["partition"],
            "target_review_status": "candidate_only_pending_audit",
            "default_guidance_target": "deny",
            "hard_gate_target": "deny",
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "hidden_from_default_queue": True,
            "next_action": "export_for_external_ai_audit",
            "formal_knowledge_id": None,
            "formal_review_status": None,
        },
        "audit_log": [
            {
                "event": "candidate_created",
                "at": TODAY,
                "by": "codex",
                "notes": "Phase 60 P0 候选生成，等待严格审计。",
            }
        ],
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
        },
    }


def build_audit_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "audit_package_id": "phase60_sandbox_replay_paper_candidate_audit_package_20260617",
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "phase": "Phase 60",
        "audit_goal": "严格审计 Phase 60 P0 候选是否可进入 accepted_for_draft；不得直接 reviewed、approved、default guidance 或 hard gate。",
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_reviewed": True,
            "reviewed_not_allowed_in_this_round": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_search_professional_sources": True,
            "must_check_sources_cases_and_data": True,
        },
        "required_audit_checks": [
            "核验来源是否足以支撑 claim。",
            "检查是否把平台特定 sandbox/testnet/paper 行为错误泛化。",
            "检查是否误把 sandbox/paper/replay 结果写成策略有效、live-ready 或实盘许可。",
            "检查是否需要补充 broker/exchange/framework 官方来源。",
            "检查是否与 Phase 37、45、58、59 formal knowledge 冲突或重复。",
            "检查中文乱码、mock/test 污染、私有策略参数、密钥或账户事实。",
        ],
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
        "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
        "expected_output_schema": {
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                }
            ]
        },
        "candidates": candidates,
    }


def build_quality_gate(candidates: list[dict[str, Any]], paths: list[Path]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for path, candidate in zip(paths, candidates, strict=True):
        cid = candidate["candidate_id"]
        if not candidate.get("source_refs"):
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "missing_source_refs"})
        if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "default_guidance_not_deny"})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if candidate.get("machine_gate", {}).get(field) is not False:
                failures.append({"candidate_id": cid, "path": rel(path), "reason": f"machine_gate_{field}_not_false"})
        if candidate.get("status", {}).get("review_status") != "candidate_ready":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "review_status_not_candidate_ready"})

    return {
        "report_id": "phase60_candidate_quality_gate",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "candidate_count": len(candidates),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "Phase 60 P0 candidates are candidate-only; no reviewed/approved/default guidance/hard gate.",
        "candidate_paths": [rel(path) for path in paths],
    }


def main() -> int:
    payloads = [candidate_payload(spec) for spec in CANDIDATES]
    paths = [repo_path("codex-expert-kit", "rag", "candidates", *spec["file"].split("/")) for spec in CANDIDATES]
    for path, payload in zip(paths, payloads, strict=True):
        write_json(path, payload)

    audit_path = repo_path("docs", "audit", "phase60_sandbox_replay_paper_candidate_audit_package_20260617.json")
    write_json(audit_path, build_audit_package(payloads))

    gate_path = repo_path("docs", "reports", "phase60_candidate_quality_gate.json")
    quality_gate = build_quality_gate(payloads, paths)
    write_json(gate_path, quality_gate)

    generation_report = {
        "report_id": "phase60_p0_candidate_generation_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "candidate_count": len(payloads),
        "candidate_paths": [rel(path) for path in paths],
        "audit_package_path": rel(audit_path),
        "quality_gate_path": rel(gate_path),
        "next_action": "Submit audit package for external strict audit.",
    }
    report_path = repo_path("docs", "reports", "phase60_p0_candidate_generation_report.json")
    write_json(report_path, generation_report)

    print(json.dumps(generation_report, ensure_ascii=False, indent=2))
    return 0 if quality_gate["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
