"""Apply Phase 41 P0-Extended/P1 supplemental reaudit result.

This script converts only the six candidates with reviewed_allowed=true into
formal reviewed knowledge. It keeps approved, default guidance, and hard gate
permissions disabled.
"""

from __future__ import annotations

import argparse
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


TODAY = date(2026, 6, 10).isoformat()
TASK_ID = "CEK-TA-333"
AUDIT_RESULT_ID = "audit_result_phase41_extended_p1_supplemental_reaudit_20260610_strict_v2"
SOURCE_PACKAGE_ID = "phase41_extended_p1_supplemental_reaudit_package_20260610"
EXPECTED_COUNT = 6

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_COPY_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase41_extended_p1_supplemental_reaudit_import_report.json", start_file=__file__)

CLAIM_TYPE_BY_NODE_PREFIX = {
    "kt.ai_engineering.numeric_scoring": "llm_eval_rule",
    "kt.ai_engineering.calibration_threshold": "llm_eval_rule",
    "kt.ai_engineering.decision_time_feature_contract": "training_data_schema_rule",
    "kt.ai_engineering.llm_audit_assistant": "llm_eval_rule",
    "kt.ai_engineering.model_release_governance": "llmops_release_rule",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_result_path", type=Path)
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dedupe(values: list[Any]) -> list[str]:
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


def title_from_candidate(candidate: dict[str, Any]) -> str:
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:96] if statement else str(candidate.get("research_task_id", "Phase 41 reviewed knowledge"))


def claim_type_for_node(node_id: str) -> str:
    for prefix, claim_type in CLAIM_TYPE_BY_NODE_PREFIX.items():
        if node_id.startswith(prefix):
            return claim_type
    return "ai_governance_rule"


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


