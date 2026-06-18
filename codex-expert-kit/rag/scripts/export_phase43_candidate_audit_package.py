"""Export Phase 43 candidate AI audit package."""

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


TODAY = "2026-06-11"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase43_candidate_audit_package_20260611.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase43_candidate_audit_package_quality_gate.json", start_file=__file__)
MATRIX = resolve_repo_path("docs", "research", "phase43_memory_collection_matrix.md", start_file=__file__)


def expected_topics() -> set[str]:
    expected: set[str] = set()
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P43-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells:
            expected.add(cells[0])
    return expected


def load_candidates() -> list[dict[str, Any]]:
    expected = expected_topics()
    candidates: list[dict[str, Any]] = []
    for path in sorted(CAND_DIR.glob("cand_20260611_phase43_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(raw.get("research_task_id", "")) in expected:
            candidates.append(raw)
    return candidates


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    expected = expected_topics()
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in candidates:
        candidate_id = str(item.get("candidate_id", ""))
        research_task_id = str(item.get("research_task_id", ""))
        seen.add(research_task_id)
        refs = item.get("source_refs") or []
        if research_task_id not in expected:
            failures.append({"candidate_id": candidate_id, "failure": "unexpected_research_task_id"})
        if len(refs) < 3:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_3"})
        if not str(item.get("classification", {}).get("canonical_node_id", "")).startswith("kt.ai_engineering.external_project_memory."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": candidate_id, "failure": "not_candidate_proposed"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate_id, "failure": "machine_gate_not_deny"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "workflow_default_guidance_not_false"})
        if item.get("workflow", {}).get("hard_gate_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "workflow_hard_gate_not_false"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
    for missing in sorted(expected - seen):
        failures.append({"research_task_id": missing, "failure": "missing_candidate"})
    return {
        "report_id": "phase43_candidate_audit_package_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 43 external project AI memory candidate audit package",
        "candidate_count": len(candidates),
        "planned_total": len(expected),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }


def build_package(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": "phase43_candidate_audit_package_20260611",
        "package_type": "candidate_ai_audit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": "43",
        "title": "Phase 43 External Project AI Memory Layer 候选知识审计包",
        "purpose": "审计 Phase 43 外接项目 AI Memory Layer 候选知识，确认是否可进入 accepted_for_draft 或需要补证/拒绝。",
        "strict_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 reviewed，也不是 approved。",
            "CEK-TA 不保存外接项目私有记忆。",
            "AI 只能 propose memory，不能直接写 active memory。",
            "Project Memory 不能污染 CEK-TA 通用专业知识库。",
            "第三方 memory engine 只能作为 adapter，不能成为 CEK-TA 核心契约。",
            "pgvector 只能作为 optional semantic index，不能作为事实源。",
            "本包不得生成买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
        ],
        "audit_instructions": [
            "逐条判断来源是否足以支持 claim，不能超出官方文档、安全组织资料、论文或工程文档可证明范围。",
            "检查 canonical_node_id 是否属于 kt.ai_engineering.external_project_memory.*。",
            "检查是否清楚区分 CEK-TA RAG Knowledge、Project Memory、event_log、adapter、canonical store 和 semantic index。",
            "检查是否有适用范围、不适用场景、冲突处理和 AI 使用边界。",
            "检查是否存在中文乱码、测试污染、mock 污染、Trading Engineering 本体污染或外接项目私有事实污染。",
            "输出只能是 accepted_for_draft、needs_more_evidence 或 rejected。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": "phase43_candidate_audit_package_20260611",
            "summary": {"total": 0, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "high | medium | low",
                    "reasons": ["string"],
                    "source_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "conflict_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "scope_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "classification_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "required_followups": ["string"],
                    "proposed_handoff_patch": {
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                    },
                }
            ],
        },
        "quality_gate": quality,
        "candidate_count": len(candidates),
        "planned_total": len(expected_topics()),
        "candidates": candidates,
    }


def main() -> int:
    candidates = load_candidates()
    quality = quality_gate(candidates)
    package = build_package(candidates, quality)
    AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_package": str(AUDIT), "quality_gate": str(QUALITY), **quality}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
