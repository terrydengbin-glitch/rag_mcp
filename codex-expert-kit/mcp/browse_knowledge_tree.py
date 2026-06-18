"""Read-only knowledge tree browser for CEK-TA MCP runtime."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from .common import error, validate_read_only_permission
except ImportError:  # pragma: no cover
    from common import error, validate_read_only_permission  # type: ignore


NODE_FIELD_RE = re.compile(r"^\s*-?\s*(node_id|parent_id|path|title|domain|subdomain|level):\s*(.*)\s*$")


def _default_tree_path() -> Path:
    return Path(__file__).resolve().parents[1] / "rag" / "knowledge_tree.md"


def load_tree_nodes(tree_path: Optional[str] = None) -> List[Dict[str, Any]]:
    path = Path(tree_path) if tree_path else _default_tree_path()
    nodes: List[Dict[str, Any]] = []
    current: Optional[Dict[str, Any]] = None

    for line in path.read_text(encoding="utf-8").splitlines():
        match = NODE_FIELD_RE.match(line)
        if not match:
            continue
        field, raw_value = match.groups()
        value: Any = raw_value.strip().strip('"')
        if value == "null":
            value = None
        if field == "level" and isinstance(value, str) and value.isdigit():
            value = int(value)
        if field == "node_id":
            if current:
                nodes.append(current)
            current = {"node_id": value}
        elif current is not None:
            current[field] = value

    if current:
        nodes.append(current)
    return nodes


def browse_knowledge_tree(
    request: Dict[str, Any],
    *,
    tree_path: Optional[str] = None,
) -> Dict[str, Any]:
    request_id = request.get("request_id")
    response: Dict[str, Any] = {
        "request_id": request_id,
        "status": "ok",
        "nodes": [],
        "warnings": [],
        "errors": [],
    }

    permission_error = validate_read_only_permission(request)
    if permission_error:
        response["status"] = "error"
        response["errors"].append(permission_error)
        return response

    try:
        nodes = load_tree_nodes(tree_path)
    except FileNotFoundError:
        response["status"] = "error"
        response["errors"].append(error("storage_unavailable", "knowledge_tree.md was not found.", "tree_path"))
        return response

    node_id = request.get("node_id")
    parent_id = request.get("parent_id")
    path_prefix = request.get("tree_path_prefix")
    include_children = bool(request.get("include_children", True))
    domain = request.get("domain")

    filtered = nodes
    if node_id:
        if include_children:
            node = next((item for item in nodes if item.get("node_id") == node_id), None)
            if node is None:
                response["status"] = "error"
                response["errors"].append(error("not_found", f"Knowledge tree node not found: {node_id}.", "node_id"))
                return response
            prefix = str(node.get("path", ""))
            filtered = [item for item in nodes if item.get("node_id") == node_id or str(item.get("path", "")).startswith(prefix + " / ")]
        else:
            filtered = [item for item in nodes if item.get("node_id") == node_id]
    if parent_id:
        filtered = [item for item in filtered if item.get("parent_id") == parent_id]
    if path_prefix:
        filtered = [item for item in filtered if str(item.get("path", "")).startswith(str(path_prefix))]
    if domain:
        filtered = [item for item in filtered if item.get("domain") == domain]

    response["nodes"] = filtered
    if not filtered:
        response["status"] = "warning"
        response["warnings"].append("No knowledge tree nodes matched the request.")
    return response
