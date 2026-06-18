"""Create formal draft knowledge from Phase 43 accepted candidates.

This script converts Phase 43 candidates that reached accepted_for_draft into
formal knowledge files with review_status=draft. It intentionally does not
create reviewed, approved, default-guidance, or hard-gate knowledge.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
TASK_ID = "CEK-TA-368"
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
KNOWLEDGE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "knowledge", "KB_AI_27_PROJECT_MEMORY", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase43_formal_draft_generation_report.json", start_file=__file__
)


CLAIM_TYPE_BY_ROLE = {
    "boundary": "project_integration_rule",
    "schema": "ai_governance_rule",
    "lifecycle": "ai_governance_rule",
    "event_log": "ai_governance_rule",
    "write_gate": "ai_security_rule",
    "mcp_api": "mcp_contract_rule",
    "retention_privacy": "ai_security_rule",
    "security": "ai_security_rule",
    "integrity": "ai_security_rule",
    "storage_baseline": "ai_governance_rule",
    "retrieval": "rag_governance_rule",
    "adapter": "project_integration_rule",
    "evaluation": "ai_governance_rule",
}

HIGH_RISK_ROLES = {"write_gate", "security", "integrity", "retention_privacy", "mcp_api"}


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


def string_value(value: Any, default: str = "") -> str:
    return value if isinstance(value, str) else default


def slug_from_candidate(candidate: dict[str, Any]) -> str:
    normalized = string_value(deep_get(candidate, ("claim", "normalized_claim")))
    slug = normalized
    if slug.startswith("phase43."):
        slug = slug[len("phase43.") :]
    if slug.endswith(".v1"):
        slug = slug[: -len(".v1")]
    slug = re.sub(r"[^a-z0-9_]+", "_", slug.lower()).strip("_")
    if not slug:
        raise ValueError(f"empty slug for {candidate.get('candidate_id')}")
    return slug


def knowledge_id_for(candidate: dict[str, Any]) -> str:
    return f"kb_ai_project_memory.phase43.{slug_from_candidate(candidate)}.v1"


def filename_for(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": string_value(source.get("source_id")),
        "source_title": string_value(source.get("source_title") or source.get("title")),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": string_value(source.get("source_type"), "other"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": string_value(source.get("accessed_at"), TODAY),
        "version": source.get("version"),
        "reliability": string_value(source.get("reliability"), "medium"),
        "relevance": string_value(source.get("relevance"), "medium"),
        "evidence_summary": string_value(source.get("evidence_summary")),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def source_quality(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    refs = [ref for ref in as_list(candidate.get("source_refs")) if isinstance(ref, dict)]
    return {
        "overall_reliability": raw.get("overall_reliability", "high" if refs else "medium"),
        "score": raw.get("score", 0),
        "score_version": raw.get("score_version", "1.1.0"),
        "primary_source_count": raw.get("primary_source_count", len([r for r in refs if r.get("reliability") == "high"])),
        "supporting_source_count": raw.get("supporting_source_count", len(refs)),
        "low_reliability_source_count": raw.get("low_reliability_source_count", 0),
        "limitations": as_list(raw.get("limitations"))
        + [
            "Phase 43 formal draft only；尚未 reviewed/approved，不得作为默认指导或 hard gate。",
        ],
    }


def conflict_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("conflict_audit") if isinstance(candidate.get("conflict_audit"), dict) else {}
    return {
        "conflict_status": raw.get("conflict_status", "none"),
        "checked_against": as_list(raw.get("checked_against")),
        "conflicts": as_list(raw.get("conflicts")),
        "resolution_summary": (
            "Phase 43 formal draft generated from accepted_for_draft candidate. "
            "It remains draft only; reviewed/approved/default guidance/hard gate require separate governance."
        ),
        "default_recommendation": "deny_until_reviewed_caveat_only_audit",
    }


def llm_usage_policy(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("llm_usage_policy") if isinstance(candidate.get("llm_usage_policy"), dict) else {}
    return {
        "allowed": as_list(raw.get("allowed"))
        + [
            "用于设计外接项目 Project Memory Contract、MemoryItem schema、MCP/API、写入门禁和检索预算的 draft 审计。",
        ],
        "not_allowed": as_list(raw.get("not_allowed"))
        + [
            "不得把 draft 当作 reviewed、approved 或默认指导。",
            "不得让 AI 直接写 active memory。",
            "不得把外接项目私有记忆写入 CEK-TA。",
        ],
        "required_context": [
            "必须确认调用方是在设计外接项目 AI Memory Layer，而不是请求保存 CEK-TA 本项目私有记忆。",
            "必须同时返回 review_status=draft、machine_gate=deny、source_evidence 和适用边界。",
        ],
        "fallback_behavior": "ask_for_context",
    }


def content(candidate: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    ai_audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}
    handoff_patch = ai_audit.get("proposed_handoff_patch") if isinstance(ai_audit.get("proposed_handoff_patch"), dict) else {}
    return {
        "statement": string_value(claim.get("statement")),
        "rationale": string_value(claim.get("interpretation_notes") or claim.get("evidence_summary")),
        "procedure": [
            "确认当前任务属于外接项目 AI Memory Layer，而不是 CEK-TA 本项目私有记忆实现。",
            "先读取 CEK-TA 专业知识，再读取外接项目 Project Memory；两者不得混为同一事实源。",
            "写入长期记忆前必须经过 source check、secret scan、prompt injection scan、memory poisoning scan、visibility check、conflict check 和人工/规则审核。",
            "Project Memory 只能辅助 AI IDE / Agent 的任务上下文，不得进入交易 final gate 或实盘执行链路。",
        ],
        "examples": [],
        "anti_patterns": [
            "自动把所有聊天、日志和中间推断写入长期记忆。",
            "把 vector hit 或第三方 memory engine 输出当作事实源。",
            "把外接项目私有目标、错误、决策、表结构或账户字段写入 CEK-TA 通用知识。",
            "让 LLM 直接写 active memory，或绕过 write gate。",
        ],
        "validation": [
            "review.review_status 必须保持 draft，直到单独 reviewed/caveat_only 审计通过。",
            "machine_gate.default_guidance 必须为 deny。",
            "source_evidence 必须非空，且 conflict_status 不得为 confirmed/unchecked。",
            "候选回链必须保留 source_candidate_id 和 ai_audit_result_id。",
        ],
        "risk_notes": as_list(applicability.get("limitations"))
        + as_list(review.get("open_questions"))
        + as_list(handoff_patch.get("boundary_patch_notes"))
        + [
            "本条是 formal draft，不是 reviewed/approved。",
            "不得创建生产数据库、实现 Project Memory MCP server 或绑定单一 memory vendor。",
        ],
        "citation_notes": string_value(claim.get("evidence_summary")),
        "audit_patch_notes": {
            "source_patch_notes": as_list(handoff_patch.get("source_patch_notes")),
            "content_patch_notes": as_list(handoff_patch.get("content_patch_notes")),
            "boundary_patch_notes": as_list(handoff_patch.get("boundary_patch_notes")),
            "conflict_patch_notes": as_list(handoff_patch.get("conflict_patch_notes")),
            "required_followups": as_list(ai_audit.get("required_followups")),
        },
    }


def candidate_to_knowledge(candidate: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    ai_audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}
    role = string_value(claim.get("memory_layer_role") or claim.get("claim_type"), "boundary")
    knowledge_id = knowledge_id_for(candidate)
    title = string_value(claim.get("statement"), knowledge_id)[:140]
    refs = [source_to_evidence(ref) for ref in as_list(candidate.get("source_refs")) if isinstance(ref, dict)]
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title,
        "metadata": {
            "partition_id": "KB_AI_27_PROJECT_MEMORY",
            "domain": "ai_engineering",
            "subdomain": string_value(classification.get("subdomain"), "external_project_memory"),
            "rule_type": string_value(classification.get("rule_type"), "governance_rule"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": string_value(classification.get("tree_node_id")),
            "tree_path": string_value(classification.get("tree_path"), "CEK-TA / AI Engineering / External Project AI Memory Layer"),
            "canonical_node_id": string_value(classification.get("canonical_node_id") or classification.get("tree_node_id")),
            "canonical_tree_path": "CEK-TA / AI Engineering / External Project AI Memory Layer",
            "risk_level": "high" if role in HIGH_RISK_ROLES else "medium",
            "used_for": sorted(set(as_list(classification.get("used_for")) + ["external_project_memory", "mcp", "vue_audit_ui"])),
            "source_candidate_id": string_value(candidate.get("candidate_id")),
            "research_task_id": string_value(candidate.get("research_task_id")),
            "claim_type": CLAIM_TYPE_BY_ROLE.get(role, "ai_governance_rule"),
            "classification_notes": (
                "Phase 43 formal draft only；用于外接项目 AI Memory Layer 契约审计。"
                "不得保存外接项目私有记忆，不得进入 reviewed/approved/default guidance/hard gate。"
            ),
        },
        "applicability": {
            "market": string_value(applicability.get("market"), "general"),
            "asset": string_value(applicability.get("asset"), "general"),
            "timeframe": string_value(applicability.get("timeframe"), "general"),
            "data_granularity": string_value(applicability.get("data_granularity"), "general"),
            "project_type": string_value(applicability.get("project_type"), "external_ai_project_memory_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": content(candidate),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": refs,
        "source_quality": source_quality(candidate),
        "conflict_audit": conflict_audit(candidate),
        "review": {
            "review_status": "draft",
            "confidence": string_value(review.get("confidence"), "medium"),
            "freshness": string_value(review.get("freshness"), "time_sensitive"),
            "reviewer": "codex",
            "reviewed_at": None,
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": string_value(candidate.get("candidate_id")),
            "ai_audit_result_id": string_value(ai_audit.get("audit_result_id")),
            "ai_audit": ai_audit,
            "open_questions": [
                "需要单独 reviewed/caveat_only 审计确认后，才能从 formal draft 升级为 reviewed。",
            ],
        },
        "llm_usage_policy": llm_usage_policy(candidate),
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 43 formal draft only; reviewed/approved/default guidance/hard gate require separate governance.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "review_status_is_draft",
                "reviewed_allowed_false_in_latest_audit",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "recommended_extra_sources": [],
        "contribution": candidate.get("contribution", {}),
        "version_history": [
            {
                "version": "v1",
                "created_at": TODAY,
                "actor": "codex",
                "change": "Created formal draft from Phase 43 accepted_for_draft candidate.",
                "audit_result_id": string_value(ai_audit.get("audit_result_id")),
            }
        ],
    }


def is_phase43_accepted_candidate(candidate: dict[str, Any]) -> bool:
    candidate_id = string_value(candidate.get("candidate_id"))
    if not candidate_id.startswith("cand_20260611_phase43_"):
        return False
    if deep_get(candidate, ("status", "review_status")) != "accepted":
        return False
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return False
    if deep_get(candidate, ("workflow", "queue_group")) not in {"ai_passed", "formalized"}:
        return False
    if string_value(candidate.get("candidate_id")).endswith("__013"):
        return False
    return True


def update_candidate(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "formalized_draft"
    workflow["queue_group"] = "formalized"
    workflow["formal_knowledge_id"] = item["knowledge_id"]
    workflow["formal_knowledge_path"] = rel(knowledge_path)
    workflow["formal_review_status"] = "draft"
    workflow["ai_audit_result_id"] = string_value(deep_get(item, ("review", "ai_audit_result_id")))
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["candidate_to_formal_allowed"] = False
    workflow["target_review_status"] = "draft"
    workflow["reviewed_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["next_action"] = "review_formal_knowledge"
    candidate.setdefault("conversion_target", {}).update(
        {
            "proposed_knowledge_id": item["knowledge_id"],
            "target_schema": "cek_ta_knowledge_item_v1_1",
            "target_review_status": "draft",
            "knowledge_path": rel(knowledge_path),
        }
    )
    candidate.setdefault("review", {}).setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "formal_draft_created",
            "reason": "Created formal draft knowledge from Phase 43 accepted_for_draft candidate.",
            "knowledge_id": item["knowledge_id"],
        }
    )


def main() -> int:
    promoted: list[dict[str, Any]] = []
    skipped = Counter()
    for candidate_path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase43_*.json")):
        candidate = read_json(candidate_path)
        if not is_phase43_accepted_candidate(candidate):
            skipped["not_phase43_accepted_for_draft"] += 1
            continue
        item = candidate_to_knowledge(candidate)
        knowledge_path = KNOWLEDGE_DIR / filename_for(item["knowledge_id"])
        write_json(knowledge_path, item)
        update_candidate(candidate, item, knowledge_path)
        write_json(candidate_path, candidate)
        promoted.append(
            {
                "candidate_id": candidate["candidate_id"],
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "review_status": "draft",
                "machine_gate": "deny",
            }
        )

    report = {
        "report_id": "phase43_formal_draft_generation_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "input_scope": "Phase 43 candidates with accepted_for_draft and workflow.queue_group in ai_passed/formalized",
        "formal_draft_count": len(promoted),
        "skipped": dict(skipped),
        "promoted": promoted,
        "boundary": "formal draft only; no reviewed, approved, default guidance, or hard gate created.",
        "next_action": "Export formal draft reviewed/caveat_only audit package before any reviewed conversion.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == 29 else 1


if __name__ == "__main__":
    raise SystemExit(main())
