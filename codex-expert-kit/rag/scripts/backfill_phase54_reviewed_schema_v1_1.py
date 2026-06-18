"""Backfill historical formal knowledge governance fields for schema v1.1."""

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


KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase54_reviewed_schema_backfill_report.json", start_file=__file__)

CLAIM_TYPES = {
    "methodological_constraint",
    "risk_boundary_rule",
    "execution_safety_rule",
    "data_quality_rule",
    "backtest_validity_rule",
    "rag_governance_rule",
    "mcp_contract_rule",
    "knowledge_governance_rule",
    "project_integration_rule",
    "llm_training_rule",
    "llm_eval_rule",
    "training_data_schema_rule",
    "ai_security_rule",
    "ai_governance_rule",
    "llmops_release_rule",
}
FALLBACK_VALUES = {"deny", "ask_for_context", "cite_with_caveat"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return payload


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def infer_claim_type(item: dict[str, Any]) -> str:
    metadata = item.setdefault("metadata", {})
    raw = metadata.get("claim_type")
    if raw in CLAIM_TYPES:
        return str(raw)

    partition = str(metadata.get("partition_id", "")).upper()
    domain = str(metadata.get("domain", "")).lower()
    canonical = str(metadata.get("canonical_node_id", "")).lower()
    subdomain = str(metadata.get("subdomain", "")).lower()
    text = " ".join([partition, domain, canonical, subdomain, str(raw or "")]).lower()

    if "ai_security" in text or "threat" in text or "sbom" in text or "supply_chain" in text:
        return "ai_security_rule"
    if "release" in text or "llmops" in text or "model_release" in text:
        return "llmops_release_rule"
    if "ai_governance" in text or "governance" in text or "memory" in text:
        return "ai_governance_rule"
    if "rag" in text:
        return "rag_governance_rule"
    if "mcp" in text:
        return "mcp_contract_rule"
    if "llm_training" in text or "training" in text or "sft" in text:
        return "llm_training_rule"
    if "eval" in text or "evaluation" in text:
        return "llm_eval_rule"
    if "dataset" in text or "feature" in text or "label" in text:
        if "ai" in partition or "training" in text:
            return "training_data_schema_rule"
        return "data_quality_rule"
    if "data" in text or "storage" in text or "database" in text or "clock" in text or "timestamp" in text:
        return "data_quality_rule"
    if "backtest" in text:
        return "backtest_validity_rule"
    if "execution" in text or "order" in text or "replay" in text or "simulation" in text or "tca" in text:
        return "execution_safety_rule"
    if "risk" in text or "margin" in text or "collateral" in text or "stress" in text:
        return "risk_boundary_rule"
    if "project" in text or "integration" in text:
        return "project_integration_rule"
    if "knowledge" in text:
        return "knowledge_governance_rule"
    return "methodological_constraint"


def ensure_list(value: Any) -> list[str]:
    if isinstance(value, list):
        result = [entry for entry in value if isinstance(entry, str) and entry.strip()]
        return result
    if isinstance(value, str) and value.strip():
        return [value]
    return []


def normalize_recommended_extra_sources(value: Any) -> tuple[list[dict[str, Any]], bool]:
    changed = False
    if value is None:
        return [], True
    if not isinstance(value, list):
        return [], True

    normalized: list[dict[str, Any]] = []
    for index, entry in enumerate(value):
        if isinstance(entry, str):
            normalized.append(
                {
                    "source_id": f"recommended_extra_source_{index + 1}",
                    "title": entry,
                    "status": "proposed",
                    "notes": "Phase 54 normalized string recommendation to object form.",
                }
            )
            changed = True
            continue
        if not isinstance(entry, dict):
            changed = True
            continue
        source = dict(entry)
        if source.get("status") not in {"proposed", "rejected"}:
            source["status"] = "proposed"
            changed = True
        if not source.get("source_id"):
            source["source_id"] = f"recommended_extra_source_{index + 1}"
            changed = True
        if not source.get("title"):
            source["title"] = source.get("source_title") or source.get("url") or "recommended extra source"
            changed = True
        normalized.append(source)
    return normalized, changed


def backfill_item(path: Path, item: dict[str, Any], checked_at: str) -> dict[str, Any] | None:
    knowledge_id = str(item.get("knowledge_id", path.stem))
    review = item.setdefault("review", {})
    if not isinstance(review, dict):
        return {
            "knowledge_id": knowledge_id,
            "source_path": rel(path),
            "reason": "review_not_object",
        }

    metadata = item.setdefault("metadata", {})
    if not isinstance(metadata, dict):
        return {
            "knowledge_id": knowledge_id,
            "source_path": rel(path),
            "reason": "metadata_not_object",
        }

    changed = False
    fields_added: list[str] = []
    fields_normalized: list[str] = []
    before_gate = dict(item.get("machine_gate") or {}) if isinstance(item.get("machine_gate"), dict) else {}
    review_status_before = review.get("review_status")

    if item.get("schema_version") != "1.1.0":
        item["schema_version"] = "1.1.0"
        changed = True
        fields_normalized.append("schema_version")

    claim_type = infer_claim_type(item)
    if metadata.get("claim_type") != claim_type:
        if "claim_type" in metadata:
            fields_normalized.append("metadata.claim_type")
        else:
            fields_added.append("metadata.claim_type")
        metadata["claim_type"] = claim_type
        changed = True

    if not isinstance(metadata.get("classification_notes"), str) or not metadata.get("classification_notes", "").strip():
        metadata["classification_notes"] = (
            "Phase 54 schema v1.1 回填：保留原知识分类语义；本条仅作为 reviewed/caveat_only 或 approved 治理字段规范化，不改变 claim、来源或适用边界。"
        )
        changed = True
        fields_added.append("metadata.classification_notes")

    policy = item.setdefault("llm_usage_policy", {})
    if not isinstance(policy, dict):
        policy = {}
        item["llm_usage_policy"] = policy
        changed = True
        fields_normalized.append("llm_usage_policy")
    if not ensure_list(policy.get("allowed")):
        policy["allowed"] = [
            "用于 AI IDE 和 RAG 检索时提供带来源、边界和 caveat 的专业知识上下文。"
        ]
        changed = True
        fields_added.append("llm_usage_policy.allowed")
    if not ensure_list(policy.get("not_allowed")):
        policy["not_allowed"] = [
            "不得据此生成买卖点、仓位、杠杆、止损止盈、实盘执行建议、法律结论或风险阈值。",
            "不得把 reviewed/caveat_only 当作 approved、default guidance 或 hard gate。"
        ]
        changed = True
        fields_added.append("llm_usage_policy.not_allowed")
    if not ensure_list(policy.get("required_context")):
        policy["required_context"] = [
            "必须同时返回 source_evidence、applicability、not_applicable_when、review_status、conflict_status 和 machine_gate。",
            "若外接项目问题涉及实盘、法律、授权、资金或风控动作，必须要求项目事实层或人工 owner 复核。"
        ]
        changed = True
        fields_added.append("llm_usage_policy.required_context")
    if policy.get("fallback_behavior") not in FALLBACK_VALUES:
        policy["fallback_behavior"] = "cite_with_caveat"
        changed = True
        fields_normalized.append("llm_usage_policy.fallback_behavior")

    gate = item.setdefault("machine_gate", {})
    if not isinstance(gate, dict):
        gate = {}
        item["machine_gate"] = gate
        changed = True
        fields_normalized.append("machine_gate")
    review_status = review.get("review_status")
    if gate.get("default_guidance") not in {"allow", "caveat_only", "deny"}:
        gate["default_guidance"] = "allow" if review_status == "approved" else "caveat_only"
        changed = True
        fields_added.append("machine_gate.default_guidance")
    if review_status == "reviewed" and gate.get("default_guidance") != "caveat_only":
        gate["default_guidance"] = "caveat_only"
        changed = True
        fields_normalized.append("machine_gate.default_guidance")
    if not isinstance(gate.get("reason"), str) or not gate.get("reason"):
        gate["reason"] = "Phase 54 schema v1.1 backfill: reviewed knowledge remains caveat_only unless separately approved."
        changed = True
        fields_added.append("machine_gate.reason")
    if not isinstance(gate.get("requires_human_escalation"), bool):
        gate["requires_human_escalation"] = review_status != "approved"
        changed = True
        fields_added.append("machine_gate.requires_human_escalation")
    if not isinstance(gate.get("blocking_reasons"), list):
        gate["blocking_reasons"] = []
        changed = True
        fields_added.append("machine_gate.blocking_reasons")
    if not isinstance(gate.get("checked_at"), str) or not gate.get("checked_at"):
        gate["checked_at"] = checked_at
        changed = True
        fields_added.append("machine_gate.checked_at")
    if gate.get("gate_version") != "1.0.0":
        gate["gate_version"] = "1.0.0"
        changed = True
        fields_added.append("machine_gate.gate_version")

    for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed"):
        if review_status == "reviewed" and review.get(field) is not False:
            review[field] = False
            changed = True
            fields_normalized.append(f"review.{field}")
        if review_status == "reviewed" and gate.get(field) is not False:
            gate[field] = False
            changed = True
            fields_normalized.append(f"machine_gate.{field}")

    extras, extras_changed = normalize_recommended_extra_sources(item.get("recommended_extra_sources"))
    if extras_changed:
        item["recommended_extra_sources"] = extras
        changed = True
        fields_normalized.append("recommended_extra_sources")

    if not changed:
        return None

    path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "knowledge_id": knowledge_id,
        "source_path": rel(path),
        "fields_added": fields_added,
        "fields_normalized": fields_normalized,
        "review_status_before": review_status_before,
        "machine_gate_before": before_gate,
        "machine_gate_after": gate,
    }


