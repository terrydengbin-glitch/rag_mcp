"""Export Phase 38 P0-Core candidate audit package."""

from __future__ import annotations

import json
import sys
from pathlib import Path


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-10"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase38_p0_core_candidate_audit_package_20260610.json", start_file=__file__)


def main() -> int:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase38_*.json")):
        candidates.append(json.loads(path.read_text(encoding="utf-8-sig")))

    package = {
        "package_id": "phase38_p0_core_candidate_audit_package_20260610",
        "package_type": "candidate_ai_audit_package",
        "generated_at": TODAY,
        "phase": "38",
        "title": "Phase 38 P0-Core AI 模型平台与交易 Gating/Scoring POC 候选知识审计包",
        "purpose": "统一审计 Phase 38 P0-Core 候选知识，确认来源充分性、适用边界、冲突风险、AI 使用安全和跨分支路由。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 approved。",
            "LLM audit assistant 不能做最终交易 gate。",
            "Numeric scorer 不能下单，也不能绕过 deterministic final gate。",
            "交易规则本体必须路由到 Phase 37 / Trading Engineering。",
            "不得把项目私有事实、账号数据、密钥或具体策略规则写入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "逐条判断候选是否可转为 formal draft/reviewed，或需要补来源、改边界、拆分、拒绝。",
            "focus_checks": [
                "是否有足够权威来源支持。",
                "是否错误收录了 Trading Engineering 规则本体。",
                "是否把 LLM 或 scorer 误设为最终交易裁决者。",
                "是否存在无来源默认指导、冲突未处理或过期依赖。",
                "是否需要补充论文、官方文档或工程实例。",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": "phase38_p0_core_candidate_audit_package_20260610",
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
            },
        },
        "candidate_count": len(candidates),
        "planned_p0_core_total": 43,
        "candidates": candidates,
    }
    AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_package": str(AUDIT), "candidate_count": len(candidates)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
