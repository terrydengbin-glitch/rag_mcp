"""Prepare Phase 41 P41-A05-R1 third-audit package.

The script supplements the remaining P41-A05-R1 candidate with direct sources
for latency/SLO, explainability boundary, and calibration quality. It keeps the
candidate out of reviewed/approved/default guidance and exports a focused
third-audit package.
"""

from __future__ import annotations

import copy
import json
import sys
from collections.abc import Iterable
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
CANDIDATE_ID = "cand_20260610_phase41_p41_a05_model_selection_business_cost_latency_explainability_calibration_governance_001"
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
THIRD_AUDIT_PACKAGE = resolve_repo_path(
    "docs", "audit", "phase41_a05_r1_third_audit_package_20260610.json", start_file=__file__
)
THIRD_AUDIT_REPORT = resolve_repo_path(
    "docs", "reports", "phase41_a05_r1_third_audit_preparation_report.md", start_file=__file__
)
REMAINING_FOLLOWUP_PATH = resolve_repo_path(
    "docs", "reports", "phase41_candidate_remaining_evidence_followups.json", start_file=__file__
)


SUPPLEMENTAL_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "src_sklearn_computational_performance_latency_throughput",
        "source_title": "Computational Performance - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/computing/computational_performance.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "latency_slo",
        "evidence_summary": "scikit-learn defines prediction latency, throughput, and percentile-based latency distributions for model performance comparisons.",
        "limitations": [
            "This source supports model-serving latency/throughput comparison, not trading PnL or execution latency.",
        ],
    },
    {
        "source_id": "src_sklearn_prediction_latency_example",
        "source_title": "Prediction Latency - scikit-learn example",
        "source_url": "https://scikit-learn.org/stable/auto_examples/applications/plot_prediction_latency.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "latency_slo",
        "evidence_summary": "scikit-learn demonstrates measuring estimator prediction latency in bulk and atomic prediction modes with latency distributions.",
        "limitations": [
            "This source supports benchmarking procedure expectations, not a fixed CEK-TA production latency target.",
        ],
    },
    {
        "source_id": "src_google_sre_implementing_slos_latency",
        "source_title": "Implementing SLOs - Google SRE Workbook",
        "source_url": "https://sre.google/workbook/implementing-slos/",
        "source_type": "standard_doc",
        "publisher": "Google SRE",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "evidence_dimension": "latency_slo",
        "evidence_summary": "Google SRE documents latency SLOs with percentile thresholds, supporting explicit SLO/SLA-style latency acceptance criteria.",
        "limitations": [
            "This source supports SLO framing; CEK-TA must define project-specific thresholds separately.",
        ],
    },
    {
        "source_id": "src_shap_causal_interpretation_boundary",
        "source_title": "Be careful when interpreting predictive models in search of causal insights - SHAP documentation",
        "source_url": "https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html",
        "source_type": "official_doc",
        "publisher": "SHAP",
        "score": 84,
        "relevance": "high",
        "freshness": "stable",
        "evidence_dimension": "explainability_boundary",
        "evidence_summary": "SHAP documentation explicitly distinguishes model correlations/feature attributions from causal insight, supporting an explainability boundary.",
        "limitations": [
            "This source supports feature-attribution boundary language; it does not validate any trading signal as causal.",
        ],
    },
    {
        "source_id": "src_sklearn_probability_calibration",
        "source_title": "Probability calibration - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/calibration.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "calibration_quality",
        "evidence_summary": "scikit-learn documents probability calibration, calibration curves/reliability diagrams, and model-specific calibration behavior.",
        "limitations": [
            "This source supports calibration-quality assessment; it does not permit raw scores to become final gate decisions.",
        ],
    },
    {
        "source_id": "src_sklearn_calibration_display_reliability_diagram",
        "source_title": "CalibrationDisplay - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibrationDisplay.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "calibration_quality",
        "evidence_summary": "scikit-learn documents calibration curves, also known as reliability diagrams, for comparing predicted probability bins with positive-class frequency.",
        "limitations": [
            "Reliability diagrams are diagnostic evidence; they are not alone sufficient for default guidance or hard gate approval.",
        ],
    },
    {
        "source_id": "src_sklearn_brier_score_loss",
        "source_title": "brier_score_loss - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "calibration_quality",
        "evidence_summary": "scikit-learn documents Brier score loss as measuring mean squared difference between predicted probabilities and actual outcomes.",
        "limitations": [
            "Brier score is one calibration/probability-quality signal and must be interpreted with reliability diagrams and holdout/calibration splits.",
        ],
    },
]


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def append_unique(target: list[Any], values: Iterable[Any]) -> None:
    for value in values:
        if value not in target:
            target.append(value)


