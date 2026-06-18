"""Apply the Phase 38 P0-Core strict audit result to candidate files.

This script records the external audit result and routes candidates into
draft-ready, needs-more-evidence, and rejected queues. It does not create
formal reviewed or approved knowledge.
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
AUDIT_RESULT_ID = "audit_result_phase38_p0_core_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase38_p0_core_candidate_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase38_p0_core_audit_import_report.json", start_file=__file__)


ACCEPTED_TASKS = {
    *(f"P38-A{i:02d}" for i in range(1, 8)),
    *(f"P38-B{i:02d}" for i in range(1, 8)),
    *(f"P38-C{i:02d}" for i in range(1, 8)),
    "P38-D01",
    "P38-D02",
    *(f"P38-E{i:02d}" for i in range(2, 7)),
    *(f"P38-F{i:02d}" for i in range(1, 7)),
    "P38-G02",
}

NEEDS_MORE_EVIDENCE = {
    "P38-D03": {
        "blocking_reasons": ["需要 CEK-TA formal index schema 和 citation resolver 契约。"],
        "required_patches": [
            "补充 knowledge_refs 到 formal knowledge index 的解析契约。",
            "补充引用失败时的 abstain/neutral 处理边界。",
        ],
        "source_requirements": ["CEK-TA formal index schema", "CEK-TA citation resolver contract"],
    },
    "P38-D04": {
        "blocking_reasons": ["no-hit / no-source abstain 当前来源不够直接。"],
        "required_patches": [
            "补充 RAG groundedness / faithfulness 来源。",
            "补充 CEK-TA no-hit policy 和默认指导阻断规则。",
        ],
        "source_requirements": ["RAG faithfulness / groundedness eval", "CEK-TA RAG retrieval policy"],
    },
    "P38-D05": {
        "blocking_reasons": ["unsupported_claims 与 final gate routing 缺少内部契约。"],
        "required_patches": [
            "定义 unsupported_claims 非空时不得默认放行。",
            "定义 unsupported_claims 到人工复核、补证或阻断的路由。",
        ],
        "source_requirements": ["CEK-TA unsupported_claim detector contract", "RAG faithfulness source"],
    },
    "P38-D06": {
        "blocking_reasons": ["reason_codes 缺少受控 taxonomy schema 和版本契约。"],
        "required_patches": [
            "定义 reason_code taxonomy v1 的枚举、版本和兼容策略。",
            "LLM 输出 reason_codes 不在 taxonomy 时必须进入 schema error 或人工复核。",
        ],
        "source_requirements": ["CEK-TA reason_code taxonomy v1", "JSON Schema enum validation"],
    },
    "P38-E01": {
        "blocking_reasons": ["offline eval 只能评估已执行交易样本的表述过于绝对。"],
        "required_patches": [
            "改为 historical offline eval 只能可靠评估已执行交易真实结果。",
            "未执行、blocked、skipped candidate 属于反事实，除非存在 shadow、paper、replay、OPE 或其他可观测/可估计机制。",
        ],
        "source_requirements": ["Open Bandit Pipeline / OPE", "shadow or paper evaluation source"],
    },
    "P38-G01": {
        "blocking_reasons": ["主动检索 CEK-TA 是内部产品协议，不能只靠通用外部来源。"],
        "required_patches": [
            "补 CEK-TA 外部项目 AI 主动检索协议。",
            "定义 gating/scoring 任务必须检索的触发条件、引用格式和 no-hit 处理。",
        ],
        "source_requirements": ["CEK-TA active retrieval protocol", "CEK-TA RAG retrieval policy"],
    },
    "P38-G03": {
        "blocking_reasons": ["machine_gate 与 review_status 的默认指导过滤缺少内部状态机契约。"],
        "required_patches": [
            "补 review_status state machine。",
            "补 machine_gate.default_guidance eligibility rules。",
        ],
        "source_requirements": ["CEK-TA machine_gate policy", "CEK-TA review_status state machine"],
    },
}

REJECTED_TASKS = {
    "P38-G04": {
        "blocking_reasons": [
            "candidate_id、normalized_claim 和 proposed_knowledge_id 含空 slug，会污染候选索引。"
        ],
        "required_patches": [
            "保留原 rejected 候选作为审计追踪。",
            "用 context_budget_field_trimming 重新生成 candidate_id、normalized_claim 和 proposed_knowledge_id。",
        ],
        "rebuilt_candidate_id": "cand_20260610_phase38_p38_g04_context_budget_field_trimming_001",
    }
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


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    review = candidate.setdefault("review", {})
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def apply_ai_audit(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": decision["decision"],
        "allowed_next_stage": decision["allowed_next_stage"],
        "blocking_reasons": decision["blocking_reasons"],
        "required_patches": decision["required_patches"],
        "source_requirements": decision["source_requirements"],
        "default_guidance_allowed": False,
        "notes": "严格审计结果只允许候选分流；不允许直接 reviewed、approved、default guidance 或 hard gate。",
    }
    review["open_questions"] = decision["required_patches"]


def mark_accepted(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "外部严格审计允许进入 formal draft 队列；不是 reviewed、approved 或 default guidance。",
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
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "strict_audit_accepted_for_draft", "可进入 formal draft 队列，但不得默认指导。")


def mark_needs_more_evidence(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "hold_for_supplemental_evidence",
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
            "hidden_from_default_queue": False,
            "next_action": "supplement_sources_and_reaudit",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "strict_audit_needs_more_evidence", "需补证后重新审计。")


def mark_rejected(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "rejected",
            "ingestion_decision": "reject",
            "decision_reason": "严格审计发现结构性 ID 缺陷，原候选保留为 rejected 审计追踪。",
            "updated_at": TODAY,
        }
    )
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False
    conflict["resolution_summary"] = "原候选含空 slug，禁止进入 formal draft；已用修复 ID 重建候选。"
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "rejected",
            "queue_group": "rejected",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "next_action": "none",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "strict_audit_rejected", "空 slug 污染风险，禁止进入 formal draft。")


def decision_for(task_id: str, candidate: dict[str, Any], decision: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    details = details or {}
    if decision == "accepted_for_draft":
        allowed_next_stage = "formal_draft_queue"
        blocking_reasons: list[str] = []
        required_patches = ["正式 draft 转换时按审计意见补 claim-specific 来源，不得直接 reviewed/approved。"]
        source_requirements = ["保留来源、边界、冲突审计和 default_guidance=false。"]
    elif decision == "needs_more_evidence":
        allowed_next_stage = "supplemental_evidence_queue"
        blocking_reasons = list(details["blocking_reasons"])
        required_patches = list(details["required_patches"])
        source_requirements = list(details["source_requirements"])
    else:
        allowed_next_stage = "rejected_archive"
        blocking_reasons = list(details["blocking_reasons"])
        required_patches = list(details["required_patches"])
        source_requirements = ["重建候选后重新审计。"]

    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": task_id,
        "decision": decision,
        "allowed_next_stage": allowed_next_stage,
        "blocking_reasons": blocking_reasons,
        "required_patches": required_patches,
        "source_requirements": source_requirements,
        "proposed_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
        "default_guidance_allowed": False,
    }


def rebuild_g04(old_candidate: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    rebuilt = copy.deepcopy(old_candidate)
    rebuilt["candidate_id"] = "cand_20260610_phase38_p38_g04_context_budget_field_trimming_001"
    rebuilt["research_task_id"] = "P38-G04-R1"
    rebuilt["claim"]["normalized_claim"] = "phase38.context_budget_field_trimming.v1"
    rebuilt["claim"]["evidence_summary"] = (
        "重建候选：知识包字段裁剪和上下文预算控制需要补充 RAG 上下文预算、字段裁剪和 no-hit 降级来源后重新审计。"
    )
    rebuilt["conversion_target"]["proposed_knowledge_id"] = (
        "kb_ai_engineering.phase38.context_budget_field_trimming.v1"
    )
    rebuilt["status"].update(
        {
            "review_status": "proposed",
            "ingestion_decision": "hold_for_reaudit",
            "decision_reason": "由 rejected G04 重建；等待补充 claim-specific 来源后二审。",
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
            "hidden_from_default_queue": False,
            "next_action": "supplement_sources_and_reaudit",
        }
    )
    rebuilt["review"]["reviewed_at"] = TODAY
    rebuilt["review"]["open_questions"] = [
        "补充字段裁剪、top-k、上下文预算、引用保留和 no-hit 降级的来源。",
        "确认该知识属于 RAG Engineering 的上下文预算治理，不沉淀交易规则本体。",
    ]
    rebuilt["review"]["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "rebuilt_from_rejected",
        "allowed_next_stage": "supplemental_evidence_queue",
        "default_guidance_allowed": False,
        "notes": "原 P38-G04 因空 slug 被拒绝，本文件是结构修复后的新候选，不是审计通过项。",
    }
    append_audit_log(rebuilt, "rebuilt_from_rejected_g04", "修复空 slug candidate/claim/knowledge id。")
    output = CANDIDATE_DIR / f"{rebuilt['candidate_id']}.json"
    return output, rebuilt


def main() -> int:
    candidates = load_candidates()
    decisions: list[dict[str, Any]] = []
    touched: list[str] = []

    expected = ACCEPTED_TASKS | set(NEEDS_MORE_EVIDENCE) | set(REJECTED_TASKS)
    missing = sorted(task_id for task_id in expected if task_id not in candidates)
    if missing:
        raise SystemExit(f"Missing Phase 38 candidates: {missing}")

    for task_id in sorted(ACCEPTED_TASKS):
        path, candidate = candidates[task_id]
        decision = decision_for(task_id, candidate, "accepted_for_draft")
        mark_accepted(candidate, decision)
        write_json(path, candidate)
        decisions.append(decision)
        touched.append(rel(path))

    for task_id in sorted(NEEDS_MORE_EVIDENCE):
        path, candidate = candidates[task_id]
        decision = decision_for(task_id, candidate, "needs_more_evidence", NEEDS_MORE_EVIDENCE[task_id])
        mark_needs_more_evidence(candidate, decision)
        write_json(path, candidate)
        decisions.append(decision)
        touched.append(rel(path))

    for task_id in sorted(REJECTED_TASKS):
        path, candidate = candidates[task_id]
        decision = decision_for(task_id, candidate, "rejected", REJECTED_TASKS[task_id])
        mark_rejected(candidate, decision)
        write_json(path, candidate)
        decisions.append(decision)
        touched.append(rel(path))
        rebuilt_path, rebuilt_candidate = rebuild_g04(candidate)
        write_json(rebuilt_path, rebuilt_candidate)
        touched.append(rel(rebuilt_path))

    audit_result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_review_imported_by_codex",
        "overall_decision": "conditional_accept_for_formal_draft_queue",
        "decision_summary": {
            "accepted_for_draft": len(ACCEPTED_TASKS),
            "needs_more_evidence": len(NEEDS_MORE_EVIDENCE),
            "rejected": len(REJECTED_TASKS),
            "rebuilt": 1,
            "misrouted_to_trading": 0,
            "direct_reviewed_allowed": 0,
            "direct_approved_allowed": 0,
            "default_guidance_allowed": 0,
        },
        "boundary": {
            "candidate_is_formal_knowledge": False,
            "accepted_for_draft_is_reviewed": False,
            "accepted_for_draft_is_approved": False,
            "llm_audit_assistant_can_final_gate": False,
            "numeric_scorer_can_trade": False,
        },
        "decisions": sorted(decisions, key=lambda item: item["research_task_id"]),
        "global_required_patches": [
            "把通用来源替换或补强为 claim-specific 来源。",
            "为 D/G 组补 CEK-TA formal index、citation resolver、reason taxonomy、machine_gate 和 review_status 契约。",
            "修正 E01 的反事实评估表述。",
            "G04 保留 rejected 原件并重建修复 ID 后重新审计。",
        ],
    }
    write_json(AUDIT_PATH, audit_result)

    report = {
        "report_id": "phase38_p0_core_audit_import_report",
        "generated_at": TODAY,
        "audit_result_path": rel(AUDIT_PATH),
        "candidate_count": len(decisions),
        "touched_file_count": len(touched),
        "touched_files": touched,
        "decision_summary": audit_result["decision_summary"],
        "next_tasks": ["CEK-TA-277", "CEK-TA-278"],
        "dod": {
            "audit_result_recorded": AUDIT_PATH.exists(),
            "candidate_status_backwritten": True,
            "g04_rebuilt": (CANDIDATE_DIR / "cand_20260610_phase38_p38_g04_context_budget_field_trimming_001.json").exists(),
            "formal_reviewed_created": False,
            "approved_created": False,
        },
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
