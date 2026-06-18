"""Generate Phase 60 P1 enhanced sandbox / replay / paper governance candidates."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-582"


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


SOURCES: dict[str, dict[str, Any]] = {
    "tt_fix_cert": {
        "source_title": "TT FIX Certification",
        "source_url": "https://library.tradingtechnologies.com/tt-fix/tt-fix-general/getting-started-tt-fix-general/tt-fix-certification/",
        "source_type": "official_doc",
        "publisher": "Trading Technologies",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "TT documents FIX certification as a process to ensure a FIX application works as expected in the TT production environment.",
        "limitations": ["TT-specific certification process; use as adapter certification pattern, not a universal requirement."],
        "source_id": "src_tt_fix_cert",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "fixsim": {
        "source_title": "FIXSIM",
        "source_url": "https://www.fixsim.com/",
        "source_type": "tool_doc",
        "publisher": "FIXSIM",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "FIXSIM describes a web-based FIX simulator for manual workflows and automated deterministic regression tests.",
        "limitations": ["Vendor tool source; use only as testing workflow example."],
        "source_id": "src_fixsim",
        "accessed_at": TODAY,
        "relevance": "medium_high",
        "quoted_excerpt_allowed": False,
    },
    "paxos_fix_cert": {
        "source_title": "FIX Certification",
        "source_url": "https://docs.paxos.com/guides/crypto-brokerage/fix/certify",
        "source_type": "official_doc",
        "publisher": "Paxos",
        "reliability": "high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Paxos documents FIX certification scenarios such as valid and invalid markets, order types and execution reports.",
        "limitations": ["Paxos-specific; use as crypto brokerage FIX certification example."],
        "source_id": "src_paxos_fix_cert",
        "accessed_at": TODAY,
        "relevance": "medium_high",
        "quoted_excerpt_allowed": False,
    },
    "jpm_replay": {
        "source_title": "How to Evaluate Trading Strategies: Single Agent Market Replay or Multi-Agent Simulation",
        "source_url": "https://www.jpmorgan.com/content/dam/jpm/cib/complex/content/technology/ai-research-publications/pdf-12.pdf",
        "source_type": "research_paper",
        "publisher": "J.P. Morgan AI Research",
        "reliability": "high",
        "score": 86,
        "freshness": "stable",
        "evidence_summary": "The paper distinguishes market replay and multi-agent simulation as different methods for strategy evaluation.",
        "limitations": ["Research context; does not define CEK-TA scenario schema or prove live readiness."],
        "source_id": "src_jpm_replay",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "alpaca_paper": {
        "source_title": "Paper Trading",
        "source_url": "https://docs.alpaca.markets/us/docs/paper-trading",
        "source_type": "official_doc",
        "publisher": "Alpaca",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Alpaca documents paper trading as a test environment and discusses limitations such as market impact, latency, queue position, fees and dividends.",
        "limitations": ["Alpaca-specific; use as paper/live gap example."],
        "source_id": "src_alpaca_paper",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "quantconnect_paper": {
        "source_title": "QuantConnect Paper Trading",
        "source_url": "https://www.quantconnect.com/docs/v2/cloud-platform/live-trading/brokerages/quantconnect-paper-trading",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect documents paper trading as live real-time data with fictional capital and simulated fills.",
        "limitations": ["Platform-specific paper brokerage behavior; not universal broker truth."],
        "source_id": "src_quantconnect_paper",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "nautilus_arch": {
        "source_title": "NautilusTrader Architecture",
        "source_url": "https://nautilustrader.io/docs/latest/concepts/architecture/",
        "source_type": "framework_doc",
        "publisher": "NautilusTrader",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "NautilusTrader separates backtest, sandbox and live contexts while sharing core runtime architecture.",
        "limitations": ["Framework-specific; use as environment implementation pattern."],
        "source_id": "src_nautilus_arch",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "sre_monitoring": {
        "source_title": "Monitoring Distributed Systems",
        "source_url": "https://sre.google/sre-book/monitoring-distributed-systems/",
        "source_type": "engineering_book",
        "publisher": "Google SRE",
        "reliability": "high",
        "score": 84,
        "freshness": "stable",
        "evidence_summary": "Google SRE describes monitoring systems with symptoms, causes and golden signals such as latency, traffic, errors and saturation.",
        "limitations": ["General SRE source; apply to trading environments only through CEK-TA boundary mapping."],
        "source_id": "src_sre_monitoring",
        "accessed_at": TODAY,
        "relevance": "medium_high",
        "quoted_excerpt_allowed": False,
    },
    "launchdarkly_canary": {
        "source_title": "Canary deployments",
        "source_url": "https://launchdarkly.com/docs/home/releases/canary",
        "source_type": "engineering_doc",
        "publisher": "LaunchDarkly",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "LaunchDarkly documents canary releases as gradual exposure to a subset of users before broader rollout.",
        "limitations": ["Software deployment source; trading live canary requires stricter broker, risk and execution boundaries."],
        "source_id": "src_launchdarkly_canary",
        "accessed_at": TODAY,
        "relevance": "medium",
        "quoted_excerpt_allowed": False,
    },
    "phase60_env_contract": {
        "source_title": "Phase 60 Sandbox / Replay / Paper Environment Contract",
        "source_url": "docs/contracts/phase60_sandbox_replay_paper_environment_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 88,
        "freshness": "current",
        "evidence_summary": "CEK-TA internal contract defines EnvironmentManifest fields, owner boundaries and machine gate restrictions.",
        "limitations": ["Internal schema; candidate requires external audit before accepted_for_draft or reviewed."],
        "source_id": "src_phase60_env_contract",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    "phase60_gap_contract": {
        "source_title": "Phase 60 Environment Promotion Decision and Gap Report Contract",
        "source_url": "docs/contracts/phase60_environment_promotion_gap_report_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "reliability": "high",
        "score": 88,
        "freshness": "current",
        "evidence_summary": "CEK-TA internal contract defines promotion decisions, gap report fields, required evidence and hard boundaries.",
        "limitations": ["Internal schema; candidate requires external audit before formal reviewed."],
        "source_id": "src_phase60_gap_contract",
        "accessed_at": TODAY,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
}


CANDIDATES: list[dict[str, Any]] = [
    {
        "task": "P60-P1-01",
        "candidate_id": "cand_20260617_phase60_p1_fix_broker_certification_required_001",
        "file": "KB_06_LIVE_EXECUTION/cand_20260617_phase60_p1_fix_broker_certification_required_001.json",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution",
        "subdomain": "adapter_certification",
        "rule_type": "adapter_certification_boundary_rule",
        "claim_type": "environment_evidence_requirement",
        "title": "FIX / broker certification sandbox 必须作为 adapter 上线前的契约测试证据",
        "statement": "外接项目接入 FIX、broker API 或 exchange adapter 前，必须把认证 sandbox / UAT / simulator 结果记录为 adapter 契约测试证据；该证据只能说明消息、字段、状态转换和错误场景被覆盖，不能证明策略收益、真实流动性或实盘许可。",
        "normalized": "phase60.p1.fix_broker_certification_required.v1",
        "sources": ["tt_fix_cert", "fixsim", "paxos_fix_cert", "phase60_env_contract"],
        "proposed_id": "kb_phase60_live_execution.adapter_certification.fix_broker_certification_required.v1",
        "used_for": ["adapter_review", "sandbox_certification", "live_execution_readiness"],
    },
    {
        "task": "P60-P1-02",
        "candidate_id": "cand_20260617_phase60_p1_replay_scenario_library_versioned_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_p1_replay_scenario_library_versioned_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "scenario_library",
        "rule_type": "scenario_replay_governance_rule",
        "claim_type": "versioned_test_evidence_requirement",
        "title": "replay / simulation scenario library 必须版本化",
        "statement": "用于测试极端行情、停牌、auction、断线、拒单、部分成交、延迟和错误恢复的 replay / simulation scenario library 必须记录 scenario_id、dataset_version、event_clock、seed、assumption_hash 和 expected_observation；场景通过只能证明测试覆盖，不能证明未来收益。",
        "normalized": "phase60.p1.replay_scenario_library_versioned.v1",
        "sources": ["jpm_replay", "nautilus_arch", "phase60_env_contract"],
        "proposed_id": "kb_phase60_replay_simulation.scenario_library.versioned_required.v1",
        "used_for": ["replay_testing", "simulation_qa", "gap_report"],
    },
    {
        "task": "P60-P1-03",
        "candidate_id": "cand_20260617_phase60_p1_paper_account_reset_trace_required_001",
        "file": "KB_06_LIVE_EXECUTION/cand_20260617_phase60_p1_paper_account_reset_trace_required_001.json",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution",
        "subdomain": "paper_account_state",
        "rule_type": "paper_account_governance_rule",
        "claim_type": "account_state_boundary",
        "title": "paper account reset、初始资金和账户状态必须可追踪",
        "statement": "paper trading 的 account reset、virtual buying power、initial cash、position seed 和 broker model version 会改变评估语义，必须写入 audit trace；paper 账户状态不得与 live 账户事实、真实保证金或真实购买力混用。",
        "normalized": "phase60.p1.paper_account_reset_trace_required.v1",
        "sources": ["alpaca_paper", "quantconnect_paper", "phase60_env_contract"],
        "proposed_id": "kb_phase60_live_execution.paper_account_state.reset_trace_required.v1",
        "used_for": ["paper_trading_review", "account_state_audit", "paper_live_gap"],
    },
    {
        "task": "P60-P1-04",
        "candidate_id": "cand_20260617_phase60_p1_realtime_sim_health_monitor_required_001",
        "file": "KB_06_LIVE_EXECUTION/cand_20260617_phase60_p1_realtime_sim_health_monitor_required_001.json",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution",
        "subdomain": "environment_health_monitoring",
        "rule_type": "runtime_observability_rule",
        "claim_type": "health_evidence_requirement",
        "title": "realtime simulation 必须记录心跳、断线、延迟和数据 stale 状态",
        "statement": "实时模拟和 sandbox execution 必须记录 heartbeat、disconnect、reconnect、latency、data stale、order event lag、adapter error 和 recovery evidence；这些指标只能说明环境健康和 adapter 稳定性，不等于交易许可或策略有效。",
        "normalized": "phase60.p1.realtime_sim_health_monitor_required.v1",
        "sources": ["sre_monitoring", "nautilus_arch", "phase60_env_contract"],
        "proposed_id": "kb_phase60_live_execution.environment_health.monitor_required.v1",
        "used_for": ["runtime_observability", "paper_trading_monitoring", "adapter_healthcheck"],
    },
    {
        "task": "P60-P1-05",
        "candidate_id": "cand_20260617_phase60_p1_live_canary_rollback_owner_required_001",
        "file": "KB_07_RISK_MANAGEMENT/cand_20260617_phase60_p1_live_canary_rollback_owner_required_001.json",
        "partition": "KB_07_RISK_MANAGEMENT",
        "tree_node": "kt.risk_management",
        "subdomain": "live_canary_governance",
        "rule_type": "live_canary_boundary_rule",
        "claim_type": "rollback_governance_requirement",
        "title": "live canary 必须有 rollback、停止条件和 owner",
        "statement": "live canary 只能作为小范围真实环境观察阶段，必须记录 scope、stop_condition_ref、rollback_plan_ref、owner、manual_review_required 和 residual_gap；canary 通过不得自动扩大为 full live 或默认 hard gate。",
        "normalized": "phase60.p1.live_canary_rollback_owner_required.v1",
        "sources": ["launchdarkly_canary", "sre_monitoring", "phase60_gap_contract"],
        "proposed_id": "kb_phase60_risk_management.live_canary.rollback_owner_required.v1",
        "used_for": ["live_canary_review", "promotion_decision", "risk_owner_review"],
    },
    {
        "task": "P60-P1-06",
        "candidate_id": "cand_20260617_phase60_p1_environment_drift_monitor_required_001",
        "file": "KB_05_REPLAY_SIMULATION/cand_20260617_phase60_p1_environment_drift_monitor_required_001.json",
        "partition": "KB_05_REPLAY_SIMULATION",
        "tree_node": "kt.replay_simulation",
        "subdomain": "environment_drift",
        "rule_type": "environment_drift_governance_rule",
        "claim_type": "drift_report_requirement",
        "title": "environment drift monitor 必须比较 replay、paper、canary 与 live 的差异趋势",
        "statement": "外接项目必须把 replay、paper、canary 与 live 的 fill、fee、latency、reject、cancel、order_state、data_staleness 和 risk_event 差异做成 environment drift report；drift report 是治理和人工复核材料，不是收益证明、交易许可或 hard gate。",
        "normalized": "phase60.p1.environment_drift_monitor_required.v1",
        "sources": ["quantconnect_paper", "alpaca_paper", "sre_monitoring", "phase60_gap_contract"],
        "proposed_id": "kb_phase60_replay_simulation.environment_drift.monitor_required.v1",
        "used_for": ["environment_drift_review", "paper_live_gap", "promotion_decision"],
    },
]


def source_refs(keys: list[str]) -> list[dict[str, Any]]:
    return [SOURCES[key] for key in keys]


def candidate_payload(spec: dict[str, Any]) -> dict[str, Any]:
    refs = source_refs(spec["sources"])
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": spec["candidate_id"],
        "research_task_id": spec["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 60 P1 enhanced environment governance candidate generated for strict external audit.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": spec["tree_node"],
            "canonical_node_id": spec["tree_node"],
            "tree_path": f"CEK-TA / Trading Engineering / {spec['tree_node'].split('.')[-1].replace('_', ' ').title()}",
            "related_nodes": [
                "kt.trading_engineering",
                "kt.replay_simulation",
                "kt.live_execution",
                "kt.risk_management",
                "kt.data_engineering",
                "kt.market_microstructure",
            ],
            "partition_id": spec["partition"],
            "domain": spec["tree_node"].replace("kt.", ""),
            "subdomain": spec["subdomain"],
            "rule_type": spec["rule_type"],
            "claim_type": spec["claim_type"],
            "used_for": spec["used_for"] + ["external_project_rag_retrieval"],
            "classification_notes": "Phase 60 P1 增强环境治理候选；只用于 sandbox/replay/paper/canary 的测试、监控、晋级和 gap 审计，不接管策略、实盘执行或风控阈值。",
        },
        "claim": {
            "claim_id": "claim_" + spec["task"].lower().replace("-", "_"),
            "title": spec["title"],
            "statement": spec["statement"],
            "normalized_claim": spec["normalized"],
            "evidence_summary": "；".join(src["evidence_summary"] for src in refs[:3]),
            "interpretation_notes": "本候选是 Phase 60 P1 增强治理知识，只允许外部审计后进入 accepted_for_draft；不得直接 reviewed、approved、default guidance 或 hard gate。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_platform_or_venue_specific_mapping",
            "asset": "general",
            "timeframe": "sandbox_replay_paper_or_live_canary_environment",
            "data_granularity": "api_message_order_event_fill_event_health_metric_or_gap_report",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目设计 sandbox、UAT、testnet、replay、paper trading 或 live canary 环境治理",
                "需要审计 adapter certification、scenario library、paper account state、runtime health、canary rollback 或 environment drift",
                "需要把 Phase 60 P0 manifest/gap report 扩展为更完整的测试治理证据",
            ],
            "not_applicable_when": [
                "需要生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议",
                "需要直接证明策略有效、live-ready 或收益优势",
                "没有平台、broker、exchange、API 版本、环境类型或数据来源证据",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含外接项目私有策略参数。",
                "每条候选都需要外部 AI/人工严格审计后才能进入 accepted_for_draft。",
                "平台和工具来源只能作为 implementation pattern 或 supporting source。",
            ],
            "limitations": [
                "P1 增强知识不能替代 P0 的 EnvironmentManifest、PromotionDecision 和 GapReport。",
                "候选不能自动创建 reviewed、approved、default guidance 或 hard gate。",
                "本候选不提供投资建议、订单建议、风险阈值或实盘许可。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "source_count": len(refs),
            "primary_source_count": sum(1 for src in refs if src["source_type"] in {"official_doc", "research_paper", "engineering_book", "internal_contract"}),
            "quality_level": "medium_high",
            "limitations": ["候选来源需要外部严格审计；vendor/tool 文档不得过度泛化。"],
            "freshness": "mixed",
        },
        "content": {
            "statement": spec["statement"],
            "required_fields_or_contract": [
                "environment_id",
                "environment_type",
                "adapter_or_scenario_version",
                "evidence_source_id",
                "audit_trace_id",
                "owner",
                "known_limitations",
                "not_live_permission",
            ],
            "procedure": [
                "识别环境类型、平台、broker/exchange、API 版本和数据来源。",
                "记录候选主题所需的 evidence 字段、owner 和限制。",
                "将通过/失败写入 gap report 或 promotion decision，不直接写成实盘许可。",
            ],
            "anti_patterns": [
                "把 paper/replay/sandbox/canary 表现写成策略有效。",
                "把 vendor-specific 行为泛化为所有市场。",
                "把测试通过写成 approved、default guidance、hard gate 或自动交易许可。",
            ],
            "validation": [
                "外部 AI/人工严格审计 source、content、boundary、conflict patch notes。",
                "正式转换前做完整 KB 冲突、重复和 owner 边界检查。",
            ],
            "risk_notes": [
                "测试环境的通过结果容易被误读为 live-ready。",
                "环境健康、认证、场景覆盖或 canary 观察都不能替代 Risk/Live owner 的正式决策。",
            ],
        },
        "review": {
            "review_status": "candidate_ready",
            "reviewed_by": None,
            "reviewed_at": None,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "notes": "等待外部严格审计。",
        },
        "conflict_audit": {
            "conflict_status": "none",
            "known_conflicts": [],
            "potential_conflicts": [
                "可能与 Phase 60 P0、Phase 58 环境等效链条、Phase 37 Replay/Live/Risk 知识重叠；正式转换前必须做重复和 owner 边界检查。"
            ],
            "resolution_summary": "候选只允许进入外部审计队列，未发现与当前 formal knowledge 的直接冲突。",
            "approval_allowed": True,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒外接项目记录环境治理证据和 gap report。",
                "用于审计 sandbox/replay/paper/canary 是否保留 owner 和边界。",
                "用于阻止 AI 把测试环境结果泛化为 live-ready。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈或风险阈值。",
                "不得授权实盘、自动拒单、自动停机或 hard gate。",
                "不得把 candidate 当作正式 reviewed 或 approved 知识。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "requires_human_escalation": True,
            "reason": "candidate_ready only; external audit required before accepted_for_draft or reviewed/caveat_only.",
        },
        "conversion_target": {
            "proposed_knowledge_id": spec["proposed_id"],
            "target_partition": spec["partition"],
            "target_review_status": "candidate_only_pending_audit",
            "default_guidance_target": "deny",
            "hard_gate_target": "deny",
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "hidden_from_default_queue": True,
            "next_action": "export_for_external_ai_audit",
            "formal_knowledge_id": None,
            "formal_review_status": None,
        },
        "audit_log": [
            {
                "event": "candidate_created",
                "at": TODAY,
                "by": "codex",
                "notes": "Phase 60 P1 候选生成，等待严格审计。",
            }
        ],
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
        },
    }


def build_quality_gate(candidates: list[dict[str, Any]], paths: list[Path]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    expected_tasks = {f"P60-P1-0{idx}" for idx in range(1, 7)}
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != expected_tasks:
        failures.append({"candidate_id": "package", "path": "", "reason": f"unexpected_task_set:{sorted(actual_tasks ^ expected_tasks)}"})
    for path, candidate in zip(paths, candidates, strict=True):
        cid = str(candidate.get("candidate_id", ""))
        blob = json.dumps(candidate, ensure_ascii=False)
        if candidate.get("status", {}).get("review_status") != "candidate_ready":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "review_status_not_candidate_ready"})
        if len(candidate.get("source_refs", [])) < 3:
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "source_refs_less_than_3"})
        if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "default_guidance_not_deny"})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if candidate.get("machine_gate", {}).get(field) is not False:
                failures.append({"candidate_id": cid, "path": rel(path), "reason": f"machine_gate_{field}_not_false"})
        if "�" in blob or "????" in blob:
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "possible_mojibake"})
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "possible_secret_field"})
    return {
        "report_id": "phase60_p1_candidate_quality_gate",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "Phase 60 P1 candidates are candidate-only; no reviewed/approved/default guidance/hard gate.",
        "candidate_paths": [rel(path) for path in paths],
    }


def main() -> int:
    payloads = [candidate_payload(spec) for spec in CANDIDATES]
    paths = [repo_path("codex-expert-kit", "rag", "candidates", *spec["file"].split("/")) for spec in CANDIDATES]
    for path, payload in zip(paths, payloads, strict=True):
        write_json(path, payload)

    quality_gate = build_quality_gate(payloads, paths)
    gate_path = repo_path("docs", "reports", "phase60_p1_candidate_quality_gate.json")
    write_json(gate_path, quality_gate)

    generation_report = {
        "report_id": "phase60_p1_candidate_generation_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(payloads),
        "candidate_paths": [rel(path) for path in paths],
        "quality_gate_path": rel(gate_path),
        "next_action": "Export Phase 60 P1 candidate audit package.",
    }
    report_path = repo_path("docs", "reports", "phase60_p1_candidate_generation_report.json")
    write_json(report_path, generation_report)

    print(json.dumps(generation_report, ensure_ascii=False, indent=2))
    return 0 if quality_gate["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
