"""Apply Phase 37 Backtest B10/B11/B12 supplemental reaudit result."""

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
TASK_ID = "CEK-TA-421"
AUDIT_RESULT_ID = "audit_result_phase37_backtest_reviewed_blocked_supplemental_reaudit_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_backtest_reviewed_blocked_supplemental_reaudit_package_20260611"
PARTITION_ID = "KB_04_BACKTEST"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION_ID, start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_backtest_reviewed_blocked_supplemental_import_report.json", start_file=__file__
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_root() -> Path:
    return resolve_repo_path(start_file=__file__)


def rel(path: Path) -> str:
    return path.relative_to(repo_root()).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    return [item.strip() for item in as_list(value) if isinstance(item, str) and item.strip()]


def dedupe_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not isinstance(value, str):
            continue
        text = value.strip()
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (str(source.get("source_url") or source.get("url") or ""), str(source.get("source_title") or source.get("title") or ""))


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    results = audit.get("candidate_results")
    if not isinstance(results, list) or len(results) != 3:
        raise ValueError("audit result must contain 3 candidate_results.")
    counts = Counter(str(result.get("decision")) for result in results)
    if counts.get("accepted_for_reviewed_caveat_only", 0) != 1 or counts.get("needs_more_evidence", 0) != 2:
        raise ValueError(f"unexpected decision counts: {dict(counts)}")
    for result in results:
        cid = result.get("candidate_id")
        if result.get("approved_allowed") is not False:
            raise ValueError(f"{cid}: approved_allowed must be false")
        if result.get("default_guidance_allowed") is not False:
            raise ValueError(f"{cid}: default_guidance_allowed must be false")
        if result.get("hard_gate_allowed") is not False:
            raise ValueError(f"{cid}: hard_gate_allowed must be false")
        if result.get("decision") == "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not True:
            raise ValueError(f"{cid}: reviewed_allowed must be true for accepted item")
        if result.get("decision") != "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not False:
            raise ValueError(f"{cid}: reviewed_allowed must be false for non-accepted item")
    return results


def normalize_patch_notes(result: dict[str, Any]) -> dict[str, list[str]]:
    groups = {"source": [], "content": [], "boundary": [], "conflict": []}
    raw = result.get("patch_notes")
    if isinstance(raw, dict):
        for key in groups:
            groups[key] = string_list(raw.get(key))
    elif isinstance(raw, list):
        groups["content"] = string_list(raw)
    return groups


def flatten_patch_notes(groups: dict[str, list[str]]) -> list[str]:
    return [f"{key}: {note}" for key in ("source", "content", "boundary", "conflict") for note in groups.get(key, [])]


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    seen = {source_key(source) for source in sources}
    return [source for source in sources if not (source_key(source) in seen and False)]


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_{index:03d}"),
        "title": str(source.get("source_title") or source.get("title") or f"source_{index}"),
        "url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type") or "reviewed_reference"),
        "publisher": source.get("publisher") or "unknown",
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium_high"),
        "summary": str(source.get("evidence_summary") or ""),
        "supports": ["claim_statement", "applicability_boundary", "caveat_only_boundary"],
    }


def build_formal(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    target = deep_get(candidate, ("workflow", "conversion_target"), {})
    knowledge_id = str(target.get("proposed_knowledge_id") or f"kb_04_backtest.{candidate['research_task_id']}.v1")
    classification = candidate.get("classification", {})
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    sources = merge_sources(candidate)
    patch_groups = normalize_patch_notes(result)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(claim.get("title") or knowledge_id),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "backtest"),
            "subdomain": classification.get("subdomain"),
            "rule_type": classification.get("rule_type", "backtest_reliability_boundary_rule"),
            "claim_type": classification.get("claim_type", "methodological_constraint"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification.get("tree_node_id", "kt.trading_engineering.backtest"),
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Backtest"),
            "canonical_node_id": classification.get("canonical_node_id", "kt.trading_engineering.backtest"),
            "canonical_tree_path": "CEK-TA / Trading Engineering / Backtest",
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": "Phase 37 Backtest formal reviewed/caveat_only；只约束指标解释边界，不是 approved/default guidance。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market"),
            "asset": applicability.get("asset"),
            "timeframe": applicability.get("timeframe"),
            "data_granularity": applicability.get("data_granularity"),
            "project_type": applicability.get("project_type"),
            "applies_when": applicability.get("applies_when", []),
            "not_applicable_when": dedupe_strings(
                as_list(applicability.get("not_applicable_when"))
                + [
                    "需要买卖点、仓位、杠杆、止损止盈参数或实盘执行建议时，本知识不得使用。",
                    "需要自动 hard gate 时，应由 Risk Management / Live Execution owner 定义。",
                ]
            ),
        },
        "content": {
            "statement": claim.get("statement"),
            "rationale": claim.get("interpretation_notes"),
            "normalized_claim": claim.get("normalized_claim"),
            "claim_strength": "reviewed_caveat_only",
            "performance_claim": False,
            "reviewed_patch_notes": patch_groups,
            "audit_reason": result.get("reasons", []),
        },
        "assumptions": applicability.get("assumptions", []),
        "limitations": dedupe_strings(
            as_list(applicability.get("limitations"))
            + [
                "reviewed/caveat_only 不等于 approved，也不允许进入默认指导队列。",
                "profit factor、drawdown、return/drawdown 类指标不得单独证明策略质量。",
                "教育/券商 glossary 只能作为 supporting source，不得单独作为 reviewed 主来源。",
            ]
        ),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_refs": sources,
        "source_quality": {
            **candidate.get("source_quality", {}),
            "reviewed_blocked_supplemental_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_confidence": result.get("confidence"),
            "supporting_source_boundary": "TitanFX or similar broker/education glossary is supporting only.",
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": candidate.get("conflict_audit", {}).get("checked_against", []),
            "conflicts": [],
            "resolution_summary": "B10 supplemental reaudit passed as reviewed/caveat_only; full formal KB conflict check remains required before any future approved/default guidance governance.",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "patch_notes": patch_groups.get("conflict", []),
        },
        "review": {
            "review_status": "reviewed",
            "reviewed_at": TODAY,
            "reviewed_by": "codex_with_external_ai_reaudit",
            "confidence": result.get("confidence"),
            "freshness": candidate.get("review", {}).get("freshness", "stable"),
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": SOURCE_PACKAGE_ID,
                "decision": result.get("decision"),
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "reasons": result.get("reasons", []),
                "patch_notes": patch_groups,
            },
            "open_questions": result.get("required_followups", []),
        },
        "llm_usage_policy": {
            "allowed": candidate.get("llm_usage_policy", {}).get("allowed", []),
            "not_allowed": dedupe_strings(
                candidate.get("llm_usage_policy", {}).get("not_allowed", [])
                + [
                    "不得作为默认指导。",
                    "不得作为 approved 知识。",
                    "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                    "不得启用 hard gate 或自动风控动作。",
                ]
            ),
            "requires_context": ["样本窗口、交易次数、成本、尾部亏损、gross/net 口径和参数选择过程。"],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": "reviewed/caveat_only only; approved/default guidance/hard gate are disabled.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "contribution": {
            "source_type": "phase37_candidate_to_reviewed",
            "source_candidate_id": candidate.get("candidate_id"),
            "audit_result_id": AUDIT_RESULT_ID,
            "private_data_removed": True,
        },
    }


