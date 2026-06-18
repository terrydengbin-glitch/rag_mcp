"""Apply Phase 45 Order Semantics ORD05 supplemental re-audit result.

This script promotes only P45-F-ORD05 from needs_more_evidence to formal
reviewed/caveat_only after the supplemental audit passed. It never creates
approved knowledge, default guidance, hard gates, order submission permission,
routing advice, fee optimization advice, auto cancel / replace actions, or live
trading actions.
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
AUDIT_RESULT_ID = "audit_phase45_order_semantics_ord05_supplemental_reaudit_20260612"
SOURCE_PACKAGE_ID = "phase45_order_semantics_ord05_supplemental_reaudit_package_20260612"
PARTITION = "KB_06_LIVE_EXECUTION"
RESEARCH_TASK_ID = "P45-F-ORD05"
CANDIDATE_ID = "cand_20260612_phase45_order_semantics_p45_f_ord05_001"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    PARTITION,
    "cand_20260612_phase45_order_semantics_exchange_specific_order_type_caveat_001.json",
    start_file=__file__,
)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_order_semantics_ord05_formal_import_report.json", start_file=__file__)


RESULT: dict[str, Any] = {
    "candidate_id": CANDIDATE_ID,
    "research_task_id": RESEARCH_TASK_ID,
    "decision": "accepted_for_reviewed_caveat_only",
    "confidence": "high",
    "reviewed_allowed": True,
    "approved_allowed": False,
    "default_guidance_allowed": False,
    "hard_gate_allowed": False,
    "trade_execution_advice_allowed": False,
    "reasons": [
        "CME FirmSoft Order Type Definitions 明确列出 MKL = Market Limit，可支撑 market-to-limit / Market Limit 作为 CME-specific order semantics。",
        "IBKR Order Types, Algos and Tools 明确列出 VWAP Best-Efforts algo order type，可支撑 VWAP 作为 broker-specific execution algo semantics。",
        "Nasdaq、NYSE、CME、Coinbase、Binance、Kraken 等来源共同支撑 exchange-specific order behavior 不得泛化为通用语义。",
        "claim 已明确所有示例必须保留 exchange、product、session、rulebook、API version 和 adapter caveat。",
        "claim 未输出订单提交许可、路由建议、费用优化、自动撤单、自动改单或 hard gate。",
    ],
    "required_followups": [
        "正式 reviewed/caveat_only 文本必须保留：CME FirmSoft / Market Limit 只支撑 CME 语境，不得泛化为所有 venue。",
        "正式文本必须保留：IBKR VWAP Best-Efforts 是 broker-specific algo，不是通用 VWAP 订单类型、策略信号或路由建议。",
        "正式文本应继续强调本条是 anti-generalization caveat，不是特殊订单类型百科。",
        "外接项目必须为自身 venue/broker/API version 提供 rulebook_or_spec_ref 和 adapter_mapping_ref。",
    ],
    "patch_notes": {
        "source": [
            "保留 Nasdaq Opening/Closing Cross、NYSE Auctions、NYSE Pillar、CME Definitions、Coinbase、Binance、Kraken。",
            "新增并保留 CME FirmSoft Market Limit 官方来源。",
            "新增并保留 IBKR VWAP Best-Efforts 官方来源。",
        ],
        "content": [
            "保留 MOO/MOC/LOC、auction-only、peg、market-with-protection、market-to-limit、iceberg、RFQ、TWAP/VWAP、post-only、reduce-only 作为 venue-specific examples。",
            "所有示例必须绑定 exchange、product、session、rulebook、API version 和 adapter caveat。",
            "本条定位为 anti-generalization caveat，不定义任何订单提交规则。",
        ],
        "boundary": [
            "不得生成通用订单行为规则。",
            "不得生成订单提交许可。",
            "不得生成路由建议。",
            "不得生成费用优化建议。",
            "不得生成自动撤单或自动改单。",
            "不得生成 hard gate。",
        ],
        "conflict": [],
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


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if str(item).strip()]


def knowledge_id_for(candidate: dict[str, Any]) -> str:
    workflow = candidate.get("workflow", {})
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    explicit = conversion.get("proposed_knowledge_id") or workflow.get("formal_knowledge_id")
    if explicit:
        return str(explicit)
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or RESEARCH_TASK_ID)
    normalized = normalized.replace("phase45_order_semantics.", "")
    return f"kb_phase45_order_semantics.{re.sub(r'[^A-Za-z0-9_.-]+', '_', normalized)}"


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 1,
            "accepted_for_reviewed_caveat_only": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [RESULT],
        "global_required_patches": [
            "ORD05 只能作为 anti-generalization caveat，不是特殊订单类型百科。",
            "不得创建 approved、default guidance、hard gate、订单提交许可、路由建议、费用优化、自动撤单/改单。",
        ],
    }


def build_formal_item(candidate: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    source_refs = candidate.get("source_refs", [])
    patch_notes = RESULT["patch_notes"]
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id_for(candidate),
        "title": str(claim.get("title") or RESEARCH_TASK_ID),
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
            "classification_notes": "Phase 45 Order Semantics formal reviewed/caveat_only；本条只约束 exchange-specific order behavior 不得泛化，不是 approved/default guidance/hard gate，不生成订单动作。",
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
                "确认问题属于 Live Execution / Order Semantics 的 venue-specific 行为边界。",
                "每个特殊订单示例都必须绑定 exchange、product、session、rulebook、API version 和 adapter caveat。",
                "外接项目必须为自身 venue/broker/API version 提供 rulebook_or_spec_ref 和 adapter_mapping_ref。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "examples": [
                "Market Limit / market-to-limit 只能作为 CME-specific 示例使用。",
                "VWAP Best-Efforts 只能作为 IBKR broker-specific algo 示例使用。",
            ],
            "anti_patterns": string_list(
                [
                    "把特殊订单类型写成跨 venue 通用行为。",
                    "把 VWAP algo 写成策略信号、路由建议或订单提交许可。",
                    "把 Market Limit 写成所有市场都有的通用订单类型。",
                ]
                + as_list(claim.get("anti_patterns"))
            ),
            "validation": [
                "source_evidence 必须包含官方交易所、broker、venue 或 API 来源，并明确来源适用边界。",
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "不得出现买卖点、仓位、杠杆、止损止盈、路由建议、费用优化、实盘执行建议、订单提交许可、自动撤单或自动改单。",
            ],
            "risk_notes": [
                "本条是 anti-generalization caveat，不是特殊订单类型百科。",
                "CME FirmSoft / Market Limit 只支撑 CME 语境，不得泛化为所有 venue。",
                "IBKR VWAP Best-Efforts 是 broker-specific algo，不是通用 VWAP 订单类型、策略信号或路由建议。",
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
            "resolution_summary": "ORD05 supplemental re-audit passed; formal creation remains caveat_only and does not create approved, default guidance, hard gate, routing advice, fee optimization, or order actions.",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "review": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "confidence": RESULT["confidence"],
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
                "reasons": RESULT["reasons"],
                "patch_notes": RESULT["patch_notes"],
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检查特殊订单类型是否被错误泛化。",
                "用于生成 order semantics checklist、adapter contract review、schema review 和 RAG 检索上下文。",
                "用于检查外接项目是否为自身 venue/broker/API version 提供 rulebook_or_spec_ref 和 adapter_mapping_ref。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、路由建议、费用优化、订单提交许可或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、自动拒单、撤单、改单或路由策略。",
            ],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_visibility": "reviewed_caveat_only",
            "reason": "ORD05 supplemental reviewed/caveat_only audit passed; approved/default guidance/hard gate remain disabled.",
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


def main() -> int:
    write_json(AUDIT_ARCHIVE, audit_result_payload())
    candidate = read_json(CANDIDATE_PATH)
    if candidate.get("research_task_id") != RESEARCH_TASK_ID:
        raise ValueError(f"unexpected research_task_id in {CANDIDATE_PATH}")

    formal_item = build_formal_item(candidate)
    knowledge_dir = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION, start_file=__file__)
    formal_path = knowledge_dir / sanitize_filename(formal_item["knowledge_id"])
    write_json(formal_path, formal_item)

    candidate.setdefault("review", {}).setdefault("audit_log", [])
    candidate["review"]["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": RESULT["confidence"],
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "trade_execution_advice_allowed": False,
        "reasons": RESULT["reasons"],
        "required_followups": RESULT["required_followups"],
        "patch_notes": RESULT["patch_notes"],
    }
    candidate.setdefault("claim", {})["audit_patch_notes"] = RESULT["patch_notes"]
    candidate["status"].update(
        {
            "review_status": "formalized",
            "ingestion_decision": "formal_reviewed_created",
            "decision_reason": "ORD05 补证复审通过，已创建 formal reviewed/caveat_only。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
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
            "next_action": "none",
        }
    )
    candidate["review"]["audit_log"].append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase45_order_semantics_ord05_formal_reviewed_created",
            "reason": "created formal reviewed/caveat_only from ORD05 supplemental re-audit result",
            "audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": formal_item["knowledge_id"],
        }
    )
    write_json(CANDIDATE_PATH, candidate)

    report = {
        "report_id": "phase45_order_semantics_ord05_formal_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "promoted_count": 1,
        "promoted": [
            {
                "research_task_id": RESEARCH_TASK_ID,
                "candidate_id": CANDIDATE_ID,
                "knowledge_id": formal_item["knowledge_id"],
                "formal_path": repo_relative(formal_path),
            }
        ],
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
        "trade_execution_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
