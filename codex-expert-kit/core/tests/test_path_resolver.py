from __future__ import annotations

import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE_DIR = ROOT / "codex-expert-kit" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_project_root, resolve_repo_path  # noqa: E402


def test_resolve_project_root_by_walking_from_file(monkeypatch) -> None:
    monkeypatch.delenv("CEK_TA_ROOT", raising=False)

    resolved = resolve_project_root(__file__)

    assert resolved == ROOT
    assert (resolved / "AGENTS.md").exists()
    assert (resolved / "docs" / "index_tasks.md").exists()


def test_resolve_project_root_from_env(monkeypatch) -> None:
    monkeypatch.setenv("CEK_TA_ROOT", str(ROOT))

    resolved = resolve_project_root()

    assert resolved == ROOT


def test_invalid_env_root_is_rejected(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CEK_TA_ROOT", str(tmp_path))

    try:
        resolve_project_root()
    except ValueError as exc:
        assert "invalid CEK-TA root" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("invalid CEK_TA_ROOT should fail")


def test_resolve_repo_path(monkeypatch) -> None:
    monkeypatch.delenv("CEK_TA_ROOT", raising=False)

    path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)

    assert path == ROOT / "codex-expert-kit" / "rag" / "indexes" / "knowledge_items.json"


def test_env_override_does_not_leak(monkeypatch) -> None:
    monkeypatch.delenv("CEK_TA_ROOT", raising=False)
    assert os.environ.get("CEK_TA_ROOT") is None
