"""Generate Phase 55 knowledge-base baseline and runtime acceptance reports."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
MCP_DIR = Path(__file__).resolve().parents[2] / "mcp"
for path in (CORE_DIR, MCP_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from path_resolver import resolve_repo_path  # noqa: E402


TASK_ID = "CEK-TA-535"
PHASE = "Phase 55"
BASELINE_REPORT = ("docs", "reports", "phase55_knowledge_base_baseline_report.json")
RUNTIME_REPORT = ("docs", "reports", "phase55_runtime_acceptance_report.json")

SEARCH_CASES = [
    {
        "case_id": "ai_numeric_scoring",
        "label": "AI Engineering 数值打分",
        "query": "numeric scoring LightGBM calibration final gate",
        "filters": {"canonical_tree_path_prefix": "CEK-TA / AI Engineering", "review_status": ["reviewed", "approved"]},
    },
    {
        "case_id": "trading_backtest",
        "label": "Trading Engineering 回测可信度",
        "query": "backtest data leakage overfitting cost model",
        "filters": {"canonical_tree_path_prefix": "CEK-TA / Trading Engineering", "review_status": ["reviewed", "approved"]},
    },
    {
        "case_id": "trade_analysis",
        "label": "交易复盘与标签",
        "query": "trade analysis reason code MAE MFE planned realized R",
        "filters": {"domain": ["trade_analysis"], "review_status": ["reviewed", "approved"]},
    },
    {
        "case_id": "mcp_rag",
        "label": "RAG/MCP 工程",
        "query": "MCP RAG citation source conflict retrieval",
        "filters": {"domain": ["rag_engineering", "mcp_engineering"], "review_status": ["reviewed", "approved"]},
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deep_get(item: dict[str, Any], dotted_path: str, default: Any = None) -> Any:
    current: Any = item
    for part in dotted_path.split("."):
        if not isinstance(current, dict):
            return default
        current = current.get(part, default)
    return current


def counter_for(items: list[dict[str, Any]], path: str) -> dict[str, int]:
    values = Counter(str(deep_get(item, path, "") or "") for item in items)
    return dict(sorted(values.items(), key=lambda pair: (-pair[1], pair[0])))


def tree_levels_from_path(path: str) -> tuple[str, str, str]:
    parts = [part.strip() for part in str(path or "").split("/") if part.strip()]
    l1 = parts[1] if len(parts) > 1 else "未分类主枝"
    l2 = parts[2] if len(parts) > 2 else "未分类分区"
    l3 = parts[3] if len(parts) > 3 else "未分类专题"
    return l1, l2, l3


def collect_baseline(
    items: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    tree_nodes: list[dict[str, Any]],
) -> dict[str, Any]:
    l1_counter: Counter[str] = Counter()
    l2_counter: Counter[str] = Counter()
    l3_counter: Counter[str] = Counter()
    node_counter: Counter[str] = Counter()
    source_counts: list[int] = []
    missing_sources: list[str] = []
    potential_conflicts: list[str] = []
    confirmed_conflicts: list[str] = []

    for item in items:
        path = deep_get(item, "metadata.canonical_tree_path", deep_get(item, "metadata.tree_path", ""))
        l1, l2, l3 = tree_levels_from_path(path)
        l1_counter[l1] += 1
        l2_counter[f"{l1} / {l2}"] += 1
        l3_counter[f"{l1} / {l2} / {l3}"] += 1
        node_counter[str(deep_get(item, "metadata.canonical_node_id", deep_get(item, "metadata.tree_node_id", "")))] += 1
        source_count = len(item.get("source_evidence") or [])
        source_counts.append(source_count)
        if source_count == 0:
            missing_sources.append(str(item.get("knowledge_id")))
        conflict_status = str(deep_get(item, "conflict_audit.conflict_status", ""))
        if conflict_status == "potential":
            potential_conflicts.append(str(item.get("knowledge_id")))
        if conflict_status == "confirmed":
            confirmed_conflicts.append(str(item.get("knowledge_id")))

    candidate_queue_counts = Counter(str(deep_get(item, "workflow.queue_group", "unknown") or "unknown") for item in candidates)
    candidate_review_counts = Counter(str(item.get("review_status") or deep_get(item, "status.review_status", "unknown")) for item in candidates)
    tree_count_by_level = Counter(str(item.get("level")) for item in tree_nodes)
    approved_items = [item for item in items if deep_get(item, "review.review_status") == "approved"]
    reviewed_items = [item for item in items if deep_get(item, "review.review_status") == "reviewed"]

    warnings: list[str] = []
    if missing_sources:
        warnings.append(f"存在 {len(missing_sources)} 条正式知识缺少 source_evidence。")
    if confirmed_conflicts:
        warnings.append(f"存在 {len(confirmed_conflicts)} 条正式知识为 confirmed conflict。")
    if not approved_items:
        warnings.append("当前没有 approved 知识；外部项目只能按 reviewed/caveat_only 或人工治理使用。")

    return {
        "report_id": "phase55_knowledge_base_baseline_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": "CEK-TA-535",
        "phase": PHASE,
        "knowledge_totals": {
            "formal_total": len(items),
            "approved_total": len(approved_items),
            "reviewed_total": len(reviewed_items),
            "missing_source_total": len(missing_sources),
            "potential_conflict_total": len(potential_conflicts),
            "confirmed_conflict_total": len(confirmed_conflicts),
        },
        "review_status_counts": counter_for(items, "review.review_status"),
        "machine_gate_counts": counter_for(items, "machine_gate.default_guidance"),
        "domain_counts": counter_for(items, "metadata.domain"),
        "partition_counts": counter_for(items, "metadata.partition_id"),
        "l1_counts": dict(sorted(l1_counter.items())),
        "l2_counts": dict(sorted(l2_counter.items())),
        "l3_counts": dict(sorted(l3_counter.items())),
        "source_quality_summary": {
            "total_source_refs": sum(source_counts),
            "min_source_count": min(source_counts) if source_counts else 0,
            "max_source_count": max(source_counts) if source_counts else 0,
            "average_source_count": round(sum(source_counts) / len(source_counts), 2) if source_counts else 0,
            "missing_source_ids": missing_sources[:50],
        },
        "candidate_totals": {"candidate_total": len(candidates)},
        "candidate_queue_counts": dict(sorted(candidate_queue_counts.items())),
        "candidate_review_counts": dict(sorted(candidate_review_counts.items())),
        "knowledge_tree_totals": {
            "node_total": len(tree_nodes),
            "node_count_by_level": dict(sorted(tree_count_by_level.items())),
        },
        "top_nodes_by_knowledge_count": [
            {"node_id": node_id, "knowledge_count": count}
            for node_id, count in node_counter.most_common(25)
        ],
        "warnings": warnings,
        "gate_status": "pass" if not missing_sources and not confirmed_conflicts else "fail",
    }


def assert_condition(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate_mcp_and_search(
    items: list[dict[str, Any]],
    tree_nodes: list[dict[str, Any]],
    knowledge_items_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    search_module = load_module(
        "phase55_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    get_module = load_module(
        "phase55_get_knowledge_item",
        resolve_repo_path("codex-expert-kit", "mcp", "get_knowledge_item.py", start_file=__file__),
    )
    browse_module = load_module(
        "phase55_browse_knowledge_tree",
        resolve_repo_path("codex-expert-kit", "mcp", "browse_knowledge_tree.py", start_file=__file__),
    )

    first_reviewed = next((item for item in items if deep_get(item, "review.review_status") == "reviewed"), None)
    first_approved = next((item for item in items if deep_get(item, "review.review_status") == "approved"), None)
    assert_condition(errors, first_reviewed is not None, "未找到 reviewed 正式知识用于 MCP get 测试。")
    assert_condition(errors, first_approved is not None, "未找到 approved 正式知识用于 default guidance smoke test。")

    mcp_tests: dict[str, Any] = {
        "get_knowledge_item": None,
        "browse_knowledge_tree": None,
        "forbidden_permission": None,
        "default_guidance_filter": None,
    }
    if first_reviewed:
        response = get_module.get_knowledge_item(
            {"knowledge_id": first_reviewed.get("knowledge_id")},
            knowledge_items_path=str(knowledge_items_path),
        )
        item = response.get("item") or {}
        assert_condition(errors, response.get("status") == "ok", f"MCP get_knowledge_item 失败：{response.get('errors')}")
        assert_condition(errors, bool(item.get("source_evidence")), "MCP get_knowledge_item 未返回 source_evidence。")
        assert_condition(errors, deep_get(item, "machine_gate.default_guidance") == "caveat_only", "reviewed 知识 machine_gate 不是 caveat_only。")
        mcp_tests["get_knowledge_item"] = {
            "knowledge_id": first_reviewed.get("knowledge_id"),
            "status": response.get("status"),
            "source_count": len(item.get("source_evidence") or []),
            "machine_gate": deep_get(item, "machine_gate.default_guidance"),
        }

        denied = search_module.search_expert_knowledge(
            {
                "query": "permission smoke",
                "requested_permission": "write_knowledge",
                "top_k": 1,
            },
            knowledge_items_path=str(knowledge_items_path),
        )
        assert_condition(errors, denied.get("status") == "error", "MCP forbidden permission 未被阻断。")
        mcp_tests["forbidden_permission"] = {
            "status": denied.get("status"),
            "errors": denied.get("errors", []),
        }

        default_only = search_module.search_expert_knowledge(
            {
                "query": str(first_reviewed.get("knowledge_id")),
                "include": {"default_guidance_only": True, "reviewed": True, "draft": False},
                "top_k": 5,
            },
            knowledge_items_path=str(knowledge_items_path),
        )
        returned_ids = [result.get("knowledge_id") for result in default_only.get("results", [])]
        assert_condition(
            errors,
            first_reviewed.get("knowledge_id") not in returned_ids,
            "default_guidance_only 错误返回 reviewed/caveat_only 知识。",
        )
        mcp_tests["default_guidance_filter"] = {
            "reviewed_knowledge_id": first_reviewed.get("knowledge_id"),
            "returned_ids": returned_ids,
            "blocked_count": len(default_only.get("blocked_results", [])),
        }

    browse = browse_module.browse_knowledge_tree({"node_id": "kt", "include_children": True})
    assert_condition(errors, browse.get("status") in ("ok", "warning"), f"MCP browse_knowledge_tree 失败：{browse.get('errors')}")
    assert_condition(
        errors,
        len(browse.get("nodes", [])) >= max(1, len(tree_nodes) - 5),
        "MCP browse_knowledge_tree 返回节点数与 UI fixture 差异过大。",
    )
    mcp_tests["browse_knowledge_tree"] = {
        "status": browse.get("status"),
        "node_count": len(browse.get("nodes", [])),
        "ui_tree_node_count": len(tree_nodes),
    }

    search_cases: list[dict[str, Any]] = []
    for case in SEARCH_CASES:
        response = search_module.search_expert_knowledge(
            {
                "query": case["query"],
                "filters": case["filters"],
                "include": {"sources": True, "conflicts": True, "reviewed": True, "draft": False},
                "top_k": 5,
            },
            knowledge_items_path=str(knowledge_items_path),
        )
        results = response.get("results", [])
        ids = [result.get("knowledge_id") for result in results]
        source_counts = [result.get("source_count", 0) for result in results]
        assert_condition(errors, bool(results), f"SearchLab 等价检索无结果：{case['label']}")
        assert_condition(errors, all(count > 0 for count in source_counts), f"SearchLab 等价检索存在无来源结果：{case['label']}")
        assert_condition(
            errors,
            all(result.get("review_status") in ("reviewed", "approved") for result in results),
            f"SearchLab 等价检索返回非正式知识：{case['label']}",
        )
        search_cases.append(
            {
                "case_id": case["case_id"],
                "label": case["label"],
                "status": response.get("status"),
                "result_count": len(results),
                "top_ids": ids[:5],
                "source_counts": source_counts,
                "warnings": response.get("warnings", [])[:10],
            }
        )

    return (
        {"errors": errors, "warnings": warnings, "tests": mcp_tests},
        {"cases": search_cases},
        {"errors": errors, "warnings": warnings},
    )


def validate_vue_fixture(
    index_items: list[dict[str, Any]],
    ui_items: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    tree_nodes: list[dict[str, Any]],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    index_ids = {item.get("knowledge_id") for item in index_items}
    ui_ids = {item.get("knowledge_id") for item in ui_items}
    missing_in_ui = sorted(str(item) for item in index_ids - ui_ids if item)
    extra_in_ui = sorted(str(item) for item in ui_ids - index_ids if item)
    tree_ids = {str(item.get("node_id")) for item in tree_nodes if item.get("node_id")}

    node_count_mismatches = []
    for node in tree_nodes:
        node_id = str(node.get("node_id") or "")
        if not node_id:
            continue
        node_path = str(node.get("path") or "")
        expected = 0
        for item in index_items:
            item_path = str(deep_get(item, "metadata.canonical_tree_path", deep_get(item, "metadata.tree_path", "")) or "")
            if item_path == node_path or item_path.startswith(f"{node_path} / "):
                expected += 1
        actual = int(node.get("reviewed_item_count") or 0) + int(node.get("approved_item_count") or 0)
        if expected != actual:
            node_count_mismatches.append({"node_id": node_id, "tree_count": actual, "index_scope_count": expected})

    formalized_candidates = [
        item
        for item in candidates
        if deep_get(item, "workflow.queue_group") == "formalized"
        or item.get("review_status") in ("formalized_reviewed", "formalized_approved")
    ]
    formalized_without_link = [
        str(item.get("candidate_id"))
        for item in formalized_candidates
        if not deep_get(item, "workflow.formal_knowledge_id")
    ]

    assert_condition(errors, not missing_in_ui, f"UI formal fixture 缺少正式知识：{missing_in_ui[:20]}")
    assert_condition(errors, not extra_in_ui, f"UI formal fixture 存在额外知识：{extra_in_ui[:20]}")
    assert_condition(errors, not formalized_without_link, f"已沉淀候选缺少 formal_knowledge_id：{formalized_without_link[:20]}")
    if node_count_mismatches:
        warnings.append(
            "知识树节点统计与直接路径前缀复算存在差异；Phase 55 记录为观察项，"
            "阻断口径以 validate_knowledge_tree_alignment.py 为准。"
        )
    if "kt.ai_engineering" not in tree_ids:
        errors.append("知识树缺少 kt.ai_engineering 节点。")
    if "kt.trading_engineering" not in tree_ids:
        errors.append("知识树缺少 kt.trading_engineering 节点。")

    return {
        "formal_index_count": len(index_items),
        "ui_formal_count": len(ui_items),
        "candidate_count": len(candidates),
        "knowledge_tree_node_count": len(tree_nodes),
        "formalized_candidate_count": len(formalized_candidates),
        "missing_in_ui_count": len(missing_in_ui),
        "extra_in_ui_count": len(extra_in_ui),
        "formalized_without_link_count": len(formalized_without_link),
        "node_count_mismatch_count": len(node_count_mismatches),
        "node_count_mismatches": node_count_mismatches[:50],
        "errors": errors,
        "warnings": warnings,
    }


def validate_governance(items: list[dict[str, Any]]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    reviewed_default_enabled = []
    reviewed_hard_gate_enabled = []
    reviewed_approved_enabled = []
    approved_without_allow = []
    deny_or_missing_gate = []

    for item in items:
        knowledge_id = str(item.get("knowledge_id"))
        review_status = deep_get(item, "review.review_status")
        default_allowed = deep_get(item, "review.default_guidance_allowed")
        hard_gate_allowed = deep_get(item, "review.hard_gate_allowed")
        approved_allowed = deep_get(item, "review.approved_allowed")
        machine_gate = deep_get(item, "machine_gate.default_guidance")
        if review_status == "reviewed":
            if default_allowed is not False:
                reviewed_default_enabled.append(knowledge_id)
            if hard_gate_allowed is not False:
                reviewed_hard_gate_enabled.append(knowledge_id)
            if approved_allowed is not False:
                reviewed_approved_enabled.append(knowledge_id)
            if machine_gate != "caveat_only":
                deny_or_missing_gate.append(knowledge_id)
        if review_status == "approved" and machine_gate != "allow":
            approved_without_allow.append(knowledge_id)

    assert_condition(errors, not reviewed_default_enabled, f"reviewed 知识错误开启 default guidance：{reviewed_default_enabled[:20]}")
    assert_condition(errors, not reviewed_hard_gate_enabled, f"reviewed 知识错误开启 hard gate：{reviewed_hard_gate_enabled[:20]}")
    assert_condition(errors, not reviewed_approved_enabled, f"reviewed 知识错误开启 approved_allowed：{reviewed_approved_enabled[:20]}")
    assert_condition(errors, not deny_or_missing_gate, f"reviewed 知识 machine_gate 非 caveat_only：{deny_or_missing_gate[:20]}")
    assert_condition(errors, not approved_without_allow, f"approved 知识 machine_gate 非 allow：{approved_without_allow[:20]}")

    return {
        "reviewed_default_enabled_count": len(reviewed_default_enabled),
        "reviewed_hard_gate_enabled_count": len(reviewed_hard_gate_enabled),
        "reviewed_approved_enabled_count": len(reviewed_approved_enabled),
        "reviewed_non_caveat_gate_count": len(deny_or_missing_gate),
        "approved_without_allow_count": len(approved_without_allow),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    index_path = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
    formal_fixture_path = resolve_repo_path("ui", "public", "data", "formalKnowledgeItems.json", start_file=__file__)
    candidate_fixture_path = resolve_repo_path("ui", "public", "data", "phase23Candidates.json", start_file=__file__)
    tree_fixture_path = resolve_repo_path("ui", "public", "data", "knowledgeTreeNodes.json", start_file=__file__)

    index_payload = load_json(index_path)
    formal_payload = load_json(formal_fixture_path)
    candidate_payload = load_json(candidate_fixture_path)
    tree_payload = load_json(tree_fixture_path)

    items = index_payload.get("items", [])
    ui_items = formal_payload.get("items", [])
    candidates = candidate_payload.get("items", [])
    tree_nodes = tree_payload.get("items") or tree_payload.get("nodes") or []
    if not isinstance(items, list) or not isinstance(ui_items, list) or not isinstance(candidates, list) or not isinstance(tree_nodes, list):
        raise ValueError("Phase 55 inputs must expose list-shaped items.")

    baseline = collect_baseline(items, candidates, tree_nodes)
    write_json(resolve_repo_path(*BASELINE_REPORT, start_file=__file__), baseline)

    mcp_validation, search_validation, shared = validate_mcp_and_search(items, tree_nodes, index_path)
    vue_validation = validate_vue_fixture(items, ui_items, candidates, tree_nodes)
    governance_validation = validate_governance(items)
    errors = []
    warnings = []
    for section in (shared, vue_validation, governance_validation):
        errors.extend(section.get("errors", []))
        warnings.extend(section.get("warnings", []))
    errors.extend(mcp_validation.get("errors", []))
    warnings.extend(mcp_validation.get("warnings", []))

    runtime_report = {
        "report_id": "phase55_runtime_acceptance_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": "CEK-TA-536",
        "phase": PHASE,
        "baseline_report": "/".join(BASELINE_REPORT),
        "mcp_tests": mcp_validation.get("tests", {}),
        "searchlab_tests": search_validation,
        "vue_fixture_tests": vue_validation,
        "permission_tests": {
            "forbidden_permission": mcp_validation.get("tests", {}).get("forbidden_permission"),
            "default_guidance_filter": mcp_validation.get("tests", {}).get("default_guidance_filter"),
        },
        "governance_tests": governance_validation,
        "errors": errors,
        "warnings": sorted(set(warnings)),
        "gate_status": "pass" if baseline.get("gate_status") == "pass" and not errors else "fail",
        "boundary": "Phase 55 只做只读验收和基线统计；不升级 approved，不启用 default guidance 或 hard gate。",
    }
    write_json(resolve_repo_path(*RUNTIME_REPORT, start_file=__file__), runtime_report)
    print(json.dumps(runtime_report, ensure_ascii=False, indent=2))
    return 0 if runtime_report["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
