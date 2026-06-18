"""Validate Phase 42 MCP/SearchLab/KnowledgeTree runtime linkage."""

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


TASK_ID = "CEK-TA-356"
PHASE = "Phase 42"
EXPECTED_PHASE42_COUNT = 34
PHASE42_PREFIX = "kb_ai_database_storage.phase42."

PHASE42_NODE_EXPECTATIONS = {
    "kt.ai_engineering.database_storage_engineering.audit_log_ledger": 4,
    "kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery": 1,
    "kt.ai_engineering.database_storage_engineering.data_contract_lineage": 6,
    "kt.ai_engineering.database_storage_engineering.data_lifecycle_retention": 1,
    "kt.ai_engineering.database_storage_engineering.feature_store_storage": 3,
    "kt.ai_engineering.database_storage_engineering.migration_versioning": 3,
    "kt.ai_engineering.database_storage_engineering.model_registry_release_storage": 2,
    "kt.ai_engineering.database_storage_engineering.relational_core_schema": 3,
    "kt.ai_engineering.database_storage_engineering.runtime_observability_trace": 1,
    "kt.ai_engineering.database_storage_engineering.security_privacy_access_control": 3,
    "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage": 7,
}

PHASE42_SEARCH_CASES = [
    {
        "case_id": "phase42_canonical_store",
        "query": "PostgreSQL canonical records vector database source of truth constraints",
        "canonical_node_id": "kt.ai_engineering.database_storage_engineering.relational_core_schema",
        "min_results": 2,
    },
    {
        "case_id": "phase42_lineage_time",
        "query": "decision_time event_time label_time dataset hash point in time correctness",
        "canonical_node_id": "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "min_results": 3,
    },
    {
        "case_id": "phase42_vector_storage",
        "query": "RAG chunks embedding model version vector search source provenance",
        "canonical_node_id": "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "min_results": 3,
    },
    {
        "case_id": "phase42_audit_ledger",
        "query": "final gate append only audit ledger actor reason trace id row hash",
        "canonical_node_id": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "min_results": 3,
    },
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


def phase42_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in items
        if item.get("metadata", {}).get("phase") == PHASE
        or str(item.get("knowledge_id", "")).startswith(PHASE42_PREFIX)
    ]


def validate_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = phase42_items(items)
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
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
    production_allowed = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("phase42_conversion", {}).get("production_database_changes_allowed") is not False
    ]

    assert_condition(errors, len(scoped) == EXPECTED_PHASE42_COUNT, f"Phase 42 formal reviewed count should be {EXPECTED_PHASE42_COUNT}, got {len(scoped)}.")
    assert_condition(errors, dict(review_counts) == {"reviewed": EXPECTED_PHASE42_COUNT}, f"Phase 42 review statuses mismatch: {dict(review_counts)}.")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": EXPECTED_PHASE42_COUNT}, f"Phase 42 machine gates mismatch: {dict(gate_counts)}.")
    for node_id, expected in PHASE42_NODE_EXPECTATIONS.items():
        assert_condition(errors, node_counts.get(node_id, 0) == expected, f"{node_id} should have {expected} items, got {node_counts.get(node_id, 0)}.")
    assert_condition(errors, not source_missing, f"Phase 42 items missing source_evidence: {source_missing}.")
    assert_condition(errors, not unsafe_conflicts, f"Phase 42 items have unsafe conflicts: {unsafe_conflicts}.")
    assert_condition(errors, not default_enabled, f"Phase 42 reviewed items unexpectedly allow default guidance: {default_enabled}.")
    assert_condition(errors, not production_allowed, f"Phase 42 items unexpectedly allow production DB changes: {production_allowed}.")

    return {
        "phase42_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "partition_counts": dict(partition_counts),
        "source_missing_count": len(source_missing),
        "unsafe_conflict_count": len(unsafe_conflicts),
        "default_guidance_enabled_count": len(default_enabled),
        "production_database_changes_allowed_count": len(production_allowed),
    }


