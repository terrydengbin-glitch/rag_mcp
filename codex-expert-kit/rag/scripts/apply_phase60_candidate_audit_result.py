"""Apply Phase 60 P0 candidate strict audit result.

The source audit text says the package summary has 9 accepted items, but the
itemized table includes P60-A01 through P60-A10 and each item is accepted for
draft. This script follows the itemized results and records the mismatch in the
import report.

It never creates reviewed, approved, default guidance, hard gates, or trading
advice.
"""

from __future__ import annotations

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
TASK_ID = "CEK-TA-577"
AUDIT_RESULT_ID = "audit_result_phase60_sandbox_replay_paper_candidate_20260617_strict_v1"
PACKAGE_ID = "phase60_sandbox_replay_paper_candidate_audit_package_20260617"


TARGETS: dict[str, dict[str, Any]] = {
    "P60-A01": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_environment_taxonomy_required_001.json"),
        "confidence": "medium_high",
        "required_followups": [
            "补 QuantConnect、Alpaca、IBKR、Binance、Coinbase 等多平台来源。",
            "明确 live canary 与 full live 的字段差异。",
        ],
        "patch_notes": {
            "source": ["NautilusTrader 只能作为 framework implementation pattern。", "补 broker/exchange/paper/testnet 直接来源。"],
            "content": ["taxonomy 可保留，但必须绑定 EnvironmentManifest。", "不得把 sandbox/testnet/paper/replay 混用同一语义。"],
            "boundary": ["不得 reviewed。", "不得 approved。", "不得 default guidance。", "不得 hard gate。"],
            "conflict": ["与 Phase 58 不冲突，应作为 environment taxonomy 上游。"],
        },
    },
    "P60-A02": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_static_api_sandbox_contract_only_001.json"),
        "confidence": "high",
        "required_followups": ["标题必须保留 static API sandbox，不得泛化到所有 sandbox。", "补 response_mocked、market_data_real、order_routing_real 等字段。"],
        "patch_notes": {
            "source": ["Coinbase 来源是 Coinbase-specific，不代表所有交易所 sandbox。"],
            "content": ["static sandbox 只能验证字段、格式、鉴权、错误结构。", "不得作为真实成交、真实账户、真实流动性或策略收益证据。"],
            "boundary": ["不得 live-ready。", "不得 hard gate。"],
            "conflict": ["与 Phase 58 等效链条不冲突。"],
        },
    },
    "P60-A03": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_testnet_endpoint_isolation_required_001.json"),
        "confidence": "high",
        "required_followups": ["补 endpoint_scope_policy、credential_scope_policy、account_scope_policy。", "补 testnet_data_source_policy。"],
        "patch_notes": {
            "source": ["Binance 来源只能作为 Binance USD-M Futures-specific。"],
            "content": ["testnet / demo endpoint 必须与 production endpoint 隔离。", "testnet 结果不得写入 production facts。"],
            "boundary": ["不得默认代表所有交易所 testnet 行为。"],
            "conflict": ["与 Live Execution owner 不冲突。"],
        },
    },
    "P60-A04": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_paper_trading_not_live_required_001.json"),
        "confidence": "high",
        "required_followups": ["与已有 paper_trading_not_equal_live 做 alias / merge。", "补 paper broker model version、paper fill policy、paper/live gap report 字段。"],
        "patch_notes": {
            "source": ["QuantConnect、Alpaca、IBKR 均是平台/券商特定来源。"],
            "content": ["paper trading 是 rehearsal，不是 live execution。", "paper PnL 不得作为 live-ready 证据。"],
            "boundary": ["不得实盘许可。", "不得交易建议。"],
            "conflict": ["与 Phase 37/58 高度重叠，建议去重。"],
        },
    },
    "P60-A05": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_replay_market_impact_assumption_required_001.json"),
        "confidence": "high",
        "required_followups": ["补 QuantConnect reconciliation 作为 backtest/live gap 来源。", "补 queue_position_policy、market_impact_assumption、partial_fill_policy。"],
        "patch_notes": {
            "source": ["HftBacktest 是 framework-specific。"],
            "content": ["replay fill 必须披露模型假设。", "replay 不能默认说明真实队列位置或真实冲击。"],
            "boundary": ["不得 live-ready。", "不得 hard gate。"],
            "conflict": ["与 Phase 58 等效链条一致。"],
        },
    },
    "P60-A06": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_environment_manifest_required_001.json"),
        "confidence": "medium_high",
        "required_followups": ["补完整 EnvironmentManifest schema。", "补 reconciliation_report_id、known_non_equivalence、audit_trace_id。"],
        "patch_notes": {
            "source": ["当前主要依赖内部 contract，reviewed 前需补外部 reconciliation / audit trail 资料。"],
            "content": ["manifest 只证明环境事实可审计，不证明策略有效。"],
            "boundary": ["不得把 manifest 完备解释为上线许可。"],
            "conflict": ["与 Phase 58 environment_equivalence_manifest 应建立上下游关系。"],
        },
    },
    "P60-A07": {
        "candidate_path": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_environment_promotion_evidence_required_001.json"),
        "confidence": "medium",
        "required_followups": [
            "补 QuantConnect reconciliation、Nautilus live reconciliation 或交易系统 QA/reconciliation 来源。",
            "补 human_reviewer_required、promotion_not_live_permission、residual_gap_acceptance_note。",
        ],
        "patch_notes": {
            "source": ["当前外部来源对“人工复核”支撑不足，只能 draft。"],
            "content": ["promotion decision 是评审证据，不是交易许可。"],
            "boundary": ["不得自动晋级。", "不得自动实盘。", "不得 hard gate。"],
            "conflict": ["与 Risk owner 不冲突，但阈值和最终许可必须归 Risk / Live owner。"],
        },
    },
    "P60-A08": {
        "candidate_path": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_sandbox_paper_live_gap_report_required_001.json"),
        "confidence": "medium_high",
        "required_followups": ["补 gap_report_not_live_permission=true。", "补 known_non_equivalence、unreconciled_gap、residual_risk_note。"],
        "patch_notes": {
            "source": ["建议补 QuantConnect reconciliation 为直接来源。"],
            "content": ["gap report 必须覆盖数据、时钟、成交、费用、滑点、延迟、market impact、订单状态、风控、账户差异。"],
            "boundary": ["gap report 通过不等于策略有效。", "gap report 通过不等于 live-ready。"],
            "conflict": ["与 Phase 58 simulation_live_gap_report_required 一致，建议 alias。"],
        },
    },
    "P60-A09": {
        "candidate_path": ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_order_lifecycle_mapping_required_001.json"),
        "confidence": "high",
        "required_followups": ["补 venue_order_status_mapping_version、reject_code_mapping_version、unknown_outcome_policy。", "补 REST/WebSocket/FIX adapter 差异说明。"],
        "patch_notes": {
            "source": ["FIX 是标准来源，但 REST/WebSocket broker states 仍需 venue-specific mapping。"],
            "content": ["统一生命周期至少覆盖接收、确认、部分成交、完全成交、撤单、拒单、过期、改单、费用事件。"],
            "boundary": ["不得把统一映射写成真实成交证明。"],
            "conflict": ["与 Phase 45 order semantics 可能重叠，需去重。"],
        },
    },
    "P60-A10": {
        "candidate_path": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json"),
        "confidence": "medium",
        "required_followups": [
            "补 broker/exchange rejection、risk control、kill switch、live risk policy 直接来源。",
            "补 risk_rehearsal_result_not_hard_gate=true。",
        ],
        "patch_notes": {
            "source": ["当前主要依赖内部 contract 和 Nautilus 环境来源，reviewed 前需补风险治理来源。"],
            "content": ["risk rehearsal 只能验证字段、策略链条和审计流程。"],
            "boundary": ["不得替代 live risk owner。", "不得自动拒单。", "不得自动停机。", "不得 hard gate。"],
            "conflict": ["与 Risk Management owner 不冲突，但必须保留 owner 边界。"],
        },
    },
}


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def archive_audit_result() -> Path:
    result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "imported_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "source_attachment": "C:/Users/dove/.codex/attachments/5e12065c-f892-4588-ac69-4efe87a6d1ef/pasted-text.txt",
        "summary_from_report": {
            "total": 9,
            "accepted_for_draft": 9,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "import_interpretation": {
            "itemized_count": len(TARGETS),
            "decision": "Use itemized P60-A01 through P60-A10 results because each listed item is accepted_for_draft.",
            "package_count_mismatch": True,
        },
        "global_required_patch": [
            "Set conflict_audit.approval_allowed=false for all Phase 60 candidates.",
            "accepted_for_draft is not reviewed, approved, default guidance, or hard gate.",
            "Platform, broker, exchange and framework sources are implementation patterns or supporting sources.",
            "Promotion, gap report, manifest and risk rehearsal results are not live permission.",
        ],
        "candidate_results": [
            {
                "candidate_id": read_json(
                    repo_path("codex-expert-kit", "rag", "candidates", *target["candidate_path"])
                )["candidate_id"],
                "research_task_id": task_id,
                "decision": "accepted_for_draft",
                "confidence": target["confidence"],
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_followups": target["required_followups"],
                "patch_notes": target["patch_notes"],
            }
            for task_id, target in TARGETS.items()
        ],
    }
    path = repo_path("docs", "audit", "audit_result_phase60_candidate_20260617_strict_v1.json")
    write_json(path, result)
    return path


