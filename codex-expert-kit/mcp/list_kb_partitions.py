"""Draft implementation of the CEK-TA list_kb_partitions MCP tool."""

from __future__ import annotations

from typing import Any, Dict

try:
    from .common import PARTITIONS, validate_read_only_permission
except ImportError:  # pragma: no cover
    from common import PARTITIONS, validate_read_only_permission  # type: ignore


def list_kb_partitions(request: Dict[str, Any]) -> Dict[str, Any]:
    request_id = request.get("request_id")
    response: Dict[str, Any] = {"request_id": request_id, "status": "ok", "partitions": [], "errors": []}

    permission_error = validate_read_only_permission(request)
    if permission_error:
        response["status"] = "error"
        response["errors"].append(permission_error)
        return response

    include_domains = bool(request.get("include_domains", True))
    if include_domains:
        response["partitions"] = list(PARTITIONS)
    else:
        response["partitions"] = [{k: v for k, v in item.items() if k != "domain"} for item in PARTITIONS]
    return response
