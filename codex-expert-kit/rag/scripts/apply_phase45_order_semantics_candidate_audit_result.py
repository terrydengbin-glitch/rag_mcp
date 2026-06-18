"""Apply Phase 45 Order Semantics first audit result.

This script archives the external strict audit result, updates the six
Order Semantics candidates to accepted_for_draft, adds reviewed-preparation
contract evidence, and exports a reviewed/caveat_only preparation package.

It never creates reviewed/approved knowledge, default guidance, hard gates,
routing advice, fee optimization advice, order submission permission, or live
trading actions.
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
TASK_ID = "CEK-TA-468"
AUDIT_RESULT_ID = "audit_phase45_order_semantics_candidate_20260612_external_strict"
PACKAGE_ID = "phase45_order_semantics_candidate_audit_package_20260612"
PREP_PACKAGE_ID = "phase45_order_semantics_reviewed_preparation_audit_package_20260612"
PARTITION = "KB_06_LIVE_EXECUTION"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION, start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase45_order_semantics_candidate_audit_import_report.json", start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase45_order_semantics_runtime_contract.md", start_file=__file__)
PREP_PACKAGE = resolve_repo_path("docs", "audit", f"{PREP_PACKAGE_ID}.json", start_file=__file__)
PREP_GATE = resolve_repo_path("docs", "reports", "phase45_order_semantics_reviewed_preparation_gap_report.json", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "research_task_id": "P45-F-ORD01",
        "candidate_id": "cand_20260612_phase45_order_semantics_p45_f_ord01_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "FIX ExecutionReport / order lifecycle 来源足以支撑订单事件、状态、fill、cancel、replace、reject 的审计边界。",
            "Coinbase、CME、Kraken 来源显示不同 venue / product / API 的 order type 行为并不相同，支持 adapter 必须声明 venue-specific semantics。",
            "claim 没有输出买卖点、仓位、杠杆、止损止盈、路由建议、费用优化或订单提交许可。",
        ],
        "required_followups": [
            "进入 reviewed 前补 internal order_semantics schema 或 contract hash。",
            "对 auction、TWAP/VWAP、iceberg 等示例保留 source_ref，不得只靠字符串枚举。",
        ],
        "patch_notes": {
            "source": ["保留 FIX Trading Community、FIX ExecutionReport、CME、Coinbase、Kraken。", "reviewed 前建议补 venue-specific technical rulebook / API version source。"],
            "content": ["保留 order intent、venue accepted order、execution report、fill、reject、expire、audit trace 分层。"],
            "boundary": ["不得生成订单提交许可。", "不得生成撤单/改单动作。", "不得生成交易建议。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD02",
        "candidate_id": "cand_20260612_phase45_order_semantics_p45_f_ord02_001",
        "decision": "accepted_for_draft",
        "confidence": "medium",
        "reasons": [
            "Nasdaq、Coinbase、Binance 直接支撑 TIF 与 venue、session、GTC/GTT/IOC/FOK/GTD、expire/cancel 行为相关。",
            "Binance 对 GTD goodTillDate 延迟 caveat 和 STP 生效条件有明确说明，支持 TIF 不能只作为本地 UI 字段。",
            "CME Confluence / EPICSANDBOX 来源偏弱，但不影响 draft；进入 reviewed 前应替换为生产规格或 rulebook。",
        ],
        "required_followups": [
            "补 FIX ExecutionReport cancel/expire 映射来源。",
            "将 CME sandbox source 替换为 production CME Globex / iLink spec。",
            "补 system clock / timestamp precision / goodTillDate 精度字段表。",
        ],
        "patch_notes": {
            "source": ["保留 Nasdaq、Coinbase、Binance。", "CME sandbox 只能作为辅助，不应作为 reviewed 主证据。"],
            "content": ["TIF 字段必须绑定 venue、session、expire time、partial fill、cancel/expire event 和 clock source。"],
            "boundary": ["不得生成自动撤单。", "不得生成订单提交许可。", "不得生成 session hard gate。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD03",
        "candidate_id": "cand_20260612_phase45_order_semantics_p45_f_ord03_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "Binance Spot LIMIT_MAKER、Binance Futures reduceOnly、Kraken Futures post-only/reduceOnly、Coinbase post-only 规则足以支撑 post-only / reduce-only 是执行约束。",
            "claim 明确 post-only / reduce-only 不等于成交保证、费用节省保证、风险安全保证或交易许可，边界正确。",
            "未发现费用优化、路由建议、强制 reduce 或实盘执行建议。",
        ],
        "required_followups": ["进入 reviewed 前补 position source / reduce-only failure event schema。", "逐 venue 声明 reject、cancel、reprice 或 accepted behavior。"],
        "patch_notes": {
            "source": ["保留 Binance Spot、Binance USD-M Futures、Kraken Futures、Coinbase。"],
            "content": ["post-only 与 reduce-only 必须保留 venue/product/API/account-mode caveat。"],
            "boundary": ["不得生成费用节省保证。", "不得生成安全保证。", "不得生成强制 reduce-only 动作。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD04",
        "candidate_id": "cand_20260612_phase45_order_semantics_p45_f_ord04_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "CME、Coinbase、Binance 来源足以支撑 STP/SMP 需要声明 account / firm / group scope、mode、cancel/decrement/reject 行为。",
            "claim 明确 STP/SMP 不等于防操纵合规结论、成交质量保证或跨 venue 通用规则，边界正确。",
            "未发现 hard gate、自动拒单、撤单或路由策略。",
        ],
        "required_followups": ["进入 reviewed 前补 STP/SMP order event mapping schema。", "补不同 venue 的 STP/SMP mode enum 和 reject/cancel reason code mapping。"],
        "patch_notes": {
            "source": ["保留 CME SMP FAQ、Coinbase STP、Coinbase International rules、Binance Futures API。"],
            "content": ["明确 STP/SMP 是 venue adapter semantics，不是合规结论。"],
            "boundary": ["不得替外接项目启用自动拒单。", "不得生成防操纵合规结论。", "不得生成成交质量保证。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD05",
        "candidate_id": "cand_20260612_phase45_order_semantics_p45_f_ord05_001",
        "decision": "accepted_for_draft",
        "confidence": "medium",
        "reasons": [
            "CME、Nasdaq、Coinbase、Binance、Kraken 来源足以支撑 exchange-specific order behavior 不可泛化的核心 claim。",
            "Coinbase 规则已经覆盖 TWAP、iceberg、RFQ、post-only、maker/taker 等多种平台特有语义；Nasdaq 覆盖多种 TIF / auction-linked 行为。",
            "但 statement 列举项很宽，reviewed 前必须为 market-with-protection、market-to-limit、MOO/MOC/LOC、peg、auction-only、VWAP 等补逐项来源或缩窄列表。",
        ],
        "required_followups": [
            "补 MOO/MOC/LOC、peg、market-to-limit、market-with-protection、VWAP 等逐项来源。",
            "或将示例列表改为“包括但不限于已 source_ref 支撑的类型”。",
            "进入 reviewed 前补 exchange_specific_order_type schema。",
        ],
        "patch_notes": {
            "source": ["保留 CME、Nasdaq、Coinbase、Binance、Kraken。", "reviewed 前补缺失 order type 的 venue rulebook/API 来源。"],
            "content": ["把本条定位为 anti-generalization caveat，不是逐项行为定义。"],
            "boundary": ["不得生成通用订单行为规则。", "不得生成路由建议。", "不得生成订单提交许可。"],
            "conflict": [],
        },
    },
    {
        "research_task_id": "P45-F-ORD06",
        "candidate_id": "cand_20260612_phase45_order_semantics_p45_f_ord06_001",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "SEC EMSAC memo、CFA trading costs、CME fees、Coinbase trading rules 足以支撑 maker/taker、add/remove liquidity、exchange fee、transaction type 必须分开审计。",
            "Coinbase 规则明确非 post-only limit order 可成为 maker、taker 或部分 maker / 部分 taker，支持“limit order 不自动等于 maker 成交”。",
            "claim 明确 maker/taker fee 不得写成策略 alpha、成交质量证明或默认路由规则，边界正确。",
        ],
        "required_followups": [
            "进入 reviewed 前补 fee_evidence schema：venue_fee_schedule_ref、fill_event_ref、liquidity_flag、fee_tier_source、transaction_type。",
            "补具体 venue fee schedule versioning 要求，但不得写真实费率或费率优化建议。",
        ],
        "patch_notes": {
            "source": ["保留 SEC EMSAC、CFA Institute、CME fees、Coinbase trading rules。"],
            "content": ["maker/taker 费用必须绑定成交结果和 fee schedule，不绑定订单类型字符串。"],
            "boundary": ["不得输出费用套利。", "不得输出路由建议。", "不得输出真实费率或费用优化策略。"],
            "conflict": [],
        },
    },
]


SUPPLEMENTAL_SOURCES: dict[str, dict[str, Any]] = {
    "fix_order_state_changes": {
        "source_title": "FIX Trading Community Order State Changes",
        "source_url": "https://www.fixtrading.org/online-specification/order-state-changes/",
        "source_type": "official_protocol_doc",
        "publisher": "FIX Trading Community",
        "reliability": "high",
        "score": 91,
        "freshness": "stable",
        "relevance": "high",
        "evidence_summary": "FIX order-state guidance supports using ExecType and OrdStatus to drive order lifecycle state changes.",
        "limitations": ["Protocol source; does not define venue-specific TIF or adapter behavior."],
    },
    "nasdaq_open_close_crosses": {
        "source_title": "Nasdaq Opening and Closing Crosses FAQ",
        "source_url": "https://nasdaqtrader.com/content/productsservices/trading/crosses/openclose_faqs.pdf",
        "source_type": "official_exchange_doc",
        "publisher": "Nasdaq Trader",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "Nasdaq opening/closing crosses FAQ documents MOO/MOC, LOO/LOC, imbalance-only and auction-specific behavior and cutoffs.",
        "limitations": ["Nasdaq equity auction context; not universal to all venues or assets."],
    },
    "nyse_auctions_fact_sheet": {
        "source_title": "NYSE Opening and Closing Auctions Fact Sheet",
        "source_url": "https://www.nyse.com/publicdocs/nyse/markets/nyse/NYSE_Opening_and_Closing_Auctions_Fact_Sheet.pdf",
        "source_type": "official_exchange_doc",
        "publisher": "NYSE",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "NYSE auction fact sheet documents MOC/LOC order-entry cutoff and closing auction behavior.",
        "limitations": ["NYSE-specific auction context; not a global auction rule."],
    },
    "nyse_pillar_differences": {
        "source_title": "NYSE Pillar Order Type Differences",
        "source_url": "https://www.nyse.com/publicdocs/nyse/markets/nyse/Pillar_Differences.pdf",
        "source_type": "official_exchange_doc",
        "publisher": "NYSE",
        "reliability": "high",
        "score": 84,
        "freshness": "time_sensitive",
        "relevance": "medium_high",
        "evidence_summary": "NYSE Pillar documentation describes peg-order and auction participation differences as venue-specific behavior.",
        "limitations": ["NYSE Pillar-specific; not a universal peg-order definition."],
    },
    "cme_definitions": {
        "source_title": "CME Group Rulebook Definitions",
        "source_url": "https://www.cmegroup.com/rulebook/NYMEX/1/NYMEX-COMEX_Definitions.pdf",
        "source_type": "official_exchange_doc",
        "publisher": "CME Group",
        "reliability": "high",
        "score": 86,
        "freshness": "time_sensitive",
        "relevance": "high",
        "evidence_summary": "CME definitions cover limit order, market-with-protection order and hidden quantity order semantics.",
        "limitations": ["CME/NYMEX/COMEX rulebook context; not a universal futures/crypto/equity definition."],
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
    primary_types = {"official_protocol_doc", "official_exchange_doc", "official_platform_doc", "regulatory_discussion", "professional_body"}
    candidate.setdefault("source_quality", {})["primary_source_count"] = sum(1 for ref in source_refs if ref.get("source_type") in primary_types)
    candidate["source_quality"]["supporting_source_count"] = len(source_refs) - candidate["source_quality"]["primary_source_count"]
    candidate["source_quality"]["score"] = round(sum(float(ref.get("score", 70)) for ref in source_refs) / len(source_refs), 2)


def archive_audit_result() -> dict[str, Any]:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 6,
            "accepted_for_draft": 6,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": [
            {
                "candidate_id": item["candidate_id"],
                "research_task_id": item["research_task_id"],
                "decision": item["decision"],
                "confidence": item["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "risk_threshold_advice_allowed": False,
                "trade_execution_advice_allowed": False,
                "reasons": item["reasons"],
                "required_followups": item["required_followups"],
                "patch_notes": item["patch_notes"],
            }
            for item in RESULTS
        ],
        "global_notes": [
            "本包 6 条 Order Semantics 候选全部 accepted_for_draft。",
            "本轮不得创建 reviewed、approved、default guidance、hard gate、交易许可、路由建议、费用优化或自动撤改单。",
            "下一轮 reviewed/caveat_only 前必须补 internal order_semantics schema、venue-specific enum/reject/fee mapping，ORD05 需补特殊订单类型逐项来源或缩窄列表。",
        ],
    }
    write_json(AUDIT_RESULT_PATH, result)
    return result


def write_contract() -> None:
    CONTRACT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONTRACT_PATH.write_text(
        """# Phase 45 Order Semantics Runtime Contract

