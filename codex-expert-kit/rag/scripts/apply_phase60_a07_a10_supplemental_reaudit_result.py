"""Apply Phase 60 A07/A10 supplemental reviewed/caveat_only audit result.

P60-A07 and P60-A10 were previously kept as needs_more_evidence. The
supplemental reaudit accepted both for formal reviewed/caveat_only. This script
materializes exactly those two items and keeps approved/default guidance/hard
gate/live permission disabled.
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


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-579"
AUDIT_RESULT_ID = "audit_result_phase60_a07_a10_supplemental_reaudit_20260617_strict_v1"
PACKAGE_ID = "phase60_a07_a10_supplemental_reaudit_package_20260617"
SOURCE_ATTACHMENT = "C:/Users/dove/.codex/attachments/d1ef31ee-97ec-489a-bfd1-dcab6e4c0536/pasted-text.txt"


TARGETS: dict[str, dict[str, Any]] = {
    "P60-A07": {
        "candidate_path": (
            "KB_07_RISK_MANAGEMENT",
            "cand_20260617_phase60_environment_promotion_evidence_required_001.json",
        ),
        "knowledge_id": "kb_phase60_risk_management.environment_promotion_evidence_required.v1",
        "knowledge_path": (
            "KB_07_RISK_MANAGEMENT",
            "kb_phase60_risk_management.environment_promotion_evidence_required.v1.json",
        ),
        "confidence": "medium_high",
        "required_followups": [
            "正式写入 reviewed/caveat_only 时保留 source limitation：QuantConnect 和 NautilusTrader 只能作为 implementation pattern。",
            "保留 promotion_not_live_permission=true。",
            "存在 residual gap 时必须记录 residual_gap_acceptance_note 和 rollback_plan_ref。",
            "明确 Live reconciliation 归 Live Execution owner，风险接受归 Risk owner / human reviewer。",
        ],
        "patch_notes": {
            "source": [
                "QuantConnect Live Trading Reconciliation 可作为 backtest/paper/live 偏差与 reconciliation 直接来源。",
                "NautilusTrader Live Execution Reconciliation 可作为 venue state 与 internal state 对齐的直接来源。",
                "Nautilus continuous reconciliation 可作为运行期订单和仓位状态持续核对的实现模式来源。",
            ],
            "content": [
                "promotion decision 必须引用 manifest、gap report、reconciliation report、risk review 和人工复核。",
                "promotion decision 是晋级评审证据，不是实盘许可。",
            ],
            "boundary": [
                "不得 approved。",
                "不得 default guidance。",
                "不得 hard gate。",
                "不得 live permission。",
                "不得交易建议或风险阈值建议。",
            ],
            "conflict": [
                "与 Phase 58 environment equivalence manifest 不冲突，应作为 promotion governance 补充。",
                "与 Live Execution owner 不冲突，reconciliation 事实归 Live Execution owner。",
                "与 Risk owner 不冲突，风险接受和人工复核归 Risk owner / human reviewer。",
            ],
        },
    },
    "P60-A10": {
        "candidate_path": (
            "KB_07_RISK_MANAGEMENT",
            "cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json",
        ),
        "knowledge_id": "kb_phase60_risk_management.sandbox_risk_rehearsal_not_hard_gate.v1",
        "knowledge_path": (
            "KB_07_RISK_MANAGEMENT",
            "kb_phase60_risk_management.sandbox_risk_rehearsal_not_hard_gate.v1.json",
        ),
        "confidence": "medium_high",
        "required_followups": [
            "正式写入 reviewed/caveat_only 时保留 Binance source limitation：仅为 Binance USD-M Futures-specific。",
            "保留 FIA source limitation：行业最佳实践，不得转写为法律意见、固定阈值或自动 hard gate。",
            "保留 risk_rehearsal_result_not_hard_gate=true。",
            "补齐 broker_or_exchange_rejection_mapping_source、live_risk_owner_policy_source、kill_switch_or_manual_override_boundary。",
        ],
        "patch_notes": {
            "source": [
                "NautilusTrader RiskEngine / Execution 文档可作为风控链条和 reason-code boundary 的实现模式来源。",
                "Binance USD-M Futures error-code 文档可作为 broker/exchange rejection mapping 的 venue-specific 来源。",
                "FIA 自动化交易风控最佳实践可作为 live risk owner、kill switch、定期复核和系统保护的行业来源。",
            ],
            "content": [
                "risk rehearsal 只能验证字段、策略链条、拒绝原因映射和审计流程。",
                "sandbox / testnet / replay / paper 风控演练不得替代 live risk owner 的真实政策、拒单、停机、解锁或 hard gate。",
            ],
            "boundary": [
                "不得 approved。",
                "不得 default guidance。",
                "不得 hard gate。",
                "不得 live permission。",
                "不得自动拒单、自动停机、自动解锁。",
                "不得生成风险阈值建议。",
            ],
            "conflict": [
                "与 Risk Management owner 不冲突，真实政策和 hard gate 所有权仍归 Risk owner。",
                "与 Live Execution owner 不冲突，真实拒单和交易所返回事实仍归 Live Execution owner。",
                "AI/RAG 只能引用 reason code 和审计证据，不拥有执行或风控许可。",
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
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_phase60_apply_module() -> Any:
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


def write_structured_audit_result(module: Any) -> Path:
    results: list[dict[str, Any]] = []
    for task_id, target in TARGETS.items():
        candidate = read_json(module.candidate_path(target["candidate_path"]))
        results.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": target["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "trade_execution_advice_allowed": False,
                "risk_threshold_advice_allowed": False,
                "live_permission_allowed": False,
                "formal_knowledge_id": target["knowledge_id"],
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            }
        )
    payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "source_attachment": SOURCE_ATTACHMENT,
        "audited_at": TODAY,
        "summary": {
            "total": 2,
            "accepted_for_reviewed_caveat_only": 2,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_caveat_only_maximum": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "candidate_results": sorted(results, key=lambda item: item["research_task_id"]),
    }
    path = repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json")
    write_json(path, payload)
    return path


def main() -> int:
    module = load_phase60_apply_module()
    audit_path = write_structured_audit_result(module)
    created: list[str] = []
    formalized_candidates: list[str] = []

    for task_id, target in TARGETS.items():
        cpath = module.candidate_path(target["candidate_path"])
        kpath = module.knowledge_path(target["knowledge_path"])
        candidate = read_json(cpath)
        if candidate.get("research_task_id") != task_id:
            raise ValueError(f"{cpath} has unexpected research_task_id")
        formal = module.build_formal(candidate, target)
        write_json(kpath, formal)
        write_json(cpath, module.update_formalized_candidate(candidate, target))
        created.append(rel(kpath))
        formalized_candidates.append(rel(cpath))

    report = {
        "schema_version": "phase60_a07_a10_supplemental_reaudit_import_report.v1",
        "task_id": TASK_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": rel(audit_path),
        "created_formal_knowledge_count": len(created),
        "created_formal_knowledge": created,
        "formalized_candidates": formalized_candidates,
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
        "task_completion_status": "all_phase60_p0_candidates_formalized_or_previously_formalized",
        "next_action": "Rebuild formal knowledge index and fixtures, then run CEK-TA-580 runtime linkage validation.",
    }
    report_path = repo_path("docs", "reports", "phase60_a07_a10_supplemental_reaudit_import_report.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
