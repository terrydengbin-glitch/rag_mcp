from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from types import ModuleType


def _load_path_resolver() -> ModuleType:
    env_root = os.environ.get("CEK_TA_ROOT")
    candidates: list[Path] = []
    if env_root:
      candidates.append(Path(env_root).expanduser().resolve() / "codex-expert-kit" / "core" / "path_resolver.py")

    current = Path(__file__).resolve()
    for parent in current.parents:
        candidates.append(parent / "core" / "path_resolver.py")
        candidates.append(parent / "codex-expert-kit" / "core" / "path_resolver.py")

    for candidate in candidates:
        if candidate.exists():
            spec = importlib.util.spec_from_file_location("cek_ta_path_resolver", candidate)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module

    raise RuntimeError("Unable to load codex-expert-kit/core/path_resolver.py")


path_resolver = _load_path_resolver()
resolve_repo_path = path_resolver.resolve_repo_path
resolve_project_root = path_resolver.resolve_project_root
