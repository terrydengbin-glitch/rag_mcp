from __future__ import annotations

from math import ceil

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from .errors import error_response, ok_response
from .services import (
    candidate_checklist,
    candidates_path,
    children_for,
    filter_candidates,
    filter_items,
    item_card,
    knowledge_items_path,
    load_candidates,
    load_index,
    node_by_id,
    tree_nodes,
)

app = FastAPI(title="CEK-TA KnowledgeTree API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5188",
        "http://127.0.0.1:5191",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5188",
        "http://localhost:5191",
    ],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    try:
        load_index.cache_clear()
        load_index()
        index_loaded = True
    except Exception:
        index_loaded = False
    return ok_response(
        {
            "service": "cek-ta-knowledge-tree-api",
            "status": "healthy" if index_loaded else "degraded",
            "read_only": True,
            "index_loaded": index_loaded,
            "knowledge_items_path": str(knowledge_items_path()),
            "resolver": "codex-expert-kit/core/path_resolver.py",
        },
        source="healthcheck",
    )


@app.get("/api/knowledge-tree/roots")
def roots():
    return ok_response({"roots": [node for node in tree_nodes() if node["level"] == 1]})


@app.get("/api/knowledge-tree/nodes/{node_id}")
def node_detail(node_id: str):
    node = node_by_id(node_id)
    if not node:
        return error_response("NODE_NOT_FOUND", "Knowledge tree node not found.", 404, {"node_id": node_id})
    return ok_response({"node": node})


@app.get("/api/knowledge-tree/nodes/{node_id}/children")
def node_children(node_id: str, include_l3: bool = False):
    node = node_by_id(node_id)
    if not node:
        return error_response("NODE_NOT_FOUND", "Knowledge tree node not found.", 404, {"node_id": node_id})
    return ok_response({"node_id": node["id"], "children": children_for(node_id, include_l3=include_l3)})


@app.get("/api/knowledge-tree/nodes/{node_id}/knowledge")
def node_knowledge(
    node_id: str,
    query: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(20),
    include_descendants: bool = True,
):
    if page_size not in {20, 50, 100}:
        return error_response("INVALID_QUERY", "page_size must be one of 20, 50, 100.", 400, {"page_size": page_size})
    node = node_by_id(node_id)
    if not node:
        return error_response("NODE_NOT_FOUND", "Knowledge tree node not found.", 404, {"node_id": node_id})
    cards = [item_card(item) for item in filter_items(node_id, query=query, include_descendants=include_descendants)]
    total = len(cards)
    start = (page - 1) * page_size
    items = cards[start : start + page_size]
    return ok_response(
        {
            "node": node,
            "knowledge": {
                "items": items,
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": max(1, ceil(total / page_size)),
                "sort": "relevance",
                "has_next": start + page_size < total,
                "has_prev": page > 1,
            },
        }
    )


@app.get("/api/knowledge-items/{knowledge_id}")
def knowledge_item(knowledge_id: str):
    item = next((item for item in load_index().get("items", []) if item.get("knowledge_id") == knowledge_id), None)
    if not item:
        return error_response("ITEM_NOT_FOUND", "Knowledge item not found.", 404, {"knowledge_id": knowledge_id})
    metadata = item.get("metadata", {})
    applicability = item.get("applicability", {})
    content = item.get("content", {})
    machine_gate = item.get("machine_gate", {})
    llm_usage_policy = item.get("llm_usage_policy", {})
    return ok_response(
        {
            "item": {
                "id": item.get("knowledge_id"),
                "title": item.get("title"),
                "summary": content.get("statement", ""),
                "content": content.get("rationale", ""),
                "tree_node_id": metadata.get("tree_node_id"),
                "canonical_node_id": metadata.get("canonical_node_id") or metadata.get("tree_node_id"),
                "claim_type": metadata.get("claim_type", "methodological_constraint"),
                "classification_notes": metadata.get("classification_notes", ""),
                "applicable_scope": " / ".join(applicability.get("applies_when", [])),
                "not_applicable_scope": " / ".join(applicability.get("not_applicable_when", [])),
                "llm_usage_policy": {
                    "allowed": llm_usage_policy.get("allowed", []),
                    "not_allowed": llm_usage_policy.get("not_allowed", []),
                    "required_context": llm_usage_policy.get("required_context", []),
                    "fallback_behavior": llm_usage_policy.get("fallback_behavior", "cite_with_caveat"),
                },
                "machine_gate": {
                    "default_guidance": machine_gate.get("default_guidance", "deny"),
                    "reason": machine_gate.get("reason", ""),
                    "requires_human_escalation": machine_gate.get("requires_human_escalation", True),
                    "blocking_reasons": machine_gate.get("blocking_reasons", []),
                    "checked_at": machine_gate.get("checked_at", ""),
                    "gate_version": machine_gate.get("gate_version", "1.0.0"),
                },
                "recommended_extra_sources_count": len(item.get("recommended_extra_sources", [])),
                "sources": item.get("source_evidence", []),
                "conflict_handling": item.get("conflict_audit", {}).get("resolution_summary", "No known direct conflict."),
                "status": item.get("review", {}).get("review_status", "draft"),
                "review_notes": item.get("review", {}).get("review_notes", []),
            }
        }
    )