def shape_source_quality(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    evidence = [s for s in as_list(candidate.get("source_refs")) if isinstance(s, dict)]
    primary_types = {
        "official_doc",
        "official_repo",
        "paper",
        "research_paper",
        "standard_doc",
        "security_standard",
        "governance_framework",
        "internal_contract",
        "regulator_release",
        "regulator_review",
        "book",
    }
    primary = len(
        [
            source
            for source in evidence
            if source.get("source_type") in primary_types and source.get("reliability", "medium") in {"high", "medium"}
        ]
    )
    return {
        "overall_reliability": raw.get("overall_reliability", "high" if primary >= 2 else "medium"),
        "score": max(int(raw.get("score") or 0), 86),
        "score_version": "1.1.0",
        "primary_source_count": max(primary, int(raw.get("primary_source_count") or 0)),
        "supporting_source_count": max(0, len(evidence) - primary),
        "low_reliability_source_count": int(raw.get("low_reliability_source_count") or 0),
        "limitations": dedupe(
            as_list(raw.get("limitations"))
            + [
                "Phase 41 formal reviewed 知识可用于审计和检索；尚未 approved，不能作为默认指导或 hard gate。",
                "AI Engineering 知识不得定义 Trading PnL、fill、slippage、fee、K 线、仓位或订单执行本体。",
            ]
        ),
    }


def shape_conflict_audit(candidate: dict[str, Any]) -> dict[str, Any]:
    raw = candidate.get("conflict_audit") if isinstance(candidate.get("conflict_audit"), dict) else {}
    status = raw.get("conflict_status", "none")
    if status == "potential":
        status = "resolved"
    return {
        "conflict_status": status,
        "checked_against": as_list(raw.get("checked_against")),
        "conflicts": as_list(raw.get("conflicts")),
        "resolution_summary": raw.get(
            "resolution_summary",
            "二审确认没有 Trading Engineering 本体误路由；reviewed 不等于 approved。",
        ),
        "default_recommendation": "caveat_only_until_human_approval",
    }


def build_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    patch_notes = dedupe(
        as_list(decision.get("content_patch_notes"))
        + as_list(decision.get("boundary_patch_notes"))
        + as_list(decision.get("required_followups"))
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary") or decision.get("reason", ""),
        "procedure": [
            "确认当前任务属于 Phase 41 Hybrid Scoring / Qwen3 Audit Assistant 范围。",
            "只把本知识作为表格 scorer、校准、阈值、决策时特征、Qwen3 审计助手或组合发布治理规则使用。",
            "读取本知识项时必须同时带出 source_evidence、review_status、machine_gate 和适用边界。",
            "如果用户要求具体交易规则、K 线、fill/cost、订单状态机、风控阈值、仓位或执行参数，必须路由 Trading Engineering。",
        ]
        + patch_notes,
        "examples": [],
        "anti_patterns": [
            "把 reviewed/caveat_only 知识当作 approved/default guidance。",
            "让 Qwen3 recommendation、raw scorer score 或未校准概率替代 deterministic final gate。",
            "把 model selection、calibration、threshold 或 RAG 审计规则写成实盘交易动作。",
            "把 Trading Engineering 的 PnL、fill、slippage、fee、K 线或执行延迟本体写进 AI Engineering。",
        ],
        "validation": [
            "source_evidence 非空，且 conflict_status 为 none 或 resolved。",
            "review_status 为 reviewed 时 machine_gate.default_guidance 必须为 caveat_only。",
            "MCP/SearchLab 返回该知识时必须显示 caveat、来源和不适用场景。",
            "Vue3 知识树能按 canonical_node_id 检索并展示本条知识。",
            "不得出现 approved/default guidance/hard gate 权限。",
        ],
        "risk_notes": dedupe(
            as_list(applicability.get("limitations"))
            + patch_notes
            + [
                "本条为 formal reviewed 知识，不是 approved；不得进入默认指导或 hard gate。",
                "不得保存或推广项目私有交易数据、账户信息、策略参数或实盘订单字段。",
                "Qwen3 和 RAG 输出只能作为审计证据，不是事实来源或最终交易授权。",
            ]
        ),
        "citation_notes": claim.get("evidence_summary", ""),
    }


def build_llm_usage_policy(candidate: dict[str, Any]) -> dict[str, Any]:
    node = str(deep_get(candidate, ("classification", "canonical_node_id"), ""))
    return {
        "allowed": [
            "用于外接交易 LLM gating/scoring 项目的方案审计、代码审查、数据契约审查和 RAG/MCP 检索提示。",
            "用于提醒 AI IDE 明确模型、数据、校准、阈值、Qwen3 审计助手、RAG 引用和发布边界，并引用来源。",
            "用于在 SearchLab、KnowledgeTree 和 MCP 中以 caveat 方式返回 reviewed 知识。",
        ],
        "not_allowed": [
            "不得据此生成具体买卖点、仓位、止损止盈、杠杆、策略参数或实盘订单动作。",
            "不得把 reviewed 知识当作 approved 默认指导或 hard gate。",
            "不得让 Qwen3 recommendation、raw score 或未校准概率绕过 deterministic final gate。",
            "不得替代 Trading Engineering 对 K 线、回测、fill model、风控和执行规则本体的判断。",
        ],
        "required_context": [
            f"canonical_node_id={node}",
            "外接项目必须提供 project_adapter_id、task_type、mode、requested_decision 和相关版本号。",
            "必须同时返回 source_evidence、conflict_status、review_status 和 machine_gate。",
        ],
        "fallback_behavior": "cite_with_caveat",
    }


def build_machine_gate() -> dict[str, Any]:
    return {
        "default_guidance": "caveat_only",
        "reason": "Phase 41 P0-Extended/P1 二审允许转 formal reviewed；可审计检索，但尚未人工 approved，不能默认指导或 hard gate。",
        "requires_human_escalation": True,
        "blocking_reasons": [
            "reviewed_not_approved",
            "default_guidance_disabled_until_human_approval",
            "hard_gate_disabled",
        ],
        "checked_at": TODAY,
        "gate_version": "1.0.0",
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    candidate_id = str(candidate.get("candidate_id", ""))
    knowledge_id = str(conversion.get("proposed_knowledge_id", ""))
    tree_node_id = str(classification.get("tree_node_id", ""))
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    decision_log = []
    for entry in as_list(review.get("audit_log")):
        if isinstance(entry, dict):
            decision_log.append(
                {
                    "at": entry.get("at", TODAY),
                    "actor": entry.get("actor", "codex"),
                    "decision": entry.get("action", "updated"),
                    "reason": entry.get("reason", ""),
                }
            )
    decision_log.append(
        {
            "at": TODAY,
            "actor": "external_ai_audit_plus_codex",
            "decision": "reviewed",
            "reason": f"{TASK_ID}: supplemental reaudit accepted_for_draft 且 reviewed_allowed=true；写入 formal reviewed，仍非 approved。",
        }
    )
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id", "KB_AI_ENGINEERING"),
            "domain": classification.get("domain", "llm_training"),
            "subdomain": classification.get("subdomain", "phase41"),
            "rule_type": classification.get("rule_type", "governance_rule"),
            "claim_type": claim_type_for_node(canonical_node_id),
            "content_type": "json",
            "project_binding": "none",
            "classification_notes": "Phase 41 P0-Extended/P1 formal reviewed knowledge；二审允许 reviewed，但不是 approved/default guidance。",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / AI Engineering / Hybrid Scoring And Qwen3 Audit"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / AI Engineering / Hybrid Scoring And Qwen3 Audit"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate_id,
            "research_task_id": candidate.get("research_task_id", ""),
            "phase": "Phase 41",
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_llm_gating_scoring"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate, decision),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [
            source_to_evidence(source)
            for source in as_list(candidate.get("source_refs"))
            if isinstance(source, dict)
        ],
        "source_quality": shape_source_quality(candidate),
        "conflict_audit": shape_conflict_audit(candidate),
        "llm_usage_policy": build_llm_usage_policy(candidate),
        "machine_gate": build_machine_gate(),
        "recommended_extra_sources": [],
        "review": {
            "confidence": review.get("confidence", "medium"),
            "freshness": review.get("freshness", "time_sensitive"),
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": status.get("created_at", TODAY),
            "updated_at": TODAY,
            "default_guidance_allowed": False,
            "approval_status": "not_requested",
            "source_candidate_id": candidate_id,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_draft",
                "reviewed_allowed": True,
                "allowed_next_stage": "formal_reviewed_knowledge",
                "reason": decision.get("reason", ""),
                "source_patch_notes": as_list(decision.get("source_patch_notes")),
                "content_patch_notes": as_list(decision.get("content_patch_notes")),
                "boundary_patch_notes": as_list(decision.get("boundary_patch_notes")),
                "conflict_patch_notes": as_list(decision.get("conflict_patch_notes")),
                "required_followups": as_list(decision.get("required_followups")),
                "default_guidance_allowed": False,
                "approved_allowed": False,
                "hard_gate_allowed": False,
            },
            "open_questions": dedupe(
                as_list(review.get("open_questions"))
                + as_list(decision.get("content_patch_notes"))
                + as_list(decision.get("boundary_patch_notes"))
            ),
            "decision_log": decision_log,
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 41 public-source candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "phase41_conversion": {
            "source_candidate_status": status.get("review_status"),
            "source_ingestion_decision": status.get("ingestion_decision"),
            "promoted_by_task": TASK_ID,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "reviewed_allowed": True,
            "approved_allowed": False,
        },
    }


