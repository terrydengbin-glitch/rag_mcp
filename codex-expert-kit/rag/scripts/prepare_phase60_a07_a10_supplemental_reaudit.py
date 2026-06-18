"""Prepare Phase 60 A07/A10 supplemental reviewed-preparation reaudit.

The previous strict reviewed-preparation audit accepted 8 Phase 60 candidates
for formal reviewed/caveat_only, but kept P60-A07 and P60-A10 as
needs_more_evidence. This script supplements direct sources and machine-readable
boundary fields, then exports a reaudit package. It does not create formal
knowledge and does not promote anything to reviewed/approved/default guidance.
"""

from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-17"
TASK_ID = "CEK-TA-579"
PACKAGE_ID = "phase60_a07_a10_supplemental_reaudit_package_20260617"
REPORT_ID = "phase60_a07_a10_supplemental_reaudit_report"
PRIOR_AUDIT_RESULT_ID = "audit_result_phase60_reviewed_preparation_20260617_strict_v1"


TARGETS: dict[str, dict[str, Any]] = {
    "P60-A07": {
        "candidate_path": (
            "KB_07_RISK_MANAGEMENT",
            "cand_20260617_phase60_environment_promotion_evidence_required_001.json",
        ),
        "required_field_patch": {
            "promotion_decision_id": "required",
            "environment_manifest_id": "required",
            "gap_report_id": "required",
            "reconciliation_report_id": "required",
            "risk_review_owner": "required",
            "human_reviewer_required": True,
            "promotion_not_live_permission": True,
            "residual_gap_acceptance_note": "required_when_residual_gap_exists",
            "rollback_plan_ref": "required",
            "decision_owner": "required",
        },
        "supplemental_sources": [
            {
                "source_id": "src_quantconnect_live_reconciliation",
                "source_title": "Reconciliation - Live Trading",
                "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/live-trading/reconciliation",
                "source_type": "official_doc",
                "publisher": "QuantConnect",
                "reliability": "high",
                "score": 88,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "QuantConnect documents live-trading reconciliation and explains that live fills, brokerage "
                    "execution, stale data, and backtest/live deviations require reconciliation instead of assuming "
                    "backtest or paper results match live behavior."
                ),
                "limitations": [
                    "QuantConnect-specific live trading implementation pattern; not a universal brokerage rule.",
                    "Supports reconciliation evidence, not live permission or strategy validity.",
                ],
                "accessed_at": TODAY,
                "relevance": "high",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_nautilus_live_execution_reconciliation",
                "source_title": "Live Trading - Execution reconciliation",
                "source_url": "https://nautilustrader.io/docs/latest/concepts/live/",
                "source_type": "framework_doc",
                "publisher": "NautilusTrader",
                "reliability": "high",
                "score": 88,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "NautilusTrader documents that live execution reconciliation aligns venue order/position state "
                    "with internal event-built state and is performed by the LiveExecutionEngine."
                ),
                "limitations": [
                    "Framework-specific; use as live reconciliation pattern, not as a CEK-TA hard dependency.",
                    "Reconciliation supports evidence review, not automatic promotion or live permission.",
                ],
                "accessed_at": TODAY,
                "relevance": "high",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_nautilus_continuous_reconciliation",
                "source_title": "Configure a Live Trading Node - Continuous reconciliation",
                "source_url": "https://nautilustrader.io/docs/nightly/how_to/configure_live_trading/",
                "source_type": "framework_doc",
                "publisher": "NautilusTrader",
                "reliability": "high",
                "score": 84,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "NautilusTrader documents continuous reconciliation loops that check in-flight orders, open "
                    "orders, position status, and own order books after startup."
                ),
                "limitations": [
                    "Nightly framework documentation; use as implementation pattern with version caveat.",
                    "Does not define CEK-TA promotion ownership by itself.",
                ],
                "accessed_at": TODAY,
                "relevance": "medium_high",
                "quoted_excerpt_allowed": False,
            },
        ],
        "supplemental_patch_notes": {
            "source": [
                "补入 QuantConnect live reconciliation 作为 backtest/paper/live 偏差和 reconciliation 的直接来源。",
                "补入 NautilusTrader live execution reconciliation 作为 venue order/position state 与 internal event state 对齐的直接来源。",
            ],
            "content": [
                "promotion decision 必须引用 manifest、gap report、reconciliation report、risk review 和人工复核。",
                "新增 promotion_not_live_permission=true，机器不得把晋级评审误读为实盘许可。",
            ],
            "boundary": [
                "promotion decision 不是 live permission，不得生成交易许可、风险阈值、下单许可或 hard gate。",
                "存在 residual gap 时必须记录 residual_gap_acceptance_note 和 rollback_plan_ref。",
            ],
            "conflict": [
                "Live reconciliation 归 Live Execution owner；promotion 风险接受必须有 Risk owner / human reviewer。",
            ],
        },
    },
    "P60-A10": {
        "candidate_path": (
            "KB_07_RISK_MANAGEMENT",
            "cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json",
        ),
        "required_field_patch": {
            "risk_rehearsal_result_not_hard_gate": True,
            "broker_or_exchange_rejection_mapping_source": "required",
            "live_risk_owner_policy_source": "required",
            "kill_switch_or_manual_override_boundary": "required",
            "order_denied_reason_code_mapping": "required",
            "sandbox_result_scope": "field_chain_and_audit_rehearsal_only",
            "live_policy_owner_required": True,
        },
        "supplemental_sources": [
            {
                "source_id": "src_nautilus_execution_risk_engine",
                "source_title": "Execution - Risk engine",
                "source_url": "https://nautilustrader.io/docs/nightly/concepts/execution/",
                "source_type": "framework_doc",
                "publisher": "NautilusTrader",
                "reliability": "high",
                "score": 90,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "NautilusTrader documents that the RiskEngine exists across backtest, sandbox and live, sits on "
                    "submit/modify paths, validates price, quantity, notional, reduce-only, balances, rate limits, "
                    "and trading states, and emits OrderDenied or OrderModifyRejected events when checks fail."
                ),
                "limitations": [
                    "Framework-specific; supports risk-engine pattern and reason-code boundary, not CEK-TA hard gate.",
                    "Nightly docs require version caveat before being treated as stable implementation detail.",
                ],
                "accessed_at": TODAY,
                "relevance": "high",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_nautilus_architecture_risk_engine",
                "source_title": "Architecture - RiskEngine and ExecutionEngine",
                "source_url": "https://nautilustrader.io/docs/latest/concepts/architecture/",
                "source_type": "framework_doc",
                "publisher": "NautilusTrader",
                "reliability": "high",
                "score": 86,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "NautilusTrader architecture describes ExecutionEngine order lifecycle tracking, coordination "
                    "with risk management, execution reports/fills, reconciliation, and RiskEngine pre-trade checks, "
                    "position/exposure monitoring, real-time calculations, and configurable rules."
                ),
                "limitations": [
                    "Framework-specific architecture source; not a universal trading-system requirement.",
                ],
                "accessed_at": TODAY,
                "relevance": "high",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_binance_usdm_futures_error_code",
                "source_title": "USDⓈ-M Futures Error Code",
                "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/error-code",
                "source_type": "official_doc",
                "publisher": "Binance Open Platform",
                "reliability": "high",
                "score": 88,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "Binance USD-M Futures error-code documentation provides concrete broker/exchange rejection "
                    "semantics, including reduce-only margin check failures, unsupported order types, and market "
                    "order rejection conditions."
                ),
                "limitations": [
                    "Binance USD-M Futures-specific; does not define all broker/exchange rejection behavior.",
                    "Supports rejection mapping evidence, not risk threshold advice or live permission.",
                ],
                "accessed_at": TODAY,
                "relevance": "high",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_fia_automated_trading_risk_controls",
                "source_title": "Best Practices for Automated Trading Risk Controls and System Safeguards",
                "source_url": "https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf",
                "source_type": "industry_best_practice",
                "publisher": "FIA",
                "reliability": "high",
                "score": 87,
                "freshness": "time_sensitive",
                "evidence_summary": (
                    "FIA best-practices guidance supports pre-trade risk controls, order-size checks, position "
                    "limits, price tolerance checks, control ownership, regular review, and system safeguards."
                ),
                "limitations": [
                    "Industry best-practice source; does not provide CEK-TA-specific thresholds or implementation.",
                    "Must not be converted into legal advice or automatic CEK-TA hard gate.",
                ],
                "accessed_at": TODAY,
                "relevance": "medium_high",
                "quoted_excerpt_allowed": False,
            },
        ],
        "supplemental_patch_notes": {
            "source": [
                "补入 NautilusTrader RiskEngine / Execution 文档，直接支撑 sandbox/live 风控链条和 OrderDenied / OrderModifyRejected 语义。",
                "补入 Binance USD-M Futures error-code 文档，直接支撑 broker/exchange rejection mapping。",
                "补入 FIA 自动化交易风控实践，支撑 live risk owner、定期复核和系统保护边界。",
            ],
            "content": [
                "risk rehearsal 只能验证字段、策略链条、拒绝原因映射和审计流程。",
                "新增 risk_rehearsal_result_not_hard_gate=true，禁止把演练结果解释为 live hard gate。",
            ],
            "boundary": [
                "sandbox 风控演练不得替代 live risk owner，不得自动拒单、自动停机、自动解锁或给出风险阈值。",
                "kill switch、manual override、live rejection 和 risk policy 归 Live/Risk owner。",
            ],
            "conflict": [
                "Risk Management owner 保留真实政策和 hard gate 所有权；AI/RAG 只能引用 reason code 和审计证据。",
            ],
        },
    },
}


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_path(parts: tuple[str, str]) -> Path:
    return repo_path("codex-expert-kit", "rag", "candidates", *parts)


