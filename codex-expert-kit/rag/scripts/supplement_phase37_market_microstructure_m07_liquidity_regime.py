"""Supplement Phase 37 Market Microstructure M07 liquidity regime evidence.

This script keeps P37-D-M07 as a candidate and exports a strict reaudit package.
It does not create formal reviewed knowledge, approved knowledge, default
guidance, hard gates, or trading execution advice.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-410"
PARTITION_ID = "KB_03_MARKET_MICROSTRUCTURE"
CANDIDATE_ID = "cand_20260611_phase37_market_microstructure_liquidity_regime_required_001"
RESEARCH_TASK_ID = "P37-D-M07"
AUDIT_PACKAGE_ID = "phase37_market_microstructure_m07_liquidity_regime_reaudit_package_20260611"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", PARTITION_ID, f"{CANDIDATE_ID}.json", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_market_microstructure_m07_liquidity_regime_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", f"{AUDIT_PACKAGE_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_market_microstructure_m07_liquidity_regime_supplemental_report.json", start_file=__file__
)


SUPPLEMENTAL_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "src_m07_nyse_trading_information_sessions_auctions",
        "source_title": "Trading Information",
        "source_url": "https://www.nyse.com/trade/trading-information",
        "source_type": "official_exchange_trading_rules",
        "publisher": "NYSE",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "live web page accessed 2026-06-11",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "NYSE documents pre-opening, early, core and late trading sessions, plus core open and closing auction timing. "
            "This supports session-specific liquidity regime boundaries."
        ),
        "limitations": [
            "NYSE-specific; external projects must map their own venue sessions and auctions.",
            "Supports session and auction taxonomy, not a profitable signal."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_nyse_hours_calendars_holidays",
        "source_title": "Holidays & Trading Hours",
        "source_url": "https://www.nyse.com/markets/hours-calendars",
        "source_type": "official_exchange_calendar",
        "publisher": "NYSE",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "2026/2027/2028 holiday and early close calendar",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "NYSE publishes holiday and early-close schedules. This supports treating holiday and early-close periods "
            "as separate liquidity regime contexts."
        ),
        "limitations": [
            "NYSE equity-market calendar only; not universal across futures, crypto or non-US markets."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_nasdaq_trade_halt_codes",
        "source_title": "Trading Halts Code",
        "source_url": "https://nasdaqtrader.com/Trader.aspx?id=TradeHaltCodes",
        "source_type": "official_exchange_halt_status_doc",
        "publisher": "Nasdaq Trader",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "live web page accessed 2026-06-11",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "Nasdaq publishes halt code categories such as news pending, news released, single-stock trading pause and "
            "extraordinary market activity. This supports explicit halt/pause regime labels."
        ),
        "limitations": [
            "Nasdaq equity halt-code semantics; other venues may use different status codes."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_nasdaq_halt_cross_rule",
        "source_title": "Nasdaq Equity Trading Rules",
        "source_url": "https://listingcenter.nasdaq.com/rulebook/nasdaq/rules/Nasdaq%20Equity%204",
        "source_type": "official_exchange_rulebook",
        "publisher": "Nasdaq",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "Equity 4 rules",
        "reliability": "high",
        "relevance": "medium_high",
        "evidence_summary": (
            "Nasdaq rules reference halt/pause handling and re-opening through a Halt Cross process. This supports "
            "auction/reopen specific regime boundaries after halts."
        ),
        "limitations": [
            "Rulebook source supports venue process boundaries, not a trading edge or execution permission."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_cme_holiday_trading_hours",
        "source_title": "CME Group Holiday and Trading Hours",
        "source_url": "https://www.cmegroup.com/trading-hours.html",
        "source_type": "official_exchange_calendar",
        "publisher": "CME Group",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "2026 holiday and trading hours page",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "CME Group provides holiday schedules and product-filtered trading hours. This supports futures-specific "
            "holiday/session regime mapping."
        ),
        "limitations": [
            "CME-specific; products may have different holiday hours and trading sessions."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_cme_expiration_calendar",
        "source_title": "Expirations Calendar",
        "source_url": "https://www.cmegroup.com/tools-information/calendars/expiration-calendar.html",
        "source_type": "official_exchange_contract_calendar",
        "publisher": "CME Group",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "live web page accessed 2026-06-11",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "CME provides important dates for futures and options expirations, deliveries, settlements and other key "
            "trading events. This supports expiration-event regime boundaries."
        ),
        "limitations": [
            "Calendar source; product-specific contract specs still need to be mapped by the external project."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_cme_equity_index_roll_dates",
        "source_title": "Equity Index Roll Dates",
        "source_url": "https://www.cmegroup.com/trading/equity-index/rolldates.html",
        "source_type": "official_exchange_roll_calendar",
        "publisher": "CME Group",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "live web page accessed 2026-06-11",
        "reliability": "high",
        "relevance": "high",
        "evidence_summary": (
            "CME explains roll dates for equity index futures and notes that the lead month can change because the "
            "near expiring contract will terminate soon and may become less liquid. This directly supports rollover "
            "liquidity regime tagging."
        ),
        "limitations": [
            "Equity-index futures specific; other futures families need their own roll rules."
        ],
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_m07_databento_status_schema",
        "source_title": "Status schema",
        "source_url": "https://databento.com/docs/schemas-and-data-formats/status",
        "source_type": "vendor_schema_doc",
        "publisher": "Databento",
        "published_at": None,
        "accessed_at": TODAY,
        "version": "live docs accessed 2026-06-11",
        "reliability": "medium_high",
        "relevance": "high",
        "evidence_summary": (
            "Databento status schema provides updates about trading sessions, halts, pauses, auction starts and matching "
            "engine statuses. This supports using vendor market-status data to label liquidity regimes."
        ),
        "limitations": [
            "Vendor schema; availability and granularity vary by publisher and dataset."
        ],
        "quoted_excerpt_allowed": False,
    },
]


TAXONOMY_CONTRACT = {
    "contract_id": "cek_ta_liquidity_regime_taxonomy_v1",
    "owner": "Trading Engineering / Market Microstructure",
    "status": "candidate_for_reaudit",
    "purpose": "将市场微观结构特征按交易时段、事件、交易所状态、合约生命周期和压力状态切分，避免把正常流动性统计外推到特殊状态。",
    "regime_labels": [
        {
            "label": "normal_continuous",
            "meaning": "交易所正常连续交易时段，且无已知 halt、auction、holiday、rollover 或异常状态。",
            "required_evidence": ["venue_session_calendar", "market_status_or_no_halt_evidence"],
        },
        {
            "label": "pre_open_or_open_auction",
            "meaning": "开盘前、开盘集合竞价或 opening cross 周边。",
            "required_evidence": ["exchange_auction_rules", "session_time_boundary"],
        },
        {
            "label": "closing_auction_or_close",
            "meaning": "收盘集合竞价、收盘失衡冻结期或 close 周边。",
            "required_evidence": ["exchange_auction_rules", "session_time_boundary"],
        },
        {
            "label": "holiday_or_early_close",
            "meaning": "交易所假日、节假日前后、提前收盘或节假日修改交易时段。",
            "required_evidence": ["exchange_holiday_calendar", "early_close_schedule"],
        },
        {
            "label": "halt_pause_reopen",
            "meaning": "交易暂停、halt、pause、re-open 或 halt cross/reopen auction 周边。",
            "required_evidence": ["halt_code_or_market_status", "reopen_or_cross_rule_if_applicable"],
        },
        {
            "label": "rollover_or_expiry",
            "meaning": "期货/期权合约换月、临近 last trading day、expiration、delivery 或 settlement 事件周边。",
            "required_evidence": ["contract_expiration_calendar", "roll_schedule_or_product_contract_spec"],
        },
        {
            "label": "stressed_liquidity",
            "meaning": "市场/资金流动性压力、波动异常、成交与报价质量恶化或风控复核触发状态。",
            "required_evidence": ["liquidity_stress_source", "project_defined_detection_rule"],
        },
        {
            "label": "thin_or_off_hours",
            "meaning": "盘前、盘后、隔夜、低成交、低深度或非核心交易时段。",
            "required_evidence": ["session_calendar", "volume_depth_or_spread_threshold_policy"],
        },
    ],
    "required_fields": [
        "market",
        "venue",
        "instrument",
        "session_id",
        "session_timezone",
        "regime_label",
        "regime_start_time",
        "regime_end_time",
        "evidence_source_id",
        "calendar_or_status_version",
        "assigned_at",
        "assigned_by",
        "confidence",
    ],
    "hard_boundaries": [
        "taxonomy 是 CEK-TA 内部标签契约，不是外部通用标准。",
        "regime 标签只能约束解释、回测分层、特征适用范围和人工/风控复核，不得单独生成买卖点、仓位或实盘执行许可。",
        "外接项目必须把自己的交易所日历、market status、合约规格和供应商字段映射到本 taxonomy，不能直接套用某一交易所或供应商的物理字段名。",
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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def repo_root() -> Path:
    return resolve_repo_path(start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(repo_root()).as_posix()


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return str(source.get("source_url") or ""), str(source.get("source_title") or "")


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [item for item in candidate.get("source_refs", []) if isinstance(item, dict)]
    seen = {source_key(item) for item in sources}
    for source in SUPPLEMENTAL_SOURCES:
        if source_key(source) not in seen:
            sources.append(source)
            seen.add(source_key(source))
    return sources


def build_research_md() -> str:
    lines = [
        "# Phase 37 Market Microstructure M07 补证研究",
        "",
        "## 任务",
        "",
        "CEK-TA-410 为 `P37-D-M07 microstructure.liquidity_regime_required.v1` 补充 reviewed/caveat_only 阻断项证据。",
        "",
        "## 审计阻断点",
        "",
        "上一轮 reviewed-preparation 审计认为：ECB/NBER/CFA 足以支持 liquidity stress caveat，但不足以支持 `rollover`、`session-specific`、休市前后、`halts/auction` 等完整 regime 边界。因此本轮只补这些直接证据，不把候选升级为正式知识。",
        "",
        "## 补证来源",
        "",
    ]
    for source in SUPPLEMENTAL_SOURCES:
        lines.extend(
            [
                f"### {source['source_id']}",
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
    lines.extend(
        [
            "## CEK-TA liquidity regime taxonomy v1",
            "",
            "本 taxonomy 是 CEK-TA 内部标签契约，不是外部交易所、监管或行业通用标准。外接项目必须把自己的交易日历、market status、合约规格和数据供应商字段映射到这些逻辑标签。",
            "",
            "| 标签 | 含义 | 必需证据 |",
            "| --- | --- | --- |",
        ]
    )
    for label in TAXONOMY_CONTRACT["regime_labels"]:
        lines.append(f"| `{label['label']}` | {label['meaning']} | {', '.join(label['required_evidence'])} |")
    lines.extend(
        [
            "",
            "## 仍然禁止",
            "",
            "```text",
            "1. 不得创建 approved。",
            "2. 不得开启 default guidance。",
            "3. 不得开启 hard gate。",
            "4. 不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "5. 不得把 CEK-TA 内部 regime 标签说成外部通用标准。",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def update_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    candidate["source_refs"] = merge_sources(candidate)
    candidate.setdefault("supplemental_contracts", {})["liquidity_regime_taxonomy"] = TAXONOMY_CONTRACT
    claim = candidate.setdefault("claim", {})
    claim["statement"] = (
        "Microstructure 特征必须使用明确的 liquidity regime 标签和证据来源区分 normal continuous、auction/open/close、holiday/early-close、halt/pause/reopen、"
        "rollover/expiry、thin/off-hours 与 stressed liquidity；不得把正常连续交易时段的盘口、滑点或订单流统计直接外推到特殊时段、事件时段或合约生命周期切换期。"
    )
    claim["evidence_summary"] = (
        "ECB/NBER/CFA 支撑市场/资金流动性压力边界；NYSE/Nasdaq/CME/Databento 官方或供应商文档补充 session、holiday、auction/halt、expiration/rollover 和 market status 直接证据。"
    )
    applicability = candidate.setdefault("applicability", {})
    applicability["applies_when"] = [
        "审计盘口、成交、滑点、市场影响或订单流特征的 liquidity regime 适用范围",
        "把流动性状态作为 backtest、replay、AI scoring 或 live execution 的上下文输入",
        "需要区分正常连续交易、auction/open/close、halt/pause/reopen、holiday/early-close、rollover/expiry、thin/off-hours 或 stressed liquidity 时",
    ]
    applicability["not_applicable_when"] = [
        "没有交易时段、交易日历、market status、事件日、交易量或报价可用性信息",
        "需要证明某个 regime 下必然盈利",
        "需要具体买卖点、仓位、杠杆、止损止盈价格、交易所私有配置、账户事实或实盘权限时，应由外接项目事实层、执行层和风控层处理。",
        "AI Engineering 只能引用本规则，不得把本规则改写为 LLM 训练、MCP、RAG 或模型部署本体规则。",
        "外接项目不能直接套用 NYSE/Nasdaq/CME/Databento 的物理字段名，必须映射到自己的 venue、instrument、session 和数据供应商契约。",
    ]
    source_quality = candidate.setdefault("source_quality", {})
    source_quality["score"] = 89.0
    source_quality["primary_source_count"] = 8
    source_quality["supporting_source_count"] = max(0, len(candidate["source_refs"]) - 8)
    source_quality["limitations"] = [
        "CEK-TA liquidity regime taxonomy 是内部逻辑标签，不是外部通用标准。",
        "交易所和供应商文档只支撑各自 venue/product/dataset 语义；外接项目必须映射自己的交易日历、market status、合约规格和数据契约。",
        "正式 reviewed/caveat_only 仍需外部审计确认补证是否足以覆盖上一轮阻断项。",
    ]
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = "CEK-TA-410 已补充 session/calendar/auction/halt/holiday/rollover/expiry 证据，等待外部再审。"
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "supplemented_for_reaudit",
            "queue_group": "needs_more_evidence",
            "current_task_id": TASK_ID,
            "next_action": "external_reaudit_for_reviewed_caveat_only",
            "ai_audit_package_id": AUDIT_PACKAGE_ID,
            "formalization_allowed": False,
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": False,
            "visible_in_default_guidance_queue": False,
        }
    )
    conversion = workflow.setdefault("conversion_target", {})
    if isinstance(conversion, dict):
        conversion["target_review_status"] = "reviewed_caveat_only_if_reaudit_passes"
        conversion["reviewed_allowed"] = False
        conversion["approved_allowed"] = False
        conversion["default_guidance_allowed"] = False
        conversion["hard_gate_allowed"] = False
    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": "pending_reaudit",
        "source_package_id": AUDIT_PACKAGE_ID,
        "decision": "needs_more_evidence_supplemented_for_reaudit",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reason": "已补齐交易所/供应商直接来源和 CEK-TA 内部 liquidity regime taxonomy，等待外部严格再审。",
    }
    review["open_questions"] = [
        "这些来源是否足以把 M07 从 needs_more_evidence 升级到 accepted_for_reviewed_caveat_only？",
        "CEK-TA liquidity regime taxonomy 是否仍存在与 M11 thin market execution risk 或 Execution/Risk owner 边界重复？",
        "是否需要继续补具体资产类别或交易所 product-level contract specs？",
    ]
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase37_market_microstructure_m07_supplemented_for_reaudit",
                "reason": "补充 NYSE/Nasdaq/CME/Databento 直接来源和 CEK-TA liquidity regime taxonomy，导出再审包。",
            }
        )
    return candidate


def build_audit_package(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": AUDIT_PACKAGE_ID,
        "created_at": TODAY,
        "created_by": "codex",
        "task_id": TASK_ID,
        "source_audit_result_id": "audit_result_phase37_market_microstructure_reviewed_preparation_20260611_strict_v1",
        "scope": {
            "phase": "Phase 37",
            "partition_id": PARTITION_ID,
            "research_task_id": RESEARCH_TASK_ID,
            "candidate_count": 1,
            "purpose": "严格再审 P37-D-M07 是否可从 needs_more_evidence 升级为 accepted_for_reviewed_caveat_only。",
        },
        "audit_instructions": {
            "language": "zh-CN",
            "must_search_external_sources": True,
            "instruction": (
                "必须搜索相关的专业网站、资料、案例和数据，对本再审包进行严格审计。重点核验：交易日历、session hours、auction/halt、holiday schedule、"
                "contract rollover/expiry、vendor market status 是否足以支撑 liquidity regime taxonomy。"
            ),
            "allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "forbidden_decisions": [
                "approved",
                "default_guidance",
                "hard_gate",
                "trade_execution_advice",
            ],
            "hard_boundaries": [
                "candidate 不是正式知识。",
                "即使再审通过，也最多只能进入 formal reviewed/caveat_only。",
                "不得创建 approved、default guidance 或 hard gate。",
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把 CEK-TA 内部 regime taxonomy 说成外部通用标准。",
            ],
        },
        "quality_gate_expectation": {
            "minimum_source_count": 8,
            "required_evidence_dimensions": [
                "exchange_session_hours",
                "auction_or_cross",
                "trading_halt_or_pause",
                "holiday_or_early_close_calendar",
                "futures_expiration",
                "futures_rollover",
                "vendor_market_status_schema",
                "liquidity_stress_context",
            ],
            "reviewed_allowed_only_if": [
                "source_refs directly support the previously blocked dimensions",
                "taxonomy is framed as CEK-TA internal labels, not universal standard",
                "M11 thin market execution risk and Execution/Risk owner boundaries are not overwritten",
                "approved/default/hard gate remain false",
            ],
        },
        "candidate": candidate,
        "expected_output_schema": {
            "audit_result_id": "string",
            "package_id": AUDIT_PACKAGE_ID,
            "quality_gate": {
                "pass": "boolean",
                "reason": "string",
            },
            "results": [
                {
                    "candidate_id": CANDIDATE_ID,
                    "research_task_id": RESEARCH_TASK_ID,
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                    "reason": "string",
                }
            ],
        },
    }


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError(f"Unexpected candidate_id: {candidate.get('candidate_id')}")
    candidate = update_candidate(candidate)
    write_json(CANDIDATE_PATH, candidate)
    write_text(RESEARCH_PATH, build_research_md())
    audit_package = build_audit_package(candidate)
    write_json(AUDIT_PACKAGE_PATH, audit_package)
    report = {
        "report_id": "phase37_market_microstructure_m07_liquidity_regime_supplemental_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_id": CANDIDATE_ID,
        "research_task_id": RESEARCH_TASK_ID,
        "source_count_after_supplement": len(candidate["source_refs"]),
        "supplemental_source_count": len(SUPPLEMENTAL_SOURCES),
        "taxonomy_contract_id": TAXONOMY_CONTRACT["contract_id"],
        "candidate_path": rel(CANDIDATE_PATH),
        "research_path": rel(RESEARCH_PATH),
        "audit_package_path": rel(AUDIT_PACKAGE_PATH),
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "boundary": "supplemental reaudit package only; candidate remains needs_more_evidence until external audit result is imported.",
        "next_action": "将再审包交给外部严格审计；审计通过后由 CEK-TA-411 导入并沉淀 formal reviewed/caveat_only。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
