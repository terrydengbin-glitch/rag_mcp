"""Apply Phase 37 Data Engineering blocked supplemental re-audit result.

Consumes the external strict audit result for P37-B-D10/D11. Only entries with
``accepted_for_reviewed_caveat_only`` and ``reviewed_allowed=true`` are written
as formal reviewed/caveat_only knowledge. It never creates approved knowledge,
default guidance, hard gates, or trading execution advice.
"""

from __future__ import annotations

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


TODAY = date(2026, 6, 11).isoformat()
TASK_ID = "CEK-TA-391"
AUDIT_RESULT_ID = "audit_result_phase37_data_engineering_blocked_supplemental_reaudit_20260611_strict_v1"
SOURCE_PACKAGE_ID = "phase37_data_engineering_blocked_supplemental_reaudit_package_20260611"
EXPECTED_TOTAL = 2
EXPECTED_PROMOTED = 1
EXPECTED_NEEDS_MORE = 1

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_02_DATA_ENGINEERING", start_file=__file__
)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_ARCHIVE_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase37_data_engineering_blocked_supplemental_reaudit_import_report.json", start_file=__file__
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


def deep_get(item: dict[str, Any], path: tuple[str, ...], default: Any = None) -> Any:
    current: Any = item
    for part in path:
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def string_list(value: Any) -> list[str]:
    result: list[str] = []
    for item in as_list(value):
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result


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


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (
        str(source.get("source_url") or source.get("url") or ""),
        str(source.get("source_title") or source.get("title") or source.get("purpose") or ""),
    )


def archive_audit_result(source_path: Path) -> dict[str, Any]:
    payload = read_json(source_path)
    if payload.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError(f"Unexpected audit_result_id: {payload.get('audit_result_id')}")
    if payload.get("package_id") != SOURCE_PACKAGE_ID:
        raise ValueError(f"Unexpected package_id: {payload.get('package_id')}")
    if deep_get(payload, ("quality_gate", "candidate_count")) != EXPECTED_TOTAL:
        raise ValueError("Audit result candidate_count must be 2.")
    AUDIT_RESULT_ARCHIVE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if source_path.resolve() != AUDIT_RESULT_ARCHIVE_PATH.resolve():
        shutil.copyfile(source_path, AUDIT_RESULT_ARCHIVE_PATH)
    else:
        write_json(AUDIT_RESULT_ARCHIVE_PATH, payload)
    return payload


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    candidates: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase37_data_engineering_*.json")):
        candidate = read_json(path)
        task_id = str(candidate.get("research_task_id", ""))
        if task_id:
            candidates[task_id] = (path, candidate)
    return candidates


def normalize_source(source: dict[str, Any], index: int) -> dict[str, Any]:
    title = str(source.get("source_title") or source.get("title") or source.get("purpose") or f"source_{index}")
    url = source.get("source_url") or source.get("url")
    return {
        "source_id": str(source.get("source_id") or f"src_{index:03d}"),
        "source_title": title,
        "source_url": url,
        "source_type": str(source.get("source_type") or source.get("type") or "reviewed_preparation_required_extra_source"),
        "publisher": source.get("publisher") or "unknown",
        "published_at": source.get("published_at"),
        "accessed_at": str(source.get("accessed_at") or TODAY),
        "version": source.get("version"),
        "reliability": str(source.get("reliability") or "medium"),
        "relevance": str(source.get("relevance") or "medium_high"),
        "evidence_summary": str(source.get("evidence_summary") or source.get("purpose") or ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def source_to_evidence(source: dict[str, Any], index: int) -> dict[str, Any]:
    normalized = normalize_source(source, index)
    normalized["source_id"] = str(source.get("source_id") or normalized["source_id"])
    return normalized


def unresolved_required_sources(decision: dict[str, Any]) -> list[dict[str, Any]]:
    unresolved: list[dict[str, Any]] = []
    for item in as_list(decision.get("required_extra_sources")):
        if isinstance(item, dict) and not (item.get("url") or item.get("source_url")):
            unresolved.append(item)
    return unresolved


def title_from_candidate(candidate: dict[str, Any]) -> str:
    statement = str(deep_get(candidate, ("claim", "statement"), "")).strip()
    return statement[:120] if statement else str(deep_get(candidate, ("conversion_target", "proposed_knowledge_id"), ""))


def build_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    required_patches = decision.get("required_patches") if isinstance(decision.get("required_patches"), dict) else {}
    risk_notes = dedupe_strings(
        as_list(applicability.get("limitations"))
        + string_list(required_patches.get("boundary"))
        + string_list(required_patches.get("conflict"))
        + [
            "本条为 formal reviewed/caveat_only，不是 approved；不得作为默认指导或 hard gate。",
            "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            "AI Engineering 只能引用本 Trading Engineering 数据工程规则本体，不得复制改写为模型训练、RAG 或 MCP 本体规则。",
        ]
    )
    return {
        "statement": claim.get("statement", ""),
        "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary", ""),
        "procedure": [
            "确认当前问题属于 CEK-TA 回测、训练、评估或审计数据契约，而不是外部监管硬要求。",
            "检查 anomaly/outlier 是否被标记、隔离、解释、保留或以版本化修复记录表达。",
            "确认 raw event、correction record、repair action、affected dataset version 和数据质量报告可追踪。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 anomaly/outlier 自动等同于错误数据并默认删除。",
            "静默重写 raw event、训练样本或回测评估样本。",
            "把 Databento、CME、Nasdaq 的供应商/venue/protocol 字段名泛化为所有数据源通用 schema。",
        ],
        "validation": [
            "source_evidence 覆盖 market-data cleaning、event taxonomy、trade correction/cancel 和 trade reporting/timestamp 边界。",
            "content.audit_patch_notes 已纳入外部审计要求的 source/content/boundary/conflict 补丁。",
            "machine_gate.default_guidance 必须为 caveat_only，review.default_guidance_allowed 必须为 false。",
        ],
        "risk_notes": risk_notes,
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": {
            "source": string_list(required_patches.get("source")),
            "content": string_list(required_patches.get("content")),
            "boundary": string_list(required_patches.get("boundary")),
            "conflict": string_list(required_patches.get("conflict")),
        },
        "suggested_fields": [
            "anomaly_flag",
            "anomaly_type",
            "detection_rule_id",
            "source_event_id",
            "correction_id",
            "correction_source",
            "repair_action",
            "repair_timestamp",
            "raw_event_ref",
            "affected_dataset_version",
        ],
    }


