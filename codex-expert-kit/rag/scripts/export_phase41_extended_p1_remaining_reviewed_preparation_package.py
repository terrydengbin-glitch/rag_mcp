"""Export remaining Phase 41 P0-Extended/P1 candidates for reviewed-preparation reaudit.

This script is read-only. It exports the 13 Phase 41 P0-Extended/P1
candidates that are already accepted_for_draft but still have
reviewed_allowed=false, so an external reviewer can explicitly decide
whether Codex may later convert them into formal reviewed/caveat_only
knowledge. It never creates formal knowledge and never enables approved,
default guidance, or hard gate.
"""

from __future__ import annotations

import json
import re
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
TASK_ID = "CEK-TA-335"
PACKAGE_ID = "phase41_extended_p1_remaining_reviewed_preparation_audit_package_20260610"
REPORT_ID = "phase41_extended_p1_remaining_reviewed_preparation_gap_report"
EXPECTED_COUNT = 13
ALLOWED_PRIORITIES = {"P0-Extended", "P1"}

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
KNOWLEDGE_INDEX_PATH = resolve_repo_path(
    "codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", f"{REPORT_ID}.json", start_file=__file__)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_root() -> Path:
    return resolve_repo_path(start_file=__file__)


def repo_rel(path: Path) -> str:
    return path.relative_to(repo_root()).as_posix()


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


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def is_remaining_phase41_reviewed_gap(candidate: dict[str, Any], formal_ids: set[str]) -> bool:
    proposed_id = target_knowledge_id(candidate)
    return (
        str(candidate.get("research_task_id", "")).startswith("P41-")
        and str(candidate.get("candidate_id", "")).startswith("cand_20260610_phase41_p41_")
        and deep_get(candidate, ("phase41_trace", "priority")) in ALLOWED_PRIORITIES
        and deep_get(candidate, ("status", "review_status")) == "accepted"
        and deep_get(candidate, ("status", "ingestion_decision")) == "accepted_for_draft"
        and deep_get(candidate, ("workflow", "queue_group")) == "ai_passed"
        and deep_get(candidate, ("workflow", "stage")) == "ai_audited"
        and deep_get(candidate, ("workflow", "formal_review_status")) == "draft"
        and deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is False
        and deep_get(candidate, ("review", "ai_audit", "approved_allowed")) is False
        and deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed")) is False
        and deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed")) is False
        and bool(proposed_id)
        and proposed_id not in formal_ids
    )


