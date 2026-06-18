"""Export Phase 43 formal draft reviewed/caveat_only audit package.

This script does not create reviewed knowledge. It only packages the 29 Phase 43
formal draft knowledge items for an external or human reviewed/caveat_only audit.
Approved, default guidance, and hard gate remain explicitly out of scope.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-368"
PHASE = "43"
EXPECTED_COUNT = 29
KNOWLEDGE_DIR = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "knowledge",
    "KB_AI_27_PROJECT_MEMORY",
    start_file=__file__,
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs",
    "audit",
    "phase43_formal_draft_reviewed_audit_package_20260611.json",
    start_file=__file__,
)
QUALITY_REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase43_formal_draft_reviewed_audit_package_quality_gate.json",
    start_file=__file__,
)
GAP_REPORT_PATH = resolve_repo_path(
    "docs",
    "reports",
    "phase43_formal_draft_reviewed_preparation_gap_report.json",
    start_file=__file__,
)

PRIMARY_SOURCE_TYPES = {
    "official_doc",
    "official_repo",
    "paper",
    "research_paper",
    "standard_doc",
    "security_standard",
    "governance_framework",
    "framework_doc",
    "internal_contract",
}
TRADING_BODY_TERMS = (
    "买卖点",
    "仓位建议",
    "止损止盈",
    "杠杆",
    "实盘执行建议",
    "订单执行建议",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(resolve_repo_path(start_file=__file__))).replace("\\", "/")


def load_phase43_formal_drafts() -> list[tuple[Path, dict[str, Any]]]:
    items: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(KNOWLEDGE_DIR.glob("*.json")):
        payload = read_json(path)
        if isinstance(payload, dict) and str(payload.get("knowledge_id", "")).startswith("kb_ai_project_memory.phase43."):
            items.append((path, payload))
    return items


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def source_types(item: dict[str, Any]) -> set[str]:
    return {
        str(source.get("source_type", ""))
        for source in item.get("source_evidence", [])
        if isinstance(source, dict)
    }


def item_source_count(item: dict[str, Any]) -> int:
    source_evidence = item.get("source_evidence")
    return len(source_evidence) if isinstance(source_evidence, list) else 0


def item_node_id(item: dict[str, Any]) -> str:
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    return str(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")


def review_status(item: dict[str, Any]) -> str:
    return str(item.get("review", {}).get("review_status", ""))


def machine_gate(item: dict[str, Any]) -> str:
    return str(item.get("machine_gate", {}).get("default_guidance", ""))


def conflict_status(item: dict[str, Any]) -> str:
    return str(item.get("conflict_audit", {}).get("conflict_status", "unchecked"))


def has_private_memory_content(item: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(item.get("content", {}).get("statement", "")),
            str(item.get("content", {}).get("rationale", "")),
            " ".join(str(x) for x in item.get("applicability", {}).get("applies_when", [])),
            " ".join(str(x) for x in item.get("applicability", {}).get("not_applicable_when", [])),
        ]
    ).lower()
    private_markers = (
        "project_id=",
        "project id:",
        "project_id:",
        "memory_id=",
        "memory_id:",
        "account_id",
        "account id:",
        "api_key",
        "api key",
        "secret",
        "access_token",
        "refresh_token",
        "password=",
        "private_key",
    )
    return any(marker in text for marker in private_markers)


def has_trading_body_pollution(item: dict[str, Any]) -> bool:
    text = " ".join(
        [
            str(item.get("title", "")),
            str(item.get("content", {}).get("statement", "")),
            str(item.get("metadata", {}).get("domain", "")),
            str(item.get("metadata", {}).get("subdomain", "")),
        ]
    )
    return any(term in text for term in TRADING_BODY_TERMS)


def quality_gate(items: list[tuple[Path, dict[str, Any]]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for path, item in items:
        knowledge_id = str(item.get("knowledge_id", ""))
        seen_ids.add(knowledge_id)
        node_id = item_node_id(item)
        if review_status(item) != "draft":
            failures.append({"knowledge_id": knowledge_id, "failure": "formal_item_not_draft"})
        if machine_gate(item) != "deny":
            failures.append({"knowledge_id": knowledge_id, "failure": "machine_gate_not_deny_before_reviewed_audit"})
        if item.get("review", {}).get("default_guidance_allowed") is not False:
            failures.append({"knowledge_id": knowledge_id, "failure": "default_guidance_allowed_not_false"})
        if item.get("review", {}).get("approval_status") not in {"not_requested", None}:
            failures.append({"knowledge_id": knowledge_id, "failure": "approval_status_not_not_requested"})
        if not node_id.startswith("kt.ai_engineering.external_project_memory."):
            failures.append({"knowledge_id": knowledge_id, "failure": "wrong_phase43_canonical_node"})
        if item_source_count(item) < 3:
            failures.append({"knowledge_id": knowledge_id, "failure": "source_evidence_lt_3"})
        if not (source_types(item) & PRIMARY_SOURCE_TYPES):
            failures.append({"knowledge_id": knowledge_id, "failure": "missing_primary_source_type"})
        if conflict_status(item) not in {"none", "resolved"}:
            failures.append({"knowledge_id": knowledge_id, "failure": "unsafe_conflict_status"})
        if has_mojibake(item):
            failures.append({"knowledge_id": knowledge_id, "failure": "mojibake_marker_detected"})
        if has_private_memory_content(item):
            failures.append({"knowledge_id": knowledge_id, "failure": "project_private_memory_content_detected"})
        if has_trading_body_pollution(item):
            failures.append({"knowledge_id": knowledge_id, "failure": "trading_body_pollution_detected"})
        if not item.get("review", {}).get("source_candidate_id"):
            failures.append({"knowledge_id": knowledge_id, "failure": "missing_source_candidate_backlink"})
    if len(seen_ids) != len(items):
        failures.append({"knowledge_id": "package", "failure": "duplicate_knowledge_id"})
    if len(items) != EXPECTED_COUNT:
        failures.append({"knowledge_id": "package", "failure": f"expected_{EXPECTED_COUNT}_items_got_{len(items)}"})
    return {
        "gate_id": "phase43_formal_draft_reviewed_audit_package_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 43 formal draft reviewed/caveat_only audit package",
        "formal_draft_count": len(items),
        "expected_count": EXPECTED_COUNT,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "This gate only exports reviewed/caveat_only audit. It does not create reviewed/approved/default guidance/hard gate.",
    }


def summarize_item(path: Path, item: dict[str, Any]) -> dict[str, Any]:
    metadata = item.get("metadata", {})
    content = item.get("content", {})
    review = item.get("review", {})
    return {
        "knowledge_id": item.get("knowledge_id"),
        "knowledge_path": rel(path),
        "title": item.get("title"),
        "statement": content.get("statement"),
        "claim_type": metadata.get("claim_type"),
        "domain": metadata.get("domain"),
        "subdomain": metadata.get("subdomain"),
        "canonical_node_id": metadata.get("canonical_node_id") or metadata.get("tree_node_id"),
        "source_candidate_id": review.get("source_candidate_id"),
        "source_count": item_source_count(item),
        "source_types": sorted(source_types(item)),
        "conflict_status": conflict_status(item),
        "current_review_status": review_status(item),
        "current_machine_gate": machine_gate(item),
        "current_default_guidance_allowed": review.get("default_guidance_allowed"),
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "applicability": {
            "applies_when": item.get("applicability", {}).get("applies_when", []),
            "not_applicable_when": item.get("applicability", {}).get("not_applicable_when", []),
            "assumptions": item.get("applicability", {}).get("assumptions", []),
        },
        "llm_usage_policy": item.get("llm_usage_policy", {}),
        "machine_gate": item.get("machine_gate", {}),
        "source_evidence": item.get("source_evidence", []),
        "conflict_audit": item.get("conflict_audit", {}),
        "review": {
            "review_status": review.get("review_status"),
            "reviewer": review.get("reviewer"),
            "source_candidate_id": review.get("source_candidate_id"),
            "ai_audit_result_id": review.get("ai_audit_result_id"),
            "approval_status": review.get("approval_status"),
            "default_guidance_allowed": review.get("default_guidance_allowed"),
        },
    }


def build_package(items: list[tuple[Path, dict[str, Any]]], quality: dict[str, Any]) -> dict[str, Any]:
    summaries = [summarize_item(path, item) for path, item in items]
    node_counts = Counter(str(summary["canonical_node_id"]) for summary in summaries)
    return {
        "package_id": "phase43_formal_draft_reviewed_audit_package_20260611",
        "package_type": "formal_draft_reviewed_preparation_audit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": PHASE,
        "task_id": TASK_ID,
        "title": "Phase 43 External Project AI Memory Layer formal draft reviewed/caveat_only 准备审计包",
        "purpose": "审计 29 条 Phase 43 formal draft 是否可由 Codex 后续转换为 formal reviewed/caveat_only 知识。",
        "allowed_decisions": [
            "accepted_for_reviewed_caveat_only",
            "needs_more_evidence",
            "rejected",
            "blocked",
        ],
        "strict_boundaries": [
            "本包只请求 reviewed/caveat_only 许可，不允许 approved。",
            "reviewed 不是 approved，也不进入 default guidance。",
            "machine_gate.default_guidance 最多只能是 caveat_only。",
            "formal draft 当前必须保持 machine_gate.default_guidance=deny，直到后续审计明确 reviewed_allowed=true。",
            "CEK-TA 只保存 Memory Contract 与治理知识，不保存外接项目私有记忆内容。",
            "AI 只能 propose memory，不能直接写 active memory。",
            "Project Memory 不能污染 CEK-TA 通用专业知识库。",
            "pgvector 只能作为可选 semantic index，不是事实源。",
            "第三方 memory engine 只能作为 adapter，不替代 CEK-TA Memory Contract。",
            "不得创建真实数据库、执行 migration、启用外部 memory vendor 或改变 MCP/API 写权限。",
            "不得生成买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
        ],
        "audit_instructions": [
            "逐条检查 formal draft 是否保留 RAG Knowledge 与 Project Memory 分离边界。",
            "检查是否有足够来源支持 claim，尤其是 Memory Contract、write gate、retrieval budget、安全治理和 adapter 选型。",
            "检查是否含外接项目私有目标、任务、错误、决策或产物内容；如有则必须 rejected。",
            "检查 source_evidence、适用范围、不适用场景、conflict_audit 和 llm_usage_policy 是否足够进入 reviewed/caveat_only。",
            "检查 canonical_node_id 是否属于 kt.ai_engineering.external_project_memory.*。",
            "输出只能是 accepted_for_reviewed_caveat_only、needs_more_evidence、rejected 或 blocked。",
            "即便 accepted_for_reviewed_caveat_only，也不得授权 approved、default guidance 或 hard gate。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": "phase43_formal_draft_reviewed_audit_package_20260611",
            "summary": {
                "total": EXPECTED_COUNT,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
                "reviewed_allowed": 0,
                "approved_allowed": 0,
                "default_guidance_allowed": 0,
                "hard_gate_allowed": 0,
            },
            "knowledge_results": [
                {
                    "knowledge_id": "string",
                    "source_candidate_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "reviewed_allowed": True,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
                    "source_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "scope_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "classification_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "memory_boundary_audit": {"status": "pass | warning | fail", "notes": ["string"]},
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
        "formal_draft_count": len(items),
        "expected_count": EXPECTED_COUNT,
        "node_counts": dict(sorted(node_counts.items())),
        "formal_drafts": summaries,
    }


def build_gap_report(items: list[tuple[Path, dict[str, Any]]], quality: dict[str, Any]) -> dict[str, Any]:
    summaries = [summarize_item(path, item) for path, item in items]
    node_counts = Counter(str(summary["canonical_node_id"]) for summary in summaries)
    return {
        "report_id": "phase43_formal_draft_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "phase": PHASE,
        "task_id": TASK_ID,
        "formal_draft_count": len(items),
        "quality_gate": quality,
        "node_counts": dict(sorted(node_counts.items())),
        "draft_summaries": [
            {
                "knowledge_id": summary["knowledge_id"],
                "source_candidate_id": summary["source_candidate_id"],
                "statement": summary["statement"],
                "canonical_node_id": summary["canonical_node_id"],
                "source_count": summary["source_count"],
                "source_types": summary["source_types"],
                "conflict_status": summary["conflict_status"],
                "current_review_status": summary["current_review_status"],
                "current_machine_gate": summary["current_machine_gate"],
            }
            for summary in summaries
        ],
        "audit_package_path": rel(AUDIT_PACKAGE_PATH),
        "formal_reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "next_action": "等待 reviewed/caveat_only 准备审计结果后，再按 Phase 32 工作流创建 formal reviewed 知识。",
    }


def main() -> int:
    items = load_phase43_formal_drafts()
    quality = quality_gate(items)
    package = build_package(items, quality)
    gap_report = build_gap_report(items, quality)
    write_json(AUDIT_PACKAGE_PATH, package)
    write_json(QUALITY_REPORT_PATH, quality)
    write_json(GAP_REPORT_PATH, gap_report)
    print(
        json.dumps(
            {
                "audit_package": str(AUDIT_PACKAGE_PATH),
                "quality_gate": str(QUALITY_REPORT_PATH),
                "gap_report": str(GAP_REPORT_PATH),
                **quality,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