def update_candidate(candidate: dict[str, Any], result: dict[str, Any], formal_path: Path | None) -> dict[str, Any]:
    decision = str(result.get("decision"))
    status = candidate.setdefault("status", {})
    workflow = candidate.setdefault("workflow", {})
    review = candidate.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log = [item for item in audit_log if not (isinstance(item, dict) and item.get("audit_result_id") == AUDIT_RESULT_ID)]
    review["audit_log"] = audit_log
    patch_groups = normalize_patch_notes(result)

    review["reviewed_blocked_supplemental_reaudit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": decision,
        "reviewed_allowed": result.get("reviewed_allowed"),
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": patch_groups,
    }
    workflow["reviewed_blocked_supplemental_audit_result_id"] = AUDIT_RESULT_ID
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    status["updated_at"] = TODAY

    if decision == "accepted_for_reviewed_caveat_only" and formal_path is not None:
        status["review_status"] = "reviewed"
        status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
        status["decision_reason"] = "B10 补证再审允许 formal reviewed/caveat_only；不允许 approved/default/hard gate。"
        workflow["stage"] = "formalized_reviewed"
        workflow["queue_group"] = "formalized"
        workflow["next_action"] = "none"
        workflow["formal_review_status"] = "reviewed"
        workflow["formal_knowledge_id"] = formal_path.stem
        workflow["formal_knowledge_path"] = rel(formal_path)
        workflow["formalization_allowed"] = True
    else:
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        status["decision_reason"] = "补证再审仍要求内联完整 contract/schema extract，暂不能 formal reviewed/caveat_only。"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "inline_contract_schema_extract_and_export_reaudit_package"
        workflow["formal_review_status"] = None
        workflow["formal_knowledge_id"] = None
        workflow["formalization_allowed"] = False

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_reaudit",
            "action": "phase37_backtest_reviewed_blocked_supplemental_reaudit_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": AUDIT_RESULT_ID,
            "patch_notes": flatten_patch_notes(patch_groups),
        }
    )
    return candidate


def main() -> None:
    audit = read_json(AUDIT_RESULT_PATH)
    results = validate_audit(audit)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    promoted: list[dict[str, str]] = []
    needs_more: list[dict[str, Any]] = []
    for result in results:
        cid = str(result["candidate_id"])
        candidate_path = CANDIDATE_DIR / f"{cid}.json"
        if not candidate_path.exists():
            raise FileNotFoundError(candidate_path)
        candidate = read_json(candidate_path)
        formal_path: Path | None = None
        if result.get("decision") == "accepted_for_reviewed_caveat_only":
            formal = build_formal(candidate, result)
            formal_path = KNOWLEDGE_DIR / sanitize_filename(str(formal["knowledge_id"]))
            write_json(formal_path, formal)
            promoted.append(
                {
                    "candidate_id": cid,
                    "research_task_id": str(result.get("research_task_id")),
                    "knowledge_id": str(formal["knowledge_id"]),
                    "formal_path": rel(formal_path),
                }
            )
        else:
            needs_more.append(
                {
                    "candidate_id": cid,
                    "research_task_id": str(result.get("research_task_id")),
                    "required_followups": result.get("required_followups", []),
                }
            )
        write_json(candidate_path, update_candidate(candidate, result, formal_path))

    report = {
        "report_id": "phase37_backtest_reviewed_blocked_supplemental_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "decision_counts": dict(Counter(str(item.get("decision")) for item in results)),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "next_step": "为 B11/B12 内联完整 contract/schema extract 并导出下一轮再审包；Backtest 全量运行时验证需等 B11/B12 完成。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
