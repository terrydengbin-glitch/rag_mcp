"""Add supplemental evidence to Phase 38 P0-Core needs-more-evidence candidates.

The script keeps candidates in the supplemental audit queue. It prepares them
for second review but does not mark them reviewed or approved.
"""

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


TODAY = date(2026, 6, 10).isoformat()
CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase38_p0_core_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase38_p0_core_supplemental_audit_package_20260610.json", start_file=__file__
)


SOURCES: dict[str, dict[str, Any]] = {
    "json_schema": {
        "source_id": "src_json_schema_docs",
        "source_title": "JSON Schema Documentation",
        "source_url": "https://json-schema.org/docs",
        "source_type": "official_doc",
        "publisher": "JSON Schema",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "JSON Schema documentation supports declarative validation of JSON object structure, required fields, data types, and enum-like constraints.",
        "quoted_excerpt_allowed": False,
    },
    "openai_structured_outputs": {
        "source_id": "src_openai_structured_outputs",
        "source_title": "Structured model outputs - OpenAI API",
        "source_url": "https://developers.openai.com/api/docs/guides/structured-outputs",
        "source_type": "official_doc",
        "publisher": "OpenAI",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "OpenAI Structured Outputs supports making model responses adhere to supplied JSON Schema, reducing missing required keys and invalid enum values.",
        "quoted_excerpt_allowed": False,
    },
    "owasp_prompt_injection": {
        "source_id": "src_owasp_prompt_injection",
        "source_title": "LLM01:2025 Prompt Injection - OWASP Gen AI Security Project",
        "source_url": "https://genai.owasp.org/llmrisk/llm01-prompt-injection/",
        "source_type": "standard_or_risk_framework",
        "publisher": "OWASP",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "OWASP prompt injection guidance supports treating RAG context and user-controlled natural language as untrusted input that can manipulate model behavior.",
        "quoted_excerpt_allowed": False,
    },
    "ragas_faithfulness": {
        "source_id": "src_ragas_faithfulness",
        "source_title": "Faithfulness - Ragas",
        "source_url": "https://docs.ragas.io/en/v0.1.21/concepts/metrics/faithfulness.html",
        "source_type": "official_doc",
        "publisher": "Ragas",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Ragas faithfulness measures factual consistency of an answer against retrieved context, supporting grounded RAG evaluation.",
        "quoted_excerpt_allowed": False,
    },
    "deepeval_faithfulness": {
        "source_id": "src_deepeval_faithfulness",
        "source_title": "Faithfulness - DeepEval",
        "source_url": "https://deepeval.com/docs/metrics-faithfulness",
        "source_type": "official_doc",
        "publisher": "DeepEval",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 80,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "DeepEval faithfulness metric supports evaluating whether generated claims are grounded in retrieved context.",
        "quoted_excerpt_allowed": False,
    },
    "open_bandit_pipeline": {
        "source_id": "src_open_bandit_pipeline",
        "source_title": "Open Bandit Pipeline documentation",
        "source_url": "https://zr-obp.readthedocs.io/en/latest/",
        "source_type": "official_doc",
        "publisher": "Open Bandit Pipeline",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Open Bandit Pipeline supports off-policy evaluation using logged bandit feedback to estimate performance of a target policy without direct online deployment.",
        "quoted_excerpt_allowed": False,
    },
    "sklearn_threshold": {
        "source_id": "src_sklearn_threshold_tuning",
        "source_title": "Tuning the decision threshold for class prediction - scikit-learn",
        "source_url": "https://scikit-learn.org/stable/modules/classification_threshold.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "evidence_summary": "scikit-learn documents threshold tuning as a separate decision step from probability estimation and warns that the metric should fit the use case.",
        "quoted_excerpt_allowed": False,
    },
    "phase35_active_retrieval": {
        "source_id": "src_cek_ta_phase35_active_retrieval_protocol",
        "source_title": "CEK-TA Phase 35 External AI Active Retrieval Protocol",
        "source_url": "docs/contracts/external_ai_active_retrieval_protocol.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "CEK-TA Phase 35 defines when external project AI must search CEK-TA, how to cite results, and how to handle no-hit outcomes.",
        "quoted_excerpt_allowed": False,
    },
    "phase38_rag_contract": {
        "source_id": "src_cek_ta_phase38_rag_citation_reason_contract",
        "source_title": "Phase 38 RAG 引用、Reason Taxonomy 与默认指导门禁契约",
        "source_url": "docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "CEK-TA Phase 38 contract defines formal index schema, citation resolver, no-hit abstain, unsupported_claims routing, reason_code taxonomy, machine_gate eligibility, and context budget trimming.",
        "quoted_excerpt_allowed": False,
    },
    "phase38_runtime_contract": {
        "source_id": "src_cek_ta_phase38_runtime_contract",
        "source_title": "Phase 38 AI scoring gate runtime contract",
        "source_url": "docs/contracts/phase38_ai_scoring_gate_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "CEK-TA Phase 38 runtime contract separates numeric scorer, LLM audit assistant, and deterministic final gate responsibilities.",
        "quoted_excerpt_allowed": False,
    },
}


