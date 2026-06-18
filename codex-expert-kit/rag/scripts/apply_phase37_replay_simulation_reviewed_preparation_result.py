"""Apply Phase 37 Replay / Simulation reviewed-preparation audit result.

This task consumes the strict reviewed/caveat_only preparation audit for the
12 Phase 37 Replay / Simulation candidates. It creates formal reviewed
knowledge only for items explicitly allowed by the audit. It never creates
approved knowledge, default guidance, hard gates, or trading execution advice.
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


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-430"
AUDIT_RESULT_ID = "audit_result_phase37_replay_simulation_reviewed_preparation_20260612_strict_v1"
SOURCE_PACKAGE_ID = "phase37_replay_simulation_reviewed_preparation_audit_package_20260612"
PARTITION_ID = "KB_05_REPLAY_SIMULATION"
EXPECTED_TOTAL = 12
EXPECTED_PROMOTED = 9
EXPECTED_NEEDS_MORE = 3

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION_ID, start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_replay_simulation_reviewed_preparation_import_report.json", start_file=__file__
)


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
    return (
        str(source.get("source_url") or source.get("url") or ""),
        str(source.get("source_title") or source.get("title") or ""),
    )


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
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase37_replay_simulation_*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            candidates[task_id] = (path, candidate)
    return candidates


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    results = audit.get("candidate_results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain candidate_results list.")
    if len(results) != EXPECTED_TOTAL:
        raise ValueError(f"expected {EXPECTED_TOTAL} results, got {len(results)}")
    counts = Counter(str(item.get("decision")) for item in results if isinstance(item, dict))
    if counts.get("accepted_for_reviewed_caveat_only", 0) != EXPECTED_PROMOTED:
        raise ValueError(f"expected {EXPECTED_PROMOTED} promoted, got {dict(counts)}")
    if counts.get("needs_more_evidence", 0) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {dict(counts)}")
    for result in results:
        if not isinstance(result, dict):
            raise ValueError("candidate_results must contain objects.")
        cid = result.get("candidate_id")
        decision = result.get("decision")
        if decision == "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not True:
            raise ValueError(f"{cid}: reviewed_allowed must be true for promoted item.")
        if decision != "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not False:
            raise ValueError(f"{cid}: reviewed_allowed must be false for non-promoted item.")
        if result.get("approved_allowed") is not False:
            raise ValueError(f"{cid}: approved_allowed must be false.")
        if result.get("default_guidance_allowed") is not False:
            raise ValueError(f"{cid}: default_guidance_allowed must be false.")
        if result.get("hard_gate_allowed") is not False:
            raise ValueError(f"{cid}: hard_gate_allowed must be false.")
    return results


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
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
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


def patch_notes(result: dict[str, Any]) -> dict[str, list[str]]:
    raw = result.get("patch_notes")
    if isinstance(raw, dict):
        return {
            "source": string_list(raw.get("source")),
            "content": string_list(raw.get("content")),
            "boundary": string_list(raw.get("boundary")),
            "conflict": string_list(raw.get("conflict")),
        }
    return {"source": [], "content": [], "boundary": [], "conflict": []}


def title_from_candidate(candidate: dict[str, Any]) -> str:
    title = str(deep_get(candidate, ("claim", "title"), "")).strip()
    if title:
        return title
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:120] if statement else str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), ""))


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
            "检查 market、venue、instrument、data_granularity、event_clock、order_type、fill_model_version、latency_model_version 和 exchange_rule_version。",
            "若涉及真实下单、真实拒单、账户同步、实盘订单状态或风控 hard gate，必须 cross-reference Live Execution / Risk Management owner。",
            "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 simulation/paper 通过解释成 live execution permission。",
            "把未声明事件顺序的模拟结果当作执行质量或策略可交易性证据。",
            "把具体框架、broker 或交易所语义泛化为所有市场通用规则。",
            "把 reviewed/caveat_only 写成 approved 默认指导。",
        ],
        "validation": [
            "source_evidence 非空，且来源没有被用来支撑超出语境的 claim。",
            "conflict_status 只能是 none、resolved、none_known_in_visible_context 或 visible_context_no_conflict。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
            "不得出现买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
        ],
        "risk_notes": dedupe_strings(
            as_list(applicability.get("limitations"))
            + patches["boundary"]
            + [
                "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
                "simulation evidence invalidation 只能表示模拟证据不可作为执行质量或可交易性证据，不能解释为自动拒单、实盘停机或风控 hard gate。",
                "Replay 只模拟规则与状态；真实下单、真实拒单、账户同步、实盘订单状态归 Live Execution owner。",
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
        "score": source_quality.get("score", 80),
        "score_version": "phase37_replay_simulation_reviewed_preparation_source_scoring_v1",
        "primary_source_count": primary,
        "supporting_source_count": max(0, len(sources) - primary),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + patches["source"]
            + [
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
                "Backtrader、QuantConnect、HftBacktest、IBKR、Binance、CME、FIX/OnixS 等只能作为各自框架、平台、交易所、broker 或标准语义来源。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
            ]
        ),
    }


def build_formal_knowledge(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
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
                "Phase 37 Replay / Simulation formal reviewed/caveat_only；这是 Trading Engineering 回放与模拟方法边界，"
                "不是 Backtest、Live Execution、Risk Management 或 AI Engineering 本体规则，也不是 approved/default guidance。"
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
                "reviewed/caveat_only preparation audit passed for this item; full formal KB duplicate/conflict/owner "
                "boundary check should be rerun after each index rebuild."
            ),
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "default_recommendation": "caveat_only_until_human_approval",
            "owner_boundary": "Replay / Simulation owns simulated event/fill/latency/order-state assumptions; Live Execution and Risk Management own real order routing and hard-gate actions.",
            "audit_conflict_patches": patches["conflict"],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计 replay、simulation、paper trading、fill model、latency model 和交易所规则模拟边界。",
                "用于提示用户补充 market、venue、instrument、data_granularity、event_clock、order_type、fill_model_version、latency_model_version 和 exchange_rule_version。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源、边界和 cross-reference。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈参数或实盘订单。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得把 paper/simulation 通过解释成 live execution permission。",
                "不得绕过外接项目事实层、交易所/经纪商规则、Live Execution owner、Risk Management hard gate 或人工治理流程。",
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
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": result.get("confidence", deep_get(review, ("ai_audit", "confidence"), "medium")),
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
    status["decision_reason"] = "reviewed-preparation 审计允许 formal reviewed/caveat_only；不允许 approved/default guidance/hard gate。"
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
                "action": "phase37_replay_simulation_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def update_candidate_needs_more(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = "; ".join(string_list(result.get("reasons"))[:2])
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
            "next_action": "supplement_internal_contract_or_owner_schema_then_reaudit",
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "formalization_allowed": False,
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "blocked_until_supplemented"
        conversion["reviewed_allowed"] = False
        conversion["approved_allowed"] = False
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
    review = candidate.setdefault("review", {})
    review["confidence"] = result.get("confidence", "high")
    patches = patch_notes(result)
    review["open_questions"] = dedupe_strings(
        as_list(review.get("open_questions"))
        + as_list(result.get("required_followups"))
        + patches["source"]
        + patches["content"]
    )
    review["reviewed_preparation_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": patches,
    }
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "reviewed-preparation 审计未通过；补内部契约/schema 前不得 formal reviewed、approved、default guidance 或 hard gate。"
    machine_gate["requires_human_escalation"] = True
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_replay_simulation_reviewed_preparation_needs_more_evidence",
                "reason": f"{TASK_ID}: {status['decision_reason']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def main() -> int:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit_result = archive_audit_result(source_path)
    results = validate_audit(audit_result)
    candidates = load_candidates()
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

    promoted: list[dict[str, Any]] = []
    needs_more: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    failures: list[str] = []

    for result in sorted(results, key=lambda item: str(item.get("research_task_id", ""))):
        task_id = str(result.get("research_task_id", ""))
        candidate_entry = candidates.get(task_id)
        if not candidate_entry:
            failures.append(f"{task_id}: candidate not found")
            continue
        candidate_path, candidate = candidate_entry
        decision = result.get("decision")
        if decision == "accepted_for_reviewed_caveat_only":
            validation_error = validate_candidate_for_reviewed(candidate)
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
        elif decision == "needs_more_evidence":
            update_candidate_needs_more(candidate, result)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            needs_more.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "decision": "needs_more_evidence",
                    "reason": "; ".join(string_list(result.get("reasons"))[:2]),
                    "next_action": "supplement_internal_contract_or_owner_schema_then_reaudit",
                    "required_followups": result.get("required_followups", []),
                    "patch_notes": patch_notes(result),
                }
            )
        else:
            failures.append(f"{task_id}: unsupported decision {decision}")

    if failures:
        raise SystemExit(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))
    if len(promoted) != EXPECTED_PROMOTED:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} promoted items, got {len(promoted)}")
    if len(needs_more) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"Expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {len(needs_more)}")

    report = {
        "report_id": "phase37_replay_simulation_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "source_quality_gate_pass": bool(deep_get(audit_result, ("quality_gate", "pass"), False)),
        "source_quality_gate_reason": deep_get(audit_result, ("quality_gate", "reason")),
        "decision_counts": dict(Counter(str(item.get("decision")) for item in results)),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "boundary": "formal reviewed/caveat_only only for 9 accepted items; R02/R10/R12 remain needs_more_evidence; no approved/default guidance/hard gate.",
        "next_action": "为 R02/R10/R12 补充 same_bar_fill_ordering、simulation_live_gap_report、execution_cost_mapping 内部契约/schema 后再审；9 条 formal reviewed/caveat_only 需重建索引并做运行时联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
