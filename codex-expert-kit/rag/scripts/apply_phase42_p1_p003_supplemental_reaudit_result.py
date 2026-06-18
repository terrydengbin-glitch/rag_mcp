"""Apply Phase 42 P42-P1-003 supplemental re-audit result.

The re-audit allows P42-P1-003 to move from needs_more_evidence to
accepted_for_draft. It still does not allow reviewed, approved, default
guidance or hard gate. This script updates candidate workflow only and exports
the six Phase 42 P1 accepted candidates for a separate reviewed-preparation
audit.
"""

from __future__ import annotations

import json
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
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
KNOWLEDGE_INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)

AUDIT_RESULT_ID = "audit_result_phase42_p1_p003_supplemental_reaudit_20260611_strict_v2"
SOURCE_PACKAGE_ID = "phase42_p1_p003_supplemental_reaudit_package_20260611"
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path("docs", "reports", "phase42_p1_p003_supplemental_reaudit_import_report.json", start_file=__file__)

REVIEWED_PACKAGE_ID = "phase42_p1_reviewed_preparation_audit_package_20260611"
REVIEWED_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{REVIEWED_PACKAGE_ID}.json", start_file=__file__)
REVIEWED_REPORT_PATH = resolve_repo_path("docs", "reports", "phase42_p1_reviewed_preparation_gap_report.json", start_file=__file__)

P003_CANDIDATE_ID = "cand_20260611_phase42_p42_p1_003_qdrant_payload_index_metadata_filter_rule_001"
P1_TASK_IDS = {"P42-P1-001", "P42-P1-002", "P42-P1-003", "P42-P1-004", "P42-P1-005", "P42-P1-006"}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    cur: Any = item
    for part in path:
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def append_unique(items: list[Any], entry: dict[str, Any], key: str) -> None:
    value = entry.get(key)
    for item in items:
        if isinstance(item, dict) and item.get(key) == value:
            return
    items.append(entry)


def candidate_path(candidate_id: str) -> Path:
    matches = list(CANDIDATE_DIR.glob(f"{candidate_id}.json"))
    if not matches:
        raise FileNotFoundError(candidate_id)
    return matches[0]


def load_formal_ids() -> set[str]:
    payload = read_json(KNOWLEDGE_INDEX_PATH)
    items = payload.get("items")
    if not isinstance(items, list):
        return set()
    return {str(item.get("knowledge_id")) for item in items if isinstance(item, dict) and item.get("knowledge_id")}


def build_audit_result() -> dict[str, Any]:
    return {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "external_ai_strict_reaudit_transcribed_by_codex",
        "audited_at": TODAY,
        "package_id": SOURCE_PACKAGE_ID,
        "summary": {
            "total": 1,
            "accepted_for_draft": 1,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
            "reviewed_allowed": 0,
            "approved_allowed": 0,
            "default_guidance_allowed": 0,
            "hard_gate_allowed": 0,
        },
        "candidate_results": [
            {
                "candidate_id": P003_CANDIDATE_ID,
                "research_task_id": "P42-P1-003",
                "decision": "accepted_for_draft",
                "confidence": "high",
                "reviewed_allowed": False,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": [
                    "补证已拆清 Qdrant payload index/filtering 工具能力与 CEK-TA provenance/citation contract。",
                    "Phase42 RAG/vector storage contract、Phase41 citation resolver contract 和 external AI active retrieval protocol 足以补足 formal_knowledge_id、citation_resolution_status、source version 语义。",
                ],
                "source_audit": {
                    "status": "pass",
                    "notes": [
                        "Qdrant 官方来源支撑 payload index/filtering。",
                        "CEK-TA 内部契约支撑 formal index、citation resolver 和 provenance metadata。",
                    ],
                },
                "conflict_audit": {
                    "status": "pass",
                    "notes": ["未发现与 Phase 42 P0 formal reviewed 知识的直接冲突。"],
                },
                "scope_audit": {
                    "status": "pass",
                    "notes": [
                        "仍归类于 kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage。",
                        "没有混入 Trading Engineering 本体。",
                    ],
                },
                "classification_audit": {
                    "status": "pass",
                    "notes": ["canonical_node_id 属于 AI Engineering 数据库/存储工程分支。"],
                },
                "required_followups": [
                    "后续 formal draft 必须拆成 Qdrant tool capability 和 CEK-TA provenance/citation contract 两节。",
                    "后续 reviewed/caveat_only 仍需单独审计许可。",
                ],
                "proposed_handoff_patch": {
                    "source_patch_notes": [
                        "保留 Qdrant 官方文档作为 payload index/filtering 工具来源。",
                        "保留 CEK-TA 内部契约作为 formal_knowledge_id/citation/source version 语义来源。",
                    ],
                    "content_patch_notes": [
                        "formal draft 必须包含 FilteredVectorRetrievalResult schema。",
                        "明确 vector hit -> source/chunk metadata -> citation resolver -> formal index lookup -> machine_gate check 的链路。",
                    ],
                    "boundary_patch_notes": [
                        "Vector DB 是 retrieval index，不是 canonical store。",
                        "Vector similarity hit 不是 citation resolved。",
                        "citation resolved 也不是 default guidance。",
                        "filtered retrieval result 不得写 final_gate。",
                    ],
                    "conflict_patch_notes": [
                        "不得把 Qdrant 查到相似 chunk 解释为 reviewed/approved knowledge。",
                    ],
                },
            }
        ],
        "hard_boundaries": [
            "accepted_for_draft 不是 reviewed。",
            "不得创建 approved/default guidance/hard gate。",
            "不得创建真实数据库、执行 migration、启用 Qdrant 或改变 MCP/API 写权限。",
        ],
    }


