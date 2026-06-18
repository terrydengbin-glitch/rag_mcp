"""Validate Phase 60 MCP/SearchLab/KnowledgeTree/Vue3 runtime linkage."""

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


TASK_ID = "CEK-TA-589"
PHASE = "Phase 60"
REPORT_JSON = resolve_repo_path("docs", "reports", "phase60_runtime_linkage_validation_report.json", start_file=__file__)
REPORT_MD = resolve_repo_path("docs", "reports", "phase60_sandbox_replay_paper_environment_report.md", start_file=__file__)

EXPECTED_IDS: dict[str, str] = {
    "kb_phase60_replay_simulation.environment_taxonomy_required.v1": "kt.replay_simulation",
    "kb_phase60_live_execution.static_api_sandbox_contract_only.v1": "kt.live_execution",
    "kb_phase60_live_execution.testnet_endpoint_isolation_required.v1": "kt.live_execution",
    "kb_phase60_replay_simulation.paper_trading_not_live_required.v1": "kt.replay_simulation",
    "kb_phase60_replay_simulation.replay_market_impact_assumption_required.v1": "kt.replay_simulation",
    "kb_phase60_replay_simulation.environment_manifest_required.v1": "kt.replay_simulation",
    "kb_phase60_risk_management.environment_promotion_evidence_required.v1": "kt.risk_management",
    "kb_phase60_replay_simulation.sandbox_paper_live_gap_report_required.v1": "kt.replay_simulation",
    "kb_phase60_live_execution.order_lifecycle_mapping_required.v1": "kt.live_execution",
    "kb_phase60_risk_management.sandbox_risk_rehearsal_not_hard_gate.v1": "kt.risk_management",
    "kb_phase60_live_execution.adapter_certification.fix_broker_certification_required.v1": "kt.live_execution",
    "kb_phase60_replay_simulation.scenario_library.versioned_required.v1": "kt.replay_simulation",
    "kb_phase60_live_execution.paper_account_state.reset_trace_required.v1": "kt.live_execution",
    "kb_phase60_live_execution.environment_health.monitor_required.v1": "kt.live_execution",
    "kb_phase60_risk_management.live_canary.rollback_owner_required.v1": "kt.risk_management",
    "kb_phase60_replay_simulation.environment_drift.monitor_required.v1": "kt.replay_simulation",
}

EXPECTED_TASKS = {
    "P60-A01",
    "P60-A02",
    "P60-A03",
    "P60-A04",
    "P60-A05",
    "P60-A06",
    "P60-A07",
    "P60-A08",
    "P60-A09",
    "P60-A10",
    "P60-P1-01",
    "P60-P1-02",
    "P60-P1-03",
    "P60-P1-04",
    "P60-P1-05",
    "P60-P1-06",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def phase60_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if item.get("knowledge_id") in EXPECTED_IDS]


def validate_index(errors: list[str]) -> dict[str, Any]:
    payload = load_json(resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__))
    items = payload.get("items", payload if isinstance(payload, list) else [])
    scoped = phase60_items(items)
    found_ids = {item.get("knowledge_id") for item in scoped}
    review_counts = Counter(item.get("review", {}).get("review_status") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance") for item in scoped)
    canonical_counts = Counter(item.get("metadata", {}).get("canonical_node_id") for item in scoped)
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
    live_permission_enabled = [
        item.get("knowledge_id") for item in scoped if item.get("machine_gate", {}).get("live_permission_allowed") is not False
    ]
    missing_sources = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    bad_nodes = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("metadata", {}).get("canonical_node_id") != EXPECTED_IDS.get(str(item.get("knowledge_id")))
    ]
    unsafe_conflicts = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}
    ]

    assert_condition(errors, found_ids == set(EXPECTED_IDS), f"Phase 60 index ids mismatch: missing={sorted(set(EXPECTED_IDS)-found_ids)} extra={sorted(found_ids-set(EXPECTED_IDS))}")
    assert_condition(errors, dict(review_counts) == {"reviewed": len(EXPECTED_IDS)}, f"Phase 60 review statuses mismatch: {dict(review_counts)}")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": len(EXPECTED_IDS)}, f"Phase 60 machine gates mismatch: {dict(gate_counts)}")
    assert_condition(errors, not approved_enabled, f"Phase 60 unexpectedly approved-enabled: {approved_enabled}")
    assert_condition(errors, not default_enabled, f"Phase 60 unexpectedly default-guidance-enabled: {default_enabled}")
    assert_condition(errors, not hard_gate_enabled, f"Phase 60 unexpectedly hard-gate-enabled: {hard_gate_enabled}")
    assert_condition(errors, not live_permission_enabled, f"Phase 60 unexpectedly live-permission-enabled: {live_permission_enabled}")
    assert_condition(errors, not missing_sources, f"Phase 60 missing sources: {missing_sources}")
    assert_condition(errors, not bad_nodes, f"Phase 60 canonical nodes mismatch: {bad_nodes}")
    assert_condition(errors, not unsafe_conflicts, f"Phase 60 unsafe conflicts: {unsafe_conflicts}")

    return {
        "index_total": len(items),
        "phase60_count": len(scoped),
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "canonical_node_counts": dict(canonical_counts),
        "missing_sources": missing_sources,
        "bad_nodes": bad_nodes,
        "unsafe_conflicts": unsafe_conflicts,
        "approved_enabled": approved_enabled,
        "default_guidance_enabled": default_enabled,
        "hard_gate_enabled": hard_gate_enabled,
        "live_permission_enabled": live_permission_enabled,
    }


