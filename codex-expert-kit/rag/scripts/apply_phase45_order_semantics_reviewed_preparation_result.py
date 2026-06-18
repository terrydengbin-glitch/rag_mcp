"""Apply Phase 45 Order Semantics reviewed/caveat_only preparation result.

This task consumes the strict reviewed/caveat_only preparation audit for the
six Phase 45 Order Semantics candidates. It creates formal reviewed/caveat_only
knowledge only for entries explicitly allowed by the audit, keeps ORD05 in
needs_more_evidence, supplements ORD05 evidence, and exports a one-item
supplemental re-audit package.

It never creates approved knowledge, default guidance, hard gates, order
submission permission, routing advice, fee optimization advice, auto cancel /
replace actions, or live trading actions.
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
TASK_ID = "CEK-TA-468"
AUDIT_RESULT_ID = "audit_phase45_order_semantics_reviewed_preparation_20260612"
SOURCE_PACKAGE_ID = "phase45_order_semantics_reviewed_preparation_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_order_semantics_ord05_supplemental_reaudit_package_20260612"
PARTITION = "KB_06_LIVE_EXECUTION"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_order_semantics_import_report.json", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_order_semantics_ord05_supplemental_reaudit_gate.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_order_semantics_ord05_supplemental_research.md", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-F-ORD01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "FIX ExecutionReport 和 FIX order state guidance 足以支撑订单生命周期、状态、fill、cancel、replace、reject 的事件证据边界。",
            "CME、Coinbase、Kraken 来源足以支撑不同 venue/product/API 的 order type 行为不能只用字符串枚举表示。",
            "内部 order_semantics contract 已提供 order_semantics_identity、order_type_mapping 和 execution_report_mapping 字段本体。",
        ],
        "patch_notes": {
            "source": [
                "保留 FIX Trading Community、FIX ExecutionReport、FIX order-state changes、CME、Coinbase、Kraken。",
                "CME education source 只能作为辅助，不替代 product-level technical spec。",
            ],
            "content": [
                "保留 order_intent、venue_order_request、venue_order_ack、execution_report、fill/reject/expire 分层。"
            ],
            "boundary": ["不得生成订单提交许可。", "不得生成撤单/改单动作。", "不得生成交易建议。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD02",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "medium_high",
        "reasons": [
            "Nasdaq、Coinbase、Binance、FIX 来源足以支撑 TIF 必须绑定 venue、session、expire/cancel、partial fill 和 order-event 语义。",
            "Binance goodTillDate 秒级精度和 GTD 延迟 caveat 支撑 good-till 时间精度和系统时钟边界。",
            "内部 contract 已提供 time_in_force_mapping 字段本体。",
        ],
        "patch_notes": {
            "source": [
                "保留 Nasdaq Equity 4、Coinbase Exchange Trading Concepts、Binance USD-M Futures New Order、FIX order-state changes。",
                "CME sandbox source 不得作为 reviewed 主证据。",
            ],
            "content": [
                "保留 expire_time、expire_time_precision、clock_source、partial_fill_behavior、cancel_or_expire_event_ref。"
            ],
            "boundary": ["不得生成自动撤单。", "不得生成订单提交许可。", "不得生成 session hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD03",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "Binance Spot、Binance Futures、Kraken Futures、Coinbase 来源足以支撑 post-only / reduce-only 是 venue-specific execution constraint。",
            "claim 明确 post-only / reduce-only 不等于成交保证、费用节省保证、风险安全保证或交易许可。",
            "内部 contract 已提供 post_reduce_constraints 字段本体。",
        ],
        "patch_notes": {
            "source": ["保留 Binance Spot、Binance USD-M Futures、Kraken Futures、Coinbase。"],
            "content": [
                "保留 post_only_flag、reduce_only_flag、position_source_ref、existing_open_orders_policy、failure_event_ref。"
            ],
            "boundary": ["不得生成费用节省保证。", "不得生成安全保证。", "不得生成强制 reduce-only 动作。", "不得生成交易许可。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD04",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "CME、Coinbase、Binance 来源足以支撑 STP/SMP 必须声明账户/firm/group 范围、mode、cancel/decrement/reject 行为和 order-event 映射。",
            "claim 明确 STP/SMP 不等于防操纵合规结论、成交质量保证或跨 venue 通用规则。",
            "内部 contract 已提供 stp_smp_mapping，并明确 compliance_boundary=not_a_market_abuse_conclusion。",
        ],
        "patch_notes": {
            "source": ["保留 CME SMP FAQ、Coinbase STP、Coinbase International rules、Binance Futures API。"],
            "content": [
                "保留 stp_smp_enabled、scope、mode、mode_source_ref、event_mapping_ref、compliance_boundary。"
            ],
            "boundary": ["不得替外接项目启用自动拒单。", "不得生成防操纵合规结论。", "不得生成成交质量保证。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD05",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "anti-generalization caveat 方向正确，但当前 statement 仍列出 market-to-limit、VWAP 等示例。",
            "当前 reviewed-preparation 包内 source_refs 没有足够直接的逐项来源。",
            "必须补 market-to-limit / Market Limit 和 VWAP 官方来源，或删除未 source_ref 支撑的示例。",
        ],
        "patch_notes": {
            "source": [
                "保留 Nasdaq Opening/Closing Cross、NYSE auctions、NYSE Pillar、CME definitions、Coinbase、Binance、Kraken。",
                "补 CME FirmSoft Market Limit 或其他 market-to-limit 官方来源。",
                "补 VWAP 官方来源，或删除该示例。",
            ],
            "content": [
                "本条应定位为 anti-generalization caveat，不应变成特殊订单类型百科。",
                "正式文本中只能列出已 source_ref 覆盖的示例。",
            ],
            "boundary": ["不得生成通用订单行为规则。", "不得生成路由建议。", "不得生成订单提交许可。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD06",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "SEC EMSAC、CFA、CME fee docs、Coinbase trading rules 足以支撑 maker/taker、add/remove liquidity、exchange fee、transaction type 必须按成交结果和 fee schedule 审计。",
            "Coinbase 明确同一订单可部分 maker、部分 taker，支撑 limit/post-only 不自动等于 maker 成交。",
            "内部 contract 已提供 fee_evidence 字段本体。",
        ],
        "patch_notes": {
            "source": ["保留 SEC EMSAC、CFA Institute、CME fees、Coinbase trading rules。"],
            "content": [
                "保留 venue_fee_schedule_ref、fee_schedule_version、fill_event_ref、liquidity_flag、transaction_type、fee_tier_source、fee_amount_source。"
            ],
            "boundary": ["不得输出费用套利。", "不得输出路由建议。", "不得输出真实费率或费用优化策略。", "不得将 fee 事件写成策略 alpha。"],
            "conflict": [],
        },
    },
]


ORD05_SUPPLEMENTAL_SOURCES: list[dict[str, Any]] = [
    {
        "source_title": "CME Group FirmSoft Order Type Definitions",
        "source_url": "https://www.cmegroup.com/tools-information/webhelp/cmeone-firmsoft/Content/OrderTypeDefinitions.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CME FirmSoft order type definitions list MKL as Market Limit and support treating Market Limit / market-to-limit as CME-specific order semantics.",
        "limitations": ["CME FirmSoft / CME context; not universal across venues, products, brokers, or crypto exchanges."],
        "source_id": "src_ord05_supplement_cme_firmsoft_market_limit",
        "accessed_at": TODAY,
        "version": None,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
    },
    {
        "source_title": "IBKR Order Types, Algos and Tools",
        "source_url": "https://www.interactivebrokers.com/en/trading/ordertypes.php",
        "source_type": "official_broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "IBKR documents VWAP Best-Efforts as an IB Algo order type available for specified instruments and time periods, supporting VWAP as broker-specific execution algorithm semantics.",
        "limitations": ["IBKR-specific order/algo offering; not a universal VWAP order type or strategy signal."],
        "source_id": "src_ord05_supplement_ibkr_vwap_algo",
        "accessed_at": TODAY,
        "version": None,
        "relevance": "high",
        "quoted_excerpt_allowed": False,
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


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def candidate_paths() -> list[Path]:
    return sorted(CANDIDATE_DIR.glob("cand_20260612_phase45_order_semantics_*.json"))


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if str(item).strip()]


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    output: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in candidate_paths():
        candidate = read_json(path)
        output[str(candidate.get("research_task_id"))] = (path, candidate)
    return output


def knowledge_id_for(candidate: dict[str, Any]) -> str:
    workflow = candidate.get("workflow", {})
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    explicit = conversion.get("proposed_knowledge_id") or workflow.get("formal_knowledge_id")
    if explicit:
        return str(explicit)
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id"))
    normalized = normalized.replace("phase45_order_semantics.", "")
    return f"kb_phase45_order_semantics.{re.sub(r'[^A-Za-z0-9_.-]+', '_', normalized)}"


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    source_refs = candidate.get("source_refs", [])
    patch_notes = result["patch_notes"]
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id_for(candidate),
        "title": str(claim.get("title") or candidate.get("research_task_id")),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": "order_semantics_boundary_rule",
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
            "classification_notes": "Phase 45 Order Semantics formal reviewed/caveat_only；只用于 live execution adapter、订单语义、TIF、STP/SMP、fee evidence 和审计检查，不是 approved/default guidance/hard gate，不生成订单动作。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_venue_specific_caveats"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "order_entry_execution_adapter_and_audit_context"),
            "data_granularity": applicability.get("data_granularity", "order_and_execution_events"),
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
                "确认问题属于 Live Execution / Order Semantics，而不是策略 alpha、路由建议或风控 hard gate。",
                "检查 order intent、venue order request、venue ack、execution report、fill/reject/expire、fee evidence 是否分层。",
                "对每个 order type、TIF、post-only、reduce-only、STP/SMP、maker/taker 字段保留 venue、product、session、API version 和 source_ref。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "examples": [],
            "anti_patterns": string_list(
                [
                    "把 order type、TIF、post-only、reduce-only、STP/SMP 或 fee 字段写成交易信号。",
                    "把某个 venue 的订单行为泛化为所有市场通用规则。",
                    "从 order semantics 生成订单提交许可、自动撤单、自动改单、路由建议或费用优化。",
                ]
                + as_list(claim.get("anti_patterns"))
            ),
            "validation": [
                "source_evidence 必须包含协议、交易所、broker 或 venue 官方来源，并明确来源适用边界。",
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "不得出现买卖点、仓位、杠杆、止损止盈、路由建议、费用套利、实盘执行建议或订单提交许可。",
            ],
            "risk_notes": [
                "Order Semantics reviewed/caveat_only 只能作为 adapter 和审计设计上下文。",
                "FIX 只是协议语义，不替代 venue/broker rulebook 或 API 事实。",
                "交易所、broker 和 crypto venue 来源具有 venue/product/session/API version 边界。",
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
            "trade_execution_advice_allowed": False,
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
            "trade_execution_advice_allowed": False,
            "approved_at": None,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "trade_execution_advice_allowed": False,
                "reasons": result["reasons"],
                "patch_notes": patch_notes,
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分 order type、TIF、adapter semantics、execution report、fill/reject/expire 和 fee evidence。",
                "用于生成 order semantics checklist、adapter contract review、simulation/live mapping review 和 RAG 检索上下文。",
                "用于检查外接项目是否把 venue-specific order behavior 误写成通用交易规则。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、路由建议、费用套利、订单提交许可或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、撤单、改单、reduce-only 强制动作或路由策略。",
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
            "trade_execution_advice_allowed": False,
        },
        "contribution": candidate.get("contribution", {}),
    }


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_reviewed_caveat_only": 5,
            "needs_more_evidence": 1,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": "",
                "research_task_id": item["research_task_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reviewed_allowed": item["decision"] == "accepted_for_reviewed_caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "trade_execution_advice_allowed": False,
                "reasons": item["reasons"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
        "global_required_patches": [
            "ORD05 需补 market-to-limit / VWAP 直接来源或缩窄 formal reviewed 文本。",
            "所有条目不得创建 approved、default guidance、hard gate、订单提交许可、路由建议、费用优化、自动撤单/改单。",
        ],
    }


def upsert_sources(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    source_refs = list(candidate.get("source_refs", []))
    existing_urls = {ref.get("source_url") for ref in source_refs if isinstance(ref, dict)}
    for ref in refs:
        if ref.get("source_url") not in existing_urls:
            source_refs.append(ref)
    candidate["source_refs"] = source_refs
    primary_types = {
        "official_protocol_doc",
        "official_exchange_doc",
        "official_platform_doc",
        "official_broker_doc",
        "regulatory_discussion",
        "professional_body",
    }
    source_quality = candidate.setdefault("source_quality", {})
    source_quality["primary_source_count"] = sum(1 for ref in source_refs if ref.get("source_type") in primary_types)
    source_quality["supporting_source_count"] = len(source_refs) - int(source_quality["primary_source_count"])
    source_quality["score"] = round(sum(float(ref.get("score", 70)) for ref in source_refs) / max(len(source_refs), 1), 2)


def write_ord05_research() -> None:
    SUPPLEMENTAL_RESEARCH.parent.mkdir(parents=True, exist_ok=True)
    SUPPLEMENTAL_RESEARCH.write_text(
        """# Phase 45 ORD05 补证记录

