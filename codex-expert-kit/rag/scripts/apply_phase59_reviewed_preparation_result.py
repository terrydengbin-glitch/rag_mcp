"""Apply Phase 59 reviewed/caveat_only audit result.

This script converts the three Phase 59 candidates that passed reviewed
preparation audit into formal reviewed/caveat_only knowledge items. It never
creates approved, default-guidance, hard-gate, DDL, migration, or trading
execution guidance.
"""

from __future__ import annotations

import copy
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 17).isoformat()
TASK_ID = "CEK-TA-570"
AUDIT_RESULT_ID = "audit_result_phase59_reviewed_preparation_20260617_strict_v1"
PACKAGE_ID = "phase59_reviewed_preparation_audit_package_20260617"

ROOT = resolve_repo_path(start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", "audit_result_phase59_reviewed_preparation_20260617_strict_v1.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase59_reviewed_preparation_import_report.json", start_file=__file__
)


TARGETS: dict[str, dict[str, Any]] = {
    "P59-MFS-001": {
        "candidate_path": resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "candidates",
            "KB_03_MARKET_MICROSTRUCTURE",
            "cand_20260617_phase59_kline_microstructure_store_separation_001.json",
            start_file=__file__,
        ),
        "knowledge_id": "kb_phase59_market_microstructure.kline_microstructure_store_separation_required.v1",
        "knowledge_path": resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "knowledge",
            "KB_03_MARKET_MICROSTRUCTURE",
            "kb_phase59_market_microstructure.kline_microstructure_store_separation_required.v1.json",
            start_file=__file__,
        ),
        "confidence": "medium_high",
        "required_fields": [
            "kline_snapshot_ref",
            "micro_snapshot_ref",
            "micro_event_store_ref",
            "data_vendor",
            "venue",
            "instrument",
            "event_time",
            "receive_time",
            "retention_policy",
            "audit_trace_id",
        ],
        "additional_sources": [
            {
                "source_id": "src_p59_binance_futures_websocket_market_streams",
                "source_title": "Websocket Market Streams",
                "source_url": "https://developers.binance.com/docs/derivatives/usds-margined-futures/websocket-market-streams",
                "source_type": "official_doc",
                "publisher": "Binance",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium_high",
                "evidence_summary": "Binance documents separate futures market data websocket streams, supporting venue-specific market data stream modeling rather than one universal wide table.",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_p59_databento_schemas_and_formats",
                "source_title": "Schemas and data formats",
                "source_url": "https://databento.com/docs/schemas-and-data-formats",
                "source_type": "official_doc",
                "publisher": "Databento",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium_high",
                "evidence_summary": "Databento documents market data schemas and formats, supporting vendor-specific event schema mapping for market data stores.",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_p59_coinapi_market_data_rest_api",
                "source_title": "Market Data REST API",
                "source_url": "https://docs.coinapi.io/market-data/rest-api",
                "source_type": "official_doc",
                "publisher": "CoinAPI",
                "accessed_at": TODAY,
                "reliability": "medium_high",
                "relevance": "medium",
                "evidence_summary": "CoinAPI market data documentation supports using vendor-specific market data contracts for candles, trades, order books, or related market data resources.",
                "quoted_excerpt_allowed": False,
            },
        ],
    },
    "P59-MFS-002": {
        "candidate_path": resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "candidates",
            "KB_AI_26_DATABASE_STORAGE",
            "cand_20260617_phase59_hybrid_training_dataset_snapshot_manifest_001.json",
            start_file=__file__,
        ),
        "knowledge_id": "kb_phase59_database_storage.hybrid_training_dataset_snapshot_manifest_required.v1",
        "knowledge_path": resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "knowledge",
            "KB_AI_26_DATABASE_STORAGE",
            "kb_phase59_database_storage.hybrid_training_dataset_snapshot_manifest_required.v1.json",
            start_file=__file__,
        ),
        "confidence": "high",
        "required_fields": [
            "prediction_time",
            "kline_snapshot_ref",
            "micro_snapshot_ref",
            "micro_feature_ref",
            "feature_schema_hash",
            "feature_materialization_version",
            "feature_generation_code_hash",
            "label_policy_version",
            "label_known_at",
            "split_manifest_ref",
            "dataset_hash",
            "join_tolerance_policy",
            "feature_ttl_policy",
            "audit_trace_id",
        ],
        "sample_chain": [
            "prediction_time",
            "kline_snapshot_ref",
            "micro_snapshot_ref",
            "micro_feature_ref",
            "feature_schema_hash",
            "label_policy_version",
            "label_known_at",
            "split_manifest_ref",
            "dataset_hash",
            "audit_trace_id",
        ],
        "additional_sources": [
            {
                "source_id": "src_p59_databricks_point_in_time_feature_joins",
                "source_title": "Point-in-time feature joins",
                "source_url": "https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series",
                "source_type": "official_doc",
                "publisher": "Databricks",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium_high",
                "evidence_summary": "Databricks documents point-in-time feature joins for training data that reflects feature values available at the label observation time.",
                "quoted_excerpt_allowed": False,
            }
        ],
    },
    "P59-MFS-003": {
        "candidate_path": resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "candidates",
            "KB_AI_26_DATABASE_STORAGE",
            "cand_20260617_phase59_canonical_registry_not_per_trader_db_001.json",
            start_file=__file__,
        ),
        "knowledge_id": "kb_phase59_database_storage.canonical_registry_not_per_trader_db_required.v1",
        "knowledge_path": resolve_repo_path(
            "codex-expert-kit",
            "rag",
            "knowledge",
            "KB_AI_26_DATABASE_STORAGE",
            "kb_phase59_database_storage.canonical_registry_not_per_trader_db_required.v1.json",
            start_file=__file__,
        ),
        "confidence": "medium_high",
        "required_fields": [
            "canonical_registry_id",
            "audit_trace_id",
            "unit_id",
            "unit_version",
            "tenant_isolation_policy",
            "cross_database_lineage_reconciliation",
            "global_audit_trace_policy",
            "rollback_policy",
        ],
        "additional_sources": [
            {
                "source_id": "src_p59_feast_registry",
                "source_title": "Registry",
                "source_url": "https://docs.feast.dev/getting-started/components/registry",
                "source_type": "official_doc",
                "publisher": "Feast",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium_high",
                "evidence_summary": "Feast documents a registry as a source of truth for feature definitions and metadata, supporting a central metadata registry pattern.",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_p59_openlineage_object_model",
                "source_title": "OpenLineage object model",
                "source_url": "https://openlineage.io/docs/spec/object-model/",
                "source_type": "official_doc",
                "publisher": "OpenLineage",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium_high",
                "evidence_summary": "OpenLineage object model supports job, run and dataset lineage metadata, relevant to cross-store lineage reconciliation.",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_p59_azure_sql_saas_tenancy_patterns",
                "source_title": "SaaS tenancy app design patterns",
                "source_url": "https://learn.microsoft.com/en-us/azure/azure-sql/database/saas-tenancy-app-design-patterns?view=azuresql",
                "source_type": "official_doc",
                "publisher": "Microsoft Azure",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium_high",
                "evidence_summary": "Azure SQL documents multitenant SaaS design patterns, supporting tenant isolation as an explicit architecture choice rather than a default per-trader database split.",
                "quoted_excerpt_allowed": False,
            },
            {
                "source_id": "src_p59_aws_saas_bridge_model",
                "source_title": "The bridge model",
                "source_url": "https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/the-bridge-model.html",
                "source_type": "official_doc",
                "publisher": "AWS",
                "accessed_at": TODAY,
                "reliability": "high",
                "relevance": "medium",
                "evidence_summary": "AWS documents bridge-style SaaS tenant isolation, supporting hybrid isolation choices when compliance, scale, or operations require physical separation.",
                "quoted_excerpt_allowed": False,
            },
        ],
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": str(source.get("source_id", "")),
        "source_title": str(source.get("source_title") or source.get("title") or ""),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": str(source.get("source_type", "other")),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability", "medium")),
        "relevance": str(source.get("relevance", "medium")),
        "evidence_summary": str(source.get("evidence_summary", "")),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def unique_sources(candidate: dict[str, Any], additional_sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source in as_list(candidate.get("source_refs")) + additional_sources:
        if not isinstance(source, dict):
            continue
        evidence = source_to_evidence(source)
        source_id = evidence["source_id"]
        if source_id and source_id not in seen:
            seen.add(source_id)
            sources.append(evidence)
    return sources


def shape_source_quality(candidate: dict[str, Any], evidence: list[dict[str, Any]]) -> dict[str, Any]:
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    high_count = sum(1 for source in evidence if source.get("reliability") in {"high", "medium_high"})
    return {
        "overall_reliability": raw.get("overall_reliability", "medium_high"),
        "score": raw.get("score", 82),
        "primary_source_count": max(int(raw.get("primary_source_count") or 0), high_count),
        "source_count": len(evidence),
        "limitations": as_list(raw.get("limitations")),
        "source_quality_notes": [
            "Reviewed/caveat_only: sources support architecture and contract boundaries, not database mandates, trading advice, or model-performance claims.",
            "Official technology and vendor documents are implementation-pattern evidence and must not be treated as mandatory CEK-TA dependencies.",
        ],
    }


def build_metadata(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    return {
        "partition_id": classification.get("partition_id"),
        "domain": classification.get("domain"),
        "subdomain": classification.get("subdomain"),
        "rule_type": classification.get("rule_type"),
        "claim_type": classification.get("claim_type", "methodological_constraint"),
        "content_type": "json",
        "project_binding": "none",
        "classification_notes": classification.get("classification_notes"),
        "tree_node_id": classification.get("tree_node_id"),
        "tree_path": classification.get("tree_path"),
        "canonical_node_id": classification.get("canonical_node_id") or classification.get("tree_node_id"),
        "canonical_tree_path": classification.get("tree_path"),
        "risk_level": "medium_high",
        "used_for": as_list(classification.get("used_for")),
        "related_nodes": as_list(classification.get("related_nodes")),
        "source_candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "phase": "Phase 59",
        "formalization_task_id": TASK_ID,
        "review_mode": "reviewed_caveat_only",
    }


def build_applicability(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    return {
        "market": raw.get("market", "general"),
        "asset": raw.get("asset", "general"),
        "timeframe": raw.get("timeframe", "general"),
        "data_granularity": raw.get("data_granularity", "general"),
        "project_type": raw.get("project_type", "trading_ai_support_layer"),
        "applies_when": as_list(raw.get("applies_when")),
        "not_applicable_when": as_list(raw.get("not_applicable_when")),
    }


def build_content(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    ai_audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}
    patch_notes = ai_audit.get("patch_notes") if isinstance(ai_audit.get("patch_notes"), dict) else {}
    required_fields = as_list(target.get("required_fields"))
    content = {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary") or "",
        "procedure": [
            "Confirm the request is about storage, feature-store, dataset manifest, registry, lineage, or audit-ledger boundaries.",
            "Return source evidence, reviewed status, machine gate, applicability, and non-applicability boundaries with the answer.",
            "Route trading signal, position, leverage, stop-loss, take-profit, live execution, or risk-threshold requests to the proper Trading Engineering owner.",
            "Treat this item as reviewed/caveat_only and never as approved default guidance or a hard gate.",
        ],
        "examples": [],
        "anti_patterns": [
            "Treating a wide analytical export as the canonical raw/high-frequency store.",
            "Using vector DB, cache, notebook outputs, or log fragments as the canonical registry or audit ledger.",
            "Reading dataset readiness, dataset_hash, or feature availability as model quality, launch permission, or trading permission.",
            "Turning this reviewed/caveat_only item into DDL, migration, database vendor mandate, trade execution advice, default guidance, or hard gate.",
        ],
        "validation": [
            "source_evidence is non-empty and official/internal contract sources are present.",
            "review.review_status is reviewed and machine_gate.default_guidance is caveat_only.",
            "approved_allowed, default_guidance_allowed, hard_gate_allowed, trade_execution_advice_allowed, and ddl_or_migration_allowed are all false.",
            "MCP/SearchLab/KnowledgeTree can retrieve the item from formal knowledge index after rebuild.",
        ],
        "risk_notes": as_list(applicability.get("limitations"))
        + as_list(patch_notes.get("boundary"))
        + [
            "Reviewed/caveat_only only; not approved and not default guidance.",
            "This item does not create a database, execute a migration, mandate a vendor, or provide trading execution advice.",
        ],
        "citation_notes": claim.get("evidence_summary", ""),
        "required_fields_or_contract": required_fields,
        "sample_chain": as_list(target.get("sample_chain")),
        "audit_patch_notes": {
            "source_patch_notes": as_list(patch_notes.get("source")),
            "content_patch_notes": as_list(patch_notes.get("content")),
            "boundary_patch_notes": as_list(patch_notes.get("boundary")),
            "conflict_patch_notes": as_list(patch_notes.get("conflict")),
        },
    }
    return content


def build_formal(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    evidence = unique_sources(candidate, as_list(target.get("additional_sources")))
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    ai_audit = review.get("ai_audit") if isinstance(review.get("ai_audit"), dict) else {}
    reviewed_audit = {
        "audit_result_id": AUDIT_RESULT_ID,
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": target.get("confidence", "medium_high"),
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "trade_execution_advice_allowed": False,
        "ddl_or_migration_allowed": False,
        "upstream_candidate_audit_result_id": ai_audit.get("audit_result_id"),
    }
    formal = {
        "schema_version": "1.1.0",
        "knowledge_id": target["knowledge_id"],
        "title": deep_get(candidate, ("claim", "title"), target["knowledge_id"]),
        "metadata": build_metadata(candidate, target),
        "applicability": build_applicability(candidate),
        "content": build_content(candidate, target),
        "assumptions": as_list(deep_get(candidate, ("applicability", "assumptions"), [])),
        "source_evidence": evidence,
        "source_quality": shape_source_quality(candidate, evidence),
        "conflict_audit": copy.deepcopy(candidate.get("conflict_audit", {})),
        "review": {
            "review_status": "reviewed",
            "confidence": target.get("confidence", "medium_high"),
            "freshness": deep_get(candidate, ("review", "freshness"), "mixed"),
            "reviewer": "external_ai_strict_audit_and_codex_backwrite",
            "reviewed_at": TODAY,
            "source_candidate_id": candidate.get("candidate_id"),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "approval_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "open_questions": as_list(deep_get(candidate, ("review", "open_questions"), [])),
            "ai_audit": reviewed_audit,
            "audit_log": as_list(deep_get(candidate, ("review", "audit_log"), []))
            + [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "action": "phase59_reviewed_preparation_audit_passed",
                    "reason": "accepted_for_reviewed_caveat_only; approved/default/hard gate remain forbidden.",
                    "audit_result_id": AUDIT_RESULT_ID,
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "formal_reviewed_caveat_only_created",
                    "reason": f"{TASK_ID} materialized formal reviewed/caveat_only knowledge.",
                },
            ],
        },
        "llm_usage_policy": copy.deepcopy(candidate.get("llm_usage_policy", {})),
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": "Formal reviewed/caveat_only only; not approved, not default guidance, not hard gate.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "ddl_or_migration_allowed": False,
            "database_selection_mandate_allowed": False,
        },
        "contract_refs": copy.deepcopy(candidate.get("contract_refs", [])),
        "workflow": {
            "source_candidate_id": candidate.get("candidate_id"),
            "source_candidate_path": rel(target["candidate_path"]),
            "formalized_by_task_id": TASK_ID,
            "formalized_at": TODAY,
            "review_mode": "reviewed_caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "contribution": copy.deepcopy(candidate.get("contribution", {})),
    }
    formal["conflict_audit"].update(
        {
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    formal["contribution"].update(
        {
            "formalized_from_candidate": candidate.get("candidate_id"),
            "private_data_removed": True,
            "contains_project_private_strategy": False,
            "contains_secret": False,
            "contains_account_facts": False,
        }
    )
    return formal


def update_candidate(candidate: dict[str, Any], target: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(candidate)
    status = candidate.setdefault("status", {})
    status["review_status"] = "formalized"
    status["ingestion_decision"] = "formal_reviewed_created"
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "current_task_id": TASK_ID,
            "next_action": "runtime_linkage_validation",
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "formalization_allowed": True,
            "formal_knowledge_id": target["knowledge_id"],
            "formal_knowledge_path": rel(target["knowledge_path"]),
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    conversion_target = workflow.setdefault("conversion_target", {})
    conversion_target.update(
        {
            "proposed_knowledge_id": target["knowledge_id"],
            "target_review_status": "reviewed_caveat_only",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    review = candidate.setdefault("review", {})
    review.setdefault("audit_log", [])
    review["audit_log"].append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "formal_reviewed_caveat_only_created",
            "reason": f"{TASK_ID} created formal reviewed/caveat_only knowledge.",
            "audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": target["knowledge_id"],
        }
    )
    review["ai_audit"] = {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": target.get("confidence", "medium_high"),
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "trade_execution_advice_allowed": False,
        "ddl_or_migration_allowed": False,
        "audit_result_id": AUDIT_RESULT_ID,
        "formal_knowledge_id": target["knowledge_id"],
    }
    return candidate


def write_audit_result(targets: dict[str, dict[str, Any]]) -> None:
    candidate_results = []
    for task_id, target in targets.items():
        candidate = read_json(target["candidate_path"])
        candidate_results.append(
            {
                "candidate_id": candidate.get("candidate_id"),
                "research_task_id": task_id,
                "decision": "accepted_for_reviewed_caveat_only",
                "confidence": target.get("confidence", "medium_high"),
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "trade_execution_advice_allowed": False,
                "ddl_or_migration_allowed": False,
                "formal_knowledge_id": target["knowledge_id"],
                "required_followups": [
                    "Keep reviewed/caveat_only boundaries.",
                    "Do not create approved, default guidance, hard gate, DDL, migration, database mandate, or trading advice.",
                ],
            }
        )
    payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "audited_at": TODAY,
        "summary": {
            "total": len(candidate_results),
            "accepted_for_reviewed_caveat_only": len(candidate_results),
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_caveat_only_maximum": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "ddl_or_migration_allowed": False,
            "database_selection_mandate_allowed": False,
        },
        "candidate_results": candidate_results,
    }
    write_json(AUDIT_RESULT_PATH, payload)


def main() -> None:
    created: list[str] = []
    touched_candidates: list[str] = []
    write_audit_result(TARGETS)
    for task_id, target in TARGETS.items():
        candidate = read_json(target["candidate_path"])
        if candidate.get("research_task_id") != task_id:
            raise ValueError(f"{target['candidate_path']} has unexpected research_task_id")
        formal = build_formal(candidate, target)
        write_json(target["knowledge_path"], formal)
        updated_candidate = update_candidate(candidate, target)
        write_json(target["candidate_path"], updated_candidate)
        created.append(rel(target["knowledge_path"]))
        touched_candidates.append(rel(target["candidate_path"]))

    report = {
        "schema_version": "phase59_reviewed_preparation_import_report.v1",
        "task_id": TASK_ID,
        "generated_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "created_formal_knowledge_count": len(created),
        "created_formal_knowledge": created,
        "touched_candidates": touched_candidates,
        "boundary": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "ddl_or_migration_allowed": False,
            "database_selection_mandate_allowed": False,
        },
        "next_action": "Rebuild formal knowledge index, Vue fixtures, and run JSON/UTF-8/runtime-linkage checks.",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
