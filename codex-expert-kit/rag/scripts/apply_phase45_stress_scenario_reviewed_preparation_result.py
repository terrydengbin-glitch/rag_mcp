"""Apply Phase 45 Stress / Scenario reviewed preparation result.

This imports the strict reviewed/caveat_only preparation audit for the six
Phase 45 Stress Testing / Scenario Risk candidates. Five entries are
materialized as formal reviewed/caveat_only knowledge. STRESS02 is supplemented
with direct market/execution liquidity sources and exported for another strict
re-audit.

It never creates approved knowledge, default guidance, hard gates, risk
thresholds, liquidation-horizon numbers, sizing advice, or live trading actions.
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
TASK_ID = "CEK-TA-466"
PARTITION = "KB_07_RISK_MANAGEMENT"
AUDIT_RESULT_ID = "audit_phase45_stress_scenario_reviewed_preparation_20260612"
SOURCE_PACKAGE_ID = "phase45_stress_scenario_reviewed_preparation_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_stress_scenario_stress02_market_liquidity_reaudit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_stress_scenario_reviewed_preparation_import_report.json", start_file=__file__
)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path(
    "docs", "reports", "phase45_stress_scenario_stress02_market_liquidity_reaudit_gate.json", start_file=__file__
)
SUPPLEMENTAL_RESEARCH = resolve_repo_path(
    "docs", "research", "phase45_stress_scenario_stress02_market_liquidity_research.md", start_file=__file__
)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-E-STRESS01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "PFMI、BCBS、CME 足以支撑 scenario stress testing、historical/hypothetical/reverse scenario、治理、方法、文档、数据版本和 owner 边界。"
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 PFMI/FMI、BCBS/bank、CME/clearing caveat。",
            "review frequency 只能作为字段或 policy_ref，不得写默认频率数值。",
            "scenario result 不得进入 execution permission。",
        ],
        "patch_notes": {
            "source": ["保留 PFMI、BCBS Stress Testing Principles、CME Clearing Stress Testing Practices。"],
            "content": ["将 owner、review frequency、data version、scenario assumption version 对齐 stress_scenario_event schema。"],
            "boundary": ["不得输出风险阈值。", "不得生成交易许可。", "不得生成 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS02",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reviewed_allowed": False,
        "reasons": [
            "当前来源足以支撑 clearing liquidity stress、credit/liquidity exposure 和 liquid resources，但不足以直接支撑 market depth、bid-ask spread、execution liquidity。",
            "首轮 accepted_for_draft 时已经要求补 market liquidity / asset liquidity stress 来源，但 reviewed preparation 包没有补入。",
        ],
        "required_followups": [
            "补 ESMA liquidity stress testing guidelines，覆盖 liquidation cost、time to liquidity、trade/order size、higher bid-ask spread、longer time to liquidate。",
            "补 market liquidity / asset liquidity / market impact 来源，覆盖 market depth、bid-ask spread、market impact、time-to-liquidation。",
            "把 clearing liquidity 与 market/execution liquidity 分成两个 source group。",
            "明确缺失 market depth / spread source 时必须标记 unknown，不得当作 normal、zero 或 safe。",
        ],
        "patch_notes": {
            "source": [
                "保留 PFMI、CPMI-IOSCO CCP resilience guidance、CME liquidity risk management、DTCC stress testing 作为 clearing liquidity 来源。",
                "新增 ESMA liquidity stress testing、SEC/eCFR liquidity classification、CFA market liquidity 和 NY Fed market depth 作为 market/execution liquidity 来源。",
            ],
            "content": [
                "把 market_depth、bid_ask_spread、market_impact、time_to_liquidate 作为 market liquidity dimensions。",
                "把 funding、settlement、collateral、clearing、liquid_resources 作为 clearing/funding liquidity dimensions。",
            ],
            "boundary": [
                "不得输出可成交数量。",
                "不得输出滑点阈值。",
                "不得输出 liquidation horizon 数值。",
                "不得生成交易许可或仓位建议。",
            ],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS03",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "补证已覆盖 concentration、wrong-way risk、correlation breakdown 直接证据，claim 已限定为 scenario assumptions。"
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 BCBS/FDIC 银行或 CCR 语境 caveat。",
            "不得从 correlation_assumption 推导降仓、拒单、hard gate。",
        ],
        "patch_notes": {
            "source": ["保留 BCBS stress testing、BCBS sound stress testing、BIS correlation breakdown、FDIC interagency CCR guidance。"],
            "content": ["保留 normal_sample_window_ref、stress_window_ref、assumption_source_refs、not_a_threshold、not_a_trade_action。"],
            "boundary": ["不得输出相关性阈值。", "不得生成降仓、拒单、交易许可或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS04",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "STRESS04 三审补证已解决 margin/funding 缺口，CME、IBKR、Binance 来源能支撑 broker/venue/clearing/account-mode/funding-interval specific scenario dimension。"
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 CME futures/clearing caveat、IBKR broker/account field caveat 和 Binance USD-M Futures caveat。",
            "外接项目必须为自身 broker、venue、clearing、account-mode、funding interval 提供版本化字段来源。",
        ],
        "patch_notes": {
            "source": [
                "保留 Nasdaq、NYSE、CME trading hours、CME Product Margins、IBKR Available for Trading Values、Binance USD-M Futures Account/Funding sources。"
            ],
            "content": ["保留 traditional_exchange、futures_session、crypto_24_7 的 market_type 分层和 direct source ref 要求。"],
            "boundary": ["不得输出风险阈值、隔夜持仓建议、止损止盈、仓位调整、交易许可或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS05",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "Basel market risk / MAR33 / Acerbi-Tasche 已补足 VaR、Expected Shortfall、liquidity horizon、tail loss 的直接依据。"
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 Basel/MAR33 银行监管资本模型 caveat。",
            "不得把 VaR/ES、scenario loss 或 liquidity-adjusted loss 变成 CEK-TA 风险阈值。",
        ],
        "patch_notes": {
            "source": [
                "保留 BCBS stress testing、PFMI、DTCC stress testing、Basel Minimum Capital Requirements for Market Risk、Basel MAR33、Acerbi-Tasche ES。"
            ],
            "content": [
                "保留 VaR、ExpectedShortfall、scenario_loss、max_single_day_loss、max_multi_day_loss、liquidity_adjusted_loss 字段分层。"
            ],
            "boundary": ["不得输出 VaR/ES 阈值。", "不得生成交易许可。", "不得生成降仓、停机或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS06",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "claim 与 stress_result_governance contract 一致：risk_review_input=true、owner_decision_input=true、scenario_backlog_input=true、trade_permission=false、hard_gate=false。"
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 PFMI/BCBS/FIA caveat。",
            "stress_test_passed 不得进入 execution permission、order admission、default guidance 或 hard gate 字段。",
        ],
        "patch_notes": {
            "source": ["保留 BCBS stress testing principles、FIA automated trading risk controls、PFMI。"],
            "content": ["保留 risk_review_input、owner_decision_input、scenario_backlog_input、not_trade_permission。"],
            "boundary": ["不得生成交易许可。", "不得生成 hard gate。", "不得生成风险阈值、仓位、杠杆、止损止盈或实盘执行建议。"],
            "conflict": [],
        },
    },
]


MARKET_LIQUIDITY_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "src_market_liquidity_001",
        "source_title": "ESMA Guidelines on Liquidity Stress Testing in UCITS and AIFs",
        "source_url": "https://www.esma.europa.eu/sites/default/files/library/esma34-39-897_guidelines_on_liquidity_stress_testing_in_ucits_and_aifs_en.pdf",
        "source_type": "regulatory_guideline",
        "publisher": "European Securities and Markets Authority",
        "reliability": "high",
        "score": 94,
        "freshness": "stable",
        "relevance": "high",
        "accessed_at": TODAY,
        "version": "ESMA34-39-897",
        "evidence_summary": "ESMA LST guidelines support liquidation cost, time to liquidity/time to liquidation, trade/order size, stressed market conditions, higher bid-ask spread, lower liquidity and longer time to liquidate.",
        "limitations": [
            "UCITS/AIF fund-liquidity stress testing context; use as market/asset liquidity stress pattern, not as a CEK-TA liquidation-horizon threshold."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_market_liquidity_002",
        "source_title": "17 CFR 270.22e-4 Liquidity risk management programs",
        "source_url": "https://www.ecfr.gov/current/title-17/chapter-II/part-270/section-270.22e-4",
        "source_type": "regulatory_rule",
        "publisher": "eCFR / U.S. Securities and Exchange Commission",
        "reliability": "high",
        "score": 91,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "accessed_at": TODAY,
        "version": None,
        "evidence_summary": "SEC liquidity risk management rule supports time-to-convert/sell/dispose-of investment concepts and significant dilution boundaries for liquidity classification.",
        "limitations": [
            "U.S. registered open-end fund context; not a universal market-depth or trading execution rule."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_market_liquidity_003",
        "source_title": "CFA Institute: Liquidity in Equity Markets",
        "source_url": "https://www.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/liquidity-in-equity-markets-characteristics-dynamics-implications-for-market-quality.pdf",
        "source_type": "professional_body",
        "publisher": "CFA Institute",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "relevance": "high",
        "accessed_at": TODAY,
        "version": None,
        "evidence_summary": "CFA Institute supports bid-ask spread as a trading-cost/liquidity measure and price impact as important for large block orders that must be worked.",
        "limitations": [
            "Equity-market liquidity paper; use as execution/market liquidity evidence, not as all-asset stress-test threshold."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_market_liquidity_004",
        "source_title": "New York Fed Liberty Street Economics: Measuring Treasury Market Depth",
        "source_url": "https://libertystreeteconomics.newyorkfed.org/2024/02/measuring-treasury-market-depth/",
        "source_type": "central_bank_research",
        "publisher": "Federal Reserve Bank of New York",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "accessed_at": TODAY,
        "version": None,
        "evidence_summary": "NY Fed describes market depth as the quantity market participants are willing to buy or sell at particular prices, supporting market depth as a distinct market-liquidity dimension.",
        "limitations": [
            "U.S. Treasury market research; use for market-depth concept, not as all-market liquidity adequacy rule."
        ],
        "quoted_excerpt_allowed": False,
    },
]


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def candidate_paths() -> list[Path]:
    candidate_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
    return sorted(candidate_dir.glob("cand_20260612_phase45_stress_scenario_*.json"))


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_reviewed_caveat_only": 5,
            "needs_more_evidence": 1,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "liquidation_horizon_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "candidate_results": [
            {
                "candidate_id": "",
                "research_task_id": item["research_task_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reviewed_allowed": item["reviewed_allowed"],
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": item["reasons"],
                "required_followups": item["required_followups"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
    }


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    output: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in candidate_paths():
        item = read_json(path)
        output[str(item.get("research_task_id"))] = (path, item)
    return output


def upsert_sources(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    source_refs = list(candidate.get("source_refs", []))
    existing_urls = {ref.get("source_url") for ref in source_refs}
    for ref in refs:
        if ref.get("source_url") not in existing_urls:
            source_refs.append(ref)
            existing_urls.add(ref.get("source_url"))
    candidate["source_refs"] = source_refs
    candidate.setdefault("source_quality", {})["primary_source_count"] = len(source_refs)
    candidate["source_quality"]["supporting_source_count"] = 0
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 75)) for ref in source_refs) / len(source_refs), 2)


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim", {})
    classification = candidate.get("classification", {})
    applicability = candidate.get("applicability", {})
    workflow = candidate.get("workflow", {})
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    knowledge_id = str(conversion.get("proposed_knowledge_id") or "")
    if not knowledge_id:
        normalized = str(claim.get("normalized_claim") or candidate.get("research_task_id", ""))
        knowledge_id = f"kb_phase45_stress_scenario.{normalized.replace('phase45_stress_scenario.', '')}"
        if not knowledge_id.endswith(".v1"):
            knowledge_id += ".v1"
    source_refs = candidate.get("source_refs", [])
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": claim.get("title") or candidate.get("research_task_id"),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": "stress_scenario_boundary_rule",
            "claim_type": classification.get("claim_type"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification.get("tree_node_id"),
            "tree_path": classification.get("tree_path"),
            "canonical_node_id": classification.get("canonical_node_id"),
            "canonical_tree_path": classification.get("tree_path"),
            "risk_level": "high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 45",
            "related_nodes": classification.get("related_nodes", []),
            "classification_notes": "Phase 45 Stress Testing / Scenario Risk formal reviewed/caveat_only；只用于压力测试设计、情景风险复核、schema review 和审计提醒，不是 approved/default guidance/hard gate，不生成风险阈值、交易许可、仓位、杠杆、止损止盈或实盘执行建议。",
        },
        "applicability": {
            "market": applicability.get("market"),
            "asset": applicability.get("asset"),
            "timeframe": applicability.get("timeframe"),
            "data_granularity": applicability.get("data_granularity"),
            "project_type": applicability.get("project_type"),
            "applies_when": applicability.get("applies_when", []),
            "not_applicable_when": applicability.get("not_applicable_when", []),
        },
        "content": {
            "statement": claim.get("statement"),
            "rationale": claim.get("interpretation_notes"),
            "normalized_claim": claim.get("normalized_claim"),
            "claim_strength": "reviewed_caveat_only",
            "performance_claim": False,
            "procedure": [
                "确认问题属于压力测试、情景风险、流动性压力、相关性失效、跳空/隔夜风险、尾部损失或 stress result governance。",
                "检查 scenario、assumption、owner、data_version、source_version、review_status 和 audit_trace 是否声明。",
                "若使用监管、清算、交易所、券商或平台来源，必须保留对应辖区、机构、产品、账户模式和实现 caveat。",
                "若压力测试结果被用作交易许可、下单许可、仓位建议或 hard gate，必须阻断并要求外接项目 Risk Management / Live Execution owner 另行定义 deterministic policy。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "examples": [],
            "anti_patterns": [
                "把 stress test passed 写成交易许可、默认放行或 hard gate。",
                "输出风险阈值、VaR/ES 阈值、流动性阈值、仓位、杠杆、止损止盈、买卖点或实盘执行建议。",
                "把 PFMI、BCBS、CME、DTCC、FIA、Basel 或券商/交易所来源泛化为所有市场的统一规则。",
                "把 scenario assumption、correlation breakdown、tail loss review 或 gap/session risk 直接推导为降仓、拒单、停机或撤单动作。",
            ]
            + as_list(claim.get("anti_patterns")),
            "validation": [
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate/risk_threshold_advice 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "source_evidence 必须保留 regulatory/clearing/exchange/broker/professional source 的适用边界。",
                "不得出现风险阈值、交易许可、仓位建议、杠杆、止损止盈或实盘执行建议。",
            ],
            "risk_notes": [
                "Stress reviewed/caveat_only 只能作为风险复核、schema review、owner 边界和审计提醒。",
                "压力测试结果不能替代 live risk gate、market data truth、order truth 或 portfolio owner 决策。",
                "本条不是 approved，不进入默认指导，不启用 hard gate。",
            ],
            "citation_notes": "；".join(str(ref.get("evidence_summary", "")) for ref in source_refs if ref.get("evidence_summary")),
            "audit_patch_notes": result["patch_notes"],
        },
        "assumptions": applicability.get("assumptions", []),
        "source_evidence": source_refs,
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": candidate.get("conflict_audit", {}).get("checked_against", []),
            "conflicts": [],
            "resolution_summary": "reviewed/caveat_only 准备审计通过；formal creation 保持 caveat_only，不创建 approved、default guidance、hard gate、风险阈值建议或交易许可。",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "review": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "confidence": result["confidence"],
            "freshness": candidate.get("review", {}).get("freshness", "mixed"),
            "reviewer": "external_ai_strict_audit_and_codex",
            "reviewed_at": TODAY,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "approved_at": None,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": result["reasons"],
                "required_followups": result["required_followups"],
                "patch_notes": result["patch_notes"],
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计压力测试、情景风险、流动性压力、尾部风险、owner 决策和 stress result governance。",
                "用于生成压力测试 checklist、schema review、RAG 检索上下文和风险 reason code。",
            ],
            "not_allowed": [
                "不得生成风险阈值、仓位、杠杆、买卖点、止损止盈、交易许可或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、停机、撤单或解锁流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_visibility": "reviewed_caveat_only",
            "reason": "reviewed/caveat_only audit passed; approved/default guidance/hard gate/risk threshold advice remain disabled.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "contribution": candidate.get("contribution", {}),
    }


def supplement_stress02(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    upsert_sources(candidate, MARKET_LIQUIDITY_SOURCES)
    candidate["claim"]["statement"] = (
        "流动性压力测试必须把 clearing/funding liquidity 与 market/execution liquidity 分开声明。"
        "clearing/funding liquidity 覆盖 funding source、settlement/collateral、clearing resources 和 liquid resources；"
        "market/execution liquidity 覆盖 market depth、bid-ask spread、market impact、trade/order size、liquidation cost 和 time-to-liquidate。"
        "缺失 market_depth_source_id、spread_source_id、market_impact_source_id 或 time_to_liquidate_source_id 时，必须标记 unknown，"
        "不得当作 normal、zero、safe 或可成交性证明。"
    )
    candidate["claim"]["evidence_summary"] = (
        "PFMI、CCP resilience、CME 和 DTCC 支撑 clearing/funding liquidity stress；ESMA LST guidelines 支撑 liquidation cost、"
        "time to liquidity/time to liquidation、trade/order size、stressed market 下 higher bid-ask spread、lower liquidity 和 longer time to liquidate；"
        "SEC/eCFR Rule 22e-4 支撑 time-to-convert/sell/dispose-of liquidity classification；"
        "CFA Institute 支撑 bid-ask spread 和 price impact 作为 market/execution liquidity 维度；"
        "NY Fed 支撑 market depth 作为特定价格上可买卖数量的市场流动性维度。"
    )
    candidate["classification"]["classification_notes"] = (
        "P45-E STRESS02 已补 market/execution liquidity 直接来源；仍需外部再审确认能否进入 reviewed/caveat_only。"
    )
    candidate.setdefault("applicability", {}).setdefault("limitations", []).extend(
        [
            "ESMA/SEC/CFA/NY Fed 来源分别具有 fund、equity、Treasury 或市场研究语境，不能直接泛化为所有交易项目的流动性阈值。",
            "market/execution liquidity 只能作为压力情景和审计维度，不输出可成交数量、滑点阈值、清仓时长数值或交易许可。",
        ]
    )
    candidate.setdefault("source_quality", {})["source_groups"] = {
        "clearing_funding_liquidity": [
            "CPMI-IOSCO PFMI",
            "CPMI-IOSCO CCP resilience guidance",
            "CME Clearing Liquidity Risk Management Practices",
            "DTCC Stress Testing",
        ],
        "market_execution_liquidity": [
            "ESMA Liquidity Stress Testing Guidelines",
            "SEC/eCFR Rule 22e-4",
            "CFA Institute Liquidity in Equity Markets",
            "NY Fed Measuring Treasury Market Depth",
        ],
    }
    candidate.setdefault("conflict_audit", {})["resolution_summary"] = (
        "STRESS02 已补 direct market/execution liquidity sources，并将 clearing/funding liquidity 与 market/execution liquidity 分组；等待再审。"
    )
    candidate["status"]["review_status"] = "needs_more_evidence"
    candidate["status"]["ingestion_decision"] = "needs_more_evidence"
    candidate["status"]["decision_reason"] = "reviewed/caveat_only 准备审计未通过；已按审计意见补 market/execution liquidity 证据并导出再审包。"
    candidate["status"]["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence_supplemented"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["allowed_next_decisions"] = ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate", "risk_threshold_advice"]
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "confidence": result["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase45_stress_scenario_stress02_market_liquidity_supplemented",
            "reason": "按 reviewed/caveat_only 审计意见补 market/execution liquidity 直接来源，等待再审。",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )


def write_supplemental_research() -> None:
    content = [
        "# Phase 45 STRESS02 market/execution liquidity 补证记录",
        "",
        "## 补证目标",
        "",
        "STRESS02 首轮 reviewed-preparation 审计认为 PFMI、CCP、CME、DTCC 来源足以支撑 clearing/funding liquidity，但不足以直接支撑 market depth、bid-ask spread、market impact 和 time-to-liquidation。本文补入 market/execution liquidity 直接来源。", 
        "",
        "## 来源分组",
        "",
        "| 分组 | 来源 | URL | 用途 |",
        "| --- | --- | --- | --- |",
        "| clearing/funding liquidity | CPMI-IOSCO PFMI | https://www.iosco.org/library/pubdocs/pdf/IOSCOPD377.pdf | FMI/CCP liquidity risk、liquid resources、stress testing 语境 |",
        "| clearing/funding liquidity | CPMI-IOSCO CCP Resilience | https://www.bis.org/cpmi/publ/d163.pdf | CCP credit/liquidity exposure 和 multiday liquidity stress 语境 |",
        "| clearing/funding liquidity | CME Liquidity Risk Management | https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-liquidity-risk-management-practices.html | CME Clearing liquidity stress 语境 |",
        "| clearing/funding liquidity | DTCC Stress Testing | https://www.dtcc.com/managing-risk/financial-risk-management/stress-testing | clearing agency credit/liquidity exposure 和 financial resources 语境 |",
        "| market/execution liquidity | ESMA Liquidity Stress Testing Guidelines | https://www.esma.europa.eu/sites/default/files/library/esma34-39-897_guidelines_on_liquidity_stress_testing_in_ucits_and_aifs_en.pdf | liquidation cost、time to liquidation、trade/order size、higher bid-ask spread、lower liquidity、longer time to liquidate |",
        "| market/execution liquidity | eCFR Rule 22e-4 | https://www.ecfr.gov/current/title-17/chapter-II/part-270/section-270.22e-4 | liquidity classification 的 time-to-convert/sell/dispose-of 边界 |",
        "| market/execution liquidity | CFA Institute Liquidity in Equity Markets | https://www.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/liquidity-in-equity-markets-characteristics-dynamics-implications-for-market-quality.pdf | bid-ask spread、price impact、block order execution cost |",
        "| market/execution liquidity | NY Fed Measuring Treasury Market Depth | https://libertystreeteconomics.newyorkfed.org/2024/02/measuring-treasury-market-depth/ | market depth 作为特定价格上可买卖数量的市场流动性维度 |",
        "",
        "## 必须保留的边界",
        "",
        "1. clearing/funding liquidity 不得被外推为 market/execution liquidity。",
        "2. market_depth_source_id、spread_source_id、market_impact_source_id、time_to_liquidate_source_id 缺失时必须标记 unknown，不得当作 normal、zero 或 safe。",
        "3. 本条不得输出可成交数量、滑点阈值、liquidation horizon 数值、交易许可、仓位建议或 hard gate。",
        "4. ESMA/SEC/CFA/NY Fed 来源具有基金、权益市场或美国国债市场等语境边界，外接项目必须按自身市场、venue、asset、data vendor 补事实来源。",
    ]
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(content) + "\n", encoding="utf-8")


def export_supplemental_package(candidate: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    urls = {ref.get("source_url") for ref in candidate.get("source_refs", [])}
    for ref in MARKET_LIQUIDITY_SOURCES:
        if ref["source_url"] not in urls:
            failures.append(f"missing market liquidity source: {ref['source_title']}")
    if candidate.get("status", {}).get("ingestion_decision") != "needs_more_evidence":
        failures.append("STRESS02 candidate is not in needs_more_evidence")
    if "market_execution_liquidity" not in candidate.get("source_quality", {}).get("source_groups", {}):
        failures.append("missing market_execution_liquidity source group")

    gate = {
        "gate_id": "phase45_stress_scenario_stress02_market_liquidity_reaudit_gate",
        "checked_at": TODAY,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": 1,
        "expected_count": 1,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只允许判断 STRESS02 是否可进入 formal reviewed/caveat_only。",
            "不得创建 approved、default guidance、hard gate、风险阈值、清仓时长数值、滑点阈值、可成交数量或实盘交易动作。",
        ],
    }
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "45",
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / Risk Management / Scenario Stress Risk",
            "target": "复审 STRESS02 liquidity stress boundary 补入 market/execution liquidity 直接来源后是否可进入 formal reviewed/caveat_only。",
            "candidate_count": 1,
        },
        "hard_boundaries": {
            "reviewed_caveat_only_max": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "liquidation_horizon_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、监管资料、交易所/市场资料、案例和数据，对补证包进行严格再审。",
            "确认 PFMI/CCP/CME/DTCC 只作为 clearing/funding liquidity 来源。",
            "确认 ESMA、SEC/eCFR、CFA、NY Fed 能否支撑 market depth、bid-ask spread、market impact、trade/order size、liquidation cost 和 time-to-liquidate 作为 market/execution liquidity 维度。",
            "确认缺失 market_depth_source_id、spread_source_id、market_impact_source_id、time_to_liquidate_source_id 时必须标记 unknown，不得当作 normal、zero 或 safe。",
            "输出只能是 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {
                "total": 1,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-E-STRESS02",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "quality_gate": gate,
        "candidates": [candidate],
    }
    write_json(SUPPLEMENTAL_GATE, gate)
    write_json(SUPPLEMENTAL_PACKAGE, package)
    return gate


def main() -> int:
    write_json(AUDIT_RESULT_ARCHIVE, audit_result_payload())
    candidates = load_candidates()
    results_by_task = {item["research_task_id"]: item for item in RESULTS}
    promoted: list[dict[str, Any]] = []
    supplemented: list[dict[str, Any]] = []
    failures: list[str] = []

    for task_id, result in results_by_task.items():
        entry = candidates.get(task_id)
        if not entry:
            failures.append(f"{task_id}: candidate not found")
            continue
        path, candidate = entry
        if result["decision"] == "accepted_for_reviewed_caveat_only":
            formal_item = build_formal_item(candidate, result)
            knowledge_dir = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION, start_file=__file__)
            formal_path = knowledge_dir / sanitize_filename(formal_item["knowledge_id"])
            write_json(formal_path, formal_item)
            candidate["status"]["review_status"] = "formalized"
            candidate["status"]["ingestion_decision"] = "formal_reviewed_created"
            candidate["status"]["decision_reason"] = "reviewed/caveat_only 准备审计通过，已创建 formal reviewed/caveat_only。"
            candidate["status"]["updated_at"] = TODAY
            workflow = candidate.setdefault("workflow", {})
            workflow["stage"] = "formalized_reviewed"
            workflow["queue_group"] = "formalized"
            workflow["formal_knowledge_id"] = formal_item["knowledge_id"]
            workflow["formal_review_status"] = "reviewed"
            workflow["formal_knowledge_path"] = repo_relative(formal_path)
            workflow["approved_allowed"] = False
            workflow["default_guidance_allowed"] = False
            workflow["hard_gate_allowed"] = False
            workflow["risk_threshold_advice_allowed"] = False
            candidate.setdefault("review", {}).setdefault("audit_log", []).append(
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_stress_scenario_formal_reviewed_created",
                    "reason": "created formal reviewed/caveat_only from reviewed-preparation audit result",
                    "audit_result_id": AUDIT_RESULT_ID,
                    "formal_knowledge_id": formal_item["knowledge_id"],
                }
            )
            write_json(path, candidate)
            promoted.append(
                {
                    "research_task_id": task_id,
                    "candidate_id": candidate.get("candidate_id"),
                    "knowledge_id": formal_item["knowledge_id"],
                    "formal_path": repo_relative(formal_path),
                }
            )
        elif result["decision"] == "needs_more_evidence":
            supplement_stress02(candidate, result)
            write_json(path, candidate)
            supplemented.append(candidate)

    if len(supplemented) != 1:
        failures.append(f"expected 1 supplemented STRESS02 candidate, got {len(supplemented)}")
        gate = {"gate_status": "fail", "failures": failures}
    else:
        gate = export_supplemental_package(supplemented[0])
    write_supplemental_research()

    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_stress_scenario_reviewed_preparation_import_report",
            "generated_at": TODAY,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "source_package_id": SOURCE_PACKAGE_ID,
            "promoted_count": len(promoted),
            "supplemented_count": len(supplemented),
            "failures": failures,
            "promoted": promoted,
            "supplemental_package": repo_relative(SUPPLEMENTAL_PACKAGE),
            "supplemental_gate": repo_relative(SUPPLEMENTAL_GATE),
            "supplemental_gate_status": gate.get("gate_status"),
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
            "risk_threshold_advice_enabled": False,
            "liquidation_horizon_advice_enabled": False,
            "trade_execution_advice_enabled": False,
        },
    )
    print(
        json.dumps(
            {
                "promoted_count": len(promoted),
                "supplemented_count": len(supplemented),
                "supplemental_gate_status": gate.get("gate_status"),
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if len(promoted) == 5 and len(supplemented) == 1 and gate.get("gate_status") == "pass" and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
