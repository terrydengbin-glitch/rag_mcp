"""Audit AI/Trading Engineering tree, knowledge, Vue and MCP alignment.

Phase 47 read-only audit.

This script does not modify knowledge. It checks whether AI Engineering and
Trading Engineering formal knowledge, candidates, Vue fixtures, and MCP search
runtime are aligned enough for follow-up remediation planning.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
MCP_DIR = Path(__file__).resolve().parents[2] / "mcp"
for module_path in (CORE_DIR, MCP_DIR):
    if str(module_path) not in sys.path:
        sys.path.insert(0, str(module_path))

from path_resolver import resolve_repo_path  # noqa: E402
from tree_alias_contract import load_aliases, normalize_node_id  # noqa: E402


TASK_IDS = {
    "tree": "CEK-TA-480",
    "formal": "CEK-TA-481",
    "linkage": "CEK-TA-482",
    "vue": "CEK-TA-483",
    "mcp": "CEK-TA-484",
    "findings": "CEK-TA-485",
}

INDEX_PATH = resolve_repo_path("codex-expert-kit", "rag", "indexes", "knowledge_items.json", start_file=__file__)
CANDIDATES_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
FORMAL_FIXTURE_PATH = resolve_repo_path("ui", "src", "data", "formalKnowledgeItems.ts", start_file=__file__)
CANDIDATE_FIXTURE_PATH = resolve_repo_path("ui", "src", "data", "phase23Candidates.ts", start_file=__file__)
TREE_FIXTURE_PATH = resolve_repo_path("ui", "src", "data", "knowledgeTreeNodes.ts", start_file=__file__)
REPORT_DIR = resolve_repo_path("docs", "reports", start_file=__file__)

TREE_REPORT_PATH = REPORT_DIR / "phase47_tree_alignment_audit_report.json"
FORMAL_REPORT_PATH = REPORT_DIR / "phase47_formal_knowledge_classification_audit.json"
LINKAGE_REPORT_PATH = REPORT_DIR / "phase47_candidate_formal_linkage_audit.json"
VUE_REPORT_PATH = REPORT_DIR / "phase47_vue3_display_alignment_report.json"
MCP_REPORT_PATH = REPORT_DIR / "phase47_mcp_runtime_alignment_report.json"
FINDINGS_PATH = REPORT_DIR / "phase47_alignment_findings_and_fix_plan.md"
ALIASES = load_aliases()


TRADING_PARTITIONS = {
    "KB_01_QUANT_FOUNDATION",
    "KB_02_DATA_ENGINEERING",
    "KB_02_KLINE_STRATEGY",
    "KB_03_MARKET_MICROSTRUCTURE",
    "KB_04_BACKTEST",
    "KB_05_REPLAY_SIMULATION",
    "KB_06_LIVE_EXECUTION",
    "KB_07_RISK_MANAGEMENT",
    "KB_07_TRADE_ANALYSIS",
}

AI_PARTITIONS = {
    "KB_08_LLM_TRAINING",
    "KB_09_LLM_TRAINING",
    "KB_09_RAG_ENGINEERING",
    "KB_10_RAG_ENGINEERING",
    "KB_11_MCP_ENGINEERING",
    "KB_AI_ENGINEERING",
    "KB_AI_20_NUMERIC_SCORING",
    "KB_AI_21_CALIBRATION_THRESHOLD",
    "KB_AI_22_DECISION_TIME_FEATURES",
    "KB_AI_23_LLM_AUDIT_ASSISTANT",
    "KB_AI_24_SHADOW_PAPER_OPE",
    "KB_AI_25_MODEL_RELEASE_GOVERNANCE",
    "KB_AI_26_DATABASE_STORAGE",
    "KB_AI_27_PROJECT_MEMORY",
}

TRADING_NODE_PREFIXES = (
    "kt.trading_engineering",
    "kt.quant_foundation",
    "kt.kline_strategy",
    "kt.market_microstructure",
    "kt.backtest",
    "kt.replay_simulation",
    "kt.live_execution",
    "kt.risk_management",
    "kt.trade_analysis",
    "kt.trading_ai_safety",
)

AI_NODE_PREFIXES = (
    "kt.ai_engineering",
    "kt.llm_training",
    "kt.rag_engineering",
    "kt.mcp_engineering",
    "kt.project_memory",
)

REQUIRED_AI_L2_NODES = {
    "kt.ai_engineering",
    "kt.ai_engineering.llm_training",
    "kt.ai_engineering.rag_engineering",
    "kt.ai_engineering.mcp_engineering",
    "kt.ai_engineering.numeric_scoring",
    "kt.ai_engineering.calibration_threshold",
    "kt.ai_engineering.decision_time_features",
    "kt.ai_engineering.llm_audit_assistant",
    "kt.ai_engineering.shadow_paper_ope",
    "kt.ai_engineering.model_release_governance",
    "kt.ai_engineering.continuous_learning",
    "kt.ai_engineering.hybrid_scoring",
    "kt.ai_engineering.project_memory",
}

REQUIRED_TRADING_L2_NODES = {
    "kt.trading_engineering",
    "kt.quant_foundation",
    "kt.trading_engineering.data_engineering",
    "kt.kline_strategy",
    "kt.market_microstructure",
    "kt.backtest",
    "kt.replay_simulation",
    "kt.live_execution",
    "kt.risk_management",
    "kt.trade_analysis",
    "kt.trading_engineering.execution_tca",
    "kt.trading_engineering.trade_audit",
    "kt.trading_engineering.resilience_incident_log",
    "kt.trading_engineering.order_semantics",
}

MCP_CASES = [
    {
        "case_id": "ai_numeric_scoring",
        "query": "LightGBM XGBoost logistic regression numeric scorer trading gating calibration final gate",
        "branch": "ai",
        "filters": {"canonical_tree_path_prefix": "CEK-TA / AI Engineering"},
    },
    {
        "case_id": "ai_llm_audit_assistant",
        "query": "Qwen3 LLM audit assistant reason code citation RAG missing field check",
        "branch": "ai",
        "filters": {"canonical_tree_path_prefix": "CEK-TA / AI Engineering"},
    },
    {
        "case_id": "trading_execution_tca",
        "query": "implementation shortfall arrival price execution cost TCA market impact",
        "branch": "trading",
        "filters": {"canonical_tree_path_prefix": "CEK-TA / Trading Engineering"},
    },
    {
        "case_id": "trading_order_semantics",
        "query": "order type semantics venue specific post only reduce only rulebook adapter",
        "branch": "trading",
        "filters": {"canonical_tree_path_prefix": "CEK-TA / Trading Engineering"},
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_ts_array(path: Path, export_name: str) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    export_pos = text.find(f"export const {export_name}")
    if export_pos < 0:
        raise ValueError(f"Unable to extract {export_name} from {path}")
    equals_pos = text.find("=", export_pos)
    start = text.find("[", equals_pos)
    if equals_pos < 0 or start < 0:
        raise ValueError(f"Unable to locate array start for {export_name} in {path}")
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : index + 1])
    raise ValueError(f"Unable to locate array end for {export_name} in {path}")


def deep_get(item: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = item
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def branch_for_item(item: dict[str, Any]) -> str:
    metadata = item.get("metadata", {})
    partition_id = str(metadata.get("partition_id", ""))
    canonical_node_id = normalize_node_id(metadata.get("canonical_node_id") or metadata.get("tree_node_id") or "", ALIASES)
    tree_path = str(metadata.get("canonical_tree_path") or metadata.get("tree_path") or "")
    if partition_id in AI_PARTITIONS or canonical_node_id.startswith(AI_NODE_PREFIXES) or "AI Engineering" in tree_path:
        return "ai"
    if partition_id in TRADING_PARTITIONS or canonical_node_id.startswith(TRADING_NODE_PREFIXES) or "Trading Engineering" in tree_path:
        return "trading"
    return "other"


def branch_for_candidate(candidate: dict[str, Any]) -> str:
    classification = candidate.get("classification", {}) if isinstance(candidate.get("classification"), dict) else {}
    partition_id = str(candidate.get("partition_id") or classification.get("partition_id") or "")
    canonical_node_id = normalize_node_id(
        candidate.get("canonical_node_id")
        or candidate.get("tree_node_id")
        or classification.get("canonical_node_id")
        or classification.get("tree_node_id")
        or "",
        ALIASES,
    )
    tree_path = str(candidate.get("tree_path") or classification.get("tree_path") or "")
    if partition_id in AI_PARTITIONS or canonical_node_id.startswith(AI_NODE_PREFIXES) or "AI Engineering" in tree_path:
        return "ai"
    if partition_id in TRADING_PARTITIONS or canonical_node_id.startswith(TRADING_NODE_PREFIXES) or "Trading Engineering" in tree_path:
        return "trading"
    return "other"


def finding(
    findings: list[dict[str, Any]],
    *,
    severity: str,
    component: str,
    expected: str,
    actual: str,
    impact: str,
    suggested_fix: str,
    owner_phase: str,
    knowledge_id: str | None = None,
    node_id: str | None = None,
) -> None:
    findings.append(
        {
            "finding_id": f"PH47-{len(findings) + 1:03d}",
            "severity": severity,
            "component": component,
            "knowledge_id": knowledge_id,
            "node_id": node_id,
            "expected": expected,
            "actual": actual,
            "impact": impact,
            "suggested_fix": suggested_fix,
            "owner_phase": owner_phase,
        }
    )


def status_from_findings(findings: list[dict[str, Any]]) -> str:
    if any(item["severity"] == "error" for item in findings):
        return "fail"
    if findings:
        return "warning"
    return "pass"


def load_knowledge_items() -> list[dict[str, Any]]:
    payload = load_json(INDEX_PATH)
    items = payload.get("items", payload if isinstance(payload, list) else [])
    if not isinstance(items, list):
        raise ValueError("knowledge_items.json must be a list or {items: [...]} object.")
    return items


def load_candidates() -> list[dict[str, Any]]:
    candidates = []
    for path in sorted(CANDIDATES_ROOT.glob("**/*.json")):
        try:
            candidate = load_json(path)
        except Exception as exc:  # noqa: BLE001
            candidate = {"candidate_id": path.stem, "_load_error": str(exc)}
        if isinstance(candidate, dict):
            candidate["_source_path"] = str(path)
            candidates.append(candidate)
    return candidates


def audit_tree(items: list[dict[str, Any]], tree_nodes: list[dict[str, Any]], findings: list[dict[str, Any]]) -> dict[str, Any]:
    node_by_id = {str(node.get("node_id")): node for node in tree_nodes}
    canonical_counts = Counter(
        normalize_node_id(deep_get(item, "metadata.canonical_node_id", ""), ALIASES) for item in items
    )
    branch_counts = Counter(branch_for_item(item) for item in items)
    missing_required_nodes = []
    for node_id in sorted(REQUIRED_AI_L2_NODES | REQUIRED_TRADING_L2_NODES):
        if node_id not in node_by_id:
            missing_required_nodes.append(node_id)
            finding(
                findings,
                severity="warning",
                component="knowledge_tree",
                node_id=node_id,
                expected="Required AI/Trading L2/L3 tree node exists in Vue tree fixture.",
                actual="Node missing from ui/src/data/knowledgeTreeNodes.ts.",
                impact="前端可能无法按预期展示或过滤该分支。",
                suggested_fix="确认 knowledge_tree.md 是否已有该节点；如已有则重建 Vue fixture，如没有则另开知识树节点修复任务。",
                owner_phase="Phase 39/47",
            )
    orphan_canonical_nodes = []
    for node_id, count in canonical_counts.items():
        if node_id and node_id not in node_by_id:
            orphan_canonical_nodes.append({"node_id": node_id, "formal_item_count": count})
            finding(
                findings,
                severity="warning",
                component="knowledge_tree",
                node_id=node_id,
                expected="Every formal knowledge canonical_node_id should exist in knowledgeTreeNodes fixture.",
                actual=f"{count} formal items point to missing node.",
                impact="知识点可能可检索但前端知识树无法正常定位。",
                suggested_fix="补齐节点或建立 alias mapping；不要直接改正式知识，先确认 canonical path 设计。",
                owner_phase="Phase 39/47",
            )
    return {
        "report_id": "phase47_tree_alignment_audit",
        "generated_at": utc_now(),
        "task_id": TASK_IDS["tree"],
        "scope": "AI Engineering and Trading Engineering L1/L2/L3 node alignment.",
        "input_files": [str(INDEX_PATH), str(TREE_FIXTURE_PATH)],
        "summary": {
            "formal_item_count": len(items),
            "tree_node_count": len(tree_nodes),
            "branch_counts": dict(branch_counts),
            "canonical_node_count": len(canonical_counts),
            "missing_required_node_count": len(missing_required_nodes),
            "orphan_canonical_node_count": len(orphan_canonical_nodes),
        },
        "checks": {
            "required_ai_nodes": sorted(REQUIRED_AI_L2_NODES),
            "required_trading_nodes": sorted(REQUIRED_TRADING_L2_NODES),
            "missing_required_nodes": missing_required_nodes,
            "orphan_canonical_nodes": orphan_canonical_nodes[:200],
        },
        "findings": [item for item in findings if item["component"] == "knowledge_tree"],
        "errors": [],
        "status": status_from_findings([item for item in findings if item["component"] == "knowledge_tree"]),
    }


def audit_formal(items: list[dict[str, Any]], findings: list[dict[str, Any]]) -> dict[str, Any]:
    branch_counts = Counter()
    review_counts: dict[str, Counter[str]] = defaultdict(Counter)
    gate_counts: dict[str, Counter[str]] = defaultdict(Counter)
    partition_counts: dict[str, Counter[str]] = defaultdict(Counter)
    items_without_sources = []
    unsafe_gate_items = []
    cross_branch_suspects = []
    conflict_items = []
    for item in items:
        knowledge_id = str(item.get("knowledge_id", ""))
        branch = branch_for_item(item)
        branch_counts[branch] += 1
        review_status = str(deep_get(item, "review.review_status", ""))
        gate = str(deep_get(item, "machine_gate.default_guidance", ""))
        partition_id = str(deep_get(item, "metadata.partition_id", ""))
        canonical_node_id = str(deep_get(item, "metadata.canonical_node_id", ""))
        partition_counts[branch][partition_id] += 1
        review_counts[branch][review_status] += 1
        gate_counts[branch][gate] += 1
        if not item.get("source_evidence"):
            items_without_sources.append(knowledge_id)
            finding(
                findings,
                severity="error",
                component="formal_knowledge",
                knowledge_id=knowledge_id,
                expected="Formal knowledge must have source_evidence.",
                actual="source_evidence is empty or missing.",
                impact="MCP/RAG 不应把无来源知识作为可用知识。",
                suggested_fix="补来源或降级/移出正式索引。",
                owner_phase="Phase 2.5/47",
            )
        if review_status == "reviewed":
            explicit_unsafe = (
                deep_get(item, "review.approved_allowed") is True
                or deep_get(item, "review.default_guidance_allowed") is True
                or deep_get(item, "review.hard_gate_allowed") is True
                or gate != "caveat_only"
            )
            missing_permission_fields = [
                field
                for field in ("approved_allowed", "default_guidance_allowed", "hard_gate_allowed")
                if field not in (item.get("review") or {})
            ]
            if explicit_unsafe:
                unsafe_gate_items.append(knowledge_id)
                finding(
                    findings,
                    severity="error",
                    component="formal_knowledge",
                    knowledge_id=knowledge_id,
                    expected="reviewed item should be caveat_only and should not allow approved/default/hard gate.",
                    actual=f"review={item.get('review', {})}; machine_gate={item.get('machine_gate', {})}",
                    impact="可能导致 reviewed 知识被误当默认指导或 hard gate。",
                    suggested_fix="修正 review 权限和 machine_gate；不得自动升级 approved。",
                    owner_phase="Phase 34/47",
                )
            elif missing_permission_fields:
                finding(
                    findings,
                    severity="warning",
                    component="formal_knowledge",
                    knowledge_id=knowledge_id,
                    expected="Reviewed item should explicitly carry approved_allowed/default_guidance_allowed/hard_gate_allowed=false.",
                    actual=f"missing fields: {missing_permission_fields}; machine_gate.default_guidance={gate}",
                    impact="当前 MCP 运行时可通过 machine_gate 阻断，但 schema 显式性不足，后续迁移到其他 RAG 平台可能产生歧义。",
                    suggested_fix="后续 schema 补齐任务中批量补 review 权限字段为 false。",
                    owner_phase="Phase 34/47",
                )
        conflict_status = str(deep_get(item, "conflict_audit.conflict_status", ""))
        if conflict_status not in {"none", "resolved", "none_known_in_visible_context"}:
            conflict_items.append({"knowledge_id": knowledge_id, "conflict_status": conflict_status})
            if review_status in {"reviewed", "approved"}:
                finding(
                    findings,
                    severity="warning",
                    component="formal_knowledge",
                    knowledge_id=knowledge_id,
                    expected="Reviewed/approved formal knowledge should have none/resolved conflict status.",
                    actual=f"conflict_status={conflict_status}",
                    impact="检索时需要人工关注潜在冲突。",
                    suggested_fix="补冲突审计结论或降级为 draft/needs review。",
                    owner_phase="Phase 16/47",
                )
        if partition_id in AI_PARTITIONS and canonical_node_id.startswith(TRADING_NODE_PREFIXES):
            cross_branch_suspects.append(knowledge_id)
        if partition_id in TRADING_PARTITIONS and canonical_node_id.startswith(AI_NODE_PREFIXES):
            cross_branch_suspects.append(knowledge_id)
    return {
        "report_id": "phase47_formal_knowledge_classification_audit",
        "generated_at": utc_now(),
        "task_id": TASK_IDS["formal"],
        "scope": "Formal knowledge branch, source, conflict, review and machine_gate audit.",
        "input_files": [str(INDEX_PATH)],
        "summary": {
            "formal_item_count": len(items),
            "branch_counts": dict(branch_counts),
            "review_counts": {key: dict(value) for key, value in review_counts.items()},
            "gate_counts": {key: dict(value) for key, value in gate_counts.items()},
            "partition_counts": {key: dict(value) for key, value in partition_counts.items()},
            "items_without_sources_count": len(items_without_sources),
            "unsafe_gate_items_count": len(unsafe_gate_items),
            "cross_branch_suspect_count": len(cross_branch_suspects),
            "conflict_item_count": len(conflict_items),
        },
        "checks": {
            "items_without_sources": items_without_sources[:200],
            "unsafe_gate_items": unsafe_gate_items[:200],
            "cross_branch_suspects": cross_branch_suspects[:200],
            "conflict_items": conflict_items[:200],
        },
        "findings": [item for item in findings if item["component"] == "formal_knowledge"],
        "errors": [],
        "status": status_from_findings([item for item in findings if item["component"] == "formal_knowledge"]),
    }


def audit_linkage(items: list[dict[str, Any]], candidates: list[dict[str, Any]], findings: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_by_id = {str(candidate.get("candidate_id")): candidate for candidate in candidates if candidate.get("candidate_id")}
    formal_by_candidate: dict[str, list[str]] = defaultdict(list)
    missing_candidate_refs = []
    duplicate_refs = []
    for item in items:
        knowledge_id = str(item.get("knowledge_id", ""))
        source_candidate_id = str(deep_get(item, "contribution.source_candidate_id", "") or deep_get(item, "metadata.source_candidate_id", ""))
        if source_candidate_id:
            formal_by_candidate[source_candidate_id].append(knowledge_id)
            if source_candidate_id not in candidate_by_id:
                missing_candidate_refs.append({"knowledge_id": knowledge_id, "source_candidate_id": source_candidate_id})
                finding(
                    findings,
                    severity="warning",
                    component="candidate_formal_linkage",
                    knowledge_id=knowledge_id,
                    expected="Formal source_candidate_id should point to an existing candidate artifact.",
                    actual=f"source_candidate_id={source_candidate_id} not found.",
                    impact="审计追踪不完整，但不一定影响 MCP 检索。",
                    suggested_fix="确认候选是否被迁移、重命名或需要补 back-link。",
                    owner_phase="Phase 32/47",
                )
    for candidate_id, knowledge_ids in formal_by_candidate.items():
        if len(knowledge_ids) > 1:
            duplicate_refs.append({"candidate_id": candidate_id, "knowledge_ids": knowledge_ids})
            finding(
                findings,
                severity="warning",
                component="candidate_formal_linkage",
                expected="One candidate should normally map to one formal knowledge item unless explicitly split.",
                actual=f"{candidate_id} maps to {knowledge_ids}",
                impact="候选沉淀可能重复或需要标注 split rationale。",
                suggested_fix="检查是否为合法拆分；如合法，在 formal/candidate metadata 中写清 split note。",
                owner_phase="Phase 32/47",
            )
    candidate_branch_counts = Counter(branch_for_candidate(candidate) for candidate in candidates)
    candidate_status_counts = Counter(str(candidate.get("status", {}).get("review_status") or candidate.get("review_status") or candidate.get("workflow", {}).get("stage") or "") for candidate in candidates)
    return {
        "report_id": "phase47_candidate_formal_linkage_audit",
        "generated_at": utc_now(),
        "task_id": TASK_IDS["linkage"],
        "scope": "Candidate to formal knowledge linkage and queue consistency audit.",
        "input_files": [str(CANDIDATES_ROOT), str(INDEX_PATH)],
        "summary": {
            "candidate_file_count": len(candidates),
            "candidate_branch_counts": dict(candidate_branch_counts),
            "candidate_status_counts": dict(candidate_status_counts),
            "formal_items_with_candidate_ref": sum(1 for values in formal_by_candidate.values() for _ in values),
            "missing_candidate_ref_count": len(missing_candidate_refs),
            "duplicate_candidate_ref_count": len(duplicate_refs),
        },
        "checks": {
            "missing_candidate_refs": missing_candidate_refs[:200],
            "duplicate_candidate_refs": duplicate_refs[:200],
        },
        "findings": [item for item in findings if item["component"] == "candidate_formal_linkage"],
        "errors": [],
        "status": status_from_findings([item for item in findings if item["component"] == "candidate_formal_linkage"]),
    }


def audit_vue(
    items: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    formal_fixture: list[dict[str, Any]],
    candidate_fixture: list[dict[str, Any]],
    tree_nodes: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    formal_fixture_ids = {str(item.get("knowledge_id")) for item in formal_fixture}
    index_ids = {str(item.get("knowledge_id")) for item in items}
    candidate_fixture_ids = {str(candidate.get("candidate_id")) for candidate in candidate_fixture}
    candidate_file_ids = {str(candidate.get("candidate_id")) for candidate in candidates if candidate.get("candidate_id")}
    missing_formal_fixture = sorted(index_ids - formal_fixture_ids)
    stale_formal_fixture = sorted(formal_fixture_ids - index_ids)
    missing_candidate_fixture = sorted(candidate_file_ids - candidate_fixture_ids)
    stale_candidate_fixture = sorted(candidate_fixture_ids - candidate_file_ids)
    tree_node_ids = {str(node.get("node_id")) for node in tree_nodes}
    missing_tree_nodes = sorted(
        {
            normalize_node_id(deep_get(item, "metadata.canonical_node_id", ""), ALIASES)
            for item in items
            if branch_for_item(item) in {"ai", "trading"}
        }
        - tree_node_ids
    )
    if missing_formal_fixture:
        finding(
            findings,
            severity="error",
            component="vue3_display",
            expected="Vue formal fixture should include every item from knowledge_items.json.",
            actual=f"missing {len(missing_formal_fixture)} formal ids.",
            impact="前端知识树/SearchLab 可能看不到正式知识。",
            suggested_fix="重建 ui/src/data/formalKnowledgeItems.ts。",
            owner_phase="Phase 39/47",
        )
    if missing_tree_nodes:
        finding(
            findings,
            severity="warning",
            component="vue3_display",
            expected="Vue knowledge tree should include canonical nodes for AI/Trading formal knowledge.",
            actual=f"missing {len(missing_tree_nodes)} canonical nodes.",
            impact="前端节点统计和点击过滤可能错位。",
            suggested_fix="补齐 knowledge tree 节点或确认 alias 映射。",
            owner_phase="Phase 39/47",
        )
    return {
        "report_id": "phase47_vue3_display_alignment",
        "generated_at": utc_now(),
        "task_id": TASK_IDS["vue"],
        "scope": "Vue3 generated fixtures alignment for formal knowledge, candidates and knowledge tree.",
        "input_files": [str(FORMAL_FIXTURE_PATH), str(CANDIDATE_FIXTURE_PATH), str(TREE_FIXTURE_PATH)],
        "summary": {
            "formal_index_count": len(index_ids),
            "formal_fixture_count": len(formal_fixture_ids),
            "candidate_file_count": len(candidate_file_ids),
            "candidate_fixture_count": len(candidate_fixture_ids),
            "tree_node_count": len(tree_node_ids),
            "missing_formal_fixture_count": len(missing_formal_fixture),
            "stale_formal_fixture_count": len(stale_formal_fixture),
            "missing_candidate_fixture_count": len(missing_candidate_fixture),
            "stale_candidate_fixture_count": len(stale_candidate_fixture),
            "missing_tree_node_count": len(missing_tree_nodes),
        },
        "checks": {
            "missing_formal_fixture": missing_formal_fixture[:200],
            "stale_formal_fixture": stale_formal_fixture[:200],
            "missing_candidate_fixture": missing_candidate_fixture[:200],
            "stale_candidate_fixture": stale_candidate_fixture[:200],
            "missing_tree_nodes": missing_tree_nodes[:200],
        },
        "findings": [item for item in findings if item["component"] == "vue3_display"],
        "errors": [],
        "status": status_from_findings([item for item in findings if item["component"] == "vue3_display"]),
    }


def audit_mcp(findings: list[dict[str, Any]]) -> dict[str, Any]:
    mcp_module = load_module(
        "phase47_search_expert_knowledge",
        resolve_repo_path("codex-expert-kit", "mcp", "search_expert_knowledge.py", start_file=__file__),
    )
    cases = []
    for case in MCP_CASES:
        response = mcp_module.search_expert_knowledge(
            {
                "request_id": f"phase47-{case['case_id']}",
                "query": case["query"],
                "top_k": 8,
                "filters": case["filters"],
                "include": {"reviewed": True, "default_guidance_only": False},
            },
            knowledge_items_path=str(INDEX_PATH),
        )
        block_response = mcp_module.search_expert_knowledge(
            {
                "request_id": f"phase47-{case['case_id']}-block",
                "query": case["query"],
                "top_k": 8,
                "filters": case["filters"],
                "include": {"reviewed": True, "default_guidance_only": True},
            },
            knowledge_items_path=str(INDEX_PATH),
        )
        result_ids = [result.get("knowledge_id") for result in response.get("results", [])]
        has_sources = all(result.get("source_count", 0) > 0 for result in response.get("results", []))
        default_leaks = [
            result.get("knowledge_id")
            for result in block_response.get("results", [])
            if result.get("machine_gate", {}).get("default_guidance") != "allow"
        ]
        if not result_ids:
            finding(
                findings,
                severity="error",
                component="mcp_runtime",
                expected="MCP should return at least one result for representative AI/Trading query.",
                actual=f"{case['case_id']} returned no results.",
                impact="外部项目调用该主线知识时可能失败。",
                suggested_fix="检查 canonical_tree_path_prefix、索引或检索文本。",
                owner_phase="Phase 14/47",
            )
        if not has_sources:
            finding(
                findings,
                severity="error",
                component="mcp_runtime",
                expected="MCP returned results should include source_count > 0.",
                actual=f"{case['case_id']} has source-less returned result.",
                impact="RAG 引用不可审计。",
                suggested_fix="补来源或阻断该结果。",
                owner_phase="Phase 14/47",
            )
        if default_leaks:
            finding(
                findings,
                severity="error",
                component="mcp_runtime",
                expected="default_guidance_only should not return caveat_only/deny items.",
                actual=f"{case['case_id']} leaked {default_leaks}",
                impact="reviewed/caveat_only 可能被误用为默认指导。",
                suggested_fix="修复 MCP include.default_guidance_only 过滤。",
                owner_phase="Phase 14/47",
            )
        cases.append(
            {
                "case_id": case["case_id"],
                "branch": case["branch"],
                "filters": case["filters"],
                "status": response.get("status"),
                "result_count": len(result_ids),
                "top_result_ids": result_ids[:5],
                "all_results_have_sources": has_sources,
                "default_guidance_blocked_count": block_response.get("audit", {}).get("blocked_count", 0),
                "default_guidance_leaks": default_leaks,
            }
        )
    return {
        "report_id": "phase47_mcp_runtime_alignment",
        "generated_at": utc_now(),
        "task_id": TASK_IDS["mcp"],
        "scope": "Read-only MCP/SearchLab runtime alignment for AI and Trading Engineering.",
        "input_files": [str(INDEX_PATH), "codex-expert-kit/mcp/search_expert_knowledge.py"],
        "summary": {
            "case_count": len(cases),
            "empty_result_cases": sum(1 for case in cases if case["result_count"] == 0),
            "source_failed_cases": sum(1 for case in cases if not case["all_results_have_sources"]),
            "default_guidance_leak_cases": sum(1 for case in cases if case["default_guidance_leaks"]),
        },
        "checks": {"cases": cases},
        "findings": [item for item in findings if item["component"] == "mcp_runtime"],
        "errors": [],
        "status": status_from_findings([item for item in findings if item["component"] == "mcp_runtime"]),
    }


def write_findings_markdown(findings: list[dict[str, Any]], reports: list[dict[str, Any]]) -> None:
    severity_counts = Counter(item["severity"] for item in findings)
    lines = [
        "# Phase 47 AI/Trading Engineering 对齐审计问题清单与修复建议",
        "",
        "## 总结",
        "",
        f"- 生成时间：{utc_now()}",
        f"- 问题总数：{len(findings)}",
        f"- error：{severity_counts.get('error', 0)}",
        f"- warning：{severity_counts.get('warning', 0)}",
        "",
        "本报告只记录审计发现，不直接修改知识本体、不升级 approved、不启用 default guidance 或 hard gate。",
        "",
        "## 子报告",
        "",
    ]
    for report in reports:
        lines.append(f"- `{report['report_id']}`：`{report['status']}`")
    lines.extend(["", "## 发现项", ""])
    if not findings:
        lines.append("未发现阻断性问题。")
    for item in findings:
        subject = item.get("knowledge_id") or item.get("node_id") or "n/a"
        lines.extend(
            [
                f"### {item['finding_id']} `{item['severity']}` {item['component']}",
                "",
                f"- 对象：`{subject}`",
                f"- 预期：{item['expected']}",
                f"- 实际：{item['actual']}",
                f"- 影响：{item['impact']}",
                f"- 建议修复：{item['suggested_fix']}",
                f"- 归属：{item['owner_phase']}",
                "",
            ]
        )
    FINDINGS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    findings: list[dict[str, Any]] = []
    items = load_knowledge_items()
    candidates = load_candidates()
    formal_fixture = extract_ts_array(FORMAL_FIXTURE_PATH, "formalKnowledgeItems")
    candidate_fixture = extract_ts_array(CANDIDATE_FIXTURE_PATH, "phase23Candidates")
    tree_nodes = extract_ts_array(TREE_FIXTURE_PATH, "knowledgeTreeNodes")

    tree_report = audit_tree(items, tree_nodes, findings)
    formal_report = audit_formal(items, findings)
    linkage_report = audit_linkage(items, candidates, findings)
    vue_report = audit_vue(items, candidates, formal_fixture, candidate_fixture, tree_nodes, findings)
    mcp_report = audit_mcp(findings)

    reports = [tree_report, formal_report, linkage_report, vue_report, mcp_report]
    write_json(TREE_REPORT_PATH, tree_report)
    write_json(FORMAL_REPORT_PATH, formal_report)
    write_json(LINKAGE_REPORT_PATH, linkage_report)
    write_json(VUE_REPORT_PATH, vue_report)
    write_json(MCP_REPORT_PATH, mcp_report)
    write_findings_markdown(findings, reports)

    status = "pass" if all(report["status"] == "pass" for report in reports) else "warning"
    if any(report["status"] == "fail" for report in reports):
        status = "fail"
    print(
        json.dumps(
            {
                "status": status,
                "finding_count": len(findings),
                "report_paths": [
                    str(TREE_REPORT_PATH),
                    str(FORMAL_REPORT_PATH),
                    str(LINKAGE_REPORT_PATH),
                    str(VUE_REPORT_PATH),
                    str(MCP_REPORT_PATH),
                    str(FINDINGS_PATH),
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if status in {"pass", "warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
