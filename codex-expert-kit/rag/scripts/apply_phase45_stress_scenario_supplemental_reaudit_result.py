"""Apply Phase 45 Stress Scenario supplemental re-audit result.

This imports the supplemental strict audit for P45-E STRESS03/04/05.
STRESS03 and STRESS05 are moved to accepted_for_draft. STRESS04 remains
needs_more_evidence, receives direct margin/funding evidence, and is exported
as a single-candidate re-audit package.

This script never creates reviewed/approved knowledge, default guidance, hard
gates, risk thresholds, positions, leverage, stop-loss/take-profit parameters,
trade permission, or live trading actions.
"""

from __future__ import annotations

import json
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

AUDIT_RESULT_ID = "audit_phase45_stress_scenario_supplemental_reaudit_20260612"
SOURCE_PACKAGE_ID = "phase45_stress_scenario_supplemental_reaudit_package_20260612"
STRESS04_PACKAGE_ID = "phase45_stress_scenario_stress04_margin_funding_reaudit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_stress_scenario_supplemental_reaudit_import_report.json", start_file=__file__
)
STRESS04_PACKAGE = resolve_repo_path("docs", "audit", f"{STRESS04_PACKAGE_ID}.json", start_file=__file__)
STRESS04_GATE = resolve_repo_path(
    "docs", "reports", "phase45_stress_scenario_stress04_margin_funding_reaudit_gate.json", start_file=__file__
)
STRESS04_RESEARCH = resolve_repo_path(
    "docs", "research", "phase45_stress_scenario_stress04_margin_funding_research.md", start_file=__file__
)


RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress03_001",
        "research_task_id": "P45-E-STRESS03",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "wrong-way risk、concentration risk、correlation breakdown 直接证据已补入。",
            "claim 已将相关性上升、结构改变、反转或 breakdown 收窄为 scenario assumptions，而不是确定性规律。",
            "claim 明确不得生成相关性阈值、降仓、拒单或 hard gate，风险边界正确。",
        ],
        "required_followups": [
            "保留 caveat：BCBS / FDIC 来源主要是银行或 counterparty credit risk 语境。",
            "保留 caveat：BIS correlation breakdown 研究只能支撑风险假设和 scenario design，不能生成交易动作。",
            "如后续进入 reviewed，需要补 CEK-TA stress_result schema 或 scenario_assumption schema。",
        ],
        "patch_notes": {
            "source": [
                "保留 BCBS stress testing principles、CPMI-IOSCO CCP resilience、CME stress testing。",
                "新增 BCBS sound stress testing practices、BIS correlation breakdown、FDIC interagency CCR guidance。",
            ],
            "content": [
                "保留常态样本相关性只能作为输入证据之一，不能证明压力时期仍然分散。",
                "保留相关性反转或 breakdown 必须标注为情景假设。",
            ],
            "boundary": ["不得输出相关性阈值。", "不得生成降仓、拒单、交易许可或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress04_001",
        "research_task_id": "P45-E-STRESS04",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "halt/pause、reopening auction、session close/open、holiday/early-close、gap risk 的直接证据已补强。",
            "claim 已区分传统交易所、期货 session 与 crypto 24/7 市场，方向正确。",
            "但 claim 仍包含保证金/融资变化，当前 source_refs 没有 broker、venue、clearing 或 exchange margin/funding 直接来源支撑。",
        ],
        "required_followups": [
            "补 broker / exchange / clearing margin documentation，例如 futures initial/maintenance margin change、overnight margin、holiday margin、funding/financing source。",
            "如不补来源，则将保证金/融资变化改为 optional dimension 或删除。",
            "明确 crypto 24/7 下的非连续风险更多来自 venue outage、funding settlement、maintenance window、liquidity gap，而非传统 exchange close/open。",
            "不得输出隔夜持仓建议、止损止盈、仓位调整、session 阈值或 hard gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 Nasdaq halt/pause order handling、NYSE MWCB FAQ、CME trading hours、gap risk supporting source。",
                "FIA / CME / BCBS 只能作为风险控制和压力测试背景来源。",
                "必须补 broker/venue/clearing margin-funding direct source，或删除 claim 中相关字段。",
            ],
            "content": [
                "把不可交易窗口、开盘/复牌 auction、订单接受规则、假日/early-close 日历、数据可用边界保留。",
                "保证金/融资变化暂不应作为已支撑 claim 主体。",
            ],
            "boundary": ["不得输出隔夜持仓建议。", "不得输出止损止盈、仓位调整、session 风险阈值或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress05_001",
        "research_task_id": "P45-E-STRESS05",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "Expected Shortfall、VaR/ES、liquidity horizon、liquidity-adjusted tail loss 直接证据已补入。",
            "Basel market risk standard 和 MAR33 足以支撑 Expected Shortfall 与 liquidity horizon 在市场风险框架中的使用。",
            "Acerbi-Tasche 支撑 Expected Shortfall 作为 worst-tail average loss 风险度量。",
            "claim 已明确 PF、胜率、均值和普通回撤只是绩效/回测指标，不能替代尾部风险评估。",
            "claim 明确不得输出 VaR/ES 阈值、交易许可、降仓、停机或 hard gate。",
        ],
        "required_followups": [
            "保留 caveat：Basel / MAR33 是银行监管资本和市场风险模型语境，不是 CEK-TA 交易阈值来源。",
            "将 VaR、Expected Shortfall、scenario loss、liquidity horizon、liquidity-adjusted loss 拆成 tail_loss_review schema 字段。",
            "如后续进入 reviewed，需要补内部 stress_result / tail_loss_review contract extract。",
        ],
        "patch_notes": {
            "source": [
                "保留 BCBS stress testing principles、PFMI、DTCC stress testing。",
                "新增 Basel Minimum Capital Requirements for Market Risk、Basel MAR33、Acerbi-Tasche Expected Shortfall。",
            ],
            "content": [
                "保留 VaR、Expected Shortfall、scenario loss、最大单日/多日损失、liquidity horizon、liquidity-adjusted loss、模型外事件和样本外覆盖字段。",
                "保留 performance/backtest metrics 与 tail risk metrics 的边界。",
            ],
            "boundary": ["不得输出 VaR/ES 阈值。", "不得把尾部亏损复核结果变成交易许可。", "不得生成降仓、停机或 hard gate。"],
            "conflict": [],
        },
    },
]


