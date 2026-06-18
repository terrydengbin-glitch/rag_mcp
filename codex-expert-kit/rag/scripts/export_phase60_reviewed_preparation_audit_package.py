"""Export Phase 60 reviewed/caveat_only preparation audit package.

This script packages Phase 60 accepted_for_draft candidates for a second-stage
strict audit. It does not create formal reviewed knowledge.
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
PACKAGE_ID = "phase60_reviewed_preparation_audit_package_20260617"
REPORT_ID = "phase60_reviewed_preparation_gap_report"
TASK_ID = "CEK-TA-578"


TARGET_PATHS = [
    ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_environment_taxonomy_required_001.json"),
    ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_static_api_sandbox_contract_only_001.json"),
    ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_testnet_endpoint_isolation_required_001.json"),
    ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_paper_trading_not_live_required_001.json"),
    ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_replay_market_impact_assumption_required_001.json"),
    ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_environment_manifest_required_001.json"),
    ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_environment_promotion_evidence_required_001.json"),
    ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_sandbox_paper_live_gap_report_required_001.json"),
    ("KB_06_LIVE_EXECUTION", "cand_20260617_phase60_order_lifecycle_mapping_required_001.json"),
    ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_sandbox_risk_rehearsal_not_hard_gate_001.json"),
]


REVIEWED_PREPARATION_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "P60-A01": {
        "required_focus": [
            "确认 taxonomy 与 Phase 58 environment equivalence 的上下游关系，不重复定义等效链条。",
            "确认多平台来源足以避免 NautilusTrader 单一框架偏见。",
        ],
        "known_risk": "环境分类是通用治理规则，不得写成所有系统必须采用 NautilusTrader 架构。",
    },
    "P60-A02": {
        "required_focus": [
            "确认 static API sandbox 仅限 mocked response / API contract 语境。",
            "确认不会把 static sandbox 泛化为 exchange testnet 或 paper trading。",
        ],
        "known_risk": "mocked response 被误读为真实市场行为。",
    },
    "P60-A03": {
        "required_focus": [
            "确认 endpoint_scope_policy、credential_scope_policy、account_scope_policy、data_source_scope_policy 足以进入 reviewed/caveat_only。",
            "确认 Binance 来源只作为 Binance USD-M Futures testnet 示例。",
        ],
        "known_risk": "testnet 订单、余额或成交被写成 production fact。",
    },
    "P60-A04": {
        "required_focus": [
            "检查与现有 paper trading 不等于 live trading 知识是否需要 alias / merge。",
            "确认 paper broker model、paper fill policy 和 paper/live gap report 字段足够。",
        ],
        "known_risk": "paper trading 盈亏被误读为 live-ready。",
    },
    "P60-A05": {
        "required_focus": [
            "确认 no-market-impact、queue position、partial fill、market impact assumption 字段足够。",
            "确认 HftBacktest 只是 replay caveat 来源，不是所有框架的强制实现。",
        ],
        "known_risk": "replay fill 被误读为真实队列位置或真实冲击证据。",
    },
    "P60-A06": {
        "required_focus": [
            "确认 EnvironmentManifest schema 字段完整。",
            "确认 manifest 不被解释为策略有效、live-ready 或上线许可。",
        ],
        "known_risk": "内部 contract 支撑较强，但 reviewed 前仍需审计字段契约完整性。",
    },
    "P60-A07": {
        "required_focus": [
            "重点审计 promotion decision 是否只表示环境推进评审证据。",
            "确认 human_reviewer_required、promotion_not_live_permission、residual_gap_acceptance_note 足够。",
            "判断是否仍需更多外部 reconciliation / governance 来源。",
        ],
        "known_risk": "A07 来源相对偏内部，可能需要 needs_more_evidence。",
    },
    "P60-A08": {
        "required_focus": [
            "确认 gap_report_not_live_permission、known_non_equivalence、unreconciled_gap、residual_risk_note 足够。",
            "确认与 Phase 58 simulation-live gap report 可建立 alias 或上下游关系。",
        ],
        "known_risk": "gap report 通过被误读为 live-ready。",
    },
    "P60-A09": {
        "required_focus": [
            "确认 FIX Execution Report 足以支撑 canonical order lifecycle mapping。",
            "确认 REST/WebSocket/broker-specific 状态仍需 adapter mapping。",
        ],
        "known_risk": "统一映射被误读为真实成交证明。",
    },
    "P60-A10": {
        "required_focus": [
            "重点审计 sandbox risk rehearsal 不能替代 live risk owner 的来源是否足够。",
            "判断是否仍需 broker/exchange rejection、risk control、kill switch、live risk policy 直接来源。",
        ],
        "known_risk": "A10 来源相对偏内部，可能需要 needs_more_evidence。",
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


def candidate_path(parts: tuple[str, str]) -> Path:
    return repo_path("codex-expert-kit", "rag", "candidates", *parts)


def source_urls(candidate: dict[str, Any]) -> set[str]:
    urls: set[str] = set()
    for src in candidate.get("source_refs", []):
        if isinstance(src, dict) and isinstance(src.get("source_url"), str):
            urls.add(src["source_url"])
    return urls


def build_gap_report(candidates: list[dict[str, Any]], paths: list[Path]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    rows: list[dict[str, Any]] = []
    formal_index = read_json(repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json"))
    formal_ids = [item.get("knowledge_id", "") for item in formal_index.get("items", []) if "phase60" in item.get("knowledge_id", "")]

    for candidate, path in zip(candidates, paths, strict=True):
        cid = candidate.get("candidate_id", "")
        task_id = candidate.get("research_task_id", "")
        status = candidate.get("status", {})
        workflow = candidate.get("workflow", {})
        machine_gate = candidate.get("machine_gate", {})
        conflict = candidate.get("conflict_audit", {})
        ai_audit = candidate.get("review", {}).get("ai_audit", {})
        urls = source_urls(candidate)

        if status.get("review_status") != "accepted_for_draft":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "candidate_not_accepted_for_draft"})
        if workflow.get("queue_group") != "ai_passed":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "candidate_not_in_ai_passed_queue"})
        if conflict.get("approval_allowed") is not False:
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "conflict_approval_allowed_not_false"})
        for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if machine_gate.get(field) is not False:
                failures.append({"candidate_id": cid, "path": rel(path), "reason": f"machine_gate_{field}_not_false"})
        if machine_gate.get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "default_guidance_not_deny"})
        if ai_audit.get("decision") != "accepted_for_draft":
            failures.append({"candidate_id": cid, "path": rel(path), "reason": "missing_ai_audit_accepted_for_draft"})
        if len(urls) < 2:
            warnings.append({"candidate_id": cid, "path": rel(path), "reason": "low_external_source_diversity"})
        if task_id in {"P60-A07", "P60-A10"}:
            warnings.append({"candidate_id": cid, "path": rel(path), "reason": "prior_audit_flagged_internal_boundary_source_risk"})

        rows.append(
            {
                "research_task_id": task_id,
                "candidate_id": cid,
                "path": rel(path),
                "review_status": status.get("review_status"),
                "source_count": len(candidate.get("source_refs", [])),
                "external_source_url_count": len(urls),
                "reviewed_preparation_expectation": REVIEWED_PREPARATION_EXPECTATIONS.get(task_id, {}),
                "ready_for_reviewed_preparation_audit": status.get("review_status") == "accepted_for_draft",
            }
        )

    if formal_ids:
        failures.append(
            {
                "candidate_id": "phase60_formal_index",
                "path": "codex-expert-kit/rag/indexes/knowledge_items.json",
                "reason": f"phase60_formal_knowledge_already_exists:{formal_ids}",
            }
        )

    return {
        "report_id": REPORT_ID,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "candidate_count": len(candidates),
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "failures": failures,
        "warnings": warnings,
        "gate_status": "pass" if not failures else "fail",
        "formal_phase60_count": len(formal_ids),
        "formal_phase60_ids": formal_ids,
        "rows": rows,
        "boundary": "This report only checks readiness for reviewed/caveat_only preparation audit; it does not create formal reviewed knowledge.",
    }


def build_audit_package(candidates: list[dict[str, Any]], gap_report: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_package_id": PACKAGE_ID,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "phase": "Phase 60",
        "task_id": TASK_ID,
        "audit_goal": "严格审计 Phase 60 accepted_for_draft 候选是否可进入 formal reviewed/caveat_only 准备；不得创建 approved、default guidance 或 hard gate。",
        "scope": {
            "candidate_count": len(candidates),
            "included_research_task_ids": [candidate.get("research_task_id") for candidate in candidates],
            "source_audit_result_id": "audit_result_phase60_sandbox_replay_paper_candidate_20260617_strict_v1",
            "gap_report_id": REPORT_ID,
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_reviewed": True,
            "reviewed_caveat_only_is_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "live_permission_allowed": False,
            "must_search_professional_sources": True,
            "must_check_sources_cases_and_data": True,
        },
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
            "risk_threshold_advice",
            "live_permission",
        ],
        "required_audit_checks": [
            "逐条核验 source_refs 是否足以支撑 reviewed/caveat_only，而不仅是 draft。",
            "必须搜索相关专业网站、资料、案例和数据，对审计报告进行严格审计。",
            "检查 static API sandbox、exchange testnet、historical replay、realtime simulation、paper trading、live canary 和 live 是否被清晰区分。",
            "检查平台、broker、exchange、framework 来源是否被错误泛化。",
            "检查是否误把 sandbox/paper/replay 结果写成策略有效、live-ready、交易许可或 hard gate。",
            "检查与 Phase 37、Phase 45、Phase 58、Phase 59 的重复、alias、owner 边界和冲突。",
            "检查 P60-A07 和 P60-A10 是否仍需补充 reconciliation、live risk、kill switch 或 broker/exchange rejection 直接来源。",
            "检查候选是否存在中文乱码、mock/test 污染、私有策略参数、密钥、账户事实、风险阈值或实盘敏感信息。",
        ],
        "expected_output_schema": {
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | medium_high | high",
                    "reviewed_allowed": "boolean; true only for accepted_for_reviewed_caveat_only",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "trade_execution_advice_allowed": False,
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
            "package_summary": {
                "total": "integer",
                "accepted_for_reviewed_caveat_only": "integer",
                "needs_more_evidence": "integer",
                "rejected": "integer",
                "blocked": "integer",
            },
        },
        "gap_report_summary": {
            "gate_status": gap_report["gate_status"],
            "failure_count": gap_report["failure_count"],
            "warning_count": gap_report["warning_count"],
            "warnings": gap_report["warnings"],
        },
        "candidates": candidates,
    }


def main() -> int:
    paths = [candidate_path(parts) for parts in TARGET_PATHS]
    candidates = [read_json(path) for path in paths]

    gap_report = build_gap_report(candidates, paths)
    gap_path = repo_path("docs", "reports", "phase60_reviewed_preparation_gap_report.json")
    write_json(gap_path, gap_report)

    package = build_audit_package(candidates, gap_report)
    package_path = repo_path("docs", "audit", "phase60_reviewed_preparation_audit_package_20260617.json")
    write_json(package_path, package)

    for candidate, path in zip(candidates, paths, strict=True):
        candidate.setdefault("workflow", {})
        candidate["workflow"]["next_action"] = "await_reviewed_preparation_audit_result"
        candidate["workflow"]["reviewed_preparation_audit_package_id"] = PACKAGE_ID
        candidate.setdefault("audit_log", [])
        candidate["audit_log"].append(
            {
                "event": "reviewed_preparation_audit_package_exported",
                "at": TODAY,
                "by": "codex",
                "task_id": TASK_ID,
                "package_id": PACKAGE_ID,
                "notes": "Exported for strict reviewed/caveat_only preparation audit; no formal reviewed knowledge created.",
            }
        )
        write_json(path, candidate)

    export_report = {
        "report_id": "phase60_reviewed_preparation_export_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "audit_package_path": rel(package_path),
        "gap_report_path": rel(gap_path),
        "gap_gate_status": gap_report["gate_status"],
        "warnings": gap_report["warnings"],
        "boundary": "No formal reviewed, approved, default guidance, hard gate, trading advice, risk threshold advice, or live permission was created.",
        "next_action": "Submit phase60_reviewed_preparation_audit_package_20260617.json for external strict audit.",
    }
    export_report_path = repo_path("docs", "reports", "phase60_reviewed_preparation_export_report.json")
    write_json(export_report_path, export_report)

    print(json.dumps(export_report, ensure_ascii=False, indent=2))
    return 0 if gap_report["gate_status"] == "pass" else 2


if __name__ == "__main__":
    raise SystemExit(main())
