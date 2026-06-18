"""Build the formal CEK-TA knowledge_items.json aggregate index.

This script keeps the source of truth in rag/knowledge/**/*.json and writes a
read-only aggregate used by the MCP runtime default path.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_project_root, resolve_repo_path  # noqa: E402


ROOT = resolve_project_root(__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
OUTPUT_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)


REQUIRED_PATHS = [
    ("knowledge_id", ("knowledge_id",)),
    ("metadata.partition_id", ("metadata", "partition_id")),
    ("metadata.domain", ("metadata", "domain")),
    ("metadata.tree_node_id", ("metadata", "tree_node_id")),
    ("source_evidence", ("source_evidence",)),
    ("review.review_status", ("review", "review_status")),
    ("review.freshness", ("review", "freshness")),
    ("conflict_audit.conflict_status", ("conflict_audit", "conflict_status")),
    ("metadata.claim_type", ("metadata", "claim_type")),
    ("llm_usage_policy", ("llm_usage_policy",)),
    ("machine_gate.default_guidance", ("machine_gate", "default_guidance")),
    ("applicability.applies_when", ("applicability", "applies_when")),
    ("applicability.not_applicable_when", ("applicability", "not_applicable_when")),
]


def deep_get(item: dict[str, Any], path: tuple[str, ...]) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def validate_item(item: dict[str, Any], source_path: Path) -> None:
    missing = []
    for label, path in REQUIRED_PATHS:
        value = deep_get(item, path)
        if value in (None, "", []):
            missing.append(label)
    if missing:
        rel = source_path.relative_to(ROOT).as_posix()
        raise ValueError(f"{rel} missing required fields: {', '.join(missing)}")


def load_items() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        item = json.loads(path.read_text(encoding="utf-8-sig"))
        if not isinstance(item, dict):
            raise ValueError(f"{path} must contain a JSON object.")
        validate_item(item, path)
        knowledge_id = str(item["knowledge_id"])
        if knowledge_id in seen_ids:
            raise ValueError(f"Duplicate knowledge_id: {knowledge_id}")
        seen_ids.add(knowledge_id)
        items.append(item)
    return sorted(items, key=lambda value: str(value.get("knowledge_id", "")))


def build_index() -> dict[str, Any]:
    items = load_items()
    return {
        "schema": "cek_ta_knowledge_items_index",
        "schema_version": "1.1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_root": "codex-expert-kit/rag/knowledge",
        "item_count": len(items),
        "items": items,
    }


def main() -> int:
    index = build_index()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_PATH} with {index['item_count']} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
