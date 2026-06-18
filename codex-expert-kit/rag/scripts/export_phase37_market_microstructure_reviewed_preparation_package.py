"""Export Phase 37 Market Microstructure reviewed/caveat_only package.

The Market Microstructure candidates have passed strict audit only as
``accepted_for_draft``. This script prepares the next external audit package
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
TASK_ID = "CEK-TA-407"
PACKAGE_ID = "phase37_market_microstructure_reviewed_preparation_audit_package_20260611"
PARTITION = "KB_03_MARKET_MICROSTRUCTURE"
FIRST_AUDIT_RESULT_ID = "audit_result_phase37_market_microstructure_candidate_audit_20260611_strict_v1"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_reviewed_preparation_gap_report.json", start_file=__file__
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
    return candidate_id(candidate).startswith("cand_20260611_phase37_market_microstructure_")


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
    if deep_get(candidate, ("review", "ai_audit", "audit_result_id")) != FIRST_AUDIT_RESULT_ID:
        gaps.append("review.ai_audit.audit_result_id_not_first_audit")
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
    if deep_get(candidate, ("conflict_audit", "conflict_status")) == "none_known_in_visible_context":
        warnings.append("formal_kb_full_conflict_check_required_before_reviewed_conversion")
    if deep_get(candidate, ("classification", "tree_node_id")) == "kt.market_microstructure.order_flow":
        warnings.append("order_flow_items_need_extra_attention_for_proxy_vs_fact_boundary")
    if deep_get(candidate, ("claim", "normalized_claim")) == "microstructure.thin_market_execution_risk.v1":
        warnings.append("verify_m11_downgrade_review_boundary_and_no_hard_gate")
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
            "sub_branch": "Market Microstructure",
            "candidate_count": len(packaged),
            "input_condition": "accepted_for_draft Market Microstructure candidates only; reviewed_allowed must currently be false.",
            "source_audit_result_ids": [FIRST_AUDIT_RESULT_ID],
        },
        "candidate_count": len(packaged),
        "audit_instruction": {
            "language": "zh-CN",
            "primary_goal": "严格判断这些 Market Microstructure 候选是否可以从 accepted_for_draft 进入 formal reviewed/caveat_only。",
            "must_search": "必须搜索相关专业网站、官方文档、监管资料、论文、交易所/API 文档、案例和数据，对审计包进行严格审计；不能只依赖候选包内摘要。",
            "must_check": [
                "来源是否足以支撑盘口深度、逐笔成交、aggressor side、订单流代理、CVD、funding/OI、流动性、市场影响、延迟、滑点和薄市场风险边界。",
                "供应商、交易所、平台或 API 文档是否被过度泛化为 universal market law。",
                "M11 是否已经从 hard gate/阻断语义改成降级/复核语义，且仍保持 hard_gate_allowed=false。",
                "是否清楚区分 Trading Engineering 市场微观结构规则本体与 AI Engineering 引用、训练、检索规则。",
                "是否存在和 Data Engineering、Replay、Backtest、Live Execution、Risk Management formal 知识的可见冲突、重复或分类错位。",
                "是否包含买卖点、仓位、杠杆、止损止盈参数、实盘执行或投资建议风险。",
            ],
            "focus_items": [
                {
                    "research_task_id": "P37-D-M04",
                    "focus": "reviewed 前重点核查 OFI/LOB imbalance proxy 与真实 order events 的边界是否足够。"
                },
                {
                    "research_task_id": "P37-D-M05",
                    "focus": "reviewed 前重点核查 CVD/Volume Delta 是否只作为数据源和采样规则下的订单流代理。"
                },
                {
                    "research_task_id": "P37-D-M07",
                    "focus": "reviewed 前重点核查 liquidity regime 标签是否为 CEK-TA 内部分类，不误称外部通用标准。"
                },
                {
                    "research_task_id": "P37-D-M11",
                    "focus": "确认 thin market item 不创建 hard gate，只允许降级为风险提示或要求外接风控复核。"
                },
            ],
            "allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "forbidden_decisions": ["approved", "default_guidance", "hard_gate", "trade_instruction"],
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_authorize_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_instruction_allowed": False,
            "reviewed_does_not_mean_approved": True,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议"],
        },
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase37_market_microstructure_reviewed_preparation_20260611_strict_v1",
            "package_id": PACKAGE_ID,
            "quality_gate": {"pass": "boolean", "reason": "string"},
            "summary": {
                "total": "integer",
                "accepted_for_reviewed_caveat_only": "integer",
                "needs_more_evidence": "integer",
                "rejected": "integer",
                "blocked": "integer",
            },
            "results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                    "reason": "string",
                }
            ],
        },
        "quality_gate": gate,
        "candidates": packaged,
    }


def main() -> None:
    candidates = load_scope_candidates()
    packaged_gaps = [candidate_gaps(candidate) for candidate in candidates]
    readiness_counter = Counter("ready" if not gaps else "blocked" for gaps in packaged_gaps)
    decision_counter = Counter(deep_get(candidate, ("status", "ingestion_decision"), "missing") for candidate in candidates)
    gap_counter = Counter(gap for gaps in packaged_gaps for gap in gaps)
    warnings_counter = Counter(w for candidate in candidates for w in candidate_warnings(candidate))
    errors: list[str] = []
    if len(candidates) != 12:
        errors.append(f"expected 12 Market Microstructure candidates, got {len(candidates)}")
    if readiness_counter.get("blocked", 0):
        errors.append(f"{readiness_counter['blocked']} candidates have reviewed-preparation gaps.")
    if decision_counter.get("accepted_for_draft", 0) != 12:
        errors.append("all candidates must be accepted_for_draft before reviewed preparation.")

    gate = {
        "pass": not errors,
        "errors": errors,
        "candidate_count": len(candidates),
        "readiness_counts": dict(readiness_counter),
        "decision_counts": dict(decision_counter),
        "gap_counts": dict(gap_counter),
        "warning_counts": dict(warnings_counter),
        "source_count_min": min((len(as_list(candidate.get("source_refs"))) for candidate in candidates), default=0),
        "source_count_max": max((len(as_list(candidate.get("source_refs"))) for candidate in candidates), default=0),
    }
    package = build_package(candidates, gate)
    report = {
        "report_id": "phase37_market_microstructure_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "quality_gate": gate,
        "audit_package": str(AUDIT_PATH),
        "next_step": "提交外部严格审计；审计通过后才能执行 CEK-TA-408 生成 formal reviewed/caveat_only。",
    }
    write_json(AUDIT_PATH, package)
    write_json(REPORT_PATH, report)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"candidate_count": len(candidates), "ready": readiness_counter.get("ready", 0)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
