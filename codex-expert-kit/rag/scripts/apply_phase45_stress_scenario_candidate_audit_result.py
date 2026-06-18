"""Apply Phase 45 Stress Testing / Scenario Risk candidate audit result.

This imports the first strict audit for P45-E. Three candidates are marked
accepted_for_draft. Three candidates are supplemented with stronger sources and
exported for supplemental re-audit.

It never creates reviewed/approved knowledge, default guidance, hard gates,
risk thresholds, positions, leverage, stop-loss/take-profit parameters, trade
permission, or live trading actions.
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
AUDIT_RESULT_ID = "audit_phase45_stress_scenario_candidate_20260612_external_strict"
PACKAGE_ID = "phase45_stress_scenario_candidate_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_stress_scenario_supplemental_reaudit_package_20260612"
PARTITION = "KB_07_RISK_MANAGEMENT"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_stress_scenario_candidate_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_stress_scenario_supplemental_reaudit_gate.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_stress_scenario_supplemental_research.md", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-E-STRESS01",
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress01_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "PFMI、BCBS stress testing principles、CME Clearing stress testing practices 足以支撑 historical、hypothetical、scenario-based stress testing、governance、methodology、documentation 和 review 边界。",
            "claim 明确压力测试不是普通最大回撤回测，方向正确。",
            "未发现交易参数、风险阈值、仓位、杠杆、止损止盈、交易许可或实盘执行建议。",
        ],
        "required_followups": [
            "进入 draft 时保留 caveat：PFMI 是 FMI/CCP 语境，BCBS 是银行/监管语境，CME 是 clearing 语境。",
            "将 owner、review frequency、data version 写成 schema 字段要求，不得写固定数值或 hard gate。",
        ],
        "patch_notes": {
            "source": ["保留 PFMI、BCBS stress testing principles、CME Clearing stress testing practices。"],
            "content": ["建议把“必须声明复核频率”改为“必须声明复核频率字段和 owner”，避免被误读为默认频率规则。"],
            "boundary": ["不得输出交易许可。", "不得输出风险阈值。", "不得把 stress test 结果变成 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS02",
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress02_001",
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reasons": [
            "PFMI、CCP resilience guidance、CME liquidity risk management、DTCC stress testing 足以支撑 liquidity stress 与 price/PnL stress 分层。",
            "claim 中 funding source、settlement/collateral、liquidation horizon、venue availability 与 clearing liquidity 语境基本匹配。",
            "market depth 和 bid-ask spread 属于 market liquidity / execution liquidity，当前来源支撑较弱，但不影响进入 draft。",
        ],
        "required_followups": [
            "补 market liquidity / asset liquidity stress 来源，覆盖 market depth、bid-ask spread、market impact、time-to-liquidation。",
            "明确本条不输出可成交数量、滑点阈值、清仓阈值或交易许可。",
            "保留 clearing/CCP/venue caveat。",
        ],
        "patch_notes": {
            "source": [
                "保留 PFMI、CPMI-IOSCO CCP resilience guidance、CME liquidity risk management、DTCC stress testing。",
                "建议补 ESMA liquidity stress testing、IOSCO liquidity risk management 或 asset liquidity stress 文献。",
            ],
            "content": ["把 market depth / bid-ask spread 标为 market liquidity dimension，不能从 clearing liquidity 直接外推。"],
            "boundary": ["不得输出具体流动性阈值。", "不得输出 liquidation horizon 数值。", "不得生成交易许可或仓位建议。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS03",
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress03_001",
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reasons": [
            "claim 方向正确：压力下常态相关性可能失效，组合分散性需要 stress scenario 复核。",
            "但当前 source_refs 对 correlation increase、correlation reversal、normal-sample correlation limitation 的直接支撑不足。",
            "wrong-way risk 在 claim 中出现，但 source_refs 未直接引用更精确的 wrong-way risk / concentration stress 来源。",
        ],
        "required_followups": [
            "补 BCBS counterparty credit risk / wrong-way risk stress testing 直接来源。",
            "补 concentration risk / correlation stress / diversification breakdown 来源。",
            "将“相关性反转”说明为 scenario assumption，而不是被当前来源直接证明的必然规律。",
        ],
        "patch_notes": {
            "source": ["新增 wrong-way risk、concentration 和 correlation breakdown 直接来源。"],
            "content": ["把“不能用常态样本相关性证明压力时期仍然分散”保留，但标注为风险 caveat。"],
            "boundary": ["不得输出相关性阈值。", "不得生成降仓、拒单或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS04",
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress04_001",
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reasons": [
            "claim 涉及跳空、隔夜、周末、假日、停牌/恢复、session close/open、价格路径不可见性、订单不可执行窗口、保证金/融资变化和数据可用边界。",
            "当前 FIA、CME、BCBS 来源只能泛化支撑自动交易风控、波动控制、压力测试框架，不能直接支撑上述全部非连续交易风险细项。",
            "尤其停牌/恢复、订单不可执行窗口、session close/open 需要交易所规则、市场微结构或 broker/venue 文档直接支持。",
        ],
        "required_followups": [
            "补交易所 market hours / trading halt / reopen / session close-open 规则来源。",
            "补 gap risk / overnight risk / non-continuous market risk 专业来源。",
            "补 margin/funding change around close/open 或 weekend/holiday 的 broker/venue 来源。",
            "把 crypto 24/7 与传统交易所 session 风险分开说明。",
        ],
        "patch_notes": {
            "source": ["FIA 可保留为 automated trading risk controls 背景；新增 gap/overnight/session/halt 直接来源。"],
            "content": ["需要明确不同市场：24/7 crypto、futures session、equities halt/auction 的差异。"],
            "boundary": ["不得输出隔夜持仓建议。", "不得输出止损止盈或仓位调整。", "不得输出 session 风险阈值或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS05",
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress05_001",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "claim 中 VaR/ES、scenario loss、最大单日/多日损失、liquidity-adjusted loss、模型外事件和样本外覆盖是合理尾部风险复核字段。",
            "当前来源能支撑 stress governance 和 scenario loss，但不能充分直接支撑 VaR/ES 与 liquidity-adjusted tail loss。",
            "PF、胜率、均值、普通回撤不能替代尾部风险评估的边界正确，但仍需更直接的 market risk / Expected Shortfall / VaR limitation 来源。",
        ],
        "required_followups": [
            "补 Basel market risk / FRTB Expected Shortfall 来源。",
            "补 VaR limitation、Expected Shortfall、tail risk 直接来源。",
            "补 liquidity-adjusted VaR / liquidity horizon / market illiquidity 来源。",
            "明确 PF、胜率、均值、普通回撤只是 performance/backtest metrics，不是 tail-loss risk measure。",
        ],
        "patch_notes": {
            "source": ["新增 Basel Minimum Capital Requirements for Market Risk / FRTB ES、VaR/ES 或 liquidity-adjusted risk 专业来源。"],
            "content": ["把 VaR/ES、scenario loss、liquidity-adjusted loss 分成 tail_loss_review schema 字段。"],
            "boundary": ["不得输出 VaR/ES 阈值。", "不得把尾部亏损复核结果变成交易许可。", "不得生成降仓、停机或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-E-STRESS06",
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress06_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "压力测试结果只能作为风险复核、资本/流动性规划、人工审批、scenario backlog 或 owner 决策输入，这与 BCBS/PFMI 的治理语境一致。",
            "claim 明确禁止压力测试通过直接生成买卖点、仓位、杠杆、止损止盈、实盘放行或 hard gate，边界正确。",
            "未发现交易参数、风险阈值、私有账户事实、密钥、交易所私有配置或实盘敏感信息。",
        ],
        "required_followups": [
            "进入 draft 时明确 stress_test_passed 只能进入 review input，不得进入 execution permission 字段。",
            "如后续引入 stress_result schema，需要提供内部 contract extract 或 hash。",
            "保留 PFMI/BCBS/FIA 的机构和行业实践 caveat。",
        ],
        "patch_notes": {
            "source": ["保留 BCBS stress testing principles、FIA automated trading risk controls、PFMI。"],
            "content": ["建议把 stress_result_governance 拆成 risk_review_input、owner_decision_input、scenario_backlog_input、not_trade_permission。"],
            "boundary": ["不得生成交易许可。", "不得生成 hard gate。", "不得生成风险阈值、仓位、杠杆、止损止盈或实盘执行建议。"],
            "conflict": [],
        },
    },
]


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "bcbs155_stress": {
        "source_title": "Principles for sound stress testing practices and supervision",
        "source_url": "https://www.bis.org/publ/bcbs155.pdf",
        "source_type": "professional_body",
        "publisher": "Basel Committee on Banking Supervision",
        "reliability": "high",
        "score": 91,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "BCBS stress-testing guidance includes stress testing of credit-risk concentrations and wrong-way risk considerations, supporting concentration/correlation stress caveats.",
        "limitations": ["Bank/supervisory guidance; not a CEK-TA trading threshold source."],
    },
    "bis_correlation_breakdown": {
        "source_title": "Evaluating correlation breakdowns during periods of market volatility",
        "source_url": "https://www.bis.org/publ/confer08k.pdf",
        "source_type": "professional_research",
        "publisher": "Bank for International Settlements",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "BIS conference paper discusses correlation breakdown during volatile markets and the problem that correlations may change dramatically during major market events.",
        "limitations": ["Research paper; supports caveat and scenario design, not deterministic trading action."],
    },
    "fdic_ccr_concentration": {
        "source_title": "Interagency Supervisory Guidance on Counterparty Credit Risk Management",
        "source_url": "https://www.fdic.gov/news/financial-institution-letters/2011/fil11053a.pdf",
        "source_type": "regulatory_guidance",
        "publisher": "FDIC / U.S. supervisory agencies",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "relevance": "medium_high",
        "evidence_summary": "Interagency guidance supports concentration analysis and counterparty credit-risk stress testing as part of risk reporting and governance.",
        "limitations": ["Counterparty credit-risk guidance; not a strategy portfolio correlation standard."],
    },
    "nasdaq_halt_orders": {
        "source_title": "Nasdaq Equity 4 Rules: Trading halt and pause order handling",
        "source_url": "https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20Equity%204",
        "source_type": "official_exchange_doc",
        "publisher": "Nasdaq",
        "reliability": "high",
        "score": 89,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Nasdaq rules include halt/pause order handling, including cases where orders entered during a halt or pause will not be accepted unless directed elsewhere.",
        "limitations": ["Nasdaq-specific equity market rules; not universal across all venues or assets."],
    },
    "nyse_mwcb_faq": {
        "source_title": "NYSE Market-Wide Circuit Breakers FAQ",
        "source_url": "https://www.nyse.com/publicdocs/nyse/NYSE_MWCB_FAQ.pdf",
        "source_type": "official_exchange_doc",
        "publisher": "NYSE",
        "reliability": "high",
        "score": 89,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "NYSE FAQ supports market-wide circuit breaker halt durations and reopening-auction processing after halts.",
        "limitations": ["NYSE/US equity market context; not universal global market behavior."],
    },
    "cme_trading_hours": {
        "source_title": "CME Group Holiday and Trading Hours",
        "source_url": "https://www.cmegroup.com/trading-hours.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "CME trading-hours and holiday schedules support session, holiday, early-close and product-specific trading-hour boundaries.",
        "limitations": ["CME-specific schedule source; product schedules may vary and must be versioned."],
    },
    "investopedia_gap_risk": {
        "source_title": "Gap Risk Explained",
        "source_url": "https://www.investopedia.com/terms/g/gaprisk.asp",
        "source_type": "education_article",
        "publisher": "Investopedia",
        "reliability": "medium",
        "score": 68,
        "freshness": "stable",
        "relevance": "medium_high",
        "evidence_summary": "Supporting source describing gap risk as price movement while markets are closed, with greater risk over weekends or longer closures.",
        "limitations": ["Education/supporting source only; not acceptable as sole reviewed evidence."],
    },
    "bis_market_risk_d457": {
        "source_title": "Minimum capital requirements for market risk",
        "source_url": "https://www.bis.org/bcbs/publ/d457.htm",
        "source_type": "professional_body",
        "publisher": "Basel Committee on Banking Supervision",
        "reliability": "high",
        "score": 92,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "BCBS market-risk standard supports the revised market-risk framework and Expected Shortfall as a market-risk measure.",
        "limitations": ["Bank capital framework; not a CEK-TA trading threshold or strategy approval source."],
    },
    "bis_mar33_liquidity_horizon": {
        "source_title": "Basel Framework MAR33 Internal models approach",
        "source_url": "https://www.bis.org/basel_framework/chapter/MAR/33.htm",
        "source_type": "professional_body",
        "publisher": "Bank for International Settlements",
        "reliability": "high",
        "score": 91,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Basel MAR33 supports liquidity horizons and stressed expected shortfall calculations in the market-risk internal models approach.",
        "limitations": ["Regulatory capital model context; not a project-level risk threshold source."],
    },
    "acerbi_tasche_es": {
        "source_title": "Expected Shortfall: a natural coherent alternative to Value at Risk",
        "source_url": "https://faculty.washington.edu/ezivot/econ589/acertasc.pdf",
        "source_type": "professional_research",
        "publisher": "Acerbi and Tasche",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "Acerbi and Tasche discuss Expected Shortfall as a coherent alternative to Value at Risk and as an average of worst-tail losses.",
        "limitations": ["Research source; does not define CEK-TA schema or trading permissions."],
    },
}


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


def source_ref(key: str, source_id: str) -> dict[str, Any]:
    ref = dict(SUPPLEMENTAL_SOURCES[key])
    ref.update({"source_id": source_id, "accessed_at": TODAY, "version": None, "quoted_excerpt_allowed": False})
    return ref


def upsert_sources(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    source_refs = list(candidate.get("source_refs", []))
    existing = {ref.get("source_url") for ref in source_refs}
    for ref in refs:
        if ref.get("source_url") not in existing:
            source_refs.append(ref)
            existing.add(ref.get("source_url"))
    candidate["source_refs"] = source_refs
    candidate.setdefault("source_quality", {})["primary_source_count"] = sum(
        1 for ref in source_refs if ref.get("source_type") != "education_article"
    )
    candidate["source_quality"]["supporting_source_count"] = sum(1 for ref in source_refs if ref.get("source_type") == "education_article")
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 75)) for ref in source_refs) / len(source_refs), 2)


def candidate_path(task_id: str) -> Path:
    for path in sorted(CANDIDATE_DIR.glob("cand_20260612_phase45_stress_scenario_*.json")):
        item = read_json(path)
        if item.get("research_task_id") == task_id:
            return path
    raise FileNotFoundError(task_id)


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_draft": 3,
            "needs_more_evidence": 3,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "candidate_results": [
            {
                **result,
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
            }
            for result in RESULTS
        ],
    }


def mark_accepted(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    candidate["status"]["review_status"] = "accepted"
    candidate["status"]["ingestion_decision"] = "accepted_for_draft"
    candidate["status"]["decision_reason"] = "外部严格审计通过，可进入 draft；不得进入 reviewed/approved/default/hard gate。"
    candidate["status"]["updated_at"] = TODAY
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "decision": result["decision"],
        "confidence": result["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": result["reasons"],
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase45_stress_scenario_candidate_audit_imported",
            "reason": f"{result['decision']} / confidence={result['confidence']}",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "accepted_for_draft"
    workflow["queue_group"] = "ai_passed"
    workflow["allowed_next_decisions"] = ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]


def supplement_candidate(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    task_id = str(candidate.get("research_task_id"))
    if task_id == "P45-E-STRESS03":
        candidate["claim"]["statement"] = (
            "压力场景应把相关性上升、相关性结构改变、集中风险、wrong-way risk 和跨资产共同冲击作为 scenario assumptions "
            "进行复核；常态样本相关性只能作为输入证据之一，不能证明组合在压力时期仍然分散。相关性反转或 breakdown 必须标注为情景假设，"
            "不得生成相关性阈值、降仓、拒单或 hard gate。"
        )
        candidate["claim"]["evidence_summary"] = (
            "BCBS stress-testing guidance 支撑 concentration / wrong-way risk stress；BIS correlation breakdown 研究支撑高波动时期相关性可能显著变化；"
            "FDIC interagency CCR guidance 支撑 concentration analysis 与 CCR stress testing governance。"
        )
        upsert_sources(
            candidate,
            [
                source_ref("bcbs155_stress", "src_supp_001"),
                source_ref("bis_correlation_breakdown", "src_supp_002"),
                source_ref("fdic_ccr_concentration", "src_supp_003"),
            ],
        )
    elif task_id == "P45-E-STRESS04":
        candidate["claim"]["statement"] = (
            "跳空、隔夜、周末、假日、停牌/恢复和 session close/open 风险必须按市场与 venue 分开声明。传统交易所、期货 session "
            "和 crypto 24/7 市场的不可交易窗口、开盘/复牌 auction、订单接受规则、假日/early-close 日历、保证金/融资变化和数据可用边界不同；"
            "不得把连续盘中回测假设外推到非连续交易时段，也不得输出隔夜持仓建议、止损止盈、仓位调整、session 阈值或 hard gate。"
        )
        candidate["claim"]["evidence_summary"] = (
            "Nasdaq 规则支撑 halt/pause 期间订单接受边界；NYSE MWCB FAQ 支撑 market-wide halt 和 reopening auction；"
            "CME trading hours 支撑 holiday/early-close/session 边界；gap risk supporting source 支撑闭市期间价格跳变风险。"
        )
        upsert_sources(
            candidate,
            [
                source_ref("nasdaq_halt_orders", "src_supp_001"),
                source_ref("nyse_mwcb_faq", "src_supp_002"),
                source_ref("cme_trading_hours", "src_supp_003"),
                source_ref("investopedia_gap_risk", "src_supp_004"),
            ],
        )
    elif task_id == "P45-E-STRESS05":
        candidate["claim"]["statement"] = (
            "尾部亏损复核应把 VaR、Expected Shortfall、scenario loss、最大单日/多日损失、liquidity horizon、liquidity-adjusted loss、"
            "模型外事件和样本外覆盖分开声明。Profit Factor、胜率、均值和普通回撤只能作为绩效/回测指标，不能替代尾部风险评估；"
            "不得输出 VaR/ES 阈值、交易许可、降仓、停机或 hard gate。"
        )
        candidate["claim"]["evidence_summary"] = (
            "BCBS market-risk standard 支撑 Expected Shortfall 与市场风险框架；Basel MAR33 支撑 liquidity horizon / stressed ES；"
            "Acerbi-Tasche 研究支撑 Expected Shortfall 作为 worst-tail average loss 风险度量。"
        )
        upsert_sources(
            candidate,
            [
                source_ref("bis_market_risk_d457", "src_supp_001"),
                source_ref("bis_mar33_liquidity_horizon", "src_supp_002"),
                source_ref("acerbi_tasche_es", "src_supp_003"),
            ],
        )
    candidate["status"]["review_status"] = "needs_more_evidence"
    candidate["status"]["ingestion_decision"] = "needs_more_evidence"
    candidate["status"]["decision_reason"] = "首轮严格审计要求补充直接证据；已按审计意见补证并导出再审包。"
    candidate["status"]["updated_at"] = TODAY
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
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
            "action": "phase45_stress_scenario_needs_more_evidence_supplemented",
            "reason": "按首轮严格审计意见补直接来源，等待再审。",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence_supplemented"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["allowed_next_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_next_decisions"] = ["reviewed", "approved", "default_guidance", "hard_gate"]


def supplemental_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    expected = {"P45-E-STRESS03", "P45-E-STRESS04", "P45-E-STRESS05"}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected supplemental task set: {sorted(actual ^ expected)}")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("status", {}).get("ingestion_decision") != "needs_more_evidence":
            failures.append(f"{cid}: not needs_more_evidence")
        if len(item.get("source_refs", [])) < 6:
            failures.append(f"{cid}: source_refs < 6")
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must remain deny")
    return {
        "gate_id": "phase45_stress_scenario_supplemental_reaudit_gate",
        "checked_at": TODAY,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 3,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本补证包只允许判断 STRESS03/04/05 是否可从 needs_more_evidence 升级为 accepted_for_draft。",
            "不得创建 reviewed、approved、default guidance、hard gate、风险阈值或交易许可。",
        ],
    }


def write_supplemental_research(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Stress Scenario 首轮审计补证记录",
        "",
        "## 补证范围",
        "",
        "本文件记录 P45-E-STRESS03、P45-E-STRESS04、P45-E-STRESS05 的首轮审计补证。补证后仍只进入再审包，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 新增来源",
        "",
        "| key | 来源 | URL | 用途 |",
        "| --- | --- | --- | --- |",
    ]
    for key, source in SUPPLEMENTAL_SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 补证候选", "", "| ID | source_count | 状态 |", "| --- | ---: | --- |"])
    for item in candidates:
        lines.append(f"| {item['research_task_id']} | {len(item.get('source_refs', []))} | {item['status']['review_status']} |")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. STRESS03 不输出相关性阈值、降仓、拒单或 hard gate。",
            "2. STRESS04 不输出隔夜持仓建议、止损止盈、仓位调整、session 风险阈值或 hard gate。",
            "3. STRESS05 不输出 VaR/ES 阈值、交易许可、降仓、停机或 hard gate。",
            "```",
        ]
    )
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_supplemental_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "45",
        "task_id": TASK_ID,
        "source_audit_result_id": AUDIT_RESULT_ID,
        "scope": {
            "branch": "Trading Engineering / Risk Management / Scenario Stress Risk",
            "target": "复审 STRESS03/STRESS04/STRESS05 补直接证据后是否可进入 accepted_for_draft。",
            "candidate_count": len(candidates),
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、交易所/清算机构文档、专业研究和案例，对补证包进行严格再审。",
            "只判断 STRESS03、STRESS04、STRESS05 是否可从 needs_more_evidence 升级为 accepted_for_draft。",
            "不得输出 reviewed、approved、default guidance 或 hard gate。",
            "不得生成风险阈值、仓位、杠杆、止损止盈、交易许可或实盘执行建议。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {"total": 3, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-E-STRESS03 | P45-E-STRESS04 | P45-E-STRESS05",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
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
        "candidates": candidates,
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)
    write_json(SUPPLEMENTAL_GATE, gate)


def main() -> int:
    write_json(AUDIT_RESULT_ARCHIVE, audit_result_payload())
    accepted: list[dict[str, Any]] = []
    supplemented: list[dict[str, Any]] = []
    failures: list[str] = []

    for result in RESULTS:
        try:
            path = candidate_path(result["research_task_id"])
            candidate = read_json(path)
            if result["decision"] == "accepted_for_draft":
                mark_accepted(candidate, result)
                accepted.append({"research_task_id": result["research_task_id"], "candidate_id": result["candidate_id"]})
            elif result["decision"] == "needs_more_evidence":
                supplement_candidate(candidate, result)
                supplemented.append(candidate)
            else:
                failures.append(f"unsupported decision {result['research_task_id']}: {result['decision']}")
            write_json(path, candidate)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{result['research_task_id']}: {exc}")

    gate = supplemental_gate(supplemented)
    export_supplemental_package(supplemented, gate)
    write_supplemental_research(supplemented)
    report = {
        "report_id": "phase45_stress_scenario_candidate_audit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": PACKAGE_ID,
        "accepted_for_draft_count": len(accepted),
        "supplemented_count": len(supplemented),
        "accepted_for_draft": accepted,
        "supplemental_package": repo_relative(SUPPLEMENTAL_PACKAGE),
        "supplemental_gate": repo_relative(SUPPLEMENTAL_GATE),
        "supplemental_gate_status": gate["gate_status"],
        "failures": failures,
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(accepted) == 3 and len(supplemented) == 3 and gate["gate_status"] == "pass" and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
