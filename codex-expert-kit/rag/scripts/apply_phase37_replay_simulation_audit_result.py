"""Apply Phase 37 Replay / Simulation first audit result to candidates.

The first audit may only move candidates to ``accepted_for_draft``,
``needs_more_evidence``, ``rejected`` or ``blocked``. It never creates formal
reviewed knowledge, approved knowledge, default guidance, or hard gates.
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
EXPECTED_PACKAGE_ID = "phase37_replay_simulation_candidate_audit_package_20260611"
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase37_replay_simulation_candidate_audit_20260611_strict_v1"
PARTITION = "KB_05_REPLAY_SIMULATION"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{EXPECTED_AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_replay_simulation_audit_import_report.json", start_file=__file__)
NO_SUPPLEMENT_REPORT = resolve_repo_path("docs", "reports", "phase37_replay_simulation_no_supplement_needed_report.json", start_file=__file__)


CONFIDENCE_BY_TASK = {
    "P37-F-R01": "medium_high",
    "P37-F-R02": "medium_high",
    "P37-F-R03": "high",
    "P37-F-R04": "high",
    "P37-F-R05": "high",
    "P37-F-R06": "medium_high",
    "P37-F-R07": "high",
    "P37-F-R08": "high",
    "P37-F-R09": "high",
    "P37-F-R10": "medium_high",
    "P37-F-R11": "high",
    "P37-F-R12": "medium_high",
}

REASONS_BY_TASK = {
    "P37-F-R01": "事件时钟、撮合时点、信号生成和订单提交顺序属于 Replay / Simulation 的基础边界，可进入 draft。",
    "P37-F-R02": "OHLC 同根 K 内 TP/SL 真实先后不可证明，必须声明处理假设；reviewed 前建议补 CEK-TA fill-ordering contract。",
    "P37-F-R03": "Fill model 必须声明成交价格、数量、spread、slippage、队列/流动性限制和适用市场，来源支撑充足。",
    "P37-F-R04": "不能默认所有订单完整成交，partial/no fill 与订单状态需要显式建模。",
    "P37-F-R05": "高频或盘中 simulation 必须声明 feed/order/confirmation/report latency。",
    "P37-F-R06": "Paper trading 只能验证流程和部分执行假设，不能等同真实成交、滑点、拒单、延迟或风控表现。",
    "P37-F-R07": "交易所/经纪商规则必须按 venue/product 映射进入模拟约束。",
    "P37-F-R08": "最小数量、步长、最小名义金额、价格精度和订单类型限制必须模拟。",
    "P37-F-R09": "拒单、撤单、撤改单、过期、pending 和回报缺失不能被省略。",
    "P37-F-R10": "simulation/paper 到 live 前需要 gap report；reviewed 前应补 CEK-TA gap report schema。",
    "P37-F-R11": "tick/order-book replay 与 OHLC replay 粒度边界清晰，不能伪装为真实市场反应。",
    "P37-F-R12": "Backtest/Replay/Paper/Live 的执行成本口径必须版本化映射；reviewed 前需与 Backtest/Execution owner schema 对齐。",
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_path(candidate_id: str) -> Path:
    return CANDIDATE_DIR / f"{candidate_id}.json"


def load_replay_candidates() -> list[dict[str, Any]]:
    candidates = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase37_replay_simulation_*.json")):
        data = read_json(path)
        if data.get("workflow", {}).get("phase") == "37":
            candidates.append(data)
    if len(candidates) != 12:
        raise ValueError(f"expected 12 replay candidates, got {len(candidates)}")
    return candidates


def build_audit_result(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    results = []
    for candidate in candidates:
        task_id = str(candidate.get("research_task_id"))
        results.append(
            {
                "candidate_id": candidate["candidate_id"],
                "research_task_id": task_id,
                "decision": "accepted_for_draft",
                "confidence": CONFIDENCE_BY_TASK.get(task_id, "medium_high"),
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [REASONS_BY_TASK.get(task_id, "内容层允许进入 accepted_for_draft。")],
                "required_followups": [
                    "进入 reviewed/caveat_only 前必须另行导出 reviewed-preparation 审计包。",
                    "不得创建 approved、default guidance 或 hard gate。",
                ],
                "patch_notes": {
                    "source": [
                        "框架、平台、交易所、broker 和 FIX 文档只能支撑各自语义，不得泛化为所有市场通用规则。"
                    ],
                    "content": [
                        "Replay / Simulation 只表达事件时钟、成交模型、partial/no fill、延迟模型、交易所/经纪商规则映射、订单状态生命周期、模拟盘/实盘 gap report、OHLC vs tick replay 粒度边界。"
                    ],
                    "boundary": [
                        "simulation evidence invalidation 不等于自动拒单、实盘停机或风控 hard gate。"
                    ],
                    "conflict": [
                        "R07/R08/R09 与 Live Execution / Exchange Adapter 重叠时，Replay 只模拟规则与状态；真实下单、真实拒单、账户同步、实盘订单状态归 Live Execution owner。"
                    ],
                },
                "source_assessment": {
                    "source_count": len(candidate.get("source_refs", [])),
                    "missing_sources": [],
                    "weak_sources": [],
                    "recommended_extra_sources": [],
                },
                "classification_assessment": {
                    "is_correct_branch": True,
                    "expected_branch": "Trading Engineering / Replay Simulation",
                    "misplaced_topics": [],
                },
            }
        )
    return {
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": EXPECTED_PACKAGE_ID,
        "quality_gate": {
            "pass": False,
            "reason": "原候选 conflict_audit.approval_allowed=true 与包级 hard boundary 冲突；导入前由 Codex 补丁修正为 false。",
            "machine_ingestion_blocker": "conflict_audit.approval_allowed must be patched to false before ingestion",
        },
        "content_decision": {
            "accepted_for_draft": 12,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "summary": {
            "total": 12,
            "accepted_for_draft": 12,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": results,
        "global_patch_notes": {
            "machine": [
                "所有候选 conflict_audit.approval_allowed 必须改为 false。",
                "所有候选 conflict_audit.default_guidance_allowed 必须为 false。",
                "所有候选 conflict_audit.hard_gate_allowed 必须为 false。",
            ],
            "boundary": [
                "所有候选必须保持 reviewed_allowed=false、approved_allowed=false、default_guidance_allowed=false、hard_gate_allowed=false。"
            ],
        },
    }


def normalize_patch_notes(value: Any) -> dict[str, list[str]]:
    notes = {"source": [], "content": [], "boundary": [], "conflict": []}
    if isinstance(value, dict):
        for key in notes:
            raw = value.get(key, [])
            if isinstance(raw, list):
                notes[key] = [str(item) for item in raw]
            elif raw:
                notes[key] = [str(raw)]
    return notes


def flatten_patch_notes(groups: dict[str, list[str]]) -> list[str]:
    flattened: list[str] = []
    for group_name in ("source", "content", "boundary", "conflict"):
        for note in groups.get(group_name, []):
            flattened.append(f"{group_name}: {note}")
    return flattened


def patch_candidate(payload: dict[str, Any], result: dict[str, Any], audit_result_id: str) -> dict[str, Any]:
    decision = str(result["decision"])
    patch_notes = normalize_patch_notes(result.get("patch_notes"))
    flat_patch_notes = flatten_patch_notes(patch_notes)

    status = payload.setdefault("status", {})
    workflow = payload.setdefault("workflow", {})
    review = payload.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log

    conflict_audit = payload.setdefault("conflict_audit", {})
    conflict_audit["approval_allowed"] = False
    conflict_audit["default_guidance_allowed"] = False
    conflict_audit["hard_gate_allowed"] = False
    conflict_audit["resolution_summary"] = (
        "首轮审计内容层 accepted_for_draft；candidate 不是 formal knowledge，"
        "不得创建 reviewed/approved/default guidance/hard gate。"
    )

    machine_gate = payload.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = (
        "Phase 37 Replay / Simulation first audit allows accepted_for_draft only; "
        "formal reviewed requires later reviewed-preparation audit."
    )
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False

    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": audit_result_id,
        "package_id": EXPECTED_PACKAGE_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "decision": decision,
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": flat_patch_notes,
        "patch_note_groups": patch_notes,
        "source_assessment": result.get("source_assessment", {}),
        "classification_assessment": result.get("classification_assessment", {}),
        "boundary": "accepted_for_draft is not reviewed or approved; this audit does not allow default guidance or hard gate.",
    }

    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"Phase 37 Replay / Simulation 首轮严格审计结论为 {decision}；"
        "已修正 conflict_audit approval/default/hard_gate 机器字段；不允许 reviewed/approved/default guidance/hard gate。"
    )

    workflow["ai_audit_result_id"] = audit_result_id
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["formalization_allowed"] = False
    conversion_patch = {
        "target_review_status": "draft" if decision == "accepted_for_draft" else "blocked",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }
    workflow["conversion_target"] = conversion_patch
    top_level_conversion = payload.setdefault("conversion_target", {})
    if isinstance(top_level_conversion, dict):
        top_level_conversion.update(conversion_patch)
        if decision == "accepted_for_draft":
            top_level_conversion["formalization_blockers"] = ["requires_reviewed_preparation_audit"]

    if decision == "accepted_for_draft":
        status["review_status"] = "accepted"
        status["ingestion_decision"] = "accepted_for_draft"
        workflow["stage"] = "ai_audited"
        workflow["queue_group"] = "ai_passed"
        workflow["next_action"] = "export_reviewed_preparation_audit_package"
    elif decision == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "supplement_sources_and_export_reaudit_package"
    elif decision == "rejected":
        status["review_status"] = "rejected"
        status["ingestion_decision"] = "rejected"
        workflow["stage"] = "rejected"
        workflow["queue_group"] = "rejected"
        workflow["next_action"] = "none"
    else:
        status["review_status"] = "blocked"
        status["ingestion_decision"] = "blocked"
        workflow["stage"] = "blocked"
        workflow["queue_group"] = "pending"
        workflow["next_action"] = "manual_review"

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase37_replay_simulation_first_audit_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": audit_result_id,
            "patch_notes": flat_patch_notes,
        }
    )
    return payload


def decision_counts(results: list[dict[str, Any]]) -> dict[str, int]:
    counter = Counter(str(result.get("decision")) for result in results)
    return {
        "total": len(results),
        "accepted_for_draft": counter.get("accepted_for_draft", 0),
        "needs_more_evidence": counter.get("needs_more_evidence", 0),
        "rejected": counter.get("rejected", 0),
        "blocked": counter.get("blocked", 0),
    }


def main() -> int:
    candidates = load_replay_candidates()
    audit = build_audit_result(candidates)
    write_json(AUDIT_RESULT_PATH, audit)
    results = audit["candidate_results"]

    updated: list[str] = []
    for result in results:
        path = candidate_path(str(result["candidate_id"]))
        payload = read_json(path)
        patched = patch_candidate(payload, result, EXPECTED_AUDIT_RESULT_ID)
        write_json(path, patched)
        updated.append(str(path))

    summary = decision_counts(results)
    report = {
        "report_id": "phase37_replay_simulation_audit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-426",
        "audit_result_path": str(AUDIT_RESULT_PATH),
        "summary": summary,
        "machine_field_patch": {
            "conflict_audit.approval_allowed": False,
            "conflict_audit.default_guidance_allowed": False,
            "conflict_audit.hard_gate_allowed": False,
        },
        "formal_knowledge_created": 0,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "updated_candidates": updated,
        "next_task": "CEK-TA-429",
    }
    write_json(REPORT_PATH, report)
    write_json(
        NO_SUPPLEMENT_REPORT,
        {
            "report_id": "phase37_replay_simulation_no_supplement_needed",
            "generated_at": TODAY,
            "tasks": ["CEK-TA-427", "CEK-TA-428"],
            "reason": "Replay / Simulation 首轮严格审计 12 条全部 accepted_for_draft，无 needs_more_evidence、rejected 或 blocked。",
            "needs_more_evidence_count": summary["needs_more_evidence"],
            "supplement_required": False,
            "reaudit_required": False,
            "next_task": "CEK-TA-429",
        },
    )
    print(json.dumps({"status": "pass", "summary": summary, "report_path": str(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
