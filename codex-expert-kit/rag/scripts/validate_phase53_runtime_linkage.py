"""Validate Phase 53 MCP/SearchLab/KnowledgeTree/Vue3 runtime linkage."""

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


TASK_ID = "CEK-TA-525"
PHASE = "Phase 53"
EXPECTED_IDS = {
    "kb_ai_security_governance.phase53.trading_ai_agent_threat_model_required.v1": "kt.ai_engineering.security_governance.agent_threat_model",
    "kb_ai_supply_chain_governance.phase53.ai_sbom_model_sbom_required.v1": "kt.ai_engineering.supply_chain_governance.ai_sbom",
    "kb_trading_market_conduct.phase53.market_conduct_surveillance_taxonomy_required.v1": "kt.trading_engineering.market_conduct.surveillance_taxonomy",
    "kb_trading_market_access.phase53.market_access_dea_regulatory_boundary_required.v1": "kt.trading_engineering.market_access.regulatory_boundary",
    "kb_trading_audit_trace.phase53.trade_audit_time_synchronization_required.v1": "kt.trading_engineering.audit_trace.time_synchronization",
}
EXPECTED_TASKS = {"P53-AI-SEC01", "P53-AI-SBOM01", "P53-TR-MC01", "P53-TR-MA01", "P53-TR-TS01"}


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


def phase53_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if item.get("knowledge_id") in EXPECTED_IDS]


def validate_index(errors: list[str]) -> dict[str, Any]:
    payload = load_json(resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__))
    items = payload.get("items", [])
    scoped = phase53_items(items)
    found_ids = {item.get("knowledge_id") for item in scoped}
    review_counts = Counter(item.get("review", {}).get("review_status") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance") for item in scoped)
    approved_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("approved_allowed") is not False
        or item.get("review", {}).get("review_status") == "approved"
    ]
    default_enabled = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("default_guidance_allowed") is not False
        or item.get("machine_gate", {}).get("visible_in_default_guidance_queue") is not False
    ]
    hard_gate_enabled = [
        item.get("knowledge_id") for item in scoped if item.get("review", {}).get("hard_gate_allowed") is not False
    ]
    missing_sources = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    bad_nodes = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("metadata", {}).get("canonical_node_id") != EXPECTED_IDS.get(str(item.get("knowledge_id")))
    ]
    assert_condition(errors, found_ids == set(EXPECTED_IDS), f"Phase 53 index ids mismatch: missing={sorted(set(EXPECTED_IDS)-found_ids)} extra={sorted(found_ids-set(EXPECTED_IDS))}")
    assert_condition(errors, dict(review_counts) == {"reviewed": 5}, f"Phase 53 review statuses mismatch: {dict(review_counts)}")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": 5}, f"Phase 53 machine gates mismatch: {dict(gate_counts)}")
    assert_condition(errors, not approved_enabled, f"Phase 53 unexpectedly approved-enabled: {approved_enabled}")
    assert_condition(errors, not default_enabled, f"Phase 53 unexpectedly default-guidance-enabled: {default_enabled}")
    assert_condition(errors, not hard_gate_enabled, f"Phase 53 unexpectedly hard-gate-enabled: {hard_gate_enabled}")
    assert_condition(errors, not missing_sources, f"Phase 53 missing sources: {missing_sources}")
    assert_condition(errors, not bad_nodes, f"Phase 53 canonical nodes mismatch: {bad_nodes}")
    return {
        "index_total": len(items),
        "phase53_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "missing_sources": missing_sources,
        "bad_nodes": bad_nodes,
    }


