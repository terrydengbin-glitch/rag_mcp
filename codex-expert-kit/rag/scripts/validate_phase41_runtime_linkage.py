"""Validate Phase 41 MCP/SearchLab/KnowledgeTree runtime linkage.

The validation proves that Phase 41 formal reviewed knowledge is reachable
from the official file index, KnowledgeTree, API/SearchLab-style filters, and
MCP search while still being blocked from default-guidance-only retrieval.
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


TASK_ID = "CEK-TA-334"
PHASE = "Phase 41"
EXPECTED_PHASE41_COUNT = 41

PHASE41_TREE_NODES = {
    "kt.ai_engineering.numeric_scoring.model_family_selection",
    "kt.ai_engineering.numeric_scoring.tabular_scorer_training",
    "kt.ai_engineering.numeric_scoring.scorer_explainability",
    "kt.ai_engineering.calibration_threshold.uncertainty",
    "kt.ai_engineering.decision_time_feature_contract.feature_store",
    "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant",
    "kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe",
    "kt.ai_engineering.model_release_governance.hybrid_runtime_contract",
    "kt.ai_engineering.model_release_governance.training_platform_governance",
}

PHASE41_FORMAL_NODE_EXPECTATIONS = {
    "kt.ai_engineering.numeric_scoring.model_family_selection": 6,
    "kt.ai_engineering.numeric_scoring.tabular_scorer_training": 6,
    "kt.ai_engineering.numeric_scoring.scorer_explainability": 1,
    "kt.ai_engineering.calibration_threshold.uncertainty": 6,
    "kt.ai_engineering.decision_time_feature_contract.feature_store": 5,
    "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant": 5,
    "kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe": 4,
    "kt.ai_engineering.model_release_governance.hybrid_runtime_contract": 5,
    "kt.ai_engineering.model_release_governance.training_platform_governance": 3,
}

PHASE41_SEARCH_CASES = [
    {
        "case_id": "phase41_numeric_scoring",
        "query": "LightGBM XGBoost Logistic Regression scorer business cost latency calibration governance",
        "canonical_node_id": "kt.ai_engineering.numeric_scoring.model_family_selection",
        "min_results": 3,
    },
    {
        "case_id": "phase41_qwen_audit",
        "query": "Qwen3 audit assistant strict JSON citation abstain",
        "canonical_node_id": "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant",
        "min_results": 3,
    },
    {
        "case_id": "phase41_feature_lineage",
        "query": "TrainingDatasetManifest FeatureLineageRecord dataset_hash source_object_ref",
        "canonical_node_id": "kt.ai_engineering.decision_time_feature_contract.feature_store",
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


def phase41_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in items
        if item.get("metadata", {}).get("phase") == PHASE
        or str(item.get("knowledge_id", "")).startswith("kb_ai_hybrid_scoring.phase41.")
    ]


def validate_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = phase41_items(items)
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

    assert_condition(errors, len(scoped) == EXPECTED_PHASE41_COUNT, f"Phase 41 formal reviewed count should be {EXPECTED_PHASE41_COUNT}, got {len(scoped)}.")
    assert_condition(errors, dict(review_counts) == {"reviewed": EXPECTED_PHASE41_COUNT}, f"Phase 41 review statuses mismatch: {dict(review_counts)}.")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": EXPECTED_PHASE41_COUNT}, f"Phase 41 machine gates mismatch: {dict(gate_counts)}.")
    for node_id, expected in PHASE41_FORMAL_NODE_EXPECTATIONS.items():
        assert_condition(errors, node_counts.get(node_id, 0) == expected, f"{node_id} should have {expected} items, got {node_counts.get(node_id, 0)}.")
    assert_condition(errors, not source_missing, f"Phase 41 items missing source_evidence: {source_missing}.")
    assert_condition(errors, not unsafe_conflicts, f"Phase 41 items have unsafe conflicts: {unsafe_conflicts}.")
    assert_condition(errors, not default_enabled, f"Phase 41 reviewed items unexpectedly allow default guidance: {default_enabled}.")

    return {
        "phase41_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "partition_counts": dict(partition_counts),
        "source_missing_count": len(source_missing),
        "unsafe_conflict_count": len(unsafe_conflicts),
        "default_guidance_enabled_count": len(default_enabled),
    }


def validate_knowledge_tree(errors: list[str]) -> dict[str, Any]:
    browse_module = load_module(
        "phase41_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )
    response = browse_module.browse_knowledge_tree({"node_id": "kt.ai_engineering", "include_children": True})
    nodes = response.get("nodes", [])
    node_ids = {node.get("node_id") for node in nodes}
    missing_tree_nodes = sorted(PHASE41_TREE_NODES - node_ids)
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree missing Phase 41 nodes: {missing_tree_nodes}.")

    return {
        "ai_engineering_node_count": len(nodes),
        "phase41_tree_nodes_expected": len(PHASE41_TREE_NODES),
        "phase41_tree_nodes_found": sorted(PHASE41_TREE_NODES & node_ids),
        "missing_tree_nodes": missing_tree_nodes,
    }


def validate_searchlab_style(errors: list[str]) -> dict[str, Any]:
    api_module = importlib.import_module("codex_expert_kit_api.services")
    results: dict[str, Any] = {}
    sample_nodes = [
        "kt.ai_engineering.numeric_scoring",
        "kt.ai_engineering.llm_audit_assistant",
        "kt.ai_engineering.decision_time_feature_contract",
        "kt.ai_engineering.model_release_governance",
    ]
    for node_id in sample_nodes:
        filtered = api_module.filter_items(node_id)
        phase41_filtered = [
            item
            for item in filtered
            if item.get("metadata", {}).get("phase") == PHASE
            or str(item.get("knowledge_id", "")).startswith("kb_ai_hybrid_scoring.phase41.")
        ]
        statuses = sorted({item.get("review", {}).get("review_status", "") for item in phase41_filtered})
        gates = sorted({item.get("machine_gate", {}).get("default_guidance", "") for item in phase41_filtered})
        results[node_id] = {
            "phase41_count": len(phase41_filtered),
            "review_statuses": statuses,
            "machine_gates": gates,
        }
        assert_condition(errors, bool(phase41_filtered), f"SearchLab/API filter did not return Phase 41 items for {node_id}.")
        assert_condition(errors, statuses == ["reviewed"], f"SearchLab/API statuses mismatch for {node_id}: {statuses}.")
        assert_condition(errors, gates == ["caveat_only"], f"SearchLab/API gates mismatch for {node_id}: {gates}.")
    return results


def validate_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase41_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    case_results: dict[str, Any] = {}
    for case in PHASE41_SEARCH_CASES:
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
            if str(result.get("knowledge_id", "")).startswith("kb_ai_hybrid_scoring.phase41.")
        ]
        case_results[case["case_id"]] = {
            "status": response.get("status"),
            "phase41_result_count": len(results),
            "top_knowledge_ids": [result.get("knowledge_id") for result in results[:5]],
            "first_result": results[0] if results else None,
        }
        assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP search status for {case['case_id']} is {response.get('status')}.")
        assert_condition(errors, len(results) >= int(case["min_results"]), f"MCP search {case['case_id']} returned {len(results)} Phase 41 results.")
        if results:
            first = results[0]
            assert_condition(errors, first.get("source_count", 0) > 0, f"MCP {case['case_id']} first result has no sources.")
            assert_condition(errors, first.get("review_status") == "reviewed", f"MCP {case['case_id']} first result is not reviewed.")
            assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP {case['case_id']} first result is not caveat_only.")
            assert_condition(errors, first.get("acceptance_level") == "accepted_reference", f"MCP {case['case_id']} acceptance level mismatch.")

    block_request = {
        "request_id": "phase41-default-guidance-block",
        "query": "Qwen3 final gate scoring dataset_hash",
        "top_k": 10,
        "filters": {"canonical_node_id": "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant"},
        "include": {"reviewed": True, "default_guidance_only": True},
    }
    blocked_response = mcp_module.search_expert_knowledge(block_request, knowledge_items=items)
    phase41_blocked = [
        item
        for item in blocked_response.get("blocked_results", [])
        if str(item.get("knowledge_id", "")).startswith("kb_ai_hybrid_scoring.phase41.")
    ]
    assert_condition(errors, not [r for r in blocked_response.get("results", []) if str(r.get("knowledge_id", "")).startswith("kb_ai_hybrid_scoring.phase41.")], "MCP default_guidance_only unexpectedly returned Phase 41 caveat_only results.")
    assert_condition(errors, bool(phase41_blocked), "MCP default_guidance_only did not block Phase 41 caveat_only results.")

    permission_response = mcp_module.search_expert_knowledge(
        {
            "request_id": "phase41-permission-deny",
            "query": "Qwen3 scoring",
            "requested_permission": "approve_knowledge",
        },
        knowledge_items=items,
    )
    assert_condition(errors, bool(permission_response.get("errors")), "MCP approval/write permission was not denied.")

    return {
        "search_cases": case_results,
        "default_guidance_blocked_count": blocked_response.get("audit", {}).get("blocked_count", 0),
        "phase41_blocked_count": len(phase41_blocked),
        "permission_denied": bool(permission_response.get("errors")),
    }


def validate_vue_fixtures(errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    expected_ids = [
        "kb_ai_hybrid_scoring.phase41.dataset_hash_split_manifest_hash_feature_schema_version_label_policy_version.v1",
        "kb_ai_hybrid_scoring.phase41.feature_lineage_source_object_ref_lineage_ref_schema_version.v1",
        "kb_ai_hybrid_scoring.phase41.qwen3_numeric_scorer_final_gate.v1",
        "kb_ai_hybrid_scoring.phase41.final_gate_scorer_risk_bucket_threshold_policy_allow_block_reduce_size_deterministic_final_gate_qwen3_recommendation_raw_model_score.v1",
        "kb_ai_hybrid_scoring.phase41.feature_attribution_top_features_final_gate.v1",
        "kb_ai_hybrid_scoring.phase41.active_learning_hard_example_mining_gold_eval.v1",
        "kb_ai_hybrid_scoring.phase41.rag_first_prompt_sft_lora.v1",
        "kb_ai_hybrid_scoring.phase41.cek_ta_resolver.v1",
        "kb_ai_hybrid_scoring.phase41.hybrid_scoring_runtime_scorer_calibrator_rag_qwen3_final_gate_latency_budget_timeout_fallback_fail_to_review_fail_closed.v1",
        "kb_ai_hybrid_scoring.phase41.catboost.v1",
        "kb_ai_hybrid_scoring.phase41.ensemble_after_single_model_baseline_insufficient.v1",
        "kb_ai_hybrid_scoring.phase41.entity_group_split_split.v1",
        "kb_ai_hybrid_scoring.phase41.platt_isotonic.v1",
        "kb_ai_hybrid_scoring.phase41.regime_strategy_family_timeframe_regime_strategy_timeframe_slice_label_ai_engineering.v1",
        "kb_ai_hybrid_scoring.phase41.conformal_abstain_band_deterministic_final_gate.v1",
        "kb_ai_hybrid_scoring.phase41.feast_feature_store_poc_manifest.v1",
        "kb_ai_hybrid_scoring.phase41.thinking_mode_non_thinking_mode_chain_of_thought_strict_json_reason_code_citation_audit_summary.v1",
        "kb_ai_hybrid_scoring.phase41.dpo_preference_pair_pnl.v1",
        "kb_ai_hybrid_scoring.phase41.vllm_qwen_serving.v1",
        "kb_ai_hybrid_scoring.phase41.hybrid_scoring_audit_trace_scorer_calibrator_rag_qwen3_final_gate.v1",
        "kb_ai_hybrid_scoring.phase41.mlflow_registry_release_manifest_poc_registry.v1",
        "kb_ai_hybrid_scoring.phase41.ray_kubeflow_phase_41.v1",
    ]
    missing_ids = [knowledge_id for knowledge_id in expected_ids if knowledge_id not in formal_text]
    missing_nodes = [node_id for node_id in PHASE41_TREE_NODES if node_id not in tree_text]
    assert_condition(errors, not missing_ids, f"Vue formalKnowledgeItems fixture missing Phase 41 ids: {missing_ids}.")
    assert_condition(errors, not missing_nodes, f"Vue knowledgeTreeNodes fixture missing Phase 41 nodes: {missing_nodes}.")
    return {
        "formal_fixture": str(formal_fixture),
        "tree_fixture": str(tree_fixture),
        "expected_ids_checked": len(expected_ids),
        "missing_ids": missing_ids,
        "phase41_tree_nodes_checked": len(PHASE41_TREE_NODES),
        "missing_nodes": missing_nodes,
    }


def main() -> int:
    errors: list[str] = []
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    payload = load_json(index_path)
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain a list or {items: [...]}.")

    report = {
        "report_id": "phase41_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "scope": "CEK-TA-334 MCP/SearchLab/KnowledgeTree Phase 41 全量 41 条最终联动验证",
        "index_path": str(index_path),
        "file_index": validate_file_index(items, errors),
        "knowledge_tree": validate_knowledge_tree(errors),
        "searchlab_style": validate_searchlab_style(errors),
        "mcp": validate_mcp(items, index_path, errors),
        "vue_fixtures": validate_vue_fixtures(errors),
        "boundaries": [
            "Phase 41 formal reviewed knowledge must stay caveat_only until separate human approval.",
            "MCP default_guidance_only must block Phase 41 reviewed/caveat_only items.",
            "MCP permissions remain read-only; approval/write requests must be denied.",
            "SearchLab/KnowledgeTree read formal knowledge from knowledge_items.json and Vue fixtures, not candidate queue.",
        ],
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }

    report_path = resolve_repo_path("docs", "reports", "phase41_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
