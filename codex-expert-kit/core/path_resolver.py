"""Portable path resolver for CEK-TA.

Use this module instead of hard-coded absolute paths. It supports local
workspace use, submodule use, and CI by resolving from CEK_TA_ROOT or by walking
upward from a known file.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union


PathLike = Union[str, os.PathLike[str]]
ROOT_MARKERS = (
    "AGENTS.md",
    "docs/index_tasks.md",
    "codex-expert-kit",
)


def _is_project_root(path: Path) -> bool:
    return all((path / marker).exists() for marker in ROOT_MARKERS)


def _candidate_start(start_file: Optional[PathLike]) -> Path:
    if start_file is None:
        return Path(__file__).resolve()
    path = Path(start_file).resolve()
    return path if path.is_dir() else path.parent


def resolve_project_root(start_file: Optional[PathLike] = None, *, env_var: str = "CEK_TA_ROOT") -> Path:
    """Resolve the CEK-TA project root.

    Priority:
    1. The env var, if set and valid.
    2. Walking upward from start_file.
    3. Raising ValueError with enough context to fix the caller.
    """

    env_value = os.environ.get(env_var)
    if env_value:
        env_root = Path(env_value).expanduser().resolve()
        if _is_project_root(env_root):
            return env_root
        raise ValueError(f"{env_var} points to an invalid CEK-TA root: {env_root}")

    current = _candidate_start(start_file)
    for candidate in (current, *current.parents):
        if _is_project_root(candidate):
            return candidate

    raise ValueError(f"Unable to resolve CEK-TA project root from: {current}")


def resolve_repo_path(*parts: PathLike, start_file: Optional[PathLike] = None) -> Path:
    """Resolve a path relative to the CEK-TA project root."""

    root = resolve_project_root(start_file=start_file)
    return root.joinpath(*(str(part) for part in parts)).resolve()