def validate_knowledge_tree(errors: list[str]) -> dict[str, Any]:
    browse_module = load_module(
        "phase42_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree(
        {"node_id": "kt.ai_engineering.database_storage_engineering", "include_children": True}
    )
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    expected_nodes = set(PHASE42_NODE_EXPECTATIONS)
    missing_tree_nodes = sorted(expected_nodes - node_ids)
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree missing Phase 42 nodes: {missing_tree_nodes}.")
    return {
        "database_storage_node_count": len(nodes),
        "phase42_tree_nodes_expected": len(expected_nodes),
        "phase42_tree_nodes_found": sorted(expected_nodes & node_ids),
        "missing_tree_nodes": missing_tree_nodes,
    }


def validate_searchlab_style(errors: list[str]) -> dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")
    results: dict[str, Any] = {}
    sample_nodes = [
        "kt.ai_engineering.database_storage_engineering.relational_core_schema",
        "kt.ai_engineering.database_storage_engineering.data_contract_lineage",
        "kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage",
        "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
    ]
    for node_id in sample_nodes:
        filtered = api_module.filter_items(node_id)
        phase42_filtered = [
            item
            for item in filtered
            if item.get("metadata", {}).get("phase") == PHASE
            or str(item.get("knowledge_id", "")).startswith(PHASE42_PREFIX)
        ]
        statuses = sorted({item.get("review", {}).get("review_status", "") for item in phase42_filtered})
        gates = sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in phase42_filtered})
        results[node_id] = {
            "phase42_count": len(phase42_filtered),
            "review_statuses": statuses,
            "machine_gates": gates,
        }
        assert_condition(errors, bool(phase42_filtered), f"SearchLab/API filter did not return Phase 42 items for {node_id}.")
        assert_condition(errors, statuses == ["reviewed"], f"SearchLab/API statuses mismatch for {node_id}: {statuses}.")
        assert_condition(errors, gates == ["caveat_only"], f"SearchLab/API gates mismatch for {node_id}: {gates}.")
    return results


def validate_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase42_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    case_results: dict[str, Any] = {}
    for case in PHASE42_SEARCH_CASES:
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
            if str(result.get("knowledge_id", "")).startswith(PHASE42_PREFIX)
        ]
        case_results[case["case_id"]] = {
            "status": response.get("status"),
            "phase42_result_count": len(results),
            "top_knowledge_ids": [result.get("knowledge_id") for result in results[:5]],
            "first_result": results[0] if results else None,
        }
        assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP search status for {case['case_id']} is {response.get('status')}.")
        assert_condition(errors, len(results) >= int(case["min_results"]), f"MCP search {case['case_id']} returned {len(results)} Phase 42 results.")
        if results:
            first = results[0]
            assert_condition(errors, first.get("source_count", 0) > 0, f"MCP {case['case_id']} first result has no sources.")
            assert_condition(errors, first.get("review_status") == "reviewed", f"MCP {case['case_id']} first result is not reviewed.")
            assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP {case['case_id']} first result is not caveat_only.")
            assert_condition(errors, first.get("acceptance_level") == "accepted_reference", f"MCP {case['case_id']} acceptance level mismatch.")

    block_request = {
        "request_id": "phase42-default-guidance-block",
        "query": "PostgreSQL canonical store vector database audit ledger",
        "top_k": 10,
        "filters": {"canonical_node_id": "kt.ai_engineering.database_storage_engineering.relational_core_schema"},
        "include": {"reviewed": True, "default_guidance_only": True},
    }
    blocked_response = mcp_module.search_expert_knowledge(block_request, knowledge_items=items)
    phase42_blocked = [
        item
        for item in blocked_response.get("blocked_results", [])
        if str(item.get("knowledge_id", "")).startswith(PHASE42_PREFIX)
    ]
    assert_condition(errors, not [r for r in blocked_response.get("results", []) if str(r.get("knowledge_id", "")).startswith(PHASE42_PREFIX)], "MCP default_guidance_only unexpectedly returned Phase 42 caveat_only results.")
    assert_condition(errors, bool(phase42_blocked), "MCP default_guidance_only did not block Phase 42 caveat_only results.")

    permission_response = mcp_module.search_expert_knowledge(
        {
            "request_id": "phase42-permission-deny",
            "query": "database migration approval",
            "requested_permission": "approve_knowledge",
        },
        knowledge_items=items,
    )
    assert_condition(errors, bool(permission_response.get("errors")), "MCP approval/write permission was not denied.")

    return {
        "search_cases": case_results,
        "default_guidance_blocked_count": blocked_response.get("audit", {}).get("blocked_count", 0),
        "phase42_blocked_count": len(phase42_blocked),
        "permission_denied": bool(permission_response.get("errors")),
    }


