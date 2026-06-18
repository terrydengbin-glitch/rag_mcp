from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from codex_expert_kit_mcp_import import import_search_tool


ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_ROOT = ROOT / "codex-expert-kit" / "rag" / "knowledge"


search_expert_knowledge = import_search_tool()


def load_seed_items() -> list[dict[str, Any]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json"))]


def test_canonical_node_id_filter_matches_canonical_metadata() -> None:
    response = search_expert_knowledge(
        {
            "request_id": "phase20_canonical_filter",
            "query": "same bar fill model assumption",
            "top_k": 5,
            "filters": {
                "canonical_node_id": "kt.trading_engineering.backtest.fill_assumption",
                "review_status": "approved",
            },
        },
        knowledge_items=load_seed_items(),
    )

    assert response["status"] in {"ok", "warning"}
    assert response["results"]
    assert all(item["canonical_node_id"] == "kt.trading_engineering.backtest.fill_assumption" for item in response["results"])
    assert response["results"][0]["canonical_tree_path"]
    assert response["results"][0]["why_matched"]["reasons"]


def test_canonical_node_id_filter_accepts_v1_alias_during_migration() -> None:
    response = search_expert_knowledge(
        {
            "request_id": "phase20_v1_alias_filter",
            "query": "unsourced RAG default guidance source quality",
            "top_k": 5,
            "filters": {
                "canonical_node_id": "kt.rag_engineering.source_quality",
                "review_status": "approved",
            },
        },
        knowledge_items=load_seed_items(),
    )

    ids = {item["knowledge_id"] for item in response["results"]}
    assert "kb_09_rag_engineering.source_quality.unsourced_default_block.v1" in ids


def test_canonical_tree_path_prefix_filters_results() -> None:
    response = search_expert_knowledge(
        {
            "request_id": "phase20_canonical_path_prefix",
            "query": "risk budget position sizing before signal",
            "top_k": 5,
            "filters": {
                "canonical_tree_path_prefix": "CEK-TA / Trading Engineering / Risk Management",
                "review_status": "approved",
            },
        },
        knowledge_items=load_seed_items(),
    )

    assert response["results"]
    assert all(
        item["canonical_tree_path"].startswith("CEK-TA / Trading Engineering / Risk Management")
        for item in response["results"]
    )


def test_blocked_results_include_reason_and_fix_for_searchlab() -> None:
    item = copy.deepcopy(load_seed_items()[0])
    item["knowledge_id"] = "kb_test.phase20.unsourced.v1"
    item["title"] = "Phase 20 unsourced blocking fixture"
    item["content"]["statement"] = "phase20 unsourced blocking fixture"
    item["source_evidence"] = []

    response = search_expert_knowledge(
        {
            "request_id": "phase20_blocked_results",
            "query": "phase20 unsourced blocking fixture",
            "top_k": 5,
            "filters": {"review_status": "approved"},
        },
        knowledge_items=[item],
    )

    assert response["results"] == []
    assert response["audit"]["blocked_count"] == 1
    assert response["blocked_results"][0]["blocked_reason"] == "missing_source_evidence"
    assert response["blocked_results"][0]["recommended_fix"] == "add_source_evidence_before_default_guidance"
