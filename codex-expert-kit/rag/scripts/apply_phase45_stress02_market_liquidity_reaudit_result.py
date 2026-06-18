"""Apply Phase 45 STRESS02 market-liquidity re-audit result.

This consumes the strict single-candidate re-audit for P45-E-STRESS02 and
materializes it as formal reviewed/caveat_only knowledge.

It never creates approved knowledge, default guidance, hard gates, risk
thresholds, liquidation-horizon values, executable sizing, or live trading
actions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from path_resolver import resolve_repo_path  # noqa: E402
from apply_phase45_stress_scenario_reviewed_preparation_result import (  # noqa: E402
    PARTITION,
    TODAY,
    build_formal_item,
    repo_relative,
    sanitize_filename,
)


TASK_ID = "CEK-TA-466"
AUDIT_RESULT_ID = "audit_phase45_stress02_market_liquidity_reaudit_20260612"
SOURCE_PACKAGE_ID = "phase45_stress_scenario_stress02_market_liquidity_reaudit_package_20260612"
RESEARCH_TASK_ID = "P45-E-STRESS02"
AUDIT_RESULT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_stress02_market_liquidity_reaudit_import_report.json", start_file=__file__
)
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    PARTITION,
    "cand_20260612_phase45_stress_scenario_liquidity_stress_boundary_001.json",
    start_file=__file__,
)


RESULT: dict[str, Any] = {
    "research_task_id": RESEARCH_TASK_ID,
    "decision": "accepted_for_reviewed_caveat_only",
    "confidence": "high",
    "reviewed_allowed": True,
    "reasons": [
        "上轮缺口已补齐：PFMI、CPMI-IOSCO CCP resilience、CME Clearing Liquidity Risk Management、DTCC Stress Testing 被正确限定为 clearing/funding liquidity 来源。",
        "ESMA LST Guidelines 可支撑 liquidation cost、time to liquidity/time to liquidation、trade/order size、stressed market liquidity、higher bid-ask spread、lower liquidity 和 longer time to liquidate 等 market/asset liquidity stress 维度。",
        "SEC/eCFR Rule 22e-4 可支撑 liquidity risk management、liquidity classification、time-to-convert/sell/dispose-of 和治理/记录保存语境，但需保留 open-end fund / ETF caveat。",
        "CFA Institute 可支撑 bid-ask spread、order book depth、market impact 作为 market/execution liquidity 维度。",
        "NY Fed Treasury market depth 研究可支撑 market depth 作为独立 order-book liquidity 维度。",
        "claim 已明确缺失 market_depth_source_id、spread_source_id、market_impact_source_id 或 time_to_liquidate_source_id 时必须标记 unknown，不得当作 normal、zero、safe 或可成交性证明。",
        "claim 未输出可成交数量、滑点阈值、清仓时长数值、风险阈值、交易许可、仓位建议或 hard gate。",
    ],
    "required_followups": [
        "正式 reviewed/caveat_only 文本必须保留 PFMI/CCP/CME/DTCC 是 clearing、funding、FMI、CCP 或 clearing-agency 语境。",
        "正式文本必须保留 ESMA LST 是 UCITS/AIF fund liquidity stress testing 语境。",
        "正式文本必须保留 SEC Rule 22e-4 是美国 open-end fund / ETF liquidity risk management 语境。",
        "正式文本必须保留 CFA Institute 来源主要是 equity market liquidity 语境。",
        "正式文本必须保留 NY Fed 来源主要是 U.S. Treasury order-book depth 研究语境。",
        "外接项目缺失 market_depth_source_id、spread_source_id、market_impact_source_id 或 time_to_liquidate_source_id 时，必须标记 unknown，不得默认 safe。",
        "如后续进入 approved 或 hard gate，必须另开任务；本条不得直接升级。",
    ],
    "patch_notes": {
        "source": [
            "保留 PFMI、CPMI-IOSCO CCP resilience、CME Clearing Liquidity Risk Management、DTCC Stress Testing 作为 clearing/funding liquidity 来源。",
            "新增并保留 ESMA LST Guidelines、SEC/eCFR Rule 22e-4、CFA Institute Liquidity in Equity Markets、NY Fed Measuring Treasury Market Depth 作为 market/execution liquidity 来源。",
            "不得把任一来源解释为所有市场、所有资产、所有账户模式的统一流动性阈值来源。",
        ],
        "content": [
            "保留 clearing/funding liquidity 与 market/execution liquidity 分层。",
            "保留 market depth、bid-ask spread、market impact、trade/order size、liquidation cost、time-to-liquidate 作为 reviewed/caveat_only 的审计维度。",
            "保留 unknown_component_policy：缺失来源必须标记 unknown_not_zero / unknown_not_safe。",
        ],
        "boundary": [
            "不得输出可成交数量。",
            "不得输出滑点阈值。",
            "不得输出 liquidation horizon 或 time-to-liquidate 数值。",
            "不得输出风险阈值。",
            "不得生成交易许可。",
            "不得生成仓位建议。",
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


def audit_result_payload(candidate_id: str) -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 1,
            "accepted_for_reviewed_caveat_only": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": candidate_id,
                "research_task_id": RESEARCH_TASK_ID,
                "decision": RESULT["decision"],
                "confidence": RESULT["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": RESULT["reasons"],
                "required_followups": RESULT["required_followups"],
                "patch_notes": RESULT["patch_notes"],
            }
        ],
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "liquidation_horizon_advice_allowed": False,
            "trade_execution_advice_allowed": False,
        },
    }


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    if candidate.get("research_task_id") != RESEARCH_TASK_ID:
        raise ValueError(f"Unexpected candidate task id: {candidate.get('research_task_id')}")

    write_json(AUDIT_RESULT_ARCHIVE, audit_result_payload(str(candidate.get("candidate_id"))))

    formal_item = build_formal_item(candidate, RESULT)
    # Preserve STRESS02-specific source grouping and unknown-component boundary
    # in the formal knowledge body.
    formal_item["content"]["procedure"].insert(
        1,
        "若是 liquidity stress，必须先区分 clearing/funding liquidity 与 market/execution liquidity，再检查 market_depth_source_id、spread_source_id、market_impact_source_id、time_to_liquidate_source_id 是否存在。",
    )
    formal_item["content"]["anti_patterns"].append(
        "缺失 market depth、spread、market impact 或 time-to-liquidate 来源时，把流动性状态写成 normal、zero、safe 或可成交性证明。"
    )
    formal_item["content"]["validation"].append(
        "STRESS02 必须保留 clearing_funding_liquidity 与 market_execution_liquidity source_groups；缺失来源必须标记 unknown_not_zero / unknown_not_safe。"
    )
    formal_item["source_quality"] = candidate.get("source_quality", {})
    formal_item["review"]["ai_audit"]["audit_result_id"] = AUDIT_RESULT_ID
    formal_item["review"]["ai_audit"]["package_id"] = SOURCE_PACKAGE_ID

    knowledge_dir = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION, start_file=__file__)
    formal_path = knowledge_dir / sanitize_filename(formal_item["knowledge_id"])
    write_json(formal_path, formal_item)

    candidate["status"]["review_status"] = "formalized"
    candidate["status"]["ingestion_decision"] = "formal_reviewed_created"
    candidate["status"]["decision_reason"] = "STRESS02 market/execution liquidity 再审通过，已创建 formal reviewed/caveat_only。"
    candidate["status"]["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "formalized_reviewed"
    workflow["queue_group"] = "formalized"
    workflow["formal_knowledge_id"] = formal_item["knowledge_id"]
    workflow["formal_review_status"] = "reviewed"
    workflow["formal_knowledge_path"] = repo_relative(formal_path)
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["risk_threshold_advice_allowed"] = False
    candidate.setdefault("review", {})["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": RESULT["confidence"],
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "required_followups": RESULT["required_followups"],
        "patch_notes": RESULT["patch_notes"],
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase45_stress02_market_liquidity_formal_reviewed_created",
            "reason": "STRESS02 re-audit accepted_for_reviewed_caveat_only; created formal reviewed/caveat_only.",
            "audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": formal_item["knowledge_id"],
        }
    )
    write_json(CANDIDATE_PATH, candidate)

    report = {
        "report_id": "phase45_stress02_market_liquidity_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "promoted_count": 1,
        "promoted": [
            {
                "research_task_id": RESEARCH_TASK_ID,
                "candidate_id": candidate.get("candidate_id"),
                "knowledge_id": formal_item["knowledge_id"],
                "formal_path": repo_relative(formal_path),
            }
        ],
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
        "liquidation_horizon_advice_enabled": False,
        "trade_execution_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps({"promoted_count": 1, "knowledge_id": formal_item["knowledge_id"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
