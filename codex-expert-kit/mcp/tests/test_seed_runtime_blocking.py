from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from codex_expert_kit_mcp_import import import_search_tool


ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_ROOT = ROOT / "codex-expert-kit" / "rag" / "knowledge"


search_expert_knowledge = import_search_tool()


def load_base_item() -> dict[str, Any]:
    path = KNOWLEDGE_ROOT / "KB_09_RAG_ENGINEERING" / "kb_09_rag_engineering.source_quality.unsourced_default_block.v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def search(items: list[dict[str, Any]]) -> dict[str, Any]:
    return search_expert_knowledge(
        {
            "request_id": "seed_blocking",
            "query": "blocking fixture should not default guidance",
            "top_k": 5,
            "filters": {"review_status": "approved"},
            "include": {"sources": True, "conflicts": True, "deprecated": False, "draft": False, "reviewed": False},
        },
        knowledge_items=items,
    )


def make_variant(suffix: str) -> dict[str, Any]:
    item = copy.deepcopy(load_base_item())
    item["knowledge_id"] = f"kb_test.blocking.{suffix}.v1"
    item["title"] = f"Blocking fixture {suffix}"
    item["content"]["statement"] = "blocking fixture should not default guidance"
    return item


def assert_blocked(item: dict[str, Any]) -> None:
    response = search([item])
    assert response["results"] == []
    assert response["audit"]["blocked_count"] == 1


def test_unsourced_approved_item_is_blocked() -> None:
    item = make_variant("unsourced")
    item["source_evidence"] = []
    assert_blocked(item)


def test_confirmed_conflict_item_is_blocked() -> None:
    item = make_variant("confirmed_conflict")
    item["conflict_audit"]["conflict_status"] = "confirmed"
    assert_blocked(item)


def test_deprecated_item_is_blocked() -> None:
    item = make_variant("deprecated")
    item["review"]["review_status"] = "deprecated"
    item["review"]["freshness"] = "deprecated"
    assert_blocked(item)


def test_draft_item_is_blocked() -> None:
    item = make_variant("draft")
    item["review"]["review_status"] = "draft"
    response = search_expert_knowledge({"request_id": "draft", "query": "blocking fixture should not default guidance", "top_k": 5}, knowledge_items=[item])
    assert response["results"] == []
    assert response["audit"]["blocked_count"] == 1


def test_rejected_item_is_blocked() -> None:
    item = make_variant("rejected")
    item["review"]["review_status"] = "rejected"
    response = search_expert_knowledge({"request_id": "rejected", "query": "blocking fixture should not default guidance", "top_k": 5}, knowledge_items=[item])
    assert response["results"] == []
    assert response["audit"]["blocked_count"] == 1


def test_project_binding_mismatch_is_blocked() -> None:
    item = make_variant("project_mismatch")
    item["metadata"]["project_binding"] = "private_project_alpha"
    response = search_expert_knowledge(
        {
            "request_id": "project_mismatch",
            "query": "blocking fixture should not default guidance",
            "project_context": {"project_name": "other_project"},
            "top_k": 5,
        },
        knowledge_items=[item],
    )
    assert response["results"] == []
    assert response["audit"]["blocked_count"] == 1


def test_reviewed_item_returns_as_default_accepted_reference() -> None:
    item = make_variant("reviewed_caveat")
    item["review"]["review_status"] = "reviewed"
    item["review"]["default_guidance_allowed"] = False
    item["machine_gate"] = {
        "default_guidance": "caveat_only",
        "reason": "reviewed but not approved",
        "requires_human_escalation": True,
        "blocking_reasons": ["review_status_not_approved"],
        "checked_at": "2026-06-09",
        "gate_version": "1.0.0",
    }
    response = search_expert_knowledge(
        {"request_id": "reviewed_default_block", "query": "blocking fixture should not default guidance", "top_k": 5},
        knowledge_items=[item],
    )
    assert response["results"]
    assert response["results"][0]["machine_gate"]["default_guidance"] == "caveat_only"
    assert response["results"][0]["acceptance_level"] == "accepted_reference"
    assert response["results"][0]["recommended_next_action"] == "cite_with_caveat"


def test_reviewed_item_is_blocked_when_caller_requests_allow_only() -> None:
    item = make_variant("reviewed_audit")
    item["review"]["review_status"] = "reviewed"
    item["review"]["default_guidance_allowed"] = False
    item["machine_gate"] = {
        "default_guidance": "caveat_only",
        "reason": "reviewed but not approved",
        "requires_human_escalation": True,
        "blocking_reasons": ["review_status_not_approved"],
        "checked_at": "2026-06-09",
        "gate_version": "1.0.0",
    }
    response = search_expert_knowledge(
        {
            "request_id": "reviewed_allow_only_mode",
            "query": "blocking fixture should not default guidance",
            "top_k": 5,
            "include": {"default_guidance_only": True},
        },
        knowledge_items=[item],
    )
    assert response["results"] == []
    assert response["audit"]["blocked_count"] == 1
    assert response["blocked_results"][0]["blocked_reason"] == "machine_gate_caveat_only"
