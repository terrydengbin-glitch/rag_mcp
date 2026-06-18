"""Apply Phase 37 Live/Risk L03/L10/L11 supplemental reaudit result.

CEK-TA-441 consumes the strict supplemental reaudit result for the three
previously blocked Live Execution / Risk Management candidates. It creates
formal reviewed/caveat_only knowledge only for explicitly allowed items.

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
TASK_ID = "CEK-TA-441"
AUDIT_RESULT_ID = "audit_result_phase37_live_risk_blocked_supplemental_reaudit_20260612_strict_v1"
SOURCE_PACKAGE_ID = "phase37_live_risk_blocked_supplemental_reaudit_package_20260612"

ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_live_risk_blocked_supplemental_import_report.json", start_file=__file__
)


TARGETS = {
    "P37-G-L03": {
        "partition_id": "KB_06_LIVE_EXECUTION",
        "candidate_id": "cand_20260612_phase37_live_risk_position_reconciliation_required_001",
        "title": "position reconciliation required",
        "claim_type": "execution_safety_rule",
        "reason": (
            "position_reconciliation 已覆盖 local/broker/statement/clearing source、"
            "discrepancy_type、mismatch_qty、mismatch_notional、source_priority、stale_source、"
            "unknown_source、reconciliation_action、owner 和 audit_trace。"
        ),
    },
    "P37-G-L10": {
        "partition_id": "KB_07_RISK_MANAGEMENT",
        "candidate_id": "cand_20260612_phase37_live_risk_portfolio_exposure_limit_required_001",
        "title": "portfolio exposure limit required",
        "claim_type": "risk_boundary_rule",
        "reason": (
            "portfolio_exposure_limit 已覆盖 account、strategy、instrument、venue、asset_class、"
            "sector/theme、direction、correlated_group、gross/net/directional exposure、price_source、"
            "price_staleness_status、aggregation_rule、policy_threshold_ref 和 audit_trace。"
        ),
    },
    "P37-G-L11": {
        "partition_id": "KB_07_RISK_MANAGEMENT",
        "candidate_id": "cand_20260612_phase37_live_risk_consecutive_loss_stop_required_001",
        "title": "consecutive loss stop required",
        "claim_type": "risk_boundary_rule",
        "reason": (
            "consecutive_loss_stop_policy 已覆盖 loss_event_basis、time_window_policy_ref、"
            "streak_count_source、reset_condition、freeze_action、manual_review_required、"
            "unlock_process_ref、priority_order_ref，以及与 single_trade_risk、daily_loss、"
            "portfolio_exposure 的交互关系。"
        ),
    },
}


COMMON_PATCH_NOTES = {
    "source": [
        "SEC/CFTC/NIST/CME/FIA/FIX/IBKR/Binance/QuantConnect 只能作为原则、监管/行业要求、venue/broker/platform 语义或 implementation pattern，不得替代 CEK-TA 内部字段契约。"
    ],
    "content": [
        "missing_source、stale、unknown、policy_missing、unresolved 不得静默当作仓位 0、within_policy 或可继续正常交易。"
    ],
    "boundary": [
        "reconciliation_required、review_required、freeze_new_entries_until_project_policy_resolves 只能表示证据/政策状态，不等于 CEK-TA 自动拒单、停机、撤单、解锁或 hard gate。",
        "不得生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
    ],
    "conflict": [
        "Live Execution 拥有真实 API/session、订单、成交、费用、broker/account position truth 和执行日志；Risk Management 拥有 policy、暴露、连续亏损停止和最终风险状态；AI Engineering 只能引用 reason code，不能拥有阈值或执行动作。"
    ],
}


def embedded_audit_result() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "quality_gate": {
            "pass": True,
            "candidate_count": 3,
            "notes": [
                "L03/L10/L11 三条全部 accepted_for_reviewed_caveat_only。",
                "所有非 reviewed 权限必须关闭：approved=false、default_guidance=false、hard_gate=false、risk_threshold_advice=false。",
            ],
        },
        "summary": {
            "total": 3,
            "accepted_for_reviewed_caveat_only": 3,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": target["candidate_id"],
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": "high",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": [target["reason"]],
                "required_followups": [
                    "正式 materialize reviewed/caveat_only 前仍需完整 CEK-TA formal KB 冲突、重复和 owner 边界检查。",
                    "保留内部契约是字段本体主来源；外部监管、broker、venue、platform 和行业资料仅作 supporting source 或 implementation pattern。",
                ],
                "patch_notes": COMMON_PATCH_NOTES,
            }
            for task_id, target in TARGETS.items()
        ],
        "strict_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
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


def patch_notes(result: dict[str, Any]) -> dict[str, list[str]]:
    raw = result.get("patch_notes")
    if not isinstance(raw, dict):
        return {"source": [], "content": [], "boundary": [], "conflict": []}
    return {
        "source": string_list(raw.get("source")),
        "content": string_list(raw.get("content")),
        "boundary": string_list(raw.get("boundary")),
        "conflict": string_list(raw.get("conflict")),
    }


def title_from_candidate(candidate: dict[str, Any]) -> str:
    title = str(deep_get(candidate, ("claim", "title"), "")).strip()
    if title:
        return title
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:120] if statement else str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), ""))


def candidate_path(target: dict[str, Any]) -> Path:
    return resolve_repo_path(
        "codex-expert-kit", "rag", "candidates", target["partition_id"], f"{target['candidate_id']}.json", start_file=__file__
    )


def knowledge_dir(partition_id: str) -> Path:
    return resolve_repo_path("codex-expert-kit", "rag", "knowledge", partition_id, start_file=__file__)


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    results = audit.get("candidate_results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain candidate_results list.")
    if len(results) != 3:
        raise ValueError(f"expected 3 results, got {len(results)}")
    counts = Counter(str(item.get("decision")) for item in results if isinstance(item, dict))
    if counts != {"accepted_for_reviewed_caveat_only": 3}:
        raise ValueError(f"expected 3 accepted_for_reviewed_caveat_only, got {dict(counts)}")
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("candidate_results must contain objects.")
        task_id = str(result.get("research_task_id") or "")
        expected = TARGETS.get(task_id)
        if not expected:
            raise ValueError(f"Unexpected task_id: {task_id}")
        if result.get("candidate_id") != expected["candidate_id"]:
            raise ValueError(f"{task_id}: candidate_id mismatch")
        for key, expected_value in {
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }.items():
            if result.get(key) is not expected_value:
                raise ValueError(f"{task_id}: {key} must be {expected_value}.")
    return results


def validate_candidate(candidate: dict[str, Any]) -> str | None:
    if deep_get(candidate, ("status", "ingestion_decision")) != "ready_for_reaudit":
        return "candidate_not_ready_for_reaudit"
    if deep_get(candidate, ("workflow", "stage")) != "supplemented_for_contract_reaudit":
        return "candidate_not_supplemented_for_contract_reaudit"
    if deep_get(candidate, ("workflow", "approved_allowed")) is not False:
        return "candidate_approved_boundary_not_false"
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        return "candidate_default_guidance_boundary_not_false"
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        return "candidate_hard_gate_boundary_not_false"
    if deep_get(candidate, ("workflow", "risk_threshold_advice_allowed")) is not False:
        return "candidate_risk_threshold_boundary_not_false"
    if deep_get(candidate, ("workflow", "hidden_from_default_queue")) is not True:
        return "candidate_hidden_from_default_queue_not_true"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "candidate_missing_proposed_knowledge_id"
    if len(as_list(candidate.get("source_refs"))) < 3:
        return "candidate_less_than_3_sources"
    return None


def build_content(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    patches = patch_notes(result)
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "normalized_claim": claim.get("normalized_claim"),
        "claim_strength": "reviewed_caveat_only",
        "performance_claim": False,
        "procedure": [
            "确认问题属于 Trading Engineering / Live Execution 或 Risk Management 的实盘执行、仓位对账、风险政策、组合暴露或连续亏损停止边界。",
            "检查 broker、venue、account_scope、order_type、risk_policy_id、permission_scope、position_source、price_source、policy_threshold_ref 和 audit_trace_id。",
            "若涉及风险阈值、拒单、停机、撤单、解锁或恢复动作，必须由外接项目正式 risk policy / execution system owner 决定。",
            "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 missing_source、stale、unknown、policy_missing 或 unresolved 静默当作仓位 0、within_policy 或可继续正常交易。",
            "把 reconciliation_required、review_required 或 freeze_new_entries_until_project_policy_resolves 解释成 CEK-TA 自动拒单、停机、撤单、解锁或 hard gate。",
            "由 AI Engineering、LLM 或 scoring 模型拥有风险阈值、最终风险状态或执行动作。",
            "把 reviewed/caveat_only 写成 approved 默认指导。",
            "输出买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
        ],
        "validation": [
            "source_evidence 非空，且内部契约是字段本体主来源。",
            "必须保留 broker、venue、platform、监管、行业资料只能作为 supporting source 或 implementation pattern 的限制。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
            "不得出现买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
        ],
        "risk_notes": dedupe_strings(
            as_list(applicability.get("limitations"))
            + patches["content"]
            + patches["boundary"]
            + [
                "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导、hard gate 或风险阈值建议。",
                "Live Execution 拥有真实 API/session、订单、成交、费用、broker/account position truth 和执行日志；Risk Management 拥有 policy、暴露、连续亏损停止和最终风险状态。",
            ]
        ),
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": patches,
    }


def build_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]], result: dict[str, Any]) -> dict[str, Any]:
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    patches = patch_notes(result)
    primary = int(source_quality.get("primary_source_count", min(3, len(sources))) or 0)
    return {
        "overall_reliability": source_quality.get("overall_reliability", "medium_high"),
        "score": source_quality.get("score", 84),
        "score_version": "phase37_live_risk_blocked_supplemental_reviewed_source_scoring_v1",
        "primary_source_count": primary,
        "supporting_source_count": max(0, len(sources) - primary),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + patches["source"]
            + [
                "CEK-TA Live/Risk 内部契约是字段本体主来源；SEC/CFTC/NIST/CME/FIA/FIX/IBKR/Binance/QuantConnect 仅作 supporting source 或 implementation pattern。",
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导、hard gate 或风险阈值建议。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
            ]
        ),
    }


def build_formal_knowledge(candidate: dict[str, Any], result: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    sources = merge_sources(candidate)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    tree_node_id = str(classification.get("tree_node_id") or "kt.live_execution")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    patches = patch_notes(result)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": target["partition_id"],
            "domain": classification.get("domain", "live_risk"),
            "subdomain": classification.get("subdomain", "live_risk"),
            "rule_type": classification.get("rule_type", "live_risk_boundary_rule"),
            "claim_type": target["claim_type"],
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Live Execution / Risk Management"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get(
                "tree_path", "CEK-TA / Trading Engineering / Live Execution / Risk Management"
            ),
            "risk_level": "high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Live Execution / Risk Management blocked supplemental formal reviewed/caveat_only；"
                "这是 Trading Engineering 实盘执行与风控边界，不是 AI Engineering 模型训练规则，"
                "也不是 approved/default guidance/hard gate/risk threshold advice。"
            ),
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_broker_venue_specific_mapping"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "live_or_paper_to_live_readiness"),
            "data_granularity": applicability.get("data_granularity", "orders_fills_positions_account_risk_events"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate, result),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_quality": build_source_quality(candidate, sources, result),
        "conflict_audit": {
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status"), "none_known_in_visible_context"),
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": (
                "supplemental reviewed/caveat_only audit passed for this item; full formal KB duplicate/conflict/owner "
                "boundary check should be rerun after each index rebuild."
            ),
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": (
                "Live Execution owns real API/session/order/fill/fee/broker/account position truth and execution logs; "
                "Risk Management owns policy, exposure, consecutive-loss stop and final risk state; AI Engineering can cite reason codes only."
            ),
            "audit_conflict_patches": patches["conflict"],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计实盘执行、仓位对账、组合暴露、连续亏损停止、风控 owner 和执行安全边界。",
                "用于提示用户补充 broker、venue、account_scope、order_type、risk_policy_id、permission_scope、position_source、price_source、policy_threshold_ref 和 audit_trace_id。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、边界和 cross-reference。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、实盘订单或风险阈值数值。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得把 reconciliation_required、review_required 或 freeze_new_entries_until_project_policy_resolves 解释成自动拒单、停机、撤单、解锁或 hard gate。",
                "不得让 AI Engineering、LLM 或 scoring 模型拥有阈值、最终风险状态或执行动作。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate、不适用场景和 owner 边界。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
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
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Live/Risk candidate; no project-private account facts, keys, thresholds or trading parameters included.",
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


def write_knowledge(item: dict[str, Any], partition_id: str) -> Path:
    folder = knowledge_dir(partition_id)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / sanitize_filename(str(item["knowledge_id"]))
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
        "patch_notes": patch_notes(result),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_live_risk_blocked_supplemental_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def main() -> int:
    audit_result = embedded_audit_result()
    write_json(AUDIT_RESULT_ARCHIVE_PATH, audit_result)
    results = validate_audit(audit_result)

    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    failures: list[str] = []

    for result in sorted(results, key=lambda item: str(item.get("research_task_id", ""))):
        task_id = str(result.get("research_task_id", ""))
        target = TARGETS[task_id]
        path = candidate_path(target)
        candidate = read_json(path)
        validation_error = validate_candidate(candidate)
        if validation_error:
            failures.append(f"{task_id}: {validation_error}")
            continue
        item = build_formal_knowledge(candidate, result, target)
        knowledge_path = write_knowledge(item, target["partition_id"])
        update_candidate_formalized(candidate, item, knowledge_path, result)
        write_json(path, candidate)
        touched_candidates.append(rel(path))
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
                "risk_threshold_advice_allowed": False,
            }
        )

    if failures:
        raise SystemExit(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))
    if len(promoted) != 3:
        raise ValueError(f"Expected 3 promoted items, got {len(promoted)}")

    report = {
        "report_id": "phase37_live_risk_blocked_supplemental_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "source_quality_gate_pass": bool(deep_get(audit_result, ("quality_gate", "pass"), False)),
        "decision_counts": dict(Counter(str(item.get("decision")) for item in results)),
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
        "next_action": "重建正式知识索引、Vue3 fixture，并执行 Phase 37 运行时联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
