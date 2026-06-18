"""Validate Phase 43 MCP/SearchLab/KnowledgeTree runtime linkage.

This gate proves that Phase 43 external project memory knowledge is reachable
from the official formal index, KnowledgeTree, API/SearchLab-style filters, and
MCP search while remaining caveat_only and blocked from default guidance or
write/approval permissions.
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


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
MCP_DIR = Path(__file__).resolve().parents[2] / "mcp"
API_DIR = Path(__file__).resolve().parents[2] / "api"
for path in (CORE_DIR, MCP_DIR, API_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from path_resolver import resolve_repo_path  # noqa: E402


TASK_ID = "CEK-TA-369"
PHASE = "Phase 43"
EXPECTED_PHASE43_COUNT = 29
PHASE43_PREFIX = "kb_ai_project_memory.phase43."
PHASE43_ROOT_NODE = "kt.ai_engineering.external_project_memory"

PHASE43_NODE_EXPECTATIONS = {
    "kt.ai_engineering.external_project_memory.memory_adapter_selection": 3,
    "kt.ai_engineering.external_project_memory.memory_boundary": 4,
    "kt.ai_engineering.external_project_memory.memory_evaluation_regression": 2,
    "kt.ai_engineering.external_project_memory.memory_event_log": 1,
    "kt.ai_engineering.external_project_memory.memory_mcp_api_contract": 1,
    "kt.ai_engineering.external_project_memory.memory_retention_privacy": 1,
    "kt.ai_engineering.external_project_memory.memory_retrieval_context": 3,
    "kt.ai_engineering.external_project_memory.memory_schema_lifecycle": 7,
    "kt.ai_engineering.external_project_memory.memory_security_governance": 2,
    "kt.ai_engineering.external_project_memory.memory_write_gate": 5,
}

PHASE43_SEARCH_CASES = [
    {
        "case_id": "phase43_memory_boundary",
        "query": "RAG Knowledge Project Memory boundary CEK-TA private memory separation",
        "canonical_node_id": "kt.ai_engineering.external_project_memory.memory_boundary",
        "min_results": 2,
    },
    {
        "case_id": "phase43_write_gate",
        "query": "AI propose memory write gate secret scan prompt injection poisoning visibility conflict",
        "canonical_node_id": "kt.ai_engineering.external_project_memory.memory_write_gate",
        "min_results": 3,
    },
    {
        "case_id": "phase43_schema_lifecycle",
        "query": "MemoryItem schema lifecycle supersede deprecated source hash review status",
        "canonical_node_id": "kt.ai_engineering.external_project_memory.memory_schema_lifecycle",
        "min_results": 3,
    },
    {
        "case_id": "phase43_adapter_selection",
        "query": "PostgreSQL JSONB pgvector memory engine adapter portability semantic index",
        "canonical_node_id": "kt.ai_engineering.external_project_memory.memory_adapter_selection",
        "min_results": 2,
    },
]

EXPECTED_FIXTURE_IDS = [
    "kb_ai_project_memory.phase43.rag_knowledge_project_memory.v1",
    "kb_ai_project_memory.phase43.project_memory_cek_ta.v1",
    "kb_ai_project_memory.phase43.cek_ta_memory_contract.v1",
    "kb_ai_project_memory.phase43.ai_propose_memory.v1",
    "kb_ai_project_memory.phase43.no_auto_save_all_chat.v1",
    "kb_ai_project_memory.phase43.memory_write_security_gate.v1",
    "kb_ai_project_memory.phase43.memoryitem_supersede.v1",
    "kb_ai_project_memory.phase43.pgvector_semantic_index.v1",
    "kb_ai_project_memory.phase43.adapter_portability_test.v1",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def assert_condition(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def phase43_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in items
        if item.get("metadata", {}).get("phase") == PHASE
        or str(item.get("knowledge_id", "")).startswith(PHASE43_PREFIX)
    ]


def validate_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = phase43_items(items)
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    review_mode_counts = Counter(item.get("review", {}).get("review_mode", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    node_counts = Counter(item.get("metadata", {}).get("canonical_node_id", "") for item in scoped)
    partition_counts = Counter(item.get("metadata", {}).get("partition_id", "") for item in scoped)
    source_missing = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    unsafe_conflicts = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}
    ]
    default_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("default_guidance_allowed") is not False
    ]
    approved_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("approved_allowed") is not False
        or item.get("review", {}).get("review_status") == "approved"
    ]
    hard_gate_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("hard_gate_allowed") is not False
    ]
    private_memory_allowed = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("phase43_conversion", {}).get("external_project_private_memory_allowed") is not False
    ]
    database_changes_allowed = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("phase43_conversion", {}).get("production_database_changes_allowed") is not False
    ]

    assert_condition(errors, len(scoped) == EXPECTED_PHASE43_COUNT, f"Phase 43 formal reviewed count should be {EXPECTED_PHASE43_COUNT}, got {len(scoped)}.")
    assert_condition(errors, dict(review_counts) == {"reviewed": EXPECTED_PHASE43_COUNT}, f"Phase 43 review statuses mismatch: {dict(review_counts)}.")
    assert_condition(errors, dict(review_mode_counts) == {"caveat_only": EXPECTED_PHASE43_COUNT}, f"Phase 43 review modes mismatch: {dict(review_mode_counts)}.")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": EXPECTED_PHASE43_COUNT}, f"Phase 43 machine gates mismatch: {dict(gate_counts)}.")
    for node_id, expected in PHASE43_NODE_EXPECTATIONS.items():
        assert_condition(errors, node_counts.get(node_id, 0) == expected, f"{node_id} should have {expected} items, got {node_counts.get(node_id, 0)}.")
    assert_condition(errors, not source_missing, f"Phase 43 items missing source_evidence: {source_missing}.")
    assert_condition(errors, not unsafe_conflicts, f"Phase 43 items have unsafe conflicts: {unsafe_conflicts}.")
    assert_condition(errors, not default_enabled, f"Phase 43 reviewed items unexpectedly allow default guidance: {default_enabled}.")
    assert_condition(errors, not approved_enabled, f"Phase 43 items unexpectedly allow approved: {approved_enabled}.")
    assert_condition(errors, not hard_gate_enabled, f"Phase 43 items unexpectedly allow hard gate: {hard_gate_enabled}.")
    assert_condition(errors, not private_memory_allowed, f"Phase 43 items unexpectedly allow external private memory: {private_memory_allowed}.")
    assert_condition(errors, not database_changes_allowed, f"Phase 43 items unexpectedly allow production DB changes: {database_changes_allowed}.")

    return {
        "phase43_count": len(scoped),
        "review_counts": dict(review_counts),
        "review_mode_counts": dict(review_mode_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "partition_counts": dict(partition_counts),
        "source_missing_count": len(source_missing),
        "unsafe_conflict_count": len(unsafe_conflicts),
        "default_guidance_enabled_count": len(default_enabled),
        "approved_enabled_count": len(approved_enabled),
        "hard_gate_enabled_count": len(hard_gate_enabled),
        "private_memory_allowed_count": len(private_memory_allowed),
        "production_database_changes_allowed_count": len(database_changes_allowed),
    }


def validate_knowledge_tree(errors: list[str]) -> dict[str, Any]:
    browse_module = load_module(
        "phase43_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree({"node_id": PHASE43_ROOT_NODE, "include_children": True})
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    expected_nodes = set(PHASE43_NODE_EXPECTATIONS)
    missing_tree_nodes = sorted(expected_nodes - node_ids)
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree missing Phase 43 nodes: {missing_tree_nodes}.")
    return {
        "external_project_memory_node_count": len(nodes),
        "phase43_tree_nodes_expected": len(expected_nodes),
        "phase43_tree_nodes_found": sorted(expected_nodes & node_ids),
        "missing_tree_nodes": missing_tree_nodes,
    }


def validate_searchlab_style(errors: list[str]) -> dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")
    results: dict[str, Any] = {}
    sample_nodes = [
        PHASE43_ROOT_NODE,
        "kt.ai_engineering.external_project_memory.memory_boundary",
        "kt.ai_engineering.external_project_memory.memory_write_gate",
        "kt.ai_engineering.external_project_memory.memory_schema_lifecycle",
        "kt.ai_engineering.external_project_memory.memory_adapter_selection",
    ]
    for node_id in sample_nodes:
        filtered = api_module.filter_items(node_id)
        phase43_filtered = [
            item
            for item in filtered
            if item.get("metadata", {}).get("phase") == PHASE
            or str(item.get("knowledge_id", "")).startswith(PHASE43_PREFIX)
        ]
        statuses = sorted({item.get("review", {}).get("review_status", "") for item in phase43_filtered})
        gates = sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in phase43_filtered})
        results[node_id] = {
            "phase43_count": len(phase43_filtered),
            "review_statuses": statuses,
            "machine_gates": gates,
        }
        assert_condition(errors, bool(phase43_filtered), f"SearchLab/API filter did not return Phase 43 items for {node_id}.")
        assert_condition(errors, statuses == ["reviewed"], f"SearchLab/API statuses mismatch for {node_id}: {statuses}.")
        assert_condition(errors, gates == ["caveat_only"], f"SearchLab/API gates mismatch for {node_id}: {gates}.")
    return results


def validate_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase43_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    case_results: dict[str, Any] = {}
    for case in PHASE43_SEARCH_CASES:
        request = {
            "request_id": case["case_id"],
            "query": case["query"],
            "top_k": 8,
            "filters": {"canonical_node_id": case["canonical_node_id"]},
            "include": {"reviewed": True, "default_guidance_only": False},
        }
        response = mcp_module.search_expert_knowledge(request, knowledge_items_path=str(index_path))
        results = [
            result
            for result in response.get("results", [])
            if str(result.get("knowledge_id", "")).startswith(PHASE43_PREFIX)
        ]
        case_results[case["case_id"]] = {
            "status": response.get("status"),
            "phase43_result_count": len(results),
            "top_knowledge_ids": [result.get("knowledge_id") for result in results[:5]],
            "first_result": results[0] if results else None,
        }
        assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP search status for {case['case_id']} is {response.get('status')}.")
        assert_condition(errors, len(results) >= int(case["min_results"]), f"MCP search {case['case_id']} returned {len(results)} Phase 43 results.")
        if results:
            first = results[0]
            assert_condition(errors, first.get("source_count", 0) > 0, f"MCP {case['case_id']} first result has no sources.")
            assert_condition(errors, first.get("review_status") == "reviewed", f"MCP {case['case_id']} first result is not reviewed.")
            assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP {case['case_id']} first result is not caveat_only.")
            assert_condition(errors, first.get("acceptance_level") == "accepted_reference", f"MCP {case['case_id']} acceptance level mismatch.")

    block_request = {
        "request_id": "phase43-default-guidance-block",
        "query": "Project Memory write gate AI propose memory",
        "top_k": 10,
        "filters": {"canonical_node_id": "kt.ai_engineering.external_project_memory.memory_write_gate"},
        "include": {"reviewed": True, "default_guidance_only": True},
    }
    blocked_response = mcp_module.search_expert_knowledge(block_request, knowledge_items=items)
    phase43_blocked = [
        item
        for item in blocked_response.get("blocked_results", [])
        if str(item.get("knowledge_id", "")).startswith(PHASE43_PREFIX)
    ]
    assert_condition(errors, not [r for r in blocked_response.get("results", []) if str(r.get("knowledge_id", "")).startswith(PHASE43_PREFIX)], "MCP default_guidance_only unexpectedly returned Phase 43 caveat_only results.")
    assert_condition(errors, bool(phase43_blocked), "MCP default_guidance_only did not block Phase 43 caveat_only results.")

    permission_response = mcp_module.search_expert_knowledge(
        {
            "request_id": "phase43-permission-deny",
            "query": "Project Memory MCP active write",
            "requested_permission": "approve_knowledge",
        },
        knowledge_items=items,
    )
    assert_condition(errors, bool(permission_response.get("errors")), "MCP approval/write permission was not denied.")

    return {
        "search_cases": case_results,
        "default_guidance_blocked_count": blocked_response.get("audit", {}).get("blocked_count", 0),
        "phase43_blocked_count": len(phase43_blocked),
        "permission_denied": bool(permission_response.get("errors")),
    }


def validate_vue_fixtures(errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    candidate_fixture = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    candidate_text = candidate_fixture.read_text(encoding="utf-8")
    missing_ids = [knowledge_id for knowledge_id in EXPECTED_FIXTURE_IDS if knowledge_id not in formal_text]
    missing_nodes = [node_id for node_id in PHASE43_NODE_EXPECTATIONS if node_id not in tree_text]
    missing_candidate_links = [knowledge_id for knowledge_id in EXPECTED_FIXTURE_IDS if knowledge_id not in candidate_text]
    assert_condition(errors, not missing_ids, f"Vue formalKnowledgeItems fixture missing Phase 43 ids: {missing_ids}.")
    assert_condition(errors, not missing_nodes, f"Vue knowledgeTreeNodes fixture missing Phase 43 nodes: {missing_nodes}.")
    assert_condition(errors, not missing_candidate_links, f"Vue candidate fixture missing Phase 43 formal links: {missing_candidate_links}.")
    return {
        "formal_fixture": str(formal_fixture),
        "tree_fixture": str(tree_fixture),
        "candidate_fixture": str(candidate_fixture),
        "expected_ids_checked": len(EXPECTED_FIXTURE_IDS),
        "missing_ids": missing_ids,
        "phase43_tree_nodes_checked": len(PHASE43_NODE_EXPECTATIONS),
        "missing_nodes": missing_nodes,
        "missing_candidate_links": missing_candidate_links,
    }


def main() -> int:
    errors: list[str] = []
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    payload = load_json(index_path)
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain a list or {items: [...]}.")

    report = {
        "report_id": "phase43_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "scope": "CEK-TA-369 MCP/SearchLab/KnowledgeTree Phase 43 外接项目 AI Memory Layer 29 条 formal reviewed/caveat_only 知识联动验证",
        "index_path": str(index_path),
        "file_index": validate_file_index(items, errors),
        "knowledge_tree": validate_knowledge_tree(errors),
        "searchlab_style": validate_searchlab_style(errors),
        "mcp": validate_mcp(items, index_path, errors),
        "vue_fixtures": validate_vue_fixtures(errors),
        "boundaries": [
            "Phase 43 formal reviewed knowledge must stay caveat_only until separate human approval.",
            "MCP default_guidance_only must block Phase 43 reviewed/caveat_only items.",
            "MCP permissions remain read-only; approval/write requests must be denied.",
            "Project Memory knowledge must not store external project private memory in CEK-TA.",
            "Project Memory knowledge must not create production databases, migrations, vendor activation, or trading execution advice.",
        ],
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }

    report_path = resolve_repo_path("docs", "reports", "phase43_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