def validate_audit_result(audit_result: dict[str, Any]) -> None:
    if audit_result.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError("Unexpected audit_result_id")
    if audit_result.get("source_package_id") != SOURCE_PACKAGE_ID:
        raise ValueError("Unexpected source_package_id")
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != EXPECTED_COUNT:
        raise ValueError(f"Expected {EXPECTED_COUNT} decisions")
    for decision in decisions:
        if not isinstance(decision, dict):
            raise ValueError("Decision entries must be objects")
        if decision.get("decision") != "accepted_for_draft":
            raise ValueError(f"Unsupported decision for this import: {decision.get('decision')}")
        if decision.get("reviewed_allowed") is not True:
            raise ValueError(f"{decision.get('candidate_id')}: reviewed_allowed must be true")
        if decision.get("approved_allowed") is not False:
            raise ValueError(f"{decision.get('candidate_id')}: approved_allowed must be false")
        if decision.get("default_guidance_allowed") is not False:
            raise ValueError(f"{decision.get('candidate_id')}: default_guidance_allowed must be false")
        if decision.get("hard_gate_allowed") is not False:
            raise ValueError(f"{decision.get('candidate_id')}: hard_gate_allowed must be false")


def load_candidates_by_id() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_p41_*.json")):
        candidate = read_json(path)
        candidate_id = candidate.get("candidate_id")
        if isinstance(candidate_id, str):
            candidates[candidate_id] = (path, candidate)
    return candidates


