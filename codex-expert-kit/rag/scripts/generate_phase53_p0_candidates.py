"""Generate Phase 53 P0 candidate knowledge and audit package.

This script stops at candidate/audit-package stage. It does not create formal
knowledge, reviewed items, approved items, default guidance, or hard gates.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-13"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source(
    source_id: str,
    title: str,
    url: str,
    source_type: str,
    publisher: str,
    summary: str,
    *,
    authority: str = "A1",
    scope: str = "general",
    limitations: list[str] | None = None,
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
        "authority_level": authority,
        "jurisdiction_or_scope": scope,
        "reliability": "high" if authority in {"A1", "A2"} else "medium",
        "score": 90 if authority == "A1" else 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "limitations": limitations or [],
        "evidence_summary": summary,
        "quoted_excerpt_allowed": False,
    }


SOURCES: dict[str, dict[str, Any]] = {
    "P53-SRC-AI-001": source(
        "P53-SRC-AI-001",
        "AI Risk Management Framework | NIST",
        "https://www.nist.gov/itl/ai-risk-management-framework",
        "official_framework",
        "NIST",
        "NIST AI RMF supports AI risk governance across design, development, use, evaluation, and monitoring.",
        scope="AI risk management",
    ),
    "P53-SRC-AI-002": source(
        "P53-SRC-AI-002",
        "OWASP Top 10 for Large Language Model Applications",
        "https://owasp.org/www-project-top-10-for-large-language-model-applications/",
        "security_standard",
        "OWASP",
        "OWASP LLM Top 10 covers prompt injection, training data poisoning, supply chain vulnerabilities, excessive agency, overreliance, and sensitive information disclosure.",
        authority="A2",
        scope="LLM application security",
    ),
    "P53-SRC-AI-003": source(
        "P53-SRC-AI-003",
        "MITRE ATLAS",
        "https://atlas.mitre.org/",
        "threat_knowledge_base",
        "MITRE",
        "MITRE ATLAS supports adversarial AI threat taxonomy and real-world AI attack observations.",
        authority="A2",
        scope="adversarial AI",
    ),
    "P53-SRC-AI-004": source(
        "P53-SRC-AI-004",
        "Software Bill of Materials (SBOM) | CISA",
        "https://www.cisa.gov/topics/information-communications-technology-supply-chain-security/sbom",
        "official_guidance",
        "CISA",
        "CISA SBOM guidance supports software component inventory and supply-chain transparency.",
        scope="software supply chain",
    ),
    "P53-SRC-AI-005": source(
        "P53-SRC-AI-005",
        "Software Bill of Materials for AI - Minimum Elements | CISA",
        "https://www.cisa.gov/resources-tools/resources/software-bill-materials-ai-minimum-elements",
        "official_guidance",
        "CISA",
        "CISA AI SBOM guidance supports AI component transparency and traceability for AI systems.",
        scope="AI supply chain",
    ),
    "P53-SRC-AI-006": source(
        "P53-SRC-AI-006",
        "Model Cards for Model Reporting | Google Research",
        "https://research.google/pubs/model-cards-for-model-reporting/",
        "research",
        "Google Research",
        "Model cards support documenting intended use, limitations, and evaluation conditions.",
        authority="A2",
        scope="model transparency",
    ),
    "P53-SRC-AI-007": source(
        "P53-SRC-AI-007",
        "Observability Primer | OpenTelemetry",
        "https://opentelemetry.io/docs/concepts/observability-primer/",
        "official_docs",
        "OpenTelemetry",
        "OpenTelemetry supports logs, metrics, traces, and external observability for production systems.",
        authority="A2",
        scope="observability",
        limitations=["Does not replace financial clock synchronization rules."],
    ),
    "P53-SRC-TR-001": source(
        "P53-SRC-TR-001",
        "Small Entity Compliance Guide: Rule 15c3-5",
        "https://www.sec.gov/files/rules/final/2010/34-63241-secg.htm",
        "regulation",
        "SEC",
        "SEC Rule 15c3-5 supports market access risk controls for brokers or dealers with market access.",
        scope="US securities market access",
        limitations=["Does not apply universally to all jurisdictions or asset classes."],
    ),
    "P53-SRC-TR-002": source(
        "P53-SRC-TR-002",
        "SEC Staff FAQ on Rule 15c3-5",
        "https://www.sec.gov/rules-regulations/staff-guidance/trading-markets-frequently-asked-questions/divisionsmarketregfaq-0",
        "regulatory_guidance",
        "SEC",
        "SEC FAQ supports direct/exclusive control, regular review, and market access supervisory procedures.",
        scope="US securities market access",
        limitations=["Does not provide numeric risk thresholds."],
    ),
    "P53-SRC-TR-003": source(
        "P53-SRC-TR-003",
        "Manipulative Trading | FINRA 2026 Annual Regulatory Oversight Report",
        "https://www.finra.org/rules-guidance/guidance/reports/2026-finra-annual-regulatory-oversight-report/manipulative-trading",
        "regulatory_report",
        "FINRA",
        "FINRA manipulative trading guidance supports surveillance programs for layering, spoofing, wash trades, and related market conduct risks.",
        scope="US broker-dealer surveillance",
        limitations=["Does not produce legal findings for a specific actor."],
    ),
    "P53-SRC-TR-004": source(
        "P53-SRC-TR-004",
        "FINRA Rule 6820 Clock Synchronization",
        "https://www.finra.org/rules-guidance/rulebooks/finra-rules/6820",
        "rule",
        "FINRA",
        "FINRA Rule 6820 supports business clock synchronization, NIST atomic clock reference, drift, and daily synchronization requirements.",
        scope="CAT reportable events",
        limitations=["Does not apply universally to non-US markets."],
    ),
    "P53-SRC-TR-005": source(
        "P53-SRC-TR-005",
        "MiFID II Article 17 Algorithmic Trading | ESMA",
        "https://www.esma.europa.eu/publications-and-data/interactive-single-rulebook/mifid-ii/article-17-algorithmic-trading",
        "regulation",
        "ESMA",
        "ESMA MiFID II Article 17 supports algorithmic trading controls, DEA controls, records, and risk controls.",
        scope="EU algorithmic trading and DEA",
        limitations=["Does not replace US SEC/FINRA market access rules."],
    ),
    "P53-SRC-TR-006": source(
        "P53-SRC-TR-006",
        "MiFID II RTS 25 Clock Synchronization",
        "https://ec.europa.eu/finance/securities/docs/isd/mifid/rts/160607-rts-25_en.pdf",
        "regulation",
        "European Commission",
        "RTS 25 supports UTC time reference and timestamp accuracy requirements for trading venues and members.",
        scope="EU trading venue clock synchronization",
        limitations=["Does not replace US CAT clock requirements."],
    ),
    "P53-SRC-TR-007": source(
        "P53-SRC-TR-007",
        "CFTC Disruptive Trading Practices",
        "https://www.cftc.gov/LawRegulation/DoddFrankAct/Rulemakings/DF_24_DisruptiveTrading/index.htm",
        "regulatory_guidance",
        "CFTC",
        "CFTC disruptive trading practice materials support futures/swaps market conduct risk context, including spoofing-related boundaries.",
        scope="US futures and swaps disruptive practices",
        limitations=["Does not replace FINRA equity surveillance guidance."],
    ),
    "P53-SRC-TR-009": source(
        "P53-SRC-TR-009",
        "Best Practices for Automated Trading Risk Controls and System Safeguards",
        "https://www.fia.org/sites/default/files/2024-07/FIA_WP_AUTOMATED%20TRADING%20RISK%20CONTROLS_FINAL_0.pdf",
        "industry_guidance",
        "FIA",
        "FIA automated trading risk controls support pre-trade controls, real-time monitoring, and post-trade reporting as industry practice.",
        authority="A2",
        scope="automated trading risk controls",
        limitations=["Does not define CEK-TA internal field contracts or regulatory compliance status."],
    ),
    "P53-SRC-TR-010": source(
        "P53-SRC-TR-010",
        "CAT Clock Synchronization Guidance",
        "https://www.catnmsplan.com/guidance/clock-synchronization",
        "official_plan",
        "CAT NMS Plan",
        "CAT clock synchronization guidance supports certification and clock sync requirements for CAT reporting.",
        scope="US CAT clock synchronization",
        limitations=["Does not cover EU RTS 25."],
    ),
}


def base_candidate(
    *,
    candidate_id: str,
    research_task_id: str,
    partition_id: str,
    domain: str,
    subdomain: str,
    tree_node_id: str,
    canonical_node_id: str,
    title: str,
    normalized_claim: str,
    statement: str,
    applies_when: list[str],
    not_applicable_when: list[str],
    source_ids: list[str],
    related_nodes: list[str],
    claim_type: str,
    used_for: list[str],
    required_fields: dict[str, Any],
    anti_patterns: list[str],
    audit_patch_notes: dict[str, list[str]],
    proposed_knowledge_id: str,
) -> dict[str, Any]:
    refs = [SOURCES[source_id] for source_id in source_ids]
    return {
        "schema_version": "1.1.0",
        "candidate_id": candidate_id,
        "research_task_id": research_task_id,
        "status": {
            "review_status": "candidate_ready",
            "ingestion_decision": "pending_external_ai_audit",
            "decision_reason": "Phase 53 P0 candidate generated after scope audit accept_with_patch. Candidate is not formal knowledge.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": tree_node_id,
            "canonical_node_id": canonical_node_id,
            "tree_path": "CEK-TA / " + ("AI Engineering" if domain == "ai_engineering" else "Trading Engineering"),
            "related_nodes": related_nodes,
            "partition_id": partition_id,
            "domain": domain,
            "subdomain": subdomain,
            "claim_type": claim_type,
            "rule_type": "governance_boundary",
            "used_for": used_for,
        },
        "claim": {
            "claim_id": "claim_001",
            "title": title,
            "statement": statement,
            "normalized_claim": normalized_claim,
            "evidence_summary": " / ".join(ref["evidence_summary"] for ref in refs[:3]),
            "interpretation_notes": "本候选仅定义可审计治理边界；不得作为 approved、default guidance、hard gate、交易建议或法律意见。",
            "claim_strength": "medium_high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "external_trading_ai_project",
            "applies_when": applies_when,
            "not_applicable_when": not_applicable_when,
            "assumptions": [
                "外接项目提供自身 jurisdiction、venue、asset class、broker/adapter、权限和项目事实。",
                "CEK-TA 只沉淀可复用专业边界和证据契约，不接管项目私有运行决策。",
            ],
            "limitations": [
                "本条仍是 candidate，必须经过外部 AI/人工严格审计和补丁回写后才能进入 formal reviewed/caveat_only。",
                "来源具有 jurisdiction、system scope 或 tool scope 限制，不得跨市场泛化。",
            ],
        },
        "required_fields_or_contract": required_fields,
        "anti_patterns": anti_patterns,
        "source_refs": refs,
        "source_quality": {
            "overall_reliability": "high",
            "score": 88,
            "score_version": "1.1.0",
            "primary_source_count": sum(1 for ref in refs if ref["authority_level"] in {"A1", "A2"}),
            "supporting_source_count": 0,
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": sorted({item for ref in refs for item in ref.get("limitations", [])}),
        },
        "conflict_audit": {
            "conflict_status": "visible_context_no_direct_conflict",
            "checked_against": [
                "Phase 52 authoritative gap audit",
                "Phase 53 scope audit accept_with_patch",
                "formal knowledge index visible to local script",
            ],
            "resolution_summary": "未发现与当前 CEK-TA formal knowledge 的可见直接冲突；正式入库前仍需完整 KB 冲突、重复和 owner 边界检查。",
            "open_questions": [
                "外部审计需确认来源是否直接支撑 candidate statement。",
                "外部审计需确认是否需要拆分 jurisdiction 或 owner 边界。",
            ],
        },
        "review": {
            "review_status": "candidate_ready",
            "freshness": "time_sensitive",
            "reviewed_by": None,
            "reviewed_at": None,
            "default_guidance_allowed": False,
            "approved_allowed": False,
            "hard_gate_allowed": False,
            "legal_opinion_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
        },
        "llm_usage_policy": {
            "allowed": [
                "用于外部 AI/人工审计候选知识边界。",
                "用于生成 reviewed/caveat_only 准备项的补丁建议。",
                "用于提醒外接项目声明来源、owner、jurisdiction 和不适用范围。",
            ],
            "not_allowed": [
                "不得作为默认指导。",
                "不得生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。",
                "不得生成法律意见或合规满足声明。",
                "不得启用 hard gate。",
            ],
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate_ready only; external audit required; reviewed/approved/default/hard gate all disabled.",
            "requires_human_escalation": True,
            "hidden_from_default_queue": True,
            "visible_in_default_guidance_queue": False,
        },
        "workflow": {
            "stage": "candidate_ready",
            "phase": 53,
            "next_allowed_decisions": [
                "accepted_for_draft",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
            "forbidden_decisions": [
                "approved",
                "default_guidance",
                "hard_gate",
                "legal_opinion",
                "trade_execution_advice",
            ],
            "target_review_status": "draft",
            "proposed_knowledge_id": proposed_knowledge_id,
            "formal_knowledge_id": None,
        },
        "audit_patch_notes": audit_patch_notes,
        "_audit_export_meta": {
            "exported_at": NOW,
            "package_scope": "phase53_p0_candidate_audit",
            "proposed_knowledge_id": proposed_knowledge_id,
            "candidate_not_formal_knowledge": True,
        },
    }


def build_candidates() -> list[dict[str, Any]]:
    return [
        base_candidate(
            candidate_id="cand_20260613_phase53_trading_ai_agent_threat_model_required_001",
            research_task_id="P53-AI-SEC01",
            partition_id="KB_AI_ENGINEERING",
            domain="ai_engineering",
            subdomain="security_governance",
            tree_node_id="kt.ai_engineering.security_governance.agent_threat_model",
            canonical_node_id="kt.ai_engineering.security_governance.agent_threat_model",
            title="Trading AI Agent Threat Model must be explicit",
            normalized_claim="phase53.trading_ai_agent_threat_model_required.v1",
            statement="交易 AI Agent 必须把 prompt injection、tool misuse、memory poisoning、excessive agency、overreliance、sensitive information disclosure 和 supply chain compromise 作为独立威胁面建模；LLM/RAG/MCP 只能提供分析、审计、解释和检索辅助，不能绕过 deterministic final gate、Risk Management 或 Live Execution owner。",
            applies_when=[
                "外接项目使用 AI IDE、RAG、MCP、记忆层或工具调用链路辅助交易系统开发、审计或运行。",
                "LLM/Agent 可以读取项目上下文、调用工具、写入记忆或影响候选决策建议。",
            ],
            not_applicable_when=[
                "纯离线人工阅读且没有工具调用、记忆写入或自动化影响。",
                "用户请求漏洞利用步骤、绕过安全控制或交易执行动作。",
            ],
            source_ids=["P53-SRC-AI-001", "P53-SRC-AI-002", "P53-SRC-AI-003"],
            related_nodes=[
                "kt.rag_engineering.retrieval_security",
                "kt.mcp_engineering.tool_governance",
                "kt.ai_engineering.project_memory.security_governance",
                "kt.ai_engineering.final_gate.boundary",
            ],
            claim_type="security_governance_boundary",
            used_for=["ai_ide", "rag_engineering", "mcp", "project_memory", "audit_assistant"],
            required_fields={
                "tool_permission_boundary": "required",
                "memory_write_policy": "required",
                "rag_source_trust": "required",
                "final_gate_bypass_denied": True,
                "threat_surface_taxonomy": [
                    "prompt_injection",
                    "tool_misuse",
                    "memory_poisoning",
                    "excessive_agency",
                    "overreliance",
                    "sensitive_information_disclosure",
                    "supply_chain_compromise",
                ],
            },
            anti_patterns=[
                "LLM 可以直接触发交易许可或绕过 final gate。",
                "把 RAG 检索结果当作无审计来源的默认指导。",
                "允许 Agent 在没有权限边界时写入项目记忆或调用外部工具。",
            ],
            audit_patch_notes={
                "source": ["NIST/OWASP/MITRE 只支撑 AI 安全威胁和治理，不证明交易策略有效。"],
                "content": ["候选必须拆成 threat surfaces、owner boundary、not_allowed 三段。"],
                "boundary": ["不能生成漏洞利用步骤、交易建议或 hard gate。"],
                "conflict": ["AI Engineering 只拥有安全治理边界；Risk/Live Execution 拥有最终运行控制。"],
            },
            proposed_knowledge_id="kb_ai_security_governance.phase53.trading_ai_agent_threat_model_required.v1",
        ),
        base_candidate(
            candidate_id="cand_20260613_phase53_ai_sbom_model_sbom_required_001",
            research_task_id="P53-AI-SBOM01",
            partition_id="KB_AI_ENGINEERING",
            domain="ai_engineering",
            subdomain="supply_chain_governance",
            tree_node_id="kt.ai_engineering.supply_chain_governance.ai_sbom",
            canonical_node_id="kt.ai_engineering.supply_chain_governance.ai_sbom",
            title="AI SBOM / Model SBOM must exist before reusable trading AI deployment",
            normalized_claim="phase53.ai_sbom_model_sbom_required.v1",
            statement="外接交易 AI 项目在使用模型、LoRA/adapter、embedding model、RAG index、训练数据、容器、依赖和推理服务前，应维护 AI SBOM / Model SBOM，用于供应链透明度、许可证审计、漏洞影响分析、模型来源追踪和回滚；SBOM 不是安全通过证明。",
            applies_when=[
                "外接项目复用或部署 LLM、embedding、reranker、numeric scorer、RAG index、容器或外部模型服务。",
                "模型或数据资产会被多个项目、环境或 AI IDE 复用。",
            ],
            not_applicable_when=[
                "一次性本地草稿实验且不共享、不部署、不复用。",
                "用户试图用 SBOM 替代安全测试、模型评估或审计批准。",
            ],
            source_ids=["P53-SRC-AI-004", "P53-SRC-AI-005", "P53-SRC-AI-002", "P53-SRC-AI-006"],
            related_nodes=[
                "kt.ai_engineering.model_registry",
                "kt.ai_engineering.training_dataset_boundary",
                "kt.database_storage.artifact_registry",
                "kt.knowledge_governance.license_governance",
            ],
            claim_type="supply_chain_governance_boundary",
            used_for=["model_release_governance", "dataset_governance", "rag_engineering", "security_review"],
            required_fields={
                "model_sbom": ["model_id", "model_version", "provider", "license", "hash_or_digest", "source_uri"],
                "dataset_sbom": ["dataset_id", "dataset_version", "license", "provenance", "privacy_boundary"],
                "rag_index_sbom": ["index_id", "embedding_model", "source_corpus_version", "chunk_policy"],
                "container_dependency_sbom": ["image_digest", "base_image", "package_manifest"],
                "inference_service_sbom": ["service_provider", "api_version", "deployment_region", "data_retention_boundary"],
                "source_confidentiality_boundary": "required",
            },
            anti_patterns=[
                "SBOM 存在即表示模型安全。",
                "未授权暴露模型来源、许可证、私有数据或供应链信息。",
                "缺少模型/数据/容器版本仍允许复用到外接项目。",
            ],
            audit_patch_notes={
                "source": ["CISA 支撑 SBOM/AI SBOM，OWASP 支撑 LLM supply chain 风险，Model Cards 支撑透明度但不替代 SBOM。"],
                "content": ["候选必须拆成 model、dataset、RAG index、container dependency、inference service 五类清单。"],
                "boundary": ["SBOM 不等于安全通过证明，不强制具体工具，不暴露未授权供应链信息。"],
                "conflict": ["AI SBOM 属于 AI Engineering 与 Database/Storage 的交界，但不接管模型发布批准。"],
            },
            proposed_knowledge_id="kb_ai_supply_chain_governance.phase53.ai_sbom_model_sbom_required.v1",
        ),
        base_candidate(
            candidate_id="cand_20260613_phase53_market_conduct_surveillance_taxonomy_required_001",
            research_task_id="P53-TR-MC01",
            partition_id="KB_08_TRADE_ANALYSIS",
            domain="trading_engineering",
            subdomain="market_conduct",
            tree_node_id="kt.trading_engineering.market_conduct.surveillance_taxonomy",
            canonical_node_id="kt.trading_engineering.market_conduct.surveillance_taxonomy",
            title="Market conduct surveillance taxonomy must not be treated as legal finding",
            normalized_claim="phase53.market_conduct_surveillance_taxonomy_required.v1",
            statement="交易系统应将 spoofing、layering、wash/self-trade、momentum ignition、marking the close、front-running 等市场行为风险作为监控 taxonomy 和审计上下文；该 taxonomy 只用于合规/审计/人工复核，不得替代法律结论、操纵定性或自动交易许可。",
            applies_when=[
                "系统处理订单事件、撤单事件、成交、订单簿或交易后复盘标签。",
                "AI 审计助手需要给出市场行为风险 reason code 或人工复核上下文。",
            ],
            not_applicable_when=[
                "只有 K 线价格数据且无订单事件或订单簿证据。",
                "用户请求法律定性、执法结论或针对个人/机构的违法判断。",
            ],
            source_ids=["P53-SRC-TR-003", "P53-SRC-TR-007"],
            related_nodes=[
                "kt.trading_engineering.order_semantics",
                "kt.trading_engineering.audit_trace",
                "kt.trade_analysis.reason_code",
                "kt.live_execution.order_event_log",
            ],
            claim_type="surveillance_taxonomy_boundary",
            used_for=["trade_analysis", "audit_trace", "live_execution_review", "ai_audit_assistant"],
            required_fields={
                "surveillance_taxonomy": [
                    "spoofing",
                    "layering",
                    "wash_or_self_trade",
                    "momentum_ignition",
                    "marking_the_close",
                    "front_running",
                ],
                "legal_owner_required": True,
                "manual_review_required": True,
                "not_hard_gate": True,
                "evidence_required": ["order_event_id", "cancel_event_id", "fill_event_id", "venue", "session", "timestamp_quality"],
            },
            anti_patterns=[
                "把 surveillance label 写成法律结论。",
                "把普通撤单或做市行为直接归类为操纵。",
                "让 LLM 根据 taxonomy 自动阻断订单或认定违法。",
            ],
            audit_patch_notes={
                "source": ["FINRA 支撑 manipulative trading surveillance，CFTC 支撑 disruptive practices 语境。"],
                "content": ["必须写成 surveillance taxonomy，不写成 manipulation finding。"],
                "boundary": ["只能用于 labels/reason codes/escalation context，不得输出法律意见或 hard gate。"],
                "conflict": ["Legal/compliance owner 才能作正式判断；CEK-TA 只提供审计上下文。"],
            },
            proposed_knowledge_id="kb_trading_market_conduct.phase53.market_conduct_surveillance_taxonomy_required.v1",
        ),
        base_candidate(
            candidate_id="cand_20260613_phase53_market_access_dea_regulatory_boundary_required_001",
            research_task_id="P53-TR-MA01",
            partition_id="KB_06_LIVE_EXECUTION",
            domain="trading_engineering",
            subdomain="market_access",
            tree_node_id="kt.trading_engineering.market_access.regulatory_boundary",
            canonical_node_id="kt.trading_engineering.market_access.regulatory_boundary",
            title="Market access and DEA boundaries must be jurisdiction-specific",
            normalized_claim="phase53.market_access_dea_regulatory_boundary_required.v1",
            statement="外接项目若连接 broker、交易所、ATS、DEA 或 sponsored access，应明确 market access owner、预交易金融/监管/错误订单控制、接入权限、周期性 review、venue jurisdiction 和 recordkeeping；CEK-TA 只能沉淀证据契约和边界，不能输出合规意见、具体阈值或监管满足声明。",
            applies_when=[
                "外接项目接入 broker、交易所、ATS、DEA、sponsored access 或自动化订单通道。",
                "系统需要描述 order admission、pre-trade controls、recordkeeping 或 market access owner。",
            ],
            not_applicable_when=[
                "纯离线回测或没有下单权限的模拟分析。",
                "用户要求具体法律意见、监管合规结论或阈值设置。",
            ],
            source_ids=["P53-SRC-TR-001", "P53-SRC-TR-002", "P53-SRC-TR-005", "P53-SRC-TR-009"],
            related_nodes=[
                "kt.live_execution.order_admission",
                "kt.risk_management.pre_trade_controls",
                "kt.trading_engineering.audit_trace.recordkeeping",
                "kt.order_semantics.adapter_contract",
            ],
            claim_type="regulatory_boundary",
            used_for=["live_execution", "risk_management", "broker_adapter", "audit_trace"],
            required_fields={
                "source_groups": {
                    "us_sec_rule_15c3_5": ["market_access_owner", "risk_controls", "direct_exclusive_control", "periodic_review"],
                    "eu_mifid_article_17": ["algorithmic_trading_controls", "DEA_controls", "records", "testing"],
                    "venue_or_broker_rules": ["adapter_mapping_ref", "order_admission_policy_ref"],
                },
                "jurisdiction_caveat": "required",
                "numeric_threshold_forbidden": True,
                "compliance_satisfaction_statement_forbidden": True,
            },
            anti_patterns=[
                "把美国 SEC/FINRA 规则泛化到 EU、crypto、期货或所有市场。",
                "输出信用额度、保证金比例、订单规模阈值。",
                "声明外接项目已满足某监管要求。",
            ],
            audit_patch_notes={
                "source": ["SEC 15c3-5 支撑美国 broker-dealer market access，ESMA Article 17 支撑 EU algo/DEA controls，FIA 仅作行业实践支撑。"],
                "content": ["必须按 source group 拆分 jurisdiction，不混写成全球通用规则。"],
                "boundary": ["只能是 evidence contract/owner boundary/recordkeeping checklist，不能给阈值或合规意见。"],
                "conflict": ["Live Execution/Risk 拥有运行时控制；CEK-TA 只定义知识边界。"],
            },
            proposed_knowledge_id="kb_trading_market_access.phase53.market_access_dea_regulatory_boundary_required.v1",
        ),
        base_candidate(
            candidate_id="cand_20260613_phase53_trade_audit_time_synchronization_required_001",
            research_task_id="P53-TR-TS01",
            partition_id="KB_06_LIVE_EXECUTION",
            domain="trading_engineering",
            subdomain="audit_trace",
            tree_node_id="kt.trading_engineering.audit_trace.time_synchronization",
            canonical_node_id="kt.trading_engineering.audit_trace.time_synchronization",
            title="Trade audit time synchronization must be explicit",
            normalized_claim="phase53.trade_audit_time_synchronization_required.v1",
            statement="交易事件、行情事件、订单状态、成交、风控动作、模型推理和 RAG/MCP 审计日志必须声明 clock source、sync status、timestamp precision、timezone、drift policy 和 ordering caveat；没有可信时间同步证据时，只能标记 ordering_unknown，不得推导执行质量、合规结论或交易许可。",
            applies_when=[
                "系统需要比较行情、订单、成交、风控、模型推理或 RAG/MCP 审计事件先后顺序。",
                "回放、模拟、实盘差异报告或执行质量审计依赖 timestamp。",
            ],
            not_applicable_when=[
                "静态文档知识不需要事件先后证明。",
                "人工备注时间不能作为机器审计证据。",
            ],
            source_ids=["P53-SRC-TR-004", "P53-SRC-TR-006", "P53-SRC-TR-010", "P53-SRC-AI-007"],
            related_nodes=[
                "kt.data_engineering.timestamp_alignment",
                "kt.live_execution.order_event_log",
                "kt.replay_simulation.simulation_live_gap_report",
                "kt.ai_engineering.runtime_observability.inference_trace",
                "kt.rag_engineering.audit_trace",
            ],
            claim_type="audit_trace_boundary",
            used_for=["market_data", "live_execution", "replay_simulation", "risk_audit", "rag_mcp_audit"],
            required_fields={
                "audit_time_sync_context": {
                    "clock_source": "required",
                    "sync_status": "required",
                    "timestamp_precision": "required",
                    "timezone": "required",
                    "drift_policy": "required",
                    "ordering_caveat": "required",
                    "last_sync_at": "optional",
                    "sync_evidence_ref": "optional",
                },
                "no_trusted_clock_sync_result": "ordering_unknown",
            },
            anti_patterns=[
                "没有可信时间同步证据却声称事件真实先后顺序。",
                "把 clock sync 状态解释成交易许可。",
                "给出具体硬件采购或高频策略建议。",
            ],
            audit_patch_notes={
                "source": ["FINRA/CAT/RTS25 支撑金融事件时间同步，OpenTelemetry 支撑 AI/RAG 推理日志可观测。"],
                "content": ["必须增加 audit_time_sync_context schema。"],
                "boundary": ["no_trusted_clock_sync 只能得到 ordering_unknown，不能推导执行质量或合规结论。"],
                "conflict": ["Data/Live/Replay/RAG 各自拥有事件事实，Time Sync 只提供审计上下文。"],
            },
            proposed_knowledge_id="kb_trading_audit_trace.phase53.trade_audit_time_synchronization_required.v1",
        ),
    ]


def build_audit_package(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "audit_package_id": "phase53_candidate_audit_package_20260613",
        "phase": 53,
        "created_at": TODAY,
        "status": "candidate_ready_for_external_ai_audit",
        "scope_audit_decision": "accept_with_patch",
        "hard_boundaries": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_reviewed": True,
            "reviewed_is_not_approved": True,
            "approved_allowed": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
            "trade_execution_advice_allowed": False,
            "risk_threshold_advice_allowed": False,
            "legal_opinion_allowed": False,
        },
        "audit_instructions": {
            "language": "zh-CN",
            "must_search_external_sources": True,
            "must_search_requirement": "必须搜索相关专业网站、官方资料、案例和数据，对候选知识进行严格审计。",
            "allowed_decisions": [
                "accepted_for_draft",
                "needs_more_evidence",
                "rejected",
                "blocked",
            ],
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
        "candidates": candidates,
    }


def build_quality_gate(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        if len(candidate.get("source_refs", [])) < 2:
            failures.append({"candidate_id": cid, "reason": "source_refs_less_than_2"})
        if candidate["review"].get("approved_allowed") is not False:
            failures.append({"candidate_id": cid, "reason": "approved_allowed_not_false"})
        if candidate["review"].get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": cid, "reason": "default_guidance_allowed_not_false"})
        if candidate["review"].get("hard_gate_allowed") is not False:
            failures.append({"candidate_id": cid, "reason": "hard_gate_allowed_not_false"})
        if candidate["machine_gate"].get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "reason": "machine_gate_default_guidance_not_deny"})
    return {
        "report_id": "phase53_candidate_quality_gate",
        "generated_at": NOW,
        "candidate_count": len(candidates),
        "failure_count": len(failures),
        "gate_status": "pass" if not failures else "fail",
        "failures": failures,
        "checks": [
            "source_refs >= 2",
            "approved_allowed=false",
            "default_guidance_allowed=false",
            "hard_gate_allowed=false",
            "machine_gate.default_guidance=deny",
        ],
    }


def patch_scope_audit_source_seed() -> None:
    path = resolve_repo_path("docs", "audit", "phase53_knowledge_scope_for_audit.json", start_file=__file__)
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {item["source_id"] for item in data.get("source_seed", [])}
    for source_id in [
        "P53-SRC-TR-002",
        "P53-SRC-TR-006",
        "P53-SRC-TR-007",
        "P53-SRC-AI-007",
    ]:
        if source_id not in existing:
            src = SOURCES[source_id]
            data.setdefault("source_seed", []).append(
                {
                    "source_id": source_id,
                    "publisher": src["publisher"],
                    "url": src["source_url"],
                }
            )
    data["scope_audit_patch_status"] = {
        "decision": "accept_with_patch",
        "patched_at": TODAY,
        "patches_applied": [
            "Added missing source_seed ids P53-SRC-TR-002, P53-SRC-TR-006, P53-SRC-TR-007, P53-SRC-AI-007.",
            "Candidate generation applies source, content, boundary, and conflict patches from scope audit.",
        ],
    }
    write_json(path, data)


def write_report(candidates: list[dict[str, Any]], quality_gate: dict[str, Any]) -> None:
    path = resolve_repo_path("docs", "reports", "phase53_candidate_generation_report.md", start_file=__file__)
    lines = [
        "# Phase 53 P0 候选知识生成报告",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结果",
        "",
        f"- 候选数量：{len(candidates)}",
        f"- 质量门禁：{quality_gate['gate_status']}",
        "- 状态：candidate_ready_for_external_ai_audit",
        "- 边界：不创建 formal knowledge、approved、default guidance 或 hard gate",
        "",
        "## 候选列表",
        "",
        "| candidate_id | research_task_id | canonical_node_id | proposed_knowledge_id |",
        "| --- | --- | --- | --- |",
    ]
    for candidate in candidates:
        lines.append(
            f"| `{candidate['candidate_id']}` | `{candidate['research_task_id']}` | "
            f"`{candidate['classification']['canonical_node_id']}` | "
            f"`{candidate['workflow']['proposed_knowledge_id']}` |"
        )
    lines.extend(
        [
            "",
            "## 审计要求",
            "",
            "外部审计必须搜索相关专业网站、官方资料、案例和数据，并输出 `accepted_for_draft`、`needs_more_evidence`、`rejected` 或 `blocked`。",
            "",
            "所有候选默认：",
            "",
            "```text",
            "approved_allowed=false",
            "default_guidance_allowed=false",
            "hard_gate_allowed=false",
            "trade_execution_advice_allowed=false",
            "legal_opinion_allowed=false",
            "risk_threshold_advice_allowed=false",
            "```",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    candidates = build_candidates()
    destinations = {
        candidates[0]["candidate_id"]: ("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING"),
        candidates[1]["candidate_id"]: ("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING"),
        candidates[2]["candidate_id"]: ("codex-expert-kit", "rag", "candidates", "KB_08_TRADE_ANALYSIS"),
        candidates[3]["candidate_id"]: ("codex-expert-kit", "rag", "candidates", "KB_06_LIVE_EXECUTION"),
        candidates[4]["candidate_id"]: ("codex-expert-kit", "rag", "candidates", "KB_06_LIVE_EXECUTION"),
    }
    for candidate in candidates:
        directory = resolve_repo_path(*destinations[candidate["candidate_id"]], start_file=__file__)
        write_json(directory / f"{candidate['candidate_id']}.json", candidate)

    audit_package = build_audit_package(candidates)
    quality_gate = build_quality_gate(candidates)
    write_json(resolve_repo_path("docs", "audit", "phase53_candidate_audit_package_20260613.json", start_file=__file__), audit_package)
    write_json(resolve_repo_path("docs", "reports", "phase53_candidate_quality_gate.json", start_file=__file__), quality_gate)
    patch_scope_audit_source_seed()
    write_report(candidates, quality_gate)
    print(json.dumps({"candidate_count": len(candidates), "gate_status": quality_gate["gate_status"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