def apply_to_candidate(task_id: str, target: dict[str, Any]) -> dict[str, Any]:
    path = repo_path("codex-expert-kit", "rag", "candidates", *target["candidate_path"])
    candidate = read_json(path)
    now = TODAY

    candidate.setdefault("status", {})
    candidate["status"].update(
        {
            "review_status": "accepted_for_draft",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Phase 60 candidate strict audit accepted this item for draft only; reviewed/approved/default guidance/hard gate are not allowed.",
            "updated_at": now,
        }
    )

    candidate.setdefault("conflict_audit", {})
    candidate["conflict_audit"]["approval_allowed"] = False
    candidate["conflict_audit"]["default_guidance_allowed"] = False
    candidate["conflict_audit"]["hard_gate_allowed"] = False
    candidate["conflict_audit"]["resolution_summary"] = (
        "External strict audit accepted this candidate for draft only. "
        "approval_allowed=false is required to avoid machine misread; formal reviewed/caveat_only requires a separate reviewed-preparation audit."
    )

    candidate.setdefault("machine_gate", {})
    candidate["machine_gate"].update(
        {
            "default_guidance": "deny",
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "requires_human_escalation": True,
            "reason": "accepted_for_draft only; reviewed/caveat_only requires a separate reviewed-preparation audit.",
        }
    )

    candidate.setdefault("conversion_target", {})
    candidate["conversion_target"]["target_review_status"] = "draft_preparation"
    candidate["conversion_target"]["default_guidance_target"] = "deny"
    candidate["conversion_target"]["hard_gate_target"] = "deny"

    candidate.setdefault("workflow", {})
    candidate["workflow"].update(
        {
            "stage": "accepted_for_draft",
            "queue_group": "ai_passed",
            "hidden_from_default_queue": True,
            "next_action": "export_reviewed_preparation_audit_package",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": None,
            "formal_review_status": None,
        }
    )

    candidate.setdefault("review", {})
    candidate["review"]["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "decision": "accepted_for_draft",
        "confidence": target["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_followups": target["required_followups"],
        "patch_notes": target["patch_notes"],
        "imported_by_task": TASK_ID,
        "imported_at": now,
    }
    candidate["review"]["review_status"] = "accepted_for_draft"
    candidate["review"]["default_guidance_allowed"] = False

    candidate.setdefault("audit_log", [])
    candidate["audit_log"].append(
        {
            "event": "external_ai_audit_imported",
            "at": now,
            "by": "codex",
            "task_id": TASK_ID,
            "audit_result_id": AUDIT_RESULT_ID,
            "decision": "accepted_for_draft",
            "notes": "Strict audit accepted for draft only; conflict_audit.approval_allowed patched to false.",
        }
    )

    write_json(path, candidate)
    return {
        "research_task_id": task_id,
        "candidate_id": candidate["candidate_id"],
        "candidate_path": rel(path),
        "decision": "accepted_for_draft",
        "confidence": target["confidence"],
    }


def main() -> int:
    audit_path = archive_audit_result()
    updated = [apply_to_candidate(task_id, target) for task_id, target in TARGETS.items()]

    report = {
        "report_id": "phase60_candidate_audit_import_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": rel(audit_path),
        "package_count_mismatch": {
            "summary_total": 9,
            "itemized_total": len(updated),
            "resolution": "Imported all 10 itemized accepted_for_draft decisions.",
        },
        "updated_count": len(updated),
        "accepted_for_draft_count": len(updated),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "blocked_count": 0,
        "updated_candidates": updated,
        "global_patch_applied": ["conflict_audit.approval_allowed=false"],
        "boundary": "No reviewed, approved, default guidance, hard gate, trading advice, or risk threshold advice was created.",
        "next_action": "Export reviewed/caveat_only preparation audit package in CEK-TA-578.",
    }
    path = repo_path("docs", "reports", "phase60_candidate_audit_import_report.json")
    write_json(path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
