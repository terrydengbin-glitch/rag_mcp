"""Import Phase 37 blocked supplemental re-audit result.

CEK-TA-382 promotes P37-A-Q02/Q06/Q11 from supplemented candidates into
formal reviewed/caveat_only knowledge. It must not create approved/default
guidance/hard gate knowledge.
"""

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

from path_resolver import resolve_project_root, resolve_repo_path  # noqa: E402


ROOT = resolve_project_root(__file__)
TODAY = "2026-06-11"
TASK_ID = "CEK-TA-382"
SOURCE_PACKAGE_ID = "phase37_quant_foundation_blocked_supplemental_reaudit_package_20260611"
AUDIT_RESULT_ID = "audit_result_phase37_quant_foundation_blocked_supplemental_reaudit_20260611_strict_v3"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_01_QUANT_FOUNDATION", start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path(
    "docs", "audit", "audit_result_phase37_quant_foundation_blocked_supplemental_reaudit_20260611_strict_v3.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_quant_foundation_blocked_supplemental_reaudit_import_report.json", start_file=__file__
)


AUDIT_RESULT: dict[str, Any] = {
    "audit_result_id": AUDIT_RESULT_ID,
    "package_id": SOURCE_PACKAGE_ID,
    "audited_at": TODAY,
    "auditor": "external_ai_strict_reaudit",
    "quality_gate": {
        "pass": True,
        "candidate_count": 3,
        "notes": [
            "3 条全部允许进入 formal reviewed/caveat_only。",
            "不得 approved、不得 default guidance、不得 hard gate。",
            "不得生成买卖点、具体仓位、杠杆、止损止盈或实盘执行建议。",
        ],
    },
    "summary": {
        "accepted_for_reviewed_caveat_only": 3,
        "needs_more_evidence": 0,
        "rejected": 0,
        "reviewed_allowed": 3,
        "approved_allowed": 0,
        "default_guidance_allowed": 0,
        "hard_gate_allowed": 0,
    },
    "decisions": [
        {
            "candidate_id": "cand_20260611_phase37_r_multiple_definition_001",
            "research_task_id": "P37-A-Q02",
            "decision": "accepted_for_reviewed_caveat_only",
            "confidence": "medium_high",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "reasons": [
                "Van Tharp Institute 概念页直接支撑 R、R-multiple distribution、expectancy 和 R-value。",
                "Van Tharp position sizing 书籍 TOC 页码线索足以支撑 caveat-only reviewed preparation。",
                "主分类已调整为 risk_normalized_metrics，position_sizing 仅作为 related dependency。",
            ],
            "required_patches": {
                "source": [
                    "保留 Van Tharp 概念页和 Position Sizing 书籍 TOC 页码线索；approved 前仍需人工核验合法正文页。"
                ],
                "content": [
                    "R-multiple 只能表达风险归一化交易结果，不是 edge、盈利能力、稳健性或实盘资格证明。"
                ],
                "boundary": [
                    "不得用 R-multiple 单独替代成本、滑点、回撤、样本量和样本外验证。",
                    "不得输出仓位、止损距离、杠杆或下单许可。"
                ],
                "conflict": [
                    "未发现买卖点、仓位、杠杆、止损止盈、实盘执行、项目私有参数或密钥污染。"
                ],
            },
            "required_extra_sources": [],
            "formal_conversion_notes": [
                "formal reviewed draft 必须保留 caveat_only。",
                "approved/default guidance/hard gate 均保持 false。"
            ],
        },
        {
            "candidate_id": "cand_20260611_phase37_position_sizing_requires_risk_unit_001",
            "research_task_id": "P37-A-Q06",
            "decision": "accepted_for_reviewed_caveat_only",
            "confidence": "medium_high",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "reasons": [
                "候选已拆分 Trading Engineering 外部事实和 CEK-TA AI governance 内部规则。",
                "CFA/SEC/Investor.gov/CrossTrade 可支撑风险预算、暴露、保证金和仓位 sizing 前置字段边界。",
                "CEK-TA Phase 38 runtime contract 可支撑 AI 只能提示缺字段、路由 human_review/needs_more_evidence，不能自行推导仓位。"
            ],
            "required_patches": {
                "source": [
                    "外部来源只支撑交易仓位 sizing 前置事实；AI 缺字段行为边界来自 CEK-TA 内部治理契约。"
                ],
                "content": [
                    "正式知识分成 Trading Engineering prerequisite fields 和 AI governance behavior 两段。"
                ],
                "boundary": [
                    "禁止具体仓位公式、百分比风险建议、杠杆倍数建议、止损/止盈建议、订单动作和账户级实盘执行判断。"
                ],
                "conflict": [
                    "Trading Engineering 保存交易规则本体；AI Engineering 只保存引用和治理边界。"
                ],
            },
            "required_extra_sources": [],
            "formal_conversion_notes": [
                "只作为字段前置条件和 AI 行为边界，不作为 position sizing 教程或实盘风控规则。",
                "approved/default guidance/hard gate 均保持 false。"
            ],
        },
        {
            "candidate_id": "cand_20260611_phase37_sample_size_and_regime_caveat_001",
            "research_task_id": "P37-A-Q11",
            "decision": "accepted_for_reviewed_caveat_only",
            "confidence": "high",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "reasons": [
                "LSEG、State Street 和 UCL 来源补齐 market regime / non-stationarity 直接证据。",
                "Bailey et al. 等来源继续支撑 backtest overfitting 和样本外验证风险。",
                "补证已能支撑单一 regime 证据不得未经验证泛化为跨市场、跨周期或跨状态规则。"
            ],
            "required_patches": {
                "source": [
                    "保留 regime/non-stationarity 专业来源，不再只依赖过拟合或样本外资料间接支撑。"
                ],
                "content": [
                    "表述为未经验证不得泛化，而不是单一 regime 结果永远不能迁移。"
                ],
                "boundary": [
                    "不定义统一 regime taxonomy，不定义统一最小样本量，不把 regime caveat 变成 hard gate。"
                ],
                "conflict": [
                    "未发现买卖点、仓位、杠杆、止损止盈、实盘执行、项目私有参数或密钥污染。"
                ],
            },
            "required_extra_sources": [],
            "formal_conversion_notes": [
                "formal reviewed draft 必须拆清 sample_count、sample_period、asset_scope、regime_coverage、validation_method。",
                "approved/default guidance/hard gate 均保持 false。"
            ],
        },
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def dedupe_strings(values: list[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value).strip()
        if text and text not in seen:
            result.append(text)
            seen.add(text)
    return result


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", knowledge_id).strip("._") + ".json"


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    evidence = {
        "source_id": source.get("source_id"),
        "source_title": source.get("source_title"),
        "source_url": source.get("source_url"),
        "source_type": source.get("source_type"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": source.get("accessed_at"),
        "version": source.get("version"),
        "reliability": source.get("reliability"),
        "relevance": source.get("relevance"),
        "evidence_summary": source.get("evidence_summary"),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }
    if source.get("page_refs"):
        evidence["page_refs"] = source.get("page_refs")
    if source.get("limitations"):
        evidence["limitations"] = source.get("limitations")
    return evidence


def merge_sources(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for source in as_list(candidate.get("source_refs")):
        if not isinstance(source, dict):
            continue
        source_id = str(source.get("source_id", ""))
        if source_id and source_id not in seen:
            result.append(source)
            seen.add(source_id)
    return result


def title_from_candidate(candidate: dict[str, Any]) -> str:
    return str(deep_get(candidate, ("claim", "statement"), candidate.get("candidate_id", "")))


def shape_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    primary = len([source for source in sources if str(source.get("reliability")) in {"high", "medium_high"}])
    return {
        "overall_reliability": raw.get("overall_reliability", "medium_high"),
        "score": raw.get("score", 84),
        "score_version": raw.get("score_version", "phase37_source_scoring_v1"),
        "primary_source_count": max(int(raw.get("primary_source_count") or 0), primary),
        "supporting_source_count": max(len(sources) - primary, 0),
        "low_reliability_source_count": raw.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(raw.get("limitations"))
            + as_list(deep_get(decision, ("required_patches", "source"), []))
            + [
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
                "外部审计未提供完整 CEK-TA formal KB，因此冲突结论限于可见上下文。",
            ]
        ),
    }


def task_specific_procedure(task_id: str) -> list[str]:
    base = [
        "确认当前问题属于 Quant Foundation / Trading Engineering 规则本体，而不是 AI Engineering 训练、RAG 或 MCP 本体。",
        "返回本知识时必须携带 source_evidence、review_status、machine_gate、适用范围和不适用场景。",
    ]
    if task_id == "P37-A-Q02":
        base.append("只把 R-multiple 作为风险归一化交易结果指标使用，并同时检查成本、滑点、样本量、回撤和验证边界。")
    elif task_id == "P37-A-Q06":
        base.append("先检查账户风险预算、风险单位、失效/止损边界、最大暴露和保证金/杠杆约束是否由外部事实层提供。")
        base.append("若字段缺失，AI 只能提示 missing_fields 并路由 human_review/needs_more_evidence，不得自行推导仓位。")
    elif task_id == "P37-A-Q11":
        base.append("检查 sample_count、sample_period、asset_scope、regime_coverage 和 validation_method 是否齐全。")
        base.append("单一 regime 或未处理 non-stationarity 的结果只能作为局部证据，不能未经验证泛化。")
    return base


def shape_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    task_id = str(candidate.get("research_task_id"))
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    risk_notes = dedupe_strings(
        as_list(applicability.get("limitations"))
        + as_list(deep_get(decision, ("required_patches", "boundary"), []))
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "AI Engineering 只能引用本 Trading Engineering 规则本体，不得复制改写为模型训练/RAG/MCP 本体规则。",
        ]
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": task_specific_procedure(task_id),
        "examples": [],
        "anti_patterns": [
            "把 caveat-only 知识当成 approved 默认指导。",
            "把交易工程边界改写成买卖信号、仓位、杠杆或实盘执行动作。",
            "忽略来源、适用边界、成本、样本、执行或验证条件就泛化结论。",
        ],
        "validation": [
            "source_evidence 非空，且来源足以支撑 claim 的定义和边界。",
            "conflict_status 只能是 none、resolved 或 none_known_in_visible_context。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
        ],
        "risk_notes": risk_notes,
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": {
            "source": as_list(deep_get(decision, ("required_patches", "source"), [])),
            "content": as_list(deep_get(decision, ("required_patches", "content"), [])),
            "boundary": as_list(deep_get(decision, ("required_patches", "boundary"), [])),
            "conflict": as_list(deep_get(decision, ("required_patches", "conflict"), [])),
        },
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    sources = merge_sources(candidate)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    if not knowledge_id:
        raise ValueError(f"{candidate.get('candidate_id')} missing conversion_target.proposed_knowledge_id")
    tree_node_id = str(classification.get("tree_node_id", "kt.quant_foundation"))
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id", "KB_01_QUANT_FOUNDATION"),
            "domain": classification.get("domain", "quant_trading"),
            "subdomain": classification.get("subdomain", "quant_foundation"),
            "rule_type": classification.get("rule_type", "principle"),
            "claim_type": classification.get("claim_type", "methodological_constraint"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Quant Foundation"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Quant Foundation"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Quant Foundation formal reviewed/caveat_only；这是 Trading Engineering 规则本体，"
                "不是 AI Engineering 训练/RAG/MCP 本体规则，也不是 approved/default guidance。"
            ),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": shape_content(candidate, decision),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source) for source in sources],
        "source_quality": shape_source_quality(candidate, sources, decision),
        "conflict_audit": {
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status"), "none_known_in_visible_context"),
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": "blocked supplemental re-audit passed; formal reviewed/caveat_only created by CEK-TA-382.",
            "default_recommendation": "caveat_only_until_human_approval",
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计交易工程基础概念和边界。",
                "用于提示用户补充来源、成本、样本、执行、风险和验证条件。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源和边界。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得绕过外接项目事实层、风控 hard gate 或人工治理流程。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate 和不适用场景。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: strict re-audit allowed formal reviewed/caveat_only only; no approved/default/hard gate.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "recommended_extra_sources": [],
        "review": {
            "confidence": decision.get("confidence", review.get("confidence", "medium")),
            "freshness": review.get("freshness", "mixed"),
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": candidate.get("candidate_id"),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "required_patches": decision.get("required_patches", {}),
                "required_extra_sources": decision.get("required_extra_sources", []),
                "formal_conversion_notes": decision.get("formal_conversion_notes", []),
            },
            "open_questions": [],
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_reaudit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": decision.get("reasons", [""])[0],
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "decision": "reviewed",
                    "reason": f"{TASK_ID}: formal reviewed/caveat_only created; approved/default guidance/hard gate all disabled.",
                },
            ],
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "phase37_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": TASK_ID,
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }


def write_knowledge(item: dict[str, Any]) -> Path:
    partition = str(item["metadata"]["partition_id"])
    path = KNOWLEDGE_ROOT / partition / sanitize_filename(str(item["knowledge_id"]))
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def update_candidate_formalized(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, decision: dict[str, Any]) -> None:
    candidate.setdefault("status", {}).update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "CEK-TA-382: strict re-audit accepted for formal reviewed/caveat_only.",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_knowledge_path": rel(knowledge_path),
            "formal_review_status": "reviewed",
            "reviewed_allowed": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "validate_runtime_linkage",
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["target_machine_gate"] = "caveat_only"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    review = candidate.setdefault("review", {})
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "accepted_for_reviewed_caveat_only",
        "reviewed_allowed": True,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_patches": decision.get("required_patches", {}),
        "formal_conversion_notes": decision.get("formal_conversion_notes", []),
    }
    audit_log = review.setdefault("audit_log", [])
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_blocked_supplemental_reaudit_formalized",
            "reason": "CEK-TA-382: external strict re-audit accepted this candidate for formal reviewed/caveat_only.",
            "audit_result_id": AUDIT_RESULT_ID,
            "formal_knowledge_id": item["knowledge_id"],
        }
    )


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            result[task_id] = (path, candidate)
    return result


