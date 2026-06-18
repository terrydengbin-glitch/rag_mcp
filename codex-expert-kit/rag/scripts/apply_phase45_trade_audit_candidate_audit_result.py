"""Import Phase 45 Audit Trail / Clock Sync first audit result.

This script does not create formal reviewed knowledge, approve knowledge,
enable default guidance, or create hard gates. It only:

1. Archives the external strict audit result as structured JSON.
2. Updates four candidates to accepted_for_draft.
3. Updates two candidates to needs_more_evidence, supplements them, and exports
   a supplemental re-audit package.
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
PHASE = "45"
TASK_ID = "CEK-TA-460"
AUDIT_RESULT_ID = "audit_phase45_trade_audit_p45_b_20260612_external_strict_v1"
PACKAGE_ID = "phase45_trade_audit_candidate_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_trade_audit_supplemental_reaudit_package_20260612"
PARTITIONS = ["KB_02_DATA_ENGINEERING", "KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_trade_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_trade_audit_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_trade_audit_supplemental_reaudit_package_quality_gate.json", start_file=__file__)


DECISIONS: dict[str, dict[str, Any]] = {
    "P45-B-AUD01": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "SEC/CAT/FINRA/ESMA 足以支撑 clock synchronization 与 reportable event timestamp 边界。",
        "required_followups": [
            "明确这是 CEK-TA 内部审计字段要求，不是全球监管统一规则。",
            "不得把 CAT / FINRA / ESMA 的精度或漂移阈值泛化到 crypto、外汇、离岸交易所或全部 broker。",
            "补充 event_time_source / timezone / precision / drift_observed / sync_provider / exception_reason / remediation_id 字段。",
        ],
    },
    "P45-B-AUD02": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "SEC Rule 613 支撑 order receipt/origination 到 routing、modification、cancellation、execution 的 time-sequenced record；FIX 支撑协议事件语义。",
        "required_followups": [
            "actor / reason / source_system 是 CEK-TA 内部 schema 强化项，应标注为内部审计字段。",
            "补充事件类型枚举：received / routed / replaced / canceled / rejected / partial_fill / fill / expired / terminal_state。",
            "补充 prev_event_id 或 causal parent 字段定义。",
        ],
    },
    "P45-B-AUD03": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "SEC/CAT 与 FIX 足以支撑多 ID 映射和订单链路可追踪。",
        "required_followups": [
            "不要把 CAT 字段直接等同于 crypto exchange 的 client_order_id / exchange_order_id。",
            "补充 venue/broker 私有 ID 映射应由外接项目事实层提供。",
            "明确 cancel/replace 关联 ID 和 idempotency request ID 是 CEK-TA 工程字段，不是 FIX/CAT 全部原生字段。",
        ],
    },
    "P45-B-AUD04": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "SEC/FIX/NIST 只能部分支撑，缺少 event stream、idempotency、dedup_key、replay_cursor 和回放不静默覆盖的工程来源。",
        "required_followups": [
            "补充 Kafka idempotent producer / transactions / delivery semantics、event sourcing、CDC replay 或数据库唯一约束/upsert 审计边界来源。",
            "补充内部 schema contract 或 contract hash，证明 event_id / dedup_key / replay_cursor 是 CEK-TA 字段契约。",
            "拆分监管/审计层与工程实现层。",
        ],
    },
    "P45-B-AUD05": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "SEC 613 + NIST 800-92 不足以证明 hash/checksum/append-only/immutable ledger，需要补 SEC 17a-4、WORM 或 audit-trail alternative 等来源。",
        "required_followups": [
            "补充 SEC Rule 17a-4 / FINRA 4511 / WORM 或 audit-trail alternative 来源。",
            "补充存储层来源：append-only ledger、object lock、hash chain、checksum、audit trail recreation policy。",
            "明确 AUD05 是 Database/Storage owner 承接的 trade audit storage boundary，不能变成策略、执行或 AI Engineering 本体规则。",
        ],
    },
    "P45-B-AUD06": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "CAT Alert 与 ESMA 足以支撑 manual/electronic timestamp boundary；所有阈值必须 jurisdiction-scoped。",
        "required_followups": [
            "不得输出具体 drift 数值作为 CEK-TA 通用阈值；数值只能作为 CAT/NMS 语境案例。",
            "增加 event_class、timestamp_source、granularity、drift_policy_ref、evidence_policy_ref 字段。",
            "明确人工录入时间不能替代电子事件时间，但电子事件精度也不能泛化到所有人工流程。",
        ],
    },
}


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "confluent_kafka_delivery": {
        "source_title": "Message Delivery Guarantees for Apache Kafka",
        "source_url": "https://docs.confluent.io/kafka/design/delivery-semantics.html",
        "source_type": "official_platform_doc",
        "publisher": "Confluent / Apache Kafka documentation ecosystem",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Kafka delivery semantics documentation explains at-least-once, at-most-once and transactions/exactly-once semantics boundaries.",
        "limitations": ["Streaming-platform semantics source; does not define trading audit fields."],
    },
    "microsoft_event_sourcing": {
        "source_title": "Event Sourcing Pattern",
        "source_url": "https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing",
        "source_type": "architecture_pattern_doc",
        "publisher": "Microsoft Learn / Azure Architecture Center",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Event Sourcing records events so systems can replay them to restore state, roll back changes, keep history, and maintain audit logs.",
        "limitations": ["Architecture pattern; not trading-regulatory schema."],
    },
    "fowler_event_sourcing": {
        "source_title": "Event Sourcing",
        "source_url": "https://martinfowler.com/eaaDev/EventSourcing.html",
        "source_type": "architecture_pattern_doc",
        "publisher": "Martin Fowler",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "Event Sourcing stores application state changes as a sequence of events and can use the event log to reconstruct past states.",
        "limitations": ["Pattern source; not a formal regulatory source."],
    },
    "debezium_cdc": {
        "source_title": "Debezium Features",
        "source_url": "https://debezium.io/documentation/reference/stable/features.html",
        "source_type": "official_platform_doc",
        "publisher": "Debezium",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "Debezium captures data changes and can include metadata such as transaction ID and old record state depending on source database capabilities.",
        "limitations": ["CDC implementation source; not CEK-TA mandatory infrastructure."],
    },
    "sec_17a4": {
        "source_title": "Amendments to Electronic Recordkeeping Requirements for Broker-Dealers",
        "source_url": "https://www.sec.gov/investment/amendments-electronic-recordkeeping-requirements-broker-dealers",
        "source_type": "regulatory_doc",
        "publisher": "U.S. SEC",
        "reliability": "high",
        "score": 92,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "SEC explains Rule 17a-4 amendments allowing either WORM or an audit-trail alternative that can recreate original records if modified or deleted.",
        "limitations": ["Broker-dealer/SBS recordkeeping context; not a global universal retention rule."],
    },
    "finra_17a4_chart": {
        "source_title": "Exchange Act Rule 17a-4 Amendments Chart of Significant Changes",
        "source_url": "https://www.finra.org/sites/default/files/2022-12/rule-17a-4-amendments.pdf",
        "source_type": "regulatory_guidance",
        "publisher": "FINRA",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "FINRA chart describes WORM and audit-trail alternatives, including time-stamped audit trail for modifications/deletions and prompt production obligations.",
        "limitations": ["FINRA interpretation aid; jurisdiction-specific."],
    },
    "aws_s3_object_lock": {
        "source_title": "Locking objects with Object Lock",
        "source_url": "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html",
        "source_type": "official_platform_doc",
        "publisher": "AWS",
        "reliability": "medium_high",
        "score": 83,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "AWS Object Lock supports retention modes such as governance and compliance for protecting object versions from deletion or overwrite.",
        "limitations": ["Cloud storage implementation pattern; not CEK-TA mandatory storage."],
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
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_trade_audit_*.json")))
    return paths


def source_ref(source_key: str, source_id: str) -> dict[str, Any]:
    source = dict(SUPPLEMENTAL_SOURCES[source_key])
    source.update({"source_id": source_id, "accessed_at": TODAY, "version": None, "quoted_excerpt_allowed": False})
    return source


def upsert_source_refs(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    existing_urls = {ref.get("source_url") for ref in candidate.get("source_refs", [])}
    source_refs = list(candidate.get("source_refs", []))
    for ref in refs:
        if ref.get("source_url") not in existing_urls:
            source_refs.append(ref)
    candidate["source_refs"] = source_refs
    primary_types = {
        "regulatory_doc",
        "regulatory_rule",
        "regulatory_guidance",
        "official_protocol_doc",
        "standard_doc",
        "official_platform_doc",
        "architecture_pattern_doc",
    }
    primary_count = sum(1 for ref in source_refs if ref.get("source_type") in primary_types)
    candidate.setdefault("source_quality", {})["primary_source_count"] = primary_count
    candidate["source_quality"]["supporting_source_count"] = len(source_refs) - primary_count
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 70)) for ref in source_refs) / len(source_refs), 2)


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_draft": 4,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "research_task_id": task,
                "decision": data["decision"],
                "confidence": data["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [data["reason"]],
                "required_followups": data["required_followups"],
            }
            for task, data in DECISIONS.items()
        ],
        "global_notes": [
            "审计包边界合格：candidate 审计，禁止 reviewed/approved/default guidance/hard gate。",
            "AUD04 需要补事件流、幂等、dedup_key、replay_cursor 和回放不静默覆盖的工程来源。",
            "AUD05 需要补 SEC 17a-4、WORM、audit-trail alternative 和存储完整性来源。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def supplement_candidate(candidate: dict[str, Any]) -> None:
    task_id = str(candidate.get("research_task_id"))
    audit_log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if task_id == "P45-B-AUD04":
        upsert_source_refs(
            candidate,
            [
                source_ref("confluent_kafka_delivery", "src_supp_001"),
                source_ref("microsoft_event_sourcing", "src_supp_002"),
                source_ref("fowler_event_sourcing", "src_supp_003"),
                source_ref("debezium_cdc", "src_supp_004"),
            ],
        )
        candidate["claim"]["statement"] = (
            "订单事件流必须同时满足监管审计层和工程实现层边界：监管层要求事件 time-sequenced、可追踪、不可静默丢失；"
            "工程层必须定义 event_id、source_system、event_time、receive_time、sequence、dedup_key、idempotency_key、replay_cursor、"
            "correction_event_id 和 replay_reason。乱序、重复、缺失和延迟事件必须显式标记，回放或回灌不得静默覆盖原始真实事件。"
        )
        candidate["claim"]["evidence_summary"] = (
            "SEC/FIX/NIST 支撑交易审计和协议事件语义；Kafka delivery semantics、Event Sourcing、CDC/Debezium 补充幂等、事件重放、变更捕获和 replay 边界。"
        )
        candidate.setdefault("applicability", {}).setdefault("limitations", []).append(
            "Kafka/Event Sourcing/CDC 来源只支撑工程模式；外接项目可用等价事件流、数据库约束或审计表实现。"
        )
        candidate["classification"]["related_nodes"] = sorted(
            set(candidate["classification"].get("related_nodes", []) + ["kt.ai_engineering.database_storage_engineering.data_contract_lineage"])
        )
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_aud04_supplemented",
                "reason": "按首轮审计要求补 Kafka delivery semantics、Event Sourcing 和 CDC/Debezium 来源，并拆分监管审计层与工程实现层。",
            }
        )
    elif task_id == "P45-B-AUD05":
        upsert_source_refs(
            candidate,
            [
                source_ref("sec_17a4", "src_supp_001"),
                source_ref("finra_17a4_chart", "src_supp_002"),
                source_ref("aws_s3_object_lock", "src_supp_003"),
            ],
        )
        candidate["claim"]["statement"] = (
            "交易审计日志、订单事件日志和监管报告中间产物必须声明 retention policy、record class、append-only 或 audit-trail alternative、"
            "integrity_check、checksum/hash、modification/deletion audit、access audit、archive_restore_path 和 legal/jurisdiction scope。"
            "普通应用日志不能在缺少修改/删除审计、保留策略和可重建原始记录能力时被当作可审计 ledger。"
        )
        candidate["claim"]["evidence_summary"] = (
            "SEC Rule 17a-4 amendments 与 FINRA 17a-4 chart 支撑 WORM 或 audit-trail alternative；"
            "AWS Object Lock 作为对象存储 retention/immutability 实现示例；SEC Rule 613/NIST 继续作为交易审计和日志治理支撑。"
        )
        candidate.setdefault("applicability", {}).setdefault("limitations", []).append(
            "不得输出具体保留年限作为通用硬规则；retention 取决于辖区、记录类型、broker/venue 和外接项目合规要求。"
        )
        candidate["classification"]["classification_notes"] = (
            "本条由 KB_AI_26_DATABASE_STORAGE / audit_log_ledger 承接存储完整性，本体仍服务 Trading Engineering audit trail；"
            "不得变成策略、执行或 AI Engineering hard gate。"
        )
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_aud05_supplemented",
                "reason": "按首轮审计要求补 SEC 17a-4、FINRA 17a-4 chart 和 AWS Object Lock 来源，收窄 retention/integrity 边界。",
            }
        )


def apply_decisions() -> dict[str, Any]:
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}
    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        paths_by_task[task_id] = path
        data_by_task[task_id] = data

    updated: list[dict[str, Any]] = []
    missing: list[str] = []
    for task_id, decision in DECISIONS.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = data_by_task[task_id]
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_trade_audit_first_audit_imported",
                "reason": f"{decision['decision']} / confidence={decision['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "required_followups": decision["required_followups"],
        }
        if decision["decision"] == "accepted_for_draft":
            data["status"]["review_status"] = "accepted"
            data["status"]["ingestion_decision"] = "accepted_for_draft"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "formal_draft_queue"
            data["workflow"]["queue_group"] = "ai_passed"
            data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        elif decision["decision"] == "needs_more_evidence":
            data["status"]["review_status"] = "needs_more_evidence"
            data["status"]["ingestion_decision"] = "needs_more_evidence"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "needs_more_evidence"
            data["workflow"]["queue_group"] = "needs_more_evidence"
            data["workflow"]["allowed_next_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
            supplement_candidate(data)
        data["workflow"]["forbidden_next_decisions"] = ["reviewed", "approved", "default_guidance", "hard_gate"]
        data["status"]["updated_at"] = TODAY
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "decision": decision["decision"], "path": repo_relative(path)})
    return {"updated": updated, "missing": missing}


def load_supplemented_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths():
        data = read_json(path)
        if data.get("research_task_id") in {"P45-B-AUD04", "P45-B-AUD05"}:
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def supplemental_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 2:
        failures.append(f"expected 2 supplemented candidates, got {len(candidates)}")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if len(item.get("source_refs", [])) < 6:
            failures.append(f"{cid}: source_refs < 6 after supplement")
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must remain deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if item.get("machine_gate", {}).get(field) is not False:
                failures.append(f"{cid}: {field} must remain false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase45_trade_audit_supplemental_reaudit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 2,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 AUD04/AUD05 补证候选；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "AUD04 的 Kafka/Event Sourcing/CDC 来源只支撑工程模式，不替代交易监管字段契约。",
            "AUD05 的 SEC 17a-4/WORM/Object Lock 来源只支撑 retention/integrity 边界，不输出通用保留年限或合规结论。",
        ],
    }


def export_supplemental_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering",
            "batch": "P45-B Audit Trail / Clock Sync supplemental re-audit",
            "candidate_count": len(candidates),
            "target": "复审首轮 needs_more_evidence 的 P45-B-AUD04 和 P45-B-AUD05，确认补证后是否可进入 accepted_for_draft。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、协议文档、标准、案例和数据，对补证内容进行严格再审。",
            "P45-B-AUD04：检查 Kafka delivery semantics、Event Sourcing、CDC/Debezium 是否足以支撑 event_id、dedup_key、idempotency_key、replay_cursor 和回放不静默覆盖边界。",
            "P45-B-AUD05：检查 SEC Rule 17a-4、FINRA 17a-4 chart、Object Lock 是否足以支撑 retention、WORM/audit-trail alternative、hash/checksum、modification/deletion audit 和可重建原始记录边界。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {"total": 2, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-B-AUD04 | P45-B-AUD05",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)


def write_supplemental_research() -> None:
    lines = [
        "# Phase 45 Audit Trail / Clock Sync 补证记录",
        "",
        "## 补证目标",
        "",
        "首轮审计中 P45-B-AUD04 与 P45-B-AUD05 被判定为 needs_more_evidence。本文件记录补证来源、claim 收窄和边界修补。",
        "",
        "## P45-B-AUD04 补证",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key in ["confluent_kafka_delivery", "microsoft_event_sourcing", "fowler_event_sourcing", "debezium_cdc"]:
        source = SUPPLEMENTAL_SOURCES[key]
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "修补后 claim：订单事件流必须拆分监管审计层和工程实现层。监管层要求事件 time-sequenced、可追踪、不可静默丢失；工程层必须定义 event_id、source_system、event_time、receive_time、sequence、dedup_key、idempotency_key、replay_cursor、correction_event_id 和 replay_reason。",
            "",
            "## P45-B-AUD05 补证",
            "",
            "| source_id | 来源 | 类型 | URL | 用途 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for key in ["sec_17a4", "finra_17a4_chart", "aws_s3_object_lock"]:
        source = SUPPLEMENTAL_SOURCES[key]
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "修补后 claim：交易审计日志和监管报告中间产物必须声明 retention policy、record class、append-only 或 audit-trail alternative、integrity_check、checksum/hash、modification/deletion audit、access audit、archive_restore_path 和 legal/jurisdiction scope。",
            "",
            "## 硬边界",
            "",
            "```text",
            "1. 补证不创建 formal reviewed。",
            "2. 补证不创建 approved、default guidance 或 hard gate。",
            "3. 不生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值。",
            "4. Kafka/Event Sourcing/CDC 只支撑工程模式，不替代监管字段契约。",
            "5. SEC 17a-4/WORM/Object Lock 只支撑 retention/integrity 边界，不输出通用保留年限或合规结论。",
            "```",
        ]
    )
    SUPPLEMENTAL_RESEARCH.parent.mkdir(parents=True, exist_ok=True)
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    audit_result = archive_audit_result()
    apply_report = apply_decisions()
    candidates = load_supplemented_candidates()
    gate = supplemental_gate(candidates)
    write_json(SUPPLEMENTAL_GATE, gate)
    export_supplemental_package(candidates, gate)
    write_supplemental_research()
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_trade_audit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "first_audit_summary": audit_result["summary"],
            "updated": apply_report["updated"],
            "missing": apply_report["missing"],
            "supplemental_research": "docs/research/phase45_trade_audit_supplemental_research.md",
            "supplemental_package": "docs/audit/phase45_trade_audit_supplemental_reaudit_package_20260612.json",
            "supplemental_gate": "docs/reports/phase45_trade_audit_supplemental_reaudit_package_quality_gate.json",
            "supplemental_gate_status": gate["gate_status"],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "updated_count": len(apply_report["updated"]), "supplemental_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" and not apply_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
