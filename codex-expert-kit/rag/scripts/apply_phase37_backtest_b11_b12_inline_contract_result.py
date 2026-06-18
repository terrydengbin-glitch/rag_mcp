"""Apply Phase 37 Backtest B11/B12 inline-contract reaudit result."""

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
TASK_ID = "CEK-TA-423"
PARTITION_ID = "KB_04_BACKTEST"
AUDIT_RESULT_ID = "audit_result_phase37_backtest_b11_b12_inline_contract_reaudit_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_backtest_b11_b12_inline_contract_reaudit_package_20260611"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", PARTITION_ID, start_file=__file__)
KNOWLEDGE_DIR = resolve_repo_path("codex-expert-kit", "rag", "knowledge", PARTITION_ID, start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
SCHEMA_EXTRACT_PATH = resolve_repo_path(
    "docs", "contracts", "phase37_backtest_run_manifest_schema_extract.json", start_file=__file__
)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_backtest_b11_b12_inline_contract_import_report.json", start_file=__file__
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


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def validate_audit(audit: dict[str, Any]) -> list[dict[str, Any]]:
    if audit.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {audit.get('audit_result_id')}")
    if audit.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {audit.get('package_id')}")
    results = audit.get("candidate_results")
    if not isinstance(results, list) or len(results) != 2:
        raise ValueError("audit result must contain 2 candidate_results.")
    counts = Counter(str(item.get("decision")) for item in results)
    if counts.get("accepted_for_reviewed_caveat_only", 0) != 2:
        raise ValueError(f"unexpected decision counts: {dict(counts)}")
    for result in results:
        cid = result.get("candidate_id")
        if result.get("reviewed_allowed") is not True:
            raise ValueError(f"{cid}: reviewed_allowed must be true")
        for key in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
            if result.get(key) is not False:
                raise ValueError(f"{cid}: {key} must be false")
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


def source_key(source: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(source.get("source_id") or ""),
        str(source.get("source_url") or source.get("url") or ""),
        str(source.get("source_title") or source.get("title") or ""),
    )


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for source in as_list(candidate.get("source_refs")):
        if not isinstance(source, dict):
            continue
        key = source_key(source)
        if key not in seen:
            seen.add(key)
            result.append(source)
    return result


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


def build_content_statement(candidate: dict[str, Any], task_id: str, patch_groups: dict[str, list[str]]) -> dict[str, Any]:
    claim = candidate.get("claim", {}) if isinstance(candidate.get("claim"), dict) else {}
    content = {
        "statement": claim.get("statement"),
        "rationale": claim.get("evidence_summary") or claim.get("interpretation_notes"),
        "normalized_claim": claim.get("normalized_claim"),
        "claim_strength": "reviewed_caveat_only",
        "performance_claim": False,
        "reviewed_patch_notes": patch_groups,
    }
    if task_id == "P37-E-B11":
        content["required_contract_fields"] = [
            "code_repository",
            "code_commit",
            "dependency_lockfile_hash",
            "container_image_digest",
            "random_seed",
            "config_file_hash",
            "input_artifact_ids",
            "output_artifact_ids",
            "log_artifact_id",
            "metric_report_id",
            "lineage_id",
            "replay_command_or_ci_job_id",
            "known_non_determinism",
        ]
        content["materialization_notes"] = [
            "known_non_determinism 必须保留，用于解释非确定性运行差异。",
            "MLflow/DVC 只是实现模式示例，字段本体以 CEK-TA schema extract 为准。",
        ]
    else:
        content["required_contract_fields"] = [
            "strategy_rule_version",
            "parameter_hash",
            "dataset_version",
            "calendar_version",
            "session_template_version",
            "cost_model_version",
            "fee_model_version",
            "slippage_model_version",
            "fill_model_version",
            "evaluation_timestamp",
        ]
        content["materialization_notes"] = [
            "evaluation_timestamp 在本 formal item 中声明为 run_identity.created_at 的 alias；如外接项目另设 audit_trace.evaluation_timestamp，必须保持同一语义。",
            "Backtest 只记录、绑定和审计一致性，不接管 Strategy/Data/Microstructure/Replay/Execution owner 本体规则。",
        ]
    return content


def build_formal(candidate: dict[str, Any], result: dict[str, Any], schema_extract: dict[str, Any]) -> dict[str, Any]:
    task_id = str(result.get("research_task_id"))
    target = deep_get(candidate, ("workflow", "conversion_target"), {})
    knowledge_id = str(target.get("proposed_knowledge_id") or f"kb_04_backtest.{task_id.lower()}.v1")
    classification = candidate.get("classification", {}) if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability", {}) if isinstance(candidate.get("applicability"), dict) else {}
    sources = merge_sources(candidate)
    patch_groups = normalize_patch_notes(result)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": str(deep_get(candidate, ("claim", "title"), knowledge_id)),
        "metadata": {
            "partition_id": PARTITION_ID,
            "domain": classification.get("domain", "backtest"),
            "subdomain": classification.get("subdomain", "reproducibility_and_versioning"),
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
            "research_task_id": task_id,
            "phase": "Phase 37",
            "classification_notes": "Phase 37 Backtest formal reviewed/caveat_only；只约束回测证据包、复现和版本绑定边界，不是 approved/default guidance。",
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
                    "需要自动 hard gate 或实盘许可时，应由 Risk Management / Live Execution owner 定义。",
                ]
            ),
        },
        "content": build_content_statement(candidate, task_id, patch_groups),
        "contract_binding": {
            "contract_path": "docs/contracts/phase37_backtest_run_manifest_contract.md",
            "schema_extract_path": rel(SCHEMA_EXTRACT_PATH),
            "schema_extract_id": schema_extract.get("schema_extract_id"),
            "contract_sha256": schema_extract.get("contract_sha256"),
            "cross_owner_mapping": schema_extract.get("cross_owner_mapping", {}),
        },
        "assumptions": applicability.get("assumptions", []),
        "limitations": dedupe_strings(
            as_list(applicability.get("limitations"))
            + [
                "reviewed/caveat_only 不等于 approved，也不允许进入默认指导队列。",
                "本知识不证明策略盈利能力、稳健性或实盘资格。",
                "MLflow、DVC、QuantConnect 只能作为实现语义示例，不是 CEK-TA 或外接项目强制工具依赖。",
            ]
        ),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_refs": sources,
        "source_quality": {
            **(candidate.get("source_quality", {}) if isinstance(candidate.get("source_quality"), dict) else {}),
            "inline_contract_audit_result_id": AUDIT_RESULT_ID,
            "reviewed_preparation_confidence": result.get("confidence"),
            "internal_contract_source": "CEK-TA backtest_run_manifest schema extract is the primary source for CEK-TA exact fields.",
            "tool_doc_boundary": "MLflow/DVC/QuantConnect are implementation-pattern/supporting sources only.",
        },
        "conflict_audit": {
            "conflict_status": "none_known_in_visible_context",
            "checked_against": deep_get(candidate, ("conflict_audit", "checked_against"), []),
            "conflicts": [],
            "resolution_summary": "Inline contract reaudit passed as reviewed/caveat_only; complete formal KB conflict and duplicate check remains required before any future approved/default governance.",
            "approval_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "owner_mapping_boundary": schema_extract.get("cross_owner_mapping", {}),
            "patch_notes": patch_groups.get("conflict", []),
        },
        "review": {
            "review_status": "reviewed",
            "reviewed_at": TODAY,
            "reviewed_by": "codex_with_external_ai_reaudit",
            "confidence": result.get("confidence"),
            "freshness": deep_get(candidate, ("review", "freshness"), "stable"),
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
            "allowed": deep_get(candidate, ("llm_usage_policy", "allowed"), []),
            "not_allowed": dedupe_strings(
                as_list(deep_get(candidate, ("llm_usage_policy", "not_allowed"), []))
                + [
                    "不得作为默认指导。",
                    "不得作为 approved 知识。",
                    "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                    "不得启用 hard gate 或自动风控动作。",
                ]
            ),
            "requires_context": [
                "backtest_run_manifest",
                "strategy_identity",
                "data_identity",
                "market_calendar_identity",
                "execution_assumption_identity",
                "reproducibility_package",
            ],
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


def update_candidate(candidate: dict[str, Any], result: dict[str, Any], formal_path: Path) -> dict[str, Any]:
    patch_groups = normalize_patch_notes(result)
    status = candidate.setdefault("status", {})
    workflow = candidate.setdefault("workflow", {})
    review = candidate.setdefault("review", {})
    audit_log = review.setdefault("audit_log", [])
    if not isinstance(audit_log, list):
        audit_log = []
        review["audit_log"] = audit_log
    audit_log = [item for item in audit_log if not (isinstance(item, dict) and item.get("audit_result_id") == AUDIT_RESULT_ID)]
    review["audit_log"] = audit_log
    review["inline_contract_reaudit_result"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": SOURCE_PACKAGE_ID,
        "decision": result.get("decision"),
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "reasons": result.get("reasons", []),
        "patch_notes": patch_groups,
    }
    status["review_status"] = "reviewed"
    status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
    status["decision_reason"] = "内联契约再审允许 formal reviewed/caveat_only；不允许 approved/default/hard gate。"
    status["updated_at"] = TODAY
    workflow["stage"] = "formalized_reviewed"
    workflow["queue_group"] = "formalized"
    workflow["current_task_id"] = TASK_ID
    workflow["next_action"] = "none"
    workflow["formalization_allowed"] = True
    workflow["formal_review_status"] = "reviewed"
    workflow["formal_knowledge_id"] = formal_path.stem
    workflow["formal_knowledge_path"] = rel(formal_path)
    workflow["inline_contract_reaudit_result_id"] = AUDIT_RESULT_ID
    workflow["approved_allowed"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    audit_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_strict_reaudit",
            "action": "phase37_backtest_b11_b12_inline_contract_reaudit_imported",
            "reason": f"{result.get('decision')} / confidence={result.get('confidence')}",
            "audit_result_id": AUDIT_RESULT_ID,
            "patch_notes": flatten_patch_notes(patch_groups),
        }
    )
    return candidate


