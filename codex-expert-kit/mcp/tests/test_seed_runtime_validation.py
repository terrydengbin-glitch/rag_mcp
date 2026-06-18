from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from codex_expert_kit_mcp_import import import_search_tool


ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_ROOT = ROOT / "codex-expert-kit" / "rag" / "knowledge"


search_expert_knowledge = import_search_tool()


def load_seed_items() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        items.append(json.loads(path.read_text(encoding="utf-8")))
    return items


SEED_CASES = [
    ("seed_runtime_001", "multiple testing overfitting backtest bias", "backtest_review", "kb_04_backtest.bias.multiple_testing_overfit.v1"),
    ("seed_runtime_002", "OHLC same bar take profit stop loss fill model", "backtest_review", "kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1"),
    ("seed_runtime_003", "Kline indicator signal timeframe market boundary", "strategy_design", "kb_02_kline_strategy.signal_boundary.timeframe_market_scope.v1"),
    ("seed_runtime_004", "live trading kill switch no new orders", "live_trading", "kb_06_live_execution.risk_control.kill_switch_no_new_orders.v1"),
    ("seed_runtime_005", "position sizing risk budget before signal", "strategy_design", "kb_01_quant_foundation.risk_return.position_risk_budget_before_signal.v1"),
    ("seed_runtime_006", "backtest fill model slippage fee assumptions", "backtest_review", "kb_04_backtest.fill_model.explicit_slippage_fee_assumptions.v1"),
    ("seed_runtime_007", "simulation execution semantics backtest not live truth", "simulation", "kb_05_replay_simulation.execution_semantics.backtest_not_live_truth.v1"),
    ("seed_runtime_009", "unsourced RAG knowledge default guidance block", "rag_engineering", "kb_09_rag_engineering.source_quality.unsourced_default_block.v1"),
    ("seed_runtime_010", "LLM RAG output source boundary human escalation trading", "llm_training", "kb_08_llm_training.eval_and_risk.source_boundary_human_escalation.v1"),
]


def test_all_seed_items_are_runtime_queryable() -> None:
    items = load_seed_items()
    item_ids = {item["knowledge_id"] for item in items}
    expected_seed_ids = {case[3] for case in SEED_CASES}
    assert expected_seed_ids.issubset(item_ids)

    for request_id, query, task_type, expected_id in SEED_CASES:
        response = search_expert_knowledge(
            {
                "request_id": request_id,
                "query": query,
                "task_type": task_type,
                "top_k": 10,
                "filters": {"review_status": "approved"},
                "include": {"sources": True, "conflicts": True, "deprecated": False, "draft": False, "reviewed": True},
            },
            knowledge_items=items,
        )

        assert response["status"] in {"ok", "warning"}, response
        result_by_id = {item["knowledge_id"]: item for item in response["results"]}
        assert expected_id in result_by_id, (request_id, response["results"])
        matched = result_by_id[expected_id]
        assert matched["review_status"] == "approved"
        assert matched["conflict_status"] in {"none", "resolved"}
        assert matched["source_refs"]
        assert matched["applicable_scope"]["applies_when"]
        assert matched["not_applicable_scope"]
        assert matched["recommended_next_action"] != "no_default_guidance"


def test_live_trading_time_sensitive_seed_returns_warning() -> None:
    response = search_expert_knowledge(
        {
            "request_id": "seed_runtime_live_warning",
            "query": "live trading kill switch no new orders",
            "task_type": "live_trading",
            "top_k": 3,
        },
        knowledge_items=load_seed_items(),
    )

    assert response["status"] == "warning"
    assert any("time_sensitive" in warning for warning in response["warnings"])
