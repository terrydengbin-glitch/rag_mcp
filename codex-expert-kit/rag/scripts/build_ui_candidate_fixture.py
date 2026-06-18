"""Build the Vue3 Phase 23 candidate fixture.

The fixture is generated from rag/candidates/**/*.json so the audit UI does not
drift away from the file-based candidate source of truth.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_project_root, resolve_repo_path  # noqa: E402


ROOT = resolve_project_root(__file__)
CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
OUTPUT_PATH = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
JSON_OUTPUT_PATH = resolve_repo_path("ui", "public", "data", "phase23Candidates.json", start_file=__file__)


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_value(value: Any, default: str = "") -> str:
    return value if isinstance(value, str) else default


def normalize_confidence(value: Any, default: str = "medium") -> str:
    raw = string_value(value, default)
    if raw in {"high", "medium", "low"}:
        return raw
    if raw in {"medium_high", "high_medium"}:
        return "high"
    if raw in {"medium_low", "low_medium"}:
        return "medium"
    return default


def normalize_freshness(value: Any, default: str = "stable") -> str:
    raw = string_value(value, default)
    if raw in {"stable", "time_sensitive", "deprecated"}:
        return raw
    if raw in {"current", "fresh", "recent", "mixed"}:
        return "time_sensitive"
    if raw in {"stale", "expired"}:
        return "deprecated"
    return default


def normalize_conflict_status(value: Any, default: str = "unchecked") -> str:
    raw = string_value(value, default)
    if raw in {"none", "potential", "confirmed", "resolved", "deprecated_by_conflict", "unchecked"}:
        return raw
    if raw == "none_known_in_visible_context":
        return "none"
    return default


def normalize_source_type(value: Any, default: str = "other") -> str:
    raw = string_value(value, default)
    allowed = {
        "official_doc",
        "official_repo",
        "paper",
        "exchange_rule",
        "framework_doc",
        "cloud_provider_doc",
        "book",
        "research_report",
        "research_paper",
        "standard_doc",
        "security_standard",
        "regulator_release",
        "regulator_review",
        "standard_or_risk_framework",
        "governance_framework",
        "engineering_article",
        "internal_report",
        "internal_contract",
        "internal_runbook",
        "task_card",
        "code_doc",
        "runbook",
        "other",
    }
    if raw in allowed:
        return raw
    mapping = {
        "professional_body": "standard_doc",
        "regulatory_guidance": "regulator_release",
        "regulatory_rule": "regulator_release",
        "regulator_investor_education": "regulator_review",
        "protocol_reference": "standard_doc",
        "professional_article": "engineering_article",
        "market_infrastructure_article": "engineering_article",
        "broker_platform_doc": "framework_doc",
        "trading_platform_doc": "framework_doc",
        "systematic_trader_article": "research_report",
        "institutional_research": "research_report",
    }
    return mapping.get(raw, default)


def source_title(source: dict[str, Any]) -> str:
    return string_value(source.get("source_title") or source.get("title"), "untitled source")


def source_url(source: dict[str, Any]) -> str | None:
    value = source.get("source_url", source.get("url"))
    return value if isinstance(value, str) and value else None


def rel_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def atomic_write_text(path: Path, text: str) -> None:
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(text, encoding="utf-8", newline="\n")
    temp_path.replace(path)


def normalize_source(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": string_value(source.get("source_id")),
        "title": source_title(source),
        "url": source_url(source),
        "source_type": normalize_source_type(source.get("source_type"), "other"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": string_value(source.get("accessed_at")),
        "version": source.get("version"),
        "reliability": normalize_confidence(source.get("reliability"), "low"),
        "score": source.get("score", 0),
        "relevance": normalize_confidence(source.get("relevance"), "medium"),
        "freshness": normalize_freshness(source.get("freshness"), "stable"),
        "limitations": list_value(source.get("limitations")),
        "evidence_summary": string_value(source.get("evidence_summary")),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def required_field_gaps(candidate: dict[str, Any]) -> list[str]:
    checks = {
        "source_refs": list_value(candidate.get("source_refs")),
        "applicability.applies_when": deep_get(candidate, ("applicability", "applies_when"), []),
        "applicability.not_applicable_when": deep_get(candidate, ("applicability", "not_applicable_when"), []),
        "applicability.assumptions": deep_get(candidate, ("applicability", "assumptions"), []),
        "claim.statement": deep_get(candidate, ("claim", "statement")),
        "classification.tree_node_id": deep_get(candidate, ("classification", "tree_node_id")),
        "classification.partition_id": deep_get(candidate, ("classification", "partition_id")),
        "source_quality.overall_reliability": deep_get(candidate, ("source_quality", "overall_reliability")),
        "conflict_audit.conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status")),
        "conversion_target.proposed_knowledge_id": deep_get(candidate, ("conversion_target", "proposed_knowledge_id")),
    }
    return [name for name, value in checks.items() if value in (None, "", [])]


def blocking_issues(candidate: dict[str, Any], gaps: list[str]) -> list[str]:
    issues: list[str] = []
    source_quality = deep_get(candidate, ("source_quality", "overall_reliability"), "low")
    conflict_status = deep_get(candidate, ("conflict_audit", "conflict_status"), "unchecked")
    approval_allowed = bool(deep_get(candidate, ("conflict_audit", "approval_allowed"), False))
    stores_full_text = bool(deep_get(candidate, ("copyright", "stores_full_text"), True))
    stores_long_quote = bool(deep_get(candidate, ("copyright", "stores_long_quote"), True))

    if "source_refs" in gaps:
        issues.append("missing_source_refs")
    if source_quality == "low":
        issues.append("low_source_reliability")
    if conflict_status in {"confirmed", "unchecked", "deprecated_by_conflict"}:
        issues.append(f"unsafe_conflict_status:{conflict_status}")
    if not approval_allowed:
        issues.append("conflict_audit_not_approval_allowed")
    if stores_full_text or stores_long_quote:
        issues.append("copyright_storage_not_summary_only")
    for required_gap in (
        "applicability.applies_when",
        "applicability.not_applicable_when",
        "applicability.assumptions",
    ):
        if required_gap in gaps:
            issues.append(f"missing_{required_gap}")
    return issues


def candidate_status(candidate: dict[str, Any], issues: list[str]) -> str:
    review_status = deep_get(candidate, ("status", "review_status"), "")
    ingestion_decision = deep_get(candidate, ("status", "ingestion_decision"), "")
    conflict_status = deep_get(candidate, ("conflict_audit", "conflict_status"), "unchecked")

    if review_status == "rejected" or ingestion_decision == "reject":
        return "rejected"
    if review_status in {"accepted", "accepted_for_draft"} and ingestion_decision == "accepted_for_draft":
        return "accepted_for_draft"
    if any(issue.startswith("unsafe_conflict_status") for issue in issues):
        return "blocked"
    if issues:
        return "needs_more_evidence"
    if review_status in {"accepted", "accepted_for_draft"}:
        return "accepted_for_draft"
    if ingestion_decision in {"convert_to_knowledge_item", "convert_to_skill_and_knowledge"} and conflict_status in {"none", "resolved"}:
        return "candidate_ready"
    return "needs_more_evidence"


def load_formal_knowledge_index() -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(raw, dict):
            continue
        review = deep_get(raw, ("review",), {})
        metadata = deep_get(raw, ("metadata",), {})
        knowledge_id = string_value(raw.get("knowledge_id"))
        candidate_id = string_value(review.get("source_candidate_id") or metadata.get("source_candidate_id"))
        if not candidate_id:
            continue
        ai_audit = review.get("ai_audit") if isinstance(review, dict) else None
        indexed[candidate_id] = {
            "knowledge_id": knowledge_id,
            "review_status": string_value(review.get("review_status")),
            "approval_status": string_value(review.get("approval_status"), "not_requested"),
            "ai_audit_result_id": string_value(review.get("ai_audit_result_id") or (ai_audit or {}).get("audit_result_id")),
            "path": rel_path(path),
        }
    return indexed


def load_formal_knowledge_ids() -> set[str]:
    indexed: set[str] = set()
    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(raw, dict):
            continue
        knowledge_id = string_value(raw.get("knowledge_id"))
        review_status = string_value(deep_get(raw, ("review", "review_status")))
        if knowledge_id and review_status == "reviewed":
            indexed.add(knowledge_id)
    return indexed


def raw_candidate_id(candidate: dict[str, Any]) -> str:
    return string_value(candidate.get("candidate_id"))


def raw_research_task_id(candidate: dict[str, Any]) -> str:
    return string_value(candidate.get("research_task_id"))


def is_rejected_candidate(candidate: dict[str, Any]) -> bool:
    return (
        deep_get(candidate, ("status", "review_status")) == "rejected"
        or deep_get(candidate, ("status", "ingestion_decision")) == "reject"
        or deep_get(candidate, ("workflow", "queue_group")) == "rejected"
    )


def formalized_candidate_info(
    candidate: dict[str, Any],
    path: Path,
    formal_index: dict[str, dict[str, Any]],
    formal_knowledge_ids: set[str],
) -> dict[str, Any] | None:
    candidate_id = raw_candidate_id(candidate)
    formal = formal_index.get(candidate_id)
    if formal and formal.get("review_status") == "reviewed":
        return {
            "candidate_id": candidate_id,
            "candidate_path": rel_path(path),
            "formal_knowledge_id": formal.get("knowledge_id"),
            "formal_review_status": formal.get("review_status"),
            "ai_audit_result_id": formal.get("ai_audit_result_id"),
        }

    workflow = deep_get(candidate, ("workflow",), {})
    if not isinstance(workflow, dict):
        return None
    knowledge_id = string_value(workflow.get("formal_knowledge_id"))
    formal_review_status = string_value(workflow.get("formal_review_status"))
    if knowledge_id in formal_knowledge_ids and formal_review_status == "reviewed":
        return {
            "candidate_id": candidate_id,
            "candidate_path": rel_path(path),
            "formal_knowledge_id": knowledge_id,
            "formal_review_status": formal_review_status,
            "ai_audit_result_id": string_value(workflow.get("ai_audit_result_id")),
        }
    return None


def task_matches_rebuild_source(old_task_id: str, replacement_task_id: str) -> bool:
    return bool(
        old_task_id
        and replacement_task_id
        and (replacement_task_id == old_task_id or replacement_task_id.startswith(f"{old_task_id}-"))
    )


def build_rebuilt_archive_index(
    raw_candidates: list[tuple[Path, dict[str, Any]]],
    formal_index: dict[str, dict[str, Any]],
    formal_knowledge_ids: set[str],
) -> dict[str, dict[str, Any]]:
    formalized_by_task: list[tuple[str, dict[str, Any]]] = []
    for path, candidate in raw_candidates:
        if is_rejected_candidate(candidate):
            continue
        info = formalized_candidate_info(candidate, path, formal_index, formal_knowledge_ids)
        if not info:
            continue
        formalized_by_task.append((raw_research_task_id(candidate), info))

    archived: dict[str, dict[str, Any]] = {}
    for _, candidate in raw_candidates:
        if not is_rejected_candidate(candidate):
            continue
        old_task_id = raw_research_task_id(candidate)
        for replacement_task_id, info in formalized_by_task:
            if task_matches_rebuild_source(old_task_id, replacement_task_id):
                archived[raw_candidate_id(candidate)] = info
                break
    return archived


def workflow_for_candidate(
    candidate: dict[str, Any],
    status_value: str,
    formal: dict[str, Any] | None,
    rebuilt_archive: dict[str, Any] | None,
) -> dict[str, Any]:
    review_status = deep_get(candidate, ("status", "review_status"), "")
    audit_result_id = string_value(deep_get(candidate, ("review", "ai_audit", "audit_result_id")))

    if (review_status == "rejected" or status_value == "rejected") and rebuilt_archive:
        return {
            "stage": "rebuilt_archived",
            "queue_group": "rebuilt_archived",
            "formal_knowledge_id": rebuilt_archive.get("formal_knowledge_id") or None,
            "formal_review_status": rebuilt_archive.get("formal_review_status") or None,
            "ai_audit_result_id": rebuilt_archive.get("ai_audit_result_id") or audit_result_id or None,
            "hidden_from_default_queue": True,
            "next_action": "none",
            "replacement_candidate_id": rebuilt_archive.get("candidate_id") or None,
            "replacement_candidate_path": rebuilt_archive.get("candidate_path") or None,
            "replacement_formal_knowledge_id": rebuilt_archive.get("formal_knowledge_id") or None,
            "archive_reason": "原 rejected 候选因 slug / normalized_claim / ID 结构问题被拒绝；已存在重建候选和 formal reviewed 替代知识。",
        }

    if review_status == "rejected" or status_value == "rejected":
        return {
            "stage": "rejected",
            "queue_group": "rejected",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": audit_result_id or None,
            "hidden_from_default_queue": True,
            "next_action": "none",
        }

    if status_value in {"blocked", "needs_more_evidence"}:
        return {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": audit_result_id or None,
            "hidden_from_default_queue": False,
            "next_action": "export_ai_audit",
        }

    workflow = deep_get(candidate, ("workflow",), {})
    if isinstance(workflow, dict) and review_status == "formalized_reviewed":
        knowledge_id = string_value(workflow.get("formal_knowledge_id"))
        if knowledge_id:
            return {
                "stage": "formalized_reviewed",
                "queue_group": "formalized",
                "formal_knowledge_id": knowledge_id,
                "formal_review_status": string_value(workflow.get("formal_review_status"), "reviewed"),
                "ai_audit_result_id": string_value(workflow.get("last_audit_result_id") or audit_result_id) or None,
                "hidden_from_default_queue": True,
                "next_action": "request_human_approval",
            }

    if formal:
        formal_status = string_value(formal.get("review_status"))
        approval_status = string_value(formal.get("approval_status"), "not_requested")
        if formal_status == "approved" and approval_status == "approved":
            stage = "approved"
            next_action = "none"
        elif formal_status == "draft":
            stage = "formalized_draft"
            next_action = "review_formal_knowledge"
        elif approval_status == "requested":
            stage = "approval_requested"
            next_action = "request_human_approval"
        else:
            stage = "formalized_reviewed"
            next_action = "request_human_approval"
        return {
            "stage": stage,
            "queue_group": "formalized",
            "formal_knowledge_id": formal.get("knowledge_id") or None,
            "formal_review_status": formal_status or None,
            "ai_audit_result_id": formal.get("ai_audit_result_id") or audit_result_id or None,
            "hidden_from_default_queue": True,
            "next_action": next_action,
        }

    if review_status == "accepted" or status_value == "accepted_for_draft":
        return {
            "stage": "ai_audited",
            "queue_group": "ai_passed",
            "formal_knowledge_id": string_value(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"))) or None,
            "formal_review_status": "draft",
            "ai_audit_result_id": audit_result_id or None,
            "hidden_from_default_queue": True,
            "next_action": "apply_ai_audit_patch",
        }

    return {
        "stage": "pending_review",
        "queue_group": "pending",
        "formal_knowledge_id": None,
        "formal_review_status": None,
        "ai_audit_result_id": audit_result_id or None,
        "hidden_from_default_queue": False,
        "next_action": "export_ai_audit",
    }


def normalize_candidate(
    candidate: dict[str, Any],
    path: Path,
    formal_index: dict[str, dict[str, Any]],
    rebuilt_archive_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    classification = deep_get(candidate, ("classification",), {})
    claim = deep_get(candidate, ("claim",), {})
    applicability = deep_get(candidate, ("applicability",), {})
    source_refs = [normalize_source(source) for source in list_value(candidate.get("source_refs")) if isinstance(source, dict)]
    source_quality = deep_get(candidate, ("source_quality",), {})
    conflict_audit = deep_get(candidate, ("conflict_audit",), {})
    review = deep_get(candidate, ("review",), {})
    status = deep_get(candidate, ("status",), {})
    conversion_target = deep_get(candidate, ("conversion_target",), {})
    copyright = deep_get(candidate, ("copyright",), {})
    gaps = required_field_gaps(candidate)
    issues = blocking_issues(candidate, gaps)
    tree_node_id = string_value(classification.get("tree_node_id"))
    canonical_node_id = string_value(classification.get("canonical_node_id") or tree_node_id)
    status_value = candidate_status(candidate, issues)
    candidate_id = string_value(candidate.get("candidate_id"))
    formal = formal_index.get(candidate_id)
    if formal:
        status_value = "accepted_for_draft"
    workflow = workflow_for_candidate(candidate, status_value, formal, rebuilt_archive_index.get(candidate_id))

    return {
        "candidate_id": candidate_id,
        "research_task_id": string_value(candidate.get("research_task_id")),
        "partition_id": string_value(classification.get("partition_id")),
        "tree_node_id": tree_node_id,
        "tree_path": string_value(classification.get("tree_path")),
        "canonical_node_id": canonical_node_id,
        "claim": string_value(claim.get("statement")),
        "title": string_value(claim.get("normalized_claim") or candidate.get("candidate_id")),
        "normalized_claim": string_value(claim.get("normalized_claim")),
        "evidence_summary": string_value(claim.get("evidence_summary")),
        "interpretation_notes": string_value(claim.get("interpretation_notes")),
        "domain": string_value(classification.get("domain")),
        "subdomain": string_value(classification.get("subdomain")),
        "rule_type": string_value(classification.get("rule_type")),
        "used_for": list_value(classification.get("used_for")),
        "source_count": len(source_refs),
        "source_quality_score": source_quality.get("score", 0),
        "source_refs": source_refs,
        "source_quality": {
            "overall_reliability": normalize_confidence(source_quality.get("overall_reliability"), "low"),
            "score": source_quality.get("score", 0),
            "score_version": string_value(source_quality.get("score_version")),
            "primary_source_count": source_quality.get("primary_source_count", 0),
            "supporting_source_count": source_quality.get("supporting_source_count", 0),
            "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
            "mandatory_downgrades": list_value(source_quality.get("mandatory_downgrades")),
            "limitations": list_value(source_quality.get("limitations")),
        },
        "applicable_scope": " / ".join(
            string_value(applicability.get(key), "general")
            for key in ("market", "asset", "timeframe", "data_granularity", "project_type")
        ),
        "not_applicable_scope": list_value(applicability.get("not_applicable_when")),
        "applies_when": list_value(applicability.get("applies_when")),
        "not_applicable_when": list_value(applicability.get("not_applicable_when")),
        "assumptions": list_value(applicability.get("assumptions")),
        "limitations": list_value(applicability.get("limitations")),
        "conflict_status": normalize_conflict_status(conflict_audit.get("conflict_status"), "unchecked"),
        "conflict_audit": {
            "conflict_status": normalize_conflict_status(conflict_audit.get("conflict_status"), "unchecked"),
            "checked_against": list_value(conflict_audit.get("checked_against")),
            "conflicts": list_value(conflict_audit.get("conflicts")),
            "resolution_summary": string_value(conflict_audit.get("resolution_summary")),
            "approval_allowed": bool(conflict_audit.get("approval_allowed", False)),
        },
        "confidence": normalize_confidence(review.get("confidence"), "low"),
        "freshness": normalize_freshness(review.get("freshness"), "stable"),
        "review_status": string_value(status.get("review_status"), "proposed"),
        "ingestion_decision": string_value(status.get("ingestion_decision"), "hold"),
        "candidate_status": status_value,
        "workflow": workflow,
        "decision_reason": string_value(status.get("decision_reason")),
        "reviewer": review.get("reviewer"),
        "reviewed_at": review.get("reviewed_at"),
        "open_questions": list_value(review.get("open_questions")),
        "audit_log": list_value(review.get("audit_log")),
        "conversion_target": {
            "proposed_knowledge_id": string_value(conversion_target.get("proposed_knowledge_id")),
            "target_schema": string_value(conversion_target.get("target_schema"), "cek_ta_knowledge_item"),
            "target_review_status": "draft",
            "skill_candidate": bool(conversion_target.get("skill_candidate", False)),
            "eval_case_candidate": bool(conversion_target.get("eval_case_candidate", False)),
        },
        "knowledge_preview": {
            "proposed_knowledge_id": string_value(conversion_target.get("proposed_knowledge_id")),
            "target_review_status": "draft",
            "domain": string_value(classification.get("domain")),
            "subdomain": string_value(classification.get("subdomain")),
            "tree_node_id": tree_node_id,
            "canonical_node_id": canonical_node_id,
            "source_count": len(source_refs),
            "conflict_status": normalize_conflict_status(conflict_audit.get("conflict_status"), "unchecked"),
            "missing_fields": gaps,
            "blocking_issues": issues,
        },
        "copyright": {
            "stores_full_text": bool(copyright.get("stores_full_text", False)),
            "stores_long_quote": bool(copyright.get("stores_long_quote", False)),
            "summary_only": bool(copyright.get("summary_only", True)),
            "license_notes": copyright.get("license_notes"),
            "reuse_risk": string_value(copyright.get("reuse_risk"), "medium"),
        },
        "source_path": rel_path(path),
        "updated_at": string_value(status.get("updated_at")),
    }


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    formal_index = load_formal_knowledge_index()
    formal_knowledge_ids = load_formal_knowledge_ids()
    raw_candidates: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(CANDIDATE_ROOT.glob("**/*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(raw, dict):
            raise ValueError(f"{rel_path(path)} must contain a JSON object.")
        raw_candidates.append((path, raw))

    rebuilt_archive_index = build_rebuilt_archive_index(raw_candidates, formal_index, formal_knowledge_ids)
    for path, raw in raw_candidates:
        candidate_id = string_value(raw.get("candidate_id"))
        if not candidate_id:
            raise ValueError(f"{rel_path(path)} missing candidate_id.")
        if candidate_id in seen_ids:
            raise ValueError(f"Duplicate candidate_id: {candidate_id}")
        seen_ids.add(candidate_id)
        candidates.append(normalize_candidate(raw, path, formal_index, rebuilt_archive_index))
    return sorted(candidates, key=lambda value: str(value["candidate_id"]))


def render_typescript(candidates: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = json.dumps(candidates, ensure_ascii=False, indent=2)
    return (
        "import type { IngestionCandidate } from '../types'\n\n"
        "// Generated by codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py.\n"
        "// Do not edit by hand; update rag/candidates/**/*.json and regenerate.\n"
        f"export const phase23CandidateFixtureGeneratedAt = {json.dumps(generated_at)}\n\n"
        f"export const phase23Candidates: IngestionCandidate[] = {payload}\n"
    )


def render_json_fixture(candidates: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "schema_version": "phase50.static_fixture.v1",
        "generated_at": generated_at,
        "source": "codex-expert-kit/rag/candidates/**/*.json",
        "count": len(candidates),
        "items": candidates,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    candidates = load_candidates()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(OUTPUT_PATH, render_typescript(candidates))
    atomic_write_text(JSON_OUTPUT_PATH, render_json_fixture(candidates))
    print(f"wrote {rel_path(OUTPUT_PATH)} and {rel_path(JSON_OUTPUT_PATH)} with {len(candidates)} candidates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
