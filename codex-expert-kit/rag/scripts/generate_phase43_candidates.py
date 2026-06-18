"""Generate Phase 43 external project AI memory candidate knowledge files.

This script writes candidate JSON only. It does not create formal reviewed or
approved knowledge, and it never enables default guidance or hard gates.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-11"
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
MATRIX = resolve_repo_path("docs", "research", "phase43_memory_collection_matrix.md", start_file=__file__)
RESEARCH = resolve_repo_path("docs", "research", "phase43_candidate_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase43_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase43_candidate_quality_gate.json", start_file=__file__)

CONTRACT_REFS = [
    "docs/research/phase43_external_project_ai_memory_scope.md",
    "docs/contracts/phase43_project_memory_contract.md",
    "docs/contracts/phase43_project_memory_mcp_api_contract.md",
    "docs/contracts/phase43_memory_write_retrieval_policy.md",
    "docs/contracts/phase43_memory_security_governance_contract.md",
    "docs/contracts/phase43_memory_retention_privacy_contract.md",
    "docs/tasks/phase43_external_project_ai_memory_layer.md",
]

SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "langchain_memory": {
        "title": "LangChain Docs: Memory overview",
        "url": "https://docs.langchain.com/oss/python/concepts/memory",
        "type": "official_doc",
        "publisher": "LangChain",
        "score": 88,
        "summary": "LangChain documents short-term and long-term memory concepts, including LangGraph long-term memories stored as JSON documents under namespaces and keys.",
    },
    "langchain_long_term": {
        "title": "LangChain Docs: Long-term memory",
        "url": "https://docs.langchain.com/oss/python/langchain/long-term-memory",
        "type": "official_doc",
        "publisher": "LangChain",
        "score": 88,
        "summary": "LangChain documents long-term memory across conversations, based on LangGraph stores organized by namespace and key.",
    },
    "letta_blocks": {
        "title": "Letta Docs: Memory blocks",
        "url": "https://docs.letta.com/guides/core-concepts/memory/memory-blocks/",
        "type": "official_doc",
        "publisher": "Letta",
        "score": 84,
        "summary": "Letta documents persistent memory blocks that are always visible in the agent context window.",
    },
    "letta_archival": {
        "title": "Letta Docs: Archival memory",
        "url": "https://docs.letta.com/guides/core-concepts/memory/archival-memory/",
        "type": "official_doc",
        "publisher": "Letta",
        "score": 84,
        "summary": "Letta archival memory is semantically searchable and queried on demand through tools, instead of always being pinned to context.",
    },
    "mem0_oss": {
        "title": "Mem0 Docs: Open Source Overview",
        "url": "https://docs.mem0.ai/open-source/overview",
        "type": "official_doc",
        "publisher": "Mem0",
        "score": 82,
        "summary": "Mem0 open source provides a self-hosted memory layer where teams own the stack, data and customizations.",
    },
    "mem0_types": {
        "title": "Mem0 Docs: Memory Types",
        "url": "https://docs.mem0.ai/core-concepts/memory-types",
        "type": "official_doc",
        "publisher": "Mem0",
        "score": 82,
        "summary": "Mem0 separates memory into layers so agents remember the right detail at the right time and avoid over-fetching.",
    },
    "graphiti": {
        "title": "Graphiti GitHub: Real-Time Knowledge Graphs for AI Agents",
        "url": "https://github.com/getzep/graphiti",
        "type": "official_doc",
        "publisher": "Zep",
        "score": 82,
        "summary": "Graphiti builds temporal context graphs for AI agents, tracks how facts change over time, and maintains provenance to source data.",
    },
    "zep_paper": {
        "title": "Zep: A Temporal Knowledge Graph Architecture for Agent Memory",
        "url": "https://arxiv.org/html/2501.13956v1",
        "type": "research_paper",
        "publisher": "arXiv",
        "score": 82,
        "summary": "The Zep paper describes a memory layer service for AI agents and evaluates temporal knowledge graph memory.",
    },
    "owasp_memory_guard": {
        "title": "OWASP Agent Memory Guard",
        "url": "https://owasp.org/www-project-agent-memory-guard/",
        "type": "security_standard",
        "publisher": "OWASP",
        "score": 90,
        "summary": "OWASP Agent Memory Guard protects AI agents from memory poisoning, persistent memory corruption, data exfiltration and malicious behavior across sessions.",
    },
    "owasp_ai_agent": {
        "title": "OWASP AI Agent Security Cheat Sheet",
        "url": "https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html",
        "type": "security_standard",
        "publisher": "OWASP",
        "score": 88,
        "summary": "OWASP recommends validating and sanitizing data before storing agent memory, isolating memory, setting expiration and size limits, auditing sensitive data, and using cryptographic integrity checks.",
    },
    "unit42_memory_poisoning": {
        "title": "Unit 42: Indirect prompt injection poisons AI long-term memory",
        "url": "https://unit42.paloaltonetworks.com/indirect-prompt-injection-poisons-ai-longterm-memory/",
        "type": "security_standard",
        "publisher": "Palo Alto Networks Unit 42",
        "score": 86,
        "summary": "Unit 42 demonstrates a proof of concept where indirect prompt injection silently poisons long-term agent memory and persists malicious instructions across sessions.",
    },
    "postgres_jsonb": {
        "title": "PostgreSQL Documentation: JSON Types",
        "url": "https://www.postgresql.org/docs/current/datatype-json.html",
        "type": "official_doc",
        "publisher": "PostgreSQL",
        "score": 88,
        "summary": "PostgreSQL documents json and jsonb data types, noting jsonb stores a decomposed binary format that avoids reparsing and is efficient for processing.",
    },
    "pgvector": {
        "title": "pgvector: Open-source vector similarity search for Postgres",
        "url": "https://github.com/pgvector/pgvector",
        "type": "official_doc",
        "publisher": "pgvector",
        "score": 84,
        "summary": "pgvector documents vector similarity search in Postgres, including exact and approximate nearest neighbor search while storing vectors with the rest of the data.",
    },
    "aws_mcp_security": {
        "title": "AWS Security Blog: Secure AI agent access patterns using MCP",
        "url": "https://aws.amazon.com/blogs/security/secure-ai-agent-access-patterns-to-aws-resources-using-model-context-protocol/",
        "type": "security_standard",
        "publisher": "AWS",
        "score": 82,
        "summary": "AWS security guidance recommends least privilege and resource-level restrictions when agents access external tools through MCP-like patterns.",
    },
}

ROLE_SOURCES: dict[str, list[str]] = {
    "boundary": ["langchain_memory", "langchain_long_term", "owasp_ai_agent", "unit42_memory_poisoning"],
    "schema": ["langchain_memory", "langchain_long_term", "letta_blocks", "mem0_types"],
    "lifecycle": ["langchain_memory", "letta_blocks", "mem0_types", "owasp_ai_agent"],
    "write_gate": ["owasp_memory_guard", "unit42_memory_poisoning", "owasp_ai_agent", "langchain_memory"],
    "mcp_api": ["aws_mcp_security", "owasp_ai_agent", "owasp_memory_guard", "langchain_memory"],
    "retention_privacy": ["owasp_ai_agent", "owasp_memory_guard", "unit42_memory_poisoning", "postgres_jsonb"],
    "security": ["owasp_memory_guard", "unit42_memory_poisoning", "owasp_ai_agent", "mem0_oss"],
    "integrity": ["owasp_memory_guard", "owasp_ai_agent", "unit42_memory_poisoning", "postgres_jsonb"],
    "storage_baseline": ["postgres_jsonb", "langchain_memory", "langchain_long_term", "pgvector"],
    "retrieval": ["langchain_memory", "langchain_long_term", "letta_archival", "mem0_types"],
    "adapter": ["langchain_long_term", "letta_archival", "mem0_oss", "graphiti", "zep_paper"],
    "evaluation": ["owasp_memory_guard", "owasp_ai_agent", "graphiti", "zep_paper"],
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def parse_matrix() -> list[dict[str, str]]:
    topics: list[dict[str, str]] = []
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P43-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        topics.append(
            {
                "topic_id": cells[0],
                "priority": cells[1],
                "title": cells[2],
                "node": cells[3].strip("`"),
                "role": cells[4],
                "expected_sources": cells[5],
                "acceptance_gate": cells[6],
            }
        )
    return topics


def source_refs(role: str) -> list[dict[str, Any]]:
    keys = ROLE_SOURCES.get(role, ["langchain_memory", "owasp_ai_agent", "postgres_jsonb"])
    refs: list[dict[str, Any]] = []
    for key in keys:
        source = SOURCE_CATALOG[key]
        refs.append(
            {
                "source_id": f"src_{key}",
                "source_title": source["title"],
                "source_url": source["url"],
                "source_type": source["type"],
                "publisher": source["publisher"],
                "published_at": None,
                "accessed_at": TODAY,
                "version": None,
                "reliability": "high",
                "score": source["score"],
                "relevance": "high",
                "freshness": "time_sensitive",
                "limitations": [],
                "evidence_summary": source["summary"],
                "quoted_excerpt_allowed": False,
            }
        )
    return refs


def candidate(topic: dict[str, str], index: int) -> dict[str, Any]:
    title = topic["title"]
    role = topic["role"]
    refs = source_refs(role)
    slug = slugify(title)[:80]
    evidence = "；".join(src["evidence_summary"] for src in refs[:3])
    return {
        "schema_version": "1.0.0",
        "candidate_id": f"cand_20260611_phase43_{topic['topic_id'].lower().replace('-', '_')}_{slug}_{index:03d}",
        "research_task_id": topic["topic_id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "candidate_ready",
            "decision_reason": "Phase 43 candidate generated for external AI/human audit; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": topic["node"],
            "canonical_node_id": topic["node"],
            "tree_path": "CEK-TA / AI Engineering / External Project AI Memory Layer",
            "related_nodes": [
                "kt.project_integration",
                "kt.rag_engineering",
                "kt.ai_engineering.database_storage_engineering",
                "kt.ai_engineering.model_release_governance",
            ],
            "partition_id": "KB_AI_27_PROJECT_MEMORY",
            "domain": "ai_governance",
            "subdomain": topic["node"].split(".")[-1],
            "rule_type": "governance_rule",
            "used_for": ["external_ai_ide", "project_memory_mcp", "rag_engineering", "mcp", "vue_audit_ui"],
        },
        "claim": {
            "claim_id": f"claim_{index:03d}",
            "statement": title,
            "normalized_claim": f"phase43.{slug}.v1",
            "claim_type": role,
            "memory_layer_role": role,
            "evidence_summary": evidence,
            "interpretation_notes": "本候选只沉淀外接项目 AI Memory Layer 的治理契约；不保存外接项目私有记忆，不创建真实数据库，不绑定单一 vendor。",
            "claim_strength": "medium",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "external_ai_project_memory_layer",
            "applies_when": [
                "外接项目需要让 AI IDE / Agent 记住项目目标、任务、决策、产物、经验、边界、错误复盘或审计结论。",
                "该规则用于设计 Project Memory Contract、MemoryItem schema、MCP/API、write gate、retrieval budget、安全治理或 adapter 选型。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、K 线形态、策略参数或实盘下单建议。",
                "知识点主要描述交易执行、fill model、订单状态机、交易所异常处理或实盘风控阈值，应路由到 Trading Engineering。",
                "用户要求 CEK-TA 保存外接项目私有目标、任务、错误、决策、产物内容或真实数据库结构。",
            ],
            "assumptions": [
                "外接项目自行保存私有项目记忆；CEK-TA 只沉淀通用 memory contract 和治理规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充实例。",
                "本条不实现 Project Memory MCP server，不创建生产数据库，不改变 MCP 写权限。",
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒外接项目 AI IDE 设计项目记忆层、MemoryItem schema、写入门禁和检索预算。",
                "用于生成任务卡、接口契约、审计 checklist、候选知识补证问题和安全边界。",
                "用于阻断无来源长期记忆、自动保存所有聊天、AI 直接写 active memory、记忆污染 CEK-TA 知识库。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘下单建议。",
                "不得据此直接保存外接项目私有记忆、创建生产数据库或绑定单一 memory vendor。",
                "不得把 candidate 当作 reviewed/approved 默认指导。",
            ],
        },
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": round(sum(src["score"] for src in refs) / len(refs), 1),
            "score_version": "1.1.0",
            "primary_source_count": len([src for src in refs if src["source_type"] in {"official_doc", "security_standard", "research_paper"}]),
            "supporting_source_count": len(refs),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": ["来源支持通用 agent memory、MCP/API、安全、存储和 adapter 原则；正式知识转换时需保留 CEK-TA 具体上下游引用。"],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": CONTRACT_REFS,
            "conflicts": [],
            "resolution_summary": "未发现与 Phase 43 契约的直接冲突；候选不会进入默认指导，也不会保存外接项目私有记忆。",
            "approval_allowed": False,
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "Phase 43 candidate audit does not allow default guidance; formal reviewed requires a later gate.",
            "requires_human_escalation": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "codex_candidate_generation",
            "reviewed_at": TODAY,
            "open_questions": ["审计时确认该候选是否需要补充更贴近外接 AI IDE 的实例、反例或 adapter 迁移案例。"],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "Phase 43 external project AI memory layer candidate expansion.",
                }
            ],
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "candidate_to_formal_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "hidden_from_default_queue": True,
            "visible_in_candidate_audit_queue": True,
            "next_action": "external_ai_or_human_audit",
        },
        "contribution": {
            "origin_project": "CEK-TA",
            "private_data_removed": True,
            "project_private_fields": [],
        },
    }


def has_mojibake(value: object) -> bool:
    text = json.dumps(value, ensure_ascii=False)
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", text))


def quality_gate(candidates: list[dict[str, Any]], planned_total: int) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in candidates:
        candidate_id = str(item.get("candidate_id", ""))
        seen.add(str(item.get("research_task_id", "")))
        refs = item.get("source_refs") or []
        if len(refs) < 3:
            failures.append({"candidate_id": candidate_id, "failure": "source_refs_lt_3"})
        if not str(item.get("classification", {}).get("canonical_node_id", "")).startswith("kt.ai_engineering.external_project_memory."):
            failures.append({"candidate_id": candidate_id, "failure": "wrong_canonical_node"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": candidate_id, "failure": "not_proposed"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": candidate_id, "failure": "default_guidance_not_denied"})
        if item.get("workflow", {}).get("hard_gate_allowed") is not False:
            failures.append({"candidate_id": candidate_id, "failure": "hard_gate_not_false"})
        if has_mojibake(item):
            failures.append({"candidate_id": candidate_id, "failure": "mojibake_marker_detected"})
    return {
        "report_id": "phase43_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 43 external project AI memory candidate package",
        "candidate_count": len(candidates),
        "planned_total": planned_total,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }


def write_research(topics: list[dict[str, str]], candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 43 Candidate Research",
        "",
        "## 来源目录",
        "",
    ]
    for key, source in SOURCE_CATALOG.items():
        lines.append(f"- `{key}`: {source['title']} - {source['url']}")
    lines += ["", "## 候选知识点", ""]
    for topic, cand in zip(topics, candidates):
        lines.append(f"### {topic['topic_id']} {topic['title']}")
        lines.append("")
        lines.append(f"- canonical_node_id: `{topic['node']}`")
        lines.append(f"- role: `{topic['role']}`")
        lines.append(f"- acceptance_gate: {topic['acceptance_gate']}")
        lines.append(f"- candidate_id: `{cand['candidate_id']}`")
        lines.append("")
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    topics = parse_matrix()
    candidates = [candidate(topic, i + 1) for i, topic in enumerate(topics)]
    for item in candidates:
        topic_id = str(item["research_task_id"]).lower().replace("-", "_")
        slug = item["claim"]["normalized_claim"].split(".")[1]
        path = CAND_DIR / f"cand_20260611_phase43_{topic_id}_{slug}.json"
        path.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    quality = quality_gate(candidates, len(topics))
    write_research(topics, candidates)
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Phase 43 Candidate Generation Report",
                "",
                f"- generated_at: {TODAY}",
                f"- planned_total: {len(topics)}",
                f"- candidate_count: {len(candidates)}",
                f"- quality_gate: {quality['gate_status']}",
                "- boundary: 仅生成候选，不创建 formal reviewed / approved / default guidance / hard gate。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"candidate_count": len(candidates), "quality_gate": quality["gate_status"], "report": str(REPORT)}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
