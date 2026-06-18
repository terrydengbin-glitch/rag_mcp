"""Generate Phase 45 Layered Risk / Credit / Margin candidate knowledge.

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
TASK_ID = "CEK-TA-461"
BATCH = "P45-C Layered Risk / Credit / Margin"
PARTITION = "KB_07_RISK_MANAGEMENT"

RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase45_layered_risk_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase45_layered_risk_candidate_generation_report.json", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase45_layered_risk_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "sec_15c3_5_final": {
        "source_title": "Risk Management Controls for Brokers or Dealers with Market Access",
        "source_url": "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm",
        "source_type": "regulatory_rule",
        "publisher": "U.S. SEC",
        "reliability": "high",
        "score": 94,
        "freshness": "time_sensitive",
        "evidence_summary": "SEC Rule 15c3-5 requires market-access broker-dealers to maintain financial and regulatory risk-management controls, including pre-set credit/capital thresholds and erroneous-order controls.",
        "limitations": ["U.S. broker-dealer market access rule; not a universal global trading-system standard."],
    },
    "sec_15c3_5_faq": {
        "source_title": "SEC Market Access Rule FAQ",
        "source_url": "https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0",
        "source_type": "regulatory_guidance",
        "publisher": "U.S. SEC",
        "reliability": "high",
        "score": 92,
        "freshness": "time_sensitive",
        "evidence_summary": "SEC FAQ explains that controls should systematically limit financial exposure, prevent orders beyond credit/capital thresholds, reject orders beyond price/size parameters, and keep financial controls under broker-dealer control.",
        "limitations": ["FAQ guidance for SEC Rule 15c3-5; not a source for CEK-TA-specific field names."],
    },
    "fia_automated_controls_2024": {
        "source_title": "Best Practices for Automated Trading Risk Controls and System Safeguards",
        "source_url": "https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf",
        "source_type": "professional_body",
        "publisher": "FIA",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "FIA best-practice paper covers pre-trade risk management, exchange volatility controls, post-trade analysis, testing, conformance, and system safeguards for automated trading.",
        "limitations": ["Industry best practices; not a binding rule and not a CEK-TA threshold source."],
    },
    "cme_pre_trade": {
        "source_title": "CME Globex Pre-Trade Risk Management",
        "source_url": "https://www.cmegroup.com/solutions/market-access/globex/trade-on-globex/pre-trade-risk-management.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CME describes pre-trade risk tools including order blocking, cancel open orders, cancel-on-disconnect, self-match prevention, duplicate order checks, and real-time activity monitoring.",
        "limitations": ["CME Globex-specific toolset; not applicable to all venues."],
    },
    "cme_credit_controls": {
        "source_title": "CME Globex Credit Controls",
        "source_url": "https://www.cmegroup.com/tools-information/webhelp/globex-credit-controls/Content/CME-Globex-Credit-Controls-Management.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CME Globex Credit Controls provide pre-execution controls for clearing-firm risk administrators to set exposure and maximum quantity limits for Globex order/trade activity.",
        "limitations": ["CME clearing and Globex context; not a universal credit framework."],
    },
    "cme_account_credit": {
        "source_title": "CME Account Manager Credit Controls",
        "source_url": "https://www.cmegroup.com/tools-information/webhelp/account-manager-service/Content/credit-controls.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "CME account-level controls include credit, long/short quantity limits and order-submission controls by product group and product.",
        "limitations": ["CME product/account implementation source; not a general CEK-TA schema."],
    },
    "cme_price_banding": {
        "source_title": "CME Globex Price Banding",
        "source_url": "https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457317722/Limits%2Band%2BBanding",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "CME price banding subjects orders to price validation and rejects orders outside the given band to prevent erroneous or market-moving orders.",
        "limitations": ["CME documentation; price bands are venue/product specific and not CEK-TA default thresholds."],
    },
    "cme_messaging_controls": {
        "source_title": "CME Globex Messaging Controls",
        "source_url": "https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457317540/Messaging%2BControls",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "CME messaging controls are designed to protect participants from excessive messaging in iLink order entry.",
        "limitations": ["CME iLink context; not a universal throttle/cancel-rate threshold source."],
    },
    "cme_span": {
        "source_title": "CME SPAN Methodology Overview",
        "source_url": "https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology-overview.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CME SPAN is a portfolio-risk methodology for calculating performance bond requirements using risk arrays and scenario-based portfolio loss estimates.",
        "limitations": ["CME margin methodology source; not a CEK-TA available-funds execution rule."],
    },
    "cme_margins_faq": {
        "source_title": "CME Performance Bonds/Margins FAQ",
        "source_url": "https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/faq-performance-bonds-margins.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "CME explains performance bonds/margins as deposits held at CME Clearing to ensure clearing members meet obligations; requirements vary by product and volatility.",
        "limitations": ["CME clearing source; not broker-specific cash availability or crypto collateral policy."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-C-RISK01",
        "slug": "layered_pre_trade_controls_required",
        "title": "pre-trade controls 必须分层声明",
        "statement": "交易系统的 pre-trade controls 必须按订单级、账户级、策略级、产品/venue 级、信用/保证金级和系统级分层声明；不能用单一 allow/block 布尔值替代分层风险检查、owner、证据和例外流程。",
        "claim_type": "layered_pre_trade_controls_rule",
        "sources": ["sec_15c3_5_final", "sec_15c3_5_faq", "fia_automated_controls_2024", "cme_pre_trade"],
    },
    {
        "task": "P45-C-RISK02",
        "slug": "credit_limit_not_strategy_risk_limit",
        "title": "credit limit 不是策略风险限额",
        "statement": "信用/资本/清算限额是 market access、broker、clearing 或 account exposure 边界，不等同于策略级亏损阈值、仓位 sizing 或 alpha 风险偏好；AI IDE 必须把 credit limit owner 与 strategy risk owner 分开。",
        "claim_type": "credit_limit_boundary_rule",
        "sources": ["sec_15c3_5_faq", "cme_credit_controls", "cme_account_credit"],
    },
    {
        "task": "P45-C-RISK03",
        "slug": "max_order_size_and_price_collar_required",
        "title": "最大订单量和价格 collar 必须独立于策略信号",
        "statement": "最大订单数量、价格 band/collar、fat-finger 检查和明显错误订单过滤是订单准入与市场完整性控制，必须声明数据源、venue/product 适用范围、拒单/复核行为和 owner；不能把策略信号强度当作绕过价格或数量控制的理由。",
        "claim_type": "max_order_size_price_collar_rule",
        "sources": ["sec_15c3_5_faq", "cme_price_banding", "cme_pre_trade", "fia_automated_controls_2024"],
    },
    {
        "task": "P45-C-RISK04",
        "slug": "message_throttle_and_cancel_rate_controls",
        "title": "消息节流和 cancel-rate controls 必须可审计",
        "statement": "自动交易系统必须声明消息速率、撤单率、quote/cancel 限制、burst 行为、超限动作和恢复流程；不能只用成交风险指标衡量系统对交易所或市场的消息压力。",
        "claim_type": "message_throttle_cancel_rate_rule",
        "sources": ["fia_automated_controls_2024", "cme_messaging_controls", "cme_pre_trade"],
    },
    {
        "task": "P45-C-RISK05",
        "slug": "margin_collateral_available_funds_boundary",
        "title": "margin、collateral 和 available funds 必须分开",
        "statement": "保证金、抵押品、可用资金、清算所 performance bond、broker buying power 和策略资金预算是不同层级的约束；交易 AI 不得把任一字段默认为可交易现金，也不得在缺少 point-in-time margin/collateral evidence 时声称订单具备资金充足性。",
        "claim_type": "margin_collateral_available_funds_boundary_rule",
        "sources": ["cme_span", "cme_margins_faq", "cme_credit_controls"],
    },
    {
        "task": "P45-C-RISK06",
        "slug": "post_trade_surveillance_not_pre_trade_gate",
        "title": "post-trade surveillance 不能替代 pre-trade gate",
        "statement": "post-trade surveillance、execution report review、异常复盘和合规监控只能发现或解释已发生风险，不能替代订单进入市场前的 pre-trade controls；若外接项目需要阻断订单，必须由 Risk Management / Live Execution owner 定义 deterministic gate。",
        "claim_type": "post_trade_surveillance_boundary_rule",
        "sources": ["sec_15c3_5_faq", "fia_automated_controls_2024", "cme_pre_trade"],
    },
]


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_layered_risk_{safe}_001.json"


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


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, idx + 1) for idx, key in enumerate(item["sources"])]
    cid = f"cand_20260612_phase45_layered_risk_{item['task'].lower().replace('-', '_')}_001"
    primary_types = {"regulatory_rule", "regulatory_guidance", "professional_body", "official_exchange_doc"}
    primary_count = sum(1 for ref in refs if ref["source_type"] in primary_types)
    source_score = round(sum(float(ref["score"]) for ref in refs) / len(refs), 2)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": cid,
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 P45-C Layered Risk / Credit / Margin 候选，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": "kt.risk_management.layered_risk_controls",
            "canonical_node_id": "kt.risk_management.layered_risk_controls",
            "tree_path": "CEK-TA / Trading Engineering / Risk Management / Layered Risk Controls",
            "related_nodes": [
                "kt.live_execution.audit_trail",
                "kt.trading_engineering.live_execution.execution_tca",
                "kt.ai_engineering.database_storage_engineering.runtime_observability_trace",
            ],
            "partition_id": PARTITION,
            "domain": "risk_management",
            "subdomain": "layered_risk_controls",
            "rule_type": "risk_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trading_ai_project_design_audit",
                "pre_trade_risk_checklist",
                "external_project_rag_retrieval",
                "risk_owner_boundary_review",
            ],
            "classification_notes": "P45-C 只补 Layered Risk / Credit / Margin 知识边界；不设置任何 CEK-TA 通用风险阈值，不启用 hard gate。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_layered_risk.{item['slug']}.v1",
            "evidence_summary": "；".join(ref["evidence_summary"] for ref in refs),
            "interpretation_notes": "本候选只定义分层风控、信用、保证金和 pre-trade/post-trade owner 边界，不输出风险阈值、交易参数或实盘执行建议。",
            "claim_strength": "candidate",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_jurisdiction_venue_and_broker_caveats",
            "asset": "general",
            "timeframe": "pre_trade_and_intraday_risk_context",
            "data_granularity": "order_account_strategy_product_venue_margin_risk_events",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要设计 pre-trade controls、信用/资本限额、订单量/价格控制、消息节流、保证金/抵押品边界或 post-trade surveillance 分工。",
                "AI IDE 需要判断风险字段、owner、证据和 gate 位置是否被混淆。",
                "需要把策略信号、资金/信用约束、交易所控制和风险复核分开建模。",
            ],
            "not_applicable_when": [
                "用户要求具体风险阈值、信用额度、保证金比例、仓位、杠杆、止损止盈或实盘交易动作。",
                "需要外接 broker、clearing firm、exchange 或账户的实时事实时，应由外接项目事实层提供。",
                "需要法律合规结论时，应由对应辖区合规/法律 owner 判断。",
            ],
            "assumptions": [
                "Layered Risk Controls 是交易工程设计和审计上下文，不是策略 alpha。",
                "所有 credit、margin、price band、message-rate 和 surveillance 来源必须声明 venue、broker、clearing、jurisdiction 或 platform caveat。",
                "候选通过 reviewed 审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "SEC Rule 15c3-5 主要适用于美国 broker-dealer market access 语境。",
                "FIA 是行业最佳实践来源，不替代具体监管、交易所或 broker 规则。",
                "CME 来源只证明 CME Globex/CME Clearing 相关机制，不得泛化为所有市场。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": source_score,
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": primary_count,
            "supporting_source_count": len(refs) - primary_count,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "监管、交易所、broker 和清算来源必须保留辖区、venue 和产品边界。",
                "内部字段契约若后续用于 reviewed，需要提供 schema extract 或 contract hash。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Risk Management formal reviewed knowledge",
                "Phase 37 Live Execution formal reviewed knowledge",
                "Phase 45 Execution TCA / Audit Trail formal reviewed knowledge",
                "Phase 45 runtime contract",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有 formal reviewed 知识的直接冲突；P45-C 只补 P1/P2 分层风控和 owner 边界。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分 strategy risk、credit/capital limit、margin/collateral、venue price/size controls 和 post-trade surveillance。",
                "用于生成风险设计 checklist、schema review、RAG 检索上下文和 owner boundary reason code。",
                "用于检查外接项目方案是否把信用、保证金、pre-trade controls 和 post-trade surveillance 混成单一风险布尔值。",
            ],
            "not_allowed": [
                "不得生成具体风险阈值、信用额度、保证金比例、买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、停机、撤单或解锁流程。",
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
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_layered_risk_candidate_generated",
                    "reason": "Generated from Phase 45 P45-C task queue with professional/regulatory/exchange sources.",
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
            "notes": "Generated for external strict audit; no project account, key, position, threshold, or private strategy data included.",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Layered Risk / Credit / Margin 候选知识采集记录",
        "",
        "## 范围",
        "",
        "本批次对应 CEK-TA-461 / P45-C，目标是采集 6 条 Layered Risk / Credit / Margin P1 候选知识。",
        "",
        "本批次只生成候选和审计包，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 来源记录",
        "",
        "| source_key | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 候选列表", "", "| ID | title | source_count | 状态 |", "| --- | --- | ---: | --- |"])
    for candidate in candidates:
        lines.append(
            f"| {candidate['research_task_id']} | {candidate['claim']['title']} | {len(candidate['source_refs'])} | {candidate['status']['review_status']} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. 不输出风险阈值、信用额度、保证金比例、买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "2. SEC、FIA、CME 来源必须保留辖区、venue、产品、broker/clearing 和 implementation caveat。",
            "3. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。",
            "```",
        ]
    )
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 candidates, got {len(candidates)}")
    expected = {f"P45-C-RISK{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition mismatch")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 2:
            failures.append(f"{cid}: primary_source_count < 2")
        gate = item.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default_guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase45_layered_risk_candidate_quality_gate",
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
            "P45-C 只能用于分层风控、信用、保证金和 pre/post-trade owner 边界，不输出风险阈值。",
        ],
    }


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
            "report_id": "phase45_layered_risk_candidate_generation_report",
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
