"""Supplement Phase 37 Backtest reviewed-blocked candidates B10/B11/B12.

The reviewed-preparation audit accepted 9 Backtest candidates and returned
B10/B11/B12 to needs_more_evidence. This script supplements those candidates
with a CEK-TA backtest_run_manifest contract and external references, then
exports a strict supplemental reaudit package.
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
TASK_ID = "CEK-TA-420"
PARTITION_ID = "KB_04_BACKTEST"
PACKAGE_ID = "phase37_backtest_reviewed_blocked_supplemental_reaudit_package_20260611"
SOURCE_AUDIT_ID = "audit_result_phase37_backtest_reviewed_preparation_20260611_strict_v1"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
CONTRACT_PATH = resolve_repo_path("docs", "contracts", "phase37_backtest_run_manifest_contract.md", start_file=__file__)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase37_backtest_reviewed_blocked_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_backtest_reviewed_blocked_supplemental_report.json", start_file=__file__
)


TARGET_TASKS = {
    "P37-E-B10": "cand_20260611_phase37_backtest_profit_factor_drawdown_context_required_001",
    "P37-E-B11": "cand_20260611_phase37_backtest_reproducibility_package_required_001",
    "P37-E-B12": "cand_20260611_phase37_backtest_strategy_version_and_data_version_required_001",
}


SUPPLEMENTAL_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P37-E-B10": [
        {
            "source_id": "src_p37_backtest_contract_metric_report",
            "source_title": "Phase 37 Backtest Run Manifest Contract",
            "source_url": "docs/contracts/phase37_backtest_run_manifest_contract.md",
            "source_type": "internal_contract",
            "publisher": "CEK-TA",
            "published_at": TODAY,
            "accessed_at": TODAY,
            "version": "v1",
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "定义 profit_factor、max_drawdown、return_over_max_drawdown 的 CEK-TA 内部 metric_report 字段和解释边界。",
            "limitations": ["内部契约只支撑 CEK-TA 字段语义，不证明任何策略有效。"],
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_quantconnect_backtest_statistics",
            "source_title": "Backtest Statistics",
            "source_url": "https://www.quantconnect.com/docs/v2/cloud-platform/api-reference/backtest-management/read-backtest/backtest-statistics",
            "source_type": "platform_doc",
            "publisher": "QuantConnect",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "medium_high",
            "evidence_summary": "列出 backtest statistics、drawdown、fees 等字段语义，可作为回测指标报告实现示例。",
            "limitations": ["平台实现示例，不能泛化为所有 backtest engine。"],
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_titanfx_profit_factor",
            "source_title": "What is Profit Factor",
            "source_url": "https://research.titanfx.com/glossary/what-is-profit-factor",
            "source_type": "broker_glossary",
            "publisher": "Titan FX",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium",
            "relevance": "medium_high",
            "evidence_summary": "给出 profit factor 的定义、用途和局限，可作为 supporting source；不得单独支撑 reviewed。",
            "limitations": ["教育/券商资料，只能作为 supporting source。"],
            "quoted_excerpt_allowed": False,
        },
    ],
    "P37-E-B11": [
        {
            "source_id": "src_p37_backtest_contract_reproducibility_package",
            "source_title": "Phase 37 Backtest Run Manifest Contract",
            "source_url": "docs/contracts/phase37_backtest_run_manifest_contract.md",
            "source_type": "internal_contract",
            "publisher": "CEK-TA",
            "published_at": TODAY,
            "accessed_at": TODAY,
            "version": "v1",
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "定义 reproducibility_package 必填字段，包括 code_commit、dependency lockfile、config hash、input/output artifacts、日志、lineage 和 replay job。",
            "limitations": ["内部契约只定义 CEK-TA 逻辑字段，不指定外部项目必须使用 MLflow 或 DVC。"],
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_mlflow_tracking",
            "source_title": "MLflow Tracking",
            "source_url": "https://mlflow.org/docs/latest/ml/tracking/",
            "source_type": "framework_doc",
            "publisher": "MLflow",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "high",
            "evidence_summary": "MLflow Tracking 支撑记录参数、代码版本、指标和输出文件。",
            "limitations": ["框架实现示例，不是 CEK-TA 唯一工具要求。"],
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_dvc_pipelines",
            "source_title": "Get Started: Data Pipelines",
            "source_url": "https://doc.dvc.org/start/data-pipelines/data-pipelines",
            "source_type": "framework_doc",
            "publisher": "DVC",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "high",
            "evidence_summary": "DVC pipelines 支撑 versioned pipeline、dependencies、outputs 和 reproducible workflows。",
            "limitations": ["框架实现示例，不是 CEK-TA 唯一工具要求。"],
            "quoted_excerpt_allowed": False,
        },
    ],
    "P37-E-B12": [
        {
            "source_id": "src_p37_backtest_contract_versioning",
            "source_title": "Phase 37 Backtest Run Manifest Contract",
            "source_url": "docs/contracts/phase37_backtest_run_manifest_contract.md",
            "source_type": "internal_contract",
            "publisher": "CEK-TA",
            "published_at": TODAY,
            "accessed_at": TODAY,
            "version": "v1",
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "定义 strategy_rule_version、parameter_hash、dataset_version、calendar/session version、cost/fill/slippage/fee model version 等回测证据包字段。",
            "limitations": ["内部契约只定义 CEK-TA 逻辑字段，外接项目需映射自身字段。"],
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_mlflow_dataset_tracking",
            "source_title": "MLflow Dataset Tracking",
            "source_url": "https://mlflow.org/docs/latest/ml/dataset/",
            "source_type": "framework_doc",
            "publisher": "MLflow",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "medium_high",
            "evidence_summary": "MLflow Dataset Tracking 支撑 dataset、model、metrics 和 evaluation artifacts 的 tracking/versioning。",
            "limitations": ["框架实现示例，不是 CEK-TA 唯一工具要求。"],
            "quoted_excerpt_allowed": False,
        },
        {
            "source_id": "src_mlflow_model_registry",
            "source_title": "MLflow Model Registry",
            "source_url": "https://mlflow.org/docs/latest/ml/model-registry/",
            "source_type": "framework_doc",
            "publisher": "MLflow",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "medium",
            "evidence_summary": "MLflow registry 支撑 model version、run linkage、lineage 和 rollback 语义，可作为版本追踪 supporting source。",
            "limitations": ["模型注册语义仅作版本追踪类比，不替代 backtest_run_manifest。"],
            "quoted_excerpt_allowed": False,
        },
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (str(source.get("source_url") or ""), str(source.get("source_title") or ""))


def merge_sources(candidate: dict[str, Any], task_id: str) -> list[dict[str, Any]]:
    sources = [source for source in candidate.get("source_refs", []) if isinstance(source, dict)]
    seen = {source_key(source) for source in sources}
    for source in SUPPLEMENTAL_SOURCES[task_id]:
        if source_key(source) not in seen:
            sources.append(source)
            seen.add(source_key(source))
    return sources


def update_candidate(candidate: dict[str, Any], task_id: str) -> dict[str, Any]:
    candidate["source_refs"] = merge_sources(candidate, task_id)
    candidate.setdefault("source_quality", {})["supplemental_evidence_status"] = "ready_for_reaudit"
    candidate["source_quality"]["supplemental_source_count"] = len(SUPPLEMENTAL_SOURCES[task_id])
    candidate["source_quality"].setdefault("limitations", []).append(
        "本轮补证将 CEK-TA 内部 backtest_run_manifest 契约作为字段本体主来源，外部工具文档仅作实现语义示例。"
    )

    review = candidate.setdefault("review", {})
    review.setdefault("open_questions", [])
    review["reviewed_blocked_supplement"] = {
        "task_id": TASK_ID,
        "source_audit_result_id": SOURCE_AUDIT_ID,
        "supplemented_at": TODAY,
        "contract_path": "docs/contracts/phase37_backtest_run_manifest_contract.md",
        "supplemental_sources": [source["source_id"] for source in SUPPLEMENTAL_SOURCES[task_id]],
        "decision_boundary": "补证后只能请求 accepted_for_reviewed_caveat_only；不得 approved/default guidance/hard gate。",
    }
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["updated_at"] = TODAY
    status["decision_reason"] = "已补充 CEK-TA backtest_run_manifest 契约和外部来源，等待 reviewed/caveat_only 再审。"

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "export_reaudit_package"
    workflow["current_task_id"] = TASK_ID
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["formalization_allowed"] = False
    return candidate


def contract_excerpt() -> dict[str, Any]:
    return {
        "path": "docs/contracts/phase37_backtest_run_manifest_contract.md",
        "status": "included_by_reference",
        "key_sections": [
            "metric_report 字段契约",
            "profit_factor / max_drawdown / return_over_max_drawdown 指标定义",
            "reproducibility_package",
            "strategy_identity / data_identity / market_calendar_identity / execution_assumption_identity",
            "MCP/RAG 使用边界",
        ],
        "summary": "CEK-TA 内部契约定义回测证据包、复现包、策略/数据/日历/成本/fill 版本和指标解释边界，是 B10/B11/B12 reviewed/caveat_only 的字段本体来源。",
    }


def build_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "package_id": PACKAGE_ID,
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "package_type": "reviewed_blocked_supplemental_reaudit",
        "scope": {
            "phase": "Phase 37",
            "branch": "Trading Engineering",
            "partition_id": PARTITION_ID,
            "tree_node_id": "kt.trading_engineering.backtest",
            "candidate_count": len(candidates),
            "target_research_task_ids": sorted(TARGET_TASKS),
            "source_audit_result_id": SOURCE_AUDIT_ID,
        },
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "this_package_may_allow_reviewed_caveat_only": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "must_not_generate": ["买卖点", "仓位", "杠杆", "止损止盈参数", "实盘执行建议"],
        },
        "audit_instructions": [
            "必须搜索相关专业网站、论文、官方文档、资料、案例和数据，对补证内容进行严格审计。",
            "重点判断 B10 的 profit factor、drawdown、return/drawdown 定义和局限是否已由 CEK-TA 契约加外部来源充分支撑。",
            "重点判断 B11/B12 的 backtest_run_manifest、reproducibility_package、strategy/data/calendar/cost/fill 版本字段是否已由 CEK-TA 内部契约充分支撑。",
            "外部工具文档只能作为实现语义示例，不得被写成强制工具依赖。",
            "只能输出 accepted_for_reviewed_caveat_only / needs_more_evidence / rejected / blocked；不得输出 approved/default guidance/hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "package_id": PACKAGE_ID,
            "quality_gate": {"pass": "boolean", "reason": "string"},
            "summary": {
                "total": 3,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "P37-E-B10 | P37-E-B11 | P37-E-B12",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "confidence": "low | medium | high",
                    "reviewed_allowed": "boolean",
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "required_followups": ["string"],
                    "patch_notes": {"source": ["string"], "content": ["string"], "boundary": ["string"], "conflict": ["string"]},
                }
            ],
        },
        "contract_excerpt": contract_excerpt(),
        "candidates": candidates,
    }


def write_research(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 37 Backtest B10/B11/B12 Reviewed 阻断项补证研究",
        "",
        f"生成时间：{TODAY}",
        "",
        "## 补证目标",
        "",
        "B10/B11/B12 在 reviewed-preparation 审计中被判定为 `needs_more_evidence`。本轮补证使用 CEK-TA 内部 `backtest_run_manifest` 契约作为字段本体主来源，并用外部工具/平台文档作为实现语义示例。",
        "",
        "## 补证边界",
        "",
        "```text",
        "不得 approved。",
        "不得 default guidance。",
        "不得 hard gate。",
        "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        "```",
        "",
        "## 候选与来源",
        "",
    ]
    for candidate in candidates:
        lines.append(f"### {candidate['research_task_id']} / {candidate['candidate_id']}")
        lines.append("")
        lines.append(candidate.get("claim", {}).get("statement", ""))
        lines.append("")
        for source in SUPPLEMENTAL_SOURCES[candidate["research_task_id"]]:
            lines.append(f"- {source['source_title']}：{source['source_url']}，作用：{source['evidence_summary']}")
        lines.append("")
    RESEARCH_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    updated_candidates: list[dict[str, Any]] = []
    for task_id, candidate_id in TARGET_TASKS.items():
        path = CANDIDATE_DIR / f"{candidate_id}.json"
        candidate = read_json(path)
        if candidate.get("research_task_id") != task_id:
            raise ValueError(f"{path}: research_task_id mismatch")
        if candidate.get("status", {}).get("ingestion_decision") not in {"needs_more_evidence", "ready_for_reaudit"}:
            raise ValueError(f"{candidate_id}: expected needs_more_evidence before supplement")
        candidate = update_candidate(candidate, task_id)
        write_json(path, candidate)
        updated_candidates.append(candidate)

    write_research(updated_candidates)
    package = build_package(updated_candidates)
    report = {
        "report_id": "phase37_backtest_reviewed_blocked_supplemental_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "quality_gate": {
            "pass": len(updated_candidates) == 3 and CONTRACT_PATH.exists(),
            "reason": "B10/B11/B12 已补充 CEK-TA backtest_run_manifest 契约和外部实现语义来源。",
        },
        "candidate_count": len(updated_candidates),
        "candidate_ids": [candidate["candidate_id"] for candidate in updated_candidates],
        "audit_package": str(AUDIT_PACKAGE_PATH),
        "research": str(RESEARCH_PATH),
        "contract": str(CONTRACT_PATH),
        "next_step": "等待外部严格再审；若通过，再执行 CEK-TA-421 沉淀剩余 3 条 formal reviewed/caveat_only。",
    }
    write_json(AUDIT_PACKAGE_PATH, package)
    write_json(REPORT_PATH, report)
    if not report["quality_gate"]["pass"]:
        raise SystemExit(json.dumps(report, ensure_ascii=False, indent=2))
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
