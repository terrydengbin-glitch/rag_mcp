"""Validate full Phase 37 Trading Engineering runtime linkage.

This gate verifies the 96 Phase 37 Trading Engineering knowledge items after
all eight P0 groups have been materialized as formal reviewed/caveat_only
knowledge. It intentionally excludes earlier seed/approved knowledge in the
same partitions.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TASK_ID = "CEK-TA-450"
PHASE = "Phase 37"
EXPECTED_TOTAL = 96
EXPECTED_PARTITION_COUNTS = {
    "KB_01_QUANT_FOUNDATION": 12,
    "KB_02_DATA_ENGINEERING": 12,
    "KB_02_KLINE_STRATEGY": 12,
    "KB_03_MARKET_MICROSTRUCTURE": 12,
    "KB_04_BACKTEST": 12,
    "KB_05_REPLAY_SIMULATION": 12,
    "KB_06_LIVE_EXECUTION": 6,
    "KB_07_RISK_MANAGEMENT": 6,
    "KB_07_TRADE_ANALYSIS": 12,
}
EXPECTED_TREE_MARKERS = [
    "kt.quant_foundation",
    "kt.trading_engineering.data_engineering",
    "kt.kline_strategy",
    "kt.market_microstructure",
    "kt.backtest",
    "kt.replay_simulation",
    "kt.live_execution",
    "kt.risk_management",
    "kt.trade_analysis",
]
SEARCH_CASES = [
    ("quant_foundation", "KB_01_QUANT_FOUNDATION", "expected value cost adjusted expectancy R multiple position sizing"),
    ("data_engineering", "KB_02_DATA_ENGINEERING", "timestamp available time raw adjusted feature ready label ready"),
    ("kline_strategy", "KB_02_KLINE_STRATEGY", "K line signal boundary indicator strategy rule version"),
    ("market_microstructure", "KB_03_MARKET_MICROSTRUCTURE", "liquidity regime session halt auction rollover expiry"),
    ("backtest", "KB_04_BACKTEST", "lookahead bias out of sample walk forward reproducibility package"),
    ("replay_simulation", "KB_05_REPLAY_SIMULATION", "same bar TP SL fill model simulation live gap execution cost"),
    ("live_execution", "KB_06_LIVE_EXECUTION", "order state position reconciliation account broker live execution"),
    ("risk_management", "KB_07_RISK_MANAGEMENT", "portfolio exposure consecutive loss risk policy hard gate boundary"),
    ("trade_analysis", "KB_07_TRADE_ANALYSIS", "planned realized R MAE MFE reason code trade review hypothesis"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def partition_id(item: dict[str, Any]) -> str:
    return item.get("partition_id") or item.get("metadata", {}).get("partition_id", "")


def task_number(item: dict[str, Any]) -> int | None:
    task_id = str(item.get("metadata", {}).get("task_id", ""))
    if not task_id.startswith("CEK-TA-"):
        return None
    try:
        return int(task_id.split("-")[-1])
    except ValueError:
        return None


def is_phase37_item(item: dict[str, Any]) -> bool:
    if item.get("metadata", {}).get("phase") == PHASE:
        return True
    number = task_number(item)
    return number is not None and 189 <= number <= 449


def searchable_blob(item: dict[str, Any]) -> str:
    chunks = [
        item.get("knowledge_id", ""),
        item.get("title", ""),
        item.get("summary", ""),
        json.dumps(item.get("content", {}), ensure_ascii=False),
        json.dumps(item.get("metadata", {}), ensure_ascii=False),
        json.dumps(item.get("llm_usage_policy", {}), ensure_ascii=False),
    ]
    return " ".join(chunks).lower()


def main() -> int:
    root = resolve_repo_path(".", start_file=__file__)
    index_path = root / "codex-expert-kit" / "rag" / "indexes" / "knowledge_items.json"
    formal_fixture_path = root / "ui" / "src" / "data" / "formalKnowledgeItems.ts"
    candidate_fixture_path = root / "ui" / "src" / "data" / "phase23Candidates.ts"
    tree_fixture_path = root / "ui" / "src" / "data" / "knowledgeTreeNodes.ts"
    report_path = root / "docs" / "reports" / "phase37_full_runtime_linkage_report.json"

    index = load_json(index_path)
    items = [item for item in index.get("items", []) if is_phase37_item(item)]
    errors: list[str] = []

    ids = [item.get("knowledge_id", "") for item in items]
    duplicate_ids = sorted({knowledge_id for knowledge_id, count in Counter(ids).items() if count > 1})
    partition_counts = Counter(partition_id(item) for item in items)
    review_counts = Counter(item.get("review", {}).get("review_status") for item in items)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance") for item in items)
    missing_sources = [item.get("knowledge_id") for item in items if not item.get("source_evidence")]
    local_path_leaks = [
        item.get("knowledge_id")
        for item in items
        if "E:\\collector\\rag" in json.dumps(item, ensure_ascii=False)
        or "C:\\Users\\dove" in json.dumps(item, ensure_ascii=False)
    ]

    if len(items) != EXPECTED_TOTAL:
        errors.append(f"Phase 37 item count should be {EXPECTED_TOTAL}, got {len(items)}.")
    if duplicate_ids:
        errors.append(f"Duplicate Phase 37 knowledge ids: {duplicate_ids}.")
    for expected_partition, expected_count in EXPECTED_PARTITION_COUNTS.items():
        actual_count = partition_counts.get(expected_partition, 0)
        if actual_count != expected_count:
            errors.append(f"{expected_partition} should have {expected_count} Phase 37 items, got {actual_count}.")
    if dict(review_counts) != {"reviewed": EXPECTED_TOTAL}:
        errors.append(f"Phase 37 review status mismatch: {dict(review_counts)}.")
    if dict(gate_counts) != {"caveat_only": EXPECTED_TOTAL}:
        errors.append(f"Phase 37 machine gate mismatch: {dict(gate_counts)}.")
    if missing_sources:
        errors.append(f"Phase 37 items missing source_evidence: {missing_sources}.")
    if local_path_leaks:
        errors.append(f"Phase 37 formal items leak local paths: {local_path_leaks}.")

    forbidden_flag_hits: dict[str, list[str]] = {}
    for flag in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
        hits = []
        for item in items:
            review = item.get("review", {})
            gate = item.get("machine_gate", {})
            if review.get(flag) is True or gate.get(flag) is True:
                hits.append(item.get("knowledge_id", ""))
        if hits:
            forbidden_flag_hits[flag] = hits
    if forbidden_flag_hits:
        errors.append(f"Forbidden Phase 37 gate flags enabled: {forbidden_flag_hits}.")

    formal_fixture = read_text(formal_fixture_path)
    missing_from_formal_fixture = [knowledge_id for knowledge_id in ids if knowledge_id not in formal_fixture]
    if missing_from_formal_fixture:
        errors.append(f"Phase 37 ids missing from Vue formal fixture: {missing_from_formal_fixture}.")

    candidate_fixture = read_text(candidate_fixture_path)
    missing_candidate_links = [
        knowledge_id
        for knowledge_id in ids
        if knowledge_id not in candidate_fixture and knowledge_id.startswith("kb_07_trade_analysis.")
    ]
    if missing_candidate_links:
        errors.append(f"Trade Analysis formal ids missing from candidate back-link fixture: {missing_candidate_links}.")

    tree_fixture = read_text(tree_fixture_path)
    missing_tree_markers = [marker for marker in EXPECTED_TREE_MARKERS if marker not in tree_fixture]
    if missing_tree_markers:
        errors.append(f"Knowledge tree fixture missing Phase 37 markers: {missing_tree_markers}.")

    search_results = []
    for case_id, expected_partition, query in SEARCH_CASES:
        terms = [term.lower() for term in query.split()]
        hits = [
            item.get("knowledge_id", "")
            for item in items
            if partition_id(item) == expected_partition and any(term in searchable_blob(item) for term in terms)
        ]
        search_results.append({"case_id": case_id, "result_count": len(hits), "top_results": hits[:8]})
        if not hits:
            errors.append(f"Search case {case_id} returned no Phase 37 hits.")

    report = {
        "report_id": "phase37_full_runtime_linkage_report",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "task_id": TASK_ID,
        "expected_total": EXPECTED_TOTAL,
        "actual_total": len(items),
        "partition_counts": dict(sorted(partition_counts.items())),
        "expected_partition_counts": EXPECTED_PARTITION_COUNTS,
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "missing_sources_count": len(missing_sources),
        "forbidden_flag_hits": forbidden_flag_hits,
        "local_path_leak_count": len(local_path_leaks),
        "fixture_checks": {
            "formal_fixture_contains_all": not missing_from_formal_fixture,
            "candidate_fixture_trade_analysis_backlinks": not missing_candidate_links,
            "knowledge_tree_contains_phase37_markers": not missing_tree_markers,
        },
        "search_results": search_results,
        "errors": errors,
        "gate_status": "pass" if not errors else "fail",
        "boundary": "Phase 37 knowledge is formal reviewed/caveat_only only; approved/default guidance/hard gate/risk threshold advice remain disabled.",
    }
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
