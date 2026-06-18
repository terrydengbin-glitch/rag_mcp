"""Apply Phase 37 Market Microstructure reviewed-preparation audit result.

This task consumes the external reviewed/caveat_only preparation audit for the
12 Phase 37 Market Microstructure candidates. It creates formal
reviewed/caveat_only knowledge only for entries explicitly allowed by the
audit. It never creates approved knowledge, default guidance, hard gates, or
trading execution advice.
"""

from __future__ import annotations

import json
import re
import shutil
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
TASK_ID = "CEK-TA-408"
AUDIT_RESULT_ID = "audit_result_phase37_market_microstructure_reviewed_preparation_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_market_microstructure_reviewed_preparation_audit_package_20260611"
PARTITION_ID = "KB_03_MARKET_MICROSTRUCTURE"
EXPECTED_TOTAL = 12
EXPECTED_PROMOTED = 11
EXPECTED_NEEDS_MORE = 1

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_reviewed_preparation_import_report.json", start_file=__file__
)


SUPPLEMENTAL_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P37-D-M04": [
        {
            "source_id": "src_reviewed_cont_kukanov_stoikov_ofi",
            "source_title": "The Price Impact of Order Book Events",
            "source_url": "https://arxiv.org/abs/1011.6402",
            "source_type": "academic_paper",
            "publisher": "arXiv",
            "published_at": "2010-11-29",
            "accessed_at": TODAY,
            "version": "arXiv:1011.6402",
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "Cont, Kukanov and Stoikov propose order-flow imbalance from limit order book events, supporting OFI/imbalance as a proxy that must declare input events and aggregation assumptions.",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-D-M05": [
        {
            "source_id": "src_reviewed_databento_trade_side_semantics",
            "source_title": "Databento schemas and fields",
            "source_url": "https://databento.com/docs/schemas-and-data-formats/schemas",
            "source_type": "vendor_schema_doc",
            "publisher": "Databento",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "medium_high",
            "evidence_summary": "Vendor schema documentation supports trade side and event-field semantics; it must not be generalized beyond the data source contract.",
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


def archive_audit_result(source_path: Path) -> dict[str, Any]:
    payload = read_json(source_path)
    if payload.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {payload.get('audit_result_id')}")
    if payload.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {payload.get('package_id')}")
    AUDIT_RESULT_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != AUDIT_RESULT_ARCHIVE_PATH.resolve():
        shutil.copyfile(source_path, AUDIT_RESULT_ARCHIVE_PATH)
    else:
        write_json(AUDIT_RESULT_ARCHIVE_PATH, payload)
    return payload


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase37_market_microstructure_*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            candidates[task_id] = (path, candidate)
    return candidates


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
    if deep_get(candidate, ("workflow", "conversion_target", "proposed_knowledge_id")) in (None, ""):
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


def normalize_source(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_audit_extra_{index:03d}"),
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


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    seen = {source_key(source) for source in sources}
    for index, source in enumerate(SUPPLEMENTAL_SOURCES.get(str(candidate.get("research_task_id")), []), start=1):
        normalized = normalize_source(source, index)
        if source_key(normalized) not in seen:
            sources.append(normalized)
            seen.add(source_key(normalized))
    return sources


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    normalized = normalize_source(source, index)
    normalized["source_id"] = str(source.get("source_id") or normalized["source_id"])
    normalized["source_type"] = str(source.get("source_type") or normalized["source_type"])
    normalized["reliability"] = str(source.get("reliability") or normalized["reliability"])
    normalized["relevance"] = str(source.get("relevance") or normalized["relevance"])
    return normalized


def title_from_candidate(candidate: dict[str, Any]) -> str:
    title = str(deep_get(candidate, ("claim", "title"), "")).strip()
    if title:
        return title
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:120] if statement else str(deep_get(candidate, ("workflow", "conversion_target", "proposed_knowledge_id"), ""))


def patch_notes(decision: dict[str, Any]) -> dict[str, list[str]]:
    notes = decision.get("patch_notes")
    if isinstance(notes, dict):
        return {
            "source": string_list(notes.get("source")),
            "content": string_list(notes.get("content")),
            "boundary": string_list(notes.get("boundary")),
            "conflict": string_list(notes.get("conflict")),
        }
    return {"source": [], "content": [], "boundary": [], "conflict": []}


def build_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    patches = patch_notes(decision)
    risk_notes = dedupe_strings(
        as_list(applicability.get("limitations"))
        + patches["boundary"]
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "不得据此生成买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
            "Market Microstructure 只拥有盘口、订单流、流动性、滑点、延迟和市场影响的 caveat 边界；Execution/Risk 分支拥有执行许可和阻断规则。",
            "AI Engineering 只能通过 canonical_node_id 引用本规则，不得复制改写为 AI 训练、RAG、MCP 或模型部署本体规则。",
        ]
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": [
            "确认当前问题属于 Trading Engineering / Market Microstructure 方法边界，而不是 AI Engineering 或实盘执行本体。",
            "检查市场、venue、instrument、数据源、timestamp、session、深度、成交方向、流动性状态、滑点、延迟和市场影响边界。",
            "若问题涉及订单状态、成交、仓位、风险阻断或实盘执行许可，必须 cross-reference Live Execution / Risk Management，不在本条中创建 hard gate。",
            "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
        ],
        "examples": [],
        "anti_patterns": [
            "把盘口、订单流、CVD、OFI、funding/OI 或价差变化直接写成买卖方向。",
            "把单一交易所、供应商、venue 或资产类别的字段语义泛化成全市场事实。",
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
        "audit_patch_notes": patches,
    }


def build_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    patches = patch_notes(decision)
    primary = int(source_quality.get("primary_source_count", min(3, len(sources))) or 0)
    return {
        "overall_reliability": source_quality.get("overall_reliability", "medium_high"),
        "score": source_quality.get("score", 82),
        "score_version": "phase37_market_microstructure_reviewed_preparation_source_scoring_v1",
        "primary_source_count": primary,
        "supporting_source_count": max(0, len(sources) - primary),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + patches["source"]
            + [
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
                "交易所、供应商、broker、监管和论文来源只能按其语境使用；外接项目必须映射自己的 venue、数据契约和执行模型。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
            ]
        ),
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = deep_get(candidate, ("workflow", "conversion_target"), {})
    if not isinstance(conversion, dict):
        conversion = {}
    sources = merge_sources(candidate)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    tree_node_id = str(classification.get("tree_node_id") or "kt.market_microstructure")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    patches = patch_notes(decision)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "market_microstructure"),
            "subdomain": classification.get("subdomain", "market_microstructure"),
            "rule_type": classification.get("rule_type", "trading_microstructure_boundary_rule"),
            "claim_type": classification.get("claim_type", "methodological_constraint"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Market Microstructure"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Market Microstructure"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Market Microstructure formal reviewed/caveat_only；这是 Trading Engineering "
                "市场微观结构方法边界，不是 AI Engineering 训练/RAG/MCP 本体规则，也不是 approved/default guidance。"
            ),
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_market_specific_mapping"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "event_to_intraday"),
            "data_granularity": applicability.get("data_granularity", "order_book_trades_or_derivatives_market_data"),
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
                "reviewed/caveat_only preparation audit passed for this item; full formal KB duplicate/conflict/owner "
                "boundary check should be rerun after each index rebuild."
            ),
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": "Market Microstructure owns caveat boundaries; Live Execution and Risk Management own execution permission and hard-gate rules.",
            "audit_conflict_patches": patches["conflict"],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计市场微观结构方法边界。",
                "用于提示用户补充 venue、instrument、数据源、timestamp、session、深度、成交方向、流动性状态、滑点、延迟和市场影响条件。",
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
            "confidence": decision.get("confidence", review.get("confidence", "medium_high")),
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
                "patch_notes": patches,
                "reason": decision.get("reason"),
            },
            "open_questions": [
                "若未来申请 approved/default guidance，必须另起人工治理任务并重新审计完整 formal KB 冲突与默认指导风险。"
            ],
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": decision.get("reason", ""),
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
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Market Microstructure candidate; no project-private trading facts included.",
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
            "knowledge_path": rel(knowledge_path),
        }
    )
    conversion = workflow.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "reviewed"
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
        conversion["approved_allowed"] = False
        conversion["reviewed_allowed"] = True
    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "patch_notes": patch_notes(decision),
        "reason": decision.get("reason"),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_market_microstructure_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
            }
        )


