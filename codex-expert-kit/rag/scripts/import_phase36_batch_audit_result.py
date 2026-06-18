"""Import one Phase 36 batch audit result and create reviewed knowledge.

The input format is the batch audit result returned by the external reviewer:

{
  "audit_result_id": "...",
  "source_package_id": "phase36_ai_engineering_candidate_audit_batch_01_of_10_20260609",
  "decisions": [...]
}

This script does not create approved knowledge. Accepted candidates become
formal reviewed knowledge with machine_gate=caveat_only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 9).isoformat()
CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_DIR = resolve_repo_path("docs", "audit", start_file=__file__)
REPORT_DIR = resolve_repo_path("docs", "reports", start_file=__file__)


CLAIM_TYPE_BY_PREFIX = {
    "approval": "ai_governance_rule",
    "audit": "ai_governance_rule",
    "business_objective": "ai_governance_rule",
    "calibration": "llm_eval_rule",
    "capability_boundary": "ai_governance_rule",
    "data_asset": "training_data_schema_rule",
    "data_license": "ai_governance_rule",
    "data_privacy": "ai_security_rule",
    "dataset": "training_data_schema_rule",
    "deployment": "llmops_release_rule",
    "eval": "llm_eval_rule",
    "feature_schema": "training_data_schema_rule",
    "gating": "risk_boundary_rule",
    "governance": "ai_governance_rule",
    "label_schema": "training_data_schema_rule",
    "leakage": "data_quality_rule",
    "llm_role_boundary": "risk_boundary_rule",
    "mcp": "mcp_contract_rule",
    "method_selection": "llm_training_rule",
    "rag": "rag_governance_rule",
    "runtime": "risk_boundary_rule",
    "safety": "ai_security_rule",
    "serving_consistency": "llmops_release_rule",
    "training_objective": "llm_training_rule",
}

SUPPLEMENTAL_SOURCE_RULES = [
    (
        "2026",
        {
            "source_id": "src_occ_fed_fdic_revised_model_risk_2026",
            "source_title": "Model Risk Management: Revised Guidance",
            "source_url": "https://occ.gov/news-issuances/bulletins/2026/bulletin-2026-13.html",
            "source_type": "standard_or_risk_framework",
            "publisher": "OCC / Federal Reserve / FDIC",
            "published_at": "2026-04-17",
            "accessed_at": TODAY,
            "version": "OCC Bulletin 2026-13 / SR 26-2",
            "reliability": "high",
            "relevance": "medium",
            "evidence_summary": "2026 年跨机构模型风险管理修订指南支持模型治理、验证、变更控制和风险分层；同时需注明 generative AI 和 agentic AI 不在其直接范围内，只能作为模型风险治理类比来源。",
            "quoted_excerpt_allowed": False,
        },
    ),
    (
        "FINRA",
        {
            "source_id": "src_finra_regulatory_notice_15_09",
            "source_title": "FINRA Regulatory Notice 15-09",
            "source_url": "https://www.finra.org/industry/notices/15-09",
            "source_type": "standard_or_risk_framework",
            "publisher": "FINRA",
            "published_at": "2015-03-01",
            "accessed_at": TODAY,
            "version": "Regulatory Notice 15-09",
            "reliability": "high",
            "relevance": "medium",
            "evidence_summary": "FINRA 15-09 支持自动化交易系统的监督、测试、控制、变更和合规治理要求，适合作为交易自动化治理类来源。",
            "quoted_excerpt_allowed": False,
        },
    ),
    (
        "SageMaker",
        {
            "source_id": "src_aws_sagemaker_shadow_tests",
            "source_title": "Shadow tests - Amazon SageMaker AI",
            "source_url": "https://docs.aws.amazon.com/sagemaker/latest/dg/shadow-tests.html",
            "source_type": "official_doc",
            "publisher": "AWS",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "relevance": "medium",
            "evidence_summary": "AWS SageMaker shadow testing 支持在不影响生产决策的情况下复制请求并比较候选模型表现，适合作为 shadow/promotion gate 的工程来源。",
            "quoted_excerpt_allowed": False,
        },
    ),
    (
        "NIST Privacy",
        {
            "source_id": "src_nist_privacy_framework",
            "source_title": "NIST Privacy Framework",
            "source_url": "https://www.nist.gov/privacy-framework",
            "source_type": "standard_or_risk_framework",
            "publisher": "NIST",
            "published_at": None,
            "accessed_at": TODAY,
            "version": "NIST Privacy Framework 1.x",
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "NIST Privacy Framework 支持企业级隐私风险管理、隐私治理和隐私控制，适合支撑训练导出前的隐私与脱敏 gate。",
            "quoted_excerpt_allowed": False,
        },
    ),
    (
        "Sensitive Information Disclosure",
        {
            "source_id": "src_owasp_llm_sensitive_information_disclosure",
            "source_title": "OWASP Top 10 for LLM Applications",
            "source_url": "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
            "source_type": "standard_or_risk_framework",
            "publisher": "OWASP",
            "published_at": None,
            "accessed_at": TODAY,
            "version": None,
            "reliability": "high",
            "relevance": "high",
            "evidence_summary": "OWASP LLM Top 10 覆盖敏感信息泄露等风险，适合支撑 secret、PII、账号标识不得进入训练导出的安全规则。",
            "quoted_excerpt_allowed": False,
        },
    ),
]


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def prefix_for(knowledge_id: str) -> str:
    return knowledge_id.split(".", 1)[0]


def normalize_title(statement: str, fallback: str) -> str:
    compact = re.sub(r"\s+", " ", statement).strip()
    return compact[:58] if compact else fallback


def candidate_paths() -> dict[str, Path]:
    indexed = {}
    for path in CANDIDATE_ROOT.glob("**/*.json"):
        item = read_json(path)
        candidate_id = item.get("candidate_id")
        if isinstance(candidate_id, str):
            indexed[candidate_id] = path
    return indexed


def source_to_evidence(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": source.get("source_id", ""),
        "source_title": source.get("source_title") or source.get("title", ""),
        "source_url": source.get("source_url") or source.get("url"),
        "source_type": source.get("source_type", "other"),
        "publisher": source.get("publisher"),
        "published_at": source.get("published_at"),
        "accessed_at": source.get("accessed_at", TODAY),
        "version": source.get("version"),
        "reliability": source.get("reliability", "medium"),
        "relevance": source.get("relevance", "medium"),
        "evidence_summary": source.get("evidence_summary", ""),
        "quoted_excerpt_allowed": bool(source.get("quoted_excerpt_allowed", False)),
    }


def supplemental_sources(decision: dict[str, Any]) -> list[dict[str, Any]]:
    text = json.dumps(decision, ensure_ascii=False)
    sources = []
    seen = set()
    for marker, source in SUPPLEMENTAL_SOURCE_RULES:
        if marker in text and source["source_id"] not in seen:
            sources.append(dict(source))
            seen.add(source["source_id"])
    return sources


def audit_notes(decision: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "source_patch_notes": list(decision.get("source_patch_notes") or []),
        "content_patch_notes": list(decision.get("content_patch_notes") or []),
        "boundary_patch_notes": list(decision.get("boundary_patch_notes") or []),
        "conflict_patch_notes": list(decision.get("conflict_patch_notes") or []),
        "required_followups": list(decision.get("required_followups") or []),
    }


def update_candidate(candidate: dict[str, Any], audit: dict[str, Any], decision: dict[str, Any]) -> None:
    status = candidate.setdefault("status", {})
    review = candidate.setdefault("review", {})
    workflow = candidate.setdefault("workflow", {})
    audit_log = review.setdefault("audit_log", [])
    decision_value = decision["decision"]

    if decision_value == "accepted_for_draft":
        status["review_status"] = "accepted"
        workflow["stage"] = "ai_audited"
        workflow["queue_group"] = "ai_passed"
        workflow["hidden_from_default_queue"] = True
        workflow["next_action"] = "apply_ai_audit_patch"
    elif decision_value == "needs_more_evidence":
        status["review_status"] = "needs_more_evidence"
        workflow["stage"] = "needs_more_evidence"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["hidden_from_default_queue"] = False
        workflow["next_action"] = "export_ai_audit"
    else:
        status["review_status"] = "rejected"
        workflow["stage"] = "rejected"
        workflow["queue_group"] = "rejected"
        workflow["hidden_from_default_queue"] = True
        workflow["next_action"] = "none"

    status["updated_at"] = TODAY
    status["decision_reason"] = f"Phase 36 batch AI audit decision: {decision_value}. 该状态不是 approved。"
    review["reviewer"] = "external_ai_and_codex_alignment"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": audit["audit_result_id"],
        "source_package_id": audit["source_package_id"],
        "decision": decision_value,
        "reason": decision.get("reason", ""),
        **audit_notes(decision),
        "boundary": "accepted_for_draft 不是 approved；reviewed 不会进入默认指导。",
    }
    workflow["ai_audit_result_id"] = audit["audit_result_id"]
    if isinstance(audit_log, list):
        audit_log.append(
            {
                "at": TODAY,
                "actor": "external_ai",
                "action": "phase36_batch_audit_result_received",
                "reason": decision.get("reason", ""),
                "audit_result_id": audit["audit_result_id"],
            }
        )


def build_content(candidate: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    claim = candidate["claim"]
    notes = audit_notes(decision)
    return {
        "statement": claim["statement"],
        "rationale": (
            f"{claim.get('interpretation_notes', '')} 审计结论：{decision.get('reason', '')}"
        ).strip(),
        "procedure": [
            "确认项目事实匹配 applies_when，且没有命中 not_applicable_when。",
            "按 source_patch_notes 检查来源是否足够支撑 statement。",
            "按 content_patch_notes 补齐正式实现、schema、字段和 checklist。",
            "按 boundary_patch_notes 确认没有把交易规则本体、项目私有参数或实盘执行规则写入 AI Engineering。",
            "保留 required_followups，后续由来源增强或治理任务继续关闭。",
        ],
        "examples": [],
        "anti_patterns": [
            "把 reviewed 知识当作 approved 默认指导。",
            "把 AI Engineering 规则扩写成具体交易阈值、仓位、买卖点或执行参数。",
            "忽略审计结果中的来源限制、适用范围和后续补强要求。",
        ],
        "validation": [
            "source_evidence 至少 2 条，且没有 low-only 来源。",
            "conflict_status 为 none 或 resolved。",
            "review_status 为 reviewed 时 machine_gate 必须是 caveat_only。",
            "MCP/SearchLab 默认指导不得把本条当作 approved 返回。",
        ],
        "risk_notes": (
            list(candidate.get("applicability", {}).get("limitations") or [])
            + notes["boundary_patch_notes"]
            + notes["conflict_patch_notes"]
            + notes["required_followups"]
        ),
        "citation_notes": claim.get("evidence_summary", ""),
        "audit_patch_notes": notes,
    }


def build_knowledge(candidate: dict[str, Any], audit: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    classification = candidate["classification"]
    applicability = candidate["applicability"]
    review = candidate["review"]
    conversion = candidate["conversion_target"]
    claim = candidate["claim"]
    knowledge_id = conversion["proposed_knowledge_id"]
    prefix = prefix_for(claim["normalized_claim"])
    source_evidence = [source_to_evidence(source) for source in candidate.get("source_refs", [])]
    existing_ids = {source["source_id"] for source in source_evidence}
    for source in supplemental_sources(decision):
        if source["source_id"] not in existing_ids:
            source_evidence.append(source)
            existing_ids.add(source["source_id"])

    reliability_scores = {"high": 90, "medium": 70, "low": 40}
    avg_score = round(sum(reliability_scores.get(src.get("reliability"), 60) for src in source_evidence) / len(source_evidence))
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": normalize_title(claim.get("statement", ""), claim["normalized_claim"]),
        "metadata": {
            "partition_id": classification["partition_id"],
            "domain": classification["domain"],
            "subdomain": classification["subdomain"],
            "rule_type": classification["rule_type"],
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification["tree_node_id"],
            "tree_path": classification["tree_path"],
            "canonical_node_id": classification.get("canonical_node_id") or classification["tree_node_id"],
            "canonical_tree_path": classification["tree_path"],
            "risk_level": "high" if prefix in {"approval", "data_privacy", "data_license", "runtime"} else "medium",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate["candidate_id"],
            "research_task_id": candidate.get("research_task_id", ""),
            "claim_type": CLAIM_TYPE_BY_PREFIX.get(prefix, "ai_governance_rule"),
            "classification_notes": "Phase 36 AI Engineering reviewed knowledge; UI tree and canonical node are inherited from candidate classification. Trading rule bodies must remain in Trading Engineering.",
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "trading_llm_assistant"),
            "applies_when": applicability["applies_when"],
            "not_applicable_when": applicability["not_applicable_when"],
        },
        "content": build_content(candidate, decision),
        "assumptions": applicability["assumptions"],
        "source_evidence": source_evidence,
        "source_quality": {
            "overall_reliability": "high" if avg_score >= 80 else "medium",
            "score": avg_score,
            "score_version": "1.0.0",
            "primary_source_count": min(2, len(source_evidence)),
            "supporting_source_count": max(0, len(source_evidence) - 2),
            "low_reliability_source_count": 0,
            "limitations": [
                "本条为 reviewed 知识，来源和审计补丁已记录；默认指导仍需后续人工治理升级 approved。"
            ],
        },
        "conflict_audit": {
            "conflict_status": candidate["conflict_audit"]["conflict_status"],
            "checked_against": candidate["conflict_audit"].get("checked_against", []),
            "conflicts": candidate["conflict_audit"].get("conflicts", []),
            "resolution_summary": candidate["conflict_audit"].get("resolution_summary", ""),
            "default_recommendation": "caveat_only_until_approved",
        },
        "review": {
            "confidence": review["confidence"],
            "freshness": review["freshness"],
            "review_status": "reviewed",
            "reviewer": "codex",
            "reviewed_at": TODAY,
            "created_at": candidate["status"].get("created_at", TODAY),
            "updated_at": TODAY,
            "open_questions": list(review.get("open_questions") or []) + list(decision.get("required_followups") or []),
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai",
                    "decision": "accepted_for_draft",
                    "reason": decision.get("reason", ""),
                    "audit_result_id": audit["audit_result_id"],
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "decision": "converted_to_reviewed",
                    "reason": "按 Phase 36 批量审计结果优化候选并转为 formal reviewed；未升级 approved。",
                    "audit_result_id": audit["audit_result_id"],
                },
            ],
            "approval_status": "not_requested",
            "default_guidance_allowed": False,
            "source_candidate_id": candidate["candidate_id"],
            "ai_audit_result_id": audit["audit_result_id"],
            "ai_audit": {
                "audit_result_id": audit["audit_result_id"],
                "source_package_id": audit["source_package_id"],
                "decision": decision["decision"],
                "reason": decision.get("reason", ""),
                **audit_notes(decision),
            },
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Phase 36 public-source AI Engineering candidate; no project-private trading facts included.",
        },
        "copyright": candidate.get("copyright", {}),
        "llm_usage_policy": {
            "allowed": [
                "用于审计 AI Engineering、LLM 训练、RAG/MCP、部署、安全或治理链路。",
                "用于提醒外接项目补齐来源、适用边界、冲突状态、审计记录和人工审批。",
                "用于 reviewed/audit 模式下带 caveat 引用。"
            ],
            "not_allowed": [
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行指令。",
                "不得覆盖确定性风控、交易执行系统或人工审批。",
                "不得作为 approved/default guidance 直接返回。"
            ],
            "required_context": [
                "project_type",
                "task_type",
                "mode",
                "strategy_version",
                "data_boundary",
                "review_status"
            ],
            "fallback_behavior": "cite_with_caveat",
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "reason": "reviewed only; accepted_for_draft is not approved; default guidance requires later human governance approval.",
            "requires_human_escalation": True,
            "blocking_reasons": ["not_approved", "phase36_batch_reviewed_only"],
            "checked_at": TODAY,
            "gate_version": "1.0.0",
        },
        "recommended_extra_sources": [
            {
                "title": note,
                "source_url": None,
                "source_type": "other",
                "purpose": "来自第一批外部审计结果的来源补强建议。",
                "status": "proposed",
            }
            for note in decision.get("source_patch_notes", [])
        ],
    }


def target_path(item: dict[str, Any]) -> Path:
    return KNOWLEDGE_ROOT / item["metadata"]["partition_id"] / f"{item['knowledge_id']}.json"


def import_audit_result(input_path: Path) -> dict[str, Any]:
    audit = read_json(input_path)
    if "decisions" not in audit:
        raise ValueError("audit result must contain decisions[]")

    stored_audit_path = AUDIT_DIR / f"{audit['audit_result_id']}.json"
    write_json(stored_audit_path, audit)

    by_candidate = candidate_paths()
    imported_candidates = []
    reviewed_items = []
    needs_more_evidence = []
    rejected = []
    skipped = []

    for decision in audit["decisions"]:
        candidate_id = decision.get("candidate_id")
        candidate_path = by_candidate.get(candidate_id)
        if candidate_path is None:
            skipped.append({"candidate_id": candidate_id, "reason": "candidate_not_found"})
            continue
        candidate = read_json(candidate_path)
        update_candidate(candidate, audit, decision)
        write_json(candidate_path, candidate)
        imported_candidates.append(rel(candidate_path))

        if decision["decision"] == "accepted_for_draft":
            item = build_knowledge(candidate, audit, decision)
            path = target_path(item)
            if path.exists():
                existing = read_json(path)
                existing_status = existing.get("review", {}).get("review_status")
                if existing_status == "approved":
                    skipped.append({"candidate_id": candidate_id, "reason": "refuse_overwrite_approved"})
                    continue
            write_json(path, item)
            candidate["workflow"]["stage"] = "formalized_reviewed"
            candidate["workflow"]["queue_group"] = "formalized"
            candidate["workflow"]["formal_knowledge_id"] = item["knowledge_id"]
            candidate["workflow"]["formal_review_status"] = "reviewed"
            candidate["workflow"]["next_action"] = "monitor_reviewed_quality"
            write_json(candidate_path, candidate)
            reviewed_items.append(rel(path))
        elif decision["decision"] == "needs_more_evidence":
            needs_more_evidence.append(candidate_id)
        else:
            rejected.append(candidate_id)

    batch_match = re.search(r"batch_(\d+)_of_(\d+)", audit["source_package_id"])
    if batch_match:
        batch_report_stem = f"phase36_batch_{batch_match.group(1)}_audit_import_report"
    else:
        safe_result_id = re.sub(r"[^a-zA-Z0-9_]+", "_", audit["audit_result_id"])
        batch_report_stem = f"{safe_result_id}_import_report"

    report = {
        "report_id": batch_report_stem,
        "audit_result_id": audit["audit_result_id"],
        "source_package_id": audit["source_package_id"],
        "stored_audit_path": rel(stored_audit_path),
        "decision_count": len(audit["decisions"]),
        "reviewed_count": len(reviewed_items),
        "needs_more_evidence_count": len(needs_more_evidence),
        "rejected_count": len(rejected),
        "updated_candidates": imported_candidates,
        "created_or_updated_reviewed_knowledge": reviewed_items,
        "needs_more_evidence": needs_more_evidence,
        "rejected": rejected,
        "skipped": skipped,
        "boundary": "accepted_for_draft -> formal reviewed only; no approved/default guidance created.",
    }
    report_path = REPORT_DIR / f"{batch_report_stem}.json"
    write_json(report_path, report)
    report["report_path"] = rel(report_path)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_result_path", help="Path to Phase 36 batch audit result JSON.")
    args = parser.parse_args()
    input_path = Path(args.audit_result_path)
    if not input_path.is_absolute():
        input_path = resolve_repo_path(*input_path.parts, start_file=__file__)
    report = import_audit_result(input_path)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["skipped"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
