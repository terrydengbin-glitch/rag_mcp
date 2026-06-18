"""Supplement Phase 37 Quant Foundation needs_more_evidence candidates.

Targets P37-A-Q02, P37-A-Q08 and P37-A-Q09, then exports a supplemental
re-audit package. The script does not promote candidates to formal reviewed,
approved, default guidance, or hard gate.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_01_QUANT_FOUNDATION", start_file=__file__)
RESEARCH = resolve_repo_path("docs", "research", "phase37_quant_foundation_supplemental_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase37_quant_foundation_supplemental_evidence_report.json", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase37_quant_foundation_supplemental_reaudit_package_20260611.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase37_quant_foundation_supplemental_reaudit_quality_gate.json", start_file=__file__)


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "r_multiple_definition": {
        "research_task_id": "P37-A-Q02",
        "patch_notes": [
            "保留主归属 kt.quant_foundation.position_sizing，因为 R multiple 依赖初始风险单位；增加 kt.trade_analysis 与 kt.backtest.metrics 作为 related_nodes。",
            "把 R multiple 定位为 risk-normalized performance metric，不再暗示其可替代成本、滑点、样本外或风控审计。",
            "补充 Van Tharp 来源线索和多家交易绩效教育来源；仍要求二审确认是否足以进入 accepted_for_draft。",
        ],
        "additional_sources": [
            {
                "source_title": "R-Multiple: The Only Metric That Scales",
                "source_url": "https://crosstrade.io/learn/performance-metrics/r-multiple",
                "source_type": "trading_education",
                "publisher": "CrossTrade",
                "score": 72,
                "reliability": "medium",
                "evidence_summary": "Defines R as initial dollar risk and R-multiple as outcome expressed in units of that risk, supporting risk-normalized comparison.",
            },
            {
                "source_title": "R and R-Multiples",
                "source_url": "https://traderlion.com/risk-management/r-and-r-multiples/",
                "source_type": "trading_education",
                "publisher": "TraderLion",
                "score": 70,
                "reliability": "medium",
                "evidence_summary": "Explains R-value as initial risk defined by stop loss and R-multiple as profit or loss expressed as a multiple of that risk.",
            },
            {
                "source_title": "What Are R-Multiples? The Key Metric Every Trader Should Know",
                "source_url": "https://trademetria.com/blog/what-are-r-multiples-the-key-metric-every-trader-should-know/",
                "source_type": "trading_journal_article",
                "publisher": "Trademetria",
                "score": 70,
                "reliability": "medium",
                "evidence_summary": "Attributes the R-multiple concept to Van K. Tharp and describes its use for comparing trade outcomes by risk units.",
            },
        ],
    },
    "signal_decision_execution_separation": {
        "research_task_id": "P37-A-Q08",
        "patch_notes": [
            "补充 FIX/FIXimate/OnixS Execution Report 来源，直接支撑订单状态、成交、拒单、费用和执行回报与信号/决策分层记录的必要性。",
            "将 claim 强化为事件链审计规则：signal、decision、order intent、execution report、fill report、trade result 必须可追踪分层。",
            "保留不输出下单许可或执行建议的边界。",
        ],
        "additional_sources": [
            {
                "source_title": "FIXimate: Message ExecutionReport",
                "source_url": "https://fiximate.fixtrading.org/en/FIX.Latest/msg9.html",
                "source_type": "protocol_reference",
                "publisher": "FIX Trading Community / FIXimate",
                "score": 86,
                "reliability": "high",
                "evidence_summary": "FIXimate describes ExecutionReport as relaying order receipt, order status, fills, rejects, and post-trade fee calculations.",
            },
            {
                "source_title": "Execution Report <8> message - FIX 4.4",
                "source_url": "https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html",
                "source_type": "protocol_reference",
                "publisher": "OnixS FIX Dictionary",
                "score": 82,
                "reliability": "medium_high",
                "evidence_summary": "The FIX dictionary states Execution Report is used to confirm orders, relay status, relay fill information and reject orders.",
            },
            {
                "source_title": "Execution Report (8) Message",
                "source_url": "https://library.tradingtechnologies.com/tt-fix/Msg_ExecutionReport_8.html",
                "source_type": "broker_platform_doc",
                "publisher": "Trading Technologies",
                "score": 78,
                "reliability": "medium_high",
                "evidence_summary": "TT FIX documentation describes Execution Report as sending order information such as confirmations, fills and unsolicited changes.",
            },
        ],
    },
    "trade_frequency_vs_quality_boundary": {
        "research_task_id": "P37-A-Q09",
        "replacement_statement": "交易频率不能单独代表交易质量；在高周转、日内、保证金、杠杆或流动性受限场景下，频率上升可能显著提高交易成本、保证金压力、滑点和执行风险，因此必须结合 TCA、账户约束、市场流动性和样本外表现评价。",
        "patch_notes": [
            "按审计意见缩窄 general claim，不再泛化为所有市场频率上升必然放大风险。",
            "补 TCA、market impact、factor strategy turnover cost 和 execution cost 来源。",
            "将频率质量边界与 cost/TCA 关联，避免把交易次数当作交易质量指标。",
        ],
        "additional_sources": [
            {
                "source_title": "Trade Strategy and Execution",
                "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
                "source_type": "professional_body",
                "publisher": "CFA Institute",
                "score": 88,
                "reliability": "high",
                "evidence_summary": "CFA Institute explains trade cost analysis and the need to manage trading costs and execution quality.",
            },
            {
                "source_title": "Transaction Costs of Factor-Investing Strategies",
                "source_url": "https://rpc.cfainstitute.org/research/financial-analysts-journal/2019/ip-transaction-costs-of-factor-investing-strategies",
                "source_type": "professional_body",
                "publisher": "CFA Institute Research and Policy Center",
                "score": 82,
                "reliability": "medium_high",
                "evidence_summary": "The summary describes analysis of trading costs for factor strategies and a large trade dataset, supporting turnover-cost sensitivity.",
            },
            {
                "source_title": "Transaction Cost Analysis in High Frequency Trading",
                "source_url": "https://questdb.com/glossary/transaction-cost-analysis-in-high-frequency-trading/",
                "source_type": "engineering_article",
                "publisher": "QuestDB",
                "score": 72,
                "reliability": "medium",
                "evidence_summary": "Explains TCA for HFT as measuring execution costs and quality at very short time scales with market microstructure context.",
            },
            {
                "source_title": "Execution Insights Through Transaction Cost Analysis",
                "source_url": "https://www.talos.com/insights/execution-insights-through-transaction-cost-analysis-tca-benchmarks-and-slippage",
                "source_type": "market_infrastructure_article",
                "publisher": "Talos",
                "score": 74,
                "reliability": "medium",
                "evidence_summary": "Provides execution examples using arrival price, fees, average execution price, TWAP, VWAP and slippage for TCA.",
            },
        ],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_path(slug: str) -> Path:
    return CANDIDATE_DIR / f"cand_20260611_phase37_{slug}_001.json"


def next_source_id(item: dict[str, Any]) -> int:
    max_id = 0
    for src in item.get("source_refs", []):
        if not isinstance(src, dict):
            continue
        source_id = str(src.get("source_id", ""))
        match = re.search(r"(\d+)$", source_id)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def append_source(item: dict[str, Any], raw: dict[str, Any], index: int) -> None:
    refs = item.setdefault("source_refs", [])
    if any(isinstance(src, dict) and src.get("source_url") == raw["source_url"] for src in refs):
        return
    refs.append(
        {
            "source_id": f"src_{index:03d}",
            "source_title": raw["source_title"],
            "source_url": raw["source_url"],
            "source_type": raw["source_type"],
            "publisher": raw["publisher"],
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": raw["reliability"],
            "score": raw["score"],
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["补证来源；正式入库前仍需二审确认是否足以支撑 claim。"],
            "evidence_summary": raw["evidence_summary"],
            "quoted_excerpt_allowed": False,
        }
    )


def patch_candidate(slug: str, patch: dict[str, Any]) -> dict[str, Any]:
    path = candidate_path(slug)
    item = read_json(path)
    start = next_source_id(item)
    for offset, source in enumerate(patch["additional_sources"]):
        append_source(item, source, start + offset)

    if patch.get("replacement_statement"):
        item.setdefault("claim", {})["statement"] = patch["replacement_statement"]
        item.setdefault("claim", {})["interpretation_notes"] = (
            "本候选已按首轮审计意见收窄表达，只适用于高周转、日内、保证金、杠杆或流动性受限等需要 TCA/执行成本评估的场景。"
        )

    if slug == "r_multiple_definition":
        classification = item.setdefault("classification", {})
        related = classification.setdefault("related_nodes", [])
        for node in ["kt.trade_analysis", "kt.backtest.metrics"]:
            if node not in related:
                related.append(node)
        classification["classification_notes"] = (
            "主归属仍为 kt.quant_foundation.position_sizing，因为 R multiple 依赖初始风险单位；同时作为 risk-normalized performance metric 关联 kt.trade_analysis 与 kt.backtest.metrics。"
        )

    source_quality = item.setdefault("source_quality", {})
    refs = item.get("source_refs", [])
    source_quality["primary_source_count"] = sum(
        1
        for src in refs
        if isinstance(src, dict)
        and src.get("source_type")
        in {"professional_body", "regulatory_guidance", "regulatory_rule", "research_paper", "book", "protocol_reference"}
    )
    source_quality["supporting_source_count"] = len(refs) - int(source_quality["primary_source_count"])
    source_quality["score"] = round(sum(int(src.get("score", 0)) for src in refs if isinstance(src, dict)) / max(len(refs), 1))
    source_quality["limitations"] = list(dict.fromkeys(source_quality.get("limitations", []) + patch["patch_notes"]))

    review = item.setdefault("review", {})
    review["open_questions"] = list(
        dict.fromkeys(
            review.get("open_questions", [])
            + [
                "二审是否认为补证足以升级为 accepted_for_draft？",
                "是否需要为 risk-normalized performance metrics 新增独立 L3 知识树节点？",
            ]
        )
    )
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_needs_more_evidence_supplemented",
            "reason": "根据首轮严格审计补充来源、边界和分类说明，并准备二审包。",
            "audit_result_id": "audit_result_phase37_quant_foundation_candidate_audit_20260611_strict_v1",
        }
    )

    status = item.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "supplemented_for_reaudit"
    status["updated_at"] = TODAY
    status["decision_reason"] = "已按首轮审计意见补证，等待二审；仍不是 reviewed/approved/default guidance。"
    workflow = item.setdefault("workflow", {})
    workflow["stage"] = "supplemented_for_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "external_ai_or_human_reaudit"
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    write_json(path, item)
    return item


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def quality_gate(items: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for item in items:
        candidate_id = str(item.get("candidate_id", ""))
        refs = item.get("source_refs", [])
        if len(refs) < 5:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_5_after_supplement"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_allowed_not_false"})
        if item.get("status", {}).get("ingestion_decision") != "supplemented_for_reaudit":
            failures.append({"candidate_id": candidate_id, "failure": "not_supplemented_for_reaudit"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
    return {
        "report_id": "phase37_quant_foundation_supplemental_reaudit_quality_gate",
        "generated_at": TODAY,
        "scope": "P37-A-Q02/Q08/Q09 supplemental re-audit package",
        "candidate_count": len(items),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "supplemented candidates remain candidate-only; no reviewed/approved/default guidance/hard gate.",
    }


def write_research(items: list[dict[str, Any]]) -> None:
    rows = [
        "| 任务 | 候选 | 补证重点 | 来源数 |",
        "| --- | --- | --- | ---: |",
    ]
    for item in items:
        slug = str(item["candidate_id"]).removeprefix("cand_20260611_phase37_").removesuffix("_001")
        rows.append(
            f"| {item['research_task_id']} | `{item['candidate_id']}` | {'；'.join(SUPPLEMENTS[slug]['patch_notes'])} | {len(item['source_refs'])} |"
        )
    content = f"""# Phase 37 Quant Foundation 补证研究记录

