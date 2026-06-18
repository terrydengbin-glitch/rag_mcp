"""Generate Phase 45 Audit Trail / Clock Sync candidate knowledge.

This script creates candidate and audit-support artifacts only. It does not
create formal reviewed knowledge, approve knowledge, enable default guidance,
or create hard gates.
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
TASK_ID = "CEK-TA-459"
BATCH = "P45-B Audit Trail / Clock Sync"
PACKAGE_ID = "phase45_trade_audit_candidate_audit_package_20260612"

RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase45_trade_audit_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase45_trade_audit_candidate_generation_report.json", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase45_trade_audit_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "sec_rule_613": {
        "source_title": "Rule 613: Consolidated Audit Trail",
        "source_url": "https://www.sec.gov/about/divisions-offices/division-trading-markets/rule-613-consolidated-audit-trail",
        "source_type": "regulatory_doc",
        "publisher": "U.S. SEC",
        "reliability": "high",
        "score": 93,
        "freshness": "time_sensitive",
        "evidence_summary": "SEC Rule 613 establishes a consolidated audit trail intended to let regulators track activity throughout U.S. NMS securities markets.",
        "limitations": ["U.S. NMS securities context; not a universal global trading-system standard."],
    },
    "ecfr_242_613": {
        "source_title": "17 CFR 242.613: Consolidated audit trail",
        "source_url": "https://www.ecfr.gov/current/title-17/chapter-II/part-242/subject-group-ECFRac68bdd026a46db/section-242.613",
        "source_type": "regulatory_rule",
        "publisher": "eCFR / U.S. SEC",
        "reliability": "high",
        "score": 94,
        "freshness": "time_sensitive",
        "evidence_summary": "17 CFR 242.613 describes accurate time-sequenced order records, reportable events, clock synchronization, timestamps, and electronic reporting to the central repository.",
        "limitations": ["Regulatory rule for CAT/NMS plan; use as audit-trail principle with jurisdiction caveat."],
    },
    "esma_article_22c": {
        "source_title": "MiFIR Article 22c: Synchronisation of business clocks",
        "source_url": "https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifir/article-22c-synchronisation-business-clocks",
        "source_type": "regulatory_rule",
        "publisher": "ESMA",
        "reliability": "high",
        "score": 91,
        "freshness": "time_sensitive",
        "evidence_summary": "ESMA Article 22c requires trading venues and relevant participants to synchronise business clocks used to record reportable events.",
        "limitations": ["EU/MiFIR context; accuracy details depend on applicable RTS and activity type."],
    },
    "finra_cat": {
        "source_title": "FINRA 2023 Report: Consolidated Audit Trail",
        "source_url": "https://www.finra.org/rules-guidance/guidance/reports/2023-finras-examination-and-risk-monitoring-program/cat",
        "source_type": "regulatory_guidance",
        "publisher": "FINRA",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA describes CAT rules covering reporting, clock synchronization, time stamps, connectivity, data transmission, recordkeeping, timeliness, accuracy, and completeness.",
        "limitations": ["FINRA member/CAT compliance context; not a global venue-agnostic standard."],
    },
    "cat_clock_alert": {
        "source_title": "CAT Alert 2020-02: Standards for self-reporting deviations of clock synchronization",
        "source_url": "https://www.catnmsplan.com/sites/default/files/2020-05/CAT-Alert-2020-02-v1.1.pdf",
        "source_type": "regulatory_guidance",
        "publisher": "CAT NMS Plan",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "CAT guidance distinguishes manual/allocation business-clock tolerance from other business clocks and references NIST atomic clock synchronization.",
        "limitations": ["CAT guidance; tolerances are jurisdiction/product specific and must not become CEK-TA universal thresholds."],
    },
    "fix_exec_report": {
        "source_title": "FIX 4.4 Execution Report",
        "source_url": "https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "evidence_summary": "FIX Execution Report supports order/execution event semantics, status transitions, fills, cancels, replaces, and identifiers.",
        "limitations": ["Protocol schema reference; does not define regulatory retention or venue-specific truth."],
    },
    "nist_800_92": {
        "source_title": "NIST SP 800-92: Guide to Computer Security Log Management",
        "source_url": "https://csrc.nist.gov/pubs/sp/800/92/final",
        "source_type": "standard_doc",
        "publisher": "NIST",
        "reliability": "high",
        "score": 87,
        "freshness": "stable",
        "evidence_summary": "NIST SP 800-92 supports log management lifecycle, retention, protection, analysis, and operational log governance.",
        "limitations": ["General computer-security log management guidance; not trading-specific CAT field schema."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-B-AUD01",
        "slug": "clock_synchronization_required",
        "partition": "KB_02_DATA_ENGINEERING",
        "tree_node": "kt.trading_engineering.data_engineering.audit_clock",
        "tree_path": "CEK-TA / Trading Engineering / Data Engineering / Audit Clock And Event Time",
        "domain": "data_engineering",
        "subdomain": "audit_clock",
        "title": "交易审计事件必须声明业务时钟同步边界",
        "statement": "交易系统的订单、成交、取消、替换、路由和人工事件必须记录可审计事件时间，并声明业务时钟同步来源、时区、精度、漂移检测和异常处理；不能把本地机器时间或日志写入时间当作监管级事件时间。",
        "claim_type": "clock_sync_boundary_rule",
        "sources": ["ecfr_242_613", "esma_article_22c", "finra_cat", "cat_clock_alert"],
    },
    {
        "task": "P45-B-AUD02",
        "slug": "order_event_causality_trace_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.audit_trail",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Audit Trail",
        "domain": "live_trading",
        "subdomain": "audit_trail",
        "title": "订单事件必须保留因果链追踪",
        "statement": "订单生命周期审计必须能从订单接收或生成开始，追踪路由、修改、取消、拒单、部分成交、完全成交和状态终结事件；每个事件必须能连接前序事件、触发 actor、原因和来源系统。",
        "claim_type": "order_event_causality_rule",
        "sources": ["ecfr_242_613", "sec_rule_613", "fix_exec_report"],
    },
    {
        "task": "P45-B-AUD03",
        "slug": "client_exchange_order_id_mapping_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.audit_trail",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Audit Trail",
        "domain": "live_trading",
        "subdomain": "audit_trail",
        "title": "client/exchange order id 映射必须可追踪",
        "statement": "实盘订单审计必须保留 client_order_id、broker_order_id、exchange_order_id、execution_id、cancel/replace 关联 ID 和幂等请求 ID 的映射；不能只保留某一个系统内 ID 后声称订单链路可复盘。",
        "claim_type": "order_identifier_mapping_rule",
        "sources": ["ecfr_242_613", "fix_exec_report", "finra_cat"],
    },
    {
        "task": "P45-B-AUD04",
        "slug": "event_sequence_and_idempotency_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.audit_trail",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Audit Trail",
        "domain": "live_trading",
        "subdomain": "audit_trail",
        "title": "事件序列和幂等处理必须可审计",
        "statement": "订单事件流必须保留 sequence、event_id、source_system、receive_time、event_time、dedup_key 和 replay_cursor；乱序、重复、缺失和延迟事件必须标记，不能在重放或回灌时静默覆盖真实事件。",
        "claim_type": "event_sequence_idempotency_rule",
        "sources": ["ecfr_242_613", "fix_exec_report", "nist_800_92"],
    },
    {
        "task": "P45-B-AUD05",
        "slug": "audit_trail_retention_and_integrity_required",
        "partition": "KB_AI_26_DATABASE_STORAGE",
        "tree_node": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "tree_path": "CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Audit Log Ledger",
        "domain": "storage_engineering",
        "subdomain": "audit_log_ledger",
        "title": "交易审计日志必须保留 retention 和完整性边界",
        "statement": "交易审计日志、订单事件日志和监管报告中间产物必须声明保留期、不可变或 append-only 策略、访问审计、校验和或 hash、归档与恢复路径；不能把普通应用日志当作可审计 ledger。",
        "claim_type": "audit_log_retention_integrity_rule",
        "sources": ["ecfr_242_613", "finra_cat", "nist_800_92"],
    },
    {
        "task": "P45-B-AUD06",
        "slug": "manual_vs_electronic_order_timestamp_boundary",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.audit_trail",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Audit Trail",
        "domain": "live_trading",
        "subdomain": "audit_trail",
        "title": "人工订单和电子订单时间戳边界必须分开",
        "statement": "人工订单事件、allocation、电子订单事件和高频自动化事件必须分开声明 timestamp source、granularity、allowed drift 和 evidence policy；不能用人工录入时间替代电子事件时间，也不能把电子事件精度要求泛化到所有人工流程。",
        "claim_type": "manual_electronic_timestamp_boundary_rule",
        "sources": ["esma_article_22c", "cat_clock_alert", "finra_cat", "ecfr_242_613"],
    },
]


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_trade_audit_{safe}_001.json"


def source_ref(source_key: str, index: int) -> dict[str, Any]:
    source = dict(SOURCES[source_key])
    source.update(
        {
            "source_id": f"src_{index:03d}",
            "accessed_at": TODAY,
            "version": None,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        }
    )
    return source


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, idx + 1) for idx, key in enumerate(item["sources"])]
    cid = f"cand_20260612_phase45_trade_audit_{item['task'].lower().replace('-', '_')}_001"
    primary_types = {"regulatory_doc", "regulatory_rule", "regulatory_guidance", "official_protocol_doc", "standard_doc"}
    primary_count = sum(1 for ref in refs if ref["source_type"] in primary_types)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": cid,
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 Audit Trail / Clock Sync candidate generated for strict external audit; not formal knowledge.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": item["tree_node"],
            "canonical_node_id": item["tree_node"],
            "tree_path": item["tree_path"],
            "related_nodes": [
                "kt.trading_engineering.data_engineering.audit_clock",
                "kt.live_execution.audit_trail",
                "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
                "kt.ai_engineering.database_storage_engineering.runtime_observability_trace",
            ],
            "partition_id": item["partition"],
            "domain": item["domain"],
            "subdomain": item["subdomain"],
            "rule_type": "audit_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trade_audit_trail_design",
                "clock_sync_review",
                "order_event_replay",
                "external_project_rag_retrieval",
                "ai_trader_project_design_audit",
            ],
            "classification_notes": "主归属 Trading Engineering / Audit Trail / Clock Sync；AUD05 的存储完整性由 Database/Storage owner 承接，但不得变成策略或执行 owner。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_trade_audit.{item['slug']}.v1",
            "evidence_summary": "Regulatory, CAT, ESMA, FINRA, FIX and NIST sources support clock synchronization, event-time, order-event audit trail, identifier mapping, sequence/idempotency, and retention/integrity boundaries.",
            "interpretation_notes": "本候选只定义交易审计链、事件时间和日志治理边界，不输出买卖点、仓位、止损止盈、杠杆、风险阈值或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_jurisdiction_and_venue_caveats",
            "asset": "general",
            "timeframe": "event_time",
            "data_granularity": "order_events_execution_reports_audit_logs",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要设计订单事件审计链、交易日志、监管报告输入或事件回放证据",
                "AI IDE 需要区分 event_time、receive_time、log_time、manual entry time 和 electronic event timestamp",
                "需要设计 client/broker/exchange ID 映射、幂等键、事件序列或审计日志完整性字段",
            ],
            "not_applicable_when": [
                "用户要求具体交易动作、仓位、杠杆、止损止盈或风险阈值",
                "需要法律合规结论时，应由对应司法辖区合规/法律 owner 判断",
                "需要 broker/venue 私有订单事实时，应由外接项目事实层和 Live Execution owner 提供",
                "只有普通应用日志且缺少事件时间、来源系统、actor、原因和完整性证据时，不能声称具备监管级审计链",
            ],
            "assumptions": [
                "Audit Trail / Clock Sync 是交易工程审计上下文，不是策略信号。",
                "所有 clock sync、timestamp precision 和 retention claim 必须声明适用市场、辖区、系统和事件类型。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "SEC/CAT/FINRA 来源主要用于美国 NMS/CAT 语境；ESMA 来源主要用于 EU/MiFIR 语境。",
                "NIST 日志管理来源是通用安全日志治理，不替代交易监管字段契约。",
                "FIX 是协议语义来源，不替代 broker/venue 的真实订单事实。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": round(sum(ref["score"] for ref in refs) / len(refs), 2),
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": primary_count,
            "supporting_source_count": len(refs) - primary_count,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "监管资料按地区适用，不能自动泛化到 crypto、外汇、非美市场或全部 broker。",
                "内部字段契约若后续用于 reviewed，需要提供 schema extract 或 contract hash。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Data Engineering / Live Execution formal reviewed knowledge",
                "Phase 42 Database/Storage contracts",
                "Phase 45 runtime contract",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有正式知识的直接冲突；Audit Trail / Clock Sync 与 Database/Storage 的关系按 owner/reference 边界处理。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计订单事件审计链、时间戳字段、ID 映射和日志完整性检查。",
                "用于生成 trade audit checklist、schema review、RAG 检索上下文和 reason code。",
                "用于检查外接项目方案是否遗漏 clock sync、event sequencing、idempotency 或 retention 边界。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得把监管来源泛化为所有市场的通用硬规则。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 45 candidate audit has not passed; formal reviewed requires later gate.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "review": {
            "confidence": "medium",
            "freshness": "mixed",
            "reviewer": "codex_candidate_generation",
            "reviewed_at": TODAY,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 audit trail / clock sync 边界？",
                "是否需要补充交易所、broker 或内部 schema contract 来源？",
                "是否存在与 Phase 37 formal reviewed 知识的重复，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 45 P45-B Audit Trail / Clock Sync 队列生成候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录 SEC、eCFR、ESMA、FINRA、CAT、FIX 和 NIST 等来源摘要。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "classified",
                    "reason": f"归类到 {item['partition']} / {item['tree_node']}。",
                },
            ],
        },
        "workflow": {
            "stage": "pending_external_audit",
            "allowed_next_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_next_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formal_knowledge_id": None,
            "audit_package_id": PACKAGE_ID,
        },
        "contribution": {
            "origin": "phase45_research_ingestion",
            "private_data_removed": True,
            "contains_project_private_strategy": False,
            "contains_secret": False,
            "notes": "通用 Trading Engineering 支持层候选知识，不包含外接项目私有交易事实。",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Audit Trail / Clock Sync 候选知识采集记录",
        "",
        "## 目标",
        "",
        "本批为 Phase 45 / P45-B / Audit Trail / Clock Sync 6 条候选知识。所有条目只进入 candidate，不创建正式 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 来源摘要",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 候选条目", "", "| research_task_id | candidate_id | partition | canonical_node_id | 来源数 |", "| --- | --- | --- | --- | --- |"])
    for item in candidates:
        lines.append(
            f"| {item['research_task_id']} | `{item['candidate_id']}` | `{item['classification']['partition_id']}` | `{item['classification']['canonical_node_id']}` | {len(item['source_refs'])} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. Audit Trail / Clock Sync 只解释订单事件审计链、时间同步、ID 映射、幂等和日志完整性边界。",
            "2. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘许可。",
            "3. SEC/CAT/FINRA/ESMA 来源具有辖区边界，不能泛化到所有市场。",
            "4. FIX 只能作为协议语义来源，不替代 broker/venue 真实订单事实。",
            "5. 候选必须等待外部 AI/人工审计。",
            "```",
        ]
    )
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 Audit Trail candidates, got {len(candidates)}")
    expected_tasks = {f"P45-B-AUD{idx:02d}" for idx in range(1, 7)}
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research_task_id set: {sorted(actual_tasks ^ expected_tasks)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    allowed_nodes = {
        "kt.trading_engineering.data_engineering.audit_clock",
        "kt.live_execution.audit_trail",
        "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
    }
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        if item.get("classification", {}).get("canonical_node_id") not in allowed_nodes:
            failures.append(f"{cid}: canonical_node_id not in Audit Trail nodes")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 2:
            failures.append(f"{cid}: primary_source_count < 2")
        gate = item.get("machine_gate", {})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase45_trade_audit_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "batch": BATCH,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批只是 Audit Trail / Clock Sync candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "时间同步、审计链和日志 retention 不能被写成策略信号或风控阈值。",
            "监管来源具有辖区边界，协议/日志标准来源只能作为语义和治理支撑。",
        ],
    }


def main() -> int:
    candidates: list[dict[str, Any]] = []
    for item in ITEMS:
        candidate = build_candidate(item)
        candidates.append(candidate)
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", item["partition"], start_file=__file__)
        write_json(cand_dir / slug_to_file_name(item["slug"]), candidate)
    write_research_report(candidates)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase45_trade_audit_candidate_generation_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "batch": BATCH,
            "candidate_count": len(candidates),
            "candidate_ids": [item["candidate_id"] for item in candidates],
            "research_report": "docs/research/phase45_trade_audit_candidate_research.md",
            "quality_gate": "docs/reports/phase45_trade_audit_candidate_quality_gate.json",
            "gate_status": gate["gate_status"],
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
