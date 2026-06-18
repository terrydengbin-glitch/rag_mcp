"""Promote Phase 42 accepted candidates into formal reviewed knowledge.

This script is Phase-42 scoped. It converts only candidates that already passed
AI audit as accepted_for_draft, writes formal reviewed/caveat_only knowledge
items, updates candidate back-links, and never creates approved/default guidance
or hard-gate knowledge.
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
TASK_ID = "CEK-TA-350"
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase42_candidates_to_reviewed_promotion_report.json", start_file=__file__
)

CLAIM_TYPE_BY_STORAGE_ROLE = {
    "canonical_store": "ai_governance_rule",
    "audit_ledger": "ai_governance_rule",
    "vector_index": "rag_governance_rule",
    "manifest_store": "training_data_schema_rule",
    "feature_store": "training_data_schema_rule",
    "registry": "llmops_release_rule",
    "backup_restore": "ai_governance_rule",
}

CLAIM_TYPE_BY_SUBDOMAIN = {
    "relational_core_schema": "ai_governance_rule",
    "data_contract_lineage": "training_data_schema_rule",
    "migration_versioning": "ai_governance_rule",
    "indexing_query_performance": "data_quality_rule",
    "audit_log_ledger": "ai_governance_rule",
    "feature_store_storage": "training_data_schema_rule",
    "vector_store_retrieval_storage": "rag_governance_rule",
    "model_registry_release_storage": "llmops_release_rule",
    "runtime_observability_trace": "ai_governance_rule",
    "data_lifecycle_retention": "ai_governance_rule",
    "security_privacy_access_control": "ai_security_rule",
    "backup_restore_disaster_recovery": "ai_governance_rule",
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


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def title_from_candidate(candidate: dict[str, Any]) -> str:
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    normalized = str(deep_get(candidate, ("claim", "normalized_claim"), "")).strip()
    if statement:
        return statement[:110]
    return normalized.replace("_", " ").replace(".", " ").title()


def claim_type_for(candidate: dict[str, Any]) -> str:
    storage_role = str(deep_get(candidate, ("claim", "storage_role"), ""))
    subdomain = str(deep_get(candidate, ("classification", "subdomain"), ""))
    return CLAIM_TYPE_BY_STORAGE_ROLE.get(
        storage_role,
        CLAIM_TYPE_BY_SUBDOMAIN.get(subdomain, "ai_governance_rule"),
    )


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
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    sources = [s for s in as_list(candidate.get("source_refs")) if isinstance(s, dict)]
    primary = int(raw.get("primary_source_count") or len([s for s in sources if s.get("reliability") == "high"]))
    return {
        "overall_reliability": raw.get("overall_reliability", "medium"),
        "score": raw.get("score", 0),
        "score_version": raw.get("score_version", "1.1.0"),
        "primary_source_count": primary,
        "supporting_source_count": raw.get("supporting_source_count", max(len(sources) - primary, 0)),
        "low_reliability_source_count": raw.get("low_reliability_source_count", 0),
        "limitations": as_list(raw.get("limitations"))
        + [
            "Phase 42 formal reviewed 知识仅可作为数据库/数据契约/存储工程审计与检索依据；默认指导仍需后续人工 approved。",
        ],
    }


def shape_conflict_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("conflict_audit") if isinstance(candidate.get("conflict_audit"), dict) else {}
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
        "resolution_summary": (
            "Phase 42 reviewed/caveat_only conversion passed; formal reviewed knowledge is searchable and citable, "
            "but not approved, not default guidance, and not hard gate."
        ),
        "default_recommendation": "caveat_only_until_human_approval",
    }


def build_content(candidate: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    ai_audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}
    risk_notes = (
        as_list(applicability.get("limitations"))
        + as_list(review.get("open_questions"))
        + as_list(ai_audit.get("boundary_patch_notes"))
        + as_list(ai_audit.get("content_patch_notes"))
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": [
            "确认当前任务属于交易 AI 数据库、数据契约、存储、审计日志、RAG/vector storage、备份恢复或生命周期治理范围。",
            "确认没有请求创建生产数据库、执行不可逆迁移、写入外部项目真实数据或改变 MCP/API 写权限。",
            "读取知识项时必须同时返回 source_evidence、review_status、machine_gate、适用边界和不适用场景。",
            "如果问题转向 K 线、fill model、仓位、止损止盈、订单状态机或实盘执行，应路由到 Trading Engineering。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 vector DB 当作事实主库或唯一 canonical store。",
            "让 LLM audit assistant 写 final_gate 决策表或绕过 deterministic final gate。",
            "把 reviewed/caveat_only 知识当作 approved 默认指导。",
            "在 CEK-TA 通用知识中写入外部项目私有表名、账户字段、策略参数或生产密钥。",
        ],
        "validation": [
            "source_evidence 非空，且 conflict_status 为 none 或 resolved。",
            "review_status 为 reviewed 时 machine_gate.default_guidance 必须为 caveat_only。",
            "MCP/SearchLab default_guidance_only 不得返回本条作为 allow。",
            "Vue3 知识树能按 canonical_node_id 展示本条，候选页能回链 formal_knowledge_id。",
        ],
        "risk_notes": risk_notes
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得进入默认指导或 hard gate。",
            "本条不创建真实数据库、不执行迁移、不改变外部服务依赖。",
        ],
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": {
            "source_patch_notes": as_list(ai_audit.get("source_patch_notes")),
            "content_patch_notes": as_list(ai_audit.get("content_patch_notes")),
            "boundary_patch_notes": as_list(ai_audit.get("boundary_patch_notes")),
            "conflict_patch_notes": as_list(ai_audit.get("conflict_patch_notes")),
        },
    }


def build_llm_usage_policy(candidate: dict[str, Any]) -> dict[str, Any]:
    node = str(deep_get(candidate, ("classification", "canonical_node_id"), ""))
    return {
        "allowed": [
            "用于外接交易 AI 项目的数据库 schema、数据契约、迁移、索引、审计日志、RAG/vector storage、备份恢复和生命周期治理审计。",
            "用于生成任务卡、接口契约、存储设计 checklist、测试计划和风险提示。",
            "用于 MCP/SearchLab/KnowledgeTree 以 caveat 方式返回 reviewed 知识和来源引用。",
        ],
        "not_allowed": [
            "不得据此生成买卖点、仓位、杠杆、止损止盈、实盘下单或交易执行建议。",
            "不得据此直接创建生产数据库、执行迁移或修改外部项目真实数据库。",
            "不得把 reviewed/caveat_only 当作 approved 默认指导或 hard gate。",
        ],
        "required_context": [
            f"canonical_node_id={node}",
            "外接项目必须提供 project_adapter_id、requested_decision、schema_version、dataset_hash、model_version、prompt_version、rag_index_version 和 audit_trace_id。",
            "必须同时返回 source_evidence、conflict_status、review_status 和 machine_gate。",
        ],
        "fallback_behavior": "cite_with_caveat",
    }


def build_machine_gate() -> dict[str, Any]:
    return {
        "default_guidance": "caveat_only",
        "reason": "CEK-TA-350 将 Phase 42 accepted_for_draft 候选沉淀为 formal reviewed；仅可审计检索，不可作为 approved 默认指导或 hard gate。",
        "requires_human_escalation": True,
        "blocking_reasons": [
            "reviewed_not_approved",
            "default_guidance_disabled_until_human_approval",
            "hard_gate_disabled",
            "production_database_changes_require_separate_task",
        ],
        "checked_at": TODAY,
        "gate_version": "1.0.0",
    }


def candidate_to_knowledge(candidate: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    ai_audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}

    candidate_id = str(candidate.get("candidate_id", ""))
    knowledge_id = str(conversion.get("proposed_knowledge_id", ""))
    tree_node_id = str(classification.get("tree_node_id", ""))
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)

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
            "reason": f"{TASK_ID}: accepted_for_draft candidate promoted to formal reviewed/caveat_only knowledge; no approved/default guidance.",
        }
    )

    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id", "KB_AI_26_DATABASE_STORAGE"),
            "domain": classification.get("domain", "storage_engineering"),
            "subdomain": classification.get("subdomain", "database_storage_engineering"),
            "rule_type": classification.get("rule_type", "governance_rule"),
            "claim_type": claim_type_for(candidate),
            "content_type": "json",
            "project_binding": "none",
            "classification_notes": (
                "Phase 42 formal reviewed/caveat_only knowledge；accepted_for_draft 已转 reviewed，但不是 approved。"
                " 数据库/存储规则只指导 AI Engineering 和 Project Integration，不创建真实数据库，不混入 Trading Engineering 本体。"
            ),
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / AI Engineering / Database Data Contract And Storage Engineering"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get(
                "tree_path", "CEK-TA / AI Engineering / Database Data Contract And Storage Engineering"
            ),
            "risk_level": "high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate_id,
            "research_task_id": candidate.get("research_task_id", ""),
            "phase": "Phase 42",
            "storage_role": deep_get(candidate, ("claim", "storage_role")),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_ai_gating_scoring_storage"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(s) for s in as_list(candidate.get("source_refs")) if isinstance(s, dict)],
        "source_quality": shape_source_quality(candidate),
        "conflict_audit": shape_conflict_audit(candidate),
        "llm_usage_policy": build_llm_usage_policy(candidate),
        "machine_gate": build_machine_gate(),
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
            "ai_audit_result_id": ai_audit.get("audit_result_id") or deep_get(candidate, ("workflow", "ai_audit_result_id")),
            "ai_audit": {
                "audit_result_id": ai_audit.get("audit_result_id") or deep_get(candidate, ("workflow", "ai_audit_result_id")),
                "decision": "accepted_for_draft",
                "allowed_next_stage": "formal_reviewed_knowledge",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
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
            "generic_mapping_notes": "Generated from Phase 42 public-source candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "phase42_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": TASK_ID,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "production_database_changes_allowed": False,
        },
    }


def validate_candidate_for_promotion(candidate: dict[str, Any]) -> str | None:
    candidate_id = str(candidate.get("candidate_id", "<unknown>"))
    if not candidate_id.startswith("cand_20260611_phase42_"):
        return "not_phase42"
    if deep_get(candidate, ("status", "review_status")) != "accepted":
        return "not_accepted"
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "not_accepted_for_draft"
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        return "not_ai_passed"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_knowledge_id"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {"none", "resolved"}:
        return "unsafe_conflict"
    if not as_list(candidate.get("source_refs")):
        return "missing_sources"
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        return "default_guidance_not_disabled"
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        return "hard_gate_not_disabled"
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    return None


def load_candidates() -> list[tuple[Path, dict[str, Any]]]:
    return [(path, read_json(path)) for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase42_*.json"))]


def write_knowledge(item: dict[str, Any]) -> Path:
    partition = item["metadata"]["partition_id"]
    path = KNOWLEDGE_ROOT / partition / sanitize_filename(item["knowledge_id"])
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
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
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval",
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
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
        audit["reviewed_allowed"] = True
        audit["approved_allowed"] = False
        audit["default_guidance_allowed"] = False
        audit["hard_gate_allowed"] = False
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only knowledge written to {rel(knowledge_path)}.",
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
                "default_guidance_allowed": False,
                "approved_allowed": False,
                "hard_gate_allowed": False,
            }
        )

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    by_partition = Counter(item["partition_id"] for item in promoted)
    report = {
        "report_id": "phase42_candidates_to_reviewed_promotion_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "input_scope": "Phase 42 candidates with accepted_for_draft and workflow.queue_group == ai_passed",
        "promoted_count": len(promoted),
        "skipped": dict(skipped),
        "by_node": dict(sorted(by_node.items())),
        "by_partition": dict(sorted(by_partition.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "formal_knowledge_created": len(promoted),
        "reviewed_created": len(promoted),
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate; no production database changes.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
