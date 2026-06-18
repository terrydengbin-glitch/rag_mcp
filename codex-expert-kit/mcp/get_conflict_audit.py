"""Draft implementation of the CEK-TA get_conflict_audit MCP tool."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .common import deep_get, error, find_item, load_knowledge_items, validate_read_only_permission
except ImportError:  # pragma: no cover
    from common import deep_get, error, find_item, load_knowledge_items, validate_read_only_permission  # type: ignore


def get_conflict_audit(
    request: Dict[str, Any],
    *,
    knowledge_items: Optional[List[Dict[str, Any]]] = None,
    knowledge_items_path: Optional[str] = None,
) -> Dict[str, Any]:
    request_id = request.get("request_id")
    response: Dict[str, Any] = {
        "request_id": request_id,
        "status": "ok",
        "conflict_status": "none",
        "checked_against": [],
        "conflicts": [],
        "resolution_summary": "",
        "approval_allowed": True,
        "errors": [],
    }

    permission_error = validate_read_only_permission(request)
    if permission_error:
        response["status"] = "error"
        response["errors"].append(permission_error)
        return response

    items = load_knowledge_items(knowledge_items, knowledge_items_path)
    knowledge_id = request.get("knowledge_id")
    if knowledge_id:
        item = find_item(items, str(knowledge_id))
        if item is None:
            response["status"] = "error"
            response["errors"].append(error("not_found", f"Knowledge item not found: {knowledge_id}.", "knowledge_id"))
            return response
        audit = item.get("conflict_audit") or {}
        response.update(
            {
                "conflict_status": audit.get("conflict_status", "none"),
                "checked_against": audit.get("checked_against", []),
                "conflicts": audit.get("conflicts", []),
                "resolution_summary": audit.get("resolution_summary", ""),
                "approval_allowed": audit.get("conflict_status") in ("none", "resolved"),
            }
        )
        if response["conflict_status"] in ("potential", "confirmed"):
            response["status"] = "warning"
        return response

    scope = request.get("scope") or {}
    if not isinstance(scope, dict) or not any(scope.values()):
        response["status"] = "error"
        response["errors"].append(error("invalid_input", "knowledge_id or non-empty scope is required.", "knowledge_id"))
        return response

    matched = []
    for item in items:
        if all(not value or deep_get(item, f"metadata.{field}", deep_get(item, f"applicability.{field}")) == value for field, value in scope.items()):
            matched.append(item)

    statuses = [deep_get(item, "conflict_audit.conflict_status", "none") for item in matched]
    if "confirmed" in statuses:
        response["conflict_status"] = "confirmed"
        response["status"] = "warning"
        response["approval_allowed"] = False
    elif "potential" in statuses:
        response["conflict_status"] = "potential"
        response["status"] = "warning"
        response["approval_allowed"] = False
    elif "resolved" in statuses:
        response["conflict_status"] = "resolved"
        response["approval_allowed"] = True

    response["checked_against"] = [item.get("knowledge_id", "") for item in matched]
    response["conflicts"] = [conflict for item in matched for conflict in (item.get("conflict_audit") or {}).get("conflicts", [])]
    response["resolution_summary"] = "Scope conflict summary generated from matching knowledge items."
    return response
