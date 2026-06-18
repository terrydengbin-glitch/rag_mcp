from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SERVER = ROOT / "codex-expert-kit" / "mcp" / "server.py"
SAMPLE_ITEMS = ROOT / "codex-expert-kit" / "rag" / "examples" / "sample_knowledge_items.json"
FORMAL_ITEMS = ROOT / "codex-expert-kit" / "rag" / "indexes" / "knowledge_items.json"


def run_server(*args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SERVER), *args],
        cwd=str(ROOT),
        env=env,
        text=True,
        capture_output=True,
        timeout=10,
        check=False,
    )


def test_list_tools() -> None:
    result = run_server("--list-tools")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert "search_expert_knowledge" in data["tools"]
    assert "browse_knowledge_tree" in data["tools"]
    assert "place_order" not in data["tools"]


def test_default_knowledge_items_path_uses_formal_index() -> None:
    result = run_server("--info")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert Path(data["knowledge_items_path"]) == FORMAL_ITEMS


def test_env_root_uses_resolver_for_formal_index() -> None:
    env = dict(os.environ)
    env["CEK_TA_ROOT"] = str(ROOT)
    result = run_server("--info", env=env)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert Path(data["knowledge_items_path"]) == FORMAL_ITEMS


def test_default_search_uses_formal_seed_knowledge() -> None:
    request = {
        "request_id": "test_default_formal_seed",
        "query": "OHLC same bar take profit stop loss fill model",
        "top_k": 5,
        "filters": {"review_status": "approved"},
    }
    result = run_server(
        "--call",
        "search_expert_knowledge",
        "--request-json",
        json.dumps(request),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    ids = {item["knowledge_id"] for item in data["data"]["results"]}
    assert "kb_04_backtest.fill_model.ohlc_same_bar_path_ambiguity.v1" in ids
    assert data["data"]["results"][0]["source_refs"]


def test_search_by_tree_node() -> None:
    request = {
        "request_id": "test_search_tree",
        "query": "lookahead bias",
        "top_k": 2,
        "filters": {"tree_node_id": "kt.backtest.bias"},
    }
    result = run_server(
        "--call",
        "search_expert_knowledge",
        "--knowledge-items-path",
        str(SAMPLE_ITEMS),
        "--request-json",
        json.dumps(request),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["trace_id"] == "test_search_tree"
    first = data["data"]["results"][0]
    assert first["tree_node_id"] == "kt.backtest.bias"
    assert first["tree_path"]
    assert first["source_refs"]
    assert first["recommended_next_action"] == "use_as_guidance"


def test_empty_query_error() -> None:
    request = {"request_id": "test_empty_query", "query": "", "top_k": 2}
    result = run_server(
        "--call",
        "search_expert_knowledge",
        "--knowledge-items-path",
        str(SAMPLE_ITEMS),
        "--request-json",
        json.dumps(request),
    )
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert data["errors"][0]["code"] == "invalid_input"


def test_forbidden_tool_is_blocked() -> None:
    result = run_server("--call", "place_order", "--request-json", "{}")
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert data["errors"][0]["code"] == "permission_denied"


def test_browse_tree() -> None:
    request = {"request_id": "test_tree", "node_id": "kt.backtest", "include_children": True}
    result = run_server("--call", "browse_knowledge_tree", "--request-json", json.dumps(request))
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    node_ids = {item["node_id"] for item in data["data"]["nodes"]}
    assert "kt.backtest" in node_ids
    assert "kt.backtest.bias" in node_ids


def test_request_file(tmp_path: Path) -> None:
    request_file = tmp_path / "request.json"
    request_file.write_text(json.dumps({"request_id": "test_file", "node_id": "kt.backtest"}), encoding="utf-8")
    result = run_server("--call", "browse_knowledge_tree", "--request-file", str(request_file))
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["trace_id"] == "test_file"