def build_source_quality(candidate: dict[str, Any], sources: list[dict[str, Any]], decision: dict[str, Any]) -> dict[str, Any]:
    source_quality = candidate.get("source_quality") if isinstance(candidate.get("source_quality"), dict) else {}
    required_patches = decision.get("required_patches") if isinstance(decision.get("required_patches"), dict) else {}
    return {
        "overall_reliability": "medium_high",
        "score": min(float(source_quality.get("score", 80)), 84.0),
        "score_version": "phase37_data_engineering_blocked_supplemental_reaudit_source_scoring_v1",
        "primary_source_count": 4,
        "supporting_source_count": max(0, len(sources) - 4),
        "low_reliability_source_count": source_quality.get("low_reliability_source_count", 0),
        "limitations": dedupe_strings(
            as_list(source_quality.get("limitations"))
            + string_list(required_patches.get("source"))
            + [
                "Great Expectations 产品页和通用框架页只能作为 supporting source。",
                "CME EPICSANDBOX / Confluence 来源必须保留 venue-specific caveat，正式生产文档可在后续版本补强。",
                "Nasdaq FIX PDF 只适用于 Nasdaq FIX Trade Reporting 语境，不能泛化为所有交易所。",
                "Databento 字段名只能作为供应商 schema 证据，不能泛化为所有市场数据字段名。",
                "本条为 formal reviewed/caveat_only；不是 approved，不得进入默认指导或 hard gate。",
            ]
        ),
    }


