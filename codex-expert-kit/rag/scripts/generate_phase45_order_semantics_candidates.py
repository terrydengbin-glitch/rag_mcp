"""Generate Phase 45 Order Type / TIF / Venue Semantics candidates.

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
PHASE = "45"
TASK_ID = "CEK-TA-467"
BATCH = "P45-F Order Type / TIF / Venue Semantics"
PARTITION = "KB_06_LIVE_EXECUTION"
TREE_NODE = "kt.live_execution.order_semantics"

RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase45_order_semantics_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase45_order_semantics_candidate_generation_report.json", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase45_order_semantics_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "fix_protocol": {
        "source_title": "FIX Trading Community FIX Protocol",
        "source_url": "https://fixtrading.org/standards/fix-protocol/",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community",
        "reliability": "high",
        "score": 91,
        "freshness": "stable",
        "evidence_summary": "FIX protocol provides standardized order-entry and execution-report message semantics used by many electronic trading integrations.",
        "limitations": ["Protocol standard; does not define every venue-specific order type, matching rule or fee behavior."],
    },
    "fix_execution_report": {
        "source_title": "FIXimate FIX 4.4 Execution Report",
        "source_url": "https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community / FIXimate",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "FIX Execution Report supports receipt, status, fill, cancel, replace and reject semantics for order-event lifecycle review.",
        "limitations": ["Protocol schema; venue/broker implementations and reject reasons still need adapter evidence."],
    },
    "cme_order_types": {
        "source_title": "CME Group Futures Order Types",
        "source_url": "https://www.cmegroup.com/education/courses/things-to-know-before-trading-cme-futures/futures-order-types",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "CME explains futures order types such as market, limit, stop and GTC-style validity and warns participants to understand available order conditions.",
        "limitations": ["CME education source; product-specific Globex behavior still depends on CME technical/rulebook references."],
    },
    "cme_order_qualifiers": {
        "source_title": "CME Globex Order Qualifiers",
        "source_url": "https://www.cmegroup.com/confluence/display/EPICSANDBOX/Order%2BQualifiers",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "CME order qualifiers describe duration, minimum execution quantity and display quantity attributes used with Globex orders.",
        "limitations": ["CME Client Systems Wiki/Confluence source; venue-specific and should be rechecked against production specs before reviewed import."],
    },
    "cme_smp": {
        "source_title": "CME Globex Self-Match Prevention FAQ",
        "source_url": "https://www.cmegroup.com/solutions/market-access/globex/trade-on-globex/faq-self-match.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "CME describes self-match prevention as optional functionality to prevent matching orders for accounts with common ownership and notes activation/rejection caveats.",
        "limitations": ["CME Globex-specific SMP behavior; not a universal STP implementation."],
    },
    "nasdaq_order_types_pdf": {
        "source_title": "Nasdaq Order Types and Modifiers",
        "source_url": "https://www.nasdaqtrader.com/content/productsservices/trading/ordertypesg.pdf",
        "source_type": "official_exchange_doc",
        "publisher": "Nasdaq Trader",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Nasdaq order type and modifier guide documents TIF behavior such as market-hours IOC, system-hours IOC and order-type availability caveats.",
        "limitations": ["Nasdaq equities context; not directly portable to futures, options, crypto or non-U.S. venues."],
    },
    "binance_futures_order": {
        "source_title": "Binance USD-M Futures New Order API",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api",
        "source_type": "official_platform_doc",
        "publisher": "Binance Developers",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance Futures order API documents order type, timeInForce, reduceOnly, selfTradePreventionMode and GTD goodTillDate behavior.",
        "limitations": ["Binance USD-M futures API context; fields and behavior may differ across spot, options, coin-margined futures and other venues."],
    },
    "binance_spot_order": {
        "source_title": "Binance Spot Trading Endpoints",
        "source_url": "https://developers.binance.com/docs/binance-spot-api-docs/rest-api/trading-endpoints",
        "source_type": "official_platform_doc",
        "publisher": "Binance Developers",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance Spot documents LIMIT_MAKER as a post-only limit order rejected if it immediately matches and trades as taker.",
        "limitations": ["Binance Spot API context; not the same as futures reduce-only or other venues' post-only behavior."],
    },
    "kraken_futures_order": {
        "source_title": "Kraken Futures Send Order API",
        "source_url": "https://docs.kraken.com/api-reference/order-management/send-order",
        "source_type": "official_platform_doc",
        "publisher": "Kraken",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Kraken futures API documents limit, post-only, IOC, market, stop, take-profit, trailing-stop and FOK order types, plus reduceOnly behavior.",
        "limitations": ["Kraken futures context; not a universal crypto venue or equity/futures exchange rule."],
    },
    "coinbase_trading_rules": {
        "source_title": "Coinbase Markets Trading Rules",
        "source_url": "https://www.coinbase.com/legal/trading_rules",
        "source_type": "official_platform_doc",
        "publisher": "Coinbase",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Coinbase trading rules define limit, market, stop, TWAP, TIF, post-only, maker/taker and fee behavior with platform caveats.",
        "limitations": ["Coinbase market/legal context; rules may differ by Coinbase entity, product and jurisdiction."],
    },
    "coinbase_trading_concepts": {
        "source_title": "Coinbase Exchange Trading Concepts",
        "source_url": "https://docs.cdp.coinbase.com/exchange/concepts/trading",
        "source_type": "official_platform_doc",
        "publisher": "Coinbase Developer Platform",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Coinbase developer documentation lists STP modes and TIF options such as GTC, GTT, IOC and FOK.",
        "limitations": ["Coinbase Exchange API context; not all Coinbase products or external venues share these modes."],
    },
    "coinbase_international_stp": {
        "source_title": "Coinbase International Exchange Trading Rules",
        "source_url": "https://www.coinbase.com/international-exchange/legal/trading-rules",
        "source_type": "official_platform_doc",
        "publisher": "Coinbase International Exchange",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Coinbase International rules describe self-trade prevention, including cancel/decrement behavior when self-execution would occur.",
        "limitations": ["Coinbase International Exchange-specific; not a universal self-trade prevention standard."],
    },
    "cfa_trading_costs": {
        "source_title": "CFA Institute Trading Costs and Electronic Markets",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
        "source_type": "professional_body",
        "publisher": "CFA Institute",
        "reliability": "high",
        "score": 89,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA describes explicit and implicit trading costs, including broker commissions, exchange fees, bid-ask spread, market impact, delay and unfilled trades.",
        "limitations": ["Professional learning source; not a venue-specific fee schedule or order-type implementation contract."],
    },
    "sec_maker_taker": {
        "source_title": "SEC EMSAC Memo: Maker-Taker Fees on Equities Exchanges",
        "source_url": "https://www.sec.gov/spotlight/emsac/memo-maker-taker-fees-on-equities-exchanges.pdf",
        "source_type": "regulatory_discussion",
        "publisher": "U.S. SEC",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "evidence_summary": "SEC EMSAC memo describes maker-taker pricing as exchanges charging to take liquidity and paying rebates to post liquidity.",
        "limitations": ["U.S. equities-market policy discussion; not a current fee schedule or crypto/futures rule."],
    },
    "cme_clearing_fees": {
        "source_title": "CME Exchange Fees for Clearing and Trading",
        "source_url": "https://www.cmegroup.com/company/clearing-fees.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "CME states exchange fees vary by membership, incentive program participant status, product, volume, venue and transaction type.",
        "limitations": ["CME fee schedule context; not a general maker/taker fee model for all venues."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-F-ORD01",
        "slug": "order_type_semantics_required",
        "title": "订单类型语义必须由 adapter 和 venue 明确声明",
        "statement": "交易系统不能只用 market、limit、stop、stop-limit、iceberg、auction、TWAP/VWAP 等字符串枚举表示订单语义；每个订单类型必须声明适用 venue、产品、触发条件、价格保护、部分成交、拒单/过期状态、订单状态机映射和 ExecutionReport 证据边界。",
        "claim_type": "order_type_semantics_rule",
        "sources": ["fix_protocol", "fix_execution_report", "cme_order_types", "coinbase_trading_rules", "kraken_futures_order"],
    },
    {
        "task": "P45-F-ORD02",
        "slug": "time_in_force_semantics_required",
        "title": "Time In Force 必须绑定 session、venue 和过期语义",
        "statement": "GTC、GTD/GTT、IOC、FOK、DAY、session-hours 等 Time In Force 语义必须声明 venue、交易时段、过期时点、部分成交处理、good-till 时间精度、系统时钟和 cancel/expire 事件；不得把 TIF 简化为本地 UI 字段。",
        "claim_type": "time_in_force_semantics_rule",
        "sources": ["fix_protocol", "cme_order_qualifiers", "nasdaq_order_types_pdf", "coinbase_trading_concepts", "binance_futures_order"],
    },
    {
        "task": "P45-F-ORD03",
        "slug": "post_only_reduce_only_boundary",
        "title": "post-only 和 reduce-only 是执行约束，不是盈利或安全保证",
        "statement": "post-only 只能表达 maker/post-to-book 意图或 taker 避免约束，reduce-only 只能表达不增加现有仓位或只减仓约束；二者必须声明 venue-specific reject/cancel/reprice 行为、已有订单交互、仓位源和失败事件，不能被写成成交保证、费用节省保证、风险安全保证或交易许可。",
        "claim_type": "post_reduce_order_constraint_rule",
        "sources": ["binance_spot_order", "binance_futures_order", "kraken_futures_order", "coinbase_trading_rules"],
    },
    {
        "task": "P45-F-ORD04",
        "slug": "self_trade_prevention_required",
        "title": "自成交防护必须声明模式、账户范围和事件处理",
        "statement": "Self-trade prevention / self-match prevention 必须声明适用账户、firm/group 范围、STP/SMP 模式、cancel/decrement/reject 行为、激活时间、order event 映射和审计证据；不得把 STP 当作防操纵合规结论、成交质量保证或跨 venue 通用规则。",
        "claim_type": "self_trade_prevention_boundary_rule",
        "sources": ["cme_smp", "coinbase_trading_concepts", "coinbase_international_stp", "binance_futures_order"],
    },
    {
        "task": "P45-F-ORD05",
        "slug": "exchange_specific_order_type_caveat",
        "title": "交易所特有订单类型不得泛化为通用语义",
        "statement": "Market with protection、market-to-limit、auction-only、MOO/MOC/LOC、iceberg、peg、post-only、reduce-only、RFQ、TWAP/VWAP 等订单类型或修饰符必须保留 exchange、product、session、rulebook、API version 和 adapter caveat；外接项目不得把某个交易所或 crypto venue 的订单行为泛化为所有市场。",
        "claim_type": "venue_specific_order_type_caveat_rule",
        "sources": ["cme_order_types", "nasdaq_order_types_pdf", "coinbase_trading_rules", "binance_futures_order", "kraken_futures_order"],
    },
    {
        "task": "P45-F-ORD06",
        "slug": "maker_taker_fee_order_type_boundary",
        "title": "maker/taker 费用必须和订单类型、成交结果分开审计",
        "statement": "maker/taker、add/remove liquidity、rebate、exchange fee、routing fee 和 transaction type 必须根据 venue fee schedule、成交结果和订单事件审计；post-only 或 limit order 不能自动等同于 maker 成交，maker/taker fee 也不能直接写成策略 alpha、成交质量证明或默认路由规则。",
        "claim_type": "maker_taker_fee_boundary_rule",
        "sources": ["sec_maker_taker", "cfa_trading_costs", "cme_clearing_fees", "coinbase_trading_rules"],
    },
]


def source_ref(source_key: str, index: int) -> dict[str, Any]:
    source = dict(SOURCES[source_key])
    source.update(
        {
            "source_id": f"src_{index:03d}",
            "accessed_at": TODAY,
            "version": None,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        }
    )
    return source


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_order_semantics_{safe}_001.json"


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, idx + 1) for idx, key in enumerate(item["sources"])]
    primary_types = {"official_protocol_doc", "official_exchange_doc", "official_platform_doc", "regulatory_discussion", "professional_body"}
    source_score = round(sum(float(ref["score"]) for ref in refs) / len(refs), 2)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": f"cand_20260612_phase45_order_semantics_{item['task'].lower().replace('-', '_')}_001",
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 P45-F Order Type / TIF / Venue Semantics 候选，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": TREE_NODE,
            "canonical_node_id": TREE_NODE,
            "tree_path": "CEK-TA / Trading Engineering / Live Execution / Order Semantics",
            "related_nodes": [
                "kt.replay_simulation.order_semantics",
                "kt.live_execution.order_state_machine",
                "kt.live_execution.trade_audit_clock_sync",
                "kt.trading_engineering.live_execution.execution_tca",
                "kt.risk_management.layered_risk_controls",
            ],
            "partition_id": PARTITION,
            "domain": "live_trading",
            "subdomain": "order_semantics",
            "rule_type": "order_semantics_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trading_ai_project_design_audit",
                "execution_adapter_contract_review",
                "order_semantics_checklist",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "P45-F 只补订单类型、TIF、post-only/reduce-only、STP/SMP、venue-specific order behavior 和 maker/taker fee 边界；不生成买卖点、仓位、费用优化建议、路由建议、交易许可或 hard gate。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_order_semantics.{item['slug']}.v1",
            "evidence_summary": "；".join(ref["evidence_summary"] for ref in refs),
            "interpretation_notes": "本候选只定义 live execution adapter / venue order semantics 的审计边界，不输出交易动作、费用优化或风控阈值。",
            "claim_strength": "candidate",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_venue_product_session_and_api_version_caveats",
            "asset": "general",
            "timeframe": "order_entry_execution_adapter_and_audit_context",
            "data_granularity": "order_intent_order_event_execution_report_fill_fee_and_reject_events",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要设计交易所 adapter、订单状态机、订单事件审计、模拟与实盘订单语义映射。",
                "AI IDE 需要检查 order type、TIF、post-only、reduce-only、STP/SMP 或 maker/taker fee 是否被误写成通用规则。",
                "需要把 order intent、venue accepted order、execution report、fill、reject、expire、fee 和 audit trace 分开建模。",
            ],
            "not_applicable_when": [
                "用户要求具体买卖点、下单价格、仓位、杠杆、止损止盈、路由选择、费用套利或实盘执行建议。",
                "需要真实 broker/venue 当前订单事实、账户事实、费率表或交易权限时，应由外接项目事实层和 Live Execution owner 提供。",
                "需要确定某个订单是否应该提交、撤销、修改或强制 reduce 时，应由外接项目 deterministic final gate / Risk Management owner 决定。",
            ],
            "assumptions": [
                "Order Type / TIF / Venue Semantics 是执行 adapter 和审计契约上下文，不是策略 alpha。",
                "所有交易所、broker、crypto venue 和 FIX 来源必须保留 venue、product、session、API version 和 account-mode caveat。",
                "候选通过外部审计前不能进入 formal reviewed 知识库。",
            ],
            "limitations": [
                "FIX 只定义协议字段语义，不替代 venue/broker 事实层或 rulebook。",
                "交易所和 crypto venue 文档只证明该 venue/product/API 的行为，不能泛化为全部市场。",
                "本候选不包含任何项目私有订单参数、账号、费率、仓位或策略配置。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": source_score,
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": sum(1 for ref in refs if ref["source_type"] in primary_types),
            "supporting_source_count": 0,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "CME/Nasdaq/Coinbase/Binance/Kraken/IBKR 等来源必须保留 venue、product、account mode、session 和 API version caveat。",
                "若后续使用内部 order_semantics schema，需要提供 contract extract 或 hash。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Live Execution order state machine formal reviewed knowledge",
                "Phase 37 Replay / Simulation order semantics formal reviewed knowledge",
                "Phase 45 Execution TCA formal reviewed knowledge",
                "Phase 45 Audit Trail / Clock Sync formal reviewed knowledge",
                "Phase 45 Layered Risk formal reviewed knowledge",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有 formal reviewed 知识的直接冲突；P45-F 只补 live adapter 和 venue-specific order behavior 边界，不接管 Replay fill model、Risk hard gate 或 Trade Analysis 复盘本体。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分 order type、TIF、venue adapter、execution report、fill/reject/expire 和 fee evidence。",
                "用于生成 order semantics checklist、adapter contract review、simulation/live mapping review 和 RAG 检索上下文。",
                "用于检查外接项目是否把 post-only、reduce-only、STP/SMP、maker/taker fee 或 venue-specific order type 误写成通用交易规则。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、费用套利、路由建议或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、撤单、改单、reduce-only 强制动作或路由策略。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; pending external strict audit; no reviewed/approved/default/hard gate.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "review": {
            "review_status": "candidate_ready",
            "review_mode": "external_strict_audit_required",
            "confidence": "medium_high",
            "freshness": "mixed",
            "reviewer": None,
            "reviewed_at": None,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_order_semantics_candidate_generated",
                    "reason": "Generated from Phase 45 P45-F task queue with FIX, exchange, venue and professional sources.",
                }
            ],
        },
        "workflow": {
            "stage": "pending_external_audit",
            "queue_group": "pending",
            "source_phase": PHASE,
            "source_task_id": TASK_ID,
            "batch": BATCH,
            "formal_knowledge_id": None,
            "formal_knowledge_path": None,
            "allowed_next_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_next_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
        },
        "contribution": {
            "source": "phase45_professional_research",
            "private_data_removed": True,
            "project_specific_details_removed": True,
            "notes": "Generated for external strict audit; no project account, key, order, fee tier, threshold, position, or private strategy data included.",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    expected = {f"P45-F-ORD{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if len(candidates) != 6:
        failures.append(f"expected 6 candidates, got {len(candidates)}")
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition mismatch")
        if item.get("classification", {}).get("canonical_node_id") != TREE_NODE:
            failures.append(f"{cid}: canonical node mismatch")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 3:
            failures.append(f"{cid}: primary_source_count < 3")
        gate = item.get("machine_gate", {})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed", "trade_execution_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase45_order_semantics_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "batch": BATCH,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批次只生成 candidate，不创建 reviewed、approved、default guidance 或 hard gate。",
            "P45-F 只能用于 order semantics、TIF、venue adapter、STP/SMP 和 maker/taker fee 边界，不输出交易动作或路由建议。",
        ],
    }


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Order Type / TIF / Venue Semantics 候选知识采集记录",
        "",
        "## 范围",
        "",
        "本批次对应 CEK-TA-467 / P45-F，目标是采集 6 条 Order Type / TIF / Venue Semantics P1 候选知识。",
        "",
        "本批次只生成候选和审计支撑材料，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 联网核验来源",
        "",
        "| source_key | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 候选列表", "", "| ID | title | source_count | 状态 |", "| --- | --- | ---: | --- |"])
    for candidate in candidates:
        lines.append(f"| {candidate['research_task_id']} | {candidate['claim']['title']} | {len(candidate['source_refs'])} | {candidate['status']['review_status']} |")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. 不输出买卖点、仓位、杠杆、止损止盈、路由建议、费用套利或实盘执行建议。",
            "2. FIX 只作为协议语义来源，不能替代 broker/venue/order truth。",
            "3. CME、Nasdaq、Coinbase、Binance、Kraken 等来源必须保留 venue、product、session、account mode 和 API version caveat。",
            "4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。",
            "```",
        ]
    )
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    candidates = [build_candidate(item) for item in ITEMS]
    for item, candidate in zip(ITEMS, candidates):
        target = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, slug_to_file_name(item["slug"]), start_file=__file__)
        write_json(target, candidate)
    write_research_report(candidates)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase45_order_semantics_candidate_generation_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "batch": BATCH,
            "candidate_count": len(candidates),
            "quality_gate": gate,
            "candidates": [
                {
                    "research_task_id": item["research_task_id"],
                    "candidate_id": item["candidate_id"],
                    "knowledge_slug": item["claim"]["normalized_claim"],
                    "source_count": len(item["source_refs"]),
                }
                for item in candidates
            ],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
