from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient


API_ROOT = Path(__file__).resolve().parents[1]
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from codex_expert_kit_api.main import app  # noqa: E402


client = TestClient(app)


def test_health_is_read_only():
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    assert payload["data"]["read_only"] is True


def test_roots_return_three_l1_branches():
    response = client.get("/api/knowledge-tree/roots")
    assert response.status_code == 200
    roots = response.json()["data"]["roots"]
    assert [item["title"] for item in roots] == ["Trading Engineering", "AI Engineering", "Project Integration"]


def test_children_do_not_expand_l3_by_default():
    response = client.get("/api/knowledge-tree/nodes/kt.trading_engineering.backtest/children")
    assert response.status_code == 200
    children = response.json()["data"]["children"]
    assert children == []


def test_children_can_include_l3_when_requested():
    response = client.get("/api/knowledge-tree/nodes/kt.trading_engineering.backtest/children?include_l3=true")
    assert response.status_code == 200
    children = response.json()["data"]["children"]
    assert any(item["id"] == "kt.backtest.bias" for item in children)


def test_phase38_ai_engineering_level2_nodes_are_exposed():
    response = client.get("/api/knowledge-tree/nodes/kt.ai_engineering/children")
    assert response.status_code == 200
    node_ids = {item["id"] for item in response.json()["data"]["children"]}
    assert {
        "kt.ai_engineering.numeric_scoring",
        "kt.ai_engineering.calibration_threshold",
        "kt.ai_engineering.decision_time_feature_contract",
        "kt.ai_engineering.llm_audit_assistant",
        "kt.ai_engineering.shadow_paper_ope_eval",
        "kt.ai_engineering.model_release_governance",
    }.issubset(node_ids)


def test_phase38_trading_ai_rag_pack_alias_is_exposed_as_l3():
    response = client.get("/api/knowledge-tree/nodes/kt.ai_engineering.rag_engineering/children?include_l3=true")
    assert response.status_code == 200
    children = response.json()["data"]["children"]
    assert any(item["id"] == "kt.rag_engineering.trading_scoring_rag_pack" for item in children)

    alias_response = client.get("/api/knowledge-tree/nodes/kt.rag_engineering.trading_scoring_rag_pack")
    assert alias_response.status_code == 200
    assert alias_response.json()["data"]["node"]["id"] == "kt.rag_engineering.trading_scoring_rag_pack"


def test_knowledge_pagination_rejects_page_size_over_limit():
    response = client.get("/api/knowledge-tree/nodes/kt.trading_engineering/knowledge?page_size=500")
    assert response.status_code == 400
    assert response.json()["error"]["error_code"] == "INVALID_QUERY"


def test_knowledge_list_supports_pagination():
    response = client.get("/api/knowledge-tree/nodes/kt.trading_engineering/knowledge?page=1&page_size=20")
    assert response.status_code == 200
    payload = response.json()["data"]["knowledge"]
    assert payload["page"] == 1
    assert payload["page_size"] == 20
    assert "items" in payload
    if payload["items"]:
        first = payload["items"][0]
        assert "claim_type" in first
        assert "llm_usage_policy" in first
        assert "machine_gate" in first
        assert "recommended_extra_sources_count" in first


def test_item_detail_contains_sources_and_scope():
    list_response = client.get("/api/knowledge-tree/nodes/kt.trading_engineering/knowledge?page_size=20")
    first = list_response.json()["data"]["knowledge"]["items"][0]
    response = client.get(f"/api/knowledge-items/{first['id']}")
    assert response.status_code == 200
    item = response.json()["data"]["item"]
    assert item["sources"]
    assert item["applicable_scope"] is not None
    assert item["not_applicable_scope"] is not None
    assert item["claim_type"]
    assert item["llm_usage_policy"]["not_allowed"]
    assert item["machine_gate"]["default_guidance"] in {"allow", "caveat_only", "deny"}
    assert "recommended_extra_sources_count" in item


def test_unknown_node_returns_node_not_found():
    response = client.get("/api/knowledge-tree/nodes/kt.unknown")
    assert response.status_code == 404
    assert response.json()["error"]["error_code"] == "NODE_NOT_FOUND"


def test_unknown_item_returns_item_not_found():
    response = client.get("/api/knowledge-items/not_real")
    assert response.status_code == 404
    assert response.json()["error"]["error_code"] == "ITEM_NOT_FOUND"


def test_api_exposes_no_write_routes():
    disallowed = {"POST", "PUT", "PATCH", "DELETE"}
    for route in app.routes:
        methods = getattr(route, "methods", set()) or set()
        assert not (methods & disallowed), f"{route.path} exposes write method {methods & disallowed}"