def source_ref(source: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(source)
    payload["published_at"] = None
    payload["accessed_at"] = TODAY
    payload["version"] = None
    payload["reliability"] = "high" if int(payload["score"]) >= 80 else "medium"
    payload["quoted_excerpt_allowed"] = False
    return payload


def add_supplemental_sources(candidate: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for source in SUPPLEMENTAL_SOURCES:
        if source["source_id"] not in existing:
            refs.append(source_ref(source))
            existing.add(source["source_id"])

    primary_types = {
        "official_doc",
        "standard_doc",
        "governance_framework",
        "internal_contract",
        "research_paper",
        "security_standard",
        "regulator_release",
        "regulator_review",
    }
    primary_count = len([ref for ref in refs if isinstance(ref, dict) and ref.get("source_type") in primary_types])
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score") or 0), 90)
    quality["primary_source_count"] = primary_count
    quality["supporting_source_count"] = max(0, len(refs) - primary_count)
    quality["claim_specific_dimensions_covered"] = [
        "business_cost",
        "latency_slo",
        "explainability_boundary",
        "calibration_quality",
        "governance_complexity",
    ]


def enforce_safety(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "export_ai_audit"
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "P41-A05-R1 is a third-audit candidate; no reviewed, approved, default guidance, or hard gate permission is allowed."

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False


def patch_candidate(candidate: dict[str, Any]) -> None:
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Unexpected candidate_id")
    if candidate.get("research_task_id") != "P41-A05-R1":
        raise ValueError("Unexpected research_task_id")

    add_supplemental_sources(candidate)
    enforce_safety(candidate)

    candidate.setdefault("status", {}).update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "已补齐 latency/SLO、explainability boundary、calibration quality 的 claim-specific 来源，等待三审判断是否可进入 accepted_for_draft。",
            "updated_at": TODAY,
        }
    )

    candidate.setdefault("claim", {})["evidence_summary"] = (
        "已补齐 P41-A05-R1 二审要求的三类直接证据："
        "latency/SLO 与 serving benchmark、feature attribution / explainability boundary、"
        "probability calibration quality / reliability diagram / Brier score。"
        "本候选仍只等待三审，不进入 reviewed/approved/default guidance。"
    )

    limitations = candidate.setdefault("applicability", {}).setdefault("limitations", [])
    append_unique(
        limitations,
        [
            "latency/SLO 比较只约束 scorer serving 与审计系统延迟，不定义交易所撮合、fill、slippage 或下单延迟。",
            "feature attribution / SHAP 只能解释模型相关性和局部贡献，不得被写成因果交易规则或买卖信号。",
            "calibration quality 必须用独立 calibration/holdout 数据、reliability diagram 和 Brier/ECE 类指标复核，不得让 raw score 直接进入 final gate。",
            "模型选择比较不得被写成收益承诺、实盘上线许可或默认交易建议。",
        ],
    )

    trace = candidate.setdefault("phase41_trace", {})
    trace["third_audit_preparation"] = {
        "prepared_at": TODAY,
        "prepared_by": "codex",
        "source_dimensions_added": {
            "latency_slo": [
                "src_sklearn_computational_performance_latency_throughput",
                "src_sklearn_prediction_latency_example",
                "src_google_sre_implementing_slos_latency",
            ],
            "explainability_boundary": [
                "src_shap_causal_interpretation_boundary",
            ],
            "calibration_quality": [
                "src_sklearn_probability_calibration",
                "src_sklearn_calibration_display_reliability_diagram",
                "src_sklearn_brier_score_loss",
            ],
        },
        "audit_request": "请三审判断 P41-A05-R1 是否已具备 accepted_for_draft 条件；不得直接 reviewed/approved/default guidance/hard gate。",
        "remaining_boundary": "Trading PnL、fill、slippage、fee、K 线和执行延迟本体仍归 Trading Engineering，不纳入 AI Engineering claim。",
    }

    review = candidate.setdefault("review", {})
    review["open_questions"] = [
        "third_audit_required",
        "confirm_sources_cover_latency_slo_explainability_boundary_calibration_quality",
        "confirm_candidate_may_enter_accepted_for_draft_only",
    ]
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_a05_r1_third_audit_sources_added",
                "reason": "补齐二审要求的 latency/SLO、explainability boundary、calibration quality 直接来源，导出三审包。",
            }
        )


