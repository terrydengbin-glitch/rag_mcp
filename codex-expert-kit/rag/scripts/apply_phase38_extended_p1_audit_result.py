"""Import Phase 38 P0-Extended / P1 strict audit result.

The audit routes 23 candidates into formal-draft, needs-more-evidence, and
rejected queues. It does not create reviewed or approved knowledge, and it
blocks default guidance and hard-gate use for every item in this batch.
"""

from __future__ import annotations

import copy
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
AUDIT_RESULT_ID = "audit_result_phase38_extended_p1_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase38_extended_p1_candidate_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_extended_p1_audit_import_report.json", start_file=__file__
)


ACCEPTED_FOR_DRAFT: dict[str, str] = {
    "P38-A08": "CatBoost 只能作为类别特征占比较高场景的 conditional challenger，不是默认主模型。",
    "P38-B08": "可进入校准切片 draft，但必须声明最小样本量和稀疏切片回退。",
    "P38-B09": "可进入 calibration drift shadow 监控 draft，但必须区分 feature/score/label/calibration drift。",
    "P38-C08": "TFDV 与 DVC 可支撑 feature schema registry 和版本治理。",
    "P38-C09": "Great Expectations 与 TFDV 可支撑 data quality expectation suite。",
    "P38-D09": "DPO 只能优化审计偏好和格式偏好，不承诺交易收益。",
    "P38-F07": "incident freeze 可用于冻结 model、prompt、RAG index 和 threshold 复盘。",
    "P38-F08": "Model card / dataset card 可支撑 intended use 与 out-of-scope use 披露。",
    "P38-F09": "latency budget 与 fallback 可以纳入发布验收，但不能绕过 deterministic final gate。",
}

NEEDS_MORE_EVIDENCE: dict[str, dict[str, list[str]]] = {
    "P38-A09": {
        "blocking_reasons": ["SHAP 来源只能支撑模型输出解释，不能直接证明 feature attribution 不是因果解释。"],
        "required_patches": ["补 causality / XAI 边界来源，把 attribution 与 causal explanation 严格分离。"],
        "source_requirements": ["causal inference source", "XAI limitation source", "SHAP limitation source"],
    },
    "P38-A10": {
        "blocking_reasons": ["MLflow Registry 与 NIST 不支撑 ranking model 作为 review priority 增强的方法本体。"],
        "required_patches": ["补 learning-to-rank 或 ranking metric 来源，并说明只用于人工复核优先级。"],
        "source_requirements": ["learning-to-rank source", "ranking evaluation source"],
    },
    "P38-B10": {
        "blocking_reasons": ["当前候选没有 conformal prediction 或 Bayesian calibration 的直接来源。"],
        "required_patches": ["补 conformal / Bayesian calibration 来源，改成增强层而非 P0 默认层。"],
        "source_requirements": ["conformal prediction source", "Bayesian calibration source"],
    },
    "P38-D07": {
        "blocking_reasons": ["TRL 只能支撑 SFT 方法，不支撑先 RAG/prompt 再 SFT 的决策流程。"],
        "required_patches": ["补 RAG/prompt baseline、ablation 和 SFT 触发条件的内部契约或来源。"],
        "source_requirements": ["RAG baseline source", "prompt baseline source", "CEK-TA SFT decision contract"],
    },
    "P38-D08": {
        "blocking_reasons": ["缺少 PEFT/LoRA、JSON Schema 和 Structured Outputs 的直接来源。"],
        "required_patches": ["补 LoRA/PEFT 与结构化输出来源，限制 SFT 只服务 schema/reason code。"],
        "source_requirements": ["PEFT/LoRA source", "JSON Schema source", "structured output source"],
    },
    "P38-D10": {
        "blocking_reasons": ["缺少 RAG faithfulness、citation resolver 和 teacher-as-judge limitation 来源。"],
        "required_patches": ["明确 teacher model 只能作为审计 baseline，不得作为事实来源。"],
        "source_requirements": ["RAG faithfulness source", "citation resolver contract", "LLM-as-judge limitation source"],
    },
    "P38-E07": {
        "blocking_reasons": ["MLflow Registry 与 DVC 只支撑版本化，不足以支撑 ablation 方法。"],
        "required_patches": ["补 ablation study 或 experiment design 来源，并定义 RAG/prompt/model/threshold 的隔离实验。"],
        "source_requirements": ["ablation study source", "experiment design source"],
    },
    "P38-E08": {
        "blocking_reasons": ["Evidently/NIST 不直接支撑 RAG 引用完整性和 no-hit/conflict shadow 指标。"],
        "required_patches": ["补 CEK-TA citation completeness 与 no-hit/conflict 记录契约。"],
        "source_requirements": ["CEK-TA citation completeness contract", "RAG evaluation source"],
    },
    "P38-E09": {
        "blocking_reasons": ["当前 OPE 来源偏弱，且 fill/cost 假设必须由 Trading Engineering 提供引用。"],
        "required_patches": ["补 OPE/paper/replay/人工复核估计来源，并引用 Trading Engineering 的 fill/cost 边界。"],
        "source_requirements": ["OPE source", "paper trading evaluation source", "Trading Engineering fill/cost reference"],
    },
    "P38-E10": {
        "blocking_reasons": ["当前来源是 OPE/contextual bandit，不是 active learning。"],
        "required_patches": ["补 active learning review sampling 来源，并声明只作增强，不作自动收益承诺。"],
        "source_requirements": ["active learning source", "human review sampling source"],
    },
    "P38-F10": {
        "blocking_reasons": ["当前无 model compression、quantization 或 distillation 的直接来源。"],
        "required_patches": ["补压缩/量化/蒸馏来源，并声明压缩不能破坏审计、校准和引用链。"],
        "source_requirements": ["model compression source", "quantization source", "distillation source"],
    },
    "P38-G05": {
        "blocking_reasons": ["需要 RAG citation、faithfulness 和 resolver 证据。"],
        "required_patches": ["补 citation completeness 指标定义和 shadow 记录契约。"],
        "source_requirements": ["RAG citation source", "RAG faithfulness source", "CEK-TA citation resolver contract"],
    },
    "P38-G06": {
        "blocking_reasons": ["Great Expectations/NIST 不支撑 RAG no-hit workflow。"],
        "required_patches": ["补 no-hit query 到知识缺口队列的 CEK-TA 工作流契约。"],
        "source_requirements": ["CEK-TA no-hit workflow contract", "RAG retrieval failure handling source"],
    },
}

