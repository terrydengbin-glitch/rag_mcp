from __future__ import annotations

from pathlib import Path
import sys

from fastapi.testclient import TestClient


API_ROOT = Path(__file__).resolve().parents[1]
if str(API_ROOT) not in sys.path:
    sys.path.insert(0, str(API_ROOT))

from codex_expert_kit_api.main import app  # noqa: E402


client = TestClient(app)


def test_candidates_list_is_read_only_fixture_api():
    response = client.get("/api/candidates?limit=3")
    assert response.status_code == 200
    payload = response.json()
    assert payload["ok"] is True
    data = payload["data"]
    assert data["source"] == "api"
    assert data["limit"] == 3
    assert data["items"]
    assert data["items"][0]["candidate_status"] in {"candidate_ready", "needs_more_evidence", "blocked"}
    assert data["items"][0]["risk_level"].startswith("risk_")


def test_candidates_filter_by_tree_node():
    response = client.get("/api/candidates?tree_node_id=kt.trading_engineering.backtest")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert any(item["tree_node_id"] == "kt.trading_engineering.backtest.bias" for item in items)


def test_phase36_ai_engineering_candidates_filter_by_ai_security_node():
    response = client.get("/api/candidates?tree_node_id=kt.ai_security_privacy_compliance")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert items
    assert all(item["tree_node_id"] == "kt.ai_security_privacy_compliance" for item in items)
    assert any("prompt_injection" in item["normalized_claim"] for item in items)


def test_phase36_ai_engineering_candidates_filter_by_llm_training_subtree():
    response = client.get("/api/candidates?tree_node_id=kt.llm_training")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert any(str(item["tree_node_id"]).startswith("kt.llm_training") for item in items)
    assert any(item["research_task_id"].startswith("RIT-P36") for item in items)


def test_phase38_candidates_filter_by_new_ai_engineering_node():
    response = client.get("/api/candidates?tree_node_id=kt.ai_engineering.numeric_scoring&limit=20")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert items
    assert all(item["tree_node_id"] == "kt.ai_engineering.numeric_scoring" for item in items)
    assert any(item["research_task_id"].startswith("P38-") for item in items)


def test_phase38_rag_pack_candidates_filter_by_display_alias():
    response = client.get("/api/candidates?tree_node_id=kt.ai_engineering.rag_engineering.trading_scoring_rag_pack&limit=20")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert items
    assert all(item["tree_node_id"] == "kt.rag_engineering.trading_scoring_rag_pack" for item in items)
    assert any(item["research_task_id"].startswith("P38-") for item in items)


def test_candidate_detail_contains_sources_and_checklist():
    list_response = client.get("/api/candidates?limit=1")
    first = list_response.json()["data"]["items"][0]
    response = client.get(f"/api/candidates/{first['candidate_id']}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["item"]["candidate_id"] == first["candidate_id"]
    assert data["sources"]
    assert data["checklist"]["checks"]
    assert "can_accept_for_draft" in data["checklist"]


def test_unknown_candidate_returns_contract_error():
    response = client.get("/api/candidates/not_real")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["error_code"] == "CANDIDATE_NOT_FOUND"
    assert error["code"] == "CANDIDATE_NOT_FOUND"
    assert error["retryable"] is False


def test_candidate_api_exposes_no_write_routes():
    disallowed = {"POST", "PUT", "PATCH", "DELETE"}
    for route in app.routes:
        if not str(route.path).startswith("/api/candidates"):
            continue
        methods = getattr(route, "methods", set()) or set()
        assert not (methods & disallowed), f"{route.path} exposes write method {methods & disallowed}"
