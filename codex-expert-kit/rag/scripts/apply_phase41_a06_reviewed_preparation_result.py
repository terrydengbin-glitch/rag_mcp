"""Apply P41-A06 reviewed/caveat_only preparation audit result.

The audit result authorizes formal reviewed/caveat_only only. It must not
create approved knowledge, default guidance, hard gate authority, or trading
execution guidance.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-340"
AUDIT_RESULT_ID = "audit_result_phase41_a06_reviewed_preparation_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase41_a06_reviewed_preparation_audit_package_20260611"
CANDIDATE_ID = "cand_20260610_phase41_p41_a06_baseline_001"
RESEARCH_TASK_ID = "P41-A06"
KNOWLEDGE_ID = "kb_ai_hybrid_scoring.phase41.ensemble_after_single_model_baseline_insufficient.v1"

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_SCRIPT = SCRIPT_DIR / "apply_phase41_reviewed_preparation_result.py"
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
AUDIT_COPY_PATH = AUDIT_RESULT_PATH
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase41_a06_reviewed_preparation_import_report.json", start_file=__file__
)


def load_base_module():
    spec = importlib.util.spec_from_file_location("phase41_reviewed_preparation_base", BASE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load base script: {BASE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.TODAY = TODAY
    module.TASK_ID = TASK_ID
    module.AUDIT_RESULT_ID = AUDIT_RESULT_ID
    module.SOURCE_PACKAGE_ID = SOURCE_PACKAGE_ID
    return module


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


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dedupe_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = value.strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def validate_audit_result(audit_result: dict[str, Any]) -> dict[str, Any]:
    if audit_result.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit_result.get('audit_result_id')}")
    if audit_result.get("source_package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected source_package_id: {audit_result.get('source_package_id')}")
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != 1:
        raise ValueError("Expected exactly one P41-A06 decision")
    decision = decisions[0]
    if not isinstance(decision, dict):
        raise ValueError("Decision must be a JSON object")
    expected = {
        "candidate_id": CANDIDATE_ID,
        "research_task_id": RESEARCH_TASK_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }
    for key, value in expected.items():
        if decision.get(key) != value:
            raise ValueError(f"Decision {key} must be {value!r}, got {decision.get(key)!r}")
    return decision


def patch_candidate_before_conversion(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    limitations = as_list(deep_get(candidate, ("applicability", "limitations"), []))
    stale = "本候选三审通过也只能进入 accepted_for_draft，不能进入 approved/default guidance/hard gate。"
    replacement = "本候选可进入 formal reviewed/caveat_only 准备，但不得 approved、default guidance 或 hard gate。"
    patched_limitations = [replacement if item == stale else item for item in limitations]
    applicability = candidate.setdefault("applicability", {})
    applicability["limitations"] = dedupe_strings(patched_limitations)

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none"
    conflict["resolution_summary"] = (
        "reviewed/caveat_only preparation audit passed; formal creation must occur in a separate task. "
        "P41-A06 remains AI Engineering / numeric scoring / model family selection and does not define Trading Engineering execution rules."
    )
    conflict["approval_allowed"] = False

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "caveat_only"
    machine_gate["reason"] = (
        "Reviewed-preparation 审计允许 formal reviewed/caveat_only；仍不得 approved、default guidance 或 hard gate。"
    )
    machine_gate["requires_human_escalation"] = True

    conversion = candidate.setdefault("conversion_target", {})
    conversion["proposed_knowledge_id"] = KNOWLEDGE_ID
    conversion["target_review_status"] = "reviewed"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = True
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    review["open_questions"] = dedupe_strings(as_list(decision.get("required_followups")))

    audit_export_meta = candidate.setdefault("_audit_export_meta", {})
    audit_export_meta["formal_index_has_target"] = True
    audit_export_meta["current_reviewed_allowed"] = True
    audit_export_meta["required_next_decision"] = (
        "已允许 formal reviewed/caveat_only；如需 approved/default/hard gate，必须另起人工治理任务。"
    )


def patch_formal_item(item: dict[str, Any], decision: dict[str, Any]) -> None:
    item["knowledge_id"] = KNOWLEDGE_ID
    item["title"] = "模型集成只能在单模型 baseline 不足且可审计性不被破坏时作为增强候选"

    metadata = item.setdefault("metadata", {})
    metadata["classification_notes"] = (
        "P41-A06 formal reviewed/caveat_only；只约束 ensemble 引入条件和审计边界，"
        "不是 approved/default guidance，也不是 Trading Engineering 执行规则。"
    )
    metadata["risk_level"] = "medium"

    content = item.setdefault("content", {})
    content["statement"] = (
        "只有当单模型 baseline 不足，且 ensemble 不破坏可审计性时，ensemble 才能作为增强候选。"
    )
    content["rationale"] = (
        "P41-A06 来源覆盖 baseline-first 工程实践、ensemble 作为增强方式、stacking 增加验证复杂度、"
        "NIST 可解释/可审计治理要求，以及 CEK-TA Phase 41 scorer/calibrator/Qwen3/RAG/final gate 分责契约。"
    )
    content["procedure"] = [
        "先完成单模型 baseline comparison report，至少比较 rule baseline、Logistic Regression、LightGBM/XGBoost 等可复现单模型。",
        "确认单模型 baseline 在业务成本、延迟、校准质量、稳定性或审计需求上存在明确不足。",
        "为 ensemble 生成 auditability impact report，覆盖模型版本、base estimator、final estimator、校准器、threshold policy、trace 和 rollback target。",
        "只把 ensemble 输出作为 scorer signal 或 review-priority signal，继续交由 calibrator、threshold policy 和 deterministic final gate 消费。",
        "如果 ensemble 让解释、追踪、校准、回滚或人工复核不可接受，保持单模型方案并记录不采用原因。",
        "MCP/SearchLab/KnowledgeTree 返回本条时必须显示 reviewed/caveat_only、来源、不适用场景和禁止默认指导边界。",
    ]
    content["anti_patterns"] = dedupe_strings(
        as_list(content.get("anti_patterns"))
        + [
            "把 ensemble 写成默认优于单模型。",
            "把 ensemble 设为 Phase 41 默认依赖。",
            "让 ensemble 直接决定交易。",
            "让 ensemble 绕过 calibrator、threshold policy 或 deterministic final gate。",
            "用 ensemble 生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        ]
    )
    content["validation"] = dedupe_strings(
        as_list(content.get("validation"))
        + [
            "必须存在 single-model baseline comparison report。",
            "必须存在 auditability impact report。",
            "MCP/SearchLab 返回本条时必须显示 caveat_only、来源和不适用场景。",
        ]
    )
    content["risk_notes"] = [
        "本条为 formal reviewed/caveat_only 知识，不是 approved；不得进入默认指导或 hard gate。",
        "不得把 ensemble 描述为默认优于单模型或 Phase 41 默认依赖。",
        "不得让 ensemble 绕过 calibrator、threshold policy 或 deterministic final gate。",
        "不得用本条生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
        "不得保存或推广项目私有交易数据、账户信息、策略参数或实盘订单字段。",
        "Qwen3 和 RAG 输出只能作为审计证据，不是事实来源或最终交易授权。",
    ]

    conflict = item.setdefault("conflict_audit", {})
    conflict["conflict_status"] = "none"
    conflict["resolution_summary"] = (
        "reviewed/caveat_only preparation audit passed; formal creation is recorded by CEK-TA-340. "
        "The rule remains AI Engineering only and does not authorize trading execution."
    )
    conflict["default_recommendation"] = "caveat_only_until_human_approval"

    machine_gate = item.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "caveat_only"
    machine_gate["reason"] = (
        "P41-A06 reviewed-preparation 审计通过；允许 formal reviewed/caveat_only 检索，"
        "但 approved/default guidance/hard gate 均为 false。"
    )
    machine_gate["requires_human_escalation"] = True
    machine_gate["blocking_reasons"] = dedupe_strings(
        as_list(machine_gate.get("blocking_reasons"))
        + [
            "reviewed_not_approved",
            "default_guidance_allowed_false",
            "approved_allowed_false",
            "hard_gate_allowed_false",
        ]
    )

    review = item.setdefault("review", {})
    review["review_status"] = "reviewed"
    review["default_guidance_allowed"] = False
    review["approval_status"] = "not_requested"
    ai_audit = review.setdefault("ai_audit", {})
    ai_audit["decision"] = "accepted_for_reviewed_caveat_only"
    ai_audit["reviewed_allowed"] = True
    ai_audit["approved_allowed"] = False
    ai_audit["default_guidance_allowed"] = False
    ai_audit["hard_gate_allowed"] = False
    ai_audit["source_patch_notes"] = as_list(decision.get("source_patch_notes"))
    ai_audit["content_patch_notes"] = as_list(decision.get("content_patch_notes"))
    ai_audit["boundary_patch_notes"] = as_list(decision.get("boundary_patch_notes"))
    ai_audit["conflict_patch_notes"] = as_list(decision.get("conflict_patch_notes"))
    ai_audit["required_followups"] = as_list(decision.get("required_followups"))
    review["open_questions"] = dedupe_strings(as_list(decision.get("required_followups")))

    item["phase41_conversion"] = {
        "source_candidate_status": "accepted",
        "source_ingestion_decision": "accepted_for_draft",
        "promoted_by_task": TASK_ID,
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
    }


def patch_candidate_after_conversion(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = (
        "P41-A06 reviewed-preparation 审计通过；已创建 formal reviewed/caveat_only，"
        "approved/default guidance/hard gate 仍全部关闭。"
    )
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval_if_default_guidance_is_needed",
            "default_guidance_allowed": False,
            "knowledge_path": repo_rel(knowledge_path),
        }
    )

    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": CANDIDATE_ID,
        "research_task_id": RESEARCH_TASK_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reason": decision.get("reason", ""),
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "source_patch_notes": as_list(decision.get("source_patch_notes")),
        "content_patch_notes": as_list(decision.get("content_patch_notes")),
        "boundary_patch_notes": as_list(decision.get("boundary_patch_notes")),
        "conflict_patch_notes": as_list(decision.get("conflict_patch_notes")),
        "required_followups": as_list(decision.get("required_followups")),
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_a06_formal_reviewed_caveat_only_created",
                "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {repo_rel(knowledge_path)}.",
            }
        )


def main() -> int:
    base = load_base_module()
    audit_result = read_json(AUDIT_RESULT_PATH)
    decision = validate_audit_result(audit_result)
    candidate = read_json(CANDIDATE_PATH)

    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError("Unexpected candidate file")
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        raise ValueError("P41-A06 must be accepted_for_draft before formal reviewed conversion")

    patch_candidate_before_conversion(candidate, decision)
    base_decision = dict(decision)
    base_decision["decision"] = "accepted_for_draft"
    item = base.candidate_to_knowledge(candidate, base_decision)
    patch_formal_item(item, decision)
    knowledge_path = base.write_knowledge(item)
    patch_candidate_after_conversion(candidate, item, knowledge_path, decision)
    write_json(CANDIDATE_PATH, candidate)

    # Keep an explicit copy step for parity with other audit import tasks.
    if AUDIT_RESULT_PATH.resolve() != AUDIT_COPY_PATH.resolve():
        shutil.copyfile(AUDIT_RESULT_PATH, AUDIT_COPY_PATH)

    report = {
        "report_id": "phase41_a06_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_COPY_PATH),
        "promoted_count": 1,
        "knowledge_id": item["knowledge_id"],
        "knowledge_path": repo_rel(knowledge_path),
        "candidate_path": repo_rel(CANDIDATE_PATH),
        "review_status": deep_get(item, ("review", "review_status")),
        "machine_gate_default_guidance": deep_get(item, ("machine_gate", "default_guidance")),
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "candidate_queue_group": deep_get(candidate, ("workflow", "queue_group")),
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate/trading execution.",
        "next_action": "重建 knowledge_items 和 Vue3 fixture，并执行 Phase 41 全量运行时联动验证。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