def load_target_candidates(formal_ids: set[str]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_p41_*.json")):
        candidate = read_json(path)
        if not is_remaining_phase41_reviewed_gap(candidate, formal_ids):
            continue
        candidate["_audit_export_meta"] = {
            "source_file": repo_rel(path),
            "proposed_knowledge_id": target_knowledge_id(candidate),
            "formal_index_has_target": False,
            "current_reviewed_allowed": False,
            "current_queue_group": deep_get(candidate, ("workflow", "queue_group")),
            "current_stage": deep_get(candidate, ("workflow", "stage")),
            "current_formal_review_status": deep_get(candidate, ("workflow", "formal_review_status")),
            "required_next_decision": "外部审计必须显式给出 reviewed_allowed=true，后续 Codex 才能生成 formal reviewed/caveat_only；否则继续 needs_more_evidence 或 rejected。",
        }
        candidates.append(candidate)
    return candidates


def summarize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    sources = as_list(candidate.get("source_refs"))
    return {
        "candidate_id": str(candidate.get("candidate_id", "")),
        "research_task_id": str(candidate.get("research_task_id", "")),
        "priority": str(deep_get(candidate, ("phase41_trace", "priority"), "")),
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
        "current_approved_allowed": deep_get(candidate, ("review", "ai_audit", "approved_allowed")),
        "current_default_guidance_allowed": deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed")),
        "current_hard_gate_allowed": deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed")),
        "formal_index_has_target": False,
    }


def quality_gate(candidates: list[dict[str, Any]], formal_ids: set[str]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    seen_research_tasks: set[str] = set()
    for candidate in candidates:
        candidate_id = str(candidate.get("candidate_id", ""))
        research_task_id = str(candidate.get("research_task_id", ""))
        proposed_id = target_knowledge_id(candidate)
        sources = as_list(candidate.get("source_refs"))
        canonical_node_id = str(deep_get(candidate, ("classification", "canonical_node_id"), ""))
        priority = deep_get(candidate, ("phase41_trace", "priority"))
        conflict_status = deep_get(candidate, ("conflict_audit", "conflict_status"))
        if candidate_id in seen_ids:
            failures.append({"candidate_id": candidate_id, "failure": "duplicate_candidate_id"})
        seen_ids.add(candidate_id)
        if research_task_id in seen_research_tasks:
            failures.append({"candidate_id": candidate_id, "failure": "duplicate_research_task_id"})
        seen_research_tasks.add(research_task_id)
        if priority not in ALLOWED_PRIORITIES:
            failures.append({"candidate_id": candidate_id, "failure": "priority_not_extended_or_p1"})
        if not proposed_id:
            failures.append({"candidate_id": candidate_id, "failure": "missing_proposed_knowledge_id"})
        if proposed_id in formal_ids:
            failures.append({"candidate_id": candidate_id, "failure": "formal_index_already_has_target"})
        if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
            failures.append({"candidate_id": candidate_id, "failure": "queue_group_not_ai_passed"})
        if deep_get(candidate, ("workflow", "stage")) != "ai_audited":
            failures.append({"candidate_id": candidate_id, "failure": "workflow_stage_not_ai_audited"})
        if deep_get(candidate, ("workflow", "formal_review_status")) != "draft":
            failures.append({"candidate_id": candidate_id, "failure": "formal_review_status_not_draft"})
        if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
            failures.append({"candidate_id": candidate_id, "failure": "not_accepted_for_draft"})
        if deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "reviewed_allowed_not_false_before_reaudit"})
        if deep_get(candidate, ("review", "ai_audit", "approved_allowed")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "approved_allowed_not_false"})
        if deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_allowed_not_false"})
        if deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "hard_gate_allowed_not_false"})
        if not canonical_node_id.startswith("kt.ai_engineering."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if len(sources) < 3:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_3"})
        if conflict_status not in {"none", "resolved"}:
            failures.append({"candidate_id": candidate_id, "failure": "unsafe_conflict_status"})
        if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "stores_full_text_not_false"})
        if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
            failures.append({"candidate_id": candidate_id, "failure": "stores_long_quote_not_false"})
        if has_mojibake(candidate):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
    if len(candidates) != EXPECTED_COUNT:
        failures.append(
            {"candidate_id": "batch", "failure": f"expected_{EXPECTED_COUNT}_candidates_but_found_{len(candidates)}"}
        )
    return {
        "gate_id": "phase41_extended_p1_remaining_reviewed_preparation_quality_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": EXPECTED_COUNT,
        "checks": {
            "count_matches_expected": "pass" if len(candidates) == EXPECTED_COUNT else "fail",
            "priority_is_p0_extended_or_p1": "pass"
            if all(deep_get(item, ("phase41_trace", "priority")) in ALLOWED_PRIORITIES for item in candidates)
            else "fail",
            "queue_group_ai_passed": "pass"
            if all(deep_get(item, ("workflow", "queue_group")) == "ai_passed" for item in candidates)
            else "fail",
            "accepted_for_draft_only": "pass"
            if all(deep_get(item, ("status", "ingestion_decision")) == "accepted_for_draft" for item in candidates)
            else "fail",
            "reviewed_allowed_false_before_reaudit": "pass"
            if all(deep_get(item, ("review", "ai_audit", "reviewed_allowed")) is False for item in candidates)
            else "fail",
            "source_refs_min_3": "pass" if all(len(as_list(item.get("source_refs"))) >= 3 for item in candidates) else "fail",
            "conflict_status_safe": "pass"
            if all(deep_get(item, ("conflict_audit", "conflict_status")) in {"none", "resolved"} for item in candidates)
            else "fail",
            "canonical_nodes_under_ai_engineering": "pass"
            if all(
                str(deep_get(item, ("classification", "canonical_node_id"), "")).startswith("kt.ai_engineering.")
                for item in candidates
            )
            else "fail",
            "no_mojibake_marker": "pass" if all(not has_mojibake(item) for item in candidates) else "fail",
        },
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
    }


