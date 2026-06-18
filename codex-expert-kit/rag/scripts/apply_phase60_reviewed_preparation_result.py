"""Apply Phase 60 reviewed/caveat_only preparation audit result.

The audit result allows 8 of 10 Phase 60 candidates to become formal
reviewed/caveat_only knowledge. P60-A07 and P60-A10 remain
needs_more_evidence and must not be formalized.

This script never creates approved, default guidance, hard gates, live
permission, trading advice, or risk-threshold advice.
"""

from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-579"
AUDIT_RESULT_ID = "audit_result_phase60_reviewed_preparation_20260617_strict_v1"
PACKAGE_ID = "phase60_reviewed_preparation_audit_package_20260617"


ACCEPTED_TARGETS: dict[str, dict[str, Any]] = {
    "P60-A01": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_environment_taxonomy_required_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.environment_taxonomy_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.environment_taxonomy_required.v1.json"),
        "confidence": "medium_high",
        "required_followups": [
            "正式写入 reviewed/caveat_only 时，把 Coinbase、Binance、QuantConnect、Alpaca、IBKR 作为 taxonomy 直接 source_refs，而不只依赖 NautilusTrader。",
            "补 live canary 与 full live 的最小字段差异。",
        ],
        "patch_notes": {
            "source": ["NautilusTrader 只能作为 framework implementation pattern。", "taxonomy source_refs 应补多平台直接来源。"],
            "content": ["taxonomy 必须绑定 EnvironmentManifest，不得只作为概念分类。"],
            "boundary": ["reviewed/caveat_only 不等于 approved、default guidance 或 hard gate。"],
            "conflict": ["与 Phase 58 environment equivalence manifest 不冲突，应作为上游 taxonomy。"],
        },
    },
    "P60-A02": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_static_api_sandbox_contract_only_001.json"),
        "knowledge_id": "kb_phase60_live_execution.static_api_sandbox_contract_only.v1",
        "knowledge_path": ("KB_06_LIVE_EXECUTION", "kb_phase60_live_execution.static_api_sandbox_contract_only.v1.json"),
        "confidence": "high",
        "required_followups": ["补 response_mocked、market_data_real、order_routing_real、account_real 字段。"],
        "patch_notes": {
            "source": ["Coinbase 来源是 Coinbase-specific，不代表所有交易所 sandbox。"],
            "content": ["必须保留 static API sandbox 表述。"],
            "boundary": ["不得 live-ready，不得 hard gate。"],
            "conflict": ["与 Phase 58 等效链条不冲突。"],
        },
    },
    "P60-A03": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_testnet_endpoint_isolation_required_001.json"),
        "knowledge_id": "kb_phase60_live_execution.testnet_endpoint_isolation_required.v1",
        "knowledge_path": ("KB_06_LIVE_EXECUTION", "kb_phase60_live_execution.testnet_endpoint_isolation_required.v1.json"),
        "confidence": "high",
        "required_followups": ["补 endpoint_scope_policy、credential_scope_policy、account_scope_policy、data_source_scope_policy。"],
        "patch_notes": {
            "source": ["Binance 来源只能作为 Binance USD-M Futures-specific。"],
            "content": ["testnet facts 不得写入 production facts。"],
            "boundary": ["不得泛化为所有交易所 testnet 行为。"],
            "conflict": ["与 Live Execution owner 不冲突。"],
        },
    },
    "P60-A04": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_paper_trading_not_live_required_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.paper_trading_not_live_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.paper_trading_not_live_required.v1.json"),
        "confidence": "high",
        "required_followups": [
            "与已有 paper_trading_not_equal_live 做 alias / merge。",
            "补 paper_broker_model_version、paper_fill_policy、paper_live_gap_report_id。",
        ],
        "alias_of": "kb_05_replay_simulation.paper_trading_not_equal_live.v1",
        "patch_notes": {
            "source": ["所有 paper 来源均有 broker/platform-specific 边界。"],
            "content": ["paper trading 是 rehearsal，不是 live execution。"],
            "boundary": ["不得实盘许可，不得交易建议。"],
            "conflict": ["与 Phase 37 / Phase 58 高度重叠，建议去重。"],
        },
    },
    "P60-A05": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_replay_market_impact_assumption_required_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.replay_market_impact_assumption_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.replay_market_impact_assumption_required.v1.json"),
        "confidence": "high",
        "required_followups": [
            "补 queue_position_policy、partial_fill_policy、market_impact_assumption_detail。",
            "补 QuantConnect reconciliation 作为辅助来源。",
        ],
        "patch_notes": {
            "source": ["HftBacktest 是 framework-specific。"],
            "content": ["replay fill 必须披露模型假设。"],
            "boundary": ["不得 live-ready，不得 hard gate。"],
            "conflict": ["与 Phase 58 等效链条一致。"],
        },
    },
    "P60-A06": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_environment_manifest_required_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.environment_manifest_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.environment_manifest_required.v1.json"),
        "confidence": "medium_high",
        "required_followups": [
            "补完整 EnvironmentManifest schema。",
            "补 reconciliation_report_id、known_non_equivalence、audit_trace_id、promotion_not_live_permission。",
        ],
        "patch_notes": {
            "source": ["manifest 名称和字段属于 CEK-TA internal governance，不是外部通用标准。"],
            "content": ["manifest 只证明环境事实可审计，不证明策略有效。"],
            "boundary": ["不得把 manifest 完备解释为上线许可。"],
            "conflict": ["与 Phase 58 environment_equivalence_manifest 应建立上下游关系。"],
        },
    },
    "P60-A08": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_sandbox_paper_live_gap_report_required_001.json"),
        "knowledge_id": "kb_phase60_replay_simulation.sandbox_paper_live_gap_report_required.v1",
        "knowledge_path": ("KB_05_REPLAY_SIMULATION", "kb_phase60_replay_simulation.sandbox_paper_live_gap_report_required.v1.json"),
        "confidence": "medium_high",
        "required_followups": [
            "补 gap_report_not_live_permission=true。",
            "补 known_non_equivalence、unreconciled_gap、residual_risk_note、human_acceptance_required。",
            "补 QuantConnect reconciliation 作为直接来源。",
        ],
        "patch_notes": {
            "source": ["FIX 是订单状态标准来源，非 REST/WebSocket 全覆盖来源。"],
            "content": ["gap report 是差异审计材料，不是通过证书。"],
            "boundary": ["gap report 通过不等于策略有效，不等于 live-ready。"],
            "conflict": ["与 Phase 58 simulation_live_gap_report_required 一致，建议 alias。"],
        },
    },
    "P60-A09": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_order_lifecycle_mapping_required_001.json"),
        "knowledge_id": "kb_phase60_live_execution.order_lifecycle_mapping_required.v1",
        "knowledge_path": ("KB_06_LIVE_EXECUTION", "kb_phase60_live_execution.order_lifecycle_mapping_required.v1.json"),
        "confidence": "high",
        "required_followups": [
            "补 venue_order_status_mapping_version、reject_code_mapping_version、unknown_outcome_policy。",
            "补 REST/WebSocket/FIX adapter 差异说明。",
        ],
        "patch_notes": {
            "source": ["FIX 是标准来源，但 REST/WebSocket broker states 仍需 venue-specific mapping。"],
            "content": ["统一生命周期不得被解释为真实成交证明。"],
            "boundary": ["不得授权执行，不得 hard gate。"],
            "conflict": ["与 Phase 45 order semantics 可能重叠，需去重。"],
        },
    },
}


