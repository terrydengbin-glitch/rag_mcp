"""Apply Phase 37 Kline / Strategy Engineering supplemental re-audit result.

This imports the second audit for P37-C-K04/K05/K10/K12. It only updates
candidate workflow state and audit trace. It does not create formal reviewed
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
AUDIT_RESULT_ID = "audit_result_phase37_kline_strategy_supplemental_reaudit_20260611_strict_v1"
PACKAGE_ID = "phase37_kline_strategy_supplemental_reaudit_package_20260611"
PARTITION = "KB_02_KLINE_STRATEGY"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_kline_strategy_supplemental_reaudit_import_report.json", start_file=__file__
)


RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260611_phase37_kline_strategy_stop_loss_requires_invalidation_logic_001",
        "research_task_id": "P37-C-K04",
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": (
            "补证已把强表述收窄为记录风险管理目的、触发条件、执行假设和交易假设失效关系；"
            "FINRA、Investor.gov、IBKR 支撑 stop/stop-limit 的触发、非保证成交价、限价可能不成交和不同触发口径差异。"
        ),
        "patch_notes": {
            "source": [
                "保留 FINRA、Investor.gov、IBKR 作为 stop/stop-limit 触发和执行风险来源。",
            ],
            "content": [
                "不得回退为所有止损都必须绑定结构失效。",
                "正式 draft 应表述为止损规则必须记录风险目的、触发条件、执行假设，以及与交易假设失效的关系。",
            ],
            "boundary": [
                "若使用 stop、stop-limit 或 order-model 语义，必须声明 stop price、limit price、触发标准、跳空、滑点和未成交风险。",
                "不得输出具体止损价格、百分比或 R 参数。",
            ],
            "conflict": [
                "当前可见上下文内未发现可证冲突；进入 reviewed/caveat_only 前仍需完整 formal KB 冲突检查。",
            ],
        },
    },
    {
        "candidate_id": "cand_20260611_phase37_kline_strategy_take_profit_requires_reachability_check_001",
        "research_task_id": "P37-C-K05",
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": (
            "补证已把止盈可达性收窄为执行和成交质量假设披露，不再写成收益保证；"
            "CFA、QuantConnect 和 Investor.gov 支撑成本、market impact、fill model、slippage、未成交风险和 order-risk 边界。"
        ),
        "patch_notes": {
            "source": [
                "保留 CFA execution、QuantConnect fill/slippage 与 Investor.gov order-risk 来源作为执行边界证据。",
            ],
            "content": [
                "不得把可达性检查写成收益保证。",
                "正式 draft 应表述为止盈目标必须声明可达性和成交质量假设。",
            ],
            "boundary": [
                "图形目标或理想 R 倍数只能作为研究假设，不能直接写成可成交收益。",
                "不得输出止盈价格、R 倍数参数、挂单建议或实盘执行建议。",
            ],
            "conflict": [
                "当前可见上下文内未发现可证冲突；进入 reviewed/caveat_only 前仍需完整 formal KB 冲突检查。",
            ],
        },
    },
    {
        "candidate_id": "cand_20260611_phase37_kline_strategy_volume_confirmation_boundary_001",
        "research_task_id": "P37-C-K10",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": (
            "Databento OHLCV、trade resampling、official statistics 和 Binance Kline 字段来源已支撑 volume 字段口径、"
            "数据源、聚合规则、交易所/供应商语义、缺失区间和质量标志边界。"
        ),
        "patch_notes": {
            "source": [
                "保留 Databento OHLCV、Databento statistics、Binance Kline 作为成交量字段和聚合语义来源。",
            ],
            "content": [
                "volume confirmation 必须拆成数据语义边界与指标解释边界。",
                "不得把单一供应商或交易所 schema 泛化为所有市场。",
            ],
            "boundary": [
                "成交量确认不得作为独立买卖许可，也不得证明突破、反转或方向预测有效。",
            ],
            "conflict": [
                "当前可见上下文内未发现可证冲突；进入 reviewed/caveat_only 前仍需完整 formal KB 冲突检查。",
            ],
        },
    },
    {
        "candidate_id": "cand_20260611_phase37_kline_strategy_strategy_rule_version_required_001",
        "research_task_id": "P37-C-K12",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": (
            "MLflow Tracking、MLflow Dataset Tracking 和 DVC pipeline 来源补上参数、代码版本、数据版本、输出文件、lineage "
            "和可复现工作流证据；White Reality Check 只作为多次规则搜索和数据复用风险来源。"
        ),
        "patch_notes": {
            "source": [
                "保留 MLflow、DVC、White Reality Check 的来源分工：前两者支撑版本追踪，White 支撑规则搜索/数据复用风险。",
            ],
            "content": [
                "strategy_rule_version、参数、代码版本、信号计算版本、数据版本、评估输出和变更原因应写成 CEK-TA 策略规则复现/审计契约字段。",
            ],
            "boundary": [
                "MLflow、DVC、Git 只能作为等价实现来源，不得被强制为唯一工具。",
                "不得把版本契约写成外部法规或所有平台强制实现。",
            ],
            "conflict": [
                "当前可见上下文内未发现可证冲突；进入 reviewed/caveat_only 前仍需完整 formal KB 冲突检查。",
            ],
        },
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


def candidate_path(candidate_id: str) -> Path:
    return CANDIDATE_DIR / f"{candidate_id}.json"


def flatten_patch_notes(groups: dict[str, list[str]]) -> list[str]:
    flattened: list[str] = []
    for group_name in ("source", "content", "boundary", "conflict"):
        for note in groups.get(group_name, []):
            flattened.append(f"{group_name}: {note}")
    return flattened


def append_unique_strings(existing: Any, additions: list[str]) -> list[str]:
    values = [str(item) for item in existing if isinstance(item, str)] if isinstance(existing, list) else []
    for addition in additions:
        if addition not in values:
            values.append(addition)
    return values


def build_audit_archive() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "auditor": "external_ai_strict_reaudit",
        "audited_at": TODAY,
        "scope": "Phase 37 Kline / Strategy Engineering supplemental re-audit for P37-C-K04/K05/K10/K12",
        "summary": {
            "total": 4,
            "accepted_for_draft": 4,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "quality_gate": {
            "pass": True,
            "reason": "4/4 supplemental Kline candidates accepted_for_draft; all reviewed/approved/default/hard gate permissions remain false.",
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "candidate_only": True,
            "trade_instruction_allowed": False,
        },
        "results": [
            {
                **result,
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
            for result in RESULTS
        ],
        "source_urls_referenced_by_auditor": [
            "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-15",
            "https://www.finra.org/investors/insights/stop-orders-factors-consider-during-volatile-markets",
            "https://www.interactivebrokers.com/campus/glossary-terms/stop-order/",
            "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
            "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
            "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts",
            "https://databento.com/docs/schemas-and-data-formats/ohlcv",
            "https://databento.com/docs/schemas-and-data-formats/statistics",
            "https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints",
            "https://mlflow.org/docs/latest/ml/tracking/",
            "https://mlflow.org/docs/latest/ml/dataset/",
            "https://doc.dvc.org/start/data-pipelines/data-pipelines",
        ],
    }


def patch_candidate(payload: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    decision = str(result["decision"])
    patch_note_groups = result["patch_notes"]
    flat_patch_notes = flatten_patch_notes(patch_note_groups)

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
        "auditor": "external_ai_strict_reaudit",
        "audited_at": TODAY,
        "decision": decision,
        "confidence": result["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reason": result["reason"],
        "patch_notes": flat_patch_notes,
        "patch_note_groups": patch_note_groups,
        "boundary": "accepted_for_draft is not reviewed or approved; this re-audit does not allow default guidance or hard gate.",
    }
    review["open_questions"] = append_unique_strings(
        review.get("open_questions", []),
        ["进入 reviewed/caveat_only 前仍需完整 formal KB 冲突、重复和 owner 边界检查。"],
    )

    claim = payload.setdefault("claim", {})
    existing_notes = str(claim.get("interpretation_notes", ""))
    patch_text = " 二审补丁：" + "；".join(flat_patch_notes)
    if patch_text not in existing_notes:
        claim["interpretation_notes"] = (existing_notes + patch_text).strip()

    source_quality = payload.setdefault("source_quality", {})
    source_quality["limitations"] = append_unique_strings(source_quality.get("limitations", []), flat_patch_notes)

    conflict = payload.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "visible_context_no_conflict"
    conflict["resolution_summary"] = (
        "二审允许 accepted_for_draft；进入 formal reviewed/caveat_only 前仍需完整 formal KB 冲突、重复和 owner 边界检查。"
    )
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False

    status["review_status"] = "accepted"
    status["ingestion_decision"] = decision
    status["updated_at"] = TODAY
    status["decision_reason"] = f"Phase 37 Kline / Strategy Engineering 二审结论为 {decision}；不得 reviewed/approved/default guidance/hard gate。"

    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["next_action"] = "export_reviewed_preparation_audit_package"
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["formalization_allowed"] = False

    machine_gate = payload.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Supplemental re-audit only allows accepted_for_draft; formal reviewed/default guidance/hard gate remain blocked."
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False

    conversion = workflow.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_reaudit",
            "action": "phase37_kline_strategy_supplemental_reaudit_imported",
            "reason": f"{decision} / confidence={result['confidence']}",
            "audit_result_id": AUDIT_RESULT_ID,
            "patch_notes": flat_patch_notes,
        }
    )
    return payload


def validate_candidates() -> list[str]:
    errors: list[str] = []
    for result in RESULTS:
        path = candidate_path(result["candidate_id"])
        if not path.exists():
            errors.append(f"missing candidate: {result['candidate_id']}")
            continue
        payload = read_json(path)
        if payload.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            errors.append(f"{result['candidate_id']}: ingestion_decision is not accepted_for_draft")
        if payload.get("machine_gate", {}).get("default_guidance") != "deny":
            errors.append(f"{result['candidate_id']}: default guidance must stay denied")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if payload.get("machine_gate", {}).get(field) is not False:
                errors.append(f"{result['candidate_id']}: machine_gate.{field} must be false")
        if payload.get("workflow", {}).get("formalization_allowed") is not False:
            errors.append(f"{result['candidate_id']}: formalization_allowed must be false")
    return errors


def main() -> None:
    archive = build_audit_archive()
    write_json(AUDIT_ARCHIVE, archive)

    for result in RESULTS:
        path = candidate_path(result["candidate_id"])
        payload = read_json(path)
        patched = patch_candidate(payload, result)
        write_json(path, patched)

    errors = validate_candidates()
    report = {
        "report_id": "phase37_kline_strategy_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-398",
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "summary": archive["summary"],
        "candidate_ids": [result["candidate_id"] for result in RESULTS],
        "quality_gate": {"pass": not errors, "errors": errors},
        "archive_path": str(AUDIT_ARCHIVE),
        "boundary": "Candidates were marked accepted_for_draft only; no formal reviewed/approved/default guidance/hard gate was created.",
    }
    write_json(REPORT_PATH, report)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"imported": len(RESULTS), "accepted_for_draft": 4, "report": str(REPORT_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
