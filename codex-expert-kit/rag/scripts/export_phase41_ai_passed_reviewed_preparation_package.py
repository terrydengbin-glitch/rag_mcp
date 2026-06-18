"""Export Phase 41 ai_passed candidates for reviewed-preparation audit.

This script is read-only. It exports Phase 41 candidates that are
accepted_for_draft but still have reviewed_allowed=false, so an external
reviewer can explicitly decide whether Codex may convert them into formal
reviewed knowledge later.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-326"
PACKAGE_ID = "phase41_ai_passed_reviewed_preparation_audit_package_20260610"
EXPECTED_COUNT = 22

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
KNOWLEDGE_INDEX_PATH = resolve_repo_path(
    "codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase41_ai_passed_reviewed_preparation_gap_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def load_formal_ids() -> set[str]:
    payload = read_json(KNOWLEDGE_INDEX_PATH)
    items = payload.get("items")
    if not isinstance(items, list):
        raise ValueError(f"{KNOWLEDGE_INDEX_PATH} must contain an items list")
    return {str(item.get("knowledge_id")) for item in items if isinstance(item, dict) and item.get("knowledge_id")}


def target_knowledge_id(candidate: dict[str, Any]) -> str:
    return str(
        deep_get(candidate, ("workflow", "formal_knowledge_id"))
        or deep_get(candidate, ("conversion_target", "proposed_knowledge_id"))
        or ""
    )


def is_phase41_ai_passed_gap(candidate: dict[str, Any], formal_ids: set[str]) -> bool:
    if not str(candidate.get("research_task_id", "")).startswith("P41-"):
        return False
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        return False
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return False
    if deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is not False:
        return False
    proposed_id = target_knowledge_id(candidate)
    return bool(proposed_id) and proposed_id not in formal_ids


def load_target_candidates(formal_ids: set[str]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_p41_*.json")):
        candidate = read_json(path)
        if is_phase41_ai_passed_gap(candidate, formal_ids):
            candidate["_audit_export_meta"] = {
                "source_file": repo_rel(path),
                "proposed_knowledge_id": target_knowledge_id(candidate),
                "formal_index_has_target": False,
                "current_reviewed_allowed": False,
                "current_queue_group": deep_get(candidate, ("workflow", "queue_group")),
                "current_ingestion_decision": deep_get(candidate, ("status", "ingestion_decision")),
                "required_next_decision": "外部审计必须显式给出 reviewed_allowed=true，后续 Codex 才能生成 formal reviewed；否则继续 needs_more_evidence 或 rejected。",
            }
            candidates.append(candidate)
    return candidates


def summarize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    sources = as_list(candidate.get("source_refs"))
    return {
        "candidate_id": str(candidate.get("candidate_id", "")),
        "research_task_id": str(candidate.get("research_task_id", "")),
        "statement": str(deep_get(candidate, ("claim", "statement"), "")),
        "canonical_node_id": str(deep_get(candidate, ("classification", "canonical_node_id"), "")),
        "proposed_knowledge_id": target_knowledge_id(candidate),
        "source_count": len(sources),
        "source_types": sorted(
            {
                str(source.get("source_type"))
                for source in sources
                if isinstance(source, dict) and source.get("source_type")
            }
        ),
        "conflict_status": str(deep_get(candidate, ("conflict_audit", "conflict_status"), "")),
        "current_reviewed_allowed": deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")),
        "current_default_guidance_allowed": deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed")),
        "current_hard_gate_allowed": deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed")),
        "formal_index_has_target": False,
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        proposed_id = target_knowledge_id(candidate)
        sources = as_list(candidate.get("source_refs"))
        canonical_node_id = str(deep_get(candidate, ("classification", "canonical_node_id"), ""))
        reviewed_allowed = deep_get(candidate, ("review", "ai_audit", "reviewed_allowed"))
        approved_allowed = deep_get(candidate, ("review", "ai_audit", "approved_allowed"))
        default_guidance_allowed = deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed"))
        hard_gate_allowed = deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed"))
        conflict_status = deep_get(candidate, ("conflict_audit", "conflict_status"))
        if candidate_id in seen_ids:
            failures.append({"candidate_id": candidate_id, "failure": "duplicate_candidate_id"})
        seen_ids.add(candidate_id)
        if not proposed_id:
            failures.append({"candidate_id": candidate_id, "failure": "missing_proposed_knowledge_id"})
        if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
            failures.append({"candidate_id": candidate_id, "failure": "queue_group_not_ai_passed"})
        if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
            failures.append({"candidate_id": candidate_id, "failure": "not_accepted_for_draft"})
        if reviewed_allowed is not False:
            failures.append({"candidate_id": candidate_id, "failure": "reviewed_allowed_not_false_before_reaudit"})
        if approved_allowed is not False:
            failures.append({"candidate_id": candidate_id, "failure": "approved_allowed_not_false"})
        if default_guidance_allowed is not False:
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_allowed_not_false"})
        if hard_gate_allowed is not False:
            failures.append({"candidate_id": candidate_id, "failure": "hard_gate_allowed_not_false"})
        if not canonical_node_id.startswith("kt.ai_engineering."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if len(sources) < 2:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_2"})
        if conflict_status not in {"none", "resolved"}:
            failures.append({"candidate_id": candidate_id, "failure": "unsafe_conflict_status"})
        if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "stores_full_text_not_false"})
        if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "stores_long_quote_not_false"})
    if len(candidates) != EXPECTED_COUNT:
        failures.append({"candidate_id": "batch", "failure": f"expected_{EXPECTED_COUNT}_candidates_but_found_{len(candidates)}"})
    return {
        "gate_id": "phase41_ai_passed_reviewed_preparation_quality_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": EXPECTED_COUNT,
        "checks": {
            "count_matches_expected": "pass" if len(candidates) == EXPECTED_COUNT else "fail",
            "queue_group_ai_passed": "pass"
            if all(deep_get(item, ("workflow", "queue_group")) == "ai_passed" for item in candidates)
            else "fail",
            "accepted_for_draft_only": "pass"
            if all(deep_get(item, ("status", "ingestion_decision")) == "accepted_for_draft" for item in candidates)
            else "fail",
            "reviewed_allowed_false_before_reaudit": "pass"
            if all(deep_get(item, ("review", "ai_audit", "reviewed_allowed")) is False for item in candidates)
            else "fail",
            "source_refs_min_2": "pass" if all(len(as_list(item.get("source_refs"))) >= 2 for item in candidates) else "fail",
            "conflict_status_safe": "pass"
            if all(deep_get(item, ("conflict_audit", "conflict_status")) in {"none", "resolved"} for item in candidates)
            else "fail",
            "canonical_nodes_under_ai_engineering": "pass"
            if all(
                str(deep_get(item, ("classification", "canonical_node_id"), "")).startswith("kt.ai_engineering.")
                for item in candidates
            )
            else "fail",
        },
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
    }


def build_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    summaries = [summarize_candidate(candidate) for candidate in candidates]
    node_counts = Counter(item["canonical_node_id"] for item in summaries)
    source_count_distribution = Counter(str(item["source_count"]) for item in summaries)
    return {
        "report_id": "phase41_ai_passed_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "phase": "41",
        "scope": "Phase 41 ai_passed candidates with proposed formal knowledge id missing from formal index",
        "conclusion": "22 条候选已 accepted_for_draft，但 reviewed_allowed=false，必须外部审计明确 reviewed_allowed=true 后才可沉淀 formal reviewed。",
        "candidate_count": len(candidates),
        "quality_gate": gate,
        "node_counts": dict(sorted(node_counts.items())),
        "source_count_distribution": dict(sorted(source_count_distribution.items())),
        "candidate_summaries": summaries,
        "hard_boundaries": [
            "本报告不把 candidate 转为 formal reviewed。",
            "accepted_for_draft 不等于 reviewed。",
            "reviewed_allowed=false 时不得生成 formal reviewed knowledge item。",
            "reviewed 也不是 approved。",
            "approved、default guidance 和 hard gate 仍需独立人工治理任务。",
            "不得把 Qwen3 recommendation、raw scorer score 或未校准概率写入 final gate 作为最终动作。",
            "Trading PnL、fill、slippage、fee、K 线和执行延迟本体继续归 Trading Engineering。",
        ],
        "next_step": "等待外部审计返回 reviewed_allowed=true / needs_more_evidence / rejected 后，再由 Codex 按 Phase 32 工作流回写和沉淀。",
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_reviewed_preparation_audit_package",
        "generated_at": TODAY,
        "phase": "41",
        "task_id": TASK_ID,
        "title": "Phase 41 ai_passed 候选 reviewed preparation 审计包",
        "purpose": "审计 22 条已 accepted_for_draft 但 reviewed_allowed=false 的 Phase 41 候选，判断是否可由 Codex 后续转换为 formal reviewed 知识。",
        "quality_gate": gate,
        "candidate_count": len(candidates),
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
        "reviewed_preparation_rules": [
            "若允许后续转 formal reviewed，必须 decision=accepted_for_draft 且 reviewed_allowed=true。",
            "若仍需补证，必须 decision=needs_more_evidence 且 reviewed_allowed=false。",
            "若候选过宽、错分或污染知识库，必须 decision=rejected 且 reviewed_allowed=false。",
            "approved_allowed、default_guidance_allowed、hard_gate_allowed 必须始终为 false。",
            "reviewed 只允许 caveat_only machine_gate，不允许 allow。",
        ],
        "hard_boundaries": [
            "本包不能直接创建 formal reviewed。",
            "本包不能创建 approved。",
            "本包不能启用 default guidance。",
            "本包不能启用 hard gate。",
            "Qwen3 只做审计助手，不做 numeric scorer、final gate 或事实来源。",
            "deterministic final gate 仍由独立交易风控/审批契约控制。",
            "Trading Engineering 本体不得混入 AI Engineering 知识项。",
        ],
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase41_ai_passed_reviewed_preparation_20260610_strict_v1",
            "source_package_id": PACKAGE_ID,
            "decisions": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reason": "string",
                    "source_patch_notes": [],
                    "content_patch_notes": [],
                    "boundary_patch_notes": [],
                    "conflict_patch_notes": [],
                    "required_followups": [],
                }
            ],
            "batch_summary": {
                "accepted_for_reviewed_count": 0,
                "needs_more_evidence_count": 0,
                "rejected_count": 0,
                "reviewed_allowed_count": 0,
                "approved_allowed_count": 0,
                "default_guidance_allowed_count": 0,
                "hard_gate_allowed_count": 0,
            },
        },
        "candidates": candidates,
    }


def main() -> int:
    formal_ids = load_formal_ids()
    candidates = load_target_candidates(formal_ids)
    gate = quality_gate(candidates)
    report = build_report(candidates, gate)
    package = build_package(candidates, gate)
    write_json(REPORT_PATH, report)
    write_json(AUDIT_PACKAGE_PATH, package)
    print(json.dumps({"package": repo_rel(AUDIT_PACKAGE_PATH), "report": repo_rel(REPORT_PATH), "gate_status": gate["gate_status"], "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
