"""Build the Vue3 knowledge tree scope index for large-branch rendering."""

from __future__ import annotations

import hashlib
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


TREE_FIXTURE_PATH = resolve_repo_path("ui", "public", "data", "knowledgeTreeNodes.json", start_file=__file__)
FORMAL_FIXTURE_PATH = resolve_repo_path("ui", "public", "data", "formalKnowledgeItems.json", start_file=__file__)
CANDIDATE_FIXTURE_PATH = resolve_repo_path("ui", "public", "data", "phase23Candidates.json", start_file=__file__)
OUTPUT_PATH = resolve_repo_path("ui", "public", "data", "knowledgeTreeScopeIndex.json", start_file=__file__)

ALIASES = load_aliases()


def atomic_write_text(path: Path, text: str) -> None:
    temp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temp_path.write_text(text, encoding="utf-8", newline="\n")
    temp_path.replace(path)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
      for chunk in iter(lambda: handle.read(1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def load_fixture(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    items = payload.get("items") if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        raise ValueError(f"{path} must contain an items array.")
    return [item for item in items if isinstance(item, dict)]


def normalize_node_id(node_id: str | None) -> str:
    return normalize_alias_node_id(node_id, ALIASES)


def item_node_ids(item: dict[str, Any]) -> set[str]:
    values = {
        item.get("canonical_node_id"),
        item.get("tree_node_id"),
    }
    return {normalize_node_id(str(value)) for value in values if isinstance(value, str) and value}


def candidate_node_ids(item: dict[str, Any]) -> set[str]:
    values = {
        item.get("canonical_node_id"),
        item.get("tree_node_id"),
    }
    return {normalize_node_id(str(value)) for value in values if isinstance(value, str) and value}


def build_descendant_index(nodes: list[dict[str, Any]]) -> dict[str, list[str]]:
    child_map: dict[str, list[str]] = {}
    node_ids = {str(node.get("node_id")) for node in nodes if node.get("node_id")}
    for node in nodes:
        node_id = str(node.get("node_id"))
        parent_id = node.get("parent_id")
        if isinstance(parent_id, str) and parent_id in node_ids:
            child_map.setdefault(parent_id, []).append(node_id)

    descendants_by_node: dict[str, list[str]] = {}
    for node_id in sorted(node_ids):
        descendants: list[str] = []
        queue = list(child_map.get(node_id, []))
        while queue:
            current = queue.pop(0)
            descendants.append(current)
            queue.extend(child_map.get(current, []))
        descendants_by_node[node_id] = descendants
    return descendants_by_node


def in_scope(candidate_ids: set[str], scope_ids: set[str]) -> bool:
    for item_id in candidate_ids:
        if item_id in scope_ids:
            return True
        if any(item_id.startswith(f"{scope_id}.") for scope_id in scope_ids):
            return True
    return False


def count_conflict(status: Any) -> bool:
    return isinstance(status, str) and status not in {"none", "resolved", ""}


def build_index() -> dict[str, Any]:
    nodes = load_fixture(TREE_FIXTURE_PATH)
    formal_items = load_fixture(FORMAL_FIXTURE_PATH)
    candidates = load_fixture(CANDIDATE_FIXTURE_PATH)
    descendants_by_node = build_descendant_index(nodes)

    output_nodes: dict[str, Any] = {}
    for node in sorted(nodes, key=lambda item: (int(item.get("level", 0) or 0), str(item.get("node_id", "")))):
        node_id = str(node.get("node_id"))
        descendant_ids = descendants_by_node.get(node_id, [])
        scope_ids = {node_id, *descendant_ids}
        scoped_formal = [
            item
            for item in formal_items
            if in_scope(item_node_ids(item), scope_ids)
        ]
        scoped_candidates = [
            item
            for item in candidates
            if in_scope(candidate_node_ids(item), scope_ids)
        ]
        output_nodes[node_id] = {
            "node_id": node_id,
            "descendant_node_ids": descendant_ids,
            "knowledge_ids": [str(item.get("knowledge_id")) for item in scoped_formal if item.get("knowledge_id")],
            "candidate_ids": [str(item.get("candidate_id")) for item in scoped_candidates if item.get("candidate_id")],
            "counts": {
                "knowledge_total": len(scoped_formal),
                "candidate_total": len(scoped_candidates),
                "reviewed": sum(1 for item in scoped_formal if item.get("review_status") == "reviewed"),
                "approved": sum(1 for item in scoped_formal if item.get("review_status") == "approved"),
                "accepted_for_draft": sum(1 for item in scoped_candidates if item.get("candidate_status") == "accepted_for_draft"),
                "needs_more_evidence": sum(1 for item in scoped_candidates if item.get("candidate_status") == "needs_more_evidence"),
                "rejected": sum(1 for item in scoped_candidates if item.get("candidate_status") == "rejected"),
                "source_count": sum(len(item.get("sources", [])) for item in scoped_formal)
                + sum(int(item.get("source_count", 0) or 0) for item in scoped_candidates),
                "open_gap_count": sum(len(scope_node.get("open_gaps", [])) for scope_node in nodes if str(scope_node.get("node_id")) in scope_ids),
                "conflict_count": sum(1 for item in scoped_formal if count_conflict(item.get("conflict_status")))
                + sum(1 for item in scoped_candidates if count_conflict(item.get("conflict_status"))),
            },
        }

    return {
        "schema_version": "phase51.scope_index.v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source": "ui/public/data/knowledgeTreeNodes.json + formalKnowledgeItems.json + phase23Candidates.json",
        "source_version": {
            "knowledge_tree": sha256_file(TREE_FIXTURE_PATH),
            "formal_knowledge": sha256_file(FORMAL_FIXTURE_PATH),
            "candidates": sha256_file(CANDIDATE_FIXTURE_PATH),
        },
        "count": len(output_nodes),
        "nodes": output_nodes,
    }


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = build_index()
    atomic_write_text(OUTPUT_PATH, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {OUTPUT_PATH} with {payload['count']} scope nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