REJECTED: dict[str, dict[str, Any]] = {
    "P38-C10": {
        "blocking_reasons": [
            "candidate_id、normalized_claim 和 proposed_knowledge_id 存在空 slug，会污染候选和 formal index。"
        ],
        "required_patches": [
            "保留原候选为 rejected 审计追踪。",
            "用 cross_market_feature_availability_recheck 重建候选。",
            "重建后补 point-in-time feature availability、training-serving skew、market/domain transfer validation、feature store AS-OF join 来源。",
        ],
        "rebuilt_candidate_id": "cand_20260610_phase38_p38_c10_cross_market_feature_availability_recheck_001",
    }
}

GLOBAL_METADATA_PATCH = {
    "target_review_status": "draft",
    "reviewed_allowed": False,
    "approved_allowed": False,
    "default_guidance_allowed": False,
    "hard_gate_allowed": False,
    "hidden_from_default_queue": True,
    "visible_in_default_guidance_queue": False,
}


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
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        candidate = read_json(path)
        task_id = candidate.get("research_task_id")
        if isinstance(task_id, str):
            candidates[task_id] = (path, candidate)
    return candidates


def append_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def block_default_and_hard_gate(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False

    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    ai_audit = review.setdefault("ai_audit", {})
    if isinstance(ai_audit, dict):
        ai_audit["default_guidance_allowed"] = False
        ai_audit["reviewed_allowed"] = False
        ai_audit["approved_allowed"] = False
        ai_audit["hard_gate_allowed"] = False

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False


def ai_audit_payload(decision: str, allowed_next_stage: str, notes: str, details: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": decision,
        "allowed_next_stage": allowed_next_stage,
        "blocking_reasons": details.get("blocking_reasons", []),
        "required_patches": details.get("required_patches", []),
        "source_requirements": details.get("source_requirements", []),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "notes": notes,
    }


def mark_accepted(candidate: dict[str, Any], reason: str) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": f"严格审计允许进入 formal draft 队列：{reason} 不是 reviewed、approved、default guidance 或 hard gate。",
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
            "next_action": "convert_to_formal_draft_then_separate_review",
        }
    )
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_strict_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = ["正式 draft 转换时必须保留审计补丁点，且继续 default_guidance=false。"]
    review["ai_audit"] = ai_audit_payload(
        "accepted_for_draft",
        "formal_draft_queue",
        reason,
        {
            "required_patches": [
                "转换 formal draft 时写清楚本条的适用边界、非适用边界和本轮审计限制。",
                "不得直接 reviewed、approved 或进入默认指导队列。",
            ],
            "source_requirements": ["保留现有来源并在 draft 中补足 claim-specific 说明。"],
        },
    )
    block_default_and_hard_gate(candidate)
    append_log(candidate, "extended_p1_audit_accepted_for_draft", reason)
    return decision_record(candidate, "accepted_for_draft", "formal_draft_queue", reason)


