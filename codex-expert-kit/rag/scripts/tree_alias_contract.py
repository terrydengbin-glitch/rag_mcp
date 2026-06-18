"""Shared knowledge tree alias contract helpers."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


ALIAS_PATH = resolve_repo_path("codex-expert-kit", "rag", "knowledge_tree_aliases.json", start_file=__file__)


def load_aliases() -> dict[str, str]:
    payload = json.loads(ALIAS_PATH.read_text(encoding="utf-8"))
    aliases = payload.get("aliases", {})
    if not isinstance(aliases, dict):
        raise ValueError(f"{ALIAS_PATH} aliases must be an object.")
    return {str(key): str(value) for key, value in aliases.items()}


def normalize_node_id(node_id: Any, aliases: dict[str, str] | None = None) -> str:
    if not node_id:
        return ""
    mapping = aliases if aliases is not None else load_aliases()
    current = str(node_id)
    seen: set[str] = set()
    while current in mapping and current not in seen:
        seen.add(current)
        current = mapping[current]
    return current
