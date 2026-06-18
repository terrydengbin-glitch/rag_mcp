"""Export Phase 38 P0-Extended / P1 candidate audit package."""

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
AUDIT = resolve_repo_path("docs", "audit", "phase38_extended_p1_candidate_audit_package_20260610.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase38_extended_p1_candidate_quality_gate.json", start_file=__file__)

TARGET_IDS = {
    "P38-A08",
    "P38-A09",
    "P38-A10",
    "P38-B08",
    "P38-B09",
    "P38-B10",
    "P38-C08",
    "P38-C09",
    "P38-C10",
    "P38-D07",
    "P38-D08",
    "P38-D09",
    "P38-D10",
    "P38-E07",
    "P38-E08",
    "P38-E09",
    "P38-E10",
    "P38-F07",
    "P38-F08",
    "P38-F09",
    "P38-F10",
    "P38-G05",
    "P38-G06",
}


def load_candidates() -> list[dict[str, Any]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase38_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if raw.get("research_task_id") in TARGET_IDS:
            candidates.append(raw)
    return candidates


def main() -> int:
    candidates = load_candidates()
    quality = json.loads(QUALITY.read_text(encoding="utf-8-sig"))
    failures = []
    if len(candidates) != 23:
        failures.append({"failure": "candidate_count_mismatch", "expected": 23, "actual": len(candidates)})
    if quality.get("gate_status") != "pass":
        failures.append({"failure": "quality_gate_not_pass", "quality_gate": quality.get("gate_status")})

    package = {
        "package_id": "phase38_extended_p1_candidate_audit_package_20260610",
        "package_type": "candidate_ai_audit_package",
        "generated_at": TODAY,
        "phase": "38",
        "task_id": "CEK-TA-285",
        "title": "Phase 38 P0-Extended / P1 AI Engineering 候选知识审计包",
        "purpose": "统一审计 Phase 38 剩余 23 条 P0-Extended / P1 候选知识，确认是否可进入 formal reviewed，或需要补证、改边界、拆分、拒绝。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 approved。",
            "reviewed 也不是 approved；默认指导必须另有人工治理任务。",
            "本包只审计 AI Engineering 方法，不审计 K 线、回测、fill model、风控、执行等 Trading Engineering 本体。",
            "LLM audit assistant 不能做最终交易 gate。",
            "Numeric scorer 不能下单，也不能绕过 deterministic final gate。",
            "不得把项目私有事实、账号数据、密钥或具体策略规则写入 AI Engineering。"
        ],
        "auditor_instruction": {
            "goal": "逐条判断候选是否可转为 formal reviewed，或需要补来源、改边界、拆分、拒绝。",
            "focus_checks": [
                "是否有至少 2 个来源，且至少 1 个为 official_doc、paper 或 governance_framework。",
                "是否错误收录了 Trading Engineering 规则本体。",
                "是否把模型解释、校准、OPE、发布治理、RAG 引用治理夸大成交易收益承诺。",
                "是否存在无来源默认指导、冲突未处理或过期依赖。",
                "是否需要补充论文、官方文档或工程实例。",
                "是否应降级为 caveat_only，而不是 allow/default guidance。"
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": "phase38_extended_p1_candidate_audit_package_20260610",
                "decisions": [
                    {
                        "candidate_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reason": "string",
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
                    "misrouted_to_trading_count": 0
                }
            }
        },
        "quality_gate": quality,
        "candidate_count": len(candidates),
        "planned_remaining_total": 23,
        "candidates": candidates,
        "export_failures": failures,
    }
    AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_package": str(AUDIT), "candidate_count": len(candidates), "failure_count": len(failures)}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