def write_third_audit_package(candidate: dict[str, Any]) -> None:
    package = {
        "package_id": "phase41_a05_r1_third_audit_package_20260610",
        "package_type": "candidate_third_audit_package",
        "generated_at": TODAY,
        "phase": "41",
        "task_id": "CEK-TA-326",
        "source_previous_audit_result_id": "audit_result_phase41_candidate_supplemental_reaudit_20260610_strict_v2",
        "title": "Phase 41 P41-A05-R1 三审补证包",
        "purpose": "请三审 P41-A05-R1 是否已具备 accepted_for_draft 条件。三审不得直接 reviewed、approved、default guidance 或 hard gate。",
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
        "forbidden_decisions": ["reviewed", "approved", "default_guidance_allowed", "hard_gate_allowed"],
        "audit_questions": [
            "新增 latency/SLO 与 serving benchmark 来源是否足以支撑模型选择必须比较延迟维度？",
            "新增 SHAP 解释性边界来源是否足以支撑可解释性边界维度？",
            "新增 calibration / reliability diagram / Brier score 来源是否足以支撑校准质量维度？",
            "该候选是否仍过宽，需要拆分为 cost/governance 与 latency/explainability/calibration 两条？",
            "如通过，只能进入 accepted_for_draft，不能进入 reviewed/approved/default guidance/hard gate。",
        ],
        "hard_boundaries": [
            "candidate 不是正式知识。",
            "accepted_for_draft 不是 reviewed 或 approved。",
            "本包不得授权 default_guidance_allowed 或 hard_gate_allowed。",
            "业务成本引用不得定义 Trading PnL、fee、slippage、fill model 或执行本体。",
            "latency/SLO 只约束 AI scorer serving 与审计系统响应，不定义交易执行延迟。",
        ],
        "candidate_count": 1,
        "candidates": [
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "status": candidate.get("status"),
                "workflow": candidate.get("workflow"),
                "classification": candidate.get("classification"),
                "claim": candidate.get("claim"),
                "applicability": candidate.get("applicability"),
                "source_refs": candidate.get("source_refs"),
                "source_quality": candidate.get("source_quality"),
                "conflict_audit": candidate.get("conflict_audit"),
                "machine_gate": candidate.get("machine_gate"),
                "conversion_target": candidate.get("conversion_target"),
                "review": candidate.get("review"),
                "phase41_trace": candidate.get("phase41_trace"),
            }
        ],
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase41_a05_r1_third_audit_20260610_strict_v3",
            "source_package_id": "phase41_a05_r1_third_audit_package_20260610",
            "decision": "accepted_for_draft | needs_more_evidence | rejected",
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "source_patch_notes": [],
            "content_patch_notes": [],
            "boundary_patch_notes": [],
            "required_followups": [],
        },
    }
    write_json(THIRD_AUDIT_PACKAGE, package)


def write_report(candidate: dict[str, Any]) -> None:
    sources = candidate.get("source_refs") or []
    dimension_counts: dict[str, int] = {}
    for source in sources:
        if isinstance(source, dict):
            dimension = source.get("evidence_dimension")
            if isinstance(dimension, str):
                dimension_counts[dimension] = dimension_counts.get(dimension, 0) + 1

    lines = [
        "# Phase 41 P41-A05-R1 三审补证报告",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        "已为 P41-A05-R1 补齐二审指出的三类证据：latency/SLO、explainability boundary、calibration quality。",
        "",
        "本次只导出三审包，不生成 formal reviewed，不设置 approved/default guidance/hard gate。",
        "",
        "## 补证维度",
        "",
        "| 维度 | 来源数量 |",
        "| --- | ---: |",
    ]
    for key in ["latency_slo", "explainability_boundary", "calibration_quality"]:
        lines.append(f"| {key} | {dimension_counts.get(key, 0)} |")
    lines.extend(
        [
            "",
            "## 三审包",
            "",
            f"- `{repo_rel(THIRD_AUDIT_PACKAGE)}`",
            "",
            "## 边界",
            "",
            "- 三审通过也只能进入 `accepted_for_draft`。",
            "- 不得进入 `reviewed`、`approved`、`default_guidance` 或 `hard_gate`。",
            "- Trading PnL、fill、slippage、fee、K 线和执行延迟本体继续归 Trading Engineering。",
            "",
        ]
    )
    THIRD_AUDIT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def write_remaining_followup(candidate: dict[str, Any]) -> None:
    payload = {
        "report_id": "phase41_candidate_remaining_evidence_followups",
        "generated_at": TODAY,
        "source_audit_result_id": "audit_result_phase41_candidate_supplemental_reaudit_20260610_strict_v2",
        "remaining_count": 1,
        "items": [
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": candidate.get("research_task_id"),
                "status": "ready_for_third_audit",
                "third_audit_package": repo_rel(THIRD_AUDIT_PACKAGE),
                "reason": "已补齐二审要求的 latency/SLO、explainability boundary、calibration quality 直接来源，等待三审。",
                "required_followups": [
                    "external_ai_or_human_third_audit",
                    "decide_accepted_for_draft_or_split_claim",
                ],
            }
        ],
        "boundary": "remaining candidates are not reviewed, approved, default guidance, or hard gate enabled.",
    }
    write_json(REMAINING_FOLLOWUP_PATH, payload)


def main() -> None:
    candidate = read_json(CANDIDATE_PATH)
    patch_candidate(candidate)
    write_json(CANDIDATE_PATH, candidate)
    write_third_audit_package(candidate)
    write_report(candidate)
    write_remaining_followup(candidate)
    result = {
        "candidate": repo_rel(CANDIDATE_PATH),
        "third_audit_package": repo_rel(THIRD_AUDIT_PACKAGE),
        "third_audit_report": repo_rel(THIRD_AUDIT_REPORT),
        "remaining_followup": repo_rel(REMAINING_FOLLOWUP_PATH),
        "source_count": len(candidate.get("source_refs") or []),
        "default_guidance_allowed": candidate.get("workflow", {}).get("default_guidance_allowed"),
        "machine_gate": candidate.get("machine_gate", {}).get("default_guidance"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