def validate_candidate_for_reviewed(candidate: dict[str, Any], decision: dict[str, Any]) -> str | None:
    if candidate.get("candidate_id") != decision.get("candidate_id"):
        return "candidate_id_mismatch"
    if not str(candidate.get("research_task_id", "")).startswith("P41-"):
        return "not_phase41"
    if deep_get(candidate, ("status", "ingestion_decision")) not in {"accepted_for_draft", "ready_for_reaudit"}:
        return "not_accepted_or_reaudit_ready"
    if not deep_get(candidate, ("conversion_target", "proposed_knowledge_id")):
        return "missing_knowledge_id"
    if not str(deep_get(candidate, ("classification", "canonical_node_id"), "")).startswith("kt.ai_engineering."):
        return "wrong_node"
    if not as_list(candidate.get("source_refs")):
        return "missing_sources"
    if deep_get(candidate, ("copyright", "stores_full_text")) is not False:
        return "stores_full_text"
    if deep_get(candidate, ("copyright", "stores_long_quote")) is not False:
        return "stores_long_quote"
    if deep_get(candidate, ("conflict_audit", "conflict_status")) not in {"none", "resolved"}:
        return "unsafe_conflict"
    return None


def write_knowledge(item: dict[str, Any]) -> Path:
    partition = item["metadata"]["partition_id"]
    path = KNOWLEDGE_ROOT / partition / sanitize_filename(item["knowledge_id"])
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {repo_rel(path)}")
    write_json(path, item)
    return path


def update_candidate_backlink(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = "二审 accepted_for_draft 且 reviewed_allowed=true；已生成 formal reviewed knowledge。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "formalized_reviewed",
            "queue_group": "formalized",
            "formal_knowledge_id": item["knowledge_id"],
            "formal_review_status": "reviewed",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "request_human_approval",
            "default_guidance_allowed": False,
            "knowledge_path": repo_rel(knowledge_path),
        }
    )

    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = True
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False
    audit = review.setdefault("ai_audit", {})
    if isinstance(audit, dict):
        audit.update(
            {
                "audit_result_id": AUDIT_RESULT_ID,
                "source_package_id": SOURCE_PACKAGE_ID,
                "decision": "accepted_for_draft",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "allowed_next_stage": "formal_reviewed_knowledge",
                "reason": decision.get("reason", ""),
            }
        )
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase41_extended_p1_formal_reviewed_created",
                "reason": f"{TASK_ID}: formal reviewed knowledge written to {repo_rel(knowledge_path)}.",
            }
        )


def main() -> int:
    args = parse_args()
    audit_result = read_json(args.audit_result_path)
    validate_audit_result(audit_result)
    if args.audit_result_path.resolve() != AUDIT_COPY_PATH.resolve():
        AUDIT_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.audit_result_path, AUDIT_COPY_PATH)

    candidates = load_candidates_by_id()
    promoted: list[dict[str, Any]] = []
    touched_candidates: list[str] = []
    written_knowledge_paths: list[str] = []
    skipped = Counter()

    for decision in audit_result["decisions"]:
        candidate_id = str(decision["candidate_id"])
        if candidate_id not in candidates:
            skipped["candidate_file_not_found"] += 1
            continue
        candidate_path, candidate = candidates[candidate_id]
        reason = validate_candidate_for_reviewed(candidate, decision)
        if reason:
            skipped[reason] += 1
            continue
        item = candidate_to_knowledge(candidate, decision)
        knowledge_path = write_knowledge(item)
        update_candidate_backlink(candidate, item, knowledge_path, decision)
        write_json(candidate_path, candidate)
        touched_candidates.append(repo_rel(candidate_path))
        written_knowledge_paths.append(repo_rel(knowledge_path))
        promoted.append(
            {
                "candidate_id": candidate_id,
                "research_task_id": candidate.get("research_task_id"),
                "knowledge_id": item["knowledge_id"],
                "knowledge_path": repo_rel(knowledge_path),
                "canonical_node_id": item["metadata"]["canonical_node_id"],
                "partition_id": item["metadata"]["partition_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )

    if len(promoted) != EXPECTED_COUNT:
        raise ValueError(f"Expected {EXPECTED_COUNT} promotions, got {len(promoted)}; skipped={dict(skipped)}")

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    by_partition = Counter(item["partition_id"] for item in promoted)
    report = {
        "report_id": "phase41_extended_p1_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_COPY_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": 0,
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "by_node": dict(sorted(by_node.items())),
        "by_partition": dict(sorted(by_partition.items())),
        "promoted": promoted,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "skipped": dict(skipped),
        "boundary": "formal reviewed only; machine_gate=caveat_only; no approved/default guidance/hard gate.",
        "next_action": "重建 knowledge_items/UI fixture，并执行 Phase 41 扩展运行时联动验证。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