def mark_needs_more(candidate: dict[str, Any], details: dict[str, list[str]]) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "严格审计要求补充 claim-specific 来源或 CEK-TA 内部契约后再二审。",
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
            "next_action": "supplement_sources_and_reaudit",
        }
    )
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_strict_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = details["required_patches"]
    review["ai_audit"] = ai_audit_payload(
        "needs_more_evidence",
        "supplemental_evidence_queue",
        "需要补证后再二审；不得进入 formal draft 或默认指导。",
        details,
    )
    block_default_and_hard_gate(candidate)
    append_log(candidate, "extended_p1_audit_needs_more_evidence", "需补证后重新审计。")
    return decision_record(
        candidate,
        "needs_more_evidence",
        "supplemental_evidence_queue",
        "；".join(details["blocking_reasons"]),
        details,
    )


def mark_rejected(candidate: dict[str, Any], details: dict[str, Any]) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "rejected",
            "ingestion_decision": "reject",
            "decision_reason": "严格审计发现结构性 ID 缺陷，原候选保留为 rejected 审计追踪。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "rejected",
            "queue_group": "rejected",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "rebuilt_candidate_created",
        }
    )
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["resolution_summary"] = "原候选含空 slug，禁止进入 formal draft；已创建修复 ID 的替代候选。"
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_strict_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = details["required_patches"]
    review["ai_audit"] = ai_audit_payload(
        "rejected",
        "rejected_archive",
        "原候选结构性 ID 缺陷，禁止进入 formal draft。",
        details,
    )
    block_default_and_hard_gate(candidate)
    append_log(candidate, "extended_p1_audit_rejected", "空 slug 污染风险，禁止入库。")
    return decision_record(
        candidate,
        "rejected",
        "rejected_archive",
        "；".join(details["blocking_reasons"]),
        details,
    )


def rebuild_c10(old_candidate: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    rebuilt = copy.deepcopy(old_candidate)
    rebuilt["candidate_id"] = "cand_20260610_phase38_p38_c10_cross_market_feature_availability_recheck_001"
    rebuilt["research_task_id"] = "P38-C10-R1"
    rebuilt["parent_rejected_candidate_id"] = old_candidate.get("candidate_id")
    rebuilt["replacement_reason"] = "fix_empty_slug"
    rebuilt["claim"]["normalized_claim"] = "phase38.cross_market_feature_availability_recheck.v1"
    rebuilt["claim"]["evidence_summary"] = (
        "重建候选：多市场迁移前必须重新检查决策时特征可用性；仍需补 point-in-time feature availability、"
        "training-serving skew、domain transfer validation 和 feature store AS-OF join 来源后再二审。"
    )
    rebuilt["conversion_target"]["proposed_knowledge_id"] = (
        "kb_ai_engineering.phase38.cross_market_feature_availability_recheck.v1"
    )
    rebuilt["status"].update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "由 rejected C10 重建；空 slug 已修复，但仍需补充 claim-specific 来源后二审。",
            "created_at": TODAY,
            "updated_at": TODAY,
        }
    )
    rebuilt["workflow"].update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "supplement_sources_and_reaudit",
        }
    )
    details = {
        "blocking_reasons": ["重建候选仍需补充跨市场迁移与决策时特征可用性的直接证据。"],
        "required_patches": [
            "补 point-in-time feature availability 来源。",
            "补 training-serving skew 来源。",
            "补 market/domain transfer validation 来源。",
            "补 feature store AS-OF join 或 timestamp correctness 来源。",
        ],
        "source_requirements": [
            "point-in-time feature availability",
            "training-serving skew",
            "market/domain transfer validation",
            "feature store AS-OF join / timestamp correctness",
        ],
    }
    review = rebuilt.setdefault("review", {})
    review["reviewer"] = "codex_rebuild_after_external_ai_audit"
    review["reviewed_at"] = TODAY
    review["open_questions"] = details["required_patches"]
    review["ai_audit"] = ai_audit_payload(
        "rebuilt_needs_more_evidence",
        "supplemental_evidence_queue",
        "空 slug 已修复；仍需补证后二审。",
        details,
    )
    block_default_and_hard_gate(rebuilt)
    append_log(rebuilt, "rebuilt_from_rejected_c10", "修复 C10 空 slug candidate/claim/knowledge id。")
    output = CANDIDATE_DIR / f"{rebuilt['candidate_id']}.json"
    return output, rebuilt


