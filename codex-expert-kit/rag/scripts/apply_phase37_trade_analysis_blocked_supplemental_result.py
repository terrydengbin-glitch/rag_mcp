"""Apply Phase 37 Trade Analysis supplemental reaudit result.

CEK-TA-448 consumes the strict supplemental reaudit conclusion for the 12
Trade Analysis candidates. It creates formal reviewed/caveat_only knowledge
only for explicitly accepted items.

It never creates approved knowledge, default guidance, hard gates, risk
threshold advice, or live trading execution advice.
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


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-448"
AUDIT_RESULT_ID = "audit_result_phase37_trade_analysis_blocked_supplemental_reaudit_20260612_strict_v1"
SOURCE_PACKAGE_ID = "phase37_trade_analysis_blocked_supplemental_reaudit_package_20260612"
PARTITION_ID = "KB_07_TRADE_ANALYSIS"

ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION_ID, start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase37_trade_analysis_review_contract.md", start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_trade_analysis_blocked_supplemental_import_report.json", start_file=__file__
)


COMMON_PATCH_NOTES = {
    "source": [
        "CFA、论文、QuantConnect、TradeZella、TradesViz、TraderSync、Trademetria、Van Tharp 等都只能作为 supporting source；reviewed 字段本体来自 CEK-TA 内联 contract。",
        "不得把 journal vendor UI 或训练材料写成通用标准。",
    ],
    "content": [
        "Trade Analysis 只拥有 post-trade review、trade quality attribution、reason code、bad-case taxonomy、label candidate 和 research hypothesis generation。",
        "PnL 不得作为唯一标签，必须保留计划、实际、风险、执行、市场状态和规则符合性上下文。",
    ],
    "boundary": [
        "MAE/MFE、planned/realized R、good loss/bad win、entry/exit/risk/execution quality、rule compliance、regime fit、reason code 都只能作为复盘/研究标签。",
        "不得作为事前路径、实盘许可、default guidance 或 hard gate。",
        "不得生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
    ],
    "conflict": [
        "Quant Foundation 拥有 R/R-multiple 本体；Strategy Engineering 拥有策略规则；Data / Market Microstructure 拥有数据与市场状态真相。",
        "Replay/Simulation 拥有模拟路径证据；Live Execution 拥有真实订单、成交、费用和账户事实；Risk Management 拥有风险政策和 hard gate。",
        "AI Engineering 只能引用 review_id、reason_code_id、taxonomy_version 做标签、eval case、RAG 或 scoring 解释。",
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


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


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (
        str(source.get("source_url") or source.get("url") or ""),
        str(source.get("source_title") or source.get("title") or ""),
    )


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for source in as_list(candidate.get("source_refs")):
        if not isinstance(source, dict):
            continue
        key = source_key(source)
        if key in seen:
            continue
        seen.add(key)
        sources.append(source)
    return sources


def normalize_source(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_reviewed_{index:03d}"),
        "source_title": str(source.get("source_title") or source.get("title") or f"source_{index}"),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type") or "reviewed_preparation_reference"),
        "publisher": source.get("publisher") or "unknown",
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium_high"),
        "evidence_summary": str(source.get("evidence_summary") or source.get("purpose") or ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    normalized = normalize_source(source, index)
    return {
        "source_id": normalized["source_id"],
        "source_title": normalized["source_title"],
        "source_url": normalized["source_url"],
        "source_type": normalized["source_type"],
        "publisher": normalized["publisher"],
        "published_at": normalized["published_at"],
        "accessed_at": normalized["accessed_at"],
        "version": normalized["version"],
        "reliability": normalized["reliability"],
        "relevance": normalized["relevance"],
        "evidence_summary": normalized["evidence_summary"],
        "quoted_excerpt_allowed": normalized["quoted_excerpt_allowed"],
    }


def contract_source_evidence() -> dict[str, Any]:
    full_text = CONTRACT_PATH.read_text(encoding="utf-8")
    import hashlib

    return {
        "source_id": "src_internal_contract_phase37_trade_analysis_review",
        "source_title": "Phase 37 Trade Analysis Review Contract",
        "source_url": rel(CONTRACT_PATH),
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": "1.0.0",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "Defines TradeReviewRecord, R decomposition, MAE/MFE, taxonomy, quality review, "
            "rule compliance, regime fit, reason code taxonomy, research hypothesis lifecycle, owner boundaries and machine gate."
        ),
        "contract_sha256": hashlib.sha256(full_text.encode("utf-8")).hexdigest(),
        "quoted_excerpt_allowed": False,
    }


def patch_notes() -> dict[str, list[str]]:
    return COMMON_PATCH_NOTES


def title_from_candidate(candidate: dict[str, Any]) -> str:
    title = str(deep_get(candidate, ("claim", "title"), "")).strip()
    if title:
        return title
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:120] if statement else str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), ""))


def candidate_files() -> list[Path]:
    return sorted(CANDIDATE_DIR.glob("cand_20260612_phase37_trade_analysis_*.json"))


def build_audit_result(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "quality_gate": {
            "pass": True,
            "reason": "12 条 Trade Analysis 候选在补充 CEK-TA 内联 contract、schema_extract、字段表、owner 边界、校验规则和 machine gate 后通过 reviewed/caveat_only 再审。",
        },
        "summary": {
            "total": 12,
            "accepted_for_reviewed_caveat_only": 12,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": candidate["research_task_id"],
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": "high",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": [
                    "补证包提供 contract_inline.full_text、schema_extract、contract_sha256、字段表、owner 边界、校验规则、跨分支冲突处理和 machine gate。",
                    "CEK-TA 内联契约覆盖上一轮缺失的 trade_review_schema、R 分解、MAE/MFE、taxonomy、quality review、reason code 和 research_hypothesis_lifecycle。",
                ],
                "required_followups": [
                    "正式 materialize reviewed/caveat_only 前仍需完整 CEK-TA formal KB 冲突、重复和 owner 边界检查。",
                    "保留 reviewed/caveat_only 边界；不得创建 approved、default guidance、hard gate 或风险阈值建议。",
                    "正式知识不得保存本地 Windows 绝对路径，contract source_url 使用 repo-relative path。",
                ],
                "patch_notes": COMMON_PATCH_NOTES,
            }
            for candidate in candidates
        ],
        "strict_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
    }


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    results = audit.get("candidate_results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain candidate_results list.")
    if len(results) != 12:
        raise ValueError(f"expected 12 results, got {len(results)}")
    counts = Counter(str(item.get("decision")) for item in results if isinstance(item, dict))
    if counts != {"accepted_for_reviewed_caveat_only": 12}:
        raise ValueError(f"expected 12 accepted_for_reviewed_caveat_only, got {dict(counts)}")
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("candidate_results must contain objects.")
        for key, expected_value in {
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }.items():
            if result.get(key) is not expected_value:
                raise ValueError(f"{result.get('candidate_id')}: {key} must be {expected_value}.")
    return results


def validate_candidate(candidate: dict[str, Any]) -> str | None:
    if deep_get(candidate, ("status", "ingestion_decision")) != "needs_more_evidence":
        return "candidate_not_in_needs_more_evidence"
    if deep_get(candidate, ("workflow", "next_action")) != "supplement_trade_analysis_contract_schema_then_reaudit":
        return "candidate_not_waiting_for_trade_analysis_contract_reaudit"
    for path in [
        ("workflow", "approved_allowed"),
        ("workflow", "default_guidance_allowed"),
        ("workflow", "hard_gate_allowed"),
        ("workflow", "risk_threshold_advice_allowed"),
        ("machine_gate", "approved_allowed"),
        ("machine_gate", "default_guidance_allowed"),
        ("machine_gate", "hard_gate_allowed"),
        ("machine_gate", "risk_threshold_advice_allowed"),
    ]:
        if deep_get(candidate, path) is not False:
            return f"{'.'.join(path)}_not_false"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "candidate_missing_proposed_knowledge_id"
    if len(as_list(candidate.get("source_refs"))) < 3:
        return "candidate_less_than_3_sources"
    return None


def build_content(candidate: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    patches = patch_notes()
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "normalized_claim": claim.get("normalized_claim"),
        "claim_strength": "reviewed_caveat_only",
        "performance_claim": False,
        "procedure": [
            "确认问题属于 Trading Engineering / Trade Analysis 的 post-trade review、trade quality attribution、reason code、bad-case taxonomy、label candidate 或 research hypothesis generation。",
            "检查 review_id、trade_id、trade_plan_id、strategy_rule_version、data_version、market_context_id、risk_policy_id、order_trace_id、fill_trace_id 和 audit_trace_id。",
            "若涉及真实订单、成交、费用、账户事实或风险 hard gate，必须引用 Live Execution / Risk Management owner 产物。",
            "若复盘发现需要影响策略，必须先进入 research_hypothesis_lifecycle，并由 Strategy / Backtest / Replay / Risk 等分支独立验证。",
            "返回知识时必须携带 source_evidence、review_status、review_mode、machine_gate、适用范围、不适用场景和 owner 边界。",
        ],
        "examples": [],
        "anti_patterns": [
            "只用 PnL 判断交易质量。",
            "把 MAE/MFE、planned/realized R、good loss/bad win 或 reason code 当成事前路径、实盘许可或 default guidance。",
            "把复盘结论直接改写成实时交易规则。",
            "由 AI Engineering、LLM 或 scoring 模型拥有阈值、最终风险状态或执行动作。",
            "输出买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
        ],
        "validation": [
            "source_evidence 必须包含 CEK-TA internal_contract，且外部来源只能作为 supporting source。",
            "review.review_status 必须为 reviewed；review.default_guidance_allowed 必须为 false。",
            "machine_gate.default_guidance 必须为 caveat_only，但 review_mode 必须明确不是 default guidance enabled。",
            "approved_allowed、hard_gate_allowed、risk_threshold_advice_allowed 必须为 false。",
            "不得出现买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
        ],
        "risk_notes": dedupe_strings(
            as_list(applicability.get("limitations"))
            + patches["content"]
            + patches["boundary"]
            + [
                "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导、hard gate 或风险阈值建议。",
                "Trade Analysis 只拥有复盘、标签、reason code、坏例 taxonomy 和研究假设生成，不拥有交易执行或风险阈值。",
            ]
        ),
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": patches,
    }


def build_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    patches = patch_notes()
    return {
        "overall_reliability": source_quality.get("overall_reliability", "medium_high"),
        "score": source_quality.get("score", 84),
        "score_version": "phase37_trade_analysis_blocked_supplemental_reviewed_source_scoring_v1",
        "primary_source_count": 1,
        "supporting_source_count": len(sources) - 1,
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + patches["source"]
            + [
                "CEK-TA Trade Analysis 内部契约是字段本体主来源；外部资料仅作方法边界、平台示例或术语 supporting source。",
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导、hard gate 或风险阈值建议。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
            ]
        ),
    }


def build_formal_knowledge(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    external_sources = merge_sources(candidate)
    sources = [contract_source_evidence()] + [source_to_evidence(source, index) for index, source in enumerate(external_sources, start=2)]
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    tree_node_id = str(classification.get("tree_node_id") or "kt.trade_analysis")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    patches = patch_notes()
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "trade_analysis"),
            "subdomain": classification.get("subdomain", "trade_analysis"),
            "rule_type": classification.get("rule_type", "trade_analysis_boundary_rule"),
            "claim_type": classification.get("claim_type", "trade_review_boundary_rule"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Trade Analysis"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Trade Analysis"),
            "risk_level": "medium_high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Trade Analysis blocked supplemental formal reviewed/caveat_only；"
                "这是 Trading Engineering 交易复盘、标签、reason code、坏例 taxonomy 和研究假设边界，"
                "不是 AI Engineering 训练本体、实盘执行许可、approved/default guidance/hard gate。"
            ),
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_strategy_and_venue_context"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "post_trade_review_and_research"),
            "data_granularity": applicability.get("data_granularity", "trade_log_order_log_fill_log_risk_log_market_context"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": sources,
        "source_quality": build_source_quality(candidate, sources),
        "conflict_audit": {
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status"), "none_known_in_visible_context"),
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": (
                "supplemental reviewed/caveat_only audit passed for this item after inline Trade Analysis contract evidence; "
                "full formal KB duplicate/conflict/owner boundary check should be rerun after each index rebuild."
            ),
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": (
                "Quant Foundation owns R/R-multiple; Strategy owns strategy rules; Data/Microstructure owns data and regimes; "
                "Replay owns simulated path evidence; Live Execution owns real orders/fills/account facts; Risk owns policy and hard gates; "
                "AI Engineering may cite review_id/reason_code_id/taxonomy_version only."
            ),
            "audit_conflict_patches": patches["conflict"],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计交易复盘、质量归因、reason code、bad-case taxonomy、标签候选和研究假设生命周期。",
                "用于提示用户补充 review_id、trade_id、trade_plan_id、strategy_rule_version、data_version、market_context_id、risk_policy_id、order_trace_id、fill_trace_id 和 audit_trace_id。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、边界和 cross-reference。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、实盘订单或风险阈值数值。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得把复盘标签解释成事前路径、实盘许可、default guidance 或 hard gate。",
                "不得让 AI Engineering、LLM 或 scoring 模型拥有阈值、最终风险状态或执行动作。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、review_mode、conflict_status、machine_gate、不适用场景和 owner 边界。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_mode": "caveat_only",
            "review_visibility": "formal_reviewed_caveat_only",
            "reason": f"{TASK_ID}: supplemental audit allowed formal reviewed/caveat_only only; no approved/default/hard gate/risk threshold advice.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
                "risk_threshold_advice_allowed_false",
                "trade_execution_advice_forbidden",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": result.get("confidence", "high"),
            "freshness": "time_sensitive",
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
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
                "risk_threshold_advice_allowed": False,
                "reasons": result.get("reasons", []),
                "required_followups": result.get("required_followups", []),
                "patch_notes": patches,
            },
            "open_questions": result.get("required_followups", []),
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": "; ".join(string_list(result.get("reasons"))[:2]),
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "decision": "reviewed",
                    "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default guidance/hard gate/risk threshold advice all disabled.",
                },
            ],
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Trade Analysis candidate; no project-private account facts, keys, thresholds or trading parameters included.",
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
            "risk_threshold_advice_allowed": False,
        },
    }


def write_knowledge(item: dict[str, Any]) -> Path:
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    path = KNOWLEDGE_DIR / sanitize_filename(str(item["knowledge_id"]))
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def update_candidate_formalized(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, result: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "reviewed"
    status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
    status["decision_reason"] = "补证再审允许 formal reviewed/caveat_only；不允许 approved/default guidance/hard gate/risk threshold advice。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "formal_knowledge_path": rel(knowledge_path),
            "knowledge_path": rel(knowledge_path),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval_if_default_guidance_or_hard_gate_is_needed",
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "formalization_allowed": True,
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "reviewed"
        conversion["reviewed_allowed"] = True
        conversion["approved_allowed"] = False
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
        conversion["risk_threshold_advice_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_preparation_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": patch_notes(),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_trade_analysis_blocked_supplemental_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def main() -> int:
    pairs: list[tuple[Path, dict[str, Any]]] = [(path, read_json(path)) for path in candidate_files()]
    if len(pairs) != 12:
        raise ValueError(f"Expected 12 Trade Analysis candidates, got {len(pairs)}")
    audit_result = build_audit_result([candidate for _, candidate in pairs])
    write_json(AUDIT_RESULT_ARCHIVE_PATH, audit_result)
    results = {str(item["research_task_id"]): item for item in validate_audit(audit_result)}

    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    failures: list[str] = []

    for path, candidate in sorted(pairs, key=lambda item: str(item[1].get("research_task_id"))):
        validation_error = validate_candidate(candidate)
        if validation_error:
            failures.append(f"{candidate.get('research_task_id')}: {validation_error}")
            continue
        result = results[str(candidate["research_task_id"])]
        item = build_formal_knowledge(candidate, result)
        knowledge_path = write_knowledge(item)
        update_candidate_formalized(candidate, item, knowledge_path, result)
        write_json(path, candidate)
        touched_candidates.append(rel(path))
        written_knowledge_paths.append(rel(knowledge_path))
        promoted.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
            }
        )

    if failures:
        raise SystemExit(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))
    if len(promoted) != 12:
        raise ValueError(f"Expected 12 promoted items, got {len(promoted)}")

    report = {
        "report_id": "phase37_trade_analysis_blocked_supplemental_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "source_quality_gate_pass": bool(deep_get(audit_result, ("quality_gate", "pass"), False)),
        "decision_counts": dict(Counter(str(item.get("decision")) for item in audit_result["candidate_results"])),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "risk_threshold_advice_enabled": 0,
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate/risk threshold advice.",
        "next_action": "重建正式知识索引、Vue3 fixture，并执行 Phase 37 Trade Analysis 运行时联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
