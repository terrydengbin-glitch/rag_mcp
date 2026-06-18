"""Apply Phase 37 Quant Foundation first audit result to candidates.

The audit result allows accepted_for_draft or needs_more_evidence only. It
does not create formal reviewed knowledge, approved knowledge, default
guidance, or hard gates.
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
AUDIT_RESULT_ID = "audit_result_phase37_quant_foundation_candidate_audit_20260611_strict_v1"
PACKAGE_ID = "phase37_quant_foundation_candidate_audit_package_20260611"
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_01_QUANT_FOUNDATION", start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_quant_foundation_audit_import_report.json", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P37-A-Q01",
        "slug": "expected_value_definition",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": ["期望值概率加权 payoff 框架有 Morgan Stanley 与 Investopedia 支撑。"],
        "required_followups": ["正式 draft 前可补概率论或投资组合教材来源。"],
    },
    {
        "research_task_id": "P37-A-Q02",
        "slug": "r_multiple_definition",
        "decision": "needs_more_evidence",
        "confidence": "high",
        "reasons": ["R-multiple 本体来源偏 vendor/教育材料，CFA 只间接支持成本/执行边界。"],
        "required_followups": ["补 R-multiple 本体来源；调整分类到 performance/risk-normalized metrics。"],
    },
    {
        "research_task_id": "P37-A-Q03",
        "slug": "risk_reward_boundary",
        "decision": "accepted_for_draft",
        "confidence": "medium",
        "reasons": ["高 R/R 不能单独证明优势，与风险收益比定义、EV 逻辑和执行成本边界一致。"],
        "required_followups": ["正式 draft 前补样本外验证或回测偏差来源。"],
    },
    {
        "research_task_id": "P37-A-Q04",
        "slug": "cost_adjusted_expectancy_required",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": ["CFA 交易执行资料足以支持成本假设是评价证据的一部分。"],
        "required_followups": [],
    },
    {
        "research_task_id": "P37-A-Q05",
        "slug": "win_rate_not_enough",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": ["胜率不能单独证明质量，EV 的 probability/payoff 框架和回测过拟合资料足以支持 draft。"],
        "required_followups": ["正式 draft 前可补 tail risk/drawdown 专门来源。"],
    },
    {
        "research_task_id": "P37-A-Q06",
        "slug": "position_sizing_requires_risk_unit",
        "decision": "accepted_for_draft",
        "confidence": "medium",
        "reasons": ["风险预算、风险单位、失效边界和最大暴露作为字段前置条件合理；AI 不能推导仓位属于治理边界。"],
        "required_followups": ["正式 draft 中明确 AI 不能推导仓位是 CEK-TA 治理边界，不是外部金融事实。"],
    },
    {
        "research_task_id": "P37-A-Q07",
        "slug": "leverage_amplifies_drawdown",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": ["FINRA/CFTC/SEC 类来源支撑杠杆和保证金的损失放大、追加保证金和强平风险。"],
        "required_followups": ["保留地区、品种和交易所差异。"],
    },
    {
        "research_task_id": "P37-A-Q08",
        "slug": "signal_decision_execution_separation",
        "decision": "needs_more_evidence",
        "confidence": "high",
        "reasons": ["现有 CFA/FINRA 来源只能间接支持执行与风险边界，不足以支撑分层记录架构规则。"],
        "required_followups": ["补 FIX Protocol、OMS/EMS、broker order lifecycle、Execution Report / fill report 来源。"],
    },
    {
        "research_task_id": "P37-A-Q09",
        "slug": "trade_frequency_vs_quality_boundary",
        "decision": "needs_more_evidence",
        "confidence": "high",
        "reasons": ["原 statement 对 general market/general asset 表述过宽，FINRA 只足以支撑日内/保证金语境。"],
        "required_followups": ["收窄到高周转、日内、保证金、杠杆或流动性受限场景；补 TCA、market microstructure、turnover cost 来源。"],
    },
    {
        "research_task_id": "P37-A-Q10",
        "slug": "edge_requires_out_of_sample_evidence",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": ["Bailey 等回测过拟合论文和回测风险资料支持独立验证、样本外和过拟合边界。"],
        "required_followups": [],
    },
    {
        "research_task_id": "P37-A-Q11",
        "slug": "sample_size_and_regime_caveat",
        "decision": "accepted_for_draft",
        "confidence": "medium",
        "reasons": ["样本数量、时期、资产范围和市场状态必须声明，与小样本、选择偏差和过拟合风险一致。"],
        "required_followups": ["正式 draft 前可补 regime/non-stationarity 直接来源。"],
    },
    {
        "research_task_id": "P37-A-Q12",
        "slug": "no_profit_claim_without_costs",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": ["CFA 执行成本与 Bailey/回测风险来源支撑没有成本和偏差说明时不得声称可复用盈利能力。"],
        "required_followups": [],
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
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "scope": "Phase 37 Quant Foundation candidate first strict audit",
        "summary": {
            "total": 12,
            "accepted_for_draft": 9,
            "needs_more_evidence": 3,
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
        "global_findings": [
            "未发现明显中文乱码、mock/test 污染、项目私有策略参数、账户事实、密钥、交易所配置或实盘敏感信息。",
            "Q02、Q08、Q09 需要补证后再进入二审。",
            "正式知识转换前应对 Q01/Q05/Q10/Q12 做语义重叠和合并检查。",
        ],
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
            }
            for item in RESULTS
        ],
    }


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
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "decision": decision,
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "boundary": "accepted_for_draft is not reviewed or approved; this audit does not allow default guidance or hard gate.",
    }

    status["updated_at"] = TODAY
    status["decision_reason"] = (
        f"Phase 37 首轮严格审计结论为 {decision}；不允许 reviewed/approved/default guidance/hard gate。"
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
    machine_gate["reason"] = "Phase 37 candidate audit does not allow default guidance; formal reviewed requires a later gate."
    machine_gate["requires_human_escalation"] = True

    conversion = payload.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft" if decision == "accepted_for_draft" else "blocked"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    if decision == "accepted_for_draft":
        status["review_status"] = "accepted"
        status["ingestion_decision"] = "accepted_for_draft"
        workflow["stage"] = "ai_audited"
        workflow["queue_group"] = "ai_passed"
        workflow["next_action"] = "prepare_formal_draft_after_separate_reviewed_gate"
    elif decision == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "supplement_sources_and_export_reaudit_package"
    else:
        status["review_status"] = decision
        status["ingestion_decision"] = decision
        workflow["stage"] = decision
        workflow["queue_group"] = decision
        workflow["next_action"] = "manual_review"

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase37_quant_foundation_first_audit_imported",
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
        "report_id": "phase37_quant_foundation_audit_import_report",
        "generated_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "updated_count": len(updated),
        "decision_counts": archive["summary"],
        "updated": updated,
        "next_action": "supplement P37-A-Q02/P37-A-Q08/P37-A-Q09 and export supplemental re-audit package.",
        "boundary": "No formal reviewed knowledge, approved knowledge, default guidance, or hard gate was created.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps({"updated_count": len(updated), "needs_more_evidence": 3}, ensure_ascii=False))


if __name__ == "__main__":
    main()
