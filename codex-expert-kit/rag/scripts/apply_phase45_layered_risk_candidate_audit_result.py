"""Import Phase 45 Layered Risk first audit result.

This script archives the external audit result, updates five candidates to
accepted_for_draft, supplements P45-C-RISK05, and exports a supplemental
re-audit package for that single needs_more_evidence candidate.

It never creates formal reviewed knowledge, approved knowledge, default
guidance, hard gates, risk thresholds, or trading execution advice.
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
TASK_ID = "CEK-TA-462"
AUDIT_RESULT_ID = "audit_phase45_layered_risk_p45_c_20260612_external_strict_v1"
PACKAGE_ID = "phase45_layered_risk_candidate_audit_package_20260612"
SUPPLEMENTAL_PACKAGE_ID = "phase45_layered_risk_supplemental_reaudit_package_20260612"
PARTITION = "KB_07_RISK_MANAGEMENT"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_layered_risk_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase45_layered_risk_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
SUPPLEMENTAL_GATE = resolve_repo_path("docs", "reports", "phase45_layered_risk_supplemental_reaudit_package_quality_gate.json", start_file=__file__)


DECISIONS: dict[str, dict[str, Any]] = {
    "P45-C-RISK01": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "SEC 15c3-5、CME 和 FIA 足以支撑 pre-trade controls 分层边界，但层级 taxonomy 是 CEK-TA 内部分类。",
        "required_followups": [
            "将订单级、账户级、策略级、产品/venue 级、信用/保证金级和系统级标记为 CEK-TA 内部分层 taxonomy。",
            "不得声称 SEC/CME/FIA 逐字要求这些 CEK-TA 字段层级。",
            "不得把分层 pre-trade control 变成默认 hard gate 或自动拒单规则。",
        ],
    },
    "P45-C-RISK02": {
        "decision": "accepted_for_draft",
        "confidence": "medium_high",
        "reason": "SEC/CME 支撑 credit/capital/exposure controls；credit owner 与 strategy risk owner 分离是 CEK-TA owner-boundary 规则。",
        "required_followups": [
            "credit limit owner 与 strategy risk owner 分开应标记为 CEK-TA owner-boundary 规则。",
            "不得从 CME clearing-firm controls 泛化到所有 broker、crypto exchange 或外接账户。",
            "不得输出具体信用额度、资本阈值或账户限制数值。",
        ],
    },
    "P45-C-RISK03": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "SEC FAQ 支撑 price/size parameter controls；CME 支撑 price banding / erroneous-order prevention。",
        "required_followups": [
            "策略信号强度不能绕过价格或数量控制应标记为 CEK-TA 风控边界。",
            "CME price banding 只能作为 CME Globex 示例，不得泛化为所有 venue。",
            "不得输出 price band、max order size 或 fat-finger 阈值数值。",
        ],
    },
    "P45-C-RISK04": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "CME/FIA 支撑 messaging controls 和 automated-trading safeguards。",
        "required_followups": [
            "不得输出 CME MPS、EMT、volume ratio 或 cancel-rate 具体数值作为 CEK-TA 通用阈值。",
            "burst 行为、超限动作、恢复流程应标记为外接项目/venue-specific contract。",
            "需要明确 message pressure 是系统/venue risk，不是成交风险、PnL 风险或策略 alpha。",
        ],
    },
    "P45-C-RISK05": {
        "decision": "needs_more_evidence",
        "confidence": "medium",
        "reason": "CME 来源足以支撑 clearing margin/performance bond，但不足以完整支撑 collateral、available funds、broker buying power、strategy capital budget 和可交易现金误判边界。",
        "required_followups": [
            "补充 broker 官方 margin / buying power / available funds 文档，例如 IBKR、prime broker、clearing broker 或 crypto exchange collateral 文档。",
            "补充 collateral 与 cash balance / available balance / buying power 的字段边界来源。",
            "补充 point-in-time margin/collateral evidence 的数据契约来源。",
            "将不得把任一字段默认为可交易现金保留为 CEK-TA 内部审计边界，而不是 CME 直接结论。",
        ],
    },
    "P45-C-RISK06": {
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reason": "SEC/FIA/CME 支撑 pre-trade controls 与 post-trade analysis 分工。",
        "required_followups": [
            "deterministic gate 应标记为 CEK-TA / 外接项目内部实现边界，不是 SEC/FIA/CME 原文要求。",
            "不得由本候选启用 hard gate、拒单、停机、撤单或解锁流程。",
            "post-trade surveillance 只能做发现、解释、复盘和合规监控，不能替代 pre-trade controls。",
        ],
    },
}


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "ibkr_available_for_trading": {
        "source_title": "Available for Trading Values",
        "source_url": "https://www.ibkrguides.com/traderworkstation/available-for-trading.htm",
        "source_type": "official_broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 88,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR distinguishes Available Funds, Excess Liquidity, Buying Power and related account values, explaining that each value has different trading or cushion semantics.",
        "limitations": ["IBKR-specific account terminology; not a universal broker/account schema."],
    },
    "ibkr_available_funds": {
        "source_title": "Current Available Funds",
        "source_url": "https://www.interactivebrokers.com/campus/glossary-terms/current-available-funds/",
        "source_type": "official_broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 87,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR defines Current Available Funds as equity available for trading, calculated from Equity with Loan Value minus Initial Margin.",
        "limitations": ["IBKR account-segment formulas and terminology are broker-specific."],
    },
    "ibkr_margin_requirements": {
        "source_title": "Margin Requirements",
        "source_url": "https://www.ibkrguides.com/advisorportal/ug/marginrequirements.htm",
        "source_type": "official_broker_doc",
        "publisher": "Interactive Brokers",
        "reliability": "high",
        "score": 87,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "IBKR margin documentation distinguishes margin requirement, available funds, excess liquidity and buying power.",
        "limitations": ["Broker-specific and account-type dependent; not a CEK-TA threshold source."],
    },
    "binance_futures_account_info": {
        "source_title": "USDⓈ-M Futures Account Information V3",
        "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/account/rest-api/Account-Information-V3",
        "source_type": "official_platform_doc",
        "publisher": "Binance Open Platform",
        "reliability": "medium_high",
        "score": 84,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "Binance Futures account information endpoint exposes account-level balance fields such as availableBalance, margin balances and wallet-related values depending on account mode.",
        "limitations": ["Crypto venue/API-specific; field names and semantics depend on product, account mode and jurisdiction availability."],
    },
    "binance_futures_balances": {
        "source_title": "What Is the Available Balance, Margin Balance, and Total Balance on Binance Futures?",
        "source_url": "https://www.binance.com/en/blog/futures/457299340443288694",
        "source_type": "official_platform_article",
        "publisher": "Binance",
        "reliability": "medium",
        "score": 78,
        "freshness": "time_sensitive",
        "relevance": "medium",
        "evidence_summary": "Binance explains that futures wallet balance, available balance, margin balance and total balance serve different purposes and reflect different funds/PnL views.",
        "limitations": ["Official educational article; supporting source only, not a universal account schema."],
    },
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


def candidate_paths() -> list[Path]:
    cand_dir = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
    return sorted(cand_dir.glob("cand_20260612_phase45_layered_risk_*.json"))


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
    primary_types = {"regulatory_rule", "regulatory_guidance", "professional_body", "official_exchange_doc", "official_broker_doc", "official_platform_doc"}
    primary_count = sum(1 for ref in source_refs if ref.get("source_type") in primary_types)
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
            "accepted_for_draft": 5,
            "needs_more_evidence": 1,
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
                "risk_threshold_advice_allowed": False,
                "reasons": [data["reason"]],
                "required_followups": data["required_followups"],
            }
            for task, data in DECISIONS.items()
        ],
        "global_notes": [
            "审计包边界合格：candidate 审计，禁止 reviewed/approved/default guidance/hard gate。",
            "5 条可进入 accepted_for_draft，P45-C-RISK05 需要补 broker/available funds/buying power/collateral 证据。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def supplement_risk05(candidate: dict[str, Any]) -> None:
    upsert_source_refs(
        candidate,
        [
            source_ref("ibkr_available_for_trading", "src_supp_001"),
            source_ref("ibkr_available_funds", "src_supp_002"),
            source_ref("ibkr_margin_requirements", "src_supp_003"),
            source_ref("binance_futures_account_info", "src_supp_004"),
            source_ref("binance_futures_balances", "src_supp_005"),
        ],
    )
    candidate["claim"]["statement"] = (
        "保证金、清算所 performance bond、抵押品、账户 available funds、buying power、excess liquidity、wallet balance、"
        "margin balance 和策略资金预算是不同层级的约束。交易 AI 不得把任一字段默认为可交易现金，也不得在缺少 point-in-time "
        "account/margin/collateral evidence、broker/venue/account-mode 语义和 owner 边界时声称订单具备资金充足性。"
    )
    candidate["claim"]["evidence_summary"] = (
        "CME SPAN / performance bond 来源支撑 clearing margin；IBKR 来源补充 available funds、excess liquidity、buying power 和 margin requirement "
        "字段区别；Binance Futures 来源补充 crypto venue account balance / available balance / margin balance 字段边界。"
    )
    candidate.setdefault("applicability", {}).setdefault("limitations", []).extend(
        [
            "IBKR 字段和公式是 broker/account-type specific，不得泛化为所有 broker。",
            "Binance Futures 字段是 crypto venue/API/product specific，不得泛化为股票、期货、外汇或全部 crypto venue。",
            "CEK-TA 不输出可用资金判断、保证金比例、信用额度或下单许可。",
        ]
    )
    candidate.setdefault("review", {}).setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase45_risk05_supplemented",
            "reason": "按首轮审计要求补 IBKR available funds / buying power / margin requirements 与 Binance Futures account balance 来源。",
        }
    )


def apply_decisions() -> dict[str, Any]:
    paths_by_task: dict[str, Path] = {}
    data_by_task: dict[str, dict[str, Any]] = {}
    for path in candidate_paths():
        data = read_json(path)
        paths_by_task[str(data.get("research_task_id"))] = path
        data_by_task[str(data.get("research_task_id"))] = data

    missing: list[str] = []
    updated: list[dict[str, Any]] = []
    for task_id, decision in DECISIONS.items():
        path = paths_by_task.get(task_id)
        if not path:
            missing.append(task_id)
            continue
        data = data_by_task[task_id]
        data.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": decision["decision"],
            "confidence": decision["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "required_followups": decision["required_followups"],
        }
        data.setdefault("review", {}).setdefault("audit_log", []).append(
            {
                "at": TODAY,
                "actor": "external_ai_strict_audit",
                "action": "phase45_layered_risk_first_audit_imported",
                "reason": f"{decision['decision']} / confidence={decision['confidence']}",
                "audit_result_id": AUDIT_RESULT_ID,
            }
        )
        if decision["decision"] == "accepted_for_draft":
            data["status"]["review_status"] = "accepted"
            data["status"]["ingestion_decision"] = "accepted_for_draft"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "formal_draft_queue"
            data["workflow"]["queue_group"] = "ai_passed"
            data["workflow"]["allowed_next_decisions"] = ["reviewed_preparation", "needs_more_evidence", "rejected"]
        else:
            data["status"]["review_status"] = "needs_more_evidence"
            data["status"]["ingestion_decision"] = "needs_more_evidence"
            data["status"]["decision_reason"] = decision["reason"]
            data["workflow"]["stage"] = "needs_more_evidence"
            data["workflow"]["queue_group"] = "needs_more_evidence"
            data["workflow"]["allowed_next_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
            supplement_risk05(data)
        data["workflow"]["forbidden_next_decisions"] = ["reviewed", "approved", "default_guidance", "hard_gate"]
        data["status"]["updated_at"] = TODAY
        write_json(path, data)
        updated.append({"research_task_id": task_id, "candidate_id": data.get("candidate_id"), "decision": decision["decision"], "path": repo_relative(path)})
    return {"updated": updated, "missing": missing}


def load_supplemented_candidate() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in candidate_paths():
        data = read_json(path)
        if data.get("research_task_id") == "P45-C-RISK05":
            candidates.append(data)
    return candidates


def supplemental_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 1:
        failures.append(f"expected 1 supplemented candidate, got {len(candidates)}")
    for item in candidates:
        cid = item.get("candidate_id", "<unknown>")
        if len(item.get("source_refs", [])) < 8:
            failures.append(f"{cid}: source_refs < 8 after supplement")
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append(f"{cid}: default guidance must remain deny")
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if item.get("machine_gate", {}).get(field) is not False:
                failures.append(f"{cid}: {field} must remain false")
        blob = json.dumps(item, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
    return {
        "gate_id": "phase45_layered_risk_supplemental_reaudit_package_quality_gate",
        "checked_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "package_id": SUPPLEMENTAL_PACKAGE_ID,
        "candidate_count": len(candidates),
        "expected_count": 1,
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只复审 P45-C-RISK05 补证候选；不得直接创建 reviewed、approved、default guidance 或 hard gate。",
            "IBKR/Binance/CME 来源只支撑各自 broker、venue、clearing 或 account-mode 语境，不输出通用资金充足性结论。",
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
            "branch": "Trading Engineering / Risk Management",
            "batch": "P45-C Layered Risk / Credit / Margin supplemental re-audit",
            "candidate_count": len(candidates),
            "target": "复审 P45-C-RISK05，确认补充 IBKR/Binance 资金、buying power、available balance、collateral 证据后是否可进入 accepted_for_draft。",
        },
        "hard_boundaries": {
            "candidate_not_formal": True,
            "accepted_for_draft_not_reviewed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_not_create_formal_knowledge": True,
        },
        "audit_instructions": [
            "必须搜索相关专业网站、官方 broker 文档、交易所文档、清算/保证金资料、案例和数据，对补证内容进行严格再审。",
            "检查 IBKR available funds / buying power / excess liquidity / margin requirements 是否足以补充 broker account 字段边界。",
            "检查 Binance Futures account information / available balance / margin balance 是否足以补充 crypto venue account balance 字段边界。",
            "检查是否仍然保留 CME clearing margin / SPAN / performance bond 与 broker buying power / available funds / collateral 的分层边界。",
            "输出只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked；不得输出 reviewed、approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": SUPPLEMENTAL_PACKAGE_ID,
            "summary": {"total": 1, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P45-C-RISK05",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": False,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
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
        "# Phase 45 Layered Risk RISK05 补证记录",
        "",
        "## 补证目标",
        "",
        "首轮审计中 P45-C-RISK05 被判定为 needs_more_evidence。本文件记录 broker available funds、buying power、crypto venue balance 和 collateral/margin 字段边界补证。",
        "",
        "## 补充来源",
        "",
        "| source_id | 来源 | 类型 | URL | 用途 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for key, source in SUPPLEMENTAL_SOURCES.items():
        lines.append(f"| `{key}` | {source['source_title']} | `{source['source_type']}` | {source['source_url']} | {source['evidence_summary']} |")
    lines.extend(
        [
            "",
            "## 修补后边界",
            "",
            "```text",
            "1. clearing margin / performance bond、broker available funds、buying power、excess liquidity、crypto futures wallet balance、available balance、margin balance 和 strategy capital budget 必须分开。",
            "2. 任一字段都不能被默认为可交易现金。",
            "3. 资金充足性判断必须依赖 point-in-time account/margin/collateral evidence、broker/venue/account-mode 语义和 owner 边界。",
            "4. 本候选不输出保证金比例、信用额度、可用资金判断或下单许可。",
            "```",
        ]
    )
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    audit_result = archive_audit_result()
    apply_report = apply_decisions()
    candidates = load_supplemented_candidate()
    gate = supplemental_gate(candidates)
    write_json(SUPPLEMENTAL_GATE, gate)
    export_supplemental_package(candidates, gate)
    write_supplemental_research()
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_layered_risk_audit_import_report",
            "generated_at": TODAY,
            "phase": PHASE,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "first_audit_summary": audit_result["summary"],
            "updated": apply_report["updated"],
            "missing": apply_report["missing"],
            "supplemental_research": repo_relative(SUPPLEMENTAL_RESEARCH),
            "supplemental_package": repo_relative(SUPPLEMENTAL_PACKAGE),
            "supplemental_gate": repo_relative(SUPPLEMENTAL_GATE),
            "supplemental_gate_status": gate["gate_status"],
            "formal_reviewed_created": 0,
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
            "risk_threshold_advice_enabled": False,
        },
    )
    print(json.dumps({"status": gate["gate_status"], "updated_count": len(apply_report["updated"]), "supplemental_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" and not apply_report["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
