"""Export Phase 42 P0 database/storage candidate AI audit package.

The package is for external AI/human audit only. It does not promote
candidates to formal reviewed knowledge and never marks anything as approved.
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


TODAY = "2026-06-11"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase42_candidate_audit_package_20260611.json", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase42_candidate_audit_package_quality_gate.json", start_file=__file__)
MATRIX = resolve_repo_path("docs", "research", "phase42_database_storage_collection_matrix.md", start_file=__file__)

PRIMARY_SOURCE_TYPES = {
    "official_doc",
    "research_paper",
    "standard_doc",
    "governance_framework",
    "security_standard",
    "framework_doc",
}

TRADING_BODY_TERMS = (
    "买卖点",
    "仓位建议",
    "止损止盈",
    "实盘执行",
    "订单执行建议",
    "具体策略参数",
)


def expected_p0() -> set[str]:
    expected: set[str] = set()
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P42-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] == "P0":
            expected.add(cells[0])
    return expected


def load_candidates() -> list[dict[str, Any]]:
    expected = expected_p0()
    candidates: list[dict[str, Any]] = []
    for path in sorted(CAND_DIR.glob("cand_20260611_phase42_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(raw.get("research_task_id", "")) in expected:
            candidates.append(raw)
    return candidates


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def has_trading_body_pollution(item: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(item.get("claim", {}).get("statement", "")),
            str(item.get("claim", {}).get("normalized_claim", "")),
            str(item.get("classification", {}).get("domain", "")),
            str(item.get("classification", {}).get("subdomain", "")),
        ]
    )
    return any(term in text for term in TRADING_BODY_TERMS)


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    expected = expected_p0()
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in candidates:
        candidate_id = str(item.get("candidate_id", ""))
        research_task_id = str(item.get("research_task_id", ""))
        seen.add(research_task_id)
        source_refs = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in source_refs if isinstance(src, dict)}
        canonical_node_id = str(item.get("classification", {}).get("canonical_node_id", ""))
        not_applicable = " ".join(item.get("applicability", {}).get("not_applicable_when", []))

        if research_task_id not in expected:
            failures.append({"candidate_id": candidate_id, "failure": "unexpected_research_task_id"})
        if not canonical_node_id.startswith("kt.ai_engineering.database_storage_engineering."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if len(source_refs) < 2:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_2"})
        if not (source_types & PRIMARY_SOURCE_TYPES):
            failures.append({"candidate_id": candidate_id, "failure": "missing_primary_source_type"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": candidate_id, "failure": "unsafe_conflict_status"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": candidate_id, "failure": "not_candidate_proposed"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate_id, "failure": "machine_gate_not_deny"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "workflow_default_guidance_not_false"})
        if "Trading Engineering" not in not_applicable:
            failures.append({"candidate_id": candidate_id, "failure": "missing_trading_boundary"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
        if has_trading_body_pollution(item):
            failures.append({"candidate_id": candidate_id, "failure": "trading_body_pollution_in_claim_or_classification"})

    for missing in sorted(expected - seen):
        failures.append({"research_task_id": missing, "failure": "missing_candidate"})

    return {
        "report_id": "phase42_candidate_audit_package_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 42 P0 database/storage candidate audit package",
        "candidate_count": len(candidates),
        "planned_p0_total": len(expected),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }


def build_package(candidates: list[dict[str, Any]], quality: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": "phase42_candidate_audit_package_20260611",
        "package_type": "candidate_ai_audit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": "42",
        "title": "Phase 42 Database / Data Contract / Storage Engineering P0 候选知识审计包",
        "purpose": "审计 Phase 42 P0 数据库、数据契约、审计日志、向量库、迁移、备份恢复和数据生命周期候选知识，确认是否可进入 accepted_for_draft 或需要补证/拒绝。",
        "strict_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 reviewed，也不是 approved。",
            "Vector DB 只能作为 retrieval index，不能作为 canonical store。",
            "PostgreSQL/关系库作为事实主库的建议必须保留适用边界，不能变成真实部署指令。",
            "LLM audit 可以写审计结果，但不能写 final_gate 决策表。",
            "final_gate、score_result、audit ledger 等高价值决策记录必须强调可追踪、可回放、可审计。",
            "本包不得生成买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
            "K 线、fill model、风控本体应路由到 Trading Engineering，不归入本分支。",
            "不得把项目私有字段、账号数据、密钥或真实生产数据库结构写入通用知识。",
        ],
        "audit_instructions": [
            "逐条判断来源是否足以支持 claim，不能超出官方文档、标准或工程文档可证明范围。",
            "检查 canonical_node_id 是否属于 kt.ai_engineering.database_storage_engineering.*。",
            "检查是否清楚区分 canonical store、audit ledger、vector index、manifest store、feature store 和 registry。",
            "检查是否有适用范围、不适用场景、冲突处理和 AI 使用边界。",
            "检查是否存在中文乱码、测试污染、mock 污染或 Trading Engineering 本体污染。",
            "输出只能是 accepted_for_draft、needs_more_evidence 或 rejected。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": "phase42_candidate_audit_package_20260611",
            "summary": {
                "total": 0,
                "accepted_for_draft": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
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
        "planned_p0_total": len(expected_p0()),
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
