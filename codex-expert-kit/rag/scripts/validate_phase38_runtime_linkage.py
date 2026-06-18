"""Validate Phase 38 reviewed knowledge runtime linkage.

This check is intentionally narrow: it proves that Phase 38 formal reviewed
knowledge can be reached by the file index, knowledge tree, API-style filters,
and MCP search while still being blocked from default-guidance-only retrieval.
"""

from __future__ import annotations

import importlib.util
import importlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[3]
CORE_PATH = ROOT / "codex-expert-kit" / "core"
if str(CORE_PATH) not in sys.path:
    sys.path.insert(0, str(CORE_PATH))
MCP_PATH = ROOT / "codex-expert-kit" / "mcp"
if str(MCP_PATH) not in sys.path:
    sys.path.insert(0, str(MCP_PATH))
API_PATH = ROOT / "codex-expert-kit" / "api"
if str(API_PATH) not in sys.path:
    sys.path.insert(0, str(API_PATH))

from path_resolver import resolve_repo_path  # noqa: E402


PHASE38_NODE_EXPECTATIONS = {
    "kt.ai_engineering.numeric_scoring": 10,
    "kt.ai_engineering.calibration_threshold": 10,
    "kt.ai_engineering.decision_time_feature_contract": 10,
    "kt.ai_engineering.llm_audit_assistant": 10,
    "kt.ai_engineering.shadow_paper_ope_eval": 10,
    "kt.ai_engineering.model_release_governance": 10,
    "kt.rag_engineering.trading_scoring_rag_pack": 6,
}

PHASE38_EXPECTED_REVIEWED_COUNT = sum(PHASE38_NODE_EXPECTATIONS.values())


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def phase38_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        item
        for item in items
        if item.get("metadata", {}).get("phase") == "Phase 38"
        or str(item.get("knowledge_id", "")).startswith("kb.ai_engineering.phase38.")
    ]


