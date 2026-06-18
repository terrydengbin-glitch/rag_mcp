"""Validate Phase 37 Trade Analysis runtime linkage.

This gate proves that the 12 Trade Analysis formal reviewed/caveat_only items
are reachable from the official formal index and Vue fixtures, and that they
remain blocked from approved/default guidance/hard gate/risk-threshold advice.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TASK_ID = "CEK-TA-449"
TODAY = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
PARTITION_ID = "KB_07_TRADE_ANALYSIS"
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_trade_analysis_runtime_linkage_report.json", start_file=__file__)
INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
FORMAL_FIXTURE_PATH = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
CANDIDATE_FIXTURE_PATH = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
TREE_FIXTURE_PATH = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)

EXPECTED_IDS = [
    "kb_07_trade_analysis.planned_vs_realized_r_required.v1",
    "kb_07_trade_analysis.mae_mfe_for_post_trade_only.v1",
    "kb_07_trade_analysis.bad_trade_taxonomy_required.v1",
    "kb_07_trade_analysis.good_loss_bad_win_distinction.v1",
    "kb_07_trade_analysis.entry_quality_review_required.v1",
    "kb_07_trade_analysis.exit_quality_review_required.v1",
    "kb_07_trade_analysis.risk_quality_review_required.v1",
    "kb_07_trade_analysis.execution_quality_review_required.v1",
    "kb_07_trade_analysis.rule_compliance_review_required.v1",
    "kb_07_trade_analysis.regime_fit_review_required.v1",
    "kb_07_trade_analysis.reason_code_required.v1",
    "kb_07_trade_analysis.research_hypothesis_requires_validation.v1",
]

SEARCH_CASES = [
    {
        "case_id": "trade_analysis_r_decomposition",
        "query": "planned realized R trade review risk reward actual net pnl",
        "min_results": 2,
    },
    {
        "case_id": "trade_analysis_mae_mfe",
        "query": "MAE MFE post trade price path evidence review",
        "min_results": 1,
    },
    {
        "case_id": "trade_analysis_reason_taxonomy",
        "query": "reason code taxonomy bad trade good loss bad win rule compliance",
        "min_results": 4,
    },
    {
        "case_id": "trade_analysis_hypothesis",
        "query": "research hypothesis lifecycle validation out of sample cost regime",
        "min_results": 1,
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def assert_condition(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def tokenize(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z0-9_./-]+", text)}


def item_text(item: dict[str, Any]) -> str:
    parts = [
        str(item.get("knowledge_id", "")),
        str(item.get("title", "")),
        str(item.get("metadata", {}).get("canonical_node_id", "")),
        str(item.get("content", {}).get("statement", "")),
        str(item.get("content", {}).get("rationale", "")),
        " ".join(item.get("content", {}).get("risk_notes", [])),
        " ".join(item.get("llm_usage_policy", {}).get("allowed", [])),
        " ".join(item.get("llm_usage_policy", {}).get("not_allowed", [])),
    ]
    return " ".join(parts)


def search_items(items: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    query_tokens = tokenize(query)
    scored: list[tuple[int, dict[str, Any]]] = []
    for item in items:
        tokens = tokenize(item_text(item))
        score = len(query_tokens & tokens)
        if score > 0:
            scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda pair: (-pair[0], str(pair[1].get("knowledge_id", ""))))]


def main() -> int:
    errors: list[str] = []
    index = load_json(INDEX_PATH)
    all_items = index.get("items", []) if isinstance(index, dict) else []
    scoped = [item for item in all_items if item.get("knowledge_id") in set(EXPECTED_IDS)]
    ids = {item.get("knowledge_id") for item in scoped}
    missing = sorted(set(EXPECTED_IDS) - ids)
    extra = sorted(ids - set(EXPECTED_IDS))
    review_counts = Counter(item.get("review", {}).get("review_status", "") for item in scoped)
    gate_counts = Counter(item.get("machine_gate", {}).get("default_guidance", "") for item in scoped)
    partition_counts = Counter(item.get("metadata", {}).get("partition_id", "") for item in scoped)
    source_missing = [item.get("knowledge_id") for item in scoped if not item.get("source_evidence")]
    internal_contract_missing = [
        item.get("knowledge_id")
        for item in scoped
        if not any(source.get("source_type") == "internal_contract" for source in item.get("source_evidence", []))
    ]
    unsafe = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("review", {}).get("approved_allowed") is not False
        or item.get("review", {}).get("default_guidance_allowed") is not False
        or item.get("review", {}).get("hard_gate_allowed") is not False
        or item.get("review", {}).get("risk_threshold_advice_allowed") is not False
        or item.get("machine_gate", {}).get("approved_allowed") is not False
        or item.get("machine_gate", {}).get("default_guidance_allowed") is not False
        or item.get("machine_gate", {}).get("hard_gate_allowed") is not False
        or item.get("machine_gate", {}).get("risk_threshold_advice_allowed") is not False
    ]
    local_path_leaks = [
        item.get("knowledge_id")
        for item in scoped
        if "E:\\collector\\rag" in json.dumps(item, ensure_ascii=False)
        or "C:\\Users\\dove" in json.dumps(item, ensure_ascii=False)
    ]

    assert_condition(errors, len(scoped) == 12, f"Trade Analysis scoped count should be 12, got {len(scoped)}")
    assert_condition(errors, not missing, f"missing ids: {missing}")
    assert_condition(errors, not extra, f"unexpected ids: {extra}")
    assert_condition(errors, dict(review_counts) == {"reviewed": 12}, f"review status mismatch: {dict(review_counts)}")
    assert_condition(errors, dict(gate_counts) == {"caveat_only": 12}, f"machine gate mismatch: {dict(gate_counts)}")
    assert_condition(errors, dict(partition_counts) == {PARTITION_ID: 12}, f"partition mismatch: {dict(partition_counts)}")
    assert_condition(errors, not source_missing, f"missing source_evidence: {source_missing}")
    assert_condition(errors, not internal_contract_missing, f"missing internal contract source: {internal_contract_missing}")
    assert_condition(errors, not unsafe, f"unsafe guidance/gate flags: {unsafe}")
    assert_condition(errors, not local_path_leaks, f"local absolute path leaks: {local_path_leaks}")

    formal_text = FORMAL_FIXTURE_PATH.read_text(encoding="utf-8")
    candidate_text = CANDIDATE_FIXTURE_PATH.read_text(encoding="utf-8")
    tree_text = TREE_FIXTURE_PATH.read_text(encoding="utf-8")
    missing_formal_fixture = [knowledge_id for knowledge_id in EXPECTED_IDS if knowledge_id not in formal_text]
    missing_candidate_links = [knowledge_id for knowledge_id in EXPECTED_IDS if knowledge_id not in candidate_text]
    assert_condition(errors, not missing_formal_fixture, f"formal fixture missing ids: {missing_formal_fixture}")
    assert_condition(errors, not missing_candidate_links, f"candidate fixture missing formal links: {missing_candidate_links}")
    assert_condition(errors, "kt.trade_analysis" in tree_text, "knowledge tree fixture missing kt.trade_analysis")

    search_results: list[dict[str, Any]] = []
    for case in SEARCH_CASES:
        hits = search_items(scoped, case["query"])
        assert_condition(
            errors,
            len(hits) >= case["min_results"],
            f"{case['case_id']} should return at least {case['min_results']} scoped results, got {len(hits)}",
        )
        search_results.append(
            {
                "case_id": case["case_id"],
                "result_count": len(hits),
                "top_results": [item.get("knowledge_id") for item in hits[:5]],
            }
        )

    default_guidance_blocked = [
        item.get("knowledge_id")
        for item in scoped
        if item.get("machine_gate", {}).get("default_guidance") == "caveat_only"
        and item.get("review", {}).get("default_guidance_allowed") is False
    ]
    assert_condition(errors, len(default_guidance_blocked) == 12, "default guidance blocking should cover all 12 items")

    report = {
        "report_id": "phase37_trade_analysis_runtime_linkage_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "partition_id": PARTITION_ID,
        "expected_count": 12,
        "actual_count": len(scoped),
        "gate_status": "pass" if not errors else "fail",
        "errors": errors,
        "review_counts": dict(review_counts),
        "machine_gate_counts": dict(gate_counts),
        "partition_counts": dict(partition_counts),
        "default_guidance_blocked_count": len(default_guidance_blocked),
        "search_results": search_results,
        "fixture_checks": {
            "formal_fixture_contains_all": not missing_formal_fixture,
            "candidate_fixture_contains_formal_links": not missing_candidate_links,
            "knowledge_tree_contains_trade_analysis": "kt.trade_analysis" in tree_text,
        },
        "boundary": "All Trade Analysis items are formal reviewed/caveat_only only; approved/default guidance/hard gate/risk threshold advice remain disabled.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
