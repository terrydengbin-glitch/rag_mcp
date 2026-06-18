"""Apply Phase 45 P2 reviewed/caveat_only preparation result.

This script consumes the strict reviewed/caveat_only preparation audit for the
eleven Phase 45 P2 candidates. It materializes only the eight entries
explicitly accepted for reviewed/caveat_only, supplements the three blocked
entries, and exports a supplemental re-audit package for DATA04, CRYPTO03 and
CRYPTO05.

It never creates approved knowledge, default guidance, hard gates, legal
license conclusions, training license conclusions, risk thresholds, liquidation
avoidance advice, or live trading actions.
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
TASK_ID = "CEK-TA-471"
AUDIT_RESULT_ID = "audit_phase45_p2_reviewed_preparation_20260612"
SOURCE_PACKAGE_ID = "phase45_p2_reviewed_preparation_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_p2_reviewed_blocked_supplemental_reaudit_package_20260612"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_ARCHIVE = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_p2_reviewed_preparation_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_p2_reviewed_blocked_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_p2_reviewed_blocked_supplemental_reaudit_gate.json", start_file=__file__)


RESULTS: dict[str, dict[str, Any]] = {
    "P45-G-DATA01": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "NYSE、Nasdaq、CME 来源足以支撑 market data display / non-display / internal use / client use / derived data / redistribution 等必须声明授权边界。",
            "本条只作为 entitlement checklist，不输出法律授权结论、训练授权结论或数据再分发许可。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 active agreement / legal owner / vendor agreement caveat。",
            "training、evaluation、RAG embedding storage 只能写成 must-declare usage boundary，不得写成 permission granted。",
        ],
        "patch_notes": {
            "source": ["保留 NYSE、Nasdaq、CME market-data policy 来源。"],
            "content": ["明确本条是授权边界审计规则，不是授权结论。"],
            "boundary": ["不得输出法律授权结论。", "不得输出训练授权结论。", "不得输出数据再分发许可。"],
            "conflict": [],
        },
    },
    "P45-G-DATA02": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "Databento PIT instrument definitions 足以支撑 reference data 必须按 point-in-time 查询。",
            "claim 防止 current metadata 回填历史训练、回测、复盘或标签生成，边界正确。",
        ],
        "required_followups": [
            "正式文本建议补 Databento Corporate Actions / Reference API source_ref。",
            "所有 PIT metadata 必须绑定 vendor、dataset、venue、schema version、effective time。",
        ],
        "patch_notes": {
            "source": ["保留 Databento Instrument Definitions、Databento PIT article、Databento Schemas、CME Product Slate。"],
            "content": ["明确 current metadata 不得静默回填历史样本。"],
            "boundary": ["不得把 reference data 写成交易信号。", "不得生成训练授权结论。"],
            "conflict": [],
        },
    },
    "P45-G-DATA03": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "Databento、Nasdaq、CME 来源足以支撑 tick size、lot size、round lot、price limit、session limit 等 reference metadata 需要按 venue/product/session/version 处理。"
        ],
        "required_followups": [
            "正式文本必须要求 effective_from / effective_to / source_ref / schema_version。",
            "Databento tutorial 类来源只能作为辅助，主证据应保留官方 schema / venue docs。",
        ],
        "patch_notes": {
            "source": ["保留 Databento Instrument Definitions、Databento Statistics、Nasdaq Symbol Directory、UTP round-lot alert、CME Daily Price Limits。"],
            "content": ["tick/lot/price-limit 是版本化 reference metadata，不是策略参数。"],
            "boundary": ["不得输出交易参数。", "不得输出风险阈值。"],
            "conflict": [],
        },
    },
    "P45-G-DATA04": {
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "dataset、schema、instrument universe、coverage 起止时间等主体方向正确。",
            "但 statement 包含 delisting / symbol change / corporate action 处理，当前 source_refs 仍缺少直接来源。",
        ],
        "required_followups": [
            "补 Databento Corporate Actions / Reference API，覆盖 listed/delisted securities、corporate actions、PIT reference events。",
            "或补 Nasdaq Daily List / FINRA Daily List 等 delisting / symbol-change 直接来源。",
            "补 dataset_coverage schema：coverage_start、coverage_end、missing_interval、filter_rule、field_availability、delisting_policy_ref。",
        ],
        "patch_notes": {
            "source": [
                "保留 Databento Schemas、Databento Instrument Definitions、Nasdaq Symbol Directory、CME Product Slate。",
                "新增 delisting / symbol-change / corporate action 直接来源后再审。",
            ],
            "content": ["不得把未声明覆盖范围的数据当成完整市场事实。"],
            "boundary": ["不得生成交易信号。", "不得生成训练授权结论。"],
            "conflict": [],
        },
    },
    "P45-G-DATA05": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "包内已提供 CEK-TA lineage contract hash，足以支撑 parser_version、normalization_version、raw_snapshot_digest、lineage_id 等字段本体。"
        ],
        "required_followups": [
            "正式文本必须区分 vendor_schema_version 与 internal parser_version / normalization_version。",
            "OpenLineage、MLflow、Iceberg、DVC 不得写成强制技术栈。",
            "market-data license、training use、redistribution permission 继续由 legal/vendor agreement owner 判断。",
        ],
        "patch_notes": {
            "source": ["保留 Databento、Nasdaq、CEK-TA lineage contract、OpenLineage、MLflow、Iceberg、DVC。"],
            "content": ["保留 vendor_id、dataset_id、schema_version、field_dictionary_ref、parser_version、parser_code_hash、normalization_version、normalization_code_hash、raw_snapshot_uri、raw_snapshot_digest、lineage_id。"],
            "boundary": ["不得输出法律授权结论。", "不得输出训练授权结论。", "不得输出数据再分发许可。", "不得生成 hard gate。"],
            "conflict": [],
        },
    },
    "P45-G-DATA06": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "Databento reference/schema 来源支撑 reference data 用于 instrument、venue、contract、session、tick/lot/limit 等标识。",
            "claim 明确 reference data 不是 alpha、买卖点、仓位、风控阈值或实盘许可。",
        ],
        "required_followups": ["若 reference data 派生为 feature，必须转入 Feature Engineering / Strategy Research / AI Engineering 的泄漏、时点和验证流程。"],
        "patch_notes": {
            "source": ["保留 Databento、NYSE、CME 来源。"],
            "content": ["明确 reference data 与 feature / alpha 的 owner boundary。"],
            "boundary": ["不得生成交易信号。", "不得生成训练授权结论。", "不得生成实盘许可。"],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO01": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["Binance Mark Price API 与 Binance / Bybit 文档足以支撑 mark price、index price、last price、funding basis 和 liquidation trigger 分开建模。"],
        "required_followups": ["正式文本必须保留 Binance / Bybit venue-specific caveat。", "oracle/composite index 需要绑定具体 venue index source_ref。"],
        "patch_notes": {
            "source": ["保留 Binance mark/index 文档、Binance Mark Price API、Bybit Mark Price 文档。"],
            "content": ["mark/index/last/oracle/funding_basis/liquidation_trigger 必须分字段。"],
            "boundary": ["不得输出止损参数。", "不得输出清算规避建议。", "不得输出交易许可。"],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO02": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": ["Binance、Bybit、OKX 来源足以支撑 funding rate、funding interval、funding timestamp、direction 和 realized funding fee 是 perpetual 独立现金流。"],
        "required_followups": ["正式文本必须要求 funding_cashflow_event schema 或等价字段。", "funding interval 与 fee source 必须按 venue/product/account mode 版本化。"],
        "patch_notes": {
            "source": ["保留 Binance Funding Rates、Binance Funding History API、Bybit Funding Rate、OKX Funding Fee。"],
            "content": ["funding fee 必须独立于 price_pnl、fee、slippage 和 strategy alpha。"],
            "boundary": ["不得输出 funding 套利建议。", "不得输出交易许可。", "不得输出仓位建议。"],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO03": {
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "liquidation 不等于普通止损的核心 claim 正确。",
            "但 source_refs 仍不足以直接覆盖 maintenance margin tier、margin mode、partial liquidation。",
        ],
        "required_followups": [
            "补 Binance Leverage & Margin / maintenance margin bracket 来源。",
            "补 Bybit Risk Limit / Maintenance Margin / laddered liquidation 来源。",
            "补 internal liquidation_event schema：maintenance_margin_source_ref、margin_mode、liquidation_price、bankruptcy_price、partial_liquidation_ref。",
        ],
        "patch_notes": {
            "source": ["保留 Binance liquidation、Binance mark price、Bybit mark price 来源。", "新增 maintenance margin tier / margin mode / partial liquidation 直接来源后再审。"],
            "content": ["liquidation price、bankruptcy price、maintenance margin、margin mode、partial liquidation 必须分字段。"],
            "boundary": ["不得输出清算规避建议。", "不得输出仓位或杠杆建议。", "不得输出止损参数。"],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO04": {
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "Binance 与 Bybit 来源足以支撑 ADL、insurance fund、bankruptcy loss coverage 是 venue-specific 风险机制。",
            "Binance ADL Risk API 支撑 ADL rating 只能作为 venue-specific risk data，不是 CEK-TA 阈值、交易信号或 hard gate。",
        ],
        "required_followups": ["正式文本必须保留 venue/product/collateral/margin mode caveat。", "ADL risk rating 不得进入交易信号、默认指导或 hard gate。"],
        "patch_notes": {
            "source": ["保留 Binance Insurance Fund、Binance ADL、Binance ADL Risk API、Bybit Insurance Fund、Bybit ADL。"],
            "content": ["ADL / insurance fund / loss allocation 必须按 venue-specific 风险机制建模。"],
            "boundary": ["不得输出清算规避。", "不得输出交易信号。", "不得输出 hard gate。"],
            "conflict": [],
        },
    },
    "P45-H-CRYPTO05": {
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "二审补证足以支撑 accepted_for_draft。",
            "但 reviewed/caveat_only 层仍缺 exchange status / incident event 直接来源，以及 mark price anomaly / index component abnormal handling 的直接规则来源。",
        ],
        "required_followups": [
            "补 Binance / Bybit / OKX status page 或 incident/outage 官方来源。",
            "补 Bybit mark price abnormal / index component abnormal handling source，或等价 venue rulebook。",
            "如保留 clawback 字段，补具体 venue clawback / loss-socialization rulebook。",
            "API/WebSocket 风险只能进入 observability / audit checklist，不得变成自动停机 hard gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 Databento Status、OKX Pre-market、Binance ADL、Binance Insurance Fund、Binance Aggregate Trade Streams、Binance WebSocket、Bybit WebSocket、Binance Maintenance Updates、Binance Mark Price API。",
                "新增 outage / incident truth source 与 mark-index anomaly handling source 后再审。",
            ],
            "content": ["exchange maintenance / service interruption、api_ws_disconnect、heartbeat_ping_pong_failure、stream_rate_limit、mark_index_monitoring、pre_market_rule、adl_insurance_event、loss_allocation_mechanism 需要分字段建模。"],
            "boundary": ["不得输出清算规避建议。", "不得输出仓位、杠杆或止损止盈。", "不得生成停机 hard gate。", "不得生成自动解锁、自动撤单或强平处理动作。", "不得把 Binance / Bybit / OKX 规则泛化为所有 crypto venue。"],
            "conflict": [],
        },
    },
}


SUPPLEMENTAL_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P45-G-DATA04": [
        {
            "source_id": "src_supp_data04_001",
            "source_title": "Corporate Actions: Data Feed Specifications",
            "source_url": "https://databento.com/docs/venues-and-datasets/corporate-actions",
            "source_type": "official_vendor_doc",
            "publisher": "Databento",
            "reliability": "high",
            "score": 87,
            "freshness": "time_sensitive",
            "relevance": "high",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "Databento corporate actions feed covers reference events such as listed/delisted securities and corporate action data specifications.",
            "limitations": ["Vendor-specific feed; not a universal corporate-actions schema."],
        },
        {
            "source_id": "src_supp_data04_002",
            "source_title": "Nasdaq Daily List",
            "source_url": "https://listingcenter.nasdaq.com/IssuersPendingSuspensionDelisting.aspx",
            "source_type": "official_exchange_doc",
            "publisher": "Nasdaq Listing Center",
            "reliability": "high",
            "score": 84,
            "freshness": "time_sensitive",
            "relevance": "medium_high",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "Nasdaq Daily List provides issuer events including pending suspension and delisting context.",
            "limitations": ["Nasdaq-specific list; other venues need their own delisting/symbol-change feeds."],
        },
    ],
    "P45-H-CRYPTO03": [
        {
            "source_id": "src_supp_crypto03_001",
            "source_title": "Binance Futures Leverage & Margin",
            "source_url": "https://www.binance.com/en/futures/trading-parameters/perpetual/leverage-margin",
            "source_type": "official_platform_doc",
            "publisher": "Binance",
            "reliability": "high",
            "score": 86,
            "freshness": "time_sensitive",
            "relevance": "high",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "Binance leverage and margin trading parameters provide venue/product-specific margin bracket context.",
            "limitations": ["Binance-specific; not a universal margin or liquidation rule."],
        },
        {
            "source_id": "src_supp_crypto03_002",
            "source_title": "Risk Limit (Perpetual and Futures)",
            "source_url": "https://www.bybit.com/en/help-center/article/Risk-Limit-USDT-Contract",
            "source_type": "official_platform_doc",
            "publisher": "Bybit",
            "reliability": "high",
            "score": 85,
            "freshness": "time_sensitive",
            "relevance": "high",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "Bybit risk limit documentation supports position tier, maintenance margin and liquidation-risk context for perpetual/futures contracts.",
            "limitations": ["Bybit-specific; not a universal crypto perpetual standard."],
        },
    ],
    "P45-H-CRYPTO05": [
        {
            "source_id": "src_supp_crypto05_006",
            "source_title": "OKX Status",
            "source_url": "https://www.okx.com/status",
            "source_type": "official_platform_doc",
            "publisher": "OKX",
            "reliability": "high",
            "score": 84,
            "freshness": "time_sensitive",
            "relevance": "medium_high",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "OKX status page provides service-status and incident/maintenance context for exchange availability checks.",
            "limitations": ["OKX-specific; not Binance/Bybit global outage truth."],
        },
        {
            "source_id": "src_supp_crypto05_007",
            "source_title": "Mark Price Calculation (Perpetual and Expiry Contracts)",
            "source_url": "https://www.bybit.com/en/help-center/article/Mark-Price-Calculation-Perpetual-Expiry-Contracts",
            "source_type": "official_platform_doc",
            "publisher": "Bybit",
            "reliability": "high",
            "score": 86,
            "freshness": "time_sensitive",
            "relevance": "high",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "Bybit mark price documentation includes mark/index calculation context and abnormal/fallback handling cues for index components.",
            "limitations": ["Bybit-specific; other venues need their own mark/index abnormal handling rules."],
        },
        {
            "source_id": "src_supp_crypto05_008",
            "source_title": "Binance Statement on Recent Market Volatility",
            "source_url": "https://www.binance.com/en/support/announcement/statement-on-recent-market-volatility-3f1a339167194f09b1c8a7538f7187ec",
            "source_type": "official_platform_doc",
            "publisher": "Binance",
            "reliability": "medium_high",
            "score": 82,
            "freshness": "time_sensitive",
            "relevance": "medium",
            "accessed_at": TODAY,
            "version": None,
            "quoted_excerpt_allowed": False,
            "evidence_summary": "Binance official announcement provides incident-style context for service stability and market-volatility reviews.",
            "limitations": ["Event-specific announcement; not a standing status-page API."],
        },
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def candidate_paths() -> list[Path]:
    dirs = [
        resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_02_DATA_ENGINEERING", start_file=__file__),
        resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_03_MARKET_MICROSTRUCTURE", start_file=__file__),
        resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_07_RISK_MANAGEMENT", start_file=__file__),
    ]
    paths: list[Path] = []
    for cand_dir in dirs:
        paths.extend(cand_dir.glob("cand_20260612_phase45_reference_data_entitlement_*.json"))
        paths.extend(cand_dir.glob("cand_20260612_phase45_crypto_perp_*.json"))
    return sorted(paths)


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if str(item).strip()]


def audit_result_payload() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_audit",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 11,
            "accepted_for_reviewed_caveat_only": 8,
            "needs_more_evidence": 3,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "research_task_id": task_id,
                "decision": result["decision"],
                "confidence": result["confidence"],
                "reviewed_allowed": result["decision"] == "accepted_for_reviewed_caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "trade_execution_advice_allowed": False,
                "legal_license_conclusion_allowed": False,
                "reasons": result["reasons"],
                "required_followups": result["required_followups"],
                "patch_notes": result["patch_notes"],
            }
            for task_id, result in RESULTS.items()
        ],
        "global_required_patches": [
            "formal reviewed 只能是 caveat_only，approved/default guidance/hard gate 必须保持 false。",
            "DATA04、CRYPTO03、CRYPTO05 需要补证后再审，不能直接 formalize。",
        ],
    }


def proposed_knowledge_id(candidate: dict[str, Any]) -> str:
    workflow = candidate.get("workflow", {})
    conversion = workflow.get("conversion_target") if isinstance(workflow.get("conversion_target"), dict) else {}
    explicit = conversion.get("proposed_knowledge_id") or workflow.get("formal_knowledge_id")
    if explicit:
        return str(explicit)
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id", ""))
    normalized = normalized.replace("phase45_reference_data_entitlement.", "phase45_p2.")
    normalized = normalized.replace("phase45_crypto_perp.", "phase45_p2.")
    return f"kb_{re.sub(r'[^A-Za-z0-9_.-]+', '_', normalized)}.v1"


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    source_refs = candidate.get("source_refs", [])
    knowledge_id = proposed_knowledge_id(candidate)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(claim.get("title") or candidate.get("research_task_id")),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": classification.get("rule_type"),
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
            "classification_notes": "Phase 45 P2 formal reviewed/caveat_only；只用于数据授权、reference data、crypto perpetual 风险审计上下文，不是 approved/default guidance/hard gate，不生成交易动作或法律授权结论。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market"),
            "asset": applicability.get("asset"),
            "timeframe": applicability.get("timeframe"),
            "data_granularity": applicability.get("data_granularity"),
            "project_type": applicability.get("project_type"),
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
                "确认问题属于 Phase 45 P2 数据授权、reference data 或 crypto perpetual 风险边界。",
                "检查 source_evidence 是否绑定 vendor、venue、dataset、product、account mode、schema/API/rulebook/version 和 accessed_at。",
                "返回知识时必须携带 reviewed/caveat_only、source_evidence、适用范围、不适用场景、owner 边界和 machine gate。",
                "不得把本条解释成法律授权结论、训练授权结论、交易许可、清算规避、仓位、杠杆、止损止盈、默认指导或 hard gate。",
            ],
            "anti_patterns": string_list(as_list(claim.get("anti_patterns")) + result["patch_notes"]["boundary"]),
            "validation": [
                "review.review_status 必须为 reviewed；review_mode 必须为 caveat_only。",
                "approved_allowed、default_guidance_allowed、hard_gate_allowed、risk_threshold_advice_allowed、trade_execution_advice_allowed、legal_license_conclusion_allowed 必须为 false。",
                "source_evidence 至少包含 3 条可审计来源，并保留 venue/vendor/product/API/rulebook 限制。",
                "不得出现买卖点、仓位、杠杆、止损止盈、清算规避、法律授权结论、训练授权结论或实盘执行建议。",
            ],
            "risk_notes": [
                "本条只可作为 reviewed/caveat_only 审计上下文。",
                "供应商、交易所、crypto venue 和 API 文档具有时间敏感性，外接项目必须复核当前有效版本。",
                "本条不创建 approved，不进入默认指导，不启用 hard gate。",
            ],
            "citation_notes": "；".join(str(ref.get("evidence_summary", "")) for ref in source_refs if ref.get("evidence_summary")),
            "audit_patch_notes": result["patch_notes"],
        },
        "assumptions": applicability.get("assumptions", []),
        "source_evidence": source_refs,
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": candidate.get("conflict_audit", {}).get("checked_against", []),
            "conflicts": [],
            "resolution_summary": "Phase 45 P2 reviewed/caveat_only preparation audit passed for this item; approved/default guidance/hard gate/legal or trading conclusions remain disabled.",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
        },
        "review": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "confidence": result["confidence"],
            "freshness": candidate.get("review", {}).get("freshness", "time_sensitive"),
            "reviewer": "external_ai_strict_audit_and_codex",
            "reviewed_at": TODAY,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "trade_execution_advice_allowed": False,
                "legal_license_conclusion_allowed": False,
                "reasons": result["reasons"],
                "required_followups": result["required_followups"],
                "patch_notes": result["patch_notes"],
            },
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 检查数据授权、reference data、point-in-time metadata、crypto perpetual 特有风险的设计边界。",
                "用于 RAG 检索、schema review、adapter contract review、数据 lineage 审计和风险上下文说明。",
            ],
            "not_allowed": [
                "不得生成法律授权结论、训练授权结论、再分发许可、买卖点、仓位、杠杆、止损止盈、清算规避或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、自动停机、自动解锁、自动撤单、自动强平处理或风控阈值。",
            ],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_visibility": "reviewed_caveat_only",
            "reason": "Phase 45 P2 reviewed/caveat_only audit passed; approved/default guidance/hard gate/legal and trading conclusions remain disabled.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
        },
        "contribution": candidate.get("contribution", {}),
    }


def upsert_sources(candidate: dict[str, Any], sources: list[dict[str, Any]]) -> None:
    refs = list(candidate.get("source_refs", []))
    seen = {ref.get("source_url") for ref in refs}
    for source in sources:
        if source.get("source_url") not in seen:
            refs.append(source)
            seen.add(source.get("source_url"))
    candidate["source_refs"] = refs
    if refs:
        candidate.setdefault("source_quality", {})["score"] = round(sum(float(ref.get("score", 70)) for ref in refs) / len(refs), 2)
        primary_types = {"official_vendor_doc", "official_exchange_doc", "official_platform_doc", "official_api_doc", "official_spec", "internal_contract"}
        candidate["source_quality"]["primary_source_count"] = sum(1 for ref in refs if ref.get("source_type") in primary_types)
        candidate["source_quality"]["supporting_source_count"] = len(refs) - candidate["source_quality"]["primary_source_count"]


def archive_audit_result() -> None:
    write_json(AUDIT_ARCHIVE, audit_result_payload())


def process_candidates() -> dict[str, Any]:
    archive_audit_result()
    formalized: list[dict[str, Any]] = []
    needs_evidence: list[dict[str, Any]] = []
    missing: list[str] = []
    paths_by_task: dict[str, Path] = {}
    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        if task_id.startswith("P45-G-DATA") or task_id.startswith("P45-H-CRYPTO"):
            paths_by_task[task_id] = path

    for task_id, result in RESULTS.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        candidate = read_json(path)
        if result["decision"] == "accepted_for_reviewed_caveat_only":
            formal = build_formal_item(candidate, result)
            partition = str(candidate.get("classification", {}).get("partition_id"))
            formal_path = resolve_repo_path("codex-expert-kit", "rag", "knowledge", partition, sanitize_filename(formal["knowledge_id"]), start_file=__file__)
            write_json(formal_path, formal)
            candidate.setdefault("status", {}).update(
                {
                    "review_status": "formalized",
                    "ingestion_decision": "formal_reviewed_created",
                    "decision_reason": "reviewed/caveat_only 准备审计通过，已创建 formal reviewed 知识；不得 approved/default/hard gate。",
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
                    "next_action": "none",
                }
            )
            formalized.append({"research_task_id": task_id, "candidate_id": candidate.get("candidate_id"), "knowledge_id": formal["knowledge_id"], "formal_path": repo_relative(formal_path)})
        else:
            upsert_sources(candidate, SUPPLEMENTAL_SOURCES.get(task_id, []))
            candidate.setdefault("status", {}).update(
                {
                    "review_status": "needs_more_evidence",
                    "ingestion_decision": "needs_more_evidence",
                    "decision_reason": "reviewed/caveat_only 准备审计仍需补证；已补直接来源并等待再审。",
                    "updated_at": TODAY,
                }
            )
            workflow = candidate.setdefault("workflow", {})
            workflow.update(
                {
                    "stage": "reviewed_preparation_blocked_supplemented",
                    "queue_group": "needs_more_evidence",
                    "allowed_next_decisions": ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"],
                    "forbidden_next_decisions": ["approved", "default_guidance", "hard_gate", "legal_license_conclusion", "trade_execution_advice"],
                    "next_action": "external_reaudit_required",
                }
            )
            needs_evidence.append({"research_task_id": task_id, "candidate_id": candidate.get("candidate_id"), "path": repo_relative(path)})

        review = candidate.setdefault("review", {})
        review["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": SOURCE_PACKAGE_ID,
            "decision": result["decision"],
            "confidence": result["confidence"],
            "reviewed_allowed": result["decision"] == "accepted_for_reviewed_caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "reasons": result["reasons"],
            "required_followups": result["required_followups"],
            "patch_notes": result["patch_notes"],
        }
        review.setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_p2_reviewed_preparation_imported",
                "reason": result["decision"],
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        candidate.setdefault("claim", {})["audit_patch_notes"] = result["patch_notes"]
        write_json(path, candidate)

    return {"formalized": formalized, "needs_evidence": needs_evidence, "missing": missing}


def build_supplemental_package(needs_evidence: list[dict[str, Any]]) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for item in needs_evidence:
        path = REPO_ROOT / item["path"]
        candidates.append(read_json(path))
    failures: list[str] = []
    expected = {"P45-G-DATA04", "P45-H-CRYPTO03", "P45-H-CRYPTO05"}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    for candidate in candidates:
        if len(candidate.get("source_refs", [])) < 5:
            failures.append(f"{candidate.get('candidate_id')}: source_refs_less_than_5_after_supplement")
        blob = json.dumps(candidate, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{candidate.get('candidate_id')}: possible_mojibake")
    gate = {
        "gate_id": "phase45_p2_reviewed_blocked_supplemental_reaudit_gate",
        "checked_at": TODAY,
        "phase": "45",
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 3,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 DATA04、CRYPTO03、CRYPTO05 是否可进入 reviewed/caveat_only；不得创建 approved、default guidance、hard gate、法律授权结论、训练授权结论、清算规避或交易执行建议。",
            "补充来源均为 vendor/venue/platform-specific，不能泛化为所有市场或所有 crypto venue。",
        ],
    }
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "phase": "45",
        "task_id": TASK_ID,
        "package_type": "reviewed_blocked_supplemental_reaudit",
        "scope": {
            "candidate_count": len(candidates),
            "target": "复审 DATA04、CRYPTO03、CRYPTO05 补证后是否可进入 formal reviewed/caveat_only。",
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "legal_license_conclusion_allowed": False,
            "training_license_conclusion_allowed": False,
            "liquidation_avoidance_advice_allowed": False,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、交易所/供应商/API 文档、案例和数据，对补证内容进行严格再审。",
            "检查 DATA04 是否已用 Databento Corporate Actions / Nasdaq Daily List 等直接来源支撑 delisting、symbol change、corporate action 与 coverage 声明。",
            "检查 CRYPTO03 是否已用 Binance leverage/margin bracket、Bybit risk limit / maintenance margin / partial liquidation 来源支撑 maintenance margin tier、margin mode 和 partial liquidation。",
            "检查 CRYPTO05 是否已用 exchange status / incident source 与 mark/index abnormal handling 来源支撑 outage、incident truth 和 mark/index 异常处理边界。",
            "输出只能是 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked；不得输出 approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {
                "total": 3,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-G-DATA04 | P45-H-CRYPTO03 | P45-H-CRYPTO05",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "legal_license_conclusion_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }
    return {"gate": gate, "package": package}


def write_supplemental_research() -> None:
    SUPPLEMENTAL_RESEARCH.write_text(
        """# Phase 45 P2 reviewed 阻断项补证记录

