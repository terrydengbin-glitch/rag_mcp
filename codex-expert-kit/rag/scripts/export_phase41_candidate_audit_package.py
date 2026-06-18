"""Export Phase 41 P0-Core candidate AI audit package.

The package is for external AI/human audit only. It does not promote candidates
to formal reviewed knowledge and never marks anything as approved.
"""

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
AUDIT = resolve_repo_path("docs", "audit", "phase41_candidate_audit_package_20260610.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase41_candidate_quality_gate.json", start_file=__file__)
MATRIX = resolve_repo_path("docs", "research", "phase41_hybrid_scoring_collection_matrix.md", start_file=__file__)


PRIMARY_SOURCE_TYPES = {
    "official_doc",
    "research_paper",
    "standard_doc",
    "governance_framework",
    "security_standard",
    "regulator_release",
    "regulator_review",
}

TRADING_BODY_TERMS = (
    "K线",
    "K 线",
    "fill model",
    "订单状态机",
    "仓位",
    "止损",
    "止盈",
    "交易所执行",
)


def expected_p0_core() -> set[str]:
    expected: set[str] = set()
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P41-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] == "P0-Core":
            expected.add(cells[0])
    return expected


def load_candidates() -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    expected = expected_p0_core()
    for path in sorted(CAND_DIR.glob("cand_20260610_phase41_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(raw.get("research_task_id", "")) in expected:
            candidates.append(raw)
    return candidates


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def has_trading_body_pollution(item: dict[str, Any]) -> bool:
    claim_text = " ".join(
        [
            str(item.get("claim", {}).get("statement", "")),
            str(item.get("claim", {}).get("normalized_claim", "")),
            str(item.get("classification", {}).get("domain", "")),
            str(item.get("classification", {}).get("subdomain", "")),
        ]
    )
    return any(term in claim_text for term in TRADING_BODY_TERMS)


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    expected = expected_p0_core()
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
        if research_task_id not in expected:
            failures.append({"candidate_id": candidate_id, "failure": "unexpected_research_task_id"})
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
        if has_trading_body_pollution(item):
            failures.append({"candidate_id": candidate_id, "failure": "trading_body_pollution_in_claim_or_classification"})
    for missing in sorted(expected - seen):
        failures.append({"research_task_id": missing, "failure": "missing_candidate"})
    return {
        "report_id": "phase41_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 41 P0-Core candidate audit package",
        "candidate_count": len(candidates),
        "planned_p0_core_total": len(expected),
        "checks": {
            "source_refs_min_3": "pass" if all(len(item.get("source_refs") or []) >= 3 for item in candidates) else "fail",
            "has_primary_source_type": "pass"
            if all(
                {str(src.get("source_type")) for src in (item.get("source_refs") or []) if isinstance(src, dict)}
                & PRIMARY_SOURCE_TYPES
                for item in candidates
            )
            else "fail",
            "conflict_status_safe": "pass"
            if all(item.get("conflict_audit", {}).get("conflict_status") in {"none", "resolved"} for item in candidates)
            else "fail",
            "review_status_candidate_only": "pass"
            if all(item.get("status", {}).get("review_status") == "proposed" for item in candidates)
            else "fail",
            "machine_gate_denies_default_guidance": "pass"
            if all(item.get("machine_gate", {}).get("default_guidance") == "deny" for item in candidates)
            else "fail",
            "canonical_nodes_under_ai_engineering": "pass"
            if all(str(item.get("classification", {}).get("canonical_node_id")).startswith("kt.ai_engineering.") for item in candidates)
            else "fail",
            "no_mojibake_markers": "pass" if all(not has_mojibake(item) for item in candidates) else "fail",
            "no_trading_body_pollution_in_claim_or_classification": "pass"
            if all(not has_trading_body_pollution(item) for item in candidates)
            else "fail",
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
        "package_id": "phase41_candidate_audit_package_20260610",
        "package_type": "candidate_ai_audit_package",
        "generated_at": TODAY,
        "phase": "41",
        "title": "Phase 41 Hybrid Scoring 与 Qwen3 审计助手 P0-Core 候选知识审计包",
        "purpose": "统一审计 Phase 41 P0-Core 候选知识，确认来源充分性、适用边界、冲突风险、AI 使用安全、Qwen3 权限边界、deterministic final gate 边界和跨分支路由。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 approved。",
            "reviewed 不等于 approved。",
            "Qwen3 只能做 audit assistant，不做 numeric scorer、final gate 或事实来源。",
            "表格/统计模型只做 scorer、risk ranking 或 review priority，不直接执行交易。",
            "raw score 不得直接作为交易概率或 final gate 输入。",
            "deterministic final gate 是最终 allow/block/reduce_size 权限来源，但可以读取校准后的 scorer 风险信号和 threshold policy。",
            "RAG context、用户交易摘要和检索文档必须视为不可信输入。",
            "交易规则本体必须路由到 Phase 37 / Trading Engineering。",
            "不得把项目私有事实、账号数据、密钥或具体策略规则写入 AI Engineering。",
        ],
        "auditor_instruction": {
            "goal": "逐条判断候选是否可转为 formal draft/reviewed，或需要补来源、改边界、拆分、拒绝。",
            "focus_checks": [
                "是否有足够权威来源支持，且至少包含官方文档、论文、标准或治理框架。",
                "是否错误收录了 Trading Engineering 规则本体。",
                "是否把 Qwen3 或 RAG 输出误设为事实来源或最终交易裁决者。",
                "是否把 raw score、未校准概率或自然语言 recommendation 直接接入 final gate。",
                "是否清楚区分 scorer、calibrator、Qwen3 audit assistant、RAG 和 deterministic final gate 的责任。",
                "是否存在无来源默认指导、冲突未处理、过期依赖或中文乱码。",
                "是否需要补充论文、官方文档、监管案例、工程实例或反例。",
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": "phase41_candidate_audit_package_20260610",
                "decisions": [
                    {
                        "candidate_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
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
        "planned_p0_core_total": len(expected_p0_core()),
        "candidates": candidates,
    }
    AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"audit_package": str(AUDIT), "quality_gate": str(QUALITY), **quality}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