def assert_condition(errors: List[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_file_index(items: List[Dict[str, Any]], errors: List[str]) -> Dict[str, Any]:
    scoped = phase38_items(items)
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    node_counts = Counter(item.get("metadata", {}).get("tree_node_id", "") for item in scoped)
    partition_counts = Counter(item.get("metadata", {}).get("partition_id", "") for item in scoped)

    assert_condition(
        errors,
        len(scoped) == PHASE38_EXPECTED_REVIEWED_COUNT,
        f"Phase 38 formal reviewed count should be {PHASE38_EXPECTED_REVIEWED_COUNT}, got {len(scoped)}.",
    )
    assert_condition(
        errors,
        dict(review_counts) == {"reviewed": PHASE38_EXPECTED_REVIEWED_COUNT},
        f"Phase 38 review statuses mismatch: {dict(review_counts)}.",
    )
    assert_condition(
        errors,
        dict(gate_counts) == {"caveat_only": PHASE38_EXPECTED_REVIEWED_COUNT},
        f"Phase 38 machine gates mismatch: {dict(gate_counts)}.",
    )
    for node_id, expected in PHASE38_NODE_EXPECTATIONS.items():
        assert_condition(errors, node_counts.get(node_id, 0) == expected, f"{node_id} should have {expected} items, got {node_counts.get(node_id, 0)}.")

    missing_sources = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    assert_condition(errors, not missing_sources, f"Phase 38 items missing source_evidence: {missing_sources[:10]}.")

    return {
        "phase38_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "partition_counts": dict(partition_counts),
    }


def validate_tree(errors: List[str]) -> Dict[str, Any]:
    browse_module = load_module(
        "phase38_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree({"node_id": "kt.ai_engineering", "include_children": True})
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    for node_id in PHASE38_NODE_EXPECTATIONS:
        if node_id.startswith("kt.ai_engineering."):
            assert_condition(errors, node_id in node_ids, f"Knowledge tree missing Phase 38 node: {node_id}.")

    rag_response = browse_module.browse_knowledge_tree(
        {"node_id": "kt.rag_engineering.trading_scoring_rag_pack", "include_children": False}
    )
    assert_condition(errors, rag_response.get("nodes"), "Knowledge tree missing RAG trading scoring pack node.")
    return {
        "ai_engineering_node_count": len(nodes),
        "phase38_ai_nodes_found": sorted(node_id for node_id in node_ids if node_id in PHASE38_NODE_EXPECTATIONS),
        "rag_pack_found": bool(rag_response.get("nodes")),
    }


def validate_api_style(items: List[Dict[str, Any]], errors: List[str]) -> Dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")

    sample_nodes = [
        "kt.ai_engineering.numeric_scoring",
        "kt.ai_engineering.llm_audit_assistant",
        "kt.rag_engineering.trading_scoring_rag_pack",
    ]
    results: Dict[str, Any] = {}
    for node_id in sample_nodes:
        filtered = api_module.filter_items(node_id)
        results[node_id] = {
            "formal_count": len(filtered),
            "review_statuses": sorted({item.get("review", {}).get("review_status", "") for item in filtered}),
            "machine_gates": sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in filtered}),
        }
        assert_condition(errors, len(filtered) >= PHASE38_NODE_EXPECTATIONS[node_id], f"API filter did not return expected items for {node_id}.")
        assert_condition(errors, "reviewed" in results[node_id]["review_statuses"], f"API filter missed reviewed status for {node_id}.")
    return results


def validate_mcp(items: List[Dict[str, Any]], index_path: Path, errors: List[str]) -> Dict[str, Any]:
    mcp_module = load_module(
        "phase38_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    request = {
        "request_id": "phase38-runtime-search",
        "query": "scorer soft gate final gate scoring threshold",
        "top_k": 5,
        "filters": {"tree_node_id": "kt.ai_engineering.numeric_scoring"},
        "include": {"reviewed": True, "default_guidance_only": False},
    }
    response = mcp_module.search_expert_knowledge(request, knowledge_items_path=str(index_path))
    results = response.get("results", [])
    assert_condition(errors, response.get("status") in ("ok", "warning"), f"MCP search status is not ok/warning: {response.get('status')}.")
    assert_condition(errors, bool(results), "MCP search returned no Phase 38 reviewed results.")
    if results:
        first = results[0]
        assert_condition(errors, first.get("source_count", 0) > 0, "MCP result has no source_count.")
        assert_condition(errors, first.get("review_status") == "reviewed", f"MCP result review_status mismatch: {first.get('review_status')}.")
        assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", "MCP result is not caveat_only.")
        assert_condition(errors, first.get("acceptance_level") == "accepted_reference", "MCP result acceptance_level is not accepted_reference.")

    default_guidance_request = dict(request)
    default_guidance_request["request_id"] = "phase38-default-guidance-block"
    default_guidance_request["include"] = {"reviewed": True, "default_guidance_only": True}
    blocked_response = mcp_module.search_expert_knowledge(default_guidance_request, knowledge_items=items)
    assert_condition(errors, not blocked_response.get("results"), "MCP default_guidance_only unexpectedly returned Phase 38 caveat_only results.")
    assert_condition(errors, blocked_response.get("audit", {}).get("blocked_count", 0) >= 1, "MCP default_guidance_only did not report blocked results.")

    permission_response = mcp_module.search_expert_knowledge(
        {"request_id": "phase38-permission-deny", "query": "scoring", "requested_permission": "approve_knowledge"},
        knowledge_items=items,
    )
    assert_condition(errors, bool(permission_response.get("errors")), "MCP write/approval permission was not denied.")

    return {
        "search_result_count": len(results),
        "first_result": results[0] if results else None,
        "default_guidance_blocked_count": blocked_response.get("audit", {}).get("blocked_count", 0),
        "permission_denied": bool(permission_response.get("errors")),
    }


def main() -> int:
    errors: List[str] = []
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    data = load_json(index_path)
    items = data.get("items", data if isinstance(data, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain a list or {items: [...]}.")

    report = {
        "report_id": "phase38_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "CEK-TA-274 MCP/SearchLab/知识树联动验证",
        "index_path": str(index_path),
        "file_index": validate_file_index(items, errors),
        "knowledge_tree": validate_tree(errors),
        "api_searchlab_style": validate_api_style(items, errors),
        "mcp": validate_mcp(items, index_path, errors),
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }

    report_path = resolve_repo_path("docs", "reports", "phase38_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
