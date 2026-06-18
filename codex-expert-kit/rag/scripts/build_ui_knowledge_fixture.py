"""Build the Vue3 formal knowledge fixture from the official knowledge index."""

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

from path_resolver import resolve_repo_path  # noqa: E402


INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
OUTPUT_PATH = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
JSON_OUTPUT_PATH = resolve_repo_path("ui", "public", "data", "formalKnowledgeItems.json", start_file=__file__)


def atomic_write_text(path: Path, text: str) -> None:
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(text, encoding="utf-8", newline="\n")
    temp_path.replace(path)


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


def normalize_conflict_status(value: Any, default: str = "none") -> str:
    raw = string_value(value, default)
    if raw in {"none", "potential", "confirmed", "resolved", "deprecated_by_conflict"}:
        return raw
    if raw in {"none_known_in_visible_context", "unchecked"}:
        return "none"
    return default


def normalize_claim_type(value: Any, default: str = "methodological_constraint") -> str:
    raw = string_value(value, default)
    allowed = {
        "methodological_constraint",
        "risk_boundary_rule",
        "execution_safety_rule",
        "data_quality_rule",
        "backtest_validity_rule",
        "rag_governance_rule",
        "mcp_contract_rule",
        "knowledge_governance_rule",
        "project_integration_rule",
        "llm_training_rule",
        "llm_eval_rule",
        "training_data_schema_rule",
        "ai_security_rule",
        "ai_governance_rule",
        "llmops_release_rule",
    }
    if raw in allowed:
        return raw
    mapping = {
        "definition": "methodological_constraint",
        "audit_gate": "methodological_constraint",
        "anti_pattern": "methodological_constraint",
        "architecture_rule": "ai_governance_rule",
        "cost_audit_boundary_rule": "risk_boundary_rule",
        "default_guidance_block": "risk_boundary_rule",
        "procedure_boundary": "risk_boundary_rule",
        "risk_normalized_metric_definition": "methodological_constraint",
    }
    return mapping.get(raw, default)