def candidate_to_knowledge(candidate: dict[str, Any], decision: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    review = candidate.get("review") if isinstance(candidate.get("review"), dict) else {}
    status = candidate.get("status") if isinstance(candidate.get("status"), dict) else {}
    conversion = candidate.get("conversion_target") if isinstance(candidate.get("conversion_target"), dict) else {}
    sources = [s for s in as_list(candidate.get("source_refs")) if isinstance(s, dict)]
    unresolved_sources = unresolved_required_sources(decision)
    knowledge_id = str(conversion.get("proposed_knowledge_id"))
    tree_node_id = str(classification.get("tree_node_id", "kt.trading_engineering.data_engineering"))
    canonical_node_id = str(classification.get("canonical_node_id") or tree_node_id)
    item = {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_from_candidate(candidate),
        "metadata": {
            "partition_id": "KB_02_DATA_ENGINEERING",
            "domain": classification.get("domain", "trading_engineering"),
            "subdomain": classification.get("subdomain", "data_quality"),
            "rule_type": classification.get("rule_type", "data_quality_gate"),
            "claim_type": classification.get("claim_type", "data_quality_gate"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": tree_node_id,
            "tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Data Engineering"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path", "CEK-TA / Trading Engineering / Data Engineering"),
            "risk_level": "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 37",
            "classification_notes": (
                "Phase 37 Data Engineering formal reviewed/caveat_only；这是 Trading Engineering 数据规则本体，"
                "不是 AI Engineering 训练/RAG/MCP 本体规则，也不是 approved/default guidance。"
            ),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "event_or_bar"),
            "project_type": applicability.get("project_type", "trading_ai_support_layer"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": build_content(candidate, decision),
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": [source_to_evidence(source, index) for index, source in enumerate(sources, start=1)],
        "source_quality": build_source_quality(candidate, sources, decision),
        "conflict_audit": {
            "conflict_status": deep_get(candidate, ("conflict_audit", "conflict_status"), "none_known_in_visible_context"),
            "checked_against": as_list(deep_get(candidate, ("conflict_audit", "checked_against"), [])),
            "conflicts": as_list(deep_get(candidate, ("conflict_audit", "conflicts"), [])),
            "resolution_summary": "D10 supplemental re-audit accepted reviewed/caveat_only in visible context; full formal KB conflict coverage remains runtime validation.",
            "default_recommendation": "caveat_only_until_human_approval",
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE 或外接项目审计交易数据异常值、correction、flags 和修复记录边界。",
                "用于提示用户补充 anomaly/correction/repair/version 字段和数据质量报告。",
                "用于 RAG/MCP/SearchLab 以 caveat 方式返回来源和边界。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得把 reviewed/caveat_only 当作 approved 默认指导。",
                "不得允许 AI 自动修复历史行情或自动改变模型/策略评估结论。",
            ],
            "required_context": [
                f"canonical_node_id={canonical_node_id}",
                "必须返回 source_evidence、review_status、conflict_status、machine_gate 和不适用场景。",
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": f"{TASK_ID}: supplemental re-audit allowed formal reviewed/caveat_only only; no approved/default/hard gate.",
            "requires_human_escalation": True,
            "blocking_reasons": [
                "reviewed_not_approved",
                "default_guidance_allowed_false",
                "hard_gate_allowed_false",
            ],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "recommended_extra_sources": unresolved_sources,
        "review": {
            "confidence": decision.get("confidence", "high"),
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
            },
            "open_questions": [
                "后续版本可补 CME 正式生产 iLink/MDP trade correction 或 trade cancellation 文档。",
                "后续版本可补更明确的 bad tick / condition flags / correction flags / sequence gap handling 文档。",
            ],
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": "; ".join(string_list(decision.get("reasons"))[:2]),
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
            "generic_mapping_notes": "Generated from Phase 37 public-source Trading Engineering Data Engineering candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get(
            "copyright",
            {
                "stores_full_text": False,
                "stores_long_quote": False,
                "summary_only": True,
                "license_notes": "仅保存来源链接、元数据和摘要，不保存长段原文。",
                "reuse_risk": "low",
            },
        ),
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
    return item, unresolved_sources


def write_knowledge(item: dict[str, Any]) -> Path:
    path = KNOWLEDGE_ROOT / str(item["metadata"]["partition_id"]) / sanitize_filename(str(item["knowledge_id"]))
    if path.exists():
        current = read_json(path)
        if deep_get(current, ("review", "review_status")) == "approved":
            raise ValueError(f"Refusing to overwrite approved item: {rel(path)}")
    write_json(path, item)
    return path


def append_log(candidate: dict[str, Any], entry: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(entry)


def update_candidate_formalized(candidate: dict[str, Any], item: dict[str, Any], knowledge_path: Path, decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "accepted"
    status["ingestion_decision"] = "accepted_for_draft"
    status["decision_reason"] = "再审允许 formal reviewed/caveat_only；已按 Phase 32/37 流程沉淀正式 reviewed 知识。"
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
            "next_action": "request_human_approval_if_default_guidance_is_needed",
            "allowed_next_decisions": ["request_human_approval", "keep_reviewed_caveat_only", "deprecate"],
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "knowledge_path": rel(knowledge_path),
        }
    )
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "reviewed"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["reviewed_allowed"] = True
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
        "required_extra_sources": decision.get("required_extra_sources", []),
    }
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "caveat_only"
    machine_gate["hidden_from_default_queue"] = True
    append_log(
        candidate,
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_data_engineering_formal_reviewed_created",
            "reason": f"{TASK_ID}: formal reviewed/caveat_only written to {rel(knowledge_path)}.",
            "audit_result_id": AUDIT_RESULT_ID,
        },
    )


def update_candidate_needs_more(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["decision_reason"] = "; ".join(string_list(decision.get("reasons"))[:2])
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "next_action": "inline_contract_then_reaudit",
            "allowed_next_decisions": ["accepted_for_reviewed_caveat_only", "needs_more_evidence", "rejected", "blocked"],
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
        }
    )
    review = candidate.setdefault("review", {})
    review["confidence"] = decision.get("confidence", "high")
    review["open_questions"] = dedupe_strings(
        as_list(review.get("open_questions"))
        + string_list(deep_get(decision, ("required_patches", "source"), []))
        + [str(source.get("path") or source.get("purpose") or source) for source in as_list(decision.get("required_extra_sources")) if isinstance(source, dict)]
    )
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "decision": "needs_more_evidence",
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "required_patches": decision.get("required_patches", {}),
        "required_extra_sources": decision.get("required_extra_sources", []),
        "reason": status["decision_reason"],
    }
    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["reason"] = "D11 再审仍需补 CEK-TA 内部契约正文；不得 formal reviewed、approved、default guidance 或 hard gate。"
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "blocked_until_contract_inline_reaudit"
    conversion["reviewed_allowed"] = False
    conversion["approved_allowed"] = False
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    append_log(
        candidate,
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase37_data_engineering_supplemental_reaudit_needs_more_evidence",
            "reason": f"{TASK_ID}: {status['decision_reason']}",
            "audit_result_id": AUDIT_RESULT_ID,
        },
    )


