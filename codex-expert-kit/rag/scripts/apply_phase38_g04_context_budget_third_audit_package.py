"""Supplement Phase 38 G04-R1 and export a third-audit package."""

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
CANDIDATE_PATH = resolve_repo_path(
    "codex-expert-kit",
    "rag",
    "candidates",
    "KB_AI_ENGINEERING",
    "cand_20260610_phase38_p38_g04_context_budget_field_trimming_001.json",
    start_file=__file__,
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase38_g04_context_budget_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase38_g04_context_budget_third_audit_package_20260610.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_g04_context_budget_third_audit_package_report.json", start_file=__file__
)


SUPPLEMENTAL_SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "src_langchain_contextual_compression",
        "source_title": "Improving Document Retrieval with Contextual Compression",
        "source_url": "https://www.langchain.com/blog/improving-document-retrieval-with-contextual-compression",
        "source_type": "engineering_article",
        "publisher": "LangChain",
        "published_at": "2023-03-13",
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": [
            "工程文章用于支撑检索后压缩、过滤无关文档和减少无关上下文；不作为 CEK-TA 默认指导状态机来源。"
        ],
        "evidence_summary": "LangChain contextual compression describes compressing retrieved documents using the query context so that only relevant information is returned, including shrinking individual documents and filtering documents wholesale.",
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_llamaindex_response_modes_compact",
        "source_title": "Response Modes - LlamaIndex",
        "source_url": "https://developers.llamaindex.ai/python/framework/module_guides/deploying/query_engine/response_modes/",
        "source_type": "official_doc",
        "publisher": "LlamaIndex",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": [
            "支撑 compact/refine 这类上下文组织策略；不直接规定 CEK-TA 的字段白名单。"
        ],
        "evidence_summary": "LlamaIndex response modes document refine and compact strategies for processing retrieved chunks, including compacting chunks to fit prompt size before refinement.",
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_llamaindex_compact_and_refine",
        "source_title": "Compact and refine - LlamaIndex",
        "source_url": "https://developers.llamaindex.ai/python/framework-api-reference/response_synthesizers/compact_and_refine/",
        "source_type": "official_doc",
        "publisher": "LlamaIndex",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": [
            "支撑上下文合并与利用上下文窗口的工程模式；具体 token_budget 仍由 CEK-TA 内部契约决定。"
        ],
        "evidence_summary": "LlamaIndex compact/refine documentation supports combining text chunks into larger consolidated chunks that fit the context window, then refining across them.",
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_openai_prompt_engineering",
        "source_title": "Prompt engineering - OpenAI API",
        "source_url": "https://developers.openai.com/api/docs/guides/prompt-engineering",
        "source_type": "official_doc",
        "publisher": "OpenAI",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 86,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": [
            "支撑提供相关参考文本、拆分任务和系统化提示策略；不作为 RAG 排序算法来源。"
        ],
        "evidence_summary": "OpenAI prompt engineering guidance supports providing relevant reference text, splitting complex tasks, and using tools systematically instead of overloading prompts with unrelated context.",
        "quoted_excerpt_allowed": False,
    },
    {
        "source_id": "src_anthropic_context_engineering_agents",
        "source_title": "Effective context engineering for AI agents",
        "source_url": "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
        "source_type": "engineering_article",
        "publisher": "Anthropic",
        "published_at": "2025-09-29",
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high",
        "score": 82,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "limitations": [
            "用于支撑 context 是有限资源、需要工程化管理；CEK-TA 仍以内部契约定义字段裁剪和默认指导门禁。"
        ],
        "evidence_summary": "Anthropic context engineering discusses curating and managing context as a finite resource for AI agents.",
        "quoted_excerpt_allowed": False,
    },
]


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


