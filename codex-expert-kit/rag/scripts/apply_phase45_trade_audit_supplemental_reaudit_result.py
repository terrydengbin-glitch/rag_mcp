"""Import Phase 45 Audit Trail supplemental re-audit result.

This script updates P45-B-AUD04 and P45-B-AUD05 from needs_more_evidence to
accepted_for_draft, then exports a reviewed/caveat_only preparation package for
all six P45-B Audit Trail / Clock Sync candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk thresholds, or trading execution advice.
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
TASK_ID = "CEK-TA-460"
AUDIT_RESULT_ID = "audit_phase45_trade_audit_supplemental_reaudit_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_trade_audit_supplemental_reaudit_package_20260612"
REVIEWED_PACKAGE_ID = "phase45_trade_audit_reviewed_preparation_audit_package_20260612"
PARTITIONS = ["KB_02_DATA_ENGINEERING", "KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_trade_audit_supplemental_reaudit_import_report.json", start_file=__file__)
REVIEWED_PACKAGE = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_GAP_REPORT = resolve_repo_path("docs", "reports", "phase45_trade_audit_reviewed_preparation_gap_report.json", start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase45_trade_audit_clock_sync_contract.md", start_file=__file__)


SUPPLEMENTAL_RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260612_phase45_trade_audit_p45_b_aud04_001",
        "research_task_id": "P45-B-AUD04",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": [
            "Kafka delivery semantics、Event Sourcing、CDC/Debezium 足以支撑 event_id、dedup_key、idempotency_key、replay_cursor 和回放不静默覆盖的工程实现层边界。"
        ],
        "required_followups": [
            "Kafka/Event Sourcing/CDC 只是工程实现模式，不是交易监管标准。",
            "event_id、dedup_key、idempotency_key、replay_cursor、correction_event_id 应标记为 CEK-TA 工程字段契约。",
            "reviewed 前仍建议提供内部 schema extract 或 contract hash。",
            "乱序、重复、缺失、延迟事件必须显式标记，不得在 replay/backfill 时覆盖原始事件。",
        ],
        "patch_notes": {
            "source": [
                "SEC/FIX/NIST 支撑监管审计层和协议事件语义。",
                "Kafka/Event Sourcing/Debezium 支撑工程实现层。",
            ],
            "content": [
                "监管审计层与工程实现层拆分合理。",
                "回放或回灌不得静默覆盖原始真实事件可以保留。",
            ],
            "boundary": [
                "不得把幂等、乱序、回放问题归因成策略 alpha 或交易胜率问题。"
            ],
            "conflict": [
                "分区仍可归入 KB_06_LIVE_EXECUTION / audit_trail，并引用 Data Engineering / Storage owner。"
            ],
        },
    },
    {
        "candidate_id": "cand_20260612_phase45_trade_audit_p45_b_aud05_001",
        "research_task_id": "P45-B-AUD05",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": [
            "SEC Rule 17a-4、FINRA 17a-4 chart 和 AWS Object Lock 足以支撑 retention、WORM/audit-trail alternative、modification/deletion audit 和 object retention implementation 的 draft 级边界。"
        ],
        "required_followups": [
            "不得输出具体保留年限作为通用规则。",
            "SEC/FINRA 17a-4 是美国 broker-dealer / SBS recordkeeping 语境，不可泛化到所有市场。",
            "AWS Object Lock 只是对象存储实现示例，不是 CEK-TA mandatory storage。",
            "reviewed 前建议补充内部 storage contract：retention_policy、record_class、integrity_check、archive_restore_path、access_audit。",
        ],
        "patch_notes": {
            "source": [
                "SEC 17a-4 / FINRA chart 支撑 WORM 或 audit-trail alternative。",
                "AWS Object Lock 支撑对象级 retention/immutability 实现示例。",
                "SEC 613 / NIST 800-92 继续作为交易审计和日志治理 supporting source。",
            ],
            "content": [
                "普通应用日志不能在缺少修改/删除审计、保留策略和可重建原始记录能力时被当作可审计 ledger 可以保留。"
            ],
            "boundary": [
                "不得输出合规结论、通用保留年限或实盘硬规则。"
            ],
            "conflict": [
                "KB_AI_26_DATABASE_STORAGE 承接 storage integrity，但服务 Trading Engineering audit trail。"
            ],
        },
    },
]


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
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_trade_audit_*.json")))
    return paths


def sanitize_slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", value).strip("_")


def proposed_knowledge_id(candidate: dict[str, Any]) -> str:
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id", ""))
    normalized = normalized.replace("phase45_trade_audit.", "").replace(".v1", "")
    return f"kb_phase45_trade_audit.{sanitize_slug(normalized)}.v1"


def contract_payload() -> dict[str, Any]:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    return {
        "path": repo_relative(CONTRACT_PATH),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "full_text": text,
        "schema_extract": {
            "order_event_audit_fields": [
                "event_id",
                "source_system",
                "event_type",
                "event_time",
                "receive_time",
                "log_time",
                "timezone",
                "timestamp_precision",
                "clock_source",
                "clock_drift_status",
                "prev_event_id",
                "parent_event_id",
                "client_order_id",
                "broker_order_id",
                "exchange_order_id",
                "actor",
                "reason_code",
            ],
            "event_sequence_idempotency_fields": [
                "sequence",
                "dedup_key",
                "idempotency_key",
                "replay_cursor",
                "replay_reason",
                "correction_event_id",
                "original_event_id",
                "ordering_status",
                "ingestion_status",
                "raw_event_hash",
            ],
            "retention_integrity_fields": [
                "audit_record_id",
                "record_class",
                "retention_policy_id",
                "jurisdiction_scope",
                "storage_mode",
                "integrity_check",
                "checksum_or_hash",
                "modification_audit_id",
                "deletion_audit_id",
                "access_audit_id",
                "archive_restore_path",
                "legal_hold_status",
                "immutability_exception_reason",
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
            "total": 2,
            "accepted_for_draft": 2,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": SUPPLEMENTAL_RESULTS,
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "global_notes": [
            "AUD04/AUD05 补证后可升级为 accepted_for_draft。",
            "本次复审不允许 reviewed、approved、default guidance 或 hard gate。",
            "后续 reviewed/caveat_only 准备审计必须包含内部 schema extract 或 contract hash。",
        ],
    }
    write_json(AUDIT_RESULT_ARCHIVE, result)
    return result


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
    results_by_task = {str(item["research_task_id"]): item for item in SUPPLEMENTAL_RESULTS}

    for task_id, result in results_by_task.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = data_by_task[task_id]
        data["status"]["review_status"] = "accepted"
        data["status"]["ingestion_decision"] = "accepted_for_draft"
        data["status"]["decision_reason"] = result["reasons"][0]
        data["status"]["updated_at"] = TODAY
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": "accepted_for_draft",
            "confidence": result["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "required_followups": result["required_followups"],
            "patch_notes": result["patch_notes"],
        }
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_trade_audit_supplemental_reaudit_imported",
                "reason": "accepted_for_draft / confidence=high",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "path": repo_relative(path)})

    for task_id, data in data_by_task.items():
        if not task_id.startswith("P45-B-AUD"):
            continue
        if data.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            continue
        path = paths_by_task[task_id]
        data.setdefault("workflow", {})["stage"] = "formal_draft_queue"
        data["workflow"]["queue_group"] = "ai_passed"
        data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        data["workflow"]["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]
        data["workflow"]["conversion_target"] = {
            "proposed_knowledge_id": proposed_knowledge_id(data),
            "target_review_status": "reviewed",
            "target_machine_gate": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
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
            "batch": "P45-B Audit Trail / Clock Sync",
            "candidate_count": len(candidates),
            "source_audit_results": [
                "audit_phase45_trade_audit_p45_b_20260612_external_strict_v1",
                AUDIT_RESULT_ID,
            ],
            "target": "判断 6 条 Audit Trail / Clock Sync accepted_for_draft 候选是否可转 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_compliance_conclusion_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "风险阈值数值", "具体合规结论"],
        },
        "contract_inline": contract,
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、协议文档、标准、案例和数据，对本 reviewed/caveat_only 准备包进行严格审计。",
            "逐条判断是否可进入 formal reviewed/caveat_only；不得允许 approved、default guidance 或 hard gate。",
            "重点复核 AUD04/AUD05 的内部契约、schema extract 和 contract hash 是否足以补齐 reviewed 前置条件。",
            "检查 Audit Trail / Clock Sync 是否只表达审计追踪、时间同步、事件序列、幂等、retention 和完整性边界，不混入策略 alpha、交易许可、风险阈值或法律合规结论。",
            "检查 Data Engineering、Live Execution、Database/Storage、Risk Management 的 owner 边界是否清晰。",
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
                "quality_gate": {
                    "package_ready": not candidate_gaps(candidate),
                    "gaps": candidate_gaps(candidate),
                },
            }
            for candidate in candidates
        ],
    }


def export_reviewed_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 accepted_for_draft candidates, got {len(candidates)}")
    expected = {f"P45-B-AUD{idx:02d}" for idx in range(1, 7)}
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
        "gate_id": "phase45_trade_audit_reviewed_preparation_gap_report",
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
            "本包只请求 reviewed/caveat_only 准备审计；不得创建 approved、default guidance 或 hard gate。",
            "Audit Trail / Clock Sync reviewed 仍只能作为审计追踪、时间同步、事件序列和存储完整性上下文，不得生成交易许可或合规结论。",
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
            "report_id": "phase45_trade_audit_supplemental_reaudit_import_report",
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
