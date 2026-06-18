from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from codex_expert_kit_mcp_import import import_search_tool


ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "docs" / "contracts" / "external_ai_active_retrieval_protocol.md"
ACTIVE_TEMPLATE = ROOT / "codex-expert-kit" / "templates" / "external_project_active_retrieval_AGENTS.md"
EXTERNAL_TEMPLATE = ROOT / "codex-expert-kit" / "templates" / "external_project_AGENTS.md"
TEST_PLAN = ROOT / "codex-expert-kit" / "templates" / "external_project_active_retrieval_test_plan.md"
KNOWLEDGE_ROOT = ROOT / "codex-expert-kit" / "rag" / "knowledge"

search_expert_knowledge = import_search_tool()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_items() -> list[dict[str, Any]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json"))]


def test_protocol_documents_define_must_search_search_citation_and_no_hit() -> None:
    text = read_text(CONTRACT)
    required = [
        "Mandatory Retrieval Triggers",
        "search_expert_knowledge",
        "accepted reference",
        "machine_gate.default_guidance = allow",
        "AI Engineering Gating/Scoring Retrieval",
        "gate_suggestion",
        "Citation Contract",
        "No-Hit Contract",
        "Do not invent professional rules",
    ]
    for phrase in required:
        assert phrase in text


def test_external_templates_reference_active_retrieval_rules() -> None:
    active = read_text(ACTIVE_TEMPLATE)
    external = read_text(EXTERNAL_TEMPLATE)
    plan = read_text(TEST_PLAN)
    for phrase in [
        "Must Search",
        "How To Search",
        "How To Cite",
        "No Hit",
        "machine_gate.default_guidance = allow",
        "accepted reference",
        "AI Engineering Gating/Scoring",
        "gate_suggestion",
    ]:
        assert phrase in active
    assert "external_project_active_retrieval_AGENTS.md" in external
    assert "test_external_ai_active_retrieval_protocol.py" in plan


def test_default_active_retrieval_returns_formal_accepted_knowledge() -> None:
    response = search_expert_knowledge(
        {
            "request_id": "active_retrieval_backtest",
            "query": "backtest data leakage lookahead overfitting",
            "task_type": "backtest_review",
            "top_k": 5,
            "filters": {"domain": "backtest"},
        },
        knowledge_items=load_items(),
    )
    assert response["status"] in {"ok", "warning"}
    assert response["results"]
    assert all(item["review_status"] in {"approved", "reviewed"} for item in response["results"])
    assert all(item["acceptance_level"] in {"approved_guidance", "accepted_reference"} for item in response["results"])
    assert all(item["source_count"] > 0 for item in response["results"])


def test_reviewed_caveat_only_is_default_accepted_reference_but_not_approved_guidance() -> None:
    base = next(item for item in load_items() if item["review"]["review_status"] == "approved")
    reviewed = copy.deepcopy(base)
    reviewed["knowledge_id"] = "kb_test.active_retrieval.reviewed_caveat.v1"
    reviewed["title"] = "Active retrieval reviewed caveat fixture"
    reviewed["content"]["statement"] = "active retrieval reviewed caveat fixture"
    reviewed["review"]["review_status"] = "reviewed"
    reviewed["review"]["default_guidance_allowed"] = False
    reviewed["machine_gate"] = {
        "default_guidance": "caveat_only",
        "reason": "reviewed but not approved",
        "requires_human_escalation": True,
        "blocking_reasons": ["review_status_not_approved"],
        "checked_at": "2026-06-09",
        "gate_version": "1.0.0",
    }

    default_response = search_expert_knowledge(
        {
            "request_id": "active_retrieval_default",
            "query": "active retrieval reviewed caveat fixture",
            "top_k": 5,
        },
        knowledge_items=[reviewed],
    )
    assert default_response["results"]
    assert default_response["results"][0]["machine_gate"]["default_guidance"] == "caveat_only"
    assert default_response["results"][0]["acceptance_level"] == "accepted_reference"
    assert default_response["results"][0]["recommended_next_action"] == "cite_with_caveat"

    allow_only_response = search_expert_knowledge(
        {
            "request_id": "active_retrieval_allow_only",
            "query": "active retrieval reviewed caveat fixture",
            "top_k": 5,
            "include": {"default_guidance_only": True},
        },
        knowledge_items=[reviewed],
    )
    assert allow_only_response["results"] == []
    assert allow_only_response["blocked_results"][0]["blocked_reason"] == "machine_gate_caveat_only"