def patch_p003(candidate: dict[str, Any], audit_result: dict[str, Any]) -> None:
    result = audit_result["candidate_results"][0]
    status = candidate.setdefault("status", {})
    workflow = candidate.setdefault("workflow", {})
    review = candidate.setdefault("review", {})
    machine_gate = candidate.setdefault("machine_gate", {})
    conversion_target = candidate.setdefault("conversion_target", {})

    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["updated_at"] = TODAY
    status["decision_reason"] = "P42-P1-003 二审通过，可升级 accepted_for_draft；不得 reviewed/approved/default guidance/hard gate。"

    workflow["stage"] = "ai_audited"
    workflow["queue_group"] = "ai_passed"
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["ai_audit_result_id"] = AUDIT_RESULT_ID
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["next_action"] = "prepare_formal_draft_after_separate_reviewed_gate"

    conversion_target["target_review_status"] = "draft"
    conversion_target["default_guidance_allowed"] = False
    conversion_target["hard_gate_allowed"] = False

    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "P42-P1-003 accepted_for_draft only; reviewed/default guidance requires later gate."
    machine_gate["requires_human_escalation"] = True

    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "auditor": audit_result["auditor"],
        "audited_at": audit_result["audited_at"],
        "decision": result["decision"],
        "confidence": result["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result["reasons"],
        "required_followups": result["required_followups"],
        "source_audit": result["source_audit"],
        "conflict_audit": result["conflict_audit"],
        "scope_audit": result["scope_audit"],
        "classification_audit": result["classification_audit"],
        "proposed_handoff_patch": result["proposed_handoff_patch"],
        "boundary": "P42-P1-003 re-audit allows accepted_for_draft only.",
    }
    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        append_unique(
            audit_log,
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase42_p1_p003_supplemental_reaudit_imported",
                "reason": "二审通过，升级为 accepted_for_draft；仍不允许 reviewed/approved/default/hard gate。",
                "audit_result_id": AUDIT_RESULT_ID,
            },
            "action",
        )


def is_phase42_p1_ai_passed(candidate: dict[str, Any], formal_ids: set[str]) -> bool:
    rid = str(candidate.get("research_task_id", ""))
    if rid not in P1_TASK_IDS:
        return False
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return False
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        return False
    if deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is not False:
        return False
    proposed_id = str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), ""))
    return bool(proposed_id) and proposed_id not in formal_ids


def load_reviewed_prep_candidates() -> list[dict[str, Any]]:
    formal_ids = load_formal_ids()
    candidates: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase42_p42_p1_*.json")):
        candidate = read_json(path)
        if is_phase42_p1_ai_passed(candidate, formal_ids):
            candidate["_audit_export_meta"] = {
                "source_file": rel(path),
                "proposed_knowledge_id": deep_get(candidate, ("conversion_target", "proposed_knowledge_id")),
                "formal_index_has_target": False,
                "current_reviewed_allowed": False,
                "current_queue_group": deep_get(candidate, ("workflow", "queue_group")),
                "current_ingestion_decision": deep_get(candidate, ("status", "ingestion_decision")),
                "required_next_decision": "外部审计必须显式给出 reviewed_allowed=true，后续 Codex 才能生成 formal reviewed/caveat_only。",
            }
            candidates.append(candidate)
    return candidates


