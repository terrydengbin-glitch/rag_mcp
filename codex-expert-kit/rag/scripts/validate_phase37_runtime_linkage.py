"""Validate Phase 37 MCP/SearchLab/KnowledgeTree runtime linkage.

This gate proves that Phase 37 formal reviewed knowledge is reachable from the
official index, KnowledgeTree, API/SearchLab-style filters, Vue fixtures, and
MCP search while staying caveat_only and blocked from default guidance / write
/ approval permissions.
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


TASK_ID = "CEK-TA-419"
PHASE = "Phase 37"
EXPECTED_PHASE37_QUANT_COUNT = 12
PHASE37_PREFIX = "kb_01_quant_foundation."
ROOT_NODE = "kt.quant_foundation"
SAFE_CONFLICT_STATUSES = {"none", "resolved", "none_known_in_visible_context"}

PHASE37_NODE_EXPECTATIONS = {
    "kt.quant_foundation": 8,
    "kt.quant_foundation.position_sizing": 2,
    "kt.quant_foundation.risk_normalized_metrics": 1,
    "kt.quant_foundation.signal_flow": 1,
}

EXPECTED_IDS = [
    "kb_01_quant_foundation.cost_adjusted_expectancy_required.v1",
    "kb_01_quant_foundation.edge_requires_out_of_sample_evidence.v1",
    "kb_01_quant_foundation.expected_value_definition.v1",
    "kb_01_quant_foundation.leverage_amplifies_drawdown.v1",
    "kb_01_quant_foundation.no_profit_claim_without_costs.v1",
    "kb_01_quant_foundation.position_sizing_requires_risk_unit.v1",
    "kb_01_quant_foundation.r_multiple_definition.v1",
    "kb_01_quant_foundation.risk_reward_boundary.v1",
    "kb_01_quant_foundation.sample_size_and_regime_caveat.v1",
    "kb_01_quant_foundation.signal_decision_execution_separation.v1",
    "kb_01_quant_foundation.trade_frequency_vs_quality_boundary.v1",
    "kb_01_quant_foundation.win_rate_not_enough.v1",
]

EXPECTED_PHASE37_BACKTEST_COUNT = 12
BACKTEST_PARTITION_ID = "KB_04_BACKTEST"
BACKTEST_FORMAL_NODE_ID = "kt.trading_engineering.backtest"
BACKTEST_TREE_NODE_ID = "kt.backtest"
BACKTEST_TREE_EXPECTED_NODES = {
    "kt.backtest",
    "kt.backtest.bias",
    "kt.backtest.data_quality",
    "kt.backtest.metrics",
}

BACKTEST_EXPECTED_IDS = [
    "kb_04_backtest.cost_model_required.v1",
    "kb_04_backtest.data_leakage_block.v1",
    "kb_04_backtest.lookahead_bias_block.v1",
    "kb_04_backtest.metric_interpretation_boundary.v1",
    "kb_04_backtest.out_of_sample_required.v1",
    "kb_04_backtest.parameter_search_separate_from_final_eval.v1",
    "kb_04_backtest.profit_factor_drawdown_context_required.v1",
    "kb_04_backtest.reproducibility_package_required.v1",
    "kb_04_backtest.slippage_fee_spread_required.v1",
    "kb_04_backtest.strategy_version_and_data_version_required.v1",
    "kb_04_backtest.survivorship_selection_bias_check.v1",
    "kb_04_backtest.walk_forward_validation_required.v1",
]

PHASE37_SEARCH_CASES = [
    {
        "case_id": "phase37_expected_value_costs",
        "query": "expected value expectancy win rate cost adjusted expectancy no profit claim without costs",
        "canonical_node_id": "kt.quant_foundation",
        "min_results": 4,
    },
    {
        "case_id": "phase37_position_sizing",
        "query": "position sizing requires risk unit leverage drawdown risk budget before signal",
        "canonical_node_id": "kt.quant_foundation.position_sizing",
        "min_results": 2,
    },
    {
        "case_id": "phase37_r_multiple",
        "query": "R multiple initial risk risk normalized trade outcome metric",
        "canonical_node_id": "kt.quant_foundation.risk_normalized_metrics",
        "min_results": 1,
    },
    {
        "case_id": "phase37_signal_decision_execution",
        "query": "signal decision execution separation trade decision signal flow",
        "canonical_node_id": "kt.quant_foundation.signal_flow",
        "min_results": 1,
    },
]

BACKTEST_SEARCH_CASES = [
    {
        "case_id": "phase37_backtest_bias",
        "query": "lookahead bias data leakage survivorship selection bias backtest audit",
        "canonical_node_id": BACKTEST_FORMAL_NODE_ID,
        "min_results": 3,
    },
    {
        "case_id": "phase37_backtest_oos_walk_forward",
        "query": "walk forward validation out of sample parameter search final evaluation separated",
        "canonical_node_id": BACKTEST_FORMAL_NODE_ID,
        "min_results": 3,
    },
    {
        "case_id": "phase37_backtest_cost_metrics",
        "query": "cost model slippage fee spread profit factor drawdown metric interpretation",
        "canonical_node_id": BACKTEST_FORMAL_NODE_ID,
        "min_results": 4,
    },
    {
        "case_id": "phase37_backtest_reproducibility_versioning",
        "query": "reproducibility package strategy version data version backtest run manifest",
        "canonical_node_id": BACKTEST_FORMAL_NODE_ID,
        "min_results": 2,
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


def phase37_quant_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = set(EXPECTED_IDS)
    return [
        item
        for item in items
        if item.get("knowledge_id") in expected
        or (
            item.get("metadata", {}).get("phase") == PHASE
            and item.get("metadata", {}).get("partition_id") == "KB_01_QUANT_FOUNDATION"
        )
    ]


def validate_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = phase37_quant_items(items)
    ids = {item.get("knowledge_id") for item in scoped}
    missing_expected = sorted(set(EXPECTED_IDS) - ids)
    extra_scoped = sorted(ids - set(EXPECTED_IDS))
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    node_counts = Counter(item.get("metadata", {}).get("canonical_node_id", "") for item in scoped)
    partition_counts = Counter(item.get("metadata", {}).get("partition_id", "") for item in scoped)
    source_missing = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    unsafe_conflicts = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("conflict_audit", {}).get("conflict_status") not in SAFE_CONFLICT_STATUSES
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

    assert_condition(errors, len(scoped) == EXPECTED_PHASE37_QUANT_COUNT, f"Phase 37 Quant Foundation count should be {EXPECTED_PHASE37_QUANT_COUNT}, got {len(scoped)}.")
    assert_condition(errors, not missing_expected, f"Phase 37 expected ids missing from index: {missing_expected}.")
    assert_condition(errors, not extra_scoped, f"Phase 37 scoped unexpected ids: {extra_scoped}.")
    assert_condition(errors, dict(review_counts) == {"reviewed": EXPECTED_PHASE37_QUANT_COUNT}, f"Phase 37 review statuses mismatch: {dict(review_counts)}.")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": EXPECTED_PHASE37_QUANT_COUNT}, f"Phase 37 machine gates mismatch: {dict(gate_counts)}.")
    for node_id, expected in PHASE37_NODE_EXPECTATIONS.items():
        assert_condition(errors, node_counts.get(node_id, 0) == expected, f"{node_id} should have {expected} Phase 37 items, got {node_counts.get(node_id, 0)}.")
    assert_condition(errors, not source_missing, f"Phase 37 items missing source_evidence: {source_missing}.")
    assert_condition(errors, not unsafe_conflicts, f"Phase 37 items have unsafe conflicts: {unsafe_conflicts}.")
    assert_condition(errors, not default_enabled, f"Phase 37 reviewed items unexpectedly allow default guidance: {default_enabled}.")
    assert_condition(errors, not approved_enabled, f"Phase 37 reviewed items unexpectedly allow approved: {approved_enabled}.")
    assert_condition(errors, not hard_gate_enabled, f"Phase 37 reviewed items unexpectedly allow hard gate: {hard_gate_enabled}.")

    return {
        "phase37_quant_count": len(scoped),
        "expected_id_count": len(EXPECTED_IDS),
        "missing_expected_ids": missing_expected,
        "extra_scoped_ids": extra_scoped,
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "partition_counts": dict(partition_counts),
        "source_missing_count": len(source_missing),
        "unsafe_conflict_count": len(unsafe_conflicts),
        "default_guidance_enabled_count": len(default_enabled),
        "approved_enabled_count": len(approved_enabled),
        "hard_gate_enabled_count": len(hard_gate_enabled),
    }


def phase37_backtest_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    expected = set(BACKTEST_EXPECTED_IDS)
    return [
        item
        for item in items
        if item.get("knowledge_id") in expected
        or (
            item.get("metadata", {}).get("phase") == PHASE
            and item.get("metadata", {}).get("partition_id") == BACKTEST_PARTITION_ID
        )
    ]


def validate_backtest_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = phase37_backtest_items(items)
    ids = {item.get("knowledge_id") for item in scoped}
    missing_expected = sorted(set(BACKTEST_EXPECTED_IDS) - ids)
    extra_scoped = sorted(ids - set(BACKTEST_EXPECTED_IDS))
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    node_counts = Counter(item.get("metadata", {}).get("canonical_node_id", "") for item in scoped)
    source_missing = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    unsafe_conflicts = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("conflict_audit", {}).get("conflict_status") not in SAFE_CONFLICT_STATUSES
    ]
    default_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("default_guidance_allowed") is True
        or item.get("machine_gate", {}).get("default_guidance") == "allow"
    ]
    approved_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("approved_allowed") is True
        or item.get("review", {}).get("review_status") == "approved"
    ]
    hard_gate_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("hard_gate_allowed") is True
        or item.get("machine_gate", {}).get("hard_gate_allowed") is True
    ]

    assert_condition(errors, len(scoped) == EXPECTED_PHASE37_BACKTEST_COUNT, f"Phase 37 Backtest count should be {EXPECTED_PHASE37_BACKTEST_COUNT}, got {len(scoped)}.")
    assert_condition(errors, not missing_expected, f"Phase 37 Backtest expected ids missing from index: {missing_expected}.")
    assert_condition(errors, not extra_scoped, f"Phase 37 Backtest scoped unexpected ids: {extra_scoped}.")
    assert_condition(errors, dict(review_counts) == {"reviewed": EXPECTED_PHASE37_BACKTEST_COUNT}, f"Phase 37 Backtest review statuses mismatch: {dict(review_counts)}.")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": EXPECTED_PHASE37_BACKTEST_COUNT}, f"Phase 37 Backtest machine gates mismatch: {dict(gate_counts)}.")
    assert_condition(errors, node_counts.get(BACKTEST_FORMAL_NODE_ID, 0) == EXPECTED_PHASE37_BACKTEST_COUNT, f"{BACKTEST_FORMAL_NODE_ID} should have {EXPECTED_PHASE37_BACKTEST_COUNT} Backtest items, got {node_counts.get(BACKTEST_FORMAL_NODE_ID, 0)}.")
    assert_condition(errors, not source_missing, f"Phase 37 Backtest items missing source_evidence: {source_missing}.")
    assert_condition(errors, not unsafe_conflicts, f"Phase 37 Backtest items have unsafe conflicts: {unsafe_conflicts}.")
    assert_condition(errors, not default_enabled, f"Phase 37 Backtest reviewed items unexpectedly allow default guidance: {default_enabled}.")
    assert_condition(errors, not approved_enabled, f"Phase 37 Backtest reviewed items unexpectedly allow approved: {approved_enabled}.")
    assert_condition(errors, not hard_gate_enabled, f"Phase 37 Backtest reviewed items unexpectedly allow hard gate: {hard_gate_enabled}.")

    return {
        "phase37_backtest_count": len(scoped),
        "expected_id_count": len(BACKTEST_EXPECTED_IDS),
        "missing_expected_ids": missing_expected,
        "extra_scoped_ids": extra_scoped,
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "source_missing_count": len(source_missing),
        "unsafe_conflict_count": len(unsafe_conflicts),
        "default_guidance_enabled_count": len(default_enabled),
        "approved_enabled_count": len(approved_enabled),
        "hard_gate_enabled_count": len(hard_gate_enabled),
    }


def validate_knowledge_tree(errors: list[str]) -> dict[str, Any]:
    browse_module = load_module(
        "phase37_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree({"node_id": ROOT_NODE, "include_children": True})
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    expected_nodes = set(PHASE37_NODE_EXPECTATIONS)
    missing_tree_nodes = sorted(expected_nodes - node_ids)
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree missing Phase 37 nodes: {missing_tree_nodes}.")
    return {
        "quant_foundation_node_count": len(nodes),
        "phase37_tree_nodes_expected": len(expected_nodes),
        "phase37_tree_nodes_found": sorted(expected_nodes & node_ids),
        "missing_tree_nodes": missing_tree_nodes,
    }


def validate_backtest_knowledge_tree(errors: list[str]) -> dict[str, Any]:
    browse_module = load_module(
        "phase37_backtest_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree({"node_id": BACKTEST_TREE_NODE_ID, "include_children": True})
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    missing_tree_nodes = sorted(BACKTEST_TREE_EXPECTED_NODES - node_ids)
    assert_condition(errors, response.get("status") == "ok", f"Backtest knowledge tree browse status is {response.get('status')}.")
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree missing Backtest nodes: {missing_tree_nodes}.")
    return {
        "backtest_node_count": len(nodes),
        "backtest_tree_nodes_expected": len(BACKTEST_TREE_EXPECTED_NODES),
        "backtest_tree_nodes_found": sorted(BACKTEST_TREE_EXPECTED_NODES & node_ids),
        "missing_tree_nodes": missing_tree_nodes,
        "note": "MCP browse_knowledge_tree validates tree topology only; formal counts are validated by SearchLab/API and Vue fixtures.",
    }


def validate_searchlab_style(errors: list[str]) -> dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")
    results: dict[str, Any] = {}
    for node_id, expected_count in PHASE37_NODE_EXPECTATIONS.items():
        filtered = api_module.filter_items(node_id)
        phase37_filtered = [item for item in filtered if item.get("knowledge_id") in EXPECTED_IDS]
        statuses = sorted({item.get("review", {}).get("review_status", "") for item in phase37_filtered})
        gates = sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in phase37_filtered})
        results[node_id] = {
            "phase37_count": len(phase37_filtered),
            "expected_count": expected_count,
            "review_statuses": statuses,
            "machine_gates": gates,
        }
        assert_condition(errors, len(phase37_filtered) >= expected_count, f"SearchLab/API filter returned {len(phase37_filtered)} Phase 37 items for {node_id}, expected at least {expected_count}.")
        assert_condition(errors, statuses == ["reviewed"], f"SearchLab/API statuses mismatch for {node_id}: {statuses}.")
        assert_condition(errors, gates == ["caveat_only"], f"SearchLab/API gates mismatch for {node_id}: {gates}.")
    return results


def validate_backtest_searchlab_style(errors: list[str]) -> dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")
    filtered = api_module.filter_items(BACKTEST_TREE_NODE_ID)
    phase37_filtered = [item for item in filtered if item.get("knowledge_id") in BACKTEST_EXPECTED_IDS]
    statuses = sorted({item.get("review", {}).get("review_status", "") for item in phase37_filtered})
    gates = sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in phase37_filtered})
    assert_condition(errors, len(phase37_filtered) >= EXPECTED_PHASE37_BACKTEST_COUNT, f"SearchLab/API Backtest filter returned {len(phase37_filtered)} Phase 37 Backtest items, expected {EXPECTED_PHASE37_BACKTEST_COUNT}.")
    assert_condition(errors, statuses == ["reviewed"], f"SearchLab/API Backtest statuses mismatch: {statuses}.")
    assert_condition(errors, gates == ["caveat_only"], f"SearchLab/API Backtest gates mismatch: {gates}.")
    return {
        "node_id": BACKTEST_TREE_NODE_ID,
        "phase37_count": len(phase37_filtered),
        "expected_count": EXPECTED_PHASE37_BACKTEST_COUNT,
        "review_statuses": statuses,
        "machine_gates": gates,
        "top_ids": [item.get("knowledge_id") for item in phase37_filtered[:12]],
    }


def validate_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase37_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    case_results: dict[str, Any] = {}
    for case in PHASE37_SEARCH_CASES:
        request = {
            "request_id": case["case_id"],
            "query": case["query"],
            "top_k": 8,
            "filters": {"canonical_node_id": case["canonical_node_id"]},
            "include": {"reviewed": True, "default_guidance_only": False},
        }
        response = mcp_module.search_expert_knowledge(request, knowledge_items_path=str(index_path))
        results = [result for result in response.get("results", []) if result.get("knowledge_id") in EXPECTED_IDS]
        case_results[case["case_id"]] = {
            "status": response.get("status"),
            "phase37_result_count": len(results),
            "top_knowledge_ids": [result.get("knowledge_id") for result in results[:5]],
            "first_result": results[0] if results else None,
        }
        assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP search status for {case['case_id']} is {response.get('status')}.")
        assert_condition(errors, len(results) >= int(case["min_results"]), f"MCP search {case['case_id']} returned {len(results)} Phase 37 results.")
        if results:
            first = results[0]
            assert_condition(errors, first.get("source_count", 0) > 0, f"MCP {case['case_id']} first result has no sources.")
            assert_condition(errors, first.get("review_status") == "reviewed", f"MCP {case['case_id']} first result is not reviewed.")
            assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP {case['case_id']} first result is not caveat_only.")
            assert_condition(errors, first.get("acceptance_level") == "accepted_reference", f"MCP {case['case_id']} acceptance level mismatch.")

    block_request = {
        "request_id": "phase37-default-guidance-block",
        "query": "expected value position sizing R multiple cost adjusted expectancy",
        "top_k": 12,
        "filters": {"partition_id": "KB_01_QUANT_FOUNDATION"},
        "include": {"reviewed": True, "default_guidance_only": True},
    }
    blocked_response = mcp_module.search_expert_knowledge(block_request, knowledge_items=items)
    phase37_blocked = [
        item
        for item in blocked_response.get("blocked_results", [])
        if item.get("knowledge_id") in EXPECTED_IDS
    ]
    phase37_allowed = [
        item
        for item in blocked_response.get("results", [])
        if item.get("knowledge_id") in EXPECTED_IDS
    ]
    assert_condition(errors, not phase37_allowed, "MCP default_guidance_only unexpectedly returned Phase 37 reviewed/caveat_only results.")
    assert_condition(errors, len(phase37_blocked) == EXPECTED_PHASE37_QUANT_COUNT, f"MCP default_guidance_only blocked {len(phase37_blocked)} Phase 37 items, expected {EXPECTED_PHASE37_QUANT_COUNT}.")

    permission_response = mcp_module.search_expert_knowledge(
        {
            "request_id": "phase37-permission-deny",
            "query": "promote Quant Foundation to approved default guidance",
            "requested_permission": "approve_knowledge",
        },
        knowledge_items=items,
    )
    assert_condition(errors, bool(permission_response.get("errors")), "MCP approval/write permission was not denied.")

    return {
        "search_cases": case_results,
        "default_guidance_blocked_count": blocked_response.get("audit", {}).get("blocked_count", 0),
        "phase37_blocked_count": len(phase37_blocked),
        "phase37_allowed_in_default_guidance_count": len(phase37_allowed),
        "permission_denied": bool(permission_response.get("errors")),
    }


def validate_backtest_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase37_backtest_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    case_results: dict[str, Any] = {}
    for case in BACKTEST_SEARCH_CASES:
        request = {
            "request_id": case["case_id"],
            "query": case["query"],
            "top_k": 12,
            "filters": {"canonical_node_id": case["canonical_node_id"]},
            "include": {"reviewed": True, "default_guidance_only": False},
        }
        response = mcp_module.search_expert_knowledge(request, knowledge_items_path=str(index_path))
        results = [result for result in response.get("results", []) if result.get("knowledge_id") in BACKTEST_EXPECTED_IDS]
        case_results[case["case_id"]] = {
            "status": response.get("status"),
            "phase37_result_count": len(results),
            "top_knowledge_ids": [result.get("knowledge_id") for result in results[:8]],
            "first_result": results[0] if results else None,
        }
        assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP Backtest search status for {case['case_id']} is {response.get('status')}.")
        assert_condition(errors, len(results) >= int(case["min_results"]), f"MCP Backtest search {case['case_id']} returned {len(results)} Phase 37 Backtest results.")
        if results:
            first = results[0]
            assert_condition(errors, first.get("source_count", 0) > 0, f"MCP Backtest {case['case_id']} first result has no sources.")
            assert_condition(errors, first.get("review_status") == "reviewed", f"MCP Backtest {case['case_id']} first result is not reviewed.")
            assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP Backtest {case['case_id']} first result is not caveat_only.")
            assert_condition(errors, first.get("acceptance_level") == "accepted_reference", f"MCP Backtest {case['case_id']} acceptance level mismatch.")

    block_request = {
        "request_id": "phase37-backtest-default-guidance-block",
        "query": "backtest reproducibility data leakage lookahead cost model strategy version",
        "top_k": 12,
        "filters": {"partition_id": BACKTEST_PARTITION_ID},
        "include": {"reviewed": True, "default_guidance_only": True},
    }
    blocked_response = mcp_module.search_expert_knowledge(block_request, knowledge_items=items)
    phase37_blocked = [
        item for item in blocked_response.get("blocked_results", []) if item.get("knowledge_id") in BACKTEST_EXPECTED_IDS
    ]
    phase37_allowed = [
        item for item in blocked_response.get("results", []) if item.get("knowledge_id") in BACKTEST_EXPECTED_IDS
    ]
    assert_condition(errors, not phase37_allowed, "MCP default_guidance_only unexpectedly returned Phase 37 Backtest reviewed/caveat_only results.")
    assert_condition(errors, len(phase37_blocked) == EXPECTED_PHASE37_BACKTEST_COUNT, f"MCP default_guidance_only blocked {len(phase37_blocked)} Backtest items, expected {EXPECTED_PHASE37_BACKTEST_COUNT}.")

    permission_response = mcp_module.search_expert_knowledge(
        {
            "request_id": "phase37-backtest-permission-deny",
            "query": "promote Backtest to approved default guidance",
            "requested_permission": "approve_knowledge",
        },
        knowledge_items=items,
    )
    assert_condition(errors, bool(permission_response.get("errors")), "MCP Backtest approval/write permission was not denied.")
    return {
        "search_cases": case_results,
        "default_guidance_blocked_count": blocked_response.get("audit", {}).get("blocked_count", 0),
        "phase37_backtest_blocked_count": len(phase37_blocked),
        "phase37_backtest_allowed_in_default_guidance_count": len(phase37_allowed),
        "permission_denied": bool(permission_response.get("errors")),
    }


def validate_vue_fixtures(errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    candidate_fixture = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    candidate_text = candidate_fixture.read_text(encoding="utf-8")
    missing_ids = [knowledge_id for knowledge_id in EXPECTED_IDS if knowledge_id not in formal_text]
    missing_nodes = [node_id for node_id in PHASE37_NODE_EXPECTATIONS if node_id not in tree_text]
    missing_candidate_links = [knowledge_id for knowledge_id in EXPECTED_IDS if knowledge_id not in candidate_text]
    assert_condition(errors, not missing_ids, f"Vue formalKnowledgeItems fixture missing Phase 37 ids: {missing_ids}.")
    assert_condition(errors, not missing_nodes, f"Vue knowledgeTreeNodes fixture missing Phase 37 nodes: {missing_nodes}.")
    assert_condition(errors, not missing_candidate_links, f"Vue candidate fixture missing Phase 37 formal links: {missing_candidate_links}.")
    return {
        "formal_fixture": str(formal_fixture),
        "tree_fixture": str(tree_fixture),
        "candidate_fixture": str(candidate_fixture),
        "expected_ids_checked": len(EXPECTED_IDS),
        "missing_ids": missing_ids,
        "phase37_tree_nodes_checked": len(PHASE37_NODE_EXPECTATIONS),
        "missing_nodes": missing_nodes,
        "missing_candidate_links": missing_candidate_links,
    }


def validate_backtest_vue_fixtures(errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    candidate_fixture = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    candidate_text = candidate_fixture.read_text(encoding="utf-8")
    missing_ids = [knowledge_id for knowledge_id in BACKTEST_EXPECTED_IDS if knowledge_id not in formal_text]
    missing_nodes = [node_id for node_id in BACKTEST_TREE_EXPECTED_NODES if node_id not in tree_text]
    missing_candidate_links = [knowledge_id for knowledge_id in BACKTEST_EXPECTED_IDS if knowledge_id not in candidate_text]
    assert_condition(errors, not missing_ids, f"Vue formalKnowledgeItems fixture missing Backtest ids: {missing_ids}.")
    assert_condition(errors, not missing_nodes, f"Vue knowledgeTreeNodes fixture missing Backtest nodes: {missing_nodes}.")
    assert_condition(errors, not missing_candidate_links, f"Vue candidate fixture missing Backtest formal links: {missing_candidate_links}.")
    return {
        "formal_fixture": str(formal_fixture),
        "tree_fixture": str(tree_fixture),
        "candidate_fixture": str(candidate_fixture),
        "expected_ids_checked": len(BACKTEST_EXPECTED_IDS),
        "missing_ids": missing_ids,
        "backtest_tree_nodes_checked": len(BACKTEST_TREE_EXPECTED_NODES),
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
        "report_id": "phase37_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "scope": "CEK-TA-419 MCP/SearchLab/KnowledgeTree Phase 37 Quant Foundation + Backtest formal reviewed/caveat_only 知识联动验证",
        "index_path": str(index_path),
        "quant_foundation": {
            "file_index": validate_file_index(items, errors),
            "knowledge_tree": validate_knowledge_tree(errors),
            "searchlab_style": validate_searchlab_style(errors),
            "mcp": validate_mcp(items, index_path, errors),
            "vue_fixtures": validate_vue_fixtures(errors),
        },
        "backtest": {
            "file_index": validate_backtest_file_index(items, errors),
            "knowledge_tree": validate_backtest_knowledge_tree(errors),
            "searchlab_style": validate_backtest_searchlab_style(errors),
            "mcp": validate_backtest_mcp(items, index_path, errors),
            "vue_fixtures": validate_backtest_vue_fixtures(errors),
        },
        "boundaries": [
            "Phase 37 Quant Foundation formal reviewed knowledge must stay caveat_only until separate human approval.",
            "Phase 37 Backtest formal reviewed knowledge must stay caveat_only until separate human approval.",
            "none_known_in_visible_context is accepted only as caveat_only and must not be promoted to approved/default guidance.",
            "MCP default_guidance_only must block Phase 37 reviewed/caveat_only items.",
            "MCP permissions remain read-only; approval/write/trade requests must be denied.",
            "Trading Engineering knowledge must not become buy/sell, leverage, position-size, stop-loss/take-profit, or live-execution advice.",
            "SearchLab and KnowledgeTree must read formal knowledge from the official index, not from candidate queues.",
        ],
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }

    report_path = resolve_repo_path("docs", "reports", "phase37_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
