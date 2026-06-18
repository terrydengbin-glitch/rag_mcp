"""Generate Phase 37 Data Engineering candidate knowledge.

This script only writes candidate and audit-support artifacts. It does not
create formal reviewed knowledge, does not approve knowledge, and does not
enable default guidance.
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


TODAY = "2026-06-11"
PHASE = "37"
PARTITION = "KB_02_DATA_ENGINEERING"
TREE_NODE = "kt.trading_engineering.data_engineering"
TREE_PATH = "CEK-TA / Trading Engineering / Data Engineering"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path(
    "docs", "research", "phase37_data_engineering_candidate_research.md", start_file=__file__
)
GENERATION_REPORT = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_candidate_generation_report.md", start_file=__file__
)
QUALITY_GATE = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_candidate_quality_gate.json", start_file=__file__
)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "databento_ohlcv": {
        "source_title": "OHLCV schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/ohlcv",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento documents OHLCV aggregate bars with O/H/L/C/V fields, interval suffixes, start timestamps, and no-record semantics for empty intervals.",
        "limitations": ["Vendor-specific schema; use as strong schema evidence but not as a universal exchange rule."],
    },
    "databento_common_fields": {
        "source_title": "Common fields, enums, and types",
        "source_url": "https://databento.com/docs/standards-and-conventions/common-fields-enums-types",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento documents primary timestamps, including ts_recv and ts_event, and sorting/indexing timestamp behavior.",
        "limitations": ["Vendor-specific timestamp semantics; external projects must map their own provider fields explicitly."],
    },
    "databento_trades": {
        "source_title": "Trades schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/trades",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 85,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento trade records distinguish matching-engine event timestamps from capture/receive timestamps.",
        "limitations": ["Vendor-specific field names; use to support timestamp-role separation, not a universal schema."],
    },
    "databento_bbo": {
        "source_title": "BBO schemas",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/bbo",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento BBO interval schemas document interval suffixes, no-record semantics, and forward-fill details for missing bid or ask sides.",
        "limitations": ["Vendor-specific BBO behavior; useful for missing/forward-fill policy evidence."],
    },
    "databento_instrument_definitions": {
        "source_title": "Instrument definitions schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/instrument-definitions",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento instrument definitions provide point-in-time reference data such as symbols, expiration, listing date, tick size, and strike price.",
        "limitations": ["Provider-specific reference data; roll and corporate action rules still need venue/index-specific policy."],
    },
    "databento_symbology": {
        "source_title": "Symbology",
        "source_url": "https://databento.com/docs/standards-and-conventions/symbology",
        "source_type": "market_data_vendor_official_doc",
        "publisher": "Databento",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databento documents symbol conventions including raw symbols, instrument IDs, parent symbols, and continuous symbols.",
        "limitations": ["Vendor-specific symbology; still requires external project mapping and versioning."],
    },
    "databricks_point_in_time": {
        "source_title": "Time series feature tables and point-in-time joins",
        "source_url": "https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series",
        "source_type": "feature_store_official_doc",
        "publisher": "Databricks",
        "published_at": None,
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "Databricks documents point-in-time correct training datasets and explains that future data leakage can impair model performance.",
        "limitations": ["Feature-store context; apply conceptually to trading features only after mapping event/available/decision times."],
    },
    "databricks_declarative_features": {
        "source_title": "Train models with declarative features",
        "source_url": "https://docs.databricks.com/aws/en/machine-learning/feature-store/train-with-declarative-features",
        "source_type": "feature_store_official_doc",
        "publisher": "Databricks",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Databricks states that features should be computed only from source data available before each row timestamp to prevent future leakage.",
        "limitations": ["ML feature-store context; does not define every market-data timestamp role."],
    },
    "ibm_data_leakage": {
        "source_title": "What is data leakage in machine learning?",
        "source_url": "https://www.ibm.com/think/topics/data-leakage-machine-learning",
        "source_type": "engineering_reference",
        "publisher": "IBM",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "stable",
        "evidence_summary": "IBM explains data leakage as using information unavailable at prediction time, inflating model performance.",
        "limitations": ["General ML source; supports leakage boundary but not market-data schema details."],
    },
    "postgres_datetime": {
        "source_title": "PostgreSQL Date/Time Types",
        "source_url": "https://www.postgresql.org/docs/current/datatype-datetime.html",
        "source_type": "database_official_doc",
        "publisher": "PostgreSQL",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "PostgreSQL documents timestamp with time zone behavior, including UTC storage/conversion semantics.",
        "limitations": ["Database behavior source; trading systems must still define market session and venue timezone policy."],
    },
    "postgres_invalid_datetime": {
        "source_title": "PostgreSQL Handling of Invalid or Ambiguous Timestamps",
        "source_url": "https://www.postgresql.org/docs/current/datetime-invalid-input.html",
        "source_type": "database_official_doc",
        "publisher": "PostgreSQL",
        "published_at": None,
        "reliability": "high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "PostgreSQL documents explicit UTC offsets and ambiguous timestamp handling, supporting explicit timezone policies.",
        "limitations": ["Database semantics; not a substitute for venue calendar and session rules."],
    },
    "great_expectations_core": {
        "source_title": "Try Great Expectations",
        "source_url": "https://docs.greatexpectations.io/docs/core/introduction/try_gx/",
        "source_type": "data_quality_framework_doc",
        "publisher": "Great Expectations",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Great Expectations documents expectations, validation results, failed counts and percentages, and generated Data Docs.",
        "limitations": ["Framework-specific quality checks; project-specific thresholds and market calendars must be defined separately."],
    },
    "great_expectations_home": {
        "source_title": "Great Expectations",
        "source_url": "https://greatexpectations.io/",
        "source_type": "data_quality_framework_doc",
        "publisher": "Great Expectations",
        "published_at": None,
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "Great Expectations positions GX as a framework to validate, test, and document data quality.",
        "limitations": ["Product site; use as supporting evidence only."],
    },
    "iceberg_spec": {
        "source_title": "Apache Iceberg Table Spec",
        "source_url": "https://iceberg.apache.org/spec/",
        "source_type": "storage_table_format_spec",
        "publisher": "Apache Iceberg",
        "published_at": None,
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "Apache Iceberg specifies snapshots, manifests, data files, and file-level metrics used to track table versions.",
        "limitations": ["Storage-table format spec; not mandatory for all CEK-TA projects."],
    },
    "iceberg_home": {
        "source_title": "Apache Iceberg",
        "source_url": "https://iceberg.apache.org/",
        "source_type": "storage_table_format_doc",
        "publisher": "Apache Iceberg",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "Apache Iceberg highlights time travel and rollback, supporting versioned dataset reproducibility concepts.",
        "limitations": ["Project overview; use with spec for stronger evidence."],
    },
    "dvc_start": {
        "source_title": "DVC Get Started",
        "source_url": "https://doc.dvc.org/start",
        "source_type": "data_versioning_tool_doc",
        "publisher": "DVC",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "DVC documents Git-based versioning for data and models with external/local storage.",
        "limitations": ["Tool-specific source; should not force DVC as a universal dependency."],
    },
    "dvc_versioning": {
        "source_title": "Versioning data and models",
        "source_url": "https://doc.dvc.org/example-scenarios/versioning-data-and-models",
        "source_type": "data_versioning_tool_doc",
        "publisher": "DVC",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "DVC explains capturing data/model versions in Git commits while storing larger contents outside Git.",
        "limitations": ["Tool-specific workflow; large lakehouse projects may prefer table-format versioning."],
    },
    "eurex_corporate_actions": {
        "source_title": "Corporate action procedures",
        "source_url": "https://www.eurex.com/ex-en/rules-regs/corporate-actions/corporate-actions-procedures",
        "source_type": "exchange_official_doc",
        "publisher": "Eurex",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Eurex documents adjustments to equity derivatives caused by corporate actions and the goal of preserving contract values.",
        "limitations": ["Exchange-specific derivatives source; equity, index, and futures roll policies differ."],
    },
    "nasdaq_corporate_actions_manual": {
        "source_title": "Corporate Actions and Events Manual Equities",
        "source_url": "https://indexes.nasdaqomx.com/docs/Corporate_Actions_and_Events_Manual_Equities.pdf",
        "source_type": "index_provider_manual",
        "publisher": "Nasdaq",
        "published_at": None,
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "evidence_summary": "Nasdaq manual documents equity corporate action and event treatment in index data contexts.",
        "limitations": ["Index-provider methodology; not a universal adjustment rule for every trading dataset."],
    },
    "ice_corporate_actions": {
        "source_title": "ICE Reference Data: Corporate Actions",
        "source_url": "https://developer.ice.com/fixed-income-data-services/catalog/ice-reference-data-corporate-actions",
        "source_type": "reference_data_provider_doc",
        "publisher": "ICE",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "ICE describes corporate action reference data for operational and risk-management workflows.",
        "limitations": ["Provider product page; use as supporting evidence for the need for corporate-action reference data."],
    },
}


TOPICS: list[dict[str, Any]] = [
    {
        "task": "P37-B-D01",
        "slug": "timestamp_alignment_required",
        "subdomain": "timestamp_alignment",
        "claim_type": "data_contract_rule",
        "statement": "交易研究、回测、训练和复盘使用市场数据前，必须声明事件时间、接收时间、bar 起始/结束时间和决策时间的含义；缺少时间角色定义时不得进行特征对齐或标签归因。",
        "applies_when": ["接入 trade、quote、OHLCV、订单簿或特征表", "构建训练样本、回测样本、标签或交易复盘数据"],
        "not_applicable_when": ["只展示原始数据字段说明且不做对齐、训练或回测", "外部数据源已经提供经过审计的时间角色映射且当前只保存引用"],
        "sources": ["databento_common_fields", "databento_trades", "databricks_point_in_time", "ibm_data_leakage"],
    },
    {
        "task": "P37-B-D02",
        "slug": "timezone_policy_required",
        "subdomain": "timezone_policy",
        "claim_type": "data_contract_rule",
        "statement": "交易数据管线必须明确存储时区、展示时区、交易所本地时区和夏令时处理策略；缺少时区策略的数据不得直接用于跨市场对齐、回测或训练。",
        "applies_when": ["跨市场、跨交易所、跨日历或跨时区处理行情和成交数据", "把数据库时间戳、交易所时间和模型决策时间联动"],
        "not_applicable_when": ["单一静态文本日期字段且不参与排序、对齐、训练或回测", "上游已提供不可变 UTC 时间戳并通过数据质量报告验证"],
        "sources": ["postgres_datetime", "postgres_invalid_datetime", "databento_common_fields", "databricks_point_in_time"],
    },
    {
        "task": "P37-B-D03",
        "slug": "missing_bar_detection_required",
        "subdomain": "data_quality",
        "claim_type": "data_quality_gate",
        "statement": "OHLCV 或区间聚合行情在用于回测、特征计算或训练前，必须检测缺失 bar、空区间和 forward-fill 规则；缺失数据不能默认为真实无波动。",
        "applies_when": ["使用分钟线、小时线、日线或自定义区间聚合数据", "基于 OHLCV 计算指标、触发信号、回测或训练"],
        "not_applicable_when": ["事件级 tick/trade 流尚未聚合成固定区间", "数据源明确声明空区间语义且策略不依赖该区间"],
        "sources": ["databento_ohlcv", "databento_bbo", "great_expectations_core", "great_expectations_home"],
    },
    {
        "task": "P37-B-D04",
        "slug": "duplicate_event_detection_required",
        "subdomain": "data_quality",
        "claim_type": "data_quality_gate",
        "statement": "交易事件、quote 更新、bar 或特征记录进入研究数据集前，必须定义唯一键和重复检测策略；重复事件不得被静默计入成交量、特征窗口或训练标签。",
        "applies_when": ["从交易所、vendor、缓存或重放系统合并数据", "数据会影响成交量、指标、标签、回测成交或训练样本"],
        "not_applicable_when": ["原始日志保留阶段且明确不会被用于指标、标签或回测", "上游提供幂等事件 ID 且下游只做只读审计"],
        "sources": ["databento_trades", "databento_common_fields", "great_expectations_core", "iceberg_spec"],
    },
    {
        "task": "P37-B-D05",
        "slug": "ohlcv_schema_required",
        "subdomain": "ohlcv_schema",
        "claim_type": "schema_contract_rule",
        "statement": "OHLCV 数据用于策略、回测、训练或审计前，必须定义 open、high、low、close、volume、interval、symbol、时间戳和空区间语义；不能只凭字段名假设数据可用。",
        "applies_when": ["导入或生成 OHLCV/K 线数据", "把 OHLCV 作为指标、信号、标签、回测或审计输入"],
        "not_applicable_when": ["只处理非 OHLCV 的事件级订单或成交流", "OHLCV 仅作为图表展示且不进入决策、训练或审计"],
        "sources": ["databento_ohlcv", "databento_common_fields", "great_expectations_core", "databento_bbo"],
    },
    {
        "task": "P37-B-D06",
        "slug": "feature_timestamp_required",
        "subdomain": "feature_timestamp",
        "claim_type": "leakage_boundary_rule",
        "statement": "任何交易特征必须携带 feature_timestamp、available_time 或等价可用时间，并证明特征在决策时间之前可用；不能用未来可见字段生成训练或回测特征。",
        "applies_when": ["构建 AI scoring/gating、回测特征、策略信号或离线训练集", "跨表 join 市场数据、特征表和标签表"],
        "not_applicable_when": ["纯事后复盘报告且明确不作为训练或决策输入", "特征只是人工说明文本，不参与模型或回测"],
        "sources": ["databricks_point_in_time", "databricks_declarative_features", "ibm_data_leakage", "databento_common_fields"],
    },
    {
        "task": "P37-B-D07",
        "slug": "data_versioning_required",
        "subdomain": "data_versioning",
        "claim_type": "reproducibility_rule",
        "statement": "用于回测、训练、评估或审计的数据集必须记录数据版本、快照或可复现引用；无法定位数据版本的结果不得宣称可复现。",
        "applies_when": ["发布回测报告、训练集、评估集、shadow/paper 结果或审计结论", "需要比较不同模型、策略或数据修复前后的结果"],
        "not_applicable_when": ["一次性探索性查看且不保存结论", "外部项目事实层已经提供不可变数据快照引用"],
        "sources": ["iceberg_spec", "iceberg_home", "dvc_start", "dvc_versioning"],
    },
    {
        "task": "P37-B-D08",
        "slug": "symbol_contract_normalization_required",
        "subdomain": "symbology",
        "claim_type": "data_contract_rule",
        "statement": "跨市场或跨供应商使用 symbol、合约、连续合约或 instrument_id 前，必须建立规范化映射和版本记录；不能把同名 symbol 当作同一交易对象。",
        "applies_when": ["整合交易所、vendor、内部订单、回测和模型特征中的 symbol/instrument 字段", "处理期货、期权、永续、连续合约或换月数据"],
        "not_applicable_when": ["单一供应商、单一市场、单一不可变 instrument_id 的只读展示", "外部项目只传入已审计 canonical instrument_id"],
        "sources": ["databento_symbology", "databento_instrument_definitions", "iceberg_spec", "great_expectations_core"],
    },
    {
        "task": "P37-B-D09",
        "slug": "corporate_action_or_contract_rollover_policy",
        "subdomain": "adjustment_rollover",
        "claim_type": "data_adjustment_boundary_rule",
        "statement": "股票复权、指数成分调整、派息拆股、期货换月或合约展期必须声明调整/换月政策；原始数据和调整后数据不得混用来评估策略质量。",
        "applies_when": ["使用股票、指数、期货、期权或连续合约历史数据", "比较跨长期样本、跨合约或跨 corporate action 前后的表现"],
        "not_applicable_when": ["只分析短期未发生调整/换月的原始事件流", "外部项目明确只保存 raw 数据且不做收益、指标或策略评估"],
        "sources": ["eurex_corporate_actions", "nasdaq_corporate_actions_manual", "ice_corporate_actions", "databento_instrument_definitions"],
    },
    {
        "task": "P37-B-D10",
        "slug": "outlier_detection_required",
        "subdomain": "data_quality",
        "claim_type": "data_quality_gate",
        "statement": "行情、成交、bar、spread 或特征数据进入回测和训练前，必须定义异常值检测与处置策略；异常值修复不得静默改变策略或模型评估结论。",
        "applies_when": ["数据中可能存在坏 tick、错误价格、极端 spread、重复成交或 vendor 修正", "异常值会影响指标、信号、标签、训练或回测成交"],
        "not_applicable_when": ["异常值仅用于原始审计日志保留且不进入计算", "人工复盘故意查看异常事件而非训练或回测"],
        "sources": ["great_expectations_core", "great_expectations_home", "databento_ohlcv", "databento_trades"],
    },
    {
        "task": "P37-B-D11",
        "slug": "raw_vs_adjusted_data_boundary",
        "subdomain": "raw_adjusted_boundary",
        "claim_type": "data_boundary_rule",
        "statement": "交易数据必须区分 raw、cleaned、adjusted、feature-ready 和 label-ready 层；不能把调整后价格、清洗后 bar 或训练特征回写污染原始数据层。",
        "applies_when": ["建立行情湖、研究数据集、特征表、训练集或回测缓存", "需要审计数据清洗、复权、修复、特征和标签的来源链路"],
        "not_applicable_when": ["只保存单次人工下载文件且不做下游训练或回测", "外部事实层已经以只读方式提供不可变 raw layer"],
        "sources": ["iceberg_spec", "dvc_versioning", "great_expectations_core", "nasdaq_corporate_actions_manual"],
    },
    {
        "task": "P37-B-D12",
        "slug": "data_quality_report_required",
        "subdomain": "data_quality_report",
        "claim_type": "audit_report_rule",
        "statement": "用于交易回测、训练、评估或上线前审计的数据集必须产出数据质量报告，至少覆盖时间范围、缺失、重复、异常值、schema 版本、来源和修复记录。",
        "applies_when": ["发布回测、训练、模型评估、shadow/paper 或交易审计报告", "数据将被外接 AI IDE、MCP/SearchLab 或交易系统复用"],
        "not_applicable_when": ["临时探索且不保存结论", "只读取已经通过等价质量报告审计的正式数据集"],
        "sources": ["great_expectations_core", "great_expectations_home", "iceberg_spec", "dvc_versioning"],
    },
]


def source_refs(keys: list[str]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for idx, key in enumerate(keys, start=1):
        source = dict(SOURCE_CATALOG[key])
        source.update(
            {
                "source_id": f"src_{idx:03d}",
                "accessed_at": TODAY,
                "version": None,
                "relevance": "high" if idx <= 3 else "medium_high",
                "quoted_excerpt_allowed": False,
            }
        )
        refs.append(source)
    return refs


def normalize_claim(slug: str) -> str:
    return f"data_engineering.{slug}.v1"


def proposed_knowledge_id(slug: str) -> str:
    return f"kb_02_data_engineering.{slug}.v1"


def candidate_id(slug: str) -> str:
    clean = re.sub(r"[^a-z0-9_]+", "_", slug.lower()).strip("_")
    return f"cand_20260611_phase37_data_engineering_{clean}_001"


def build_candidate(topic: dict[str, Any]) -> dict[str, Any]:
    refs = source_refs(topic["sources"])
    primary_count = sum(1 for item in refs if item["score"] >= 84)
    supporting_count = len(refs) - primary_count
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": candidate_id(topic["slug"]),
        "research_task_id": topic["task"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Data Engineering 候选生成完成，等待外部 AI/人工严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": TREE_NODE,
            "canonical_node_id": TREE_NODE,
            "tree_path": TREE_PATH,
            "related_nodes": [
                "kt.trading_engineering",
                "kt.ai_engineering.decision_time_feature_contract",
                "kt.ai_engineering.external_project_memory.memory_schema_lifecycle",
            ],
            "partition_id": PARTITION,
            "domain": "trading_engineering",
            "subdomain": topic["subdomain"],
            "rule_type": topic["claim_type"],
            "claim_type": topic["claim_type"],
            "used_for": [
                "trading_data_contract",
                "backtest_data_audit",
                "ai_training_dataset_boundary",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "本候选主归属 Trading Engineering / Data Engineering；AI Engineering 只能通过 knowledge_refs 引用，不得复制市场数据工程规则本体。",
        },
        "claim": {
            "claim_id": f"claim_{topic['task'].lower().replace('-', '_')}",
            "statement": topic["statement"],
            "normalized_claim": normalize_claim(topic["slug"]),
            "evidence_summary": "; ".join(item["evidence_summary"] for item in refs[:3]),
            "interpretation_notes": "本候选定义交易数据工程边界，不输出买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "event_or_bar",
            "project_type": "trading_ai_support_layer",
            "applies_when": topic["applies_when"],
            "not_applicable_when": [
                *topic["not_applicable_when"],
                "需要具体交易策略参数、账户事实、交易所私有配置、密钥或实盘权限时，应由外接项目事实层处理。",
                "AI Engineering 只能引用本规则，不得把本规则改写为模型训练、MCP 或 RAG 本体规则。",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，而不是某个项目私有数据源配置。",
                "所有数据工程结论必须保留来源、时间戳、版本、schema、修复和验证边界。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "本批来源包含数据供应商、数据库、数据质量框架、特征存储和交易所/指数/参考数据资料，仍需要外部 AI/人工严格审计。",
                "供应商和框架文档只能支撑通用工程边界，不能替代具体外接项目的数据契约。",
                "本候选不提供任何投资建议或实盘执行许可。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high" if primary_count >= 2 else "medium_high",
            "score": round(sum(item["score"] for item in refs) / len(refs), 1),
            "score_version": "phase37_data_engineering_source_scoring_v1",
            "primary_source_count": primary_count,
            "supporting_source_count": supporting_count,
            "low_reliability_source_count": sum(1 for item in refs if item["score"] < 70),
            "mandatory_downgrades": [],
            "limitations": [
                "正式入库前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "vendor/framework 文档按其自身产品适用，不能自动泛化为所有交易所或所有数据平台实现。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "Phase 36/38/40/41 AI Engineering 知识边界",
                "现有 KB_01_QUANT_FOUNDATION formal 知识",
                "Phase 37 Trading 与 AI 跨分支引用契约",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与可见正式知识的直接冲突；本候选只定义 Trading Engineering 数据工程规则本体，AI Engineering 只能引用。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检索 Trading Engineering 数据工程规则本体。",
                "用于审计交易项目方案中是否缺少时间戳、schema、版本、数据质量和调整边界。",
                "用于辅助外接项目设计数据契约、质量报告、训练集和回测数据审计清单。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把候选知识当作 approved、default guidance 或 hard gate。",
                "不得绕过外接项目事实、数据供应商契约、风控 hard gate 或人工治理流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 37 Data Engineering candidate audit does not allow default guidance; formal reviewed requires a later gate.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
        },
        "review": {
            "confidence": "medium_high",
            "freshness": "mixed",
            "reviewer": "codex_pre_audit_generation",
            "reviewed_at": TODAY,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 claim？",
                "是否需要补充更强的一手交易所、数据供应商、数据库或数据质量资料？",
                "是否存在与现有 Data Engineering 或 AI Engineering formal 知识的重叠，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 37 P37-B Data Engineering 队列生成 Trading Engineering 候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录公开专业资料、官方文档、交易所/指数/参考数据资料和数据质量框架来源摘要。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "classified",
                    "reason": f"归类到 {PARTITION} / {TREE_NODE} / {topic['subdomain']}。",
                },
            ],
        },
        "workflow": {
            "stage": "candidate_ready",
            "allowed_next_decisions": [
                "accepted_for_draft",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "forbidden_decisions": [
                "reviewed",
                "approved",
                "default_guidance",
                "hard_gate",
            ],
            "formal_knowledge_id": proposed_knowledge_id(topic["slug"]),
            "formalization_allowed": False,
            "formalization_notes": "只有外部 AI/人工严格审计通过后，才能按 Phase 32 流程转 formal reviewed/caveat_only。",
        },
        "conversion_target": {
            "proposed_knowledge_id": proposed_knowledge_id(topic["slug"]),
            "target_partition_id": PARTITION,
            "target_tree_node_id": TREE_NODE,
            "target_review_status": "draft_after_audit_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "contribution": {
            "source": "codex_research_ingestion",
            "private_data_removed": True,
            "contains_project_private_facts": False,
            "contains_trade_secrets": False,
        },
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 candidates, got {len(candidates)}")
    ids = [item["candidate_id"] for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item["candidate_id"]
        if item["classification"]["canonical_node_id"] != TREE_NODE:
            failures.append(f"{cid}: wrong canonical_node_id")
        if item["classification"]["partition_id"] != PARTITION:
            failures.append(f"{cid}: wrong partition_id")
        if len(item["source_refs"]) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item["source_quality"]["primary_source_count"] < 1:
            failures.append(f"{cid}: primary_source_count < 1")
        if item["status"]["ingestion_decision"] != "candidate_ready":
            failures.append(f"{cid}: not candidate_ready")
        if item["machine_gate"]["default_guidance"] != "deny":
            failures.append(f"{cid}: default_guidance must be deny")
        text = json.dumps(item, ensure_ascii=False)
        if "�" in text or "????" in text:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", text, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase37_data_engineering_candidate_quality_gate",
        "checked_at": TODAY,
        "candidate_count": len(candidates),
        "expected_count": 12,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": warnings,
        "policy": {
            "candidate_not_formal": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_candidate_files(candidates: list[dict[str, Any]]) -> None:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    for item in candidates:
        write_json(CAND_DIR / f"{item['candidate_id']}.json", item)


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    rows = [
        "| 任务 | 候选 | 子域 | 来源数 | 主来源数 | 状态 |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for item in candidates:
        rows.append(
            f"| {item['research_task_id']} | `{item['conversion_target']['proposed_knowledge_id']}` | "
            f"{item['classification']['subdomain']} | {len(item['source_refs'])} | "
            f"{item['source_quality']['primary_source_count']} | candidate_ready |"
        )
    content = f"""# Phase 37 Data Engineering 候选研究记录

