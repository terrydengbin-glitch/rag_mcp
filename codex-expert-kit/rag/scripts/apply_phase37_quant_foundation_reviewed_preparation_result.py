"""Apply Phase 37 Quant Foundation reviewed-preparation audit result.

The external strict audit allows nine Quant Foundation candidates to become
formal reviewed/caveat_only knowledge and keeps three candidates in
needs_more_evidence. This script preserves that boundary: no approved
knowledge, no default guidance, no hard gate, and no trading execution advice.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-380"
AUDIT_RESULT_ID = "phase37_quant_foundation_reviewed_preparation_audit_result_20260611_strict_v2"
SOURCE_PACKAGE_ID = "phase37_quant_foundation_reviewed_preparation_audit_package_20260611"
EXPECTED_TOTAL = 12
EXPECTED_PROMOTED = 9
EXPECTED_NEEDS_MORE = 3

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_01_QUANT_FOUNDATION", start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_quant_foundation_reviewed_preparation_import_report.json", start_file=__file__
)


ACCEPTED_TASKS = {
    "P37-A-Q01": {
        "confidence": "medium",
        "reason": "EV 的 probability × payoff 定义稳定，可作为 caveat-only 定义。",
        "required_patches": [
            "补概率论/统计学或机构级 expected value 来源；Investopedia/CrossTrade 只能作为 supporting。",
        ],
    },
    "P37-A-Q03": {
        "confidence": "medium",
        "reason": "高 R/R 不得单独描述为策略优势是保守方法论边界。",
        "required_patches": [
            "补 Bailey/OOS 或回测偏差来源。",
            "补 CFA trading-costs 来源。",
        ],
    },
    "P37-A-Q04": {
        "confidence": "high",
        "reason": "CFA Trade Strategy and Execution 与 Trading Costs 支撑成本调整边界。",
        "required_patches": [
            "显式补 CFA Trading Costs 到 source_refs。",
        ],
    },
    "P37-A-Q05": {
        "confidence": "medium",
        "reason": "胜率不能单独证明系统质量，由 EV 的概率/幅度结构支持。",
        "required_patches": [
            "补 tail risk/drawdown 和 CFA cost/TCA 来源。",
        ],
    },
    "P37-A-Q07": {
        "confidence": "high",
        "reason": "SEC/Investor.gov 和 FINRA 保证金资料直接支持杠杆放大损失风险。",
        "required_patches": [
            "保留美国证券保证金、期货、crypto、CFD、海外 broker/venue 的适用差异。",
        ],
    },
    "P37-A-Q08": {
        "confidence": "high",
        "reason": "FIX ExecutionReport 来源支持 signal/decision/execution 分层审计。",
        "required_patches": [
            "限定为 CEK-TA 事件流与审计 schema 架构要求，不得说成所有市场监管硬要求。",
        ],
    },
    "P37-A-Q09": {
        "confidence": "high",
        "reason": "FINRA 26-10 与 intraday margin 资料支持高频率交易成本和风险边界。",
        "required_patches": [
            "保留 FINRA 26-10 的发布时间、生效时间和 phase-in 边界。",
        ],
    },
    "P37-A-Q10": {
        "confidence": "high",
        "reason": "Bailey 等 backtest overfitting / out-of-sample degradation 支撑样本内不能证明 edge。",
        "required_patches": [
            "把进入默认指导或实盘前写成 CEK-TA governance 语境，不是外部金融事实。",
        ],
    },
    "P37-A-Q12": {
        "confidence": "high",
        "reason": "CFA trading-costs 与 Bailey/backtesting 资料支持无成本说明时不得描述为可复用盈利能力。",
        "required_patches": [
            "formal item 继续保持 default_guidance_allowed=false，避免 default_guidance_block 命名造成机器误用。",
        ],
    },
}

NEEDS_MORE_TASKS = {
    "P37-A-Q02": {
        "confidence": "high",
        "reason": "R-multiple 三审只够 accepted_for_draft；reviewed 前仍缺 Van Tharp 书籍页码级证据。",
        "required_followups": [
            "补 Super Trader 或 The Definitive Guide to Position Sizing 的页码级书籍证据。",
            "保留 risk_normalized_metrics 主分类，position_sizing 仅作为 related dependency。",
        ],
        "next_action": "supplement_page_level_van_tharp_book_evidence_then_reaudit",
    },
    "P37-A-Q06": {
        "confidence": "high",
        "reason": "需要拆分 Trading Engineering 仓位 sizing 外部金融事实与 CEK-TA AI governance 内部规则。",
        "required_followups": [
            "将外部规则限定为仓位 sizing 需要风险预算、风险单位、失效边界和最大暴露。",
            "将“AI 只能提示缺字段，不能推导仓位”拆为 CEK-TA 内部 AI governance/schema 规则，并补内部正式来源。",
        ],
        "next_action": "split_position_sizing_rule_and_ai_governance_boundary_then_reaudit",
    },
    "P37-A-Q11": {
        "confidence": "high",
        "reason": "现有来源支撑过拟合和样本外风险，但不足以直接支撑完整 regime / non-stationarity 泛化边界。",
        "required_followups": [
            "补 regime / non-stationarity 一手或高质量专业来源。",
            "将单一 regime 不得泛化跨市场、跨周期、跨状态的强规则与样本量/过拟合规则区分。",
        ],
        "next_action": "supplement_regime_non_stationarity_sources_then_reaudit",
    },
}

SUPPLEMENTAL_SOURCES = {
    "P37-A-Q01": [
        {
            "source_id": "src_audit_ms_probabilities_payoffs",
            "source_title": "Probabilities and Payoffs",
            "source_url": "https://www.morganstanley.com/im/publication/insights/articles/article_probabilitiesandpayoffs.pdf",
            "source_type": "institutional_research",
            "publisher": "Morgan Stanley Investment Management",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "score": 82,
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["机构研究资料；用于支撑 expected value 的概率与 payoff 表达，不构成交易建议。"],
            "evidence_summary": "说明 expected value 需要 payoff 与对应概率相乘后求和。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q03": [
        {
            "source_id": "src_audit_cfa_trading_costs",
            "source_title": "Trading Costs and Electronic Markets",
            "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
            "source_type": "professional_body",
            "publisher": "CFA Institute",
            "published_at": "2026-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 90,
            "relevance": "high",
            "freshness": "time_sensitive",
            "limitations": ["CFA 专业学习资料；用于成本和执行边界，不支持任何具体策略优势。"],
            "evidence_summary": "覆盖 explicit/implicit costs、bid-ask spread、market impact、delay、unfilled trades 等交易成本。",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_audit_bailey_backtest_overfitting",
            "source_title": "The Probability of Backtest Overfitting",
            "source_url": "https://sdm.lbl.gov/oapapers/ssrn-id2326253.pdf",
            "source_type": "paper",
            "publisher": "SSRN / Lawrence Berkeley National Laboratory",
            "published_at": "2014-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 88,
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["论文支撑过拟合和样本外边界，不直接证明任何交易信号有效。"],
            "evidence_summary": "讨论回测过拟合和样本外表现退化风险，支撑 R/R 不能脱离验证被描述为 edge。",
            "quoted_excerpt_allowed": False,
        },
    ],
    "P37-A-Q04": [
        {
            "source_id": "src_audit_cfa_trading_costs",
            "source_title": "Trading Costs and Electronic Markets",
            "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
            "source_type": "professional_body",
            "publisher": "CFA Institute",
            "published_at": "2026-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 90,
            "relevance": "high",
            "freshness": "time_sensitive",
            "limitations": ["CFA 专业学习资料；用于成本和执行边界，不支持任何具体策略优势。"],
            "evidence_summary": "列出显性和隐性交易成本、点差、市场冲击、延迟和未成交等成本项。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q05": [
        {
            "source_id": "src_audit_cfa_trading_costs",
            "source_title": "Trading Costs and Electronic Markets",
            "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
            "source_type": "professional_body",
            "publisher": "CFA Institute",
            "published_at": "2026-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 90,
            "relevance": "high",
            "freshness": "time_sensitive",
            "limitations": ["用于成本和执行边界；胜率/期望值解释仍需结合 payoff 与样本验证。"],
            "evidence_summary": "成本、点差、市场冲击和延迟会改变交易结果评价，支撑胜率不能单独判断系统质量。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q07": [
        {
            "source_id": "src_audit_investor_gov_margin_accounts",
            "source_title": "Investor Bulletin: Understanding Margin Accounts",
            "source_url": "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-29",
            "source_type": "regulator_investor_education",
            "publisher": "Investor.gov / SEC",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 88,
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["美国证券保证金账户教育资料；不自动泛化到期货、crypto、CFD 或海外交易场所。"],
            "evidence_summary": "说明保证金交易可能放大损失、触发追加保证金和强制卖出等风险。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q08": [
        {
            "source_id": "src_audit_onixs_fix_execution_report",
            "source_title": "Execution Report <8> message - FIX 4.2",
            "source_url": "https://www.onixs.biz/fix-dictionary/4.2/msgtype_8_8.html",
            "source_type": "protocol_reference",
            "publisher": "OnixS FIX Dictionary",
            "published_at": None,
            "accessed_at": TODAY,
            "version": "FIX 4.2",
            "reliability": "medium_high",
            "score": 84,
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["FIX 协议参考；用于事件语义和执行回报边界，不等同所有市场监管硬要求。"],
            "evidence_summary": "ExecutionReport 覆盖订单状态、成交、拒单等执行事件，支持 signal/decision/execution 分层。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q09": [
        {
            "source_id": "src_audit_finra_26_10",
            "source_title": "Regulatory Notice 26-10",
            "source_url": "https://www.finra.org/rules-guidance/notices/26-10",
            "source_type": "regulatory_notice",
            "publisher": "FINRA",
            "published_at": "2026-04-20",
            "accessed_at": TODAY,
            "version": "Effective 2026-06-04; phase-in through 2027-10-20",
            "reliability": "high",
            "score": 88,
            "relevance": "medium_high",
            "freshness": "current",
            "limitations": ["FINRA 规则通知适用于对应监管范围；不自动泛化到全部市场。"],
            "evidence_summary": "提供日内保证金和高频交易相关监管上下文，支持高频率交易质量必须结合成本和约束审计。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q10": [
        {
            "source_id": "src_audit_bailey_statistical_overfitting",
            "source_title": "Statistical Overfitting and Backtest Performance",
            "source_url": "https://sdm.lbl.gov/oapapers/ssrn-id2507040-bailey.pdf",
            "source_type": "paper",
            "publisher": "SSRN / Lawrence Berkeley National Laboratory",
            "published_at": "2014-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 88,
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["论文支撑回测过拟合和样本外退化，不证明任何具体策略 edge。"],
            "evidence_summary": "讨论 backtest overfitting 和 out-of-sample degradation，支持样本内结果不能单独证明可复用 edge。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-A-Q12": [
        {
            "source_id": "src_audit_cfa_trading_costs",
            "source_title": "Trading Costs and Electronic Markets",
            "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
            "source_type": "professional_body",
            "publisher": "CFA Institute",
            "published_at": "2026-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 90,
            "relevance": "high",
            "freshness": "time_sensitive",
            "limitations": ["用于交易成本和执行边界；不支持任何具体盈利承诺。"],
            "evidence_summary": "支撑无成本、成交和执行质量说明时不得把结果描述为可复用盈利能力。",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_audit_bailey_backtest_overfitting",
            "source_title": "The Probability of Backtest Overfitting",
            "source_url": "https://sdm.lbl.gov/oapapers/ssrn-id2326253.pdf",
            "source_type": "paper",
            "publisher": "SSRN / Lawrence Berkeley National Laboratory",
            "published_at": "2014-01-01",
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 88,
            "relevance": "high",
            "freshness": "stable",
            "limitations": ["支撑回测偏差边界，不证明盈利能力。"],
            "evidence_summary": "支撑没有数据偏差、样本外和成本审计时不得宣称可复用盈利能力。",
            "quoted_excerpt_allowed": False,
        },
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_root() -> Path:
    return resolve_repo_path(start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(repo_root()).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dedupe_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = value.strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (str(source.get("source_url") or ""), str(source.get("source_title") or source.get("title") or ""))


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [s for s in as_list(candidate.get("source_refs")) if isinstance(s, dict)]
    for source in SUPPLEMENTAL_SOURCES.get(str(candidate.get("research_task_id")), []):
        if source_key(source) not in {source_key(existing) for existing in sources}:
            sources.append(source)
    return sources


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id", "")),
        "source_title": str(source.get("source_title") or source.get("title") or ""),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type", "other")),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability", "medium")),
        "relevance": str(source.get("relevance", "medium")),
        "evidence_summary": str(source.get("evidence_summary", "")),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def title_from_candidate(candidate: dict[str, Any]) -> str:
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:96] if statement else str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), ""))


def build_audit_result() -> dict[str, Any]:
    decisions = []
    for task_id, meta in ACCEPTED_TASKS.items():
        decisions.append(
            {
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": meta["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [meta["reason"]],
                "required_patches": {
                    "source": [patch for patch in meta["required_patches"] if "补" in patch or "来源" in patch],
                    "content": [patch for patch in meta["required_patches"] if "写成" in patch or "限定" in patch],
                    "boundary": meta["required_patches"],
                    "conflict": ["可见上下文内未发现可证冲突；完整 formal KB 冲突检查由 CEK-TA-196/197 继续执行。"],
                },
                "required_extra_sources": SUPPLEMENTAL_SOURCES.get(task_id, []),
                "formal_conversion_notes": [
                    "formal reviewed/caveat_only only",
                    "approved_allowed=false",
                    "default_guidance_allowed=false",
                    "hard_gate_allowed=false",
                ],
            }
        )
    for task_id, meta in NEEDS_MORE_TASKS.items():
        decisions.append(
            {
                "research_task_id": task_id,
                "decision": "needs_more_evidence",
                "confidence": meta["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [meta["reason"]],
                "required_patches": {
                    "source": meta["required_followups"],
                    "content": meta["required_followups"],
                    "boundary": [
                        "补证前不得 formal reviewed。",
                        "不得 approved、default guidance 或 hard gate。",
                    ],
                    "conflict": ["补证后重新执行 formal KB 可见冲突检查。"],
                },
                "required_extra_sources": [],
                "formal_conversion_notes": [meta["next_action"]],
            }
        )
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "task_id": TASK_ID,
        "quality_gate": {
            "pass": False,
            "candidate_count": EXPECTED_TOTAL,
            "accepted_for_reviewed_caveat_only": EXPECTED_PROMOTED,
            "needs_more_evidence": EXPECTED_NEEDS_MORE,
            "rejected": 0,
            "notes": [
                "外部严格审计不同意包内自评全部通过。",
                "9 条可进入 formal reviewed/caveat_only。",
                "3 条继续 needs_more_evidence。",
            ],
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trading_execution_advice_allowed": False,
        },
        "decisions": sorted(decisions, key=lambda item: str(item["research_task_id"])),
    }


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            result[task_id] = (path, candidate)
    return result


def validate_candidate_for_reviewed(candidate: dict[str, Any]) -> str | None:
    if deep_get(candidate, ("status", "review_status")) != "accepted":
        return "status_not_accepted"
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "not_accepted_for_draft"
    queue_group = deep_get(candidate, ("workflow", "queue_group"))
    if queue_group not in {"ai_passed", "formalized"}:
        return "not_ai_passed"
    if queue_group == "formalized" and not deep_get(candidate, ("workflow", "formal_knowledge_id")):
        return "formalized_missing_formal_knowledge_id"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_proposed_knowledge_id"
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        return "default_guidance_not_disabled"
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        return "hard_gate_not_disabled"
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {"none", "resolved", "none_known_in_visible_context"}:
        return "unsafe_conflict"
    if not merge_sources(candidate):
        return "missing_sources"
    return None


def shape_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    primary = len([source for source in sources if str(source.get("reliability")) in {"high", "medium_high"}])
    limitations = dedupe_strings(
        as_list(raw.get("limitations"))
        + as_list(deep_get(decision, ("required_patches", "source"), []))
        + [
            "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
            "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文。",
        ]
    )
    return {
        "overall_reliability": raw.get("overall_reliability", "medium"),
        "score": raw.get("score", 0),
        "score_version": raw.get("score_version", "phase37_source_scoring_v1"),
        "primary_source_count": max(int(raw.get("primary_source_count") or 0), primary),
        "supporting_source_count": max(len(sources) - primary, 0),
        "low_reliability_source_count": raw.get("low_reliability_source_count", 0),
        "limitations": limitations,
    }


def shape_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    task_id = str(candidate.get("research_task_id"))
    risk_notes = dedupe_strings(
        as_list(applicability.get("limitations"))
        + as_list(deep_get(decision, ("required_patches", "boundary"), []))
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "AI Engineering 只能引用本 Trading Engineering 规则本体，不得复制改写为模型训练/RAG/MCP 本体规则。",
        ]
    )
    procedure = [
        "确认当前问题属于 Quant Foundation / Trading Engineering 规则本体，而不是 AI Engineering 训练、RAG 或 MCP 本体。",
        "同时检查概率、payoff、成本、样本、执行、风险和验证边界，避免单一指标泛化。",
        "返回本知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
    ]
    if task_id in {"P37-A-Q03", "P37-A-Q04", "P37-A-Q05", "P37-A-Q12"}:
        procedure.append("必须显式检查手续费、点差、滑点、市场冲击、延迟、未成交和数据偏差。")
    if task_id == "P37-A-Q08":
        procedure.append("必须区分 signal、decision 和 execution event，不得把信号直接当作订单执行结果。")
    if task_id == "P37-A-Q10":
        procedure.append("必须区分样本内结果、样本外证据和 CEK-TA 默认指导治理要求。")
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": procedure,
        "examples": [],
        "anti_patterns": [
            "把单一指标当作交易系统质量证明。",
            "忽略成本、执行、样本外验证或数据偏差就声明可复用盈利能力。",
            "把 reviewed/caveat_only 知识说成 approved 默认指导。",
        ],
        "validation": [
            "source_evidence 非空，且来源类型覆盖定义、成本、执行或回测边界中的相关维度。",
            "conflict_status 只能是 none、resolved 或 none_known_in_visible_context。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
        ],
        "risk_notes": risk_notes,
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": {
            "source": as_list(deep_get(decision, ("required_patches", "source"), [])),
            "content": as_list(deep_get(decision, ("required_patches", "content"), [])),
            "boundary": as_list(deep_get(decision, ("required_patches", "boundary"), [])),
            "conflict": as_list(deep_get(decision, ("required_patches", "conflict"), [])),
        },
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    sources = merge_sources(candidate)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    tree_node_id = str(classification.get("tree_node_id", ""))
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    decision_log = [
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "decision": "accepted_for_reviewed_caveat_only",
            "reason": decision.get("reasons", [""])[0],
        },
        {
            "at": TODAY,
            "actor": "codex",
            "decision": "reviewed",
            "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default guidance/hard gate all disabled.",
        },
    ]
    claim_type = str(classification.get("claim_type") or "methodological_constraint")
    if str(candidate.get("research_task_id")) == "P37-A-Q12":
        claim_type = "cost_audit_boundary_rule"
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id", "KB_01_QUANT_FOUNDATION"),
            "domain": classification.get("domain", "quant_trading"),
            "subdomain": classification.get("subdomain", "quant_foundation"),
            "rule_type": classification.get("rule_type", "principle"),
            "claim_type": claim_type,
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Quant Foundation"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Quant Foundation"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Quant Foundation formal reviewed/caveat_only；这是 Trading Engineering 规则本体，"
                "不是 AI Engineering 训练/RAG/MCP 本体规则，也不是 approved/default guidance。"
            ),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": shape_content(candidate, decision),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source) for source in sources],
        "source_quality": shape_source_quality(candidate, sources, decision),
        "conflict_audit": {
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status"), "none_known_in_visible_context"),
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": "reviewed/caveat_only preparation audit passed for this item; full formal KB conflict coverage remains a runtime validation concern.",
            "default_recommendation": "caveat_only_until_human_approval",
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计交易工程基础概念和边界。",
                "用于提示用户补充成本、样本、执行、风险和验证条件。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源和边界。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得绕过外接项目事实层、风控 hard gate 或人工治理流程。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate 和不适用场景。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: reviewed-preparation audit allowed formal reviewed/caveat_only only; no approved/default/hard gate.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": decision.get("confidence", review.get("confidence", "medium")),
            "freshness": review.get("freshness", "stable"),
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": candidate.get("candidate_id"),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_patches": decision.get("required_patches", {}),
                "required_extra_sources": decision.get("required_extra_sources", []),
            },
            "open_questions": [],
            "decision_log": decision_log,
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "phase37_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": TASK_ID,
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }


def write_knowledge(item: dict[str, Any]) -> Path:
    path = KNOWLEDGE_ROOT / str(item["metadata"]["partition_id"]) / sanitize_filename(str(item["knowledge_id"]))
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def update_candidate_formalized(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, decision: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval_if_default_guidance_is_needed",
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "knowledge_path": rel(knowledge_path),
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_patches": decision.get("required_patches", {}),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_quant_foundation_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
            }
        )


def update_candidate_needs_more(candidate: dict[str, Any], decision: dict[str, Any], meta: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = meta["reason"]
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
            "next_action": meta["next_action"],
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    review = candidate.setdefault("review", {})
    review["confidence"] = meta["confidence"]
    review["open_questions"] = dedupe_strings(as_list(review.get("open_questions")) + meta["required_followups"])
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_followups": meta["required_followups"],
        "reason": meta["reason"],
    }
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "reviewed-preparation 审计未通过；补证前不得 formal reviewed、approved、default guidance 或 hard gate。"
    machine_gate["requires_human_escalation"] = True
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_quant_foundation_reviewed_preparation_needs_more_evidence",
                "reason": f"{TASK_ID}: {meta['reason']}",
            }
        )


def main() -> int:
    audit_result = build_audit_result()
    write_json(AUDIT_RESULT_PATH, audit_result)
    candidates = load_candidates()
    promoted: list[dict[str, Any]] = []
    needs_more: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    skipped = Counter()

    decisions_by_task = {decision["research_task_id"]: decision for decision in audit_result["decisions"]}
    for task_id, decision in sorted(decisions_by_task.items()):
        if task_id not in candidates:
            skipped["candidate_missing"] += 1
            continue
        candidate_path, candidate = candidates[task_id]
        if task_id in ACCEPTED_TASKS:
            reason = validate_candidate_for_reviewed(candidate)
            if reason:
                skipped[reason] += 1
                continue
            item = candidate_to_knowledge(candidate, decision)
            knowledge_path = write_knowledge(item)
            update_candidate_formalized(candidate, item, knowledge_path, decision)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            written_knowledge_paths.append(rel(knowledge_path))
            promoted.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "knowledge_id": item["knowledge_id"],
                    "knowledge_path": rel(knowledge_path),
                    "canonical_node_id": item["metadata"]["canonical_node_id"],
                    "review_status": "reviewed",
                    "machine_gate": "caveat_only",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                }
            )
        else:
            meta = NEEDS_MORE_TASKS[task_id]
            update_candidate_needs_more(candidate, decision, meta)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            needs_more.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "decision": "needs_more_evidence",
                    "reason": meta["reason"],
                    "next_action": meta["next_action"],
                    "required_followups": meta["required_followups"],
                }
            )

    if len(promoted) != EXPECTED_PROMOTED:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} promoted items, got {len(promoted)}; skipped={dict(skipped)}")
    if len(needs_more) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"Expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {len(needs_more)}")

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase37_quant_foundation_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "skipped": dict(skipped),
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate. Three candidates remain needs_more_evidence.",
        "next_action": "重建 knowledge_items/UI fixture，执行运行时联动验证；Q02/Q06/Q11 按补证要求进入 CEK-TA-381。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