def validate_mcp(errors: list[str]) -> dict[str, Any]:
    search_module = load_module(
        "phase60_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    get_module = load_module(
        "phase60_get_knowledge_item",
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
        assert_condition(errors, bool(item.get("source_evidence")), f"MCP get missing sources for {knowledge_id}")

        search_response = search_module.search_expert_knowledge(
            {
                "query": knowledge_id.replace("_", " ").replace(".", " "),
                "task_type": "mcp",
                "filters": {"canonical_node_id": [node_id], "review_status": ["reviewed"]},
                "include": {"sources": True, "conflicts": True, "reviewed": True, "draft": False},
                "top_k": 8,
            },
            knowledge_items_path=knowledge_items_path,
        )
        ids = [result.get("knowledge_id") for result in search_response.get("results", [])]
        assert_condition(errors, knowledge_id in ids, f"MCP search did not return {knowledge_id}; got {ids}")

        approved_response = search_module.search_expert_knowledge(
            {
                "query": knowledge_id.replace("_", " ").replace(".", " "),
                "task_type": "mcp",
                "filters": {"canonical_node_id": [node_id], "review_status": ["approved"]},
                "include": {"sources": True, "conflicts": True, "reviewed": False, "draft": False},
                "top_k": 8,
            },
            knowledge_items_path=knowledge_items_path,
        )
        approved_ids = [result.get("knowledge_id") for result in approved_response.get("results", [])]
        assert_condition(errors, knowledge_id not in approved_ids, f"approved/default-style search unexpectedly returned {knowledge_id}")

        cases.append(
            {
                "knowledge_id": knowledge_id,
                "canonical_node_id": node_id,
                "mcp_get_status": item_response.get("status"),
                "mcp_search_returned": knowledge_id in ids,
                "approved_filter_blocked": knowledge_id not in approved_ids,
            }
        )
    return {"case_count": len(cases), "cases": cases}


def validate_searchlab_fixture(errors: list[str]) -> dict[str, Any]:
    """SearchLab uses the same formal index fixture path in this repository."""

    formal = load_json(resolve_repo_path("ui", "public", "data", "formalKnowledgeItems.json", start_file=__file__))
    items = formal.get("items", [])
    found = {item.get("knowledge_id") for item in items if item.get("knowledge_id") in EXPECTED_IDS}
    source_missing = [
        item.get("knowledge_id")
        for item in items
        if item.get("knowledge_id") in EXPECTED_IDS and not (item.get("source_evidence") or item.get("sources"))
    ]
    assert_condition(errors, found == set(EXPECTED_IDS), f"SearchLab/formal fixture missing Phase 60 ids: {sorted(set(EXPECTED_IDS)-found)}")
    assert_condition(errors, not source_missing, f"SearchLab/formal fixture Phase 60 source missing: {source_missing}")
    return {
        "fixture": "ui/public/data/formalKnowledgeItems.json",
        "phase60_count": len(found),
        "source_missing": source_missing,
    }


def validate_ui_and_tree(errors: list[str]) -> dict[str, Any]:
    formal = load_json(resolve_repo_path("ui", "public", "data", "formalKnowledgeItems.json", start_file=__file__))
    candidates = load_json(resolve_repo_path("ui", "public", "data", "phase23Candidates.json", start_file=__file__))
    tree = load_json(resolve_repo_path("ui", "public", "data", "knowledgeTreeNodes.json", start_file=__file__))
    scope_index = load_json(resolve_repo_path("ui", "public", "data", "knowledgeTreeScopeIndex.json", start_file=__file__))

    formal_items = formal.get("items", [])
    candidate_items = candidates.get("items", [])
    tree_nodes = tree.get("nodes") or tree.get("items") or []
    raw_scope_nodes = scope_index.get("nodes") or scope_index.get("items") or []
    if isinstance(raw_scope_nodes, dict):
        scope_nodes = list(raw_scope_nodes.values())
    else:
        scope_nodes = raw_scope_nodes

    formal_found = {item.get("knowledge_id") for item in formal_items if item.get("knowledge_id") in EXPECTED_IDS}
    candidate_rows = [item for item in candidate_items if item.get("research_task_id") in EXPECTED_TASKS]
    formalized_tasks = {
        item.get("research_task_id")
        for item in candidate_rows
        if item.get("review_status") == "formalized"
        and item.get("workflow", {}).get("queue_group") == "formalized"
        and item.get("workflow", {}).get("formal_review_status") == "reviewed"
    }
    tree_node_ids = {node.get("node_id") for node in tree_nodes}
    scope_node_ids = {node.get("node_id") for node in scope_nodes if isinstance(node, dict)}
    expected_nodes = set(EXPECTED_IDS.values())
    missing_tree_nodes = sorted(expected_nodes - tree_node_ids)
    missing_scope_nodes = sorted(expected_nodes - scope_node_ids)

    assert_condition(errors, formal_found == set(EXPECTED_IDS), f"UI formal fixture missing Phase 60 ids: {sorted(set(EXPECTED_IDS)-formal_found)}")
    assert_condition(errors, formalized_tasks == EXPECTED_TASKS, f"UI candidate fixture formalized task mismatch: {sorted(EXPECTED_TASKS-formalized_tasks)}")
    assert_condition(errors, not missing_tree_nodes, f"Knowledge tree fixture missing nodes: {missing_tree_nodes}")
    assert_condition(errors, not missing_scope_nodes, f"Knowledge tree scope index missing nodes: {missing_scope_nodes}")
    return {
        "ui_formal_total": formal.get("count"),
        "ui_phase60_formal_count": len(formal_found),
        "ui_candidate_phase60_count": len(candidate_rows),
        "ui_candidate_formalized_count": len(formalized_tasks),
        "knowledge_tree_node_total": len(tree_nodes),
        "scope_node_total": len(scope_nodes),
        "missing_tree_nodes": missing_tree_nodes,
        "missing_scope_nodes": missing_scope_nodes,
    }


def write_markdown_report(report: dict[str, Any]) -> None:
    lines = [
        "# Phase 60 Sandbox / Replay / Paper Trading 环境治理验收报告",
        "",
        f"- 生成时间：`{report['generated_at']}`",
        f"- 任务：`{TASK_ID}`",
        f"- 结论：`{report['gate_status']}`",
        "",
        "## 验收范围",
        "",
        "本次验收覆盖 Phase 60 已沉淀的 10 条 `formal reviewed/caveat_only` 知识，验证正式索引、MCP/SearchLab、KnowledgeTree、Vue3 fixture 和候选回链。",
        "",
        "## 边界",
        "",
        "- 全部知识仅为 `reviewed/caveat_only`。",
        "- 未进入 `approved`。",
        "- 未进入默认指导队列。",
        "- 未启用 hard gate、live permission、交易建议或风险阈值建议。",
        "",
        "## 正式知识",
        "",
    ]
    for knowledge_id in sorted(EXPECTED_IDS):
        lines.append(f"- `{knowledge_id}` -> `{EXPECTED_IDS[knowledge_id]}`")
    lines.extend(
        [
            "",
            "## 验证摘要",
            "",
            f"- 正式索引 Phase 60 数量：`{report['index_validation']['phase60_count']}`",
            f"- MCP 验证用例：`{report['mcp_validation']['case_count']}`",
            f"- SearchLab/formal fixture 数量：`{report['searchlab_validation']['phase60_count']}`",
            f"- Vue 候选 formalized 数量：`{report['ui_and_tree_validation']['ui_candidate_formalized_count']}`",
            f"- 知识树缺失节点：`{report['ui_and_tree_validation']['missing_tree_nodes']}`",
            "",
            "## 错误",
            "",
        ]
    )
    if report["errors"]:
        for error in report["errors"]:
            lines.append(f"- {error}")
    else:
        lines.append("- 无")
    lines.append("")
    write_text(REPORT_MD, "\n".join(lines))


def main() -> int:
    errors: list[str] = []
    report = {
        "report_id": "phase60_runtime_linkage_validation_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "phase": PHASE,
        "scope": sorted(EXPECTED_IDS),
        "index_validation": validate_index(errors),
        "mcp_validation": validate_mcp(errors),
        "searchlab_validation": validate_searchlab_fixture(errors),
        "ui_and_tree_validation": validate_ui_and_tree(errors),
        "errors": errors,
        "gate_status": "pass" if not errors else "fail",
        "boundary": "Phase 60 items are reviewed/caveat_only only; approved/default guidance/hard gate/live permission remain blocked.",
    }
    write_json(REPORT_JSON, report)
    write_markdown_report(report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
