"""Export Phase 60 P1 accepted candidates for reviewed/caveat_only preparation audit."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-585"
PACKAGE_ID = "phase60_p1_reviewed_preparation_audit_package_20260617"
EXPECTED_TASKS = {f"P60-P1-0{idx}" for idx in range(1, 7)}
PARTITIONS = ["KB_05_REPLAY_SIMULATION", "KB_06_LIVE_EXECUTION", "KB_07_RISK_MANAGEMENT"]


REVIEWED_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "P60-P1-01": {
        "required_focus": [
            "确认 certification_result_not_live_permission、adapter_certification_scope、certified_message_types、certified_order_lifecycle_cases 是否足够。",
            "确认 TT / Paxos / FIXSIM 均保留平台或工具来源边界。",
        ],
        "known_risk": "FIX/broker certification 被误读为真实流动性、策略收益或上线许可。",
    },
    "P60-P1-02": {
        "required_focus": [
            "重点审计 scenario schema 是否足以进入 reviewed/caveat_only。",
            "判断是否仍需补更直接的 regression testing / simulation reproducibility / dataset snapshot manifest 来源。",
        ],
        "known_risk": "scenario library 通过被误读为未来收益或 live-ready。",
    },
    "P60-P1-03": {
        "required_focus": [
            "确认 paper account reset、initial_cash、position_seed_ref、paper_broker_model_version 和 paper_account_api_key_scope 是否足够。",
            "确认 paper account state 不会混入 live account facts。",
        ],
        "known_risk": "paper 虚拟账户状态被误读为真实账户、保证金或购买力。",
    },
    "P60-P1-04": {
        "required_focus": [
            "确认 heartbeat、disconnect、reconnect、data_stale、order_event_lag、adapter_error reason code 是否足够。",
            "确认 Google SRE 只作为通用工程来源，不生成交易 hard gate。",
        ],
        "known_risk": "环境健康监控被误读为交易许可或策略有效。",
    },
    "P60-P1-05": {
        "required_focus": [
            "重点审计 canary_scope、stop_condition_ref、rollback_plan_ref、risk_owner、live_execution_owner、manual_review_required 和 residual_gap。",
            "判断是否需要交易系统特定 live canary / broker risk owner 来源才能 reviewed/caveat_only。",
        ],
        "known_risk": "live canary 通过被误读为 full live 或自动扩容许可。",
    },
    "P60-P1-06": {
        "required_focus": [
            "确认 drift report 字段是否足以比较 replay、paper、canary 与 live 差异趋势。",
            "判断是否需要 QuantConnect live reconciliation 或 Nautilus live reconciliation 作为 reviewed 前直接来源。",
        ],
        "known_risk": "environment drift report 被误读为收益证明、交易许可或 hard gate。",
    },
}


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain JSON object")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_candidates() -> tuple[list[dict[str, Any]], list[Path]]:
    pairs: list[tuple[dict[str, Any], Path]] = []
    for partition in PARTITIONS:
        base = repo_path("codex-expert-kit", "rag", "candidates", partition)
        for path in sorted(base.glob("cand_20260617_phase60_p1_*.json")):
            item = read_json(path)
            if item.get("research_task_id") in EXPECTED_TASKS:
                pairs.append((item, path))
    pairs.sort(key=lambda pair: str(pair[0].get("research_task_id")))
    return [item for item, _ in pairs], [path for _, path in pairs]


def build_gap_report(candidates: list[dict[str, Any]], paths: list[Path]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    rows: list[dict[str, Any]] = []
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != EXPECTED_TASKS:
        failures.append({"candidate_id": "package", "path": "", "reason": f"unexpected_task_set:{sorted(actual_tasks ^ EXPECTED_TASKS)}"})

    for candidate, path in zip(candidates, paths, strict=True):
        cid = str(candidate.get("candidate_id", ""))
        task_id = str(candidate.get("research_task_id", ""))
        status = candidate.get("status", {})
        workflow = candidate.get("workflow", {})
        gate = candidate.get("machine_gate", {})
        conflict = candidate.get("conflict_audit", {})
        ai_audit = candidate.get("review", {}).get("ai_audit", {})
        source_count = len(candidate.get("source_refs", []))
        fields = candidate.get("content", {}).get("required_fields_or_contract", [])

        if status.get("review_status") != "accepted_for_draft":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "candidate_not_accepted_for_draft"})
        if workflow.get("queue_group") != "ai_passed":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "candidate_not_ai_passed"})
        if conflict.get("approval_allowed") is not False:
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "conflict_approval_allowed_not_false"})
        if ai_audit.get("decision") != "accepted_for_draft":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "missing_ai_audit_accepted_for_draft"})
        for field in ("reviewed_allowed", "approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append({"candidate_id": cid, "path": rel(path), "reason": f"machine_gate_{field}_not_false"})
        if source_count < 3:
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "source_refs_less_than_3"})
        if len(fields) < 8:
            warnings.append({"candidate_id": cid, "path": rel(path), "reason": "required_fields_or_contract_may_need_more_review_detail"})

        rows.append(
            {
                "candidate_id": cid,
                "research_task_id": task_id,
                "path": rel(path),
                "source_count": source_count,
                "required_field_count": len(fields),
                "reviewed_preparation_expectation": REVIEWED_EXPECTATIONS.get(task_id, {}),
            }
        )

    return {
        "report_id": "phase60_p1_reviewed_preparation_gap_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
        "rows": rows,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "This package may only allow accepted_for_reviewed_caveat_only / needs_more_evidence / rejected / blocked. It must not create approved/default guidance/hard gate.",
    }


def build_package(candidates: list[dict[str, Any]], gap_report: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "created_by": "codex",
        "phase": "Phase 60",
        "task_id": TASK_ID,
        "audit_goal": "严格审计 Phase 60 P1 accepted_for_draft 候选是否可进入 formal reviewed/caveat_only；不得创建 approved、default guidance 或 hard gate。",
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_reviewed": True,
            "reviewed_allowed_only_if_explicitly_accepted_for_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
            "must_search_professional_sources": True,
            "must_check_sources_cases_and_data": True,
        },
        "required_audit_checks": [
            "逐条判断是否可进入 accepted_for_reviewed_caveat_only。",
            "检查 source、content、boundary、conflict patch 是否已被正确回写。",
            "特别检查 P60-P1-02、P60-P1-05、P60-P1-06 是否仍需更多直接来源。",
            "检查是否存在 approval_allowed=true、默认指导、hard gate、交易建议、上线许可或风险阈值。",
            "检查与 Phase 60 P0、Phase 58、Phase 37、Phase 45 的重复、alias 和 owner 边界。",
            "检查中文乱码、mock/test 污染、私有策略参数、账户事实、密钥或实盘敏感信息。",
        ],
        "allowed_decisions": ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"],
        "forbidden_decisions": ["approved", "default_guidance", "hard_gate", "live_permission"],
        "expected_output_schema": {
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
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
            ]
        },
        "gap_report": gap_report,
        "candidates": candidates,
    }


def main() -> int:
    candidates, paths = load_candidates()
    gap_report = build_gap_report(candidates, paths)
    package = build_package(candidates, gap_report)
    package_path = repo_path("docs", "audit", f"{PACKAGE_ID}.json")
    gap_path = repo_path("docs", "reports", "phase60_p1_reviewed_preparation_gap_report.json")
    export_report_path = repo_path("docs", "reports", "phase60_p1_reviewed_preparation_export_report.json")
    write_json(package_path, package)
    write_json(gap_path, gap_report)
    export_report = {
        "report_id": "phase60_p1_reviewed_preparation_export_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "audit_package_path": rel(package_path),
        "gap_report_path": rel(gap_path),
        "gate_status": gap_report["gate_status"],
        "next_action": "Submit reviewed-preparation package for strict external audit.",
    }
    write_json(export_report_path, export_report)
    print(json.dumps(export_report, ensure_ascii=False, indent=2))
    return 0 if gap_report["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