NEEDS_MORE_EVIDENCE_TARGETS: dict[str, dict[str, Any]] = {
    "P60-A07": {
        "candidate_path": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_environment_promotion_evidence_required_001.json"),
        "confidence": "medium",
        "required_followups": [
            "补 QuantConnect Live Trading Reconciliation。",
            "补 NautilusTrader Live Execution Reconciliation。",
            "补 human_reviewer_required、promotion_not_live_permission、risk_review_owner、residual_gap_acceptance_note。",
            "补 promotion decision 不等于 live permission 的机器可读字段。",
        ],
        "patch_notes": {
            "source": ["必须补 reconciliation / live execution 直接来源。"],
            "content": ["promotion decision 是评审证据，不是交易许可。"],
            "boundary": ["不得自动晋级，不得自动实盘，不得 hard gate。"],
            "conflict": ["与 Risk owner 不冲突，但最终许可必须归 Risk / Live owner。"],
        },
    },
    "P60-A10": {
        "candidate_path": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json"),
        "confidence": "medium",
        "required_followups": [
            "补 NautilusTrader RiskEngine / Execution docs。",
            "补 Binance Futures Error Code / Order Reject docs。",
            "补 broker_or_exchange_rejection_mapping_source。",
            "补 live_risk_owner_policy_source。",
            "补 risk_rehearsal_result_not_hard_gate=true。",
            "补 kill_switch_or_manual_override_boundary。",
        ],
        "patch_notes": {
            "source": ["必须补 live risk / rejection / kill switch 直接来源。"],
            "content": ["risk rehearsal 只能验证字段、策略链条和审计流程。"],
            "boundary": ["不得替代 live risk owner，不得自动拒单，不得自动停机，不得 hard gate。"],
            "conflict": ["与 Risk Management owner 不冲突，但必须保留 owner 边界。"],
        },
    },
}


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def candidate_path(parts: tuple[str, str]) -> Path:
    return repo_path("codex-expert-kit", "rag", "candidates", *parts)


