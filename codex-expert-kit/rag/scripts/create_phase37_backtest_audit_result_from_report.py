"""Create Phase 37 Backtest first audit JSON from the reviewed report.

This script exists to avoid PowerShell console encoding corruption when writing
Chinese audit text. It writes UTF-8 JSON artifacts only.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
PARTITION = "KB_04_BACKTEST"
PACKAGE_ID = "phase37_backtest_candidate_audit_package_20260611"
AUDIT_RESULT_ID = "audit_result_phase37_backtest_candidate_audit_20260611_strict_v1"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
NO_SUPPLEMENT_REPORT = resolve_repo_path(
    "docs", "reports", "phase37_backtest_no_supplement_needed_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


GLOBAL_PATCH = {
    "source": [
        "平台文档只能作为实现语义示例，不得泛化为所有 backtest engine。",
        "B03 需补 survivorship bias / delisted assets / historical universe / contract expiry-rollover 的直接来源。",
        "B10 需补 profit factor、drawdown、收益回撤比的专业定义和局限来源。",
        "B11/B12 需补 CEK-TA backtest_run_manifest 或 reproducibility_package schema。",
    ],
    "content": [
        "把 block/阻断改写为 evidence invalidation：该回测不得作为策略有效性证据。",
        "所有回测结论必须声明数据版本、策略版本、参数、成本、滑点、fill model、样本划分和评估时间。",
        "gross result、net result、research result、validation result 必须分开。",
    ],
    "boundary": [
        "不得创建 reviewed、approved、default guidance 或 hard gate。",
        "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
        "样本外、walk-forward 或成本建模通过，也不等于实盘许可。",
    ],
    "conflict": [
        "与 Quant Foundation、Data Engineering、Market Microstructure、Replay、Live Execution、Risk Management、AI Engineering 只做引用和 owner 边界拆分。"
    ],
}


ITEMS = {
    "P37-E-B07": (
        "cand_20260611_phase37_backtest_cost_model_required_001",
        "high",
        "成本模型边界成立；CFA execution/TCA 与 QuantConnect fee/slippage/fill 文档支持交易成本、market impact、opportunity cost、费用、滑点和成交模型语义。",
    ),
    "P37-E-B02": (
        "cand_20260611_phase37_backtest_data_leakage_block_001",
        "high",
        "数据泄漏不得进入特征或规则选择流程；该结果不得作为有效性证据，但不得解释为 hard gate。",
    ),
    "P37-E-B01": (
        "cand_20260611_phase37_backtest_lookahead_bias_block_001",
        "high",
        "lookahead bias 破坏 decision_time 可见性；回测结果不能作为策略有效性证据。",
    ),
    "P37-E-B09": (
        "cand_20260611_phase37_backtest_metric_interpretation_boundary_001",
        "high",
        "Sharpe、Sortino、profit factor、win rate、drawdown、turnover 等指标必须结合成本、样本、交易次数、尾部风险、非正态与选择偏差解释。",
    ),
    "P37-E-B06": (
        "cand_20260611_phase37_backtest_out_of_sample_required_001",
        "high",
        "样本内表现不能单独证明策略有效性；样本外、时间后推或独立周期验证边界成立。",
    ),
    "P37-E-B04": (
        "cand_20260611_phase37_backtest_parameter_search_separate_from_final_eval_001",
        "high",
        "参数搜索、特征选择、模型选择与最终评估样本必须分离，避免 data snooping / multiple testing 风险。",
    ),
    "P37-E-B10": (
        "cand_20260611_phase37_backtest_profit_factor_drawdown_context_required_001",
        "medium",
        "profit factor 不能单独证明策略质量成立；reviewed 前必须补 profit factor、drawdown 和收益回撤比的专业定义与局限来源。",
    ),
    "P37-E-B11": (
        "cand_20260611_phase37_backtest_reproducibility_package_required_001",
        "medium",
        "MLflow/DVC 支撑实验参数、代码版本、指标、artifact、pipeline stage、依赖和输出追踪；reviewed 前需要 CEK-TA backtest package schema 补强。",
    ),
    "P37-E-B08": (
        "cand_20260611_phase37_backtest_slippage_fee_spread_required_001",
        "high",
        "fill price、slippage、fee、spread、partial fill 和 order type 假设必须声明。",
    ),
    "P37-E-B12": (
        "cand_20260611_phase37_backtest_strategy_version_and_data_version_required_001",
        "medium",
        "MLflow/DVC 支撑参数、代码、artifact、数据/模型版本和 pipeline tracking；CEK-TA 专用版本字段 reviewed 前需 schema 补强。",
    ),
    "P37-E-B03": (
        "cand_20260611_phase37_backtest_survivorship_selection_bias_check_001",
        "medium",
        "选择偏差由 White/DSR/STW 支撑；reviewed 前需要幸存者偏差、退市资产、过期合约和 historical universe 直接来源。",
    ),
    "P37-E-B05": (
        "cand_20260611_phase37_backtest_walk_forward_validation_required_001",
        "high",
        "CFA rolling-window backtesting、Bailey PBO、White data snooping 和 metadata 来源支持训练窗口、验证窗口、步长、重优化频率、参数冻结点和数据可用时间边界。",
    ),
}


WEAK_FOLLOWUPS = {
    "P37-E-B01": ["reviewed 前补 point-in-time / available_time / bar availability 来源。"],
    "P37-E-B03": ["reviewed 前补 survivorship bias / delisted assets / historical universe / contract expiry-rollover 的直接来源。"],
    "P37-E-B10": ["reviewed 前补 profit factor、drawdown、收益回撤比的专业定义和局限来源。"],
    "P37-E-B11": ["reviewed 前补 CEK-TA backtest_run_manifest 或 reproducibility_package schema。"],
    "P37-E-B12": ["reviewed 前补 CEK-TA strategy_rule_version / calendar_session_version / cost_fill_model_version schema。"],
}


def build_result(task_id: str, candidate_id: str, confidence: str, reason: str) -> dict[str, Any]:
    candidate = read_json(CAND_DIR / f"{candidate_id}.json")
    followups = WEAK_FOLLOWUPS.get(task_id, [])
    patch = {key: list(value) for key, value in GLOBAL_PATCH.items()}
    if task_id in {"P37-E-B01", "P37-E-B02"}:
        patch["content"].append("B01/B02 的 block/阻断只能表示证据失效，不得被机器消费为 hard gate。")
    return {
        "candidate_id": candidate_id,
        "research_task_id": task_id,
        "decision": "accepted_for_draft",
        "confidence": confidence,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": [reason],
        "required_followups": followups,
        "patch_notes": patch,
        "source_assessment": {
            "source_count": len(candidate.get("source_refs", [])),
            "missing_sources": followups,
            "weak_sources": ["平台/框架文档只能作为实现示例"]
            if task_id in {"P37-E-B07", "P37-E-B08", "P37-E-B11", "P37-E-B12"}
            else [],
            "recommended_extra_sources": followups,
        },
        "classification_assessment": {
            "correct_partition": True,
            "expected_partition": PARTITION,
            "correct_tree_node": candidate.get("classification", {}).get("canonical_node_id")
            == "kt.trading_engineering.backtest",
            "notes": "归类到 Trading Engineering / Backtest；其他分支只做引用和 owner 边界拆分。",
        },
        "boundary_assessment": {
            "no_trade_advice": True,
            "candidate_only": True,
            "requires_external_project_facts": True,
            "notes": "本轮不能 reviewed/approved/default/hard gate，也不能产生交易执行建议。",
        },
    }


def main() -> None:
    candidate_results = [
        build_result(task_id, candidate_id, confidence, reason)
        for task_id, (candidate_id, confidence, reason) in ITEMS.items()
    ]
    audit = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit_from_user_report",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "quality_gate": {
            "pass": True,
            "reason": "12 条 Backtest 候选严格审计均 accepted_for_draft；本轮不允许 reviewed/approved/default/hard gate。",
        },
        "summary": {
            "total": 12,
            "accepted_for_draft": 12,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "global_patch_notes": GLOBAL_PATCH,
        "candidate_results": candidate_results,
    }
    no_supplement = {
        "report_id": "phase37_backtest_no_supplement_needed_report",
        "generated_at": TODAY,
        "phase": "37",
        "partition_id": PARTITION,
        "source_report": "docs/reports/phase37_backtest_audit_import_report.json",
        "quality_gate": {
            "pass": True,
            "reason": "首轮严格审计中 needs_more_evidence/rejected/blocked 均为 0；CEK-TA-415 和 CEK-TA-416 无需执行补证与二审导入。",
        },
        "decision_counts": {
            "total": 12,
            "accepted_for_draft": 12,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "no_op_tasks": [
            {"task_id": "CEK-TA-415", "reason": "没有 needs_more_evidence 候选，补证脚本无需生成。"},
            {"task_id": "CEK-TA-416", "reason": "没有补证二审结果需要导入。"},
        ],
        "next_step": "进入 CEK-TA-417，导出 12 条 accepted_for_draft 候选的 reviewed/caveat_only 准备审计包。",
    }
    write_json(AUDIT_RESULT_PATH, audit)
    write_json(NO_SUPPLEMENT_REPORT, no_supplement)
    print(json.dumps({"audit_result": str(AUDIT_RESULT_PATH), "no_supplement": str(NO_SUPPLEMENT_REPORT)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
