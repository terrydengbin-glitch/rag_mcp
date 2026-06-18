"""Apply Phase 37 Live Execution / Risk Management reviewed-preparation audit.

This script imports the strict reviewed/caveat_only preparation audit for the
12 Phase 37 Live/Risk candidates. It creates formal reviewed/caveat_only
knowledge only for the 9 entries explicitly allowed by the audit, and keeps
L03/L10/L11 in the needs_more_evidence queue.
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
TASK_ID = "CEK-TA-439"
AUDIT_RESULT_ID = "audit_result_phase37_live_risk_reviewed_preparation_20260612_strict_v1"
SOURCE_PACKAGE_ID = "phase37_live_risk_reviewed_preparation_audit_package_20260612"
EXPECTED_TOTAL = 12
EXPECTED_PROMOTED = 9
EXPECTED_NEEDS_MORE = 3

CANDIDATE_PARTITIONS = ("KB_06_LIVE_EXECUTION", "KB_07_RISK_MANAGEMENT")
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_live_risk_reviewed_preparation_import_report.json", start_file=__file__
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


def patch_groups(result: dict[str, Any]) -> dict[str, list[str]]:
    raw = result.get("patch_notes")
    groups = {"source": [], "content": [], "boundary": [], "conflict": []}
    if isinstance(raw, dict):
        for key in groups:
            groups[key] = string_list(raw.get(key))
    elif isinstance(raw, list):
        groups["content"] = string_list(raw)
    return groups


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
    for partition in CANDIDATE_PARTITIONS:
        candidate_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        for path in sorted(candidate_dir.glob("cand_20260612_phase37_live_risk_*.json")):
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
            raise ValueError(f"{cid}: reviewed_allowed must be true for accepted reviewed/caveat item.")
        if decision != "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not False:
            raise ValueError(f"{cid}: reviewed_allowed must be false for non-promoted item.")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if result.get(field) is not False:
                raise ValueError(f"{cid}: {field} must be false.")
    return results


def validate_candidate_for_reviewed(candidate: dict[str, Any]) -> str | None:
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "candidate_not_accepted_for_draft"
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        return "candidate_not_in_ai_passed_queue"
    for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
        if deep_get(candidate, ("workflow", field)) is not False:
            return f"candidate_{field}_not_false"
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


def partition_knowledge_dir(candidate: dict[str, Any]) -> Path:
    partition = str(deep_get(candidate, ("classification", "partition_id"), ""))
    if partition not in CANDIDATE_PARTITIONS:
        raise ValueError(f"Unexpected partition for candidate {candidate.get('candidate_id')}: {partition}")
    return resolve_repo_path("codex-expert-kit", "rag", "knowledge", partition, start_file=__file__)


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_reviewed_{index:03d}"),
        "title": str(source.get("source_title") or source.get("title") or f"source_{index}"),
        "url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type") or "reviewed_preparation_reference"),
        "publisher": source.get("publisher") or "unknown",
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium_high"),
        "summary": str(source.get("evidence_summary") or source.get("purpose") or ""),
        "supports": ["claim_statement", "owner_boundary", "non_default_guidance_boundary"],
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def build_formal_knowledge(candidate: dict[str, Any], result: dict[str, Any], global_patches: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    partition = str(classification.get("partition_id"))
    tree_node_id = str(classification.get("tree_node_id") or "kt.live_execution")
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    claim_type = "execution_safety_rule" if partition == "KB_06_LIVE_EXECUTION" else "risk_boundary_rule"
    patches = patch_groups(result)
    global_boundary = string_list(global_patches.get("boundary") if isinstance(global_patches, dict) else [])
    global_source = string_list(global_patches.get("source") if isinstance(global_patches, dict) else [])
    global_content = string_list(global_patches.get("content") if isinstance(global_patches, dict) else [])
    global_conflict = string_list(global_patches.get("conflict") if isinstance(global_patches, dict) else [])
    owner_boundary = (
        "Live Execution owns API permissions, order states, adapter errors, real orders/fills/fees, "
        "position reconciliation and audit logs. Risk Management owns deterministic pre-trade policy, "
        "risk limits, daily loss, portfolio exposure, consecutive-loss policies and kill/stop boundaries."
    )
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(claim.get("title") or knowledge_id),
        "metadata": {
            "partition_id": partition,
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": classification.get("rule_type", "live_risk_boundary_rule"),
            "claim_type": claim_type,
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path"),
            "risk_level": "medium_high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Live Execution / Risk Management formal reviewed/caveat_only。"
                "本条只定义实盘执行或风控治理边界，不是 approved/default guidance，也不启用 hard gate。"
            ),
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market"),
            "asset": applicability.get("asset"),
            "timeframe": applicability.get("timeframe"),
            "data_granularity": applicability.get("data_granularity"),
            "project_type": applicability.get("project_type"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": dedupe_strings(
                as_list(applicability.get("not_applicable_when"))
                + [
                    "需要买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值时不得使用。",
                    "需要实际 hard gate、拒单、停机或资金划转时，必须使用外接项目的正式风控与执行系统配置。",
                ]
            ),
        },
        "content": {
            "statement": claim.get("statement"),
            "rationale": claim.get("interpretation_notes"),
            "normalized_claim": claim.get("normalized_claim"),
            "claim_strength": "reviewed_caveat_only",
            "performance_claim": False,
            "procedure": [
                "确认问题属于 Live Execution 或 Risk Management owner 边界。",
                "检查 broker、venue、account_scope、order_type、risk_policy_id、permission_scope、position_source 和 audit_trace_id。",
                "若涉及阈值、拒单、停机、解锁或真实执行动作，必须交由外接项目 owner 配置，CEK-TA 只提供审计边界。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
            ],
            "anti_patterns": [
                "把 reviewed/caveat_only 写成 approved 默认指导。",
                "把风控边界写成具体阈值、仓位、杠杆、止损止盈或实盘订单建议。",
                "让 AI scoring、Agent 或策略信号绕过 deterministic final gate。",
                "把 broker、venue 或平台文档泛化为所有市场通用规则。",
            ],
            "validation": [
                "source_evidence 非空，且来源没有被用来支撑超出语境的 claim。",
                "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
                "approved_allowed、hard_gate_allowed、risk_threshold_advice_allowed 必须为 false。",
                "不得出现买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
            ],
            "risk_notes": dedupe_strings(
                as_list(applicability.get("limitations"))
                + patches["boundary"]
                + global_boundary
                + [
                    "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或可执行 hard gate。",
                    "风险阈值、账户配置和执行动作必须由外接项目 owner 定义，本知识库不得提供数值或实盘许可。",
                ]
            ),
            "citation_notes": claim.get("evidence_summary"),
            "audit_patch_notes": patches,
            "global_patch_notes": global_patches,
        },
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_refs": sources,
        "source_quality": {
            **(candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}),
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_confidence": result.get("confidence"),
            "limitations": dedupe_strings(
                as_list(deep_get(candidate, ("source_quality", "limitations"), []))
                + patches["source"]
                + global_source
                + [
                    "外部来源只支撑原则、监管/行业要求或具体 venue/broker/platform 语义，不得写成所有市场通用规则。",
                    "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文和本次本地索引检查。",
                ]
            ),
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": (
                "reviewed/caveat_only preparation audit passed for this item; full formal KB duplicate/conflict/owner "
                "boundary check should be rerun after each index rebuild."
            ),
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "owner_boundary": owner_boundary,
            "patch_notes": dedupe_strings(patches["conflict"] + global_conflict),
        },
        "llm_usage_policy": {
            "allowed": as_list(deep_get(candidate, ("llm_usage_policy", "allowed"), [])),
            "not_allowed": dedupe_strings(
                as_list(deep_get(candidate, ("llm_usage_policy", "not_allowed"), []))
                + [
                    "不得作为 approved、默认指导或可执行 hard gate。",
                    "不得生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
                    "不得绕过外接项目 deterministic final gate、Live Execution owner 或 Risk Management owner。",
                ]
            ),
            "required_context": as_list(deep_get(candidate, ("llm_usage_policy", "requires_context"), []))
            or [
                "broker",
                "venue",
                "account_scope",
                "order_type",
                "risk_policy_id",
                "permission_scope",
                "position_source",
                "audit_trace_id",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: reviewed-preparation audit allowed formal reviewed/caveat_only only; no approved/default/hard gate/risk-threshold advice.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
                "risk_threshold_advice_forbidden",
                "trade_execution_advice_forbidden",
            ],
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "review": {
            "review_status": "reviewed",
            "reviewed_at": TODAY,
            "reviewed_by": "codex_with_external_ai_audit",
            "confidence": result.get("confidence"),
            "freshness": deep_get(candidate, ("review", "freshness"), "stable"),
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": result.get("decision"),
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": result.get("reasons", []),
                "required_followups": result.get("required_followups", []),
                "patch_notes": patches,
            },
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
                    "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default/hard gate/risk-threshold advice all disabled.",
                },
            ],
        },
        "contribution": {
            "source_type": "phase37_candidate_to_reviewed",
            "source_candidate_id": candidate.get("candidate_id"),
            "audit_result_id": AUDIT_RESULT_ID,
            "private_data_removed": True,
            "contains_account_facts": False,
            "contains_secret": False,
            "contains_project_private_strategy": False,
        },
        "recommended_extra_sources": [],
    }


def write_knowledge(candidate: dict[str, Any], formal: dict[str, Any]) -> Path:
    knowledge_dir = partition_knowledge_dir(candidate)
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    path = knowledge_dir / sanitize_filename(str(formal["knowledge_id"]))
    if path.exists() and deep_get(read_json(path), ("review", "review_status")) == "approved":
        raise ValueError(f"Refusing to overwrite approved knowledge: {rel(path)}")
    write_json(path, formal)
    return path


def update_candidate_formalized(candidate: dict[str, Any], formal: dict[str, Any], formal_path: Path, result: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "reviewed"
    status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
    status["decision_reason"] = "reviewed-preparation 审计允许 formal reviewed/caveat_only；不允许 approved/default guidance/hard gate/风险阈值建议。"
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "next_action": "none",
            "formalization_allowed": True,
            "formal_knowledge_id": formal["knowledge_id"],
            "formal_review_status": "reviewed",
            "formal_knowledge_path": rel(formal_path),
            "knowledge_path": rel(formal_path),
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion.update(
            {
                "target_review_status": "reviewed",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
            }
        )
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
        "patch_notes": patch_groups(result),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_live_risk_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(formal_path)}.",
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
            "next_action": "supplement_internal_contract_schema_then_reaudit",
            "formalization_allowed": False,
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion.update(
            {
                "target_review_status": "blocked_until_supplemented",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
            }
        )
    review = candidate.setdefault("review", {})
    patches = patch_groups(result)
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
        "risk_threshold_advice_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": patches,
    }
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate.update(
        {
            "default_guidance": "deny",
            "reason": "reviewed-preparation 审计未通过；补内部契约/schema 前不得 formal reviewed、approved、default guidance、hard gate 或风险阈值建议。",
            "requires_human_escalation": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }
    )
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_live_risk_reviewed_preparation_needs_more_evidence",
                "reason": f"{TASK_ID}: {status['decision_reason']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )


def main() -> int:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit = archive_audit_result(source_path)
    results = validate_audit(audit)
    candidates = load_candidates()
    global_patches = audit.get("global_patch_notes") if isinstance(audit.get("global_patch_notes"), dict) else {}

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
            formal = build_formal_knowledge(candidate, result, global_patches)
            formal_path = write_knowledge(candidate, formal)
            update_candidate_formalized(candidate, formal, formal_path, result)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            written_knowledge_paths.append(rel(formal_path))
            promoted.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "knowledge_id": formal["knowledge_id"],
                    "knowledge_path": rel(formal_path),
                    "canonical_node_id": deep_get(formal, ("metadata", "canonical_node_id")),
                    "review_status": "reviewed",
                    "machine_gate": "caveat_only",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
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
                    "required_followups": result.get("required_followups", []),
                    "patch_notes": patch_groups(result),
                    "next_action": "补充内部契约/schema 后导出再审包",
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
        "report_id": "phase37_live_risk_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "archive_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "source_quality_gate_pass": bool(deep_get(audit, ("quality_gate", "pass"), False)),
        "source_quality_gate_reason": deep_get(audit, ("quality_gate", "reason")),
        "decision_counts": dict(Counter(str(item.get("decision")) for item in results)),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "risk_threshold_advice_enabled": 0,
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "boundary": (
            "formal reviewed/caveat_only only for 9 accepted items; L03/L10/L11 remain needs_more_evidence; "
            "no approved/default guidance/hard gate/risk-threshold advice."
        ),
        "next_action": (
            "CEK-TA-440: 为 L03/L10/L11 补充 position_reconciliation、portfolio_exposure_limit、"
            "consecutive_loss_stop_policy 内部契约/schema 后再审。"
        ),
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