@app.get("/api/knowledge-tree/nodes/{node_id}/audit-summary")
def audit_summary(node_id: str):
    node = node_by_id(node_id)
    if not node:
        return error_response("NODE_NOT_FOUND", "Knowledge tree node not found.", 404, {"node_id": node_id})
    cards = [item_card(item) for item in filter_items(node_id)]
    candidates = filter_candidates(tree_node_id=node["id"])
    return ok_response(
        {
            "summary": {
                "node_id": node["id"],
                "approved_count": sum(1 for item in cards if item["status"] == "approved"),
                "reviewed_count": sum(1 for item in cards if item["status"] == "reviewed"),
                "knowledge_count": len(cards),
                "candidate_count": len(candidates),
                "source_count": sum(item["source_count"] for item in cards),
                "open_gap_count": 0,
                "conflict_count": sum(1 for item in cards if item["conflict_status"] not in {"none", "resolved"}),
                "stale_count": sum(1 for item in cards if item["freshness_status"] in {"stale", "deprecated"}),
                "next_actions": [
                    {"label": "查看候选", "target": f"/ingestion?tree_node_id={node['id']}", "kind": "route"},
                    {"label": "带入 SearchLab 检索测试", "target": f"/search-lab?canonical_node_id={node['id']}", "kind": "route"},
                ],
                "manual_review_hints": ["draft/candidate 不可作为默认指导", "外部项目回灌不可直写"],
            }
        }
    )


@app.get("/api/candidates")
def candidates(
    q: str = "",
    partition_id: str | None = None,
    tree_node_id: str | None = None,
    candidate_status: str | None = None,
    conflict_status: str | None = None,
    risk_level: str | None = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    try:
        load_candidates.cache_clear()
        filtered = filter_candidates(
            q=q,
            partition_id=partition_id,
            tree_node_id=tree_node_id,
            candidate_status=candidate_status,
            conflict_status=conflict_status,
            risk_level=risk_level,
        )
    except FileNotFoundError:
        return error_response(
            "CANDIDATE_INDEX_NOT_FOUND",
            "Candidate directory not found.",
            404,
            {"candidate_path": str(candidates_path())},
        )
    total = len(filtered)
    return ok_response(
        {
            "items": filtered[offset : offset + limit],
            "total": total,
            "limit": limit,
            "offset": offset,
            "source": "api",
            "candidate_path": str(candidates_path()),
        },
        source="candidate_files",
    )


@app.get("/api/candidates/{candidate_id}")
def candidate_detail(candidate_id: str):
    try:
        load_candidates.cache_clear()
        item = next((candidate for candidate in load_candidates() if candidate.get("candidate_id") == candidate_id), None)
    except FileNotFoundError:
        return error_response(
            "CANDIDATE_INDEX_NOT_FOUND",
            "Candidate directory not found.",
            404,
            {"candidate_path": str(candidates_path())},
        )
    if not item:
        return error_response("CANDIDATE_NOT_FOUND", "Candidate not found.", 404, {"candidate_id": candidate_id})
    return ok_response(
        {
            "item": item,
            "sources": item.get("source_refs", []),
            "checklist": candidate_checklist(item),
            "source": "api",
        },
        source="candidate_files",
    )
