"""Generate Phase 45 Market Data Entitlement / Reference Data candidates.

This script creates candidate and audit-support artifacts only. It does not
create formal reviewed knowledge, approve knowledge, enable default guidance,
or create hard gates.
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
PHASE = "45"
TASK_ID = "CEK-TA-469"
BATCH = "P45-G Market Data Entitlement / Reference Data"
PARTITION = "KB_02_DATA_ENGINEERING"
TREE_NODE = "kt.trading_engineering.data_engineering.reference_data_entitlement"

RESEARCH_REPORT = resolve_repo_path(
    "docs", "research", "phase45_reference_data_entitlement_candidate_research.md", start_file=__file__
)
GENERATION_REPORT = resolve_repo_path(
    "docs", "reports", "phase45_reference_data_entitlement_candidate_generation_report.json", start_file=__file__
)
QUALITY_GATE = resolve_repo_path(
    "docs", "reports", "phase45_reference_data_entitlement_candidate_quality_gate.json", start_file=__file__
)


SOURCES: dict[str, dict[str, Any]] = {
    "nyse_market_data_policy": {
        "source_title": "NYSE Proprietary Market Data Comprehensive Policy Package",
        "source_url": "https://www.nyse.com/publicdocs/nyse/data/NYSE_Proprietary_Market_Data_Comprehensive_Policy_Package.pdf",
        "source_type": "official_exchange_policy",
        "publisher": "NYSE",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "NYSE policy documents Non-Display Use categories, internal use, use on behalf of clients and derived data policy boundaries.",
        "limitations": ["NYSE proprietary market data policy; not a universal market-data license for all venues or vendors."],
    },
    "nasdaq_data_policies": {
        "source_title": "Nasdaq U.S. Equities and Options Data Policies",
        "source_url": "https://www.nasdaqtrader.com/content/AdministrationSupport/Policy/USEquitiesandOptionsDataPolicies.pdf",
        "source_type": "official_exchange_policy",
        "publisher": "Nasdaq Trader",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "Nasdaq policies describe non-display applications, internal usage and market-data product usage constraints.",
        "limitations": ["Nasdaq U.S. equities/options policy context; not directly portable to futures, crypto, OTC or non-U.S. data."],
    },
    "nasdaq_non_display_clarification": {
        "source_title": "Nasdaq Clarification for U.S. Non-Display Policy",
        "source_url": "https://nasdaqtrader.com/TraderNews.aspx?id=dn2015-09",
        "source_type": "official_exchange_policy",
        "publisher": "Nasdaq Trader",
        "reliability": "high",
        "score": 84,
        "freshness": "stable",
        "evidence_summary": "Nasdaq defines Non-Display as machine or automated-device access or use without a natural-person display.",
        "limitations": ["Clarification notice; current customer obligations still require the active policy and agreement."],
    },
    "cme_derived_data": {
        "source_title": "CME Group Derived Data",
        "source_url": "https://www.cmegroup.com/market-data/browse-data/derived-data.html",
        "source_type": "official_exchange_policy",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "CME describes licensing for derived works and derived data use cases based on CME market data.",
        "limitations": ["CME licensing context; derived data permissions must be checked against active agreement and product scope."],
    },
    "cme_license_data": {
        "source_title": "CME Group License Data Products",
        "source_url": "https://www.cmegroup.com/market-data/license-data.html",
        "source_type": "official_exchange_policy",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "CME market-data licensing page directs firms to license market data and derived data products by use case.",
        "limitations": ["High-level licensing entry point; exact permissions require the active customer agreement and fee schedule."],
    },
    "databento_definitions": {
        "source_title": "Databento Instrument Definitions",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/instrument-definitions",
        "source_type": "official_vendor_doc",
        "publisher": "Databento",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento instrument definitions provide point-in-time reference information including symbol, name, listing, expiration, tick size and strike price.",
        "limitations": ["Databento schema context; field coverage and semantics depend on dataset, venue and vendor version."],
    },
    "databento_schemas": {
        "source_title": "Databento Schemas and Data Formats",
        "source_url": "https://databento.com/docs/schemas-and-data-formats",
        "source_type": "official_vendor_doc",
        "publisher": "Databento",
        "reliability": "high",
        "score": 87,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento documents supported market-data schemas and field dictionaries such as MBO, MBP, trades, bars, definitions and statistics.",
        "limitations": ["Vendor-specific schema documentation; not a universal market-data schema standard."],
    },
    "databento_statistics": {
        "source_title": "Databento Statistics Schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/statistics",
        "source_type": "official_vendor_doc",
        "publisher": "Databento",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento statistics include session fields such as upper and lower price limits, settlement and venue-specific volume/price fields.",
        "limitations": ["Statistics schema availability and meaning depend on venue and dataset."],
    },
    "databento_definitions_blog": {
        "source_title": "Databento: Evaluating Market Data APIs - Point-in-Time Definitions",
        "source_url": "https://databento.com/blog/instrument-definitions",
        "source_type": "vendor_technical_article",
        "publisher": "Databento",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "stable",
        "evidence_summary": "Databento explains why point-in-time instrument definitions matter for historical and real-time reference data and backtesting.",
        "limitations": ["Vendor article; useful rationale, but reviewed field contracts should use official schema docs."],
    },
    "databento_tick_sizes": {
        "source_title": "Databento: Getting Futures Tick Sizes and Notional Tick Values",
        "source_url": "https://databento.com/blog/tick-sizes-and-values",
        "source_type": "vendor_technical_article",
        "publisher": "Databento",
        "reliability": "medium_high",
        "score": 80,
        "freshness": "stable",
        "evidence_summary": "Databento discusses futures variable tick sizes, contract multipliers and display styles that should not be hardcoded.",
        "limitations": ["Technical tutorial; exact fields and production contracts should rely on official schema and venue specs."],
    },
    "nasdaq_symbol_directory": {
        "source_title": "Nasdaq Symbol Directory Data Fields and Definitions",
        "source_url": "https://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs",
        "source_type": "official_exchange_doc",
        "publisher": "Nasdaq Trader",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "Nasdaq Symbol Directory defines fields such as round lot size, test issue and symbol directory metadata.",
        "limitations": ["Nasdaq symbol directory context; not a universal reference-data schema."],
    },
    "nasdaq_round_lot": {
        "source_title": "UTP Vendor Alert: Regulation NMS Round Lot Designations",
        "source_url": "https://www.nasdaqtrader.com/TraderNews.aspx?id=UTP2025-10",
        "source_type": "official_exchange_doc",
        "publisher": "Nasdaq Trader",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "UTP vendor alert describes semiannual round-lot designations for NMS stocks based on price-based evaluation periods.",
        "limitations": ["U.S. NMS stock context; does not apply to futures, crypto or all equities globally."],
    },
    "cme_product_slate": {
        "source_title": "CME Group Product Slate",
        "source_url": "https://www.cmegroup.com/markets/products",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "CME product slate links searchable product contract specifications and previous-day volume/open-interest data.",
        "limitations": ["CME product universe; contract specifications and reference metadata can change by product and date."],
    },
    "cme_price_limits": {
        "source_title": "CME Group Daily Price Limits",
        "source_url": "https://www.cmegroup.com/trading/price-limits.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "CME publishes daily price limits for multiple product groups, showing that price-limit metadata is product and session dependent.",
        "limitations": ["CME products only; not a universal limit-up/limit-down rule."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-G-DATA01",
        "slug": "market_data_entitlement_boundary",
        "title": "市场数据授权必须声明展示、非展示、衍生和训练用途",
        "statement": "交易 AI 项目使用交易所或供应商市场数据时，必须声明 display、non-display、internal use、client use、redistribution、derived data、backtest、replay、training 和 evaluation 的授权边界；AI/RAG/LLM 不得默认把可查看数据等同为可存储、可训练、可再分发或可供其他项目复用的数据。",
        "claim_type": "market_data_entitlement_boundary_rule",
        "sources": ["nyse_market_data_policy", "nasdaq_data_policies", "nasdaq_non_display_clarification", "cme_derived_data", "cme_license_data"],
    },
    {
        "task": "P45-G-DATA02",
        "slug": "point_in_time_instrument_definition_required",
        "title": "instrument definition 必须按 point-in-time 保存",
        "statement": "symbol、instrument_id、listing、expiration、corporate action、contract specification、tick size、lot size 等 reference data 必须按 point-in-time 版本保存和查询；不得用当前 instrument metadata 回填历史训练、回测、复盘或标签生成。",
        "claim_type": "point_in_time_reference_data_rule",
        "sources": ["databento_definitions", "databento_definitions_blog", "databento_schemas", "cme_product_slate"],
    },
    {
        "task": "P45-G-DATA03",
        "slug": "tick_size_lot_size_price_limit_metadata_required",
        "title": "tick size、lot size 和 price limit 必须作为版本化元数据",
        "statement": "tick size、lot size、round lot、contract multiplier、daily price limit、limit state 和 session price band 必须按 venue、instrument、product、session 和生效时间版本化；不得把 tick/lot/price-limit 规则硬编码成永久不变的常量。",
        "claim_type": "reference_metadata_versioning_rule",
        "sources": ["databento_definitions", "databento_statistics", "nasdaq_symbol_directory", "nasdaq_round_lot", "cme_price_limits", "databento_tick_sizes"],
    },
    {
        "task": "P45-G-DATA04",
        "slug": "dataset_coverage_universe_declaration_required",
        "title": "数据集覆盖范围和 universe 必须显式声明",
        "statement": "任何交易研究、回测、训练或 RAG 检索使用的数据集，都必须声明数据供应商、dataset、venue、asset class、instrument universe、覆盖起止时间、交易时段、缺失区间、delisting/symbol change 处理、过滤规则和可用字段；不得把未声明覆盖范围的数据当成完整市场事实。",
        "claim_type": "dataset_coverage_universe_rule",
        "sources": ["databento_schemas", "databento_definitions", "nasdaq_symbol_directory", "cme_product_slate"],
    },
    {
        "task": "P45-G-DATA05",
        "slug": "vendor_schema_version_required",
        "title": "供应商 schema 和解析版本必须可追踪",
        "statement": "市场数据 ingestion、解析、标准化和导出必须记录 vendor、dataset、schema、字段版本、parser_version、normalization_version、raw_snapshot 或 source digest；供应商字段、单位、枚举或语义变化不得静默影响回测、训练、TCA 或实盘审计。",
        "claim_type": "vendor_schema_versioning_rule",
        "sources": ["databento_schemas", "databento_definitions", "databento_statistics", "nasdaq_symbol_directory"],
    },
    {
        "task": "P45-G-DATA06",
        "slug": "reference_data_not_feature_signal",
        "title": "reference data 不是默认交易信号",
        "statement": "reference data 用于标识 instrument、venue、contract、session、tick/lot/limit、授权和覆盖范围；它本身不是 alpha、买卖点、仓位、风控阈值或实盘许可。若将 reference data 派生为模型特征，必须另行进入 Feature Engineering、Strategy Research 或 AI Engineering 的泄漏、时点和验证流程。",
        "claim_type": "reference_data_usage_boundary_rule",
        "sources": ["databento_definitions", "databento_statistics", "databento_schemas", "nyse_market_data_policy", "cme_derived_data"],
    },
]


def source_ref(source_key: str, index: int) -> dict[str, Any]:
    source = dict(SOURCES[source_key])
    source.update(
        {
            "source_id": f"src_{index:03d}",
            "accessed_at": TODAY,
            "version": None,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        }
    )
    return source


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_reference_data_entitlement_{safe}_001.json"


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, idx + 1) for idx, key in enumerate(item["sources"])]
    primary_types = {"official_exchange_policy", "official_exchange_doc", "official_vendor_doc"}
    source_score = round(sum(float(ref["score"]) for ref in refs) / len(refs), 2)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": f"cand_20260612_phase45_reference_data_entitlement_{item['task'].lower().replace('-', '_')}_001",
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 P45-G Market Data Entitlement / Reference Data 候选，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": TREE_NODE,
            "canonical_node_id": TREE_NODE,
            "tree_path": "CEK-TA / Trading Engineering / Data Engineering / Reference Data Entitlement",
            "related_nodes": [
                "kt.trading_engineering.data_engineering.data_quality",
                "kt.trading_engineering.market_microstructure.session_calendar",
                "kt.trading_engineering.strategy_engineering.feature_boundary",
                "kt.ai_engineering.training_dataset_boundary",
            ],
            "partition_id": PARTITION,
            "domain": "data_engineering",
            "subdomain": "reference_data_entitlement",
            "rule_type": "market_data_reference_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trading_ai_project_design_audit",
                "market_data_contract_review",
                "reference_data_schema_review",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "P45-G 只补市场数据授权、reference data、point-in-time 元数据、数据覆盖和 schema 版本边界；不定义交易信号或执行许可。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_reference_data_entitlement.{item['slug']}.v1",
            "evidence_summary": "；".join(ref["evidence_summary"] for ref in refs),
            "interpretation_notes": "本候选只定义数据授权、reference data 与时点一致性边界，不输出交易参数、买卖点、训练许可或数据授权法律结论。",
            "claim_strength": "candidate",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_vendor_exchange_license_and_dataset_caveats",
            "asset": "general",
            "timeframe": "historical_realtime_backtest_replay_training_and_audit_context",
            "data_granularity": "market_data_reference_data_instrument_definitions_statistics_schema_metadata",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要采集、存储、解析、训练、回测、重放、检索或展示市场数据与 reference data。",
                "AI IDE 需要检查数据授权、数据覆盖、instrument definition、tick/lot/price-limit 和 schema version 是否被显式声明。",
                "需要避免 current metadata 回填历史样本、授权边界被 RAG/LLM 默认绕过或 reference data 被误写成 alpha。",
            ],
            "not_applicable_when": [
                "用户要求法律意见、合同解释或市场数据授权结论；这必须由项目 owner/legal/vendor agreement 判断。",
                "用户要求买卖点、仓位、杠杆、止损止盈、交易许可、风控阈值或实盘执行动作。",
                "需要特定交易所、供应商或账户的实时授权事实时，应由外接项目事实层提供。",
            ],
            "assumptions": [
                "Market data entitlement 和 reference data 是数据工程与治理边界，不是交易策略。",
                "授权、schema、覆盖范围和 point-in-time 元数据必须保留 vendor、venue、dataset、product 和时间边界。",
                "候选通过外部审计前不能进入 formal reviewed 知识库。",
            ],
            "limitations": [
                "交易所、供应商和政策页面会随时间变化，正式 reviewed 前必须由审计确认活跃政策和可引用版本。",
                "官方技术文档只能证明对应 vendor/venue 的字段语义，不能替代外接项目合同、license 或 legal review。",
                "本候选不包含任何项目私有数据、账号信息、密钥、实盘授权状态或交易参数。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": source_score,
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": sum(1 for ref in refs if ref["source_type"] in primary_types),
            "supporting_source_count": sum(1 for ref in refs if ref["source_type"] not in primary_types),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "交易所/供应商市场数据政策和 schema 文档必须保留 active agreement、product、venue、dataset、jurisdiction 和版本 caveat。",
                "若后续使用内部 entitlement 或 reference_data schema，需要提供 contract extract 或 hash。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Data Engineering formal reviewed knowledge",
                "Phase 37 Market Microstructure formal reviewed knowledge",
                "Phase 38/41 AI Engineering training-data boundary knowledge",
                "Phase 45 Audit Trail / Clock Sync formal reviewed knowledge",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有 formal reviewed 知识的直接冲突；P45-G 补数据授权、reference data、point-in-time 元数据和 vendor schema 边界。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检查市场数据授权、非展示、衍生、训练、再分发和 retention 边界。",
                "用于生成 reference data、instrument definition、schema version、coverage universe 和 point-in-time 元数据 checklist。",
                "用于检查外接项目是否把 reference data 误写成交易信号、实盘许可或默认训练授权。",
            ],
            "not_allowed": [
                "不得输出法律授权结论、合同解释、买卖点、仓位、杠杆、止损止盈、交易许可或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、停机、撤单、数据再分发或训练授权。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; pending external strict audit; no reviewed/approved/default/hard gate.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "review": {
            "review_status": "candidate_ready",
            "review_mode": "external_strict_audit_required",
            "confidence": "medium_high",
            "freshness": "mixed",
            "reviewer": None,
            "reviewed_at": None,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_reference_data_entitlement_candidate_generated",
                    "reason": "Generated from Phase 45 P45-G task queue with official exchange, market-data policy and vendor schema sources.",
                }
            ],
        },
        "workflow": {
            "stage": "pending_external_audit",
            "queue_group": "pending",
            "source_phase": PHASE,
            "source_task_id": TASK_ID,
            "batch": BATCH,
            "formal_knowledge_id": None,
            "formal_knowledge_path": None,
            "allowed_next_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_next_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
        },
        "contribution": {
            "source": "phase45_professional_research",
            "private_data_removed": True,
            "project_specific_details_removed": True,
            "notes": "Generated for external strict audit; no project account, license agreement text, key, position, threshold, or private strategy data included.",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    expected = {f"P45-G-DATA{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if len(candidates) != 6:
        failures.append(f"expected 6 candidates, got {len(candidates)}")
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition mismatch")
        if item.get("classification", {}).get("canonical_node_id") != TREE_NODE:
            failures.append(f"{cid}: canonical node mismatch")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 3:
            failures.append(f"{cid}: primary_source_count < 3")
        gate = item.get("machine_gate", {})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "trade_execution_advice_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase45_reference_data_entitlement_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "batch": BATCH,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批次只生成 candidate，不创建 reviewed、approved、default guidance 或 hard gate。",
            "P45-G 只能用于市场数据授权、reference data、point-in-time 元数据和 schema 边界，不输出法律结论、交易信号或交易许可。",
        ],
    }


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Market Data Entitlement / Reference Data 候选知识采集记录",
        "",
        "## 范围",
        "",
        "本批次对应 CEK-TA-469 / P45-G，目标是采集 6 条 Market Data Entitlement / Reference Data P2 候选知识。",
        "",
        "本批次只生成候选知识、研究记录和质量门禁，不创建 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 联网核验来源",
        "",
        "| source_key | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 候选列表", "", "| ID | title | source_count | 状态 |", "| --- | --- | ---: | --- |"])
    for candidate in candidates:
        lines.append(f"| {candidate['research_task_id']} | {candidate['claim']['title']} | {len(candidate['source_refs'])} | {candidate['status']['review_status']} |")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. 不输出法律授权结论、买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "2. 交易所/供应商数据政策和 schema 文档必须保留 active agreement、venue、dataset、product、jurisdiction 和版本边界。",
            "3. reference data 只做身份、覆盖、授权、元数据和时点一致性约束；若作为模型特征，必须转入特征工程/策略研究/AI Engineering 验证。",
            "4. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。",
            "```",
        ]
    )
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    candidates = [build_candidate(item) for item in ITEMS]
    for item, candidate in zip(ITEMS, candidates):
        target = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, slug_to_file_name(item["slug"]), start_file=__file__)
        write_json(target, candidate)
    write_research_report(candidates)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase45_reference_data_entitlement_candidate_generation_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "batch": BATCH,
            "candidate_count": len(candidates),
            "quality_gate": gate,
            "candidates": [
                {
                    "research_task_id": item["research_task_id"],
                    "candidate_id": item["candidate_id"],
                    "knowledge_slug": item["claim"]["normalized_claim"],
                    "source_count": len(item["source_refs"]),
                }
                for item in candidates
            ],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
