"""Export Phase 37 Backtest reviewed/caveat_only preparation package.

Backtest candidates have only passed as ``accepted_for_draft``. This package
asks an external reviewer whether each item may become formal
``reviewed/caveat_only``. It never creates formal knowledge and never enables
approved, default guidance, or hard-gate status.
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
TASK_ID = "CEK-TA-417"
PACKAGE_ID = "phase37_backtest_reviewed_preparation_audit_package_20260611"
PARTITION = "KB_04_BACKTEST"
FIRST_AUDIT_RESULT_ID = "audit_result_phase37_backtest_candidate_audit_20260611_strict_v1"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_backtest_reviewed_preparation_gap_report.json", start_file=__file__
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
    return candidate_id(candidate).startswith("cand_20260611_phase37_backtest_")


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
    task_id = str(candidate.get("research_task_id"))
    claim = str(deep_get(candidate, ("claim", "normalized_claim"), ""))
    if deep_get(candidate, ("conflict_audit", "conflict_status")) == "none_known_in_visible_context":
        warnings.append("formal_kb_full_conflict_check_required_before_reviewed_conversion")
    if task_id in {"P37-E-B01", "P37-E-B02"} or claim.endswith("_block.v1"):
        warnings.append("verify_block_means_evidence_invalidation_not_hard_gate")
    if task_id == "P37-E-B03":
        warnings.append("reviewed_requires_survivorship_delisted_assets_historical_universe_or_contract_rollover_sources")
    if task_id == "P37-E-B10":
        warnings.append("reviewed_requires_profit_factor_drawdown_and_return_drawdown_context_sources")
    if task_id in {"P37-E-B11", "P37-E-B12"}:
        warnings.append("reviewed_requires_cek_ta_backtest_manifest_or_version_schema_support")
    if task_id == "P37-E-B01":
        warnings.append("reviewed_requires_point_in_time_available_time_bar_availability_sources")
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
            "tree_node_id": "kt.trading_engineering.backtest",
            "candidate_count": len(packaged),
            "source_first_audit_result_id": FIRST_AUDIT_RESULT_ID,
            "target": "判断 12 条 Backtest 回测可信度 accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、论文、官方文档、资料、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance 或 hard gate。",
            "重点复核 B01/B02 的 block 是否已经限定为 evidence invalidation，而不是自动 hard gate。",
            "重点复核 B03/B10/B11/B12 是否已有足够来源和内部 schema 支撑进入 reviewed/caveat_only。",
            "检查 Backtest 分支是否只表达回测可信度、偏差、成本、验证和复现边界，不混入 Replay、Live Execution、Risk Management 或 AI Engineering 本体。",
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
        "candidates": packaged,
    }


def build_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 scope candidates, got {len(candidates)}")
    for candidate in candidates:
        cid = candidate_id(candidate)
        gaps = candidate_gaps(candidate)
        item_warnings = candidate_warnings(candidate)
        if gaps:
            failures.append(f"{cid}: {gaps}")
        warnings.extend(f"{cid}: {warning}" for warning in item_warnings)
    counts = Counter(deep_get(candidate, ("status", "ingestion_decision")) for candidate in candidates)
    return {
        "gate_id": "phase37_backtest_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "status_counts": dict(counts),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
    }


def main() -> None:
    candidates = load_scope_candidates()
    gate = build_gate(candidates)
    write_json(REPORT_PATH, gate)
    write_json(AUDIT_PATH, build_package(candidates, gate))
    if gate["gate_status"] != "pass":
        raise SystemExit(f"reviewed preparation gate failed: {gate['failures']}")
    print(
        json.dumps(
            {
                "candidate_count": len(candidates),
                "audit_package": str(AUDIT_PATH),
                "report": str(REPORT_PATH),
                "gate_status": gate["gate_status"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
