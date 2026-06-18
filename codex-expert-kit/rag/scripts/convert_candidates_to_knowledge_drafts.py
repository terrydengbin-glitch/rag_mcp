"""Convert accepted ingestion candidates into formal knowledge draft items."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)


ALLOWED_INGESTION_DECISIONS = {
    "convert_to_knowledge_item",
    "convert_to_skill_and_knowledge",
}
ALLOWED_CONFLICT_STATUSES = {"none", "resolved"}


class CandidateRejected(ValueError):
    """Raised when a candidate does not satisfy the draft conversion gate."""


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def require_non_empty(item: dict[str, Any], path: tuple[str, ...], candidate_id: str) -> Any:
    value = deep_get(item, path)
    if value in (None, "", []):
        raise CandidateRejected(f"{candidate_id} missing required field: {'.'.join(path)}")
    return value


def validate_candidate(candidate: dict[str, Any]) -> None:
    candidate_id = str(require_non_empty(candidate, ("candidate_id",), "<unknown>"))
    ingestion_decision = require_non_empty(candidate, ("status", "ingestion_decision"), candidate_id)
    target_review_status = require_non_empty(candidate, ("conversion_target", "target_review_status"), candidate_id)
    conflict_status = require_non_empty(candidate, ("conflict_audit", "conflict_status"), candidate_id)

    if ingestion_decision not in ALLOWED_INGESTION_DECISIONS:
        raise CandidateRejected(f"{candidate_id} ingestion_decision is not convertible: {ingestion_decision}")
    if target_review_status != "draft":
        raise CandidateRejected(f"{candidate_id} target_review_status must be draft, got: {target_review_status}")
    if conflict_status not in ALLOWED_CONFLICT_STATUSES:
        raise CandidateRejected(f"{candidate_id} conflict_status is not allowed for draft: {conflict_status}")
    if deep_get(candidate, ("conflict_audit", "approval_allowed")) is not True:
        raise CandidateRejected(f"{candidate_id} approval_allowed must be true before draft conversion")
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        raise CandidateRejected(f"{candidate_id} stores_full_text must be false")
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        raise CandidateRejected(f"{candidate_id} stores_long_quote must be false")

    for path in (
        ("conversion_target", "proposed_knowledge_id"),
        ("classification", "partition_id"),
        ("classification", "domain"),
        ("classification", "subdomain"),
        ("classification", "tree_node_id"),
        ("classification", "tree_path"),
        ("classification", "rule_type"),
        ("claim", "statement"),
        ("claim", "evidence_summary"),
        ("applicability", "applies_when"),
        ("applicability", "not_applicable_when"),
        ("applicability", "assumptions"),
        ("source_refs",),
        ("source_quality",),
        ("review", "confidence"),
        ("review", "freshness"),
    ):
        require_non_empty(candidate, path, candidate_id)


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source.get("source_id", ""),
        "source_title": source.get("source_title", ""),
        "source_url": source.get("source_url"),
        "source_type": source.get("source_type", "other"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": source.get("accessed_at", ""),
        "version": source.get("version"),
        "reliability": source.get("reliability", ""),
        "relevance": source.get("relevance", ""),
        "evidence_summary": source.get("evidence_summary", ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def shape_conflict(candidate_conflict: dict[str, Any]) -> dict[str, Any]:
    conflicts = []
    for conflict in candidate_conflict.get("conflicts", []) or []:
        conflicts.append(
            {
                "knowledge_id": conflict.get("knowledge_id", ""),
                "conflict_type": conflict.get("conflict_type", ""),
                "severity": conflict.get("severity", ""),
                "resolution": conflict.get("resolution", ""),
                "applicability_boundary": json.dumps(conflict.get("overlap_scope", {}), ensure_ascii=False),
                "default_recommendation": conflict.get("default_recommendation"),
            }
        )
    return {
        "conflict_status": candidate_conflict.get("conflict_status", "none"),
        "checked_against": candidate_conflict.get("checked_against", []),
        "conflicts": conflicts,
        "resolution_summary": candidate_conflict.get("resolution_summary", ""),
        "default_recommendation": "no_default_guidance_until_reviewed",
    }


def build_content(candidate: dict[str, Any]) -> dict[str, Any]:
    claim = candidate["claim"]
    applicability = candidate["applicability"]
    open_questions = deep_get(candidate, ("review", "open_questions"), []) or []
    limitations = applicability.get("limitations", []) or []
    return {
        "statement": claim["statement"],
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": [
            "确认当前项目事实匹配 applies_when。",
            "确认没有命中 not_applicable_when。",
            "确认来源、冲突状态和 open_questions 已在正式评审中关闭或保留 caveat。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 draft 知识当作 approved 默认指导。",
            "在不匹配适用边界时复用该规则。",
        ],
        "validation": [
            "检查 source_evidence 非空且来源可靠性为 medium 或 high。",
            "检查 conflict_status 为 none 或 resolved。",
            "检查 applies_when、not_applicable_when 和 assumptions 均非空。",
        ],
        "risk_notes": limitations + open_questions,
        "citation_notes": claim.get("evidence_summary", ""),
    }


def candidate_to_knowledge(candidate: dict[str, Any]) -> dict[str, Any]:
    validate_candidate(candidate)

    classification = candidate["classification"]
    applicability = candidate["applicability"]
    status = candidate["status"]
    review = candidate["review"]
    knowledge_id = candidate["conversion_target"]["proposed_knowledge_id"]
    today = datetime.now(timezone.utc).date().isoformat()

    audit_log = []
    for entry in review.get("audit_log", []) or []:
        audit_log.append(
            {
                "at": entry.get("at", status.get("updated_at", today)),
                "actor": entry.get("actor", "codex"),
                "decision": entry.get("action", "created"),
                "reason": entry.get("reason", ""),
            }
        )
    audit_log.append(
        {
            "at": today,
            "actor": "codex",
            "decision": "created",
            "reason": f"Converted from ingestion candidate {candidate['candidate_id']} by CEK-TA-102 as draft only.",
        }
    )

    return {
        "schema_version": "1.0.0",
        "knowledge_id": knowledge_id,
        "title": candidate["claim"]["normalized_claim"].replace("_", " ").title(),
        "metadata": {
            "partition_id": classification["partition_id"],
            "domain": classification["domain"],
            "subdomain": classification["subdomain"],
            "rule_type": classification["rule_type"],
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification["tree_node_id"],
            "tree_path": classification["tree_path"],
            "canonical_node_id": classification["tree_node_id"],
            "canonical_tree_path": classification["tree_path"],
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate["candidate_id"],
            "research_task_id": candidate.get("research_task_id", ""),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "general"),
            "applies_when": applicability["applies_when"],
            "not_applicable_when": applicability["not_applicable_when"],
        },
        "content": build_content(candidate),
        "assumptions": applicability["assumptions"],
        "source_evidence": [source_to_evidence(source) for source in candidate["source_refs"]],
        "source_quality": candidate["source_quality"],
        "conflict_audit": shape_conflict(candidate["conflict_audit"]),
        "review": {
            "confidence": review["confidence"],
            "freshness": review["freshness"],
            "review_status": "draft",
            "reviewer": review.get("reviewer"),
            "reviewed_at": None,
            "created_at": status.get("created_at", today),
            "updated_at": status.get("updated_at", today),
            "open_questions": review.get("open_questions", []),
            "decision_log": audit_log,
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from public-source Phase 23 ingestion candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
    }


def target_path_for(item: dict[str, Any]) -> Path:
    return KNOWLEDGE_ROOT / item["metadata"]["partition_id"] / f"{item['knowledge_id']}.json"


def existing_item(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_draft(item: dict[str, Any]) -> Path:
    path = target_path_for(item)
    current = existing_item(path)
    if current and deep_get(current, ("review", "review_status")) != "draft":
        raise ValueError(f"Refusing to overwrite non-draft knowledge item: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def load_candidates() -> list[dict[str, Any]]:
    candidates = []
    for path in sorted(CANDIDATE_ROOT.glob("**/*.json")):
        candidates.append(json.loads(path.read_text(encoding="utf-8-sig")))
    return candidates


def main() -> int:
    converted: list[Path] = []
    skipped: list[str] = []

    for candidate in load_candidates():
        try:
            item = candidate_to_knowledge(candidate)
        except CandidateRejected as exc:
            skipped.append(str(exc))
            continue
        converted.append(write_draft(item))

    for path in converted:
        print(f"draft: {path}")
    if skipped:
        print("skipped:")
        for reason in skipped:
            print(f"- {reason}")
    print(f"converted {len(converted)} candidates to draft knowledge items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