PATCHES: dict[str, dict[str, Any]] = {
    "P38-D03": {
        "sources": ["phase38_rag_contract", "phase35_active_retrieval", "json_schema"],
        "patch": "knowledge_refs 必须解析到 formal index；解析失败时 recommendation 必须降级为 abstain/neutral，并触发人工复核。",
    },
    "P38-D04": {
        "sources": ["phase38_rag_contract", "ragas_faithfulness", "deepeval_faithfulness", "owasp_prompt_injection"],
        "patch": "no-hit 或无来源时不得默认生成指导；应输出 neutral/abstain，并记录缺口和查询上下文。",
    },
    "P38-D05": {
        "sources": ["phase38_rag_contract", "ragas_faithfulness", "owasp_prompt_injection"],
        "patch": "unsupported_claims 非空时不得默认 allow；应进入补证、人工复核或阻断队列。",
    },
    "P38-D06": {
        "sources": ["phase38_rag_contract", "json_schema", "openai_structured_outputs"],
        "patch": "reason_codes 必须来自受控 taxonomy v1，并通过 schema enum 校验；未知 code 必须降级和人工复核。",
    },
    "P38-E01": {
        "sources": ["open_bandit_pipeline", "sklearn_threshold", "phase38_runtime_contract"],
        "patch": "historical offline eval 只能可靠评估已执行交易真实结果；未执行、blocked、skipped candidate 属于反事实，除非存在 shadow、paper、replay、OPE 或其他可观测/可估计机制。",
        "statement": "historical offline eval 只能可靠评估已执行交易真实结果；未执行、blocked、skipped candidate 属于反事实，除非存在 shadow、paper、replay、OPE 或其他可观测/可估计机制。",
        "normalized_claim": "phase38.offline_eval_counterfactual_boundary.v1",
    },
    "P38-G01": {
        "sources": ["phase35_active_retrieval", "phase38_rag_contract", "phase38_runtime_contract"],
        "patch": "scoring/gating 任务属于必须主动检索 CEK-TA 的高风险任务；无命中时必须声明 no-hit，不得凭空补规则。",
    },
    "P38-G03": {
        "sources": ["phase38_rag_contract", "phase35_active_retrieval", "json_schema"],
        "patch": "默认指导必须同时满足 approved、approval_status approved、machine_gate allow、无冲突和有来源；reviewed 只能 caveat 或审计参考。",
    },
    "P38-G04-R1": {
        "sources": ["phase38_rag_contract", "phase35_active_retrieval", "owasp_prompt_injection"],
        "patch": "知识包默认只返回最小必要字段；详细审计必须显式请求，并保留 top-k、字段白名单和 token budget。",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    indexed: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        item = read_json(path)
        task_id = item.get("research_task_id")
        if isinstance(task_id, str):
            indexed[task_id] = (path, item)
    return indexed


def add_sources(candidate: dict[str, Any], source_keys: list[str]) -> None:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for key in source_keys:
        source = dict(SOURCES[key])
        if source["source_id"] not in existing:
            refs.append(source)
            existing.add(source["source_id"])
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score", 0) or 0), 86)
    quality["primary_source_count"] = len([ref for ref in refs if ref.get("reliability") == "high"])
    quality["supporting_source_count"] = max(len(refs) - int(quality["primary_source_count"]), 0)
    limitations = quality.setdefault("limitations", [])
    note = "已按 Phase 38 严格审计补充 claim-specific 外部来源和 CEK-TA 内部契约；仍需二审后才能进入 formal draft。"
    if isinstance(limitations, list) and note not in limitations:
        limitations.append(note)


def patch_candidate(task_id: str, path: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    patch = PATCHES[task_id]
    add_sources(candidate, patch["sources"])
    claim = candidate.setdefault("claim", {})
    if "statement" in patch:
        claim["statement"] = patch["statement"]
    if "normalized_claim" in patch:
        claim["normalized_claim"] = patch["normalized_claim"]
        candidate.setdefault("conversion_target", {})["proposed_knowledge_id"] = (
            "kb_ai_engineering." + patch["normalized_claim"]
        )
    claim["evidence_summary"] = patch["patch"]
    review = candidate.setdefault("review", {})
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = ["补证已完成，等待外部 AI/人工二审确认是否可进入 formal draft。"]
    review.setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "supplemental_evidence_added",
            "reason": patch["patch"],
        }
    )
    review.setdefault("ai_audit", {})["supplemental_evidence_status"] = "ready_for_reaudit"
    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已补证，等待二审；不是 reviewed、approved 或 default guidance。"
    status["updated_at"] = TODAY
    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "ready_for_reaudit"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "export_supplemental_audit_package"
    workflow["hidden_from_default_queue"] = False
    checked = candidate.setdefault("conflict_audit", {}).setdefault("checked_against", [])
    contract = "docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md"
    if isinstance(checked, list) and contract not in checked:
        checked.append(contract)
    write_json(path, candidate)
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": task_id,
        "claim": claim.get("statement"),
        "normalized_claim": claim.get("normalized_claim"),
        "source_count": len(candidate.get("source_refs", [])),
        "patch_summary": patch["patch"],
        "source_ids": [SOURCES[key]["source_id"] for key in patch["sources"]],
        "path": rel(path),
    }


