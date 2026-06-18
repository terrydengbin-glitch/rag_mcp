"""Import Phase 43 candidate audit result and export supplemental re-audit package.

This script updates candidate audit state only. It does not create formal
reviewed knowledge, approved knowledge, default guidance, or hard gates.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
AUDIT_SOURCE = Path(r"C:\Users\dove\Downloads\audit_result_phase43_candidate_audit_package_20260611_strict_v1.json")
AUDIT_ARCHIVE = resolve_repo_path(
    "docs", "audit", "audit_result_phase43_candidate_audit_package_20260611_strict_v1.json", start_file=__file__
)
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
IMPORT_REPORT = resolve_repo_path("docs", "reports", "phase43_candidate_audit_import_report.json", start_file=__file__)
SUPPLEMENT_RESEARCH = resolve_repo_path("docs", "research", "phase43_supplemental_research.md", start_file=__file__)
SUPPLEMENT_AUDIT = resolve_repo_path("docs", "audit", "phase43_supplemental_reaudit_package_20260611.json", start_file=__file__)
SUPPLEMENT_QUALITY = resolve_repo_path("docs", "reports", "phase43_supplemental_reaudit_quality_gate.json", start_file=__file__)


REBUILD_SLUGS = {
    "P43-P0-013": "memory_write_security_gate",
    "P43-P0-014": "no_auto_save_all_chat",
    "P43-P0-015": "memory_write_whitelist",
    "P43-P0-016": "memory_write_blacklist",
    "P43-P0E-002": "default_context_key_memory_only",
    "P43-P0E-003": "explicit_request_long_logs_audit_history",
}

ACCEPTED_RENAMES = {
    "P43-P0-021": "memoryitem_rollback_integrity",
}


INTERNAL_SOURCES: dict[str, dict[str, Any]] = {
    "phase43_project_memory_contract": {
        "source_id": "src_phase43_project_memory_contract",
        "source_title": "Phase 43 Project Memory Contract",
        "source_url": "docs/contracts/phase43_project_memory_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines MemoryItem v0.1, memory types, lifecycle, source, write_policy, security, retrieval and integrity fields.",
    },
    "phase43_mcp_api_contract": {
        "source_id": "src_phase43_project_memory_mcp_api_contract",
        "source_title": "Phase 43 Project Memory MCP/API Contract",
        "source_url": "docs/contracts/phase43_project_memory_mcp_api_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines Project Memory MCP/API tools, read/write/admin permissions, error schema, and forbidden direct active writes.",
    },
    "phase43_write_retrieval_policy": {
        "source_id": "src_phase43_memory_write_retrieval_policy",
        "source_title": "Phase 43 Memory Write Gate and Retrieval Policy",
        "source_url": "docs/contracts/phase43_memory_write_retrieval_policy.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines source checks, secret scan, prompt injection scan, memory poisoning scan, visibility checks, conflict checks and retrieval budgets.",
    },
    "phase43_security_governance": {
        "source_id": "src_phase43_memory_security_governance_contract",
        "source_title": "Phase 43 Memory Security Governance Contract",
        "source_url": "docs/contracts/phase43_memory_security_governance_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines memory poisoning, prompt injection, rollback, integrity, visibility and third-party adapter security boundaries.",
    },
    "phase43_retention_privacy": {
        "source_id": "src_phase43_memory_retention_privacy_contract",
        "source_title": "Phase 43 Memory Retention Privacy Contract",
        "source_url": "docs/contracts/phase43_memory_retention_privacy_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines retention, deletion, export, tombstone, privacy minimization and stale memory review rules.",
    },
    "phase43_scope": {
        "source_id": "src_phase43_external_project_ai_memory_scope",
        "source_title": "Phase 43 External Project AI Memory Layer Scope",
        "source_url": "docs/research/phase43_external_project_ai_memory_scope.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines Phase 43 scope, L3 topics, cross-branch boundaries and the 29-topic candidate matrix.",
    },
    "external_ai_active_retrieval_protocol": {
        "source_id": "src_cek_ta_external_ai_active_retrieval_protocol",
        "source_title": "External AI Active Retrieval Protocol",
        "source_url": "docs/contracts/external_ai_active_retrieval_protocol.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "summary": "Defines when external project AI must search CEK-TA knowledge, how to cite, and what to do when retrieval is missing.",
    },
    "phase35_task_card": {
        "source_id": "src_phase35_external_ai_active_retrieval_task_card",
        "source_title": "Phase 35 External AI Active Retrieval Protocol Task Card",
        "source_url": "docs/tasks/phase35_external_ai_active_retrieval_protocol.md",
        "source_type": "task_card",
        "publisher": "CEK-TA",
        "summary": "Documents the external AI active retrieval workflow and governance scope.",
    },
    "postgres_jsonb": {
        "source_id": "src_postgres_jsonb",
        "source_title": "PostgreSQL Documentation: JSON Types",
        "source_url": "https://www.postgresql.org/docs/current/datatype-json.html",
        "source_type": "official_doc",
        "publisher": "PostgreSQL",
        "summary": "PostgreSQL documents jsonb as a decomposed binary format that is efficient for processing JSON data.",
    },
    "pgvector": {
        "source_id": "src_pgvector",
        "source_title": "pgvector: Open-source vector similarity search for Postgres",
        "source_url": "https://github.com/pgvector/pgvector",
        "source_type": "official_doc",
        "publisher": "pgvector",
        "summary": "pgvector documents vector similarity search in Postgres while storing vectors with the rest of the data.",
    },
}

REJECTED_ORIGINAL_CLAIMS = {
    "P43-P0-013": "rejected_original_p43_p0_013_empty_slug",
    "P43-P0-014": "rejected_original_p43_p0_014_empty_slug",
    "P43-P0-015": "rejected_original_p43_p0_015_empty_slug",
    "P43-P0-016": "rejected_original_p43_p0_016_empty_slug",
    "P43-P0E-002": "rejected_original_p43_p0e_002_empty_slug",
    "P43-P0E-003": "rejected_original_p43_p0e_003_duplicate_deprecated_memory",
}

SOURCE_TYPE_MAP = {
    "security_research": "security_standard",
    "security_guidance": "security_standard",
    "internal_scope": "internal_contract",
    "internal_task_card": "task_card",
}


def normalize_source_types(item: dict[str, Any]) -> None:
    for ref in item.get("source_refs") or []:
        if not isinstance(ref, dict):
            continue
        source_type = ref.get("source_type")
        if source_type in SOURCE_TYPE_MAP:
            ref["source_type"] = SOURCE_TYPE_MAP[source_type]


SUPPLEMENT_SOURCES = {
    "P43-P0-004": ["phase43_mcp_api_contract", "external_ai_active_retrieval_protocol", "phase35_task_card"],
    "P43-P0-005": ["phase43_project_memory_contract", "phase43_scope"],
    "P43-P0-006": ["phase43_project_memory_contract", "phase43_write_retrieval_policy"],
    "P43-P0-007": ["phase43_project_memory_contract", "phase43_scope"],
    "P43-P0-008": ["phase43_project_memory_contract", "phase43_scope"],
    "P43-P0-009": ["phase43_project_memory_contract", "phase43_security_governance"],
    "P43-P0-010": ["phase43_project_memory_contract", "phase43_retention_privacy"],
    "P43-P0-011": ["phase43_project_memory_contract", "phase43_write_retrieval_policy"],
    "P43-P0-019": ["phase43_project_memory_contract", "phase43_security_governance"],
    "P43-P1-002": ["pgvector", "postgres_jsonb", "phase43_project_memory_contract"],
    "P43-P1-003": ["phase43_mcp_api_contract", "phase43_retention_privacy", "phase43_scope"],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def candidate_paths() -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for path in CAND_DIR.glob("cand_20260611_phase43_*.json"):
        data = load_json(path)
        paths[str(data.get("candidate_id"))] = path
    return paths


def find_candidate_path(paths: dict[str, Path], candidate_id: str, topic_id: str) -> Path:
    if candidate_id in paths:
        return paths[candidate_id]
    topic_prefix = topic_id.lower().replace("-", "_")
    matches = sorted(CAND_DIR.glob(f"cand_20260611_phase43_{topic_prefix}_*.json"))
    if not matches:
        raise KeyError(f"Candidate not found: {candidate_id}")
    return matches[0]


def source_ref(key: str) -> dict[str, Any]:
    src = deepcopy(INTERNAL_SOURCES[key])
    src["source_type"] = SOURCE_TYPE_MAP.get(src["source_type"], src["source_type"])
    src.update(
        {
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "score": 86 if src["source_type"].startswith("internal") else 84,
            "relevance": "high",
            "freshness": "time_sensitive",
            "limitations": [],
            "evidence_summary": src.pop("summary"),
            "quoted_excerpt_allowed": False,
        }
    )
    return src


def append_unique_sources(item: dict[str, Any], keys: list[str]) -> None:
    normalize_source_types(item)
    refs = item.setdefault("source_refs", [])
    existing = {str(ref.get("source_id")) for ref in refs if isinstance(ref, dict)}
    for key in keys:
        ref = source_ref(key)
        if ref["source_id"] not in existing:
            refs.append(ref)
            existing.add(ref["source_id"])
    source_quality = item.setdefault("source_quality", {})
    source_quality["supporting_source_count"] = len(refs)
    source_quality["primary_source_count"] = len(
        [ref for ref in refs if ref.get("source_type") in {"official_doc", "security_standard", "research_paper", "internal_contract", "task_card"}]
    )
    source_quality["score"] = round(sum(float(ref.get("score", 70)) for ref in refs) / len(refs), 1)
    evidence = "；".join(str(ref.get("evidence_summary", "")) for ref in refs[:5])
    item.setdefault("claim", {})["evidence_summary"] = evidence


def add_audit(item: dict[str, Any], result: dict[str, Any], action: str) -> None:
    review = item.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": "audit_result_phase43_candidate_audit_package_20260611_strict_v1",
        "package_id": "phase43_candidate_audit_package_20260611",
        "auditor": "GPT-5.5 Pro",
        "decision": result["decision"],
        "confidence": result.get("confidence"),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "proposed_handoff_patch": result.get("proposed_handoff_patch", {}),
    }
    review.setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": action,
            "reason": f"Imported Phase 43 audit decision: {result['decision']}.",
            "audit_result_id": "audit_result_phase43_candidate_audit_package_20260611_strict_v1",
        }
    )


def set_gate_defaults(item: dict[str, Any]) -> None:
    item.setdefault("machine_gate", {})["default_guidance"] = "deny"
    item["machine_gate"]["requires_human_escalation"] = True
    workflow = item.setdefault("workflow", {})
    workflow["reviewed_allowed"] = False
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["visible_in_default_guidance_queue"] = False
    workflow["hidden_from_default_queue"] = True


def set_slug(item: dict[str, Any], topic_id: str, slug: str, sequence: str = "001") -> None:
    item["candidate_id"] = f"cand_20260611_phase43_{topic_id.lower().replace('-', '_')}_{slug}_{sequence}"
    item.setdefault("claim", {})["normalized_claim"] = f"phase43.{slug}.v1"


def main() -> int:
    if AUDIT_SOURCE.exists():
        shutil.copyfile(AUDIT_SOURCE, AUDIT_ARCHIVE)
    audit = load_json(AUDIT_ARCHIVE)
    paths = candidate_paths()
    supplemental: list[dict[str, Any]] = []
    rebuilt_count = 0
    accepted_count = 0
    needs_count = 0
    rejected_count = 0

    for result in audit["candidate_results"]:
        candidate_id = result["candidate_id"]
        topic_id = result["research_task_id"]
        path = find_candidate_path(paths, candidate_id, topic_id)
        item = load_json(path)
        normalize_source_types(item)
        set_gate_defaults(item)
        add_audit(item, result, "phase43_candidate_audit_result_imported")

        decision = result["decision"]
        if decision == "accepted_for_draft":
            accepted_count += 1
            item["status"]["review_status"] = "accepted"
            item["status"]["ingestion_decision"] = "accepted_for_draft"
            item["status"]["decision_reason"] = "Phase 43 严格审计结论为 accepted_for_draft；不得 reviewed/approved/default guidance/hard gate。"
            item["status"]["updated_at"] = TODAY
            item.setdefault("workflow", {})["stage"] = "accepted_for_draft"
            item["workflow"]["queue_group"] = "ai_passed"
            item["workflow"]["candidate_to_formal_allowed"] = True
            item["workflow"]["target_review_status"] = "draft"
            item["workflow"]["next_action"] = "review_formal_knowledge"
            if topic_id in ACCEPTED_RENAMES:
                set_slug(item, topic_id, ACCEPTED_RENAMES[topic_id], "001")
                new_path = CAND_DIR / f"cand_20260611_phase43_{topic_id.lower().replace('-', '_')}_{ACCEPTED_RENAMES[topic_id]}.json"
                write_json(new_path, item)
                if new_path != path:
                    path.unlink()
            else:
                write_json(path, item)
        elif decision == "needs_more_evidence":
            needs_count += 1
            append_unique_sources(item, SUPPLEMENT_SOURCES.get(topic_id, ["phase43_project_memory_contract", "phase43_scope"]))
            item["status"]["review_status"] = "needs_more_evidence"
            item["status"]["ingestion_decision"] = "needs_more_evidence"
            item["status"]["decision_reason"] = "Phase 43 严格审计要求补充直接契约来源；已补证，等待二审。"
            item["status"]["updated_at"] = TODAY
            item.setdefault("workflow", {})["stage"] = "supplemented_for_reaudit"
            item["workflow"]["queue_group"] = "needs_more_evidence"
            item["workflow"]["candidate_to_formal_allowed"] = False
            item["workflow"]["next_action"] = "supplemental_reaudit"
            write_json(path, item)
            supplemental.append(item)
        elif decision == "rejected":
            rejected_count += 1
            item["status"]["review_status"] = "rejected"
            item["status"]["ingestion_decision"] = "reject"
            item["status"]["decision_reason"] = "Phase 43 严格审计发现 slug/normalized_claim 结构问题；原候选拒绝并重建。"
            item["status"]["updated_at"] = TODAY
            item.setdefault("claim", {})["normalized_claim"] = f"phase43.{REJECTED_ORIGINAL_CLAIMS[topic_id]}.v1"
            item.setdefault("workflow", {})["stage"] = "rejected_rebuild_required"
            item["workflow"]["queue_group"] = "rejected"
            item["workflow"]["candidate_to_formal_allowed"] = False
            item["workflow"]["visible_in_candidate_audit_queue"] = False
            item["workflow"]["next_action"] = "rebuilt_candidate_created"
            write_json(path, item)

            rebuilt = deepcopy(item)
            slug = REBUILD_SLUGS[topic_id]
            set_slug(rebuilt, topic_id, slug, "001")
            rebuilt["status"] = {
                "review_status": "proposed",
                "ingestion_decision": "pending_external_audit",
                "decision_reason": "Rebuilt after Phase 43 audit rejected the original candidate because of slug/normalized_claim structure risk.",
                "created_at": TODAY,
                "updated_at": TODAY,
            }
            rebuilt.setdefault("workflow", {})["stage"] = "rebuilt_for_reaudit"
            rebuilt["workflow"]["queue_group"] = "pending"
            rebuilt["workflow"]["candidate_to_formal_allowed"] = False
            rebuilt["workflow"]["visible_in_candidate_audit_queue"] = True
            rebuilt["workflow"]["next_action"] = "supplemental_reaudit"
            rebuilt.setdefault("review", {}).setdefault("audit_log", []).append(
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "rebuilt_after_rejection",
                    "reason": f"Rebuilt with normalized_claim phase43.{slug}.v1.",
                }
            )
            append_unique_sources(rebuilt, SUPPLEMENT_SOURCES.get(topic_id, ["phase43_project_memory_contract", "phase43_scope"]))
            new_path = CAND_DIR / f"cand_20260611_phase43_{topic_id.lower().replace('-', '_')}_{slug}.json"
            write_json(new_path, rebuilt)
            supplemental.append(rebuilt)
            rebuilt_count += 1

    quality_failures: list[dict[str, str]] = []
    seen_claims: set[str] = set()
    for item in supplemental:
        candidate_id = str(item.get("candidate_id", ""))
        normalized_claim = str(item.get("claim", {}).get("normalized_claim", ""))
        if normalized_claim in seen_claims:
            quality_failures.append({"candidate_id": candidate_id, "failure": "duplicate_normalized_claim"})
        seen_claims.add(normalized_claim)
        if re.search(r"phase43\\.\\.v1", normalized_claim):
            quality_failures.append({"candidate_id": candidate_id, "failure": "empty_slug"})
        if len(item.get("source_refs") or []) < 3:
            quality_failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_3"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            quality_failures.append({"candidate_id": candidate_id, "failure": "default_guidance_not_false"})
        if item.get("workflow", {}).get("hard_gate_allowed") is not False:
            quality_failures.append({"candidate_id": candidate_id, "failure": "hard_gate_not_false"})

    supplement_quality = {
        "report_id": "phase43_supplemental_reaudit_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 43 supplemental re-audit package for 11 supplemented + 6 rebuilt candidates",
        "candidate_count": len(supplemental),
        "failure_count": len(quality_failures),
        "failures": quality_failures,
        "gate_status": "pass" if not quality_failures else "fail",
    }
    package = {
        "package_id": "phase43_supplemental_reaudit_package_20260611",
        "package_type": "candidate_ai_reaudit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "phase": "43",
        "title": "Phase 43 External Project AI Memory Layer 补证/重建候选二审包",
        "purpose": "审计 11 条已补充直接契约来源的候选和 6 条已重建 slug/normalized_claim 的候选是否可进入 accepted_for_draft。",
        "strict_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 reviewed，也不是 approved。",
            "reviewed_allowed=false，approved_allowed=false，default_guidance_allowed=false，hard_gate_allowed=false。",
            "CEK-TA 不保存外接项目私有记忆。",
            "AI 只能 propose memory，不能直接写 active memory。",
            "Project Memory 不能污染 CEK-TA 通用专业知识库。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": "phase43_supplemental_reaudit_package_20260611",
            "summary": {"total": 17, "accepted_for_draft": 0, "needs_more_evidence": 0, "rejected": 0, "blocked": 0},
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "high | medium | low",
                    "reasons": ["string"],
                    "required_followups": ["string"],
                }
            ],
        },
        "quality_gate": supplement_quality,
        "candidate_count": len(supplemental),
        "candidates": supplemental,
    }
    SUPPLEMENT_AUDIT.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SUPPLEMENT_QUALITY.write_text(json.dumps(supplement_quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    SUPPLEMENT_RESEARCH.write_text(
        "\n".join(
            [
                "# Phase 43 Supplemental Research",
                "",
                f"- generated_at: {TODAY}",
                "- scope: 11 条 needs_more_evidence 补直接契约来源，6 条 rejected 重建 slug/normalized_claim。",
                "",
                "## 补证来源",
                "",
                *[f"- `{src['source_id']}`: {src['source_title']} - {src['source_url']}" for src in INTERNAL_SOURCES.values()],
                "",
                "## 二审候选",
                "",
                *[
                    f"- `{item['research_task_id']}` `{item['candidate_id']}` `{item['claim']['normalized_claim']}`"
                    for item in supplemental
                ],
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    report = {
        "report_id": "phase43_candidate_audit_import_report",
        "generated_at": TODAY,
        "audit_result_id": audit["audit_result_id"],
        "summary": audit["summary"],
        "accepted_updated": accepted_count,
        "needs_more_evidence_supplemented": needs_count,
        "rejected_originals_marked": rejected_count,
        "rebuilt_candidates_created": rebuilt_count,
        "supplemental_reaudit_candidate_count": len(supplemental),
        "supplemental_reaudit_package": str(SUPPLEMENT_AUDIT),
        "supplemental_quality_gate": supplement_quality,
        "boundary": "No formal reviewed, approved, default guidance, or hard gate was created.",
    }
    write_json(IMPORT_REPORT, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if supplement_quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
