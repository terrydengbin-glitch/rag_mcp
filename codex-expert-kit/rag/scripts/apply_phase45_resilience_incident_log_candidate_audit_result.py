"""Import Phase 45 Resilience / Incident / Log first audit result.

This script archives the external audit result, updates four candidates to
accepted_for_draft, supplements OPS02/OPS03, and exports a supplemental
re-audit package for the two needs_more_evidence candidates.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk thresholds, or trading execution advice.
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
TASK_ID = "CEK-TA-464"
AUDIT_RESULT_ID = "audit_phase45_resilience_incident_log_20260612_external_strict_v1"
PACKAGE_ID = "phase45_resilience_incident_log_candidate_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_resilience_incident_log_supplemental_reaudit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_resilience_incident_log_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_resilience_incident_log_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_resilience_incident_log_supplemental_reaudit_package_quality_gate.json", start_file=__file__)
RUNTIME_CONTRACT = resolve_repo_path("docs", "contracts", "phase45_resilience_incident_log_runtime_contract.md", start_file=__file__)


DECISIONS: dict[str, dict[str, Any]] = {
    "P45-D-OPS01": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "FINRA Rule 4370、Reg SCI、NIST SP 800-34、AWS DR 足以支撑 BC/DR、关键系统、备份恢复、依赖和 owner 边界。",
        "required_followups": [
            "保留 FINRA/Reg SCI 的美国监管或 SCI entity/member firm caveat。",
            "补 internal dependency map/schema 字段要求，但不得上升为 hard gate。",
            "不得定义 CEK-TA RTO/RPO 数值、自动停机、重启、撤单或重发订单。",
        ],
    },
    "P45-D-OPS02": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "现有来源主要支撑 DR、incident response 和 cloud reliability，不足以直接支撑交易系统 read-only/write-disabled 操作语义。",
        "required_followups": [
            "补 Google SRE graceful degradation / overload handling 来源。",
            "补数据库 read-only / write disabled / fail-safe mode 工程来源。",
            "补 CEK-TA runtime mode schema：normal、degraded、read_only、recovery、manual_intervention_required。",
            "明确 read-only 下允许 query/audit/reconcile，禁止 new_order/cancel_replace/replay_write。",
        ],
    },
    "P45-D-OPS03": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "failover/recovery/replay 边界正确，但缺少订单协议/API 级证据和内部 order truth source contract。",
        "required_followups": [
            "补 FIX ClOrdID / OrigClOrdID / CancelReplace 来源。",
            "补 Binance newClientOrderId 或目标交易所 client order id 语义。",
            "补 broker/venue 关于 duplicate order id、filled order cannot modify、cancel/replace rejection 的来源。",
            "补内部 order_state_machine：source_of_truth、idempotency_key、venue_order_id、client_order_id、replay_mode。",
        ],
    },
    "P45-D-OPS04": {
        "decision": "accepted_for_draft",
        "confidence": "medium",
        "reason": "事故 taxonomy 用于审计、复盘、优先级排序，边界正确；但具体 taxonomy 列表应标成 CEK-TA 内部分类。",
        "required_followups": [
            "把“至少区分”改为“CEK-TA draft taxonomy 建议至少覆盖”。",
            "补 incident taxonomy schema：category、impact_area、affected_system、market_impact、data_quality、order_state、human_action。",
            "明确 taxonomy label 只能进入 audit/review queue，不能触发交易动作。",
        ],
    },
    "P45-D-OPS05": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "Google SRE postmortem、NIST incident response、Reg SCI event notification/recordkeeping 足以支撑 post-incident review 边界。",
        "required_followups": [
            "补 post-incident review template 字段，但保持 draft 层级。",
            "补验证证据字段：test_id、fix_owner、evidence_uri、residual_risk、reopen_condition。",
            "复盘 action item 不得直接成为策略规则或实盘放行条件。",
        ],
    },
    "P45-D-OPS06": {
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": "NIST SP 800-92、Reg SCI、OpenTelemetry 支撑日志治理和遥测边界，归入 Database Storage / Audit Log Ledger 正确。",
        "required_followups": [
            "补 SEC Rule 17a-4 / FINRA 4511 / CFTC 1.31 作为金融记录保存和完整性来源。",
            "补 audit ledger schema：correlation_id、event_id、source_ts、ingest_ts、hash、prev_hash、actor、access_log、delete_log。",
            "明确 OpenTelemetry 仅为 telemetry，不是 audit ledger。",
        ],
    },
}


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "google_sre_handling_overload": {
        "source_title": "Google SRE Book: Handling Overload",
        "source_url": "https://sre.google/sre-book/handling-overload/",
        "source_type": "engineering_practice",
        "publisher": "Google SRE",
        "reliability": "medium_high",
        "score": 83,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "Google SRE describes graceful handling of overload, including serving degraded responses that are easier to compute and may rely on cached/local data.",
        "limitations": ["General SRE practice; not a trading execution permission or financial regulation."],
    },
    "aws_graceful_degradation": {
        "source_title": "AWS Well-Architected: Implement graceful degradation",
        "source_url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_mitigate_interaction_failure_graceful_degradation.html",
        "source_type": "cloud_architecture_doc",
        "publisher": "AWS",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "AWS Reliability guidance states graceful degradation maintains important functionality during failures by reducing functionality rather than failing completely.",
        "limitations": ["Cloud workload design source; not a broker, exchange or trading-system hard gate."],
    },
    "postgres_hot_standby": {
        "source_title": "PostgreSQL Documentation: Hot Standby",
        "source_url": "https://www.postgresql.org/docs/current/hot-standby.html",
        "source_type": "official_database_doc",
        "publisher": "PostgreSQL Global Development Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "PostgreSQL Hot Standby allows connections and read-only queries while a server is in archive recovery or standby mode.",
        "limitations": ["Database implementation example; CEK-TA does not require PostgreSQL."],
    },
    "phase45_runtime_contract": {
        "source_title": "Phase 45 Resilience / Incident / Log Runtime Contract",
        "source_url": "docs/contracts/phase45_resilience_incident_log_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 90,
        "freshness": "current",
        "relevance": "high",
        "evidence_summary": "CEK-TA contract defines runtime_mode, allowed/forbidden operations, read_only write policy, replay boundary, owner boundary and machine gate.",
        "limitations": ["Internal CEK-TA contract; must be used with external supporting sources."],
    },
    "fix_cancel_replace": {
        "source_title": "FIX 4.4 Order Cancel/Replace Request",
        "source_url": "https://www.b2bits.com/fixopaedia/fixdic44/message_Order_Cancel_Replace_Request_G.html",
        "source_type": "official_protocol_reference",
        "publisher": "FIXopaedia / FIX 4.4 reference",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "FIX Cancel/Replace uses ClOrdID and OrigClOrdID and may be rejected when a request cannot be processed, supporting order identifier and cancel/replace boundaries.",
        "limitations": ["Protocol reference; venue/broker behavior can differ."],
    },
    "fix_order_cancel_reject": {
        "source_title": "FIX Latest OrderCancelReject",
        "source_url": "https://fiximate.fixtrading.org/en/FIX.Latest/msg10.html",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "FIX OrderCancelReject includes ClOrdID and OrigClOrdID semantics for cancel/replace requests that could not be processed.",
        "limitations": ["Protocol semantics source; not a guarantee of a specific broker/venue implementation."],
    },
    "binance_futures_new_order": {
        "source_title": "Binance USDⓈ-M Futures New Order",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/trade/rest-api",
        "source_type": "official_exchange_api_doc",
        "publisher": "Binance Open Platform",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Binance Futures New Order documents newClientOrderId as a unique id among open orders, supporting client order id boundaries in one venue/API context.",
        "limitations": ["Binance Futures-specific; not universal order-id semantics."],
    },
    "ibkr_order_ids": {
        "source_title": "IBKR TWS API Documentation",
        "source_url": "https://www.interactivebrokers.com/campus/ibkr-api-page/trader-workstation-api/",
        "source_type": "official_broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 87,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR documentation states requests should use unique identifiers and the same order identifier cannot be reused except to modify an existing order.",
        "limitations": ["IBKR-specific API semantics; not universal broker behavior."],
    },
    "ibkr_modifying_orders": {
        "source_title": "IBKR TWS API: Modifying Orders",
        "source_url": "https://interactivebrokers.github.io/tws-api/modifying_orders.html",
        "source_type": "official_broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "archived",
        "relevance": "medium_high",
        "evidence_summary": "IBKR modifying-orders documentation explains that manual orders must be bound before API modification/cancellation and that API order IDs depend on session/client binding.",
        "limitations": ["Archived IBKR documentation; supporting source only."],
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
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_resilience_incident_log_*.json")))
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
            existing_urls.add(ref.get("source_url"))
    candidate["source_refs"] = source_refs
    primary_types = {
        "regulatory_rule",
        "standard_doc",
        "engineering_practice",
        "framework_doc",
        "cloud_architecture_doc",
        "official_database_doc",
        "internal_contract",
        "official_protocol_reference",
        "official_protocol_doc",
        "official_exchange_api_doc",
        "official_broker_doc",
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
                "risk_threshold_advice_allowed": False,
                "reasons": [data["reason"]],
                "required_followups": data["required_followups"],
            }
            for task, data in DECISIONS.items()
        ],
        "global_notes": [
            "审计包边界合格：candidate 审计，禁止 reviewed/approved/default guidance/hard gate。",
            "OPS02 需要补 degraded/read-only mode 直接来源和 runtime mode schema。",
            "OPS03 需要补订单协议/API/状态机证据和 replay/live action 边界。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def supplement_candidate(candidate: dict[str, Any]) -> None:
    task_id = str(candidate.get("research_task_id"))
    audit_log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if task_id == "P45-D-OPS02":
        upsert_source_refs(
            candidate,
            [
                source_ref("google_sre_handling_overload", "src_supp_001"),
                source_ref("aws_graceful_degradation", "src_supp_002"),
                source_ref("postgres_hot_standby", "src_supp_003"),
                source_ref("phase45_runtime_contract", "src_supp_004"),
            ],
        )
        candidate["claim"]["statement"] = (
            "交易系统进入 degraded、read_only、recovery 或 manual_intervention_required 模式时，必须声明 mode_reason、允许/禁止操作、"
            "数据新鲜度、写入禁用语义、人工接管、退出条件和审计 trace。read_only 模式默认只允许 query/audit/reconcile/report，"
            "禁止 new_order、cancel_replace、live_order_replay_write、position_mutation 和 risk_threshold_change；不得在依赖不完整或状态不明时静默继续正常交易。"
        )
        candidate["claim"]["evidence_summary"] = (
            "Google SRE 与 AWS 支撑 graceful degradation；PostgreSQL Hot Standby 支撑 read-only query 语义；"
            "CEK-TA runtime contract 定义 normal/degraded/read_only/recovery/manual_intervention_required 状态机和 forbidden operations。"
        )
        candidate.setdefault("applicability", {}).setdefault("limitations", []).extend(
            [
                "Google SRE/AWS 是工程实践来源，不是交易监管要求。",
                "PostgreSQL 只是 read-only database mode 示例，外接项目可使用等价数据库或权限控制。",
                "CEK-TA 不输出停机阈值、恢复阈值、自动拒单、自动撤单或实盘动作。",
            ]
        )
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_ops02_supplemented",
                "reason": "按首轮审计要求补 graceful degradation、read-only database mode 和 CEK-TA runtime mode contract。",
            }
        )
    elif task_id == "P45-D-OPS03":
        upsert_source_refs(
            candidate,
            [
                source_ref("fix_cancel_replace", "src_supp_001"),
                source_ref("fix_order_cancel_reject", "src_supp_002"),
                source_ref("binance_futures_new_order", "src_supp_003"),
                source_ref("ibkr_order_ids", "src_supp_004"),
                source_ref("ibkr_modifying_orders", "src_supp_005"),
                source_ref("phase45_runtime_contract", "src_supp_006"),
            ],
        )
        candidate["claim"]["statement"] = (
            "故障切换、恢复和事件 replay 必须区分 audit_replay、simulation_replay、state_rebuild 和 live_order_action。"
            "audit_replay 只用于审计解释，simulation_replay 只用于模拟，state_rebuild 只用于恢复内部状态视图。"
            "live_order_action 必须依赖订单真相源、client_order_id、venue/broker_order_id、idempotency_key、当前订单状态快照、"
            "Risk/Live Execution owner 审批和 audit_trace_id；没有这些证据时，不得通过 replay 自动重发、修改或撤销真实订单。"
        )
        candidate["claim"]["evidence_summary"] = (
            "FIX ClOrdID/OrigClOrdID 与 CancelReject 支撑 cancel/replace 身份和拒绝边界；Binance newClientOrderId 支撑 venue client order id 唯一性示例；"
            "IBKR order id 来源支撑 broker API order id 与修改边界；CEK-TA runtime contract 定义 replay_mode、source_of_truth、idempotency_key 和 live_action_requires。"
        )
        candidate.setdefault("applicability", {}).setdefault("limitations", []).extend(
            [
                "FIX、Binance、IBKR 是协议或 venue/broker 示例，不能泛化为所有市场。",
                "live_order_action 必须由外接项目 Live Execution / Risk Management owner 明确授权。",
                "CEK-TA 不输出自动重发订单、自动撤单、自动修改订单、恢复阈值或风控阈值。",
            ]
        )
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_ops03_supplemented",
                "reason": "按首轮审计要求补 FIX、Binance、IBKR 和 CEK-TA replay boundary contract。",
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
                "action": "phase45_resilience_incident_log_first_audit_imported",
                "reason": f"{decision['decision']} / confidence={decision['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "required_followups": decision["required_followups"],
        }
        if decision["decision"] == "accepted_for_draft":
            data["status"]["review_status"] = "accepted"
            data["status"]["ingestion_decision"] = "accepted_for_draft"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "formal_draft_queue"
            data["workflow"]["queue_group"] = "ai_passed"
            data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        else:
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
        if data.get("research_task_id") in {"P45-D-OPS02", "P45-D-OPS03"}:
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def supplemental_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 2:
        failures.append(f"expected 2 supplemented candidates, got {len(candidates)}")
    if not RUNTIME_CONTRACT.exists():
        failures.append("runtime contract missing")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if len(item.get("source_refs", [])) < 8:
            failures.append(f"{cid}: source_refs < 8 after supplement")
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
        "gate_id": "phase45_resilience_incident_log_supplemental_reaudit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 2,
        "runtime_contract": repo_relative(RUNTIME_CONTRACT),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 OPS02/OPS03 补证候选；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "degraded/read-only 和 replay/live-action 边界只能用于审计与方案设计，不触发实盘动作。",
            "Google SRE/AWS/PostgreSQL/FIX/Binance/IBKR 来源均具有工程、venue、broker 或 implementation caveat。",
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
            "branch": "Trading Engineering / Live Execution / Resilience Incident Log",
            "batch": "P45-D Resilience / Incident / Log supplemental re-audit",
            "candidate_count": len(candidates),
            "target": "复审 OPS02 degraded/read-only mode 和 OPS03 failover/recovery/replay 边界补证后是否可进入 accepted_for_draft。",
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
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议", "停机阈值", "自动拒单", "自动重发订单", "自动撤单"],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、协议文档、broker/venue API、SRE/数据库资料和案例，对补证内容进行严格再审。",
            "OPS02：检查 Google SRE graceful degradation、AWS graceful degradation、PostgreSQL hot standby/read-only、CEK-TA runtime mode contract 是否足以支撑 degraded/read_only 操作边界。",
            "OPS03：检查 FIX ClOrdID/OrigClOrdID/CancelReject、Binance newClientOrderId、IBKR order id/modify boundary、CEK-TA replay boundary contract 是否足以支撑 replay 不得自动重发/修改真实订单。",
            "检查是否仍然禁止 reviewed、approved、default guidance、hard gate、风险阈值、停机阈值、自动实盘动作。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {"total": 2, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-D-OPS02 | P45-D-OPS03",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "quality_gate": gate,
        "runtime_contract": {
            "path": repo_relative(RUNTIME_CONTRACT),
            "purpose": "提供 runtime mode、read-only forbidden operations、replay boundary、owner boundary 和 machine gate 契约。",
        },
        "candidates": candidates,
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)


def write_supplemental_research() -> None:
    lines = [
        "# Phase 45 Resilience / Incident / Log 补证记录",
        "",
        "## 补证目标",
        "",
        "首轮审计中 P45-D-OPS02 与 P45-D-OPS03 被判定为 needs_more_evidence。本文件记录 degraded/read-only mode 与 failover/recovery/replay 边界补证。",
        "",
        "## 新增内部契约",
        "",
        f"- `{repo_relative(RUNTIME_CONTRACT)}`：定义 runtime_mode、allowed/forbidden operations、read-only 写入禁用、replay boundary、owner boundary 和 machine gate。",
        "",
        "## P45-D-OPS02 补证来源",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key in ["google_sre_handling_overload", "aws_graceful_degradation", "postgres_hot_standby", "phase45_runtime_contract"]:
        source = SUPPLEMENTAL_SOURCES[key]
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "修补后 OPS02 claim：degraded/read_only/recovery/manual_intervention_required 必须声明 mode_reason、允许/禁止操作、数据新鲜度、写入禁用语义、人工接管、退出条件和 audit trace。read_only 下默认禁止 new_order、cancel_replace、live_order_replay_write、position_mutation 和 risk_threshold_change。",
            "",
            "## P45-D-OPS03 补证来源",
            "",
            "| source_id | 来源 | 类型 | URL | 用途 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for key in ["fix_cancel_replace", "fix_order_cancel_reject", "binance_futures_new_order", "ibkr_order_ids", "ibkr_modifying_orders", "phase45_runtime_contract"]:
        source = SUPPLEMENTAL_SOURCES[key]
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "修补后 OPS03 claim：replay 必须区分 audit_replay、simulation_replay、state_rebuild 和 live_order_action。没有订单真相源、client/venue/broker order id、idempotency_key、当前订单状态快照、Risk/Live Execution owner 审批和 audit_trace_id 时，不得通过 replay 自动重发、修改或撤销真实订单。",
            "",
            "## 硬边界",
            "",
            "```text",
            "1. 补证不创建 formal reviewed。",
            "2. 补证不创建 approved、default guidance 或 hard gate。",
            "3. 不生成买卖点、仓位、杠杆、止损止盈、实盘执行建议、停机阈值或风险阈值。",
            "4. 不触发自动拒单、自动撤单、自动重发订单、自动恢复交易。",
            "5. 外部来源均保留 implementation / venue / broker / protocol caveat。",
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
            "report_id": "phase45_resilience_incident_log_audit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "first_audit_summary": audit_result["summary"],
            "updated": apply_report["updated"],
            "missing": apply_report["missing"],
            "runtime_contract": repo_relative(RUNTIME_CONTRACT),
            "supplemental_research": repo_relative(SUPPLEMENTAL_RESEARCH),
            "supplemental_package": repo_relative(SUPPLEMENTAL_PACKAGE),
            "supplemental_gate": repo_relative(SUPPLEMENTAL_GATE),
            "supplemental_gate_status": gate["gate_status"],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
            "risk_threshold_advice_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "updated_count": len(apply_report["updated"]), "supplemental_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" and not apply_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
