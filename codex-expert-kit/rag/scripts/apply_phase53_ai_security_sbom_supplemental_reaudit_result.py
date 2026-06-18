"""Apply Phase 53 AI Security/SBOM supplemental reviewed/caveat_only audit result.

This script handles the two Phase 53 candidates that were previously
`needs_more_evidence`. The supplemental audit allows them to become formal
reviewed/caveat_only knowledge, but still forbids approved/default guidance,
hard gates, legal/security-pass claims, and trading execution advice.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

base = importlib.import_module("apply_phase53_reviewed_preparation_result")

TODAY = "2026-06-13"
TASK_ID = "CEK-TA-524"
AUDIT_RESULT_ID = "audit_phase53_ai_security_sbom_supplemental_reaudit_20260613"
PACKAGE_ID = "phase53_ai_security_sbom_supplemental_reaudit_package_20260613"

base.AUDIT_RESULT_ID = AUDIT_RESULT_ID
base.PACKAGE_ID = PACKAGE_ID
base.IMPORT_REPORT_PATH = base.resolve_repo_path(
    "docs", "reports", "phase53_ai_security_sbom_supplemental_reaudit_import_report.json", start_file=__file__
)
base.AUDIT_RESULT_PATH = base.resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)

SUPPLEMENTAL_PACKAGE_PATH = base.resolve_repo_path(
    "docs", "audit", "phase53_ai_security_sbom_supplemental_reaudit_package_20260613.json", start_file=__file__
)


RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260613_phase53_trading_ai_agent_threat_model_required_001",
        "research_task_id": "P53-AI-SEC01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "补证已加入 CEK-TA MCP Server Spec / Permission Model，支撑 tool_permission_boundary、只读 knowledge retrieval、no trade、no secret、no account access。",
            "补证已加入 Phase 43 Project Memory Contract 和 Memory MCP/API Contract，支撑 proposed-only memory、受控写入、review_required 和 audit_event_id。",
            "补证已加入 Phase 41 Hybrid Scoring Runtime Contract / Deterministic Final Gate，支撑 LLM/Qwen 只做审计解释、reason code、RAG 引用、缺字段检查和人工复核摘要。",
            "OWASP / NIST 只作为通用 AI/agent security 风险治理来源，不替代 CEK-TA 内部权限契约。",
            "claim 未输出漏洞利用步骤、绕过安全控制、交易许可、交易建议、风险阈值或 hard gate。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 MCP permission、Project Memory、Memory MCP/API、Phase 41 final gate 契约 hash 或稳定引用。",
            "memory_poisoning 必须绑定 memory_write_policy、source trust、review status、integrity / rollback / quarantine 字段，不得泛化为模型判断。",
            "tool misuse 必须绑定 tool_permission_boundary、tool_call_audit_ref、secret/account/trade access denial。",
            "LLM/RAG/MCP 只能辅助检索、审计、解释和 proposed memory，不得绕过 deterministic final gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 NIST AI RMF、OWASP GenAI Security、OWASP Agent Memory Guard、MITRE ATLAS。",
                "新增并保留 CEK-TA MCP Server Permission Model。",
                "新增并保留 Phase 43 Project Memory Contract。",
                "新增并保留 Phase 43 Project Memory MCP/API Contract。",
                "新增并保留 Phase 41 Hybrid Scoring Runtime Contract / Deterministic Final Gate。",
            ],
            "content": [
                "把 claim 写成 threat model / audit checklist / governance boundary。",
                "保留 threat_surface_taxonomy、tool_permission_boundary、memory_write_policy、rag_source_trust、final_gate_bypass_denied。",
                "明确 AI/RAG/MCP/memory 只能辅助检索、审计、解释和候选记忆 proposed。",
            ],
            "boundary": [
                "不得包含漏洞利用步骤。",
                "不得把 threat model 写成安全通过证明。",
                "不得生成交易许可、风险阈值、订单动作或 hard gate。",
                "不得让 AI Engineering 接管 Risk Management / Live Execution / deterministic final gate。",
            ],
            "conflict": [
                "Risk Management / Live Execution / deterministic final gate 拥有最终交易动作；AI Engineering 只拥有治理、审计和说明边界。"
            ],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_ai_sbom_model_sbom_required_001",
        "research_task_id": "P53-AI-SBOM01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "补证已加入 CycloneDX ML-BOM，直接支撑 models、datasets、dependencies、dataset provenance、training methodologies、AI framework configuration 等 AI/ML inventory 字段。",
            "补证已加入 SPDX 3.0.1 AI Profile，直接支撑 AI software package/system、model artifacts、models、datasets 等 AI profile 字段。",
            "补证已加入 NIST AI RMF 1.0，可作为 provenance、accountability、transparency 的辅助治理来源。",
            "补证已加入 Phase 40 / Phase 42 内部 release artifact、manifest、artifact lineage 契约。",
            "claim 明确 SBOM 只能提供供应链透明度、审计上下文和发布审核输入，不等于安全通过、发布批准、合规满足或 hard gate。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 CycloneDX ML-BOM 与 SPDX AI Profile 作为外部 schema 来源。",
            "正式文本必须保留 Phase 40 / Phase 42 内部 release artifact / manifest / artifact registry 契约 hash 或稳定引用。",
            "AI SBOM / Model SBOM 字段应分为 model、dataset、dependency、prompt、RAG snapshot、calibrator、threshold/final-gate policy、release manifest、artifact URI/hash。",
            "SBOM 不得作为安全通过证明、发布批准、合规满足声明、交易许可、风险阈值或 hard gate。",
        ],
        "patch_notes": {
            "source": [
                "保留 CISA SBOM、CISA AI SBOM、OWASP LLM Top 10、Model Cards。",
                "新增并保留 CycloneDX ML-BOM。",
                "新增并保留 SPDX 3.0.1 AI Profile。",
                "新增并保留 NIST AI RMF 1.0 作为 provenance/accountability 辅助来源。",
                "新增并保留 Phase 40 Composite Release Artifact Contract。",
                "新增并保留 Phase 40 Release Manifest Kill Switch Contract。",
                "新增并保留 Phase 42 Database/Storage manifest contract。",
            ],
            "content": [
                "AI SBOM / Model SBOM 必须记录模型、数据集、依赖、prompt、RAG snapshot、calibrator、threshold/final-gate policy、release manifest、artifact URI/hash 和来源边界。",
                "SBOM 只能提供供应链透明度、审计上下文和发布审核输入。",
                "source_confidentiality_boundary 必须保留，避免泄露未授权供应链信息、私有模型来源、密钥或数据。",
            ],
            "boundary": [
                "SBOM 不是安全通过证明。",
                "SBOM 不是发布批准。",
                "SBOM 不是合规满足声明。",
                "SBOM 不得创建 hard gate、交易许可或风险阈值。",
                "Release approval、kill switch、rollback、secret scan 和 final gate policy 仍由 Phase 40 / 外接项目 owner 管理。",
            ],
            "conflict": [
                "AI Engineering 只定义 inventory 和审计边界；Release approval、kill switch、rollback、secret scan、final gate policy 由对应 release / risk / owner 管理。"
            ],
        },
    },
]


def source_key(source: dict[str, Any]) -> tuple[str, str]:
    return (str(source.get("source_id") or ""), str(source.get("source_url") or source.get("url") or source.get("path") or ""))


def normalize_external_source(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": raw.get("source_id"),
        "source_title": raw.get("title"),
        "source_url": raw.get("url"),
        "source_type": raw.get("source_type", "official_reference"),
        "publisher": raw.get("publisher"),
        "published_at": raw.get("published_at"),
        "accessed_at": raw.get("accessed_at", TODAY),
        "version": raw.get("version"),
        "authority_level": "A2",
        "jurisdiction_or_scope": raw.get("jurisdiction_or_scope", "AI/security governance"),
        "reliability": raw.get("reliability", "high"),
        "score": 86,
        "relevance": raw.get("relevance", "high"),
        "freshness": "time_sensitive",
        "limitations": raw.get("limitations", []),
        "evidence_summary": raw.get("evidence_summary", ""),
        "quoted_excerpt_allowed": False,
    }


def normalize_internal_contract(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": raw.get("source_id"),
        "source_title": raw.get("title"),
        "source_url": raw.get("path"),
        "source_type": "internal_contract_extract",
        "publisher": "CEK-TA",
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "authority_level": "A1_INTERNAL",
        "jurisdiction_or_scope": "CEK-TA internal contract",
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "limitations": [
            "内部契约只定义 CEK-TA / 外接项目设计边界，不替代外部法律、安全或交易系统 owner 判断。"
        ],
        "evidence_summary": raw.get("extract", ""),
        "quoted_excerpt_allowed": False,
    }


def supplement_candidate(candidate: dict[str, Any], supplemental: dict[str, Any]) -> dict[str, Any]:
    source_refs = candidate.setdefault("source_refs", [])
    existing = {source_key(source) for source in source_refs if isinstance(source, dict)}
    evidence = supplemental.get("supplemental_evidence", {})
    for raw in evidence.get("external_sources", []):
        normalized = normalize_external_source(raw)
        key = source_key(normalized)
        if key not in existing:
            source_refs.append(normalized)
            existing.add(key)
    for raw in evidence.get("internal_contract_extracts", []):
        normalized = normalize_internal_contract(raw)
        key = source_key(normalized)
        if key not in existing:
            source_refs.append(normalized)
            existing.add(key)

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["overall_reliability"] = "high"
    source_quality["score"] = max(int(source_quality.get("score", 0) or 0), 90)
    source_quality["primary_source_count"] = len(source_refs)
    source_quality["supporting_source_count"] = 0
    source_quality["low_reliability_source_count"] = 0
    limitations = source_quality.setdefault("limitations", [])
    if isinstance(limitations, list) and "补证复审后仍必须保留 reviewed/caveat_only 边界，不得升级 approved/default/hard gate。" not in limitations:
        limitations.append("补证复审后仍必须保留 reviewed/caveat_only 边界，不得升级 approved/default/hard gate。")

    claim = candidate.setdefault("claim", {})
    notes = claim.get("interpretation_notes", "")
    claim["interpretation_notes"] = (
        f"{notes} 补证复审通过后仅可作为 formal reviewed/caveat_only；不得作为 approved、default guidance、hard gate、安全通过证明或交易执行建议。"
    ).strip()
    return candidate


def main() -> int:
    supplemental_package = base.load_json(SUPPLEMENTAL_PACKAGE_PATH)
    supplemental_by_id = {
        item["candidate_id"]: item
        for item in supplemental_package.get("candidate_results_to_reaudit", [])
        if isinstance(item, dict) and item.get("candidate_id")
    }

    audit_payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 2,
            "accepted_for_reviewed_caveat_only": 2,
            "needs_more_evidence": 0,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": RESULTS,
        "boundary": "No approved/default guidance/hard gate/security-pass/legal opinion/trading execution advice/risk threshold created.",
    }
    base.dump_json(base.AUDIT_RESULT_PATH, audit_payload)

    promoted: list[dict[str, Any]] = []
    for result in RESULTS:
        candidate_path, candidate = base.find_candidate(result["candidate_id"])
        supplemental = supplemental_by_id.get(result["candidate_id"], {})
        candidate = supplement_candidate(candidate, supplemental)
        formal = base.build_formal_item(candidate, result)
        knowledge_id = formal["knowledge_id"]
        knowledge_path = base.write_formal(formal)
        updated = base.update_candidate(candidate, result, knowledge_path, knowledge_id)
        base.dump_json(candidate_path, updated)
        promoted.append(
            {
                "candidate_id": result["candidate_id"],
                "research_task_id": result["research_task_id"],
                "knowledge_id": knowledge_id,
                "knowledge_path": base.rel(knowledge_path),
                "canonical_node_id": formal["metadata"]["canonical_node_id"],
                "review_status": "reviewed",
                "machine_gate": "caveat_only",
            }
        )

    report = {
        "report_id": "phase53_ai_security_sbom_supplemental_reaudit_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": PACKAGE_ID,
        "formal_reviewed_created": len(promoted),
        "needs_more_evidence_count": 0,
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "promoted": promoted,
        "boundary": "formal reviewed/caveat_only only; no approved/default guidance/hard gate/security-pass/trading execution advice.",
    }
    base.dump_json(base.IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