def summarize(candidate: dict[str, Any]) -> dict[str, Any]:
    sources = as_list(candidate.get("source_refs"))
    return {
        "candidate_id": str(candidate.get("candidate_id", "")),
        "research_task_id": str(candidate.get("research_task_id", "")),
        "statement": str(deep_get(candidate, ("claim", "statement"), "")),
        "canonical_node_id": str(deep_get(candidate, ("classification", "canonical_node_id"), "")),
        "proposed_knowledge_id": str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), "")),
        "source_count": len(sources),
        "source_types": sorted({str(source.get("source_type")) for source in sources if isinstance(source, dict)}),
        "conflict_status": str(deep_get(candidate, ("conflict_audit", "conflict_status"), "")),
        "current_reviewed_allowed": deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")),
        "current_default_guidance_allowed": deep_get(candidate, ("review", "ai_audit", "default_guidance_allowed")),
        "current_hard_gate_allowed": deep_get(candidate, ("review", "ai_audit", "hard_gate_allowed")),
    }


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for candidate in candidates:
        cid = str(candidate.get("candidate_id", ""))
        if cid in seen:
            failures.append({"candidate_id": cid, "failure": "duplicate_candidate_id"})
        seen.add(cid)
        if str(candidate.get("research_task_id", "")) not in P1_TASK_IDS:
            failures.append({"candidate_id": cid, "failure": "not_phase42_p1"})
        if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
            failures.append({"candidate_id": cid, "failure": "not_accepted_for_draft"})
        if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
            failures.append({"candidate_id": cid, "failure": "queue_group_not_ai_passed"})
        if deep_get(candidate, ("review", "ai_audit", "reviewed_allowed")) is not False:
            failures.append({"candidate_id": cid, "failure": "reviewed_allowed_not_false"})
        if deep_get(candidate, ("review", "ai_audit", "approved_allowed")) is not False:
            failures.append({"candidate_id": cid, "failure": "approved_allowed_not_false"})
        if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
            failures.append({"candidate_id": cid, "failure": "default_guidance_allowed_not_false"})
        if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
            failures.append({"candidate_id": cid, "failure": "hard_gate_allowed_not_false"})
        if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if len(as_list(candidate.get("source_refs"))) < 2:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_2"})
        if not str(deep_get(candidate, ("classification", "canonical_node_id"), "")).startswith(
            "kt.ai_engineering.database_storage_engineering."
        ):
            failures.append({"candidate_id": cid, "failure": "wrong_canonical_node"})
    if len(candidates) != 6:
        failures.append({"candidate_id": "batch", "failure": f"expected_6_candidates_but_found_{len(candidates)}"})
    return {
        "gate_id": "phase42_p1_reviewed_preparation_quality_gate",
        "generated_at": TODAY,
        "candidate_count": len(candidates),
        "expected_count": 6,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "This gate only exports reviewed-preparation audit. It does not create formal knowledge.",
    }


def build_reviewed_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": REVIEWED_PACKAGE_ID,
        "package_type": "candidate_reviewed_preparation_audit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": "42",
        "title": "Phase 42 P1 accepted_for_draft 候选 reviewed/caveat_only 准备审计包",
        "purpose": "审计 6 条 Phase 42 P1 候选是否可由 Codex 后续转换为 formal reviewed/caveat_only 知识。",
        "allowed_decisions": ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"],
        "strict_boundaries": [
            "本包只请求 reviewed/caveat_only 许可，不允许 approved。",
            "reviewed 不是 approved，也不进入 default guidance。",
            "machine_gate.default_guidance 最多只能是 caveat_only。",
            "不得创建真实数据库、执行 migration、启用 Qdrant/Feast/MLflow/RLS/pgAudit 或改变 MCP/API 写权限。",
            "不得生成买卖点、仓位、止损止盈、杠杆或实盘执行建议。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": REVIEWED_PACKAGE_ID,
            "summary": {
                "total": 6,
                "accepted_for_reviewed_caveat_only": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
                "approved_allowed": 0,
                "default_guidance_allowed": 0,
                "hard_gate_allowed": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_reviewed_caveat_only | needs_more_evidence | rejected | blocked",
                    "reviewed_allowed": True,
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                    "reasons": ["string"],
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
        "quality_gate": gate,
        "candidate_summaries": [summarize(candidate) for candidate in candidates],
        "candidates": candidates,
    }


def write_reviewed_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    summaries = [summarize(candidate) for candidate in candidates]
    node_counts = Counter(item["canonical_node_id"] for item in summaries)
    report = {
        "report_id": "phase42_p1_reviewed_preparation_gap_report",
        "generated_at": TODAY,
        "phase": "42",
        "candidate_count": len(candidates),
        "quality_gate": gate,
        "node_counts": dict(sorted(node_counts.items())),
        "candidate_summaries": summaries,
        "audit_package_path": str(REVIEWED_PACKAGE_PATH),
        "formal_knowledge_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "next_action": "等待 reviewed/caveat_only 准备审计结果后，再按 Phase 32 工作流创建 formal reviewed 知识。",
    }
    write_json(REVIEWED_REPORT_PATH, report)


def run() -> dict[str, Any]:
    audit_result = build_audit_result()
    write_json(AUDIT_RESULT_PATH, audit_result)

    path = candidate_path(P003_CANDIDATE_ID)
    candidate = read_json(path)
    patch_p003(candidate, audit_result)
    write_json(path, candidate)

    reviewed_candidates = load_reviewed_prep_candidates()
    gate = quality_gate(reviewed_candidates)
    package = build_reviewed_package(reviewed_candidates, gate)
    write_json(REVIEWED_PACKAGE_PATH, package)
    write_reviewed_report(reviewed_candidates, gate)

    report = {
        "report_id": "phase42_p1_p003_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "updated_candidate_id": P003_CANDIDATE_ID,
        "updated_decision": "accepted_for_draft",
        "reviewed_preparation_package_path": str(REVIEWED_PACKAGE_PATH),
        "reviewed_preparation_candidate_count": len(reviewed_candidates),
        "formal_knowledge_created": 0,
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "gate_status": "pass" if gate["gate_status"] == "pass" else "fail",
        "boundary": "P42-P1-003 is accepted_for_draft only. Formal reviewed conversion requires the exported reviewed-preparation audit result.",
    }
    write_json(IMPORT_REPORT_PATH, report)
    return report


def main() -> int:
    report = run()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
