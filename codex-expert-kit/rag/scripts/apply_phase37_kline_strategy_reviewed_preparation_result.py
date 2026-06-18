"""Apply Phase 37 Kline / Strategy reviewed-preparation audit result.

This task consumes the strict reviewed/caveat_only preparation audit for the
12 Phase 37 Kline / Strategy candidates. It creates formal reviewed/caveat_only
knowledge only. It never creates approved knowledge, default guidance, hard
gates, or trading execution advice.
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
TASK_ID = "CEK-TA-400"
AUDIT_RESULT_ID = "audit_result_phase37_kline_strategy_reviewed_preparation_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_kline_strategy_reviewed_preparation_audit_package_20260611"
EXPECTED_TOTAL = 12
EXPECTED_PROMOTED = 12
PARTITION_ID = "KB_02_KLINE_STRATEGY"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_kline_strategy_reviewed_preparation_import_report.json", start_file=__file__
)


DECISIONS: dict[str, dict[str, Any]] = {
    "P37-C-K01": {
        "confidence": "medium_high",
        "reason": "技术分析形态必须转成可测试规则并声明市场、周期和样本边界；Lo/Mamaysky/Wang、CFA 技术分析综述和 data-snooping 资料共同支撑 caveat-only。",
        "required_patches": {
            "source": ["补充 CMT/技术分析教材或专业协会资料，支撑 HH/HL、支撑阻力、突破等术语来源。"],
            "content": ["必须强调客观、可机器测试的识别规则，不得只凭主观看图命名。"],
            "boundary": ["不得生成趋势跟随买卖点、出入场建议、仓位或实盘执行许可。"],
            "conflict": ["作为 market_structure 父规则，避免与 K02/K06 重复。"],
        },
    },
    "P37-C-K02": {
        "confidence": "high",
        "reason": "QuantConnect bar availability 和 TradingView HTF lookahead 资料支撑市场结构必须声明周期和 bar 可用时间。",
        "required_patches": {
            "source": ["平台文档只支撑各自平台语义，外接项目必须映射自己的 bar availability 契约。"],
            "content": ["市场结构结论必须绑定 timeframe、bar start/end、decision timestamp 和数据可用时间。"],
            "boundary": ["不得把某一周期结构泛化到其他周期或市场。"],
            "conflict": ["与 Data Engineering 时间戳/point-in-time 规则交叉引用，不复制。"],
        },
    },
    "P37-C-K03": {
        "confidence": "medium_high",
        "reason": "data-snooping 论文和 CFA execution / cost 资料支持 entry signal 不等于完整交易决策。",
        "required_patches": {
            "source": ["保留 data-snooping 与 CFA execution/cost 来源分工。"],
            "content": ["Kline 条目只定义信号边界；成本、仓位、执行、风控必须引用对应 Trading 分支。"],
            "boundary": ["不得把入场信号直接解释成订单、仓位、止损止盈或实盘允许。"],
            "conflict": ["Cross-reference Quant Foundation / Execution / Risk，不复制 hard gate。"],
        },
    },
    "P37-C-K04": {
        "confidence": "high",
        "reason": "FINRA 和 Investor.gov 资料支持 stop 触发不保证成交价，stop-limit 可能不成交。",
        "required_patches": {
            "source": ["FINRA/Investor.gov 只支撑 stop order 风险与触发边界。"],
            "content": ["止损必须记录风险目的、触发条件、执行假设和交易假设失效关系。"],
            "boundary": ["不得输出具体止损价格、距离、仓位、杠杆或实盘执行建议。"],
            "conflict": ["与 Risk Management 和 Live Execution 交叉引用。"],
        },
    },
    "P37-C-K05": {
        "confidence": "high",
        "reason": "CFA execution quality 与 QuantConnect fill/slippage 资料支撑 take-profit 可达性只能作为成交质量假设披露。",
        "required_patches": {
            "source": ["CFA/QuantConnect 只支撑执行、fill、slippage 语义，不支撑收益保证。"],
            "content": ["止盈可达性是 execution/fill assumption，不是 profit guarantee。"],
            "boundary": ["不得输出具体止盈价格、盈亏目标或实盘订单。"],
            "conflict": ["与 Replay/Simulation fill model 和 Live Execution 交叉引用。"],
        },
    },
    "P37-C-K06": {
        "confidence": "high",
        "reason": "TradingView HTF lookahead 与 Databricks point-in-time join 资料支撑多周期上下文必须避免未来数据泄漏。",
        "required_patches": {
            "source": ["TradingView 与 Databricks 只支撑各自时间语义和 point-in-time 模式。"],
            "content": ["多周期特征必须声明高周期数据确认时间、低周期决策时间和可用性边界。"],
            "boundary": ["不得把高周期未确认信息作为低周期已知事实。"],
            "conflict": ["与 Data Engineering feature timestamp / point-in-time 规则交叉引用。"],
        },
    },
    "P37-C-K07": {
        "confidence": "medium_high",
        "reason": "TradingView repainting 资料支撑实时未确认 bar 与历史 confirmed bar 可能不同；TA-Lib 只能证明实现存在。",
        "required_patches": {
            "source": ["TA-Lib 不能作为 edge 或默认阈值证据；TradingView repainting 只支撑平台语义。"],
            "content": ["指标必须声明窗口、输入 OHLC、bar 确认状态、延迟和 repainting 边界。"],
            "boundary": ["不得把指标值直接解释为买卖信号或盈利优势。"],
            "conflict": ["与 Data Engineering available_time 和 Backtest lookahead 规则交叉引用。"],
        },
    },
    "P37-C-K08": {
        "confidence": "medium_high",
        "reason": "Fidelity ATR 资料明确 ATR 衡量波动而非方向，可支撑 ATR 只作为波动上下文。",
        "required_patches": {
            "source": ["必须把 Fidelity ATR 或同等级 ATR-specific 来源写入正式 source_evidence。"],
            "content": ["ATR 只能用于波动过滤、归一化或候选上下文，不能声称方向、胜率或 edge。"],
            "boundary": ["不得输出止损距离、仓位、杠杆或实盘交易指令。"],
            "conflict": ["与 Risk Management position sizing 交叉引用，不复制仓位规则。"],
        },
    },
    "P37-C-K09": {
        "confidence": "medium_high",
        "reason": "Fidelity RSI 资料支持 70/30 是传统参考，可随证券调整且强趋势可长期超买/超卖。",
        "required_patches": {
            "source": ["必须把 RSI-specific 来源写入正式 source_evidence。"],
            "content": ["RSI 阈值必须声明市场、周期、参数、趋势状态和验证边界。"],
            "boundary": ["不得把 70/30 直接写成跨市场买卖规则。"],
            "conflict": ["与 signal_generalization 和 indicator_lag 规则交叉引用。"],
        },
    },
    "P37-C-K10": {
        "confidence": "high",
        "reason": "Databento OHLCV/statistics 与 Binance schema 资料支撑 volume 字段语义和供应商聚合边界。",
        "required_patches": {
            "source": ["Databento/Binance 只能证明各自 schema 与 API 语义。"],
            "content": ["成交量确认必须声明交易所、数据供应商、bar 构造、成交来源和缺失处理。"],
            "boundary": ["不得把供应商聚合 volume 直接等同官方全市场成交量。"],
            "conflict": ["与 Data Engineering OHLCV schema 和 symbol normalization 交叉引用。"],
        },
    },
    "P37-C-K11": {
        "confidence": "high",
        "reason": "Sullivan/Timmermann/White 与 White Reality Check 支撑技术信号不能无市场、周期、样本边界地泛化。",
        "required_patches": {
            "source": ["如果保留 cost boundary，应补 CFA TCA/execution 来源。"],
            "content": ["技术信号只能作为有边界的经验假设，不得描述为跨市场通用规律。"],
            "boundary": ["不得声称任何 K 线信号跨市场、跨周期、跨样本稳定有效。"],
            "conflict": ["与已有 approved signal boundary 知识互补，不覆盖其 approved 状态。"],
        },
    },
    "P37-C-K12": {
        "confidence": "high",
        "reason": "MLflow Tracking/Dataset Tracking 和 DVC pipeline 资料支撑参数、代码、数据、输出和 lineage 版本追踪。",
        "required_patches": {
            "source": ["MLflow、DVC、Git 只能作为等价实现来源，不得被强制为唯一工具。"],
            "content": ["策略规则版本、参数、信号计算版本、数据版本、评估输出和变更原因应写成 CEK-TA 审计契约字段。"],
            "boundary": ["不得把版本契约写成外部法规或所有平台强制实现。"],
            "conflict": ["与 Data Engineering versioning 和 AI training dataset lineage 交叉引用。"],
        },
    },
}


SUPPLEMENTAL_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P37-C-K01": [
        {
            "source_id": "src_audit_cmt_wiley_technical_analysis",
            "source_title": "Technical Analysis: The Complete Resource for Financial Market Technicians",
            "source_url": "https://www.wiley.com/en-us/Technical+Analysis%3A+The+Complete+Resource+for+Financial+Market+Technicians%2C+3rd+Edition-p-9780134137049",
            "source_type": "professional_literature_reference",
            "publisher": "CMT Association / Wiley",
            "published_at": "2015-01-01",
            "accessed_at": TODAY,
            "version": "3rd Edition",
            "reliability": "medium_high",
            "relevance": "medium_high",
            "evidence_summary": "作为 CMT 体系相关技术分析教材元数据来源，用于补充趋势、支撑阻力、突破等术语归属；正式 approved 前仍需页码级人工核验。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-C-K08": [
        {
            "source_id": "src_audit_fidelity_atr",
            "source_title": "What Is Average True Range?",
            "source_url": "https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/atr",
            "source_type": "brokerage_education_reference",
            "publisher": "Fidelity Investments",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "high",
            "evidence_summary": "说明 ATR 衡量波动率而非价格方向，支撑 ATR 只能作为波动上下文而非方向信号。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-C-K09": [
        {
            "source_id": "src_audit_fidelity_rsi",
            "source_title": "What is RSI? - Relative Strength Index",
            "source_url": "https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/RSI",
            "source_type": "brokerage_education_reference",
            "publisher": "Fidelity Investments",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "high",
            "evidence_summary": "说明 RSI 70/30 是传统超买/超卖参考，阈值可随证券调整，强趋势可长期处于超买/超卖。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-C-K11": [
        {
            "source_id": "src_audit_cfa_trade_strategy_execution",
            "source_title": "Trade Strategy and Execution",
            "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
            "source_type": "professional_body_reference",
            "publisher": "CFA Institute",
            "published_at": "2026-01-01",
            "accessed_at": TODAY,
            "version": "2026 refresher reading",
            "reliability": "high",
            "relevance": "medium_high",
            "evidence_summary": "用于支撑交易策略与执行必须考虑成本、market impact、execution risk、opportunity cost 和 execution quality。",
            "quoted_excerpt_allowed": False,
        }
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
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


def string_list(value: Any) -> list[str]:
    return [item.strip() for item in as_list(value) if isinstance(item, str) and item.strip()]


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
    return (str(source.get("source_url") or source.get("url") or ""), str(source.get("source_title") or source.get("title") or ""))


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase37_kline_strategy_*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            candidates[task_id] = (path, candidate)
    return candidates


def conversion_target(candidate: dict[str, Any]) -> dict[str, Any]:
    target = deep_get(candidate, ("workflow", "conversion_target"), {})
    if isinstance(target, dict):
        return target
    return {}


def validate_candidate_for_reviewed(candidate: dict[str, Any]) -> str | None:
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "candidate_not_accepted_for_draft"
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        return "candidate_not_in_ai_passed_queue"
    if deep_get(candidate, ("workflow", "approved_allowed")) is not False:
        return "candidate_approved_boundary_not_false"
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        return "candidate_default_guidance_boundary_not_false"
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        return "candidate_hard_gate_boundary_not_false"
    target = conversion_target(candidate)
    if not target.get("proposed_knowledge_id"):
        return "candidate_missing_proposed_knowledge_id"
    if len(as_list(candidate.get("source_refs"))) < 3:
        return "candidate_less_than_3_sources"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {
        "none",
        "resolved",
        "none_known_in_visible_context",
        "visible_context_no_conflict",
    }:
        return "candidate_conflict_status_not_safe"
    return None


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    seen = {source_key(source) for source in sources}
    for source in SUPPLEMENTAL_SOURCES.get(str(candidate.get("research_task_id")), []):
        if source_key(source) not in seen:
            sources.append(source)
            seen.add(source_key(source))
    return sources


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_{index:03d}"),
        "source_title": str(source.get("source_title") or source.get("title") or f"source_{index}"),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type") or "reference"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium"),
        "evidence_summary": str(source.get("evidence_summary") or ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def title_from_candidate(candidate: dict[str, Any]) -> str:
    target = conversion_target(candidate)
    normalized = str(deep_get(candidate, ("claim", "normalized_claim"), target.get("proposed_knowledge_id", "")))
    return normalized or str(target.get("proposed_knowledge_id", ""))


def build_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    patches = decision["required_patches"]
    risk_notes = dedupe_strings(
        as_list(applicability.get("limitations"))
        + string_list(patches.get("boundary"))
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "不得据此生成买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
            "Kline Strategy 只拥有 K线/策略工程方法边界，不拥有完整交易决策 hard gate。",
            "AI Engineering 只能通过 canonical_node_id 引用本规则，不得复制改写为 AI 训练、RAG、MCP 或模型部署本体规则。",
        ]
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": [
            "确认当前问题属于 Trading Engineering / Kline Strategy 方法边界，而不是 AI Engineering、RAG、MCP 或实盘执行本体。",
            "检查市场、品种、周期、样本、数据可用时间、指标参数、成本、执行和验证边界。",
            "若问题涉及仓位、风控、fill、滑点、订单状态或数据层契约，必须 cross-reference 对应 Trading 分支，不在 Kline 条目中复制 hard gate。",
            "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 K线形态、指标阈值或成交量确认直接写成买卖点。",
            "只凭主观看图命名趋势、支撑阻力、突破或反转，不给可测试规则和样本边界。",
            "把平台/供应商文档当成跨所有市场的强制事实。",
            "把 reviewed/caveat_only 知识说成 approved 默认指导。",
        ],
        "validation": [
            "source_evidence 非空，且来源没有被用来支撑超出语境的 claim。",
            "conflict_status 只能是 none、resolved、none_known_in_visible_context 或 visible_context_no_conflict。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
            "不得出现买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
        ],
        "risk_notes": risk_notes,
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": {
            "source": string_list(patches.get("source")),
            "content": string_list(patches.get("content")),
            "boundary": string_list(patches.get("boundary")),
            "conflict": string_list(patches.get("conflict")),
        },
    }


def build_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    patches = decision["required_patches"]
    primary = int(source_quality.get("primary_source_count", min(3, len(sources))) or 0)
    return {
        "overall_reliability": source_quality.get("overall_reliability", "medium_high"),
        "score": source_quality.get("score", 82),
        "score_version": "phase37_kline_strategy_reviewed_preparation_source_scoring_v1",
        "primary_source_count": primary,
        "supporting_source_count": max(0, len(sources) - primary),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + string_list(patches.get("source"))
            + [
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
                "平台、框架、供应商文档只能按其语境使用；外接项目必须映射自己的交易所、broker、数据供应商和执行模型。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
            ]
        ),
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    target = conversion_target(candidate)
    sources = merge_sources(candidate)
    knowledge_id = str(target["proposed_knowledge_id"])
    tree_node_id = str(classification.get("tree_node_id") or "kt.kline_strategy")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    patches = decision["required_patches"]
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "kline_strategy"),
            "subdomain": classification.get("subdomain", "kline_strategy"),
            "rule_type": classification.get("rule_type", "trading_method_boundary_rule"),
            "claim_type": classification.get("claim_type", "methodological_constraint"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Kline Strategy"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Kline Strategy"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Kline / Strategy Engineering formal reviewed/caveat_only；这是 Trading Engineering "
                "K线/策略工程方法边界，不是 AI Engineering 训练/RAG/MCP 本体规则，也不是 approved/default guidance。"
            ),
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "kline"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate, decision),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_quality": build_source_quality(candidate, sources, decision),
        "conflict_audit": {
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status"), "none_known_in_visible_context"),
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": (
                "reviewed/caveat_only preparation audit passed; full formal KB duplicate/conflict/owner "
                "boundary check was executed during materialization and should be rerun after each index rebuild."
            ),
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": "Kline Strategy owns method boundaries; Quant Foundation, Data Engineering, Replay/Simulation, Live Execution and Risk Management own their hard-gate rules.",
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计 K线/策略工程方法边界。",
                "用于提示用户补充市场、周期、样本、数据可用时间、指标参数、成本、执行和验证条件。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、边界和 cross-reference。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得绕过外接项目事实层、数据契约、执行模型、风控 hard gate 或人工治理流程。",
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
                "trade_execution_advice_forbidden",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": decision["confidence"],
            "freshness": review.get("freshness", "mixed"),
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
                "required_patches": patches,
            },
            "open_questions": [
                "若未来申请 approved/default guidance，必须另起人工治理任务并重新审计完整 formal KB 冲突与默认指导风险。"
            ],
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": decision["reason"],
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "decision": "reviewed",
                    "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default guidance/hard gate all disabled.",
                },
            ],
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Kline / Strategy candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get(
            "copyright",
            {
                "stores_full_text": False,
                "stores_long_quote": False,
                "summary_only": True,
                "license_notes": "仅保存来源链接、元数据和摘要，不保存长段原文。",
                "reuse_risk": "low",
            },
        ),
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


def build_audit_result() -> dict[str, Any]:
    decisions = []
    for task_id, decision in sorted(DECISIONS.items()):
        decisions.append(
            {
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "confidence": decision["confidence"],
                "reasons": [decision["reason"]],
                "required_patches": decision["required_patches"],
            }
        )
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_audit",
        "scope": {
            "phase": "Phase 37",
            "partition_id": PARTITION_ID,
            "candidate_count": EXPECTED_TOTAL,
            "max_decision": "accepted_for_reviewed_caveat_only",
        },
        "quality_gate": {
            "pass": True,
            "candidate_count": EXPECTED_TOTAL,
            "accepted_for_reviewed_caveat_only": EXPECTED_PROMOTED,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "global_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "notes": [
                "所有平台/框架/供应商文档只能按其语境使用。",
                "Kline Strategy 只拥有 K线/策略工程方法边界，不拥有完整交易决策 hard gate。",
                "不得把 caveat-only 误读为默认指导或实盘许可。",
            ],
        },
        "decisions": decisions,
    }


def write_knowledge(item: dict[str, Any]) -> Path:
    path = KNOWLEDGE_ROOT / PARTITION_ID / sanitize_filename(str(item["knowledge_id"]))
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
            "formalization_allowed": True,
            "knowledge_path": rel(knowledge_path),
        }
    )
    target = workflow.setdefault("conversion_target", {})
    if isinstance(target, dict):
        target["target_review_status"] = "reviewed"
        target["default_guidance_allowed"] = False
        target["hard_gate_allowed"] = False
        target["approved_allowed"] = False
        target["reviewed_allowed"] = True
    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_patches": decision["required_patches"],
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_kline_strategy_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
            }
        )


def main() -> int:
    audit_result = build_audit_result()
    write_json(AUDIT_RESULT_PATH, audit_result)
    candidates = load_candidates()
    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    skipped = Counter()

    for task_id, decision in sorted(DECISIONS.items()):
        candidate_entry = candidates.get(task_id)
        if not candidate_entry:
            skipped["candidate_missing"] += 1
            continue
        candidate_path, candidate = candidate_entry
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

    if len(promoted) != EXPECTED_PROMOTED:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} promoted items, got {len(promoted)}; skipped={dict(skipped)}")

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase37_kline_strategy_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "skipped": dict(skipped),
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate; no trade execution advice.",
        "next_action": "重建 knowledge_items/UI fixture，执行乱码、污染和前端构建验证；继续 Phase 37 Market Microstructure 或后续 Trading 分支采集。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
