"""Draft implementation of the CEK-TA get_knowledge_item MCP tool."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .common import error, find_item, load_knowledge_items, validate_read_only_permission
except ImportError:  # pragma: no cover
    from common import error, find_item, load_knowledge_items, validate_read_only_permission  # type: ignore


def get_knowledge_item(
    request: Dict[str, Any],
    *,
    knowledge_items: Optional[List[Dict[str, Any]]] = None,
    knowledge_items_path: Optional[str] = None,
) -> Dict[str, Any]:
    request_id = request.get("request_id")
    response: Dict[str, Any] = {"request_id": request_id, "status": "ok", "item": None, "errors": []}

    permission_error = validate_read_only_permission(request)
    if permission_error:
        response["status"] = "error"
        response["errors"].append(permission_error)
        return response

    knowledge_id = str(request.get("knowledge_id", "")).strip()
    if not knowledge_id:
        response["status"] = "error"
        response["errors"].append(error("invalid_input", "knowledge_id is required.", "knowledge_id"))
        return response

    item = find_item(load_knowledge_items(knowledge_items, knowledge_items_path), knowledge_id)
    if item is None:
        response["status"] = "error"
        response["errors"].append(error("not_found", f"Knowledge item not found: {knowledge_id}.", "knowledge_id"))
        return response

    include = request.get("include") or {}
    item_out = dict(item)
    if not include.get("decision_log", False):
        review = dict(item_out.get("review") or {})
        review.pop("decision_log", None)
        item_out["review"] = review

    response["item"] = item_out
    return response
