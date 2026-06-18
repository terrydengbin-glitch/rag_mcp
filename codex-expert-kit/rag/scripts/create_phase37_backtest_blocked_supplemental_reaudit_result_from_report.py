"""Create Phase 37 Backtest B10/B11/B12 supplemental reaudit JSON.

The user supplied a strict reaudit report in Markdown. This script writes a
machine-readable UTF-8 JSON result so later import logic does not depend on
PowerShell console encoding.
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
AUDIT_RESULT_ID = "audit_result_phase37_backtest_reviewed_blocked_supplemental_reaudit_20260611_strict_v1"
PACKAGE_ID = "phase37_backtest_reviewed_blocked_supplemental_reaudit_package_20260611"
OUT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    audit = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "auditor": "external_ai_strict_reaudit_from_user_report",
        "audited_at": TODAY,
        "quality_gate": {
            "pass": False,
            "reason": "B10 可以进入 reviewed/caveat_only；B11/B12 仍需内联完整 contract 正文、schema extract、字段表、版本或 hash。",
        },
        "summary": {
            "total": 3,
            "accepted_for_reviewed_caveat_only": 1,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "candidate_results": [
            {
                "candidate_id": "cand_20260611_phase37_backtest_profit_factor_drawdown_context_required_001",
                "research_task_id": "P37-E-B10",
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": "medium_high",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [
                    "B10 的 claim 是方法边界：profit factor / return-drawdown 类指标不能单独证明策略质量，必须结合 drawdown、交易次数、样本覆盖、成本、尾部亏损和参数选择过程。",
                    "CFA backtesting、Deflated Sharpe Ratio、White data snooping、QuantConnect backtest statistics/reporting 和新增 profit factor supporting source 共同支撑 reviewed/caveat_only。",
                ],
                "required_followups": [
                    "formal import 中 TitanFX 或类似券商/教育 glossary 只能作为 supporting source，不得单独作为 reviewed 主来源。",
                    "如 formal item 使用 CEK-TA exact metric_report field names，应补 contract 正文或 hash；本条当前只允许 caveat_only。",
                ],
                "patch_notes": {
                    "source": [
                        "QuantConnect backtest results/reporting 支撑 backtest 输出需要 equity curve、trades、logs、performance statistics 等上下文。",
                        "TitanFX profit factor 或同类券商/教育 glossary 只能作为 supporting source。",
                    ],
                    "content": [
                        "profit factor、drawdown、return/drawdown 类指标不得单独证明策略质量。",
                        "指标解释必须绑定样本、交易次数、成本、尾部亏损、参数选择过程和 gross/net 口径。",
                    ],
                    "boundary": [
                        "reviewed/caveat_only 不等于 approved、default guidance 或 hard gate。",
                        "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
                    ],
                    "conflict": [
                        "与 Quant Foundation、Data Engineering、Market Microstructure、Replay、Live Execution、Risk Management、AI Engineering 仅做 cross-reference 和 owner 边界拆分。"
                    ],
                },
            },
            {
                "candidate_id": "cand_20260611_phase37_backtest_reproducibility_package_required_001",
                "research_task_id": "P37-E-B11",
                "decision": "needs_more_evidence",
                "confidence": "high",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [
                    "MLflow/DVC 可以支持实验追踪和复现工作流，但 B11 的 claim 要求 CEK-TA reproducibility_package 字段本体。",
                    "当前包只提供 contract path、key_sections 和 summary，没有内联完整 contract 或 schema extract。"
                ],
                "required_followups": [
                    "上传或内联 phase37_backtest_run_manifest_contract.md 正文。",
                    "提供 reproducibility_package 字段表、required/optional 标记、字段语义、版本或 hash。",
                    "明确 code_commit、dependency_lockfile、config_hash、random_seed、environment、input_artifacts、output_artifacts、logs、lineage_id、replay_job_id 等字段。"
                ],
                "patch_notes": {
                    "source": [
                        "内部契约型来源必须至少提供正文、schema extract、字段表或可校验 hash。",
                        "MLflow/DVC 只能作为实现语义示例，不能替代 CEK-TA 字段契约。"
                    ],
                    "content": [
                        "区分 MLflow/DVC 可支持的实验追踪能力与 CEK-TA 内部字段契约。"
                    ],
                    "boundary": [
                        "继续阻断 reviewed/caveat_only；不得 approved/default/hard gate。"
                    ],
                    "conflict": [
                        "B11 字段本体需与 Data Engineering lineage、AI training dataset lineage 和 Backtest run manifest owner 边界对齐。"
                    ],
                },
            },
            {
                "candidate_id": "cand_20260611_phase37_backtest_strategy_version_and_data_version_required_001",
                "research_task_id": "P37-E-B12",
                "decision": "needs_more_evidence",
                "confidence": "high",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [
                    "MLflow Tracking / Dataset Tracking / Model Registry 可以支持参数、指标、artifact、dataset、model version、run linkage、lineage 和 rollback 语义。",
                    "B12 的核心是 CEK-TA 专用字段，当前包没有内联完整 schema 正文。"
                ],
                "required_followups": [
                    "上传或内联 strategy_identity / data_identity / market_calendar_identity / execution_assumption_identity 章节。",
                    "提供字段类型、语义、生成规则、校验规则和 schema version/hash。",
                    "说明 strategy_rule_version、parameter_hash、data_version、calendar/session version、cost/fill model version、evaluation timestamp 如何生成、保存和验证。",
                    "说明它们如何映射到 Data Engineering、Market Microstructure、Replay 和 Execution owner 字段。"
                ],
                "patch_notes": {
                    "source": [
                        "内部契约型来源必须提供完整 schema 正文或 schema extract。",
                        "MLflow/DVC 只能作为版本追踪类实现示例。"
                    ],
                    "content": [
                        "B12 应以内联 CEK-TA strategy/data/calendar/execution assumption 字段契约作为字段本体主证据。"
                    ],
                    "boundary": [
                        "继续阻断 reviewed/caveat_only；不得 approved/default/hard gate。"
                    ],
                    "conflict": [
                        "字段映射必须与 Data Engineering、Market Microstructure、Replay 和 Live Execution owner 边界对齐。"
                    ],
                },
            },
        ],
    }
    write_json(OUT_PATH, audit)
    print(json.dumps({"audit_result": str(OUT_PATH), "summary": audit["summary"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