def validate_mcp(errors: list[str]) -> dict[str, Any]:
    search_module = load_module(
        "phase53_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    get_module = load_module(
        "phase53_get_knowledge_item",
        resolve_repo_path("codex-expert-kit", "mcp", "get_knowledge_item.py", start_file=__file__),
    )
    knowledge_items_path = str(
        resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    )
    cases = []
    for knowledge_id, node_id in EXPECTED_IDS.items():
        item_response = get_module.get_knowledge_item({"knowledge_id": knowledge_id}, knowledge_items_path=knowledge_items_path)
        item = item_response.get("item") or {}
        assert_condition(errors, item_response.get("status") == "ok", f"MCP get failed for {knowledge_id}: {item_response.get('errors')}")
        assert_condition(errors, item.get("review", {}).get("review_status") == "reviewed", f"MCP get review_status mismatch for {knowledge_id}")
        assert_condition(errors, item.get("machine_gate", {}).get("default_guidance") == "caveat_only", f"MCP get gate mismatch for {knowledge_id}")

        search_response = search_module.search_expert_knowledge(
            {
                "query": knowledge_id.replace("_", " "),
                "task_type": "mcp",
                "filters": {"canonical_node_id": [node_id], "review_status": ["reviewed"]},
                "include": {"sources": True, "conflicts": True, "reviewed": True, "draft": False},
                "top_k": 5,
            },
            knowledge_items_path=knowledge_items_path,
        )
        ids = [result.get("knowledge_id") for result in search_response.get("results", [])]
        assert_condition(errors, knowledge_id in ids, f"MCP search did not return {knowledge_id}; got {ids}")

        default_response = search_module.search_expert_knowledge(
            {
                "query": knowledge_id.replace("_", " "),
                "task_type": "mcp",
                "filters": {"canonical_node_id": [node_id], "review_status": ["approved"]},
                "include": {"sources": True, "conflicts": True, "reviewed": False, "draft": False},
                "top_k": 5,
            },
            knowledge_items_path=knowledge_items_path,
        )
        assert_condition(
            errors,
            knowledge_id not in [result.get("knowledge_id") for result in default_response.get("results", [])],
            f"default/approved search unexpectedly returned {knowledge_id}",
        )
        cases.append(
            {
                "knowledge_id": knowledge_id,
                "canonical_node_id": node_id,
                "mcp_get_status": item_response.get("status"),
                "mcp_search_returned": knowledge_id in ids,
                "approved_filter_blocked": knowledge_id
                not in [result.get("knowledge_id") for result in default_response.get("results", [])],
            }
        )
    return {"case_count": len(cases), "cases": cases}


def validate_ui_and_tree(errors: list[str]) -> dict[str, Any]:
    formal = load_json(resolve_repo_path("ui", "public", "data", "formalKnowledgeItems.json", start_file=__file__))
    candidates = load_json(resolve_repo_path("ui", "public", "data", "phase23Candidates.json", start_file=__file__))
    tree = load_json(resolve_repo_path("ui", "public", "data", "knowledgeTreeNodes.json", start_file=__file__))
    formal_items = formal.get("items", [])
    candidate_items = candidates.get("items", [])
    tree_nodes = tree.get("nodes") or tree.get("items") or []

    formal_found = {item.get("knowledge_id") for item in formal_items if item.get("knowledge_id") in EXPECTED_IDS}
    candidate_rows = [item for item in candidate_items if item.get("research_task_id") in EXPECTED_TASKS]
    formalized_tasks = {
        item.get("research_task_id")
        for item in candidate_rows
        if item.get("review_status") == "formalized_reviewed"
        and item.get("workflow", {}).get("queue_group") == "formalized"
        and item.get("workflow", {}).get("formal_review_status") == "reviewed"
    }
    tree_node_ids = {node.get("node_id") for node in tree_nodes}
    missing_tree_nodes = sorted(set(EXPECTED_IDS.values()) - tree_node_ids)

    assert_condition(errors, formal_found == set(EXPECTED_IDS), f"UI formal fixture missing Phase 53 ids: {sorted(set(EXPECTED_IDS)-formal_found)}")
    assert_condition(errors, formalized_tasks == EXPECTED_TASKS, f"UI candidate fixture formalized task mismatch: {sorted(EXPECTED_TASKS-formalized_tasks)}")
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree fixture missing nodes: {missing_tree_nodes}")
    return {
        "ui_formal_total": formal.get("count"),
        "ui_phase53_formal_count": len(formal_found),
        "ui_candidate_phase53_count": len(candidate_rows),
        "ui_candidate_formalized_count": len(formalized_tasks),
        "knowledge_tree_node_total": len(tree_nodes),
        "missing_tree_nodes": missing_tree_nodes,
    }


def main() -> int:
    errors: list[str] = []
    report = {
        "report_id": "phase53_runtime_linkage_validation_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "phase": PHASE,
        "scope": sorted(EXPECTED_IDS),
        "index_validation": validate_index(errors),
        "mcp_validation": validate_mcp(errors),
        "ui_and_tree_validation": validate_ui_and_tree(errors),
        "errors": errors,
        "gate_status": "pass" if not errors else "fail",
        "boundary": "Phase 53 items are reviewed/caveat_only only; approved/default guidance/hard gate remain blocked.",
    }
    path = resolve_repo_path("docs", "reports", "phase53_runtime_linkage_validation_report.json", start_file=__file__)
    write_json(path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
