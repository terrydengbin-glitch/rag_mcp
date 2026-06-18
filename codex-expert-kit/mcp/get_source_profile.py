"""Draft implementation of the CEK-TA get_source_profile MCP tool."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .common import error, find_item, load_knowledge_items, validate_read_only_permission
except ImportError:  # pragma: no cover
    from common import error, find_item, load_knowledge_items, validate_read_only_permission  # type: ignore


def get_source_profile(
    request: Dict[str, Any],
    *,
    knowledge_items: Optional[List[Dict[str, Any]]] = None,
    knowledge_items_path: Optional[str] = None,
) -> Dict[str, Any]:
    request_id = request.get("request_id")
    response: Dict[str, Any] = {"request_id": request_id, "status": "ok", "sources": [], "errors": []}

    permission_error = validate_read_only_permission(request)
    if permission_error:
        response["status"] = "error"
        response["errors"].append(permission_error)
        return response

    knowledge_id = request.get("knowledge_id")
    source_id = request.get("source_id")
    if not knowledge_id and not source_id:
        response["status"] = "error"
        response["errors"].append(error("invalid_input", "knowledge_id or source_id is required.", "knowledge_id"))
        return response

    items = load_knowledge_items(knowledge_items, knowledge_items_path)
    if knowledge_id:
        item = find_item(items, str(knowledge_id))
        if item is None:
            response["status"] = "error"
            response["errors"].append(error("not_found", f"Knowledge item not found: {knowledge_id}.", "knowledge_id"))
            return response
        response["sources"] = item.get("source_evidence") or []
        return response

    for item in items:
        for source in item.get("source_evidence") or []:
            if source.get("source_id") == source_id:
                response["sources"].append(source)

    if not response["sources"]:
        response["status"] = "error"
        response["errors"].append(error("not_found", f"Source not found: {source_id}.", "source_id"))
    return response
