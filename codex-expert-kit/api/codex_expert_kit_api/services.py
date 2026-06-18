from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Any

from .resolver_bridge import resolve_repo_path


TREE_NODES: list[dict[str, Any]] = [
    {"id": "kt.trading_engineering", "canonical_node_id": "kt.trading_engineering", "parent_id": None, "level": 1, "title": "Trading Engineering", "subtitle": "交易工程", "summary": "交易工程主枝，覆盖量化基础、数据工程、策略工程、回测、回放模拟、实盘执行、风险管理和交易分析。", "sort_order": 100},
    {"id": "kt.ai_engineering", "canonical_node_id": "kt.ai_engineering", "parent_id": None, "level": 1, "title": "AI Engineering", "subtitle": "RAG / MCP / LLM training / scoring", "summary": "AI 工程主枝，覆盖 LLM 训练、RAG 工程、MCP 工程、数值打分、校准阈值、LLM 审计助手、shadow/paper/OPE 和模型发布治理。", "sort_order": 200},
    {"id": "kt.project_support", "canonical_node_id": "kt.project_support", "parent_id": None, "level": 1, "title": "Project Support", "subtitle": "接入 / 回灌 / 治理", "summary": "项目支持主枝，覆盖外部项目接入和知识治理。", "sort_order": 300},
    {"id": "kt.trading_engineering.quant_foundation", "canonical_node_id": "kt.trading_engineering.quant_foundation", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_01 Quant Foundation", "subtitle": "EV / R:R / costs / sizing", "summary": "期望值、成本、收益风险比和仓位公式。", "sort_order": 110},
    {"id": "kt.trading_engineering.data_engineering", "canonical_node_id": "kt.trading_engineering.data_engineering", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_02 Data Engineering", "subtitle": "time alignment / data quality", "summary": "时间对齐、缺失重复、时区和数据版本。", "sort_order": 120},
    {"id": "kt.trading_engineering.strategy_engineering", "canonical_node_id": "kt.trading_engineering.strategy_engineering", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_03 Strategy Engineering", "subtitle": "K-line / indicators / microstructure", "summary": "信号、入场、出场、指标边界和微观结构。", "sort_order": 130},
    {"id": "kt.trading_engineering.backtest", "canonical_node_id": "kt.trading_engineering.backtest", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_04 Backtest", "subtitle": "bias / cost / metrics / reproducibility", "summary": "回测可信度、偏差、数据泄漏、成本模型和可复现性。", "sort_order": 140},
    {"id": "kt.trading_engineering.replay_simulation", "canonical_node_id": "kt.trading_engineering.replay_simulation", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_05 Replay and Simulation", "subtitle": "fill / slippage / latency", "summary": "回放时钟、事件重放、成交模型、滑点和延迟。", "sort_order": 150},
    {"id": "kt.trading_engineering.live_execution", "canonical_node_id": "kt.trading_engineering.live_execution", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_06 Live Execution", "subtitle": "orders / reconciliation / kill switch", "summary": "订单状态机、仓位同步、安全停机和事故处理。", "sort_order": 160},
    {"id": "kt.trading_engineering.risk_management", "canonical_node_id": "kt.trading_engineering.risk_management", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_07 Risk Management", "subtitle": "risk gates / exposure / loss limits", "summary": "风控闸门、单笔风险、组合暴露和日亏损。", "sort_order": 170},
    {"id": "kt.trading_engineering.trade_analysis", "canonical_node_id": "kt.trading_engineering.trade_analysis", "parent_id": "kt.trading_engineering", "level": 2, "title": "KB_08 Trade Analysis", "subtitle": "quality / taxonomy / R:R decomposition", "summary": "交易质量、坏例 taxonomy、R/R 分解和成本分解。", "sort_order": 180},
    {"id": "kt.ai_engineering.llm_training", "canonical_node_id": "kt.ai_engineering.llm_training", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_09 LLM Training", "subtitle": "dataset / eval / leakage control", "summary": "数据集、评测、RAG vs finetune 和泄漏控制。", "sort_order": 210},
    {"id": "kt.ai_engineering.rag_engineering", "canonical_node_id": "kt.ai_engineering.rag_engineering", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_10 RAG Engineering", "subtitle": "metadata / citation / retrieval", "summary": "metadata、chunking、检索、citation 和冲突感知检索。", "sort_order": 220},
    {"id": "kt.ai_engineering.mcp_engineering", "canonical_node_id": "kt.ai_engineering.mcp_engineering", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_11 MCP and Agent Engineering", "subtitle": "tool contract / read only / errors", "summary": "MCP tool contract、权限边界、错误结构和只读策略。", "sort_order": 230},
    {"id": "kt.ai_engineering.numeric_scoring", "canonical_node_id": "kt.ai_engineering.numeric_scoring", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_AI_20 Numeric Scoring", "subtitle": "scoring / meta-labeling / review priority", "summary": "数值 scorer、规则基线、Logistic Regression、LightGBM、XGBoost、meta-labeling 和复核优先级。", "sort_order": 240},
    {"id": "kt.ai_engineering.calibration_threshold", "canonical_node_id": "kt.ai_engineering.calibration_threshold", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_AI_21 Calibration and Threshold", "subtitle": "calibration / Brier / cost matrix", "summary": "校准集、Brier、可靠性曲线、成本矩阵、阈值策略、false allow 和 false block。", "sort_order": 250},
    {"id": "kt.ai_engineering.decision_time_feature_contract", "canonical_node_id": "kt.ai_engineering.decision_time_feature_contract", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_AI_22 Decision-Time Features", "subtitle": "feature time / leakage gate", "summary": "event_time、feature_available_time、decision_time、label_observation_end_time、特征血缘和泄漏单测。", "sort_order": 260},
    {"id": "kt.ai_engineering.llm_audit_assistant", "canonical_node_id": "kt.ai_engineering.llm_audit_assistant", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_AI_23 LLM Audit Assistant", "subtitle": "schema / reason code / citation", "summary": "LLM 审计助手的严格 JSON schema、reason code、引用回链、unsupported claim 检测和 no-hit 降级。", "sort_order": 270},
    {"id": "kt.ai_engineering.shadow_paper_ope_eval", "canonical_node_id": "kt.ai_engineering.shadow_paper_ope_eval", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_AI_24 Shadow Paper OPE", "subtitle": "offline / shadow / counterfactual", "summary": "离线评估、shadow 模式、paper/replay 评估、反事实/OPE 和人工复核精度。", "sort_order": 280},
    {"id": "kt.ai_engineering.model_release_governance", "canonical_node_id": "kt.ai_engineering.model_release_governance", "parent_id": "kt.ai_engineering", "level": 2, "title": "KB_AI_25 Model Release Governance", "subtitle": "lineage / rollback / approval", "summary": "release manifest、模型注册、dataset hash、rollback、kill switch 和 hard gate owner approval。", "sort_order": 290},
    {"id": "kt.project_integration", "canonical_node_id": "kt.project_integration", "parent_id": "kt.project_support", "level": 2, "title": "KB_12 Project Integration", "subtitle": "adapter / truth boundary / healthcheck", "summary": "外部项目 adapter、truth boundary、healthcheck 和回灌边界。", "sort_order": 310},
    {"id": "kt.knowledge_governance", "canonical_node_id": "kt.knowledge_governance", "parent_id": "kt.project_support", "level": 2, "title": "KB_13 Knowledge Governance", "subtitle": "status / source / conflict gates", "summary": "知识生命周期、来源评分、冲突阻断和人工审核。", "sort_order": 320},
    {"id": "kt.trading_engineering.backtest.bias", "canonical_node_id": "kt.trading_engineering.backtest.bias", "parent_id": "kt.trading_engineering.backtest", "level": 3, "title": "Backtest Bias", "subtitle": "lookahead / leakage / overfitting", "summary": "前视偏差、数据泄漏、幸存者偏差和过拟合。", "sort_order": 141},
    {"id": "kt.trading_engineering.replay_simulation.fill_model", "canonical_node_id": "kt.trading_engineering.replay_simulation.fill_model", "parent_id": "kt.trading_engineering.replay_simulation", "level": 3, "title": "Fill Model", "subtitle": "OHLC same bar / tick replay", "summary": "同根 K 线成交顺序、partial fill、手续费和滑点假设。", "sort_order": 151},
    {"id": "kt.ai_engineering.rag_engineering.trading_scoring_rag_pack", "canonical_node_id": "kt.ai_engineering.rag_engineering.trading_scoring_rag_pack", "parent_id": "kt.ai_engineering.rag_engineering", "level": 3, "title": "Trading AI RAG Pack", "subtitle": "active retrieval / citation / context budget", "summary": "交易 gating/scoring 项目的主动检索、引用完整率、machine gate、上下文预算和 no-hit 降级。", "sort_order": 221},
]

def aliases_path() -> Path:
    override = os.environ.get("CEK_TA_KNOWLEDGE_TREE_ALIASES_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return resolve_repo_path("codex-expert-kit", "rag", "knowledge_tree_aliases.json")


@lru_cache(maxsize=2)
def load_aliases(path: str | None = None) -> dict[str, str]:
    resolved = Path(path).resolve() if path else aliases_path()
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    aliases = payload.get("aliases", {})
    if not isinstance(aliases, dict):
        raise ValueError(f"{resolved} aliases must be an object.")
    return {str(key): str(value) for key, value in aliases.items()}


ALIASES = load_aliases()


def normalize_node_id(node_id: str | None) -> str:
    if not node_id:
        return ""
    current = node_id
    seen: set[str] = set()
    while current in ALIASES and current not in seen:
        seen.add(current)
        current = ALIASES[current]
    return current


def knowledge_tree_path() -> Path:
    override = os.environ.get("CEK_TA_KNOWLEDGE_TREE_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return resolve_repo_path("codex-expert-kit", "rag", "knowledge_tree.md")


def _parse_scalar(raw_value: str) -> Any:
    value = raw_value.strip().strip('"')
    if value == "null":
        return None
    if value.isdigit():
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"').strip("'") for part in inner.split(",")]
    return value


@lru_cache(maxsize=2)
def load_tree_nodes(path: str | None = None) -> list[dict[str, Any]]:
    resolved = Path(path).resolve() if path else knowledge_tree_path()
    nodes: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    sort_order = 0

    for line in resolved.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- node_id:") or stripped.startswith("node_id:"):
            if current:
                nodes.append(current)
            sort_order += 10
            current = {"sort_order": sort_order}
            raw_value = stripped.split("node_id:", 1)[1]
            node_id = str(_parse_scalar(raw_value))
            current["id"] = node_id
            current["node_id"] = node_id
            current["canonical_node_id"] = node_id
            continue
        if current is None or ":" not in stripped:
            continue
        field, raw_value = stripped.split(":", 1)
        if field in {
            "parent_id",
            "path",
            "title",
            "domain",
            "subdomain",
            "level",
            "summary",
            "coverage_status",
            "review_status",
            "freshness_status",
            "conflict_status",
            "related_nodes",
            "key_concepts",
            "expected_knowledge_types",
        }:
            current[field] = _parse_scalar(raw_value)

    if current:
        nodes.append(current)

    return [_normalize_tree_node(node) for node in nodes]


def _normalize_tree_node(node: dict[str, Any]) -> dict[str, Any]:
    node_id = str(node.get("node_id") or node.get("id") or "")
    key_concepts = node.get("key_concepts") if isinstance(node.get("key_concepts"), list) else []
    return {
        "id": node_id,
        "node_id": node_id,
        "canonical_node_id": node_id,
        "parent_id": node.get("parent_id"),
        "path": node.get("path", node_id),
        "title": node.get("title", node_id),
        "subtitle": " / ".join(str(item) for item in key_concepts[:3]),
        "domain": node.get("domain", "unknown"),
        "subdomain": node.get("subdomain", "unknown"),
        "level": int(node.get("level", 0) or 0),
        "summary": node.get("summary", ""),
        "coverage_status": node.get("coverage_status", "partial"),
        "review_status": node.get("review_status", "reviewed"),
        "freshness_status": node.get("freshness_status", "stable"),
        "conflict_status": node.get("conflict_status", "unchecked"),
        "related_nodes": node.get("related_nodes") if isinstance(node.get("related_nodes"), list) else [],
        "aliases": [alias for alias, target in ALIASES.items() if target == node_id],
        "sort_order": int(node.get("sort_order", 0) or 0),
    }


def _raw_node_by_id(node_id: str) -> dict[str, Any] | None:
    canonical = normalize_node_id(node_id)
    return next((node for node in load_tree_nodes() if node["id"] == canonical), None)


def _node_children(node_id: str) -> list[dict[str, Any]]:
    return [item for item in load_tree_nodes() if item.get("parent_id") == node_id]


def _node_scope(node_id: str) -> set[str]:
    node = _raw_node_by_id(node_id)
    if not node:
        return set()
    result = {node["id"]}
    queue = [node["id"]]
    while queue:
        current = queue.pop(0)
        for child in _node_children(current):
            result.add(child["id"])
            queue.append(child["id"])
    return result


def _node_in_scope(item_node: str, scope: set[str]) -> bool:
    canonical = normalize_node_id(item_node)
    return canonical in scope or any(canonical.startswith(f"{node}.") for node in scope)


def _item_review_status(item: dict[str, Any]) -> str:
    return item.get("review", {}).get("review_status", "draft")


def _candidate_node_id(candidate: dict[str, Any]) -> str:
    return normalize_node_id(candidate.get("canonical_node_id") or candidate.get("tree_node_id") or "")


def _stats_for_node(node_id: str) -> dict[str, int]:
    scope = _node_scope(node_id)
    formal = [item for item in load_index().get("items", []) if _node_in_scope(item_node_id(item), scope)]
    try:
        candidates = [item for item in load_candidates() if _node_in_scope(_candidate_node_id(item), scope)]
    except FileNotFoundError:
        candidates = []
    children = _node_children(node_id)
    return {
        "children_count": len(children),
        "knowledge_count": len(formal),
        "approved_item_count": sum(1 for item in formal if _item_review_status(item) == "approved"),
        "reviewed_item_count": sum(1 for item in formal if _item_review_status(item) == "reviewed"),
        "candidate_count": len(candidates),
        "source_count": sum(len(item.get("source_evidence", [])) for item in formal)
        + sum(int(item.get("source_count", 0) or 0) for item in candidates),
        "open_gap_count": 0,
        "conflict_count": sum(
            1
            for item in formal
            if item.get("conflict_audit", {}).get("conflict_status", "none") not in {"none", "resolved"}
        )
        + sum(1 for item in candidates if item.get("conflict_status", "none") not in {"none", "resolved"}),
    }


def tree_node_view(node: dict[str, Any]) -> dict[str, Any]:
    view = dict(node)
    view.update(_stats_for_node(node["id"]))
    return view


def tree_nodes() -> list[dict[str, Any]]:
    return [tree_node_view(node) for node in load_tree_nodes()]


TREE_NODES = load_tree_nodes()


def knowledge_items_path() -> Path:
    override = os.environ.get("CEK_TA_KNOWLEDGE_ITEMS_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json")


def candidates_path() -> Path:
    override = os.environ.get("CEK_TA_CANDIDATES_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return resolve_repo_path("codex-expert-kit", "rag", "candidates")


@lru_cache(maxsize=4)
def load_index(path: str | None = None) -> dict[str, Any]:
    resolved = Path(path).resolve() if path else knowledge_items_path()
    with resolved.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=4)
def load_candidates(path: str | None = None) -> list[dict[str, Any]]:
    resolved = Path(path).resolve() if path else candidates_path()
    if not resolved.exists():
        raise FileNotFoundError(str(resolved))
    candidates: list[dict[str, Any]] = []
    for candidate_file in sorted(resolved.rglob("*.json")):
        with candidate_file.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        candidates.append(candidate_card(raw, candidate_file))
    return candidates


def node_by_id(node_id: str) -> dict[str, Any] | None:
    node = _raw_node_by_id(node_id)
    return tree_node_view(node) if node else None


def children_for(node_id: str, include_l3: bool = False) -> list[dict[str, Any]]:
    node = _raw_node_by_id(node_id)
    if not node:
        return []
    children = _node_children(node["id"])
    if not include_l3:
        children = [item for item in children if item["level"] <= 2]
    return [tree_node_view(item) for item in sorted(children, key=lambda item: item["sort_order"])]


def descendants(node_id: str) -> set[str]:
    return _node_scope(node_id)


def item_node_id(item: dict[str, Any]) -> str:
    metadata = item.get("metadata", {})
    return normalize_node_id(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "")


def item_card(item: dict[str, Any]) -> dict[str, Any]:
    metadata = item.get("metadata", {})
    sources = item.get("source_evidence", [])
    content = item.get("content", {})
    machine_gate = item.get("machine_gate", {})
    llm_usage_policy = item.get("llm_usage_policy", {})
    return {
        "id": item.get("knowledge_id"),
        "title": item.get("title"),
        "tree_node_id": metadata.get("tree_node_id"),
        "canonical_node_id": metadata.get("canonical_node_id") or metadata.get("tree_node_id"),
        "claim_type": metadata.get("claim_type", "methodological_constraint"),
        "classification_notes": metadata.get("classification_notes", ""),
        "status": item.get("review", {}).get("review_status", "draft"),
        "source_count": len(sources),
        "conflict_status": item.get("conflict_audit", {}).get("conflict_status", "none"),
        "freshness_status": item.get("freshness", {}).get("freshness_status", "unknown"),
        "llm_usage_policy": {
            "allowed": llm_usage_policy.get("allowed", []),
            "not_allowed": llm_usage_policy.get("not_allowed", []),
            "required_context": llm_usage_policy.get("required_context", []),
            "fallback_behavior": llm_usage_policy.get("fallback_behavior", "cite_with_caveat"),
        },
        "machine_gate": {
            "default_guidance": machine_gate.get("default_guidance", "deny"),
            "reason": machine_gate.get("reason", ""),
            "requires_human_escalation": machine_gate.get("requires_human_escalation", True),
            "blocking_reasons": machine_gate.get("blocking_reasons", []),
            "checked_at": machine_gate.get("checked_at", ""),
            "gate_version": machine_gate.get("gate_version", "1.0.0"),
        },
        "recommended_extra_sources_count": len(item.get("recommended_extra_sources", [])),
        "summary": content.get("statement", ""),
        "updated_at": item.get("updated_at"),
    }


def filter_items(node_id: str, query: str = "", include_descendants: bool = True) -> list[dict[str, Any]]:
    scope = descendants(node_id) if include_descendants else {node_by_id(node_id)["id"]}  # type: ignore[index]
    q = query.lower().strip()
    items = []
    for item in load_index().get("items", []):
        canonical = item_node_id(item)
        text = json.dumps(item, ensure_ascii=False).lower()
        if canonical in scope or any(canonical.startswith(f"{node}.") for node in scope):
            if not q or q in text:
                items.append(item)
    return items


def _source_card(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source.get("source_id"),
        "title": source.get("source_title") or source.get("title"),
        "url": source.get("source_url") or source.get("url"),
        "source_type": source.get("source_type", "other"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": source.get("accessed_at"),
        "version": source.get("version"),
        "reliability": source.get("reliability", "low"),
        "score": source.get("score", 0),
        "relevance": source.get("relevance", "medium"),
        "freshness": source.get("freshness", "stable"),
        "limitations": source.get("limitations", []),
        "evidence_summary": source.get("evidence_summary", ""),
        "quoted_excerpt_allowed": source.get("quoted_excerpt_allowed", False),
    }


def _candidate_status(raw: dict[str, Any]) -> str:
    source_refs = raw.get("source_refs", [])
    conflict = raw.get("conflict_audit", {}).get("conflict_status", "unchecked")
    target_status = raw.get("conversion_target", {}).get("target_review_status")
    if not source_refs or conflict in {"confirmed", "unchecked"}:
        return "blocked"
    if target_status == "draft" and conflict in {"none", "resolved"}:
        return "candidate_ready"
    return "needs_more_evidence"


def _risk_level(candidate: dict[str, Any]) -> str:
    reliability = candidate.get("source_quality", {}).get("overall_reliability") or candidate.get("confidence", "low")
    conflict = candidate.get("conflict_status", "unchecked")
    missing = candidate.get("knowledge_preview", {}).get("missing_fields", [])
    blockers = candidate.get("knowledge_preview", {}).get("blocking_issues", [])
    if candidate.get("candidate_status") == "blocked" or conflict in {"confirmed", "unchecked"} or candidate.get("source_count", 0) == 0:
        return "risk_blocked"
    if candidate.get("candidate_status") == "needs_more_evidence" or reliability == "low" or candidate.get("source_quality_score", 0) < 0.6 or missing or blockers:
        return "risk_high"
    if conflict == "potential" or candidate.get("freshness") == "time_sensitive":
        return "risk_medium"
    return "risk_low"


def _knowledge_preview(raw: dict[str, Any]) -> dict[str, Any]:
    classification = raw.get("classification", {})
    source_refs = raw.get("source_refs", [])
    conflict = raw.get("conflict_audit", {}).get("conflict_status", "unchecked")
    conversion = raw.get("conversion_target", {})
    applicability = raw.get("applicability", {})
    missing_fields = []
    if not source_refs:
        missing_fields.append("source_refs")
    if not applicability.get("applies_when"):
        missing_fields.append("applies_when")
    if not applicability.get("not_applicable_when"):
        missing_fields.append("not_applicable_when")
    if not applicability.get("assumptions"):
        missing_fields.append("assumptions")
    blocking_issues = []
    if conflict in {"confirmed", "unchecked"}:
        blocking_issues.append(f"conflict_status:{conflict}")
    return {
        "proposed_knowledge_id": conversion.get("proposed_knowledge_id"),
        "target_review_status": conversion.get("target_review_status", "draft"),
        "domain": classification.get("domain"),
        "subdomain": classification.get("subdomain"),
        "tree_node_id": classification.get("tree_node_id"),
        "canonical_node_id": classification.get("canonical_node_id") or classification.get("tree_node_id"),
        "source_count": len(source_refs),
        "conflict_status": conflict,
        "missing_fields": missing_fields,
        "blocking_issues": blocking_issues,
    }


def candidate_card(raw: dict[str, Any], source_file: Path | None = None) -> dict[str, Any]:
    status = raw.get("status", {})
    classification = raw.get("classification", {})
    claim = raw.get("claim", {})
    applicability = raw.get("applicability", {})
    review = raw.get("review", {})
    source_refs = [_source_card(source) for source in raw.get("source_refs", [])]
    source_quality = raw.get("source_quality", {})
    conflict_audit = raw.get("conflict_audit", {})
    preview = _knowledge_preview(raw)
    candidate = {
        "candidate_id": raw.get("candidate_id"),
        "research_task_id": raw.get("research_task_id"),
        "partition_id": classification.get("partition_id"),
        "tree_node_id": classification.get("tree_node_id"),
        "tree_path": classification.get("tree_path"),
        "canonical_node_id": classification.get("canonical_node_id") or classification.get("tree_node_id"),
        "title": claim.get("statement", "")[:96],
        "claim": claim.get("statement", ""),
        "summary": claim.get("evidence_summary", ""),
        "normalized_claim": claim.get("normalized_claim"),
        "evidence_summary": claim.get("evidence_summary"),
        "interpretation_notes": claim.get("interpretation_notes"),
        "domain": classification.get("domain"),
        "subdomain": classification.get("subdomain"),
        "rule_type": classification.get("rule_type"),
        "used_for": classification.get("used_for", []),
        "source_count": len(source_refs),
        "source_quality_score": source_quality.get("score", 0),
        "source_refs": source_refs,
        "source_quality": source_quality,
        "applicable_scope": " / ".join(applicability.get("applies_when", [])),
        "not_applicable_scope": applicability.get("not_applicable_when", []),
        "applies_when": applicability.get("applies_when", []),
        "not_applicable_when": applicability.get("not_applicable_when", []),
        "assumptions": applicability.get("assumptions", []),
        "limitations": applicability.get("limitations", []),
        "conflict_status": conflict_audit.get("conflict_status", "unchecked"),
        "conflict_audit": conflict_audit,
        "confidence": review.get("confidence", "low"),
        "freshness": review.get("freshness", "stable"),
        "review_status": status.get("review_status", "proposed"),
        "ingestion_decision": status.get("ingestion_decision", "pending"),
        "decision_reason": status.get("decision_reason"),
        "reviewer": review.get("reviewer"),
        "reviewed_at": review.get("reviewed_at"),
        "open_questions": review.get("open_questions", []),
        "audit_log": review.get("audit_log", []),
        "conversion_target": raw.get("conversion_target", {}),
        "knowledge_preview": preview,
        "copyright": raw.get("copyright", {}),
        "source_path": str(source_file) if source_file else "",
        "updated_at": status.get("updated_at"),
    }
    candidate["candidate_status"] = _candidate_status(raw)
    candidate["risk_level"] = _risk_level(candidate)
    return candidate


def candidate_checklist(candidate: dict[str, Any]) -> dict[str, Any]:
    reliability = candidate.get("source_quality", {}).get("overall_reliability") or candidate.get("confidence", "low")
    conflict = candidate.get("conflict_status", "unchecked")
    missing = candidate.get("knowledge_preview", {}).get("missing_fields", [])
    blockers = candidate.get("knowledge_preview", {}).get("blocking_issues", [])
    checks = [
        {"key": "has_sources", "label": "有可追踪来源", "status": "pass" if candidate.get("source_count", 0) > 0 else "fail", "reason": f"{candidate.get('source_count', 0)} sources"},
        {"key": "source_quality", "label": "来源质量足够", "status": "pass" if reliability in {"high", "medium"} else "warning", "reason": reliability},
        {"key": "conflict_checked", "label": "冲突已审计", "status": "pass" if conflict in {"none", "resolved"} else "fail", "reason": conflict},
        {"key": "scope_defined", "label": "适用和不适用边界完整", "status": "pass" if not {"applies_when", "not_applicable_when"} & set(missing) else "fail", "reason": "scope fields"},
        {"key": "tree_classified", "label": "已归类到知识树节点", "status": "pass" if candidate.get("canonical_node_id") else "fail", "reason": candidate.get("canonical_node_id") or "missing"},
        {"key": "draft_ready", "label": "可进入 draft 交接", "status": "pass" if candidate.get("candidate_status") == "candidate_ready" and not blockers else "warning", "reason": candidate.get("candidate_status")},
    ]
    return {
        "candidate_id": candidate.get("candidate_id"),
        "can_accept_for_draft": all(item["status"] == "pass" for item in checks),
        "checks": checks,
    }


def filter_candidates(
    q: str = "",
    partition_id: str | None = None,
    tree_node_id: str | None = None,
    candidate_status: str | None = None,
    conflict_status: str | None = None,
    risk_level: str | None = None,
) -> list[dict[str, Any]]:
    text_query = q.strip().lower()
    requested_node = normalize_node_id(tree_node_id)
    requested_scope = _node_scope(requested_node) if requested_node and _raw_node_by_id(requested_node) else {requested_node}
    result = []
    for candidate in load_candidates():
        haystack = json.dumps(candidate, ensure_ascii=False).lower()
        if text_query and text_query not in haystack:
            continue
        if partition_id and candidate.get("partition_id") != partition_id:
            continue
        candidate_tree_node = normalize_node_id(candidate.get("tree_node_id"))
        candidate_canonical_node = normalize_node_id(candidate.get("canonical_node_id"))
        if requested_node and not (
            _node_in_scope(candidate_tree_node, requested_scope)
            or _node_in_scope(candidate_canonical_node, requested_scope)
        ):
            continue
        if candidate_status and candidate.get("candidate_status") != candidate_status:
            continue
        if conflict_status and candidate.get("conflict_status") != conflict_status:
            continue
        if risk_level and candidate.get("risk_level") != risk_level:
            continue
        result.append(candidate)
    return sorted(result, key=lambda item: (item.get("risk_level", ""), -item.get("source_quality_score", 0)))
