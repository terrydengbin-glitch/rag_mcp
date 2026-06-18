"""Apply Phase 37 Live Execution / Risk Management first audit result.

The first audit only moves candidates to accepted_for_draft. It never creates
formal reviewed knowledge, approved knowledge, default guidance, or hard gates.
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
TASK_ID = "CEK-TA-437"
EXPECTED_PACKAGE_ID = "phase37_live_risk_candidate_audit_package_20260612"
EXPECTED_AUDIT_RESULT_ID = "audit_result_phase37_live_risk_candidate_audit_20260612_strict_v1"
LIVE_PARTITION = "KB_06_LIVE_EXECUTION"
RISK_PARTITION = "KB_07_RISK_MANAGEMENT"

LIVE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", LIVE_PARTITION, start_file=__file__)
RISK_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", RISK_PARTITION, start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{EXPECTED_AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_live_risk_audit_import_report.json", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    ("P37-G-L01", "least_privilege_api_required", "high", "NIST least privilege 支撑最小权限原则，SEC/CME 支撑 market access 与 pre-trade control；不得泛化为所有 broker 的具体权限矩阵。"),
    ("P37-G-L02", "order_state_machine_required", "high", "FIX Execution Report / OrdStatus 支撑订单接收、成交、拒单、取消、过期和 pending 等状态语义。"),
    ("P37-G-L03", "position_reconciliation_required", "medium_high", "本地订单、成交和仓位必须与 broker/account source 对账；reviewed 前需补 position reconciliation schema。"),
    ("P37-G-L04", "kill_switch_required", "high", "CME Kill Switch 支撑 block new order entry / cancel working orders；kill switch 是执行安全控制，不是策略判断。"),
    ("P37-G-L05", "exchange_adapter_error_contract_required", "medium_high", "IBKR、Binance filters、FIX 状态语义支撑 adapter 需要结构化错误契约，不能靠字符串异常驱动实盘决策。"),
    ("P37-G-L06", "order_fill_trade_log_required", "high", "FIX Execution Report 与审计日志来源支撑订单请求、成交、拒单、撤单、费用、状态迁移和人工操作可追踪。"),
    ("P37-G-L07", "single_trade_risk_limit_required", "high", "SEC 15c3-5、CFTC 17 CFR 1.11、CME/FIA 支撑 pre-trade risk controls；不得给单笔风险阈值数值。"),
    ("P37-G-L08", "daily_loss_limit_required", "high", "需定义 realized/unrealized loss 口径、重置时区、冻结动作和恢复流程；阈值必须由项目 owner 配置。"),
    ("P37-G-L09", "max_open_positions_required", "high", "SEC/CFTC/CME 资料支持订单、资本、信用、数量等 pre-trade 限制；本条未给具体数值，可进入 draft。"),
    ("P37-G-L10", "portfolio_exposure_limit_required", "medium_high", "组合/账户/品种/方向暴露上限作为 risk control 方向成立；QuantConnect 只能作平台示例，reviewed 前需补 exposure taxonomy。"),
    ("P37-G-L11", "consecutive_loss_stop_required", "medium", "方向可接受，但来源偏原则性；reviewed 前必须补亏损事件口径、时间窗口、重置条件、冻结动作和人工复核 schema。"),
    ("P37-G-L12", "hard_risk_gate_precedes_execution", "high", "SEC/CFTC/CME/FIA 支撑 deterministic pre-trade risk controls 先于市场订单；本轮只允许 draft，不得实际启用 hard gate。"),
]


GLOBAL_PATCH_NOTES = {
    "source": [
        "SEC/CFTC/NIST/CME/FIA/FIX/IBKR/Binance/QuantConnect 只能支撑原则、监管/行业要求或具体 venue/broker/platform 语义。",
        "不得把任何 broker、venue、platform 文档写成所有市场通用规则。",
    ],
    "content": [
        "Live Execution 负责 API 权限、订单状态、适配器错误、真实订单/成交/费用、仓位对账和审计日志。",
        "Risk Management 负责 deterministic pre-trade risk gates、风险限额、日亏损、组合暴露、连续亏损和 kill/stop 事件政策边界。",
    ],
    "boundary": [
        "accepted_for_draft 不是 reviewed、approved、default guidance 或 hard gate。",
        "不得生成买卖点、仓位、杠杆、止损止盈参数、实盘执行建议或风险阈值数值。",
    ],
    "conflict": [
        "AI scoring / Agent 只能引用这些规则，不能绕过 deterministic final gate。",
        "Replay/Simulation 只模拟；Live Execution / Risk Management 拥有真实订单、真实状态和风控动作。",
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def flatten_patch_notes(groups: dict[str, list[str]]) -> list[str]:
    flattened: list[str] = []
    for group_name in ("source", "content", "boundary", "conflict"):
        for note in groups.get(group_name, []):
            flattened.append(f"{group_name}: {note}")
    return flattened


def candidate_path(candidate_id: str) -> Path:
    for directory in (LIVE_DIR, RISK_DIR):
        path = directory / f"{candidate_id}.json"
        if path.exists():
            return path
    raise FileNotFoundError(candidate_id)


def candidate_id(slug: str) -> str:
    return f"cand_20260612_phase37_live_risk_{slug}_001"


def build_audit_result() -> dict[str, Any]:
    candidate_results = []
    for task_id, slug, confidence, reason in RESULTS:
        candidate_results.append(
            {
                "candidate_id": candidate_id(slug),
                "research_task_id": task_id,
                "decision": "accepted_for_draft",
                "confidence": confidence,
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": [reason],
                "required_followups": [
                    "进入 reviewed/caveat_only 前必须另行导出 reviewed-preparation 审计包。",
                    "不得创建 approved、default guidance 或 hard gate。",
                ],
                "patch_notes": GLOBAL_PATCH_NOTES,
                "source_assessment": {
                    "source_count": 4,
                    "missing_sources": [],
                    "weak_sources": [],
                    "recommended_extra_sources": [],
                },
                "classification_assessment": {
                    "is_correct_branch": True,
                    "expected_branch": "Trading Engineering / Live Execution or Risk Management",
                    "misplaced_topics": [],
                },
            }
        )
    return {
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": EXPECTED_PACKAGE_ID,
        "quality_gate": {"pass": True},
        "summary": {
            "total": 12,
            "accepted_for_draft": 12,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "candidate_results": candidate_results,
        "global_patch_notes": GLOBAL_PATCH_NOTES,
    }


def patch_candidate(payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    patch_notes = result.get("patch_notes", GLOBAL_PATCH_NOTES)
    if not isinstance(patch_notes, dict):
        patch_notes = GLOBAL_PATCH_NOTES
    flat_patch_notes = flatten_patch_notes(patch_notes)

    status = payload.setdefault("status", {})
    workflow = payload.setdefault("workflow", {})
    review = payload.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log

    conflict = payload.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False
    conflict["resolution_summary"] = (
        "首轮审计内容层 accepted_for_draft；candidate 不是 formal knowledge，"
        "不得创建 reviewed、approved、default guidance 或 hard gate。"
    )

    machine_gate = payload.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Phase 37 Live/Risk first audit allows accepted_for_draft only; reviewed requires later reviewed-preparation audit."
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False

    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
        "package_id": EXPECTED_PACKAGE_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "decision": "accepted_for_draft",
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": flat_patch_notes,
        "patch_note_groups": patch_notes,
        "source_assessment": result.get("source_assessment", {}),
        "classification_assessment": result.get("classification_assessment", {}),
        "boundary": "accepted_for_draft is not reviewed or approved; this audit does not allow default guidance or hard gate.",
    }

    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["updated_at"] = TODAY
    status["decision_reason"] = (
        "Phase 37 Live Execution / Risk Management 首轮严格审计结论为 accepted_for_draft；"
        "不允许 reviewed、approved、default guidance、hard gate 或风险阈值建议。"
    )

    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["next_action"] = "export_reviewed_preparation_audit_package"
    workflow["ai_audit_result_id"] = EXPECTED_AUDIT_RESULT_ID
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["formalization_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False

    conversion = payload.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "draft"
        conversion["reviewed_allowed"] = False
        conversion["approved_allowed"] = False
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
        conversion["formalization_blockers"] = ["requires_reviewed_preparation_audit"]

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase37_live_risk_first_audit_imported",
            "reason": f"accepted_for_draft / confidence={result.get('confidence')}",
            "audit_result_id": EXPECTED_AUDIT_RESULT_ID,
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
    audit = build_audit_result()
    results = audit["candidate_results"]
    write_json(AUDIT_RESULT_PATH, audit)

    updated = []
    for result in results:
        cid = str(result["candidate_id"])
        path = candidate_path(cid)
        payload = patch_candidate(read_json(path), result)
        write_json(path, payload)
        updated.append({"candidate_id": cid, "research_task_id": result["research_task_id"], "path": str(path)})

    report = {
        "report_id": "phase37_live_risk_audit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_path": str(AUDIT_RESULT_PATH),
        "decision_counts": decision_counts(results),
        "formal_knowledge_created": 0,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "risk_threshold_advice_enabled": 0,
        "updated_candidates": updated,
        "next_task": "CEK-TA-438",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"status": "pass", "summary": report["decision_counts"], "report_path": str(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
