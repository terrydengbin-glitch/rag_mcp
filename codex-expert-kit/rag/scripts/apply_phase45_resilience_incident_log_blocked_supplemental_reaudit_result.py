"""Apply Phase 45 Resilience / Incident / Log blocked supplemental re-audit.

This materializes OPS04 and OPS06 as formal reviewed/caveat_only knowledge
after the strict supplemental re-audit accepted both items. It does not create
approved knowledge, default guidance, hard gates, risk thresholds, stop
thresholds, legal compliance conclusions, or live trading actions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import apply_phase45_resilience_incident_log_reviewed_preparation_result as base  # noqa: E402


TODAY = "2026-06-12"
TASK_ID = "CEK-TA-464"
AUDIT_RESULT_ID = "audit_phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_20260612"
PACKAGE_ID = "phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_package_20260612"

base.AUDIT_RESULT_ID = AUDIT_RESULT_ID
base.SOURCE_PACKAGE_ID = PACKAGE_ID

AUDIT_RESULT_ARCHIVE = base.resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = base.resolve_repo_path(
    "docs", "reports", "phase45_resilience_incident_log_blocked_supplemental_reaudit_import_report.json", start_file=__file__
)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-D-OPS04",
        "candidate_id": "cand_20260612_phase45_resilience_incident_log_p45_d_ops04_001",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": [
            "上轮 blocked 点已修复：statement 已明确为 CEK-TA reviewed/caveat_only 内部事故 taxonomy，而不是外部监管或标准强制分类。",
            "taxonomy 使用范围已限制为 audit、review、priority queue、post-incident review、RAG 检索上下文。",
            "claim 明确不得自动触发交易动作、风控阈值、停机阈值、拒单、撤单、重发订单或 hard gate。",
            "Reg SCI、NIST、Google SRE 只作为事故响应和复盘框架来源；具体 taxonomy 字段由 CEK-TA runtime contract 提供本体来源，来源分工合理。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留：该 taxonomy 是 CEK-TA internal taxonomy，不是监管原文分类。",
            "正式文本必须保留：taxonomy label 只能进入 audit/review/priority queue，不得进入 execution gate。",
            "如未来扩展为自动化治理，必须另开任务重新审计，不得从本条推导 hard gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 NIST SP 800-61、Reg SCI、FINRA 4370、Google SRE Postmortem Culture。",
                "CEK-TA runtime contract 作为 incident_taxonomy schema 的字段本体来源。",
            ],
            "content": [
                "保留 system_availability、data_quality、order_and_fill、risk_policy、account_and_funding、external_dependency、market_state、human_action 八类为 CEK-TA 内部建议分类。",
                "保留 category、impact_area、affected_system、market_impact、data_quality、order_state、human_action、audit_trace_id 字段。",
            ],
            "boundary": [
                "不得生成交易动作。",
                "不得生成风控阈值。",
                "不得生成停机阈值。",
                "不得生成拒单、撤单、重发订单或 hard gate。",
            ],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-D-OPS06",
        "candidate_id": "cand_20260612_phase45_resilience_incident_log_p45_d_ops06_001",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": [
            "上轮缺口已补齐：SEC Rule 17a-4、FINRA 4511、CFTC 1.31 已纳入，足以支撑金融记录保存、电子记录、audit trail、真实性、可靠性和生产要求的 caveat_only 边界。",
            "NIST SP 800-92 被正确限定为通用 log management 来源。",
            "OpenTelemetry 被正确限定为 observability/telemetry 来源，不再被误用为金融审计账本或 retention 标准。",
            "CEK-TA runtime contract 提供 audit_ledger_event schema 和 log layer boundaries，外部监管/标准来源提供 supporting evidence，来源分工合理。",
            "claim 已明确 debug_log、telemetry_log、incident_log、audit_ledger、order_truth_source 分层；普通 debug 日志不能替代 audit ledger，audit ledger 也不能替代 broker/venue/order source of truth。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 jurisdiction_scope，不得给出统一 retention 数值。",
            "正式文本必须保留：SEC/FINRA/CFTC 来源具有美国 broker-dealer、FINRA member、CFTC records entity 等适用边界。",
            "正式文本必须保留：audit ledger 不得推导交易许可、不得触发 hard gate、自动恢复、自动撤单或自动重发。",
            "如外接项目不受 SEC/FINRA/CFTC 管辖，应由其 jurisdiction/platform/compliance owner 提供等价记录保存规则。",
        ],
        "patch_notes": {
            "source": [
                "保留 SEC Rule 17a-4 / SEC electronic recordkeeping amendments。",
                "保留 FINRA Rule 4511。",
                "保留 CFTC Regulation 1.31。",
                "保留 NIST SP 800-92 作为通用日志治理来源。",
                "保留 OpenTelemetry 作为 telemetry/traces/metrics/logs 来源。",
                "CEK-TA runtime contract 作为 audit_ledger_event schema 字段本体来源。",
            ],
            "content": [
                "保留 retention_policy_ref、jurisdiction_scope、完整性校验、访问/删除审计、关联 ID、时间源、归档恢复和最小必要字段。",
                "保留 debug_log、telemetry_log、incident_log、audit_ledger、order_truth_source 分层。",
                "保留 audit ledger 不能替代 broker/venue/order source of truth。",
            ],
            "boundary": [
                "不得写死 retention 数值。",
                "不得输出交易许可。",
                "不得触发 hard gate。",
                "不得自动恢复、自动撤单或自动重发订单。",
            ],
            "conflict": [],
        },
    },
]


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 2,
            "accepted_for_reviewed_caveat_only": 2,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
        },
        "candidate_results": RESULTS,
    }


def candidate_path(result: dict[str, Any]) -> Path:
    partition = "KB_AI_26_DATABASE_STORAGE" if result["research_task_id"] == "P45-D-OPS06" else "KB_06_LIVE_EXECUTION"
    candidate_dir = base.resolve_repo_path(
        "codex-expert-kit",
        "rag",
        "candidates",
        partition,
        start_file=__file__,
    )
    for path in sorted(candidate_dir.glob("cand_20260612_phase45_resilience_incident_log_*.json")):
        item = base.read_json(path)
        if item.get("candidate_id") == result["candidate_id"] or item.get("research_task_id") == result["research_task_id"]:
            return path
    return candidate_dir / f"{result['candidate_id']}.json"


def formal_path_for(formal_item: dict[str, Any]) -> Path:
    partition = str(formal_item["metadata"]["partition_id"])
    knowledge_dir = base.resolve_repo_path("codex-expert-kit", "rag", "knowledge", partition, start_file=__file__)
    return knowledge_dir / base.sanitize_filename(formal_item["knowledge_id"])


def update_candidate(candidate: dict[str, Any], result: dict[str, Any], formal_item: dict[str, Any], formal_path: Path) -> None:
    candidate["status"]["review_status"] = "formalized"
    candidate["status"]["ingestion_decision"] = "formal_reviewed_created"
    candidate["status"]["decision_reason"] = "blocked supplemental re-audit 通过，已创建 formal reviewed/caveat_only。"
    candidate["status"]["updated_at"] = TODAY
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "decision": result["decision"],
        "confidence": result["confidence"],
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "reasons": result["reasons"],
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit_and_codex",
            "action": "phase45_resilience_incident_log_blocked_supplemental_reaudit_formalized",
            "reason": "blocked supplemental re-audit accepted this item for formal reviewed/caveat_only.",
            "audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": formal_item["knowledge_id"],
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "formalized_reviewed"
    workflow["queue_group"] = "formalized"
    workflow["formal_knowledge_id"] = formal_item["knowledge_id"]
    workflow["formal_review_status"] = "reviewed"
    workflow["formal_knowledge_path"] = base.repo_relative(formal_path)
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["risk_threshold_advice_allowed"] = False


def main() -> int:
    base.write_json(AUDIT_RESULT_ARCHIVE, audit_result_payload())
    promoted: list[dict[str, Any]] = []
    failures: list[str] = []

    for result in RESULTS:
        path = candidate_path(result)
        if not path.exists():
            failures.append(f"{result['research_task_id']}: candidate file not found: {path}")
            continue
        candidate = base.read_json(path)
        formal_item = base.build_formal_item(candidate, result)
        formal_path = formal_path_for(formal_item)
        base.write_json(formal_path, formal_item)
        update_candidate(candidate, result, formal_item, formal_path)
        base.write_json(path, candidate)
        promoted.append(
            {
                "research_task_id": result["research_task_id"],
                "candidate_id": result["candidate_id"],
                "knowledge_id": formal_item["knowledge_id"],
                "formal_path": base.repo_relative(formal_path),
                "review_status": "reviewed",
                "review_mode": "caveat_only",
            }
        )

    report = {
        "report_id": "phase45_resilience_incident_log_blocked_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": PACKAGE_ID,
        "promoted_count": len(promoted),
        "failures": failures,
        "promoted": promoted,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
        "automatic_live_action_enabled": False,
    }
    base.write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == 2 and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
