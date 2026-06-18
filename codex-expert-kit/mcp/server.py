"""CEK-TA Knowledge MCP runtime entrypoint.

This Phase 14 runtime intentionally avoids external dependencies. It provides:

1. A JSON-RPC-like stdio loop for MCP-style clients.
2. CLI helpers for tests and local debugging.
3. A read-only dispatcher over the CEK-TA knowledge tools.

It does not trade, read secrets, read account data, write approved knowledge,
or approve contributions.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Callable, Dict, Optional

CORE_DIR = Path(__file__).resolve().parents[1] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_project_root, resolve_repo_path  # noqa: E402

try:
    from .browse_knowledge_tree import browse_knowledge_tree
    from .get_conflict_audit import get_conflict_audit
    from .get_knowledge_item import get_knowledge_item
    from .get_source_profile import get_source_profile
    from .list_kb_partitions import list_kb_partitions
    from .search_expert_knowledge import search_expert_knowledge
except ImportError:  # pragma: no cover - supports direct script execution
    from browse_knowledge_tree import browse_knowledge_tree  # type: ignore
    from get_conflict_audit import get_conflict_audit  # type: ignore
    from get_knowledge_item import get_knowledge_item  # type: ignore
    from get_source_profile import get_source_profile  # type: ignore
    from list_kb_partitions import list_kb_partitions  # type: ignore
    from search_expert_knowledge import search_expert_knowledge  # type: ignore


SERVER_NAME = "cek-ta-knowledge-mcp"
SERVER_VERSION = "0.2.0"
MODE = "read_only"

FORBIDDEN_TOOL_NAMES = {
    "submit_knowledge_contribution",
    "approve_knowledge_item",
    "write_approved_knowledge",
    "place_order",
    "read_project_secrets",
    "read_account_data",
}


def repo_root() -> Path:
    return resolve_project_root(__file__)


def default_knowledge_items_path() -> str:
    env_path = os.environ.get("CEK_TA_KNOWLEDGE_ITEMS_PATH")
    if env_path:
        return env_path
    formal_index = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    if formal_index.exists():
        return str(formal_index)
    return str(resolve_repo_path("codex-expert-kit", "rag", "examples", "sample_knowledge_items.json", start_file=__file__))


def tool_specs() -> Dict[str, Dict[str, Any]]:
    return {
        "search_expert_knowledge": {
            "description": "Search source-backed CEK-TA professional knowledge.",
            "permissions": ["read_knowledge", "read_sources", "read_conflict_status"],
            "input": ["query", "filters", "project_context", "include", "top_k"],
        },
        "get_knowledge_item": {
            "description": "Fetch one CEK-TA knowledge item by knowledge_id.",
            "permissions": ["read_knowledge", "read_sources", "read_conflict_status"],
            "input": ["knowledge_id", "include"],
        },
        "get_conflict_audit": {
            "description": "Read conflict audit for a knowledge item or scope.",
            "permissions": ["read_conflict_status"],
            "input": ["knowledge_id", "scope"],
        },
        "get_source_profile": {
            "description": "Read source evidence profile by knowledge_id or source_id.",
            "permissions": ["read_sources"],
            "input": ["knowledge_id", "source_id"],
        },
        "list_kb_partitions": {
            "description": "List CEK-TA knowledge base partitions.",
            "permissions": ["read_knowledge"],
            "input": ["include_domains"],
        },
        "browse_knowledge_tree": {
            "description": "Browse the CEK-TA knowledge tree by node, parent, path prefix, or domain.",
            "permissions": ["read_knowledge"],
            "input": ["node_id", "parent_id", "tree_path_prefix", "domain", "include_children"],
        },
    }


def _trace_id(request: Dict[str, Any]) -> str:
    return str(request.get("trace_id") or request.get("request_id") or uuid.uuid4())


def _collect_sources(raw: Dict[str, Any]) -> Any:
    if "sources" in raw:
        return raw.get("sources") or []
    if "results" in raw:
        sources = []
        for item in raw.get("results") or []:
            if item.get("source_refs"):
                sources.extend(item["source_refs"])
            elif item.get("source"):
                sources.append(item["source"])
        return sources
    if "item" in raw and isinstance(raw["item"], dict):
        return raw["item"].get("source_evidence") or []
    return []


def _collect_confidence(raw: Dict[str, Any]) -> str:
    if "results" in raw and raw["results"]:
        confidences = [item.get("confidence") for item in raw["results"] if item.get("confidence")]
        if "high" in confidences:
            return "high"
        if "medium" in confidences:
            return "medium"
        if "low" in confidences:
            return "low"
    if "item" in raw and isinstance(raw["item"], dict):
        return str(((raw["item"].get("review") or {}).get("confidence")) or "")
    return ""


def normalize_tool_output(tool_name: str, request: Dict[str, Any], raw: Dict[str, Any]) -> Dict[str, Any]:
    status = raw.get("status", "ok")
    errors = raw.get("errors") or []
    warnings = raw.get("warnings") or []
    return {
        "ok": status != "error" and not errors,
        "tool": tool_name,
        "status": status,
        "data": raw,
        "sources": _collect_sources(raw),
        "confidence": _collect_confidence(raw),
        "warnings": warnings,
        "errors": errors,
        "trace_id": _trace_id(request),
    }


def call_tool(tool_name: str, request: Dict[str, Any], *, knowledge_items_path: Optional[str] = None) -> Dict[str, Any]:
    if tool_name in FORBIDDEN_TOOL_NAMES:
        trace_id = _trace_id(request)
        return {
            "ok": False,
            "tool": tool_name,
            "status": "error",
            "data": None,
            "sources": [],
            "confidence": "",
            "warnings": [],
            "errors": [
                {
                    "code": "permission_denied",
                    "message": f"Tool '{tool_name}' is not exposed by CEK-TA Phase 14 read-only runtime.",
                    "field": "tool",
                    "details": {"mode": MODE},
                }
            ],
            "trace_id": trace_id,
        }

    path = knowledge_items_path or default_knowledge_items_path()
    dispatch: Dict[str, Callable[..., Dict[str, Any]]] = {
        "search_expert_knowledge": lambda req: search_expert_knowledge(req, knowledge_items_path=path),
        "get_knowledge_item": lambda req: get_knowledge_item(req, knowledge_items_path=path),
        "get_conflict_audit": lambda req: get_conflict_audit(req, knowledge_items_path=path),
        "get_source_profile": lambda req: get_source_profile(req, knowledge_items_path=path),
        "list_kb_partitions": list_kb_partitions,
        "browse_knowledge_tree": browse_knowledge_tree,
    }
    if tool_name not in dispatch:
        return {
            "ok": False,
            "tool": tool_name,
            "status": "error",
            "data": None,
            "sources": [],
            "confidence": "",
            "warnings": [],
            "errors": [
                {
                    "code": "not_found",
                    "message": f"Unknown tool: {tool_name}.",
                    "field": "tool",
                    "details": {"available_tools": sorted(dispatch)},
                }
            ],
            "trace_id": _trace_id(request),
        }
    try:
        raw = dispatch[tool_name](request)
    except FileNotFoundError as exc:
        raw = {
            "request_id": request.get("request_id"),
            "status": "error",
            "errors": [
                {
                    "code": "storage_unavailable",
                    "message": str(exc),
                    "field": "knowledge_items_path",
                    "details": {"knowledge_items_path": path},
                }
            ],
        }
    except Exception as exc:  # pragma: no cover - defensive runtime boundary
        raw = {
            "request_id": request.get("request_id"),
            "status": "error",
            "errors": [
                {
                    "code": "retrieval_failed",
                    "message": str(exc),
                    "field": None,
                    "details": {"tool": tool_name},
                }
            ],
        }
    return normalize_tool_output(tool_name, request, raw)


def server_info() -> Dict[str, Any]:
    return {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "mode": MODE,
        "tools": tool_specs(),
        "knowledge_items_path": default_knowledge_items_path(),
        "forbidden_capabilities": sorted(FORBIDDEN_TOOL_NAMES),
    }


def jsonrpc_response(message_id: Any, result: Any = None, error_obj: Any = None) -> Dict[str, Any]:
    response: Dict[str, Any] = {"jsonrpc": "2.0", "id": message_id}
    if error_obj is not None:
        response["error"] = error_obj
    else:
        response["result"] = result
    return response


def handle_jsonrpc(message: Dict[str, Any]) -> Dict[str, Any]:
    method = message.get("method")
    params = message.get("params") or {}
    message_id = message.get("id")

    if method == "initialize":
        return jsonrpc_response(message_id, {"serverInfo": server_info()})
    if method == "tools/list":
        return jsonrpc_response(message_id, {"tools": tool_specs()})
    if method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(arguments, dict):
            return jsonrpc_response(
                message_id,
                error_obj={"code": -32602, "message": "arguments must be an object."},
            )
        return jsonrpc_response(message_id, call_tool(str(tool_name), arguments))
    return jsonrpc_response(message_id, error_obj={"code": -32601, "message": f"Unknown method: {method}"})


def stdio_loop() -> int:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
            response = handle_jsonrpc(message)
        except json.JSONDecodeError as exc:
            response = jsonrpc_response(None, error_obj={"code": -32700, "message": str(exc)})
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="CEK-TA Knowledge MCP read-only runtime")
    parser.add_argument("--info", action="store_true", help="Print server metadata")
    parser.add_argument("--list-tools", action="store_true", help="Print tool specs")
    parser.add_argument("--call", help="Call a tool by name")
    parser.add_argument("--request-json", default="{}", help="JSON request object for --call")
    parser.add_argument("--request-file", help="Read JSON request object from a UTF-8 file for --call")
    parser.add_argument("--knowledge-items-path", help="Override knowledge item JSON path")
    args = parser.parse_args(argv)

    if args.info:
        print(json.dumps(server_info(), ensure_ascii=False, indent=2))
        return 0
    if args.list_tools:
        print(json.dumps({"tools": tool_specs()}, ensure_ascii=False, indent=2))
        return 0
    if args.call:
        try:
            if args.request_file:
                request_text = Path(args.request_file).read_text(encoding="utf-8-sig")
            else:
                request_text = args.request_json
            request = json.loads(request_text)
            if not isinstance(request, dict):
                raise ValueError("request JSON must be an object")
        except Exception as exc:
            print(json.dumps({"ok": False, "errors": [{"code": "invalid_input", "message": str(exc)}]}, ensure_ascii=False))
            return 2
        response = call_tool(args.call, request, knowledge_items_path=args.knowledge_items_path)
        print(json.dumps(response, ensure_ascii=False, indent=2))
        return 0 if response.get("ok") else 1
    return stdio_loop()


if __name__ == "__main__":
    raise SystemExit(main())