生成日期：{TODAY}

## 范围

本文件只记录首轮审计中 3 条 `needs_more_evidence` 候选的补证，不创建正式知识、不创建 reviewed、不创建 approved、不进入默认指导。

## 补证清单

{chr(10).join(rows)}

## 二审入口

```text
docs/audit/phase37_quant_foundation_supplemental_reaudit_package_20260611.json
```
"""
    RESEARCH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH.write_text(content, encoding="utf-8")


def build_package(items: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": "phase37_quant_foundation_supplemental_reaudit_package_20260611",
        "package_type": "candidate_ai_reaudit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": "37",
        "title": "Phase 37 Quant Foundation 3 条补证候选二审包",
        "purpose": "严格复审 P37-A-Q02、P37-A-Q08、P37-A-Q09 补证后是否可升级为 accepted_for_draft，或仍需补证/拒绝。",
        "strict_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "二审最多允许 accepted_for_draft，不允许 reviewed、approved、default guidance 或 hard gate。",
            "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "如果来源仍不足或表述仍过宽，必须继续 needs_more_evidence 或 rejected。",
        ],
        "audit_instructions": [
            "必须搜索相关的专业网站、资料、案例和数据，对补证质量进行严格审计。",
            "检查 Q02 的 R multiple 来源是否足以支撑 risk-normalized metric 定义；若仍只是 vendor/教育来源，请保持 needs_more_evidence。",
            "检查 Q08 的 FIX/Execution Report 来源是否足以支撑 signal/decision/order/execution/fill/result 分层记录规则。",
            "检查 Q09 是否已经缩窄到高周转、日内、保证金、杠杆或流动性受限场景，并且 TCA/turnover cost 来源是否足够。",
            "输出只能是 accepted_for_draft、needs_more_evidence 或 rejected。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": "phase37_quant_foundation_supplemental_reaudit_package_20260611",
            "auditor": "string",
            "audited_at": "string",
            "summary": {"total": 3, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": ["string"],
                }
            ],
        },
        "quality_gate": quality,
        "candidates": items,
    }


def main() -> None:
    items = [patch_candidate(slug, patch) for slug, patch in SUPPLEMENTS.items()]
    quality = quality_gate(items)
    write_json(QUALITY, quality)
    write_json(AUDIT, build_package(items, quality))
    write_research(items)
    write_json(
        REPORT,
        {
            "report_id": "phase37_quant_foundation_supplemental_evidence_report",
            "generated_at": TODAY,
            "supplemented_count": len(items),
            "candidate_ids": [item["candidate_id"] for item in items],
            "audit_package": str(AUDIT),
            "quality_gate": quality,
            "boundary": "No formal reviewed knowledge, approved knowledge, default guidance, or hard gate was created.",
        },
    )
    if quality["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {quality['failures']}")
    print(json.dumps({"supplemented": len(items), "reaudit_package": str(AUDIT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