## 目标

本契约服务 CEK-TA Phase 45 / P45-F Order Type / TIF / Venue Semantics。它定义外接交易项目在建模 live execution adapter、订单状态机、TIF、post-only/reduce-only、STP/SMP、venue-specific order type 和 maker/taker fee 时必须保留的字段边界。

本契约不是交易策略，不给买卖点、仓位、杠杆、止损止盈、路由建议、费用优化建议、订单提交许可或 hard gate。

## 上游输入

```text
order_intent
venue_order_request
venue_order_ack
execution_report
fill_event
reject_event
cancel_or_replace_event
expire_event
fee_event
position_snapshot
venue_fee_schedule_snapshot
market_session_calendar
```

## 输出契约

### order_semantics_identity

```json
{
  "order_semantics_id": "string",
  "venue": "string",
  "product_type": "spot | futures | options | perpetual | equity | other",
  "api_or_protocol": "FIX | REST | websocket | native | broker_sdk | other",
  "api_version": "string",
  "rulebook_or_spec_ref": "string",
  "adapter_version": "string",
  "semantics_version": "string"
}
```

### order_type_mapping

```json
{
  "internal_order_type": "string",
  "venue_order_type": "string",
  "ord_type_or_api_field": "string",
  "trigger_condition": "string | null",
  "price_fields": ["limit_price", "stop_price", "protection_price"],
  "allowed_sessions": ["string"],
  "partial_fill_policy": "string",
  "reject_reason_mapping": "string",
  "execution_report_mapping": "string",
  "not_applicable_when": ["string"]
}
```

