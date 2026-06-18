"""Apply Phase 37 Market Microstructure M07 liquidity regime reaudit result.

This script materializes only P37-D-M07 as formal reviewed/caveat_only after
the supplemental strict audit accepted it. It never creates approved knowledge,
default guidance, hard gates, or trading execution advice.
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
TASK_ID = "CEK-TA-411"
PARTITION_ID = "KB_03_MARKET_MICROSTRUCTURE"
RESEARCH_TASK_ID = "P37-D-M07"
CANDIDATE_ID = "cand_20260611_phase37_market_microstructure_liquidity_regime_required_001"
AUDIT_RESULT_ID = "audit_result_phase37_market_microstructure_m07_liquidity_regime_reaudit_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_market_microstructure_m07_liquidity_regime_reaudit_package_20260611"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", PARTITION_ID, f"{CANDIDATE_ID}.json", start_file=__file__
)
KNOWLEDGE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "knowledge",
    PARTITION_ID,
    "kb_03_market_microstructure.liquidity_regime_required.v1.json",
    start_file=__file__,
)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_m07_liquidity_regime_reaudit_import_report.json", start_file=__file__
)


PATCH_NOTES = {
    "source": [
        "NYSE / Nasdaq / CME / Databento 只能证明各自 venue、product、dataset 或 schema 的语义，不能泛化为所有市场。",
        "外接项目如果使用 crypto perpetuals、非美股票、其他期货品类、期权或外汇，必须补对应交易所的 session calendar、market status、contract spec、expiry/roll rule。",
    ],
    "content": [
        "normal_continuous、pre_open_or_open_auction、closing_auction_or_close、holiday_or_early_close、halt_pause_reopen、rollover_or_expiry、stressed_liquidity、thin_or_off_hours 必须写成 CEK-TA internal liquidity regime labels，不是外部通用标准。",
        "每个 regime 标签至少应带 market、venue、instrument、session_timezone、regime_start_time、regime_end_time、evidence_source_id、calendar_or_status_version 和 confidence。",
    ],
    "boundary": [
        "本条只能约束解释、分层回测、特征适用范围、审计和人工/风控复核上下文。",
        "不得从 liquidity regime 标签生成买卖点、仓位、杠杆、止损止盈或交易许可。",
        "真正的拒单、阻断或自动风控只能由外接项目的 Risk Management / Live Execution owner 定义。",
    ],
    "conflict": [
        "正式 materialize reviewed/caveat_only 前仍需完整 KB 冲突、重复和 owner 边界检查。",
        "与 M11 thin market execution risk、Execution/Risk owner 边界只 cross-reference，不覆盖其阻断权限。",
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


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dedupe_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
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


def normalize_source(source: dict[str, Any], index: int) -> dict[str, Any]:
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


def audit_result_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "quality_gate": {
            "pass": True,
            "reason": "M07 supplemental evidence accepted; reviewed/caveat_only only.",
        },
        "summary": {
            "total": 1,
            "accepted_for_reviewed_caveat_only": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "results": [
            {
                "candidate_id": CANDIDATE_ID,
                "research_task_id": RESEARCH_TASK_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": "high",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "patch_notes": PATCH_NOTES,
                "reason": (
                    "NYSE、Nasdaq、CME、Databento 的直接来源覆盖 session、auction、halt/pause/reopen、holiday/early-close、"
                    "expiration/rollover 和 vendor market-status schema，可支撑 CEK-TA 内部 liquidity regime taxonomy 的 caveat-only 知识。"
                ),
            }
        ],
        "global_notes": [
            "本审计不创建 approved/default guidance/hard gate。",
            "所有 regime labels 是 CEK-TA internal labels，不是外部通用标准。",
            "本条不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        ],
        "source_candidate_snapshot": {
            "candidate_id": candidate.get("candidate_id"),
            "source_count": len(as_list(candidate.get("source_refs"))),
            "taxonomy_contract_id": candidate.get("supplemental_contracts", {})
            .get("liquidity_regime_taxonomy", {})
            .get("contract_id"),
        },
    }


def validate_candidate(candidate: dict[str, Any]) -> None:
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError(f"Unexpected candidate_id: {candidate.get('candidate_id')}")
    if candidate.get("research_task_id") != RESEARCH_TASK_ID:
        raise ValueError(f"Unexpected research_task_id: {candidate.get('research_task_id')}")
    if len(as_list(candidate.get("source_refs"))) < 8:
        raise ValueError("M07 candidate must have at least 8 sources after supplement.")
    taxonomy = candidate.get("supplemental_contracts", {}).get("liquidity_regime_taxonomy")
    if not isinstance(taxonomy, dict) or taxonomy.get("contract_id") != "cek_ta_liquidity_regime_taxonomy_v1":
        raise ValueError("M07 candidate missing liquidity regime taxonomy contract.")


def build_content(candidate: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    taxonomy = candidate.get("supplemental_contracts", {}).get("liquidity_regime_taxonomy", {})
    labels = taxonomy.get("regime_labels", []) if isinstance(taxonomy, dict) else []
    risk_notes = dedupe_strings(
        as_list(applicability.get("limitations"))
        + PATCH_NOTES["boundary"]
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "CEK-TA liquidity regime taxonomy 是内部逻辑标签，不是外部通用标准。",
            "外接项目必须映射自己的交易所、broker、数据供应商、合约规格和交易日历。",
            "Risk Management / Live Execution 才拥有真正拒单、阻断和自动风控 owner 权限。",
        ]
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "liquidity_regime_taxonomy": taxonomy,
        "regime_label_summary": [
            {
                "label": item.get("label"),
                "meaning": item.get("meaning"),
                "required_evidence": item.get("required_evidence", []),
            }
            for item in labels
            if isinstance(item, dict)
        ],
        "procedure": [
            "确认当前 market、venue、instrument、session_timezone、数据源、market status 和合约生命周期上下文。",
            "将样本或实时上下文映射到 CEK-TA internal liquidity regime labels。",
            "为每个 regime 记录 regime_start_time、regime_end_time、evidence_source_id、calendar_or_status_version 和 confidence。",
            "若 regime 触发执行风险，只能交给 Risk Management / Live Execution owner 决定是否降级、复核或阻断。",
        ],
        "anti_patterns": [
            "把正常连续交易时段的盘口、滑点或订单流统计外推到 auction、halt、holiday、rollover 或 thin/off-hours。",
            "把 NYSE/Nasdaq/CME/Databento 字段名当成所有市场的通用字段。",
            "把 liquidity regime 标签直接写成买卖点、仓位、杠杆或实盘执行许可。",
        ],
        "validation": [
            "source_evidence 必须覆盖 session、auction/halt、holiday/early-close、expiration/rollover 和 market-status schema。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
            "hidden_from_default_queue 必须为 true，visible_in_default_guidance_queue 必须为 false。",
            "不得出现买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
        ],
        "risk_notes": risk_notes,
        "audit_patch_notes": PATCH_NOTES,
    }


def candidate_to_knowledge(candidate: dict[str, Any], audit_result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    workflow = candidate.get("workflow") if isinstance(candidate.get("workflow"), dict) else {}
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    knowledge_id = str(conversion.get("proposed_knowledge_id") or "kb_03_market_microstructure.liquidity_regime_required.v1")
    if sanitize_filename(knowledge_id) != KNOWLEDGE_PATH.name:
        raise ValueError(f"Unexpected knowledge_id filename mapping: {knowledge_id}")
    tree_node_id = str(classification.get("tree_node_id") or "kt.market_microstructure")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(candidate.get("claim", {}).get("title") or "流动性状态必须按 regime 标注"),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "market_microstructure"),
            "subdomain": classification.get("subdomain", "liquidity_regime"),
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
            "research_task_id": RESEARCH_TASK_ID,
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Market Microstructure formal reviewed/caveat_only；liquidity regime taxonomy 是 CEK-TA internal labels，"
                "不是外部通用标准，也不是 approved/default guidance。"
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
        "content": build_content(candidate),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [normalize_source(source, index) for index, source in enumerate(sources, start=1)],
        "source_quality": {
            "overall_reliability": candidate.get("source_quality", {}).get("overall_reliability", "medium_high"),
            "score": candidate.get("source_quality", {}).get("score", 89.0),
            "score_version": "phase37_market_microstructure_m07_reaudit_source_scoring_v1",
            "primary_source_count": candidate.get("source_quality", {}).get("primary_source_count", 8),
            "supporting_source_count": candidate.get("source_quality", {}).get("supporting_source_count", 4),
            "low_reliability_source_count": candidate.get("source_quality", {}).get("low_reliability_source_count", 0),
            "limitations": dedupe_strings(as_list(candidate.get("source_quality", {}).get("limitations")) + PATCH_NOTES["source"]),
        },
        "conflict_audit": {
            "conflict_status": candidate.get("conflict_audit", {}).get("conflict_status", "none_known_in_visible_context"),
            "checked_against": as_list(candidate.get("conflict_audit", {}).get("checked_against")),
            "conflicts": as_list(candidate.get("conflict_audit", {}).get("conflicts")),
            "resolution_summary": (
                "M07 supplemental strict reaudit accepted formal reviewed/caveat_only. Complete formal KB duplicate/conflict "
                "and owner boundary validation must be rerun after index rebuild."
            ),
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": "Market Microstructure owns liquidity regime caveat labels; Risk Management and Live Execution own reject/block/automation decisions.",
            "audit_conflict_patches": PATCH_NOTES["conflict"],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计市场微观结构 regime 边界。",
                "用于提示用户补充 session calendar、market status、contract expiry/roll、holiday/early-close、auction/halt 证据。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、边界和 cross-reference。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得把 CEK-TA internal liquidity regime labels 当成外部通用标准。",
                "不得绕过 Risk Management / Live Execution owner 的拒单、阻断或自动风控规则。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate 和不适用场景。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: supplemental strict audit allowed formal reviewed/caveat_only only; no approved/default/hard gate.",
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
        "review": {
            "confidence": "high",
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
            "source_candidate_id": CANDIDATE_ID,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": audit_result["results"][0],
            "open_questions": [
                "若未来申请 approved/default guidance，必须另起人工治理任务并重新审计完整 formal KB 冲突与默认指导风险。"
            ],
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": audit_result["results"][0]["reason"],
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


def update_candidate_formalized(candidate: dict[str, Any], item: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
    status["decision_reason"] = "P37-D-M07 补证严格再审通过，可进入 formal reviewed/caveat_only；不得 approved/default/hard gate。"
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "current_task_id": TASK_ID,
            "next_action": "phase37_market_microstructure_runtime_linkage_validation",
            "next_allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "forbidden_decisions": [
                "approved",
                "default_guidance",
                "hard_gate",
                "trade_execution_advice",
            ],
            "formalization_allowed": True,
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "knowledge_path": rel(KNOWLEDGE_PATH),
        }
    )
    conversion = workflow.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "reviewed"
        conversion["reviewed_allowed"] = True
        conversion["approved_allowed"] = False
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate.update(
        {
            "default_guidance": "caveat_only",
            "reason": "P37-D-M07 补证再审通过，但仅允许 formal reviewed/caveat_only；不得 approved/default/hard gate。",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    review = candidate.setdefault("review", {})
    review["ai_audit"] = audit_result_payload(candidate)["results"][0]
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_market_microstructure_m07_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(KNOWLEDGE_PATH)}.",
            }
        )


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    validate_candidate(candidate)
    audit_result = audit_result_payload(candidate)
    write_json(AUDIT_RESULT_PATH, audit_result)
    item = candidate_to_knowledge(candidate, audit_result)
    if KNOWLEDGE_PATH.exists():
        existing = read_json(KNOWLEDGE_PATH)
        if existing.get("review", {}).get("review_status") == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(KNOWLEDGE_PATH)}")
    write_json(KNOWLEDGE_PATH, item)
    update_candidate_formalized(candidate, item)
    write_json(CANDIDATE_PATH, candidate)
    report = {
        "report_id": "phase37_market_microstructure_m07_liquidity_regime_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "candidate_id": CANDIDATE_ID,
        "research_task_id": RESEARCH_TASK_ID,
        "promoted_count": 1,
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "knowledge_id": item["knowledge_id"],
        "knowledge_path": rel(KNOWLEDGE_PATH),
        "candidate_path": rel(CANDIDATE_PATH),
        "machine_gate": "caveat_only",
        "hidden_from_default_queue": True,
        "visible_in_default_guidance_queue": False,
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate; no trade execution advice.",
        "next_action": "重建 knowledge_items/UI fixture，执行 CEK-TA-409 MCP/SearchLab/KnowledgeTree/Vue3 联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
