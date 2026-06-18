"""Validate current Phase 45 MCP/SearchLab/KnowledgeTree runtime linkage.

This is an incremental gate for Phase 45 while P1/P2 collection is still in
progress. It validates all currently materialized Phase 45 formal knowledge in
the official formal index, checks candidate back-links and Vue fixtures, and
proves MCP search can retrieve reviewed/caveat_only items while blocking them
from default-guidance-only retrieval.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
MCP_DIR = Path(__file__).resolve().parents[2] / "mcp"
for path in (CORE_DIR, MCP_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from path_resolver import resolve_repo_path  # noqa: E402


TASK_ID = "CEK-TA-472"
PHASE = "Phase 45"
REPORT_PATH = resolve_repo_path("docs", "reports", "phase45_runtime_linkage_report.json", start_file=__file__)
PHASE45_PREFIXES = (
    "kb_phase45_execution_tca.",
    "kb_phase45_trade_audit.",
    "kb_phase45_layered_risk.",
    "kb_phase45_resilience_incident_log.",
    "kb_phase45_stress_scenario.",
)


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


def is_phase45_item(item: dict[str, Any]) -> bool:
    knowledge_id = str(item.get("knowledge_id", ""))
    return item.get("metadata", {}).get("phase") == PHASE or knowledge_id.startswith(PHASE45_PREFIXES)


def validate_file_index(items: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    scoped = [item for item in items if is_phase45_item(item)]
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    node_counts = Counter(item.get("metadata", {}).get("canonical_node_id", "") for item in scoped)
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

    assert_condition(errors, bool(scoped), "Phase 45 formal reviewed items not found in knowledge_items.json.")
    assert_condition(errors, set(review_counts) <= {"reviewed"}, f"Phase 45 review statuses contain unexpected states: {dict(review_counts)}.")
    assert_condition(errors, set(gate_counts) <= {"caveat_only"}, f"Phase 45 machine gates contain unexpected states: {dict(gate_counts)}.")
    assert_condition(errors, not source_missing, f"Phase 45 items missing source_evidence: {source_missing}.")
    assert_condition(errors, not unsafe_conflicts, f"Phase 45 items have unsafe conflicts: {unsafe_conflicts}.")
    assert_condition(errors, not default_enabled, f"Phase 45 items unexpectedly allow default guidance: {default_enabled}.")
    assert_condition(errors, not approved_enabled, f"Phase 45 items unexpectedly allow approved: {approved_enabled}.")
    assert_condition(errors, not hard_gate_enabled, f"Phase 45 items unexpectedly allow hard gate: {hard_gate_enabled}.")

    return {
        "phase45_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "node_counts": dict(node_counts),
        "source_missing_count": len(source_missing),
        "unsafe_conflict_count": len(unsafe_conflicts),
        "default_guidance_enabled_count": len(default_enabled),
        "approved_enabled_count": len(approved_enabled),
        "hard_gate_enabled_count": len(hard_gate_enabled),
    }


def validate_mcp(items: list[dict[str, Any]], index_path: Path, errors: list[str]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase45_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    search_cases = [
        {
            "case_id": "phase45_stress_scenario",
            "query": "scenario stress testing owner data version stress result not trade permission",
            "canonical_node_id": "kt.risk_management.stress_scenario",
            "expected_prefix": "kb_phase45_stress_scenario.",
        },
        {
            "case_id": "phase45_layered_risk",
            "query": "pre trade controls credit margin available funds buying power boundary",
            "canonical_node_id": "kt.risk_management.layered_risk_controls",
            "expected_prefix": "kb_phase45_layered_risk.",
        },
    ]
    results_by_case: dict[str, Any] = {}
    for case in search_cases:
        response = mcp_module.search_expert_knowledge(
            {
                "request_id": case["case_id"],
                "query": case["query"],
                "top_k": 8,
                "filters": {"canonical_node_id": case["canonical_node_id"]},
                "include": {"reviewed": True, "default_guidance_only": False},
            },
            knowledge_items_path=str(index_path),
        )
        matching = [
            result
            for result in response.get("results", [])
            if str(result.get("knowledge_id", "")).startswith(case["expected_prefix"])
        ]
        results_by_case[case["case_id"]] = {
            "status": response.get("status"),
            "matching_count": len(matching),
            "top_knowledge_ids": [item.get("knowledge_id") for item in matching[:5]],
        }
        assert_condition(errors, response.get("status") in {"ok", "warning"}, f"MCP search status failed for {case['case_id']}: {response.get('status')}.")
        assert_condition(errors, bool(matching), f"MCP search did not return expected Phase 45 items for {case['case_id']}.")
        if matching:
            first = matching[0]
            assert_condition(errors, first.get("source_count", 0) > 0, f"MCP {case['case_id']} first result has no sources.")
            assert_condition(errors, first.get("review_status") == "reviewed", f"MCP {case['case_id']} first result is not reviewed.")
            assert_condition(errors, first.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP {case['case_id']} first result is not caveat_only.")

    block_response = mcp_module.search_expert_knowledge(
        {
            "request_id": "phase45-default-guidance-block",
            "query": "scenario stress testing risk review",
            "top_k": 10,
            "filters": {"canonical_node_id": "kt.risk_management.stress_scenario"},
            "include": {"reviewed": True, "default_guidance_only": True},
        },
        knowledge_items=items,
    )
    phase45_blocked = [
        item
        for item in block_response.get("blocked_results", [])
        if str(item.get("knowledge_id", "")).startswith("kb_phase45_stress_scenario.")
    ]
    assert_condition(errors, not [r for r in block_response.get("results", []) if str(r.get("knowledge_id", "")).startswith("kb_phase45_stress_scenario.")], "MCP default_guidance_only unexpectedly returned Phase 45 caveat_only results.")
    assert_condition(errors, bool(phase45_blocked), "MCP default_guidance_only did not block Phase 45 caveat_only results.")
    return {
        "search_cases": results_by_case,
        "default_guidance_blocked_count": block_response.get("audit", {}).get("blocked_count", 0),
        "phase45_blocked_count": len(phase45_blocked),
    }


def validate_vue_fixtures(errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    candidate_fixture = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    candidate_text = candidate_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    expected_formal = [
        "kb_phase45_stress_scenario.scenario_stress_test_required.v1",
        "kb_phase45_stress_scenario.correlation_breakdown_caveat.v1",
        "kb_phase45_stress_scenario.gap_and_overnight_risk_required.v1",
        "kb_phase45_stress_scenario.tail_loss_review_required.v1",
        "kb_phase45_stress_scenario.stress_test_not_trade_permission.v1",
    ]
    missing_formal = [item for item in expected_formal if item not in formal_text]
    missing_candidate_links = [item for item in expected_formal if item not in candidate_text]
    assert_condition(errors, not missing_formal, f"Vue formalKnowledgeItems fixture missing Phase 45 stress ids: {missing_formal}.")
    assert_condition(errors, not missing_candidate_links, f"Vue candidate fixture missing Phase 45 formal links: {missing_candidate_links}.")
    assert_condition(errors, "kt.risk_management.stress_scenario" in tree_text, "Vue knowledge tree fixture missing stress scenario node.")
    return {
        "formal_fixture": str(formal_fixture),
        "candidate_fixture": str(candidate_fixture),
        "tree_fixture": str(tree_fixture),
        "expected_formal_checked": len(expected_formal),
        "missing_formal": missing_formal,
        "missing_candidate_links": missing_candidate_links,
        "stress_node_present": "kt.risk_management.stress_scenario" in tree_text,
    }


def main() -> int:
    errors: list[str] = []
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    payload = load_json(index_path)
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain a list or {items: [...]}.")

    report = {
        "report_id": "phase45_runtime_linkage_validation",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "scope": "Phase 45 incremental runtime validation for currently materialized formal reviewed/caveat_only knowledge.",
        "index_path": str(index_path),
        "file_index": validate_file_index(items, errors),
        "mcp": validate_mcp(items, index_path, errors),
        "vue_fixtures": validate_vue_fixtures(errors),
        "boundaries": [
            "Phase 45 reviewed knowledge remains caveat_only until separate human approval.",
            "MCP default_guidance_only must block Phase 45 reviewed/caveat_only items.",
            "No approved/default guidance/hard gate/risk threshold advice is enabled.",
        ],
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
