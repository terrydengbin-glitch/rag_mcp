"""Apply Phase 53 candidate audit result and prepare supplemental re-audit.

This task imports the external strict audit result for the five Phase 53 P0
candidates. Four candidates are marked accepted_for_draft. The Market Conduct
candidate remains needs_more_evidence, receives the missing direct FINRA
Momentum Ignition source, and is exported as a one-item supplemental re-audit
package.

This script does not create reviewed/approved knowledge, default guidance,
hard gates, legal opinions, risk thresholds, or trading execution advice.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-13"
TASK_ID = "CEK-TA-523"
AUDIT_RESULT_ID = "audit_phase53_candidate_20260613_external_strict"
PACKAGE_ID = "phase53_candidate_audit_package_20260613"
SUPPLEMENTAL_PACKAGE_ID = "phase53_market_conduct_supplemental_reaudit_package_20260613"

AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
SUPPLEMENTAL_PACKAGE_PATH = resolve_repo_path("docs", "audit", f"{SUPPLEMENTAL_PACKAGE_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path("docs", "reports", "phase53_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_GATE_PATH = resolve_repo_path(
    "docs", "reports", "phase53_market_conduct_supplemental_reaudit_gate.json", start_file=__file__
)
CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)


AUDIT_RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260613_phase53_trading_ai_agent_threat_model_required_001",
        "research_task_id": "P53-AI-SEC01",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "NIST AI RMF / GenAI Profile 足以支撑 AI risk governance 和 GenAI-specific risk framing。",
            "OWASP LLM Top 10 直接覆盖 prompt injection、training data poisoning、supply chain vulnerabilities、sensitive information disclosure、excessive agency、overreliance。",
            "MITRE ATLAS 支撑 adversarial AI threat taxonomy 和真实 AI attack observations。",
            "claim 明确 LLM/RAG/MCP 不能绕过 deterministic final gate、Risk Management 或 Live Execution owner，边界正确。",
        ],
        "required_followups": [
            "进入 reviewed 前补 memory poisoning 的更直接来源，或将其映射为 memory_write_policy / RAG source poisoning 子类。",
            "补 tool misuse 与 MCP tool governance 的内部 contract extract。",
            "不得输出漏洞利用步骤、交易信号或 hard gate。",
        ],
        "patch_notes": {
            "source": ["保留 NIST AI RMF / NIST AI 600-1、OWASP LLM Top 10、MITRE ATLAS。"],
            "content": ["拆成 threat_surface_taxonomy、tool_permission_boundary、memory_write_policy、rag_source_trust、final_gate_bypass_denied。"],
            "boundary": ["不得生成漏洞利用步骤。", "不得生成交易建议。", "不得把 AI security risk 自动解释成交易 hard gate。"],
            "conflict": [],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_ai_sbom_model_sbom_required_001",
        "research_task_id": "P53-AI-SBOM01",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "CISA SBOM 来源支撑 software component inventory 与 supply-chain transparency。",
            "CISA SBOM for AI Minimum Elements 支撑 AI system component transparency / traceability。",
            "OWASP LLM Top 10 支撑 LLM supply-chain vulnerabilities 作为 AI security risk。",
            "Model Cards 支撑 model transparency、intended use、limitations 和 evaluation conditions，但不替代 SBOM。",
            "claim 已明确 SBOM 不是安全通过证明，不强制具体工具，不暴露未授权供应链信息。",
        ],
        "required_followups": [
            "进入 reviewed 前补 CycloneDX ML-BOM、SPDX AI / AI-BOM 或等价 model supply-chain schema 来源。",
            "明确 LoRA / adapter / embedding model / RAG index 字段来自 AI SBOM minimum elements 或内部 model registry contract。",
            "不得把 SBOM 写成安全批准、发布批准或合规满足证明。",
        ],
        "patch_notes": {
            "source": ["保留 CISA SBOM、CISA SBOM for AI Minimum Elements、OWASP LLM Top 10、Model Cards。"],
            "content": [
                "拆成 model_sbom、dataset_sbom、rag_index_sbom、container_dependency_sbom、inference_service_sbom。",
                "增加 source_confidentiality_boundary。",
            ],
            "boundary": ["SBOM 不等于安全通过证明。", "不得暴露未授权供应链信息。", "不得生成 hard gate。"],
            "conflict": [],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_market_conduct_surveillance_taxonomy_required_001",
        "research_task_id": "P53-TR-MC01",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "FINRA 来源足以支撑 spoofing、layering、wash trades、marking the close、front running 等 surveillance taxonomy。",
            "CFTC disruptive trading practices 来源可支撑 futures/swaps disruptive trading 与 spoofing-related 边界。",
            "但 candidate statement 仍包含 momentum ignition，本包 source_refs 未提供 momentum ignition 的直接来源。",
            "范围审计已明确要求补 momentum ignition 直接来源，或删除 / 降级为 pending source 项。",
        ],
        "required_followups": [
            "补 FINRA/SEC/CFTC/ESMA/IOSCO 中明确覆盖 momentum ignition 的直接来源。",
            "将 taxonomy 明确写成 surveillance labels / reason codes / manual escalation context，不得写成 manipulation finding。",
            "补 legal_owner_required=true、manual_review_required=true、not_hard_gate=true。",
        ],
        "patch_notes": {
            "source": ["保留 FINRA Manipulative Trading 与 CFTC Disruptive Trading Practices。", "补 momentum ignition 直接来源后再审。"],
            "content": ["taxonomy 不等于法律结论。", "不得把普通做市、撤单或订单簿管理直接归类为操纵。"],
            "boundary": ["不得输出法律意见。", "不得生成操纵定性。", "不得把异常标签直接变成硬阻断。"],
            "conflict": [],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_market_access_dea_regulatory_boundary_required_001",
        "research_task_id": "P53-TR-MA01",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "SEC Rule 15c3-5 / SEC FAQ 足以支撑 US securities market access controls、direct and exclusive control、regular / annual review 与 supervisory procedures。",
            "ESMA MiFID II Article 17 足以支撑 EU algorithmic trading / DEA controls、records、risk controls。",
            "FIA automated trading risk controls 可作为行业实践辅助来源。",
            "claim 明确 CEK-TA 只能沉淀证据契约和边界，不能输出合规意见、具体阈值或监管满足声明。",
        ],
        "required_followups": [
            "进入 reviewed 前按 source group 拆分 US SEC 15c3-5、EU MiFID Article 17、FIA industry practice。",
            "不得把 SEC / FINRA / ESMA 规则泛化到 crypto、期货或非美国/欧盟市场。",
            "不得输出信用额度、保证金比例、订单规模阈值、合规满足声明。",
        ],
        "patch_notes": {
            "source": ["保留 SEC Rule 15c3-5、SEC FAQ、ESMA MiFID II Article 17、FIA automated trading controls。"],
            "content": ["拆成 market_access_owner、pre_trade_controls、recordkeeping、jurisdiction_caveat、periodic_review、venue_or_broker_rules。"],
            "boundary": ["不得输出合规意见。", "不得输出具体阈值。", "不得生成交易许可或 hard gate。"],
            "conflict": [],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_trade_audit_time_synchronization_required_001",
        "research_task_id": "P53-TR-TS01",
        "decision": "accepted_for_draft",
        "confidence": "high",
        "reasons": [
            "FINRA Rule 6820 支撑 business clock synchronization、NIST atomic clock、drift 和 daily synchronization。",
            "CAT clock synchronization guidance 支撑 CAT reporting clock sync / certification 语境。",
            "MiFID RTS 25 支撑 EU trading venue / member timestamp accuracy 和 UTC time reference。",
            "OpenTelemetry 支撑 logs / metrics / traces / observability，但不能替代金融 clock synchronization rules。",
            "claim 明确 no trusted clock sync 只能输出 ordering_unknown，不得推导执行质量、合规结论或交易许可。",
        ],
        "required_followups": [
            "进入 reviewed 前补 audit_time_sync_context schema extract。",
            "按 source group 标注 FINRA/CAT 为 US CAT 语境，RTS 25 为 EU 语境，OpenTelemetry 为 observability 语境。",
            "不得给出具体硬件采购建议、高频策略建议或交易许可。",
        ],
        "patch_notes": {
            "source": ["保留 FINRA Rule 6820、CAT Clock Sync、MiFID RTS 25、OpenTelemetry Observability Primer。"],
            "content": [
                "保留 clock_source、sync_status、timestamp_precision、timezone、drift_policy、ordering_caveat、last_sync_at、sync_evidence_ref。",
                "no_trusted_clock_sync_result 必须等于 ordering_unknown。",
            ],
            "boundary": ["不得推导执行质量结论。", "不得推导合规结论。", "不得生成交易许可或 hard gate。"],
            "conflict": [],
        },
    },
]


MOMENTUM_IGNITION_SOURCE: dict[str, Any] = {
    "source_id": "P53-SRC-TR-011",
    "source_title": "Manipulative Trading | FINRA 2024 Annual Regulatory Oversight Report",
    "source_url": "https://www.finra.org/rules-guidance/guidance/reports/2024-finra-annual-regulatory-oversight-report/manipulative-trading",
    "source_type": "regulatory_report",
    "publisher": "FINRA",
    "published_at": None,
    "accessed_at": TODAY,
    "version": None,
    "authority_level": "A1",
    "jurisdiction_or_scope": "US broker-dealer surveillance",
    "reliability": "high",
    "score": 90,
    "relevance": "high",
    "freshness": "time_sensitive",
    "limitations": [
        "只支撑美国 broker-dealer surveillance 语境，不直接生成法律裁决。",
        "只作为 momentum ignition 直接来源；不得把 taxonomy 写成操纵定性或自动 hard gate。",
    ],
    "evidence_summary": "FINRA 2024 Manipulative Trading 报告直接列出 Momentum Ignition Trading，并要求 firms 设计监控以检测潜在 momentum ignition trading，包括 layering/spoofing variants 和 marking the close 等语境。",
    "quoted_excerpt_allowed": False,
}


def json_dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def find_candidate_path(candidate_id: str) -> Path:
    matches = sorted(CANDIDATE_ROOT.glob(f"**/{candidate_id}.json"))
    if not matches:
        raise FileNotFoundError(candidate_id)
    if len(matches) > 1:
        raise RuntimeError(f"multiple candidates found for {candidate_id}: {matches}")
    return matches[0]


def merge_patch_notes(candidate: dict[str, Any], patch_notes: dict[str, list[str]]) -> None:
    audit_patch_notes = candidate.setdefault("audit_patch_notes", {})
    for key in ("source", "content", "boundary", "conflict"):
        values = audit_patch_notes.setdefault(key, [])
        for item in patch_notes.get(key, []):
            if item not in values:
                values.append(item)


def update_review(candidate: dict[str, Any], result: dict[str, Any], status: str) -> None:
    review = candidate.setdefault("review", {})
    review["review_status"] = status
    review["default_guidance_allowed"] = False
    review["approved_allowed"] = False
    review["hard_gate_allowed"] = False
    review["legal_opinion_allowed"] = False
    review["trade_execution_advice_allowed"] = False
    review["risk_threshold_advice_allowed"] = False
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "decision": result["decision"],
        "confidence": result["confidence"],
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "imported_at": TODAY,
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }


def update_candidate(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    decision = result["decision"]
    status = candidate.setdefault("status", {})
    status["updated_at"] = TODAY
    status["review_status"] = decision
    status["ingestion_decision"] = decision
    if decision == "accepted_for_draft":
        status["decision_reason"] = (
            "Phase 53 外部严格审计结论为 accepted_for_draft；candidate 不是 formal knowledge，"
            "不得视为 reviewed/approved/default guidance/hard gate。"
        )
        workflow_stage = "accepted_for_draft"
    else:
        status["decision_reason"] = (
            "Phase 53 外部严格审计结论为 needs_more_evidence；已按 patch notes 补证，"
            "等待补证二审，仍不得视为 accepted/reviewed/approved/default guidance/hard gate。"
        )
        workflow_stage = "supplemented_for_reaudit"

    update_review(candidate, result, decision)
    merge_patch_notes(candidate, result["patch_notes"])

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = workflow_stage
    workflow["last_audit_result_id"] = AUDIT_RESULT_ID
    workflow["last_audit_decision"] = decision
    workflow["next_allowed_decisions"] = ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"]
    workflow["forbidden_decisions"] = [
        "reviewed",
        "approved",
        "default_guidance",
        "hard_gate",
        "legal_opinion",
        "trade_execution_advice",
    ]

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["hidden_from_default_queue"] = True
    machine_gate["visible_in_default_guidance_queue"] = False
    machine_gate["reason"] = f"{decision}; no reviewed/approved/default/hard gate created by Phase 53 candidate audit import."

    return candidate


def supplement_market_conduct(candidate: dict[str, Any]) -> dict[str, Any]:
    source_refs = candidate.setdefault("source_refs", [])
    if not any(source.get("source_id") == MOMENTUM_IGNITION_SOURCE["source_id"] for source in source_refs):
        source_refs.append(MOMENTUM_IGNITION_SOURCE)

    claim = candidate.setdefault("claim", {})
    evidence_summary = claim.get("evidence_summary", "")
    addition = " / FINRA 2024 Manipulative Trading report directly supports Momentum Ignition Trading surveillance context."
    if addition not in evidence_summary:
        claim["evidence_summary"] = f"{evidence_summary}{addition}"
    claim["interpretation_notes"] = (
        "本候选已补 momentum ignition 直接来源，但仍需补证二审；taxonomy 只用于 surveillance labels、reason codes 和人工复核上下文，不得作为法律结论。"
    )

    source_quality = candidate.setdefault("source_quality", {})
    source_quality["primary_source_count"] = len(source_refs)
    limitations = source_quality.setdefault("limitations", [])
    for limitation in MOMENTUM_IGNITION_SOURCE["limitations"]:
        if limitation not in limitations:
            limitations.append(limitation)

    audit_patch_notes = candidate.setdefault("audit_patch_notes", {})
    source_notes = audit_patch_notes.setdefault("source", [])
    note = "已补 FINRA 2024 Manipulative Trading 作为 momentum ignition 直接来源，供补证二审核验。"
    if note not in source_notes:
        source_notes.append(note)

    return candidate


def main() -> None:
    audit_payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "audited_at": TODAY,
        "summary": {
            "total": len(AUDIT_RESULTS),
            "accepted_for_draft": sum(1 for item in AUDIT_RESULTS if item["decision"] == "accepted_for_draft"),
            "needs_more_evidence": sum(1 for item in AUDIT_RESULTS if item["decision"] == "needs_more_evidence"),
            "rejected": 0,
            "blocked": 0,
        },
        "hard_boundaries": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "candidate_results": AUDIT_RESULTS,
    }
    json_dump(AUDIT_RESULT_PATH, audit_payload)

    changed: list[dict[str, str]] = []
    market_conduct_candidate: dict[str, Any] | None = None
    for result in AUDIT_RESULTS:
        path = find_candidate_path(result["candidate_id"])
        candidate = update_candidate(load_json(path), result)
        if result["research_task_id"] == "P53-TR-MC01":
            candidate = supplement_market_conduct(candidate)
            market_conduct_candidate = candidate
        json_dump(path, candidate)
        changed.append({"candidate_id": result["candidate_id"], "decision": result["decision"], "path": path.as_posix()})

    if market_conduct_candidate is None:
        raise RuntimeError("market conduct candidate not processed")

    supplemental_package = {
        "audit_package_id": SUPPLEMENTAL_PACKAGE_ID,
        "phase": 53,
        "created_at": TODAY,
        "status": "supplemental_reaudit_ready",
        "reason": "P53-TR-MC01 首轮审计为 needs_more_evidence；已补 FINRA 2024 Momentum Ignition direct source，等待二审。",
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_reviewed": True,
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "trade_execution_advice_allowed": False,
        },
        "audit_instructions": {
            "language": "zh-CN",
            "must_search_external_sources": True,
            "must_search_requirement": "必须搜索相关专业网站、官方资料、案例和数据，重点核验 FINRA 2024 是否直接支撑 momentum ignition surveillance taxonomy。",
            "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected", "blocked"],
            "required_output_fields": [
                "candidate_id",
                "research_task_id",
                "decision",
                "confidence",
                "reviewed_allowed",
                "approved_allowed",
                "default_guidance_allowed",
                "hard_gate_allowed",
                "reasons",
                "required_followups",
                "patch_notes",
            ],
        },
        "candidates": [market_conduct_candidate],
    }
    json_dump(SUPPLEMENTAL_PACKAGE_PATH, supplemental_package)

    supplemental_gate = {
        "report_id": "phase53_market_conduct_supplemental_reaudit_gate",
        "created_at": TODAY,
        "status": "pass",
        "candidate_id": market_conduct_candidate["candidate_id"],
        "source_count": len(market_conduct_candidate.get("source_refs", [])),
        "momentum_ignition_source_present": any(
            source.get("source_id") == MOMENTUM_IGNITION_SOURCE["source_id"]
            for source in market_conduct_candidate.get("source_refs", [])
        ),
        "permissions": {
            "reviewed_allowed": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }
    json_dump(SUPPLEMENTAL_GATE_PATH, supplemental_gate)

    import_report = {
        "report_id": "phase53_audit_import_report",
        "task_id": TASK_ID,
        "created_at": TODAY,
        "audit_result_id": AUDIT_RESULT_ID,
        "audit_result_path": AUDIT_RESULT_PATH.relative_to(resolve_repo_path(".", start_file=__file__)).as_posix(),
        "accepted_for_draft_count": 4,
        "needs_more_evidence_count": 1,
        "supplemented_for_reaudit_count": 1,
        "supplemental_reaudit_package": SUPPLEMENTAL_PACKAGE_PATH.relative_to(resolve_repo_path(".", start_file=__file__)).as_posix(),
        "supplemental_gate": SUPPLEMENTAL_GATE_PATH.relative_to(resolve_repo_path(".", start_file=__file__)).as_posix(),
        "changed_candidates": changed,
        "boundary": "No reviewed/approved/default guidance/hard gate created. Market Conduct still requires supplemental external re-audit.",
    }
    json_dump(IMPORT_REPORT_PATH, import_report)

    print(json.dumps({"updated": len(changed), "supplemental_package": str(SUPPLEMENTAL_PACKAGE_PATH)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
