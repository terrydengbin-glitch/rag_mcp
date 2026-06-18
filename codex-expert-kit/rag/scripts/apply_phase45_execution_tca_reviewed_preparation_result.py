"""Apply Phase 45 Execution TCA reviewed/caveat_only preparation result.

This task consumes the strict reviewed/caveat_only preparation audit for the
six Phase 45 Execution TCA candidates. It creates formal reviewed/caveat_only
knowledge only for entries explicitly allowed by the audit. It never creates
approved knowledge, default guidance, hard gates, risk thresholds, or trading
execution advice.
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
TASK_ID = "CEK-TA-458"
AUDIT_RESULT_ID = "audit_phase45_execution_tca_reviewed_caveat_only_preparation_20260612_v1"
SOURCE_PACKAGE_ID = "phase45_execution_tca_reviewed_preparation_audit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_07_TRADE_ANALYSIS"]
EXPECTED_TOTAL = 6

AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_execution_tca_import_report.json", start_file=__file__)
REPO_ROOT = resolve_repo_path(".", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-A-TCA01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["implementation shortfall、显性/隐性成本、market impact、delay、opportunity cost 的证据充足。"],
        "patch_notes": {
            "source": ["CFA 是 TCA 概念主来源；平台文档只能作为实现 supporting。"],
            "content": ["必须记录解释为 CEK-TA Execution TCA reviewed/caveat_only 内部字段要求，不是全球监管硬规则。"],
            "boundary": ["不得把 TCA 结果当作策略 alpha 或交易许可。"],
            "conflict": ["未发现与 Live Execution / Trade Analysis 分区冲突。"],
        },
    },
    {
        "research_task_id": "P45-A-TCA02",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["CFA 支撑 arrival price、VWAP、TWAP 等 benchmark 选择边界。"],
        "patch_notes": {
            "source": ["CFA 是 benchmark selection 主来源；FINRA 仅作 best execution context supporting。"],
            "content": ["benchmark 必须绑定使用目的、时间窗口、订单类型、数据源和不可解释范围。"],
            "boundary": ["不得从单一 benchmark 表现推导执行整体好。"],
            "conflict": ["无明显冲突。"],
        },
    },
    {
        "research_task_id": "P45-A-TCA03",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["FIXatdl 和 IBKR 文档足以支撑 VWAP/TWAP/POV 属于 execution algo / participation algo 语义。"],
        "patch_notes": {
            "source": ["FIXatdl 只能证明算法订单接口和参数语义；IBKR 只能作为 broker-specific 示例。"],
            "content": ["VWAP/TWAP/POV 是 execution scheduling / participation algorithm，不是交易信号。"],
            "boundary": ["不得泛化为所有交易所或所有市场。"],
            "conflict": ["未发现与 Live Execution / Execution TCA 分区冲突。"],
        },
    },
    {
        "research_task_id": "P45-A-TCA04",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["delay cost、market impact、spread/fee/slippage、opportunity cost 拆分有 CFA 直接支撑。"],
        "patch_notes": {
            "source": ["CFA 是成本拆分主来源；QuantConnect 只能作为 fill/slippage/fee 建模辅助。"],
            "content": ["缺失 benchmark / arrival_price / order_ts / unfilled_qty 时应输出 missing-data reason code。"],
            "boundary": ["不得把 opportunity cost 静默忽略，也不得直接归因成策略胜率问题。"],
            "conflict": ["无明显冲突。"],
        },
    },
    {
        "research_task_id": "P45-A-TCA05",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["FINRA 5310 和 SEC Rule 606 足以支撑 best execution / routing context，但必须保留辖区边界。"],
        "patch_notes": {
            "source": ["FINRA/SEC 只支撑美国 broker-dealer / NMS stocks / listed options 等语境。"],
            "content": ["routing context 应保留 market、venue、order、conflict、disclosure、execution_result。"],
            "boundary": ["不能泛化到 crypto、外汇、离岸交易所或所有 broker。"],
            "conflict": ["无明显冲突。"],
        },
    },
    {
        "research_task_id": "P45-A-TCA06",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["Bailey PBO 和 White Reality Check 足以支撑 execution-derived alpha 必须进入独立策略验证流程。"],
        "patch_notes": {
            "source": ["CFA/QuantConnect 支撑 execution cost/fill/slippage 边界；Bailey/White 支撑过拟合和 data snooping 边界。"],
            "content": ["本条不证明任何 execution feature 具有 alpha；只要求若主张 alpha 必须独立验证。"],
            "boundary": ["低滑点、VWAP outperform、routing improvement 默认只能解释 implementation cost。"],
            "conflict": ["显式引用 Strategy Research / Backtest Validation；与 Execution TCA 分区不冲突。"],
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
    paths: list[Path] = []
    for partition in PARTITIONS:
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_execution_tca_*.json")))
    return paths


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
                "reasons": item["reasons"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
        "global_required_patches": [
            "修正 workflow.forbidden_next_decisions 与 conversion_target.target_review_status=reviewed 的元数据冲突。",
            "formal reviewed 只能是 caveat_only，approved/default guidance/hard gate 必须保持 false。",
        ],
    }


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if str(item).strip()]


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    workflow = candidate.get("workflow", {})
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    knowledge_id = str(conversion.get("proposed_knowledge_id") or candidate.get("workflow", {}).get("formal_knowledge_id") or "")
    if not knowledge_id:
        normalized = str(candidate.get("claim", {}).get("normalized_claim", candidate.get("research_task_id", "")))
        knowledge_id = f"kb_phase45_execution_tca.{re.sub(r'[^a-zA-Z0-9_.-]+', '_', normalized)}.v1"
    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    patch_notes = result["patch_notes"]
    source_refs = candidate.get("source_refs", [])
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(claim.get("title") or candidate.get("research_task_id")),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": "execution_tca_boundary_rule",
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
            "classification_notes": "Phase 45 Execution TCA formal reviewed/caveat_only；只用于执行成本、benchmark、routing context 和执行质量审计，不是 approved/default guidance/hard gate，不生成交易动作。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general_with_market_specific_caveats"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
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
                "确认问题属于 Execution TCA、执行成本、benchmark、routing context 或执行质量审计。",
                "检查订单、成交、费用、滑点、未成交数量、benchmark、arrival/decision timestamp 和 routing context 是否可追溯。",
                "若涉及真实订单、成交、费用或 broker/venue 事实，必须引用 Live Execution owner 产物。",
                "若把 execution-derived feature 主张为 alpha，必须转入 Strategy Research / Backtest Validation 分支独立验证。",
                "返回知识时必须携带 source_evidence、review_status、machine_gate、适用范围、不适用场景和 owner 边界。",
            ],
            "examples": [],
            "anti_patterns": string_list(
                [
                    "把 execution algo、TCA 优化、低滑点或 benchmark outperform 直接写成交易信号。",
                    "用单一 benchmark 表现证明整体 execution quality。",
                    "把 FINRA/SEC 规则泛化到所有市场、所有 broker 或 crypto/外汇/离岸交易所。",
                    "把 TCA 结果用于买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值。",
                ]
                + as_list(claim.get("anti_patterns"))
            ),
            "validation": [
                "source_evidence 至少包含专业/监管/协议/官方平台来源，并明确来源适用边界。",
                "review.review_status 必须为 reviewed；approved/default guidance/hard gate 必须为 false。",
                "machine_gate.default_guidance 必须为 caveat_only，且 visible_in_default_guidance_queue=false。",
                "不得出现买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
            ],
            "risk_notes": [
                "Execution TCA reviewed/caveat_only 只能作为执行成本和执行质量审计上下文。",
                "TCA、benchmark、routing context 和 execution algo 不证明策略有效或可盈利。",
                "监管来源具有辖区边界；broker/platform 来源具有实现边界。",
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
            "approved_at": None,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": result["reasons"],
                "patch_notes": patch_notes,
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分策略信号、执行算法、订单事实和 TCA 复盘。",
                "用于设计 execution-quality reason code、audit checklist、RAG 检索上下文。",
                "用于检查外接项目方案是否遗漏成本、benchmark、routing context 或 opportunity cost。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得把执行算法、TCA 指标或 routing 选择写成策略 alpha 或 hard gate。",
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
        workflow = candidate.setdefault("workflow", {})
        workflow["forbidden_next_decisions"] = ["approved", "default_guidance", "hard_gate"]
        conversion = workflow.setdefault("conversion_target", {})
        conversion.update(
            {
                "target_review_status": "reviewed",
                "target_machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
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
        candidate.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_execution_tca_formal_reviewed_created",
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
        "report_id": "phase45_execution_tca_import_report",
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
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps({"promoted_count": len(promoted), "failures": failures}, ensure_ascii=False, indent=2))
    return 0 if len(promoted) == EXPECTED_TOTAL and not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
