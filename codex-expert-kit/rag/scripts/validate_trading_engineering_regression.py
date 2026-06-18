"""Validate Trading Engineering knowledge retrieval and governance regression.

Phase 46 regression gate.

The goal is not to add knowledge. It checks whether representative Trading
Engineering formal knowledge can be found through the MCP/SearchLab path,
returns citations, keeps reviewed/caveat_only boundaries, and is blocked from
default-guidance-only retrieval.
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
for module_path in (CORE_DIR, MCP_DIR):
    if str(module_path) not in sys.path:
        sys.path.insert(0, str(module_path))

from path_resolver import resolve_repo_path  # noqa: E402


TASK_ID = "CEK-TA-475"
REPORT_PATH = resolve_repo_path("docs", "reports", "phase46_trading_engineering_regression_report.json", start_file=__file__)
CASE_MATRIX_PATH = resolve_repo_path("docs", "reports", "phase46_searchlab_case_matrix.json", start_file=__file__)
VUE_CONSISTENCY_PATH = resolve_repo_path("docs", "reports", "phase46_vue_tree_candidate_consistency_report.json", start_file=__file__)
INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)

NODE_ALIASES = {
    "kt.trading_engineering.backtest": "kt.backtest",
    "kt.risk_management.layered_risk_controls": "kt.trading_ai_safety.risk_gate_precedence",
    "kt.trading_engineering.market_microstructure.crypto_perpetual": "kt.market_microstructure.crypto_perpetual",
    "kt.trading_engineering.risk_management.crypto_perpetual_risk": "kt.trading_ai_safety",
}

EXPECTED_CASES: list[dict[str, str]] = [
    {
        "case_id": "quant_r_multiple",
        "query": "R multiple 初始风险单位 交易结果 风险归一化 复盘",
        "expected_knowledge_id": "kb_01_quant_foundation.r_multiple_definition.v1",
    },
    {
        "case_id": "data_point_in_time_reference",
        "query": "point in time instrument definition reference data current metadata 回填 历史样本",
        "expected_knowledge_id": "kb_phase45_p2.point_in_time_instrument_definition_required.v1",
    },
    {
        "case_id": "backtest_overfit_bias",
        "query": "回测 data snooping overfitting parameter search final evaluation",
        "expected_knowledge_id": "kb_04_backtest.parameter_search_separate_from_final_eval.v1",
    },
    {
        "case_id": "replay_ohlc_same_bar",
        "query": "OHLC same bar TP SL ordering tick replay conservative optimistic",
        "expected_knowledge_id": "kb_05_replay_simulation.ohlc_same_bar_tp_sl_ordering_required.v1",
    },
    {
        "case_id": "execution_tca_is",
        "query": "implementation shortfall arrival price execution cost market impact opportunity cost",
        "expected_knowledge_id": "kb_phase45_execution_tca.implementation_shortfall_required.v1",
    },
    {
        "case_id": "order_semantics",
        "query": "order type semantics venue specific TIF post only reduce only rulebook adapter mapping",
        "expected_knowledge_id": "kb_phase45_order_semantics.order_type_semantics_required.v1",
    },
    {
        "case_id": "risk_layered_controls",
        "query": "layered pre trade controls credit limit max order size price collar throttle margin",
        "expected_knowledge_id": "kb_phase45_layered_risk.layered_pre_trade_controls_required.v1",
    },
    {
        "case_id": "stress_not_permission",
        "query": "stress test scenario risk not trade permission tail loss liquidity correlation breakdown",
        "expected_knowledge_id": "kb_phase45_stress_scenario.stress_test_not_trade_permission.v1",
    },
    {
        "case_id": "trade_analysis_reason_code",
        "query": "post trade analysis reason code taxonomy bad trade good loss bad win",
        "expected_knowledge_id": "kb_07_trade_analysis.reason_code_required.v1",
    },
    {
        "case_id": "crypto_mark_index_last",
        "query": "crypto perpetual mark price index price last price liquidation trigger funding basis",
        "expected_knowledge_id": "kb_phase45_p2.mark_price_index_price_last_price_boundary.v1",
    },
    {
        "case_id": "crypto_outage_loss_allocation",
        "query": "crypto exchange outage websocket disconnect heartbeat mark index abnormal loss allocation ADL",
        "expected_knowledge_id": "kb_phase45_p2.exchange_outage_and_clawback_risk.v1",
    },
    {
        "case_id": "live_audit_order_causality",
        "query": "order event causality trace client order id exchange order id execution report audit trail",
        "expected_knowledge_id": "kb_phase45_trade_audit.order_event_causality_trace_required.v1",
    },
    {
        "case_id": "resilience_degraded_readonly",
        "query": "degraded mode read only mode trading system failover recovery incident log operational resilience",
        "expected_knowledge_id": "kb_phase45_resilience_incident_log.degraded_mode_and_readonly_mode_required.v1",
    },
    {
        "case_id": "data_entitlement_boundary",
        "query": "market data entitlement display non display derived data redistribution training license boundary",
        "expected_knowledge_id": "kb_phase45_p2.market_data_entitlement_boundary.v1",
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


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def get_items() -> list[dict[str, Any]]:
    payload = load_json(INDEX_PATH)
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must contain a list or {items: [...]}.")
    return items


def trading_inventory(items: list[dict[str, Any]]) -> dict[str, Any]:
    trading_partitions = {
        "KB_01_QUANT_FOUNDATION",
        "KB_02_DATA_ENGINEERING",
        "KB_03_MARKET_MICROSTRUCTURE",
        "KB_04_BACKTEST",
        "KB_05_REPLAY_SIMULATION",
        "KB_06_LIVE_EXECUTION",
        "KB_07_RISK_MANAGEMENT",
        "KB_07_TRADE_ANALYSIS",
    }
    scoped = [item for item in items if item.get("metadata", {}).get("partition_id") in trading_partitions or item.get("metadata", {}).get("phase") in {"Phase 37", "Phase 45"}]
    return {
        "count": len(scoped),
        "review_counts": dict(Counter(item.get("review", {}).get("review_status", "") for item in scoped)),
        "gate_counts": dict(Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)),
        "partition_counts": dict(Counter(item.get("metadata", {}).get("partition_id", "") for item in scoped)),
        "phase_counts": dict(Counter(item.get("metadata", {}).get("phase", "") for item in scoped)),
    }


def validate_case(
    mcp_module: Any,
    item_by_id: dict[str, dict[str, Any]],
    case: dict[str, str],
    errors: list[str],
) -> dict[str, Any]:
    expected_id = case["expected_knowledge_id"]
    expected = item_by_id.get(expected_id)
    if expected is None:
        fail(errors, f"{case['case_id']}: expected item missing from knowledge index: {expected_id}")
        return {"case_id": case["case_id"], "status": "missing_expected", "expected_knowledge_id": expected_id}

    canonical_node_id = expected.get("metadata", {}).get("canonical_node_id")
    response = mcp_module.search_expert_knowledge(
        {
            "request_id": f"phase46-{case['case_id']}",
            "query": case["query"],
            "top_k": 8,
            "filters": {"canonical_node_id": canonical_node_id},
            "include": {"reviewed": True, "default_guidance_only": False},
        },
        knowledge_items_path=str(INDEX_PATH),
    )
    result_ids = [str(result.get("knowledge_id", "")) for result in response.get("results", [])]
    found = expected_id in result_ids
    if not found:
        fail(errors, f"{case['case_id']}: expected {expected_id} not found in MCP results: {result_ids}")

    first_expected = next((result for result in response.get("results", []) if result.get("knowledge_id") == expected_id), None)
    if first_expected is not None:
        if first_expected.get("source_count", 0) <= 0:
            fail(errors, f"{case['case_id']}: expected result has no source_count: {expected_id}")
        if first_expected.get("review_status") != "reviewed":
            fail(errors, f"{case['case_id']}: expected result is not reviewed: {expected_id}")
        if first_expected.get("machine_gate", {}).get("default_guidance") != "caveat_only":
            fail(errors, f"{case['case_id']}: expected result is not caveat_only: {expected_id}")

    block_response = mcp_module.search_expert_knowledge(
        {
            "request_id": f"phase46-{case['case_id']}-default-block",
            "query": case["query"],
            "top_k": 8,
            "filters": {"canonical_node_id": canonical_node_id},
            "include": {"reviewed": True, "default_guidance_only": True},
        },
        knowledge_items_path=str(INDEX_PATH),
    )
    default_result_ids = [str(result.get("knowledge_id", "")) for result in block_response.get("results", [])]
    blocked_ids = [str(result.get("knowledge_id", "")) for result in block_response.get("blocked_results", [])]
    if expected_id in default_result_ids:
        fail(errors, f"{case['case_id']}: caveat_only item leaked into default_guidance_only results: {expected_id}")
    if expected.get("machine_gate", {}).get("default_guidance") == "caveat_only" and expected_id not in blocked_ids:
        fail(errors, f"{case['case_id']}: caveat_only item was not listed in blocked_results: {expected_id}")

    return {
        "case_id": case["case_id"],
        "query": case["query"],
        "canonical_node_id": canonical_node_id,
        "partition_id": expected.get("metadata", {}).get("partition_id"),
        "phase": expected.get("metadata", {}).get("phase"),
        "expected_knowledge_id": expected_id,
        "mcp_status": response.get("status"),
        "found_expected": found,
        "top_result_ids": result_ids[:5],
        "default_guidance_blocked": expected_id not in default_result_ids and expected_id in blocked_ids,
        "blocked_count": block_response.get("audit", {}).get("blocked_count", 0),
    }


def validate_boundaries(items: list[dict[str, Any]], item_by_id: dict[str, dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    expected_items = [item_by_id[case["expected_knowledge_id"]] for case in EXPECTED_CASES if case["expected_knowledge_id"] in item_by_id]
    unsafe: list[str] = []
    source_missing: list[str] = []
    for item in expected_items:
        knowledge_id = str(item.get("knowledge_id"))
        if not item.get("source_evidence"):
            source_missing.append(knowledge_id)
        review = item.get("review", {})
        gate = item.get("machine_gate", {})
        if review.get("review_status") != "reviewed":
            unsafe.append(f"{knowledge_id}: review_status={review.get('review_status')}")
        if review.get("approved_allowed") is not False or review.get("default_guidance_allowed") is not False or review.get("hard_gate_allowed") is not False:
            unsafe.append(f"{knowledge_id}: review permissions unsafe")
        if gate.get("default_guidance") != "caveat_only":
            unsafe.append(f"{knowledge_id}: machine_gate.default_guidance={gate.get('default_guidance')}")
    if source_missing:
        fail(errors, f"expected regression items missing sources: {source_missing}")
    if unsafe:
        fail(errors, f"expected regression items have unsafe governance: {unsafe}")
    return {
        "expected_checked": len(expected_items),
        "source_missing_count": len(source_missing),
        "unsafe_count": len(unsafe),
        "source_missing": source_missing,
        "unsafe": unsafe,
    }


def validate_vue_fixture(item_by_id: dict[str, dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    formal_fixture = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
    tree_fixture = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    formal_text = formal_fixture.read_text(encoding="utf-8")
    tree_text = tree_fixture.read_text(encoding="utf-8")
    missing_formal = [case["expected_knowledge_id"] for case in EXPECTED_CASES if case["expected_knowledge_id"] not in formal_text]
    expected_nodes = sorted(
        {
            str(item_by_id[case["expected_knowledge_id"]].get("metadata", {}).get("canonical_node_id"))
            for case in EXPECTED_CASES
            if case["expected_knowledge_id"] in item_by_id
        }
    )
    missing_nodes = [
        node_id
        for node_id in expected_nodes
        if node_id and node_id not in tree_text and NODE_ALIASES.get(node_id, "") not in tree_text
    ]
    if missing_formal:
        fail(errors, f"Vue formal fixture missing expected ids: {missing_formal}")
    if missing_nodes:
        fail(errors, f"Vue tree fixture missing expected nodes: {missing_nodes}")
    return {
        "formal_fixture": str(formal_fixture),
        "tree_fixture": str(tree_fixture),
        "expected_formal_count": len(EXPECTED_CASES),
        "missing_formal": missing_formal,
        "expected_node_count": len(expected_nodes),
        "missing_nodes": missing_nodes,
    }


def build_case_matrix(search_cases: list[dict[str, Any]], item_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for result in search_cases:
        expected_id = result.get("expected_knowledge_id")
        item = item_by_id.get(str(expected_id), {})
        review = item.get("review", {})
        machine_gate = item.get("machine_gate", {})
        rows.append(
            {
                "case_id": result.get("case_id"),
                "query": result.get("query"),
                "expected_knowledge_id": expected_id,
                "canonical_node_id": result.get("canonical_node_id"),
                "partition_id": result.get("partition_id"),
                "phase": result.get("phase"),
                "review_status": review.get("review_status"),
                "machine_gate_default_guidance": machine_gate.get("default_guidance"),
                "source_count": len(item.get("source_evidence", []) or []),
                "found_expected": result.get("found_expected"),
                "default_guidance_blocked": result.get("default_guidance_blocked"),
                "top_result_ids": result.get("top_result_ids", []),
            }
        )
    return {
        "report_id": "phase46_searchlab_case_matrix",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": "CEK-TA-476",
        "case_count": len(rows),
        "coverage_note": "覆盖 Trading Engineering 代表性正式知识、Phase 37 核心分支和 Phase 45 扩展节点；用于 MCP/SearchLab 回归。",
        "hard_boundaries": [
            "case matrix 只验证 reviewed/caveat_only 的检索和阻断。",
            "不得把本矩阵结果解释为 approved/default guidance/hard gate。",
        ],
        "cases": rows,
        "status": "pass" if all(row["found_expected"] and row["default_guidance_blocked"] for row in rows) else "fail",
    }


def build_vue_consistency_report(vue_checks: dict[str, Any], search_cases: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "report_id": "phase46_vue_tree_candidate_consistency",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": "CEK-TA-477",
        "scope": "检查 Vue3 formal knowledge fixture 和知识树 fixture 是否包含 Phase 46 代表性 Trading Engineering 知识。",
        "formal_fixture": vue_checks.get("formal_fixture"),
        "tree_fixture": vue_checks.get("tree_fixture"),
        "expected_formal_count": vue_checks.get("expected_formal_count"),
        "expected_node_count": vue_checks.get("expected_node_count"),
        "missing_formal": vue_checks.get("missing_formal", []),
        "missing_nodes": vue_checks.get("missing_nodes", []),
        "case_ids": [case.get("case_id") for case in search_cases],
        "status": "pass" if not vue_checks.get("missing_formal") and not vue_checks.get("missing_nodes") else "fail",
    }


def main() -> int:
    errors: list[str] = []
    items = get_items()
    item_by_id = {str(item.get("knowledge_id")): item for item in items}
    mcp_module = load_module(
        "phase46_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    search_cases = [validate_case(mcp_module, item_by_id, case, errors) for case in EXPECTED_CASES]
    boundary_checks = validate_boundaries(items, item_by_id, errors)
    vue_fixture_checks = validate_vue_fixture(item_by_id, errors)
    case_matrix = build_case_matrix(search_cases, item_by_id)
    vue_consistency_report = build_vue_consistency_report(vue_fixture_checks, search_cases)
    if case_matrix["status"] != "pass":
        fail(errors, "SearchLab case matrix failed.")
    if vue_consistency_report["status"] != "pass":
        fail(errors, "Vue consistency report failed.")
    report = {
        "report_id": "phase46_trading_engineering_regression",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "scope": "Representative Trading Engineering MCP/SearchLab/KnowledgeTree regression for Phase 37 and Phase 45 formal knowledge.",
        "inventory": trading_inventory(items),
        "case_count": len(EXPECTED_CASES),
        "search_cases": search_cases,
        "boundary_checks": boundary_checks,
        "vue_fixture_checks": vue_fixture_checks,
        "case_matrix_report": str(CASE_MATRIX_PATH),
        "vue_consistency_report": str(VUE_CONSISTENCY_PATH),
        "hard_boundaries": [
            "reviewed/caveat_only 不能进入 default guidance。",
            "不得把 Trading Engineering 知识作为 approved 或 hard gate。",
            "不得输出买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。",
        ],
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    case_matrix["status"] = "pass" if not errors and case_matrix["status"] == "pass" else case_matrix["status"]
    vue_consistency_report["status"] = "pass" if not errors and vue_consistency_report["status"] == "pass" else vue_consistency_report["status"]
    write_json(CASE_MATRIX_PATH, case_matrix)
    write_json(VUE_CONSISTENCY_PATH, vue_consistency_report)
    write_json(REPORT_PATH, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
