"""Apply Phase 37 Replay / Simulation R02/R10/R12 supplemental reaudit result.

CEK-TA-433 consumes the strict supplemental reaudit result for the three
previously blocked Replay / Simulation candidates. It creates formal
reviewed/caveat_only knowledge only for explicitly allowed items.

It never creates approved knowledge, default guidance, hard gates, or trading
execution advice.
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
TASK_ID = "CEK-TA-433"
AUDIT_RESULT_ID = "audit_result_phase37_replay_simulation_blocked_supplemental_reaudit_20260612_strict_v1"
SOURCE_PACKAGE_ID = "phase37_replay_simulation_blocked_supplemental_reaudit_package_20260612"
PARTITION_ID = "KB_05_REPLAY_SIMULATION"

ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION_ID, start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_replay_simulation_blocked_supplemental_import_report.json", start_file=__file__
)


TARGETS = {
    "P37-F-R02": {
        "candidate_id": "cand_20260611_phase37_replay_simulation_ohlc_same_bar_tp_sl_ordering_required_001",
        "title": "OHLC same-bar TP/SL ordering",
        "reason": (
            "same_bar_fill_ordering 已定义 tick_replay、conservative、optimistic、next_bar_only、"
            "unknown_ordering_blocked 的字段、owner、验证规则和 hard boundary。"
        ),
    },
    "P37-F-R10": {
        "candidate_id": "cand_20260611_phase37_replay_simulation_simulation_live_gap_report_required_001",
        "title": "simulation-live gap report",
        "reason": (
            "simulation_live_gap_report 已覆盖 fill price、fill qty、fee、slippage、latency delta、"
            "reject/cancel delta、order state delta、risk trigger delta、缺失字段和 gap classification。"
        ),
    },
    "P37-F-R12": {
        "candidate_id": "cand_20260611_phase37_replay_simulation_execution_cost_consistency_required_001",
        "title": "execution cost consistency",
        "reason": (
            "execution_cost_mapping 已覆盖 Backtest、Replay、Paper、Live 之间 fee、spread、slippage、"
            "market impact、fill model 的版本映射与 owner 边界。"
        ),
    },
}


COMMON_PATCH_NOTES = {
    "source": [
        "Backtrader、HftBacktest、QuantConnect、FIX、IBKR 等只能作为 implementation pattern 或 supporting source，不得替代 CEK-TA 内部字段契约，也不得写成所有市场通用规则。"
    ],
    "content": [
        "unknown_ordering_blocked、invalidates_simulation_evidence、unresolved 只能表示模拟证据不可用于执行质量或可交易性证明，不能被机器解释成自动拒单、停机或风控 hard gate。"
    ],
    "boundary": [
        "formal reviewed/caveat_only 不代表策略有效，不代表实盘许可，不进入 default guidance queue，也不得生成任何交易参数。",
        "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
    ],
    "conflict": [
        "Replay / Simulation 只负责模拟假设、差异审计和证据边界；真实订单、真实成交、真实拒单、账户同步、真实费用和风控动作仍归 Live Execution / Risk Management owner。"
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
                "R02/R10/R12 三条全部 accepted_for_reviewed_caveat_only。",
                "所有非 reviewed 权限必须关闭：approved=false、default_guidance=false、hard_gate=false。",
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
                "reasons": [target["reason"]],
                "required_followups": [
                    "正式 materialize reviewed/caveat_only 前仍需完整 CEK-TA formal KB 冲突、重复和 owner 边界检查。",
                    "保留 vendor/framework/exchange/broker/FIX 文档只能作为 supporting source 或 implementation pattern 的限制。",
                ],
                "patch_notes": COMMON_PATCH_NOTES,
            }
            for task_id, target in TARGETS.items()
        ],
        "strict_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
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
        if result.get("reviewed_allowed") is not True:
            raise ValueError(f"{task_id}: reviewed_allowed must be true.")
        if result.get("approved_allowed") is not False:
            raise ValueError(f"{task_id}: approved_allowed must be false.")
        if result.get("default_guidance_allowed") is not False:
            raise ValueError(f"{task_id}: default_guidance_allowed must be false.")
        if result.get("hard_gate_allowed") is not False:
            raise ValueError(f"{task_id}: hard_gate_allowed must be false.")
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
            "确认问题属于 Trading Engineering / Replay Simulation 的回放、模拟、成交模型、延迟或订单状态边界。",
            "检查 market、venue、instrument、data_granularity、event_clock、order_type、fill_model_version、latency_model_version、exchange_rule_version 和 execution_cost_mapping。",
            "若涉及真实下单、真实拒单、账户同步、实盘订单状态或风控 hard gate，必须 cross-reference Live Execution / Risk Management owner。",
            "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 simulation/paper 通过解释成 live execution permission。",
            "把 unknown_ordering_blocked、invalidates_simulation_evidence 或 unresolved 解释成自动拒单、停机或风控 hard gate。",
            "把未声明事件顺序的模拟结果当作执行质量或策略可交易性证据。",
            "把具体框架、broker、FIX 或交易所语义泛化为所有市场通用规则。",
            "把 reviewed/caveat_only 写成 approved 默认指导。",
        ],
        "validation": [
            "source_evidence 非空，且来源没有被用来支撑超出语境的 claim。",
            "必须保留 CEK-TA 内部契约 source 作为字段本体主来源。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
            "不得出现买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
        ],
        "risk_notes": dedupe_strings(
            as_list(applicability.get("limitations"))
            + patches["content"]
            + patches["boundary"]
            + [
                "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
                "Replay / Simulation 只负责模拟假设、差异审计和证据边界；真实订单、真实成交、真实拒单、账户同步、真实费用和风控动作仍归 Live Execution / Risk Management owner。",
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
        "score": source_quality.get("score", 82),
        "score_version": "phase37_replay_simulation_blocked_supplemental_reviewed_source_scoring_v1",
        "primary_source_count": primary,
        "supporting_source_count": max(0, len(sources) - primary),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + patches["source"]
            + [
                "CEK-TA Replay / Simulation 内部契约是字段本体主来源；外部框架、平台、FIX 或 broker 文档只作为 implementation pattern 或 supporting source。",
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
            ]
        ),
    }


def build_formal_knowledge(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    sources = merge_sources(candidate)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    tree_node_id = str(classification.get("tree_node_id") or "kt.replay_simulation")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    patches = patch_notes(result)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "replay_simulation"),
            "subdomain": classification.get("subdomain", "replay_simulation"),
            "rule_type": classification.get("rule_type", "replay_simulation_boundary_rule"),
            "claim_type": classification.get("claim_type", "methodological_constraint"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Replay Simulation"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Replay Simulation"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Replay / Simulation blocked supplemental formal reviewed/caveat_only；这是 Trading Engineering "
                "回放与模拟方法边界，不是 Backtest、Live Execution、Risk Management 或 AI Engineering 本体规则，也不是 approved/default guidance。"
            ),
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_venue_specific_mapping"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "historical_replay_or_paper_simulation"),
            "data_granularity": applicability.get("data_granularity", "ohlc_tick_quote_order_book_and_order_events"),
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
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": "Replay / Simulation owns simulated assumptions, gap reports and evidence boundaries; Live Execution and Risk Management own real order routing, real fills, account state and hard-gate actions.",
            "audit_conflict_patches": patches["conflict"],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计 replay、simulation、paper trading、fill model、latency model、same-bar ordering、gap report 和 execution cost mapping 边界。",
                "用于提示用户补充 market、venue、instrument、data_granularity、event_clock、order_type、fill_model_version、latency_model_version、exchange_rule_version 和 cost mapping。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、边界和 cross-reference。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈参数或实盘订单。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得把 paper/simulation 通过解释成 live execution permission。",
                "不得把 unknown_ordering_blocked、invalidates_simulation_evidence 或 unresolved 解释成自动拒单、停机或风控 hard gate。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate 和不适用场景。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: supplemental audit allowed formal reviewed/caveat_only only; no approved/default/hard gate.",
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
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": result.get("confidence", "high"),
            "freshness": "stable",
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
                    "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default guidance/hard gate all disabled.",
                },
            ],
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Replay / Simulation candidate; no project-private trading facts included.",
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
    status["decision_reason"] = "补证再审允许 formal reviewed/caveat_only；不允许 approved/default guidance/hard gate。"
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
            "next_action": "request_human_approval_if_default_guidance_is_needed",
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
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

    review = candidate.setdefault("review", {})
    review["reviewed_preparation_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
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
                "action": "phase37_replay_simulation_blocked_supplemental_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def main() -> int:
    audit_result = embedded_audit_result()
    write_json(AUDIT_RESULT_ARCHIVE_PATH, audit_result)
    results = validate_audit(audit_result)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    failures: list[str] = []

    for result in sorted(results, key=lambda item: str(item.get("research_task_id", ""))):
        task_id = str(result.get("research_task_id", ""))
        candidate_path = CANDIDATE_DIR / f"{TARGETS[task_id]['candidate_id']}.json"
        candidate = read_json(candidate_path)
        validation_error = validate_candidate(candidate)
        if validation_error:
            failures.append(f"{task_id}: {validation_error}")
            continue
        item = build_formal_knowledge(candidate, result)
        knowledge_path = write_knowledge(item)
        update_candidate_formalized(candidate, item, knowledge_path, result)
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

    if failures:
        raise SystemExit(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))
    if len(promoted) != 3:
        raise ValueError(f"Expected 3 promoted items, got {len(promoted)}")

    report = {
        "report_id": "phase37_replay_simulation_blocked_supplemental_import_report",
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
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate.",
        "next_action": "重建正式知识索引、Vue3 fixture，并执行 CEK-TA-431 运行时联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
