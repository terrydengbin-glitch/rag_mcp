"""Apply Phase 45 Resilience / Incident / Log reviewed preparation result.

This imports the strict reviewed/caveat_only preparation audit for P45-D. Four
entries are materialized as formal reviewed/caveat_only knowledge. OPS04 and
OPS06 are supplemented and exported for another strict re-audit.

It never creates approved knowledge, default guidance, hard gates, risk
thresholds, stop thresholds, legal compliance conclusions, or live trading
actions.
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
TASK_ID = "CEK-TA-464"
AUDIT_RESULT_ID = "audit_phase45_resilience_incident_log_reviewed_preparation_20260612"
SOURCE_PACKAGE_ID = "phase45_resilience_incident_log_reviewed_preparation_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_AI_26_DATABASE_STORAGE"]

AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_resilience_incident_log_formal_import_report.json", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path(
    "docs", "reports", "phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_gate.json", start_file=__file__
)
SUPPLEMENTAL_RESEARCH = resolve_repo_path(
    "docs", "research", "phase45_resilience_incident_log_reviewed_blocked_supplemental_research.md", start_file=__file__
)
RUNTIME_CONTRACT = resolve_repo_path("docs", "contracts", "phase45_resilience_incident_log_runtime_contract.md", start_file=__file__)
REPO_ROOT = resolve_repo_path(".", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-D-OPS01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "BC/DR、关键系统、依赖、备份恢复、owner、客户/交易对手边界有 FINRA Rule 4370、Reg SCI、NIST SP 800-34、AWS DR 支撑。"
        ],
        "required_followups": [
            "正式文本中保留 FINRA member firm、Reg SCI entity、NIST general contingency、AWS cloud pattern caveat。",
            "恢复目标只能要求声明 owner/evidence，不得写 CEK-TA 固定 RTO/RPO 数值。",
        ],
        "patch_notes": {
            "source": ["保留 FINRA Rule 4370、Reg SCI、NIST SP 800-34、AWS DR。"],
            "content": ["将“交易系统必须”收窄为“进入 CEK-TA reviewed/caveat_only 的交易系统韧性知识应要求声明”。"],
            "boundary": ["不得生成恢复阈值、停机阈值、自动重启、自动撤单或自动重发订单。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-D-OPS02",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "补证已覆盖 graceful degradation、degraded response、read-only database mode 和 CEK-TA runtime mode contract。"
        ],
        "required_followups": [
            "正式文本必须说明 Google SRE/AWS 是工程实践，不是金融监管要求。",
            "PostgreSQL 只能作为 read-only 实现示例，外接项目可使用等价数据库权限、服务层写禁用或访问控制。",
            "退出条件只能声明 owner、证据和审计 trace，不能写停机阈值、恢复阈值或自动拒单规则。",
        ],
        "patch_notes": {
            "source": ["保留 Google SRE Handling Overload、AWS graceful degradation、PostgreSQL Hot Standby、CEK-TA runtime contract。"],
            "content": ["将“退出条件”固定为 owner/evidence/audit_trace 维度，不允许数值阈值化。"],
            "boundary": ["不得输出自动拒单、自动撤单、自动重发订单、自动恢复交易或风险阈值变更。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-D-OPS03",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "补证已覆盖 FIX cancel/replace 身份链、CancelReject 边界、Binance client order id 示例、IBKR order identifier 复用/修改边界和 CEK-TA replay contract。"
        ],
        "required_followups": [
            "正式文本必须说明 FIX、Binance、IBKR 是协议/venue/broker 示例，不能泛化为所有交易所和券商。",
            "外接项目必须提供自己的 order_state_machine / order truth source contract。",
            "OpenTelemetry 只能作为 trace/audit_trace_id 辅助来源，不能作为订单 replay 权限来源。",
        ],
        "patch_notes": {
            "source": ["保留 FIX Order Cancel/Replace、FIX OrderCancelReject、Binance Futures New Order、IBKR TWS API、CEK-TA runtime contract。"],
            "content": ["保留四分法；state_rebuild 只能重建内部状态视图，不得写入 venue/broker。"],
            "boundary": ["不得输出自动重发订单、自动撤单、自动修改订单、恢复阈值或风控阈值。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-D-OPS04",
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reviewed_allowed": False,
        "reasons": [
            "当前 claim 仍写成外部强制 taxonomy，尚未明确为 CEK-TA 内部 taxonomy。",
            "来源支撑 incident response、SCI event、postmortem 和 BCP，但不直接支撑该具体交易事故分类表作为外部标准。",
        ],
        "required_followups": [
            "将 statement 改为 CEK-TA reviewed/caveat_only 内部事故 taxonomy 建议至少覆盖系统可用性、数据质量、订单/成交、风控策略、账户/资金、外部依赖、市场状态和人工操作影响。",
            "补 incident taxonomy schema：category、impact_area、affected_system、market_impact、data_quality、order_state、human_action、audit_trace_id。",
            "明确 taxonomy label 只能进入 audit/review/priority queue，不能触发交易动作、风控阈值或 hard gate。",
        ],
        "patch_notes": {
            "source": ["Reg SCI/NIST/Google SRE 只能支撑事故响应和复盘框架，不能声称支持该具体 taxonomy 原文。"],
            "content": ["删除或收窄“交易事故必须有 taxonomy”的泛化强制语气。", "加入“CEK-TA internal taxonomy”限定。"],
            "boundary": ["事故标签不得自动生成交易动作。", "事故标签不得自动生成风险阈值、停机阈值或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-D-OPS05",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "reasons": [
            "post-incident review 的时间线、影响范围、根因/促成因素、检测与恢复过程、纠正措施、owner、验证证据和遗留风险，能够由 Google SRE、NIST SP 800-61、Reg SCI 支撑。"
        ],
        "required_followups": [
            "正式文本保留 caveat：Google SRE 是工程实践，不是金融监管要求。",
            "补 post_incident_review schema：timeline、impact_scope、contributing_factors、detection、recovery、corrective_actions、owner、verification_evidence、residual_risk。",
            "复盘 action item 只能进入工程修复/审计队列，不得直接成为策略规则或实盘放行条件。",
        ],
        "patch_notes": {
            "source": ["保留 NIST SP 800-61、Google SRE postmortem、Reg SCI、FINRA Rule 4370。"],
            "content": ["将“重大交易事故后必须形成”收窄为 CEK-TA reviewed/caveat_only 的运行事故复盘要求。"],
            "boundary": ["不得生成策略规则、实盘放行条件、自动恢复规则或风险阈值。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-D-OPS06",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reviewed_allowed": False,
        "reasons": [
            "当前 reviewed preparation 包未补入 SEC Rule 17a-4、FINRA 4511、CFTC 1.31 和 audit ledger schema。",
            "NIST SP 800-92 支撑通用 log management；OpenTelemetry 只支撑 telemetry，不是金融审计账本或订单事实来源。",
        ],
        "required_followups": [
            "补 SEC Rule 17a-4 或 SEC electronic recordkeeping amendments，覆盖 WORM/audit-trail、time-stamped audit trail、修改/删除记录。",
            "补 FINRA Rule 4511，覆盖 books and records 保存义务。",
            "如覆盖 futures/derivatives 场景，补 CFTC Regulation 1.31。",
            "补 CEK-TA audit ledger schema：correlation_id、event_id、source_ts、ingest_ts、actor、hash、prev_hash、access_log、delete_log、retention_policy_ref、order_truth_source_ref。",
            "明确 debug_log、telemetry_log、incident_log、audit_ledger、order_truth_source 的层级边界。",
        ],
        "patch_notes": {
            "source": [
                "NIST SP 800-92 保留为通用日志管理来源。",
                "OpenTelemetry 保留为 observability/telemetry 来源。",
                "必须新增 SEC/FINRA/CFTC 金融记录保存来源，否则不能进入 reviewed/caveat_only。",
            ],
            "content": [
                "retention 数值留给 jurisdiction/platform/compliance owner，不得在 CEK-TA 中写死。",
                "普通 debug 日志不能替代 audit ledger；audit ledger 也不能替代 venue/broker/order source of truth。",
            ],
            "boundary": [
                "日志完整性不得推导交易许可。",
                "日志或审计账本不得触发 hard gate、自动恢复、自动撤单或自动重发。",
            ],
            "conflict": [],
        },
    },
]


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "phase45_runtime_contract": {
        "source_title": "Phase 45 Resilience / Incident / Log Runtime Contract",
        "source_url": "docs/contracts/phase45_resilience_incident_log_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 90,
        "freshness": "current",
        "relevance": "high",
        "evidence_summary": "CEK-TA contract now defines incident_taxonomy, audit_ledger_event, log layer boundaries, runtime mode and replay boundary schemas.",
        "limitations": ["Internal CEK-TA contract; use with external supporting sources."],
    },
    "sec_rule_17a_4": {
        "source_title": "17 CFR § 240.17a-4 Records to be preserved by certain exchange members, brokers and dealers",
        "source_url": "https://www.law.cornell.edu/cfr/text/17/240.17a-4",
        "source_type": "regulatory_rule",
        "publisher": "Legal Information Institute / eCFR-derived CFR text",
        "reliability": "high",
        "score": 91,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Rule 17a-4 supports broker-dealer records preservation and electronic recordkeeping audit-trail requirements.",
        "limitations": ["U.S. broker-dealer recordkeeping context; not universal global retention policy."],
    },
    "finra_rule_4511": {
        "source_title": "FINRA Rule 4511 General Requirements",
        "source_url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/4511",
        "source_type": "regulatory_rule",
        "publisher": "FINRA",
        "reliability": "high",
        "score": 92,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "FINRA Rule 4511 requires members to make and preserve books and records under FINRA rules, Exchange Act and applicable Exchange Act rules, and preserve records in a format/media compliant with SEA Rule 17a-4.",
        "limitations": ["FINRA member-firm context; not a universal global trading log standard."],
    },
    "cftc_reg_1_31": {
        "source_title": "17 CFR § 1.31 Regulatory records; retention and production",
        "source_url": "https://www.ecfr.gov/current/title-17/chapter-I/part-1/subject-group-ECFR26e2c365a191fa7/section-1.31",
        "source_type": "regulatory_rule",
        "publisher": "eCFR / CFTC",
        "reliability": "high",
        "score": 91,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "CFTC Regulation 1.31 supports regulatory records retention, authenticity, reliability, production and electronic regulatory record controls.",
        "limitations": ["CFTC regulated records context; not universal for all products or jurisdictions."],
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
        candidate_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(candidate_dir.glob("cand_20260612_phase45_resilience_incident_log_*.json")))
    return paths


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def source_ref(source_key: str, source_id: str) -> dict[str, Any]:
    source = dict(SUPPLEMENTAL_SOURCES[source_key])
    source.update({"source_id": source_id, "accessed_at": TODAY, "version": None, "quoted_excerpt_allowed": False})
    return source


def upsert_sources(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    source_refs = list(candidate.get("source_refs", []))
    existing_urls = {ref.get("source_url") for ref in source_refs}
    for ref in refs:
        if ref.get("source_url") not in existing_urls:
            source_refs.append(ref)
            existing_urls.add(ref.get("source_url"))
    candidate["source_refs"] = source_refs
    candidate.setdefault("source_quality", {})["primary_source_count"] = len(source_refs)
    candidate["source_quality"]["supporting_source_count"] = 0
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 75)) for ref in source_refs) / len(source_refs), 2)


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_reviewed_caveat_only": 4,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "stop_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
        },
        "candidate_results": [
            {
                "candidate_id": "",
                "research_task_id": item["research_task_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reviewed_allowed": item["reviewed_allowed"],
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": item["reasons"],
                "required_followups": item["required_followups"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
    }


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim", {})
    classification = candidate.get("classification", {})
    applicability = candidate.get("applicability", {})
    normalized = str(claim.get("normalized_claim") or candidate.get("research_task_id", ""))
    knowledge_id = f"kb_phase45_resilience_incident_log.{normalized.replace('phase45_resilience_incident_log.', '')}"
    if not knowledge_id.endswith(".v1"):
        knowledge_id += ".v1"
    source_refs = candidate.get("source_refs", [])
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": claim.get("title") or candidate.get("research_task_id"),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": "resilience_incident_boundary_rule",
            "claim_type": classification.get("claim_type"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification.get("tree_node_id"),
            "tree_path": classification.get("tree_path"),
            "canonical_node_id": classification.get("canonical_node_id"),
            "canonical_tree_path": classification.get("tree_path"),
            "risk_level": "high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 45",
            "related_nodes": classification.get("related_nodes", []),
            "classification_notes": "Phase 45 Resilience / Incident / Log formal reviewed/caveat_only；只用于系统韧性、事故响应、恢复/replay 边界和日志治理，不是 approved/default guidance/hard gate，不生成交易动作、阈值或法律合规结论。",
        },
        "applicability": {
            "market": applicability.get("market"),
            "asset": applicability.get("asset"),
            "timeframe": applicability.get("timeframe"),
            "data_granularity": applicability.get("data_granularity"),
            "project_type": applicability.get("project_type"),
            "applies_when": applicability.get("applies_when", []),
            "not_applicable_when": applicability.get("not_applicable_when", []),
        },
        "content": {
            "statement": claim.get("statement"),
            "rationale": claim.get("interpretation_notes"),
            "normalized_claim": normalized,
            "claim_strength": "reviewed_caveat_only",
            "performance_claim": False,
            "procedure": [
                "确认问题属于系统韧性、事故响应、降级/只读模式、恢复/replay、post-incident review 或运行时日志治理。",
                "检查来源是否只在其辖区、平台、协议、数据库或工程实践边界内使用。",
                "检查是否声明 owner、evidence、audit_trace、状态字段和不适用场景。",
                "遇到 replay、recovery、read_only、incident label 或 log integrity 时，不得推导自动实盘动作或 hard gate。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "anti_patterns": [
                "把 reviewed/caveat_only 当作 approved 或 default guidance。",
                "把事故标签、日志完整性、恢复回放、read-only mode 自动解释为拒单、撤单、重发订单、恢复交易或 hard gate。",
                "输出停机阈值、恢复阈值、风险阈值、买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            ],
            "validation": [
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "source_evidence 必须保留监管、标准、工程实践、协议、数据库或内部 contract 的适用边界。",
            ],
            "risk_notes": [
                "本条只做系统韧性与事故治理知识，不代表交易系统可自动动作。",
                "监管来源具有辖区边界；工程来源和协议来源具有实现边界。",
                "本条不是 approved，不进入默认指导，不启用 hard gate。",
            ],
            "citation_notes": "；".join(str(ref.get("evidence_summary", "")) for ref in source_refs if ref.get("evidence_summary")),
            "audit_patch_notes": result["patch_notes"],
        },
        "assumptions": applicability.get("assumptions", []),
        "source_evidence": source_refs,
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": candidate.get("conflict_audit", {}).get("checked_against", []),
            "conflicts": [],
            "resolution_summary": "reviewed/caveat_only 准备审计通过；formal creation 保持 caveat_only，不创建 approved、default guidance、hard gate、风险阈值、停机阈值或自动实盘动作。",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
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
            "automatic_live_action_allowed": False,
            "approved_at": None,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": result["reasons"],
                "required_followups": result["required_followups"],
                "patch_notes": result["patch_notes"],
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计系统韧性、事故响应、runtime mode、replay boundary、post-incident review 和日志治理。",
                "用于生成运行时治理 checklist、schema review、RAG 检索上下文和审计 reason code。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、风险阈值、停机阈值、恢复阈值或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、停机、撤单、重发订单、恢复交易或解锁流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_visibility": "reviewed_caveat_only",
            "reason": "reviewed/caveat_only audit passed; approved/default guidance/hard gate/risk threshold advice remain disabled.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
        },
        "contribution": candidate.get("contribution", {}),
    }


def supplement_candidate(candidate: dict[str, Any], result: dict[str, Any]) -> None:
    task_id = str(candidate.get("research_task_id"))
    if task_id == "P45-D-OPS04":
        candidate["claim"]["statement"] = (
            "CEK-TA reviewed/caveat_only 的交易事故内部 taxonomy 建议至少覆盖 system_availability、data_quality、"
            "order_and_fill、risk_policy、account_and_funding、external_dependency、market_state 和 human_action。"
            "该 taxonomy 只用于 audit、review、priority queue、post-incident review 或 RAG 检索上下文，不得自动触发交易动作、"
            "风控阈值、停机阈值、拒单、撤单、重发订单或 hard gate。"
        )
        candidate["claim"]["evidence_summary"] = (
            "Reg SCI/NIST/Google SRE 支撑事故响应和复盘框架；CEK-TA runtime contract 内联 incident_taxonomy schema，"
            "明确 taxonomy_scope=CEK-TA internal taxonomy 以及 category、impact_area、affected_system、market_impact、data_quality、order_state、human_action、audit_trace_id 字段。"
        )
        upsert_sources(candidate, [source_ref("phase45_runtime_contract", "src_supp_reviewed_001")])
    elif task_id == "P45-D-OPS06":
        candidate["claim"]["statement"] = (
            "交易运行时日志、事故日志、遥测日志和审计账本必须声明 retention_policy_ref、jurisdiction_scope、完整性校验、"
            "访问/删除审计、关联 ID、时间源、归档恢复和最小必要字段。debug_log、telemetry_log、incident_log、audit_ledger "
            "和 order_truth_source 必须分层；普通 debug 日志不能替代正式 audit ledger，audit ledger 也不能替代 broker/venue/order source of truth。"
        )
        candidate["claim"]["evidence_summary"] = (
            "NIST SP 800-92 支撑通用 log management；OpenTelemetry 支撑 telemetry/traces/metrics/logs；SEC Rule 17a-4、FINRA 4511 "
            "和 CFTC 1.31 支撑金融记录保存、电子记录、audit trail、真实性、可靠性和生产要求；CEK-TA runtime contract 内联 audit_ledger_event schema。"
        )
        upsert_sources(
            candidate,
            [
                source_ref("sec_rule_17a_4", "src_supp_reviewed_001"),
                source_ref("finra_rule_4511", "src_supp_reviewed_002"),
                source_ref("cftc_reg_1_31", "src_supp_reviewed_003"),
                source_ref("phase45_runtime_contract", "src_supp_reviewed_004"),
            ],
        )
    candidate["status"]["review_status"] = "needs_more_evidence"
    candidate["status"]["ingestion_decision"] = "needs_more_evidence"
    candidate["status"]["decision_reason"] = "reviewed/caveat_only 准备审计未通过，已按审计意见补证并导出再审包。"
    candidate["status"]["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence_supplemented"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["allowed_next_decisions"] = ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "decision": "needs_more_evidence",
        "confidence": result["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase45_resilience_incident_log_reviewed_preparation_supplemented",
            "reason": "按 reviewed/caveat_only 审计意见补证，等待再审。",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    output: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in candidate_paths():
        item = read_json(path)
        output[str(item.get("research_task_id"))] = (path, item)
    return output


def export_supplemental_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 2:
        failures.append(f"expected 2 supplemental candidates, got {len(candidates)}")
    for item in candidates:
        if item.get("status", {}).get("ingestion_decision") != "needs_more_evidence":
            failures.append(f"{item.get('research_task_id')}: not in needs_more_evidence")
        if len(item.get("source_refs", [])) < 5:
            failures.append(f"{item.get('research_task_id')}: source_refs < 5")
    gate = {
        "gate_id": "phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_gate",
        "checked_at": TODAY,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 2,
        "runtime_contract": repo_relative(RUNTIME_CONTRACT),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只允许判断 OPS04/OPS06 是否可进入 formal reviewed/caveat_only。",
            "不得创建 approved、default guidance、hard gate、风险阈值、停机阈值或自动实盘动作。",
        ],
    }
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "45",
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / Live Execution / Resilience Incident Log",
            "target": "复审 OPS04 incident taxonomy 和 OPS06 log retention / audit ledger 补证后是否可进入 formal reviewed/caveat_only。",
            "candidate_count": len(candidates),
        },
        "hard_boundaries": {
            "reviewed_caveat_only_max": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "automatic_live_action_allowed": False,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、监管资料、官方文档、SRE/日志治理资料和案例，对补证包进行严格再审。",
            "OPS04：确认 taxonomy 已收窄为 CEK-TA internal taxonomy，且字段 schema、owner 和不触发交易动作边界充分。",
            "OPS06：确认 SEC Rule 17a-4、FINRA 4511、CFTC 1.31、NIST SP 800-92、OpenTelemetry 和 CEK-TA audit ledger schema 的来源分工正确。",
            "输出只能是 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {
                "total": 2,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-D-OPS04 | P45-D-OPS06",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "reviewed_allowed": "boolean",
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
        "candidates": candidates,
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)
    write_json(SUPPLEMENTAL_GATE, gate)
    return gate


def write_supplemental_research() -> None:
    content = [
        "# Phase 45 Resilience / Incident / Log reviewed 阻断项补证记录",
        "",
        "## OPS04 Incident Taxonomy",
        "",
        "补丁：将 taxonomy 明确收窄为 CEK-TA internal taxonomy，并在 runtime contract 中补充 `incident_taxonomy` schema。",
        "",
        "边界：taxonomy label 只能进入 audit、review、priority queue、post-incident review 或 RAG 检索上下文，不得自动触发交易动作、风控阈值、停机阈值、拒单、撤单、重发订单或 hard gate。",
        "",
        "## OPS06 Log Retention / Audit Ledger",
        "",
        "| 来源 | URL | 用途 |",
        "| --- | --- | --- |",
        "| SEC Rule 17a-4 | https://www.law.cornell.edu/cfr/text/17/240.17a-4 | broker-dealer records preservation 与 electronic recordkeeping audit trail 支撑 |",
        "| FINRA Rule 4511 | https://www.finra.org/rules-guidance/rulebooks/finra-rules/4511 | books and records 保存义务，并引用 SEA Rule 17a-4 的格式/介质要求 |",
        "| CFTC Regulation 1.31 | https://www.ecfr.gov/current/title-17/chapter-I/part-1/subject-group-ECFR26e2c365a191fa7/section-1.31 | regulatory records retention、authenticity、reliability、production 和 emergency availability 支撑 |",
        "| Phase 45 Runtime Contract | docs/contracts/phase45_resilience_incident_log_runtime_contract.md | audit_ledger_event schema 和 log layer boundary 字段本体 |",
        "",
        "边界：debug_log、telemetry_log、incident_log、audit_ledger 和 order_truth_source 必须分层；audit ledger 不替代 broker/venue/order source of truth，也不能推导交易许可或 hard gate。",
    ]
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(content) + "\n", encoding="utf-8")


def main() -> int:
    write_json(AUDIT_RESULT_ARCHIVE, audit_result_payload())
    candidates = load_candidates()
    results_by_task = {item["research_task_id"]: item for item in RESULTS}
    promoted: list[dict[str, Any]] = []
    supplemented: list[dict[str, Any]] = []
    failures: list[str] = []

    for task_id, result in results_by_task.items():
        entry = candidates.get(task_id)
        if not entry:
            failures.append(f"{task_id}: candidate not found")
            continue
        path, candidate = entry
        if result["decision"] == "accepted_for_reviewed_caveat_only":
            formal_item = build_formal_item(candidate, result)
            partition_id = str(formal_item["metadata"]["partition_id"])
            knowledge_dir = resolve_repo_path("codex-expert-kit", "rag", "knowledge", partition_id, start_file=__file__)
            formal_path = knowledge_dir / sanitize_filename(formal_item["knowledge_id"])
            write_json(formal_path, formal_item)
            candidate["status"]["review_status"] = "formalized"
            candidate["status"]["ingestion_decision"] = "formal_reviewed_created"
            candidate["status"]["decision_reason"] = "reviewed/caveat_only 准备审计通过，已创建 formal reviewed/caveat_only。"
            candidate["status"]["updated_at"] = TODAY
            workflow = candidate.setdefault("workflow", {})
            workflow["stage"] = "formalized_reviewed"
            workflow["queue_group"] = "formalized"
            workflow["formal_knowledge_id"] = formal_item["knowledge_id"]
            workflow["formal_review_status"] = "reviewed"
            workflow["formal_knowledge_path"] = repo_relative(formal_path)
            workflow["approved_allowed"] = False
            workflow["default_guidance_allowed"] = False
            workflow["hard_gate_allowed"] = False
            workflow["risk_threshold_advice_allowed"] = False
            candidate.setdefault("review", {}).setdefault("audit_log", []).append(
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_resilience_incident_log_formal_reviewed_created",
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
                    "formal_path": repo_relative(formal_path),
                }
            )
        elif result["decision"] == "needs_more_evidence":
            supplement_candidate(candidate, result)
            write_json(path, candidate)
            supplemented.append(candidate)

    gate = export_supplemental_package(supplemented)
    write_supplemental_research()
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_resilience_incident_log_formal_import_report",
            "generated_at": TODAY,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "source_package_id": SOURCE_PACKAGE_ID,
            "promoted_count": len(promoted),
            "supplemented_count": len(supplemented),
            "failures": failures,
            "promoted": promoted,
            "supplemental_package": repo_relative(SUPPLEMENTAL_PACKAGE),
            "supplemental_gate": repo_relative(SUPPLEMENTAL_GATE),
            "supplemental_gate_status": gate["gate_status"],
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
            "risk_threshold_advice_enabled": False,
            "automatic_live_action_enabled": False,
        },
    )
    print(
        json.dumps(
            {
                "promoted_count": len(promoted),
                "supplemented_count": len(supplemented),
                "supplemental_gate_status": gate["gate_status"],
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if len(promoted) == 4 and len(supplemented) == 2 and gate["gate_status"] == "pass" and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
