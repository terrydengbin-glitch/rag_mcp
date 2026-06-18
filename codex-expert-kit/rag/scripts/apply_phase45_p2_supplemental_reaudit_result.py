"""Import Phase 45 P2 supplemental re-audit result.

This script upgrades DATA05 and CRYPTO05 from needs_more_evidence to
accepted_for_draft, then exports a reviewed/caveat_only preparation package for
all eleven Phase 45 P2 candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, legal license conclusions, risk thresholds, liquidation
avoidance advice, or live trading actions.
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
TASK_ID = "CEK-TA-471"
AUDIT_RESULT_ID = "audit_phase45_p2_needs_evidence_supplemental_reaudit_20260612"
SOURCE_PACKAGE_ID = "phase45_p2_needs_evidence_supplemental_reaudit_package_20260612"
REVIEWED_PACKAGE_ID = "phase45_p2_reviewed_preparation_audit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_p2_supplemental_reaudit_import_report.json", start_file=__file__)
REVIEWED_PACKAGE = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_GAP_REPORT = resolve_repo_path("docs", "reports", "phase45_p2_reviewed_preparation_gap_report.json", start_file=__file__)
LINEAGE_CONTRACT = resolve_repo_path("docs", "contracts", "phase45_market_data_ingestion_lineage_contract.md", start_file=__file__)


SUPPLEMENTAL_RESULTS: dict[str, dict[str, Any]] = {
    "P45-G-DATA05": {
        "candidate_id": "cand_20260612_phase45_reference_data_entitlement_p45_g_data05_001",
        "research_task_id": "P45-G-DATA05",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "trade_execution_advice_allowed": False,
        "legal_license_conclusion_allowed": False,
        "reasons": [
            "CEK-TA internal lineage contract 支撑 parser_version、normalization_version、raw_snapshot_digest、lineage_id 等字段本体。",
            "OpenLineage、MLflow、Iceberg、DVC 只作为 lineage / digest / snapshot / reproducibility 模式来源，不是强制工具依赖。",
            "claim 未输出法律授权结论、训练授权结论、数据再分发许可、交易信号或 hard gate。",
        ],
        "required_followups": [
            "进入 reviewed 前必须提供 CEK-TA internal lineage contract 的 contract hash 或 schema extract。",
            "正式文本必须区分 vendor_schema_version 与 internal parser_version / normalization_version。",
            "OpenLineage、MLflow、Iceberg、DVC 只能作为参考模式，不得写成强制技术栈。",
            "market-data license、training use、redistribution permission 必须继续交给 legal/vendor agreement owner 判断。",
        ],
        "patch_notes": {
            "source": [
                "保留 Databento Schemas、Databento Instrument Definitions、Databento Statistics、Nasdaq Symbol Directory。",
                "新增并保留 CEK-TA Market Data Ingestion Lineage Contract。",
                "新增并保留 OpenLineage、MLflow Dataset Tracking / Dataset API、Apache Iceberg、DVC 作为 lineage / digest / snapshot / reproducibility 模式来源。",
            ],
            "content": [
                "保留 vendor、dataset、venue、schema_version、field_dictionary_ref、parser_version、parser_code_hash、normalization_version、normalization_code_hash、raw_snapshot_uri、raw_snapshot_digest、lineage_id、input_dataset_version、output_dataset_version 字段。",
                "明确供应商字段、单位、枚举或语义变化不得静默影响回测、训练、TCA 或实盘审计。",
            ],
            "boundary": [
                "不得输出法律授权结论。",
                "不得输出训练授权结论。",
                "不得输出数据再分发许可。",
                "不得生成交易信号。",
                "不得生成 hard gate。",
            ],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO05": {
        "candidate_id": "cand_20260612_phase45_crypto_perp_p45_h_crypto05_001",
        "research_task_id": "P45-H-CRYPTO05",
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "trade_execution_advice_allowed": False,
        "legal_license_conclusion_allowed": False,
        "reasons": [
            "Binance / Bybit WebSocket 文档支撑 API/WebSocket 断连、heartbeat / ping-pong、连接有效期和限流风险。",
            "Binance maintenance updates 支撑交易所维护窗口来源；Binance Mark Price API 支撑 mark/index 监控字段。",
            "claim 已将 clawback 收窄为 exchange-specific loss-allocation mechanism，未输出清算规避、仓位、杠杆、止损止盈、停机 hard gate、自动解锁或实盘执行建议。",
        ],
        "required_followups": [
            "进入 reviewed 前补具体 exchange status page / incident event source，而不只使用 maintenance announcement list。",
            "进入 reviewed 前补 mark price anomaly 或 index component abnormal handling 的直接规则来源；当前 Mark Price API 只支撑监控字段，不支撑异常处理规则。",
            "若继续使用 clawback 一词，必须补对应 venue rulebook；否则正式文本继续使用 exchange-specific loss-allocation mechanism。",
            "API/WebSocket 风险只能进入 observability / audit checklist，不得变成自动停机 hard gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 Databento Status、OKX Pre-market、Binance ADL、Binance Insurance Fund、Binance Aggregate Trade Streams。",
                "新增并保留 Binance USD-M Futures WebSocket Market Streams、Binance WebSocket API General Info、Binance Maintenance Updates、Bybit WebSocket Connect、Binance Mark Price API。",
            ],
            "content": [
                "将 exchange maintenance / service interruption、api_ws_disconnect、heartbeat_ping_pong_failure、stream_rate_limit、mark_index_monitoring、pre_market_rule、adl_insurance_event、loss_allocation_mechanism 分字段建模。",
                "把 clawback 收窄为 exchange-specific loss-allocation mechanism。",
            ],
            "boundary": [
                "不得输出清算规避建议。",
                "不得输出仓位、杠杆或止损止盈。",
                "不得生成停机 hard gate。",
                "不得生成自动解锁、自动撤单或强平处理动作。",
                "不得把 Binance / Bybit / OKX 规则泛化为所有 crypto venue。",
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


def sanitize_slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value).strip("_")


def proposed_knowledge_id(candidate: dict[str, Any]) -> str:
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id", ""))
    normalized = normalized.replace("phase45_reference_data_entitlement.", "phase45_p2.")
    normalized = normalized.replace("phase45_crypto_perp.", "phase45_p2.")
    normalized = normalized.replace(".v1", "")
    return f"kb_{sanitize_slug(normalized)}.v1"


def candidate_paths() -> list[Path]:
    dirs = [
        resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_02_DATA_ENGINEERING", start_file=__file__),
        resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_03_MARKET_MICROSTRUCTURE", start_file=__file__),
        resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_07_RISK_MANAGEMENT", start_file=__file__),
    ]
    paths: list[Path] = []
    for cand_dir in dirs:
        paths.extend(cand_dir.glob("cand_20260612_phase45_reference_data_entitlement_*.json"))
        paths.extend(cand_dir.glob("cand_20260612_phase45_crypto_perp_*.json"))
    return sorted(paths)


def archive_audit_result() -> None:
    payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 2,
            "accepted_for_draft": 2,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": list(SUPPLEMENTAL_RESULTS.values()),
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
        },
        "global_notes": [
            "DATA05 与 CRYPTO05 可以从 needs_more_evidence 升级为 accepted_for_draft。",
            "本次复审不允许创建 formal reviewed、approved、default guidance 或 hard gate。",
            "后续若转 reviewed/caveat_only，必须另行 reviewed-preparation 审计。",
        ],
    }
    write_json(AUDIT_ARCHIVE, payload)


def update_candidates() -> dict[str, Any]:
    by_task: dict[str, Path] = {}
    for path in candidate_paths():
        data = read_json(path)
        by_task[str(data.get("research_task_id"))] = path

    updated: list[dict[str, Any]] = []
    missing: list[str] = []
    for task_id, result in SUPPLEMENTAL_RESULTS.items():
        path = by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = read_json(path)
        data.setdefault("status", {}).update(
            {
                "review_status": "accepted",
                "ingestion_decision": "accepted_for_draft",
                "decision_reason": "补证二审通过，可进入 accepted_for_draft；不得直接 reviewed/approved/default/hard gate。",
                "updated_at": TODAY,
            }
        )
        review = data.setdefault("review", {})
        review["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": SOURCE_PACKAGE_ID,
            "decision": "accepted_for_draft",
            "confidence": result["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "reasons": result["reasons"],
            "required_followups": result["required_followups"],
            "patch_notes": result["patch_notes"],
        }
        review.setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_p2_supplemental_reaudit_imported",
                "reason": f"{task_id} accepted_for_draft / confidence={result['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        data.setdefault("claim", {})["audit_patch_notes"] = result["patch_notes"]
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "path": repo_relative(path)})

    # Normalize all accepted P2 candidates into the formal draft queue.
    for path in candidate_paths():
        data = read_json(path)
        if data.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            continue
        workflow = data.setdefault("workflow", {})
        workflow["stage"] = "formal_draft_queue"
        workflow["queue_group"] = "ai_passed"
        workflow["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate", "legal_license_conclusion", "risk_threshold_advice", "trade_execution_advice"]
        workflow["conversion_target"] = {
            "proposed_knowledge_id": proposed_knowledge_id(data),
            "target_review_status": "reviewed",
            "target_machine_gate": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
        }
        gate = data.setdefault("machine_gate", {})
        gate["default_guidance"] = "deny"
        gate["approved_allowed"] = False
        gate["default_guidance_allowed"] = False
        gate["hard_gate_allowed"] = False
        gate["risk_threshold_advice_allowed"] = False
        gate["trade_execution_advice_allowed"] = False
        gate["legal_license_conclusion_allowed"] = False
        write_json(path, data)

    return {"updated": updated, "missing": missing}


def contract_payload() -> dict[str, Any]:
    text = LINEAGE_CONTRACT.read_text(encoding="utf-8")
    return {
        "path": repo_relative(LINEAGE_CONTRACT),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "full_text": text,
        "schema_extract": {
            "market_data_ingestion_lineage": [
                "vendor_id",
                "dataset_id",
                "venue",
                "schema_version",
                "field_dictionary_ref",
                "parser_version",
                "parser_code_hash",
                "normalization_version",
                "normalization_code_hash",
                "raw_snapshot_uri",
                "raw_snapshot_digest",
                "lineage_id",
                "input_dataset_version",
                "output_dataset_version",
                "source_license_scope_ref",
            ],
            "crypto_perp_operational_risk_context": [
                "exchange",
                "product",
                "account_mode",
                "maintenance_or_status_ref",
                "api_ws_disconnect_policy_ref",
                "heartbeat_policy_ref",
                "mark_index_monitoring_ref",
                "adl_insurance_event_ref",
                "loss_allocation_mechanism_ref",
                "evidence_source_id",
            ],
        },
    }


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
    for field in (
        "approved_allowed",
        "default_guidance_allowed",
        "hard_gate_allowed",
        "risk_threshold_advice_allowed",
        "trade_execution_advice_allowed",
        "legal_license_conclusion_allowed",
    ):
        if gate.get(field) is not False:
            gaps.append(f"machine_gate.{field}_not_false")
    blob = json.dumps(candidate, ensure_ascii=False)
    if "�" in blob or "????" in blob:
        gaps.append(f"{cid}: possible_mojibake")
    if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
        gaps.append(f"{cid}: possible_secret_private_field")
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
            "batch": "P2 Market Data Entitlement / Reference Data + Crypto Perpetual",
            "candidate_count": len(candidates),
            "source_audit_results": [
                "audit_phase45_p2_candidate_20260612_external_strict",
                AUDIT_RESULT_ID,
            ],
            "target": "判断 11 条 P2 accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "training_license_conclusion_allowed": False,
            "liquidation_avoidance_advice_allowed": False,
            "must_not_generate": ["法律授权结论", "训练授权结论", "买卖点", "仓位", "杠杆", "止损止盈参数", "清算规避", "实盘执行建议", "风险阈值数值", "hard gate"],
        },
        "contract_inline": contract,
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、交易所/供应商/API 文档、数据血缘资料、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance、hard gate、法律授权结论、训练授权结论或交易执行建议。",
            "重点复核 DATA01/DATA05 的 market-data entitlement、training/evaluation license boundary、RAG embedding storage、parser/normalization lineage 与 source digest 边界。",
            "重点复核 CRYPTO03/CRYPTO05 的 maintenance margin/liquidation、API/WebSocket disconnect、exchange maintenance/status、mark/index monitoring、ADL/insurance fund、loss-allocation 机制边界。",
            "检查 Data Engineering、Market Microstructure、Risk Management、Live Execution、AI Engineering、Legal/Vendor Agreement owner 边界是否清晰。",
            "检查是否有中文乱码、mock/test 污染、项目私有参数、账户事实、密钥、交易所私有配置或实盘敏感信息。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": REVIEWED_PACKAGE_ID,
            "summary": {
                "total": 11,
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
                    "trade_execution_advice_allowed": False,
                    "legal_license_conclusion_allowed": False,
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
    expected = {
        "P45-G-DATA01",
        "P45-G-DATA02",
        "P45-G-DATA03",
        "P45-G-DATA04",
        "P45-G-DATA05",
        "P45-G-DATA06",
        "P45-H-CRYPTO01",
        "P45-H-CRYPTO02",
        "P45-H-CRYPTO03",
        "P45-H-CRYPTO04",
        "P45-H-CRYPTO05",
    }
    actual = {str(item.get("research_task_id")) for item in candidates}
    if len(candidates) != 11:
        failures.append(f"expected 11 accepted_for_draft candidates, got {len(candidates)}")
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    contract = contract_payload()
    if not contract["sha256"]:
        failures.append("contract_sha256_missing")
    for candidate in candidates:
        for gap in candidate_gaps(candidate):
            failures.append(f"{candidate.get('candidate_id')}: {gap}")
    gate = {
        "gate_id": "phase45_p2_reviewed_preparation_gap_report",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": REVIEWED_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 11,
        "contract_path": contract["path"],
        "contract_sha256": contract["sha256"],
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只请求 reviewed/caveat_only 准备审计；不得创建 approved、default guidance、hard gate、法律授权结论、训练授权结论或交易执行建议。",
            "P2 reviewed 仍只能作为数据授权/reference data/crypto perpetual 风险审计上下文，不得生成交易许可、仓位、杠杆、清算规避或法律许可结论。",
        ],
    }
    write_json(REVIEWED_GAP_REPORT, gate)
    write_json(REVIEWED_PACKAGE, build_reviewed_package(candidates, gate, contract))
    return gate


def main() -> int:
    archive_audit_result()
    update_report = update_candidates()
    candidates = load_reviewed_prep_candidates()
    gate = export_reviewed_package(candidates)
    report = {
        "report_id": "phase45_p2_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "updated": update_report["updated"],
        "missing": update_report["missing"],
        "accepted_for_draft_total": len(candidates),
        "reviewed_preparation_package": repo_relative(REVIEWED_PACKAGE),
        "reviewed_preparation_gap_report": repo_relative(REVIEWED_GAP_REPORT),
        "reviewed_preparation_gate_status": gate["gate_status"],
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "legal_license_conclusion_enabled": False,
        "trade_execution_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" and not update_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
