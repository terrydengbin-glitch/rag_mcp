"""Supplement Phase 42 needs_more_evidence candidates and export re-audit package."""

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


TODAY = date(2026, 6, 11).isoformat()
CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", "phase42_needs_evidence_supplemental_reaudit_package_20260611.json", start_file=__file__
)
REPORT_JSON_PATH = resolve_repo_path(
    "docs", "reports", "phase42_needs_evidence_supplemental_report.json", start_file=__file__
)
REPORT_MD_PATH = resolve_repo_path(
    "docs", "research", "phase42_needs_evidence_supplemental_research.md", start_file=__file__
)


def source(
    source_id: str,
    title: str,
    url: str,
    source_type: str,
    publisher: str,
    summary: str,
    *,
    score: int = 86,
    relevance: str = "high",
    reliability: str = "high",
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "source_title": title,
        "source_url": url,
        "source_type": source_type,
        "publisher": publisher,
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": reliability,
        "score": score,
        "relevance": relevance,
        "freshness": "time_sensitive",
        "limitations": [],
        "evidence_summary": summary,
        "quoted_excerpt_allowed": False,
    }


COMMON_INTERNAL_CONTRACT = source(
    "src_phase42_database_storage_contract",
    "Phase 42 交易 AI 数据库与数据契约",
    "docs/contracts/phase42_database_storage_contract.md",
    "internal_contract",
    "CEK-TA",
    "CEK-TA Phase 42 内部契约定义 trade_candidate、score_result、llm_audit_result、final_gate_ledger、feedback/outcome/label、manifest、权限、迁移和生命周期边界。",
    score=82,
)

COMMON_RAG_CONTRACT = source(
    "src_phase42_rag_vector_storage_contract",
    "Phase 42 RAG / Vector Storage 契约",
    "docs/contracts/phase42_rag_vector_storage_contract.md",
    "internal_contract",
    "CEK-TA",
    "CEK-TA Phase 42 RAG/vector 契约定义 rag_document、rag_chunk、embedding_record、vector_index_manifest、citation_result 和默认指导阻断边界。",
    score=82,
)

