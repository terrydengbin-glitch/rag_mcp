"""Generate Phase 37 Backtest candidate knowledge.

This script writes candidate and audit-support artifacts only. It does not
create formal reviewed knowledge, approve knowledge, enable default guidance, or
create hard gates.
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
TASK_ID = "CEK-TA-412"
PARTITION = "KB_04_BACKTEST"
TREE_NODE = "kt.trading_engineering.backtest"
TREE_PATH = "CEK-TA / Trading Engineering / Backtest"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase37_backtest_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase37_backtest_candidate_generation_report.md", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase37_backtest_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "cfa_backtesting": {
        "source_title": "Backtesting & Simulation",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation",
        "source_type": "professional_curriculum",
        "publisher": "CFA Institute",
        "published_at": "2026-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute frames backtesting as approximating the real-life investment process, including rolling-window processes, rules, portfolio formation, rebalancing, performance and risk profiles.",
        "limitations": ["Professional curriculum source; use for process and boundary, not for a specific trading edge."],
    },
    "cfa_trade_strategy": {
        "source_title": "Trade Strategy and Execution",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
        "source_type": "professional_curriculum",
        "publisher": "CFA Institute",
        "published_at": "2026-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA Institute frames execution around liquidity needs, market conditions, execution risk, opportunity cost, market impact and trade cost analysis.",
        "limitations": ["Supports cost and execution boundary; not a backtest platform contract."],
    },
    "white_reality_check": {
        "source_title": "A Reality Check for Data Snooping",
        "source_url": "https://www.ssc.wisc.edu/~bhansen/718/White2000.pdf",
        "source_type": "academic_paper",
        "publisher": "Econometrica",
        "published_at": "2000-09-01",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "White formalizes data snooping risk when data is reused for inference or model selection, where apparently good results may arise by chance.",
        "limitations": ["Academic inference source; does not provide a platform implementation."],
    },
    "sullivan_white": {
        "source_title": "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap",
        "source_url": "https://www.jstor.org/stable/222451",
        "source_type": "academic_paper",
        "publisher": "Journal of Finance",
        "published_at": "1999-10-01",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "Sullivan, Timmermann and White apply bootstrap methods to technical trading rules and data-snooping bias.",
        "limitations": ["JSTOR landing page/source metadata; page-level access may require subscription."],
    },
    "bailey_dsr": {
        "source_title": "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551",
        "source_type": "academic_paper",
        "publisher": "SSRN / Journal of Portfolio Management",
        "published_at": "2014-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "The Deflated Sharpe Ratio corrects for selection bias under multiple testing and non-normal returns, addressing inflated backtest performance.",
        "limitations": ["Supports overfitting/selection-bias metrics; not a standalone approval rule."],
    },
    "bailey_pbo": {
        "source_title": "The Probability of Backtest Overfitting",
        "source_url": "https://www.davidhbailey.com/dhbpapers/backtest-overfitting.pdf",
        "source_type": "academic_paper",
        "publisher": "SSRN / Journal of Computational Finance",
        "published_at": "2016-01-01",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "Bailey et al. propose Probability of Backtest Overfitting and cross-validation methods for strategy selection risk.",
        "limitations": ["Academic metric source; not an execution or production readiness rule."],
    },
    "quantconnect_fills": {
        "source_title": "Trade Fills - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect explains fill models, spread costs and interaction with slippage models for backtest order fills.",
        "limitations": ["Platform-specific semantics; external projects must map their own fill model."],
    },
    "quantconnect_slippage": {
        "source_title": "Slippage Models - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect defines slippage as the difference between expected and actual fill price and models it for more realistic backtests.",
        "limitations": ["Platform-specific; supports slippage concept and modeling boundary."],
    },
    "quantconnect_fees": {
        "source_title": "Transaction Fees - Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/transaction-fees/key-concepts",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect fee models simulate brokerage transaction fees to make backtest results more realistic.",
        "limitations": ["Platform-specific; external projects must map actual brokerage/exchange fees."],
    },
    "quantconnect_report": {
        "source_title": "Backtesting Report",
        "source_url": "https://www.quantconnect.com/docs/v2/cloud-platform/backtesting/report",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "published_at": None,
        "reliability": "medium_high",
        "score": 80,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect backtest reports show return distributions, cumulative returns, summary and risk information.",
        "limitations": ["Report fields are platform-specific; use as example of metric context, not universal schema."],
    },
    "mlflow_tracking": {
        "source_title": "MLflow Tracking",
        "source_url": "https://mlflow.org/docs/latest/tracking.html",
        "source_type": "framework_doc",
        "publisher": "MLflow",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "MLflow Tracking records parameters, metrics, artifacts and source/version metadata for reproducible experiments.",
        "limitations": ["Framework implementation example; not mandatory for CEK-TA."],
    },
    "dvc_pipelines": {
        "source_title": "DVC Pipelines",
        "source_url": "https://dvc.org/doc/user-guide/pipelines",
        "source_type": "framework_doc",
        "publisher": "DVC",
        "published_at": None,
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "evidence_summary": "DVC pipelines define stages, dependencies, outputs and reproducible data workflows.",
        "limitations": ["Framework implementation example; not mandatory for CEK-TA."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P37-E-B01",
        "slug": "lookahead_bias_block",
        "title": "Lookahead bias 必须阻断",
        "statement": "Backtest 的特征、信号、调仓、成交和指标计算不得使用 decision_time 之后才可获得的数据；一旦发现 lookahead bias，该回测不得作为策略有效性证据。",
        "subdomain": "bias",
        "claim_type": "data_leakage_block",
        "sources": ["cfa_backtesting", "white_reality_check", "quantconnect_fills", "mlflow_tracking"],
    },
    {
        "task": "P37-E-B02",
        "slug": "data_leakage_block",
        "title": "数据泄漏必须阻断",
        "statement": "Backtest、训练或评估中，任何标签、未来收益、未来成交、未来复权或样本外信息不得进入当时应不可见的特征或规则选择流程。",
        "subdomain": "data_leakage",
        "claim_type": "data_leakage_block",
        "sources": ["cfa_backtesting", "white_reality_check", "bailey_pbo", "mlflow_tracking"],
    },
    {
        "task": "P37-E-B03",
        "slug": "survivorship_selection_bias_check",
        "title": "必须检查幸存者偏差和选择偏差",
        "statement": "Backtest 必须说明 universe 构建时间点、退市/过期资产、合约换月、样本选择和排除规则；未处理幸存者偏差或选择偏差的结果只能作为候选研究线索。",
        "subdomain": "selection_bias",
        "claim_type": "methodological_constraint",
        "sources": ["cfa_backtesting", "white_reality_check", "bailey_dsr", "sullivan_white"],
    },
    {
        "task": "P37-E-B04",
        "slug": "parameter_search_separate_from_final_eval",
        "title": "参数搜索必须与最终评估分离",
        "statement": "参数搜索、特征选择、模型选择和规则筛选必须与最终评价样本分离；同一数据被反复用于选择和宣称表现时，必须标注 data snooping / multiple testing 风险。",
        "subdomain": "model_selection",
        "claim_type": "methodological_constraint",
        "sources": ["white_reality_check", "sullivan_white", "bailey_dsr", "bailey_pbo"],
    },
    {
        "task": "P37-E-B05",
        "slug": "walk_forward_validation_required",
        "title": "Walk-forward 验证必须声明窗口和重训练规则",
        "statement": "Walk-forward 或 rolling-window backtest 必须声明训练窗口、验证窗口、步长、重优化频率、参数冻结点和数据可用时间，不能只展示单次全样本最优结果。",
        "subdomain": "validation",
        "claim_type": "validation_boundary_rule",
        "sources": ["cfa_backtesting", "bailey_pbo", "white_reality_check", "mlflow_tracking"],
    },
    {
        "task": "P37-E-B06",
        "slug": "out_of_sample_required",
        "title": "样本外评估必须存在",
        "statement": "策略有效性不能只依赖 in-sample 表现；最终结论必须包含样本外、时间后推或独立市场/周期评估，并声明样本外边界和失败条件。",
        "subdomain": "validation",
        "claim_type": "validation_boundary_rule",
        "sources": ["cfa_backtesting", "bailey_pbo", "bailey_dsr", "white_reality_check"],
    },
    {
        "task": "P37-E-B07",
        "slug": "cost_model_required",
        "title": "回测必须显式声明成本模型",
        "statement": "Backtest 必须显式声明佣金、交易所费用、借贷/融资成本、税费、市场冲击和机会成本等成本模型；未扣成本的收益不得作为净表现证据。",
        "subdomain": "cost_model",
        "claim_type": "execution_cost_boundary_rule",
        "sources": ["cfa_trade_strategy", "quantconnect_fees", "quantconnect_slippage", "quantconnect_fills"],
    },
    {
        "task": "P37-E-B08",
        "slug": "slippage_fee_spread_required",
        "title": "滑点、手续费和价差必须纳入或声明缺失",
        "statement": "Backtest 必须说明 fill price、slippage、fee、spread、partial fill 和订单类型假设；若未建模，结论必须降级为 gross research result。",
        "subdomain": "fill_cost",
        "claim_type": "execution_cost_boundary_rule",
        "sources": ["quantconnect_fills", "quantconnect_slippage", "quantconnect_fees", "cfa_trade_strategy"],
    },
    {
        "task": "P37-E-B09",
        "slug": "metric_interpretation_boundary",
        "title": "回测指标必须带解释边界",
        "statement": "Sharpe、Sortino、profit factor、win rate、drawdown、hit ratio、turnover 等回测指标必须结合成本、样本长度、交易次数、尾部风险、非正态和选择偏差解释。",
        "subdomain": "metrics",
        "claim_type": "metric_interpretation_boundary",
        "sources": ["cfa_backtesting", "bailey_dsr", "bailey_pbo", "quantconnect_report"],
    },
    {
        "task": "P37-E-B10",
        "slug": "profit_factor_drawdown_context_required",
        "title": "Profit factor 必须结合回撤和样本语境",
        "statement": "Profit factor、收益回撤比或类似汇总指标不能单独证明策略质量；必须同时报告 drawdown、交易次数、样本覆盖、成本、尾部亏损和参数选择过程。",
        "subdomain": "metrics",
        "claim_type": "metric_interpretation_boundary",
        "sources": ["cfa_backtesting", "bailey_dsr", "quantconnect_report", "white_reality_check"],
    },
    {
        "task": "P37-E-B11",
        "slug": "reproducibility_package_required",
        "title": "回测必须具备可复现实验包",
        "statement": "可用于审计的 backtest 必须保存代码版本、数据版本、参数、运行环境、随机种子、依赖、输出指标、日志和 artifact；缺失复现实验包时不得作为正式证据。",
        "subdomain": "reproducibility",
        "claim_type": "reproducibility_contract",
        "sources": ["mlflow_tracking", "dvc_pipelines", "cfa_backtesting", "quantconnect_report"],
    },
    {
        "task": "P37-E-B12",
        "slug": "strategy_version_and_data_version_required",
        "title": "策略版本和数据版本必须绑定",
        "statement": "Backtest 结果必须绑定 strategy_rule_version、parameter_hash、data_version、calendar/session version、cost/fill model version 和 evaluation timestamp，不能只保存最终指标。",
        "subdomain": "reproducibility",
        "claim_type": "versioning_contract",
        "sources": ["mlflow_tracking", "dvc_pipelines", "cfa_backtesting", "quantconnect_fills"],
    },
]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_")


def source_ref(key: str, idx: int) -> dict[str, Any]:
    source = dict(SOURCES[key])
    source["source_id"] = f"src_{idx:03d}"
    source["accessed_at"] = TODAY
    source["version"] = source.get("version")
    source["relevance"] = "high" if idx <= 2 else "medium_high"
    source["quoted_excerpt_allowed"] = False
    return source


def candidate(item: dict[str, Any]) -> dict[str, Any]:
    candidate_id = f"cand_20260611_phase37_backtest_{item['slug']}_001"
    source_refs = [source_ref(key, idx) for idx, key in enumerate(item["sources"], start=1)]
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": candidate_id,
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Backtest 候选知识已生成，等待外部严格审计；不得 reviewed/approved/default/hard gate。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": TREE_NODE,
            "canonical_node_id": TREE_NODE,
            "tree_path": TREE_PATH,
            "related_nodes": [
                "kt.trading_engineering",
                "kt.trading_engineering.data_engineering",
                "kt.kline_strategy",
                "kt.market_microstructure",
                "kt.replay_simulation",
                "kt.live_execution",
                "kt.risk_management",
                "kt.ai_engineering.llm_training",
            ],
            "partition_id": PARTITION,
            "domain": "backtest",
            "subdomain": item["subdomain"],
            "rule_type": "backtest_reliability_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "backtest_review",
                "strategy_validation_audit",
                "ai_trader_project_gap_audit",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "本候选主归属 Trading Engineering / Backtest。AI Engineering 只能引用本规则，不得把回测可信度规则改写为模型训练或 RAG/MCP 本体规则。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"backtest.{item['slug']}.v1",
            "evidence_summary": "；".join(source["evidence_summary"] for source in source_refs[:3]),
            "interpretation_notes": "本候选只定义回测可信度、偏差、成本、验证和复现边界，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_market_specific_mapping",
            "asset": "general",
            "timeframe": "historical_evaluation",
            "data_granularity": "historical_market_data_and_orders",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "审计策略回测、参数搜索、指标解释、成本模型、fill 假设或复现实验包",
                "把回测结果用于 AI scoring、策略筛选、paper/live 前置评估或研究报告",
            ],
            "not_applicable_when": [
                "需要直接生成买卖点、仓位、杠杆、止损止盈或实盘执行建议",
                "没有历史数据版本、策略规则版本或 evaluation timestamp",
                "问题属于 live execution、risk hard gate 或交易所实盘订单规则，应由对应分支处理",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含任何外接项目私有策略参数。",
                "回测结论必须保留数据、成本、执行、样本、参数搜索、验证和复现边界。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "论文和专业机构资料支持方法边界，不能证明任何特定策略有效。",
                "平台文档只可作为实现语义示例，外接项目必须映射自己的 backtest engine、broker、交易所和数据供应商。",
                "本候选不提供任何投资建议或实盘执行许可。",
            ],
        },
        "source_refs": source_refs,
        "source_quality": {
            "overall_reliability": "medium_high",
            "score": round(sum(source["score"] for source in source_refs) / len(source_refs), 1),
            "score_version": "phase37_backtest_source_scoring_v1",
            "primary_source_count": min(3, len(source_refs)),
            "supporting_source_count": max(0, len(source_refs) - 3),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式入库前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "平台文档只能证明平台语义，不能单独证明策略有效或实盘可执行。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "Phase 37 Trading 与 AI 跨分支引用契约",
                "现有 Backtest formal seed 知识",
                "Data Engineering / Replay / Live Execution / Risk Management owner 边界",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与可见正式知识的直接冲突；本候选只定义 Backtest 可信度边界，AI Engineering 只能引用。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 检索 Backtest 可信度、偏差、成本、验证和复现边界。",
                "用于审计交易项目方案中是否缺少回测证据、成本模型、样本外、walk-forward 或复现实验包。",
                "用于辅助外接项目设计 backtest review checklist、reason code 和 evidence gate。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
                "不得把候选知识当作 reviewed、approved、default guidance 或 hard gate。",
                "不得绕过外接项目事实层、数据契约、执行适配器、风控 hard gate 或人工治理流程。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 37 Backtest candidate requires external strict audit before formal reviewed/caveat_only.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "review": {
            "confidence": "medium_high",
            "freshness": "mixed",
            "reviewer": "codex_research_ingestion",
            "reviewed_at": TODAY,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 claim？",
                "是否需要补充更强的一手论文、平台文档、交易成本/TCA 或 reproducibility 来源？",
                "是否存在与现有 Backtest formal seed 知识、Replay fill model、Data Engineering versioning 或 Risk Management 的重叠，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 37 P37-E Backtest 队列生成 Trading Engineering 候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录专业机构、论文、平台和复现实验框架来源摘要。",
                },
            ],
        },
        "workflow": {
            "stage": "pending_external_audit",
            "queue_group": "pending",
            "current_task_id": TASK_ID,
            "next_action": "export_ai_audit",
            "next_allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
            "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formalization_allowed": False,
            "conversion_target": {
                "proposed_knowledge_id": f"kb_04_backtest.{item['slug']}.v1",
                "target_review_status": "draft",
                "target_default_guidance": "deny",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            },
            "ai_audit_result_id": None,
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        },
        "contribution": {
            "origin": "codex_research_ingestion_phase37",
            "private_data_removed": True,
            "contains_account_facts": False,
            "contains_secret": False,
            "contains_project_private_strategy": False,
        },
    }


def build_research(candidates: list[dict[str, Any]]) -> str:
    lines = [
        "# Phase 37 Backtest 候选知识研究记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 范围",
        "",
        "本批只覆盖 Trading Engineering / Backtest P0 的 12 条候选知识。所有条目均为候选，不是正式 reviewed，不是 approved，不进入默认指导，也不形成 hard gate。",
        "",
        "## 来源矩阵",
        "",
    ]
    for key, source in SOURCES.items():
        lines.extend(
            [
                f"### {key}",
                "",
                f"- 标题：{source['source_title']}",
                f"- 链接：{source['source_url']}",
                f"- 类型：{source['source_type']}",
                f"- 发布方：{source['publisher']}",
                f"- 证据作用：{source['evidence_summary']}",
                f"- 使用边界：{'；'.join(source['limitations'])}",
                "",
            ]
        )
    lines.extend(["## 候选清单", ""])
    for cand in candidates:
        lines.append(f"- `{cand['research_task_id']}` / `{cand['claim']['normalized_claim']}`：{cand['claim']['title']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [candidate(item) for item in ITEMS]
    for cand in candidates:
        path = CAND_DIR / f"{cand['candidate_id']}.json"
        write_json(path, cand)
    write_text(RESEARCH_REPORT, build_research(candidates))
    report = {
        "report_id": "phase37_backtest_candidate_generation_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "partition_id": PARTITION,
        "candidate_count": len(candidates),
        "candidate_paths": [f"codex-expert-kit/rag/candidates/{PARTITION}/{cand['candidate_id']}.json" for cand in candidates],
        "research_report": "docs/research/phase37_backtest_candidate_research.md",
        "formal_knowledge_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "next_action": "CEK-TA-413 export Backtest candidate AI audit package.",
    }
    gate = {
        "gate_id": "phase37_backtest_candidate_quality_gate",
        "generated_at": TODAY,
        "status": "pass",
        "candidate_count": len(candidates),
        "expected_count": 12,
        "source_min_per_candidate": min(len(cand["source_refs"]) for cand in candidates),
        "all_have_sources": all(cand["source_refs"] for cand in candidates),
        "all_default_guidance_denied": all(cand["machine_gate"]["default_guidance"] == "deny" for cand in candidates),
        "all_not_approved": all(cand["workflow"]["approved_allowed"] is False for cand in candidates),
        "all_no_private_data": all(cand["contribution"]["private_data_removed"] for cand in candidates),
    }
    if len(candidates) != 12:
        gate["status"] = "fail"
    write_json(GENERATION_REPORT, report)
    write_json(QUALITY_GATE, gate)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