def list_value(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def normalize_source(source: dict[str, Any], knowledge_id: str) -> dict[str, Any]:
    return {
        "source_id": string_value(source.get("source_id"), f"{knowledge_id}:source"),
        "title": string_value(source.get("source_title") or source.get("title"), "untitled source"),
        "url": source.get("source_url") or source.get("url"),
        "source_type": string_value(source.get("source_type"), "other"),
        "publisher": string_value(source.get("publisher"), "unknown"),
        "published_at": source.get("published_at"),
        "accessed_at": string_value(source.get("accessed_at")),
        "reliability": normalize_confidence(source.get("reliability"), "medium"),
        "score": source.get("score", 0),
        "cited_by": [knowledge_id],
        "stale": string_value(source.get("freshness"), "stable") == "deprecated",
    }


def normalize_conflict(conflict: dict[str, Any], knowledge_id: str) -> dict[str, Any]:
    return {
        "conflict_id": string_value(conflict.get("conflict_id"), f"{knowledge_id}:conflict"),
        "conflict_type": string_value(conflict.get("conflict_type"), "scope_conflict"),
        "severity": string_value(conflict.get("severity"), "warning"),
        "left_id": string_value(conflict.get("left_id"), knowledge_id),
        "right_id": string_value(conflict.get("right_id") or conflict.get("knowledge_id")),
        "left_source_reliability": normalize_confidence(conflict.get("left_source_reliability"), "medium"),
        "right_source_reliability": normalize_confidence(conflict.get("right_source_reliability"), "medium"),
        "scope_compare": string_value(conflict.get("scope_compare") or conflict.get("overlap_scope")),
        "version_compare": string_value(conflict.get("version_compare")),
        "resolution": string_value(conflict.get("resolution")),
        "review_decision": string_value(conflict.get("review_decision"), "pending"),
    }


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    knowledge_id = string_value(item.get("knowledge_id"))
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    applicability = item.get("applicability") if isinstance(item.get("applicability"), dict) else {}
    content = item.get("content") if isinstance(item.get("content"), dict) else {}
    review = item.get("review") if isinstance(item.get("review"), dict) else {}
    conflict_audit = item.get("conflict_audit") if isinstance(item.get("conflict_audit"), dict) else {}
    llm_usage_policy = item.get("llm_usage_policy") if isinstance(item.get("llm_usage_policy"), dict) else {}
    machine_gate = item.get("machine_gate") if isinstance(item.get("machine_gate"), dict) else {}
    sources = [normalize_source(source, knowledge_id) for source in list_value(item.get("source_evidence")) if isinstance(source, dict)]
    conflicts = [
        normalize_conflict(conflict, knowledge_id)
        for conflict in list_value(conflict_audit.get("conflicts"))
        if isinstance(conflict, dict)
    ]
    return {
        "knowledge_id": knowledge_id,
        "title": string_value(item.get("title") or content.get("title") or knowledge_id),
        "domain": string_value(metadata.get("domain")),
        "subdomain": string_value(metadata.get("subdomain")),
        "tree_node_id": string_value(metadata.get("tree_node_id")),
        "tree_path": string_value(metadata.get("tree_path")),
        "canonical_node_id": string_value(metadata.get("canonical_node_id") or metadata.get("tree_node_id")),
        "canonical_tree_path": string_value(metadata.get("canonical_tree_path") or metadata.get("tree_path")),
        "rule_type": string_value(metadata.get("rule_type"), "principle"),
        "claim_type": normalize_claim_type(metadata.get("claim_type"), "methodological_constraint"),
        "classification_notes": string_value(metadata.get("classification_notes")),
        "source_type": sources[0]["source_type"] if sources else "other",
        "statement": string_value(content.get("statement") or item.get("statement")),
        "rationale": string_value(content.get("rationale") or content.get("citation_notes")),
        "applies_to": {
            "market": string_value(applicability.get("market"), "general"),
            "asset": string_value(applicability.get("asset"), "general"),
            "timeframe": string_value(applicability.get("timeframe"), "general"),
            "data_granularity": string_value(applicability.get("data_granularity"), "general"),
            "project_type": string_value(applicability.get("project_type"), "general"),
        },
        "assumptions": list_value(applicability.get("assumptions")),
        "not_applicable_when": list_value(applicability.get("not_applicable_when")),
        "sources": sources,
        "conflicts": conflicts,
        "resolution": string_value(conflict_audit.get("resolution_summary") or content.get("conflict_resolution")),
        "confidence": normalize_confidence(review.get("confidence"), "medium"),
        "freshness": normalize_freshness(review.get("freshness"), "stable"),
        "review_status": string_value(review.get("review_status"), "draft"),
        "conflict_status": normalize_conflict_status(conflict_audit.get("conflict_status"), "none"),
        "llm_usage_policy": {
            "allowed": list_value(llm_usage_policy.get("allowed")),
            "not_allowed": list_value(llm_usage_policy.get("not_allowed")),
            "required_context": list_value(llm_usage_policy.get("required_context")),
            "fallback_behavior": string_value(llm_usage_policy.get("fallback_behavior"), "cite_with_caveat"),
        },
        "machine_gate": {
            "default_guidance": string_value(machine_gate.get("default_guidance"), "deny"),
            "reason": string_value(machine_gate.get("reason")),
            "requires_human_escalation": bool(machine_gate.get("requires_human_escalation", True)),
            "blocking_reasons": list_value(machine_gate.get("blocking_reasons")),
            "checked_at": string_value(machine_gate.get("checked_at")),
            "gate_version": string_value(machine_gate.get("gate_version"), "1.0.0"),
        },
        "recommended_extra_sources_count": len(list_value(item.get("recommended_extra_sources"))),
        "updated_at": string_value(review.get("updated_at") or review.get("reviewed_at")),
        "version_history": list_value(item.get("version_history")),
    }


def load_items() -> list[dict[str, Any]]:
    payload = json.loads(INDEX_PATH.read_text(encoding="utf-8-sig"))
    items = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain an items array.")
    return [normalize_item(item) for item in items if isinstance(item, dict)]


def render_typescript(items: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = json.dumps(items, ensure_ascii=False, indent=2)
    return (
        "import type { KnowledgeItem } from '../types'\n\n"
        "// Generated by codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py.\n"
        "// Do not edit by hand; update rag/knowledge/**/*.json and regenerate.\n"
        f"export const formalKnowledgeFixtureGeneratedAt = {json.dumps(generated_at)}\n\n"
        f"export const formalKnowledgeItems: KnowledgeItem[] = {payload}\n"
    )


def render_json_fixture(items: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "schema_version": "phase50.static_fixture.v1",
        "generated_at": generated_at,
        "source": "codex-expert-kit/rag/indexes/knowledge_items.json",
        "count": len(items),
        "items": items,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    items = load_items()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(OUTPUT_PATH, render_typescript(items))
    atomic_write_text(JSON_OUTPUT_PATH, render_json_fixture(items))
    print(f"wrote {OUTPUT_PATH} and {JSON_OUTPUT_PATH} with {len(items)} formal knowledge items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
