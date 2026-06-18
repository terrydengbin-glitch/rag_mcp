"""Supplement Phase 37 Live/Risk L03/L10/L11 blocked candidates.

CEK-TA-440 enriches only the three needs_more_evidence candidates and exports a
supplemental reaudit package. It does not create formal reviewed knowledge,
approved knowledge, default guidance, hard gates, or risk threshold advice.
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
TASK_ID = "CEK-TA-440"
PACKAGE_ID = "phase37_live_risk_blocked_supplemental_reaudit_package_20260612"
PREVIOUS_AUDIT_RESULT_ID = "audit_result_phase37_live_risk_reviewed_preparation_20260612_strict_v1"

ROOT = resolve_repo_path(start_file=__file__)
CONTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_live_risk_reconciliation_exposure_loss_policy_contract.md", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path("docs", "research", "phase37_live_risk_blocked_supplemental_research.md", start_file=__file__)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase37_live_risk_blocked_supplemental_report.json", start_file=__file__)

TARGETS: dict[str, dict[str, str]] = {
    "P37-G-L03": {
        "candidate_path": "codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/cand_20260612_phase37_live_risk_position_reconciliation_required_001.json",
        "schema_key": "position_reconciliation",
        "source_suffix": "position_reconciliation",
        "statement": "实盘系统必须把本地订单、成交和仓位与 broker、exchange、account statement 或 clearing source 对账；发现差异时必须进入 reconciliation_required 或等价审计状态，而不是继续按未核验的本地状态下单。",
        "evidence_summary": "内联 position_reconciliation schema，定义 local_position_ref、broker_position_ref、account_statement_ref、discrepancy_type、mismatch_qty、mismatch_notional、stale_source、unknown_source、reconciliation_action、owner 和 audit_trace 字段。",
        "open_question": "审计方是否认可 position_reconciliation schema 足以支撑 L03 的 reviewed/caveat_only 字段本体？",
    },
    "P37-G-L10": {
        "candidate_path": "codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/cand_20260612_phase37_live_risk_portfolio_exposure_limit_required_001.json",
        "schema_key": "portfolio_exposure_limit",
        "source_suffix": "portfolio_exposure_limit",
        "statement": "组合暴露治理必须定义账户、策略、品种、venue、相关资产、行业/主题、方向、gross/net exposure、价格源、聚合规则、stale pricing 处理、owner 和 audit trace；阈值只引用外接项目 policy，不由 CEK-TA 推荐。",
        "evidence_summary": "内联 portfolio_exposure_limit schema，定义 exposure taxonomy、aggregation_rule、price_source、gross/net/directional exposure、correlated_group、policy_threshold_ref、owner 和 audit_trace 字段。",
        "open_question": "审计方是否认可 portfolio_exposure_limit schema 足以支撑 L10 的 reviewed/caveat_only 字段本体？",
    },
    "P37-G-L11": {
        "candidate_path": "codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/cand_20260612_phase37_live_risk_consecutive_loss_stop_required_001.json",
        "schema_key": "consecutive_loss_stop_policy",
        "source_suffix": "consecutive_loss_stop_policy",
        "statement": "若交易系统使用连续亏损停止规则，必须定义亏损事件口径、时间窗口政策引用、计数来源、重置条件、冻结动作、人工复核、解锁流程，以及与单笔风险、日亏损和组合暴露规则的优先级；不得写入 CEK-TA 推荐阈值。",
        "evidence_summary": "内联 consecutive_loss_stop_policy schema，定义 loss_event_basis、time_window_policy_ref、streak_count_source、reset_condition、freeze_action、manual_review_required、unlock_process_ref、priority_order_ref 和 audit_trace 字段。",
        "open_question": "审计方是否认可 consecutive_loss_stop_policy schema 足以支撑 L11 的 reviewed/caveat_only 字段本体？",
    },
}


SCHEMA_EXTRACT: dict[str, Any] = {
    "schema_extract_id": "phase37_live_risk_reconciliation_exposure_loss_policy_schema_extract_v1",
    "schema_version": "1.0.0",
    "generated_at": TODAY,
    "objects": {
        "position_reconciliation": {
            "owner": "Live Execution",
            "consumed_by": ["Risk Management"],
            "required_fields": [
                "reconciliation_id",
                "account_id_ref",
                "strategy_id",
                "instrument_id",
                "local_position_ref",
                "broker_position_ref",
                "account_statement_ref",
                "local_qty",
                "broker_qty",
                "local_notional",
                "broker_notional",
                "mismatch_qty",
                "mismatch_notional",
                "discrepancy_type",
                "source_priority",
                "local_snapshot_time",
                "broker_snapshot_time",
                "stale_source",
                "unknown_source",
                "reconciliation_status",
                "reconciliation_action",
                "owner",
                "consumed_by_risk",
                "audit_trace_id",
                "created_at",
            ],
            "validation_rules": [
                "missing_source 不得静默当作仓位为 0。",
                "reconciliation_required 只表示证据状态，不等于 CEK-TA 自动拒单或 hard gate。",
                "Live Execution 拥有 broker/account position truth；Risk Management 只消费状态。",
            ],
        },
        "portfolio_exposure_limit": {
            "owner": "Risk Management",
            "depends_on": ["Data Engineering", "Market Microstructure", "Live Execution"],
            "required_fields": [
                "exposure_check_id",
                "risk_policy_id",
                "account_id_ref",
                "strategy_id",
                "instrument_id",
                "venue",
                "asset_class",
                "sector_or_theme",
                "direction",
                "correlated_group_id",
                "exposure_dimension",
                "gross_exposure",
                "net_exposure",
                "directional_exposure",
                "price_source_id",
                "price_timestamp",
                "price_staleness_status",
                "aggregation_rule_id",
                "exposure_status",
                "policy_threshold_ref",
                "owner",
                "audit_trace_id",
                "created_at",
            ],
            "validation_rules": [
                "price_staleness_status=stale|unknown|missing 时不得静默通过为 within_policy。",
                "policy_threshold_ref 只引用外接项目政策，不存 CEK-TA 推荐阈值。",
                "Market/Data owner 提供 grouping、reference data、price source；Risk owner 负责暴露政策。",
            ],
        },
        "consecutive_loss_stop_policy": {
            "owner": "Risk Management",
            "depends_on": ["Live Execution"],
            "required_fields": [
                "loss_stop_policy_id",
                "risk_policy_id",
                "account_id_ref",
                "strategy_id",
                "loss_event_basis",
                "loss_event_source",
                "time_window_policy_ref",
                "streak_count_source",
                "reset_condition",
                "freeze_action",
                "manual_review_required",
                "unlock_process_ref",
                "priority_order_ref",
                "interaction_with_single_trade_risk",
                "interaction_with_daily_loss",
                "interaction_with_portfolio_exposure",
                "policy_status",
                "owner",
                "audit_trace_id",
                "created_at",
            ],
            "validation_rules": [
                "连续亏损停止不能替代单笔风险、日亏损或组合暴露限制。",
                "freeze_action 是政策状态标签，不等于 CEK-TA 直接执行停机或拒单。",
                "time_window_policy_ref 和 priority_order_ref 只能引用外接项目政策，不写推荐数值。",
                "解锁必须经过 unlock_process_ref 或人工复核流程，不能由 AI scoring 自动解锁。",
            ],
        },
    },
    "hard_boundaries": {
        "reviewed_caveat_only_is_maximum": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "risk_threshold_advice_allowed": False,
        "trade_execution_advice_allowed": False,
    },
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


def internal_contract_source(target: dict[str, str], contract_hash: str) -> dict[str, Any]:
    return {
        "source_id": f"src_p37_live_risk_contract_{target['source_suffix']}",
        "source_title": "Phase 37 Live/Risk Reconciliation Exposure Loss Policy Contract",
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
            "该来源只定义 CEK-TA 内部逻辑字段、owner 边界和审计状态，外部项目可映射等价字段。",
            "该来源只支撑 reviewed/caveat_only 再审，不支撑 approved、default guidance、hard gate 或风险阈值建议。",
        ],
        "contract_sha256": contract_hash,
        "schema_object": target["schema_key"],
        "quoted_excerpt_allowed": False,
    }


def patch_candidate(candidate: dict[str, Any], task_id: str, target: dict[str, str], contract_hash: str) -> dict[str, Any]:
    ensure_source(candidate, internal_contract_source(target, contract_hash))

    claim = candidate.setdefault("claim", {})
    claim["statement"] = target["statement"]
    claim["evidence_summary"] = (
        f"{target['evidence_summary']} 外部监管、broker、venue、platform 文档只作为原则或实现模式支撑，字段本体以 CEK-TA 内部契约为准。"
    )
    claim["claim_strength"] = "reviewed_caveat_only_pending_reaudit"

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["internal_contract_evidence_status"] = "inline_contract_and_schema_extract_added"
    source_quality["internal_contract_sha256"] = contract_hash
    source_quality["limitations"] = append_unique_strings(
        source_quality.get("limitations", []),
        [
            "CEK-TA Live/Risk 内部契约已内联到再审包，支撑字段本体、owner 边界和机器门禁。",
            "监管、broker、venue 和平台文档只能支撑原则或实现模式，不得泛化为所有市场通用规则。",
            "本轮仍只请求 reviewed/caveat_only，不请求 approved、default guidance、hard gate 或风险阈值建议。",
        ],
    )

    applicability = candidate.setdefault("applicability", {})
    applicability["limitations"] = append_unique_strings(
        applicability.get("limitations", []),
        [
            "本候选只约束 Live Execution / Risk Management 字段、状态和审计边界。",
            "本候选不得生成买卖点、仓位、杠杆、止损止盈、实盘执行建议或风险阈值数值。",
            "实际拒单、停机、冻结、解锁和恢复动作仍由外接项目正式 risk_policy_id 和 execution system 决定。",
        ],
    )

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none_known_in_visible_context"
    conflict["resolution_summary"] = (
        "CEK-TA-440 已补充 Live/Risk 内部契约和 schema extract；仍需外部再审确认是否可进入 formal reviewed/caveat_only。"
    )
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False
    conflict["risk_threshold_advice_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate.update(
        {
            "default_guidance": "deny",
            "reason": "已补内部契约并等待 reviewed/caveat_only 再审；不得作为默认指导、hard gate 或风险阈值建议。",
            "requires_human_escalation": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        }
    )

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已补充 CEK-TA Live/Risk 内部契约和 schema extract，等待 reviewed/caveat_only 严格再审。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "supplemented_for_contract_reaudit",
            "queue_group": "needs_more_evidence",
            "current_task_id": TASK_ID,
            "next_action": "external_ai_or_human_contract_reaudit",
            "next_allowed_decisions": [
                "accepted_for_reviewed_caveat_only",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "forbidden_decisions": ["approved", "default_guidance", "hard_gate"],
            "formalization_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "risk_threshold_advice_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "ai_audit_result_id": f"pending_{PACKAGE_ID}",
        }
    )

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked_until_contract_reaudit"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conversion["risk_threshold_advice_allowed"] = False

    review = candidate.setdefault("review", {})
    review["open_questions"] = [
        target["open_question"],
        "审计方是否确认本候选仍只能进入 formal reviewed/caveat_only，而不能进入 approved、default guidance、hard gate 或风险阈值建议？",
        "审计方是否发现与 Data Engineering、Market Microstructure、Replay/Simulation、Live Execution 或 Risk Management owner 边界冲突？",
    ]
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_live_risk_blocked_contract_supplemented",
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
        "risk_threshold_advice_allowed": False,
        "required_checks": [
            "contract_full_text_present",
            "schema_extract_present",
            "contract_sha256_present",
            "owner_boundary_present",
            "threshold_values_absent",
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
        "# Phase 37 Live/Risk L03/L10/L11 阻断项补证研究",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 任务目标",
        "",
        "`CEK-TA-440` 只为 L03/L10/L11 补充内部契约和 schema extract，并导出 reviewed/caveat_only 再审包。",
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
            "6. 不允许风险阈值建议。",
            "7. 不允许生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "```",
            "",
            "## 来源使用边界",
            "",
            "外部监管、broker、venue 和 platform 文档只用于说明原则和实现模式；CEK-TA exact field、owner mapping、workflow gate 由内部契约支撑。",
            "",
        ]
    )
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text("\n".join(lines), encoding="utf-8")


def build_audit_package(candidates: list[dict[str, Any]], contract_text: str, contract_hash: str) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "package_type": "live_risk_blocked_supplemental_reaudit",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "language": "zh-CN",
        "phase": "37",
        "title": "Phase 37 Live/Risk L03/L10/L11 内部契约补证再审包",
        "purpose": "严格复审 L03/L10/L11 在补齐 CEK-TA Live/Risk 内部契约和 schema extract 后，是否可进入 formal reviewed/caveat_only。",
        "strict_boundaries": [
            "candidate 不是正式知识。",
            "本次审计最多只能允许 accepted_for_reviewed_caveat_only。",
            "不得创建 approved。",
            "不得启用 default guidance。",
            "不得启用 hard gate。",
            "不得允许 risk threshold advice。",
            "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        ],
        "audit_instructions": [
            "必须搜索相关的专业网站、资料、案例和数据，对审计报告进行严格审计。",
            "重点检查 position_reconciliation 是否覆盖 local/broker/statement/clearing source、差异类型、source priority、stale/unknown、owner 和 audit trace。",
            "重点检查 portfolio_exposure_limit 是否覆盖账户、策略、品种、venue、相关资产、行业/主题、方向、gross/net exposure、价格源、聚合规则、stale pricing、owner 和 audit trace。",
            "重点检查 consecutive_loss_stop_policy 是否覆盖亏损事件口径、时间窗口、计数来源、重置、冻结、人工复核、解锁和与其他 risk gates 的优先级。",
            "检查外部监管、broker、venue、platform 文档是否只作为原则或实现模式支撑，没有被误用为 CEK-TA 字段本体。",
            "检查包内是否没有风险阈值数值、买卖点、仓位、杠杆、止损止盈或实盘许可。",
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
                    "research_task_id": "P37-G-L03 | P37-G-L10 | P37-G-L11",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "risk_threshold_advice_allowed": False,
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
            "internal_contract_source": "CEK-TA Live/Risk contract 是字段本体主来源。",
            "external_sources": "SEC/CFTC/NIST/CME/FIA/FIX/IBKR/Binance/QuantConnect 等只能作为 principle、regulatory、venue、broker 或 platform supporting source。",
            "source_quality_boundary": "不得把外部工具或监管材料写成 CEK-TA 阈值政策或 universal market rule。",
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
    for required in ("position_reconciliation", "portfolio_exposure_limit", "consecutive_loss_stop_policy"):
        if required not in objects:
            failures.append({"failure": f"schema_object_missing:{required}"})
    for candidate in candidates:
        cid = str(candidate.get("candidate_id"))
        workflow = candidate.get("workflow", {})
        if workflow.get("stage") != "supplemented_for_contract_reaudit":
            failures.append({"failure": f"{cid}:workflow_stage_wrong"})
        for key in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed", "risk_threshold_advice_allowed"):
            if workflow.get(key) is not False:
                failures.append({"failure": f"{cid}:workflow_{key}_not_false"})
        if workflow.get("hidden_from_default_queue") is not True:
            failures.append({"failure": f"{cid}:hidden_from_default_queue_not_true"})
    if has_mojibake(package):
        failures.append({"failure": "mojibake_marker_detected"})
    return {
        "gate_id": "phase37_live_risk_blocked_supplemental_quality_gate",
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
        "risk_threshold_advice_created": 0,
    }


def main() -> int:
    contract_text = CONTRACT_PATH.read_text(encoding="utf-8")
    contract_hash = sha256_text(contract_text)
    SCHEMA_EXTRACT["contract_path"] = rel(CONTRACT_PATH)
    SCHEMA_EXTRACT["contract_sha256"] = contract_hash

    candidates: list[dict[str, Any]] = []
    for task_id, target in TARGETS.items():
        path = resolve_repo_path(*target["candidate_path"].split("/"), start_file=__file__)
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
        "report_id": "phase37_live_risk_blocked_supplemental_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "targets": sorted(TARGETS),
        "contract_path": rel(CONTRACT_PATH),
        "contract_sha256": contract_hash,
        "research_record": rel(RESEARCH_PATH),
        "audit_package": rel(AUDIT_PACKAGE_PATH),
        "quality_gate": gate,
        "boundary": "Candidate supplement only; no formal reviewed knowledge, approved knowledge, default guidance, hard gate, risk threshold advice, or MCP index update was created.",
        "next_action": "把再审包交给外部 AI/人工严格审计；若返回 accepted_for_reviewed_caveat_only 且 reviewed_allowed=true，再导入并 materialize formal reviewed/caveat_only。",
    }
    write_json(REPORT_PATH, report)
    if gate["gate_status"] != "pass":
        raise SystemExit(f"quality gate failed: {gate['failures']}")
    print(json.dumps({"audit_package": rel(AUDIT_PACKAGE_PATH), "quality_gate": gate["gate_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
