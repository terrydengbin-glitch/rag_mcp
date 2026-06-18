"""Import Phase 45 STRESS04 margin/funding third-audit result.

This upgrades P45-E-STRESS04 from needs_more_evidence to accepted_for_draft
and exports a reviewed/caveat_only preparation package for all six P45-E
Stress Testing / Scenario Risk candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk thresholds, position advice, stop-loss/take-profit
parameters, trade permission, or live trading actions.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-12"
PHASE = "45"
TASK_ID = "CEK-TA-466"
PARTITION = "KB_07_RISK_MANAGEMENT"

AUDIT_RESULT_ID = "audit_phase45_stress04_margin_funding_reaudit_20260612"
SOURCE_PACKAGE_ID = "phase45_stress_scenario_stress04_margin_funding_reaudit_package_20260612"
REVIEWED_PACKAGE_ID = "phase45_stress_scenario_reviewed_preparation_audit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_stress_scenario_stress04_margin_funding_reaudit_import_report.json", start_file=__file__
)
REVIEWED_PACKAGE = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_GAP_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_stress_scenario_reviewed_preparation_gap_report.json", start_file=__file__
)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase45_stress_scenario_risk_contract.md", start_file=__file__)


STRESS04_RESULT: dict[str, Any] = {
    "candidate_id": "cand_20260612_phase45_stress_scenario_p45_e_stress04_001",
    "research_task_id": "P45-E-STRESS04",
    "decision": "accepted_for_draft",
    "confidence": "high",
    "reviewed_allowed": False,
    "approved_allowed": False,
    "default_guidance_allowed": False,
    "hard_gate_allowed": False,
    "risk_threshold_advice_allowed": False,
    "reasons": [
        "CME Product Margins 支撑 futures/clearing margin/performance bond 会随产品和市场波动变化。",
        "IBKR Available for Trading Values 支撑 broker/account-specific Available Funds、Excess Liquidity、Buying Power、Initial Margin、Maintenance Margin、Overnight Available Funds 等字段边界。",
        "Binance USD-M Futures Account Information、Funding Info、Balance and Position Update 支撑 crypto futures availableBalance、marginAvailable、fundingIntervalHours、funding fee balance update 等 venue/account-mode/funding-interval-specific 语义。",
        "claim 已将保证金/融资变化收窄为 broker、venue、clearing、account-mode 或 funding-interval specific 的情景维度，并要求直接来源和字段版本。",
        "claim 明确不得输出隔夜持仓建议、止损止盈、仓位调整、session 阈值或 hard gate。",
    ],
    "required_followups": [
        "保留 caveat：CME 只支撑 CME futures/clearing margin 语境，不能泛化为所有交易所或所有资产。",
        "保留 caveat：IBKR 是 broker/account field 示例，不能泛化为所有 broker。",
        "保留 caveat：Binance USD-M Futures 是 crypto futures venue/account-mode/funding interval 示例，不能泛化为所有 crypto 或传统期货融资语义。",
        "要求外接项目为自己的 broker、venue、clearing、account-mode、funding interval 提供版本化字段来源。",
        "如未来进入 reviewed，需要补 CEK-TA stress_scenario_event / session_gap_risk schema extract 或 contract hash。",
    ],
    "patch_notes": {
        "source": [
            "保留 Nasdaq halt/pause order handling、NYSE MWCB FAQ、CME trading hours、FIA automated trading risk controls、CME/BCBS stress testing 背景来源。",
            "新增并保留 CME Product Margins、IBKR Available for Trading Values、Binance USD-M Futures Account Information、Binance Funding Info、Binance Balance and Position Update。",
            "Investopedia gap risk 只能作为辅助教育来源，不能作为 reviewed 级主证据。",
        ],
        "content": [
            "保留按市场与 venue 分开声明的结构。",
            "保留传统交易所、期货 session、crypto 24/7 市场差异。",
            "保留保证金/融资变化只能作为 broker、venue、clearing、account-mode 或 funding-interval specific scenario dimension。",
            "保留直接来源和字段版本要求。",
        ],
        "boundary": [
            "不得输出风险阈值。",
            "不得输出隔夜持仓建议。",
            "不得输出止损止盈。",
            "不得输出仓位调整。",
            "不得输出交易许可。",
            "不得输出 hard gate。",
        ],
        "conflict": [],
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
    return sorted(CANDIDATE_DIR.glob("cand_20260612_phase45_stress_scenario_*.json"))


def sanitize_slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def proposed_knowledge_id(candidate: dict[str, Any]) -> str:
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id", ""))
    normalized = normalized.replace("phase45_stress_scenario.", "").replace(".v1", "")
    return f"kb_phase45_stress_scenario.{sanitize_slug(normalized)}.v1"


def contract_payload() -> dict[str, Any]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    return {
        "path": repo_relative(CONTRACT_PATH),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "full_text": text,
        "schema_extract": {
            "stress_scenario_event": [
                "scenario_id",
                "scenario_type",
                "owner",
                "market",
                "venue",
                "source_refs",
                "scenario_assumption_version",
                "data_version",
                "calendar_or_session_version",
                "audit_trace_id",
            ],
            "liquidity_stress_context": [
                "market_depth_source_id",
                "spread_source_id",
                "venue_availability_source_id",
                "funding_source_id",
                "collateral_source_id",
                "unknown_component_policy",
            ],
            "correlation_stress_assumption": [
                "assumption_type",
                "normal_sample_window_ref",
                "stress_window_ref",
                "assumption_source_refs",
                "not_a_threshold",
                "not_a_trade_action",
            ],
            "session_gap_risk": [
                "market_type",
                "venue",
                "session_timezone",
                "close_time",
                "open_time",
                "halt_or_pause_event_ref",
                "auction_or_reopen_event_ref",
                "holiday_or_early_close_calendar_ref",
                "order_acceptance_rule_ref",
                "margin_or_performance_bond_source_ref",
                "broker_account_field_source_ref",
                "funding_interval_source_ref",
                "funding_fee_event_source_ref",
                "field_version",
                "not_position_advice",
                "not_hard_gate",
            ],
            "tail_loss_review": [
                "risk_measure",
                "measure_definition_ref",
                "liquidity_horizon_ref",
                "sample_window_ref",
                "out_of_sample_ref",
                "not_a_threshold",
                "not_trade_permission",
                "not_hard_gate",
            ],
            "stress_result_governance": [
                "stress_result_id",
                "risk_review_input",
                "owner_decision_input",
                "scenario_backlog_input",
                "trade_permission",
                "hard_gate",
                "default_guidance",
            ],
        },
    }


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 1,
            "accepted_for_draft": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [STRESS04_RESULT],
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
    }
    write_json(AUDIT_ARCHIVE, result)
    return result


def update_candidates() -> dict[str, Any]:
    updated: list[dict[str, Any]] = []
    missing: list[str] = []
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}

    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        paths_by_task[task_id] = path
        data_by_task[task_id] = data

    task_id = STRESS04_RESULT["research_task_id"]
    path = paths_by_task.get(task_id)
    if not path:
        missing.append(task_id)
    else:
        data = data_by_task[task_id]
        data["status"]["review_status"] = "accepted"
        data["status"]["ingestion_decision"] = "accepted_for_draft"
        data["status"]["decision_reason"] = STRESS04_RESULT["reasons"][0]
        data["status"]["updated_at"] = TODAY
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": SOURCE_PACKAGE_ID,
            "decision": "accepted_for_draft",
            "confidence": STRESS04_RESULT["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "reasons": STRESS04_RESULT["reasons"],
            "required_followups": STRESS04_RESULT["required_followups"],
            "patch_notes": STRESS04_RESULT["patch_notes"],
        }
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_stress04_margin_funding_reaudit_imported",
                "reason": "accepted_for_draft / confidence=high",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "path": repo_relative(path)})

    for task_id, data in data_by_task.items():
        if not task_id.startswith("P45-E-STRESS"):
            continue
        if data.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            continue
        path = paths_by_task[task_id]
        data.setdefault("workflow", {})["stage"] = "formal_draft_queue"
        data["workflow"]["queue_group"] = "ai_passed"
        data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        data["workflow"]["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate", "risk_threshold_advice"]
        data["workflow"]["conversion_target"] = {
            "proposed_knowledge_id": proposed_knowledge_id(data),
            "target_review_status": "reviewed",
            "target_machine_gate": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        }
        data.setdefault("machine_gate", {})["default_guidance"] = "deny"
        data["machine_gate"]["approved_allowed"] = False
        data["machine_gate"]["default_guidance_allowed"] = False
        data["machine_gate"]["hard_gate_allowed"] = False
        data["machine_gate"]["risk_threshold_advice_allowed"] = False
        write_json(path, data)

    return {"updated": updated, "missing": missing}


def load_reviewed_prep_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths():
        data = read_json(path)
        if data.get("status", {}).get("ingestion_decision") == "accepted_for_draft":
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def candidate_gaps(candidate: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    cid = candidate.get("candidate_id", "<unknown>")
    if candidate.get("status", {}).get("review_status") != "accepted":
        gaps.append("status.review_status_not_accepted")
    if candidate.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
        gaps.append("status.ingestion_decision_not_accepted_for_draft")
    if candidate.get("workflow", {}).get("stage") != "formal_draft_queue":
        gaps.append("workflow.stage_not_formal_draft_queue")
    if not candidate.get("workflow", {}).get("conversion_target", {}).get("proposed_knowledge_id"):
        gaps.append("conversion_target.proposed_knowledge_id_missing")
    if len(candidate.get("source_refs", [])) < 3:
        gaps.append("source_refs_less_than_3")
    gate = candidate.get("machine_gate", {})
    if gate.get("default_guidance") != "deny":
        gaps.append("machine_gate.default_guidance_not_deny")
    for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
        if gate.get(field) is not False:
            gaps.append(f"machine_gate.{field}_not_false")
    blob = json.dumps(candidate, ensure_ascii=False)
    if "�" in blob or "????" in blob:
        gaps.append(f"{cid}: possible_mojibake")
    return gaps


def build_reviewed_package(candidates: list[dict[str, Any]], gate: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": REVIEWED_PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_caveat_only_preparation_audit",
        "scope": {
            "phase": "Phase 45",
            "branch": "Trading Engineering",
            "batch": "P45-E Stress Testing / Scenario Risk",
            "candidate_count": len(candidates),
            "source_audit_results": [
                "audit_phase45_stress_scenario_candidate_20260612_external_strict",
                "audit_phase45_stress_scenario_supplemental_reaudit_20260612",
                AUDIT_RESULT_ID,
            ],
            "target": "判断 6 条 Stress Testing / Scenario Risk accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值", "交易许可", "hard gate"],
        },
        "contract_inline": contract,
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、交易所/券商/清算资料、论文、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance、hard gate 或风险阈值建议。",
            "重点复核 STRESS04 的 CME、IBKR、Binance 来源和内部 session_gap_risk contract 是否足以进入 reviewed/caveat_only。",
            "检查 Stress/Scenario Risk 是否只表达压力测试、情景设计、尾部风险、session/gap/funding 证据边界和 risk owner 输入，不混入交易许可、仓位建议或 hard gate。",
            "检查 Risk Management、Live Execution、Market Microstructure、Data Engineering、AI Engineering 的 owner 边界是否清晰。",
            "检查是否有中文乱码、mock/test 污染、项目私有参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
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
                }
            ],
        },
        "quality_gate": gate,
        "candidates": [
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "status": candidate.get("status", {}),
                "workflow": candidate.get("workflow", {}),
                "classification": candidate.get("classification", {}),
                "claim": candidate.get("claim", {}),
                "applicability": candidate.get("applicability", {}),
                "source_refs": candidate.get("source_refs", []),
                "source_quality": candidate.get("source_quality", {}),
                "conflict_audit": candidate.get("conflict_audit", {}),
                "llm_usage_policy": candidate.get("llm_usage_policy", {}),
                "machine_gate": candidate.get("machine_gate", {}),
                "review": candidate.get("review", {}),
                "quality_gate": {"package_ready": not candidate_gaps(candidate), "gaps": candidate_gaps(candidate)},
            }
            for candidate in candidates
        ],
    }


def export_reviewed_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 accepted_for_draft candidates, got {len(candidates)}")
    expected = {f"P45-E-STRESS{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    contract = contract_payload()
    if not contract["sha256"]:
        failures.append("contract_sha256_missing")
    for candidate in candidates:
        for gap in candidate_gaps(candidate):
            failures.append(f"{candidate.get('candidate_id')}: {gap}")
    gate = {
        "gate_id": "phase45_stress_scenario_reviewed_preparation_gap_report",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": REVIEWED_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "contract_path": contract["path"],
        "contract_sha256": contract["sha256"],
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只请求 reviewed/caveat_only 准备审计；不得创建 approved、default guidance、hard gate 或风险阈值建议。",
            "Stress/Scenario reviewed 仍只能作为风险复核、情景设计和证据审计上下文，不得生成交易许可、仓位建议或资金充足性结论。",
        ],
    }
    write_json(REVIEWED_GAP_REPORT, gate)
    write_json(REVIEWED_PACKAGE, build_reviewed_package(candidates, gate, contract))
    return gate


def main() -> int:
    audit_result = archive_audit_result()
    update_report = update_candidates()
    candidates = load_reviewed_prep_candidates()
    gate = export_reviewed_package(candidates)
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_stress_scenario_stress04_margin_funding_reaudit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "source_package_id": SOURCE_PACKAGE_ID,
            "audit_summary": audit_result["summary"],
            "updated": update_report["updated"],
            "missing": update_report["missing"],
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
                "updated_count": len(update_report["updated"]),
                "reviewed_preparation_candidate_count": len(candidates),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" and not update_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
