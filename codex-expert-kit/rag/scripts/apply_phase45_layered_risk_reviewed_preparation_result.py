"""Apply Phase 45 Layered Risk reviewed/caveat_only preparation result.

This task consumes the strict reviewed/caveat_only preparation audit for the
six Phase 45 Layered Risk / Credit / Margin candidates. It creates formal
reviewed/caveat_only knowledge only for entries explicitly allowed by the
audit. It never creates approved knowledge, default guidance, hard gates, risk
thresholds, credit limits, margin ratios, funding sufficiency conclusions, or
trading execution advice.
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
TASK_ID = "CEK-TA-462"
AUDIT_RESULT_ID = "audit_phase45_layered_risk_reviewed_caveat_only_preparation_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_layered_risk_reviewed_preparation_audit_package_20260612"
PARTITION = "KB_07_RISK_MANAGEMENT"
EXPECTED_TOTAL = 6

AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_layered_risk_formal_import_report.json", start_file=__file__)
REPO_ROOT = resolve_repo_path(".", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-C-RISK01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "SEC 15c3-5、CME pre-trade risk tools 和 FIA automated trading safeguards 足以支撑 pre-trade controls 分层边界。"
        ],
        "patch_notes": {
            "source": [
                "SEC Rule 15c3-5 只支撑美国 broker-dealer market access 语境。",
                "CME 和 FIA 来源分别是 venue-specific 工具与行业最佳实践来源。"
            ],
            "content": [
                "订单级、账户级、策略级、产品/venue 级、信用/保证金级和系统级是 CEK-TA 内部分层 taxonomy。"
            ],
            "boundary": [
                "不得把分层 control 自动变成 hard gate；不得输出任何风险阈值。"
            ],
            "conflict": ["未发现与 Phase 37 Risk Management 或 Phase 45 runtime contract 的直接冲突。"],
        },
    },
    {
        "research_task_id": "P45-C-RISK02",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "SEC FAQ 和 CME Globex Credit Controls 足以支撑 credit/capital/exposure control 与 strategy risk owner 分离。"
        ],
        "patch_notes": {
            "source": [
                "SEC FAQ 只支撑 broker-dealer financial exposure controls。",
                "CME Globex Credit Controls 只支撑 clearing-firm risk administrator 与 CME 语境。"
            ],
            "content": [
                "credit limit 不等于 strategy loss limit、仓位 sizing 或 alpha risk preference。"
            ],
            "boundary": [
                "不得输出信用额度、资本阈值、账户限制数值或资金充足性结论。"
            ],
            "conflict": ["credit owner 与 strategy risk owner 必须在外接项目中保持分离。"],
        },
    },
    {
        "research_task_id": "P45-C-RISK03",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "SEC price/size parameter controls 和 CME price banding/pre-trade risk tools 足以支撑 order admission controls 独立于策略信号。"
        ],
        "patch_notes": {
            "source": [
                "CME price banding 只能作为 venue-specific 示例，不得泛化为所有 venue。"
            ],
            "content": [
                "最大订单量、price collar、price band 和 fat-finger controls 必须声明 venue/product/version/evidence。"
            ],
            "boundary": [
                "策略信号强度、AI 置信度或 alpha 分数不得作为绕过 order admission controls 的理由。"
            ],
            "conflict": ["order admission controls 归 Live Execution / Risk Management owner。"],
        },
    },
    {
        "research_task_id": "P45-C-RISK04",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "CME messaging controls 和 FIA automated trading safeguards 足以支撑 message throttle / cancel-rate controls 的审计边界。"
        ],
        "patch_notes": {
            "source": [
                "CME messaging controls 只支撑 CME iLink / CME venue excessive messaging 语境。"
            ],
            "content": [
                "message pressure 是 system / venue risk，不是成交风险、PnL 风险或策略 alpha。"
            ],
            "boundary": [
                "不得输出 CME MPS、EMT、volume ratio、cancel-rate 等具体数值作为 CEK-TA 通用阈值。"
            ],
            "conflict": ["message throttle / cancel-rate controls 引用 Live Execution、Market Microstructure 和 Audit Trail。"],
        },
    },
    {
        "research_task_id": "P45-C-RISK05",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "CME 支撑 clearing margin/performance bond/SPAN，IBKR 支撑 available funds/excess liquidity/buying power，Binance Futures API 支撑 crypto venue availableBalance/wallet/margin 字段语义，内部 contract 补齐 point-in-time account_margin_collateral_evidence。"
        ],
        "patch_notes": {
            "source": [
                "CME 来源只支撑 CME Clearing / SPAN / performance bond 语境。",
                "IBKR 字段只支撑 IBKR broker/account-type 语境。",
                "Binance Futures 字段只支撑 Binance USDⓈ-M Futures/API/account-mode 语境。"
            ],
            "content": [
                "margin、performance bond、collateral、available funds、buying power、wallet balance、margin balance、strategy capital budget 必须拆分。",
                "point-in-time account/margin/collateral evidence 必须包含 broker/venue、account_mode、field_name、source timestamp、snapshot_id、staleness_status、semantic_boundary 和 owner。"
            ],
            "boundary": [
                "任何账户字段都不能默认解释为可交易现金。",
                "不得输出资金充足性结论、保证金比例、信用额度、可用资金判断或下单许可。"
            ],
            "conflict": ["未发现与 Phase 37 Risk Management、Phase 45 Execution TCA / Audit Trail 或 runtime contract 的直接冲突。"],
        },
    },
    {
        "research_task_id": "P45-C-RISK06",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "SEC 15c3-5、FIA 和 CME pre-trade risk tools 足以支撑 post-trade surveillance 不能替代 pre-trade controls 的边界。"
        ],
        "patch_notes": {
            "source": [
                "SEC/FIA/CME 来源支撑 pre-trade controls 与 post-trade analysis 的职责区分，但不直接定义 CEK-TA deterministic gate。"
            ],
            "content": [
                "post-trade surveillance 只能发现、解释和复盘已发生事件。"
            ],
            "boundary": [
                "本候选不得启用拒单、停机、撤单、解锁或任何 hard gate。"
            ],
            "conflict": ["deterministic gate 只能由外接项目 Risk Management / Live Execution owner 另行定义。"],
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
    cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
    return sorted(cand_dir.glob("cand_20260612_phase45_layered_risk_*.json"))


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
                "risk_threshold_advice_allowed": False,
                "reasons": item["reasons"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
        "mandatory_caveats": [
            "SEC Rule 15c3-5 只支撑美国 broker-dealer market access 语境，不得泛化为全球市场、crypto venue 或全部 broker。",
            "FIA 是行业最佳实践来源，不是 CEK-TA 阈值来源，也不是强制监管规则。",
            "CME 来源只支撑 CME Globex / CME Clearing / CME product 语境。",
            "IBKR 字段只支撑 IBKR broker/account-type 语境。",
            "Binance Futures 字段只支撑 Binance USDⓈ-M Futures/API/account-mode 语境。",
            "reviewed/caveat_only 只能用于风控设计、owner 边界、证据字段和审计提醒，不能生成交易许可、资金充足性结论、风控阈值或 hard gate。",
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
        normalized = str(candidate.get("claim", {}).get("normalized_claim", candidate.get("research_task_id", "")))
        normalized = normalized.replace("phase45_layered_risk.", "")
        knowledge_id = f"kb_phase45_layered_risk.{re.sub(r'[^a-zA-Z0-9_.-]+', '_', normalized)}.v1"

    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    source_refs = candidate.get("source_refs", [])
    patch_notes = result["patch_notes"]

    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(claim.get("title") or candidate.get("research_task_id")),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": "layered_risk_boundary_rule",
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
            "classification_notes": "Phase 45 Layered Risk formal reviewed/caveat_only；只用于风控设计、owner 边界、证据字段和审计提醒，不是 approved/default guidance/hard gate，不生成交易许可、资金充足性结论、风控阈值、信用额度或保证金比例。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_broker_venue_jurisdiction_caveats"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "pre_trade_and_post_trade_events"),
            "data_granularity": applicability.get("data_granularity", "risk_controls_account_snapshots_order_events"),
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
                "确认问题属于 Layered Risk / Credit / Margin、pre-trade controls、credit/capital exposure、order admission、message pressure、account/margin/collateral evidence 或 post-trade surveillance。",
                "检查每个风控字段是否声明 owner、evidence_source_id、policy_version、decision_time、result、action_semantics 和 audit_trace_id。",
                "若涉及 broker/venue/account 字段，必须保留 product_scope、account_mode、field_name、source timestamp、snapshot_id、staleness_status、semantic_boundary 和 owner。",
                "若出现 unavailable、stale、unknown，不得静默视为 pass、资金充足或可下单。",
                "若外接项目需要拒单、停机、撤单、解锁或下单许可，必须由外接项目 Risk Management / Live Execution owner 的 deterministic policy 定义。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "examples": [],
            "anti_patterns": string_list(
                [
                    "把 SEC、CME、IBKR、Binance 或 FIA 来源泛化为所有市场或所有 broker。",
                    "把 available funds、buying power、excess liquidity、wallet balance、available balance、margin balance、collateral、performance bond 互相等同。",
                    "把任一账户字段默认解释为可交易现金。",
                    "输出风险阈值、信用额度、保证金比例、资金充足性结论、下单许可、买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                    "把 reviewed/caveat_only 当作 approved、default guidance 或 hard gate。",
                    "把 post-trade surveillance 当作 pre-trade controls 的替代品。",
                ]
                + as_list(claim.get("anti_patterns"))
            ),
            "validation": [
                "source_evidence 至少包含监管/交易所/券商/清算/平台来源，并明确来源适用边界。",
                "若涉及 RISK05，必须包含 point-in-time account/margin/collateral evidence 契约或等价字段说明。",
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate/risk_threshold_advice 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "不得出现资金充足性结论、信用额度、保证金比例、可用资金判断或下单许可。",
            ],
            "risk_notes": [
                "Layered Risk reviewed/caveat_only 只能作为风控设计、owner 边界和证据审计上下文。",
                "监管来源具有辖区边界；broker/venue/platform 来源具有账户类型、产品和 API 语义边界。",
                "AI Engineering 只能引用 reason code 和 evidence，不拥有阈值或执行动作。",
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
            "resolution_summary": "reviewed/caveat_only 准备审计通过；formal creation 保持 caveat_only，不创建 approved、default guidance、hard gate、风险阈值建议或资金充足性结论。",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "funding_sufficiency_conclusion_allowed": False,
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
            "funding_sufficiency_conclusion_allowed": False,
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
                "risk_threshold_advice_allowed": False,
                "reasons": result["reasons"],
                "patch_notes": patch_notes,
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计分层风控、owner 边界、证据字段和审计 checklist。",
                "用于检查外接项目是否区分 credit limit、strategy risk limit、order admission、message pressure、account/margin/collateral evidence 和 post-trade surveillance。",
                "用于生成 reason code、schema review、RAG 检索上下文和风险设计审计问题。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈、实盘执行建议、风险阈值、信用额度、保证金比例、资金充足性结论或下单许可。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得把 account field check、message pressure 或 post-trade surveillance 写成 CEK-TA hard gate。",
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
            "funding_sufficiency_conclusion_allowed": False,
            "trade_execution_advice_allowed": False,
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
        if candidate.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            failures.append(f"{task_id}: candidate is not accepted_for_draft")
            continue

        workflow = candidate.setdefault("workflow", {})
        workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate", "risk_threshold_advice"]
        conversion = workflow.setdefault("conversion_target", {})
        conversion.update(
            {
                "target_review_status": "reviewed",
                "target_machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
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
        workflow["funding_sufficiency_conclusion_allowed"] = False
        workflow["trade_execution_advice_allowed"] = False
        candidate.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_layered_risk_formal_reviewed_created",
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
        "report_id": "phase45_layered_risk_formal_import_report",
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
        "funding_sufficiency_conclusion_enabled": False,
        "trade_execution_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps({"promoted_count": len(promoted), "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == EXPECTED_TOTAL and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
