"""Draft implementation of the CEK-TA search_expert_knowledge MCP tool."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .common import (
        MAX_QUERY_CHARS,
        MAX_TOP_K,
        SUPPORTED_FILTERS,
        base_response,
        error,
        filter_items,
        finalize_audit,
        load_knowledge_items,
        normalize_include,
        shape_result,
        shape_blocked_result,
        text_score,
        validate_read_only_permission,
    )
except ImportError:  # pragma: no cover - allows direct script execution
    from common import (  # type: ignore
        MAX_QUERY_CHARS,
        MAX_TOP_K,
        SUPPORTED_FILTERS,
        base_response,
        error,
        filter_items,
        finalize_audit,
        load_knowledge_items,
        normalize_include,
        shape_result,
        shape_blocked_result,
        text_score,
        validate_read_only_permission,
    )


def search_expert_knowledge(
    request: Dict[str, Any],
    *,
    knowledge_items: Optional[List[Dict[str, Any]]] = None,
    knowledge_items_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Search CEK-TA knowledge with read-only MCP semantics.

    The current draft uses lightweight lexical scoring so the contract can be
    tested before a real RAGFlow/vector adapter is introduced.
    """

    request_id = request.get("request_id")
    response = base_response(request_id)

    permission_error = validate_read_only_permission(request)
    if permission_error:
        response["errors"].append(permission_error)
        return finalize_audit(response)

    query = str(request.get("query", "")).strip()
    if not query:
        response["errors"].append(error("invalid_input", "query is required.", "query"))
        return finalize_audit(response)
    if len(query) > MAX_QUERY_CHARS:
        response["errors"].append(error("invalid_input", f"query must be <= {MAX_QUERY_CHARS} characters.", "query"))
        return finalize_audit(response)

    top_k = request.get("top_k", 5)
    if not isinstance(top_k, int) or top_k < 1 or top_k > MAX_TOP_K:
        response["errors"].append(error("invalid_input", f"top_k must be an integer from 1 to {MAX_TOP_K}.", "top_k"))
        return finalize_audit(response)

    filters = request.get("filters") or {}
    if not isinstance(filters, dict):
        response["errors"].append(error("invalid_input", "filters must be an object.", "filters"))
        return finalize_audit(response)
    unsupported = sorted(set(filters) - SUPPORTED_FILTERS)
    if unsupported:
        response["errors"].append(error("unsupported_filter", f"Unsupported filters: {', '.join(unsupported)}.", "filters"))
        return finalize_audit(response)

    project_context = request.get("project_context") or {}
    if not isinstance(project_context, dict):
        response["errors"].append(error("invalid_input", "project_context must be an object.", "project_context"))
        return finalize_audit(response)

    include = normalize_include(request.get("include"))
    items = load_knowledge_items(knowledge_items, knowledge_items_path)
    accepted, warnings, blocked = filter_items(items, filters, project_context, include)

    scored = [(item, text_score(query, item)) for item in accepted]
    scored.sort(
        key=lambda pair: (
            pair[0].get("review", {}).get("review_status") == "approved",
            pair[1],
            pair[0].get("source_quality", {}).get("overall_reliability") == "high",
        ),
        reverse=True,
    )

    results = [shape_result(item, score) for item, score in scored[:top_k]]

    if request.get("task_type") == "live_trading":
        for result in results:
            if result["freshness"] == "time_sensitive":
                result["warnings"].append("time_sensitive knowledge should be rechecked before high-impact live trading use.")
                warnings.append(f"{result['knowledge_id']} is time_sensitive for live_trading.")

    if not results and blocked:
        if all(item.get("conflict_audit", {}).get("conflict_status") == "confirmed" for item in blocked):
            response["errors"].append(error("conflict_blocked", "Only confirmed unresolved conflict items matched the request."))

    response["results"] = results
    response["blocked_results"] = [shape_blocked_result(item) for item in blocked]
    response["warnings"] = sorted(set(warnings))
    response["applied_filters"] = {"filters": filters, "project_context": project_context, "include": include}
    response["audit"]["blocked_count"] = len(blocked)
    return finalize_audit(response)


if __name__ == "__main__":
    demo = search_expert_knowledge({"query": "same candle TP SL", "task_type": "backtest_review"})
    print(demo)
