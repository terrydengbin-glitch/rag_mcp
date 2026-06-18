"""Import Phase 45 Resilience / Incident / Log supplemental re-audit result.

This script handles the strict supplemental review for P45-D-OPS02 and
P45-D-OPS03. It only promotes candidates to accepted_for_draft and exports the
next reviewed/caveat_only preparation audit package for all six P45-D
candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk thresholds, stop thresholds, or live trading actions.
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


TODAY = "2026-06-12"
PHASE = "45"
TASK_ID = "CEK-TA-464"
AUDIT_RESULT_ID = "audit_phase45_resilience_incident_log_supplemental_reaudit_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_resilience_incident_log_supplemental_reaudit_package_20260612"
REVIEWED_PACKAGE_ID = "phase45_resilience_incident_log_reviewed_preparation_audit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_resilience_incident_log_supplemental_reaudit_import_report.json", start_file=__file__
)
REVIEWED_PACKAGE = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_GAP_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_resilience_incident_log_reviewed_preparation_gap_report.json", start_file=__file__
)
RUNTIME_CONTRACT = resolve_repo_path("docs", "contracts", "phase45_resilience_incident_log_runtime_contract.md", start_file=__file__)


SUPPLEMENTAL_DECISIONS: dict[str, dict[str, Any]] = {
    "P45-D-OPS02": {
        "candidate_id": "cand_20260612_phase45_resilience_incident_log_p45_d_ops02_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": (
            "Google SRE / AWS 支撑 degraded response 与 graceful degradation；PostgreSQL Hot Standby 支撑 "
            "read-only query 与 write-disabled 语义；CEK-TA runtime contract 支撑 normal/degraded/read_only/"
            "recovery/manual_intervention_required 状态机。"
        ),
        "required_followups": [
            "保留 caveat：Google SRE/AWS 是工程实践，不是交易监管要求。",
            "保留 caveat：PostgreSQL 只是 read-only database mode 示例，外接项目可使用等价数据库、权限控制或服务层写禁用实现。",
            "退出条件只能描述 owner、证据和审计 trace，不得写具体停机阈值、恢复阈值或自动拒单规则。",
        ],
        "patch_notes": {
            "source": [
                "保留 Google SRE Handling Overload、AWS graceful degradation、PostgreSQL Hot Standby、CEK-TA runtime contract。",
                "Reg SCI/NIST 只能作为韧性/事故响应背景来源，不作为 read-only 操作语义直接来源。",
            ],
            "content": [
                "把“必须声明退出条件”收窄为“必须声明退出条件的 owner、证据和审计 trace”。",
                "forbidden operations 只作为 draft design boundary，不生成 machine hard gate。",
            ],
            "boundary": [
                "不得输出停机阈值。",
                "不得输出恢复阈值。",
                "不得触发自动拒单、自动撤单、自动重发订单或其他实盘动作。",
            ],
            "conflict": [],
        },
    },
    "P45-D-OPS03": {
        "candidate_id": "cand_20260612_phase45_resilience_incident_log_p45_d_ops03_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": (
            "FIX ClOrdID/OrigClOrdID/CancelReject 支撑 cancel/replace 身份链与拒绝边界；Binance "
            "newClientOrderId 支撑 venue client order id 唯一性示例；IBKR order identifier 支撑 broker API "
            "order-id 复用/修改边界；CEK-TA runtime contract 支撑 replay/live action 边界。"
        ),
        "required_followups": [
            "保留 caveat：FIX、Binance、IBKR 是协议、venue 或 broker 示例，不能泛化为所有交易所或券商。",
            "外接项目必须提供自己的 order_state_machine / order truth source contract。",
            "live_order_action 必须位于人工/owner 审批和审计 trace 之后，不得由 replay 自动触发。",
        ],
        "patch_notes": {
            "source": [
                "保留 FIX Order Cancel/Replace、FIX OrderCancelReject、Binance Futures New Order、IBKR TWS API、CEK-TA runtime contract。",
                "OpenTelemetry 只能作为 trace/audit_trace_id 辅助来源，不能作为订单 replay 权限来源。",
            ],
            "content": [
                "保留 audit_replay、simulation_replay、state_rebuild、live_order_action 四分法。",
                "state_rebuild 只能重建内部状态视图，不得写入真实 venue/broker。",
                "live_order_action 是人工/owner 审批后的外部项目动作，不是 CEK-TA 自动动作。",
            ],
            "boundary": [
                "不得输出自动重发订单。",
                "不得输出自动撤单。",
                "不得输出自动修改订单。",
                "不得输出风控阈值或恢复阈值。",
            ],
            "conflict": [],
        },
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for partition in PARTITIONS:
        candidate_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(candidate_dir.glob("cand_20260612_phase45_resilience_incident_log_*.json")))
    return paths


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_reaudit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "scope": {
            "phase": PHASE,
            "task_id": TASK_ID,
            "reviewed_candidates": ["P45-D-OPS02", "P45-D-OPS03"],
            "purpose": "判断 OPS02/OPS03 补证后是否可从 needs_more_evidence 升级为 accepted_for_draft。",
        },
        "summary": {
            "total": 2,
            "accepted_for_draft": 2,
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
            "stop_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
        },
        "candidate_results": [
            {
                "candidate_id": payload["candidate_id"],
                "research_task_id": research_task_id,
                "decision": payload["decision"],
                "confidence": payload["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": [payload["reason"]],
                "required_followups": payload["required_followups"],
                "patch_notes": payload["patch_notes"],
            }
            for research_task_id, payload in SUPPLEMENTAL_DECISIONS.items()
        ],
        "global_notes": [
            "OPS02/OPS03 可以进入 draft 队列，但仍不得进入 reviewed、approved、default guidance 或 hard gate。",
            "运行时韧性与事故恢复边界不能被解释为自动拒单、自动撤单、自动重发、自动恢复交易或风险阈值规则。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def apply_supplemental_decisions() -> dict[str, Any]:
    paths_by_task: dict[str, Path] = {}
    for path in candidate_paths():
        data = read_json(path)
        paths_by_task[str(data.get("research_task_id"))] = path

    updated: list[dict[str, Any]] = []
    missing: list[str] = []
    for research_task_id, decision in SUPPLEMENTAL_DECISIONS.items():
        path = paths_by_task.get(research_task_id)
        if path is None:
            missing.append(research_task_id)
            continue

        candidate = read_json(path)
        candidate.setdefault("status", {})["review_status"] = "accepted"
        candidate["status"]["ingestion_decision"] = "accepted_for_draft"
        candidate["status"]["decision_reason"] = decision["reason"]
        candidate["status"]["updated_at"] = TODAY

        candidate.setdefault("workflow", {})["stage"] = "formal_draft_queue"
        candidate["workflow"]["queue_group"] = "ai_passed"
        candidate["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        candidate["workflow"]["forbidden_next_decisions"] = ["reviewed", "approved", "default_guidance", "hard_gate"]

        review = candidate.setdefault("review", {})
        review["review_status"] = "candidate_ready"
        review["review_mode"] = "reviewed_preparation_required"
        review["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": "accepted_for_draft",
            "confidence": decision["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "required_followups": decision["required_followups"],
            "patch_notes": decision["patch_notes"],
        }
        review.setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_reaudit",
                "action": "phase45_resilience_incident_log_supplemental_reaudit_imported",
                "reason": f"accepted_for_draft / confidence={decision['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )

        machine_gate = candidate.setdefault("machine_gate", {})
        machine_gate["default_guidance"] = "deny"
        machine_gate["reason"] = "accepted_for_draft only; reviewed preparation required; no approved/default/hard gate."
        machine_gate["hidden_from_default_queue"] = True
        machine_gate["visible_in_default_guidance_queue"] = False
        machine_gate["approved_allowed"] = False
        machine_gate["default_guidance_allowed"] = False
        machine_gate["hard_gate_allowed"] = False
        machine_gate["risk_threshold_advice_allowed"] = False

        write_json(path, candidate)
        updated.append(
            {
                "research_task_id": research_task_id,
                "candidate_id": candidate.get("candidate_id"),
                "decision": "accepted_for_draft",
                "path": repo_relative(path),
            }
        )
    return {"updated": updated, "missing": missing}


def load_all_p45d_candidates() -> list[dict[str, Any]]:
    candidates = [read_json(path) for path in candidate_paths()]
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def reviewed_preparation_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 P45-D candidates, got {len(candidates)}")
    if not RUNTIME_CONTRACT.exists():
        failures.append("runtime contract missing")
    for item in candidates:
        cid = str(item.get("candidate_id", "<unknown>"))
        task_id = str(item.get("research_task_id", "<unknown>"))
        status = item.get("status", {})
        machine_gate = item.get("machine_gate", {})
        if status.get("ingestion_decision") != "accepted_for_draft":
            failures.append(f"{task_id}: ingestion_decision is not accepted_for_draft")
        if status.get("review_status") != "accepted":
            failures.append(f"{task_id}: review_status is not accepted")
        if len(item.get("source_refs", [])) < 4:
            failures.append(f"{task_id}: source_refs < 4")
        if machine_gate.get("default_guidance") != "deny":
            failures.append(f"{task_id}: machine_gate.default_guidance must stay deny before reviewed preparation")
        for flag in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if machine_gate.get(flag) is not False:
                failures.append(f"{task_id}: machine_gate.{flag} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if "自动重发订单" in blob or "自动撤单" in blob:
            warnings.append(f"{task_id}: contains forbidden-action wording; audit must confirm it is negated/not_allowed context")
    return {
        "gate_id": "phase45_resilience_incident_log_reviewed_preparation_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": REVIEWED_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "runtime_contract": repo_relative(RUNTIME_CONTRACT),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings
        + [
            "本包只允许审计是否进入 formal reviewed/caveat_only；不得创建 approved/default guidance/hard gate。",
            "OPS02/OPS03 的补证通过只代表 accepted_for_draft，不代表 reviewed 已完成。",
            "任何恢复、replay、read-only、degraded mode 规则都不得产生自动实盘动作或风险阈值。",
        ],
    }


def export_reviewed_preparation_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    package = {
        "package_id": REVIEWED_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / Live Execution / Resilience Incident Log",
            "batch": "P45-D Resilience / Incident / Log",
            "candidate_count": len(candidates),
            "target": "判断 6 条 accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "reviewed_caveat_only_max": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "stop_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": [
                "买卖点",
                "仓位",
                "杠杆",
                "止损止盈参数",
                "实盘执行建议",
                "停机阈值",
                "恢复阈值",
                "自动拒单",
                "自动撤单",
                "自动重发订单",
            ],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、监管资料、官方文档、协议文档、数据库/SRE 文档和案例，对 reviewed/caveat_only 准备包进行严格审计。",
            "确认所有来源是否只支撑其可证明范围，尤其 FINRA/Reg SCI/NIST/AWS/Google SRE/PostgreSQL/FIX/Binance/IBKR/OpenTelemetry 的适用边界。",
            "确认 CEK-TA 内部 runtime contract 是否足以作为字段本体来源，外部来源是否只是 supporting source 或 implementation pattern。",
            "确认 P45-D 只用于运行时韧性、事故响应、恢复/replay 边界和日志治理，不混入策略 alpha、订单执行许可、风险阈值或 hard gate。",
            "输出只能是 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": REVIEWED_PACKAGE_ID,
            "summary": {
                "total": 6,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-D-OPS01..P45-D-OPS06",
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
        "runtime_contract": {
            "path": repo_relative(RUNTIME_CONTRACT),
            "purpose": "提供 runtime mode、read-only forbidden operations、replay boundary、owner boundary 和 machine gate 契约。",
        },
        "candidates": candidates,
    }
    write_json(REVIEWED_PACKAGE, package)


def main() -> int:
    audit_result = archive_audit_result()
    apply_report = apply_supplemental_decisions()
    candidates = load_all_p45d_candidates()
    gate = reviewed_preparation_gate(candidates)
    export_reviewed_preparation_package(candidates, gate)
    write_json(REVIEWED_GAP_REPORT, gate)
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_resilience_incident_log_supplemental_reaudit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "source_package_id": SOURCE_PACKAGE_ID,
            "summary": audit_result["summary"],
            "updated": apply_report["updated"],
            "missing": apply_report["missing"],
            "reviewed_preparation_package": repo_relative(REVIEWED_PACKAGE),
            "reviewed_preparation_gap_report": repo_relative(REVIEWED_GAP_REPORT),
            "reviewed_preparation_gate_status": gate["gate_status"],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
            "risk_threshold_advice_enabled": False,
        },
    )
    print(
        json.dumps(
            {
                "status": gate["gate_status"],
                "updated_count": len(apply_report["updated"]),
                "reviewed_preparation_candidate_count": len(candidates),
                "reviewed_preparation_package": repo_relative(REVIEWED_PACKAGE),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" and not apply_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