def main() -> int:
    source_path = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else AUDIT_RESULT_ARCHIVE_PATH
    audit_result = archive_audit_result(source_path)
    candidates = load_candidates()
    decisions = audit_result.get("decisions")
    if not isinstance(decisions, list) or len(decisions) != EXPECTED_TOTAL:
        raise ValueError(f"Expected {EXPECTED_TOTAL} audit decisions.")

    promoted: list[dict[str, Any]] = []
    needs_more: list[dict[str, Any]] = []
    written_knowledge_paths: list[str] = []
    touched_candidates: list[str] = []
    skipped = Counter()

    for decision in sorted(decisions, key=lambda item: str(item.get("research_task_id", ""))):
        if not isinstance(decision, dict):
            skipped["invalid_decision"] += 1
            continue
        task_id = str(decision.get("research_task_id", ""))
        candidate_entry = candidates.get(task_id)
        if not candidate_entry:
            skipped["candidate_missing"] += 1
            continue
        candidate_path, candidate = candidate_entry
        decision_value = decision.get("decision")
        if decision_value == "accepted_for_reviewed_caveat_only" and decision.get("reviewed_allowed") is True:
            item, unresolved_sources = candidate_to_knowledge(candidate, decision)
            knowledge_path = write_knowledge(item)
            update_candidate_formalized(candidate, item, knowledge_path, decision)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            written_knowledge_paths.append(rel(knowledge_path))
            promoted.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "knowledge_id": item["knowledge_id"],
                    "knowledge_path": rel(knowledge_path),
                    "canonical_node_id": item["metadata"]["canonical_node_id"],
                    "review_status": "reviewed",
                    "machine_gate": "caveat_only",
                    "unresolved_extra_source_count": len(unresolved_sources),
                    "approved_allowed": False,
                    "default_guidance_allowed": False,
                    "hard_gate_allowed": False,
                }
            )
        elif decision_value == "needs_more_evidence" and decision.get("reviewed_allowed") is False:
            update_candidate_needs_more(candidate, decision)
            write_json(candidate_path, candidate)
            touched_candidates.append(rel(candidate_path))
            needs_more.append(
                {
                    "candidate_id": candidate.get("candidate_id"),
                    "research_task_id": task_id,
                    "decision": "needs_more_evidence",
                    "reason": "; ".join(string_list(decision.get("reasons"))[:2]),
                    "next_action": "inline_contract_then_reaudit",
                    "required_patches": decision.get("required_patches", {}),
                    "required_extra_sources": decision.get("required_extra_sources", []),
                }
            )
        else:
            skipped[f"unsupported_decision_{decision_value}"] += 1

    if len(promoted) != EXPECTED_PROMOTED:
        raise ValueError(f"Expected {EXPECTED_PROMOTED} promoted items, got {len(promoted)}; skipped={dict(skipped)}")
    if len(needs_more) != EXPECTED_NEEDS_MORE:
        raise ValueError(f"Expected {EXPECTED_NEEDS_MORE} needs_more_evidence, got {len(needs_more)}")

    by_node = Counter(item["canonical_node_id"] for item in promoted)
    report = {
        "report_id": "phase37_data_engineering_blocked_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_path": rel(AUDIT_RESULT_ARCHIVE_PATH),
        "promoted_count": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "rejected_count": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "by_node": dict(sorted(by_node.items())),
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "touched_candidates": touched_candidates,
        "written_knowledge_paths": written_knowledge_paths,
        "skipped": dict(skipped),
        "boundary": "Only D10 became formal reviewed/caveat_only. D11 remains needs_more_evidence. No approved/default guidance/hard gate.",
        "next_action": "为 D11 生成包含内部 contract 正文的三审包，或在后续任务中继续补 OpenLineage/ML Metadata 证据。",
    }
    write_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
