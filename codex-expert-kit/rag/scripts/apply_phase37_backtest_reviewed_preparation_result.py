"""Apply Phase 37 Backtest reviewed-preparation audit result.

This task consumes the strict reviewed/caveat_only preparation audit for the
12 Phase 37 Backtest candidates. It creates formal reviewed/caveat_only
knowledge only for entries explicitly allowed by the audit. It never creates
approved knowledge, default guidance, hard gates, or trading execution advice.
"""

from __future__ import annotations

import json
import re
import shutil
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
TASK_ID = "CEK-TA-418"
AUDIT_RESULT_ID = "audit_result_phase37_backtest_reviewed_preparation_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_backtest_reviewed_preparation_audit_package_20260611"
PARTITION_ID = "KB_04_BACKTEST"
EXPECTED_TOTAL = 12
EXPECTED_PROMOTED = 9
EXPECTED_NEEDS_MORE = 3

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION_ID, start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_backtest_reviewed_preparation_import_report.json", start_file=__file__
)


SUPPLEMENTAL_SOURCES: dict[str, list[dict[str, Any]]] = {
    "P37-E-B01": [
        {
            "source_id": "src_reviewed_databricks_point_in_time_feature_joins",
            "source_title": "Point-in-time feature joins",
            "source_url": "https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series",
            "source_type": "platform_doc",
            "publisher": "Databricks",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "medium_high",
            "relevance": "high",
            "evidence_summary": "支撑 available_time / label-time 可见性边界，避免使用 observation time 之后才可得的特征。",
            "quoted_excerpt_allowed": False,
        }
    ],
    "P37-E-B03": [
        {
            "source_id": "src_reviewed_cfa_backtesting_survivorship",
            "source_title": "Backtesting & Simulation",
            "source_url": "https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation",
            "source_type": "professional_body_reference",
            "publisher": "CFA Institute",
            "published_at": "2026-01-01",
            "accessed_at": TODAY,
            "version": "2026 refresher reading",
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "支持 backtesting 中 survivorship/look-ahead 等偏差风险需要审计。",
            "quoted_excerpt_allowed": False,
        }
    ],
}


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


def archive_audit_result(source_path: Path) -> dict[str, Any]:
    payload = read_json(source_path)
    if payload.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {payload.get('audit_result_id')}")
    if payload.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {payload.get('package_id')}")
    if source_path.resolve() != AUDIT_RESULT_ARCHIVE_PATH.resolve():
        AUDIT_RESULT_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, AUDIT_RESULT_ARCHIVE_PATH)
    else:
        write_json(AUDIT_RESULT_ARCHIVE_PATH, payload)
    return payload


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase37_backtest_*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            candidates[task_id] = (path, candidate)
    return candidates


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    results = audit.get("candidate_results")
    if not isinstance(results, list):
        raise ValueError("audit result must contain candidate_results list.")
    if len(results) != EXPECTED_TOTAL:
        raise ValueError(f"expected {EXPECTED_TOTAL} results, got {len(results)}")
    counts = Counter(str(item.get("decision")) for item in results)
    if counts.get("accepted_for_reviewed_caveat_only", 0) != EXPECTED_PROMOTED:
        raise ValueError(f"expected {EXPECTED_PROMOTED} promoted, got {counts}")
    if counts.get("needs_more_evidence", 0) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {counts}")
    for result in results:
        decision = result.get("decision")
        cid = result.get("candidate_id")
        if decision == "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not True:
            raise ValueError(f"{cid}: reviewed_allowed must be true for promoted item.")
        if decision != "accepted_for_reviewed_caveat_only" and result.get("reviewed_allowed") is not False:
            raise ValueError(f"{cid}: reviewed_allowed must be false for non-promoted item.")
        if result.get("approved_allowed") is not False:
            raise ValueError(f"{cid}: approved_allowed must be false.")
        if result.get("default_guidance_allowed") is not False:
            raise ValueError(f"{cid}: default_guidance_allowed must be false.")
        if result.get("hard_gate_allowed") is not False:
            raise ValueError(f"{cid}: hard_gate_allowed must be false.")
    return results


