"""Import Phase 45 Layered Risk supplemental re-audit result.

This script upgrades P45-C-RISK05 from needs_more_evidence to
accepted_for_draft, then exports a reviewed/caveat_only preparation package
for all six P45-C Layered Risk / Credit / Margin candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk thresholds, funding sufficiency conclusions, or
trading execution advice.
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
TASK_ID = "CEK-TA-462"
AUDIT_RESULT_ID = "audit_phase45_layered_risk_supplemental_reaudit_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_layered_risk_supplemental_reaudit_package_20260612"
REVIEWED_PACKAGE_ID = "phase45_layered_risk_reviewed_preparation_audit_package_20260612"
PARTITION = "KB_07_RISK_MANAGEMENT"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_layered_risk_supplemental_reaudit_import_report.json", start_file=__file__)
REVIEWED_PACKAGE = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_GAP_REPORT = resolve_repo_path("docs", "reports", "phase45_layered_risk_reviewed_preparation_gap_report.json", start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase45_layered_risk_controls_contract.md", start_file=__file__)


SUPPLEMENTAL_RESULT: dict[str, Any] = {
    "candidate_id": "cand_20260612_phase45_layered_risk_p45_c_risk05_001",
    "research_task_id": "P45-C-RISK05",
    "decision": "accepted_for_draft",
    "confidence": "high",
    "reviewed_allowed": False,
    "approved_allowed": False,
    "default_guidance_allowed": False,
    "hard_gate_allowed": False,
    "risk_threshold_advice_allowed": False,
    "reasons": [
        "CME supports clearing margin/performance bond, IBKR supports broker available funds/excess liquidity/buying power boundaries, and Binance Futures supports crypto venue available balance / margin field boundaries at draft level."
    ],
    "required_followups": [
        "CME 只支撑 CME Clearing / CME Globex / SPAN / performance bond 语境，不得泛化为所有清算或保证金制度。",
        "IBKR 字段只支撑 IBKR broker/account-type 语境，不得泛化为所有 broker。",
        "Binance Futures 字段只支撑 Binance USDⓈ-M Futures/API/account-mode 语境，不得泛化为股票、传统期货、外汇或全部 crypto venue。",
        "不得把任一字段默认为可交易现金应作为 CEK-TA 内部审计边界，而不是 CME/IBKR/Binance 的直接统一结论。",
        "reviewed 前必须引用内部 schema extract 或 contract hash，定义 point-in-time account/margin/collateral evidence。",
    ],
    "patch_notes": {
        "source": [
            "CME SPAN / performance bond 来源支撑 clearing margin 层。",
            "IBKR Available Funds / Excess Liquidity / Buying Power 来源支撑 broker account 字段层。",
            "Binance Futures account/balance 来源支撑 crypto venue account balance 字段层。",
        ],
        "content": [
            "claim 已正确拆分 margin、performance bond、collateral、available funds、buying power、wallet balance、margin balance、strategy capital budget。",
            "保留 point-in-time account/margin/collateral evidence 要求。",
        ],
        "boundary": [
            "不得输出保证金比例、信用额度、可用资金判断、下单许可、仓位、杠杆或实盘执行建议。",
            "不得把 account field check 变成 CEK-TA hard gate。",
        ],
        "conflict": [
            "分区正确：KB_07_RISK_MANAGEMENT / layered_risk_controls。",
            "未发现与 Phase 37 Risk Management、Phase 45 Execution TCA / Audit Trail 或 runtime contract 的直接冲突。",
        ],
    },
}

BINANCE_BALANCE_V2_SOURCE: dict[str, Any] = {
    "source_id": "src_supp_006",
    "source_title": "Futures Account Balance V2",
    "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Futures-Account-Balance-V2",
    "source_type": "official_platform_doc",
    "publisher": "Binance Open Platform",
    "accessed_at": TODAY,
    "reliability": "medium_high",
    "score": 84,
    "freshness": "time_sensitive",
    "relevance": "medium_high",
    "evidence_summary": "Binance USDⓈ-M Futures balance endpoint exposes wallet balance, cross wallet balance, availableBalance, maxWithdrawAmount and marginAvailable fields.",
    "limitations": [
        "Crypto venue/API-specific; field semantics depend on product, account mode and jurisdiction availability."
    ],
    "version": None,
    "quoted_excerpt_allowed": False,
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
    cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
    return sorted(cand_dir.glob("cand_20260612_phase45_layered_risk_*.json"))


def sanitize_slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def proposed_knowledge_id(candidate: dict[str, Any]) -> str:
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id", ""))
    normalized = normalized.replace("phase45_layered_risk.", "").replace(".v1", "")
    return f"kb_phase45_layered_risk.{sanitize_slug(normalized)}.v1"


def contract_payload() -> dict[str, Any]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    return {
        "path": repo_relative(CONTRACT_PATH),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "full_text": text,
        "schema_extract": {
            "layered_pre_trade_control": [
                "control_id",
                "control_layer",
                "owner",
                "control_purpose",
                "evidence_source_id",
                "policy_version",
                "decision_time",
                "result",
                "action_semantics",
                "audit_trace_id",
            ],
            "credit_exposure_boundary": [
                "credit_scope",
                "limit_owner",
                "exposure_measure_id",
                "account_id_ref",
                "policy_version",
                "source_timestamp",
                "snapshot_id",
                "semantic_boundary",
                "audit_trace_id",
            ],
            "order_admission_control": [
                "control_type",
                "venue",
                "instrument_id",
                "control_version",
                "market_state_ref",
                "input_order_id",
                "result",
                "audit_trace_id",
            ],
            "message_pressure_control": [
                "venue",
                "connection_id",
                "message_type",
                "control_type",
                "window_policy_id",
                "measurement_source",
                "result",
                "recovery_policy_ref",
            ],
            "account_margin_collateral_evidence": [
                "account_ref",
                "broker_or_venue",
                "product_scope",
                "account_mode",
                "field_name",
                "source_endpoint_or_report",
                "source_timestamp",
                "receive_timestamp",
                "decision_timestamp",
                "snapshot_id",
                "schema_version",
                "staleness_status",
                "semantic_boundary",
                "owner",
                "audit_trace_id",
            ],
            "post_trade_surveillance_event": [
                "surveillance_event_id",
                "event_type",
                "detected_at",
                "classification",
                "owner",
                "pre_trade_control_refs",
                "audit_trace_id",
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
        "candidate_results": [SUPPLEMENTAL_RESULT],
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "global_notes": [
            "P45-C-RISK05 补证后可从 needs_more_evidence 升级为 accepted_for_draft。",
            "本次复审不允许 reviewed、approved、default guidance 或 hard gate。",
            "后续 reviewed/caveat_only 准备审计必须包含 point-in-time account/margin/collateral evidence 内部契约。",
        ],
    }
    write_json(AUDIT_RESULT_ARCHIVE, result)
    return result


def upsert_source(candidate: dict[str, Any], source: dict[str, Any]) -> None:
    refs = list(candidate.get("source_refs", []))
    urls = {ref.get("source_url") for ref in refs}
    if source.get("source_url") not in urls:
        refs.append(source)
    candidate["source_refs"] = refs
    primary_types = {
        "regulatory_rule",
        "regulatory_guidance",
        "professional_body",
        "official_exchange_doc",
        "official_broker_doc",
        "official_platform_doc",
    }
    primary_count = sum(1 for ref in refs if ref.get("source_type") in primary_types)
    candidate.setdefault("source_quality", {})["primary_source_count"] = primary_count
    candidate["source_quality"]["supporting_source_count"] = len(refs) - primary_count
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 70)) for ref in refs) / len(refs), 2)


def update_candidates() -> dict[str, Any]:
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}
    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        paths_by_task[task_id] = path
        data_by_task[task_id] = data

    missing: list[str] = []
    updated: list[dict[str, Any]] = []
    task_id = SUPPLEMENTAL_RESULT["research_task_id"]
    path = paths_by_task.get(task_id)
    if not path:
        missing.append(task_id)
    else:
        data = data_by_task[task_id]
        upsert_source(data, BINANCE_BALANCE_V2_SOURCE)
        data["status"]["review_status"] = "accepted"
        data["status"]["ingestion_decision"] = "accepted_for_draft"
        data["status"]["decision_reason"] = SUPPLEMENTAL_RESULT["reasons"][0]
        data["status"]["updated_at"] = TODAY
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": "accepted_for_draft",
            "confidence": SUPPLEMENTAL_RESULT["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "required_followups": SUPPLEMENTAL_RESULT["required_followups"],
            "patch_notes": SUPPLEMENTAL_RESULT["patch_notes"],
        }
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_layered_risk_supplemental_reaudit_imported",
                "reason": "accepted_for_draft / confidence=high",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "path": repo_relative(path)})

    for task_id, data in data_by_task.items():
        if not task_id.startswith("P45-C-RISK"):
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
    if candidate.get("research_task_id") == "P45-C-RISK05" and len(candidate.get("source_refs", [])) < 9:
        gaps.append("risk05_source_refs_less_than_9_after_binance_v2_patch")
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
            "batch": "P45-C Layered Risk / Credit / Margin",
            "candidate_count": len(candidates),
            "source_audit_results": [
                "audit_phase45_layered_risk_p45_c_20260612_external_strict_v1",
                AUDIT_RESULT_ID,
            ],
            "target": "判断 6 条 Layered Risk / Credit / Margin accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "funding_sufficiency_conclusion_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值", "信用额度", "保证金比例", "资金充足性结论"],
        },
        "contract_inline": contract,
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、交易所/券商/清算资料、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance、hard gate 或风险阈值建议。",
            "重点复核 RISK05 的 CME、IBKR、Binance 来源和内部 point-in-time account/margin/collateral evidence contract 是否足以进入 reviewed/caveat_only。",
            "检查 Layered Risk 是否只表达分层风控、owner、证据、信用/保证金/账户字段边界和 post-trade/pre-trade 分工，不混入策略 alpha、交易许可或资金充足性结论。",
            "检查 Risk Management、Live Execution、Broker/Venue Adapter、Database/Storage、AI Engineering 的 owner 边界是否清晰。",
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
    expected = {f"P45-C-RISK{idx:02d}" for idx in range(1, 7)}
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
        "gate_id": "phase45_layered_risk_reviewed_preparation_gap_report",
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
            "Layered Risk reviewed 仍只能作为风控设计、owner 边界和证据审计上下文，不得生成交易许可、信用额度或资金充足性结论。",
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
            "report_id": "phase45_layered_risk_supplemental_reaudit_import_report",
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
