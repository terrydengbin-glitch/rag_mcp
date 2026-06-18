"""Apply Phase 37 Quant Foundation supplemental re-audit result.

This imports the second audit for P37-A-Q02/Q08/Q09. It only updates
candidate workflow state and patch notes. It does not create formal reviewed
knowledge, approved knowledge, default guidance, or hard gates.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
AUDIT_RESULT_ID = "audit_result_phase37_quant_foundation_supplemental_reaudit_20260611_strict_v1"
PACKAGE_ID = "phase37_quant_foundation_supplemental_reaudit_package_20260611"
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_01_QUANT_FOUNDATION", start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_quant_foundation_supplemental_reaudit_import_report.json", start_file=__file__
)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P37-A-Q02",
        "slug": "r_multiple_definition",
        "decision": "needs_more_evidence",
        "confidence": "high",
        "reasons": [
            "R-multiple 直接本体来源仍主要是交易日志、教育或供应商网页，不足以作为专业知识库中 risk-normalized metric 定义的强来源。",
            "CFA execution/risk 来源只能支持成本、执行和风险边界，不能计为 R-multiple 定义的一手主来源。",
            "canonical node 仍在 position_sizing，只增加 related_nodes，未完全满足 performance/risk-normalized metrics 的分类要求。",
        ],
        "required_followups": [
            "补充更强的 R/R-multiple 本体来源：可核验书籍版次和页码、专业课程材料、研究论文或机构级交易绩效评价资料。",
            "将 canonical node 调整为 performance_metrics / risk_normalized_metrics，或新增独立 L3 节点；position_sizing 只能作为 related dependency。",
            "保留边界：R-multiple 只能作为风险归一化复盘/标签候选指标，不能替代成本、滑点、样本外验证、回撤和风控审计。",
        ],
        "patch_notes": [
            "保持 needs_more_evidence，不升级 accepted_for_draft。",
            "后续应单独处理 L3 节点或分类契约，而不是把 position_sizing 当作主节点长期承载 performance metric。",
        ],
    },
    {
        "research_task_id": "P37-A-Q08",
        "slug": "signal_decision_execution_separation",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "FIX/FIXimate、OnixS、Trading Technologies 的 ExecutionReport 来源已直接支撑 order/execution/fill/result 层的证据链。",
            "CFA Trade Strategy and Execution 支撑决策、订单、执行、评价链路和 execution quality 审计。",
        ],
        "required_followups": [
            "正式 draft 前补 OMS/EMS/order lifecycle 文档或内部事件链 schema 标准。",
            "补充不同 venue / broker / asset class 下 ExecutionReport 或 fill-report 字段差异。",
        ],
        "patch_notes": [
            "将“必须分层记录”限定为 CEK-TA 交易系统事件流与 AI 审计 schema 的架构要求，不表述为所有市场的外部监管硬要求。",
            "建议 schema 显式拆分 signal_id、decision_id、order_intent_id、execution_report_id、fill_id、trade_result_id。",
            "AI Engineering 只能引用，不得复制或改写 Trading Engineering 规则本体。",
        ],
    },
    {
        "research_task_id": "P37-A-Q09",
        "slug": "trade_frequency_vs_quality_boundary",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "补证后 statement 已收窄到高周转、日内、保证金、杠杆或流动性受限场景，解决原泛化过宽问题。",
            "FINRA 2026 intraday margin 资料、CFA 交易成本材料和 factor-cost 摘要支撑 TCA/turnover cost 边界。",
        ],
        "required_followups": [
            "正式 draft 前补更强的 TCA / market microstructure 教材、论文或机构材料。",
            "更新 FINRA intraday margin 来源元数据：Regulatory Notice 26-10 发布于 2026-04-20，生效日为 2026-06-04，phase-in 到 2027-10-20。",
        ],
        "patch_notes": [
            "保留高周转、日内、保证金、杠杆或流动性受限场景限定，不得回退为所有市场/所有资产泛化断言。",
            "保留“可能显著提高”，不得改写为“必然提高”。",
            "不得把该规则改写为禁止高频/高周转策略，也不得输出交易频率、仓位或执行建议。",
        ],
    },
]


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_path(slug: str) -> Path:
    return CANDIDATE_DIR / f"cand_20260611_phase37_{slug}_001.json"


def build_audit_archive() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "auditor": "external_ai_strict_reaudit",
        "audited_at": TODAY,
        "scope": "Phase 37 Quant Foundation supplemental re-audit for P37-A-Q02/Q08/Q09",
        "summary": {
            "total": 3,
            "accepted_for_draft": 2,
            "needs_more_evidence": 1,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "candidate_only": True,
        },
        "candidate_results": [
            {
                "candidate_id": f"cand_20260611_phase37_{item['slug']}_001",
                "research_task_id": item["research_task_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": item["reasons"],
                "required_followups": item["required_followups"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
        "source_urls_referenced_by_auditor": [
            "https://trademetria.com/blog/what-are-r-multiples-the-key-metric-every-trader-should-know/",
            "https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html?find=Side",
            "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
            "https://www.finra.org/rules-guidance/rulebooks/finra-rules/2270",
            "https://www.finra.org/rules-guidance/notices/26-10",
            "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
            "https://rpc.cfainstitute.org/research/financial-analysts-journal/2019/ip-transaction-costs-of-factor-investing-strategies",
        ],
    }


def append_unique_strings(existing: list[Any], additions: list[str]) -> list[str]:
    values: list[str] = [str(item) for item in existing if isinstance(item, str)]
    for addition in additions:
        if addition not in values:
            values.append(addition)
    return values


def patch_candidate(payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    decision = str(result["decision"])
    status = payload.setdefault("status", {})
    workflow = payload.setdefault("workflow", {})
    review = payload.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log

    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    review["open_questions"] = append_unique_strings(review.get("open_questions", []), result.get("required_followups", []))
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "auditor": "external_ai_strict_reaudit",
        "audited_at": TODAY,
        "decision": decision,
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": result.get("patch_notes", []),
        "boundary": "accepted_for_draft is not reviewed or approved; this re-audit does not allow default guidance or hard gate.",
    }

    claim = payload.setdefault("claim", {})
    interpretation = str(claim.get("interpretation_notes", ""))
    patch_text = " 二审补丁：" + "；".join(result.get("patch_notes", []))
    if patch_text not in interpretation:
        claim["interpretation_notes"] = (interpretation + patch_text).strip()

    source_quality = payload.setdefault("source_quality", {})
    source_quality["limitations"] = append_unique_strings(source_quality.get("limitations", []), result.get("patch_notes", []))

    conflict = payload.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False
    if decision == "accepted_for_draft":
        conflict["resolution_summary"] = (
            "二审允许 accepted_for_draft，但仍需后续 reviewed/caveat_only 准备审计；不得直接 approved/default guidance/hard gate。"
        )
    else:
        conflict["resolution_summary"] = "二审仍为 needs_more_evidence，需继续补来源和分类契约。"

    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"Phase 37 二审结论为 {decision}；不允许 reviewed/approved/default guidance/hard gate。"
    )
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False

    machine_gate = payload.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Phase 37 candidate re-audit does not allow default guidance; formal reviewed requires a later gate."
    machine_gate["requires_human_escalation"] = True

    conversion = payload.setdefault("conversion_target", {})
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    if decision == "accepted_for_draft":
        status["review_status"] = "accepted"
        status["ingestion_decision"] = "accepted_for_draft"
        workflow["stage"] = "ai_audited"
        workflow["queue_group"] = "ai_passed"
        workflow["next_action"] = "prepare_formal_draft_after_separate_reviewed_gate"
        conversion["target_review_status"] = "draft"
    elif decision == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "supplement_stronger_sources_and_classification_contract"
        conversion["target_review_status"] = "blocked"
    else:
        status["review_status"] = decision
        status["ingestion_decision"] = decision
        workflow["stage"] = decision
        workflow["queue_group"] = decision
        workflow["next_action"] = "manual_review"
        conversion["target_review_status"] = "blocked"

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_reaudit",
            "action": "phase37_quant_foundation_supplemental_reaudit_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )
    return payload


def main() -> None:
    archive = build_audit_archive()
    write_json(AUDIT_ARCHIVE, archive)
    updated: list[dict[str, str]] = []
    for result in archive["candidate_results"]:
        slug = str(result["candidate_id"]).removeprefix("cand_20260611_phase37_").removesuffix("_001")
        path = candidate_path(slug)
        if not path.exists():
            raise FileNotFoundError(path)
        payload = patch_candidate(read_json(path), result)
        write_json(path, payload)
        updated.append({"candidate_id": result["candidate_id"], "decision": result["decision"], "path": str(path)})

    report = {
        "report_id": "phase37_quant_foundation_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "updated_count": len(updated),
        "decision_counts": archive["summary"],
        "updated": updated,
        "remaining_needs_more_evidence": ["P37-A-Q02"],
        "next_action": "Either supplement P37-A-Q02 with stronger sources and a new metrics node contract, or hold it outside formal conversion. Other 11 candidates can enter the later formal reviewed-preparation gate.",
        "boundary": "No formal reviewed knowledge, approved knowledge, default guidance, or hard gate was created.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"updated_count": len(updated), "accepted_for_draft": 2, "needs_more_evidence": 1}, ensure_ascii=False))


if __name__ == "__main__":
    main()