SOURCES = {
    "owasp_a09": source(
        "src_owasp_a09",
        "OWASP Top 10 2021 A09: Security Logging and Monitoring Failures",
        "https://owasp.org/Top10/2021/A09_2021-Security_Logging_and_Monitoring_Failures/",
        "security_standard",
        "OWASP",
        "OWASP A09 强调日志、监控、告警、事件响应和高价值活动可追踪性，可支撑 append-only/integrity-controlled audit trail 的风险边界。",
    ),
    "w3c_prov": source(
        "src_w3c_prov_dm",
        "W3C PROV-DM: The PROV Data Model",
        "https://www.w3.org/TR/prov-dm/",
        "standard_doc",
        "W3C",
        "W3C PROV-DM 用 entity、activity、agent 描述数据生产、使用和责任主体，支撑 feedback/outcome/label 的 provenance 分离。",
    ),
    "data_cards": source(
        "src_google_data_cards_playbook",
        "The Data Cards Playbook",
        "https://sites.research.google/datacardsplaybook/",
        "governance_framework",
        "Google Research",
        "Data Cards 是用于透明记录数据集事实、用途、生命周期和责任信息的结构化文档，支撑 label policy/source 和 dataset manifest 说明。",
    ),
    "datacite": source(
        "src_datacite_metadata_schema",
        "DataCite Metadata Schema",
        "https://schema.datacite.org/",
        "standard_doc",
        "DataCite",
        "DataCite Metadata Schema 定义用于准确、一致标识、引用和检索资源的核心元数据属性，支撑 source_uri、版本、引用和 related identifier。",
    ),
    "fair": source(
        "src_fair_principles",
        "FAIR Principles",
        "https://www.go-fair.org/fair-principles/",
        "governance_framework",
        "GO FAIR",
        "FAIR 原则要求 metadata/data 可发现、可访问、可互操作、可复用，并包含可引用的相关 metadata，支撑 RAG chunk/source provenance。",
    ),
    "cc_faq": source(
        "src_creative_commons_machine_readable_license",
        "Creative Commons FAQ: machine-readable licenses",
        "https://creativecommons.org/faq/",
        "governance_framework",
        "Creative Commons",
        "Creative Commons FAQ 说明机器可读 license metadata，支撑 RAG 文档和 chunk 保存 license/copyright policy。",
        score=80,
    ),
    "openai_file_search": source(
        "src_openai_file_search_results",
        "OpenAI File Search Guide",
        "https://developers.openai.com/api/docs/guides/tools-file-search",
        "official_doc",
        "OpenAI",
        "OpenAI File Search 文档说明输出可包含文件引用 annotations，并可 include search results，支撑 citation/source binding 与 unsupported/no-hit 处理。",
    ),
    "llamaindex_citation": source(
        "src_llamaindex_citation_query_engine",
        "LlamaIndex CitationQueryEngine",
        "https://developers.llamaindex.ai/python/examples/query_engine/citation_query_engine/",
        "framework_doc",
        "LlamaIndex",
        "LlamaIndex CitationQueryEngine 展示带 source citation 的检索问答模式，支撑 LLM audit 输出必须绑定 citation/source 的工程边界。",
        score=82,
    ),
    "qdrant_filtering": source(
        "src_qdrant_filtering",
        "Qdrant Documentation: Filtering",
        "https://qdrant.tech/documentation/search/filtering/",
        "official_doc",
        "Qdrant",
        "Qdrant filtering 文档说明基于 payload 条件过滤向量检索结果，支撑 knowledge_id、document_id、chunk_id 等 metadata 回链过滤。",
    ),
    "qdrant_points": source(
        "src_qdrant_points",
        "Qdrant Documentation: Points",
        "https://qdrant.tech/documentation/manage-data/points/",
        "official_doc",
        "Qdrant",
        "Qdrant points 文档说明 point 可组合 vector 与 JSON payload，支撑 embedding/vector record 保存 payload metadata、source/chunk/index 信息。",
    ),
    "stripe_idempotency": source(
        "src_stripe_idempotent_requests",
        "Stripe API Reference: Idempotent requests",
        "https://docs.stripe.com/api/idempotent_requests",
        "official_doc",
        "Stripe",
        "Stripe 文档说明 idempotency key 可安全重试请求并避免重复执行，支撑高价值写路径的幂等键要求。",
    ),
    "aws_idempotency": source(
        "src_aws_ec2_api_idempotency",
        "AWS EC2: Ensuring idempotency in API requests",
        "https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html",
        "official_doc",
        "AWS",
        "AWS 文档说明 client token 用于 API 幂等请求，且同一 token 不应复用于不同请求，支撑写路径幂等和去重边界。",
    ),
    "confluent_schema": source(
        "src_confluent_schema_evolution",
        "Confluent Documentation: Schema Evolution and Compatibility",
        "https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html",
        "official_doc",
        "Confluent",
        "Confluent Schema Registry 文档定义 backward、forward、full compatibility 等 schema compatibility 类型，支撑 schema_version 变更兼容性检查。",
    ),
    "openapi_spec": source(
        "src_openapi_specification",
        "OpenAPI Specification 3.1.0",
        "https://swagger.io/specification/",
        "standard_doc",
        "OpenAPI Initiative",
        "OpenAPI 规范要求 OpenAPI 文档声明规范版本，并定义 API 契约结构，支撑下游 MCP/SearchLab/API consumer compatibility 文档化。",
    ),
    "openlineage": source(
        "src_openlineage_object_model",
        "OpenLineage Object Model",
        "https://openlineage.io/docs/spec/object-model/",
        "standard_doc",
        "OpenLineage",
        "OpenLineage object model 定义 Dataset、Job、Run 等抽象并关注数据如何产生，支撑 feature/dataset manifest 的 lineage references。",
    ),
    "feast_feature_retrieval": source(
        "src_feast_feature_retrieval",
        "Feast Documentation: Feature retrieval",
        "https://docs.feast.dev/getting-started/concepts/feature-retrieval",
        "official_doc",
        "Feast",
        "Feast feature retrieval 文档说明 event timestamp 和 point-in-time joins 支撑历史特征生成，支撑 feature snapshot 与 schema lineage。",
    ),
    "owasp_secrets": source(
        "src_owasp_secrets_management",
        "OWASP Secrets Management Cheat Sheet",
        "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html",
        "security_standard",
        "OWASP",
        "OWASP Secrets Management Cheat Sheet 覆盖 secrets 的集中存储、配置、审计、轮换和管理，直接支撑密钥不得写入业务表。",
    ),
    "owasp_crypto": source(
        "src_owasp_cryptographic_storage",
        "OWASP Cryptographic Storage Cheat Sheet",
        "https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html",
        "security_standard",
        "OWASP",
        "OWASP Cryptographic Storage Cheat Sheet 明确不应把 keys 硬编码到源码或提交到版本控制，并建议限制 key 存储暴露面。",
    ),
    "nist_ac6": source(
        "src_nist_sp800_53_ac6",
        "NIST SP 800-53 Rev.5 AC-6 Least Privilege",
        "https://csf.tools/reference/nist-sp-800-53/r5/ac/ac-6/",
        "security_standard",
        "NIST",
        "NIST AC-6 要求只允许完成任务所需的授权访问，支撑 MCP/SearchLab 默认只读和写路径最小权限边界。",
    ),
}