def validate_candidate_for_reviewed(candidate: dict[str, Any]) -> str | None:
    if deep_get(candidate, ("status", "ingestion_decision")) != "accepted_for_draft":
        return "candidate_not_accepted_for_draft"
    if deep_get(candidate, ("workflow", "queue_group")) != "ai_passed":
        return "candidate_not_in_ai_passed_queue"
    if deep_get(candidate, ("workflow", "approved_allowed")) is not False:
        return "candidate_approved_boundary_not_false"
    if deep_get(candidate, ("workflow", "default_guidance_allowed")) is not False:
        return "candidate_default_guidance_boundary_not_false"
    if deep_get(candidate, ("workflow", "hard_gate_allowed")) is not False:
        return "candidate_hard_gate_boundary_not_false"
    if not deep_get(candidate, ("workflow", "conversion_target", "proposed_knowledge_id")):
        return "candidate_missing_proposed_knowledge_id"
    if len(as_list(candidate.get("source_refs"))) < 3:
        return "candidate_less_than_3_sources"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {
        "none",
        "resolved",
        "none_known_in_visible_context",
        "visible_context_no_conflict",
    }:
        return "candidate_conflict_status_not_safe"
    return None


def normalize_source(source: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id") or f"src_audit_extra_{index:03d}"),
        "source_title": str(source.get("source_title") or source.get("title") or f"source_{index}"),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type") or "reviewed_preparation_reference"),
        "publisher": source.get("publisher") or "unknown",
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium_high"),
        "evidence_summary": str(source.get("evidence_summary") or source.get("purpose") or ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    sources = [source for source in as_list(candidate.get("source_refs")) if isinstance(source, dict)]
    seen = {source_key(source) for source in sources}
    for index, source in enumerate(SUPPLEMENTAL_SOURCES.get(str(candidate.get("research_task_id")), []), start=1):
        normalized = normalize_source(source, index)
        if source_key(normalized) not in seen:
            sources.append(normalized)
            seen.add(source_key(normalized))
    return sources


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    normalized = normalize_source(source, index)
    return {
        "source_id": normalized["source_id"],
        "title": normalized["source_title"],
        "url": normalized["source_url"],
        "source_type": normalized["source_type"],
        "publisher": normalized["publisher"],
        "published_at": normalized["published_at"],
        "accessed_at": normalized["accessed_at"],
        "version": normalized["version"],
        "reliability": normalized["reliability"],
        "relevance": normalized["relevance"],
        "summary": normalized["evidence_summary"],
        "supports": ["claim_statement", "applicability_boundary", "non_default_guidance_boundary"],
    }


def result_patch_groups(result: dict[str, Any]) -> dict[str, list[str]]:
    raw = result.get("patch_notes")
    groups = {"source": [], "content": [], "boundary": [], "conflict": []}
    if isinstance(raw, dict):
        for key in groups:
            groups[key] = string_list(raw.get(key))
    elif isinstance(raw, list):
        groups["content"] = string_list(raw)
    return groups


def build_formal_knowledge(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    target = deep_get(candidate, ("workflow", "conversion_target"), {})
    knowledge_id = str(target.get("proposed_knowledge_id") or f"kb_backtest.{deep_get(candidate, ('claim', 'normalized_claim'), candidate['research_task_id'])}")
    sources = merge_sources(candidate)
    patch_groups = result_patch_groups(result)
    claim = candidate.get("claim", {})
    applicability = candidate.get("applicability", {})
    classification = candidate.get("classification", {})
    machine_gate_reason = (
        "reviewed/caveat_only only; approved/default guidance/hard gate are disabled. "
        "Backtest knowledge only constrains evidence reliability and may not produce trade instructions."
    )
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
            "classification_notes": "Phase 37 Backtest formal reviewed/caveat_only；只约束回测可信度、偏差、成本、验证和复现边界，不是 approved/default guidance。",
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
                    "需要自动拒单、自动停机或 hard gate 时，应由 Risk Management / Live Execution owner 定义。",
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
                "平台文档只作为实现语义示例，外接项目必须映射自己的 backtest engine、数据供应商、broker 和交易所契约。",
            ]
        ),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_refs": sources,
        "source_quality": {
            **candidate.get("source_quality", {}),
            "reviewed_preparation_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_confidence": result.get("confidence"),
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": candidate.get("conflict_audit", {}).get("checked_against", []),
            "conflicts": candidate.get("conflict_audit", {}).get("conflicts", []),
            "resolution_summary": "reviewed/caveat_only preparation audit passed; full formal KB conflict check remains required before any future approved/default guidance governance.",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "patch_notes": patch_groups.get("conflict", []),
        },
        "review": {
            "review_status": "reviewed",
            "reviewed_at": TODAY,
            "reviewed_by": "codex_with_external_ai_audit",
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
            "requires_context": ["外接项目的 backtest engine、数据版本、成本模型、fill model、样本划分和评估时间。"],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": machine_gate_reason,
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
    audit_log = [
        item
        for item in audit_log
        if not (isinstance(item, dict) and item.get("audit_result_id") == AUDIT_RESULT_ID)
    ]
    review["audit_log"] = audit_log

    status["updated_at"] = TODAY
    review["reviewed_preparation_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": decision,
        "reviewed_allowed": result.get("reviewed_allowed"),
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "required_followups": result.get("required_followups", []),
        "patch_notes": result_patch_groups(result),
    }
    workflow["reviewed_preparation_audit_result_id"] = AUDIT_RESULT_ID
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False

    if decision == "accepted_for_reviewed_caveat_only" and formal_path is not None:
        status["review_status"] = "reviewed"
        status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
        status["decision_reason"] = "reviewed-preparation 审计允许 formal reviewed/caveat_only；不允许 approved/default/hard gate。"
        workflow["stage"] = "formalized_reviewed"
        workflow["queue_group"] = "formalized"
        workflow["next_action"] = "none"
        workflow["formal_review_status"] = "reviewed"
        workflow["formal_knowledge_id"] = formal_path.stem
        workflow["formal_knowledge_path"] = rel(formal_path)
        workflow["formalization_allowed"] = True
    elif decision == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        status["decision_reason"] = "reviewed-preparation 审计要求补证，暂不能 formal reviewed/caveat_only。"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["next_action"] = "supplement_sources_and_export_reaudit_package"
        workflow["formal_review_status"] = None
        workflow["formal_knowledge_id"] = None
        workflow["formalization_allowed"] = False
    else:
        status["review_status"] = "blocked"
        status["ingestion_decision"] = "blocked"
        workflow["stage"] = "blocked"
        workflow["queue_group"] = "pending"
        workflow["next_action"] = "manual_review"
        workflow["formalization_allowed"] = False

    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_audit",
            "action": "phase37_backtest_reviewed_preparation_imported",
            "reason": f"{decision} / confidence={result.get('confidence')}",
            "audit_result_id": AUDIT_RESULT_ID,
        }
    )
    return candidate