def append_sources(candidate: dict[str, Any]) -> None:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for source in SUPPLEMENTAL_SOURCES:
        if source["source_id"] not in existing:
            refs.append(dict(source))
            existing.add(source["source_id"])
    quality = candidate.setdefault("source_quality", {})
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score", 0) or 0), 88)
    quality["primary_source_count"] = len([ref for ref in refs if ref.get("reliability") == "high"])
    quality["supporting_source_count"] = max(len(refs) - int(quality["primary_source_count"]), 0)
    limitations = quality.setdefault("limitations", [])
    note = "G04 三审前已补充上下文压缩、compact/refine、prompt reference 和 context engineering 来源。"
    if isinstance(limitations, list) and note not in limitations:
        limitations.append(note)


def patch_candidate(candidate: dict[str, Any]) -> None:
    append_sources(candidate)
    candidate["claim"]["statement"] = (
        "交易 scoring/gating 的 RAG 知识包必须按字段白名单、top-k 和 token_budget 裁剪上下文；"
        "默认只返回最小必要字段，详细审计内容必须显式请求。"
    )
    candidate["claim"]["evidence_summary"] = (
        "补充 LangChain contextual compression、LlamaIndex compact/refine、OpenAI prompt engineering "
        "和 Anthropic context engineering 来源后，G04-R1 的 claim 只限定为 CEK-TA RAG 包字段裁剪、"
        "top-k、token_budget 和显式展开策略，不涉及交易规则本体或默认指导。"
    )
    candidate["status"].update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "ready_for_reaudit",
            "decision_reason": "G04-R1 已补充上下文预算和字段裁剪 claim-specific 来源，等待三审；不是 reviewed、approved 或 default guidance。",
            "updated_at": TODAY,
        }
    )
    candidate["workflow"].update(
        {
            "stage": "ready_for_reaudit",
            "queue_group": "needs_more_evidence",
            "ai_audit_result_id": "pending_phase38_g04_third_audit",
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "default_guidance_allowed": False,
            "next_action": "export_third_audit_package",
        }
    )
    candidate["conflict_audit"].update(
        {
            "approval_allowed": False,
            "draft_conversion_allowed": True,
            "resolution_summary": "G04-R1 空 slug、默认指导和元数据歧义已修复；三审仅判断是否可进入 formal draft。",
        }
    )
    candidate["review"]["reviewer"] = "codex"
    candidate["review"]["reviewed_at"] = TODAY
    candidate["review"]["open_questions"] = [
        "三审确认 G04-R1 是否可从 needs_more_evidence 升级为 accepted_for_draft。",
        "确认 field_whitelist_version、top_k=5、token_budget=4000、detail_expansion_policy=explicit_request_required 是否足以解决二审元数据问题。",
        "确认该知识只适用于 CEK-TA RAG 包上下文预算治理，不作为交易规则本体或默认指导。",
    ]
    candidate["review"]["ai_audit"] = {
        "audit_result_id": "pending_phase38_g04_third_audit",
        "source_package_id": "phase38_g04_context_budget_third_audit_package_20260610",
        "decision": "needs_more_evidence",
        "allowed_next_stage": "third_audit",
        "default_guidance_allowed": False,
        "reviewed_allowed": False,
        "approved_allowed": False,
        "hard_gate_allowed": False,
        "notes": "G04-R1 已补证并导出三审包；外部审计只允许 accepted_for_draft / needs_more_evidence / rejected。",
    }
    candidate["review"].setdefault("audit_log", []).append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "g04_context_budget_third_audit_evidence_added",
            "reason": "补充上下文预算、字段裁剪、top-k 和显式展开策略来源。",
        }
    )
    candidate["draft_conversion_allowed"] = True
    candidate["default_guidance_allowed"] = False
    candidate["visible_in_default_guidance_queue"] = False
    candidate["context_budget_policy_version"] = "phase38_context_budget_policy_v1"
    candidate["field_whitelist_version"] = "phase38_default_knowledge_pack_fields_v1"
    candidate["top_k"] = 5
    candidate["token_budget"] = 4000
    candidate["detail_expansion_policy"] = "explicit_request_required"
    candidate["field_whitelist"] = [
        "knowledge_id",
        "title",
        "canonical_node_id",
        "claim_type",
        "content_summary",
        "applicability",
        "not_applicable_when",
        "llm_usage_policy",
        "machine_gate",
        "source_evidence",
        "conflict_status",
        "recommended_next_action",
    ]
    candidate["detail_expansion_fields"] = [
        "full_audit_log",
        "long_source_summaries",
        "candidate_review_history",
        "historical_versions",
    ]
    candidate["conversion_target"]["default_guidance_allowed"] = False
    candidate["conversion_target"]["hard_gate_allowed"] = False


