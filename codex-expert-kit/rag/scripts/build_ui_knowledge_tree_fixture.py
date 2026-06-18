"""Build the Vue3 knowledge tree fixture from knowledge_tree.md."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402
from tree_alias_contract import load_aliases, normalize_node_id as normalize_alias_node_id  # noqa: E402


TREE_PATH = resolve_repo_path("codex-expert-kit", "rag", "knowledge_tree.md", start_file=__file__)
INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
OUTPUT_PATH = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
JSON_OUTPUT_PATH = resolve_repo_path("ui", "public", "data", "knowledgeTreeNodes.json", start_file=__file__)

ALIASES = load_aliases()


def atomic_write_text(path: Path, text: str) -> None:
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(text, encoding="utf-8", newline="\n")
    temp_path.replace(path)


def parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip().strip('"')
    if value == "null":
        return None
    if value.isdigit():
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"').strip("'") for part in inner.split(",")]
    return value


def normalize_node_id(node_id: str | None) -> str:
    return normalize_alias_node_id(node_id, ALIASES)


def parse_tree_nodes() -> list[dict[str, Any]]:
    nodes: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    sort_order = 0
    fields = {
        "parent_id",
        "path",
        "title",
        "domain",
        "subdomain",
        "level",
        "summary",
        "coverage_status",
        "review_status",
        "freshness_status",
        "conflict_status",
        "related_nodes",
    }
    for line in TREE_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- node_id:") or stripped.startswith("node_id:"):
            if current:
                nodes.append(current)
            sort_order += 10
            node_id = str(parse_scalar(stripped.split("node_id:", 1)[1]))
            current = {"node_id": node_id, "sort_order": sort_order}
            continue
        if current is None or ":" not in stripped:
            continue
        field, raw_value = stripped.split(":", 1)
        if field in fields:
            current[field] = parse_scalar(raw_value)
    if current:
        nodes.append(current)
    return [normalize_tree_node(node) for node in nodes]


def normalize_tree_node(node: dict[str, Any]) -> dict[str, Any]:
    return {
        "node_id": str(node.get("node_id", "")),
        "parent_id": node.get("parent_id"),
        "path": str(node.get("path", "")),
        "title": str(node.get("title") or node.get("node_id")),
        "domain": str(node.get("domain", "unknown")),
        "subdomain": str(node.get("subdomain", "unknown")),
        "level": int(node.get("level", 0) or 0),
        "summary": str(node.get("summary", "")),
        "coverage_status": str(node.get("coverage_status", "partial")),
        "review_status": str(node.get("review_status", "reviewed")),
        "freshness_status": str(node.get("freshness_status", "stable")),
        "conflict_status": str(node.get("conflict_status", "unchecked")),
        "approved_item_count": 0,
        "reviewed_item_count": 0,
        "source_count": 0,
        "open_gaps": [],
        "related_nodes": node.get("related_nodes") if isinstance(node.get("related_nodes"), list) else [],
        "sort_order": int(node.get("sort_order", 0) or 0),
    }


def descendants(node_id: str, nodes: list[dict[str, Any]]) -> set[str]:
    result = {node_id}
    queue = [node_id]
    while queue:
        current = queue.pop(0)
        for child in [node for node in nodes if node.get("parent_id") == current]:
            child_id = str(child["node_id"])
            result.add(child_id)
            queue.append(child_id)
    return result


def in_scope(item_node_id: str, scope: set[str]) -> bool:
    canonical = normalize_node_id(item_node_id)
    return canonical in scope or any(canonical.startswith(f"{node}.") for node in scope)


def load_formal_items() -> list[dict[str, Any]]:
    payload = json.loads(INDEX_PATH.read_text(encoding="utf-8-sig"))
    items = payload.get("items", payload if isinstance(payload, list) else [])
    return items if isinstance(items, list) else []


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_ROOT.glob("**/*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(raw, dict):
            candidates.append(raw)
    return candidates


def item_node_id(item: dict[str, Any]) -> str:
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    return normalize_node_id(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")


def candidate_node_id(item: dict[str, Any]) -> str:
    classification = item.get("classification") if isinstance(item.get("classification"), dict) else {}
    return normalize_node_id(classification.get("canonical_node_id") or classification.get("tree_node_id") or "")


def apply_counts(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    formal_items = load_formal_items()
    candidates = load_candidates()
    enriched: list[dict[str, Any]] = []
    for node in nodes:
        scope = descendants(node["node_id"], nodes)
        scoped_formal = [item for item in formal_items if in_scope(item_node_id(item), scope)]
        scoped_candidates = [item for item in candidates if in_scope(candidate_node_id(item), scope)]
        clone = dict(node)
        clone["approved_item_count"] = sum(
            1 for item in scoped_formal if item.get("review", {}).get("review_status") == "approved"
        )
        clone["reviewed_item_count"] = sum(
            1 for item in scoped_formal if item.get("review", {}).get("review_status") == "reviewed"
        )
        clone["source_count"] = sum(len(item.get("source_evidence", [])) for item in scoped_formal) + sum(
            len(item.get("source_refs", [])) for item in scoped_candidates
        )
        if not scoped_formal and clone["coverage_status"] == "empty":
            clone["open_gaps"] = ["暂无正式知识条目"]
        enriched.append(clone)
    return enriched


def render_typescript(nodes: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = json.dumps(nodes, ensure_ascii=False, indent=2)
    return (
        "import type { KnowledgeTreeNode } from '../types'\n\n"
        "// Generated by codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py.\n"
        "// Do not edit by hand; update codex-expert-kit/rag/knowledge_tree.md and regenerate.\n"
        f"export const knowledgeTreeFixtureGeneratedAt = {json.dumps(generated_at)}\n\n"
        f"export const knowledgeTreeNodes: KnowledgeTreeNode[] = {payload}\n"
    )


def render_json_fixture(nodes: list[dict[str, Any]]) -> str:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "schema_version": "phase50.static_fixture.v1",
        "generated_at": generated_at,
        "source": "codex-expert-kit/rag/knowledge_tree.md",
        "count": len(nodes),
        "items": nodes,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    nodes = apply_counts(parse_tree_nodes())
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(OUTPUT_PATH, render_typescript(nodes))
    atomic_write_text(JSON_OUTPUT_PATH, render_json_fixture(nodes))
    print(f"wrote {OUTPUT_PATH} and {JSON_OUTPUT_PATH} with {len(nodes)} knowledge tree nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
