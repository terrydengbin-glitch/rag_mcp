"""Apply Phase 53 reviewed/caveat_only preparation audit result.

The reviewed-preparation audit allows three Trading Engineering candidates to
become formal reviewed/caveat_only knowledge. Two AI Engineering candidates
remain needs_more_evidence and must not be materialized yet.

This script never creates approved knowledge, default guidance, hard gates,
legal opinions, manipulation findings, compliance satisfaction statements,
risk thresholds, or trading execution advice.
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


TODAY = "2026-06-13"
TASK_ID = "CEK-TA-524"
AUDIT_RESULT_ID = "audit_phase53_reviewed_preparation_20260613"
PACKAGE_ID = "phase53_reviewed_preparation_audit_package_20260613"

REPO_ROOT = resolve_repo_path(".", start_file=__file__)
CANDIDATE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "candidates", start_file=__file__)
KNOWLEDGE_ROOT = resolve_repo_path("codex-expert-kit", "rag", "knowledge", start_file=__file__)
AUDIT_RESULT_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
IMPORT_REPORT_PATH = resolve_repo_path("docs", "reports", "phase53_reviewed_preparation_import_report.json", start_file=__file__)


RESULTS: list[dict[str, Any]] = [
    {
        "candidate_id": "cand_20260613_phase53_trading_ai_agent_threat_model_required_001",
        "research_task_id": "P53-AI-SEC01",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "NIST/OWASP/MITRE 足以支撑外部威胁面，但 reviewed/caveat_only 层需要 CEK-TA 内部 tool_permission_boundary、memory_write_policy、rag_source_trust、final_gate_bypass_denied 字段契约。",
            "当前包只有字段列表，没有 MCP tool governance / memory governance / final gate boundary 的 contract extract 或 hash。",
        ],
        "required_followups": [
            "补 MCP/tool governance internal contract extract 或 hash。",
            "补 memory governance contract extract。",
            "补 final_gate_boundary contract extract。",
            "正式文本必须避免漏洞利用步骤，只保留 threat model / audit checklist / governance boundary。",
        ],
        "patch_notes": {
            "source": [
                "保留 NIST AI RMF / NIST AI 600-1、OWASP LLM Top 10、MITRE ATLAS。",
                "新增 CEK-TA MCP/tool governance、memory governance、final gate boundary 内部 contract 来源。",
            ],
            "content": [
                "拆成 threat_surface_taxonomy、tool_permission_boundary、memory_write_policy、rag_source_trust、final_gate_bypass_denied。",
                "memory_poisoning 可以保留，但必须绑定 memory_write_policy 和 memory_integrity evidence。",
            ],
            "boundary": [
                "不得生成漏洞利用步骤。",
                "不得生成交易建议。",
                "不得把 AI security risk 自动解释成交易 hard gate。",
                "不得让 LLM/RAG/MCP 直接触发交易许可。",
            ],
            "conflict": ["AI Engineering 只拥有安全治理边界；Risk Management / Live Execution 拥有最终运行控制。"],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_ai_sbom_model_sbom_required_001",
        "research_task_id": "P53-AI-SBOM01",
        "decision": "needs_more_evidence",
        "confidence": "medium_high",
        "reasons": [
            "CISA SBOM、CISA AI SBOM、OWASP LLM Top 10、Model Cards 足以支撑方向。",
            "reviewed/caveat_only 层字段覆盖 model_sbom、dataset_sbom、rag_index_sbom、container_dependency_sbom、inference_service_sbom，需要 CycloneDX ML-BOM、SPDX AI/Dataset Profile 或内部 registry contract 直接来源。",
        ],
        "required_followups": [
            "补 CycloneDX ML-BOM 或 SPDX AI / Dataset Profile 作为 model/dataset/dependency schema 直接来源。",
            "或补 CEK-TA model_registry / artifact_registry contract extract。",
            "明确 SBOM 不是安全通过证明、发布批准、合规满足声明或 hard gate。",
            "保留 source_confidentiality_boundary。",
        ],
        "patch_notes": {
            "source": [
                "保留 CISA SBOM、CISA AI SBOM、OWASP LLM Top 10、Model Cards。",
                "新增 CycloneDX ML-BOM / SPDX AI BOM 或内部 model/artifact registry contract。",
            ],
            "content": [
                "拆成 model_sbom、dataset_sbom、rag_index_sbom、container_dependency_sbom、inference_service_sbom。",
                "增加 source_confidentiality_boundary。",
                "LoRA/adapter、embedding model、RAG index 必须有明确字段来源或内部 contract。",
            ],
            "boundary": [
                "SBOM 不等于安全通过证明。",
                "不得暴露未授权供应链信息。",
                "不得生成发布批准、合规满足声明或 hard gate。",
            ],
            "conflict": ["AI SBOM 属于 AI Engineering / Supply Chain Governance，不接管模型发布批准。"],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_market_conduct_surveillance_taxonomy_required_001",
        "research_task_id": "P53-TR-MC01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "FINRA 2026 / 2025 / 2024 Manipulative Trading 来源足以支撑 spoofing、layering、wash_or_self_trade、momentum_ignition、marking_the_close、front_running 作为 surveillance taxonomy。",
            "CFTC disruptive trading practices 来源可作为 futures/swaps disruptive practice 和 spoofing-related 边界来源。",
            "candidate 已明确 legal_owner_required=true、manual_review_required=true、not_hard_gate=true。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 FINRA/CFTC jurisdiction caveat。",
            "不得把普通撤单、做市、报价更新或订单簿管理直接归类为操纵。",
            "如用于非美国证券、crypto、期货或其他 venue，必须补对应 jurisdiction / venue-specific 来源。",
        ],
        "patch_notes": {
            "source": [
                "保留 FINRA 2026 Manipulative Trading。",
                "保留 FINRA 2024 Manipulative Trading 作为 momentum ignition direct source。",
                "保留 CFTC Disruptive Trading Practices。",
            ],
            "content": [
                "surveillance_taxonomy 可包含 spoofing、layering、wash_or_self_trade、momentum_ignition、marking_the_close、front_running。",
                "taxonomy 只能用于 surveillance labels、reason codes、人工复核和 escalation context。",
                "保留 evidence_required：order_event_id、cancel_event_id、fill_event_id、venue、session、timestamp_quality。",
            ],
            "boundary": [
                "不得输出法律意见。",
                "不得生成操纵定性。",
                "不得把异常标签直接变成硬阻断。",
                "不得生成交易许可或 hard gate。",
            ],
            "conflict": ["Legal / compliance owner 才能作正式判断；CEK-TA 只提供审计上下文。"],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_market_access_dea_regulatory_boundary_required_001",
        "research_task_id": "P53-TR-MA01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "SEC Rule 15c3-5 / SEC FAQ 足以支撑美国 securities market access、direct/exclusive control、regular review、supervisory procedures。",
            "ESMA MiFID II Article 17 足以支撑 EU algorithmic trading / DEA controls、records、risk controls。",
            "FIA automated trading controls 可作为 industry practice 辅助来源。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须保留 US SEC、EU MiFID、FIA source-group caveat。",
            "不得把 SEC / FINRA / ESMA 规则泛化到 crypto、期货或非美国/欧盟市场。",
            "不得输出信用额度、保证金比例、订单规模阈值、合规满足声明。",
        ],
        "patch_notes": {
            "source": ["保留 SEC Rule 15c3-5、SEC FAQ、ESMA MiFID II Article 17、FIA automated trading controls。"],
            "content": [
                "保留 market_access_owner、pre_trade_controls、recordkeeping、jurisdiction_caveat、periodic_review、venue_or_broker_rules。",
                "明确 CEK-TA 只能沉淀 evidence contract / owner boundary / recordkeeping checklist。",
            ],
            "boundary": ["不得输出合规意见。", "不得输出具体阈值。", "不得生成交易许可或 hard gate。"],
            "conflict": ["Live Execution / Risk Management 拥有运行时控制；CEK-TA 只定义知识边界。"],
        },
    },
    {
        "candidate_id": "cand_20260613_phase53_trade_audit_time_synchronization_required_001",
        "research_task_id": "P53-TR-TS01",
        "decision": "accepted_for_reviewed_caveat_only",
        "confidence": "high",
        "reasons": [
            "FINRA Rule 6820、CAT guidance、MiFID RTS 25 足以支撑金融事件 clock source、sync status、timestamp precision、drift policy 与 clock synchronization 语境。",
            "OpenTelemetry 足以支撑模型推理和 RAG/MCP 审计日志的 observability 语境，但不替代金融 clock synchronization 规则。",
            "candidate 已提供 audit_time_sync_context schema extract，并明确 no_trusted_clock_sync_result=ordering_unknown。",
        ],
        "required_followups": [
            "正式 reviewed/caveat_only 文本必须按 source group 标注 FINRA/CAT 为 US CAT 语境，RTS 25 为 EU 语境，OpenTelemetry 为 observability 语境。",
            "不得给出具体硬件采购建议、高频策略建议或交易许可。",
            "ordering_unknown 只能作为审计 caveat，不能成为 hard gate。",
        ],
        "patch_notes": {
            "source": ["保留 FINRA Rule 6820、CAT Clock Sync、MiFID RTS 25、OpenTelemetry Observability Primer。"],
            "content": [
                "保留 clock_source、sync_status、timestamp_precision、timezone、drift_policy、ordering_caveat、last_sync_at、sync_evidence_ref。",
                "no_trusted_clock_sync_result 必须等于 ordering_unknown。",
            ],
            "boundary": ["不得推导执行质量结论。", "不得推导合规结论。", "不得生成交易许可或 hard gate。"],
            "conflict": ["Data / Live / Replay / RAG 各自拥有事件事实；Time Sync 只提供审计上下文。"],
        },
    },
]


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def sanitize_filename(knowledge_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", knowledge_id).strip("_") + ".json"


def find_candidate(candidate_id: str) -> tuple[Path, dict[str, Any]]:
    matches = sorted(CANDIDATE_ROOT.glob(f"**/{candidate_id}.json"))
    if not matches:
        raise FileNotFoundError(candidate_id)
    if len(matches) > 1:
        raise RuntimeError(f"multiple candidates found for {candidate_id}")
    return matches[0], load_json(matches[0])


def knowledge_id_for(candidate: dict[str, Any]) -> str:
    workflow = candidate.get("workflow") if isinstance(candidate.get("workflow"), dict) else {}
    explicit = workflow.get("proposed_knowledge_id") or workflow.get("formal_knowledge_id")
    if explicit:
        return str(explicit)
    normalized = str(candidate.get("claim", {}).get("normalized_claim") or candidate.get("research_task_id"))
    return f"kb_phase53.{normalized}"


def title_for(candidate: dict[str, Any]) -> str:
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    return str(claim.get("title") or claim.get("statement") or candidate.get("research_task_id"))[:120]


def source_evidence(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for source in as_list(candidate.get("source_refs")):
        if not isinstance(source, dict):
            continue
        output.append(
            {
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
                "limitations": as_list(source.get("limitations")),
            }
        )
    return output


def build_formal_item(candidate: dict[str, Any], result: dict[str, Any]) -> dict[str, Any]:
    classification = candidate.get("classification") if isinstance(candidate.get("classification"), dict) else {}
    applicability = candidate.get("applicability") if isinstance(candidate.get("applicability"), dict) else {}
    claim = candidate.get("claim") if isinstance(candidate.get("claim"), dict) else {}
    source_refs = as_list(candidate.get("source_refs"))
    knowledge_id = knowledge_id_for(candidate)
    canonical_node_id = str(classification.get("canonical_node_id") or classification.get("tree_node_id"))
    return {
        "schema_version": "1.1.0",
        "knowledge_id": knowledge_id,
        "title": title_for(candidate),
        "metadata": {
            "partition_id": classification.get("partition_id"),
            "domain": classification.get("domain"),
            "subdomain": classification.get("subdomain"),
            "rule_type": classification.get("rule_type", "governance_boundary"),
            "claim_type": classification.get("claim_type"),
            "content_type": "json",
            "project_binding": "none",
            "tree_node_id": classification.get("tree_node_id"),
            "tree_path": classification.get("tree_path"),
            "canonical_node_id": canonical_node_id,
            "canonical_tree_path": classification.get("tree_path"),
            "risk_level": "high",
            "used_for": classification.get("used_for", []),
            "source_candidate_id": candidate.get("candidate_id"),
            "research_task_id": candidate.get("research_task_id"),
            "phase": "Phase 53",
            "classification_notes": "Phase 53 formal reviewed/caveat_only；只用于审计上下文、schema review、RAG 检索和人工复核，不是 approved/default guidance/hard gate。",
            "related_nodes": classification.get("related_nodes", []),
        },
        "applicability": {
            "market": applicability.get("market", "general"),
            "asset": applicability.get("asset", "general"),
            "timeframe": applicability.get("timeframe", "general"),
            "data_granularity": applicability.get("data_granularity", "general"),
            "project_type": applicability.get("project_type", "external_trading_ai_project"),
            "applies_when": as_list(applicability.get("applies_when")),
            "not_applicable_when": as_list(applicability.get("not_applicable_when")),
        },
        "content": {
            "statement": claim.get("statement"),
            "rationale": claim.get("interpretation_notes") or claim.get("evidence_summary"),
            "normalized_claim": claim.get("normalized_claim"),
            "claim_strength": "reviewed_caveat_only",
            "performance_claim": False,
            "procedure": [
                "确认问题属于 Phase 53 的 AI/Trading 安全、市场行为或运行治理范围。",
                "读取本知识时必须同时返回 source_evidence、review_status、machine_gate、适用范围、不适用场景和 jurisdiction/source caveat。",
                "如果请求法律意见、操纵定性、合规满足声明、交易许可、风险阈值或实盘执行建议，必须拒绝并提示转交对应 owner。",
                "如应用到非来源覆盖的 market、venue、jurisdiction 或 asset class，必须要求外接项目补充对应来源。",
            ],
            "examples": [],
            "anti_patterns": as_list(candidate.get("anti_patterns"))
            + [
                "把 reviewed/caveat_only 当作 approved 或默认指导。",
                "把审计标签、监管边界或时间同步 caveat 解释成交易 hard gate。",
                "输出法律意见、操纵定性、合规满足声明、交易许可或风险阈值。",
            ],
            "validation": [
                "review.review_status 必须为 reviewed，review_mode 必须为 caveat_only。",
                "approved_allowed、default_guidance_allowed、hard_gate_allowed 必须为 false。",
                "source_evidence 必须包含官方监管、标准、交易所、行业协议或官方文档来源。",
                "MCP/SearchLab default guidance 查询不得把本条作为 approved 指导返回。",
            ],
            "risk_notes": as_list(applicability.get("limitations"))
            + result["required_followups"]
            + [
                "本条不是 approved，不进入默认指导，不启用 hard gate。",
                "本条不得生成法律意见、合规满足声明、交易许可、风险阈值或实盘执行建议。",
            ],
            "citation_notes": "；".join(str(ref.get("evidence_summary", "")) for ref in source_refs if isinstance(ref, dict)),
            "audit_patch_notes": result["patch_notes"],
        },
        "assumptions": as_list(applicability.get("assumptions")),
        "source_evidence": source_evidence(candidate),
        "source_quality": candidate.get("source_quality", {}),
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": as_list(candidate.get("conflict_audit", {}).get("checked_against")),
            "conflicts": [],
            "resolution_summary": "reviewed/caveat_only 准备审计通过；formal creation 保持 caveat_only，不创建 approved、default guidance 或 hard gate。",
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "review": {
            "review_status": "reviewed",
            "review_mode": "caveat_only",
            "confidence": result["confidence"],
            "freshness": candidate.get("review", {}).get("freshness", "time_sensitive"),
            "reviewer": "external_ai_strict_audit_and_codex",
            "reviewed_at": TODAY,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "source_candidate_id": candidate.get("candidate_id"),
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "ai_audit": {
                "audit_result_id": AUDIT_RESULT_ID,
                "package_id": PACKAGE_ID,
                "decision": "accepted_for_reviewed_caveat_only",
                "reviewed_allowed": True,
                "approved_allowed": False,
                "default_guidance_allowed": False,
                "hard_gate_allowed": False,
                "legal_opinion_allowed": False,
                "trade_execution_advice_allowed": False,
                "risk_threshold_advice_allowed": False,
                "reasons": result["reasons"],
                "patch_notes": result["patch_notes"],
            },
            "decision_log": [
                {
                    "at": TODAY,
                    "actor": "external_ai_strict_audit",
                    "decision": "accepted_for_reviewed_caveat_only",
                    "reason": f"{AUDIT_RESULT_ID}: reviewed/caveat_only allowed; no approved/default/hard gate.",
                },
                {
                    "at": TODAY,
                    "actor": "codex",
                    "decision": "formal_reviewed_created",
                    "reason": f"{TASK_ID}: materialized formal reviewed/caveat_only knowledge.",
                },
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于 AI IDE、MCP、SearchLab 和知识树以 caveat 方式返回审计上下文。",
                "用于生成 schema review、source review、owner boundary、人工复核 checklist。",
                "用于提醒外接项目补充 jurisdiction、venue、source 或内部 contract。",
            ],
            "not_allowed": [
                "不得作为 approved 默认指导。",
                "不得生成法律意见、操纵定性、合规满足声明、交易许可、风险阈值或 hard gate。",
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
            ],
        },
        "machine_gate": {
            "default_guidance": "caveat_only",
            "review_visibility": "reviewed_caveat_only",
            "reason": "reviewed/caveat_only audit passed; approved/default guidance/hard gate remain disabled.",
            "requires_human_escalation": False,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "contribution": {
            "contribution_id": None,
            "source_project": None,
            "sanitization_status": "not_applicable",
            "private_data_removed": True,
            "generic_mapping_notes": "Generated from Phase 53 public-source candidate; no project-private trading facts included.",
        },
        "phase53_conversion": {
            "source_candidate_status": candidate.get("status", {}).get("review_status"),
            "promoted_by_task": TASK_ID,
            "approved_created": False,
            "default_guidance_created": False,
            "hard_gate_created": False,
        },
    }


def update_candidate(candidate: dict[str, Any], result: dict[str, Any], knowledge_path: Path | None, knowledge_id: str | None) -> dict[str, Any]:
    status = candidate.setdefault("status", {})
    review = candidate.setdefault("review", {})
    workflow = candidate.setdefault("workflow", {})
    decision = result["decision"]
    if decision == "accepted_for_reviewed_caveat_only":
        status["review_status"] = "formalized_reviewed"
        status["ingestion_decision"] = "accepted_for_reviewed_caveat_only"
        status["decision_reason"] = (
            "Phase 53 reviewed-preparation 审计通过，已 materialize 为 formal reviewed/caveat_only；"
            "不得视为 approved/default guidance/hard gate。"
        )
        workflow["stage"] = "formalized_reviewed"
        workflow["queue_group"] = "formalized"
        workflow["formal_knowledge_id"] = knowledge_id
        workflow["formal_review_status"] = "reviewed"
        workflow["knowledge_path"] = rel(knowledge_path) if knowledge_path else None
    else:
        status["review_status"] = "needs_more_evidence"
        status["ingestion_decision"] = "needs_more_evidence"
        status["decision_reason"] = (
            "Phase 53 reviewed-preparation 审计要求补证；尚不得 materialize 为 formal reviewed/caveat_only。"
        )
        workflow["stage"] = "needs_more_evidence_for_reviewed_preparation"
        workflow["queue_group"] = "needs_more_evidence"
        workflow["formal_review_status"] = None
    status["updated_at"] = TODAY
    workflow["last_audit_result_id"] = AUDIT_RESULT_ID
    workflow["last_audit_decision"] = decision
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    workflow["hard_gate_allowed"] = False

    review["review_status"] = status["review_status"]
    review["default_guidance_allowed"] = False
    review["approved_allowed"] = False
    review["hard_gate_allowed"] = False
    review["legal_opinion_allowed"] = False
    review["trade_execution_advice_allowed"] = False
    review["risk_threshold_advice_allowed"] = False
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "package_id": PACKAGE_ID,
        "decision": decision,
        "confidence": result["confidence"],
        "reviewed_allowed": decision == "accepted_for_reviewed_caveat_only",
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "legal_opinion_allowed": False,
        "trade_execution_advice_allowed": False,
        "risk_threshold_advice_allowed": False,
        "imported_at": TODAY,
        "reasons": result["reasons"],
        "required_followups": result["required_followups"],
        "patch_notes": result["patch_notes"],
    }
    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "reviewed_preparation_result_imported",
                "reason": f"{AUDIT_RESULT_ID}: {decision}",
            }
        )

    gate = candidate.setdefault("machine_gate", {})
    gate["default_guidance"] = "caveat_only" if decision == "accepted_for_reviewed_caveat_only" else "deny"
    gate["hidden_from_default_queue"] = True
    gate["visible_in_default_guidance_queue"] = False
    gate["approved_allowed"] = False
    gate["default_guidance_allowed"] = False
    gate["hard_gate_allowed"] = False
    gate["reason"] = f"{decision}; no approved/default/hard gate."
    return candidate


def write_formal(item: dict[str, Any]) -> Path:
    partition = str(item["metadata"].get("partition_id") or "KB_06_LIVE_EXECUTION")
    path = KNOWLEDGE_ROOT / partition / sanitize_filename(item["knowledge_id"])
    if path.exists():
        existing = load_json(path)
        if existing.get("review", {}).get("review_status") == "approved":
            raise RuntimeError(f"Refusing to overwrite approved knowledge: {rel(path)}")
    dump_json(path, item)
    return path


def main() -> int:
    audit_payload = {
        "audit_result_id": AUDIT_RESULT_ID,
        "auditor": "GPT-5.5 Thinking",
        "audited_at": TODAY,
        "package_id": PACKAGE_ID,
        "summary": {
            "total": 5,
            "accepted_for_reviewed_caveat_only": 3,
            "needs_more_evidence": 2,
            "rejected": 0,
            "blocked": 0,
        },
        "candidate_results": RESULTS,
        "boundary": "No approved/default guidance/hard gate/legal opinion/manipulation finding/compliance statement/trading execution advice/risk threshold created.",
    }
    dump_json(AUDIT_RESULT_PATH, audit_payload)

    promoted: list[dict[str, Any]] = []
    needs_more: list[dict[str, Any]] = []
    for result in RESULTS:
        candidate_path, candidate = find_candidate(result["candidate_id"])
        knowledge_path: Path | None = None
        knowledge_id: str | None = None
        if result["decision"] == "accepted_for_reviewed_caveat_only":
            formal = build_formal_item(candidate, result)
            knowledge_id = formal["knowledge_id"]
            knowledge_path = write_formal(formal)
            promoted.append(
                {
                    "candidate_id": result["candidate_id"],
                    "research_task_id": result["research_task_id"],
                    "knowledge_id": knowledge_id,
                    "knowledge_path": rel(knowledge_path),
                    "canonical_node_id": formal["metadata"]["canonical_node_id"],
                    "review_status": "reviewed",
                    "machine_gate": "caveat_only",
                }
            )
        else:
            needs_more.append(
                {
                    "candidate_id": result["candidate_id"],
                    "research_task_id": result["research_task_id"],
                    "decision": result["decision"],
                    "required_followups": result["required_followups"],
                }
            )
        updated = update_candidate(candidate, result, knowledge_path, knowledge_id)
        dump_json(candidate_path, updated)

    report = {
        "report_id": "phase53_reviewed_preparation_import_report",
        "generated_at": TODAY,
        "task_id": TASK_ID,
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": PACKAGE_ID,
        "formal_reviewed_created": len(promoted),
        "needs_more_evidence_count": len(needs_more),
        "approved_created": 0,
        "default_guidance_created": 0,
        "hard_gate_created": 0,
        "promoted": promoted,
        "needs_more_evidence": needs_more,
        "boundary": "formal reviewed/caveat_only only for accepted entries; no approved/default guidance/hard gate.",
    }
    dump_json(IMPORT_REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
