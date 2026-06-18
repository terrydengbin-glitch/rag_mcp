"""Import Phase 45 Execution TCA first audit result and prepare supplements.

This script does not create formal reviewed knowledge, approve knowledge,
enable default guidance, or create hard gates. It only:

1. Archives the external audit result as structured JSON.
2. Updates the six Execution TCA candidates to accepted_for_draft or
   needs_more_evidence.
3. Supplements P45-A-TCA03 and P45-A-TCA06 with claim-specific evidence.
4. Exports a supplemental re-audit package for those two candidates.
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
TASK_ID = "CEK-TA-458"
AUDIT_RESULT_ID = "audit_phase45_execution_tca_p45_a_20260612_external_strict_v1"
PACKAGE_ID = "phase45_execution_tca_candidate_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_execution_tca_supplemental_reaudit_package_20260612"
PARTITIONS = ["KB_06_LIVE_EXECUTION", "KB_07_TRADE_ANALYSIS"]

AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_execution_tca_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_execution_tca_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_execution_tca_supplemental_reaudit_package_quality_gate.json", start_file=__file__)


DECISIONS: dict[str, dict[str, Any]] = {
    "P45-A-TCA01": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "CFA 直接支撑 implementation shortfall、显性/隐性成本、market impact、delay 和 opportunity cost。",
        "required_followups": [
            "将强制措辞收窄为 CEK-TA draft 默认要求。",
            "补充 decision_ts、arrival_price、order_submit_ts、first_fill_ts、avg_fill_price、fee、spread、unfilled_qty、benchmark_price 字段建议。",
            "明确 buy/sell cost 正负号口径。",
        ],
    },
    "P45-A-TCA02": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "CFA 支撑 arrival、VWAP、TWAP 等 benchmark 选择边界；FINRA 只作为 best execution context 辅助。",
        "required_followups": [
            "增加 benchmark registry：arrival / decision / VWAP / TWAP / close / custom。",
            "每个 benchmark 绑定使用目的、适用订单类型、时间窗口、数据源和不可解释范围。",
            "不得从单一 benchmark 表现推出执行整体好坏。",
        ],
    },
    "P45-A-TCA03": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "方向正确，但 FIX ExecutionReport 只能支撑订单/成交事件语义，不能证明 VWAP/TWAP/POV 的算法边界。",
        "required_followups": [
            "补充 FIXatdl、broker algo spec 或交易所/broker VWAP/TWAP/POV 文档。",
            "补充 POV / participation algorithm 定义来源。",
            "把不能绕过订单、风控、流动性和市场状态约束标记为 CEK-TA 内部边界。",
        ],
    },
    "P45-A-TCA04": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "CFA 直接支撑 delay、market impact、spread/fee/slippage 和 opportunity cost 拆分。",
        "required_followups": [
            "明确 unfilled / partial fill / delayed submit 的 opportunity cost 计算边界。",
            "加入 missing_benchmark、missing_arrival_price、missing_order_ts、missing_unfilled_qty reason code。",
            "不得把 execution opportunity cost 误归因成 strategy win-rate 问题。",
        ],
    },
    "P45-A-TCA05": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "FINRA 5310 和 SEC Rule 606 支撑 best execution routing context，但必须保留司法辖区限制。",
        "required_followups": [
            "明确 FINRA/SEC 只适用于对应美国 broker-dealer / NMS / listed options 语境。",
            "routing context 字段分为 market_context、venue_context、order_context、conflict_context、disclosure_context、execution_result。",
            "显式写明 best execution 不等于单一最优成交价。",
        ],
    },
    "P45-A-TCA06": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "执行层来源可支撑 execution/fill/slippage 边界，但不足以支撑 strategy alpha / out-of-sample validation 规则。",
        "required_followups": [
            "补充 strategy research validation、out-of-sample、walk-forward 或 leakage control 来源。",
            "拆分 claim：execution optimization improves implementation cost；若写成 alpha 必须转入策略研究验证流程。",
            "增加 Strategy Research / Backtest validation cross-reference。",
        ],
    },
}


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "fixatdl": {
        "source_title": "FIX Algorithmic Trading Definition Language",
        "source_url": "https://fixtrading.org/standards/fix-algorithmic-trading-definition-language/",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "FIXatdl is a vendor-neutral standard for describing algorithmic trading strategy user interfaces and parameters across order/execution management systems.",
        "limitations": ["Supports algo-parameter semantics; does not define CEK-TA risk or alpha boundaries."],
    },
    "ibkr_algos": {
        "source_title": "IBKR Order Types, Algos and Tools",
        "source_url": "https://www.interactivebrokers.com/en/trading/ordertypes.php",
        "source_type": "broker_official_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR lists broker order types and algos as execution tools used to limit risks, speed execution, support price improvement and simplify trading process.",
        "limitations": ["Broker-specific; not a universal market standard."],
    },
    "ibkr_vwap": {
        "source_title": "IBKR VWAP Best Efforts Order",
        "source_url": "https://www.interactivebrokers.com/campus/trading-lessons/vwap-best-efforts-order-in-ibkr-desktop/",
        "source_type": "broker_official_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR describes VWAP as an algo seeking to achieve the volume-weighted average price over a defined interval.",
        "limitations": ["Broker-specific and product-specific; use only as VWAP execution-algo example."],
    },
    "ibkr_twap": {
        "source_title": "IBKR Time-Weighted Average Price (TWAP)",
        "source_url": "https://www.interactivebrokers.com/campus/trading-lessons/time-weighted-average-price-twap/",
        "source_type": "broker_official_doc",
        "publisher": "Interactive Brokers",
        "reliability": "medium_high",
        "score": 82,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR describes TWAP as an algo designed to attain time-weighted average price during a specified period.",
        "limitations": ["Broker-specific implementation; not CEK-TA mandatory tooling."],
    },
    "bailey_pbo": {
        "source_title": "The Probability of Backtest Overfitting",
        "source_url": "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253",
        "source_type": "paper",
        "publisher": "SSRN",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "Bailey et al. propose a framework to estimate probability of backtest overfitting in investment simulations, supporting independent validation before promoting claims.",
        "limitations": ["Backtest validation source; supports strategy-research boundary, not execution-algo mechanics."],
    },
    "white_reality_check": {
        "source_title": "A Reality Check for Data Snooping",
        "source_url": "https://www.jstor.org/stable/2999444",
        "source_type": "paper",
        "publisher": "Econometrica / JSTOR",
        "reliability": "high",
        "score": 90,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "White's Reality Check addresses data-snooping risk when the same data is reused for inference or model selection.",
        "limitations": ["Methodological source; supports validation workflow, not TCA implementation details."],
    },
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_paths() -> list[Path]:
    paths: list[Path] = []
    for partition in PARTITIONS:
        cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", partition, start_file=__file__)
        paths.extend(sorted(cand_dir.glob("cand_20260612_phase45_execution_tca_*.json")))
    return paths


def source_ref(source_key: str, source_id: str) -> dict[str, Any]:
    source = dict(SUPPLEMENTAL_SOURCES[source_key])
    source.update({"source_id": source_id, "accessed_at": TODAY, "version": None, "quoted_excerpt_allowed": False})
    return source


def upsert_source_refs(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> None:
    existing_urls = {ref.get("source_url") for ref in candidate.get("source_refs", [])}
    source_refs = list(candidate.get("source_refs", []))
    for ref in refs:
        if ref.get("source_url") not in existing_urls:
            source_refs.append(ref)
    candidate["source_refs"] = source_refs
    primary_count = sum(
        1
        for ref in source_refs
        if ref.get("source_type") in {"professional_body_reading", "regulatory_rule", "regulatory_guidance", "official_protocol_doc", "paper"}
    )
    candidate.setdefault("source_quality", {})["primary_source_count"] = primary_count
    candidate["source_quality"]["supporting_source_count"] = len(source_refs) - primary_count
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 70)) for ref in source_refs) / len(source_refs), 2)


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_draft": 4,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "research_task_id": task,
                "decision": data["decision"],
                "confidence": data["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [data["reason"]],
                "required_followups": data["required_followups"],
            }
            for task, data in DECISIONS.items()
        ],
        "global_notes": [
            "审计包边界合格：candidate 审计，禁止 reviewed/approved/default guidance/hard gate。",
            "TCA03 不得用 FIX ExecutionReport 证明 VWAP/TWAP/POV 算法边界。",
            "TCA06 不得用执行成本来源证明 strategy alpha / out-of-sample validation 规则。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def supplement_candidate(candidate: dict[str, Any]) -> None:
    task_id = str(candidate.get("research_task_id"))
    audit_log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if task_id == "P45-A-TCA03":
        upsert_source_refs(
            candidate,
            [
                source_ref("fixatdl", "src_supp_001"),
                source_ref("ibkr_algos", "src_supp_002"),
                source_ref("ibkr_vwap", "src_supp_003"),
                source_ref("ibkr_twap", "src_supp_004"),
            ],
        )
        candidate["claim"]["statement"] = (
            "VWAP、TWAP、POV 或 participation 类算法应被描述为 execution scheduling / participation algorithm；"
            "它们可以帮助描述订单调度、时间切片、成交参与率或基准跟踪，但不是策略 alpha。"
            "CEK-TA 内部边界要求它们不得绕过订单、风控、流动性、市场状态和 venue-specific 约束。"
        )
        candidate["claim"]["evidence_summary"] = (
            "CFA 支撑 execution evaluation；FIXatdl 和 IBKR algo 文档补充算法订单/参数/执行算法语义；"
            "FIX ExecutionReport 仅保留为订单/成交事件 supporting source。"
        )
        candidate.setdefault("applicability", {}).setdefault("limitations", []).append(
            "不能把 broker-specific VWAP/TWAP 说明泛化为所有市场或所有执行算法。"
        )
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_tca03_supplemented",
                "reason": "按首轮审计要求补 FIXatdl、IBKR VWAP/TWAP 和 broker algo 来源，并拆分 execution algorithm scope 与 CEK-TA internal boundary。",
            }
        )
    elif task_id == "P45-A-TCA06":
        upsert_source_refs(
            candidate,
            [
                source_ref("bailey_pbo", "src_supp_001"),
                source_ref("white_reality_check", "src_supp_002"),
            ],
        )
        candidate["claim"]["statement"] = (
            "执行算法、路由算法和 TCA 优化默认只能改善或解释 implementation cost；"
            "如果外接项目想把 execution-derived feature、低滑点或 benchmark outperform 写成 alpha，"
            "必须转入独立策略研究验证流程，并接受样本外、data snooping、过拟合和 leakage 审计。"
        )
        candidate["claim"]["evidence_summary"] = (
            "CFA/QuantConnect 支撑执行层成本和成交模型边界；Bailey PBO 与 White Reality Check 补充策略研究验证、过拟合和 data snooping 边界。"
        )
        candidate["classification"]["related_nodes"] = sorted(
            set(candidate["classification"].get("related_nodes", []) + ["kt.backtest.bias", "kt.kline_strategy.indicators"])
        )
        candidate.setdefault("applicability", {}).setdefault("limitations", []).append(
            "本条不证明任何 execution feature 具有 alpha；只要求若被主张为 alpha，必须另走策略研究验证。"
        )
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase45_tca06_supplemented",
                "reason": "按首轮审计要求补 Bailey PBO 与 White Reality Check，并把强断言改为转入策略研究验证流程。",
            }
        )


def apply_decisions() -> dict[str, Any]:
    updated: list[dict[str, Any]] = []
    missing: list[str] = []
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}
    for path in candidate_paths():
        data = read_json(path)
        task_id = str(data.get("research_task_id"))
        paths_by_task[task_id] = path
        data_by_task[task_id] = data

    for task_id, decision in DECISIONS.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = data_by_task[task_id]
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_execution_tca_first_audit_imported",
                "reason": f"{decision['decision']} / confidence={decision['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "required_followups": decision["required_followups"],
        }
        if decision["decision"] == "accepted_for_draft":
            data["status"]["review_status"] = "accepted"
            data["status"]["ingestion_decision"] = "accepted_for_draft"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "formal_draft_queue"
            data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        elif decision["decision"] == "needs_more_evidence":
            data["status"]["review_status"] = "needs_more_evidence"
            data["status"]["ingestion_decision"] = "needs_more_evidence"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "needs_more_evidence"
            data["workflow"]["allowed_next_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
            supplement_candidate(data)
        data["status"]["updated_at"] = TODAY
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "decision": decision["decision"], "path": str(path)})
    return {"updated": updated, "missing": missing}


def load_supplemented_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths():
        data = read_json(path)
        if data.get("research_task_id") in {"P45-A-TCA03", "P45-A-TCA06"}:
            candidates.append(data)
    return sorted(candidates, key=lambda item: str(item.get("research_task_id")))


def supplemental_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 2:
        failures.append(f"expected 2 supplemented candidates, got {len(candidates)}")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if len(item.get("source_refs", [])) < 5:
            failures.append(f"{cid}: source_refs < 5 after supplement")
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must remain deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if item.get("machine_gate", {}).get(field) is not False:
                failures.append(f"{cid}: {field} must remain false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake detected")
        if re.search(r"\b(api_key|secret|private_key|password)\b", blob, flags=re.IGNORECASE):
            failures.append(f"{cid}: possible secret/private field detected")
    return {
        "gate_id": "phase45_execution_tca_supplemental_reaudit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 2,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 TCA03/TCA06 补证候选；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "TCA03 的 broker algo 文档只能证明算法执行语义，不得泛化为所有市场。",
            "TCA06 的策略验证来源只支撑转入策略研究验证流程，不证明任何 execution feature 具有 alpha。",
        ],
    }


def export_supplemental_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    package = {
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": PHASE,
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering",
            "batch": "P45-A Execution TCA supplemental re-audit",
            "candidate_count": len(candidates),
            "target": "复审首轮 needs_more_evidence 的 P45-A-TCA03 和 P45-A-TCA06，确认补证后是否可进入 accepted_for_draft。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "reviewed_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方文档、协议文档、论文、案例和数据，对补证内容进行严格再审。",
            "P45-A-TCA03：检查 FIXatdl、IBKR VWAP/TWAP/Algo 来源是否足以支撑 VWAP/TWAP/POV 属于 execution scheduling / participation algorithm，而不是策略 alpha。",
            "P45-A-TCA06：检查 Bailey PBO 与 White Reality Check 是否足以支撑 execution-derived alpha 必须转入独立策略研究验证流程。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {"total": 2, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-A-TCA03 | P45-A-TCA06",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "quality_gate": gate,
        "candidates": candidates,
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)


def write_supplemental_research() -> None:
    lines = [
        "# Phase 45 Execution TCA 补证记录",
        "",
        "## 补证目标",
        "",
        "首轮审计中 P45-A-TCA03 与 P45-A-TCA06 被判定为 needs_more_evidence。本文件记录补证来源、claim 收窄和边界修补。",
        "",
        "## P45-A-TCA03 补证",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key in ["fixatdl", "ibkr_algos", "ibkr_vwap", "ibkr_twap"]:
        source = SUPPLEMENTAL_SOURCES[key]
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "修补后 claim：VWAP/TWAP/POV 或 participation 类算法应被描述为 execution scheduling / participation algorithm；它们不是策略 alpha。CEK-TA 内部边界要求它们不得绕过订单、风控、流动性、市场状态和 venue-specific 约束。",
            "",
            "## P45-A-TCA06 补证",
            "",
            "| source_id | 来源 | 类型 | URL | 用途 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for key in ["bailey_pbo", "white_reality_check"]:
        source = SUPPLEMENTAL_SOURCES[key]
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "修补后 claim：execution optimization 默认只能改善或解释 implementation cost；如果要把 execution-derived feature、低滑点或 benchmark outperform 写成 alpha，必须转入独立策略研究验证流程，并接受样本外、data snooping、过拟合和 leakage 审计。",
            "",
            "## 硬边界",
            "",
            "```text",
            "1. 补证不创建 formal reviewed。",
            "2. 补证不创建 approved、default guidance 或 hard gate。",
            "3. 不生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值。",
            "4. broker-specific algorithm docs 只能作为算法执行语义示例。",
            "5. strategy validation papers 只支撑转入策略研究验证流程，不证明执行特征有 alpha。",
            "```",
        ]
    )
    SUPPLEMENTAL_RESEARCH.parent.mkdir(parents=True, exist_ok=True)
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    audit_result = archive_audit_result()
    apply_report = apply_decisions()
    candidates = load_supplemented_candidates()
    gate = supplemental_gate(candidates)
    write_json(SUPPLEMENTAL_GATE, gate)
    export_supplemental_package(candidates, gate)
    write_supplemental_research()
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_execution_tca_audit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "first_audit_summary": audit_result["summary"],
            "updated": apply_report["updated"],
            "missing": apply_report["missing"],
            "supplemental_research": str(SUPPLEMENTAL_RESEARCH),
            "supplemental_package": str(SUPPLEMENTAL_PACKAGE),
            "supplemental_gate": str(SUPPLEMENTAL_GATE),
            "supplemental_gate_status": gate["gate_status"],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "updated_count": len(apply_report["updated"]), "supplemental_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" and not apply_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
