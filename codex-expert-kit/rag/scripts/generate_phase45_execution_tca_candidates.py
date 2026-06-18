"""Generate Phase 45 Execution TCA candidate knowledge.

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
TASK_ID = "CEK-TA-456"
BATCH = "P45-A Execution TCA"

RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase45_execution_tca_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase45_execution_tca_candidate_generation_report.md", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase45_execution_tca_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "cfa_trading_costs": {
        "source_title": "Trading Costs and Electronic Markets",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trading-costs-and-electronic-markets",
        "source_type": "professional_body_reading",
        "publisher": "CFA Institute",
        "reliability": "high",
        "score": 92,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA explains implementation shortfall, explicit and implicit trading costs, market impact, delay cost, opportunity cost, and benchmark limitations in electronic markets.",
        "limitations": ["Professional curriculum source; use for TCA concepts, not as venue-specific execution policy."],
    },
    "cfa_trade_strategy_execution": {
        "source_title": "Trade Strategy and Execution",
        "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/trade-strategy-execution",
        "source_type": "professional_body_reading",
        "publisher": "CFA Institute",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "CFA describes trade cost analysis, execution quality, trading policies, escalation procedures, venue/partner selection, and post-trade evaluation.",
        "limitations": ["Professional reading; not a CEK-TA schema contract and not a direct trading recommendation."],
    },
    "finra_5310": {
        "source_title": "FINRA Rule 5310: Best Execution and Interpositioning",
        "source_url": "https://www.finra.org/rules-guidance/rulebooks/finra-rules/5310",
        "source_type": "regulatory_rule",
        "publisher": "FINRA",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "FINRA Rule 5310 requires reasonable diligence to ascertain the best market and obtain favorable execution under prevailing market conditions.",
        "limitations": ["U.S. broker-dealer rule; not universal to all venues, assets, or jurisdictions."],
    },
    "sec_rule_606_faq": {
        "source_title": "SEC FAQ: Rule 606 of Regulation NMS",
        "source_url": "https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/faq-rule-606-regulation",
        "source_type": "regulatory_guidance",
        "publisher": "U.S. SEC",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "SEC Rule 606 guidance supports order routing disclosure and execution-quality transparency for routing services.",
        "limitations": ["U.S. equity/options disclosure context; use for routing transparency boundary only."],
    },
    "fix_execution_report": {
        "source_title": "FIX 4.4 Execution Report",
        "source_url": "https://fiximate.fixtrading.org/legacy/en/FIX.4.4/body_5756.html",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "stable",
        "evidence_summary": "FIX Execution Report supports order/execution event semantics and the separation of order state, fills, and post-trade reports.",
        "limitations": ["Protocol schema reference; does not define TCA metrics or best-execution obligations."],
    },
    "quantconnect_fills": {
        "source_title": "QuantConnect Reality Modeling: Trade Fills Key Concepts",
        "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
        "source_type": "platform_doc",
        "publisher": "QuantConnect",
        "reliability": "medium_high",
        "score": 78,
        "freshness": "time_sensitive",
        "evidence_summary": "QuantConnect fill modeling docs support the boundary that execution assumptions, fills, slippage, and fees are modeled components rather than strategy edge.",
        "limitations": ["Platform-specific implementation pattern; not a universal execution standard."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-A-TCA01",
        "slug": "implementation_shortfall_required",
        "partition": "KB_07_TRADE_ANALYSIS",
        "tree_node": "kt.trade_analysis.execution_tca_review",
        "tree_path": "CEK-TA / Trading Engineering / Trade Analysis / Execution TCA Review",
        "domain": "trade_analysis",
        "subdomain": "execution_tca_review",
        "title": "Execution TCA 必须记录 implementation shortfall",
        "statement": "执行成本分析必须能表达 implementation shortfall 或等价的 arrival-price 成本口径，并拆分显性费用、隐性成本、市场冲击、延迟成本和机会成本；不能只用成交均价或最终 PnL 判断执行质量。",
        "claim_type": "execution_tca_boundary_rule",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy_execution", "quantconnect_fills"],
    },
    {
        "task": "P45-A-TCA02",
        "slug": "execution_benchmark_selection_boundary",
        "partition": "KB_07_TRADE_ANALYSIS",
        "tree_node": "kt.trade_analysis.execution_tca_review",
        "tree_path": "CEK-TA / Trading Engineering / Trade Analysis / Execution TCA Review",
        "domain": "trade_analysis",
        "subdomain": "execution_tca_review",
        "title": "Execution benchmark 必须声明选择边界",
        "statement": "执行质量复盘必须声明 benchmark 口径，例如 arrival price、decision price、VWAP、TWAP、close price 或自定义 benchmark；不同 benchmark 解释不同问题，不能混用后声称执行好坏。",
        "claim_type": "benchmark_boundary_rule",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy_execution", "finra_5310"],
    },
    {
        "task": "P45-A-TCA03",
        "slug": "vwap_twap_pov_is_algorithm_scope",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.execution_tca",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Execution TCA",
        "domain": "live_trading",
        "subdomain": "execution_tca",
        "title": "VWAP/TWAP/POV 属于执行算法口径",
        "statement": "VWAP、TWAP、POV 或 arrival-price 算法只能描述执行调度和成本控制目标；它们不是策略 alpha、不是交易信号，也不能绕过订单、风控、流动性和市场状态约束。",
        "claim_type": "execution_algorithm_scope_rule",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy_execution", "fix_execution_report"],
    },
    {
        "task": "P45-A-TCA04",
        "slug": "delay_market_impact_opportunity_cost_decomposition",
        "partition": "KB_07_TRADE_ANALYSIS",
        "tree_node": "kt.trade_analysis.execution_tca_review",
        "tree_path": "CEK-TA / Trading Engineering / Trade Analysis / Execution TCA Review",
        "domain": "trade_analysis",
        "subdomain": "execution_tca_review",
        "title": "执行成本必须拆分 delay、impact 和 opportunity cost",
        "statement": "交易执行复盘应拆分 delay cost、market impact、spread/fee/slippage 和 opportunity cost；未成交、部分成交或延迟提交造成的机会成本不能静默忽略，也不能当作策略胜率问题处理。",
        "claim_type": "cost_decomposition_rule",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy_execution", "quantconnect_fills"],
    },
    {
        "task": "P45-A-TCA05",
        "slug": "best_execution_routing_context_required",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.execution_tca",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Execution TCA",
        "domain": "live_trading",
        "subdomain": "execution_tca",
        "title": "Best execution 必须保留 routing context",
        "statement": "best execution 或 routing 质量评审必须保留市场、venue、订单类型、流动性、冲突安排、路由选择、披露和 prevailing market conditions 上下文；不能只用最优价格或单一成交价格判断。",
        "claim_type": "best_execution_context_rule",
        "sources": ["finra_5310", "sec_rule_606_faq", "cfa_trade_strategy_execution"],
    },
    {
        "task": "P45-A-TCA06",
        "slug": "algorithmic_execution_not_strategy_edge",
        "partition": "KB_06_LIVE_EXECUTION",
        "tree_node": "kt.live_execution.execution_tca",
        "tree_path": "CEK-TA / Trading Engineering / Live Execution / Execution TCA",
        "domain": "live_trading",
        "subdomain": "execution_tca",
        "title": "算法执行不能被写成策略 edge",
        "statement": "执行算法、路由算法和 TCA 优化只能改善或解释交易实现成本；除非经过独立研究和样本外验证，否则不能把更低执行成本、VWAP 优于基准或更少滑点写成策略 alpha 或交易信号。",
        "claim_type": "execution_strategy_boundary_rule",
        "sources": ["cfa_trading_costs", "cfa_trade_strategy_execution", "finra_5310", "quantconnect_fills"],
    },
]


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_execution_tca_{safe}_001.json"


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


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, idx + 1) for idx, key in enumerate(item["sources"])]
    cid = f"cand_20260612_phase45_execution_tca_{item['task'].lower().replace('-', '_')}_001"
    primary_count = sum(1 for ref in refs if ref["source_type"] in {"professional_body_reading", "regulatory_rule", "regulatory_guidance"})
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": cid,
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 Execution TCA candidate generated for strict external audit; not formal knowledge.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": item["tree_node"],
            "canonical_node_id": item["tree_node"],
            "tree_path": item["tree_path"],
            "related_nodes": [
                "kt.live_execution.execution_tca",
                "kt.trade_analysis.execution_tca_review",
                "kt.replay_simulation.fill_model",
                "kt.ai_engineering.llm_audit_assistant",
            ],
            "partition_id": item["partition"],
            "domain": item["domain"],
            "subdomain": item["subdomain"],
            "rule_type": "boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "execution_quality_review",
                "trade_cost_analysis_context",
                "external_project_rag_retrieval",
                "ai_trader_project_design_audit",
            ],
            "classification_notes": "主归属 Trading Engineering / Execution TCA；AI Engineering 只能通过 knowledge_refs 引用，不得复制为模型训练或 hard gate 本体。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_execution_tca.{item['slug']}.v1",
            "evidence_summary": "Professional and regulatory sources support TCA, execution-quality, cost-decomposition, benchmark and routing-context boundaries.",
            "interpretation_notes": "本候选只定义执行成本和执行质量审计边界，不输出买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_market_specific_caveats",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "order_and_execution_events",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要评估订单执行质量、交易成本、路由上下文或执行算法边界",
                "AI IDE 需要区分策略信号、订单执行、TCA 和 post-trade review",
                "需要设计 execution report、fill report、cost report、routing context 或 TCA reason code",
            ],
            "not_applicable_when": [
                "用户要求具体买卖点、仓位、杠杆或止损止盈参数",
                "没有订单、成交、费用、滑点、时间戳或 benchmark 数据，无法做执行质量判断",
                "需要 broker/venue 私有路由事实时，应由外接项目事实层和 Live Execution owner 提供",
                "需要监管合规结论时，应由对应司法辖区的合规/法律 owner 判断",
            ],
            "assumptions": [
                "Execution TCA 是交易工程审计上下文，不是策略 edge。",
                "所有 benchmark、venue 和 routing claim 必须声明市场、产品、交易所、订单类型和时间范围。",
                "候选通过外部审计前不能进入正式 reviewed 知识库。",
            ],
            "limitations": [
                "CFA/FINRA/SEC 来源具有专业或辖区边界，不能泛化为所有市场的硬规则。",
                "平台文档只能作为实现示例，不替代 CEK-TA 或外接项目字段契约。",
                "本候选不提供投资建议、风控阈值或实盘执行许可。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": round(sum(ref["score"] for ref in refs) / len(refs), 2),
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": primary_count,
            "supporting_source_count": len(refs) - primary_count,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "监管资料按地区适用，不能自动泛化到 crypto、外汇、非美市场或全部 broker。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Live Execution / Replay / Trade Analysis formal reviewed knowledge",
                "Phase 41 AI scoring boundary",
                "Phase 42 Database/Storage contracts",
                "Phase 45 runtime contract",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有正式知识的直接冲突；Execution TCA 与策略工程、回放仿真、AI scoring 的关系按 owner/reference 边界处理。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分策略信号、执行算法、订单事实和 TCA 复盘。",
                "用于设计 execution-quality reason code、audit checklist、RAG 检索上下文。",
                "用于检查外接项目方案是否遗漏成本、benchmark、routing context 或 opportunity cost。",
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得把执行算法、TCA 指标或 routing 选择写成策略 alpha 或 hard gate。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 45 candidate audit has not passed; formal reviewed requires later gate.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "review": {
            "confidence": "medium",
            "freshness": "mixed",
            "reviewer": "codex_candidate_generation",
            "reviewed_at": TODAY,
            "open_questions": [
                "外部审计是否认为来源足以支撑该 TCA 边界？",
                "是否需要补充更强的一手监管、交易所、broker 或论文来源？",
                "是否存在与 Phase 37 formal reviewed 知识的重复，需要合并或拆分？",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "根据 Phase 45 P45-A Execution TCA 队列生成候选知识。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "sourced",
                    "reason": "记录 CFA、FINRA、SEC、FIX 和平台文档等来源摘要。",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "classified",
                    "reason": f"归类到 {item['partition']} / {item['tree_node']}。",
                },
            ],
        },
        "workflow": {
            "stage": "pending_external_audit",
            "allowed_next_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "forbidden_next_decisions": ["reviewed", "approved", "default_guidance", "hard_gate"],
            "formal_knowledge_id": None,
            "audit_package_id": "phase45_execution_tca_candidate_audit_package_20260612",
        },
        "contribution": {
            "origin": "phase45_research_ingestion",
            "private_data_removed": True,
            "contains_project_private_strategy": False,
            "contains_secret": False,
            "notes": "通用 Trading Engineering 支持层候选知识，不包含外接项目私有交易事实。",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Execution TCA 候选知识采集记录",
        "",
        "## 目标",
        "",
        "本批为 Phase 45 / P45-A / Execution TCA 6 条候选知识。所有条目只进入 candidate，不创建正式 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 来源摘要",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(["", "## 候选条目", "", "| research_task_id | candidate_id | partition | canonical_node_id | 来源数 |", "| --- | --- | --- | --- | --- |"])
    for item in candidates:
        lines.append(
            f"| {item['research_task_id']} | `{item['candidate_id']}` | `{item['classification']['partition_id']}` | `{item['classification']['canonical_node_id']}` | {len(item['source_refs'])} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "```text",
            "1. Execution TCA 只解释执行成本、执行质量、benchmark、routing context 和算法执行边界。",
            "2. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘许可。",
            "3. 不把 VWAP/TWAP/POV/arrival-price 算法写成策略 edge。",
            "4. FINRA/SEC 来源只约束对应辖区和场景，不泛化到所有市场。",
            "5. 候选必须等待外部 AI/人工审计。",
            "```",
        ]
    )
    RESEARCH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 Execution TCA candidates, got {len(candidates)}")
    expected_tasks = {f"P45-A-TCA{idx:02d}" for idx in range(1, 7)}
    actual_tasks = {str(item.get("research_task_id")) for item in candidates}
    if actual_tasks != expected_tasks:
        failures.append(f"unexpected research_task_id set: {sorted(actual_tasks ^ expected_tasks)}")
    ids = [item.get("candidate_id") for item in candidates]
    if len(ids) != len(set(ids)):
        failures.append("duplicate candidate_id detected")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if item.get("status", {}).get("review_status") != "candidate_ready":
            failures.append(f"{cid}: review_status is not candidate_ready")
        if item.get("workflow", {}).get("stage") != "pending_external_audit":
            failures.append(f"{cid}: workflow.stage is not pending_external_audit")
        if item.get("classification", {}).get("canonical_node_id") not in {
            "kt.live_execution.execution_tca",
            "kt.trade_analysis.execution_tca_review",
        }:
            failures.append(f"{cid}: canonical_node_id not in Execution TCA nodes")
        if len(item.get("source_refs", [])) < 3:
            failures.append(f"{cid}: source_refs < 3")
        if item.get("source_quality", {}).get("primary_source_count", 0) < 2:
            failures.append(f"{cid}: primary_source_count < 2")
        gate = item.get("machine_gate", {})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase45_execution_tca_candidate_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "batch": BATCH,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本批只是 Execution TCA candidate，不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "TCA 只能用于执行成本、benchmark、routing context 和执行质量审计，不得证明策略 alpha。",
            "监管来源具有辖区边界，平台来源只能作为实现示例。",
        ],
    }


def main() -> int:
    candidates: list[dict[str, Any]] = []
    for item in ITEMS:
        candidate = build_candidate(item)
        candidates.append(candidate)
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", item["partition"], start_file=__file__)
        write_json(cand_dir / slug_to_file_name(item["slug"]), candidate)
    write_research_report(candidates)
    gate = quality_gate(candidates)
    write_json(QUALITY_GATE, gate)
    write_json(
        GENERATION_REPORT,
        {
            "report_id": "phase45_execution_tca_candidate_generation_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "batch": BATCH,
            "candidate_count": len(candidates),
            "candidate_ids": [item["candidate_id"] for item in candidates],
            "research_report": str(RESEARCH_REPORT),
            "quality_gate": str(QUALITY_GATE),
            "gate_status": gate["gate_status"],
        },
    )
    print(json.dumps({"status": gate["gate_status"], "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
