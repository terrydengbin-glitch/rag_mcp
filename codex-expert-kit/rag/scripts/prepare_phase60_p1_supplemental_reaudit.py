"""Supplement Phase 60 P1 needs_more_evidence candidates and export reaudit package."""

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


TODAY = "2026-06-18"
TASK_ID = "CEK-TA-587"
PACKAGE_ID = "phase60_p1_needs_evidence_supplemental_reaudit_package_20260618"
TARGETS = {
    "P60-P1-02": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_p1_replay_scenario_library_versioned_001.json"),
    "P60-P1-05": ("KB_07_RISK_MANAGEMENT", "cand_20260617_phase60_p1_live_canary_rollback_owner_required_001.json"),
    "P60-P1-06": ("KB_05_REPLAY_SIMULATION", "cand_20260617_phase60_p1_environment_drift_monitor_required_001.json"),
}


SUPPLEMENTAL_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P60-P1-02": [
        {
            "source_id": "src_dvc_reproducible_pipelines",
            "source_title": "Get Started with DVC",
            "source_url": "https://doc.dvc.org/start",
            "source_type": "official_doc",
            "publisher": "DVC",
            "reliability": "high",
            "score": 82,
            "freshness": "time_sensitive",
            "evidence_summary": "DVC describes Git-based data and model versioning and reproducible data-driven pipelines.",
            "limitations": ["General data/ML workflow source; map to replay scenario datasets through CEK-TA contract."],
            "accessed_at": TODAY,
            "relevance": "medium_high",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_mlflow_dataset_tracking",
            "source_title": "MLflow Dataset Tracking",
            "source_url": "https://mlflow.org/docs/latest/ml/dataset/",
            "source_type": "official_doc",
            "publisher": "MLflow",
            "reliability": "high",
            "score": 82,
            "freshness": "time_sensitive",
            "evidence_summary": "MLflow documents dataset tracking, versioning, management and lineage from raw data to model predictions.",
            "limitations": ["ML dataset source; use for dataset snapshot manifest and lineage, not trading outcome proof."],
            "accessed_at": TODAY,
            "relevance": "medium_high",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_pytest_parametrize",
            "source_title": "Parametrizing tests",
            "source_url": "https://docs.pytest.org/en/7.1.x/example/parametrize.html",
            "source_type": "official_doc",
            "publisher": "pytest",
            "reliability": "high",
            "score": 78,
            "freshness": "stable",
            "evidence_summary": "pytest documents parametrized tests, supporting repeatable scenario-style checks across input cases.",
            "limitations": ["General software testing source; does not define CEK-TA replay scenario schema."],
            "accessed_at": TODAY,
            "relevance": "medium",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_abides_high_fidelity_market_simulation",
            "source_title": "ABIDES: Towards High-Fidelity Market Simulation for AI Research",
            "source_url": "https://arxiv.org/abs/1904.12066",
            "source_type": "research_paper",
            "publisher": "arXiv",
            "reliability": "high",
            "score": 84,
            "freshness": "stable",
            "evidence_summary": "ABIDES is an agent-based interactive discrete event simulation environment for market applications with configurable scenarios and latency assumptions.",
            "limitations": ["Research simulator source; does not prove live profitability or CEK-TA schema by itself."],
            "accessed_at": TODAY,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        },
    ],
    "P60-P1-05": [
        {
            "source_id": "src_fia_automated_trading_risk_controls",
            "source_title": "Best Practices for Automated Trading Risk Controls and System Safeguards",
            "source_url": "https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf",
            "source_type": "industry_guidance",
            "publisher": "FIA",
            "reliability": "high",
            "score": 86,
            "freshness": "stable",
            "evidence_summary": "FIA discusses automated trading risk controls, granular pre-trade controls, kill switches, monitoring and governance responsibilities.",
            "limitations": ["Industry guidance; not legal advice and not a fixed CEK-TA threshold source."],
            "accessed_at": TODAY,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_cftc_automated_trading_safeguards",
            "source_title": "Concept Release on Risk Controls and System Safeguards for Automated Trading Environments",
            "source_url": "https://www.federalregister.gov/documents/2013/09/12/2013-22185/concept-release-on-risk-controls-and-system-safeguards-for-automated-trading-environments",
            "source_type": "regulatory_source",
            "publisher": "CFTC / Federal Register",
            "reliability": "high",
            "score": 82,
            "freshness": "stable",
            "evidence_summary": "The CFTC concept release discusses risk controls and safeguards for automated trading environments.",
            "limitations": ["Regulatory context source; does not define CEK-TA canary schema or live permission."],
            "accessed_at": TODAY,
            "relevance": "medium_high",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_google_sre_canarying_releases",
            "source_title": "Canarying Releases",
            "source_url": "https://sre.google/workbook/canarying-releases/",
            "source_type": "engineering_book",
            "publisher": "Google SRE",
            "reliability": "high",
            "score": 82,
            "freshness": "stable",
            "evidence_summary": "Google SRE documents canarying releases as exposing changes to small production traffic subsets and evaluating safety before wider rollout.",
            "limitations": ["Software deployment source; trading canary requires risk and live execution owner mapping."],
            "accessed_at": TODAY,
            "relevance": "medium_high",
            "quoted_excerpt_allowed": False,
        },
    ],
    "P60-P1-06": [
        {
            "source_id": "src_quantconnect_live_reconciliation",
            "source_title": "Reconciliation",
            "source_url": "https://www.quantconnect.com/docs/v2/writing-algorithms/live-trading/reconciliation",
            "source_type": "platform_doc",
            "publisher": "QuantConnect",
            "reliability": "high",
            "score": 86,
            "freshness": "time_sensitive",
            "evidence_summary": "QuantConnect documents deviations between model predictions and live brokerage fills, fees and order execution and the need for reconciliation.",
            "limitations": ["Platform-specific reconciliation source; use as drift/reconciliation pattern."],
            "accessed_at": TODAY,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_nautilus_live_reconciliation",
            "source_title": "Live Trading",
            "source_url": "https://nautilustrader.io/docs/latest/concepts/live/",
            "source_type": "framework_doc",
            "publisher": "NautilusTrader",
            "reliability": "high",
            "score": 86,
            "freshness": "time_sensitive",
            "evidence_summary": "NautilusTrader documents execution reconciliation aligning venue actual order and position state with internal event-built state.",
            "limitations": ["Framework-specific reconciliation source; not a universal broker rule."],
            "accessed_at": TODAY,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_nautilus_continuous_reconciliation",
            "source_title": "Configure a Live Trading Node",
            "source_url": "https://nautilustrader.io/docs/nightly/how_to/configure_live_trading/",
            "source_type": "framework_doc",
            "publisher": "NautilusTrader",
            "reliability": "medium_high",
            "score": 82,
            "freshness": "time_sensitive",
            "evidence_summary": "NautilusTrader describes continuous reconciliation by checking in-flight orders, open orders, position status and own order books.",
            "limitations": ["Nightly framework documentation; use as implementation pattern with version caveat."],
            "accessed_at": TODAY,
            "relevance": "high",
            "quoted_excerpt_allowed": False,
        },
    ],
}