## P45-G-DATA04

- Databento Corporate Actions：补充 listed/delisted securities、corporate actions、PIT reference event 语境。
- Nasdaq Daily List：补充 Nasdaq-specific pending suspension / delisting event 语境。
- 边界：这些来源只支撑对应 vendor/venue，不代表所有市场。

## P45-H-CRYPTO03

- Binance Futures Leverage & Margin：补充 Binance-specific margin bracket / leverage / maintenance margin 语境。
- Bybit Risk Limit：补充 Bybit-specific risk limit、maintenance margin 与阶梯风险语境。
- 边界：不得输出仓位、杠杆、清算规避或止损参数。

## P45-H-CRYPTO05

- OKX Status：补充 exchange status / incident / maintenance 语境。
- Bybit Mark Price Calculation：补充 mark/index 异常处理或 fallback 语境。
- Binance Market Volatility Statement：补充 incident-style 官方公告语境。
- 边界：API/WebSocket 风险只能进入 observability / audit checklist，不得变成自动停机 hard gate。
""",
        encoding="utf-8",
    )


def main() -> int:
    result = process_candidates()
    supplemental = build_supplemental_package(result["needs_evidence"])
    write_json(SUPPLEMENTAL_GATE, supplemental["gate"])
    write_json(SUPPLEMENTAL_PACKAGE, supplemental["package"])
    write_supplemental_research()
    report = {
        "report_id": "phase45_p2_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "formal_reviewed_created": len(result["formalized"]),
        "formalized": result["formalized"],
        "needs_more_evidence_count": len(result["needs_evidence"]),
        "needs_more_evidence": result["needs_evidence"],
        "missing": result["missing"],
        "supplemental_reaudit_package": repo_relative(SUPPLEMENTAL_PACKAGE),
        "supplemental_reaudit_gate": repo_relative(SUPPLEMENTAL_GATE),
        "supplemental_research": repo_relative(SUPPLEMENTAL_RESEARCH),
        "approved_created": 0,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "legal_license_conclusion_enabled": False,
        "trade_execution_advice_enabled": False,
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if supplemental["gate"]["gate_status"] == "pass" and not result["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
