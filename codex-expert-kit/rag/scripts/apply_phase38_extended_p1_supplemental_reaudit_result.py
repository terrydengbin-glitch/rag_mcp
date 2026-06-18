"""Import Phase 38 P0-Extended / P1 supplemental re-audit result.

The second audit accepts 13 supplemented candidates for the formal draft queue
and keeps B10 in needs-more-evidence. It does not create reviewed or approved
knowledge and does not enable default guidance or hard-gate use.
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
AUDIT_RESULT_ID = "audit_result_phase38_extended_p1_supplemental_reaudit_20260610_strict_v2"
SOURCE_PACKAGE_ID = "phase38_extended_p1_supplemental_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_extended_p1_supplemental_reaudit_import_report.json", start_file=__file__
)


ACCEPTED_TASKS: dict[str, str] = {
    "P38-A09": "SHAP causal warning 与 causal inference 来源已补足；feature attribution 不得当作因果证据。",
    "P38-A10": "NDCG 与 LightGBM ranking 来源已补足；ranking model 仅用于人工复核优先级。",
    "P38-C10-R1": "空 slug 已修复；point-in-time、training-serving skew 与 domain shift 来源足够。",
    "P38-D07": "RAG、prompt/model optimization 与 SFT 来源组合足够；该规则是 CEK-TA P0/P1 治理策略。",
    "P38-D08": "PEFT/LoRA、structured output 与 JSON Schema 来源已补足；LoRA 不作为事实来源。",
    "P38-D10": "RAG faithfulness、LLM-as-judge 与 CEK-TA citation contract 足够；teacher 只作 baseline/judge。",
    "P38-E07": "ablation study 与 MLflow/DVC 版本追踪足够；必须隔离变量。",
    "P38-E08": "Ragas 与 CEK-TA citation contract 足够；shadow 记录不得自动放行交易。",
    "P38-E09": "OPE 与 Trading Engineering fill/cost boundary 已补足；AI Engineering 不定义交易成本本体。",
    "P38-E10": "active learning survey 支撑 human-in-the-loop 采样；draft 需补 sampling bias 防护。",
    "P38-F10": "LLM compression survey 支撑 compression/quantization/distillation；压缩后必须重新评估。",
    "P38-G05": "RAG faithfulness 与 CEK-TA citation resolver 足够；citation completeness 仅作 shadow 指标。",
    "P38-G06": "CEK-TA active retrieval 与 citation contract 足够；no-hit 不允许现场编造规则。",
}

B10_TASK = "P38-B10"
B10_REASON = (
    "conformal prediction 与 probability calibration 来源已补足，但当前候选仍写 "
    "conformal / Bayesian calibration，缺 Bayesian calibration / Bayesian uncertainty calibration 直接来源。"
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


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    indexed: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        item = read_json(path)
        task_id = item.get("research_task_id")
        if isinstance(task_id, str):
            indexed[task_id] = (path, item)
    return indexed


def block_default_guidance(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    audit = review.setdefault("ai_audit", {})
    if isinstance(audit, dict):
        audit["reviewed_allowed"] = False
        audit["approved_allowed"] = False
        audit["default_guidance_allowed"] = False
        audit["hard_gate_allowed"] = False
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


def append_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def mark_accepted(candidate: dict[str, Any], reason: str) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": f"补证二审通过：{reason} 仅进入 formal draft 队列，不是 reviewed、approved、default guidance 或 hard gate。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "ai_audited",
            "queue_group": "ai_passed",
            "formal_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
            "formal_review_status": "draft",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "next_action": "apply_ai_audit_patch",
        }
    )
    block_default_guidance(candidate)
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_reaudit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = ["进入 formal draft 转换时必须保留二审 patch notes 和 default_guidance=false。"]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "notes": reason,
    }
    append_log(candidate, "extended_p1_supplemental_reaudit_accepted_for_draft", reason)
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "notes": reason,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }


def keep_b10_needs_more(candidate: dict[str, Any]) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": B10_REASON,
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "next_action": "supplement_bayesian_calibration_source_then_reaudit",
        }
    )
    block_default_guidance(candidate)
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_reaudit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = [
        "补 Bayesian calibration / Bayesian uncertainty calibration 直接来源后再二审。",
        "或将 claim 改为 conformal / probability calibration / uncertainty layer，另拆 Bayesian 候选。",
    ]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "allowed_next_stage": "bayesian_calibration_supplemental_evidence_queue",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "blocking_reasons": [B10_REASON],
        "required_patches": [
            "补 Bayesian calibration / Bayesian uncertainty calibration 直接来源。",
            "或移除 Bayesian 字样并把 Bayesian calibration 另拆候选。",
        ],
        "source_requirements": [
            "Bayesian calibration source",
            "Bayesian uncertainty calibration source",
        ],
        "notes": B10_REASON,
    }
    append_log(candidate, "extended_p1_supplemental_reaudit_needs_more_evidence", B10_REASON)
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": "needs_more_evidence",
        "allowed_next_stage": "bayesian_calibration_supplemental_evidence_queue",
        "notes": B10_REASON,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }


def main() -> int:
    indexed = load_candidates()
    expected = set(ACCEPTED_TASKS) | {B10_TASK}
    missing = sorted(task_id for task_id in expected if task_id not in indexed)
    if missing:
        raise SystemExit(f"Missing candidates: {missing}")

    decisions: list[dict[str, Any]] = []
    touched: list[str] = []
    for task_id, reason in ACCEPTED_TASKS.items():
        path, candidate = indexed[task_id]
        decisions.append(mark_accepted(candidate, reason))
        write_json(path, candidate)
        touched.append(rel(path))

    b10_path, b10 = indexed[B10_TASK]
    decisions.append(keep_b10_needs_more(b10))
    write_json(b10_path, b10)
    touched.append(rel(b10_path))

    audit_result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_reaudit_imported_by_codex",
        "overall_decision": "conditional_accept_for_formal_draft_queue",
        "decision_summary": {
            "accepted_for_draft": len(ACCEPTED_TASKS),
            "needs_more_evidence": 1,
            "rejected": 0,
            "direct_reviewed_allowed": 0,
            "direct_approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "global_patch": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "draft_conversion_allowed": True,
            "formal_review_status": None,
        },
        "decisions": sorted(decisions, key=lambda item: item["research_task_id"]),
    }
    write_json(AUDIT_PATH, audit_result)

    report = {
        "report_id": "phase38_extended_p1_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_path": rel(AUDIT_PATH),
        "candidate_count": len(decisions),
        "touched_file_count": len(touched),
        "touched_files": touched,
        "decision_summary": audit_result["decision_summary"],
        "b10_status": "needs_more_evidence_bayesian_calibration_source_missing",
        "formal_reviewed_created": False,
        "approved_created": False,
        "default_guidance_enabled": False,
        "hard_gate_enabled": False,
        "next_tasks": [
            "如需让 B10 进入 formal draft，补 Bayesian calibration / Bayesian uncertainty calibration 直接来源后再三审。",
            "13 条 accepted_for_draft 可在后续单独治理任务中转换 formal reviewed，但不得自动 approved。",
        ],
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
