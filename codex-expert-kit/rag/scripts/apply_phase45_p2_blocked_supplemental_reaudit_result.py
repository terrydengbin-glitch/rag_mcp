"""Import Phase 45 P2 blocked supplemental re-audit result.

This script materializes DATA04, CRYPTO03 and CRYPTO05 as formal
reviewed/caveat_only knowledge after the strict supplemental re-audit.

It never creates approved knowledge, default guidance, hard gates, legal
license conclusions, training license conclusions, risk thresholds,
liquidation-avoidance advice, or live trading actions.
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

import apply_phase45_p2_reviewed_preparation_result as p2_reviewed  # noqa: E402


TODAY = "2026-06-12"
TASK_ID = "CEK-TA-471"
AUDIT_RESULT_ID = "audit_phase45_p2_reviewed_blocked_supplemental_reaudit_20260612"
SOURCE_PACKAGE_ID = "phase45_p2_reviewed_blocked_supplemental_reaudit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path(
    "docs",
    "reports",
    "phase45_p2_reviewed_blocked_supplemental_import_report.json",
    start_file=__file__,
)


RESULTS: dict[str, dict[str, Any]] = {
    "P45-G-DATA04": {
        "candidate_id": "cand_20260612_phase45_reference_data_entitlement_p45_g_data04_001",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "trade_execution_advice_allowed": False,
        "legal_license_conclusion_allowed": False,
        "training_license_conclusion_allowed": False,
        "reasons": [
            "补证已加入 Databento Corporate Actions，直接支撑 corporate action、listed/delisted securities 与 coverage event 语境。",
            "补证已加入 Nasdaq Daily List / pending suspension delisting 来源，支撑 Nasdaq-specific delisting / symbol event 语境。",
            "原有 Databento Schemas、Databento Instrument Definitions、Nasdaq Symbol Directory、CME Product Slate 可继续支撑 dataset、schema、instrument universe、product coverage 与可用字段边界。",
            "claim 仅要求 dataset coverage / universe / missing interval / delisting / symbol change / filter rule 显式声明，未输出交易信号、训练授权结论或法律授权结论。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 Databento vendor-specific caveat。",
            "Nasdaq Daily List 只能支撑 Nasdaq-specific delisting / suspension 语境，其他 venue 需各自 source_ref。",
            "外接项目必须声明 dataset_coverage schema：coverage_start、coverage_end、missing_interval、filter_rule、field_availability、delisting_policy_ref、symbol_change_policy_ref。",
        ],
        "patch_notes": {
            "source": [
                "保留 Databento Schemas、Databento Instrument Definitions、Nasdaq Symbol Directory、CME Product Slate。",
                "新增并保留 Databento Corporate Actions。",
                "新增并保留 Nasdaq Daily List / pending suspension delisting 来源。",
            ],
            "content": [
                "DATA04 可作为 dataset coverage / universe declaration 的 reviewed/caveat_only 知识。",
                "不得把未声明覆盖范围的数据当成完整市场事实。",
                "delisting、symbol change、corporate action 只能作为必须声明的 coverage 维度，不是交易信号。",
            ],
            "boundary": [
                "不得生成交易信号。",
                "不得生成训练授权结论。",
                "不得生成法律授权结论。",
                "不得生成 hard gate。",
            ],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO03": {
        "candidate_id": "cand_20260612_phase45_crypto_perp_p45_h_crypto03_001",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "trade_execution_advice_allowed": False,
        "legal_license_conclusion_allowed": False,
        "training_license_conclusion_allowed": False,
        "reasons": [
            "补证已加入 Binance Futures Leverage & Margin，支撑 Binance-specific leverage / margin bracket / margin context。",
            "补证已加入 Bybit Risk Limit，支撑 position tier、risk limit tier、maintenance margin requirement 与 liquidation-risk context。",
            "外部复核来源显示 Bybit liquidation process 使用 laddered approach 调整 maintenance margin requirement，足以支撑 partial / staged liquidation 语境。",
            "claim 明确 liquidation price、bankruptcy price、maintenance margin、margin mode、partial liquidation 必须分字段建模，并禁止把清算价等同普通止损。",
            "claim 未输出仓位、杠杆、止损止盈、清算规避或实盘执行建议。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 Binance-specific 与 Bybit-specific caveat。",
            "maintenance_margin_source_ref、margin_mode、liquidation_price、bankruptcy_price、partial_liquidation_ref 必须来自外接项目事实层或对应 venue rulebook/API。",
            "不得将 maintenance margin tier 或 risk limit tier 转换为 CEK-TA 风险阈值或 hard gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 Binance liquidation、Binance mark price、Bybit mark price 来源。",
                "新增并保留 Binance Futures Leverage & Margin。",
                "新增并保留 Bybit Risk Limit / maintenance margin / liquidation-risk 来源。",
            ],
            "content": [
                "CRYPTO03 可作为 maintenance margin / liquidation boundary 的 reviewed/caveat_only 知识。",
                "liquidation price、bankruptcy price、maintenance margin、margin mode、partial liquidation 必须分字段。",
                "清算价不得等同普通止损。",
            ],
            "boundary": [
                "不得输出清算规避建议。",
                "不得输出仓位或杠杆建议。",
                "不得输出止损参数。",
                "不得生成 hard gate。",
            ],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO05": {
        "candidate_id": "cand_20260612_phase45_crypto_perp_p45_h_crypto05_001",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "trade_execution_advice_allowed": False,
        "legal_license_conclusion_allowed": False,
        "training_license_conclusion_allowed": False,
        "reasons": [
            "补证已加入 OKX Status，支撑 exchange status / incident / maintenance 语境，但仅限 OKX-specific。",
            "补证已加入 Bybit Mark Price Calculation，直接支撑 index price abnormal、data unavailable 与 mark price fallback 处理语境。",
            "原有 Binance / Bybit WebSocket 文档支撑 API/WebSocket disconnect、heartbeat/ping-pong、连接有效期与限流风险。",
            "原有 Binance Maintenance Updates、Binance Mark Price API、Binance ADL、Binance Insurance Fund、Binance Aggregate Trade Streams 可继续支撑维护、mark/index monitoring、ADL / insurance-fund event 与 loss-allocation evidence boundary。",
            "claim 已将 clawback 收窄为 exchange-specific loss-allocation mechanism，未输出清算规避、仓位、杠杆、止损止盈、停机 hard gate、自动解锁或实盘执行建议。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 Binance / Bybit / OKX / Databento venue-specific caveat。",
            "OKX Status 不能泛化为 Binance / Bybit / 全市场 outage truth；其他 venue 需独立 status / incident source。",
            "Bybit mark/index abnormal handling 只能支撑 Bybit-specific fallback 语境，其他 venue 需各自 rulebook。",
            "如正式文本继续出现 clawback 字样，必须写成 exchange-specific loss-allocation mechanism，并要求对应 venue rulebook source_ref。",
        ],
        "patch_notes": {
            "source": [
                "保留 Databento Status、OKX Pre-market、Binance ADL、Binance Insurance Fund、Binance Aggregate Trade Streams。",
                "保留 Binance WebSocket、Bybit WebSocket、Binance Maintenance Updates、Binance Mark Price API。",
                "新增并保留 OKX Status。",
                "新增并保留 Bybit Mark Price abnormal / fallback 处理来源。",
                "新增并保留 Binance event-style volatility statement 作为事件案例辅助来源，不作为 standing status API。",
            ],
            "content": [
                "CRYPTO05 可作为 crypto venue outage / pre-market / loss-allocation risk 的 reviewed/caveat_only 知识。",
                "exchange maintenance / service interruption、api_ws_disconnect、heartbeat_ping_pong_failure、stream_rate_limit、mark_index_monitoring、pre_market_rule、adl_insurance_event、loss_allocation_mechanism 必须分字段建模。",
                "24/7 continuous trading 不得等同于无停机、无断连、无数据缺口或无交易所机制风险。",
            ],
            "boundary": [
                "不得输出清算规避建议。",
                "不得输出仓位、杠杆或止损止盈。",
                "不得生成停机 hard gate。",
                "不得生成自动解锁、自动撤单或强平处理动作。",
                "不得把 Binance / Bybit / OKX 规则泛化为所有 crypto venue。",
            ],
            "conflict": [],
        },
    },
}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def archive_audit_result() -> None:
    payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 3,
            "accepted_for_reviewed_caveat_only": 3,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": result["candidate_id"],
                "research_task_id": task_id,
                "decision": result["decision"],
                "confidence": result["confidence"],
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "trade_execution_advice_allowed": False,
                "legal_license_conclusion_allowed": False,
                "training_license_conclusion_allowed": False,
                "reasons": result["reasons"],
                "required_followups": result["required_followups"],
                "patch_notes": result["patch_notes"],
            }
            for task_id, result in RESULTS.items()
        ],
        "global_required_patches": [
            "formal reviewed 只能是 caveat_only，approved/default guidance/hard gate 必须保持 false。",
            "不得生成法律授权结论、训练授权结论、交易执行建议、仓位、杠杆、止损止盈、清算规避或风险阈值。",
        ],
    }
    write_json(AUDIT_ARCHIVE, payload)


def candidate_paths_by_task() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for path in p2_reviewed.candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        if task_id in RESULTS:
            paths[task_id] = path
    return paths


def process_candidates() -> dict[str, Any]:
    # Reuse the already-validated Phase 45 P2 formal item builder with the
    # current re-audit ids.
    p2_reviewed.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    p2_reviewed.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID

    archive_audit_result()
    formalized: list[dict[str, Any]] = []
    missing: list[str] = []
    paths = candidate_paths_by_task()

    for task_id, result in RESULTS.items():
        path = paths.get(task_id)
        if not path:
            missing.append(task_id)
            continue

        candidate = read_json(path)
        formal = p2_reviewed.build_formal_item(candidate, result)
        partition = str(candidate.get("classification", {}).get("partition_id"))
        formal_path = resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "knowledge",
            partition,
            p2_reviewed.sanitize_filename(formal["knowledge_id"]),
            start_file=__file__,
        )
        write_json(formal_path, formal)

        candidate.setdefault("status", {}).update(
            {
                "review_status": "formalized",
                "ingestion_decision": "formal_reviewed_created",
                "decision_reason": "补证复审通过，已创建 formal reviewed/caveat_only；不得 approved/default/hard gate。",
                "updated_at": TODAY,
            }
        )
        workflow = candidate.setdefault("workflow", {})
        workflow.update(
            {
                "stage": "formalized_reviewed",
                "queue_group": "formalized",
                "formal_knowledge_id": formal["knowledge_id"],
                "formal_review_status": "reviewed",
                "formal_knowledge_path": repo_relative(formal_path),
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "trade_execution_advice_allowed": False,
                "legal_license_conclusion_allowed": False,
                "training_license_conclusion_allowed": False,
                "next_action": "none",
            }
        )

        review = candidate.setdefault("review", {})
        review["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": SOURCE_PACKAGE_ID,
            "decision": "accepted_for_reviewed_caveat_only",
            "confidence": result["confidence"],
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "training_license_conclusion_allowed": False,
            "reasons": result["reasons"],
            "required_followups": result["required_followups"],
            "patch_notes": result["patch_notes"],
        }
        review.setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_p2_reviewed_blocked_supplemental_imported",
                "reason": f"{task_id} accepted_for_reviewed_caveat_only / confidence={result['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        candidate.setdefault("claim", {})["audit_patch_notes"] = result["patch_notes"]
        write_json(path, candidate)

        formalized.append(
            {
                "research_task_id": task_id,
                "candidate_id": candidate.get("candidate_id"),
                "knowledge_id": formal["knowledge_id"],
                "formal_path": repo_relative(formal_path),
            }
        )

    return {"formalized": formalized, "missing": missing}


def main() -> int:
    result = process_candidates()
    report = {
        "report_id": "phase45_p2_reviewed_blocked_supplemental_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "formal_reviewed_created": len(result["formalized"]),
        "formalized": result["formalized"],
        "missing": result["missing"],
        "p2_formal_reviewed_total_after_import": 11,
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "risk_threshold_advice_enabled": False,
        "legal_license_conclusion_enabled": False,
        "training_license_conclusion_enabled": False,
        "trade_execution_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not result["missing"] and len(result["formalized"]) == 3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
