"""Export Phase 37 Trade Analysis reviewed/caveat_only preparation package.

Trade Analysis candidates have only passed as ``accepted_for_draft``.
This package asks an external reviewer whether each item may become formal
``reviewed/caveat_only``. It never creates formal knowledge and never enables
approved, default guidance, risk-threshold advice, or hard-gate status.
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


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-445"
PACKAGE_ID = "phase37_trade_analysis_reviewed_preparation_audit_package_20260612"
PARTITION = "KB_07_TRADE_ANALYSIS"
FIRST_AUDIT_RESULT_ID = "audit_result_phase37_trade_analysis_candidate_audit_20260612_strict_v1"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_trade_analysis_reviewed_preparation_gap_report.json", start_file=__file__
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
    return candidate_id(candidate).startswith("cand_20260612_phase37_trade_analysis_")


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
    if deep_get(candidate, ("workflow", "risk_threshold_advice_allowed")) is not False:
        gaps.append("workflow.risk_threshold_advice_not_disabled")
    if not target.get("proposed_knowledge_id"):
        gaps.append("conversion_target.proposed_knowledge_id_missing")
    if target.get("target_review_status") not in {"draft", "reviewed"}:
        gaps.append("conversion_target.target_review_status_not_draft")
    if len(as_list(candidate.get("source_refs"))) < 3:
        gaps.append("source_refs_less_than_3")
    if conflict_status not in {"none", "resolved", "none_known_in_visible_context", "visible_context_no_conflict"}:
        gaps.append("conflict_status_not_safe_for_reviewed_preparation")
    for path in [
        ("conflict_audit", "approval_allowed"),
        ("conflict_audit", "default_guidance_allowed"),
        ("conflict_audit", "hard_gate_allowed"),
        ("machine_gate", "approved_allowed"),
        ("machine_gate", "default_guidance_allowed"),
        ("machine_gate", "hard_gate_allowed"),
        ("machine_gate", "risk_threshold_advice_allowed"),
    ]:
        if deep_get(candidate, path) is not False:
            gaps.append(".".join(path) + "_not_false")
    if deep_get(candidate, ("machine_gate", "default_guidance")) != "deny":
        gaps.append("machine_gate.default_guidance_not_denied")
    if deep_get(candidate, ("machine_gate", "hidden_from_default_queue")) is not True:
        gaps.append("machine_gate.hidden_from_default_queue_not_true")
    if deep_get(candidate, ("machine_gate", "visible_in_default_guidance_queue")) is not False:
        gaps.append("machine_gate.visible_in_default_guidance_queue_not_false")
    return gaps


def candidate_warnings(candidate: dict[str, Any]) -> list[str]:
    task_id = str(candidate.get("research_task_id"))
    warnings = ["formal_kb_full_conflict_check_required_before_reviewed_conversion"]
    if task_id == "P37-H-T01":
        warnings.append("reviewed_requires_trade_review_r_decomposition_schema")
    if task_id == "P37-H-T02":
        warnings.append("reviewed_requires_mae_mfe_calculation_contract_and_post_trade_boundary")
    if task_id == "P37-H-T03":
        warnings.append("reviewed_requires_bad_trade_taxonomy_schema")
    if task_id == "P37-H-T04":
        warnings.append("reviewed_requires_good_loss_bad_win_policy_schema")
    if task_id in {"P37-H-T05", "P37-H-T06", "P37-H-T07", "P37-H-T08"}:
        warnings.append("reviewed_requires_entry_exit_risk_execution_quality_review_schema")
    if task_id == "P37-H-T09":
        warnings.append("reviewed_requires_rule_compliance_schema")
    if task_id == "P37-H-T10":
        warnings.append("reviewed_requires_regime_fit_review_contract")
    if task_id == "P37-H-T11":
        warnings.append("reviewed_requires_reason_code_taxonomy")
    if task_id == "P37-H-T12":
        warnings.append("reviewed_requires_research_hypothesis_lifecycle_contract")
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
            "risk_threshold_advice_allowed": deep_get(candidate, ("review", "ai_audit", "risk_threshold_advice_allowed")),
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
        "reviewed_preparation_schema_contracts_to_check": [
            "trade_review_schema",
            "planned_vs_realized_r_decomposition",
            "mae_mfe_calculation_contract",
            "bad_trade_taxonomy",
            "good_loss_bad_win_policy",
            "entry_quality_review",
            "exit_quality_review",
            "risk_quality_review",
            "execution_quality_review",
            "rule_compliance_schema",
            "regime_fit_review",
            "reason_code_taxonomy",
            "research_hypothesis_lifecycle",
        ],
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
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def build_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    packaged_gaps: dict[str, list[str]] = {}
    warnings: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 Trade Analysis candidates, got {len(candidates)}")
    for candidate in candidates:
        cid = candidate_id(candidate)
        gaps = candidate_gaps(candidate)
        if gaps:
            packaged_gaps[cid] = gaps
        warnings.extend(f"{cid}: {warning}" for warning in candidate_warnings(candidate))
    if packaged_gaps:
        failures.append("some candidates are not ready for reviewed-preparation audit")
    counts = Counter(deep_get(candidate, ("status", "ingestion_decision")) for candidate in candidates)
    return {
        "gate_id": "phase37_trade_analysis_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "candidate_count": len(candidates),
        "status_counts": dict(counts),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "candidate_gaps": packaged_gaps,
        "warnings": warnings,
        "known_reviewed_preparation_gaps": [
            "需要外部审计复核 trade_review_schema 是否足以承载计划、实际、风险、执行、市场状态和规则符合性上下文。",
            "需要外部审计复核 planned_vs_realized_r_decomposition 与 Quant Foundation R/R-multiple 本体边界是否清晰。",
            "需要外部审计复核 MAE/MFE 是否仅限 post-trade/research，不得写成事前路径或实盘许可。",
            "需要外部审计复核 bad trade taxonomy、good loss/bad win、reason code 是否不输出交易建议。",
            "需要外部审计复核复盘发现必须转为 research hypothesis，并经过独立验证后才能影响策略规则。",
        ],
    }


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
            "tree_node_id": "kt.trade_analysis",
            "candidate_count": len(packaged),
            "source_first_audit_result_id": FIRST_AUDIT_RESULT_ID,
            "target": "判断 12 条 Trade Analysis accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_reviewed": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、论文、官方文档、资料、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance、hard gate 或风险阈值建议。",
            "重点复核 Trade Analysis 是否只负责 post-trade 复盘、标签、reason code、质量归因、bad-case taxonomy 和 research hypothesis 生成。",
            "重点复核复盘结论是否必须转为 research hypothesis 并经过独立验证，不能直接改写实时交易规则。",
            "重点复核 PnL 是否没有被作为唯一标签；必须保留计划、实际、风险、执行、市场状态和规则符合性上下文。",
            "重点复核 MAE/MFE、planned/realized R、good loss/bad win、reason code 是否仅为 post-trade/research labeling 边界，不得作为事前路径或实盘许可。",
            "检查 Quant Foundation 是否拥有 R/R-multiple 本体；Trade Analysis 只能消费这些指标做复盘标签。",
            "检查 Live Execution / Risk Management 是否拥有真实订单、成交、风险动作和 hard gate；Trade Analysis 不接管实时执行或风控动作。",
            "检查 AI Engineering 是否只能引用这些字段设计 LLM scoring 标签、eval case 和 RAG 检索，不得把复盘结论改写成模型训练本体或交易执行规则。",
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
                    "source_assessment": {
                        "source_count": "integer",
                        "weak_sources": ["string"],
                        "missing_sources": ["string"],
                    },
                    "schema_contract_assessment": {
                        "required_contracts_present": "boolean",
                        "missing_contracts": ["string"],
                        "field_level_gaps": ["string"],
                    },
                    "classification_assessment": {
                        "is_correct_branch": "boolean",
                        "expected_branch": "Trading Engineering / Trade Analysis",
                        "misplaced_topics": ["string"],
                    },
                }
            ],
        },
        "quality_gate": gate,
        "candidates": packaged,
    }


def main() -> int:
    candidates = load_scope_candidates()
    gate = build_gate(candidates)
    write_json(REPORT_PATH, gate)
    write_json(AUDIT_PATH, build_package(candidates, gate))
    print(
        json.dumps(
            {
                "status": gate["gate_status"],
                "candidate_count": len(candidates),
                "audit_package": str(AUDIT_PATH),
                "report": str(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
