"""Supplement Phase 37 Kline / Strategy Engineering needs-more-evidence candidates.

This script patches four candidate artifacts and exports a supplemental
re-audit package. It does not create formal reviewed knowledge, approved
knowledge, default guidance, or hard gates.
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
PHASE = "37"
TASK_ID = "CEK-TA-397"
PARTITION = "KB_02_KLINE_STRATEGY"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase37_kline_strategy_supplemental_research.md", start_file=__file__)
AUDIT_PACKAGE = resolve_repo_path("docs", "audit", "phase37_kline_strategy_supplemental_reaudit_package_20260611.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_kline_strategy_supplemental_reaudit_report.json", start_file=__file__)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "finra_stop_orders": {
        "source_title": "Stop Orders: Factors to Consider During Volatile Markets",
        "source_url": "https://www.finra.org/investors/insights/stop-orders-factors-consider-during-volatile-markets",
        "source_type": "regulator_guidance",
        "publisher": "FINRA",
        "published_at": None,
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA explains stop orders and stop-limit orders, including that stop-limit orders may not execute and that volatile markets require careful consideration.",
        "limitations": ["Equity-investor guidance; use for order behavior and execution risk, not for K-line stop placement alpha."],
    },
    "investor_gov_stop_orders": {
        "source_title": "Investor Bulletin: Stop, Stop-Limit, and Trailing Stop Orders",
        "source_url": "https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-15",
        "source_type": "regulator_guidance",
        "publisher": "SEC Investor.gov",
        "published_at": "2017-07-13",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "Investor.gov states that stop prices are not guaranteed execution prices and stop-limit orders may not execute if price moves away.",
        "limitations": ["Investor education source; supports execution caveats but not structural invalidation methods."],
    },
    "ibkr_stop_order": {
        "source_title": "Stop Order",
        "source_url": "https://www.interactivebrokers.com/campus/glossary-terms/stop-order/",
        "source_type": "broker_official_doc",
        "publisher": "Interactive Brokers",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Interactive Brokers defines stop orders as market orders triggered by a stop price and notes that a specific execution price is not guaranteed.",
        "limitations": ["Broker-specific order documentation; external projects must map their own broker/exchange order rules."],
    },
    "cfa_trade_execution": {
        "source_title": "Trade Strategy and Execution",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
        "source_type": "professional_body_reference",
        "publisher": "CFA Institute",
        "published_at": "2026",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute discusses trade cost analysis, market impact, execution risk, trading policy documents, and execution-quality improvement.",
        "limitations": ["Professional execution reference; does not define CEK-TA strategy-rule schema fields."],
    },
    "quantconnect_trade_fills": {
        "source_title": "Trade Fills - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
        "source_type": "trading_engine_official_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect states that fill models determine fill price and quantity, incorporate spread costs, and work with slippage models.",
        "limitations": ["LEAN-specific simulation model; use as engineering evidence for fill assumptions, not live execution guarantees."],
    },
    "quantconnect_slippage": {
        "source_title": "Slippage models - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts",
        "source_type": "trading_engine_official_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect defines slippage as the difference between expected and actual fill price and models it to make backtests more realistic.",
        "limitations": ["Backtesting-platform source; project-specific live slippage must be measured independently."],
    },
    "databento_ohlcv": {
        "source_title": "Aggregate bars (OHLCV)",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/ohlcv",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento defines OHLCV aggregate bars as prices and total volume aggregated from trades over intervals.",
        "limitations": ["Vendor-specific schema convention; use as one concrete volume semantic source."],
    },
    "databento_custom_ohlcv": {
        "source_title": "Resampling trades data at a fixed interval",
        "source_url": "https://databento.com/docs/examples/basics-historical/custom-ohlcv",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento explains OHLCV schemas are derived from trades and demonstrates constructing bars by resampling trade data.",
        "limitations": ["Example documentation; still requires provider-specific aggregation and no-trade interval policy."],
    },
    "databento_statistics": {
        "source_title": "Statistics schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/statistics",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento distinguishes official venue summary statistics from Databento-computed OHLCV bars, including volume fields.",
        "limitations": ["Vendor/platform-specific distinction; supports source-semantic boundary only."],
    },
    "binance_klines": {
        "source_title": "Kline/Candlestick Data",
        "source_url": "https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints",
        "source_type": "exchange_official_doc",
        "publisher": "Binance",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "Binance spot Kline data includes volume, quote asset volume, number of trades, taker buy base volume and taker buy quote volume.",
        "limitations": ["Crypto spot exchange schema; not universal for equities, futures, or aggregated vendor feeds."],
    },
    "mlflow_tracking": {
        "source_title": "ML Experiment Tracking",
        "source_url": "https://mlflow.org/docs/latest/ml/tracking/",
        "source_type": "mlops_official_doc",
        "publisher": "MLflow",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "MLflow Tracking logs parameters, code versions, metrics and output files for later visualization and comparison.",
        "limitations": ["ML experiment tracking source; strategy-rule fields still need CEK-TA-specific naming."],
    },
    "mlflow_dataset": {
        "source_title": "MLflow Dataset Tracking",
        "source_url": "https://mlflow.org/docs/latest/ml/dataset/",
        "source_type": "mlops_official_doc",
        "publisher": "MLflow",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "MLflow Dataset Tracking tracks and versions datasets used in training, validation and evaluation with lineage from raw data to predictions.",
        "limitations": ["ML dataset source; trading strategy rules must map strategy inputs and signal versions explicitly."],
    },
    "dvc_pipelines": {
        "source_title": "Get Started: Data Pipelines",
        "source_url": "https://doc.dvc.org/start/data-pipelines/data-pipelines",
        "source_type": "data_versioning_official_doc",
        "publisher": "DVC",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "DVC pipelines capture, organize, version and reproduce data science and ML workflows, including pipeline stages and parameters.",
        "limitations": ["DVC-specific workflow source; CEK-TA does not require DVC as the only implementation."],
    },
}


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "cand_20260611_phase37_kline_strategy_stop_loss_requires_invalidation_logic_001": {
        "research_task_id": "P37-C-K04",
        "source_keys": ["finra_stop_orders", "investor_gov_stop_orders", "ibkr_stop_order", "cfa_trade_execution"],
        "statement": "止损规则必须记录其风险管理目的、触发条件、执行假设和与交易假设失效之间的关系；若使用 stop/stop-limit/order-model 语义，必须说明 stop price、limit price、触发标准、跳空、滑点和未成交风险。",
        "patch_notes": [
            "把原先较强的“必须绑定结构失效”收窄为“必须记录止损规则的风险目的、触发条件、执行假设和失效关系”。",
            "新增 FINRA、Investor.gov、IBKR 和 CFA 来源支撑 stop/stop-limit 执行不确定性、交易成本和执行风险。",
            "Backtrader 仅保留为框架例子，不作为主来源。",
        ],
    },
    "cand_20260611_phase37_kline_strategy_take_profit_requires_reachability_check_001": {
        "research_task_id": "P37-C-K05",
        "source_keys": ["cfa_trade_execution", "quantconnect_trade_fills", "quantconnect_slippage", "investor_gov_stop_orders"],
        "statement": "止盈目标必须声明可达性和成交质量假设，包括目标触发条件、order/fill model、bar 粒度、滑点、成本、流动性和未成交风险；不得把图形目标或理想 R 倍数直接写成可成交收益。",
        "patch_notes": [
            "把止盈可达性从盈利主张收窄为执行/成交质量假设披露规则。",
            "新增 CFA TCA、QuantConnect fill/slippage 和 Investor.gov order-risk 来源。",
            "明确不生成止盈价格、R 倍数参数或实盘执行建议。",
        ],
    },
    "cand_20260611_phase37_kline_strategy_volume_confirmation_boundary_001": {
        "research_task_id": "P37-C-K10",
        "source_keys": ["databento_ohlcv", "databento_custom_ohlcv", "databento_statistics", "binance_klines"],
        "statement": "成交量确认必须声明 volume 字段口径、数据源、聚合规则、交易所/供应商语义、缺失区间和质量标志；不同市场、合约、现货/衍生品、官方统计与供应商聚合 bars 不能默认等价。",
        "patch_notes": [
            "新增 Databento OHLCV、trade resampling、official statistics 和 Binance Kline 字段来源支撑 volume 语义差异。",
            "把一般 TA 成交量确认收窄为数据口径/聚合/质量边界。",
            "明确成交量确认不是独立交易信号，也不证明突破、反转或方向预测有效。",
        ],
    },
    "cand_20260611_phase37_kline_strategy_strategy_rule_version_required_001": {
        "research_task_id": "P37-C-K12",
        "source_keys": ["mlflow_tracking", "mlflow_dataset", "dvc_pipelines", "white_reality_check"],
        "statement": "K线策略规则进入回测、模拟、AI 训练或人工审计前，必须记录策略规则版本、参数、代码/信号计算版本、数据集或数据版本、评估输出和变更原因；否则无法复现、比较或审计规则变更。",
        "patch_notes": [
            "新增 MLflow Tracking、MLflow Dataset Tracking 和 DVC pipeline 来源支撑参数、代码版本、数据版本、输出文件、lineage 和可复现工作流。",
            "White Reality Check 继续作为多次规则搜索和数据复用风险来源，不再单独支撑版本字段本体。",
            "明确 CEK-TA 不强制 MLflow/DVC，只要求等价的版本追踪字段。",
        ],
        "extra_sources": {
            "white_reality_check": {
                "source_title": "A Reality Check for Data Snooping",
                "source_url": "https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152",
                "source_type": "peer_reviewed_paper",
                "publisher": "Econometrica / Wiley",
                "published_at": "2000-09-01",
                "reliability": "high",
                "score": 90,
                "freshness": "stable",
                "evidence_summary": "White explains data snooping risk when the same data is reused for inference or model selection.",
                "limitations": ["Supports rule-search audit pressure; not a schema source for version fields."],
            }
        },
    },
}


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_from_key(key: str, supplement: dict[str, Any], start_index: int) -> dict[str, Any]:
    catalog = {**SOURCE_CATALOG, **supplement.get("extra_sources", {})}
    source = dict(catalog[key])
    source.update(
        {
            "source_id": f"src_supp_{start_index:03d}",
            "accessed_at": TODAY,
            "version": None,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        }
    )
    return source


def append_sources(candidate: dict[str, Any], sources: list[dict[str, Any]]) -> None:
    existing = candidate.setdefault("source_refs", [])
    urls = {source.get("source_url") for source in existing if isinstance(source, dict)}
    for source in sources:
        if source["source_url"] not in urls:
            existing.append(source)
            urls.add(source["source_url"])


def patch_candidate(candidate_id: str, supplement: dict[str, Any]) -> dict[str, Any]:
    path = CANDIDATE_DIR / f"{candidate_id}.json"
    candidate = read_json(path)
    source_start = len(candidate.get("source_refs", [])) + 1
    new_sources = [
        source_from_key(key, supplement, source_start + offset)
        for offset, key in enumerate(supplement["source_keys"])
    ]
    append_sources(candidate, new_sources)

    candidate["claim"]["statement"] = supplement["statement"]
    candidate["claim"]["evidence_summary"] = "; ".join(source["evidence_summary"] for source in new_sources[:3])
    candidate["claim"]["claim_strength"] = "medium_high"
    candidate["status"]["review_status"] = "needs_more_evidence"
    candidate["status"]["ingestion_decision"] = "ready_for_reaudit"
    candidate["status"]["updated_at"] = TODAY
    candidate["status"]["decision_reason"] = "已根据首轮严格审计补充专业来源和边界，进入二审 ready_for_reaudit；仍不得 reviewed/approved/default guidance/hard gate。"

    source_refs = candidate.get("source_refs", [])
    scores = [float(source.get("score", 0)) for source in source_refs if isinstance(source, dict)]
    candidate["source_quality"] = {
        **candidate.get("source_quality", {}),
        "overall_reliability": "high" if sum(scores) / len(scores) >= 82 else "medium_high",
        "score": round(sum(scores) / len(scores), 2),
        "score_version": "phase37_kline_strategy_supplemental_source_scoring_v1",
        "primary_source_count": len(
            [
                source
                for source in source_refs
                if source.get("source_type") in {"regulator_guidance", "professional_body_reference", "mlops_official_doc", "data_versioning_official_doc", "peer_reviewed_paper"}
            ]
        ),
        "supporting_source_count": len(source_refs),
        "low_reliability_source_count": 0,
        "limitations": [
            "补证来源用于支撑候选进入二审，不代表 formal reviewed 或 approved。",
            "平台、经纪商、供应商和框架文档只能支撑对应语义；外接项目必须映射自己的交易所、broker、数据供应商和执行模型。",
        ],
    }

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "export_ai_audit"
    workflow["supplemental_research_status"] = "ready_for_reaudit"
    workflow["supplemental_package_id"] = "phase37_kline_strategy_supplemental_reaudit_package_20260611"
    workflow["default_guidance_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["formalization_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "Supplemental Kline candidate is ready for re-audit only; formal reviewed/default guidance/hard gate remain blocked."
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_supplemental_research"
    review["reviewed_at"] = TODAY
    review["supplemental_research"] = {
        "task_id": TASK_ID,
        "status": "ready_for_reaudit",
        "patch_notes": supplement["patch_notes"],
        "added_source_ids": [source["source_id"] for source in new_sources],
        "added_source_urls": [source["source_url"] for source in new_sources],
    }
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_kline_strategy_supplemental_research_added",
            "reason": "根据首轮严格审计 needs_more_evidence 补充专业来源、收窄 claim 并导出二审包。",
            "patch_notes": supplement["patch_notes"],
        }
    )
    write_json(path, candidate)
    return candidate


def validate(candidates: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if len(candidates) != 4:
        errors.append(f"expected 4 candidates, got {len(candidates)}")
    for candidate in candidates:
        cid = candidate["candidate_id"]
        if candidate["status"]["ingestion_decision"] != "ready_for_reaudit":
            errors.append(f"{cid}: ingestion_decision must be ready_for_reaudit")
        if len(candidate.get("source_refs", [])) < 7:
            errors.append(f"{cid}: source_refs < 7 after supplement")
        if candidate.get("machine_gate", {}).get("default_guidance") != "deny":
            errors.append(f"{cid}: default guidance must stay denied")
        if candidate.get("machine_gate", {}).get("approved_allowed") is not False:
            errors.append(f"{cid}: approved_allowed must be false")
        if candidate.get("workflow", {}).get("formalization_allowed") is not False:
            errors.append(f"{cid}: formalization_allowed must be false")
    return errors


def write_research_report(candidates: list[dict[str, Any]], errors: list[str]) -> None:
    lines = [
        "# Phase 37 Kline / Strategy Engineering 补证研究记录",
        "",
        f"日期：{TODAY}",
        "",
        "## 补证范围",
        "",
        "本次只处理首轮严格审计中的 4 条 `needs_more_evidence`：P37-C-K04、P37-C-K05、P37-C-K10、P37-C-K12。",
        "",
        "## 补证结果",
        "",
        "| research_task_id | candidate_id | 新状态 | source_count | 关键补证方向 |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for candidate in candidates:
        supp = candidate.get("review", {}).get("supplemental_research", {})
        lines.append(
            f"| {candidate['research_task_id']} | `{candidate['candidate_id']}` | `{candidate['status']['ingestion_decision']}` | {len(candidate.get('source_refs', []))} | {'; '.join(supp.get('patch_notes', []))} |"
        )
    lines.extend(
        [
            "",
            "## 来源目录",
            "",
            "| key | title | publisher | type | role |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for key, source in SOURCE_CATALOG.items():
        lines.append(f"| `{key}` | {source['source_title']} | {source['publisher']} | {source['source_type']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "## 质量门禁",
            "",
            "```json",
            json.dumps({"pass": not errors, "errors": errors}, ensure_ascii=False, indent=2),
            "```",
            "",
            "## 边界",
            "",
            "本次补证不创建 formal reviewed，不创建 approved，不启用 default guidance 或 hard gate，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "",
        ]
    )
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines), encoding="utf-8")


def export_package(candidates: list[dict[str, Any]], errors: list[str]) -> None:
    package = {
        "schema_version": "1.0.0",
        "package_id": "phase37_kline_strategy_supplemental_reaudit_package_20260611",
        "source_audit_result_id": "audit_result_phase37_kline_strategy_candidate_audit_20260611_strict_v1",
        "phase": PHASE,
        "task_id": TASK_ID,
        "created_at": TODAY,
        "purpose": "对 Phase 37 Kline / Strategy Engineering 4 条补证候选进行二审，判断是否可升级为 accepted_for_draft。",
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "reviewed_allowed_in_this_package": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_instruction_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议"],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、监管资料、论文、案例和数据，对补证来源与 claim 进行严格审计。",
            "重点确认 P37-C-K04 是否仍过度声称结构失效，P37-C-K05 是否把可达性误写成收益保证，P37-C-K10 是否正确区分 volume 语义，P37-C-K12 是否有足够版本追踪证据。",
            "只允许输出 accepted_for_draft / needs_more_evidence / rejected；不得输出 reviewed、approved、default_guidance 或 hard_gate。",
            "若仍 needs_more_evidence，请列出需要补充的具体来源、应收窄的 statement 和冲突处理建议。",
        ],
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase37_kline_strategy_supplemental_reaudit_20260611_strict_v1",
            "package_id": "phase37_kline_strategy_supplemental_reaudit_package_20260611",
            "quality_gate": {"pass": "boolean", "reason": "string"},
            "results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                    "reason": "string",
                }
            ],
        },
        "quality_gate": {"pass": not errors, "errors": errors},
        "candidate_count": len(candidates),
        "candidates": candidates,
    }
    report = {
        "report_id": "phase37_kline_strategy_supplemental_reaudit_report",
        "package_id": package["package_id"],
        "generated_at": TODAY,
        "candidate_count": len(candidates),
        "quality_gate": package["quality_gate"],
        "audit_package": str(AUDIT_PACKAGE),
        "research_report": str(RESEARCH_REPORT),
        "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
        "boundary": "No formal reviewed/approved/default/hard gate was created.",
    }
    write_json(AUDIT_PACKAGE, package)
    write_json(REPORT_PATH, report)


def main() -> None:
    candidates = [patch_candidate(candidate_id, supplement) for candidate_id, supplement in SUPPLEMENTS.items()]
    errors = validate(candidates)
    write_research_report(candidates, errors)
    export_package(candidates, errors)
    if errors:
        raise SystemExit("\n".join(errors))
    print(json.dumps({"supplemented": len(candidates), "audit_package": str(AUDIT_PACKAGE)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