def write_research_doc(items: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 38 P0-Core 补证采集记录",
        "",
        "## 目标",
        "",
        "根据 Phase 38 P0-Core 严格审计报告，为 7 条 needs_more_evidence 候选和 1 条重建 G04 补充 claim-specific 外部来源与 CEK-TA 内部契约。本记录只用于二审准备，不代表 reviewed、approved 或 default guidance。",
        "",
        "## 补证结果",
        "",
    ]
    for item in items:
        lines.extend(
            [
                f"### {item['research_task_id']} - {item['candidate_id']}",
                "",
                f"- 补丁摘要：{item['patch_summary']}",
                f"- 来源数量：{item['source_count']}",
                f"- 来源 ID：{', '.join(item['source_ids'])}",
                f"- 候选路径：`{item['path']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## 边界",
            "",
            "```text",
            "1. 补证完成不等于审计通过。",
            "2. 本批候选仍停留在 needs_more_evidence / ready_for_reaudit。",
            "3. 二审通过后才允许进入 formal draft 队列。",
            "4. 任何候选都不能直接进入 reviewed、approved 或 default guidance。",
            "```",
        ]
    )
    RESEARCH_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_audit_package(items: list[dict[str, Any]]) -> None:
    candidates = []
    for item in items:
        candidates.append(read_json(resolve_repo_path(item["path"], start_file=__file__)))
    package = {
        "package_id": "phase38_p0_core_supplemental_audit_package_20260610",
        "generated_at": TODAY,
        "source_audit_result_id": "audit_result_phase38_p0_core_20260610_strict_v1",
        "purpose": "请复审 Phase 38 P0-Core 补证候选，判断是否可从 needs_more_evidence 升级为 accepted_for_draft。不要直接标记 reviewed、approved 或 default guidance。",
        "candidate_count": len(candidates),
        "review_instructions": {
            "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
            "must_check": [
                "来源是否直接支撑 claim。",
                "CEK-TA 内部契约是否足以支撑 D/G 组规则。",
                "E01 是否已经避免绝对化反事实表述。",
                "G04 是否已修复空 slug，且仍不进入默认指导。",
            ],
            "forbidden": [
                "不得直接输出 reviewed。",
                "不得直接输出 approved。",
                "不得允许 default guidance。",
            ],
        },
        "candidates": candidates,
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def main() -> int:
    indexed = load_candidates()
    missing = sorted(set(PATCHES) - set(indexed))
    if missing:
        raise SystemExit(f"Missing candidates for supplemental evidence: {missing}")
    results = []
    for task_id in sorted(PATCHES):
        path, candidate = indexed[task_id]
        results.append(patch_candidate(task_id, path, candidate))
    write_research_doc(results)
    write_audit_package(results)
    print(
        json.dumps(
            {
                "supplemented": len(results),
                "research_path": rel(RESEARCH_PATH),
                "audit_package_path": rel(AUDIT_PACKAGE_PATH),
                "items": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
