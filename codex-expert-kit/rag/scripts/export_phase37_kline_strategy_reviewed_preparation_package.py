"""Export Phase 37 Kline / Strategy Engineering reviewed-preparation package.

The 12 Kline / Strategy Engineering candidates have passed candidate audit only
as ``accepted_for_draft``. This script prepares the next external audit package
that asks whether each candidate may become formal ``reviewed/caveat_only``.
It never creates formal knowledge and never enables approved, default guidance,
or hard-gate status.
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
TASK_ID = "CEK-TA-399"
PACKAGE_ID = "phase37_kline_strategy_reviewed_preparation_audit_package_20260611"
PARTITION = "KB_02_KLINE_STRATEGY"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_kline_strategy_reviewed_preparation_gap_report.json", start_file=__file__
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
    return candidate_id(candidate).startswith("cand_20260611_phase37_kline_strategy_")


def conversion_target(candidate: dict[str, Any]) -> dict[str, Any]:
    top_level = candidate.get("conversion_target")
    if isinstance(top_level, dict):
        return top_level
    workflow_target = deep_get(candidate, ("workflow", "conversion_target"), {})
    return workflow_target if isinstance(workflow_target, dict) else {}


def audit_patch_notes(candidate: dict[str, Any]) -> list[str]:
    audit = deep_get(candidate, ("review", "ai_audit"), {})
    notes = audit.get("patch_notes")
    if isinstance(notes, list):
        return [str(note) for note in notes]
    if isinstance(notes, dict):
        flattened: list[str] = []
        for key, value in notes.items():
            for item in as_list(value):
                flattened.append(f"{key}: {item}")
        return flattened
    return []


def candidate_gaps(candidate: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    target = conversion_target(candidate)
    conflict_status = deep_get(candidate, ("conflict_audit", "conflict_status"))
    if deep_get(candidate, ("status", "review_status")) != "accepted":
        gaps.append("status.review_status_not_accepted")
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        gaps.append("status.ingestion_decision_not_accepted_for_draft")
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        gaps.append("workflow.queue_group_not_ai_passed")
    if deep_get(candidate, ("review", "ai_audit", "decision")) != "accepted_for_draft":
        gaps.append("review.ai_audit.decision_not_accepted_for_draft")
    if deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is not False:
        gaps.append("input_already_reviewed_allowed_or_missing_boundary")
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        gaps.append("workflow.default_guidance_not_disabled")
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        gaps.append("workflow.hard_gate_not_disabled")
    if deep_get(candidate, ("workflow", "approved_allowed")) is not False:
        gaps.append("workflow.approved_not_disabled")
    if not target.get("proposed_knowledge_id"):
        gaps.append("conversion_target.proposed_knowledge_id_missing")
    if target.get("target_review_status") not in {"draft", "reviewed"}:
        gaps.append("conversion_target.target_review_status_not_draft")
    if len(as_list(candidate.get("source_refs"))) < 3:
        gaps.append("source_refs_less_than_3")
    if conflict_status not in {"none", "resolved", "none_known_in_visible_context", "visible_context_no_conflict"}:
        gaps.append("conflict_status_not_safe_for_reviewed_preparation")
    if not as_list(deep_get(candidate, ("applicability", "applies_when"), [])):
        gaps.append("applicability.applies_when_missing")
    if not as_list(deep_get(candidate, ("applicability", "not_applicable_when"), [])):
        gaps.append("applicability.not_applicable_when_missing")
    if deep_get(candidate, ("machine_gate", "default_guidance")) != "deny":
        gaps.append("machine_gate.default_guidance_not_denied")
    if deep_get(candidate, ("machine_gate", "approved_allowed")) is not False:
        gaps.append("machine_gate.approved_not_disabled")
    if deep_get(candidate, ("machine_gate", "default_guidance_allowed")) is not False:
        gaps.append("machine_gate.default_guidance_not_disabled")
    if deep_get(candidate, ("machine_gate", "hard_gate_allowed")) is not False:
        gaps.append("machine_gate.hard_gate_not_disabled")
    return gaps


def candidate_warnings(candidate: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    copyright_meta = candidate.get("copyright")
    if not isinstance(copyright_meta, dict):
        warnings.append("copyright_metadata_missing_but_candidate_stores_no_full_text")
    elif copyright_meta.get("stores_full_text") is not False or copyright_meta.get("stores_long_quote") is not False:
        warnings.append("copyright_metadata_requires_manual_check")
    if deep_get(candidate, ("conflict_audit", "conflict_status")) == "visible_context_no_conflict":
        warnings.append("formal_kb_full_conflict_check_required_before_reviewed_conversion")
    return warnings


def package_candidate(candidate: dict[str, Any], gaps: list[str], warnings: list[str]) -> dict[str, Any]:
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
        "conversion_target": conversion_target(candidate),
        "classification": candidate.get("classification", {}),
        "claim": candidate.get("claim", {}),
        "applicability": candidate.get("applicability", {}),
        "source_refs": candidate.get("source_refs", []),
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": candidate.get("conflict_audit", {}),
        "llm_usage_policy": candidate.get("llm_usage_policy", {}),
        "machine_gate": candidate.get("machine_gate", {}),
        "review": {
            "candidate_confidence": deep_get(candidate, ("review", "confidence")),
            "freshness": deep_get(candidate, ("review", "freshness")),
            "open_questions": as_list(deep_get(candidate, ("review", "open_questions"), [])),
            "ai_audit": audit,
        },
        "candidate_audit_patch_notes_to_verify": audit_patch_notes(candidate),
        "quality_gate": {
            "package_ready": not gaps,
            "gaps": gaps,
            "warnings": warnings,
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
    packaged = [
        package_candidate(candidate, candidate_gaps(candidate), candidate_warnings(candidate))
        for candidate in candidates
    ]
    return {
        "package_id": PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_caveat_only_preparation_audit",
        "scope": {
            "phase": "Phase 37",
            "branch": "Trading Engineering",
            "partition_id": PARTITION,
            "sub_branch": "Kline / Strategy Engineering",
            "candidate_count": len(packaged),
            "input_condition": "accepted_for_draft Kline / Strategy Engineering candidates only; reviewed_allowed must currently be false.",
            "source_audit_result_ids": [
                "audit_result_phase37_kline_strategy_candidate_audit_20260611_strict_v1",
                "audit_result_phase37_kline_strategy_supplemental_reaudit_20260611_strict_v1",
            ],
        },
        "candidate_count": len(packaged),
        "audit_instruction": {
            "language": "zh-CN",
            "primary_goal": (
                "严格判断这些 Kline / Strategy Engineering 候选是否可以从 accepted_for_draft "
                "进入 formal reviewed/caveat_only。"
            ),
            "must_search": (
                "必须搜索相关专业网站、官方文档、监管资料、论文、案例和数据，对审计包进行严格审计；"
                "不能只依赖候选包内摘要。"
            ),
            "must_check": [
                "来源是否足以支撑 K线结构、市场结构、入场信号、止损、止盈、多周期、指标滞后、ATR、RSI、成交量和策略版本 claim。",
                "候选是否把技术指标、图形结构、成交量确认或 ATR/RSI 等写成跨市场、跨周期、跨样本的普适有效信号。",
                "是否清楚区分 Trading Engineering 规则本体与 AI Engineering 的引用、训练、检索和审计规则。",
                "是否存在把回测框架、交易平台、供应商 schema 或单一交易所 API 泛化为所有交易项目通用规则的问题。",
                "是否存在和现有 CEK-TA formal knowledge 的可见冲突、重复或分类错位。",
                "是否包含买卖点、仓位、杠杆、具体止损止盈价格、实盘执行或投资建议风险。",
                "是否需要补充页码级书籍证据、论文、监管/交易所资料、数据供应商文档、交易引擎文档或 CEK-TA 内部契约。",
            ],
            "focus_items": [
                {"research_task_id": "P37-C-K01", "focus": "趋势结构只能作为上下文/假设描述，不得写成方向预测或买卖许可。"},
                {"research_task_id": "P37-C-K03", "focus": "入场信号必须与决策、风控、订单执行分离。"},
                {"research_task_id": "P37-C-K04", "focus": "止损规则必须保留 stop/stop-limit 触发、未成交和滑点边界。"},
                {"research_task_id": "P37-C-K05", "focus": "止盈可达性只表示成交质量假设披露，不是收益保证。"},
                {"research_task_id": "P37-C-K10", "focus": "成交量确认必须拆分数据字段语义和指标解释边界。"},
                {"research_task_id": "P37-C-K12", "focus": "策略规则版本必须写成复现/审计契约字段，不强制 MLflow/DVC/Git 为唯一实现。"},
            ],
            "hard_boundaries": [
                "candidate 不是正式知识。",
                "accepted_for_draft 不等于 reviewed。",
                "本次审计最多只能允许 formal reviewed/caveat_only。",
                "不得创建 approved。",
                "不得启用 default guidance。",
                "不得启用 hard gate。",
                "不得生成买卖点、仓位、杠杆、止损止盈价格或实盘执行建议。",
            ],
            "allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "required_output_schema": {
                "audit_result_id": "audit_result_phase37_kline_strategy_reviewed_preparation_20260611_strict_v1",
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
                        "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                        "confidence": "low | medium | medium_high | high",
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
    packaged_gaps = {candidate_id(candidate): candidate_gaps(candidate) for candidate in candidates}
    packaged_warnings = {candidate_id(candidate): candidate_warnings(candidate) for candidate in candidates}
    gap_counts = Counter(gap for gaps in packaged_gaps.values() for gap in gaps)
    warning_counts = Counter(warning for warnings in packaged_warnings.values() for warning in warnings)
    by_node = Counter(str(deep_get(candidate, ("classification", "canonical_node_id"), "")) for candidate in candidates)
    by_research = {str(candidate.get("research_task_id")): candidate_id(candidate) for candidate in candidates}
    gate = {
        "pass": len(candidates) == 12 and not any(packaged_gaps.values()),
        "candidate_count": len(candidates),
        "expected_candidate_count": 12,
        "ready_count": sum(1 for gaps in packaged_gaps.values() if not gaps),
        "blocked_count": sum(1 for gaps in packaged_gaps.values() if gaps),
        "gap_counts": dict(sorted(gap_counts.items())),
        "warning_counts": dict(sorted(warning_counts.items())),
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "boundary": "export only; no formal reviewed knowledge is created by this task.",
    }
    package = build_package(candidates, gate)
    report = {
        "report_id": "phase37_kline_strategy_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "by_canonical_node": dict(sorted(by_node.items())),
        "by_research_task": dict(sorted(by_research.items())),
        "quality_gate": gate,
        "audit_package": str(AUDIT_PATH),
        "boundary": "No formal reviewed/approved/default guidance/hard gate was created.",
    }
    write_json(AUDIT_PATH, package)
    write_json(REPORT_PATH, report)
    print(json.dumps({"package": str(AUDIT_PATH), "quality_gate": gate}, ensure_ascii=False))
    return 0 if gate["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