def main() -> int:
    audit = read_json(AUDIT_RESULT_PATH)
    results = validate_audit(audit)
    schema_extract = read_json(SCHEMA_EXTRACT_PATH)
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    promoted: list[dict[str, str]] = []
    for result in results:
        cid = str(result["candidate_id"])
        candidate_path = CANDIDATE_DIR / f"{cid}.json"
        if not candidate_path.exists():
            raise FileNotFoundError(candidate_path)
        candidate = read_json(candidate_path)
        formal = build_formal(candidate, result, schema_extract)
        formal_path = KNOWLEDGE_DIR / sanitize_filename(str(formal["knowledge_id"]))
        write_json(formal_path, formal)
        write_json(candidate_path, update_candidate(candidate, result, formal_path))
        promoted.append(
            {
                "candidate_id": cid,
                "research_task_id": str(result.get("research_task_id")),
                "knowledge_id": str(formal["knowledge_id"]),
                "formal_path": rel(formal_path),
            }
        )
    report = {
        "report_id": "phase37_backtest_b11_b12_inline_contract_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "decision_counts": dict(Counter(str(item.get("decision")) for item in results)),
        "promoted_count": len(promoted),
        "promoted": promoted,
        "hard_boundaries": {
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "next_step": "执行 CEK-TA-419 验证 Backtest 在 MCP/SearchLab/KnowledgeTree/Vue3 的联动命中、引用和阻断。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