def knowledge_path(parts: tuple[str, str]) -> Path:
    return repo_path("codex-expert-kit", "rag", "knowledge", *parts)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id", "")),
        "source_title": str(source.get("source_title") or source.get("title") or ""),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type", "other")),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability", "medium")),
        "relevance": str(source.get("relevance", "medium")),
        "evidence_summary": str(source.get("evidence_summary", "")),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def unique_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    evidence: list[dict[str, Any]] = []
    for source in as_list(candidate.get("source_refs")):
        if not isinstance(source, dict):
            continue
        shaped = source_to_evidence(source)
        key = shaped["source_id"] or str(shaped.get("source_url") or shaped.get("source_title"))
        if key in seen:
            continue
        seen.add(key)
        evidence.append(shaped)
    return evidence


def build_metadata(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    metadata = {
        "partition_id": classification.get("partition_id"),
        "domain": classification.get("domain"),
        "subdomain": classification.get("subdomain"),
        "rule_type": classification.get("rule_type"),
        "claim_type": classification.get("claim_type"),
        "content_type": "json",
        "project_binding": "none",
        "tree_node_id": classification.get("tree_node_id"),
        "tree_path": classification.get("tree_path"),
        "canonical_node_id": classification.get("canonical_node_id") or classification.get("tree_node_id"),
        "canonical_tree_path": classification.get("tree_path"),
        "related_nodes": as_list(classification.get("related_nodes")),
        "risk_level": "medium_high",
        "used_for": sorted(set(as_list(classification.get("used_for")) + ["mcp", "searchlab", "vue_audit_ui"])),
        "classification_notes": classification.get("classification_notes"),
        "source_candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "phase": "Phase 60",
        "formalization_task_id": TASK_ID,
        "review_mode": "reviewed_caveat_only",
    }
    if target.get("alias_of"):
        metadata["alias_of"] = target["alias_of"]
        metadata["alias_notes"] = "本条按 reviewed/caveat_only 方式作为既有 paper trading 边界知识的 Phase 60 alias / merge companion，不得与既有 formal knowledge 形成竞争规则。"
    return metadata


def build_content(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    patch_notes = target["patch_notes"]
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary") or "",
        "procedure": [
            "确认当前问题属于 sandbox、testnet、historical replay、realtime simulation、paper trading、live canary 或 live 环境治理。",
            "要求外接项目提供 environment_manifest、gap_report、promotion_decision 或 order lifecycle mapping 的可审计证据。",
            "返回来源、适用范围、不适用场景、owner 边界和 caveat，不返回交易执行许可。",
            "遇到 live permission、risk threshold、hard gate 或实盘动作请求时，路由给外接项目 Live Execution / Risk Management owner。",
        ],
        "anti_patterns": [
            "把 static API sandbox mocked response 当作真实市场行为。",
            "把 testnet 订单、余额或成交写成 production fact。",
            "把 paper trading 盈亏写成 live-ready 或策略有效。",
            "把 historical replay fill 写成真实队列位置、真实 market impact 或 live 可成交性。",
            "把 environment_manifest、promotion_decision 或 gap_report 写成实盘许可、自动晋级、自动拒单、自动停机或 hard gate。",
        ],
        "validation": [
            "检查 source_evidence 是否至少包含官方/框架/标准/内部契约来源。",
            "检查 conflict_audit.approval_allowed=false。",
            "检查 machine_gate.default_guidance=caveat_only 且 approved/default/hard gate 均为 false。",
            "检查内容没有买卖点、仓位、杠杆、止损止盈、风险阈值或 live permission。",
        ],
        "risk_notes": as_list(applicability.get("limitations"))
        + patch_notes.get("boundary", [])
        + [
            "reviewed/caveat_only 只允许作为审计上下文、RAG 检索和项目方案 review；不等于 approved。",
            "平台、broker、exchange 和 framework 来源必须保留具体适用范围，不得泛化为所有市场。",
        ],
        "citation_notes": claim.get("evidence_summary", ""),
        "required_followups": target["required_followups"],
        "audit_patch_notes": {
            "source_patch_notes": patch_notes.get("source", []),
            "content_patch_notes": patch_notes.get("content", []),
            "boundary_patch_notes": patch_notes.get("boundary", []),
            "conflict_patch_notes": patch_notes.get("conflict", []),
        },
    }


def build_formal(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    evidence = unique_sources(candidate)
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    ai_audit = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": target["confidence"],
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "trade_execution_advice_allowed": False,
        "risk_threshold_advice_allowed": False,
        "live_permission_allowed": False,
        "required_followups": target["required_followups"],
        "patch_notes": target["patch_notes"],
    }
    conflict = copy.deepcopy(candidate.get("conflict_audit", {}))
    conflict.update(
        {
            "approval_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    contribution = copy.deepcopy(candidate.get("contribution", {}))
    contribution.update(
        {
            "formalized_from_candidate": candidate.get("candidate_id"),
            "private_data_removed": True,
            "contains_project_private_strategy": False,
            "contains_secret": False,
            "contains_account_facts": False,
        }
    )
    return {
        "schema_version": "1.1.0",
        "knowledge_id": target["knowledge_id"],
        "title": deep_get(candidate, ("claim", "title"), target["knowledge_id"]),
        "metadata": build_metadata(candidate, target),
        "applicability": {
            "market": deep_get(candidate, ("applicability", "market"), "general"),
            "asset": deep_get(candidate, ("applicability", "asset"), "general"),
            "timeframe": deep_get(candidate, ("applicability", "timeframe"), "general"),
            "data_granularity": deep_get(candidate, ("applicability", "data_granularity"), "general"),
            "project_type": deep_get(candidate, ("applicability", "project_type"), "trading_ai_support_layer"),
            "applies_when": as_list(deep_get(candidate, ("applicability", "applies_when"), [])),
            "not_applicable_when": as_list(deep_get(candidate, ("applicability", "not_applicable_when"), [])),
        },
        "content": build_content(candidate, target),
        "assumptions": as_list(deep_get(candidate, ("applicability", "assumptions"), [])),
        "source_evidence": evidence,
        "source_quality": {
            "overall_reliability": source_quality.get("overall_reliability", "medium_high"),
            "score": source_quality.get("score", 84),
            "source_count": len(evidence),
            "primary_source_count": source_quality.get("primary_source_count", len(evidence)),
            "limitations": as_list(source_quality.get("limitations")),
            "source_quality_notes": [
                "Reviewed/caveat_only sources support environment governance and audit boundaries, not strategy profitability or live permission.",
                "Platform, broker, exchange and framework sources are implementation-pattern evidence and must retain scope caveats.",
            ],
        },
        "conflict_audit": conflict,
        "review": {
            "review_status": "reviewed",
            "confidence": target["confidence"],
            "freshness": "mixed",
            "reviewer": "external_ai_strict_audit_and_codex_backwrite",
            "reviewed_at": TODAY,
            "source_candidate_id": candidate.get("candidate_id"),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "approval_status": "not_requested",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "ai_audit": ai_audit,
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "action": "phase60_reviewed_preparation_audit_passed",
                    "reason": "accepted_for_reviewed_caveat_only; approved/default/hard gate remain forbidden.",
                    "audit_result_id": AUDIT_RESULT_ID,
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "formal_reviewed_caveat_only_created",
                    "reason": f"{TASK_ID} materialized formal reviewed/caveat_only knowledge.",
                },
            ],
        },
        "llm_usage_policy": copy.deepcopy(candidate.get("llm_usage_policy", {})),
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": "Formal reviewed/caveat_only only; not approved, not default guidance, not hard gate, not live permission.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "contract_refs": copy.deepcopy(candidate.get("contract_refs", [])),
        "workflow": {
            "source_candidate_id": candidate.get("candidate_id"),
            "source_candidate_path": rel(candidate_path(target["candidate_path"])),
            "formalized_by_task_id": TASK_ID,
            "formalized_at": TODAY,
            "review_mode": "reviewed_caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "live_permission_allowed": False,
        },
        "contribution": contribution,
    }


def update_formalized_candidate(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(candidate)
    candidate.setdefault("status", {})
    candidate["status"].update(
        {
            "review_status": "formalized",
            "ingestion_decision": "formal_reviewed_created",
            "decision_reason": "Phase 60 reviewed-preparation strict audit allowed this item to become formal reviewed/caveat_only.",
            "updated_at": TODAY,
        }
    )
    candidate.setdefault("workflow", {})
    candidate["workflow"].update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "current_task_id": TASK_ID,
            "next_action": "runtime_linkage_validation",
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "formalization_allowed": True,
            "formal_knowledge_id": target["knowledge_id"],
            "formal_knowledge_path": rel(knowledge_path(target["knowledge_path"])),
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    candidate.setdefault("review", {})
    candidate["review"].update(
        {
            "review_status": "formalized",
            "default_guidance_allowed": False,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": target["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "formal_knowledge_id": target["knowledge_id"],
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            },
        }
    )
    candidate.setdefault("audit_log", [])
    candidate["audit_log"].append(
        {
            "event": "formal_reviewed_caveat_only_created",
            "at": TODAY,
            "by": "codex",
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": target["knowledge_id"],
            "notes": "Formal reviewed/caveat_only created; no approved/default/hard gate.",
        }
    )
    return candidate


def update_needs_more_evidence_candidate(candidate: dict[str, Any], task_id: str, target: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(candidate)
    candidate.setdefault("status", {})
    candidate["status"].update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "Phase 60 reviewed-preparation strict audit requires additional direct evidence before reviewed/caveat_only.",
            "updated_at": TODAY,
        }
    )
    candidate.setdefault("workflow", {})
    candidate["workflow"].update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "current_task_id": TASK_ID,
            "next_action": "supplement_evidence_and_export_reaudit_package",
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "formalization_allowed": False,
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    candidate.setdefault("review", {})
    candidate["review"].update(
        {
            "review_status": "needs_more_evidence",
            "default_guidance_allowed": False,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": PACKAGE_ID,
                "decision": "needs_more_evidence",
                "confidence": target["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            },
        }
    )
    candidate.setdefault("audit_log", [])
    candidate["audit_log"].append(
        {
            "event": "reviewed_preparation_needs_more_evidence",
            "at": TODAY,
            "by": "codex",
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "notes": f"{task_id} needs more direct source evidence before formal reviewed/caveat_only.",
        }
    )
    return candidate


def write_structured_audit_result() -> Path:
    results: list[dict[str, Any]] = []
    for task_id, target in ACCEPTED_TARGETS.items():
        candidate = read_json(candidate_path(target["candidate_path"]))
        results.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": target["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "trade_execution_advice_allowed": False,
                "risk_threshold_advice_allowed": False,
                "formal_knowledge_id": target["knowledge_id"],
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            }
        )
    for task_id, target in NEEDS_MORE_EVIDENCE_TARGETS.items():
        candidate = read_json(candidate_path(target["candidate_path"]))
        results.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": task_id,
                "decision": "needs_more_evidence",
                "confidence": target["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "trade_execution_advice_allowed": False,
                "risk_threshold_advice_allowed": False,
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            }
        )
    payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "source_attachment": "C:/Users/dove/.codex/attachments/b9772aab-1e4f-4bba-90c4-bbf027d08178/pasted-text.txt",
        "audited_at": TODAY,
        "package_summary": {
            "total": 10,
            "accepted_for_reviewed_caveat_only": 8,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_caveat_only_maximum": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "candidate_results": sorted(results, key=lambda item: item["research_task_id"]),
    }
    path = repo_path("docs", "audit", "audit_result_phase60_reviewed_preparation_20260617_strict_v1.json")
    write_json(path, payload)
    return path


