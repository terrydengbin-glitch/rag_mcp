from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[3]
MCP_DIR = ROOT / "codex-expert-kit" / "mcp"


def import_search_tool() -> Callable[..., dict[str, Any]]:
    if str(MCP_DIR) not in sys.path:
        sys.path.insert(0, str(MCP_DIR))
    module_path = MCP_DIR / "search_expert_knowledge.py"
    spec = importlib.util.spec_from_file_location("search_expert_knowledge", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load search_expert_knowledge.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.search_expert_knowledge
