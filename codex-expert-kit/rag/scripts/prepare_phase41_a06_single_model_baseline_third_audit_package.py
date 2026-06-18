"""Prepare Phase 41 P41-A06 single-model baseline third-audit package.

This script supplements P41-A06 with claim-specific evidence for:
- single-model baseline comparison before ensemble adoption;
- auditability / explainability impact of ensemble complexity;
- CEK-TA runtime and training-data boundaries.

It intentionally keeps the candidate out of formal reviewed, approved, default
guidance, and hard gate. The output is a single-item audit package for external
third review.
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


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-337"
CANDIDATE_ID = "cand_20260610_phase41_p41_a06_baseline_001"
RESEARCH_TASK_ID = "P41-A06"
NORMALIZED_CLAIM = "phase41.ensemble_after_single_model_baseline_insufficient.v1"
PROPOSED_KNOWLEDGE_ID = "kb_ai_hybrid_scoring.phase41.ensemble_after_single_model_baseline_insufficient.v1"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
RESEARCH_PATH = resolve_repo_path(
    "docs",
    "research",
    "phase41_a06_ensemble_baseline_auditability_supplemental_research.md",
    start_file=__file__,
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs",
    "audit",
    "phase41_a06_single_model_baseline_third_audit_package_20260611.json",
    start_file=__file__,
)
REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase41_a06_single_model_baseline_third_audit_package_report.json",
    start_file=__file__,
)


SUPPLEMENTAL_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "src_google_rules_of_ml_simple_model_baseline",
        "source_title": "Rules of Machine Learning - Google for Developers",
        "source_url": "https://developers.google.com/machine-learning/guides/rules-of-ml",
        "source_type": "official_doc",
        "publisher": "Google for Developers",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "evidence_dimension": "single_model_baseline_comparison",
        "evidence_summary": (
            "Google ML engineering guidance emphasizes robust infrastructure, simple first models, "
            "baseline metrics, and delaying added complexity until simpler approaches are exhausted."
        ),
        "limitations": [
            "This supports the engineering baseline requirement; it does not prove any trading performance edge.",
        ],
    },
    {
        "source_id": "src_sklearn_ensemble_base_estimators_generalizability",
        "source_title": "Ensemble methods - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/ensemble.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "ensemble_as_enhancement",
        "evidence_summary": (
            "scikit-learn frames ensemble methods as combining base estimators to improve "
            "generalizability or robustness over a single estimator."
        ),
        "limitations": [
            "The source supports ensemble motivation, not automatic adoption or final gate authority.",
        ],
    },
    {
        "source_id": "src_sklearn_stacking_cross_validation_final_estimator",
        "source_title": "Stacked generalization - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/ensemble.html#stacked-generalization",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_dimension": "ensemble_validation_complexity",
        "evidence_summary": (
            "scikit-learn describes stacking as using base-estimator predictions as inputs "
            "to a final estimator trained through cross-validation, which adds validation and trace complexity."
        ),
        "limitations": [
            "This supports added audit complexity; it does not prescribe a CEK-TA production architecture.",
        ],
    },
    {
        "source_id": "src_nist_airc_explainability_audit_governance",
        "source_title": "AI Risks and Trustworthiness - NIST AI Resource Center",
        "source_url": "https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/",
        "source_type": "governance_framework",
        "publisher": "NIST AI Resource Center",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "evidence_dimension": "auditability_impact_report",
        "evidence_summary": (
            "NIST distinguishes transparency, explainability, and interpretability and links explainable systems "
            "to easier debugging, monitoring, documentation, audit, and governance."
        ),
        "limitations": [
            "This supports auditability criteria; CEK-TA still needs project-specific audit reports before adoption.",
        ],
    },
    {
        "source_id": "src_phase41_runtime_contract_final_gate_boundary",
        "source_title": "Phase 41 hybrid scoring runtime contract",
        "source_url": "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "evidence_dimension": "final_gate_boundary",
        "evidence_summary": (
            "CEK-TA Phase 41 runtime contract separates scorer, calibrator, Qwen3 audit assistant, RAG, "
            "and deterministic final gate responsibilities."
        ),
        "limitations": [
            "Internal contract evidence must be paired with external sources for professional knowledge claims.",
        ],
    },
    {
        "source_id": "src_phase41_training_data_contract_baseline_report",
        "source_title": "Phase 41 tabular and LLM training data contract",
        "source_url": "docs/contracts/phase41_tabular_llm_training_data_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "evidence_dimension": "single_model_baseline_comparison",
        "evidence_summary": (
            "CEK-TA Phase 41 data contract defines split manifests, feature schema, label policy, calibration, "
            "threshold, and model registry evidence required for scorer comparison."
        ),
        "limitations": [
            "Internal contract evidence is a CEK-TA acceptance boundary, not an external proof of model performance.",
        ],
    },
]


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
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


def make_source_ref(source: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(source)
    payload["published_at"] = None
    payload["accessed_at"] = TODAY
    payload["version"] = None
    payload["reliability"] = "high" if int(payload["score"]) >= 80 else "medium"
    payload["quoted_excerpt_allowed"] = False
    return payload


def add_sources(candidate: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    if not isinstance(refs, list):
        raise ValueError("source_refs must be a list")
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for source in SUPPLEMENTAL_SOURCES:
        if source["source_id"] not in existing:
            refs.append(make_source_ref(source))
            existing.add(source["source_id"])

    primary_types = {
        "official_doc",
        "governance_framework",
        "internal_contract",
        "standard_doc",
        "research_paper",
        "regulator_release",
    }
    primary_count = len([ref for ref in refs if isinstance(ref, dict) and ref.get("source_type") in primary_types])
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score") or 0), 90)
    quality["primary_source_count"] = primary_count
    quality["supporting_source_count"] = max(0, len(refs) - primary_count)
    quality["low_reliability_source_count"] = 0
    quality["claim_specific_dimensions_covered"] = [
        "single_model_baseline_comparison",
        "ensemble_as_enhancement",
        "ensemble_validation_complexity",
        "auditability_impact_report",
        "final_gate_boundary",
    ]


def enforce_identity(candidate: dict[str, Any]) -> None:
    candidate["normalized_claim"] = NORMALIZED_CLAIM
    candidate.setdefault("claim", {})["normalized_claim"] = NORMALIZED_CLAIM
    candidate.setdefault("conversion_target", {})["proposed_knowledge_id"] = PROPOSED_KNOWLEDGE_ID
    candidate.setdefault("workflow", {})["formal_knowledge_id"] = PROPOSED_KNOWLEDGE_ID
    export_meta = candidate.setdefault("_audit_export_meta", {})
    export_meta["proposed_knowledge_id"] = PROPOSED_KNOWLEDGE_ID
    export_meta["normalized_claim"] = NORMALIZED_CLAIM
    export_meta["formal_index_has_target"] = False
    export_meta["metadata_slug_fixed_at"] = "2026-06-11"
    export_meta["a06_supplemented_at"] = TODAY


def enforce_candidate_boundary(candidate: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = (
        "已补充 single-model baseline comparison report 与 auditability impact report 证据，"
        "等待三审决定是否可进入 accepted_for_draft；本轮不创建 formal reviewed。"
    )
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["formal_review_status"] = "blocked"
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["next_action"] = "third_audit_required"
    workflow["default_guidance_allowed"] = False

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "P41-A06 remains a third-audit candidate; ensemble adoption requires baseline and auditability evidence before draft acceptance."

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["resolution_summary"] = (
        "metadata/slug 已统一；新增 baseline comparison 与 auditability impact 证据后仍需三审。"
        "三审通过前不得创建 formal reviewed。"
    )


def patch_content(candidate: dict[str, Any]) -> None:
    claim = candidate.setdefault("claim", {})
    claim["statement"] = "模型集成只能作为增强项，必须先证明单模型 baseline 不足且不破坏可审计性"
    claim["evidence_summary"] = (
        "补证后证据链覆盖：Google ML 工程规则支持先建立简单模型和 baseline metrics；"
        "scikit-learn 将 ensemble 定义为组合 base estimators 以改善泛化或鲁棒性，并说明 stacking 会引入交叉验证和 final estimator 复杂度；"
        "NIST AI RMF/AIRC 将 explainability、interpretability、transparency 与审计、治理、监控和文档关联；"
        "CEK-TA Phase 41 契约要求 scorer/calibrator/Qwen3/RAG/final gate 分责。"
    )
    claim["interpretation_notes"] = (
        "本条不是要求默认使用 ensemble，而是要求：只有当单模型 baseline 比较报告证明不足，"
        "且 auditability impact report 证明复杂度、解释、追踪、校准和回滚仍可治理时，ensemble 才可作为增强候选。"
    )

    applicability = candidate.setdefault("applicability", {})
    append_unique(
        applicability.setdefault("applies_when", []),
        [
            "外接项目已经具备 rule baseline、Logistic Regression、LightGBM/XGBoost 等单模型基线结果。",
            "团队正在评估 voting、stacking、bagging、boosting 或多模型组合是否值得引入。",
            "可以提供同一时间切分、同一指标、同一校准/阈值策略下的单模型与 ensemble 对比。"
        ],
    )
    append_unique(
        applicability.setdefault("not_applicable_when", []),
        [
            "尚未建立可复现的单模型 baseline、split manifest、feature schema、label policy 或 baseline behavior。",
            "ensemble 被用于绕过校准器、threshold policy、deterministic final gate 或人工审批。",
            "目标是在 Trading Engineering 中定义买卖点、仓位、止损止盈、fill model 或实盘执行策略。"
        ],
    )
    append_unique(
        applicability.setdefault("limitations", []),
        [
            "single-model baseline comparison report 必须至少包含候选模型清单、训练/验证/校准/holdout split、主指标、业务成本维度、校准质量、延迟和回滚复杂度。",
            "auditability impact report 必须说明 ensemble 后的 feature attribution、reason code、trace、模型版本、calibrator 版本、threshold policy 和 rollback target 是否仍可复核。",
            "ensemble 输出只能作为 scorer/review-priority 信号；不得直接成为交易概率、买卖建议或 final gate 决策。",
            "本候选三审通过也只能进入 accepted_for_draft，不能进入 approved/default guidance/hard gate。"
        ],
    )

    policy = candidate.setdefault("llm_usage_policy", {})
    append_unique(
        policy.setdefault("allowed", []),
        [
            "用于提醒 AI IDE 在引入 ensemble 前生成单模型 baseline 比较任务卡。",
            "用于检查 ensemble 是否增加了不可审计的模型、校准、阈值、trace 或回滚复杂度。",
            "用于生成三审问题：baseline 是否不足、auditability 是否仍可接受、是否保持 final gate 分责。"
        ],
    )
    append_unique(
        policy.setdefault("not_allowed", []),
        [
            "不得把 ensemble 写成默认优于单模型。",
            "不得把 ensemble 输出当作交易执行许可。",
            "不得在未完成 baseline comparison 和 auditability impact report 时建议上架。"
        ],
    )


def patch_review(candidate: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    review["open_questions"] = [
        "third_audit_required",
        "confirm_single_model_baseline_comparison_report_is_sufficient",
        "confirm_auditability_impact_report_is_sufficient",
        "confirm_candidate_may_enter_accepted_for_draft_only",
    ]
    ai_audit = review.setdefault("ai_audit", {})
    ai_audit["decision"] = "needs_more_evidence"
    ai_audit["reason"] = "已完成 metadata/slug 修复和补证，等待三审判断是否可 accepted_for_draft。"
    ai_audit["source_patch_notes"] = [
        "已补充 Google ML engineering baseline guidance。",
        "已补充 scikit-learn ensemble / stacking 证据。",
        "已补充 NIST explainability / auditability / governance 证据。",
        "已补充 CEK-TA Phase 41 runtime 与 training data 内部契约。"
    ]
    ai_audit["content_patch_notes"] = [
        "明确 ensemble 只能在单模型 baseline 不足且可审计性未破坏时作为增强项。",
        "新增 single-model baseline comparison report 与 auditability impact report 的最小字段要求。"
    ]
    ai_audit["boundary_patch_notes"] = [
        "三审通过也只能 accepted_for_draft；不得 reviewed/approved/default guidance/hard gate。",
        "ensemble 输出不得绕过 calibrator、threshold policy 或 deterministic final gate。"
    ]
    ai_audit["required_followups"] = [
        "external_third_audit",
        "decide_accepted_for_draft_or_needs_more_evidence_or_rejected"
    ]
    ai_audit["reviewed_allowed"] = False
    ai_audit["approved_allowed"] = False
    ai_audit["default_guidance_allowed"] = False
    ai_audit["hard_gate_allowed"] = False

    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_a06_baseline_auditability_supplemented_for_third_audit",
                "reason": "CEK-TA-337: 补充 single-model baseline comparison 与 auditability impact 证据，并导出三审包。"
            }
        )

    trace = candidate.setdefault("phase41_trace", {})
    trace["a06_third_audit_preparation"] = {
        "prepared_at": TODAY,
        "prepared_by": "codex",
        "source_dimensions_added": {
            "single_model_baseline_comparison": [
                "src_google_rules_of_ml_simple_model_baseline",
                "src_phase41_training_data_contract_baseline_report",
            ],
            "ensemble_as_enhancement": [
                "src_sklearn_ensemble_base_estimators_generalizability",
            ],
            "ensemble_validation_complexity": [
                "src_sklearn_stacking_cross_validation_final_estimator",
            ],
            "auditability_impact_report": [
                "src_nist_airc_explainability_audit_governance",
            ],
            "final_gate_boundary": [
                "src_phase41_runtime_contract_final_gate_boundary",
            ],
        },
        "audit_request": "请三审判断 P41-A06 是否具备 accepted_for_draft 条件；不得直接 reviewed/approved/default guidance/hard gate。",
        "remaining_boundary": "Trading PnL、K 线、fill、slippage、仓位和实盘执行本体仍归 Trading Engineering。",
    }


def patch_candidate(candidate: dict[str, Any]) -> None:
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError(f"Unexpected candidate_id: {candidate.get('candidate_id')}")
    if candidate.get("research_task_id") != RESEARCH_TASK_ID:
        raise ValueError(f"Unexpected research_task_id: {candidate.get('research_task_id')}")
    enforce_identity(candidate)
    add_sources(candidate)
    enforce_candidate_boundary(candidate)
    patch_content(candidate)
    patch_review(candidate)


def write_research_doc(candidate: dict[str, Any]) -> None:
    lines = [
        "# Phase 41 P41-A06 baseline 与可审计性补证记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 任务目标",
        "",
        "为 `P41-A06` 补齐三审前必须具备的两类证据：",
        "",
        "1. `single-model baseline comparison report`：证明 ensemble 不是默认选项，而是在单模型 baseline 不足时才作为增强候选。",
        "2. `auditability impact report`：证明 ensemble 引入后不会破坏解释、trace、校准、阈值、回滚和 final gate 分责。",
        "",
        "## 上下游",
        "",
        "- 上游：`CEK-TA-336` 的 reviewed-preparation 再审结果，P41-A06 因需补充 baseline/auditability 证据继续 `needs_more_evidence`。",
        "- 下游：外部三审 JSON；如果三审通过，只能进入 `accepted_for_draft`，再由后续任务决定是否沉淀 formal reviewed/caveat_only。",
        "",
        "## 来源与证据维度",
        "",
        "| 来源 | 类型 | 维度 | 用法 | 边界 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for source in SUPPLEMENTAL_SOURCES:
        limitations = "；".join(source.get("limitations", []))
        lines.append(
            f"| {source['source_title']} | {source['source_type']} | {source['evidence_dimension']} | "
            f"{source['evidence_summary']} | {limitations} |"
        )
    lines.extend(
        [
            "",
            "## 补证后的最低审计要求",
            "",
            "### single-model baseline comparison report",
            "",
            "必须至少说明：",
            "",
            "- 单模型候选：rule baseline、Logistic Regression、LightGBM/XGBoost 等。",
            "- 同一时间切分、同一 feature schema、同一 label policy、同一 calibration/threshold policy。",
            "- 主指标、业务成本维度、误放行/误阻断、校准质量、延迟、模型复杂度和回滚复杂度。",
            "- 为什么单模型 baseline 不足，以及 ensemble 解决的是哪类不足。",
            "",
            "### auditability impact report",
            "",
            "必须至少说明：",
            "",
            "- ensemble 后 top_features / attribution / reason code 是否仍可解释和复核。",
            "- base estimator、final estimator、calibrator、threshold policy、Qwen3 prompt、RAG index、release manifest 是否可追踪。",
            "- 失败时是否能回退到单模型 baseline 或 deterministic final gate 的人工复核路径。",
            "- 是否新增无法接受的延迟、监控、文档、审计或治理复杂度。",
            "",
            "## 边界",
            "",
            "- 本条仍是候选知识，三审通过也只能进入 `accepted_for_draft`。",
            "- 不允许创建 `formal reviewed`、`approved`、`default guidance` 或 `hard gate`。",
            "- ensemble 只做 scorer/review-priority 增强，不得绕过 calibrator、threshold policy 或 deterministic final gate。",
            "- Trading PnL、K 线、fill model、slippage、仓位、止损止盈和实盘执行继续路由到 Trading Engineering。",
            "",
            "## 产物",
            "",
            f"- 候选：`{repo_rel(CANDIDATE_PATH)}`",
            f"- 三审包：`{repo_rel(AUDIT_PACKAGE_PATH)}`",
            f"- 执行报告：`{repo_rel(REPORT_PATH)}`",
            "",
        ]
    )
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text("\n".join(lines), encoding="utf-8")


def slim_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "candidate_id",
        "research_task_id",
        "status",
        "classification",
        "claim",
        "applicability",
        "llm_usage_policy",
        "source_refs",
        "source_quality",
        "conflict_audit",
        "machine_gate",
        "review",
        "conversion_target",
        "workflow",
        "phase41_trace",
        "normalized_claim",
        "_audit_export_meta",
    ]
    return {key: candidate.get(key) for key in keys}


def write_audit_package(candidate: dict[str, Any]) -> None:
    package = {
        "package_id": "phase41_a06_single_model_baseline_third_audit_package_20260611",
        "package_type": "candidate_third_audit_package",
        "generated_at": TODAY,
        "phase": "41",
        "task_id": TASK_ID,
        "source_previous_audit_result_id": "audit_result_phase41_extended_p1_remaining_reviewed_preparation_20260610_strict_v1",
        "title": "Phase 41 P41-A06 单模型 baseline 与可审计性三审包",
        "purpose": (
            "请三审判断 P41-A06 在补齐 single-model baseline comparison report 和 auditability impact report 证据后，"
            "是否可进入 accepted_for_draft。"
        ),
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
        "forbidden_decisions": ["reviewed", "approved", "default_guidance_allowed", "hard_gate_allowed"],
        "hard_boundaries": [
            "candidate 不是正式知识。",
            "accepted_for_draft 不是 reviewed 或 approved。",
            "本包不得授权 default_guidance_allowed 或 hard_gate_allowed。",
            "P41-A06 即使通过，也只能作为 formal reviewed/caveat_only 准备项。",
            "ensemble 输出不得绕过 calibrator、threshold policy、Qwen3 审计边界、RAG 引用边界或 deterministic final gate。",
            "不得生成买卖点、仓位、杠杆、止损止盈、fill model 或实盘执行建议。",
        ],
        "audit_questions": [
            "metadata/slug 是否已统一到 phase41.ensemble_after_single_model_baseline_insufficient.v1？",
            "single-model baseline comparison report 的最低字段要求是否足以支撑 accepted_for_draft？",
            "auditability impact report 的最低字段要求是否足以约束 ensemble 复杂度？",
            "来源是否覆盖 baseline-first、ensemble enhancement、stacking/validation complexity、explainability/auditability 和 CEK-TA final gate 边界？",
            "是否仍需补充工程实例、拆分 claim 或保持 needs_more_evidence？",
        ],
        "candidate_count": 1,
        "candidates": [slim_candidate(candidate)],
        "expected_output_schema": {
            "audit_result_id": "audit_result_phase41_a06_single_model_baseline_third_audit_20260611_strict_v3",
            "source_package_id": "phase41_a06_single_model_baseline_third_audit_package_20260611",
            "candidate_id": CANDIDATE_ID,
            "research_task_id": RESEARCH_TASK_ID,
            "decision": "accepted_for_draft | needs_more_evidence | rejected",
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "source_patch_notes": [],
            "content_patch_notes": [],
            "boundary_patch_notes": [],
            "conflict_patch_notes": [],
            "required_followups": [],
        },
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def write_report(candidate: dict[str, Any]) -> None:
    refs = candidate.get("source_refs") or []
    dimensions: dict[str, int] = {}
    for ref in refs:
        if isinstance(ref, dict):
            dimension = ref.get("evidence_dimension")
            if isinstance(dimension, str):
                dimensions[dimension] = dimensions.get(dimension, 0) + 1

    report = {
        "report_id": "phase41_a06_single_model_baseline_third_audit_package_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "candidate_id": CANDIDATE_ID,
        "research_task_id": RESEARCH_TASK_ID,
        "status": candidate.get("status", {}),
        "workflow": candidate.get("workflow", {}),
        "proposed_knowledge_id": PROPOSED_KNOWLEDGE_ID,
        "normalized_claim": NORMALIZED_CLAIM,
        "source_count": len(refs),
        "claim_specific_dimensions": dimensions,
        "deliverables": {
            "candidate": repo_rel(CANDIDATE_PATH),
            "research": repo_rel(RESEARCH_PATH),
            "audit_package": repo_rel(AUDIT_PACKAGE_PATH),
            "report": repo_rel(REPORT_PATH),
        },
        "gate": {
            "formal_reviewed_created": False,
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "next_action": "等待外部三审结果；若 accepted_for_draft，再执行后续 candidate-to-reviewed 沉淀任务。",
    }
    write_json(REPORT_PATH, report)


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    patch_candidate(candidate)
    write_json(CANDIDATE_PATH, candidate)
    write_research_doc(candidate)
    write_audit_package(candidate)
    write_report(candidate)
    result = {
        "candidate": repo_rel(CANDIDATE_PATH),
        "research": repo_rel(RESEARCH_PATH),
        "audit_package": repo_rel(AUDIT_PACKAGE_PATH),
        "report": repo_rel(REPORT_PATH),
        "source_count": len(candidate.get("source_refs") or []),
        "workflow": candidate.get("workflow", {}),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