### time_in_force_mapping

```json
{
  "internal_tif": "GTC | GTD | GTT | IOC | FOK | DAY | SESSION | OTHER",
  "venue_tif": "string",
  "session_calendar_ref": "string",
  "expire_time": "timestamp | null",
  "expire_time_precision": "string",
  "clock_source": "string",
  "partial_fill_behavior": "string",
  "cancel_or_expire_event_ref": "string"
}
```

### post_reduce_constraints

```json
{
  "post_only_flag": "boolean | null",
  "reduce_only_flag": "boolean | null",
  "position_source_ref": "string | null",
  "existing_open_orders_policy": "string",
  "venue_reject_cancel_reprice_behavior": "string",
  "failure_event_ref": "string"
}
```

### stp_smp_mapping

```json
{
  "stp_smp_enabled": "boolean",
  "scope": "account | firm | group | venue_specific",
  "mode": "cancel_newest | cancel_oldest | cancel_both | decrement | reject | venue_specific",
  "mode_source_ref": "string",
  "event_mapping_ref": "string",
  "compliance_boundary": "not_a_market_abuse_conclusion"
}
```

### fee_evidence

```json
{
  "venue_fee_schedule_ref": "string",
  "fee_schedule_version": "string",
  "fill_event_ref": "string",
  "liquidity_flag": "maker | taker | mixed | unknown",
  "transaction_type": "string",
  "fee_tier_source": "string | null",
  "fee_amount_source": "execution_report | venue_statement | clearing_statement | unknown"
}
```

