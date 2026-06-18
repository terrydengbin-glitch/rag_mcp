"""Generate Phase 37 Trade Analysis candidate knowledge.

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
TASK_ID = "CEK-TA-442"
PHASE = "37"
PARTITION = "KB_07_TRADE_ANALYSIS"
TREE_NODE = "kt.trade_analysis"
TREE_PATH = "CEK-TA / Trading Engineering / Trade Analysis"

CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase37_trade_analysis_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase37_trade_analysis_candidate_generation_report.md", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase37_trade_analysis_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "cfa_trade_execution": {
        "source_title": "Trade Strategy and Execution",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
        "source_type": "professional_body_reading",
        "publisher": "CFA Institute",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA explains trade evaluation, execution quality, transaction costs, opportunity cost, and benchmark-based trade cost analysis.",
        "limitations": ["Execution-quality source; does not define retail journal taxonomy or CEK-TA reason-code fields."],
    },
    "cfa_performance_attribution": {
        "source_title": "Return-Based, Holdings-Based and Transaction-Based Performance Attribution",
        "source_url": "https://analystprep.com/study-notes/cfa-level-iii/return-based-holdings-based-and-transaction-based-performance-attribution-2/",
        "source_type": "cfa_study_note",
        "publisher": "AnalystPrep / CFA Level III study note",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "Performance attribution can use return-based, holdings-based, or transaction-based inputs depending on data availability and investment process.",
        "limitations": ["Study-note summary; use as supporting source for attribution input boundary, not CEK-TA field contract."],
    },
    "van_tharp_concepts": {
        "source_title": "Tharp Think Trading Concepts",
        "source_url": "https://vantharpinstitute.com/tharp-think-trading-concepts/",
        "source_type": "professional_training_concept",
        "publisher": "Van Tharp Institute",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "evidence_summary": "Van Tharp concepts define initial risk R, R-multiple distributions, expectancy, and SQN-style analysis.",
        "limitations": ["Training concept page; reviewed knowledge should avoid treating it as a formal academic standard."],
    },
    "trademetria_mae_mfe": {
        "source_title": "Understanding MAE and MFE Metrics",
        "source_url": "https://trademetria.com/blog/understanding-mae-and-mfe-metrics-a-guide-for-traders/",
        "source_type": "trading_journal_vendor_education",
        "publisher": "Trademetria",
        "reliability": "medium",
        "score": 70,
        "freshness": "time_sensitive",
        "evidence_summary": "MAE and MFE are described as post-trade metrics for the worst adverse and best favorable move during a trade.",
        "limitations": ["Vendor education; use only as supporting evidence for journal metric semantics."],
    },
    "tradersync_mae_mfe": {
        "source_title": "MFE and MAE Metrics",
        "source_url": "https://tradersync.com/mfe-and-mae-metrics/",
        "source_type": "trading_journal_vendor_education",
        "publisher": "TraderSync",
        "reliability": "medium",
        "score": 70,
        "freshness": "time_sensitive",
        "evidence_summary": "TraderSync explains price and position MAE/MFE as trade-journal analytics, not as entry signals.",
        "limitations": ["Vendor source; should not be used as sole source for formal reviewed claims."],
    },
    "tradezella_rr": {
        "source_title": "Risk-Reward Ratio: How to Calculate and Use It",
        "source_url": "https://www.tradezella.com/blog/risk-reward-ratio",
        "source_type": "trading_journal_vendor_education",
        "publisher": "TradeZella",
        "reliability": "medium",
        "score": 70,
        "freshness": "time_sensitive",
        "evidence_summary": "TradeZella distinguishes planned risk/reward before a trade from R-multiple after exit.",
        "limitations": ["Vendor education; use as supporting source for planned-vs-realized review terminology only."],
    },
    "tradesviz_trade_plan": {
        "source_title": "Mastering Your Trading with R-Value and Profit Factor in TradesViz",
        "source_url": "https://www.tradesviz.com/blog/what-is-r-value-profit-factor/",
        "source_type": "trading_journal_vendor_education",
        "publisher": "TradesViz",
        "reliability": "medium",
        "score": 68,
        "freshness": "time_sensitive",
        "evidence_summary": "TradesViz discusses tagging trades by plan/checklist completion and comparing metrics by trade setup, conditions, and rule adherence.",
        "limitations": ["Vendor workflow example; not a universal trading-quality taxonomy."],
    },
    "quantconnect_results": {
        "source_title": "Backtesting Results",
        "source_url": "https://www.quantconnect.com/docs/v2/cloud-platform/backtesting/results",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect backtest results include charts, orders, logs, statistics and reports, supporting audit-trace and multi-metric review needs.",
        "limitations": ["Platform-specific reporting semantics; not CEK-TA mandatory tooling."],
    },
    "bailey_pbo": {
        "source_title": "The Probability of Backtest Overfitting",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253",
        "source_type": "paper",
        "publisher": "SSRN",
        "reliability": "high",
        "score": 88,
        "freshness": "stable",
        "evidence_summary": "Bailey et al. discuss backtest overfitting risk, supporting that research hypotheses and performance claims require validation rather than anecdotal trade examples.",
        "limitations": ["Backtest-overfitting paper; supports validation boundary, not trade-journal UI fields."],
    },
    "white_reality_check": {
        "source_title": "A Reality Check for Data Snooping",
        "source_url": "https://www.jstor.org/stable/2669537",
        "source_type": "paper",
        "publisher": "Econometrica / JSTOR",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "evidence_summary": "White's reality check addresses data snooping, supporting separation of research hypotheses from validated conclusions.",
        "limitations": ["Methodological source; not a trade-log taxonomy source."],
    },
    "ssrn_execution_quality": {
        "source_title": "The Role of Trading in Portfolio Performance Attribution",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2928963",
        "source_type": "paper",
        "publisher": "SSRN",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "evidence_summary": "The paper discusses execution quality in portfolio performance attribution and limitations of conventional TCA incentives.",
        "limitations": ["Portfolio-trading context; use as supporting source for execution-quality attribution boundary."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P37-H-T01",
        "slug": "planned_vs_realized_r_required",
        "title": "复盘必须区分计划 R 与实际 R",
        "statement": "交易复盘必须区分入场前计划的 risk/reward 或计划 R 与出场后的 realized R；不能只用最终 PnL 判断执行质量。",
        "subdomain": "r_decomposition",
        "claim_type": "trade_review_boundary_rule",
        "sources": ["van_tharp_concepts", "tradezella_rr", "cfa_trade_execution", "quantconnect_results"],
    },
    {
        "task": "P37-H-T02",
        "slug": "mae_mfe_for_post_trade_only",
        "title": "MAE/MFE 只能用于复盘和研究",
        "statement": "MAE/MFE 应作为 post-trade 复盘、止损止盈研究和执行质量分析指标；不能在事前被当作已知路径或直接生成入场/出场建议。",
        "subdomain": "mae_mfe",
        "claim_type": "post_trade_metric_boundary",
        "sources": ["trademetria_mae_mfe", "tradersync_mae_mfe", "cfa_trade_execution", "bailey_pbo"],
    },
    {
        "task": "P37-H-T03",
        "slug": "bad_trade_taxonomy_required",
        "title": "坏交易必须有 taxonomy",
        "statement": "交易复盘必须把坏交易按计划错误、规则破坏、入场质量、出场质量、风险质量、执行质量、市场状态不匹配和数据/系统问题分类，而不是只标记亏损。",
        "subdomain": "bad_case_taxonomy",
        "tree_node": "kt.trade_analysis.bad_case_taxonomy",
        "tree_path": "CEK-TA / Trading Engineering / Trade Analysis / Bad Case Taxonomy",
        "claim_type": "taxonomy_rule",
        "sources": ["tradesviz_trade_plan", "cfa_trade_execution", "quantconnect_results", "cfa_performance_attribution"],
    },
    {
        "task": "P37-H-T04",
        "slug": "good_loss_bad_win_distinction",
        "title": "好亏损和坏盈利必须区分",
        "statement": "复盘必须区分遵守规则但亏损的 good loss 与违反计划但盈利的 bad win；不能把盈利自动标记为好交易，也不能把亏损自动标记为坏交易。",
        "subdomain": "trade_quality_taxonomy",
        "tree_node": "kt.trade_analysis.bad_case_taxonomy",
        "tree_path": "CEK-TA / Trading Engineering / Trade Analysis / Bad Case Taxonomy",
        "claim_type": "trade_quality_taxonomy_rule",
        "sources": ["tradesviz_trade_plan", "tradezella_rr", "van_tharp_concepts", "quantconnect_results"],
    },
    {
        "task": "P37-H-T05",
        "slug": "entry_quality_review_required",
        "title": "入场质量必须独立复盘",
        "statement": "入场质量复盘必须记录信号、触发条件、时间框架、市场状态、计划价差、延迟和是否按规则入场；不能由最终盈亏倒推出入场正确。",
        "subdomain": "entry_quality",
        "claim_type": "trade_review_boundary_rule",
        "sources": ["cfa_trade_execution", "tradesviz_trade_plan", "quantconnect_results", "ssrn_execution_quality"],
    },
    {
        "task": "P37-H-T06",
        "slug": "exit_quality_review_required",
        "title": "出场质量必须独立复盘",
        "statement": "出场质量复盘必须记录计划出场、实际出场、MAE/MFE、滑点、提前/延后出场原因和规则符合性；不能只用是否盈利判断出场质量。",
        "subdomain": "exit_quality",
        "claim_type": "trade_review_boundary_rule",
        "sources": ["trademetria_mae_mfe", "tradersync_mae_mfe", "cfa_trade_execution", "tradezella_rr"],
    },
    {
        "task": "P37-H-T07",
        "slug": "risk_quality_review_required",
        "title": "风险质量必须独立复盘",
        "statement": "风险质量复盘必须记录初始风险 R、实际承担风险、仓位、止损执行、风险变更、规则是否被移动或放宽；不能只用收益覆盖风险问题。",
        "subdomain": "risk_quality",
        "claim_type": "risk_review_boundary_rule",
        "sources": ["van_tharp_concepts", "tradezella_rr", "tradesviz_trade_plan", "cfa_trade_execution"],
    },
    {
        "task": "P37-H-T08",
        "slug": "execution_quality_review_required",
        "title": "执行质量必须独立复盘",
        "statement": "执行质量复盘必须记录订单、成交、滑点、费用、延迟、拒单、撤单、机会成本和 broker/venue/algorithm 表现；不能把策略信号质量和执行质量混在一起。",
        "subdomain": "execution_quality",
        "claim_type": "execution_quality_review_rule",
        "sources": ["cfa_trade_execution", "ssrn_execution_quality", "quantconnect_results", "cfa_performance_attribution"],
    },
    {
        "task": "P37-H-T09",
        "slug": "rule_compliance_review_required",
        "title": "规则符合性必须复盘",
        "statement": "每笔交易必须记录策略规则、入场/出场规则、风控规则和人工 override 是否被遵守；rule compliance 不能由 PnL 替代。",
        "subdomain": "rule_compliance",
        "claim_type": "rule_compliance_review_rule",
        "sources": ["tradesviz_trade_plan", "quantconnect_results", "cfa_trade_execution", "bailey_pbo"],
    },
    {
        "task": "P37-H-T10",
        "slug": "regime_fit_review_required",
        "title": "市场状态适配必须复盘",
        "statement": "交易复盘必须记录市场状态、波动率、流动性、趋势/震荡、交易时段和策略适配情况；不能把单笔输赢直接归因于策略有效或无效。",
        "subdomain": "regime_fit",
        "claim_type": "regime_review_boundary_rule",
        "sources": ["cfa_trade_execution", "cfa_performance_attribution", "ssrn_execution_quality", "bailey_pbo"],
    },
    {
        "task": "P37-H-T11",
        "slug": "reason_code_required",
        "title": "交易复盘必须有 reason code",
        "statement": "交易复盘、LLM scoring 和坏例分析必须使用稳定 reason code 描述交易原因、错误类型、执行问题和风险问题；不能只保存自由文本评论。",
        "subdomain": "reason_code",
        "claim_type": "trade_analysis_schema_rule",
        "sources": ["tradesviz_trade_plan", "quantconnect_results", "cfa_trade_execution", "cfa_performance_attribution"],
    },
    {
        "task": "P37-H-T12",
        "slug": "research_hypothesis_requires_validation",
        "title": "复盘假设必须另行验证",
        "statement": "交易复盘中发现的 pattern、错误归因或改进假设只能作为 research hypothesis，必须经过样本外、参数稳定性、成本和市场状态验证后才能进入策略规则。",
        "subdomain": "research_hypothesis",
        "claim_type": "research_validation_boundary_rule",
        "sources": ["bailey_pbo", "white_reality_check", "cfa_performance_attribution", "van_tharp_concepts"],
    },
]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slug_id(slug: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", slug.lower()).strip("_")


def source_refs(keys: list[str]) -> list[dict[str, Any]]:
    refs = []
    for idx, key in enumerate(keys, start=1):
        source = dict(SOURCES[key])
        source.update(
            {
                "source_id": f"src_{idx:03d}",
                "accessed_at": TODAY,
                "version": None,
                "relevance": "high" if idx <= 2 else "medium_high",
                "quoted_excerpt_allowed": False,
            }
        )
        refs.append(source)
    return refs


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = source_refs(item["sources"])
    tree_node = item.get("tree_node", TREE_NODE)
    tree_path = item.get("tree_path", TREE_PATH)
    slug = slug_id(item["slug"])
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": f"cand_{TODAY.replace('-', '')}_phase37_trade_analysis_{slug}_001",
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 37 Trade Analysis 候选已完成来源采集，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": tree_node,
            "canonical_node_id": tree_node,
            "tree_path": tree_path,
            "related_nodes": [
                "kt.trading_engineering",
                "kt.trade_analysis",
                "kt.quant_foundation.risk_normalized_metrics",
                "kt.risk_management.pre_trade_gates",
                "kt.live_execution",
                "kt.ai_engineering.llm_training",
            ],
            "partition_id": PARTITION,
            "domain": "trade_analysis",
            "subdomain": item["subdomain"],
            "rule_type": "trade_analysis_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trade_review",
                "llm_scoring_label_design",
                "bad_case_taxonomy",
                "external_project_rag_retrieval",
                "ai_trader_project_gap_audit",
            ],
            "classification_notes": "本候选主归属 Trading Engineering / Trade Analysis。AI Engineering 只能引用本规则设计标签、reason code 和 eval case，不得把复盘指标直接改写成交易执行规则。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"trade_analysis.{slug}.v1",
            "evidence_summary": "；".join(source["evidence_summary"] for source in refs[:3]),
            "interpretation_notes": "本候选只定义交易复盘、标签、reason code、质量归因和研究假设边界，不输出买卖点、仓位、杠杆、止损止盈参数或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_strategy_and_venue_context",
            "asset": "general",
            "timeframe": "post_trade_review_and_research",
            "data_granularity": "trade_log_order_log_fill_log_risk_log_market_context",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "审计外接项目的交易复盘、LLM scoring 标签、坏例 taxonomy、reason code、交易质量归因或训练样本描述",
                "把交易日志、订单日志、成交日志、风险日志和市场上下文整理成可复盘、可审计、可训练的数据",
            ],
            "not_applicable_when": [
                "需要生成买卖点、仓位、杠杆、止损止盈或实盘执行建议",
                "问题属于实时风控 gate、订单路由、回测统计或数据工程本体，应由对应分支处理",
                "没有 trade plan、actual execution、market context、risk context 或 audit trace 上下文",
            ],
            "assumptions": [
                "候选用于 CEK-TA 通用支持层知识库，不包含外接项目私有账户事实、密钥或策略参数。",
                "复盘字段必须从交易计划、订单/成交、风险、市场上下文和人工审计记录中可追溯生成。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "交易日志和 journal vendor 资料只能支持复盘模式，不能证明策略有效或可盈利。",
                "复盘结论不能直接改变实盘规则；必须转成 research hypothesis 并经过独立验证。",
                "本候选不提供任何投资建议、实盘许可或风险阈值建议。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "medium_high",
            "score": round(sum(float(source["score"]) for source in refs) / len(refs), 2),
            "score_version": "phase37_trade_analysis_source_scoring_v1",
            "primary_source_count": len([source for source in refs if source["reliability"] in {"high", "medium_high"}]),
            "supporting_source_count": len(refs),
            "low_reliability_source_count": len([source for source in refs if source["reliability"] == "medium"]),
            "mandatory_downgrades": [],
            "limitations": [
                "正式入库前必须由外部审计确认 vendor journal sources 没有被过度使用。",
                "CFA、论文和平台文档只能支持执行质量、归因和验证边界；CEK-TA 字段契约后续需要 reviewed-preparation 再审确认。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": [
                "Phase 37 Trading 与 AI 跨分支引用契约",
                "Quant Foundation R/R 与 R-multiple 边界",
                "Live Execution / Risk Management owner 边界",
                "AI Engineering LLM scoring / label governance 边界",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与可见正式知识直接冲突；候选不创建 reviewed、approved、default guidance 或 hard gate。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 设计交易复盘、坏例 taxonomy、reason code、标签和 eval case 时必须保留计划、实际、风险、执行和市场上下文。",
                "用于审计 LLM scoring / gating 项目是否把 PnL 当作唯一标签或把复盘结论直接写成交易规则。",
                "用于阻止 AI 把复盘指标当作事前路径、实盘许可或默认交易建议。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈参数或实盘订单。",
                "不得把候选知识当作 reviewed、approved、default guidance 或 hard gate。",
                "不得根据单笔交易复盘直接宣布策略有效、无效或可实盘。",
            ],
            "requires_context": [
                "trade_plan_id",
                "strategy_rule_version",
                "risk_policy_id",
                "order_trace_id",
                "fill_trace_id",
                "market_regime",
                "reason_code",
                "reviewer",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; pending external strict audit; not formal reviewed; no default guidance.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "conversion_target": {
            "proposed_knowledge_id": f"kb_07_trade_analysis.{slug}.v1",
            "target_review_status": "candidate_only_pending_external_audit",
            "default_guidance_after_conversion": "deny_until_reviewed_caveat_only_audit",
            "formalization_blockers": ["requires_external_strict_audit"],
        },
        "workflow": {
            "phase": PHASE,
            "task_id": TASK_ID,
            "stage": "pending_external_audit",
            "queue_group": "pending",
            "next_allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formalization_allowed": False,
        },
        "contribution": {
            "origin": "codex_research_ingestion_phase37",
            "private_data_removed": True,
            "contains_account_facts": False,
            "contains_secret": False,
            "contains_project_private_strategy": False,
        },
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 12:
        failures.append(f"expected 12 candidates, got {len(candidates)}")
    expected_tasks = {f"P37-H-T{idx:02d}" for idx in range(1, 13)}
    actual_tasks = {candidate.get("research_task_id") for candidate in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research task set: {sorted(actual_tasks ^ expected_tasks)}")
    for candidate in candidates:
        cid = candidate.get("candidate_id", "<unknown>")
        if candidate.get("classification", {}).get("partition_id") != PARTITION:
            failures.append(f"{cid}: partition mismatch")
        if candidate.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if candidate.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        gate = candidate.get("machine_gate", {})
        if gate.get("default_guidance") != "deny":
            failures.append(f"{cid}: default_guidance must be deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        if len(candidate.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        blob = json.dumps(candidate, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase37_trade_analysis_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "expected_count": 12,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批只是 Trade Analysis candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "Vendor journal sources 只能作为复盘工作流示例，不能单独支撑 reviewed 级字段本体。",
            "复盘发现只能进入 research hypothesis 或 label/eval 设计，不能直接变成实盘交易规则。",
        ],
    }


def write_research_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    lines = [
        "# Phase 37 Trade Analysis Candidate Research",
        "",
        f"- generated_at: {TODAY}",
        f"- task_id: {TASK_ID}",
        f"- partition: {PARTITION}",
        f"- candidate_count: {len(candidates)}",
        f"- gate_status: {gate['gate_status']}",
        "",
        "## 来源种子",
        "",
    ]
    for key, source in SOURCES.items():
        lines.append(f"- `{key}`: {source['source_title']} ({source['publisher']}) - {source['source_url']}")
    lines.extend(["", "## 候选知识点", ""])
    for candidate in candidates:
        lines.append(f"- `{candidate['research_task_id']}` `{candidate['claim']['normalized_claim']}`: {candidate['claim']['statement']}")
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 本批候选只处理 Trade Analysis / 交易复盘规则本体，不处理实盘下单权限、账户事实、仓位建议或策略收益声明。",
            "- AI Engineering 只能引用本批知识设计标签、reason code、eval case 和审计解释，不得复制改写交易规则本体。",
            "- 候选不得直接进入 reviewed、approved、default guidance 或 hard gate。",
        ]
    )
    write_text(RESEARCH_REPORT, "\n".join(lines) + "\n")


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    candidates = [build_candidate(item) for item in ITEMS]
    for candidate in candidates:
        slug = candidate["claim"]["normalized_claim"].split(".")[1]
        path = CAND_DIR / f"cand_{TODAY.replace('-', '')}_phase37_trade_analysis_{slug}_001.json"
        write_json(path, candidate)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_research_report(candidates, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase37_trade_analysis_candidate_generation",
            "generated_at": TODAY,
            "task_id": TASK_ID,
            "partition_id": PARTITION,
            "candidate_count": len(candidates),
            "candidate_dir": str(CAND_DIR),
            "quality_gate": gate,
            "candidate_ids": [candidate["candidate_id"] for candidate in candidates],
            "formal_knowledge_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": 0,
            "hard_gate_enabled": 0,
            "next_action": "CEK-TA-443 export Trade Analysis candidate AI audit package.",
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates), "quality_gate": str(QUALITY_GATE)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