def repo_path(*parts: str) -> Path:
    return resolve_repo_path(*parts, start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain JSON object")
    return data


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_path(task_id: str) -> Path:
    return repo_path("codex-expert-kit", "rag", "candidates", *TARGETS[task_id])


def add_sources(candidate: dict[str, Any], sources: list[dict[str, Any]]) -> dict[str, Any]:
    item = copy.deepcopy(candidate)
    existing = item.setdefault("source_refs", [])
    existing_ids = {str(source.get("source_id")) for source in existing if isinstance(source, dict)}
    for source in sources:
        if source["source_id"] not in existing_ids:
            existing.append(source)
    item.setdefault("source_quality", {})
    item["source_quality"]["source_count"] = len(existing)
    item["source_quality"]["primary_source_count"] = sum(
        1 for source in existing if isinstance(source, dict) and source.get("source_type") in {"official_doc", "framework_doc", "research_paper", "engineering_book", "industry_guidance", "regulatory_source"}
    )
    item["source_quality"]["quality_level"] = "medium_high"
    item.setdefault("audit_log", []).append(
        {
            "event": "supplemental_evidence_added",
            "at": TODAY,
            "by": "codex",
            "task_id": TASK_ID,
            "notes": "Added direct supplemental sources for Phase 60 P1 needs_more_evidence reaudit.",
        }
    )
    return item


def build_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "created_by": "codex",
        "phase": "Phase 60",
        "task_id": TASK_ID,
        "audit_goal": "严格复审 Phase 60 P1 三条 needs_more_evidence 候选是否可进入 accepted_for_reviewed_caveat_only；不得创建 approved、default guidance、hard gate 或 live permission。",
        "hard_boundaries": {
            "candidate_not_formal_knowledge": True,
            "reviewed_caveat_only_maximum": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "live_permission_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "must_search_professional_sources": True,
            "must_check_sources_cases_and_data": True,
        },
        "supplemental_focus": {
            "P60-P1-02": [
                "regression testing / reproducibility / dataset manifest 是否足以支撑 scenario library schema",
                "scenario library 通过是否仍被限制为测试覆盖证据",
            ],
            "P60-P1-05": [
                "FIA/CFTC/Google SRE 是否足以支撑 live canary rollback owner 的 reviewed/caveat_only 边界",
                "是否仍需要 broker-specific risk owner 来源",
            ],
            "P60-P1-06": [
                "QuantConnect / Nautilus live reconciliation 是否足以支撑 environment drift report",
                "drift report 是否仍被限制为治理和人工复核材料",
            ],
        },
        "allowed_decisions": ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"],
        "forbidden_decisions": ["approved", "default_guidance", "hard_gate", "live_permission"],
        "expected_output_schema": {
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
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
            ]
        },
        "candidates": candidates,
    }