def update_candidate_needs_more(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = str(decision.get("reason") or "")
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
            "next_action": "supplement_session_calendar_auction_halt_rollover_sources_then_reaudit",
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    conversion = workflow.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "blocked_until_supplemented"
        conversion["reviewed_allowed"] = False
        conversion["approved_allowed"] = False
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
    review = candidate.setdefault("review", {})
    review["confidence"] = decision.get("confidence", "high")
    patches = patch_notes(decision)
    review["open_questions"] = dedupe_strings(
        as_list(review.get("open_questions"))
        + patches["source"]
        + patches["content"]
        + [
            "补齐交易所交易日历、session hours、auction/halts、holiday schedule、contract rollover/expiry 规则或数据供应商 session/market status 文档。",
            "将 normal/thin/stressed/event-driven/rollover/session-specific 明确写成 CEK-TA 内部 liquidity regime taxonomy。",
        ]
    )
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "patch_notes": patches,
        "reason": status["decision_reason"],
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
                "action": "phase37_market_microstructure_reviewed_preparation_needs_more_evidence",
                "reason": f"{TASK_ID}: {status['decision_reason']}",
            }
        )


def main() -> int:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit_result = archive_audit_result(source_path)
    candidates = load_candidates()
    decisions = audit_result.get("results")
    if not isinstance(decisions, list) or len(decisions) != EXPECTED_TOTAL:
        raise ValueError(f"Expected {EXPECTED_TOTAL} audit decisions, got {len(decisions) if isinstance(decisions, list) else 'invalid'}")

    promoted: list[dict[str, Any]] = []
    needs_more: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    skipped = Counter()

    for decision in sorted(decisions, key=lambda item: str(item.get("research_task_id", ""))):
        if not isinstance(decision, dict):
            skipped["invalid_decision"] += 1
            continue
        task_id = str(decision.get("research_task_id", ""))
        candidate_entry = candidates.get(task_id)
        if not candidate_entry:
            skipped["candidate_missing"] += 1
            continue
        candidate_path, candidate = candidate_entry
        decision_value = decision.get("decision")
        if decision_value == "accepted_for_reviewed_caveat_only" and decision.get("reviewed_allowed") is True:
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
        elif decision_value == "needs_more_evidence":
            update_candidate_needs_more(candidate, decision)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            needs_more.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "decision": "needs_more_evidence",
                    "reason": decision.get("reason"),
                    "next_action": "supplement_session_calendar_auction_halt_rollover_sources_then_reaudit",
                    "patch_notes": patch_notes(decision),
                }
            )
        else:
            skipped[f"unsupported_decision_{decision_value}"] += 1

    if len(promoted) != EXPECTED_PROMOTED:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} promoted items, got {len(promoted)}; skipped={dict(skipped)}")
    if len(needs_more) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"Expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {len(needs_more)}")

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase37_market_microstructure_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "source_quality_gate_pass": bool(deep_get(audit_result, ("quality_gate", "pass"), False)),
        "source_quality_gate_reason": deep_get(audit_result, ("quality_gate", "reason")),
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
        "boundary": "formal reviewed/caveat_only only for 11 accepted items; M07 remains needs_more_evidence; no approved/default guidance/hard gate.",
        "next_action": "重建 knowledge_items/UI fixture，执行运行时联动验证；为 P37-D-M07 补充 session/calendar/auction/halt/rollover 证据后再审。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
