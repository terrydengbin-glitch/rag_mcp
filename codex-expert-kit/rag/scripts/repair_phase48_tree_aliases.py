"""Repair Phase 48 knowledge tree canonical node and alias alignment."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402
from tree_alias_contract import load_aliases  # noqa: E402


TREE_PATH = resolve_repo_path("codex-expert-kit", "rag", "knowledge_tree.md", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase48_tree_alias_repair_report.json", start_file=__file__)
PLAN_PATH = resolve_repo_path("docs", "reports", "phase48_tree_alias_repair_plan.json", start_file=__file__)


DIRECT_RENAMES = {
    "kt.llm_training": "kt.ai_engineering.llm_training",
    "kt.rag_engineering": "kt.ai_engineering.rag_engineering",
    "kt.mcp": "kt.ai_engineering.mcp_engineering",
    "kt.ai_engineering.decision_time_feature_contract": "kt.ai_engineering.decision_time_features",
    "kt.ai_engineering.shadow_paper_ope_eval": "kt.ai_engineering.shadow_paper_ope",
    "kt.ai_engineering.external_project_memory": "kt.ai_engineering.project_memory",
    "kt.ai_feedback_governance": "kt.ai_engineering.continuous_learning",
    "kt.live_execution.execution_tca": "kt.trading_engineering.execution_tca",
    "kt.live_execution.audit_trail": "kt.trading_engineering.trade_audit",
    "kt.live_execution.resilience_incident": "kt.trading_engineering.resilience_incident_log",
    "kt.live_execution.order_semantics": "kt.trading_engineering.order_semantics",
}

PARENT_FIXES = {
    "kt.trading_engineering.execution_tca": "kt.trading_engineering",
    "kt.trading_engineering.trade_audit": "kt.trading_engineering",
    "kt.trading_engineering.resilience_incident_log": "kt.trading_engineering",
    "kt.trading_engineering.order_semantics": "kt.trading_engineering",
}

PATH_FIXES = {
    "kt.trading_engineering.execution_tca": "CEK-TA / Trading Engineering / Execution TCA",
    "kt.trading_engineering.trade_audit": "CEK-TA / Trading Engineering / Trade Audit",
    "kt.trading_engineering.resilience_incident_log": "CEK-TA / Trading Engineering / Resilience Incident Log",
    "kt.trading_engineering.order_semantics": "CEK-TA / Trading Engineering / Order Semantics",
}

REQUIRED_NODE_BLOCKS = {
    "kt.ai_engineering.hybrid_scoring": """- node_id: kt.ai_engineering.hybrid_scoring
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Hybrid Scoring
  title: Hybrid Scoring
  domain: ai_engineering
  subdomain: hybrid_scoring
  level: 2
  summary: Hybrid scoring architecture for combining tabular/statistical scorers, calibration, Qwen-style audit explanation, RAG citations, and deterministic final gates without turning language models into numeric scorers.
  key_concepts: [tabular scorer, calibration, Qwen audit assistant, final gate, reason code]
  expected_knowledge_types: [architecture_rule, schema, boundary_rule, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none
  item_mapping:
    partition_id: KB_AI_ENGINEERING
    allowed_domains: [ai_engineering]
    allowed_subdomains: [hybrid_scoring, numeric_scoring, calibration_threshold, llm_audit_assistant, final_gate]
""",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def node_ids(text: str) -> set[str]:
    return set(re.findall(r"^\s*-?\s*node_id:\s*([^\s]+)\s*$", text, flags=re.MULTILINE))


def replace_identifier(text: str, source: str, target: str) -> tuple[str, int]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_.]){re.escape(source)}(?![A-Za-z0-9_.])")
    return pattern.subn(target, text)


def replace_field_in_block(text: str, node_id: str, field: str, value: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"(?P<head>-\s*node_id:\s*{re.escape(node_id)}\n(?:(?!-\s*node_id:).)*?^\s*{field}:\s*)[^\n]+",
        flags=re.MULTILINE | re.DOTALL,
    )
    return pattern.subn(rf"\g<head>{value}", text)


def append_missing_nodes(text: str) -> tuple[str, list[str]]:
    existing = node_ids(text)
    appended: list[str] = []
    if "kt.ai_engineering.hybrid_scoring" not in existing:
        marker = "- node_id: kt.ai_engineering.numeric_scoring"
        index = text.find(marker)
        block = REQUIRED_NODE_BLOCKS["kt.ai_engineering.hybrid_scoring"].rstrip() + "\n\n"
        if index >= 0:
            text = text[:index] + block + text[index:]
        else:
            text = text.rstrip() + "\n\n" + block
        appended.append("kt.ai_engineering.hybrid_scoring")
    return text, appended


def main() -> int:
    aliases = load_aliases()
    original = TREE_PATH.read_text(encoding="utf-8")
    text = original
    rename_counts: dict[str, int] = {}

    for source, target in sorted(DIRECT_RENAMES.items(), key=lambda item: len(item[0]), reverse=True):
        text, count = replace_identifier(text, source, target)
        rename_counts[f"{source}->{target}"] = count

    for source, target in sorted(aliases.items(), key=lambda item: len(item[0]), reverse=True):
        if source in DIRECT_RENAMES:
            continue
        text, count = replace_identifier(text, source, target)
        if count:
            rename_counts[f"{source}->{target}"] = count

    parent_fix_counts: dict[str, int] = {}
    for node_id, parent_id in PARENT_FIXES.items():
        text, count = replace_field_in_block(text, node_id, "parent_id", parent_id)
        parent_fix_counts[node_id] = count

    path_fix_counts: dict[str, int] = {}
    for node_id, path in PATH_FIXES.items():
        text, count = replace_field_in_block(text, node_id, "path", path)
        path_fix_counts[node_id] = count

    text, appended_nodes = append_missing_nodes(text)
    TREE_PATH.write_text(text, encoding="utf-8", newline="\n")

    after_nodes = node_ids(text)
    required_nodes = {
        "kt.ai_engineering.continuous_learning",
        "kt.ai_engineering.decision_time_features",
        "kt.ai_engineering.hybrid_scoring",
        "kt.ai_engineering.llm_training",
        "kt.ai_engineering.mcp_engineering",
        "kt.ai_engineering.project_memory",
        "kt.ai_engineering.rag_engineering",
        "kt.ai_engineering.shadow_paper_ope",
        "kt.trading_engineering.execution_tca",
        "kt.trading_engineering.order_semantics",
        "kt.trading_engineering.resilience_incident_log",
        "kt.trading_engineering.trade_audit",
    }
    missing_required = sorted(required_nodes - after_nodes)
    remaining_legacy_nodes = sorted(set(aliases) & after_nodes)

    plan = {
        "report_id": "phase48_tree_alias_repair_plan",
        "generated_at": utc_now(),
        "task_ids": ["CEK-TA-488", "CEK-TA-489"],
        "source": str(TREE_PATH),
        "alias_contract": "codex-expert-kit/rag/knowledge_tree_aliases.json",
        "rename_targets": DIRECT_RENAMES,
        "required_nodes": sorted(required_nodes),
        "boundary": {
            "knowledge_content_changed": False,
            "review_status_changed": False,
            "approved_or_default_guidance_changed": False,
        },
    }
    report = {
        "report_id": "phase48_tree_alias_repair_report",
        "generated_at": utc_now(),
        "task_ids": ["CEK-TA-488", "CEK-TA-489"],
        "summary": {
            "changed": text != original,
            "rename_count_total": sum(rename_counts.values()),
            "appended_node_count": len(appended_nodes),
            "missing_required_node_count": len(missing_required),
            "remaining_legacy_node_count": len(remaining_legacy_nodes),
        },
        "checks": {
            "rename_counts": rename_counts,
            "parent_fix_counts": parent_fix_counts,
            "path_fix_counts": path_fix_counts,
            "appended_nodes": appended_nodes,
            "missing_required_nodes": missing_required,
            "remaining_legacy_nodes": remaining_legacy_nodes,
        },
        "status": "pass" if not missing_required else "fail",
    }
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"] | {"status": report["status"]}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
