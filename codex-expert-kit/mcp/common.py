"""Shared helpers for CEK-TA Knowledge MCP draft tools.

The draft tools are intentionally dependency-free and read-only. They operate
on in-memory knowledge item objects or JSON files supplied by a future adapter.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


MAX_TOP_K = 20
MAX_QUERY_CHARS = 2000

FORBIDDEN_PERMISSIONS = {
    "write_knowledge",
    "approve_knowledge",
    "submit_contribution",
    "trade",
    "read_account",
    "read_secret",
}

SUPPORTED_FILTERS = {
    "tree_node_id",
    "tree_path",
    "tree_path_prefix",
    "canonical_node_id",
    "canonical_tree_path",
    "canonical_tree_path_prefix",
    "partition_id",
    "domain",
    "subdomain",
    "rule_type",
    "review_status",
    "confidence",
    "freshness",
    "conflict_status",
    "source_type",
}

DEFAULT_INCLUDE = {
    "sources": True,
    "conflicts": True,
    "deprecated": False,
    "draft": False,
    "reviewed": True,
    "default_guidance_only": False,
}


PARTITIONS = [
    {
        "partition_id": "KB_01_QUANT_FOUNDATION",
        "name": "Quant Foundation",
        "domain": "quant_trading",
        "purpose": "General trading-system architecture, signal flow, risk, sizing, costs, and execution principles.",
    },
    {
        "partition_id": "KB_02_KLINE_STRATEGY",
        "name": "Kline Strategy",
        "domain": "kline_strategy",
        "purpose": "K-line trend, entries, multi-timeframe alignment, structure levels, indicators, SL/TP design.",
    },
    {
        "partition_id": "KB_03_MARKET_MICROSTRUCTURE",
        "name": "Market Microstructure",
        "domain": "market_microstructure",
        "purpose": "Order flow, liquidity, spreads, order book behavior, trade prints, and microstructure features.",
    },
    {
        "partition_id": "KB_04_BACKTEST",
        "name": "Backtest",
        "domain": "backtest",
        "purpose": "Backtest credibility, bias detection, data quality, metrics, costs, and reproducibility.",
    },
    {
        "partition_id": "KB_05_REPLAY_SIMULATION",
        "name": "Replay and Simulation",
        "domain": "replay_simulation",
        "purpose": "Market replay, event-driven simulation, fill models, and paper-trading fidelity.",
    },
    {
        "partition_id": "KB_06_LIVE_EXECUTION",
        "name": "Live Execution",
        "domain": "live_trading",
        "purpose": "Live readiness, exchange adapters, order state machines, reconciliation, and incident response.",
    },
    {
        "partition_id": "KB_07_TRADE_ANALYSIS",
        "name": "Trade Analysis",
        "domain": "trade_analysis",
        "purpose": "Trade quality metrics, labels, failure modes, bad-case taxonomy, and iteration loops.",
    },
    {
        "partition_id": "KB_08_LLM_TRAINING",
        "name": "LLM Training",
        "domain": "llm_training",
        "purpose": "RAG, SFT, DPO, evals, dataset cards, preference data, and training workflow.",
    },
    {
        "partition_id": "KB_09_RAG_ENGINEERING",
        "name": "RAG Engineering",
        "domain": "rag_engineering",
        "purpose": "Metadata, chunking, retrieval policy, source quality, reranking, citation, and MCP integration.",
    },
    {
        "partition_id": "KB_10_PROJECT_RUNBOOKS",
        "name": "Project Runbooks",
        "domain": "project_runbooks",
        "purpose": "Sanitized project adapters, task cards, audit reports, incident summaries, and reusable runbooks.",
    },
]


def error(code: str, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {"code": code, "message": message, "field": field, "details": details or {}}


def base_response(request_id: Optional[str], status: str = "ok") -> Dict[str, Any]:
    return {
        "request_id": request_id,
        "status": status,
        "results": [],
        "warnings": [],
        "applied_filters": {},
        "audit": {
            "retrieval_policy_version": "0.1.0",
            "result_count": 0,
            "blocked_count": 0,
            "returned_review_statuses": [],
            "returned_conflict_statuses": [],
        },
        "errors": [],
    }


def validate_read_only_permission(request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    requested = request.get("requested_permission") or request.get("permission")
    if isinstance(requested, str) and requested in FORBIDDEN_PERMISSIONS:
        return error("permission_denied", f"Permission '{requested}' is not allowed by Phase 3 read-only MCP.", "requested_permission")
    if isinstance(requested, list):
        denied = sorted(set(requested) & FORBIDDEN_PERMISSIONS)
        if denied:
            return error("permission_denied", f"Permissions are not allowed by Phase 3 read-only MCP: {', '.join(denied)}.", "requested_permission")
    return None


def load_knowledge_items(knowledge_items: Optional[List[Dict[str, Any]]] = None, knowledge_items_path: Optional[str] = None) -> List[Dict[str, Any]]:
    if knowledge_items is not None:
        return list(knowledge_items)
    if not knowledge_items_path:
        return []
    path = Path(knowledge_items_path)
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    if isinstance(data, list):
        return data
    raise ValueError("knowledge_items_path must contain a JSON list or an object with an 'items' list.")


def deep_get(item: Dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = item
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def metadata_value(item: Dict[str, Any], field: str) -> Any:
    if field == "source_type":
        return first_source(item).get("source_type")
    mapping = {
        "tree_node_id": "metadata.tree_node_id",
        "tree_path": "metadata.tree_path",
        "canonical_node_id": "metadata.canonical_node_id",
        "canonical_tree_path": "metadata.canonical_tree_path",
        "partition_id": "metadata.partition_id",
        "domain": "metadata.domain",
        "subdomain": "metadata.subdomain",
        "rule_type": "metadata.rule_type",
        "review_status": "review.review_status",
        "confidence": "review.confidence",
        "freshness": "review.freshness",
        "conflict_status": "conflict_audit.conflict_status",
    }
    return deep_get(item, mapping[field])


def first_source(item: Dict[str, Any]) -> Dict[str, Any]:
    evidence = item.get("source_evidence") or []
    return evidence[0] if evidence and isinstance(evidence[0], dict) else {}


def machine_gate_for_item(item: Dict[str, Any]) -> Dict[str, Any]:
    gate = item.get("machine_gate")
    if isinstance(gate, dict) and gate.get("default_guidance"):
        return gate
    review_status = deep_get(item, "review.review_status", "")
    default_allowed_raw = deep_get(item, "review.default_guidance_allowed", None)
    default_allowed = True if default_allowed_raw is None and review_status == "approved" else bool(default_allowed_raw)
    conflict_status = deep_get(item, "conflict_audit.conflict_status", "")
    freshness = deep_get(item, "review.freshness", "")
    source_count = len(item.get("source_evidence") or [])
    reliability = deep_get(item, "source_quality.overall_reliability", "")
    if (
        review_status == "approved"
        and default_allowed
        and conflict_status in ("none", "resolved")
        and freshness != "deprecated"
        and source_count > 0
        and reliability in ("high", "medium")
    ):
        return {
            "default_guidance": "allow",
            "reason": "Compatibility gate inferred allow from approved status and source/conflict checks.",
            "requires_human_escalation": False,
            "blocking_reasons": [],
            "checked_at": "",
            "gate_version": "compat",
        }
    if review_status == "reviewed" and conflict_status in ("none", "resolved") and source_count > 0:
        return {
            "default_guidance": "caveat_only",
            "reason": "Compatibility gate inferred caveat_only from reviewed status.",
            "requires_human_escalation": True,
            "blocking_reasons": ["review_status_not_approved"],
            "checked_at": "",
            "gate_version": "compat",
        }
    return {
        "default_guidance": "deny",
        "reason": "Compatibility gate denied default guidance.",
        "requires_human_escalation": True,
        "blocking_reasons": ["machine_gate_missing_or_quality_gate_failed"],
        "checked_at": "",
        "gate_version": "compat",
    }


def normalize_include(include: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged = dict(DEFAULT_INCLUDE)
    if isinstance(include, dict):
        merged.update({k: bool(v) for k, v in include.items() if k in merged})
    return merged


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9]+|[\u4e00-\u9fff]", text.lower())


def item_text(item: Dict[str, Any]) -> str:
    source_text = " ".join(
        " ".join(
            str(source.get(field, ""))
            for field in ("source_title", "source_type", "publisher", "evidence_summary")
        )
        for source in item.get("source_evidence", [])
        if isinstance(source, dict)
    )
    fields = [
        item.get("knowledge_id", ""),
        item.get("title", ""),
        deep_get(item, "content.statement", ""),
        deep_get(item, "content.rationale", ""),
        deep_get(item, "content.citation_notes", ""),
        " ".join(deep_get(item, "content.procedure", []) or []),
        " ".join(deep_get(item, "content.examples", []) or []),
        " ".join(deep_get(item, "content.anti_patterns", []) or []),
        " ".join(deep_get(item, "assumptions", []) or []),
        source_text,
        deep_get(item, "metadata.tree_node_id", ""),
        deep_get(item, "metadata.tree_path", ""),
        deep_get(item, "metadata.canonical_node_id", ""),
        deep_get(item, "metadata.canonical_tree_path", ""),
        deep_get(item, "metadata.domain", ""),
        deep_get(item, "metadata.subdomain", ""),
    ]
    return " ".join(str(value) for value in fields if value)


def text_score(query: str, item: Dict[str, Any]) -> float:
    q_tokens = tokenize(query)
    if not q_tokens:
        return 0.0
    text_tokens = set(tokenize(item_text(item)))
    hits = sum(1 for token in q_tokens if token in text_tokens)
    return hits / max(len(q_tokens), 1)


def filter_items(
    items: Iterable[Dict[str, Any]],
    filters: Dict[str, Any],
    project_context: Dict[str, Any],
    include: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[str], List[Dict[str, Any]]]:
    warnings: List[str] = []
    blocked: List[Dict[str, Any]] = []
    accepted: List[Dict[str, Any]] = []

    for item in items:
        review_status = deep_get(item, "review.review_status")
        freshness = deep_get(item, "review.freshness")
        conflict_status = deep_get(item, "conflict_audit.conflict_status")
        project_binding = deep_get(item, "metadata.project_binding", "none")
        machine_gate = machine_gate_for_item(item)
        default_guidance = machine_gate.get("default_guidance")

        if include.get("default_guidance_only") and default_guidance != "allow":
            item["_blocked_reason"] = f"machine_gate_{default_guidance}"
            blocked.append(item)
            continue

        if review_status == "rejected":
            item["_blocked_reason"] = "review_status_rejected"
            blocked.append(item)
            continue
        if review_status == "deprecated" or freshness == "deprecated":
            if not include["deprecated"]:
                item["_blocked_reason"] = "deprecated"
                blocked.append(item)
                continue
        if review_status == "draft" and not include["draft"]:
            item["_blocked_reason"] = "review_status_draft"
            blocked.append(item)
            continue
        if review_status == "reviewed" and not include["reviewed"]:
            item["_blocked_reason"] = "review_status_reviewed_not_included"
            blocked.append(item)
            continue
        if conflict_status == "confirmed":
            item["_blocked_reason"] = "confirmed_conflict"
            blocked.append(item)
            continue
        if not item.get("source_evidence"):
            item["_blocked_reason"] = "missing_source_evidence"
            blocked.append(item)
            continue
        if project_binding not in ("none", "sanitized_project_case"):
            if project_binding != project_context.get("project_name"):
                item["_blocked_reason"] = "project_binding_mismatch"
                blocked.append(item)
                continue

        mismatch = False
        for field, expected_values in filters.items():
            if field not in SUPPORTED_FILTERS:
                continue
            if expected_values is None:
                continue
            if field == "tree_path_prefix":
                prefixes = expected_values if isinstance(expected_values, list) else [expected_values]
                tree_path = str(deep_get(item, "metadata.tree_path", ""))
                if prefixes and not any(tree_path.startswith(str(prefix)) for prefix in prefixes):
                    mismatch = True
                    break
                continue
            if field == "canonical_tree_path_prefix":
                prefixes = expected_values if isinstance(expected_values, list) else [expected_values]
                canonical_tree_path = str(deep_get(item, "metadata.canonical_tree_path", ""))
                if prefixes and not any(canonical_tree_path.startswith(str(prefix)) for prefix in prefixes):
                    mismatch = True
                    break
                continue
            if not isinstance(expected_values, list):
                expected_values = [expected_values]
            if field == "canonical_node_id":
                actual_values = {
                    deep_get(item, "metadata.canonical_node_id"),
                    deep_get(item, "metadata.tree_node_id"),
                }
                if expected_values and not actual_values.intersection(set(expected_values)):
                    mismatch = True
                    break
                continue
            if expected_values and metadata_value(item, field) not in expected_values:
                mismatch = True
                break
        if mismatch:
            continue

        for field in ("market", "asset", "timeframe", "data_granularity", "project_type"):
            expected = project_context.get(field)
            actual = deep_get(item, f"applicability.{field}")
            if expected and actual and actual not in (expected, "general"):
                mismatch = True
                break
        if mismatch:
            continue

        if review_status == "reviewed":
            warnings.append(f"{item.get('knowledge_id')} is reviewed but not approved.")
        if conflict_status == "potential":
            warnings.append(f"{item.get('knowledge_id')} has potential conflicts.")
        if conflict_status == "resolved":
            warnings.append(f"{item.get('knowledge_id')} has resolved conflicts; check resolution.")

        accepted.append(item)

    return accepted, warnings, blocked


def shape_result(item: Dict[str, Any], score: float) -> Dict[str, Any]:
    source = first_source(item)
    review_status = deep_get(item, "review.review_status", "")
    conflict_status = deep_get(item, "conflict_audit.conflict_status", "")
    freshness = deep_get(item, "review.freshness", "")
    machine_gate = machine_gate_for_item(item)
    default_guidance = machine_gate.get("default_guidance")
    if default_guidance == "allow":
        recommended_next_action = "use_as_guidance"
        acceptance_level = "approved_guidance"
    elif default_guidance == "caveat_only":
        recommended_next_action = "cite_with_caveat"
        acceptance_level = "accepted_reference"
    elif conflict_status in ("potential", "confirmed"):
        recommended_next_action = "review_conflict"
        acceptance_level = "blocked_reference"
    elif freshness == "time_sensitive":
        recommended_next_action = "refresh_source"
        acceptance_level = "accepted_reference"
    elif review_status == "reviewed":
        recommended_next_action = "cite_with_caveat"
        acceptance_level = "accepted_reference"
    else:
        recommended_next_action = "no_default_guidance"
        acceptance_level = "not_accepted"

    statement = deep_get(item, "content.statement", "")
    return {
        "item_id": item.get("knowledge_id", ""),
        "knowledge_id": item.get("knowledge_id", ""),
        "title": item.get("title", ""),
        "claim": statement,
        "partition_id": deep_get(item, "metadata.partition_id", ""),
        "tree_node_id": deep_get(item, "metadata.tree_node_id", ""),
        "tree_path": deep_get(item, "metadata.tree_path", ""),
        "canonical_node_id": deep_get(item, "metadata.canonical_node_id", deep_get(item, "metadata.tree_node_id", "")),
        "canonical_tree_path": deep_get(item, "metadata.canonical_tree_path", deep_get(item, "metadata.tree_path", "")),
        "domain": deep_get(item, "metadata.domain", ""),
        "subdomain": deep_get(item, "metadata.subdomain", ""),
        "rule_type": deep_get(item, "metadata.rule_type", ""),
        "claim_type": deep_get(item, "metadata.claim_type", "methodological_constraint"),
        "classification_notes": deep_get(item, "metadata.classification_notes", ""),
        "summary": statement,
        "source": {
            "title": source.get("source_title", ""),
            "url": source.get("source_url"),
            "source_type": source.get("source_type", ""),
            "publisher": source.get("publisher"),
            "published_at": source.get("published_at"),
            "accessed_at": source.get("accessed_at", ""),
            "version": source.get("version"),
            "reliability": source.get("reliability", ""),
        },
        "citation": {
            "source_id": source.get("source_id", ""),
            "evidence_summary": source.get("evidence_summary", ""),
        },
        "source_refs": item.get("source_evidence", []),
        "source_count": len(item.get("source_evidence", [])),
        "confidence": deep_get(item, "review.confidence", ""),
        "freshness": deep_get(item, "review.freshness", ""),
        "review_status": deep_get(item, "review.review_status", ""),
        "conflict_status": deep_get(item, "conflict_audit.conflict_status", ""),
        "llm_usage_policy": item.get("llm_usage_policy", {}),
        "machine_gate": machine_gate,
        "acceptance_level": acceptance_level,
        "adoption_status": acceptance_level,
        "recommended_extra_sources_count": len(item.get("recommended_extra_sources") or []),
        "applicability": {
            "market": deep_get(item, "applicability.market", ""),
            "asset": deep_get(item, "applicability.asset", ""),
            "timeframe": deep_get(item, "applicability.timeframe", ""),
            "data_granularity": deep_get(item, "applicability.data_granularity", ""),
            "project_type": deep_get(item, "applicability.project_type", ""),
            "applies_when": deep_get(item, "applicability.applies_when", []),
            "not_applicable_when": deep_get(item, "applicability.not_applicable_when", []),
        },
        "applicable_scope": {
            "market": deep_get(item, "applicability.market", ""),
            "asset": deep_get(item, "applicability.asset", ""),
            "timeframe": deep_get(item, "applicability.timeframe", ""),
            "data_granularity": deep_get(item, "applicability.data_granularity", ""),
            "project_type": deep_get(item, "applicability.project_type", ""),
            "applies_when": deep_get(item, "applicability.applies_when", []),
        },
        "not_applicable_scope": deep_get(item, "applicability.not_applicable_when", []),
        "conflict_summary": deep_get(item, "conflict_audit.resolution_summary"),
        "why_matched": {
            "match_type": "lexical",
            "matched_fields": ["query", "metadata", "content"],
            "score": round(score, 4),
            "reasons": ["lexical_token_overlap", "metadata_scope_boost_available"],
            "notes": [],
        },
        "recommended_next_action": recommended_next_action,
        "warnings": [],
        "score": round(score, 4),
    }


def shape_blocked_result(item: Dict[str, Any]) -> Dict[str, Any]:
    reason = item.get("_blocked_reason", "filtered_or_not_allowed")
    return {
        "item_id": item.get("knowledge_id", ""),
        "knowledge_id": item.get("knowledge_id", ""),
        "title": item.get("title", ""),
        "blocked_reason": reason,
        "review_status": deep_get(item, "review.review_status", ""),
        "conflict_status": deep_get(item, "conflict_audit.conflict_status", ""),
        "freshness": deep_get(item, "review.freshness", ""),
        "has_source_refs": bool(item.get("source_evidence")),
        "tree_node_id": deep_get(item, "metadata.tree_node_id", ""),
        "canonical_node_id": deep_get(item, "metadata.canonical_node_id", deep_get(item, "metadata.tree_node_id", "")),
        "recommended_fix": {
            "missing_source_evidence": "add_source_evidence_before_default_guidance",
            "confirmed_conflict": "resolve_conflict_before_default_guidance",
            "deprecated": "replace_with_current_approved_knowledge",
            "review_status_draft": "complete_review_before_default_guidance",
            "review_status_rejected": "do_not_use_rejected_knowledge",
            "project_binding_mismatch": "query_with_matching_project_context_or_use_sanitized_knowledge",
            "machine_gate_caveat_only": "request_audit_mode_or_human_approval_before_default_guidance",
            "machine_gate_deny": "fix_machine_gate_blocking_reasons_before_default_guidance",
        }.get(reason, "review_filter_or_scope"),
        "machine_gate": machine_gate_for_item(item),
    }


def finalize_audit(response: Dict[str, Any]) -> Dict[str, Any]:
    results = response.get("results", [])
    response["audit"]["result_count"] = len(results)
    response["audit"]["returned_review_statuses"] = sorted({item.get("review_status", "") for item in results if item.get("review_status")})
    response["audit"]["returned_conflict_statuses"] = sorted({item.get("conflict_status", "") for item in results if item.get("conflict_status")})
    if response["errors"]:
        response["status"] = "error"
    elif response["warnings"]:
        response["status"] = "warning"
    else:
        response["status"] = "ok"
    return response


def find_item(items: Iterable[Dict[str, Any]], knowledge_id: str) -> Optional[Dict[str, Any]]:
    for item in items:
        if item.get("knowledge_id") == knowledge_id:
            return item
    return None
