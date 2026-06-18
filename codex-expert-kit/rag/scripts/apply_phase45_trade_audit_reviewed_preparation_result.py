"""Apply Phase 45 Audit Trail reviewed/caveat_only preparation result.

This task consumes the strict reviewed/caveat_only preparation audit for the
six Phase 45 Audit Trail / Clock Sync candidates. It creates formal
reviewed/caveat_only knowledge only for entries explicitly allowed by the
audit. It never creates approved knowledge, default guidance, hard gates, risk
thresholds, legal compliance conclusions, or trading execution advice.
"""

from __future__ import annotations

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
TASK_ID = "CEK-TA-460"
AUDIT_RESULT_ID = "audit_phase45_trade_audit_reviewed_caveat_only_preparation_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_trade_audit_reviewed_preparation_audit_package_20260612"
PARTITIONS = ["KB_02_DATA_ENGINEERING", "KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]
EXPECTED_TOTAL = 6

AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_trade_audit_formal_import_report.json", start_file=__file__)
REPO_ROOT = resolve_repo_path(".", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-B-AUD01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["SEC Rule 613、CAT 和 FINRA 6820 足以支撑 clock synchronization、reportable event timestamp 和 business clock 同步边界。"],
        "patch_notes": {
            "source": ["SEC/CAT/FINRA 主要适用于美国 NMS/CAT/FINRA member 语境；ESMA/MiFIR 只适用于 EU/MiFIR 语境。"],
            "content": ["字段以内部契约为准：event_time、receive_time、log_time、timezone、timestamp_precision、clock_source、clock_drift_status。"],
            "boundary": ["不得把 CAT/FINRA/ESMA 的精度或漂移阈值写成 CEK-TA 通用硬规则。"],
            "conflict": ["未发现与 Data Engineering / Live Execution / Audit Trail 分区冲突。"],
        },
    },
    {
        "research_task_id": "P45-B-AUD02",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["SEC Rule 613 支撑 order receipt/origination 到 routing、modification、cancellation、execution 的 time-sequenced audit trail；FIX 支撑协议事件语义。"],
        "patch_notes": {
            "source": ["SEC/CAT 支撑监管审计链；FIX Execution Report 只支撑协议事件语义，不替代 venue/broker 事实层。"],
            "content": ["actor、reason_code、source_system 必须标记为 CEK-TA 内部审计字段。"],
            "boundary": ["prev_event_id / parent_event_id 用于因果链，不得被写成策略信号；不得用审计链完整推导策略有效。"],
            "conflict": ["未发现与 Live Execution / Audit Trail 分区冲突。"],
        },
    },
    {
        "research_task_id": "P45-B-AUD03",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["SEC/CAT 支撑 order/customer/reporter 等审计标识；FIX 支撑 OrderID、ClOrdID、OrigClOrdID、ExecID 等协议 ID 语义。"],
        "patch_notes": {
            "source": ["CAT/FIX 来源具有辖区、协议和 venue/broker 实现边界。"],
            "content": ["broker_order_id / exchange_order_id 必须由外接项目事实层提供。"],
            "boundary": ["不得把 CAT 字段直接等同于 crypto exchange 的 client_order_id / exchange_order_id。"],
            "conflict": ["cancel/replace 关联 ID 和 idempotency_key 属于 CEK-TA 工程字段契约。"],
        },
    },
    {
        "research_task_id": "P45-B-AUD04",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["内部契约、schema extract、contract hash 已补齐；Kafka、Event Sourcing、Debezium 足以支撑工程实现层边界。"],
        "patch_notes": {
            "source": ["Kafka/Event Sourcing/CDC 只能作为工程实现模式，不是交易监管标准。"],
            "content": ["event_id、dedup_key、idempotency_key、replay_cursor、correction_event_id 以 CEK-TA 内部契约为准。"],
            "boundary": ["replay/backfill/correction 不得静默覆盖 original_event；exactly-once 等语义不得写成交易所或监管统一保证。"],
            "conflict": ["归入 KB_06_LIVE_EXECUTION / audit_trail，并引用 Data Engineering / Storage owner。"],
        },
    },
    {
        "research_task_id": "P45-B-AUD05",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["SEC Rule 17a-4、FINRA 17a-4 chart、AWS Object Lock 和 NIST SP 800-92 足以支撑 retention / integrity 的 caveat_only 边界。"],
        "patch_notes": {
            "source": ["SEC/FINRA 17a-4 只作为美国 broker-dealer / SBS recordkeeping 语境来源；AWS Object Lock 只是实现示例。"],
            "content": ["retention_policy、record_class、integrity_check、archive_restore_path、access_audit 以内部契约为准。"],
            "boundary": ["不得输出具体 retention 年限、合规结论或实盘硬规则。"],
            "conflict": ["Database/Storage Engineering 只拥有 storage integrity / lifecycle，不拥有策略、订单执行或风控阈值。"],
        },
    },
    {
        "research_task_id": "P45-B-AUD06",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["CAT clock synchronization materials 与 ESMA Article 22c 足以支撑 manual/electronic timestamp boundary；数值必须 jurisdiction-scoped。"],
        "patch_notes": {
            "source": ["CAT/ESMA 来源只能用于对应辖区和报告事件语境。"],
            "content": ["event_class、timestamp_source、granularity、drift_policy_ref、evidence_policy_ref 必须引用内部契约。"],
            "boundary": ["人工录入时间不能替代电子事件时间；电子事件 timestamp 精度也不得泛化到所有人工流程。"],
            "conflict": ["未发现与 Data Engineering / Live Execution / Audit Trail 分区冲突。"],
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


def candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for partition in PARTITIONS:
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_trade_audit_*.json")))
    return paths


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_reviewed_caveat_only": 6,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": "",
                "research_task_id": item["research_task_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": item["reasons"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
        "mandatory_caveats": [
            "SEC/CAT/FINRA 主要适用于美国 NMS/CAT/FINRA member 语境，不能泛化到 crypto、外汇、离岸交易所或所有 broker。",
            "ESMA/MiFIR 只适用于 EU/MiFIR 语境，不能泛化为全球 clock sync 规则。",
            "Kafka/Event Sourcing/CDC/Object Lock 只是工程实现模式，不是交易监管字段契约，也不是 CEK-TA mandatory vendor。",
            "reviewed/caveat_only 只能用于审计链、时间同步、事件序列、幂等、retention 和完整性检查，不能生成交易许可、风控阈值或法律合规结论。",
        ],
    }


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if str(item).strip()]


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    workflow = candidate.get("workflow", {})
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    knowledge_id = str(conversion.get("proposed_knowledge_id") or workflow.get("formal_knowledge_id") or "")
    if not knowledge_id:
        normalized = str(candidate.get("claim", {}).get("normalized_claim", candidate.get("research_task_id", ""))).replace(
            "phase45_trade_audit.", ""
        )
        knowledge_id = f"kb_phase45_trade_audit.{re.sub(r'[^a-zA-Z0-9_.-]+', '_', normalized)}.v1"
    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    patch_notes = result["patch_notes"]
    source_refs = candidate.get("source_refs", [])
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(claim.get("title") or candidate.get("research_task_id")),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": "trade_audit_boundary_rule",
            "claim_type": classification.get("claim_type"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification.get("tree_node_id"),
            "tree_path": classification.get("tree_path"),
            "canonical_node_id": classification.get("canonical_node_id"),
            "canonical_tree_path": classification.get("tree_path"),
            "risk_level": "medium_high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 45",
            "classification_notes": "Phase 45 Audit Trail / Clock Sync formal reviewed/caveat_only；只用于审计链、时间同步、事件序列、幂等、retention 和完整性检查，不是 approved/default guidance/hard gate，不生成交易许可、风险阈值或法律合规结论。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_jurisdiction_and_venue_caveats"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "event_time"),
            "data_granularity": applicability.get("data_granularity", "order_events_execution_reports_audit_logs"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": applicability.get("applies_when", []),
            "not_applicable_when": applicability.get("not_applicable_when", []),
        },
        "content": {
            "statement": claim.get("statement"),
            "rationale": claim.get("interpretation_notes"),
            "normalized_claim": claim.get("normalized_claim"),
            "claim_strength": "reviewed_caveat_only",
            "performance_claim": False,
            "procedure": [
                "确认问题属于 Audit Trail / Clock Sync、订单事件审计链、事件时间、事件序列、幂等、retention 或日志完整性。",
                "检查事件是否声明 event_time、receive_time、log_time、timezone、timestamp_precision、source_system 和 owner。",
                "检查订单事件链是否保留 event_id、prev_event_id、parent_event_id、client/broker/exchange ID 映射和原因字段。",
                "若涉及 replay/backfill/correction，必须确认原始事件未被静默覆盖，并保留 replay_cursor、correction_event_id 和 replay_reason。",
                "若涉及 retention/integrity，必须声明 record_class、retention_policy_id、jurisdiction_scope、storage_mode、integrity_check 和 archive_restore_path。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "examples": [],
            "anti_patterns": string_list(
                [
                    "把 CAT/FINRA/ESMA 的 clock sync 数值写成全球通用硬规则。",
                    "把 Kafka/Event Sourcing/CDC/Object Lock 写成 CEK-TA mandatory vendor。",
                    "用审计链完整性推导策略有效、交易许可、风控阈值或法律合规结论。",
                    "在 replay/backfill/correction 中静默覆盖原始事件。",
                    "把普通应用日志当作可审计 ledger，而没有 retention、修改/删除审计、完整性校验和恢复路径。",
                ]
                + as_list(claim.get("anti_patterns"))
            ),
            "validation": [
                "source_evidence 至少包含监管/协议/标准/官方平台来源，并明确辖区、协议或实现边界。",
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "不得出现买卖点、仓位、杠杆、止损止盈、实盘执行建议、风险阈值数值或法律合规结论。",
            ],
            "risk_notes": [
                "Audit Trail / Clock Sync reviewed/caveat_only 只能作为交易审计和工程设计检查上下文。",
                "监管来源具有辖区边界；协议和平台来源具有实现边界。",
                "Database/Storage 只拥有存储完整性和生命周期，不拥有策略、订单执行或风控阈值。",
                "本条不是 approved，不进入默认指导，不启用 hard gate。",
            ],
            "citation_notes": "；".join(str(ref.get("evidence_summary", "")) for ref in source_refs if ref.get("evidence_summary")),
            "audit_patch_notes": patch_notes,
        },
        "assumptions": applicability.get("assumptions", []),
        "source_evidence": source_refs,
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": candidate.get("conflict_audit", {}).get("checked_against", []),
            "conflicts": [],
            "resolution_summary": "reviewed/caveat_only 准备审计通过；formal creation 保持 caveat_only，不创建 approved、default guidance 或 hard gate。",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "legal_compliance_conclusion_allowed": False,
        },
        "review": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "confidence": result["confidence"],
            "freshness": candidate.get("review", {}).get("freshness", "mixed"),
            "reviewer": "external_ai_strict_audit_and_codex",
            "reviewed_at": TODAY,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "legal_compliance_conclusion_allowed": False,
            "approved_at": None,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": result["reasons"],
                "patch_notes": patch_notes,
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计订单事件审计链、时间戳字段、ID 映射、幂等和日志完整性检查。",
                "用于生成 trade audit checklist、schema review、RAG 检索上下文和 reason code。",
                "用于检查外接项目方案是否遗漏 clock sync、event sequencing、idempotency、retention 或 integrity 边界。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。",
                "不得输出法律合规结论或具体 retention 年限作为通用规则。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得把审计追踪、时间同步、事件序列或存储完整性写成策略 alpha 或 hard gate。",
            ],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_visibility": "reviewed_caveat_only",
            "reason": "reviewed/caveat_only audit passed; approved/default guidance/hard gate remain disabled.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "legal_compliance_conclusion_allowed": False,
        },
        "contribution": candidate.get("contribution", {}),
    }


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    output: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in candidate_paths():
        candidate = read_json(path)
        output[str(candidate.get("research_task_id"))] = (path, candidate)
    return output