STRESS04_MARGIN_FUNDING_SOURCES: list[dict[str, Any]] = [
    {
        "source_title": "CME Group Product Margins",
        "source_url": "https://www.cmegroup.com/solutions/risk-management/margin-services/product-margins.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "CME defines futures margins/performance bonds as deposits required to cover potential losses and notes margin requirements vary by product and market volatility.",
        "limitations": ["CME futures/clearing context only; not universal broker or crypto venue margin semantics."],
        "source_id": "src_margin_001",
        "accessed_at": TODAY,
        "version": None,
        "quoted_excerpt_allowed": False,
    },
    {
        "source_title": "IBKR Available for Trading Values",
        "source_url": "https://www.ibkrguides.com/traderworkstation/available-for-trading.htm",
        "source_type": "broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR distinguishes Available Funds, Excess Liquidity and Buying Power, supporting broker/account-specific margin and financing field boundaries.",
        "limitations": ["IBKR-specific account field semantics; not universal across brokers or venues."],
        "source_id": "src_margin_002",
        "accessed_at": TODAY,
        "version": None,
        "quoted_excerpt_allowed": False,
    },
    {
        "source_title": "Binance USD-M Futures Account Balance",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Account-Balance-V2",
        "source_type": "official_exchange_api_doc",
        "publisher": "Binance Open Platform",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance USD-M Futures account balance response exposes wallet balance, cross wallet balance, available balance and margin availability fields.",
        "limitations": ["Binance USD-M Futures API/account-mode context only; not a general broker or exchange rule."],
        "source_id": "src_margin_003",
        "accessed_at": TODAY,
        "version": None,
        "quoted_excerpt_allowed": False,
    },
    {
        "source_title": "Binance USD-M Futures Get Funding Info",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-Info",
        "source_type": "official_exchange_api_doc",
        "publisher": "Binance Open Platform",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance funding-info endpoint returns symbols with funding-rate cap/floor or fundingIntervalHours adjustments, supporting venue-specific funding-change evidence.",
        "limitations": ["Binance USD-M Futures funding semantics only; not universal crypto or traditional futures financing semantics."],
        "source_id": "src_margin_004",
        "accessed_at": TODAY,
        "version": None,
        "quoted_excerpt_allowed": False,
    },
    {
        "source_title": "Binance Futures Balance and Position Update Event",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/user-data-streams/Event-Balance-and-Position-Update",
        "source_type": "official_exchange_api_doc",
        "publisher": "Binance Open Platform",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "Binance user data stream documents account updates for balance, position, margin type and funding-fee balance changes.",
        "limitations": ["Binance USD-M Futures event semantics only; not universal account-event schema."],
        "source_id": "src_margin_005",
        "accessed_at": TODAY,
        "version": None,
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


def candidate_path(task_id: str) -> Path:
    for path in sorted(CANDIDATE_DIR.glob("cand_20260612_phase45_stress_scenario_*.json")):
        item = read_json(path)
        if item.get("research_task_id") == task_id:
            return path
    raise FileNotFoundError(task_id)


def audit_archive_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 3,
            "accepted_for_draft": 2,
            "needs_more_evidence": 1,
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


def result_by_task(task_id: str) -> dict[str, Any]:
    for result in RESULTS:
        if result["research_task_id"] == task_id:
            return result
    raise KeyError(task_id)


def mark_accepted(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    candidate["status"]["review_status"] = "accepted"
    candidate["status"]["ingestion_decision"] = "accepted_for_draft"
    candidate["status"]["decision_reason"] = "补证再审通过，可进入 draft；不得进入 reviewed/approved/default/hard gate。"
    candidate["status"]["updated_at"] = TODAY
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_draft",
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
            "action": "phase45_stress_scenario_supplemental_reaudit_imported",
            "reason": "accepted_for_draft; no reviewed/approved/default/hard gate.",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "accepted_for_draft"
    workflow["queue_group"] = "ai_passed"
    workflow["allowed_next_decisions"] = ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]


def upsert_sources(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    source_refs = list(candidate.get("source_refs", []))
    existing = {ref.get("source_url") for ref in source_refs}
    for ref in refs:
        if ref["source_url"] not in existing:
            source_refs.append(ref)
            existing.add(ref["source_url"])
    candidate["source_refs"] = source_refs
    candidate.setdefault("source_quality", {})["primary_source_count"] = sum(
        1 for ref in source_refs if ref.get("source_type") != "education_article"
    )
    candidate["source_quality"]["supporting_source_count"] = sum(
        1 for ref in source_refs if ref.get("source_type") == "education_article"
    )
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 75)) for ref in source_refs) / len(source_refs), 2)


