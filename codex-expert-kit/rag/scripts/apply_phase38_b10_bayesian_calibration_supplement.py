"""Supplement Phase 38 B10 with Bayesian calibration evidence.

This script prepares only B10 for a third audit. It keeps B10 out of reviewed,
approved, default guidance, and hard-gate use.
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


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "P38-B10"
PACKAGE_ID = "phase38_b10_bayesian_calibration_third_audit_package_20260610"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    "cand_20260610_phase38_p38_b10_conformal_bayesian_calibration_001.json",
    start_file=__file__,
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase38_b10_bayesian_calibration_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_b10_bayesian_calibration_supplement_report.json", start_file=__file__
)


BAYESIAN_SOURCES = [
    {
        "source_id": "src_pmlr_kuleshov_calibrated_regression_bayesian_uncertainty",
        "source_title": "Accurate Uncertainties for Deep Learning Using Calibrated Regression",
        "source_url": "https://proceedings.mlr.press/v80/kuleshov18a.html",
        "source_type": "paper",
        "publisher": "PMLR / ICML",
        "published_at": "2018-07-03",
        "accessed_at": TODAY,
        "version": "PMLR v80",
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "limitations": [
            "该论文主要讨论回归/不确定性校准，不等同于交易阈值或 hard gate 策略。"
        ],
        "evidence_summary": (
            "Kuleshov et al. state that Bayesian methods provide an uncertainty framework, but approximate inference "
            "and model misspecification can make Bayesian uncertainty estimates inaccurate; they propose calibrated "
            "regression that can calibrate Bayesian/probabilistic uncertainty estimates given enough data."
        ),
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_aaai_bayesian_binning_into_quantiles",
        "source_title": "Obtaining Well Calibrated Probabilities Using Bayesian Binning",
        "source_url": "https://ojs.aaai.org/index.php/AAAI/article/view/9602",
        "source_type": "paper",
        "publisher": "AAAI",
        "published_at": "2015-01-25",
        "accessed_at": TODAY,
        "version": "AAAI 2015",
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "limitations": [
            "Bayesian Binning into Quantiles 是分类概率校准方法，不代表所有 Bayesian uncertainty calibration 场景。"
        ],
        "evidence_summary": (
            "The AAAI paper presents Bayesian Binning into Quantiles as a non-parametric Bayesian calibration method "
            "for classifier probability estimates and compares calibration performance against common post-processing methods."
        ),
        "quoted_excerpt_allowed": False,
    },
]


PATCH_SUMMARY = (
    "B10 已补 Bayesian calibration / Bayesian uncertainty calibration 直接来源："
    "PMLR calibrated regression 支撑 Bayesian/probabilistic uncertainty estimates 需要校准；"
    "AAAI Bayesian Binning into Quantiles 支撑 Bayesian classifier probability calibration。"
    "本条仍只能作为 calibration/uncertainty 增强层，不能替代 deterministic final gate。"
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def append_sources(candidate: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for source in BAYESIAN_SOURCES:
        if source["source_id"] not in existing:
            refs.append(source)
            existing.add(source["source_id"])

    quality = candidate.setdefault("source_quality", {})
    high_count = len([ref for ref in refs if isinstance(ref, dict) and ref.get("reliability") == "high"])
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score", 0) or 0), 88)
    quality["primary_source_count"] = high_count
    quality["supporting_source_count"] = max(len(refs) - high_count, 0)
    limitations = quality.setdefault("limitations", [])
    note = "已为 B10 补充 Bayesian calibration / Bayesian uncertainty calibration 直接来源；等待三审。"
    if isinstance(limitations, list) and note not in limitations:
        limitations.append(note)


def block_default(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    candidate["reviewed_allowed"] = False
    candidate["approved_allowed"] = False
    candidate["default_guidance_allowed"] = False
    candidate["hard_gate_allowed"] = False
    candidate["draft_conversion_allowed"] = True


def update_candidate(candidate: dict[str, Any]) -> None:
    append_sources(candidate)
    block_default(candidate)
    claim = candidate.setdefault("claim", {})
    claim["evidence_summary"] = PATCH_SUMMARY
    claim["interpretation_notes"] = (
        "B10 只定义 calibration/uncertainty 增强层；任何 Bayesian/conformal/probability calibration "
        "都不能绕过 deterministic final gate、阈值治理、shadow/paper 评估和人工审计。"
    )

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已补 Bayesian calibration 直接来源，等待三审；不是 reviewed、approved、default guidance 或 hard gate。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["next_action"] = "export_ai_audit"

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_b10_bayesian_calibration_supplement"
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = [
        "三审确认 PMLR calibrated regression 与 AAAI Bayesian Binning 是否足以支撑 Bayesian calibration 字样。",
        "三审确认是否保留 conformal / Bayesian calibration 合并 claim，或拆分为两个 formal draft。",
    ]
    ai_audit = review.setdefault("ai_audit", {})
    if isinstance(ai_audit, dict):
        ai_audit["supplemental_evidence_status"] = "ready_for_third_audit"
        ai_audit["reviewed_allowed"] = False
        ai_audit["approved_allowed"] = False
        ai_audit["default_guidance_allowed"] = False
        ai_audit["hard_gate_allowed"] = False
        ai_audit["source_requirements_resolved"] = [
            "Bayesian calibration source",
            "Bayesian uncertainty calibration source",
        ]

    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "b10_bayesian_calibration_supplement_added",
                "reason": PATCH_SUMMARY,
            }
        )


def write_research_doc(candidate: dict[str, Any]) -> None:
    lines = [
        "# Phase 38 B10 Bayesian Calibration 补证记录",
        "",
        "## 目标",
        "",
        "为二审保留的 B10 单独补充 Bayesian calibration / Bayesian uncertainty calibration 直接来源。本记录只用于三审准备，不代表 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 候选",
        "",
        f"- candidate_id: `{candidate['candidate_id']}`",
        f"- research_task_id: `{candidate['research_task_id']}`",
        f"- normalized_claim: `{candidate['claim']['normalized_claim']}`",
        f"- statement: {candidate['claim']['statement']}",
        "",
        "## 新增来源",
        "",
    ]
    for source in BAYESIAN_SOURCES:
        lines.extend(
            [
                f"### {source['source_id']}",
                "",
                f"- 标题：{source['source_title']}",
                f"- 链接：{source['source_url']}",
                f"- 类型：{source['source_type']}",
                f"- 证据摘要：{source['evidence_summary']}",
                "",
            ]
        )
    lines.extend(
        [
            "## 补丁摘要",
            "",
            PATCH_SUMMARY,
            "",
            "## 边界",
            "",
            "```text",
            "1. B10 仍是 candidate，等待三审。",
            "2. 不直接 reviewed，不 approved，不进入 default guidance，不允许 hard gate。",
            "3. calibration / uncertainty layer 只作为模型风险和人工复核辅助，不能替代确定性风控。",
            "```",
        ]
    )
    RESEARCH_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_audit_package(candidate: dict[str, Any]) -> None:
    package = {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_ai_third_audit_package",
        "generated_at": TODAY,
        "phase": "38",
        "task_id": "CEK-TA-289",
        "source_audit_result_id": "audit_result_phase38_extended_p1_supplemental_reaudit_20260610_strict_v2",
        "title": "Phase 38 B10 Bayesian Calibration 单条三审包",
        "purpose": "请复审 B10 补充 Bayesian calibration / Bayesian uncertainty calibration 来源后，是否可升级为 accepted_for_draft。",
        "candidate_count": 1,
        "hard_boundaries": [
            "candidate 不是正式知识。",
            "accepted_for_draft 不是 reviewed，也不是 approved。",
            "不得直接标记 reviewed、approved、default guidance 或 hard gate。",
            "calibration / uncertainty layer 不能绕过 deterministic final gate。",
        ],
        "auditor_instruction": {
            "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
            "must_check": [
                "PMLR calibrated regression 是否足以支撑 Bayesian/probabilistic uncertainty calibration。",
                "AAAI Bayesian Binning into Quantiles 是否足以支撑 Bayesian classifier probability calibration。",
                "claim 是否应保留 conformal / Bayesian calibration 合并表达，或拆成两个候选。",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": PACKAGE_ID,
                "decisions": [
                    {
                        "candidate_id": "string",
                        "research_task_id": "P38-B10",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reason": "string",
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "required_followups": ["string"],
                        "reviewed_allowed": False,
                        "approved_allowed": False,
                        "default_guidance_allowed": False,
                        "hard_gate_allowed": False,
                    }
                ],
            },
        },
        "candidate": candidate,
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    if candidate.get("research_task_id") != TASK_ID:
        raise SystemExit(f"Unexpected candidate task id: {candidate.get('research_task_id')}")
    update_candidate(candidate)
    write_json(CANDIDATE_PATH, candidate)
    write_research_doc(candidate)
    write_audit_package(candidate)
    report = {
        "report_id": "phase38_b10_bayesian_calibration_supplement_report",
        "generated_at": TODAY,
        "candidate_id": candidate["candidate_id"],
        "research_task_id": TASK_ID,
        "source_count": len(candidate.get("source_refs", [])),
        "new_source_ids": [source["source_id"] for source in BAYESIAN_SOURCES],
        "research_path": rel(RESEARCH_PATH),
        "audit_package_path": rel(AUDIT_PACKAGE_PATH),
        "candidate_path": rel(CANDIDATE_PATH),
        "boundary": {
            "formal_reviewed_created": False,
            "approved_created": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