SUPPLEMENTS: dict[str, dict[str, Any]] = {
    "P42-P0-004": {
        "source_keys": ["owasp_a09"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 ScoreResultRecord/ledger 内部契约与 OWASP A09，明确 score_result append-only、raw_score 不覆盖、版本绑定和审计追踪。",
    },
    "P42-P0-007": {
        "source_keys": ["w3c_prov", "data_cards"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 W3C PROV、Data Cards 和 feedback/outcome/label_event 内部契约，支撑三类事件按 provenance、时点和训练含义分离。",
    },
    "P42-P0-008": {
        "source_keys": ["w3c_prov", "data_cards"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 label_event 内部契约、W3C PROV 和 Data Cards，支撑 label_policy_version、label_source、责任主体和语义复现。",
    },
    "P42-P0-009": {
        "source_keys": ["openlineage"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 model_release_manifest 内部契约和 OpenLineage，明确 model/prompt/RAG index 共同作为 LLM audit release unit 的版本回链。",
    },
    "P42-P0-010": {
        "source_keys": ["openai_file_search", "llamaindex_citation"],
        "internal_sources": [COMMON_RAG_CONTRACT],
        "notes": "补充 OpenAI File Search、LlamaIndex citation 和 CEK-TA citation_result 契约，支撑 citation/source/index version 与 unsupported_claims 绑定。",
    },
    "P42-P0-011": {
        "source_keys": ["qdrant_filtering", "qdrant_points", "openai_file_search"],
        "internal_sources": [COMMON_RAG_CONTRACT],
        "notes": "补充 Qdrant payload/points 和 CEK-TA formal knowledge index 边界，明确 vector hit 必须回链 source document/chunk/formal knowledge id。",
    },
    "P42-P0-012": {
        "source_keys": ["datacite", "fair", "cc_faq"],
        "internal_sources": [COMMON_RAG_CONTRACT],
        "notes": "补充 DataCite、FAIR、Creative Commons 和 RAGChunkManifest 契约，支撑 source_uri、license/copyright、content hash、chunk_version。",
    },
    "P42-P0-013": {
        "source_keys": ["qdrant_points", "qdrant_filtering"],
        "internal_sources": [COMMON_RAG_CONTRACT],
        "notes": "补充 vector_index_manifest/embedding_record 内部契约和 Qdrant payload 证据，明确 embedding model version 变更必须绑定 index version/rebuild plan。",
    },
    "P42-P0-015": {
        "source_keys": ["stripe_idempotency", "aws_idempotency"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 Stripe/AWS 幂等键来源和 CEK-TA idempotency_key 契约，支撑高价值写路径去重和安全重试。",
    },
    "P42-P0-018": {
        "source_keys": ["confluent_schema", "openapi_spec"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT, COMMON_RAG_CONTRACT],
        "notes": "补充 Schema Registry compatibility、OpenAPI 和 CEK-TA consumer compatibility report，支撑 schema_version 变更前兼容性检查。",
    },
    "P42-P0-021": {
        "source_keys": ["feast_feature_retrieval", "openlineage"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 Feast feature retrieval、OpenLineage 和 FeatureSnapshotManifest 契约，支撑 feature_schema_hash 与 lineage references。",
    },
    "P42-P0-022": {
        "source_keys": ["datacite", "data_cards", "openlineage"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 DataCite、Data Cards、OpenLineage 和 DatasetSnapshotManifest 契约，支撑 dataset_hash、split manifest、label policy refs。",
    },
    "P42-P0-026": {
        "source_keys": ["owasp_secrets", "owasp_crypto"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT],
        "notes": "补充 OWASP Secrets Management/Cryptographic Storage 和权限契约，直接支撑 DB credentials/API keys/exchange secrets 不入业务表。",
    },
    "P42-P0-028": {
        "source_keys": ["nist_ac6", "owasp_a09"],
        "internal_sources": [COMMON_INTERNAL_CONTRACT, COMMON_RAG_CONTRACT],
        "notes": "补充 NIST AC-6、OWASP A09 和 CEK-TA MCP/SearchLab 权限契约，支撑默认只读、最小权限和写动作审计。",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object.")
    return data


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_source_refs(candidate: dict[str, Any], refs: list[dict[str, Any]]) -> list[str]:
    source_refs = candidate.setdefault("source_refs", [])
    existing = {str(src.get("source_id")) for src in source_refs if isinstance(src, dict)}
    added: list[str] = []
    for ref in refs:
        if ref["source_id"] not in existing:
            source_refs.append(ref)
            added.append(ref["source_id"])
            existing.add(ref["source_id"])
    return added


def normalize_generated_fields(candidate: dict[str, Any]) -> None:
    for src in candidate.get("source_refs", []):
        if isinstance(src, dict) and src.get("source_type") == "license_doc":
            src["source_type"] = "governance_framework"
    audit_log = candidate.get("review", {}).get("audit_log", [])
    if isinstance(audit_log, list):
        for entry in audit_log:
            if isinstance(entry, dict) and "supplement_id" in entry:
                entry["audit_package"] = entry.pop("supplement_id")


def update_source_quality(candidate: dict[str, Any]) -> None:
    source_refs = [src for src in candidate.get("source_refs", []) if isinstance(src, dict)]
    primary_types = {"official_doc", "standard_doc", "security_standard", "governance_framework", "framework_doc"}
    primary = [src for src in source_refs if src.get("source_type") in primary_types]
    quality = candidate.setdefault("source_quality", {})
    quality["primary_source_count"] = len(primary)
    quality["supporting_source_count"] = max(0, len(source_refs) - len(primary))
    quality["low_reliability_source_count"] = len([src for src in source_refs if src.get("reliability") == "low"])
    if source_refs:
        quality["score"] = round(sum(int(src.get("score", 70)) for src in source_refs) / len(source_refs))
    quality["overall_reliability"] = "high" if len(primary) >= 2 else "medium"
    limitations = quality.setdefault("limitations", [])
    if isinstance(limitations, list):
        note = "已补充 claim-specific 外部来源和 Phase 42 内部契约证据；二审仍需确认是否足以进入 accepted_for_draft。"
        if note not in limitations:
            limitations.append(note)


def supplement_candidate(path: Path) -> dict[str, Any] | None:
    candidate = read_json(path)
    research_task_id = str(candidate.get("research_task_id", ""))
    spec = SUPPLEMENTS.get(research_task_id)
    if spec is None:
        return None
    normalize_generated_fields(candidate)

    refs = [SOURCES[key] for key in spec["source_keys"]] + spec.get("internal_sources", [])
    added = append_source_refs(candidate, refs)
    verified_source_ids = [ref["source_id"] for ref in refs]

    claim = candidate.setdefault("claim", {})
    old_summary = str(claim.get("evidence_summary", ""))
    addition = "；".join(ref["evidence_summary"] for ref in refs)
    if addition and addition not in old_summary:
        claim["evidence_summary"] = f"{old_summary}；{addition}" if old_summary else addition
    notes = claim.setdefault("interpretation_notes", "")
    supplement_note = f" 补证说明：{spec['notes']}"
    if supplement_note.strip() not in str(notes):
        claim["interpretation_notes"] = f"{notes}{supplement_note}".strip()

    review = candidate.setdefault("review", {})
    review["supplemented_at"] = TODAY
    review["supplement_status"] = "ready_for_reaudit"
    review["supplemental_evidence"] = {
        "supplement_id": "phase42_needs_evidence_supplement_20260611",
        "added_source_ids": added,
        "verified_source_ids": verified_source_ids,
        "supplement_notes": spec["notes"],
        "source_count_after": len(candidate.get("source_refs", [])),
        "reaudit_package": "docs/audit/phase42_needs_evidence_supplemental_reaudit_package_20260611.json",
    }
    audit_log = review.setdefault("audit_log", [])
    if isinstance(audit_log, list):
        audit_log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "phase42_needs_more_evidence_supplemented",
                "reason": spec["notes"],
                "audit_package": "phase42_needs_evidence_supplement_20260611",
            }
        )

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["next_action"] = "export_ai_audit"
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "needs_more_evidence"
    status["updated_at"] = TODAY
    status["decision_reason"] = "已按第一轮审计要求补充证据，等待二审；不得视为 accepted/reviewed/approved。"

    update_source_quality(candidate)
    write_json(path, candidate)
    return candidate


def load_supplemented() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for path in sorted(CANDIDATE_DIR.glob("cand_20260611_phase42_*.json")):
        item = supplement_candidate(path)
        if item is not None:
            items.append(item)
    return items


def quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    expected = set(SUPPLEMENTS)
    seen: set[str] = set()
    for item in candidates:
        rid = str(item.get("research_task_id"))
        seen.add(rid)
        cid = str(item.get("candidate_id"))
        source_refs = item.get("source_refs") or []
        if len(source_refs) < 4:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_4_after_supplement"})
        if item.get("workflow", {}).get("stage") != "needs_more_evidence":
            failures.append({"candidate_id": cid, "failure": "workflow_stage_not_needs_more_evidence"})
        if item.get("workflow", {}).get("hidden_from_default_queue") is not True:
            failures.append({"candidate_id": cid, "failure": "hidden_from_default_queue_not_true"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "failure": "machine_gate_not_deny"})
        if item.get("status", {}).get("review_status") != "needs_more_evidence":
            failures.append({"candidate_id": cid, "failure": "status_not_needs_more_evidence"})
        if not item.get("review", {}).get("supplemental_evidence", {}).get("verified_source_ids"):
            failures.append({"candidate_id": cid, "failure": "missing_verified_source_ids"})
    for missing in sorted(expected - seen):
        failures.append({"research_task_id": missing, "failure": "missing_supplemented_candidate"})
    return {
        "gate_id": "phase42_needs_evidence_supplemental_quality_gate",
        "generated_at": TODAY,
        "candidate_count": len(candidates),
        "expected_count": len(SUPPLEMENTS),
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "Supplementation does not promote candidates; second audit decides accepted_for_draft/needs_more_evidence/rejected.",
    }


def build_audit_package(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> dict[str, Any]:
    return {
        "package_id": "phase42_needs_evidence_supplemental_reaudit_package_20260611",
        "package_type": "candidate_ai_reaudit_package",
        "schema_version": "1.0.0",
        "generated_at": TODAY,
        "language": "zh-CN",
        "source_audit_result_id": "audit_result_phase42_candidate_audit_package_20260611_strict_v1",
        "source_package_id": "phase42_candidate_audit_package_20260611",
        "phase": "42",
        "title": "Phase 42 14 条 needs_more_evidence 候选补证后二审包",
        "purpose": "请只审计本包 14 条补证候选是否可从 needs_more_evidence 升级为 accepted_for_draft，或仍需补证/拒绝。",
        "strict_boundaries": [
            "本包不能创建 reviewed、approved、default guidance 或 hard gate。",
            "accepted_for_draft 只表示可进入后续 formal draft/reviewed 准备，不等于 reviewed 或 approved。",
            "数据库/存储建议只服务 AI Engineering 和外接项目设计，不创建生产数据库，不执行 migration。",
            "Vector DB 仍只能作为 retrieval index，不能成为 canonical store。",
            "LLM audit 仍不能写 final_gate。",
        ],
        "audit_instructions": [
            "重点检查补充来源是否直接覆盖第一轮 source_patch_notes 中的缺口。",
            "检查内部 Phase 42 契约是否作为 CEK-TA 项目内规则使用，而不是伪装成外部行业标准。",
            "检查是否仍存在来源不足、claim 过强、Trading Engineering 污染、默认指导越权或乱码。",
            "输出 decision 只能是 accepted_for_draft、needs_more_evidence、rejected 或 blocked。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "auditor": "string",
            "audited_at": "string",
            "package_id": "phase42_needs_evidence_supplemental_reaudit_package_20260611",
            "summary": {
                "total": 14,
                "accepted_for_draft": 0,
                "needs_more_evidence": 0,
                "rejected": 0,
                "blocked": 0,
            },
            "candidate_results": [
                {
                    "candidate_id": "string",
                    "research_task_id": "string",
                    "decision": "accepted_for_draft | needs_more_evidence | rejected | blocked",
                    "confidence": "high | medium | low",
                    "reasons": ["string"],
                    "source_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "conflict_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "scope_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "classification_audit": {"status": "pass | warning | fail", "notes": ["string"]},
                    "required_followups": ["string"],
                    "proposed_handoff_patch": {
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                    },
                }
            ],
        },
        "quality_gate": gate,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def write_markdown_report(candidates: list[dict[str, Any]], gate: dict[str, Any]) -> None:
    lines = [
        "# Phase 42 需补证候选补证记录",
        "",
        "## 结论",
        "",
        f"本轮为 Phase 42 第一轮审计中 `needs_more_evidence` 的 `{len(candidates)}` 条候选补充了来源和内部契约证据。",
        "",
        f"质量门禁：`{gate['gate_status']}`，失败数 `{gate['failure_count']}`。",
        "",
        "## 补证清单",
        "",
        "| research_task_id | candidate_id | source_count | added_source_ids |",
        "| --- | --- | --- | --- |",
    ]
    for item in candidates:
        sup = item.get("review", {}).get("supplemental_evidence", {})
        lines.append(
            f"| {item.get('research_task_id')} | `{item.get('candidate_id')}` | "
            f"{len(item.get('source_refs', []))} | `{', '.join(sup.get('verified_source_ids', []))}` |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "本轮补证不代表 accepted、reviewed、approved、default guidance 或 hard gate。二审通过后仍需按 Phase 32/42 流程继续转换。",
            "",
        ]
    )
    REPORT_MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    candidates = load_supplemented()
    gate = quality_gate(candidates)
    package = build_audit_package(candidates, gate)
    write_json(AUDIT_PACKAGE_PATH, package)
    report = {
        "report_id": "phase42_needs_evidence_supplemental_report",
        "generated_at": TODAY,
        "candidate_count": len(candidates),
        "quality_gate": gate,
        "audit_package_path": str(AUDIT_PACKAGE_PATH),
        "research_report_path": str(REPORT_MD_PATH),
        "supplemented_research_task_ids": [item.get("research_task_id") for item in candidates],
        "formal_knowledge_created": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
    }
    write_json(REPORT_JSON_PATH, report)
    write_markdown_report(candidates, gate)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if gate["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