def supplement_stress04(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    candidate["claim"]["statement"] = (
        "跳空、隔夜、周末、假日、停牌/恢复和 session close/open 风险必须按市场与 venue 分开声明。"
        "传统交易所、期货 session 和 crypto 24/7 市场的不可交易窗口、开盘/复牌 auction、订单接受规则、"
        "假日/early-close 日历、保证金/融资变化和数据可用边界不同；保证金/融资变化只能写成 broker、"
        "venue、clearing、account-mode 或 funding-interval specific 的情景维度，必须带直接来源和字段版本。"
        "不得把连续盘中回测假设外推到非连续交易时段，也不得输出隔夜持仓建议、止损止盈、仓位调整、session 阈值或 hard gate。"
    )
    candidate["claim"]["evidence_summary"] = (
        "Nasdaq 规则支撑 halt/pause 期间订单接受边界；NYSE MWCB FAQ 支撑 market-wide halt 和 reopening auction；"
        "CME trading hours 支撑 holiday/early-close/session 边界；CME product margins 支撑 futures margin/performance bond "
        "随产品和市场波动变化；IBKR 文档支撑 Available Funds、Excess Liquidity、Buying Power 等 broker 账户字段差异；"
        "Binance USD-M Futures 文档支撑 crypto futures available balance、margin availability、funding interval/rate adjustment "
        "和 funding-fee balance update 的 venue/account-mode 语义。"
    )
    upsert_sources(candidate, STRESS04_MARGIN_FUNDING_SOURCES)
    candidate["status"]["review_status"] = "needs_more_evidence"
    candidate["status"]["ingestion_decision"] = "needs_more_evidence"
    candidate["status"]["decision_reason"] = "补证再审仍要求 margin/funding 直接来源；已补 CME/IBKR/Binance 直接来源并导出单条三审包。"
    candidate["status"]["updated_at"] = TODAY
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
        "reasons": result["reasons"],
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase45_stress04_margin_funding_evidence_supplemented",
            "reason": "补 CME margin、IBKR account margin/buying power、Binance funding/account balance 直接来源，等待单条三审。",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence_supplemented"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["allowed_next_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_next_decisions"] = ["reviewed", "approved", "default_guidance", "hard_gate"]


def stress04_gate(candidate: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    urls = {ref.get("source_url") for ref in candidate.get("source_refs", [])}
    required_urls = {ref["source_url"] for ref in STRESS04_MARGIN_FUNDING_SOURCES}
    missing = sorted(required_urls - urls)
    if missing:
        failures.append(f"missing margin/funding direct sources: {missing}")
    if candidate.get("status", {}).get("ingestion_decision") != "needs_more_evidence":
        failures.append("STRESS04 must remain needs_more_evidence before third audit")
    if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
        failures.append("machine_gate.default_guidance must remain deny")
    return {
        "gate_id": "phase45_stress_scenario_stress04_margin_funding_reaudit_gate",
        "checked_at": TODAY,
        "task_id": TASK_ID,
        "package_id": STRESS04_PACKAGE_ID,
        "candidate_count": 1,
        "expected_count": 1,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只判断 STRESS04 补 margin/funding direct source 后是否可进入 accepted_for_draft。",
            "不得创建 reviewed、approved、default guidance、hard gate、风险阈值或交易许可。",
        ],
    }


def export_stress04_package(candidate: dict[str, Any], gate: dict[str, Any]) -> None:
    package = {
        "package_id": STRESS04_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "45",
        "task_id": TASK_ID,
        "source_audit_result_id": AUDIT_RESULT_ID,
        "scope": {
            "branch": "Trading Engineering / Risk Management / Scenario Stress Risk",
            "target": "复审 STRESS04 补 broker/venue/clearing margin-funding direct source 后是否可进入 accepted_for_draft。",
            "candidate_count": 1,
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
            "必须搜索相关专业网站、官方文档、监管资料、交易所/清算机构文档、broker/venue API 文档、专业案例和数据，对 STRESS04 进行严格三审。",
            "只判断 STRESS04 是否可从 needs_more_evidence 升级为 accepted_for_draft。",
            "重点核验 CME margin/performance bond、IBKR Available Funds/Excess Liquidity/Buying Power、Binance futures account balance/funding interval/funding fee 来源是否足以支撑 guarantee/margin/funding change 作为 venue/account-mode-specific scenario dimension。",
            "不得输出 reviewed、approved、default guidance 或 hard gate。",
            "不得生成风险阈值、仓位、杠杆、止损止盈、交易许可或实盘执行建议。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": STRESS04_PACKAGE_ID,
            "summary": {"total": 1, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress04_001",
                    "research_task_id": "P45-E-STRESS04",
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
        "candidate": candidate,
    }
    write_json(STRESS04_PACKAGE, package)
    write_json(STRESS04_GATE, gate)


def write_stress04_research(candidate: dict[str, Any]) -> None:
    lines = [
        "# Phase 45 STRESS04 保证金/融资变化补证记录",
        "",
        "## 补证目标",
        "",
        "补齐 STRESS04 在二审中指出的 margin / funding direct source 缺口。补证后仍只导出三审包，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 新增直接来源",
        "",
        "| 来源 | URL | 用途 | 边界 |",
        "| --- | --- | --- | --- |",
    ]
    for ref in STRESS04_MARGIN_FUNDING_SOURCES:
        lines.append(f"| {ref['source_title']} | {ref['source_url']} | {ref['evidence_summary']} | {ref['limitations'][0]} |")
    lines.extend(
        [
            "",
            "## 候选状态",
            "",
            f"- candidate_id: `{candidate['candidate_id']}`",
            f"- research_task_id: `{candidate['research_task_id']}`",
            f"- source_count: `{len(candidate.get('source_refs', []))}`",
            "- 当前状态：`needs_more_evidence_supplemented`，等待 STRESS04 单条三审。",
            "",
            "## 保留边界",
            "",
            "```text",
            "1. margin / funding 只能作为 broker、venue、clearing、account-mode 或 funding-interval specific 的情景维度。",
            "2. 不得输出隔夜持仓建议、止损止盈、仓位调整、session 风险阈值或 hard gate。",
            "3. 不得把 Binance funding、IBKR buying power 或 CME performance bond 泛化成所有市场规则。",
            "```",
        ]
    )
    STRESS04_RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    write_json(AUDIT_ARCHIVE, audit_archive_payload())
    accepted: list[dict[str, str]] = []
    failures: list[str] = []

    for task_id in ["P45-E-STRESS03", "P45-E-STRESS05"]:
        result = result_by_task(task_id)
        try:
            path = candidate_path(task_id)
            candidate = read_json(path)
            mark_accepted(candidate, result)
            write_json(path, candidate)
            accepted.append({"research_task_id": task_id, "candidate_id": result["candidate_id"]})
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{task_id}: {exc}")

    stress04_candidate: dict[str, Any] | None = None
    try:
        stress04_path = candidate_path("P45-E-STRESS04")
        stress04_candidate = read_json(stress04_path)
        supplement_stress04(stress04_candidate, result_by_task("P45-E-STRESS04"))
        write_json(stress04_path, stress04_candidate)
        gate = stress04_gate(stress04_candidate)
        export_stress04_package(stress04_candidate, gate)
        write_stress04_research(stress04_candidate)
    except Exception as exc:  # noqa: BLE001
        failures.append(f"P45-E-STRESS04: {exc}")
        gate = {"gate_status": "fail", "failures": failures}

    report = {
        "report_id": "phase45_stress_scenario_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "accepted_for_draft_count": len(accepted),
        "still_needs_more_evidence_count": 1 if stress04_candidate else 0,
        "accepted_for_draft": accepted,
        "stress04_reaudit_package": repo_relative(STRESS04_PACKAGE),
        "stress04_reaudit_gate": repo_relative(STRESS04_GATE),
        "stress04_research": repo_relative(STRESS04_RESEARCH),
        "stress04_gate_status": gate.get("gate_status"),
        "failures": failures + list(gate.get("failures", [])),
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["accepted_for_draft_count"] == 2 and report["stress04_gate_status"] == "pass" and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