def main() -> int:
    candidates: list[dict[str, Any]] = []
    updated_paths: list[str] = []
    for task_id in sorted(TARGETS):
        path = candidate_path(task_id)
        candidate = read_json(path)
        if candidate.get("status", {}).get("review_status") != "needs_more_evidence":
            raise ValueError(f"{path} is not needs_more_evidence")
        updated = add_sources(candidate, SUPPLEMENTAL_SOURCES[task_id])
        write_json(path, updated)
        candidates.append(updated)
        updated_paths.append(rel(path))

    package_path = repo_path("docs", "audit", f"{PACKAGE_ID}.json")
    report_path = repo_path("docs", "reports", "phase60_p1_needs_evidence_supplemental_reaudit_report.json")
    research_path = repo_path("docs", "research", "phase60_p1_needs_evidence_supplemental_research.md")
    write_json(package_path, build_package(candidates))

    report = {
        "report_id": "phase60_p1_needs_evidence_supplemental_reaudit_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "candidate_count": len(candidates),
        "updated_candidate_paths": updated_paths,
        "audit_package_path": rel(package_path),
        "supplemental_source_counts": {task_id: len(sources) for task_id, sources in SUPPLEMENTAL_SOURCES.items()},
        "next_action": "Submit supplemental reaudit package for strict external AI/human review.",
    }
    write_json(report_path, report)
    research_lines = [
        "# Phase 60 P1 needs_more_evidence 补证记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 补证范围",
        "",
        "P60-P1-02、P60-P1-05、P60-P1-06 在 reviewed-preparation 审计中仍需补直接来源。本轮补充 DVC、MLflow、pytest、ABIDES、FIA、CFTC、Google SRE、QuantConnect Reconciliation 和 NautilusTrader Live Reconciliation 等来源。",
        "",
        "## 边界",
        "",
        "补证只用于三审，不创建 reviewed、approved、default guidance、hard gate、live permission、交易建议或风险阈值。",
    ]
    research_path.write_text("\n".join(research_lines) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