def main() -> None:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit = archive_audit_result(source_path)
    results = validate_audit(audit)
    candidates = load_candidates()
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

    promoted: list[dict[str, Any]] = []
    needs_more: list[dict[str, Any]] = []
    failures: list[str] = []
    for result in results:
        task_id = str(result.get("research_task_id"))
        candidate_record = candidates.get(task_id)
        if candidate_record is None:
            failures.append(f"{task_id}: candidate not found")
            continue
        candidate_path, candidate = candidate_record
        formal_path: Path | None = None
        if result.get("decision") == "accepted_for_reviewed_caveat_only":
            validation_error = validate_candidate_for_reviewed(candidate)
            if validation_error:
                failures.append(f"{task_id}: {validation_error}")
                continue
            formal = build_formal_knowledge(candidate, result)
            formal_path = KNOWLEDGE_DIR / sanitize_filename(str(formal["knowledge_id"]))
            write_json(formal_path, formal)
            promoted.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "knowledge_id": formal["knowledge_id"],
                    "formal_path": rel(formal_path),
                }
            )
        elif result.get("decision") == "needs_more_evidence":
            needs_more.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "required_followups": result.get("required_followups", []),
                }
            )
        updated_candidate = update_candidate(candidate, result, formal_path)
        write_json(candidate_path, updated_candidate)

    if failures:
        raise SystemExit(json.dumps({"failures": failures}, ensure_ascii=False, indent=2))

    report = {
        "report_id": "phase37_backtest_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_path": str(source_path),
        "archive_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
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
        "next_step": "为 B10/B11/B12 补证并导出再审包；9 条 formal reviewed/caveat_only 需重建索引并做运行时联动验证。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