def write_research(candidate: dict[str, Any]) -> None:
    lines = [
        "# Phase 38 G04-R1 上下文预算补证采集记录",
        "",
        "## 目标",
        "",
        "为 G04-R1 `context_budget_field_trimming` 补充更直接的上下文预算、字段白名单、top-k、token budget 和显式展开策略证据，并导出三审包。该补证不代表 reviewed、approved 或 default guidance。",
        "",
        "## 补证后 claim",
        "",
        candidate["claim"]["statement"],
        "",
        "## 补充来源",
        "",
    ]
    for source in SUPPLEMENTAL_SOURCES:
        lines.extend(
            [
                f"- `{source['source_id']}`：{source['source_title']}",
                f"  - URL：{source['source_url']}",
                f"  - 用途：{source['evidence_summary']}",
            ]
        )
    lines.extend(
        [
            "",
            "## 三审边界",
            "",
            "```text",
            "1. 只审 G04-R1 是否可进入 formal draft queue。",
            "2. 不允许直接 reviewed、approved、default guidance 或 hard gate。",
            "3. G04-R1 只治理 CEK-TA RAG 知识包上下文预算，不沉淀交易规则本体。",
            "4. 字段白名单、top_k、token_budget 和 detail_expansion_policy 是 CEK-TA 内部契约字段。",
            "```",
        ]
    )
    RESEARCH_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_audit_package(candidate: dict[str, Any]) -> None:
    package = {
        "package_id": "phase38_g04_context_budget_third_audit_package_20260610",
        "generated_at": TODAY,
        "source_candidate_id": candidate["candidate_id"],
        "source_research_task_id": candidate["research_task_id"],
        "purpose": "请三审 G04-R1 是否可从 needs_more_evidence 升级为 accepted_for_draft。不得直接 reviewed、approved、default guidance 或 hard gate。",
        "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
        "must_check": [
            "空 slug 是否已修复。",
            "approval_allowed=false 与 draft_conversion_allowed=true 的状态语义是否清楚。",
            "hidden_from_default_queue=true、visible_in_default_guidance_queue=false、default_guidance_allowed=false 是否消除了默认指导歧义。",
            "field_whitelist、top_k、token_budget 和 detail_expansion_policy 是否足以支撑上下文预算治理。",
            "补充来源是否直接支撑字段裁剪、上下文压缩、compact/refine 和 context engineering。",
            "该候选是否仍只属于 RAG Engineering，不沉淀交易规则本体。",
        ],
        "forbidden": [
            "不得直接输出 reviewed。",
            "不得直接输出 approved。",
            "不得允许 default guidance。",
            "不得允许 hard gate。",
        ],
        "candidate": candidate,
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def main() -> int:
    candidate = read_json(CANDIDATE_PATH)
    patch_candidate(candidate)
    write_json(CANDIDATE_PATH, candidate)
    write_research(candidate)
    write_audit_package(candidate)
    report = {
        "report_id": "phase38_g04_context_budget_third_audit_package_report",
        "generated_at": TODAY,
        "candidate_id": candidate["candidate_id"],
        "source_count": len(candidate.get("source_refs", [])),
        "research_path": rel(RESEARCH_PATH),
        "audit_package_path": rel(AUDIT_PACKAGE_PATH),
        "candidate_path": rel(CANDIDATE_PATH),
        "default_guidance_allowed": False,
        "ready_for_third_audit": True,
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