def main() -> int:
    audit = audit_result_payload()
    write_json(AUDIT_RESULT_ARCHIVE, audit)
    results_by_task = {item["research_task_id"]: item for item in RESULTS}
    candidates = load_candidates()

    promoted: list[dict[str, Any]] = []
    failures: list[str] = []
    for task_id, result in results_by_task.items():
        entry = candidates.get(task_id)
        if not entry:
            failures.append(f"{task_id}: candidate not found")
            continue
        path, candidate = entry
        workflow = candidate.setdefault("workflow", {})
        workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]
        conversion = workflow.setdefault("conversion_target", {})
        conversion.update(
            {
                "target_review_status": "reviewed",
                "target_machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
        )
        formal_item = build_formal_item(candidate, result)
        partition_id = str(formal_item["metadata"]["partition_id"])
        knowledge_dir = resolve_repo_path("codex-expert-kit", "rag", "knowledge", partition_id, start_file=__file__)
        formal_path = knowledge_dir / sanitize_filename(formal_item["knowledge_id"])
        write_json(formal_path, formal_item)

        candidate["status"]["review_status"] = "formalized"
        candidate["status"]["ingestion_decision"] = "formal_reviewed_created"
        candidate["status"]["decision_reason"] = "reviewed/caveat_only 准备审计通过，已创建 formal reviewed/caveat_only。"
        candidate["status"]["updated_at"] = TODAY
        workflow["stage"] = "formalized_reviewed"
        workflow["queue_group"] = "formalized"
        workflow["formal_knowledge_id"] = formal_item["knowledge_id"]
        workflow["formal_review_status"] = "reviewed"
        formal_path_relative = repo_relative(formal_path)
        workflow["formal_knowledge_path"] = formal_path_relative
        workflow["approved_allowed"] = False
        workflow["default_guidance_allowed"] = False
        workflow["hard_gate_allowed"] = False
        workflow["risk_threshold_advice_allowed"] = False
        workflow["legal_compliance_conclusion_allowed"] = False
        candidate.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_trade_audit_formal_reviewed_created",
                "reason": "created formal reviewed/caveat_only from reviewed-preparation audit result",
                "audit_result_id": AUDIT_RESULT_ID,
                "formal_knowledge_id": formal_item["knowledge_id"],
            }
        )
        write_json(path, candidate)
        promoted.append(
            {
                "research_task_id": task_id,
                "candidate_id": candidate.get("candidate_id"),
                "knowledge_id": formal_item["knowledge_id"],
                "formal_path": formal_path_relative,
            }
        )

    report = {
        "report_id": "phase45_trade_audit_formal_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "expected_total": EXPECTED_TOTAL,
        "promoted_count": len(promoted),
        "failures": failures,
        "promoted": promoted,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
        "legal_compliance_conclusion_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps({"promoted_count": len(promoted), "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == EXPECTED_TOTAL and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