def validate_vue_fixtures(errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    candidate_fixture = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    candidate_text = candidate_fixture.read_text(encoding="utf-8")
    expected_ids = [
        "kb_ai_database_storage.phase42.canonical_records_postgresql_not_vector_db.v1",
        "kb_ai_database_storage.phase42.every_decision_requires_audit_trace_id.v1",
        "kb_ai_database_storage.phase42.final_gate_decision_append_only.v1",
        "kb_ai_database_storage.phase42.rag_chunks_store_source_license_hash_version.v1",
        "kb_ai_database_storage.phase42.dataset_snapshot_manifest_dataset_hash.v1",
        "kb_ai_database_storage.phase42.backup_restore_must_be_tested.v1",
        "kb_ai_database_storage.phase42.pgvector_vs_qdrant_selection_boundary.v1",
        "kb_ai_database_storage.phase42.qdrant_payload_index_metadata_filter_rule.v1",
        "kb_ai_database_storage.phase42.rls_pgaudit_adoption_boundary.v1",
    ]
    missing_ids = [knowledge_id for knowledge_id in expected_ids if knowledge_id not in formal_text]
    missing_nodes = [node_id for node_id in PHASE42_NODE_EXPECTATIONS if node_id not in tree_text]
    missing_candidate_links = [knowledge_id for knowledge_id in expected_ids if knowledge_id not in candidate_text]
    assert_condition(errors, not missing_ids, f"Vue formalKnowledgeItems fixture missing Phase 42 ids: {missing_ids}.")
    assert_condition(errors, not missing_nodes, f"Vue knowledgeTreeNodes fixture missing Phase 42 nodes: {missing_nodes}.")
    assert_condition(errors, not missing_candidate_links, f"Vue candidate fixture missing Phase 42 formal links: {missing_candidate_links}.")
    return {
        "formal_fixture": str(formal_fixture),
        "tree_fixture": str(tree_fixture),
        "candidate_fixture": str(candidate_fixture),
        "expected_ids_checked": len(expected_ids),
        "missing_ids": missing_ids,
        "phase42_tree_nodes_checked": len(PHASE42_NODE_EXPECTATIONS),
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
        "report_id": "phase42_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "scope": "CEK-TA-356 MCP/SearchLab/KnowledgeTree Phase 42 全量 34 条数据库存储知识联动验证",
        "index_path": str(index_path),
        "file_index": validate_file_index(items, errors),
        "knowledge_tree": validate_knowledge_tree(errors),
        "searchlab_style": validate_searchlab_style(errors),
        "mcp": validate_mcp(items, index_path, errors),
        "vue_fixtures": validate_vue_fixtures(errors),
        "boundaries": [
            "Phase 42 formal reviewed knowledge must stay caveat_only until separate human approval.",
            "MCP default_guidance_only must block Phase 42 reviewed/caveat_only items.",
            "MCP permissions remain read-only; approval/write requests must be denied.",
            "Phase 42 knowledge must not create production databases, execute migrations, or define Trading Engineering bodies.",
        ],
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }

    report_path = resolve_repo_path("docs", "reports", "phase42_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
