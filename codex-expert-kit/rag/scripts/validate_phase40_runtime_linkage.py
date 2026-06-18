"""Validate Phase 40 reviewed knowledge runtime linkage.

This check proves that Phase 40 formal reviewed knowledge can be reached by the
formal index, knowledge tree, API/SearchLab-style filters, and MCP search while
still being blocked from default-guidance-only retrieval.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


PHASE40_PARTITION = "KB_AI_18_FEEDBACK_GOVERNANCE"
PHASE40_EXPECTED_REVIEWED_COUNT = 36
PHASE40_NODE_EXPECTATIONS = {
    "kt.ai_feedback_governance.feedback_logging": 5,
    "kt.ai_feedback_governance.label_refresh": 5,
    "kt.ai_feedback_governance.drift_monitoring": 4,
    "kt.ai_feedback_governance.retraining_trigger": 4,
    "kt.ai_feedback_governance.recalibration_loop": 3,
    "kt.ai_feedback_governance.champion_challenger": 3,
    "kt.ai_feedback_governance.shadow_paper_canary": 2,
    "kt.ai_feedback_governance.rollback_governance": 3,
    "kt.ai_feedback_governance.llm_prompt_rag_sft_loop": 4,
    "kt.ai_feedback_governance.feedback_loop_risk": 3,
}
PHASE40_TREE_NODES = {
    "kt.ai_feedback_governance",
    "kt.ai_feedback_governance.feedback_logging",
    "kt.ai_feedback_governance.label_refresh",
    "kt.ai_feedback_governance.drift_monitoring",
    "kt.ai_feedback_governance.retraining_trigger",
    "kt.ai_feedback_governance.recalibration_loop",
    "kt.ai_feedback_governance.champion_challenger",
    "kt.ai_feedback_governance.shadow_paper_canary",
    "kt.ai_feedback_governance.rollback_governance",
    "kt.ai_feedback_governance.llm_prompt_rag_sft_loop",
    "kt.ai_feedback_governance.feedback_loop_risk",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def phase40_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in items
        if item.get("metadata", {}).get("partition_id") == PHASE40_PARTITION
        or str(item.get("knowledge_id", "")).startswith("kb_ai_feedback_governance.phase40.")
    ]


def assert_condition(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = phase40_items(items)
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    node_counts = Counter(item.get("metadata", {}).get("canonical_node_id", "") for item in scoped)
    partition_counts = Counter(item.get("metadata", {}).get("partition_id", "") for item in scoped)

    assert_condition(
        errors,
        len(scoped) == PHASE40_EXPECTED_REVIEWED_COUNT,
        f"Phase 40 formal reviewed count should be {PHASE40_EXPECTED_REVIEWED_COUNT}, got {len(scoped)}.",
    )
    assert_condition(
        errors,
        dict(review_counts) == {"reviewed": PHASE40_EXPECTED_REVIEWED_COUNT},
        f"Phase 40 review statuses mismatch: {dict(review_counts)}.",
    )
    assert_condition(
        errors,
        dict(gate_counts) == {"caveat_only": PHASE40_EXPECTED_REVIEWED_COUNT},
        f"Phase 40 machine gates mismatch: {dict(gate_counts)}.",
    )
    assert_condition(
        errors,
        dict(partition_counts) == {PHASE40_PARTITION: PHASE40_EXPECTED_REVIEWED_COUNT},
        f"Phase 40 partition mismatch: {dict(partition_counts)}.",
    )
    for node_id, expected in PHASE40_NODE_EXPECTATIONS.items():
        assert_condition(errors, node_counts.get(node_id, 0) == expected, f"{node_id} should have {expected} items, got {node_counts.get(node_id, 0)}.")

    missing_sources = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    assert_condition(errors, not missing_sources, f"Phase 40 items missing source_evidence: {missing_sources}.")

    wrong_default_flags = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("default_guidance_allowed") is not False
    ]
    assert_condition(errors, not wrong_default_flags, f"Phase 40 items unexpectedly allow default guidance: {wrong_default_flags}.")

    return {
        "phase40_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "partition_counts": dict(partition_counts),
    }


def validate_tree(errors: list[str]) -> dict[str, Any]:
    browse_module = load_module(
        "phase40_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree({"node_id": "kt.ai_feedback_governance", "include_children": True})
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    missing = sorted(PHASE40_TREE_NODES - node_ids)
    assert_condition(errors, response.get("status") == "ok", f"Knowledge tree status should be ok, got {response.get('status')}.")
    assert_condition(errors, not missing, f"Knowledge tree missing Phase 40 nodes: {missing}.")
    return {
        "status": response.get("status"),
        "node_count": len(nodes),
        "phase40_nodes_found": sorted(node_id for node_id in node_ids if node_id in PHASE40_TREE_NODES),
        "missing_nodes": missing,
    }


def validate_api_searchlab_style(errors: list[str]) -> dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")
    sample_nodes = [
        "kt.ai_feedback_governance.label_refresh",
        "kt.ai_feedback_governance.drift_monitoring",
        "kt.ai_feedback_governance.champion_challenger",
        "kt.ai_feedback_governance.shadow_paper_canary",
        "kt.ai_feedback_governance.rollback_governance",
        "kt.ai_feedback_governance.llm_prompt_rag_sft_loop",
    ]
    results: dict[str, Any] = {}
    for node_id in sample_nodes:
        filtered = api_module.filter_items(node_id)
        statuses = sorted({item.get("review", {}).get("review_status", "") for item in filtered})
        gates = sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in filtered})
        results[node_id] = {
            "formal_count": len(filtered),
            "review_statuses": statuses,
            "machine_gates": gates,
        }
        assert_condition(errors, len(filtered) >= PHASE40_NODE_EXPECTATIONS[node_id], f"API/SearchLab filter missed items for {node_id}.")
        assert_condition(errors, "reviewed" in statuses, f"API/SearchLab filter missed reviewed status for {node_id}.")
        assert_condition(errors, "caveat_only" in gates, f"API/SearchLab filter missed caveat_only gate for {node_id}.")
    return results


def validate_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase40_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    request = {
        "request_id": "phase40-runtime-search",
        "query": "feedback label refresh good loss bad win drift retraining calibration challenger",
        "top_k": 5,
        "filters": {"canonical_node_id": list(PHASE40_NODE_EXPECTATIONS)},
        "include": {"reviewed": True, "default_guidance_only": False},
    }
    response = mcp_module.search_expert_knowledge(request, knowledge_items_path=str(index_path))
    results = response.get("results", [])
    assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP search status is not ok/warning: {response.get('status')}.")
    assert_condition(errors, bool(results), "MCP search returned no Phase 40 reviewed results.")
    if results:
        first = results[0]
        assert_condition(errors, first.get("source_count", 0) > 0, "MCP result has no source_count.")
        assert_condition(errors, first.get("review_status") == "reviewed", f"MCP result review_status mismatch: {first.get('review_status')}.")
        assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", "MCP result is not caveat_only.")
        assert_condition(errors, first.get("acceptance_level") == "accepted_reference", "MCP result acceptance_level is not accepted_reference.")

    default_guidance_request = dict(request)
    default_guidance_request["request_id"] = "phase40-default-guidance-block"
    default_guidance_request["include"] = {"reviewed": True, "default_guidance_only": True}
    blocked_response = mcp_module.search_expert_knowledge(default_guidance_request, knowledge_items=items)
    assert_condition(errors, not blocked_response.get("results"), "MCP default_guidance_only unexpectedly returned Phase 40 caveat_only results.")
    assert_condition(
        errors,
        blocked_response.get("audit", {}).get("blocked_count", 0) >= PHASE40_EXPECTED_REVIEWED_COUNT,
        "MCP default_guidance_only did not report blocked Phase 40 results.",
    )

    permission_response = mcp_module.search_expert_knowledge(
        {"request_id": "phase40-permission-deny", "query": "feedback governance", "requested_permission": "approve_knowledge"},
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
    errors: list[str] = []
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    data = load_json(index_path)
    items = data.get("items", data if isinstance(data, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain a list or {items: [...]}.")

    report = {
        "report_id": "phase40_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": "CEK-TA-316",
        "scope": "Phase 40 MCP/SearchLab/KnowledgeTree 联动验证",
        "index_path": str(index_path),
        "file_index": validate_file_index(items, errors),
        "knowledge_tree": validate_tree(errors),
        "api_searchlab_style": validate_api_searchlab_style(errors),
        "mcp": validate_mcp(items, index_path, errors),
        "errors": errors,
        "status": "pass" if not errors else "fail",
        "boundary": "Phase 40 reviewed/caveat_only knowledge is searchable and citable, but blocked from default guidance and hard-gate use.",
    }

    report_path = resolve_repo_path("docs", "reports", "phase40_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