def merge_sources(candidate: dict[str, Any], sources: list[dict[str, Any]]) -> list[str]:
    existing = {
        str(source.get("source_id"))
        for source in candidate.get("source_refs", [])
        if isinstance(source, dict)
    }
    added: list[str] = []
    candidate.setdefault("source_refs", [])
    for source in sources:
        if source["source_id"] not in existing:
            candidate["source_refs"].append(copy.deepcopy(source))
            added.append(source["source_id"])
            existing.add(source["source_id"])
    return added


def append_unique(values: list[Any], additions: list[Any]) -> list[Any]:
    result = list(values)
    for item in additions:
        if item not in result:
            result.append(item)
    return result


def supplement_candidate(task_id: str, target: dict[str, Any]) -> tuple[dict[str, Any], Path, list[str]]:
    path = candidate_path(target["candidate_path"])
    candidate = read_json(path)
    if candidate.get("research_task_id") != task_id:
        raise ValueError(f"{path} has unexpected research_task_id")

    added_sources = merge_sources(candidate, target["supplemental_sources"])

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = (
        "Supplemental direct evidence added for reviewed/caveat_only reaudit; candidate remains non-formal until external audit returns."
    )
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "supplemented_pending_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "external_reaudit_for_reviewed_caveat_only"
    workflow["supplemental_reaudit_package_id"] = PACKAGE_ID
    workflow["current_task_id"] = TASK_ID
    workflow["formalization_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["visible_in_default_guidance_queue"] = False
    workflow["hidden_from_default_queue"] = True

    claim = candidate.setdefault("claim", {})
    summary = claim.get("evidence_summary", "")
    supplement_summary = "；".join(source["evidence_summary"] for source in target["supplemental_sources"])
    if supplement_summary and supplement_summary not in summary:
        claim["evidence_summary"] = f"{summary}；{supplement_summary}" if summary else supplement_summary
    notes = claim.get("interpretation_notes", "")
    boundary_note = (
        "补证后仍只能等待 reviewed/caveat_only 复审；不得解释为 approved、default guidance、hard gate、live permission、交易建议或风险阈值。"
    )
    if boundary_note not in notes:
        claim["interpretation_notes"] = f"{notes} {boundary_note}".strip()

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["source_count"] = len(candidate.get("source_refs", []))
    source_quality["primary_source_count"] = len(
        [s for s in candidate.get("source_refs", []) if isinstance(s, dict) and s.get("relevance") in {"high", "medium_high"}]
    )
    source_quality["needs_more_evidence"] = "pending_reaudit"
    source_quality["supplement_status"] = "direct_sources_added_pending_external_reaudit"
    source_quality["supplemental_source_ids"] = append_unique(source_quality.get("supplemental_source_ids", []), added_sources)

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["default_guidance_allowed"] = False
    conflict["hard_gate_allowed"] = False
    conflict["resolution_summary"] = (
        "Supplemental evidence added for reviewed/caveat_only reaudit only. Formal reviewed creation requires external audit; "
        "approved/default guidance/hard gate/live permission remain forbidden."
    )

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reviewed_allowed"] = False
    machine_gate["approved_allowed"] = False
    machine_gate["default_guidance_allowed"] = False
    machine_gate["hard_gate_allowed"] = False
    machine_gate["trade_execution_advice_allowed"] = False
    machine_gate["risk_threshold_advice_allowed"] = False
    machine_gate["live_permission_allowed"] = False
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "Supplemented candidate pending external reviewed/caveat_only reaudit; no formal use yet."

    candidate["supplemental_reaudit"] = {
        "package_id": PACKAGE_ID,
        "prior_audit_result_id": PRIOR_AUDIT_RESULT_ID,
        "task_id": TASK_ID,
        "prepared_at": TODAY,
        "allowed_reaudit_decisions": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
            "blocked",
        ],
        "forbidden_decisions": [
            "approved",
            "default_guidance",
            "hard_gate",
            "live_permission",
            "trade_execution_advice",
            "risk_threshold_advice",
        ],
        "added_source_ids": added_sources,
        "required_field_patch": target["required_field_patch"],
        "patch_notes": target["supplemental_patch_notes"],
    }

    candidate.setdefault("audit_log", []).append(
        {
            "event": "supplemental_evidence_added_for_reaudit",
            "at": TODAY,
            "by": "codex",
            "task_id": TASK_ID,
            "package_id": PACKAGE_ID,
            "added_source_ids": added_sources,
            "notes": "Added direct sources and machine-readable boundary fields for reviewed/caveat_only supplemental reaudit.",
        }
    )

    write_json(path, candidate)
    return candidate, path, added_sources


