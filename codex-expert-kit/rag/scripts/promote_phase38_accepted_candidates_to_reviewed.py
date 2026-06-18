"""Promote Phase 38 accepted candidates into formal reviewed knowledge.

This script is intentionally Phase-38 scoped. It converts only candidates whose
status is accepted_for_draft, writes formal reviewed KnowledgeItem v1.1 files,
updates candidate formal back-links, and keeps default guidance disabled.
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


TODAY = date(2026, 6, 10).isoformat()
AUDIT_TASK_ID = "CEK-TA-273"
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_candidates_to_reviewed_promotion_report.json", start_file=__file__
)

CLAIM_TYPE_BY_NODE = {
    "kt.ai_engineering.numeric_scoring": "llm_eval_rule",
    "kt.ai_engineering.calibration_threshold": "llm_eval_rule",
    "kt.ai_engineering.decision_time_feature_contract": "training_data_schema_rule",
    "kt.ai_engineering.llm_audit_assistant": "llm_eval_rule",
    "kt.ai_engineering.shadow_paper_ope_eval": "llm_eval_rule",
    "kt.ai_engineering.model_release_governance": "llmops_release_rule",
    "kt.rag_engineering.trading_scoring_rag_pack": "rag_governance_rule",
}

DISPLAY_NODE_ALIAS = {
    "kt.rag_engineering.trading_scoring_rag_pack": "kt.ai_engineering.rag_engineering.trading_scoring_rag_pack",
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def title_from_candidate(candidate: dict[str, Any]) -> str:
    claim = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    normalized = str(deep_get(candidate, ("claim", "normalized_claim"), "")).strip()
    if claim:
        return claim[:96]
    return normalized.replace("_", " ").replace(".", " ").title()


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


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


def shape_source_quality(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = deep_get(candidate, ("source_quality",), {}) or {}
    evidence = as_list(candidate.get("source_refs"))
    primary = int(raw.get("primary_source_count") or len([s for s in evidence if s.get("reliability") == "high"]))
    return {
        "overall_reliability": raw.get("overall_reliability", "medium"),
        "score": raw.get("score", 0),
        "score_version": raw.get("score_version", "1.0.0"),
        "primary_source_count": primary,
        "supporting_source_count": raw.get("supporting_source_count", max(len(evidence) - primary, 0)),
        "low_reliability_source_count": raw.get("low_reliability_source_count", 0),
        "limitations": as_list(raw.get("limitations"))
        + [
            "Phase 38 formal reviewed 知识可用于审计和检索；默认指导仍需后续人工治理升级 approved。",
        ],
    }


def shape_conflict_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = deep_get(candidate, ("conflict_audit",), {}) or {}
    conflicts = []
    for conflict in as_list(raw.get("conflicts")):
        if not isinstance(conflict, dict):
            continue
        conflicts.append(
            {
                "knowledge_id": conflict.get("knowledge_id", ""),
                "conflict_type": conflict.get("conflict_type", "scope_conflict"),
                "severity": conflict.get("severity", "warning"),
                "resolution": conflict.get("resolution", ""),
                "applicability_boundary": json.dumps(conflict.get("overlap_scope", {}), ensure_ascii=False),
            }
        )
    return {
        "conflict_status": raw.get("conflict_status", "none"),
        "checked_against": as_list(raw.get("checked_against")),
        "conflicts": conflicts,
        "resolution_summary": raw.get(
            "resolution_summary",
            "未发现与当前 CEK-TA formal knowledge 的直接冲突；reviewed 不等于 approved。",
        ),
        "default_recommendation": "caveat_only_until_human_approval",
    }


def build_content(candidate: dict[str, Any]) -> dict[str, Any]:
    claim = deep_get(candidate, ("claim",), {}) or {}
    applicability = deep_get(candidate, ("applicability",), {}) or {}
    limitations = as_list(applicability.get("limitations"))
    open_questions = as_list(deep_get(candidate, ("review", "open_questions"), []))
    custom_risk_notes = []
    if candidate.get("top_k") is not None:
        custom_risk_notes.append("top_k=5 只是 Phase 38 P0 policy default，不是全局最优或性能结论。")
    if candidate.get("token_budget") is not None:
        custom_risk_notes.append("token_budget=4000 只是 Phase 38 P0 policy default，不是全局最优或性能结论。")
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": [
            "确认当前外接项目任务属于 Phase 38 AI Engineering 范围。",
            "确认没有要求具体买卖点、仓位、止损止盈、fill model、执行参数或实盘动作。",
            "读取本知识项时必须同时带出 source_evidence、review_status、machine_gate 和适用边界。",
            "若命中 Trading Engineering 边界，必须路由到对应交易知识分支。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 reviewed 知识当作 approved 默认指导。",
            "把 AI Engineering 方法论规则扩展成具体交易策略或实盘执行动作。",
            "在缺少项目事实、来源引用或适用边界时让 AI IDE 直接输出强结论。",
        ],
        "validation": [
            "source_evidence 非空，且 conflict_status 为 none 或 resolved。",
            "review_status 为 reviewed 时 machine_gate.default_guidance 必须为 caveat_only。",
            "MCP/SearchLab 返回该知识时必须显示 caveat、来源和不适用场景。",
            "Vue3 知识树能按 canonical_node_id 检索并展示本条知识。",
        ],
        "risk_notes": limitations
        + open_questions
        + custom_risk_notes
        + [
            "本条为 formal reviewed 知识，不是 approved；不得进入默认指导或 hard gate。",
            "不得保存或推广项目私有交易数据、账户信息、策略参数或实盘订单字段。",
        ],
        "citation_notes": claim.get("evidence_summary", ""),
    }


def build_llm_usage_policy(candidate: dict[str, Any]) -> dict[str, Any]:
    classification = deep_get(candidate, ("classification",), {}) or {}
    node = classification.get("tree_node_id", "")
    return {
        "allowed": [
            "用于外接交易 LLM gating/scoring 项目的方案审计、代码审查、数据契约审查和 RAG/MCP 检索提示。",
            "用于提醒 AI IDE 明确模型、数据、评估、发布或检索边界，并引用来源。",
            "用于在 SearchLab、KnowledgeTree 和 MCP 中以 caveat 方式返回 reviewed 知识。",
        ],
        "not_allowed": [
            "不得据此生成具体买卖点、仓位、止损止盈、杠杆、策略参数或实盘订单动作。",
            "不得把 reviewed 知识当作 approved 默认指导或 hard gate。",
            "不得替代 Trading Engineering 对 K 线、回测、fill model、风控和执行规则本体的判断。",
        ],
        "required_context": [
            f"canonical_node_id={node}",
            "外接项目必须提供 project_adapter_id、task_type、mode、requested_decision 和相关版本号。",
            "必须同时返回 source_evidence、conflict_status、review_status 和 machine_gate。",
        ],
        "fallback_behavior": "cite_with_caveat",
    }


def build_machine_gate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "default_guidance": "caveat_only",
        "reason": "Phase 38 候选已通过 AI/人工审计并沉淀为 formal reviewed；可审计检索，但尚未人工 approved。",
        "requires_human_escalation": True,
        "blocking_reasons": [
            "reviewed_not_approved",
            "default_guidance_disabled_until_human_approval",
            "hard_gate_disabled",
        ],
        "checked_at": TODAY,
        "gate_version": "1.0.0",
    }


def candidate_to_knowledge(candidate: dict[str, Any]) -> dict[str, Any]:
    classification = deep_get(candidate, ("classification",), {}) or {}
    applicability = deep_get(candidate, ("applicability",), {}) or {}
    review = deep_get(candidate, ("review",), {}) or {}
    status = deep_get(candidate, ("status",), {}) or {}
    conversion = deep_get(candidate, ("conversion_target",), {}) or {}
    candidate_id = candidate.get("candidate_id", "")
    knowledge_id = conversion.get("proposed_knowledge_id", "")
    tree_node_id = classification.get("tree_node_id", "")
    canonical_node_id = classification.get("canonical_node_id") or tree_node_id
    display_alias = DISPLAY_NODE_ALIAS.get(canonical_node_id)
    claim_type = CLAIM_TYPE_BY_NODE.get(canonical_node_id, CLAIM_TYPE_BY_NODE.get(tree_node_id, "ai_governance_rule"))
    audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}
    decision_log = []
    for entry in as_list(review.get("audit_log")):
        if not isinstance(entry, dict):
            continue
        decision_log.append(
            {
                "at": entry.get("at", status.get("updated_at", TODAY)),
                "actor": entry.get("actor", "codex"),
                "decision": entry.get("action", "updated"),
                "reason": entry.get("reason", ""),
            }
        )
    decision_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "decision": "reviewed",
            "reason": f"{AUDIT_TASK_ID}: accepted_for_draft candidate promoted to formal reviewed knowledge; no approved/default guidance.",
        }
    )

    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id", "KB_AI_ENGINEERING"),
            "domain": classification.get("domain", "llm_training"),
            "subdomain": classification.get("subdomain", "phase38"),
            "rule_type": classification.get("rule_type", "checklist"),
            "claim_type": claim_type,
            "content_type": "json",
            "project_binding": "none",
            "classification_notes": (
                "Phase 38 formal reviewed knowledge；accepted_for_draft 已转 reviewed，但不是 approved。"
                + (f" UI display alias: {display_alias}." if display_alias else "")
            ),
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / AI Engineering"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / AI Engineering"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate_id,
            "research_task_id": candidate.get("research_task_id", ""),
            "phase": "Phase 38",
            "display_node_alias": display_alias,
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_llm_assistant"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source) for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)],
        "source_quality": shape_source_quality(candidate),
        "conflict_audit": shape_conflict_audit(candidate),
        "llm_usage_policy": build_llm_usage_policy(candidate),
        "machine_gate": build_machine_gate(candidate),
        "recommended_extra_sources": [],
        "review": {
            "confidence": review.get("confidence", "medium"),
            "freshness": review.get("freshness", "time_sensitive"),
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": candidate_id,
            "ai_audit_result_id": audit.get("audit_result_id") or deep_get(candidate, ("workflow", "ai_audit_result_id")),
            "ai_audit": {
                "audit_result_id": audit.get("audit_result_id") or deep_get(candidate, ("workflow", "ai_audit_result_id")),
                "decision": "accepted_for_draft",
                "allowed_next_stage": "formal_reviewed_knowledge",
                "default_guidance_allowed": False,
                "approved_allowed": False,
                "hard_gate_allowed": False,
            },
            "open_questions": as_list(review.get("open_questions")),
            "decision_log": decision_log,
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 38 public-source candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "phase38_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": AUDIT_TASK_ID,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }


def validate_candidate_for_promotion(candidate: dict[str, Any]) -> str | None:
    candidate_id = str(candidate.get("candidate_id", "<unknown>"))
    if not candidate_id.startswith("cand_20260610_phase38_"):
        return "not_phase38"
    if deep_get(candidate, ("status", "review_status")) != "accepted":
        return "not_accepted"
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "not_accepted_for_draft"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_knowledge_id"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {"none", "resolved"}:
        return "unsafe_conflict"
    if not as_list(candidate.get("source_refs")):
        return "missing_sources"
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    return None


def load_candidates() -> list[tuple[Path, dict[str, Any]]]:
    result = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        result.append((path, read_json(path)))
    return result


def write_knowledge(item: dict[str, Any]) -> Path:
    partition = item["metadata"]["partition_id"]
    path = KNOWLEDGE_ROOT / partition / sanitize_filename(item["knowledge_id"])
    if path.exists():
        current = read_json(path)
        current_status = deep_get(current, ("review", "review_status"))
        if current_status == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def update_candidate_backlink(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "hidden_from_default_queue": True,
            "next_action": "request_human_approval",
            "default_guidance_allowed": False,
            "knowledge_path": rel(knowledge_path),
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    review = candidate.setdefault("review", {})
    audit = review.setdefault("ai_audit", {})
    if isinstance(audit, dict):
        audit["allowed_next_stage"] = "formal_reviewed_knowledge"
        audit["default_guidance_allowed"] = False
        audit["reviewed_allowed"] = True
        audit["approved_allowed"] = False
        audit["hard_gate_allowed"] = False
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "formal_reviewed_created",
                "reason": f"{AUDIT_TASK_ID}: formal reviewed knowledge written to {rel(knowledge_path)}.",
            }
        )


def main() -> int:
    promoted: list[dict[str, Any]] = []
    skipped = Counter()
    touched_candidates: list[str] = []
    for candidate_path, candidate in load_candidates():
        reason = validate_candidate_for_promotion(candidate)
        if reason:
            skipped[reason] += 1
            continue
        item = candidate_to_knowledge(candidate)
        knowledge_path = write_knowledge(item)
        update_candidate_backlink(candidate, item, knowledge_path)
        write_json(candidate_path, candidate)
        touched_candidates.append(rel(candidate_path))
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": candidate["research_task_id"],
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    by_partition = Counter(item["partition_id"] for item in promoted)
    report = {
        "report_id": "phase38_candidates_to_reviewed_promotion_report",
        "generated_at": TODAY,
        "task_id": AUDIT_TASK_ID,
        "promoted_count": len(promoted),
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "by_partition": dict(sorted(by_partition.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