def main() -> int:
    audit_path = write_structured_audit_result()
    created: list[str] = []
    formalized_candidates: list[str] = []
    needs_more_evidence: list[str] = []

    for task_id, target in ACCEPTED_TARGETS.items():
        cpath = candidate_path(target["candidate_path"])
        kpath = knowledge_path(target["knowledge_path"])
        candidate = read_json(cpath)
        if candidate.get("research_task_id") != task_id:
            raise ValueError(f"{cpath} has unexpected research_task_id")
        formal = build_formal(candidate, target)
        write_json(kpath, formal)
        write_json(cpath, update_formalized_candidate(candidate, target))
        created.append(rel(kpath))
        formalized_candidates.append(rel(cpath))

    for task_id, target in NEEDS_MORE_EVIDENCE_TARGETS.items():
        cpath = candidate_path(target["candidate_path"])
        candidate = read_json(cpath)
        if candidate.get("research_task_id") != task_id:
            raise ValueError(f"{cpath} has unexpected research_task_id")
        write_json(cpath, update_needs_more_evidence_candidate(candidate, task_id, target))
        needs_more_evidence.append(rel(cpath))

    report = {
        "schema_version": "phase60_reviewed_preparation_import_report.v1",
        "task_id": TASK_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": rel(audit_path),
        "created_formal_knowledge_count": len(created),
        "created_formal_knowledge": created,
        "formalized_candidates": formalized_candidates,
        "needs_more_evidence_count": len(needs_more_evidence),
        "needs_more_evidence_candidates": needs_more_evidence,
        "boundary": {
            "review_status": "reviewed_for_accepted_items",
            "review_mode": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "task_completion_status": "partial_pending_supplemental_evidence",
        "next_action": "Rebuild formal knowledge index and fixtures, then supplement P60-A07/P60-A10 evidence.",
    }
    report_path = repo_path("docs", "reports", "phase60_reviewed_preparation_import_report.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
