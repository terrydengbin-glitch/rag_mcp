"""Import Phase 38 G04-R1 third audit result.

The third audit upgrades G04-R1 from needs_more_evidence to accepted_for_draft
only. It must not create reviewed, approved, default guidance, or hard-gate
permissions.
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
AUDIT_RESULT_ID = "audit_result_phase38_g04_context_budget_third_reaudit_20260610_strict_v3"
SOURCE_PACKAGE_ID = "phase38_g04_context_budget_third_audit_package_20260610"
CANDIDATE_ID = "cand_20260610_phase38_p38_g04_context_budget_field_trimming_001"

CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    f"{CANDIDATE_ID}.json",
    start_file=__file__,
)
AUDIT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_g04_context_budget_third_reaudit_import_report.json", start_file=__file__
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


def append_unique(items: list[Any], value: Any) -> None:
    if value not in items:
        items.append(value)


def append_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    review = candidate.setdefault("review", {})
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def enforce_no_default_guidance(candidate: dict[str, Any]) -> None:
    candidate["default_guidance_allowed"] = False
    candidate["visible_in_default_guidance_queue"] = False
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    audit = review.setdefault("ai_audit", {})
    if isinstance(audit, dict):
        audit["default_guidance_allowed"] = False
        audit["reviewed_allowed"] = False
        audit["approved_allowed"] = False
        audit["hard_gate_allowed"] = False


def patch_g04(candidate: dict[str, Any]) -> None:
    if candidate.get("candidate_id") != CANDIDATE_ID:
        raise ValueError(f"Unexpected candidate_id: {candidate.get('candidate_id')}")
    if candidate.get("research_task_id") != "P38-G04-R1":
        raise ValueError(f"Unexpected research_task_id: {candidate.get('research_task_id')}")

    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": (
                "三审通过：G04-R1 允许进入 formal draft queue；不得 reviewed、approved、"
                "default guidance 或 hard gate。"
            ),
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
            "visible_in_default_guidance_queue": False,
            "default_guidance_allowed": False,
        }
    )

    conflict = candidate.setdefault("conflict_audit", {})
    conflict.update(
        {
            "conflict_status": "none",
            "approval_allowed": False,
            "draft_conversion_allowed": True,
            "resolution_summary": (
                "G04-R1 三审通过，可进入 formal draft queue；approval/default guidance/hard gate 仍被阻断。"
            ),
        }
    )

    review = candidate.setdefault("review", {})
    review["confidence"] = "medium"
    review["freshness"] = "time_sensitive"
    review["reviewer"] = "external_ai_third_reaudit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["open_questions"] = [
        "formal draft 转换时必须声明 top_k=5 和 token_budget=4000 只是 P0 policy default，不是全局最优。",
        "formal draft 必须保留 detail_expansion_policy=explicit_request_required 的机器校验要求。",
        "formal draft 不得沉淀交易规则本体；交易规则必须路由到 Trading Engineering。",
    ]
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_draft",
        "allowed_next_stage": "formal_draft_queue",
        "default_guidance_allowed": False,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "hard_gate_allowed": False,
        "notes": (
            "三审确认空 slug 已修复，draft_conversion_allowed=true 与 approval_allowed=false 语义一致，"
            "hidden_from_default_queue=true、visible_in_default_guidance_queue=false、"
            "default_guidance_allowed=false 已消除默认指导歧义。"
        ),
    }

    limitations = candidate.setdefault("applicability", {}).setdefault("limitations", [])
    if isinstance(limitations, list):
        append_unique(limitations, "top_k=5 只是 P0 默认值，不是全局最优。")
        append_unique(limitations, "token_budget=4000 只是 phase38_context_budget_policy_v1 默认预算，不是全局最优。")
        append_unique(limitations, "field_whitelist 必须版本化维护，不能硬编码后无人治理。")
        append_unique(limitations, "详细审计内容必须显式请求，默认不得返回完整审计日志、长来源摘要、候选审计历史或历史版本。")

    candidate["draft_conversion_allowed"] = True
    candidate["default_guidance_allowed"] = False
    candidate["context_budget_policy_version"] = "phase38_context_budget_policy_v1"
    candidate["field_whitelist_version"] = "phase38_default_knowledge_pack_fields_v1"
    candidate["top_k"] = 5
    candidate["token_budget"] = 4000
    candidate["top_k_scope"] = "P0 policy default, not a global optimum"
    candidate["token_budget_scope"] = "P0 policy default, not a global optimum"
    candidate["detail_expansion_policy"] = "explicit_request_required"
    candidate["must_not_return_by_default"] = [
        "private_strategy_body",
        "account_data",
        "secrets",
        "raw_trading_rule_text",
        "execution_parameters",
        "fill_model_details",
        "full_audit_log",
        "long_source_summaries",
        "candidate_review_history",
        "historical_versions",
    ]
    candidate["required_formal_draft_tests"] = [
        "empty_slug_rejection_test",
        "default_queue_guard_test",
        "detail_expansion_guard_test",
        "token_budget_guard_test",
        "trading_rule_boundary_test",
    ]
    enforce_no_default_guidance(candidate)
    append_log(candidate, "third_reaudit_accepted_for_draft", "G04-R1 三审通过，仅进入 formal draft queue。")


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    patch_g04(candidate)
    write_json(CANDIDATE_PATH, candidate)

    audit_result = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audited_at": TODAY,
        "auditor": "external_ai_strict_third_reaudit_imported_by_codex",
        "overall_decision": "accepted_for_draft",
        "decision_summary": {
            "accepted_for_draft": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "direct_reviewed_allowed": 0,
            "direct_approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "decisions": [
            {
                "candidate_id": CANDIDATE_ID,
                "research_task_id": "P38-G04-R1",
                "decision": "accepted_for_draft",
                "allowed_next_stage": "formal_draft_queue",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_formal_draft_patches": [
                    "写明 top_k=5 和 token_budget=4000 是 P0 默认值，不是全局最优。",
                    "保留 field_whitelist_version 和 context_budget_policy_version。",
                    "默认不得返回 full_audit_log、long_source_summaries、candidate_review_history、historical_versions。",
                    "交易规则本体必须路由到 Trading Engineering。",
                ],
            }
        ],
        "timestamp_note": (
            "本项目当前运行日期为 2026-06-10；三审文本中提到 2026-06-09 与文件系统时间差异，"
            "本次按 CEK-TA 当前本地日期归档为 2026-06-10。"
        ),
    }
    write_json(AUDIT_PATH, audit_result)

    report = {
        "report_id": "phase38_g04_context_budget_third_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-282",
        "candidate_path": rel(CANDIDATE_PATH),
        "audit_result_path": rel(AUDIT_PATH),
        "candidate_id": CANDIDATE_ID,
        "before": "needs_more_evidence / ready_for_reaudit",
        "after": "accepted / accepted_for_draft",
        "formal_review_status": "draft",
        "reviewed_created": False,
        "approved_created": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "boundary": "accepted_for_draft only; no reviewed, approved, default guidance, or hard gate.",
        "next_step": "CEK-TA-273 can convert accepted Phase 38 candidates to formal reviewed knowledge in a separate governed task.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
