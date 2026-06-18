"""Export Phase 41 P0-Extended/P1 joint candidate audit package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-10"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
MATRIX = resolve_repo_path("docs", "research", "phase41_hybrid_scoring_collection_matrix.md", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase41_extended_p1_candidate_audit_package_20260610.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase41_extended_p1_candidate_quality_gate.json", start_file=__file__)

PRIMARY_SOURCE_TYPES = {
    "official_doc",
    "research_paper",
    "standard_doc",
    "governance_framework",
    "security_standard",
    "internal_contract",
}


def expected_topics() -> dict[str, str]:
    expected: dict[str, str] = {}
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P41-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] in {"P0-Extended", "P1"}:
            expected[cells[0]] = cells[1]
    return expected


def load_candidates() -> list[dict[str, Any]]:
    expected = expected_topics()
    candidates: list[dict[str, Any]] = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase41_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(raw.get("research_task_id", "")) in expected:
            candidates.append(raw)
    return candidates


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    expected = expected_topics()
    failures: list[dict[str, str]] = []
    seen = set()
    for item in candidates:
        candidate_id = str(item.get("candidate_id", ""))
        research_task_id = str(item.get("research_task_id", ""))
        seen.add(research_task_id)
        source_refs = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in source_refs if isinstance(src, dict)}
        conflict_status = item.get("conflict_audit", {}).get("conflict_status")
        review_status = item.get("status", {}).get("review_status")
        default_guidance = item.get("machine_gate", {}).get("default_guidance")
        workflow_default = item.get("workflow", {}).get("default_guidance_allowed")
        canonical_node_id = str(item.get("classification", {}).get("canonical_node_id"))
        priority = item.get("phase41_trace", {}).get("priority")
        if research_task_id not in expected:
            failures.append({"candidate_id": candidate_id, "failure": "unexpected_research_task_id"})
        if priority != expected.get(research_task_id):
            failures.append({"candidate_id": candidate_id, "failure": "priority_mismatch"})
        if not canonical_node_id.startswith("kt.ai_engineering."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if len(source_refs) < 3:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_3"})
        if not (source_types & PRIMARY_SOURCE_TYPES):
            failures.append({"candidate_id": candidate_id, "failure": "missing_primary_source_type"})
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
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
    for missing in sorted(set(expected) - seen):
        failures.append({"research_task_id": missing, "failure": "missing_candidate"})
    return {
        "report_id": "phase41_extended_p1_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 41 P0-Extended/P1 joint candidate audit package",
        "candidate_count": len(candidates),
        "planned_total": len(expected),
        "p0_extended_total": sum(1 for value in expected.values() if value == "P0-Extended"),
        "p1_total": sum(1 for value in expected.values() if value == "P1"),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; P0-Extended and P1 are audited together before formal conversion.",
    }


def main() -> int:
    candidates = load_candidates()
    quality = quality_gate(candidates)
    package = {
        "package_id": "phase41_extended_p1_candidate_audit_package_20260610",
        "package_type": "candidate_ai_audit_package",
        "generated_at": TODAY,
        "phase": "41",
        "title": "Phase 41 P0-Extended/P1 Hybrid Scoring 与 Qwen3 审计助手候选知识联合审计包",
        "purpose": "统一审计 Phase 41 剩余 P0-Extended 12 条和 P1 7 条候选知识，确认这些增强能力是否可进入 formal draft/reviewed，或需要补证、降级、拆分、拒绝。",
        "hard_boundaries": [
            "P0-Extended 和 P1 放在同一批审计，但必须保留优先级标签。",
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 approved。",
            "reviewed 不等于 approved。",
            "P0-Extended/P1 是增强能力，不得变成外接项目默认依赖。",
            "Qwen3 只能做 audit assistant，不做 numeric scorer、final gate 或事实来源。",
            "表格/统计模型只做 scorer、risk ranking 或 review priority，不直接执行交易。",
            "deterministic final gate 是最终 allow/block/reduce_size 权限来源。",
            "交易规则本体必须路由到 Phase 37 / Trading Engineering。",
            "不得把项目私有事实、账号数据、密钥或具体策略规则写入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "逐条判断候选是否可转为 formal draft/reviewed，或需要补来源、改边界、拆分、拒绝。",
            "focus_checks": [
                "来源是否足够权威，是否包含官方文档、论文、治理框架或 CEK-TA 内部契约。",
                "候选是否仍然只是增强项，没有被描述为 POC 必需默认依赖。",
                "是否错误收录 Trading Engineering 规则本体。",
                "是否清楚区分 scorer、calibrator、Qwen3 audit assistant、RAG、platform 和 deterministic final gate 的责任。",
                "是否存在无来源默认指导、冲突未处理、过期依赖或中文乱码。",
                "是否需要补充更贴近交易 AI 的工程实例、反例、延迟/SLO、回滚或人工审批边界。",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": "phase41_extended_p1_candidate_audit_package_20260610",
                "decisions": [
                    {
                        "candidate_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reason": "string",
                        "reviewed_allowed": False,
                        "approved_allowed": False,
                        "default_guidance_allowed": False,
                        "hard_gate_allowed": False,
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                        "required_followups": ["string"]
                    }
                ],
                "batch_summary": {
                    "accepted_count": 0,
                    "needs_more_evidence_count": 0,
                    "rejected_count": 0,
                    "critical_conflicts": ["string"]
                }
            },
            "decision_policy": {
                "accepted_for_draft": "来源、边界、冲突和优先级均清楚，可进入后续 Codex formal reviewed 准备流程，但不得直接 approved。",
                "needs_more_evidence": "方向正确但来源、实例、契约、边界或冲突说明不足，需要 Codex 补证后再审。",
                "rejected": "与 Phase 41 边界冲突、混入交易规则本体、缺少专业价值、无法治理或存在高风险误导。"
            }
        },
        "quality_gate": quality,
        "candidates": candidates,
    }
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": quality["gate_status"], "candidate_count": len(candidates), "audit_package": str(AUDIT)}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
