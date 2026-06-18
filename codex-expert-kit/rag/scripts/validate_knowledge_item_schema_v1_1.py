"""Validate CEK-TA formal knowledge items against schema v1.1 gates."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase34_schema_v1_1_validation_report.json", start_file=__file__)

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
GATE_VALUES = {"allow", "caveat_only", "deny"}
FALLBACK_VALUES = {"deny", "ask_for_context", "cite_with_caveat"}


def deep_get(item: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = item
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def validate_item(item: dict[str, Any], rel_path: str) -> list[str]:
    errors: list[str] = []
    if item.get("schema_version") != "1.1.0":
        errors.append("schema_version_not_1_1_0")
    claim_type = deep_get(item, "metadata.claim_type")
    if claim_type not in CLAIM_TYPES:
        errors.append("metadata.claim_type_invalid_or_missing")
    notes = deep_get(item, "metadata.classification_notes")
    if not isinstance(notes, str) or not notes.strip():
        errors.append("metadata.classification_notes_missing")

    policy = item.get("llm_usage_policy")
    if not isinstance(policy, dict):
        errors.append("llm_usage_policy_missing")
    else:
        for field in ("allowed", "not_allowed", "required_context"):
            value = policy.get(field)
            if not isinstance(value, list) or not value or not all(isinstance(entry, str) and entry.strip() for entry in value):
                errors.append(f"llm_usage_policy.{field}_invalid")
        if policy.get("fallback_behavior") not in FALLBACK_VALUES:
            errors.append("llm_usage_policy.fallback_behavior_invalid")

    gate = item.get("machine_gate")
    if not isinstance(gate, dict):
        errors.append("machine_gate_missing")
    else:
        if gate.get("default_guidance") not in GATE_VALUES:
            errors.append("machine_gate.default_guidance_invalid")
        if not isinstance(gate.get("reason"), str) or not gate.get("reason"):
            errors.append("machine_gate.reason_missing")
        if not isinstance(gate.get("requires_human_escalation"), bool):
            errors.append("machine_gate.requires_human_escalation_invalid")
        if not isinstance(gate.get("blocking_reasons"), list):
            errors.append("machine_gate.blocking_reasons_invalid")
        if not isinstance(gate.get("checked_at"), str) or not gate.get("checked_at"):
            errors.append("machine_gate.checked_at_missing")
        if gate.get("gate_version") != "1.0.0":
            errors.append("machine_gate.gate_version_invalid")

    review_status = deep_get(item, "review.review_status")
    default_allowed = deep_get(item, "review.default_guidance_allowed", False)
    gate_value = deep_get(item, "machine_gate.default_guidance")
    conflict_status = deep_get(item, "conflict_audit.conflict_status")
    source_count = len(item.get("source_evidence") or [])
    reliability = deep_get(item, "source_quality.overall_reliability")

    if review_status == "reviewed" and gate_value != "caveat_only":
        errors.append("reviewed_must_be_caveat_only")
    if review_status == "approved" and default_allowed is True and conflict_status in {"none", "resolved"} and source_count > 0 and reliability in {"high", "medium"}:
        if gate_value != "allow":
            errors.append("approved_default_guidance_should_allow")
    if gate_value == "allow":
        if review_status != "approved":
            errors.append("allow_requires_approved")
        if default_allowed is not True:
            errors.append("allow_requires_default_guidance_allowed_true")
        if source_count < 1:
            errors.append("allow_requires_source_evidence")
        if conflict_status not in {"none", "resolved"}:
            errors.append("allow_requires_no_blocking_conflict")
    extras = item.get("recommended_extra_sources")
    if not isinstance(extras, list):
        errors.append("recommended_extra_sources_must_be_list")
    else:
        for index, source in enumerate(extras):
            if not isinstance(source, dict):
                errors.append(f"recommended_extra_sources.{index}_not_object")
                continue
            if source.get("status") not in {"proposed", "verified", "rejected"}:
                errors.append(f"recommended_extra_sources.{index}.status_invalid")
            if source.get("status") == "verified":
                errors.append(f"recommended_extra_sources.{index}.verified_must_move_to_source_evidence")

    return [f"{rel_path}: {error}" for error in errors]


def main() -> int:
    failures: list[str] = []
    gate_counts: dict[str, int] = {}
    item_count = 0
    for path in sorted(KNOWLEDGE_ROOT.glob("**/*.json")):
        item_count += 1
        item = json.loads(path.read_text(encoding="utf-8-sig"))
        rel = path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()
        gate = deep_get(item, "machine_gate.default_guidance", "missing")
        gate_counts[gate] = gate_counts.get(gate, 0) + 1
        failures.extend(validate_item(item, rel))

    report = {
        "schema": "cek_ta_schema_v1_1_validation_report",
        "gate_status": "pass" if not failures else "fail",
        "item_count": item_count,
        "gate_counts": gate_counts,
        "failure_count": len(failures),
        "failures": failures,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
