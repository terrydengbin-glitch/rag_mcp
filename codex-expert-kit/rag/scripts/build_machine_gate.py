"""Upgrade formal knowledge items with schema v1.1 AI usage and gate fields."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
GATE_VERSION = "1.0.0"
SCHEMA_VERSION = "1.1.0"


CLAIM_TYPE_BY_DOMAIN = {
    "backtest": "backtest_validity_rule",
    "replay_simulation": "execution_safety_rule",
    "live_trading": "execution_safety_rule",
    "risk_management": "risk_boundary_rule",
    "trade_analysis": "methodological_constraint",
    "llm_training": "methodological_constraint",
    "rag_engineering": "rag_governance_rule",
    "mcp_engineering": "mcp_contract_rule",
    "project_runbooks": "project_integration_rule",
    "project_integration": "project_integration_rule",
    "knowledge_governance": "knowledge_governance_rule",
    "quant_trading": "risk_boundary_rule",
    "kline_strategy": "methodological_constraint",
}

SOURCE_ENHANCEMENTS = {
    "backtest": [
        {
            "title": "White, 2000, A Reality Check for Data Snooping",
            "source_url": None,
            "source_type": "paper",
            "purpose": "补强 data snooping、多重测试和样本外检验边界。",
            "status": "proposed",
        },
        {
            "title": "Bailey et al., The Probability of Backtest Overfitting",
            "source_url": None,
            "source_type": "paper",
            "purpose": "补强回测过拟合概率、参数搜索和模型选择风险。",
            "status": "proposed",
        },
    ],
    "kline_strategy": [
        {
            "title": "Sullivan, Timmermann, White, 1999, Data-Snooping, Technical Trading Rule Performance, and the Bootstrap",
            "source_url": None,
            "source_type": "paper",
            "purpose": "补强技术交易规则的数据窥探和 bootstrap 检验边界。",
            "status": "proposed",
        }
    ],
    "rag_engineering": [
        {
            "title": "NIST AI Risk Management Framework",
            "source_url": None,
            "source_type": "official_doc",
            "purpose": "补强 AI 系统风险治理、可追踪性和文档化边界。",
            "status": "proposed",
        }
    ],
}


def deep_get(item: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = item
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def infer_claim_type(item: dict[str, Any]) -> str:
    metadata = item.setdefault("metadata", {})
    existing = metadata.get("claim_type")
    if isinstance(existing, str) and existing:
        return existing
    domain = str(metadata.get("domain") or "")
    subdomain = str(metadata.get("subdomain") or "")
    rule_type = str(metadata.get("rule_type") or "")
    if "mcp" in domain or "mcp" in subdomain:
        return "mcp_contract_rule"
    if "governance" in domain or "governance" in subdomain:
        return "knowledge_governance_rule"
    if "risk" in domain or "risk" in subdomain:
        return "risk_boundary_rule"
    if "data" in domain or "leak" in subdomain:
        return "data_quality_rule"
    if rule_type in {"adapter_rule", "schema"}:
        return "project_integration_rule"
    return CLAIM_TYPE_BY_DOMAIN.get(domain, "methodological_constraint")


def classification_notes(item: dict[str, Any]) -> str | None:
    metadata = item.setdefault("metadata", {})
    tree_node = metadata.get("tree_node_id")
    canonical_node = metadata.get("canonical_node_id") or tree_node
    tree_path = metadata.get("tree_path")
    canonical_path = metadata.get("canonical_tree_path") or tree_path
    existing = metadata.get("classification_notes")
    if isinstance(existing, str) and existing:
        return existing
    if tree_node != canonical_node or tree_path != canonical_path:
        return f"UI tree node is {tree_node}; canonical classification is {canonical_node}."
    return "UI tree node and canonical classification are aligned."


def llm_usage_policy(item: dict[str, Any]) -> dict[str, Any]:
    existing = item.get("llm_usage_policy")
    if isinstance(existing, dict) and existing.get("allowed") and existing.get("not_allowed"):
        return existing
    metadata = item.get("metadata", {})
    claim_type = metadata.get("claim_type") or infer_claim_type(item)
    domain = metadata.get("domain", "general")
    tree_path = metadata.get("canonical_tree_path") or metadata.get("tree_path") or domain
    allowed = [
        f"用于审计和解释 {tree_path} 范围内的专业边界。",
        "用于提醒用户补充适用范围、来源、冲突状态和验证条件。",
        "用于阻止 AI 把未满足边界的知识当成默认交易建议。",
    ]
    not_allowed = [
        "不得据此生成买卖点、仓位、杠杆或实盘执行指令。",
        "不得在缺少适用边界、来源或冲突状态时作为默认指导。",
        "不得把 reviewed 或 caveat_only 知识表述为 approved 结论。",
    ]
    if claim_type in {"execution_safety_rule", "risk_boundary_rule"}:
        not_allowed.append("不得绕过人工风险确认或项目事实核验。")
    return {
        "allowed": allowed,
        "not_allowed": not_allowed,
        "required_context": [
            "project_type",
            "market",
            "asset",
            "timeframe",
            "data_granularity",
            "task_type",
        ],
        "fallback_behavior": "cite_with_caveat",
    }


def build_gate(item: dict[str, Any]) -> dict[str, Any]:
    review_status = deep_get(item, "review.review_status")
    default_allowed = bool(deep_get(item, "review.default_guidance_allowed", False))
    freshness = deep_get(item, "review.freshness")
    conflict_status = deep_get(item, "conflict_audit.conflict_status")
    reliability = deep_get(item, "source_quality.overall_reliability")
    private_removed = bool(deep_get(item, "contribution.private_data_removed", False))
    project_binding = deep_get(item, "metadata.project_binding", "none")
    source_count = len(item.get("source_evidence") or [])

    blocking: list[str] = []
    if source_count < 1:
        blocking.append("missing_source_evidence")
    if reliability not in {"high", "medium"}:
        blocking.append("source_reliability_not_high_or_medium")
    if conflict_status not in {"none", "resolved"}:
        blocking.append(f"conflict_status_{conflict_status}")
    if freshness == "deprecated" or review_status == "deprecated":
        blocking.append("deprecated")
    if review_status in {"draft", "rejected"}:
        blocking.append(f"review_status_{review_status}")
    if not private_removed:
        blocking.append("private_data_not_confirmed_removed")
    if project_binding not in {"none", "sanitized_project_case"}:
        blocking.append("project_binding_not_reusable")

    if not blocking and review_status == "approved" and default_allowed:
        return {
            "default_guidance": "allow",
            "reason": "approved; default_guidance_allowed=true; sources, conflict, freshness, and privacy gates passed.",
            "requires_human_escalation": False,
            "blocking_reasons": [],
            "checked_at": date.today().isoformat(),
            "gate_version": GATE_VERSION,
        }
    if not blocking and review_status == "reviewed":
        return {
            "default_guidance": "caveat_only",
            "reason": "reviewed but not approved; usable for audit/search with explicit caveat only.",
            "requires_human_escalation": True,
            "blocking_reasons": ["review_status_not_approved"],
            "checked_at": date.today().isoformat(),
            "gate_version": GATE_VERSION,
        }
    if not default_allowed and review_status == "approved":
        blocking.append("default_guidance_allowed_false")
    if review_status not in {"approved", "reviewed"} and f"review_status_{review_status}" not in blocking:
        blocking.append(f"review_status_{review_status}")
    return {
        "default_guidance": "deny",
        "reason": "Machine gate denied default guidance because one or more quality, source, conflict, review, or privacy gates failed.",
        "requires_human_escalation": True,
        "blocking_reasons": sorted(set(blocking)),
        "checked_at": date.today().isoformat(),
        "gate_version": GATE_VERSION,
    }


def recommended_extra_sources(item: dict[str, Any]) -> list[dict[str, Any]]:
    existing = item.get("recommended_extra_sources")
    if isinstance(existing, list):
        return existing
    domain = str(deep_get(item, "metadata.domain", ""))
    return SOURCE_ENHANCEMENTS.get(domain, [])


def upgrade_item(item: dict[str, Any]) -> dict[str, Any]:
    item["schema_version"] = SCHEMA_VERSION
    metadata = item.setdefault("metadata", {})
    metadata["claim_type"] = infer_claim_type(item)
    metadata["classification_notes"] = classification_notes(item)
    item["llm_usage_policy"] = llm_usage_policy(item)
    item["machine_gate"] = build_gate(item)
    item["recommended_extra_sources"] = recommended_extra_sources(item)
    return item


def main() -> int:
    paths = sorted(KNOWLEDGE_ROOT.glob("**/*.json"))
    for path in paths:
        item = json.loads(path.read_text(encoding="utf-8-sig"))
        upgraded = upgrade_item(item)
        path.write_text(json.dumps(upgraded, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"upgraded {len(paths)} knowledge items to schema {SCHEMA_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