生成日期：{TODAY}

## 范围

本文件记录 Phase 37 `P37-B` Data Engineering 12 条候选知识的来源选择、分类和边界。所有条目仍是 candidate，不是 formal reviewed，不是 approved，不进入默认指导。

## 来源原则

```text
1. 优先使用数据供应商官方文档、数据库官方文档、数据质量框架、特征存储文档、交易所/指数/参考数据资料。
2. vendor/framework 文档只能支撑通用工程边界，不能替代外接项目自己的数据契约。
3. 时间戳、时区、schema、缺失、重复、异常值、版本、复权/换月必须写明适用边界和不适用场景。
4. 不输出买卖点、仓位、杠杆、止损止盈或实盘执行建议。
```

## 候选清单

{chr(10).join(rows)}

## 下游

```text
docs/audit/phase37_data_engineering_candidate_audit_package_20260611.json
```
"""
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text(content, encoding="utf-8")


def write_generation_report(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> None:
    content = f"""# Phase 37 Data Engineering 候选生成报告

生成日期：{TODAY}

## 本批范围

```text
分支：Trading Engineering
分区：{PARTITION}
批次：P37-B Data Engineering
候选数：{len(candidates)}
质量门禁：{quality['gate_status']}
```

## 已完成

```text
CEK-TA-383 采集并生成 12 条 Data Engineering 候选知识
```