## Owner 边界

```text
Live Execution: adapter、order state machine、venue order truth、execution report、fill/reject/expire event。
Replay / Simulation: 模拟订单语义映射和 fill model 假设，不拥有 live venue truth。
Risk Management: 是否允许提交/撤单/改单/降低仓位的 deterministic policy。
Execution TCA: fee、slippage、benchmark、maker/taker attribution 的事后分析，不拥有订单许可。
Trade Audit: event sequence、idempotency、timestamp、retention 和审计链。
```

## 禁止事项

```text
1. 不得从 order type、TIF、post-only、reduce-only、STP/SMP 或 maker/taker fee 生成交易信号。
2. 不得输出订单提交许可、自动撤单、自动改单、强制 reduce 或路由建议。
3. 不得把某个 venue 的订单语义泛化成所有市场通用规则。
4. 不得把 maker/taker fee 写成策略 alpha、费用套利或成交质量保证。
5. 不得把 STP/SMP 写成防操纵合规结论。
```
""",
        encoding="utf-8",
    )


def candidate_paths() -> list[Path]:
    return sorted(CANDIDATE_DIR.glob("cand_20260612_phase45_order_semantics_*.json"))


def update_candidates(audit_result: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {item["research_task_id"]: item for item in RESULTS}
    updated: list[dict[str, Any]] = []
    for path in candidate_paths():
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id"))
        if task_id not in by_task:
            continue
        result = by_task[task_id]
        candidate["status"].update(
            {
                "review_status": "accepted_for_draft",
                "ingestion_decision": "accepted_for_draft",
                "decision_reason": "外部严格首审通过，可进入 draft 队列；不得创建 reviewed/approved/default/hard gate。",
                "updated_at": TODAY,
            }
        )
        candidate["workflow"].update(
            {
                "stage": "accepted_for_draft",
                "queue_group": "ai_passed",
                "ai_audit_result_id": AUDIT_RESULT_ID,
                "reviewed_preparation_package_id": PREP_PACKAGE_ID,
                "allowed_next_decisions": ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"],
                "forbidden_next_decisions": ["approved", "default_guidance", "hard_gate"],
            }
        )
        candidate.setdefault("review", {})["ai_audit"] = {
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": PACKAGE_ID,
            "decision": result["decision"],
            "confidence": result["confidence"],
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "trade_execution_advice_allowed": False,
            "reasons": result["reasons"],
            "required_followups": result["required_followups"],
            "patch_notes": result["patch_notes"],
        }
        candidate.setdefault("claim", {})["audit_patch_notes"] = result["patch_notes"]
        candidate.setdefault("claim", {})["reviewed_preparation_contract"] = {
            "contract_path": repo_relative(CONTRACT_PATH),
            "contract_sections": [
                "order_semantics_identity",
                "order_type_mapping",
                "time_in_force_mapping",
                "post_reduce_constraints",
                "stp_smp_mapping",
                "fee_evidence",
            ],
        }
        if task_id in {"P45-F-ORD01", "P45-F-ORD02"}:
            upsert_source_refs(candidate, [source_ref("fix_order_state_changes", "src_reviewed_prep_fix_order_state_changes")])
        if task_id == "P45-F-ORD05":
            upsert_source_refs(
                candidate,
                [
                    source_ref("nasdaq_open_close_crosses", "src_reviewed_prep_nasdaq_open_close"),
                    source_ref("nyse_auctions_fact_sheet", "src_reviewed_prep_nyse_auctions"),
                    source_ref("nyse_pillar_differences", "src_reviewed_prep_nyse_pillar"),
                    source_ref("cme_definitions", "src_reviewed_prep_cme_definitions"),
                ],
            )
            candidate["claim"]["statement"] = (
                "交易所特有订单类型和修饰符不得被泛化为通用语义；MOO/MOC/LOC、auction-only、peg、market-with-protection、market-to-limit、iceberg、RFQ、TWAP/VWAP、post-only、reduce-only 等示例必须保留 exchange、product、session、rulebook、API version 和 adapter caveat。外接项目不得把某个交易所或 crypto venue 的订单行为泛化为所有市场。"
            )
        if task_id == "P45-F-ORD06":
            candidate["claim"]["statement"] = (
                "maker/taker、add/remove liquidity、rebate、exchange fee、routing fee 和 transaction type 必须根据 venue fee schedule、成交结果、liquidity flag、fee tier source 和 order event 审计；post-only 或 limit order 不能自动等同于 maker 成交，maker/taker fee 也不能直接写成策略 alpha、成交质量证明、费用套利或默认路由规则。"
            )
        write_json(path, candidate)
        updated.append(candidate)
    return sorted(updated, key=lambda item: str(item.get("research_task_id")))


def prep_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    if len(candidates) != 6:
        failures.append(f"expected 6 candidates, got {len(candidates)}")
    expected = {f"P45-F-ORD{idx:02d}" for idx in range(1, 7)}
    actual = {str(item.get("research_task_id")) for item in candidates}
    if actual != expected:
        failures.append(f"unexpected research_task_id set: {sorted(actual ^ expected)}")
    if not CONTRACT_PATH.exists():
        failures.append("missing order semantics runtime contract")
    for candidate in candidates:
        cid = str(candidate.get("candidate_id"))
        if candidate.get("status", {}).get("ingestion_decision") != "accepted_for_draft":
            failures.append(f"{cid}: not accepted_for_draft")
        if len(candidate.get("source_refs", [])) < 4:
            failures.append(f"{cid}: source_refs < 4")
        if candidate.get("classification", {}).get("canonical_node_id") != "kt.live_execution.order_semantics":
            failures.append(f"{cid}: canonical_node_id mismatch")
        gate = candidate.get("machine_gate", {})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "trade_execution_advice_allowed"):
            if gate.get(field) is not False:
                failures.append(f"{cid}: {field} must remain false")
        blob = json.dumps(candidate, ensure_ascii=False)
        if "�" in blob or "????" in blob:
            failures.append(f"{cid}: possible mojibake")
    return {
        "gate_id": "phase45_order_semantics_reviewed_preparation_gap_report",
        "checked_at": TODAY,
        "package_id": PREP_PACKAGE_ID,
        "candidate_count": len(candidates),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "warnings": [
            "本包只允许外部审计判断是否 accepted_for_reviewed_caveat_only。",
            "不得创建 approved、default guidance、hard gate、交易许可、路由建议、费用优化或自动撤改单。",
            "reviewed/caveat_only 也只能作为审计和 RAG 检索知识，不得作为默认交易指导。",
        ],
    }


def export_reviewed_preparation_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    payload = {
        "package_id": PREP_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "45",
        "task_id": TASK_ID,
        "scope": {
            "branch": "Trading Engineering / Live Execution / Order Semantics",
            "partition": PARTITION,
            "candidate_count": len(candidates),
            "target": "审计 6 条 Order Semantics accepted_for_draft 候选是否可进入 formal reviewed/caveat_only 准备。",
        },
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "routing_advice_allowed": False,
            "fee_optimization_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈", "订单提交许可", "路由建议", "费用套利", "自动撤单", "自动改单"],
        },
        "audit_instructions": [
            "必须搜索相关的专业网站、官方文档、监管资料、交易所/协议资料、broker/venue API 文档、案例和数据，对本 reviewed-preparation 包进行严格审计。",
            "最高只能输出 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
            "检查 internal order_semantics contract 是否足以支撑字段本体，但不得把 contract 解释为交易许可或 hard gate。",
            "检查 ORD05 是否已经足够补齐 MOO/MOC/LOC、auction、peg、market-with-protection、market-to-limit 等特殊订单来源，或是否仍需缩窄。",
            "检查 maker/taker fee 是否和订单类型、fill event、liquidity flag、fee schedule version 分开审计。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "package_id": PREP_PACKAGE_ID,
            "summary": {
                "total": 6,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": True,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "contract_inline": {
            "path": repo_relative(CONTRACT_PATH),
            "contract_sha256_note": "Repo-local UTF-8 contract text is inlined for audit readability; hash may be added by a later formalization task.",
            "full_text": contract_text,
        },
        "quality_gate": gate,
        "candidates": candidates,
    }
    write_json(PREP_PACKAGE, payload)


def write_import_report(audit_result: dict[str, Any], candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    write_json(
        IMPORT_REPORT,
        {
            "report_id": "phase45_order_semantics_candidate_audit_import_report",
            "generated_at": TODAY,
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "package_id": PACKAGE_ID,
            "accepted_for_draft_count": len(candidates),
            "needs_more_evidence_count": 0,
            "rejected_count": 0,
            "blocked_count": 0,
            "reviewed_preparation_package": repo_relative(PREP_PACKAGE),
            "reviewed_preparation_gate": gate,
            "candidates": [
                {
                    "research_task_id": item["research_task_id"],
                    "candidate_id": item["candidate_id"],
                    "status": item.get("status", {}).get("ingestion_decision"),
                    "source_count": len(item.get("source_refs", [])),
                }
                for item in candidates
            ],
            "approved_created": 0,
            "default_guidance_enabled": False,
            "hard_gate_enabled": False,
            "trade_execution_advice_enabled": False,
            "routing_advice_enabled": False,
            "fee_optimization_advice_enabled": False,
        },
    )


def main() -> int:
    audit_result = archive_audit_result()
    write_contract()
    candidates = update_candidates(audit_result)
    gate = prep_quality_gate(candidates)
    write_json(PREP_GATE, gate)
    export_reviewed_preparation_package(candidates, gate)
    write_import_report(audit_result, candidates, gate)
    print(
        json.dumps(
            {
                "status": gate["gate_status"],
                "accepted_for_draft_count": len(candidates),
                "reviewed_preparation_package": repo_relative(PREP_PACKAGE),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
