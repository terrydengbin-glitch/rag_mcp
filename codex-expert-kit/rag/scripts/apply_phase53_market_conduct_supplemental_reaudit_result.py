"""Apply Phase 53 Market Conduct supplemental re-audit result.

The supplemental audit upgrades P53-TR-MC01 from needs_more_evidence to
accepted_for_draft after adding a direct FINRA Momentum Ignition source.

This script updates only the candidate lifecycle and audit trace. It does not
create formal reviewed/approved knowledge, default guidance, hard gates, legal
opinions, manipulation findings, trading permissions, or risk thresholds.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-13"
TASK_ID = "CEK-TA-523"
AUDIT_RESULT_ID = "audit_phase53_market_conduct_supplemental_reaudit_20260613"
PACKAGE_ID = "phase53_market_conduct_supplemental_reaudit_package_20260613"
CANDIDATE_ID = "cand_20260613_phase53_market_conduct_surveillance_taxonomy_required_001"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_08_TRADE_ANALYSIS",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase53_market_conduct_supplemental_reaudit_import_report.json", start_file=__file__
)
CUMULATIVE_REPORT_PATH = resolve_repo_path("docs", "reports", "phase53_audit_import_report.json", start_file=__file__)


RESULT: dict[str, Any] = {
    "candidate_id": CANDIDATE_ID,
    "research_task_id": "P53-TR-MC01",
    "decision": "accepted_for_draft",
    "confidence": "high",
    "reviewed_allowed": False,
    "approved_allowed": False,
    "default_guidance_allowed": False,
    "hard_gate_allowed": False,
    "reasons": [
        "补证已加入 FINRA 2024 Manipulative Trading 直接来源，可支撑 momentum ignition trading 作为 surveillance taxonomy 项。",
        "FINRA 2026 来源可支撑 manipulative trading surveillance program 语境，包括 layering、spoofing、wash trades、marking the close 等风险。",
        "CFTC disruptive trading practice 来源可支撑 futures / swaps disruptive practices 与 spoofing-related 语境。",
        "claim 已明确 taxonomy 只用于合规/审计/人工复核，不得替代法律结论、操纵定性或自动交易许可。",
        "required_fields_or_contract 已包含 legal_owner_required=true、manual_review_required=true、not_hard_gate=true 和 order/cancel/fill/timestamp evidence。",
    ],
    "required_followups": [
        "进入 reviewed/caveat_only 前必须保留 FINRA / CFTC jurisdiction caveat。",
        "正式文本必须写成 surveillance labels / reason codes / manual escalation context，不得写成 manipulation finding。",
        "不得把普通撤单、做市、报价更新或订单簿管理直接归类为操纵。",
        "如用于非美国证券市场、crypto、期货或其他 venue，必须补对应 jurisdiction / venue-specific 来源。",
    ],
    "patch_notes": {
        "source": [
            "保留 FINRA 2026 Manipulative Trading。",
            "保留 CFTC Disruptive Trading Practices。",
            "新增并保留 FINRA 2024 Manipulative Trading 作为 momentum ignition direct source。",
        ],
        "content": [
            "surveillance_taxonomy 可包含 spoofing、layering、wash_or_self_trade、momentum_ignition、marking_the_close、front_running。",
            "taxonomy 只能用于 surveillance labels、reason codes、人工复核和 escalation context。",
            "必须保留 evidence_required：order_event_id、cancel_event_id、fill_event_id、venue、session、timestamp_quality。",
        ],
        "boundary": [
            "不得输出法律意见。",
            "不得生成操纵定性。",
            "不得把异常标签直接变成硬阻断。",
            "不得生成交易许可。",
            "不得生成 hard gate。",
        ],
        "conflict": ["Legal / compliance owner 才能作正式判断；CEK-TA 只提供审计上下文。"],
    },
}


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def append_unique(target: list[Any], values: list[Any]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def apply_result(candidate: dict[str, Any]) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted_for_draft"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = (
        "Phase 53 Market Conduct 补证二审结论为 accepted_for_draft；candidate 不是 formal knowledge，"
        "不得视为 reviewed/approved/default guidance/hard gate。"
    )
    status["updated_at"] = TODAY

    review = candidate.setdefault("review", {})
    review["review_status"] = "accepted_for_draft"
    review["default_guidance_allowed"] = False
    review["approved_allowed"] = False
    review["hard_gate_allowed"] = False
    review["legal_opinion_allowed"] = False
    review["trade_execution_advice_allowed"] = False
    review["risk_threshold_advice_allowed"] = False
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "decision": RESULT["decision"],
        "confidence": RESULT["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "imported_at": TODAY,
        "required_followups": RESULT["required_followups"],
        "patch_notes": RESULT["patch_notes"],
    }

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "accepted_for_draft"
    workflow["last_audit_result_id"] = AUDIT_RESULT_ID
    workflow["last_audit_decision"] = "accepted_for_draft"
    workflow["target_review_status"] = "draft"
    workflow["next_allowed_decisions"] = ["reviewed_preparation_audit", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_decisions"] = [
        "reviewed",
        "approved",
        "default_guidance",
        "hard_gate",
        "legal_opinion",
        "trade_execution_advice",
        "risk_threshold_advice",
    ]

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = (
        "accepted_for_draft only; reviewed preparation still required; no approved/default/hard gate allowed."
    )
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False

    audit_patch_notes = candidate.setdefault("audit_patch_notes", {})
    for key, values in RESULT["patch_notes"].items():
        append_unique(audit_patch_notes.setdefault(key, []), values)

    conflict_audit = candidate.setdefault("conflict_audit", {})
    conflict_audit["conflict_status"] = "visible_context_no_direct_conflict"
    conflict_audit["resolution_summary"] = (
        "补证二审允许 accepted_for_draft；正式 reviewed/caveat_only 前仍需完整 KB 冲突、重复和 owner 边界检查。"
    )

    claim = candidate.setdefault("claim", {})
    claim["interpretation_notes"] = (
        "本候选补证二审通过，可进入 accepted_for_draft；taxonomy 只用于 surveillance labels、reason codes 和人工复核上下文，"
        "不得作为法律结论、操纵定性、交易许可或 hard gate。"
    )
    return candidate


def main() -> None:
    audit_payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "audited_at": TODAY,
        "summary": {
            "total": 1,
            "accepted_for_draft": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "manipulation_finding_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "candidate_results": [RESULT],
    }
    dump_json(AUDIT_RESULT_PATH, audit_payload)

    candidate = apply_result(load_json(CANDIDATE_PATH))
    dump_json(CANDIDATE_PATH, candidate)

    import_report = {
        "report_id": "phase53_market_conduct_supplemental_reaudit_import_report",
        "task_id": TASK_ID,
        "created_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "candidate_id": CANDIDATE_ID,
        "decision": "accepted_for_draft",
        "reviewed_created": False,
        "approved_created": False,
        "default_guidance_created": False,
        "hard_gate_created": False,
        "next_step": "Phase 53 的 5 条 P0 候选均已 accepted_for_draft；如需入正式知识，必须先导出 reviewed-preparation 审计包。",
        "boundary": "accepted_for_draft is not reviewed/approved/default guidance/hard gate.",
    }
    dump_json(IMPORT_REPORT_PATH, import_report)

    if CUMULATIVE_REPORT_PATH.exists():
        cumulative = load_json(CUMULATIVE_REPORT_PATH)
        cumulative["accepted_for_draft_count"] = 5
        cumulative["needs_more_evidence_count"] = 0
        cumulative["supplemented_for_reaudit_count"] = 1
        cumulative["supplemental_reaudit_result"] = AUDIT_RESULT_PATH.relative_to(
            resolve_repo_path(".", start_file=__file__)
        ).as_posix()
        cumulative["phase53_p0_candidate_status"] = "all_accepted_for_draft"
        cumulative["boundary"] = (
            "All five Phase 53 P0 candidates are accepted_for_draft only. "
            "No reviewed/approved/default guidance/hard gate created."
        )
        dump_json(CUMULATIVE_REPORT_PATH, cumulative)

    print(json.dumps({"candidate_id": CANDIDATE_ID, "decision": "accepted_for_draft"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
