"""Apply Phase 60 P1 supplemental reviewed/caveat_only audit result.

This script materializes the remaining three Phase 60 P1 candidates as
formal reviewed/caveat_only knowledge after strict supplemental reaudit.
It never creates approved knowledge, default guidance, hard gates, live
permission, trading advice, or risk-threshold advice.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-18"
TASK_ID = "CEK-TA-588"
AUDIT_RESULT_ID = "audit_result_phase60_p1_needs_evidence_supplemental_reaudit_20260618_strict_v1"
PACKAGE_ID = "phase60_p1_needs_evidence_supplemental_reaudit_package_20260618"


ACCEPTED_TARGETS: dict[str, dict[str, Any]] = {
    "P60-P1-02": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_p1_replay_scenario_library_versioned_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.scenario_library.versioned_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.scenario_library.versioned_required.v1.json"),
        "confidence": "medium_high",
        "required_followups": [
            "正式写入 reviewed/caveat_only 时保留 scenario_result_not_profit_evidence=true。",
            "保留 scenario_library_not_live_permission=true。",
            "标注 DVC / MLflow / pytest 为通用工程来源，ABIDES 为研究模拟器来源。",
            "与 Phase 37 replay/simulation 做 alias 或测试治理子项映射。",
        ],
        "patch_notes": {
            "source": [
                "DVC 支撑数据版本和可复现 pipeline。",
                "MLflow 支撑 dataset tracking、versioning 和 lineage。",
                "pytest 支撑参数化场景测试。",
                "ABIDES 支撑高保真市场模拟、可配置 latency 和 scenario-style experiment。",
            ],
            "content": [
                "scenario library 是测试覆盖和复现证据，不是策略有效证据。",
                "scenario schema 可以包含 scenario_id、dataset_version、event_clock、seed、assumption_hash、expected_observation。",
            ],
            "boundary": [
                "不得收益证明。",
                "不得 live-ready。",
                "不得 hard gate。",
                "不得交易许可。",
            ],
            "conflict": [
                "与 Phase 37 replay/simulation 不冲突，应作为 replay 测试治理补充。",
            ],
        },
    },
    "P60-P1-05": {
        "candidate_path": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_p1_live_canary_rollback_owner_required_001.json"),
        "knowledge_id": "kb_phase60_risk_management.live_canary.rollback_owner_required.v1",
        "knowledge_path": ("KB_07_RISK_MANAGEMENT", "kb_phase60_risk_management.live_canary.rollback_owner_required.v1.json"),
        "confidence": "medium_high",
        "required_followups": [
            "正式写入 reviewed/caveat_only 时保留 canary_not_full_live_permission=true。",
            "保留 manual_review_required=true。",
            "标注 Google SRE / LaunchDarkly 为软件部署来源，FIA / CFTC 为行业/监管治理来源。",
            "项目落地时必须补 venue-specific broker/exchange risk owner mapping。",
        ],
        "patch_notes": {
            "source": [
                "Google SRE / LaunchDarkly 支撑 canary 小范围发布、监控和回滚模式。",
                "FIA / CFTC 支撑自动化交易风险控制、系统保护和治理责任。",
            ],
            "content": [
                "live canary 是小范围真实环境观察阶段，不是 full live。",
                "必须记录 scope、stop_condition_ref、rollback_plan_ref、risk_owner、live_execution_owner、manual_review_required 和 residual_gap。",
            ],
            "boundary": [
                "不得自动扩大为 full live。",
                "不得上线许可。",
                "不得交易许可。",
                "不得 hard gate。",
                "不得风险阈值建议。",
            ],
            "conflict": [
                "与 Phase 60 PromotionDecision / Risk owner 边界一致。",
                "与 Live Execution owner 不冲突，真实执行事实仍归 Live Execution owner。",
            ],
        },
    },
    "P60-P1-06": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_p1_environment_drift_monitor_required_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.environment_drift.monitor_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.environment_drift.monitor_required.v1.json"),
        "confidence": "high",
        "required_followups": [
            "正式写入 reviewed/caveat_only 时保留 drift_report_not_live_permission=true。",
            "保留 human_review_required。",
            "与 Phase 58 / Phase 60 P0 gap report 建立 drift 子报告关系。",
            "标注 QuantConnect / NautilusTrader 为平台或框架来源，不得泛化为所有 broker。",
        ],
        "patch_notes": {
            "source": [
                "QuantConnect live reconciliation 支撑 model prediction 与 live brokerage execution 偏差。",
                "NautilusTrader live reconciliation 支撑 venue state 与 internal state 对齐。",
                "Google SRE 可作为 drift monitor 的通用监控来源。",
            ],
            "content": [
                "environment drift report 应覆盖 fill、fee、latency、reject、cancel、order_state、data_staleness、risk_event 等差异趋势。",
                "drift report 是治理和人工复核材料。",
            ],
            "boundary": [
                "不得收益证明。",
                "不得交易许可。",
                "不得 hard gate。",
                "不得 live permission。",
            ],
            "conflict": [
                "与 Phase 58 / Phase 60 P0 gap report 一致，应作为 drift 子报告。",
                "与 Live Execution owner 不冲突，真实订单和仓位 reconciliation 仍归 Live Execution owner。",
            ],
        },
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


def load_base_module() -> Any:
    path = Path(__file__).with_name("apply_phase60_reviewed_preparation_result.py")
    spec = importlib.util.spec_from_file_location("phase60_apply_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.TODAY = TODAY
    module.TASK_ID = TASK_ID
    module.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    module.PACKAGE_ID = PACKAGE_ID
    return module


def candidate_path(parts: tuple[str, str]) -> Path:
    return repo_path("codex-expert-kit", "rag", "candidates", *parts)


def knowledge_path(parts: tuple[str, str]) -> Path:
    return repo_path("codex-expert-kit", "rag", "knowledge", *parts)


def build_audit_result() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_audit_and_codex_structured_backwrite",
        "phase": "Phase 60",
        "task_id": TASK_ID,
        "summary": {
            "total": 3,
            "accepted_for_reviewed_caveat_only": 3,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_caveat_only_maximum": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "live_permission_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "candidate_results": [
            {
                "candidate_id": read_json(candidate_path(target["candidate_path"])).get("candidate_id"),
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": target["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "live_permission_allowed": False,
                "trade_execution_advice_allowed": False,
                "risk_threshold_advice_allowed": False,
                "formal_knowledge_id": target["knowledge_id"],
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            }
            for task_id, target in ACCEPTED_TARGETS.items()
        ],
    }


def validate_formal_items(paths: list[str], candidate_paths: list[str]) -> list[dict[str, str]]:
    failures: list[dict[str, str]] = []
    for path_text in paths:
        item = read_json(repo_path(*path_text.split("/")))
        gate = item.get("machine_gate", {})
        review = item.get("review", {})
        if review.get("review_status") != "reviewed":
            failures.append({"path": path_text, "reason": "formal_not_reviewed"})
        if gate.get("default_guidance") != "caveat_only":
            failures.append({"path": path_text, "reason": "default_guidance_not_caveat_only"})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append({"path": path_text, "reason": f"{field}_not_false"})
    for path_text in candidate_paths:
        candidate = read_json(repo_path(*path_text.split("/")))
        if candidate.get("status", {}).get("review_status") != "formalized":
            failures.append({"path": path_text, "reason": "candidate_not_formalized"})
    return failures


def main() -> int:
    base = load_base_module()
    audit_result_path = repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json")
    write_json(audit_result_path, build_audit_result())

    created: list[str] = []
    formalized_candidates: list[str] = []
    for _, target in ACCEPTED_TARGETS.items():
        cpath = candidate_path(target["candidate_path"])
        kpath = knowledge_path(target["knowledge_path"])
        candidate = read_json(cpath)
        if candidate.get("status", {}).get("review_status") not in {"needs_more_evidence", "accepted_for_draft", "accepted"}:
            raise ValueError(f"{cpath} has unexpected review_status: {candidate.get('status', {}).get('review_status')}")
        formal = base.build_formal(candidate, target)
        write_json(kpath, formal)
        write_json(cpath, base.update_formalized_candidate(candidate, target))
        created.append(rel(kpath))
        formalized_candidates.append(rel(cpath))

    failures = validate_formal_items(created, formalized_candidates)
    report = {
        "schema_version": "phase60_p1_supplemental_reaudit_import_report.v1",
        "task_id": TASK_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": rel(audit_result_path),
        "created_formal_knowledge_count": len(created),
        "created_formal_knowledge": created,
        "formalized_candidates": formalized_candidates,
        "failure_count": len(failures),
        "failures": failures,
        "boundary": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "task_completion_status": "phase60_p1_all_reviewed_caveat_only_created",
        "next_action": "Rebuild indexes, fixtures, and run Phase 60 P1 runtime linkage validation.",
        "gate_status": "pass" if not failures else "fail",
    }
    report_path = repo_path("docs", "reports", "phase60_p1_supplemental_reaudit_import_report.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