def build_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    summaries = [summarize_candidate(candidate) for candidate in candidates]
    node_counts = Counter(item["canonical_node_id"] for item in summaries)
    priority_counts = Counter(item["priority"] for item in summaries)
    source_count_distribution = Counter(str(item["source_count"]) for item in summaries)
    return {
        "report_id": REPORT_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "phase": "41",
        "scope": "Phase 41 P0-Extended/P1 remaining ai_passed candidates that still need reviewed permission",
        "conclusion": "13 条候选已 accepted_for_draft，但 reviewed_allowed=false，必须外部审计明确 reviewed_allowed=true 后才可沉淀 formal reviewed/caveat_only。",
        "candidate_count": len(candidates),
        "quality_gate": gate,
        "priority_counts": dict(sorted(priority_counts.items())),
        "node_counts": dict(sorted(node_counts.items())),
        "source_count_distribution": dict(sorted(source_count_distribution.items())),
        "candidate_summaries": summaries,
        "hard_boundaries": [
            "本报告不把 candidate 转为 formal reviewed。",
            "accepted_for_draft 不等于 reviewed。",
            "reviewed_allowed=false 时不得生成 formal reviewed knowledge item。",
            "reviewed 也不是 approved。",
            "approved、default guidance 和 hard gate 仍需独立人工治理任务。",
            "本轮再审计只解决是否允许 formal reviewed/caveat_only，不解决 approved。",
            "Trading PnL、fill、slippage、fee、K 线和执行延迟本体继续归 Trading Engineering。",
        ],
        "next_step": "等待外部审计返回 reviewed_allowed=true / needs_more_evidence / rejected 后，再由 Codex 按 Phase 32 工作流回写和沉淀。",
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_reviewed_preparation_reaudit_package",
        "generated_at": TODAY,
        "phase": "41",
        "task_id": TASK_ID,
        "title": "Phase 41 P0-Extended/P1 剩余 13 条候选 reviewed preparation 再审计包",
        "purpose": "审计 13 条已 accepted_for_draft 但 reviewed_allowed=false 的 Phase 41 P0-Extended/P1 候选，判断是否可由 Codex 后续转换为 formal reviewed/caveat_only 知识。",
        "quality_gate": gate,
        "candidate_count": len(candidates),
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
        "reviewed_preparation_rules": [
            "若允许后续转 formal reviewed，必须 decision=accepted_for_draft 且 reviewed_allowed=true。",
            "若仍需补证，必须 decision=needs_more_evidence 且 reviewed_allowed=false。",
            "若候选过宽、错分、证据不足或污染知识库，必须 decision=rejected 且 reviewed_allowed=false。",
            "approved_allowed、default_guidance_allowed、hard_gate_allowed 必须始终为 false。",
            "reviewed 只允许 machine_gate.default_guidance=caveat_only，不允许 allow。",
            "source_patch_notes、content_patch_notes、boundary_patch_notes 和 conflict_patch_notes 必须写出可回写的具体修改点。",
        ],
        "auditor_focus": [
            "来源是否足以支持具体 claim，而不是只支持泛泛工程概念。",
            "P0-Extended/P1 是否仍是增强项，没有被写成外接项目默认依赖。",
            "是否清楚区分 scorer、calibrator、Qwen3 audit assistant、RAG、platform 和 deterministic final gate 的责任。",
            "是否错误收录 K 线、fill model、实盘风控或交易执行本体。",
            "是否有适用范围、不适用场景、冲突状态、freshness 和 fallback/rollback 边界。",
            "是否存在无来源默认指导、未消解冲突、过期依赖、私有业务字段或中文乱码。",
        ],
        "hard_boundaries": [
            "本包不能直接创建 formal reviewed。",
            "本包不能创建 approved。",
            "本包不能启用 default guidance。",
            "本包不能启用 hard gate。",
            "Qwen3 只做审计助手，不做 numeric scorer、final gate 或事实来源。",
            "表格/统计模型只做 scorer、risk ranking 或 review priority，不直接执行交易。",
            "deterministic final gate 仍由独立交易风控/审批契约控制。",
            "Trading Engineering 本体不得混入 AI Engineering 知识项。",
        ],
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase41_extended_p1_remaining_reviewed_preparation_20260610_strict_v1",
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
                    "source_patch_notes": ["string"],
                    "content_patch_notes": ["string"],
                    "boundary_patch_notes": ["string"],
                    "conflict_patch_notes": ["string"],
                    "required_followups": ["string"],
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
    gate = quality_gate(candidates, formal_ids)
    write_json(REPORT_PATH, build_report(candidates, gate))
    write_json(AUDIT_PACKAGE_PATH, build_package(candidates, gate))
    print(
        json.dumps(
            {
                "package": repo_rel(AUDIT_PACKAGE_PATH),
                "report": repo_rel(REPORT_PATH),
                "gate_status": gate["gate_status"],
                "candidate_count": len(candidates),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