## 交付物

```text
codex-expert-kit/rag/candidates/{PARTITION}/
docs/research/phase37_data_engineering_candidate_research.md
docs/reports/phase37_data_engineering_candidate_generation_report.md
docs/reports/phase37_data_engineering_candidate_quality_gate.json
```

## 运行时注意

本批候选的 `tree_node_id` 和 `canonical_node_id` 统一写入 `kt.trading_engineering.data_engineering`。同时已修正 API/UI 中旧的 alias 跑偏问题，避免 Data Engineering 被统计到 Quant Foundation。

## 停止点

当前应继续导出审计包并进入外部 AI/人工严格审计。审计前不得创建 formal reviewed、approved、default guidance 或 hard gate。
"""
    GENERATION_REPORT.parent.mkdir(parents=True, exist_ok=True)
    GENERATION_REPORT.write_text(content, encoding="utf-8")


def main() -> None:
    candidates = [build_candidate(topic) for topic in TOPICS]
    write_candidate_files(candidates)
    quality = quality_gate(candidates)
    write_json(QUALITY_GATE, quality)
    write_research_report(candidates)
    write_generation_report(candidates, quality)
    if quality["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {quality['failures']}")
    print(
        json.dumps(
            {
                "generated": len(candidates),
                "candidate_dir": str(CAND_DIR),
                "quality_gate": str(QUALITY_GATE),
                "gate_status": quality["gate_status"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
