"""Supplement Phase 37 Replay / Simulation R02/R10/R12 blocked candidates.

CEK-TA-432 only enriches candidates and exports a supplemental reaudit package.
It does not create formal reviewed knowledge, approved knowledge, default
guidance, hard gates, or MCP index changes.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 12).isoformat()
TASK_ID = "CEK-TA-432"
PARTITION_ID = "KB_05_REPLAY_SIMULATION"
PACKAGE_ID = "phase37_replay_simulation_blocked_supplemental_reaudit_package_20260612"
PREVIOUS_AUDIT_RESULT_ID = "audit_result_phase37_replay_simulation_reviewed_preparation_20260612_strict_v1"

ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
CONTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_replay_simulation_execution_assumption_contract.md", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_replay_simulation_blocked_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_replay_simulation_blocked_supplemental_report.json", start_file=__file__
)

TARGETS = {
    "P37-F-R02": {
        "candidate_id": "cand_20260611_phase37_replay_simulation_ohlc_same_bar_tp_sl_ordering_required_001",
        "schema_key": "same_bar_fill_ordering",
        "source_suffix": "same_bar_fill_ordering",
        "evidence_summary": "内联 same_bar_fill_ordering schema，定义 tick_replay、conservative、optimistic、next_bar_only、unknown_ordering_blocked 的字段和判定规则。",
        "statement": "仅有 OHLC bar 且同一根 K 内同时触达止盈和止损时，系统不能声称知道真实先后顺序；必须声明 tick_replay、conservative、optimistic、next_bar_only 或 unknown_ordering_blocked 处理假设。",
        "open_question": "审计方是否认可 same_bar_fill_ordering schema 足以支撑 OHLC same-bar TP/SL ordering 的 reviewed/caveat_only 字段本体？",
    },
    "P37-F-R10": {
        "candidate_id": "cand_20260611_phase37_replay_simulation_simulation_live_gap_report_required_001",
        "schema_key": "simulation_live_gap_report",
        "source_suffix": "simulation_live_gap_report",
        "evidence_summary": "内联 simulation_live_gap_report schema，定义模拟/实盘成交价格、数量、延迟、拒单、费用、订单状态、风控触发、缺失字段和 owner 边界。",
        "statement": "从 simulation / paper 进入 live 前，必须生成 simulation_live_gap_report，记录模拟与真实订单、成交、费用、延迟、拒单、订单状态和风控触发差异；该报告用于审计模拟证据，不等于实盘许可。",
        "open_question": "审计方是否认可 simulation_live_gap_report schema 足以支撑 gap report 字段、owner、生成时点、对齐对象和缺失处理？",
    },
    "P37-F-R12": {
        "candidate_id": "cand_20260611_phase37_replay_simulation_execution_cost_consistency_required_001",
        "schema_key": "execution_cost_mapping",
        "source_suffix": "execution_cost_mapping",
        "evidence_summary": "内联 execution_cost_mapping schema，定义 Backtest、Replay、Paper、Live 之间费用、spread、slippage、market impact 和 fill model 的版本化映射与 owner 边界。",
        "statement": "Backtest、Replay、Paper 和 Live 的费用、spread、slippage、market impact 与 fill model 必须有 execution_cost_mapping 版本化映射；成本口径不一致时不能直接比较表现。",
        "open_question": "审计方是否认可 execution_cost_mapping schema 足以支撑 Backtest/Replay/Paper/Live 成本版本映射和 owner 边界？",
    },
}


SCHEMA_EXTRACT: dict[str, Any] = {
    "schema_extract_id": "phase37_replay_simulation_execution_assumption_schema_extract_v1",
    "schema_version": "1.0.0",
    "generated_at": TODAY,
    "objects": {
        "same_bar_fill_ordering": {
            "purpose": "定义 OHLC same-bar TP/SL ambiguity 的处理假设和证据字段。",
            "owner": "Replay / Simulation",
            "required_fields": [
                "ordering_policy_id",
                "ordering_policy_version",
                "market",
                "venue",
                "instrument_id",
                "timeframe",
                "bar_id",
                "bar_start_time",
                "bar_end_time",
                "bar_open",
                "bar_high",
                "bar_low",
                "bar_close",
                "entry_event_time",
                "entry_price",
                "stop_loss_price",
                "take_profit_price",
                "touches_stop_loss",
                "touches_take_profit",
                "same_bar_both_touched",
                "intrabar_path_available",
                "intrabar_evidence_type",
                "intrabar_evidence_ref",
                "ordering_mode",
                "tie_break_policy",
                "assumption_reason",
                "created_at",
                "audit_trace_id",
            ],
            "allowed_ordering_modes": [
                "tick_replay",
                "conservative",
                "optimistic",
                "next_bar_only",
                "unknown_ordering_blocked",
            ],
            "validation_rules": [
                "OHLC-only 且 same_bar_both_touched=true 时不得声称真实先后顺序。",
                "tick_replay 只能在 intrabar path evidence 可用时使用。",
                "unknown_ordering_blocked 只表示该样本不能作为成交质量证据，不等于实盘风控 hard gate。",
            ],
        },
        "simulation_live_gap_report": {
            "purpose": "定义 simulation/paper 与 live 订单、成交、费用、延迟、状态和风控差异报告。",
            "owner": "Replay / Simulation",
            "required_fields": [
                "gap_report_id",
                "simulation_run_id",
                "live_reference_id",
                "strategy_id",
                "strategy_rule_version",
                "data_version",
                "market",
                "venue",
                "instrument_id",
                "order_id",
                "simulation_order_event_ref",
                "live_order_event_ref",
                "simulation_event_time",
                "live_event_time",
                "simulation_fill_price",
                "live_fill_price",
                "simulation_fill_qty",
                "live_fill_qty",
                "simulation_fee",
                "live_fee",
                "simulation_slippage",
                "live_slippage",
                "latency_delta_ms",
                "fill_price_delta",
                "fill_qty_delta",
                "fee_delta",
                "slippage_delta",
                "reject_cancel_delta",
                "order_state_delta",
                "risk_trigger_delta",
                "missing_live_fields",
                "missing_simulation_fields",
                "acceptable_gap_policy_id",
                "gap_classification",
                "generated_at",
                "audit_trace_id",
            ],
            "allowed_gap_classifications": [
                "within_expected_range",
                "requires_review",
                "invalidates_simulation_evidence",
                "unresolved",
            ],
            "validation_rules": [
                "缺失字段必须进入 missing_live_fields 或 missing_simulation_fields，不得静默填 0。",
                "Live Execution 拥有真实订单、成交、拒单、费用和状态事实。",
                "gap_classification=invalidates_simulation_evidence 不等于自动拒单、停机或 hard gate。",
            ],
        },
        "execution_cost_mapping": {
            "purpose": "定义 Backtest、Replay、Paper、Live 之间执行成本组件和版本映射。",
            "owner": "Replay / Simulation with Backtest / Paper / Live Execution owner mapping",
            "required_fields": [
                "cost_mapping_id",
                "scope",
                "market",
                "venue",
                "backtest_cost_model_version",
                "replay_fill_model_version",
                "live_fee_schedule_version",
                "spread_model_version",
                "slippage_model_version",
                "commission_currency",
                "cost_components",
                "component_mapping_status",
                "owner_mapping",
                "valid_from",
                "created_at",
                "audit_trace_id",
            ],
            "cost_components": [
                "commission",
                "exchange_fee",
                "clearing_fee",
                "spread_cost",
                "slippage_cost",
                "borrow_or_funding_cost",
                "market_impact_cost",
                "tax_or_stamp_duty",
            ],
            "validation_rules": [
                "未映射成本组件必须标记 unknown_component_present 或 unresolved，不得静默当作 0。",
                "Backtest 只记录 cost model version，不拥有真实费用事实。",
                "Live Execution 提供真实费用、真实成交和真实订单状态事实。",
                "成本口径不一致时不得直接比较 Backtest / Replay / Paper / Live 的表现。",
            ],
        },
    },
    "hard_boundaries": {
        "reviewed_caveat_only_is_maximum": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "trade_execution_advice_allowed": False,
    },
}


SUPPORTING_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P37-F-R02": [
        {
            "source_id": "src_backtrader_order_execution_same_bar_boundary",
            "source_title": "Orders - Creation/Execution",
            "source_url": "https://www.backtrader.com/docu/order-creation-execution/order-creation-execution/",
            "source_type": "framework_doc",
            "publisher": "Backtrader",
            "reliability": "medium_high",
            "score": 80,
            "evidence_summary": "Backtrader order execution assumptions support the need to declare event timing and same-bar execution assumptions.",
            "limitations": ["Framework-specific; supports simulation timing caveat, not universal market truth."],
        },
        {
            "source_id": "src_hftbacktest_order_fill_replay_boundary",
            "source_title": "Order Fill",
            "source_url": "https://hftbacktest.readthedocs.io/en/latest/order_fill.html",
            "source_type": "framework_doc",
            "publisher": "HftBacktest",
            "reliability": "medium_high",
            "score": 82,
            "evidence_summary": "HftBacktest order-fill docs support replay/fill-model caveats and market-data replay limitations.",
            "limitations": ["Framework-specific; useful for fill-model caveats, not a universal exchange simulator."],
        },
    ],
    "P37-F-R10": [
        {
            "source_id": "src_fix_execution_report_gap_fields",
            "source_title": "Execution Report <8> message - FIX 4.4",
            "source_url": "https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html",
            "source_type": "standard_doc",
            "publisher": "OnixS FIX Dictionary",
            "reliability": "medium_high",
            "score": 78,
            "evidence_summary": "FIX Execution Report supports order status, fills, rejects and fee-related event trace semantics.",
            "limitations": ["FIX dictionary mirror; useful for status semantics, not venue-specific implementation."],
        },
        {
            "source_id": "src_quantconnect_slippage_gap_concept",
            "source_title": "Slippage Models - Key Concepts",
            "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/slippage/key-concepts",
            "source_type": "framework_doc",
            "publisher": "QuantConnect",
            "reliability": "medium_high",
            "score": 82,
            "evidence_summary": "QuantConnect slippage concepts support comparing expected versus actual fill price in simulations.",
            "limitations": ["Platform-specific; does not define CEK-TA gap report schema."],
        },
    ],
    "P37-F-R12": [
        {
            "source_id": "src_quantconnect_transaction_fee_model",
            "source_title": "Transaction Fees - Key Concepts",
            "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/transaction-fees/key-concepts",
            "source_type": "framework_doc",
            "publisher": "QuantConnect",
            "reliability": "medium_high",
            "score": 80,
            "evidence_summary": "QuantConnect fee model docs support recording transaction-fee assumptions in simulation/backtest results.",
            "limitations": ["Platform-specific; external projects must map their own fee schedules."],
        },
        {
            "source_id": "src_quantconnect_fill_model_cost_boundary",
            "source_title": "Trade Fills - Key Concepts",
            "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/reality-modeling/trade-fills/key-concepts",
            "source_type": "framework_doc",
            "publisher": "QuantConnect",
            "reliability": "medium_high",
            "score": 82,
            "evidence_summary": "QuantConnect fill model docs support fill price/quantity and spread-cost modeling boundaries.",
            "limitations": ["Platform-specific; not a CEK-TA cross-owner cost mapping contract."],
        },
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def append_unique_strings(existing: Any, additions: list[str]) -> list[str]:
    result = [item for item in existing if isinstance(item, str)] if isinstance(existing, list) else []
    for item in additions:
        if item not in result:
            result.append(item)
    return result


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (str(source.get("source_id") or ""), str(source.get("source_url") or source.get("source_title") or ""))


def ensure_source(candidate: dict[str, Any], source: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    if not isinstance(refs, list):
        refs = []
        candidate["source_refs"] = refs
    keys = {source_key(item) for item in refs if isinstance(item, dict)}
    if source_key(source) not in keys:
        refs.append(source)


def internal_contract_source(task_id: str, target: dict[str, str], contract_hash: str) -> dict[str, Any]:
    return {
        "source_id": f"src_p37_replay_contract_{target['source_suffix']}",
        "source_title": "Phase 37 Replay / Simulation Execution Assumption Contract",
        "source_url": rel(CONTRACT_PATH),
        "source_type": "internal_contract_schema_extract",
        "publisher": "CEK-TA",
        "published_at": TODAY,
        "accessed_at": TODAY,
        "version": SCHEMA_EXTRACT["schema_version"],
        "reliability": "high",
        "relevance": "high",
        "score": 92,
        "evidence_summary": target["evidence_summary"],
        "limitations": [
            "该来源只定义 CEK-TA 内部逻辑字段和 owner 边界，外部项目可映射等价字段。",
            "该来源只支撑 reviewed/caveat_only 再审，不支撑 approved、default guidance 或 hard gate。",
        ],
        "contract_sha256": contract_hash,
        "schema_object": target["schema_key"],
        "quoted_excerpt_allowed": False,
    }


def normalized_supporting_source(source: dict[str, Any]) -> dict[str, Any]:
    payload = dict(source)
    payload.setdefault("published_at", None)
    payload["accessed_at"] = TODAY
    payload.setdefault("version", None)
    payload.setdefault("freshness", "time_sensitive")
    payload.setdefault("relevance", "medium_high")
    payload.setdefault("quoted_excerpt_allowed", False)
    return payload


def patch_candidate(candidate: dict[str, Any], task_id: str, target: dict[str, str], contract_hash: str) -> dict[str, Any]:
    ensure_source(candidate, internal_contract_source(task_id, target, contract_hash))
    for source in SUPPORTING_SOURCES[task_id]:
        ensure_source(candidate, normalized_supporting_source(source))

    claim = candidate.setdefault("claim", {})
    claim["statement"] = target["statement"]
    claim["evidence_summary"] = (
        f"{target['evidence_summary']} 外部框架、FIX 或平台文档只作为实现模式支撑，字段本体以 CEK-TA 内部契约为准。"
    )
    claim["claim_strength"] = "reviewed_caveat_only_pending_reaudit"

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["internal_contract_evidence_status"] = "inline_contract_and_schema_extract_added"
    source_quality["internal_contract_sha256"] = contract_hash
    source_quality["limitations"] = append_unique_strings(
        source_quality.get("limitations", []),
        [
            "CEK-TA Replay / Simulation 内部契约已内联到再审包，支撑字段本体、owner 边界和机器门禁。",
            "框架、平台、交易所、broker 和 FIX 文档只能支撑各自语义，不得泛化为所有市场通用规则。",
            "本轮仍只请求 reviewed/caveat_only，不请求 approved、default guidance 或 hard gate。",
        ],
    )

    applicability = candidate.setdefault("applicability", {})
    applicability["limitations"] = append_unique_strings(
        applicability.get("limitations", []),
        [
            "本候选只约束 Replay / Simulation 审计证据和假设声明，不证明策略盈利能力。",
            "本候选不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "Live Execution / Risk Management 事实和动作仍由对应 owner 处理。",
        ],
    )

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none_known_in_visible_context"
    conflict["resolution_summary"] = (
        "CEK-TA-432 已补充 Replay / Simulation 内部契约和 schema extract；仍需外部再审确认是否可进入 "
        "formal reviewed/caveat_only。与 Live Execution / Risk Management 重叠时，Replay 只模拟和审计假设，不拥有真实执行事实。"
    )
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "已补内部契约并等待 reviewed/caveat_only 再审；不得作为默认指导。"
    machine_gate["requires_human_escalation"] = True
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已补充 CEK-TA Replay / Simulation 内部契约和 schema extract，等待 reviewed/caveat_only 严格再审。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "supplemented_for_contract_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["current_task_id"] = TASK_ID
    workflow["next_action"] = "external_ai_or_human_contract_reaudit"
    workflow["next_allowed_decisions"] = [
        "accepted_for_reviewed_caveat_only",
        "needs_more_evidence",
        "rejected",
        "blocked",
    ]
    workflow["forbidden_decisions"] = ["approved", "default_guidance", "hard_gate"]
    workflow["formalization_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["ai_audit_result_id"] = f"pending_{PACKAGE_ID}"

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked_until_contract_reaudit"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    review = candidate.setdefault("review", {})
    review["open_questions"] = [
        target["open_question"],
        "审计方是否确认本候选仍只能进入 formal reviewed/caveat_only，而不能进入 approved、default guidance 或 hard gate？",
        "审计方是否发现与 Backtest、Live Execution、Risk Management 或 Market Microstructure owner 边界冲突？",
    ]
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_replay_simulation_blocked_contract_supplemented",
            "reason": f"{TASK_ID}: 补充 {target['schema_key']} 内部契约、schema extract、contract hash 和 owner 边界。",
            "audit_result_id": f"pending_{PACKAGE_ID}",
        }
    )
    review["contract_reaudit"] = {
        "package_id": PACKAGE_ID,
        "previous_audit_result_id": PREVIOUS_AUDIT_RESULT_ID,
        "schema_object": target["schema_key"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_checks": [
            "contract_full_text_present",
            "schema_extract_present",
            "contract_sha256_present",
            "owner_boundary_present",
            "tool_docs_not_used_as_internal_contract",
            "no_trade_execution_advice",
        ],
    }
    candidate["_inline_contract_evidence"] = {
        "task_id": TASK_ID,
        "contract_path": rel(CONTRACT_PATH),
        "contract_sha256": contract_hash,
        "schema_extract_id": SCHEMA_EXTRACT["schema_extract_id"],
        "schema_object": target["schema_key"],
    }
    return candidate


def write_research(candidates: list[dict[str, Any]], contract_hash: str) -> None:
    lines = [
        "# Phase 37 Replay / Simulation R02/R10/R12 阻断项补证研究",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 任务目标",
        "",
        "`CEK-TA-432` 只为 R02/R10/R12 补充内部契约和 schema extract，并导出 reviewed/caveat_only 再审包。",
        "",
        "## 内部契约",
        "",
        f"- 契约路径：`{rel(CONTRACT_PATH)}`",
        f"- 契约 SHA256：`{contract_hash}`",
        f"- schema_extract_id：`{SCHEMA_EXTRACT['schema_extract_id']}`",
        "",
        "## 补证对象",
        "",
    ]
    for candidate in candidates:
        task_id = str(candidate.get("research_task_id"))
        target = TARGETS[task_id]
        lines.extend(
            [
                f"### {task_id} / {candidate.get('candidate_id')}",
                "",
                f"- schema object：`{target['schema_key']}`",
                f"- claim：{candidate.get('claim', {}).get('statement', '')}",
                f"- 补证重点：{target['evidence_summary']}",
                "",
            ]
        )
    lines.extend(
        [
            "## 审计边界",
            "",
            "```text",
            "1. candidate 不是正式知识。",
            "2. 本包最多允许 accepted_for_reviewed_caveat_only。",
            "3. 不允许 approved。",
            "4. 不允许 default guidance。",
            "5. 不允许 hard gate。",
            "6. 不允许生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "```",
            "",
            "## 来源使用边界",
            "",
            "外部框架、平台、FIX 或 broker 文档只用于说明实现模式和字段方向；CEK-TA exact field、owner mapping、workflow gate 由内部契约支撑。",
            "",
        ]
    )
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_audit_package(candidates: list[dict[str, Any]], contract_text: str, contract_hash: str) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "replay_simulation_blocked_supplemental_reaudit",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "language": "zh-CN",
        "phase": "37",
        "title": "Phase 37 Replay / Simulation R02/R10/R12 内部契约补证再审包",
        "purpose": "严格复审 R02/R10/R12 在补齐 CEK-TA Replay / Simulation 内部契约和 schema extract 后，是否可进入 formal reviewed/caveat_only。",
        "strict_boundaries": [
            "candidate 不是正式知识。",
            "本次审计最多只能允许 accepted_for_reviewed_caveat_only。",
            "不得创建 approved。",
            "不得启用 default guidance。",
            "不得启用 hard gate。",
            "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        ],
        "audit_instructions": [
            "必须搜索相关的专业网站、资料、案例和数据，对审计报告进行严格审计。",
            "重点检查 same_bar_fill_ordering 是否足以支撑 OHLC 同根 K TP/SL 成交排序假设。",
            "重点检查 simulation_live_gap_report 是否覆盖 fill_price、fill_qty、latency、reject/cancel、slippage、fee、order_state、risk_trigger、live_reference、simulation_reference、owner 和缺失字段处理。",
            "重点检查 execution_cost_mapping 是否覆盖 fee、spread、slippage、market_impact、fill_model 在 Backtest、Replay、Paper、Live 之间的版本映射与 owner 边界。",
            "检查外部框架、平台、交易所、broker 和 FIX 文档是否只作为实现模式支撑，没有被误用为 CEK-TA 字段本体。",
            "如果仍缺来源、字段定义、owner 映射、冲突审计或边界，必须返回 needs_more_evidence 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "auditor": "string",
            "audited_at": "YYYY-MM-DD",
            "quality_gate": {"pass": "boolean", "candidate_count": 3, "notes": ["string"]},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P37-F-R02 | P37-F-R10 | P37-F-R12",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                }
            ],
        },
        "contract_inline": {
            "path": rel(CONTRACT_PATH),
            "sha256": contract_hash,
            "full_text": contract_text,
            "schema_extract": SCHEMA_EXTRACT,
        },
        "source_review_notes": {
            "internal_contract_source": "CEK-TA Replay / Simulation execution assumption contract 是字段本体主来源。",
            "external_tool_sources": "Backtrader、HftBacktest、QuantConnect、FIX、IBKR 等只能作为 implementation pattern 或 supporting source。",
            "source_quality_boundary": "不得把 tool-specific docs 写成 universal market rule 或 CEK-TA internal contract。",
        },
        "candidates": candidates,
    }


def quality_gate(package: dict[str, Any], candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    if len(candidates) != 3:
        failures.append({"failure": "candidate_count_not_3"})
    if not package.get("contract_inline", {}).get("full_text"):
        failures.append({"failure": "contract_full_text_missing"})
    objects = package.get("contract_inline", {}).get("schema_extract", {}).get("objects", {})
    for required in ("same_bar_fill_ordering", "simulation_live_gap_report", "execution_cost_mapping"):
        if required not in objects:
            failures.append({"failure": f"schema_object_missing:{required}"})
    for candidate in candidates:
        cid = str(candidate.get("candidate_id"))
        workflow = candidate.get("workflow", {})
        if workflow.get("stage") != "supplemented_for_contract_reaudit":
            failures.append({"failure": f"{cid}:workflow_stage_wrong"})
        for key in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if workflow.get(key) is not False:
                failures.append({"failure": f"{cid}:workflow_{key}_not_false"})
        if workflow.get("hidden_from_default_queue") is not True:
            failures.append({"failure": f"{cid}:hidden_from_default_queue_not_true"})
    if has_mojibake(package):
        failures.append({"failure": "mojibake_marker_detected"})
    return {
        "gate_id": "phase37_replay_simulation_blocked_supplemental_quality_gate",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
    }


def main() -> int:
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    contract_hash = sha256_text(contract_text)
    SCHEMA_EXTRACT["contract_path"] = rel(CONTRACT_PATH)
    SCHEMA_EXTRACT["contract_sha256"] = contract_hash

    candidates: list[dict[str, Any]] = []
    for task_id, target in TARGETS.items():
        path = CANDIDATE_DIR / f"{target['candidate_id']}.json"
        candidate = read_json(path)
        if candidate.get("research_task_id") != task_id:
            raise ValueError(f"{path}: expected {task_id}, got {candidate.get('research_task_id')}")
        patched = patch_candidate(candidate, task_id, target, contract_hash)
        write_json(path, patched)
        candidates.append(patched)

    write_research(candidates, contract_hash)
    package = build_audit_package(candidates, contract_text, contract_hash)
    gate = quality_gate(package, candidates)
    package["quality_gate"] = gate
    write_json(AUDIT_PACKAGE_PATH, package)

    report = {
        "report_id": "phase37_replay_simulation_blocked_supplemental_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "targets": sorted(TARGETS),
        "contract_path": rel(CONTRACT_PATH),
        "contract_sha256": contract_hash,
        "research_record": rel(RESEARCH_PATH),
        "audit_package": rel(AUDIT_PACKAGE_PATH),
        "quality_gate": gate,
        "boundary": "Candidate supplement only; no formal reviewed knowledge, approved knowledge, default guidance, hard gate, or MCP index update was created.",
        "next_action": "把再审包交给外部 AI/人工严格审计；若返回 accepted_for_reviewed_caveat_only 且 reviewed_allowed=true，再执行 CEK-TA-433。",
    }
    write_json(REPORT_PATH, report)
    if gate["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {gate['failures']}")
    print(json.dumps({"audit_package": rel(AUDIT_PACKAGE_PATH), "quality_gate": gate["gate_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