def main() -> int:
    write_json(AUDIT_RESULT_PATH, AUDIT_RESULT)
    candidates = load_candidates()
    promoted: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    for decision in AUDIT_RESULT["decisions"]:
        task_id = str(decision["research_task_id"])
        if decision["decision"] != "accepted_for_reviewed_caveat_only":
            skipped.append({"research_task_id": task_id, "reason": decision["decision"]})
            continue
        path, candidate = candidates[task_id]
        if candidate.get("candidate_id") != decision["candidate_id"]:
            raise ValueError(f"{task_id} candidate id mismatch.")
        if deep_get(candidate, ("workflow", "queue_group")) not in {"needs_more_evidence", "formalized"}:
            raise ValueError(f"{task_id} candidate not in expected queue.")
        item = candidate_to_knowledge(candidate, decision)
        knowledge_path = write_knowledge(item)
        update_candidate_formalized(candidate, item, knowledge_path, decision)
        write_json(path, candidate)
        promoted.append(
            {
                "research_task_id": task_id,
                "candidate_id": candidate["candidate_id"],
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": rel(knowledge_path),
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
            }
        )

    if len(promoted) != 3:
        raise ValueError(f"Expected 3 promoted candidates, got {len(promoted)}; skipped={skipped}")

    report = {
        "report_id": "phase37_quant_foundation_blocked_supplemental_reaudit_import_report",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "promoted": promoted,
        "skipped": skipped,
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate.",
        "next_action": "重建 knowledge_items/UI fixture，并执行 MCP/SearchLab/KnowledgeTree 联动验证。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