def package_candidate(candidate: dict[str, Any], path: Path) -> dict[str, Any]:
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "path": rel(path),
        "current_status": {
            "review_status": candidate.get("status", {}).get("review_status"),
            "ingestion_decision": candidate.get("status", {}).get("ingestion_decision"),
            "workflow_stage": candidate.get("workflow", {}).get("stage"),
            "queue_group": candidate.get("workflow", {}).get("queue_group"),
            "formalization_allowed": candidate.get("workflow", {}).get("formalization_allowed"),
        },
        "classification": candidate.get("classification", {}),
        "claim": candidate.get("claim", {}),
        "applicability": candidate.get("applicability", {}),
        "source_refs": candidate.get("source_refs", []),
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": candidate.get("conflict_audit", {}),
        "llm_usage_policy": candidate.get("llm_usage_policy", {}),
        "machine_gate": candidate.get("machine_gate", {}),
        "conversion_target": candidate.get("conversion_target", {}),
        "supplemental_reaudit": candidate.get("supplemental_reaudit", {}),
    }


def main() -> int:
    packaged: list[dict[str, Any]] = []
    report_rows: list[dict[str, Any]] = []

    for task_id, target in TARGETS.items():
        candidate, path, added_sources = supplement_candidate(task_id, target)
        packaged.append(package_candidate(candidate, path))
        report_rows.append(
            {
                "research_task_id": task_id,
                "candidate_id": candidate.get("candidate_id"),
                "path": rel(path),
                "added_source_ids": added_sources,
                "source_count": len(candidate.get("source_refs", [])),
                "status": candidate.get("status", {}).get("review_status"),
                "workflow_stage": candidate.get("workflow", {}).get("stage"),
            }
        )

    package = {
        "schema_version": "phase60_supplemental_reaudit_package.v1",
        "package_id": PACKAGE_ID,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "prior_audit_result_id": PRIOR_AUDIT_RESULT_ID,
        "scope": {
            "phase": "Phase 60",
            "purpose": "Reaudit P60-A07/P60-A10 after direct evidence supplementation.",
            "candidate_count": len(packaged),
            "research_task_ids": sorted(TARGETS),
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "max_allowed_positive_decision": "accepted_for_reviewed_caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
        },
        "allowed_decisions": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
            "blocked",
        ],
        "audit_questions": [
            "补充来源是否直接支撑 P60-A07 的 promotion decision / reconciliation / human review / risk owner 边界？",
            "补充来源是否直接支撑 P60-A10 的 live risk owner / broker rejection mapping / sandbox rehearsal not hard gate 边界？",
            "是否仍存在 source_refs 过度依赖内部契约的问题？",
            "是否存在把 promotion、risk rehearsal、gap report 误读为 live permission、hard gate 或风险阈值的风险？",
            "如果通过，是否只能进入 formal reviewed/caveat_only，而不得进入 approved/default guidance/hard gate？",
        ],
        "expected_audit_output_schema": {
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "trade_execution_advice_allowed": False,
                    "risk_threshold_advice_allowed": False,
                    "live_permission_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {
                        "source": ["string"],
                        "content": ["string"],
                        "boundary": ["string"],
                        "conflict": ["string"],
                    },
                }
            ]
        },
        "candidates": packaged,
    }
    package_path = repo_path("docs", "audit", f"{PACKAGE_ID}.json")
    write_json(package_path, package)

    report = {
        "report_id": REPORT_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "package_id": PACKAGE_ID,
        "package_path": rel(package_path),
        "updated_candidate_count": len(report_rows),
        "rows": report_rows,
        "boundary": "Supplemental evidence package only; no formal reviewed knowledge created.",
        "next_action": "Send package for strict external audit, then import the returned result.",
    }
    report_path = repo_path("docs", "reports", f"{REPORT_ID}.json")
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
