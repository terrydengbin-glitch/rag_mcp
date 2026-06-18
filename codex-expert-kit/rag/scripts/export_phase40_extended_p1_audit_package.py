"""Export Phase 40 Batch D/E candidate AI audit package.

The package is for external AI/human audit only. It does not promote candidates
to formal reviewed knowledge and never marks anything as approved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-10"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase40_extended_p1_candidate_audit_package_20260610.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase40_extended_p1_candidate_quality_gate.json", start_file=__file__)

EXPECTED_BATCH_DE = {f"P40-E{i:02d}" for i in range(1, 13)} | {f"P40-P{i:02d}" for i in range(1, 7)}


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase40_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if raw.get("research_task_id") in EXPECTED_BATCH_DE:
            candidates.append(raw)
    return candidates


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    seen = set()
    for item in candidates:
        candidate_id = str(item.get("candidate_id", ""))
        research_task_id = str(item.get("research_task_id", ""))
        seen.add(research_task_id)
        source_refs = item.get("source_refs") or []
        conflict_status = item.get("conflict_audit", {}).get("conflict_status")
        review_status = item.get("status", {}).get("review_status")
        default_guidance = item.get("machine_gate", {}).get("default_guidance")
        workflow_default = item.get("workflow", {}).get("default_guidance_allowed")
        canonical_node_id = item.get("classification", {}).get("canonical_node_id")
        if research_task_id not in EXPECTED_BATCH_DE:
            failures.append({"candidate_id": candidate_id, "failure": "unexpected_research_task_id"})
        if not str(canonical_node_id).startswith("kt.ai_feedback_governance."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if len(source_refs) < 2:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_2"})
        if conflict_status not in {"none", "resolved"}:
            failures.append({"candidate_id": candidate_id, "failure": "unsafe_conflict_status"})
        if review_status != "proposed":
            failures.append({"candidate_id": candidate_id, "failure": "not_candidate_proposed"})
        if default_guidance != "deny":
            failures.append({"candidate_id": candidate_id, "failure": "machine_gate_not_deny"})
        if workflow_default is not False:
            failures.append({"candidate_id": candidate_id, "failure": "workflow_default_guidance_not_false"})
        if item.get("status", {}).get("review_status") == "approved":
            failures.append({"candidate_id": candidate_id, "failure": "status_review_status_is_approved"})
        if item.get("status", {}).get("ingestion_decision") == "approved":
            failures.append({"candidate_id": candidate_id, "failure": "status_ingestion_decision_is_approved"})
    for missing in sorted(EXPECTED_BATCH_DE - seen):
        failures.append({"research_task_id": missing, "failure": "missing_candidate"})
    return {
        "report_id": "phase40_extended_p1_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 40 Batch D/E candidate audit package",
        "candidate_count": len(candidates),
        "planned_total": len(EXPECTED_BATCH_DE),
        "checks": {
            "source_refs_min_2": "pass" if all(len(item.get("source_refs") or []) >= 2 for item in candidates) else "fail",
            "conflict_status_safe": "pass" if all(item.get("conflict_audit", {}).get("conflict_status") in {"none", "resolved"} for item in candidates) else "fail",
            "review_status_candidate_only": "pass" if all(item.get("status", {}).get("review_status") == "proposed" for item in candidates) else "fail",
            "machine_gate_denies_default_guidance": "pass" if all(item.get("machine_gate", {}).get("default_guidance") == "deny" for item in candidates) else "fail",
            "canonical_nodes_under_feedback_governance": "pass" if all(str(item.get("classification", {}).get("canonical_node_id")).startswith("kt.ai_feedback_governance.") for item in candidates) else "fail",
        },
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }


def main() -> int:
    candidates = load_candidates()
    quality = quality_gate(candidates)
    package = {
        "package_id": "phase40_extended_p1_candidate_audit_package_20260610",
        "package_type": "candidate_ai_audit_package",
        "generated_at": TODAY,
        "phase": "40",
        "task_id": "CEK-TA-311",
        "title": "Phase 40 Batch D/E 持续学习候选知识审计包",
        "purpose": "审计 Phase 40 尚未采集的 P0-Extended 与 P1 持续学习候选知识，确认来源充分性、适用边界、冲突风险、AI 使用安全和跨分支路由。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 approved。",
            "reviewed 不等于 approved。",
            "持续学习不等于线上自动学习。",
            "再训练只能生成 candidate model，不得自动替换 champion model。",
            "LLM audit assistant 不能做最终交易 gate。",
            "shadow/paper/canary 只是发布证据，不是自动上线许可。",
            "hard gate 启用必须有人工审批、release manifest、rollback target 和 kill switch。",
            "交易规则本体必须路由到 Phase 37 / Trading Engineering。",
            "不得把项目私有事实、账号数据、密钥或具体策略规则写入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "逐条判断候选是否可转为 accepted_for_draft，或需要补来源、改边界、拆分、拒绝。",
            "focus_checks": [
                "是否有足够权威来源支持。",
                "是否错误收录了 Trading Engineering 规则本体。",
                "是否把持续学习误写成线上自动学习。",
                "是否把再训练结果误设为自动上线或替换 champion。",
                "是否把 LLM audit assistant 误设为最终交易裁决者。",
                "是否存在无来源默认指导、冲突未处理或过期依赖。",
                "是否需要补充论文、官方文档或工程实例。",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": "phase40_extended_p1_candidate_audit_package_20260610",
                "decisions": [
                    {
                        "candidate_id": "string",
                        "research_task_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reviewed_allowed": False,
                        "approved_allowed": False,
                        "default_guidance_allowed": False,
                        "hard_gate_allowed": False,
                        "reason": "string",
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                        "required_followups": ["string"],
                    }
                ],
                "batch_summary": {
                    "accepted_count": 0,
                    "needs_more_evidence_count": 0,
                    "rejected_count": 0,
                    "misrouted_to_trading_count": 0,
                },
            },
        },
        "quality_gate": quality,
        "candidate_count": len(candidates),
        "planned_total": len(EXPECTED_BATCH_DE),
        "candidates": candidates,
    }
    AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_package": str(AUDIT), "quality_gate": str(QUALITY), **quality}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
