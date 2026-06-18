"""Generate Phase 37 Live Execution / Risk Management candidate knowledge.

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


TODAY = "2026-06-12"
TASK_ID = "CEK-TA-435"
PHASE = "37"
LIVE_PARTITION = "KB_06_LIVE_EXECUTION"
RISK_PARTITION = "KB_07_RISK_MANAGEMENT"

LIVE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", LIVE_PARTITION, start_file=__file__)
RISK_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", RISK_PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase37_live_risk_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase37_live_risk_candidate_generation_report.md", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase37_live_risk_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "nist_least_privilege": {
        "source_title": "Least Privilege - NIST CSRC Glossary",
        "source_url": "https://csrc.nist.gov/glossary/term/least_privilege",
        "source_type": "security_standard",
        "publisher": "NIST CSRC",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "NIST defines least privilege as restricting user or process privileges to the minimum necessary for assigned tasks.",
        "limitations": ["Security principle source; trading API permissions still require venue/broker mapping."],
    },
    "ibkr_api": {
        "source_title": "TWS API Documentation",
        "source_url": "https://www.interactivebrokers.com/campus/ibkr-api-page/trader-workstation-api/",
        "source_type": "broker_api_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR documents API connectivity for placing and monitoring orders, reviewing account information, and handling market data.",
        "limitations": ["Broker-specific API; supports adapter boundary, not universal exchange behavior."],
    },
    "ibkr_positions": {
        "source_title": "TWS API Positions",
        "source_url": "https://interactivebrokers.github.io/tws-api/positions.html",
        "source_type": "broker_api_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR TWS API provides position subscriptions and account/position update mechanisms that support position reconciliation.",
        "limitations": ["Legacy GitHub docs; use with current IBKR Campus docs for production."],
    },
    "ibkr_orders": {
        "source_title": "Placing Orders using TWS Python API",
        "source_url": "https://www.interactivebrokers.com/campus/trading-lessons/python-placing-orders/",
        "source_type": "broker_api_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR explains that valid orders produce order status, open order, and execution detail callbacks.",
        "limitations": ["Broker-specific order lifecycle example."],
    },
    "fix_execution_report": {
        "source_title": "Execution Report <8> message - FIX 4.4",
        "source_url": "https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html",
        "source_type": "standard_doc",
        "publisher": "OnixS FIX Dictionary",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "stable",
        "evidence_summary": "FIX Execution Report covers order receipt, order status, fills, rejects, changes, and post-trade fee calculations.",
        "limitations": ["FIX dictionary mirror; venue adapters still need native mapping."],
    },
    "fix_ordstatus": {
        "source_title": "OrdStatus <39> field - FIX 4.4",
        "source_url": "https://www.onixs.biz/fix-dictionary/4.4/tagnum_39.html",
        "source_type": "standard_doc",
        "publisher": "OnixS FIX Dictionary",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "stable",
        "evidence_summary": "FIX OrdStatus vocabulary includes new, partially filled, filled, canceled, rejected, pending cancel, and expired states.",
        "limitations": ["Status vocabulary only; exact transitions remain adapter-specific."],
    },
    "binance_filters": {
        "source_title": "Filters",
        "source_url": "https://developers.binance.com/docs/binance-spot-api-docs/filters",
        "source_type": "exchange_rule",
        "publisher": "Binance Open Platform",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance official filters define minimum notional, quantity, step size, and price constraints for order validation.",
        "limitations": ["Crypto venue-specific; only supports per-venue order constraint mapping."],
    },
    "sec_market_access": {
        "source_title": "Rule 15c3-5 Risk Management Controls for Brokers or Dealers with Market Access",
        "source_url": "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm",
        "source_type": "regulatory_rule",
        "publisher": "SEC",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "SEC Rule 15c3-5 requires risk management controls and supervisory procedures for market access and addresses automated electronic trading risk.",
        "limitations": ["US broker-dealer market-access rule; not directly universal across all venues/assets."],
    },
    "cftc_risk_program": {
        "source_title": "17 CFR 1.11 Risk Management Program",
        "source_url": "https://www.ecfr.gov/current/title-17/chapter-I/part-1/subject-group-ECFR812208927193be3/section-1.11",
        "source_type": "regulatory_rule",
        "publisher": "eCFR / CFTC",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "CFTC risk management program rules include controls designed to prevent erroneous orders exceeding capital, credit, or volume thresholds.",
        "limitations": ["US futures commission merchant context; supports risk-control principle, not CEK-TA parameter values."],
    },
    "cme_pretrade": {
        "source_title": "Pre-Trade Risk Management",
        "source_url": "https://www.cmegroup.com/solutions/market-access/globex/trade-on-globex/pre-trade-risk-management.html",
        "source_type": "exchange_risk_doc",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "CME describes pre-trade risk management across limit, order, permissions management, dashboards, reports, and audit trail.",
        "limitations": ["CME-specific systems; use as exchange pattern, not universal requirement."],
    },
    "cme_kill_switch": {
        "source_title": "Enforcing Kill Switch",
        "source_url": "https://www.cmegroup.com/tools-information/webhelp/globex-credit-controls/Content/KS_Detail.html",
        "source_type": "exchange_risk_doc",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "CME Kill Switch can block new order entry and cancel working orders for configured entities.",
        "limitations": ["CME-specific kill switch semantics; external projects need their own broker/venue control mapping."],
    },
    "cme_audit_trail": {
        "source_title": "Audit Trail - CME Group Risk Management",
        "source_url": "https://www.cmegroup.com/tools-information/webhelp/brokertec-risk-management/Content/audit-trail.html",
        "source_type": "exchange_risk_doc",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "CME risk management settings and updates are recorded in risk-management audit trails.",
        "limitations": ["CME/BrokerTec implementation pattern; not a universal audit schema."],
    },
    "fia_risk_controls": {
        "source_title": "Best Practices for Automated Trading Risk Controls and System Safeguards",
        "source_url": "https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf",
        "source_type": "industry_guidance",
        "publisher": "FIA",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "FIA discusses automated trading risk controls such as maximum order size and kill switches from trader, broker, and venue perspectives.",
        "limitations": ["Industry guidance; not a substitute for project-specific risk policy."],
    },
    "quantconnect_risk": {
        "source_title": "Risk Management - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/algorithm-framework/risk-management/key-concepts",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect risk management models include trailing stop, option hedging, sector exposure, and flash crash detection examples.",
        "limitations": ["Platform-specific model examples; not CEK-TA mandatory tooling or live permission."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P37-G-L01",
        "partition": LIVE_PARTITION,
        "tree_node": "kt.live_execution",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution",
        "domain": "live_trading",
        "subdomain": "api_permission",
        "slug": "least_privilege_api_required",
        "title": "实盘 API 必须最小权限",
        "statement": "实盘 API key、broker session 和交易权限必须按最小权限配置；只读、下单、撤单、资金划转、账户管理和管理端权限必须分离，不能用全权限密钥运行交易机器人。",
        "claim_type": "live_security_boundary",
        "sources": ["nist_least_privilege", "ibkr_api", "sec_market_access", "cme_pretrade"],
    },
    {
        "task": "P37-G-L02",
        "partition": LIVE_PARTITION,
        "tree_node": "kt.live_execution",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution",
        "domain": "live_trading",
        "subdomain": "order_state",
        "slug": "order_state_machine_required",
        "title": "实盘订单必须有状态机",
        "statement": "实盘执行必须维护订单状态机，覆盖 submitted、accepted、partially_filled、filled、cancel_pending、canceled、rejected、expired、unknown 和 reconciliation_required 等状态及合法迁移。",
        "claim_type": "order_state_contract",
        "sources": ["fix_execution_report", "fix_ordstatus", "ibkr_orders", "ibkr_api"],
    },
    {
        "task": "P37-G-L03",
        "partition": LIVE_PARTITION,
        "tree_node": "kt.live_execution",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution",
        "domain": "live_trading",
        "subdomain": "reconciliation",
        "slug": "position_reconciliation_required",
        "title": "实盘仓位必须定期对账",
        "statement": "实盘系统必须把本地订单/成交/仓位与 broker、exchange、account statement 或 clearing source 对账；发现差异时必须进入 reconciliation_required，而不是继续按本地状态下单。",
        "claim_type": "position_reconciliation_contract",
        "sources": ["ibkr_positions", "ibkr_api", "fix_execution_report", "cme_audit_trail"],
    },
    {
        "task": "P37-G-L04",
        "partition": LIVE_PARTITION,
        "tree_node": "kt.live_execution.risk_control",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Risk Control",
        "domain": "live_trading",
        "subdomain": "kill_switch",
        "slug": "kill_switch_required",
        "title": "实盘系统必须有安全停机和撤单机制",
        "statement": "实盘系统必须定义 kill switch、order-entry block、cancel working orders、manual override 和恢复流程；kill switch 触发不能等同于策略判断，只能作为执行安全控制。",
        "claim_type": "incident_control_contract",
        "sources": ["cme_kill_switch", "cme_pretrade", "fia_risk_controls", "sec_market_access"],
    },
    {
        "task": "P37-G-L05",
        "partition": LIVE_PARTITION,
        "tree_node": "kt.live_execution",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution",
        "domain": "live_trading",
        "subdomain": "exchange_adapter",
        "slug": "exchange_adapter_error_contract_required",
        "title": "交易所适配器必须有错误契约",
        "statement": "交易所或 broker adapter 必须把网络错误、认证错误、限频、风控拒单、参数非法、状态未知、成交回报缺失和服务降级映射为结构化错误，不能用字符串异常驱动实盘决策。",
        "claim_type": "adapter_error_contract",
        "sources": ["ibkr_api", "binance_filters", "fix_execution_report", "sec_market_access"],
    },
    {
        "task": "P37-G-L06",
        "partition": LIVE_PARTITION,
        "tree_node": "kt.live_execution",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution",
        "domain": "live_trading",
        "subdomain": "audit_log",
        "slug": "order_fill_trade_log_required",
        "title": "实盘订单、成交和交易日志必须可审计",
        "statement": "实盘执行必须保存订单请求、broker 回报、成交、拒单、撤单、费用、滑点、状态迁移、风险触发和人工操作日志，并能回放到每个交易决策和执行事件。",
        "claim_type": "live_audit_trace_contract",
        "sources": ["fix_execution_report", "cme_audit_trail", "ibkr_orders", "cme_pretrade"],
    },
    {
        "task": "P37-G-L07",
        "partition": RISK_PARTITION,
        "tree_node": "kt.risk_management.pre_trade_gates",
        "tree_path": "CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates",
        "domain": "risk_management",
        "subdomain": "single_trade_risk",
        "slug": "single_trade_risk_limit_required",
        "title": "单笔交易风险必须有上限",
        "statement": "交易系统必须在下单前检查单笔风险、订单名义金额、最大数量、价格偏离和账户可承受损失；超过策略或账户限额的订单不能进入执行适配器。",
        "claim_type": "pre_trade_risk_gate",
        "sources": ["sec_market_access", "cftc_risk_program", "cme_pretrade", "fia_risk_controls"],
    },
    {
        "task": "P37-G-L08",
        "partition": RISK_PARTITION,
        "tree_node": "kt.risk_management.pre_trade_gates",
        "tree_path": "CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates",
        "domain": "risk_management",
        "subdomain": "daily_loss",
        "slug": "daily_loss_limit_required",
        "title": "日亏损限制必须先于继续交易",
        "statement": "交易系统必须定义日内 realized/unrealized loss 口径、重置时区、触发阈值、冻结动作和人工恢复流程；达到日亏损限制后不能继续按普通信号自动下单。",
        "claim_type": "loss_limit_gate",
        "sources": ["cftc_risk_program", "sec_market_access", "cme_pretrade", "fia_risk_controls"],
    },
    {
        "task": "P37-G-L09",
        "partition": RISK_PARTITION,
        "tree_node": "kt.risk_management.pre_trade_gates",
        "tree_path": "CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates",
        "domain": "risk_management",
        "subdomain": "position_limit",
        "slug": "max_open_positions_required",
        "title": "最大持仓数和未完成订单数必须限制",
        "statement": "交易系统必须检查最大持仓数、未完成订单数、同向/反向重复订单和账户级未结风险；超过限额时必须阻止新的自动开仓请求。",
        "claim_type": "position_limit_gate",
        "sources": ["sec_market_access", "cftc_risk_program", "cme_pretrade", "fix_execution_report"],
    },
    {
        "task": "P37-G-L10",
        "partition": RISK_PARTITION,
        "tree_node": "kt.risk_management.pre_trade_gates",
        "tree_path": "CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates",
        "domain": "risk_management",
        "subdomain": "exposure_limit",
        "slug": "portfolio_exposure_limit_required",
        "title": "组合暴露必须有上限",
        "statement": "风险管理必须定义账户、策略、品种、相关资产、行业或方向暴露上限；组合暴露检查应在下单前执行，且不能被单个信号或 AI scoring 绕过。",
        "claim_type": "exposure_limit_gate",
        "sources": ["sec_market_access", "cftc_risk_program", "quantconnect_risk", "cme_pretrade"],
    },
    {
        "task": "P37-G-L11",
        "partition": RISK_PARTITION,
        "tree_node": "kt.risk_management.pre_trade_gates",
        "tree_path": "CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates",
        "domain": "risk_management",
        "subdomain": "loss_streak",
        "slug": "consecutive_loss_stop_required",
        "title": "连续亏损停止规则必须定义",
        "statement": "交易系统若使用连续亏损停止规则，必须定义亏损事件口径、时间窗口、重置条件、冻结动作和人工复核流程；该规则不能替代单笔风险、日亏损或组合暴露限制。",
        "claim_type": "risk_policy_boundary",
        "sources": ["fia_risk_controls", "cftc_risk_program", "quantconnect_risk", "cme_pretrade"],
    },
    {
        "task": "P37-G-L12",
        "partition": RISK_PARTITION,
        "tree_node": "kt.risk_management.pre_trade_gates",
        "tree_path": "CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates",
        "domain": "risk_management",
        "subdomain": "hard_gate",
        "slug": "hard_risk_gate_precedes_execution",
        "title": "Hard risk gate 必须先于实盘执行",
        "statement": "任何 AI scoring、策略信号或人工队列都不能绕过 deterministic hard risk gate；最终下单前必须经过权限、订单约束、风险限额、账户状态、市场状态和 kill-switch 状态检查。",
        "claim_type": "hard_risk_gate_boundary",
        "sources": ["sec_market_access", "cftc_risk_program", "cme_kill_switch", "fia_risk_controls"],
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")


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
    partition = item["partition"]
    branch = "Live Execution" if partition == LIVE_PARTITION else "Risk Management"
    candidate_id = f"cand_{TODAY.replace('-', '')}_phase37_live_risk_{slugify(item['slug'])}_001"
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": candidate_id,
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Live Execution / Risk Management 候选已完成来源采集，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": item["tree_node"],
            "canonical_node_id": item["tree_node"],
            "tree_path": item["tree_path"],
            "related_nodes": [
                "kt.trading_engineering",
                "kt.live_execution",
                "kt.risk_management",
                "kt.replay_simulation",
                "kt.market_microstructure",
                "kt.ai_engineering.llm_training",
            ],
            "partition_id": partition,
            "domain": item["domain"],
            "subdomain": item["subdomain"],
            "rule_type": "live_risk_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "live_readiness_review",
                "risk_gate_design_review",
                "external_project_rag_retrieval",
                "ai_trader_project_gap_audit",
            ],
            "classification_notes": f"本候选主归属 Trading Engineering / {branch}。AI Engineering 只能引用本规则，不得把实盘执行或风险管理本体改写为模型训练规则。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"{item['domain']}.{item['slug']}.v1",
            "evidence_summary": "；".join(source["evidence_summary"] for source in refs[:3]),
            "interpretation_notes": "本候选只定义实盘执行与风险管理边界，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_broker_venue_specific_mapping",
            "asset": "general",
            "timeframe": "live_or_paper_to_live_readiness",
            "data_granularity": "orders_fills_positions_account_risk_events",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "审计外接项目的实盘执行、订单状态机、仓位对账、交易所适配器、risk gate 或 kill switch 设计",
                "把 AI scoring / strategy signal 接入实盘前，需要确认 deterministic final gate 和执行安全边界",
            ],
            "not_applicable_when": [
                "需要生成买卖点、仓位、杠杆、止损止盈或具体下单建议",
                "问题属于回测、回放或模拟假设，应由 Backtest / Replay Simulation 分支处理",
                "没有 broker、venue、account、order、position、risk policy 或 audit trace 上下文",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含外接项目私有账户事实、密钥或策略参数。",
                "实盘执行和风控规则必须按 broker、venue、asset、account、policy 和时间版本映射。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "监管、交易所、broker 和平台来源只能支持原则和实现模式，不能替代外接项目自己的风控政策。",
                "风险限制阈值必须由外接项目 owner 设定，本知识库不提供阈值数值建议。",
                "本候选不提供任何投资建议或实盘许可。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "medium_high",
            "score": round(sum(float(source["score"]) for source in refs) / len(refs), 2),
            "score_version": "phase37_live_risk_source_scoring_v1",
            "primary_source_count": len([source for source in refs if source["reliability"] in {"high", "medium_high"}]),
            "supporting_source_count": len(refs),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式入库前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "broker/venue/platform 文档不得被泛化为所有市场通用规则。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "Phase 37 Trading 与 AI 跨分支引用契约",
                "Replay / Simulation execution cost and gap-report boundaries",
                "Market Microstructure venue/session boundaries",
                "AI Engineering deterministic final gate boundaries",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与可见正式知识的直接冲突；候选不创建 approved、default guidance 或 hard gate。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计实盘执行和风险管理时必须声明权限、状态、对账、日志、限额和安全停机边界。",
                "用于审计 AI trader 项目是否缺少 deterministic final gate、order-state trace、position reconciliation 或 risk policy。",
                "用于阻止 AI scoring 或策略信号绕过实盘执行和风控 owner。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘订单。",
                "不得把候选知识当作 reviewed、approved、default guidance 或 hard gate。",
                "不得提供任何具体风险阈值、账户配置、交易所私有配置或资金划转建议。",
            ],
            "requires_context": [
                "broker",
                "venue",
                "account_scope",
                "order_type",
                "risk_policy_id",
                "permission_scope",
                "position_source",
                "audit_trace_id",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; pending external strict audit; not formal reviewed; no default guidance.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "conversion_target": {
            "proposed_knowledge_id": f"kb_{'06_live_execution' if partition == LIVE_PARTITION else '07_risk_management'}.{item['slug']}.v1",
            "target_review_status": "candidate_only_pending_external_audit",
            "default_guidance_after_conversion": "deny_until_reviewed_caveat_only_audit",
            "formalization_blockers": ["requires_external_strict_audit"],
        },
        "workflow": {
            "phase": PHASE,
            "task_id": TASK_ID,
            "stage": "pending_external_audit",
            "queue_group": "pending",
            "next_allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formalization_allowed": False,
        },
        "contribution": {
            "origin": "codex_research_ingestion_phase37",
            "private_data_removed": True,
            "contains_account_facts": False,
            "contains_secret": False,
            "contains_project_private_strategy": False,
        },
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 candidates, got {len(candidates)}")
    expected_tasks = {f"P37-G-L{idx:02d}" for idx in range(1, 13)}
    actual_tasks = {candidate.get("research_task_id") for candidate in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research task set: {sorted(actual_tasks ^ expected_tasks)}")
    for candidate in candidates:
        cid = candidate.get("candidate_id", "<unknown>")
        partition = candidate.get("classification", {}).get("partition_id")
        if partition not in {LIVE_PARTITION, RISK_PARTITION}:
            failures.append(f"{cid}: unexpected partition {partition}")
        if candidate.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if candidate.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        gate = candidate.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default_guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        if len(candidate.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        blob = json.dumps(candidate, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase37_live_risk_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": 12,
        "live_execution_count": len([item for item in candidates if item["classification"]["partition_id"] == LIVE_PARTITION]),
        "risk_management_count": len([item for item in candidates if item["classification"]["partition_id"] == RISK_PARTITION]),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批只是 Live Execution / Risk Management candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "风险阈值必须由外接项目 owner 按账户、市场、品种、策略和监管环境设定，本知识库不提供阈值数值建议。",
        ],
    }


def write_research_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    lines = [
        "# Phase 37 Live Execution / Risk Management Candidate Research",
        "",
        f"- generated_at: {TODAY}",
        f"- task_id: {TASK_ID}",
        f"- candidate_count: {len(candidates)}",
        f"- live_execution_count: {gate['live_execution_count']}",
        f"- risk_management_count: {gate['risk_management_count']}",
        f"- gate_status: {gate['gate_status']}",
        "",
        "## 来源种子",
        "",
    ]
    for key, source in SOURCES.items():
        lines.append(f"- `{key}`: {source['source_title']} ({source['publisher']}) - {source['source_url']}")
    lines.extend(["", "## 候选知识点", ""])
    for candidate in candidates:
        lines.append(f"- `{candidate['research_task_id']}` / `{candidate['claim']['normalized_claim']}`: {candidate['claim']['statement']}")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 本批候选只处理实盘执行和风控规则本体，不处理回测、回放、AI 训练、RAG/MCP 或项目私有策略参数。",
            "- 候选不得直接进入 reviewed、approved、default guidance 或 hard gate。",
            "- 风险阈值、账户配置、交易所配置和密钥权限必须由外接项目 owner 自行定义并审计。",
        ]
    )
    write_text(RESEARCH_REPORT, "\n".join(lines) + "\n")


def main() -> int:
    LIVE_DIR.mkdir(parents=True, exist_ok=True)
    RISK_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [build_candidate(item) for item in ITEMS]
    for candidate in candidates:
        target_dir = LIVE_DIR if candidate["classification"]["partition_id"] == LIVE_PARTITION else RISK_DIR
        write_json(target_dir / f"{candidate['candidate_id']}.json", candidate)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_research_report(candidates, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase37_live_risk_candidate_generation",
            "generated_at": TODAY,
            "task_id": TASK_ID,
            "candidate_count": len(candidates),
            "candidate_dirs": [str(LIVE_DIR), str(RISK_DIR)],
            "quality_gate": gate,
            "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
            "formal_knowledge_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": 0,
            "hard_gate_enabled": 0,
            "next_action": "CEK-TA-436 export Live Execution / Risk Management candidate AI audit package.",
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "quality_gate": str(QUALITY_GATE)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