def main() -> int:
    checked_at = utc_now()
    updated: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    unsafe: list[dict[str, Any]] = []
    scanned = 0

    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        scanned += 1
        item = load_json(path)
        review = item.get("review") if isinstance(item.get("review"), dict) else {}
        review_status = review.get("review_status") if isinstance(review, dict) else None
        if review_status not in {"reviewed", "approved"}:
            skipped.append({"path": rel(path), "reason": "not_reviewed_or_approved", "review_status": review_status})
            continue
        before_review = dict(review)
        result = backfill_item(path, item, checked_at)
        if result is None:
            continue
        if result.get("reason"):
            unsafe.append(result)
            continue
        after = load_json(path)
        after_review = after.get("review", {}) if isinstance(after.get("review"), dict) else {}
        if before_review.get("review_status") != after_review.get("review_status"):
            unsafe.append({**result, "reason": "review_status_changed"})
            continue
        if before_review.get("review_status") == "reviewed" and (
            after_review.get("approved_allowed") is True
            or after_review.get("default_guidance_allowed") is True
            or after_review.get("hard_gate_allowed") is True
        ):
            unsafe.append({**result, "reason": "reviewed_permission_enabled"})
            continue
        updated.append(result)

    report = {
        "report_id": "phase54_reviewed_schema_backfill_report",
        "generated_at": checked_at,
        "task_id": "CEK-TA-529",
        "scanned_count": scanned,
        "updated_count": len(updated),
        "skipped_count": len(skipped),
        "unsafe_count": len(unsafe),
        "updated_items": updated,
        "unsafe_items": unsafe,
        "skipped_sample": skipped[:100],
        "boundary": {
            "claim_content_changed": False,
            "source_evidence_changed": False,
            "approved_upgrade_allowed": False,
            "default_guidance_enable_allowed": False,
            "hard_gate_enable_allowed": False,
        },
        "status": "pass" if not unsafe else "fail",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("scanned_count", "updated_count", "unsafe_count", "status")}, ensure_ascii=False, indent=2))
    return 0 if not unsafe else 1


if __name__ == "__main__":
    raise SystemExit(main())
