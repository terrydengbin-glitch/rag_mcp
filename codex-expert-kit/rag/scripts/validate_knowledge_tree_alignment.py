"""Validate CEK-TA knowledge tree alignment across API, UI, formal knowledge and candidates."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
CORE_PATH = ROOT / "codex-expert-kit" / "core"
API_PATH = ROOT / "codex-expert-kit" / "api"
if str(CORE_PATH) not in sys.path:
    sys.path.insert(0, str(CORE_PATH))
if str(API_PATH) not in sys.path:
    sys.path.insert(0, str(API_PATH))

from path_resolver import resolve_repo_path  # noqa: E402
from codex_expert_kit_api import services  # noqa: E402


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as fh:
        return json.load(fh)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def item_node_id(item: dict[str, Any]) -> str:
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    return services.normalize_node_id(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")


def candidate_node_id(item: dict[str, Any]) -> str:
    classification = item.get("classification") if isinstance(item.get("classification"), dict) else {}
    return services.normalize_node_id(classification.get("canonical_node_id") or classification.get("tree_node_id") or "")


def best_node(node_id: str, tree_ids: set[str]) -> str | None:
    if not node_id:
        return None
    matches = [candidate for candidate in tree_ids if node_id == candidate or node_id.startswith(f"{candidate}.")]
    if not matches:
        return None
    return max(matches, key=len)


def extract_ui_nodes(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig")
    match = re.search(r"export const knowledgeTreeNodes: KnowledgeTreeNode\[] = (\[.*\])\s*$", text, re.S)
    if not match:
        raise ValueError("Unable to parse ui knowledgeTreeNodes fixture.")
    data = json.loads(match.group(1))
    if not isinstance(data, list):
        raise ValueError("UI knowledgeTreeNodes fixture must contain a JSON array.")
    return data


def load_candidates(candidate_root: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(candidate_root.glob("**/*.json")):
        raw = load_json(path)
        if isinstance(raw, dict):
            candidates.append(raw)
    return candidates


def main() -> int:
    errors: list[str] = []
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    candidate_root = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
    ui_tree_path = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
    report_path = resolve_repo_path("docs", "reports", "phase39_knowledge_tree_alignment_report.json", start_file=__file__)

    api_nodes = services.tree_nodes()
    raw_tree_nodes = services.load_tree_nodes()
    ui_nodes = extract_ui_nodes(ui_tree_path)
    tree_ids = {node["id"] for node in raw_tree_nodes}
    ui_ids = {node["node_id"] for node in ui_nodes}

    data = load_json(index_path)
    formal_items = data.get("items", data if isinstance(data, list) else [])
    if not isinstance(formal_items, list):
        raise ValueError("knowledge_items.json must contain an items array.")
    candidates = load_candidates(candidate_root)

    formal_uncovered = [
        item.get("knowledge_id")
        for item in formal_items
        if (best_node(item_node_id(item), tree_ids) in {None, "kt"})
    ]
    candidate_uncovered = [
        item.get("candidate_id")
        for item in candidates
        if (best_node(candidate_node_id(item), tree_ids) in {None, "kt"})
    ]

    if len(raw_tree_nodes) != len(ui_nodes):
        errors.append(f"API tree node count {len(raw_tree_nodes)} != UI tree node count {len(ui_nodes)}.")
    missing_in_ui = sorted(tree_ids - ui_ids)
    missing_in_api = sorted(ui_ids - tree_ids)
    if missing_in_ui:
        errors.append(f"Nodes missing in UI fixture: {missing_in_ui[:20]}.")
    if missing_in_api:
        errors.append(f"Nodes missing in API tree: {missing_in_api[:20]}.")
    if formal_uncovered:
        errors.append(f"Formal knowledge not mapped below a non-root tree node: {formal_uncovered[:20]}.")
    if candidate_uncovered:
        errors.append(f"Candidates not mapped below a non-root tree node: {candidate_uncovered[:20]}.")

    ui_by_id = {node["node_id"]: node for node in ui_nodes}
    api_by_id = {node["id"]: node for node in api_nodes}
    count_mismatches: list[dict[str, Any]] = []
    for node_id in sorted(tree_ids):
        api_node = api_by_id[node_id]
        ui_node = ui_by_id.get(node_id)
        if not ui_node:
            continue
        for field in ("approved_item_count", "reviewed_item_count", "source_count"):
            if int(api_node.get(field, 0) or 0) != int(ui_node.get(field, 0) or 0):
                count_mismatches.append(
                    {
                        "node_id": node_id,
                        "field": field,
                        "api": api_node.get(field, 0),
                        "ui": ui_node.get(field, 0),
                    }
                )
    if count_mismatches:
        errors.append(f"API/UI count mismatches: {count_mismatches[:20]}.")

    formal_owner_counts = Counter(best_node(item_node_id(item), tree_ids) for item in formal_items)
    candidate_owner_counts = Counter(best_node(candidate_node_id(item), tree_ids) for item in candidates)

    report = {
        "report_id": "phase39_knowledge_tree_alignment",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tree_node_count": len(raw_tree_nodes),
        "api_node_count": len(api_nodes),
        "ui_node_count": len(ui_nodes),
        "formal_knowledge_count": len(formal_items),
        "candidate_count": len(candidates),
        "formal_uncovered_count": len(formal_uncovered),
        "candidate_uncovered_count": len(candidate_uncovered),
        "formal_review_status_counts": Counter(item.get("review", {}).get("review_status", "") for item in formal_items),
        "candidate_decision_counts": Counter(item.get("status", {}).get("ingestion_decision", "") for item in candidates),
        "top_formal_owner_nodes": formal_owner_counts.most_common(30),
        "top_candidate_owner_nodes": candidate_owner_counts.most_common(30),
        "node_count_mismatches": count_mismatches,
        "errors": errors,
        "status": "pass" if not errors else "fail",
    }
    write_json(report_path, report)
    print(json.dumps({"status": report["status"], "errors": errors, "report_path": str(report_path)}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