def decision_record(
    candidate: dict[str, Any],
    decision: str,
    allowed_next_stage: str,
    notes: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    details = details or {}
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": candidate["research_task_id"],
        "decision": decision,
        "allowed_next_stage": allowed_next_stage,
        "notes": notes,
        "blocking_reasons": details.get("blocking_reasons", []),
        "required_patches": details.get("required_patches", []),
        "source_requirements": details.get("source_requirements", []),
        "proposed_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
        **GLOBAL_METADATA_PATCH,
    }


def main() -> int:
    candidates = load_candidates()
    expected = set(ACCEPTED_FOR_DRAFT) | set(NEEDS_MORE_EVIDENCE) | set(REJECTED)
    missing = sorted(task_id for task_id in expected if task_id not in candidates)
    if missing:
        raise SystemExit(f"Missing Phase 38 P0-Extended/P1 candidates: {missing}")

    decisions: list[dict[str, Any]] = []
    touched: list[str] = []

    for task_id in sorted(ACCEPTED_FOR_DRAFT):
        path, candidate = candidates[task_id]
        decisions.append(mark_accepted(candidate, ACCEPTED_FOR_DRAFT[task_id]))
        write_json(path, candidate)
        touched.append(rel(path))

    for task_id in sorted(NEEDS_MORE_EVIDENCE):
        path, candidate = candidates[task_id]
        decisions.append(mark_needs_more(candidate, NEEDS_MORE_EVIDENCE[task_id]))
        write_json(path, candidate)
        touched.append(rel(path))

    for task_id in sorted(REJECTED):
        path, candidate = candidates[task_id]
        decisions.append(mark_rejected(candidate, REJECTED[task_id]))
        write_json(path, candidate)
        touched.append(rel(path))
        rebuilt_path, rebuilt = rebuild_c10(candidate)
        write_json(rebuilt_path, rebuilt)
        touched.append(rel(rebuilt_path))

    audit_result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_review_imported_by_codex",
        "overall_decision": "conditional_accept_for_formal_draft_queue",
        "decision_summary": {
            "accepted_for_draft": len(ACCEPTED_FOR_DRAFT),
            "needs_more_evidence": len(NEEDS_MORE_EVIDENCE),
            "rejected": len(REJECTED),
            "rebuilt": 1,
            "direct_reviewed_allowed": 0,
            "direct_approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
            "misrouted_to_trading": 0,
        },
        "global_metadata_patch": GLOBAL_METADATA_PATCH,
        "boundary": {
            "candidate_is_formal_knowledge": False,
            "accepted_for_draft_is_reviewed": False,
            "accepted_for_draft_is_approved": False,
            "llm_audit_assistant_can_final_gate": False,
            "numeric_scorer_can_trade": False,
        },
        "decisions": sorted(decisions, key=lambda item: item["research_task_id"]),
    }
    write_json(AUDIT_PATH, audit_result)

    report = {
        "report_id": "phase38_extended_p1_audit_import_report",
        "generated_at": TODAY,
        "audit_result_path": rel(AUDIT_PATH),
        "candidate_count": len(decisions),
        "touched_file_count": len(touched),
        "touched_files": touched,
        "decision_summary": audit_result["decision_summary"],
        "next_tasks": [
            "为 13 条 needs_more_evidence 和 C10-R1 执行补证采集。",
            "补证后二审通过后再进入 formal draft 或 reviewed 治理任务。",
        ],
        "dod": {
            "audit_result_recorded": AUDIT_PATH.exists(),
            "candidate_status_backwritten": True,
            "c10_rebuilt": (
                CANDIDATE_DIR
                / "cand_20260610_phase38_p38_c10_cross_market_feature_availability_recheck_001.json"
            ).exists(),
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
