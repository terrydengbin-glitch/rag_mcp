"""Generate Phase 45 Stress Testing / Scenario Risk candidate knowledge.

This creates candidate and audit-support artifacts only. It does not create
formal reviewed knowledge, approve knowledge, enable default guidance, or
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


TODAY = "2026-06-12"
PHASE = "45"
TASK_ID = "CEK-TA-465"
BATCH = "P45-E Stress Testing / Scenario Risk"
PARTITION = "KB_07_RISK_MANAGEMENT"
TREE_NODE = "kt.risk_management.stress_scenario"

RESEARCH_REPORT = resolve_repo_path("docs", "research", "phase45_stress_scenario_candidate_research.md", start_file=__file__)
GENERATION_REPORT = resolve_repo_path("docs", "reports", "phase45_stress_scenario_candidate_generation_report.json", start_file=__file__)
QUALITY_GATE = resolve_repo_path("docs", "reports", "phase45_stress_scenario_candidate_quality_gate.json", start_file=__file__)


SOURCES: dict[str, dict[str, Any]] = {
    "cpmi_iosco_pfmi": {
        "source_title": "CPMI-IOSCO Principles for Financial Market Infrastructures",
        "source_url": "https://www.iosco.org/library/pubdocs/pdf/IOSCOPD377.pdf",
        "source_type": "professional_body",
        "publisher": "CPMI-IOSCO",
        "reliability": "high",
        "score": 93,
        "freshness": "stable",
        "evidence_summary": "PFMI supports stress testing, liquidity-risk management and extreme-but-plausible scenario analysis for financial market infrastructures.",
        "limitations": ["FMI/CCP-focused principles; must be mapped carefully to trading-system project risk review."],
    },
    "bis_stress_testing_principles": {
        "source_title": "Basel Committee Stress Testing Principles",
        "source_url": "https://www.bis.org/bcbs/publ/d450.htm",
        "source_type": "professional_body",
        "publisher": "Bank for International Settlements / BCBS",
        "reliability": "high",
        "score": 92,
        "freshness": "stable",
        "evidence_summary": "BCBS stress testing principles cover objectives, governance, policies, processes, methodology, resources and documentation for stress-testing frameworks.",
        "limitations": ["Bank/supervisory stress-testing framework; not a CEK-TA trading gate or strategy-performance standard."],
    },
    "bis_ccp_resilience": {
        "source_title": "CPMI-IOSCO Resilience of Central Counterparties: Further Guidance on the PFMI",
        "source_url": "https://www.bis.org/cpmi/publ/d163.pdf",
        "source_type": "professional_body",
        "publisher": "BIS CPMI / IOSCO",
        "reliability": "high",
        "score": 92,
        "freshness": "stable",
        "evidence_summary": "The CCP resilience guidance discusses stress-testing frameworks, credit and liquidity risk exposure, extreme but plausible market conditions, and multiday liquidity stress considerations.",
        "limitations": ["CCP-focused; use as scenario and liquidity-stress pattern, not as project-specific threshold source."],
    },
    "cme_clearing_stress": {
        "source_title": "CME Clearing Stress Testing Practices",
        "source_url": "https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-stress-testing-practices.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CME describes scenario-based clearing stress testing using historical and hypothetical scenarios across price and volatility risk factors.",
        "limitations": ["CME Clearing context; not universal for all venues, brokers or trading projects."],
    },
    "cme_liquidity_stress": {
        "source_title": "CME Clearing Liquidity Risk Management Practices",
        "source_url": "https://www.cmegroup.com/articles/brochures-and-handbooks/101-overview-cme-clearing-liquidity-risk-management-practices.html",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "evidence_summary": "CME describes liquidity stress testing with historical and hypothetical scenarios for clearing liquidity-risk management.",
        "limitations": ["CME Clearing liquidity context; not a universal strategy-liquidity rule."],
    },
    "dtcc_stress_testing": {
        "source_title": "DTCC Stress Testing",
        "source_url": "https://www.dtcc.com/managing-risk/financial-risk-management/stress-testing",
        "source_type": "official_platform_doc",
        "publisher": "DTCC",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "evidence_summary": "DTCC states stress testing measures stress-scenario impact on credit and liquidity exposures and financial resources for each clearing agency.",
        "limitations": ["Clearing-agency risk management context; not a trading-strategy approval source."],
    },
    "fia_automated_controls_2024": {
        "source_title": "Best Practices for Automated Trading Risk Controls and System Safeguards",
        "source_url": "https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf",
        "source_type": "professional_body",
        "publisher": "FIA",
        "reliability": "high",
        "score": 90,
        "freshness": "time_sensitive",
        "evidence_summary": "FIA covers automated trading risk controls, exchange volatility controls, post-trade analysis, testing and system safeguards.",
        "limitations": ["Industry best practice; not a binding rule and not a CEK-TA threshold source."],
    },
}


ITEMS: list[dict[str, Any]] = [
    {
        "task": "P45-E-STRESS01",
        "slug": "scenario_stress_test_required",
        "title": "场景压力测试必须声明场景、假设和 owner",
        "statement": "交易系统的压力测试必须声明 historical、hypothetical、reverse 或 combined scenario 的来源、冲击变量、时间范围、覆盖资产、数据版本、模型假设、owner 和复核频率；不能只用单一回测最大回撤替代场景压力测试。",
        "claim_type": "scenario_stress_test_rule",
        "sources": ["cpmi_iosco_pfmi", "bis_stress_testing_principles", "cme_clearing_stress"],
    },
    {
        "task": "P45-E-STRESS02",
        "slug": "liquidity_stress_boundary",
        "title": "流动性压力必须和价格 PnL 压力分开",
        "statement": "流动性压力测试必须单独声明 market depth、bid-ask spread、funding source、settlement/collateral、venue availability 和 liquidation horizon；不能把价格 PnL 冲击等同于可成交性、融资能力或出清能力。",
        "claim_type": "liquidity_stress_boundary_rule",
        "sources": ["cpmi_iosco_pfmi", "bis_ccp_resilience", "cme_liquidity_stress", "dtcc_stress_testing"],
    },
    {
        "task": "P45-E-STRESS03",
        "slug": "correlation_breakdown_caveat",
        "title": "相关性在压力下可能失效",
        "statement": "压力场景必须显式考虑相关性上升、相关性反转、集中持仓、wrong-way risk 和跨资产共同冲击；不能用常态样本相关性证明组合在压力时期仍然分散。",
        "claim_type": "correlation_breakdown_caveat_rule",
        "sources": ["bis_stress_testing_principles", "bis_ccp_resilience", "cme_clearing_stress"],
    },
    {
        "task": "P45-E-STRESS04",
        "slug": "gap_and_overnight_risk_required",
        "title": "跳空和隔夜风险必须独立审计",
        "statement": "跳空、隔夜、周末、假日、停牌/恢复和 session close/open 风险必须独立建模并声明价格路径不可见性、订单不可执行窗口、保证金/融资变化和数据可用边界；不能假设 intraday continuous market 风险可以覆盖非连续交易时段。",
        "claim_type": "gap_overnight_risk_rule",
        "sources": ["fia_automated_controls_2024", "cme_clearing_stress", "bis_stress_testing_principles"],
    },
    {
        "task": "P45-E-STRESS05",
        "slug": "tail_loss_review_required",
        "title": "尾部亏损必须配合压力场景复核",
        "statement": "尾部亏损复核必须声明 VaR/ES、scenario loss、最大单日/多日损失、liquidity-adjusted loss、模型外事件和样本外覆盖；不能用均值、胜率、Profit Factor 或普通回撤指标替代尾部风险评估。",
        "claim_type": "tail_loss_review_rule",
        "sources": ["bis_stress_testing_principles", "cpmi_iosco_pfmi", "dtcc_stress_testing"],
    },
    {
        "task": "P45-E-STRESS06",
        "slug": "stress_test_not_trade_permission",
        "title": "压力测试通过不等于交易许可",
        "statement": "压力测试结果只能作为风险复核、资本/流动性规划、人工审批、scenario backlog 或风险 owner 决策输入；通过某个压力测试不得直接生成买卖点、仓位、杠杆、止损止盈、实盘放行或 hard gate 结论。",
        "claim_type": "stress_test_permission_boundary_rule",
        "sources": ["bis_stress_testing_principles", "fia_automated_controls_2024", "cpmi_iosco_pfmi"],
    },
]


def source_ref(source_key: str, index: int) -> dict[str, Any]:
    source = dict(SOURCES[source_key])
    source.update({"source_id": f"src_{index:03d}", "accessed_at": TODAY, "version": None, "relevance": "high", "quoted_excerpt_allowed": False})
    return source


def slug_to_file_name(slug: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", slug).strip("_")
    return f"cand_20260612_phase45_stress_scenario_{safe}_001.json"


def build_candidate(item: dict[str, Any]) -> dict[str, Any]:
    refs = [source_ref(key, idx + 1) for idx, key in enumerate(item["sources"])]
    primary_types = {"professional_body", "official_exchange_doc", "official_platform_doc"}
    source_score = round(sum(float(ref["score"]) for ref in refs) / len(refs), 2)
    return {
        "schema_version": "1.1.0-candidate",
        "candidate_id": f"cand_20260612_phase45_stress_scenario_{item['task'].lower().replace('-', '_')}_001",
        "research_task_id": item["task"],
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 45 P45-E Stress Testing / Scenario Risk 候选，等待外部严格审计。",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": TREE_NODE,
            "canonical_node_id": TREE_NODE,
            "tree_path": "CEK-TA / Trading Engineering / Risk Management / Scenario Stress Risk",
            "related_nodes": [
                "kt.risk_management.layered_risk_controls",
                "kt.live_execution.resilience_incident_log",
                "kt.trading_engineering.live_execution.execution_tca",
                "kt.trade_analysis.review_reason_code",
            ],
            "partition_id": PARTITION,
            "domain": "risk_management",
            "subdomain": "scenario_stress_risk",
            "rule_type": "stress_risk_boundary_rule",
            "claim_type": item["claim_type"],
            "used_for": [
                "trading_ai_project_design_audit",
                "stress_testing_review",
                "scenario_risk_checklist",
                "external_project_rag_retrieval",
            ],
            "classification_notes": "P45-E 只补压力测试、情景风险和尾部风险边界；不设置任何 CEK-TA 通用风险阈值，不启用 hard gate。",
        },
        "claim": {
            "claim_id": f"claim_{item['task'].lower().replace('-', '_')}",
            "title": item["title"],
            "statement": item["statement"],
            "normalized_claim": f"phase45_stress_scenario.{item['slug']}.v1",
            "evidence_summary": "；".join(ref["evidence_summary"] for ref in refs),
            "interpretation_notes": "本候选只定义压力测试、场景风险、流动性压力、尾部损失和风险复核边界，不输出风险阈值、交易参数或实盘执行建议。",
            "claim_strength": "candidate",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general_with_clearing_venue_broker_and_jurisdiction_caveats",
            "asset": "general",
            "timeframe": "stress_scenario_and_risk_review_context",
            "data_granularity": "portfolio_exposure_scenario_market_liquidity_risk_events",
            "project_type": "trading_ai_support_layer",
            "applies_when": [
                "外接项目需要设计场景压力测试、流动性压力、相关性失效、跳空/隔夜风险、尾部亏损复核或 stress result governance。",
                "AI IDE 需要判断风险评估是否把普通回测指标误当作 stress test。",
                "需要把 scenario result、risk owner、人工审批和 deterministic final gate 分开建模。",
            ],
            "not_applicable_when": [
                "用户要求具体风险阈值、仓位、杠杆、止损止盈、买卖点、交易许可或实盘执行动作。",
                "需要外接项目真实账户、清算、保证金、融资或实时市场事实时，应由外接项目事实层提供。",
                "需要监管资本、清算资源或合规结论时，应由对应机构/合规/legal owner 判断。",
            ],
            "assumptions": [
                "Stress Testing / Scenario Risk 是风险复核与治理上下文，不是策略 alpha。",
                "所有 stress、liquidity、clearing、CCP、banking 和 exchange 来源必须声明适用边界。",
                "候选通过外部审计前不能进入 formal reviewed 知识库。",
            ],
            "limitations": [
                "PFMI、BCBS、CCP、CME、DTCC 来源多为 FMI、银行、清算或交易所风险管理语境，不等同于所有交易项目规则。",
                "压力测试不能替代 live risk gate、market data truth、order truth 或 portfolio owner 决策。",
                "本候选不包含任何项目私有风险阈值或交易参数。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": source_score,
            "score_version": "phase45_source_scoring_v1",
            "primary_source_count": sum(1 for ref in refs if ref["source_type"] in primary_types),
            "supporting_source_count": 0,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "正式 reviewed 前必须由外部审计确认 claim 没有超出来源可证明范围。",
                "FMI、CCP、banking、exchange 来源必须保留 jurisdiction、clearing、venue 和 product caveat。",
                "若后续使用内部 stress_result schema，需要提供 contract extract 或 hash。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "Phase 37 Risk Management formal reviewed knowledge",
                "Phase 45 Layered Risk formal reviewed knowledge",
                "Phase 45 Resilience Incident Log formal reviewed knowledge",
                "Phase 45 Execution TCA formal reviewed knowledge",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与现有 formal reviewed 知识的直接冲突；P45-E 只补场景压力、流动性压力、尾部风险和 stress result governance 边界。",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分 backtest drawdown、scenario stress、liquidity stress、tail loss 和 final gate。",
                "用于生成压力测试设计 checklist、schema review、RAG 检索上下文和风险 reason code。",
                "用于检查外接项目是否把 stress test 通过结果误写成交易许可或默认放行。",
            ],
            "not_allowed": [
                "不得生成具体风险阈值、仓位、杠杆、买卖点、止损止盈、交易许可或实盘执行建议。",
                "不得把候选知识当作 approved 或默认指导。",
                "不得替外接项目启用 hard gate、拒单、停机、撤单或解锁流程。",
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
            "risk_threshold_advice_allowed": False,
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "phase45_stress_scenario_candidate_generated",
                    "reason": "Generated from Phase 45 P45-E task queue with professional, clearing and exchange sources.",
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
            "notes": "Generated for external strict audit; no project account, key, position, threshold, or private strategy data included.",
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    expected = {f"P45-E-STRESS{idx:02d}" for idx in range(1, 7)}
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
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must be false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field")
    return {
        "gate_id": "phase45_stress_scenario_candidate_quality_gate",
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
            "P45-E 只能用于压力测试、场景风险、流动性压力和尾部风险边界，不输出风险阈值或交易许可。",
        ],
    }


def write_research_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 45 Stress Testing / Scenario Risk 候选知识采集记录",
        "",
        "## 范围",
        "",
        "本批次对应 CEK-TA-465 / P45-E，目标是采集 6 条 Stress Testing / Scenario Risk P1 候选知识。",
        "",
        "本批次只生成候选和审计包，不创建 reviewed、approved、default guidance 或 hard gate。",
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
            "1. 不输出风险阈值、仓位、杠杆、买卖点、止损止盈或实盘执行建议。",
            "2. PFMI、BCBS、CCP、CME、DTCC、FIA 来源必须保留机构、清算、venue、产品和治理语境边界。",
            "3. 候选知识必须等待外部严格审计，不得直接进入 formal reviewed。",
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
            "report_id": "phase45_stress_scenario_candidate_generation_report",
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
