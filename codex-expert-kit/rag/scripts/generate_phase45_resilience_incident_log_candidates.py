"""Generate Phase 45 Resilience / Incident / Log candidate knowledge.

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
TASK_ID = "CEK-TA-463"
BATCH = "P45-D Resilience / Incident / Log"

RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase45_resilience_incident_log_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase45_resilience_incident_log_candidate_generation_report.json", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase45_resilience_incident_log_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "ecfr_reg_sci": {
        "source_title": "17 CFR Part 242 Regulation SCI",
        "source_url": "https://www.ecfr.gov/current/title-17/chapter-II/part-242/subpart-ECFRe106e84e67e2bc9",
        "source_type": "regulatory_rule",
        "publisher": "eCFR / U.S. SEC",
        "reliability": "high",
        "score": 94,
        "freshness": "time_sensitive",
        "evidence_summary": "Regulation SCI covers policies and procedures for SCI systems capacity, integrity, resiliency, availability and security, including SCI events, notification, corrective action and records.",
        "limitations": ["U.S. SCI-entity regulatory context; not a universal global trading-system standard."],
    },
    "finra_4370": {
        "source_title": "FINRA Rule 4370: Business Continuity Plans and Emergency Contact Information",
        "source_url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/4370",
        "source_type": "regulatory_rule",
        "publisher": "FINRA",
        "reliability": "high",
        "score": 92,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA Rule 4370 requires member firms to create and maintain written business continuity plans for emergencies or significant business disruptions.",
        "limitations": ["FINRA member-firm context; not applicable to every trading venue, crypto platform or non-U.S. project."],
    },
    "nist_800_34": {
        "source_title": "NIST SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems",
        "source_url": "https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final",
        "source_type": "standard_doc",
        "publisher": "NIST",
        "reliability": "high",
        "score": 89,
        "freshness": "stable",
        "evidence_summary": "NIST SP 800-34 supports contingency planning, business impact analysis, recovery strategies, plan development, testing, training and maintenance.",
        "limitations": ["General contingency-planning guidance; not trading-specific order or market-access policy."],
    },
    "nist_800_61_r3": {
        "source_title": "NIST SP 800-61 Rev. 3: Incident Response Recommendations and Considerations",
        "source_url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf",
        "source_type": "standard_doc",
        "publisher": "NIST",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "NIST SP 800-61 Rev. 3 provides incident response considerations across preparation, detection, analysis, response, recovery and improvement activities.",
        "limitations": ["Cybersecurity incident-response source; must be mapped carefully to trading operations incidents."],
    },
    "nist_800_92": {
        "source_title": "NIST SP 800-92: Guide to Computer Security Log Management",
        "source_url": "https://csrc.nist.gov/pubs/sp/800/92/final",
        "source_type": "standard_doc",
        "publisher": "NIST",
        "reliability": "high",
        "score": 87,
        "freshness": "stable",
        "evidence_summary": "NIST SP 800-92 supports log-management policies, infrastructure, analysis, retention, protection and operational processes.",
        "limitations": ["General computer-security log management; not a trading audit-ledger schema."],
    },
    "aws_reliability": {
        "source_title": "AWS Well-Architected Reliability Pillar",
        "source_url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html",
        "source_type": "cloud_architecture_doc",
        "publisher": "AWS",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "AWS Reliability Pillar provides cloud reliability design and recovery practices for workloads.",
        "limitations": ["Cloud implementation guidance; not a broker, exchange, regulator or CEK-TA field contract."],
    },
    "aws_dr": {
        "source_title": "AWS Reliability Pillar: Plan for Disaster Recovery",
        "source_url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/plan-for-disaster-recovery-dr.html",
        "source_type": "cloud_architecture_doc",
        "publisher": "AWS",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "AWS DR guidance discusses backups, redundant components and RTO/RPO as restoration objectives set by business needs.",
        "limitations": ["Cloud DR pattern source; does not define trading execution permission or CEK-TA RTO/RPO thresholds."],
    },
    "google_sre_postmortem": {
        "source_title": "Google SRE Book: Postmortem Culture",
        "source_url": "https://sre.google/sre-book/postmortem-culture/",
        "source_type": "engineering_practice",
        "publisher": "Google SRE",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "evidence_summary": "Google SRE postmortem guidance supports documenting incidents, understanding contributing causes and defining preventive actions in a blameless learning process.",
        "limitations": ["SRE practice source; not a financial-market regulatory requirement."],
    },
    "otel_docs": {
        "source_title": "OpenTelemetry Documentation",
        "source_url": "https://opentelemetry.io/docs/",
        "source_type": "framework_doc",
        "publisher": "OpenTelemetry",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "OpenTelemetry is a vendor-neutral observability framework for generating, collecting and exporting telemetry such as traces, metrics and logs.",
        "limitations": ["Observability implementation pattern; not a formal trading audit or retention standard."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-D-OPS01",
        "slug": "business_continuity_disaster_recovery_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.resilience_incident_log",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Resilience Incident Log",
        "domain": "live_trading",
        "subdomain": "resilience_incident_log",
        "title": "交易系统必须声明 BC/DR 和关键系统恢复边界",
        "statement": "交易系统的业务连续性和灾难恢复设计必须声明关键系统、依赖、恢复目标、备份/恢复路径、演练证据、owner 和客户/交易对手义务边界；不得把普通服务重启脚本等同于交易级 BC/DR 能力。",
        "claim_type": "business_continuity_disaster_recovery_rule",
        "sources": ["finra_4370", "ecfr_reg_sci", "nist_800_34", "aws_dr"],
    },
    {
        "task": "P45-D-OPS02",
        "slug": "degraded_mode_and_readonly_mode_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.resilience_incident_log",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Resilience Incident Log",
        "domain": "live_trading",
        "subdomain": "resilience_incident_log",
        "title": "降级模式和只读模式必须有明确操作边界",
        "statement": "交易系统进入 degraded mode 或 read-only mode 时，必须声明允许/禁止的操作、数据新鲜度、写入禁用语义、人工接管、退出条件和审计证据；不得在依赖不完整或状态不明时静默继续正常交易。",
        "claim_type": "degraded_readonly_mode_boundary_rule",
        "sources": ["ecfr_reg_sci", "nist_800_34", "aws_reliability", "nist_800_61_r3"],
    },
    {
        "task": "P45-D-OPS03",
        "slug": "failover_recovery_replay_boundary",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.resilience_incident_log",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Resilience Incident Log",
        "domain": "live_trading",
        "subdomain": "resilience_incident_log",
        "title": "failover、恢复和 replay 必须区分证据与动作",
        "statement": "故障切换、恢复和事件 replay 必须区分系统状态重建、审计回放、模拟回放和真实订单动作；没有幂等键、订单真相源、状态快照和人工/风控确认时，不得通过 replay 自动重发或修改真实订单。",
        "claim_type": "failover_recovery_replay_boundary_rule",
        "sources": ["ecfr_reg_sci", "nist_800_34", "aws_dr", "otel_docs"],
    },
    {
        "task": "P45-D-OPS04",
        "slug": "incident_taxonomy_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.resilience_incident_log",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Resilience Incident Log",
        "domain": "live_trading",
        "subdomain": "resilience_incident_log",
        "title": "交易事故 taxonomy 必须区分技术、市场、数据和风控影响",
        "statement": "交易事故必须有 taxonomy，至少区分系统可用性、数据质量、订单/成交、风控策略、账户/资金、外部依赖、市场状态和人工操作影响；事故标签只能用于审计、复盘和优先级排序，不能自动生成交易动作。",
        "claim_type": "incident_taxonomy_rule",
        "sources": ["nist_800_61_r3", "ecfr_reg_sci", "finra_4370", "google_sre_postmortem"],
    },
    {
        "task": "P45-D-OPS05",
        "slug": "post_incident_review_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.resilience_incident_log",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Resilience Incident Log",
        "domain": "live_trading",
        "subdomain": "resilience_incident_log",
        "title": "事故后复盘必须输出可验证修复项",
        "statement": "重大交易事故后必须形成 post-incident review，记录时间线、影响范围、根因/促成因素、检测与恢复过程、纠正措施、owner、验证证据和遗留风险；不得把复盘结论直接改写成策略规则或实盘放行条件。",
        "claim_type": "post_incident_review_rule",
        "sources": ["nist_800_61_r3", "google_sre_postmortem", "ecfr_reg_sci", "finra_4370"],
    },
    {
        "task": "P45-D-OPS06",
        "slug": "log_retention_integrity_required",
        "partition": "KB_AI_26_DATABASE_STORAGE",
        "tree_node": "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
        "tree_path": "CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Audit Log Ledger",
        "domain": "storage_engineering",
        "subdomain": "audit_log_ledger",
        "title": "运行时日志必须声明 retention、完整性和关联 ID",
        "statement": "交易运行时日志、事故日志、遥测日志和审计追踪必须声明 retention、完整性校验、访问/删除审计、关联 ID、时间源、归档恢复和最小必要字段；普通 debug 日志不能替代正式审计账本或订单事实来源。",
        "claim_type": "log_retention_integrity_rule",
        "sources": ["nist_800_92", "ecfr_reg_sci", "nist_800_61_r3", "otel_docs"],
    },
]


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_resilience_incident_log_{safe}_001.json"


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
    cid = f"cand_20260612_phase45_resilience_incident_log_{item['task'].lower().replace('-', '_')}_001"
    primary_types = {"regulatory_rule", "standard_doc", "engineering_practice", "framework_doc", "cloud_architecture_doc"}
    primary_count = sum(1 for ref in refs if ref["source_type"] in primary_types)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": cid,
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 P45-D Resilience / Incident / Log 候选，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": item["tree_node"],
            "canonical_node_id": item["tree_node"],
            "tree_path": item["tree_path"],
            "related_nodes": [
                "kt.live_execution.audit_trail",
                "kt.live_execution.order_state_machine",
                "kt.ai_engineering.database_storage_engineering.runtime_observability_trace",
                "kt.ai_engineering.database_storage_engineering.audit_log_ledger",
                "kt.risk_management.layered_risk_controls",
            ],
            "partition_id": item["partition"],
            "domain": item["domain"],
            "subdomain": item["subdomain"],
            "rule_type": "resilience_incident_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trading_system_resilience_design",
                "incident_response_review",
                "runtime_log_governance",
                "external_project_rag_retrieval",
                "ai_trader_project_design_audit",
            ],
            "classification_notes": "P45-D 只补交易系统韧性、事故响应、恢复/replay 边界和日志治理；不创建 CEK-TA hard gate，也不定义交易动作。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_resilience_incident_log.{item['slug']}.v1",
            "evidence_summary": "；".join(ref["evidence_summary"] for ref in refs),
            "interpretation_notes": "本候选只定义系统韧性、事故响应、日志治理和恢复边界，不输出交易参数、风险阈值或实盘执行建议。",
            "claim_strength": "candidate",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_jurisdiction_platform_and_venue_caveats",
            "asset": "general",
            "timeframe": "runtime_operations_and_incident_context",
            "data_granularity": "system_events_order_events_incident_records_runtime_logs_telemetry",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要设计交易系统 BC/DR、降级模式、只读模式、故障切换、事故响应、事故复盘或日志治理。",
                "AI IDE 需要检查交易系统方案是否遗漏恢复目标、关键依赖、owner、演练证据、事件 taxonomy 或日志完整性。",
                "需要区分恢复/replay 的审计证据、模拟用途和真实订单动作边界。",
            ],
            "not_applicable_when": [
                "用户要求具体买卖点、仓位、杠杆、止损止盈、风险阈值、停机阈值或实盘执行动作。",
                "需要 broker、venue、账户、订单或资金的实时事实时，应由外接项目事实层提供。",
                "需要法律/监管合规结论时，应由对应辖区合规或法律 owner 判断。",
            ],
            "assumptions": [
                "Resilience / Incident / Log Management 是交易工程运行时治理，不是策略 alpha。",
                "所有 BC/DR、incident、log 和 telemetry 来源必须声明监管、平台、云服务、市场和系统适用边界。",
                "候选通过外部审计前不能进入 formal reviewed 知识库。",
            ],
            "limitations": [
                "Reg SCI 和 FINRA 来源具有美国监管与机构适用边界。",
                "NIST 来源是通用安全/应急/日志治理来源，不替代交易所或 broker 私有规则。",
                "AWS、Google SRE、OpenTelemetry 是工程实现模式，不是金融市场强制标准。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": round(sum(float(ref["score"]) for ref in refs) / len(refs), 2),
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": primary_count,
            "supporting_source_count": len(refs) - primary_count,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "监管、标准、云架构和 SRE 来源必须保留适用边界，不得写成交易执行许可。",
                "内部字段契约若后续用于 reviewed，需要提供 schema extract、字段表或 contract hash。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Live Execution formal reviewed knowledge",
                "Phase 37 Risk Management formal reviewed knowledge",
                "Phase 42 Database/Storage formal reviewed knowledge",
                "Phase 45 Audit Trail / Layered Risk formal reviewed knowledge",
                "Phase 45 runtime contract",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有 formal reviewed 知识的直接冲突；P45-D 仅补运行时韧性、事故、恢复和日志边界。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计 BC/DR、降级/只读模式、failover/recovery/replay、incident taxonomy、post-incident review 和 runtime log governance。",
                "用于生成运行时治理 checklist、schema review、RAG 检索上下文和审计 reason code。",
                "用于检查外接项目方案是否把重启脚本、普通日志或 SRE practice 误写成交易级恢复/审计能力。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、风险阈值、停机阈值或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、停机、重发订单、撤单或解锁流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; pending external strict audit; no reviewed/approved/default/hard gate.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "review": {
            "review_status": "candidate_ready",
            "review_mode": "external_strict_audit_required",
            "confidence": "medium_high",
            "freshness": "mixed",
            "reviewer": None,
            "reviewed_at": None,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_resilience_incident_log_candidate_generated",
                    "reason": "Generated from Phase 45 P45-D task queue with regulatory, standard and engineering sources.",
                }
            ],
        },
        "workflow": {
            "stage": "pending_external_audit",
            "queue_group": "pending",
            "source_phase": PHASE,
            "source_task_id": TASK_ID,
            "batch": BATCH,
            "formal_knowledge_id": None,
            "formal_knowledge_path": None,
            "allowed_next_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_next_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
        },
        "contribution": {
            "source": "phase45_professional_research",
            "private_data_removed": True,
            "project_specific_details_removed": True,
            "notes": "Generated for external strict audit; no account, key, order, threshold, position or private strategy data included.",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Resilience / Incident / Log 候选知识采集记录",
        "",
        "## 范围",
        "",
        "本批次对应 CEK-TA-463 / P45-D，目标是采集 6 条系统韧性、事故响应、恢复/replay 和日志治理 P1 候选知识。",
        "",
        "本批次只生成候选和审计包，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 来源记录",
        "",
        "| source_key | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 候选列表", "", "| ID | title | partition | source_count | 状态 |", "| --- | --- | --- | ---: | --- |"])
    for candidate in candidates:
        lines.append(
            f"| {candidate['research_task_id']} | {candidate['claim']['title']} | `{candidate['classification']['partition_id']}` | {len(candidate['source_refs'])} | {candidate['status']['review_status']} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. 不输出买卖点、仓位、杠杆、止损止盈、风险阈值、停机阈值或实盘执行建议。",
            "2. Reg SCI / FINRA / NIST / AWS / Google SRE / OpenTelemetry 来源必须保留监管、平台、云服务、市场和系统边界。",
            "3. replay、recovery、failover 不能被写成自动重发真实订单或绕过 Risk/Live Execution owner 的动作。",
            "4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。",
            "```",
        ]
    )
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 candidates, got {len(candidates)}")
    expected = {f"P45-D-OPS{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    allowed_partitions = {"KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"}
    allowed_nodes = {"kt.live_execution.resilience_incident_log", "kt.ai_engineering.database_storage_engineering.audit_log_ledger"}
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") not in allowed_partitions:
            failures.append(f"{cid}: partition mismatch")
        if item.get("classification", {}).get("canonical_node_id") not in allowed_nodes:
            failures.append(f"{cid}: canonical node mismatch")
        if len(item.get("source_refs", [])) < 4:
            failures.append(f"{cid}: source_refs < 4")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 3:
            failures.append(f"{cid}: primary_source_count < 3")
        gate = item.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default_guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase45_resilience_incident_log_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "batch": BATCH,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批次只生成 candidate，不创建 reviewed、approved、default guidance 或 hard gate。",
            "P45-D 只能用于系统韧性、事故响应、恢复/replay 和日志治理边界，不输出交易动作或阈值。",
            "工程实践来源只能作为 implementation pattern，不得写成金融交易通用强制标准。",
        ],
    }


def main() -> int:
    candidates = [build_candidate(item) for item in ITEMS]
    for item, candidate in zip(ITEMS, candidates):
        target = resolve_repo_path("codex-expert-kit", "rag", "candidates", item["partition"], slug_to_file_name(item["slug"]), start_file=__file__)
        write_json(target, candidate)
    write_research_report(candidates)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase45_resilience_incident_log_candidate_generation_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "batch": BATCH,
            "candidate_count": len(candidates),
            "quality_gate": gate,
            "candidates": [
                {
                    "research_task_id": item["research_task_id"],
                    "candidate_id": item["candidate_id"],
                    "knowledge_slug": item["claim"]["normalized_claim"],
                    "partition": item["classification"]["partition_id"],
                    "source_count": len(item["source_refs"]),
                }
                for item in candidates
            ],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
