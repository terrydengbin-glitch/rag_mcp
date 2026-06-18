"""Export Phase 37 Data Engineering reviewed/caveat_only audit package.

The Data Engineering candidates have passed strict audit only as
``accepted_for_draft``. This script prepares the next external audit package
that asks whether each candidate can be converted to formal
``reviewed/caveat_only`` knowledge. It never creates formal knowledge and never
enables approved, default guidance, or hard-gate status.
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


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-387"
PACKAGE_ID = "phase37_data_engineering_reviewed_preparation_audit_package_20260611"
PATCHED_AUDIT_RESULT_ID = "audit_result_phase37_data_engineering_candidate_audit_20260611_strict_v1_schema_patched"
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_02_DATA_ENGINEERING", start_file=__file__
)
AUDIT_PATH = resolve_repo_path(
    "docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_reviewed_preparation_gap_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def candidate_id(candidate: dict[str, Any]) -> str:
    return str(candidate.get("candidate_id", ""))


def is_scope_candidate(candidate: dict[str, Any]) -> bool:
    return candidate_id(candidate).startswith("cand_20260611_phase37_data_engineering_")


def audit_patch_notes(candidate: dict[str, Any]) -> list[str]:
    audit = deep_get(candidate, ("review", "ai_audit"), {})
    return [str(note) for note in as_list(audit.get("patch_notes"))]


def candidate_gaps(candidate: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    ai_audit = deep_get(candidate, ("review", "ai_audit"), {})
    if deep_get(candidate, ("status", "review_status")) != "accepted":
        gaps.append("status.review_status_not_accepted")
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        gaps.append("status.ingestion_decision_not_accepted_for_draft")
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        gaps.append("workflow.queue_group_not_ai_passed")
    if ai_audit.get("audit_result_id") != PATCHED_AUDIT_RESULT_ID:
        gaps.append("review.ai_audit.audit_result_id_not_schema_patched")
    if ai_audit.get("decision") != "accepted_for_draft":
        gaps.append("review.ai_audit.decision_not_accepted_for_draft")
    if ai_audit.get("confidence") not in {"low", "medium", "high"}:
        gaps.append("review.ai_audit.confidence_enum_invalid")
    if deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is not False:
        gaps.append("input_already_reviewed_allowed_or_missing_boundary")
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        gaps.append("workflow.default_guidance_not_disabled")
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        gaps.append("workflow.hard_gate_not_disabled")
    if deep_get(candidate, ("workflow", "approved_allowed")) is not False:
        gaps.append("workflow.approved_not_disabled")
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        gaps.append("conversion_target.proposed_knowledge_id_missing")
    if deep_get(candidate, ("conversion_target", "target_partition_id")) != "KB_02_DATA_ENGINEERING":
        gaps.append("conversion_target.target_partition_not_data_engineering")
    if len(as_list(candidate.get("source_refs"))) < 3:
        gaps.append("source_refs_less_than_3")
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {
        "none",
        "resolved",
        "none_known_in_visible_context",
    }:
        gaps.append("conflict_status_not_safe_for_reviewed_preparation")
    if not as_list(deep_get(candidate, ("applicability", "applies_when"), [])):
        gaps.append("applicability.applies_when_missing")
    if not as_list(deep_get(candidate, ("applicability", "not_applicable_when"), [])):
        gaps.append("applicability.not_applicable_when_missing")
    if deep_get(candidate, ("copyright", "stores_full_text"), False) is not False:
        gaps.append("copyright.stores_full_text_not_false")
    if deep_get(candidate, ("copyright", "stores_long_quote"), False) is not False:
        gaps.append("copyright.stores_long_quote_not_false")
    return gaps


def package_candidate(candidate: dict[str, Any], gaps: list[str]) -> dict[str, Any]:
    audit = deep_get(candidate, ("review", "ai_audit"), {})
    return {
        "candidate_id": candidate_id(candidate),
        "research_task_id": candidate.get("research_task_id"),
        "current_status": {
            "review_status": deep_get(candidate, ("status", "review_status")),
            "ingestion_decision": deep_get(candidate, ("status", "ingestion_decision")),
            "workflow_stage": deep_get(candidate, ("workflow", "stage")),
            "queue_group": deep_get(candidate, ("workflow", "queue_group")),
            "reviewed_allowed": deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")),
            "approved_allowed": deep_get(candidate, ("review", "ai_audit", "approved_allowed")),
            "default_guidance_allowed": deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed")),
            "hard_gate_allowed": deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed")),
        },
        "conversion_target": candidate.get("conversion_target", {}),
        "classification": candidate.get("classification", {}),
        "claim": candidate.get("claim", {}),
        "applicability": candidate.get("applicability", {}),
        "source_refs": candidate.get("source_refs", []),
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": candidate.get("conflict_audit", {}),
        "llm_usage_policy": candidate.get("llm_usage_policy", {}),
        "machine_gate": candidate.get("machine_gate", {}),
        "review": {
            "legacy_candidate_confidence": deep_get(candidate, ("review", "confidence")),
            "freshness": deep_get(candidate, ("review", "freshness")),
            "open_questions": as_list(deep_get(candidate, ("review", "open_questions"), [])),
            "ai_audit": audit,
        },
        "first_audit_patch_notes_to_verify": audit_patch_notes(candidate),
        "quality_gate": {
            "package_ready": not gaps,
            "gaps": gaps,
            "source_count": len(as_list(candidate.get("source_refs"))),
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status")),
        },
        "requested_audit_decision": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
            "blocked",
        ],
    }


def load_scope_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_DIR.glob("*.json")):
        candidate = read_json(path)
        if is_scope_candidate(candidate):
            candidates.append(candidate)
    return candidates


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    packaged = [package_candidate(candidate, candidate_gaps(candidate)) for candidate in candidates]
    return {
        "package_id": PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_caveat_only_preparation_audit",
        "scope": {
            "phase": "Phase 37",
            "branch": "Trading Engineering",
            "partition_id": "KB_02_DATA_ENGINEERING",
            "candidate_count": len(packaged),
            "input_condition": (
                "accepted_for_draft Data Engineering candidates only; "
                "reviewed_allowed must currently be false."
            ),
            "source_audit_result_id": PATCHED_AUDIT_RESULT_ID,
        },
        "audit_instruction": {
            "language": "zh-CN",
            "primary_goal": (
                "严格判断这些 Data Engineering 候选是否可以从 accepted_for_draft "
                "进入 formal reviewed/caveat_only。"
            ),
            "must_search": (
                "必须搜索相关的专业网站、资料、案例和数据，对审计报告进行严格审计；"
                "不能只依赖候选包内摘要。"
            ),
            "must_check": [
                "来源是否足以支撑数据工程 claim，尤其是时间戳、时区、缺失、重复、schema、版本、symbol、rollover、异常值、raw/adjusted 和质量报告边界。",
                "首轮审计 patch_notes 是否已足以进入 reviewed/caveat_only，还是必须先补来源或改写 claim。",
                "是否存在把供应商字段、框架功能或交易所单一规则泛化为所有交易项目通用规则的问题。",
                "是否清楚区分 Trading Engineering 数据规则本体与 AI Engineering 引用、训练、检索规则。",
                "是否存在和现有 CEK-TA formal knowledge 的可见冲突、重复或分类错位。",
                "是否包含买卖点、仓位、杠杆、止损止盈、实盘执行或投资建议风险。",
            ],
            "focus_items": [
                {
                    "research_task_id": "P37-B-D09",
                    "focus": "补查 continuous futures / roll methodology / raw-adjusted-back-adjusted 边界，避免只靠 corporate action 来源支撑换月。"
                },
                {
                    "research_task_id": "P37-B-D12",
                    "focus": "补查 Great Expectations Data Docs / Checkpoints、Deequ、Soda、dbt tests 或 CEK-TA data_quality_report schema。"
                },
                {
                    "research_task_id": "P37-B-D04",
                    "focus": "确认重复事件检测的主键、event_id、timestamp+symbol+venue 组合键、去重审计日志证据。"
                },
                {
                    "research_task_id": "P37-B-D10",
                    "focus": "确认异常值检测不能自动删除行情，只能进入 quarantine/review/repair 记录。"
                },
                {
                    "research_task_id": "P37-B-D11",
                    "focus": "确认 raw、adjusted、normalized、feature-store 层级和回测/训练引用边界。"
                }
            ],
            "hard_boundaries": [
                "candidate 不是正式知识。",
                "accepted_for_draft 不等于 reviewed。",
                "本次审计最多只能允许 formal reviewed/caveat_only。",
                "不得创建 approved。",
                "不得启用 default guidance。",
                "不得启用 hard gate。",
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            ],
            "allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "package_id": PACKAGE_ID,
                "audited_at": "YYYY-MM-DD",
                "quality_gate": {
                    "pass": "boolean",
                    "candidate_count": "integer",
                    "notes": "array<string>",
                },
                "decisions": [
                    {
                        "candidate_id": "string",
                        "research_task_id": "string",
                        "decision": (
                            "accepted_for_reviewed_caveat_only | "
                            "needs_more_evidence | rejected | blocked"
                        ),
                        "confidence": "low | medium | high",
                        "reviewed_allowed": "boolean",
                        "approved_allowed": False,
                        "default_guidance_allowed": False,
                        "hard_gate_allowed": False,
                        "reasons": "array<string>",
                        "required_patches": {
                            "source": "array<string>",
                            "content": "array<string>",
                            "boundary": "array<string>",
                            "conflict": "array<string>",
                        },
                        "required_extra_sources": "array<object>",
                        "formal_conversion_notes": "array<string>",
                    }
                ],
            },
        },
        "quality_gate": gate,
        "candidates": packaged,
    }


def main() -> int:
    candidates = load_scope_candidates()
    packaged_gaps = {candidate_id(c): candidate_gaps(c) for c in candidates}
    gap_counts = Counter(gap for gaps in packaged_gaps.values() for gap in gaps)
    by_node = Counter(str(deep_get(c, ("classification", "canonical_node_id"), "")) for c in candidates)
    by_research = {str(c.get("research_task_id")): candidate_id(c) for c in candidates}
    patch_notes_by_candidate = {
        candidate_id(c): audit_patch_notes(c)
        for c in candidates
        if audit_patch_notes(c)
    }
    gate = {
        "pass": len(candidates) == 12 and not any(packaged_gaps.values()),
        "expected_candidate_count": 12,
        "candidate_count": len(candidates),
        "ready_count": sum(1 for gaps in packaged_gaps.values() if not gaps),
        "blocked_count": sum(1 for gaps in packaged_gaps.values() if gaps),
        "gap_counts": dict(sorted(gap_counts.items())),
        "source_audit_result_id": PATCHED_AUDIT_RESULT_ID,
        "schema_patched_audit_used": True,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "export only; no formal reviewed knowledge is created by this task.",
    }
    package = build_package(candidates, gate)
    report = {
        "report_id": "phase37_data_engineering_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "audit_package": AUDIT_PATH.as_posix(),
        "candidate_count": len(candidates),
        "by_node": dict(sorted(by_node.items())),
        "by_research_task": dict(sorted(by_research.items())),
        "patch_notes_by_candidate": patch_notes_by_candidate,
        "quality_gate": gate,
        "next_action": (
            "将审计包交给外部 AI/人工严格审计；只有返回 "
            "accepted_for_reviewed_caveat_only 且 reviewed_allowed=true 的候选，"
            "才能进入后续 formal reviewed/caveat_only 转换。"
        ),
        "known_non_blocking_notes": [
            "候选 review.confidence 可能保留历史 medium_high 文案；本门禁只以 review.ai_audit.confidence 的 schema-patched low/medium/high 为准。",
            "首轮审计 patch_notes 必须在 reviewed-preparation 审计或 formal conversion 时逐条处理。",
            "本任务不创建正式知识，不重建 knowledge_items.json，不影响 MCP/SearchLab 默认正式知识索引。",
        ],
    }
    write_json(AUDIT_PATH, package)
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