## 目标

补齐 P45-F-ORD05 在 reviewed/caveat_only 准备审计中指出的 `market-to-limit / Market Limit` 和 `VWAP` 直接来源缺口。

## 补充来源

| 来源 | 类型 | 支撑范围 | 边界 |
| --- | --- | --- | --- |
| CME Group FirmSoft Order Type Definitions | official_exchange_doc | Market Limit / MKL order type 属于 CME/FirmSoft 语义 | 仅支撑 CME 语境，不可泛化 |
| IBKR Order Types, Algos and Tools | official_broker_doc | VWAP Best-Efforts 属于 IBKR IB Algo / broker-specific execution algo | 仅支撑 IBKR 可用产品和算法订单语义，不是策略信号 |

## 结论

ORD05 仍定位为 anti-generalization caveat。补证后可以重新审计是否进入 formal reviewed/caveat_only；即使通过，也不得创建 approved、default guidance、hard gate、路由建议、费用优化或订单提交许可。
""",
        encoding="utf-8",
    )


def export_ord05_supplemental_package(candidate: dict[str, Any]) -> dict[str, Any]:
    failures: list[str] = []
    urls = {ref.get("source_url") for ref in candidate.get("source_refs", []) if isinstance(ref, dict)}
    for ref in ORD05_SUPPLEMENTAL_SOURCES:
        if ref["source_url"] not in urls:
            failures.append(f"missing supplemental source: {ref['source_title']}")
    if candidate.get("status", {}).get("review_status") != "needs_more_evidence":
        failures.append("ORD05 must remain needs_more_evidence before supplemental audit")
    gate = {
        "gate_id": "phase45_order_semantics_ord05_supplemental_reaudit_gate",
        "checked_at": TODAY,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": 1,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 ORD05 是否可从 needs_more_evidence 升级为 accepted_for_reviewed_caveat_only。",
            "不得创建 approved、default guidance、hard gate、订单提交许可、路由建议、费用优化或自动撤改单。",
        ],
    }
    write_json(SUPPLEMENTAL_GATE, gate)
    payload = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "45",
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / Live Execution / Order Semantics",
            "partition": PARTITION,
            "candidate_count": 1,
            "target": "复审 ORD05 在补齐 market-to-limit / VWAP 官方来源后是否可进入 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "routing_advice_allowed": False,
            "fee_optimization_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈", "订单提交许可", "路由建议", "费用套利", "自动撤单", "自动改单"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、交易所/协议资料、broker/venue API 文档、案例和数据，对 ORD05 补证包进行严格审计。",
            "最高只能输出 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
            "重点检查 CME FirmSoft 是否足以支撑 market-to-limit / Market Limit 示例，IBKR 是否足以支撑 VWAP 作为 broker-specific execution algo 示例。",
            "即使通过，也只能 formal reviewed/caveat_only，不能 approved/default guidance/hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {
                "total": 1,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-F-ORD05",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "trade_execution_advice_allowed": False,
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
        "candidate": candidate,
        "supplemental_research_path": repo_relative(SUPPLEMENTAL_RESEARCH),
    }
    write_json(SUPPLEMENTAL_PACKAGE, payload)
    return gate


def main() -> int:
    audit = audit_result_payload()
    write_json(AUDIT_ARCHIVE, audit)
    write_ord05_research()
    candidates = load_candidates()
    results_by_task = {item["research_task_id"]: item for item in RESULTS}

    promoted: list[dict[str, Any]] = []
    needs_more_evidence: list[dict[str, Any]] = []
    failures: list[str] = []

    for task_id, result in results_by_task.items():
        entry = candidates.get(task_id)
        if not entry:
            failures.append(f"{task_id}: candidate not found")
            continue
        path, candidate = entry
        candidate.setdefault("review", {}).setdefault("audit_log", [])
        candidate["review"]["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": SOURCE_PACKAGE_ID,
            "decision": result["decision"],
            "confidence": result["confidence"],
            "reviewed_allowed": result["decision"] == "accepted_for_reviewed_caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "reasons": result["reasons"],
            "patch_notes": result["patch_notes"],
        }
        candidate.setdefault("claim", {})["audit_patch_notes"] = result["patch_notes"]

        workflow = candidate.setdefault("workflow", {})
        workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]

        if result["decision"] == "accepted_for_reviewed_caveat_only":
            formal_item = build_formal_item(candidate, result)
            knowledge_dir = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION, start_file=__file__)
            formal_path = knowledge_dir / sanitize_filename(formal_item["knowledge_id"])
            write_json(formal_path, formal_item)
            candidate["status"].update(
                {
                    "review_status": "formalized",
                    "ingestion_decision": "formal_reviewed_created",
                    "decision_reason": "reviewed/caveat_only 准备审计通过，已创建 formal reviewed/caveat_only。",
                    "updated_at": TODAY,
                }
            )
            workflow.update(
                {
                    "stage": "formalized_reviewed",
                    "queue_group": "formalized",
                    "formal_knowledge_id": formal_item["knowledge_id"],
                    "formal_review_status": "reviewed",
                    "formal_knowledge_path": repo_relative(formal_path),
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "trade_execution_advice_allowed": False,
                }
            )
            candidate["review"]["audit_log"].append(
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_order_semantics_formal_reviewed_created",
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
            continue

        if task_id == "P45-F-ORD05":
            upsert_sources(candidate, ORD05_SUPPLEMENTAL_SOURCES)
            candidate["status"].update(
                {
                    "review_status": "needs_more_evidence",
                    "ingestion_decision": "needs_more_evidence",
                    "decision_reason": "reviewed/caveat_only 准备审计未通过；已补 market-to-limit / VWAP 官方来源，等待单条补证复审。",
                    "updated_at": TODAY,
                }
            )
            workflow.update(
                {
                    "stage": "needs_more_evidence",
                    "queue_group": "needs_more_evidence",
                    "formal_knowledge_id": None,
                    "formal_review_status": None,
                    "formal_knowledge_path": None,
                    "supplemental_reaudit_package_id": SUPPLEMENTAL_PACKAGE_ID,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "next_action": "external_ai_or_human_inline_contract_reaudit",
                }
            )
            candidate["review"]["audit_log"].append(
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_order_semantics_ord05_needs_more_evidence_supplemented",
                    "reason": "supplemented CME FirmSoft Market Limit and IBKR VWAP official sources for re-audit",
                    "audit_result_id": AUDIT_RESULT_ID,
                    "supplemental_reaudit_package_id": SUPPLEMENTAL_PACKAGE_ID,
                }
            )
            write_json(path, candidate)
            gate = export_ord05_supplemental_package(candidate)
            needs_more_evidence.append(
                {
                    "research_task_id": task_id,
                    "candidate_id": candidate.get("candidate_id"),
                    "supplemental_package": repo_relative(SUPPLEMENTAL_PACKAGE),
                    "gate_status": gate["gate_status"],
                }
            )
            continue

        failures.append(f"{task_id}: unsupported decision {result['decision']}")

    report = {
        "report_id": "phase45_order_semantics_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "expected_total": 6,
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more_evidence),
        "failures": failures,
        "promoted": promoted,
        "needs_more_evidence": needs_more_evidence,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
        "trade_execution_advice_enabled": False,
        "supplemental_reaudit_package": repo_relative(SUPPLEMENTAL_PACKAGE),
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == 5 and len(needs_more_evidence) == 1 and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
