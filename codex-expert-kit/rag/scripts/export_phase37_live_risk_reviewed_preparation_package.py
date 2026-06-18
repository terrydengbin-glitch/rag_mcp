"""Export Phase 37 Live Execution / Risk Management reviewed/caveat audit package."""

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


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-438"
PACKAGE_ID = "phase37_live_risk_reviewed_preparation_audit_package_20260612"
FIRST_AUDIT_RESULT_ID = "audit_result_phase37_live_risk_candidate_audit_20260612_strict_v1"
LIVE_PARTITION = "KB_06_LIVE_EXECUTION"
RISK_PARTITION = "KB_07_RISK_MANAGEMENT"

LIVE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", LIVE_PARTITION, start_file=__file__)
RISK_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", RISK_PARTITION, start_file=__file__)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_live_risk_reviewed_preparation_gap_report.json", start_file=__file__)


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
    return candidate_id(candidate).startswith("cand_20260612_phase37_live_risk_")


def conversion_target(candidate: dict[str, Any]) -> dict[str, Any]:
    target = candidate.get("conversion_target")
    return target if isinstance(target, dict) else {}


def candidate_gaps(candidate: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
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
    for path in [
        ("review", "ai_audit", "reviewed_allowed"),
        ("workflow", "default_guidance_allowed"),
        ("workflow", "hard_gate_allowed"),
        ("workflow", "approved_allowed"),
        ("machine_gate", "approved_allowed"),
        ("machine_gate", "default_guidance_allowed"),
        ("machine_gate", "hard_gate_allowed"),
        ("conflict_audit", "approval_allowed"),
        ("conflict_audit", "default_guidance_allowed"),
        ("conflict_audit", "hard_gate_allowed"),
    ]:
        if deep_get(candidate, path) is not False:
            gaps.append(".".join(path) + "_not_false")
    if deep_get(candidate, ("machine_gate", "default_guidance")) != "deny":
        gaps.append("machine_gate.default_guidance_not_denied")
    if not conversion_target(candidate).get("proposed_knowledge_id"):
        gaps.append("conversion_target.proposed_knowledge_id_missing")
    if len(as_list(candidate.get("source_refs"))) < 3:
        gaps.append("source_refs_less_than_3")
    return gaps


def candidate_warnings(candidate: dict[str, Any]) -> list[str]:
    task_id = str(candidate.get("research_task_id"))
    warnings = ["formal_kb_full_conflict_check_required_before_reviewed_conversion"]
    if task_id == "P37-G-L03":
        warnings.append("reviewed_requires_position_reconciliation_schema")
    if task_id == "P37-G-L10":
        warnings.append("reviewed_requires_exposure_taxonomy")
    if task_id == "P37-G-L11":
        warnings.append("reviewed_requires_loss_event_window_reset_freeze_review_schema")
    if task_id == "P37-G-L12":
        warnings.append("hard_risk_gate_wording_must_remain_caveat_only_not_actual_hard_gate")
    return warnings


def load_scope_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for directory in (LIVE_DIR, RISK_DIR):
        for path in sorted(directory.glob("cand_20260612_phase37_live_risk_*.json")):
            candidate = read_json(path)
            if is_scope_candidate(candidate):
                candidates.append(candidate)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def package_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    gaps = candidate_gaps(candidate)
    warnings = candidate_warnings(candidate)
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
            "ai_audit": deep_get(candidate, ("review", "ai_audit"), {}),
            "open_questions": as_list(deep_get(candidate, ("review", "open_questions"), [])),
        },
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


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    packaged_gaps: dict[str, list[str]] = {}
    if len(candidates) != 12:
        failures.append(f"expected 12 live/risk candidates, got {len(candidates)}")
    for candidate in candidates:
        gaps = candidate_gaps(candidate)
        if gaps:
            packaged_gaps[candidate_id(candidate)] = gaps
    if packaged_gaps:
        failures.append("some candidates are not ready for reviewed-preparation audit")
    decision_counts = Counter(deep_get(candidate, ("status", "ingestion_decision")) for candidate in candidates)
    return {
        "gate_id": "phase37_live_risk_reviewed_preparation_gap_report",
        "checked_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "decision_counts": dict(decision_counts),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "candidate_gaps": packaged_gaps,
        "warnings": [
            "本包只请求 reviewed/caveat_only；不得创建 approved、default guidance 或 hard gate。",
            "即使 reviewed/caveat_only 通过，也不得生成风险阈值数值、买卖点、仓位、杠杆或实盘执行建议。",
        ],
    }


def build_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_caveat_only_preparation_audit",
        "scope": {
            "phase": "Phase 37",
            "branch": "Trading Engineering",
            "partitions": [LIVE_PARTITION, RISK_PARTITION],
            "candidate_count": len(candidates),
            "source_first_audit_result_id": FIRST_AUDIT_RESULT_ID,
            "target": "判断 12 条 Live Execution / Risk Management accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、监管规则、交易所资料、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance 或 hard gate。",
            "重点复核 L03 是否需要 position reconciliation schema，L10 是否需要 exposure taxonomy，L11 是否需要亏损事件/窗口/重置/冻结/人工复核 schema。",
            "重点复核 L12 的 hard risk gate 语义是否仅为 caveat_only 边界，不得变成实际 hard gate 权限。",
            "检查 Live Execution 与 Risk Management owner 边界：真实订单、真实状态、真实风控动作归对应 owner；AI scoring 只能引用，不能绕过 final gate。",
            "检查是否有中文乱码、mock/test 污染、项目私有参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "quality_gate": {"pass": "boolean", "reason": "string"},
            "summary": {
                "total": 12,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                }
            ],
        },
        "quality_gate": gate,
        "candidates": [package_candidate(candidate) for candidate in candidates],
    }


def main() -> int:
    candidates = load_scope_candidates()
    gate = quality_gate(candidates)
    write_json(REPORT_PATH, gate)
    write_json(AUDIT_PATH, build_package(candidates, gate))
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "audit_package": str(AUDIT_PATH)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
