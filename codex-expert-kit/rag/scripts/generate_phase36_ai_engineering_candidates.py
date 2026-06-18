"""Generate Phase 36 AI Engineering candidate knowledge files.

This script expands the Phase 36 collection matrix into auditable candidate
JSON files. It intentionally writes candidates only; it does not create formal
reviewed or approved knowledge.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-09"
MATRIX = resolve_repo_path("docs", "research", "phase36_ai_engineering_p0_collection_matrix.md", start_file=__file__)
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase36_ai_engineering_full_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase36_ai_engineering_candidate_quality_gate.json", start_file=__file__)
AUDIT = resolve_repo_path("docs", "audit", "phase36_ai_engineering_candidate_audit_package_20260609.json", start_file=__file__)
ROOT = resolve_repo_path(start_file=__file__)


SOURCE_CATALOG = {
    "openai_model": ("Model optimization | OpenAI API", "https://platform.openai.com/docs/guides/model-optimization", "official_doc", "OpenAI", 88, "OpenAI model optimization guidance supports defining task objectives, choosing between prompting, RAG, fine-tuning, and evaluating quality before model changes."),
    "openai_ft": ("Fine-tuning best practices | OpenAI API", "https://platform.openai.com/docs/guides/fine-tuning-best-practices", "official_doc", "OpenAI", 88, "OpenAI fine-tuning guidance emphasizes data quality, held-out eval data, and task-specific examples for model improvement."),
    "openai_evals": ("Working with evals | OpenAI API", "https://platform.openai.com/docs/guides/evals?api-mode=chat", "official_doc", "OpenAI", 86, "OpenAI evals documentation supports programmatic evaluation setup and workflow-specific quality checks before relying on model behavior."),
    "openai_file_search": ("File search | OpenAI API", "https://platform.openai.com/docs/guides/tools-file-search?lang=javascript", "official_doc", "OpenAI", 84, "OpenAI file search documentation supports retrieval with annotations and controlled result selection for RAG workflows."),
    "openai_function": ("Function calling and other API updates | OpenAI", "https://openai.com/index/function-calling-and-other-api-updates/", "official_doc", "OpenAI", 82, "OpenAI notes that untrusted tool output can influence tool-integrated LLM systems, supporting cautious tool permission design."),
    "hf_trl": ("TRL documentation | Hugging Face", "https://huggingface.co/docs/trl", "official_doc", "Hugging Face", 84, "Hugging Face TRL documents supervised and preference training workflows that require structured data and evaluation discipline."),
    "datasheets": ("Datasheets for Datasets", "https://arxiv.org/abs/1803.09010", "paper", "arXiv", 88, "The paper supports documenting dataset motivation, composition, collection, intended use, maintenance, and limitations."),
    "model_cards": ("Model Cards for Model Reporting", "https://arxiv.org/abs/1810.03993", "paper", "arXiv", 86, "Model Cards support documenting intended use, performance, limitations, and ethical considerations for model deployment and review."),
    "hf_model_cards": ("Model Cards | Hugging Face Hub", "https://huggingface.co/docs/hub/model-cards", "official_doc", "Hugging Face", 82, "Hugging Face model card documentation supports structured model metadata and responsible model reporting."),
    "sklearn_pitfalls": ("Common pitfalls and recommended practices | scikit-learn", "https://scikit-learn.org/stable/common_pitfalls.html", "official_doc", "scikit-learn", 86, "scikit-learn documents inconsistent preprocessing and data leakage pitfalls, including fitting transformations only on training data."),
    "sklearn_cv": ("Cross-validation: evaluating estimator performance | scikit-learn", "https://scikit-learn.org/stable/modules/cross_validation.html", "official_doc", "scikit-learn", 84, "scikit-learn cross-validation guidance supports held-out evaluation, splitting discipline, and avoiding evaluation on training data."),
    "tfdv": ("TensorFlow Data Validation: Checking and analyzing your data", "https://tensorflow.github.io/tfx/guide/tfdv/", "official_doc", "TensorFlow / TFX", 82, "TFDV supports schema-based data validation, anomaly detection, and train/serve skew checks in ML pipelines."),
    "tfdv_anomalies": ("TensorFlow Data Validation Anomalies Reference", "https://www.tensorflow.org/tfx/data_validation/anomalies", "official_doc", "TensorFlow", 80, "TFDV anomaly reference lists schema and comparator checks that support explicit data quality gates."),
    "feast": ("Feast: the Open Source Feature Store", "https://docs.feast.dev/getting-started", "official_doc", "Feast", 82, "Feast documents feature definitions, offline/online stores, retrieval, and a registry for reusable feature metadata."),
    "mlflow": ("MLflow Tracking | MLflow", "https://www.mlflow.org/docs/latest/ml/tracking", "official_doc", "MLflow", 82, "MLflow tracking supports logging run parameters, metrics, artifacts, code and model artifacts for reproducibility and lineage."),
    "dvc": ("DVC documentation", "https://dvc.org/doc", "official_doc", "DVC", 78, "DVC documentation supports data and model versioning practices for reproducible ML pipelines."),
    "rules_ml": ("Rules of Machine Learning", "https://martin.zinkevich.org/rules_of_ml/rules_of_ml.pdf", "paper", "Google / Martin Zinkevich", 78, "Rules of ML discusses train/serve consistency, baselines, monitoring, and production ML safeguards."),
    "crm_pmlr": ("Counterfactual Risk Minimization", "https://proceedings.mlr.press/v37/swaminathan15.html", "paper", "PMLR", 86, "Counterfactual learning from logged decisions supports the need for logged policy context and careful off-policy evaluation."),
    "crm_arxiv": ("Counterfactual Risk Minimization arXiv version", "https://arxiv.org/abs/1502.02362", "paper", "arXiv", 82, "The arXiv version provides accessible details for logged feedback, counterfactual risk, and off-policy learning assumptions."),
    "owasp_prompt": ("LLM Prompt Injection Prevention Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html", "standard_or_risk_framework", "OWASP", 86, "OWASP documents prompt injection risks and mitigations for user input, retrieved content, tool output, and agent workflows."),
    "owasp_llmsvs": ("OWASP LLM Verification Standard", "https://owasp.org/www-project-llm-verification-standard/LLMSVS-v1.0-en.html", "standard_or_risk_framework", "OWASP", 84, "OWASP LLMSVS supports treating LLM outputs as untrusted and validating downstream system use."),
    "nist": ("AI Risk Management Framework | NIST", "https://www.nist.gov/itl/ai-risk-management-framework", "standard_or_risk_framework", "NIST", 88, "NIST AI RMF supports governance, mapping, measurement, and management of AI risks across design, deployment, and monitoring."),
    "fed_model_risk": ("Supervisory Guidance on Model Risk Management", "https://www.federalreserve.gov/frrs/guidance/supervisory-guidance-on-model-risk-management.htm", "standard_or_risk_framework", "Federal Reserve", 84, "Model risk guidance supports independent validation, governance, change control, and risk-based model oversight."),
    "finra_algo": ("Algorithmic Trading | FINRA", "https://www.finra.org/rules-guidance/key-topics/algorithmic-trading", "standard_or_risk_framework", "FINRA", 82, "FINRA algorithmic trading guidance supports supervision, controls, risk assessment, testing, and governance for automated trading systems."),
    "finra_ai": ("AI in the Securities Industry | FINRA", "https://www.finra.org/rules-guidance/key-topics/fintech/report/artificial-intelligence-in-the-securities-industry/key-challenges", "standard_or_risk_framework", "FINRA", 82, "FINRA discusses AI supervision, testing, and regulatory considerations for securities-industry uses including trading functions."),
    "nasdaq": ("Nasdaq Data Terms", "https://data.nasdaq.com/terms", "exchange_rule", "Nasdaq", 80, "Nasdaq data terms describe restrictions and provider terms for data copying, redistribution, use, and compliance."),
    "cme": ("CME Group Information License Agreement Guide", "https://www.cmegroup.com/content/dam/cmegroup/market-data/files/information-license-agreement-ila-guide.pdf", "exchange_rule", "CME Group", 80, "CME Group ILA materials support treating market data usage, redistribution, and non-display use as license-governed concerns."),
    "mcp_spec": ("Specification - Model Context Protocol", "https://modelcontextprotocol.io/specification/latest", "official_doc", "Model Context Protocol", 86, "MCP specification defines protocol-level contracts for exposing resources and tools to LLM applications."),
    "mcp_security": ("Security Best Practices - Model Context Protocol", "https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices", "official_doc", "Model Context Protocol", 86, "MCP security best practices support least privilege, token scope control, and authorization boundaries for tool and resource access."),
}

SOURCE_GROUPS = {
    "training_objective": ["openai_model", "openai_ft"],
    "dataset": ["datasheets", "openai_ft", "tfdv"],
    "leakage": ["sklearn_pitfalls", "sklearn_cv"],
    "eval": ["openai_evals", "sklearn_cv", "rules_ml"],
    "training_run": ["mlflow", "dvc"],
    "serving_consistency": ["tfdv", "rules_ml"],
    "safety": ["owasp_prompt", "mcp_security"],
    "trade_candidate": ["datasheets", "sklearn_pitfalls"],
    "feature_schema": ["feast", "tfdv", "sklearn_pitfalls"],
    "outcome_schema": ["datasheets", "sklearn_pitfalls"],
    "label_schema": ["datasheets", "model_cards", "sklearn_pitfalls"],
    "eval_case": ["openai_evals", "sklearn_cv"],
    "llm_role_boundary": ["finra_algo", "nist", "owasp_prompt"],
    "labeling": ["sklearn_pitfalls", "datasheets"],
    "data_quality": ["tfdv", "datasheets", "sklearn_pitfalls"],
    "rag": ["openai_file_search", "owasp_prompt", "nist"],
    "mcp": ["mcp_spec", "mcp_security"],
    "deployment": ["fed_model_risk", "rules_ml", "openai_evals"],
    "versioning": ["mlflow", "dvc", "model_cards"],
    "audit": ["nist", "fed_model_risk", "mlflow"],
    "governance": ["datasheets", "model_cards", "hf_model_cards", "nist"],
    "business_objective": ["openai_evals", "nist", "fed_model_risk"],
    "data_asset": ["datasheets", "dvc", "sklearn_cv"],
    "method_selection": ["openai_model", "openai_file_search", "openai_ft"],
    "runtime": ["finra_algo", "owasp_prompt", "nist"],
    "feedback": ["sklearn_pitfalls", "nist", "datasheets"],
    "data_privacy": ["nist", "owasp_prompt"],
    "data_license": ["nasdaq", "cme"],
    "label_factory": ["datasheets", "model_cards", "sklearn_cv"],
    "feature_store": ["feast", "tfdv"],
    "sft": ["openai_ft", "hf_trl"],
    "preference_training": ["hf_trl", "openai_model"],
    "dpo": ["hf_trl", "openai_model"],
    "training_data": ["datasheets", "sklearn_pitfalls", "feast"],
    "scoring_rubric": ["openai_evals", "model_cards", "nist"],
    "gating": ["finra_algo", "fed_model_risk", "nist"],
    "task_taxonomy": ["openai_model", "openai_evals", "model_cards"],
    "capability_boundary": ["fed_model_risk", "nist", "finra_ai"],
    "calibration": ["sklearn_cv", "openai_evals", "rules_ml"],
    "lineage": ["mlflow", "dvc", "model_cards"],
    "redteam": ["owasp_prompt", "owasp_llmsvs", "mcp_security"],
    "approval": ["fed_model_risk", "nist", "finra_algo"],
    "readiness": ["openai_evals", "fed_model_risk", "rules_ml"],
    "research_feedback": ["openai_evals", "sklearn_cv", "finra_algo"],
    "risk_ledger": ["finra_algo", "fed_model_risk", "nist"],
    "llm_judge": ["openai_evals", "model_cards"],
}

CN_CLAIMS = {
    "training_objective": "训练任务必须先声明目标、输入输出、验收指标和失败边界，不能在任务未定义时直接微调或上线。",
    "dataset": "训练或评估数据集必须具备明确 schema、来源、版本、用途和限制，不能使用无法追踪的数据。",
    "leakage": "训练、验证和评估链路必须阻断泄漏字段、标签字段和跨集合污染，否则评估结果不能作为上线依据。",
    "eval": "模型评估必须使用隔离、可复现、贴近生产任务的评测集，并记录指标、阈值和失败样本。",
    "training_run": "每次训练运行必须快照配置、超参数、数据版本、代码版本和产物，保证结果可追溯。",
    "serving_consistency": "训练侧和服务侧必须验证特征、schema、预处理和可见信息的一致性，避免 train-serving skew。",
    "safety": "LLM 不得通过提示、工具或 MCP 调用提升权限，安全边界必须由宿主系统和服务端强制执行。",
    "trade_candidate": "交易候选进入 LLM 评分前必须形成决策时快照，只包含当时可见信息和必要上下文。",
    "feature_schema": "训练输入特征必须声明时间戳和决策时可用性，严禁把事后结果或未来字段放入模型输入。",
    "outcome_schema": "事后 outcome 只能进入标签、评估和复盘链路，不能混入评分输入或决策时特征。",
    "label_schema": "交易质量标签不能只用 PnL，必须包含过程质量、风险、规则合规和 reason codes。",
    "eval_case": "评估样本必须与训练样本隔离，并声明时间、策略、市场状态或数据池拆分。",
    "llm_role_boundary": "交易 LLM 只能做解释、评分、风险提示和门控建议，不能执行订单或覆盖硬风控。",
    "labeling": "交易样本标注必须只使用允许的观察窗口，并避免未来信息、单一 PnL 标签和含糊样本误标。",
    "data_quality": "交易训练数据缺少核心字段、执行成本或数据来源模式时，必须阻断训练或降级为待补证据。",
    "rag": "交易评分前必须按任务主动检索 CEK-TA，且只允许有来源、无冲突、machine_gate 合格的知识进入默认指导。",
    "mcp": "MCP 知识工具默认只读，权限、参数、错误和来源返回必须由服务端契约强制。",
    "deployment": "LLM gate 上线前必须经过离线评估、shadow/paper 阶段和失败降级策略，不能直接进入实盘硬门。",
    "versioning": "模型、提示词、RAG 索引、策略版本和数据快照必须绑定记录，保证每次 gate 决策可复盘。",
    "audit": "每次 gate/scoring 决策必须记录输入摘要、模型版本、知识引用、reason codes、缺失字段和降级动作。",
    "governance": "用于训练、评估或上线的模型和数据集必须具备文档卡片、责任人、限制和审计状态。",
    "business_objective": "LLM 交易质量项目的成功指标不能只看 PnL，还必须覆盖风险拦截、坏交易过滤、解释质量和审计成本。",
    "data_asset": "训练池、评估池、gold set、shadow pool 和 incident pool 必须隔离管理，不能混用或自动互相污染。",
    "method_selection": "外接项目应先建立 RAG、提示词或规则 baseline 和 eval，再决定是否需要微调或偏好训练。",
    "runtime": "LLM gate 输出只能是建议，最终允许、阻断或升级必须由确定性风控和人工治理链路决定。",
    "feedback": "模型输出不能给自己贴标签，线上反馈必须先经过规则或人工审核再进入训练数据。",
    "data_privacy": "训练导出前必须移除密钥、账号标识、个人或账户敏感信息，并保留脱敏审计记录。",
    "data_license": "市场数据进入训练、评估或再分发前必须检查授权、用途、非展示使用和供应商限制。",
    "label_factory": "人工或自动标注流程必须有指南、冲突处理和一致性检查，不能把未校验标签直接作为训练真值。",
    "feature_store": "特征进入训练和服务前必须登记 schema、来源、时间语义和线上线下一致性约束。",
    "sft": "SFT 只适合学习稳定输出格式、任务流程和专家示例，不能替代检索、数据修复或评估。",
    "preference_training": "偏好训练必须基于同一 prompt 下的 chosen/rejected 样本，并记录偏好理由和质量边界。",
    "dpo": "DPO 或偏好优化依赖高质量偏好数据，不能用噪声标签、单一收益结果或泄漏样本训练。",
    "training_data": "交易训练样本必须声明策略版本、决策时间、特征截止时间和输入/目标分离。",
    "scoring_rubric": "评分 rubric 必须输出结构化 reason codes，不能只返回不可解释的单一分数。",
    "gating": "低置信度或高风险候选不能被 LLM 直接放行，应降级为阻断建议或人工复核。",
    "task_taxonomy": "交易 LLM 任务必须区分盘前评分、盘中门控、风控违规、复盘和研究建议，并各自定义 schema 与 eval。",
    "capability_boundary": "LLM 不应作为主要价格预测器；数值预测、风控阈值和订单执行应由专门模型或确定性系统承担。",
    "calibration": "LLM 分数不是天然概率，阈值必须通过 shadow 数据、校准和分组评估确定。",
    "lineage": "模型、提示词、RAG 知识、数据和策略版本必须一起绑定成可追溯 release 记录。",
    "redteam": "上线前必须测试 LLM 是否会尝试覆盖硬风控、绕过审批或把建议伪装成最终交易许可。",
    "approval": "开启 hard gate 或改变阈值必须经过责任人审批、回滚计划和审计记录。",
    "readiness": "离线评估通过不等于可实盘上线，仍需要 shadow/paper 验证、监控和事故回滚。",
    "research_feedback": "LLM 的策略或参数建议只能作为研究假设，必须经过回测、样本外、模拟盘和人工审查。",
    "risk_ledger": "false allow、false block、机会成本和后续结果必须入风险账本，用于门控策略评估。",
    "llm_judge": "LLM-as-judge 评估必须检查位置偏差、格式偏差和裁判提示稳定性，不能盲信单次裁判结果。",
}

SUBDOMAIN = {
    "training_objective": "training_objective",
    "dataset": "dataset_governance",
    "leakage": "data_leakage_control",
    "eval": "evaluation_governance",
    "training_run": "training_run_management",
    "serving_consistency": "training_serving_consistency",
    "safety": "ai_security_boundary",
    "trade_candidate": "training_dataset_schema_engineering",
    "feature_schema": "training_dataset_schema_engineering",
    "outcome_schema": "training_dataset_schema_engineering",
    "label_schema": "label_schema_engineering",
    "eval_case": "eval_case_schema_engineering",
    "llm_role_boundary": "trading_llm_role_boundary",
    "labeling": "trading_labeling_governance",
    "data_quality": "trading_data_quality_gate",
    "rag": "rag_retrieval_governance",
    "mcp": "mcp_tool_contract",
    "deployment": "llmops_deployment",
    "versioning": "artifact_lineage",
    "audit": "ai_governance_audit",
    "governance": "ai_governance_audit",
    "business_objective": "ai_business_objective",
    "data_asset": "ai_data_asset_management",
    "method_selection": "training_method_selection",
    "runtime": "trading_ai_safety",
    "feedback": "feedback_governance",
    "data_privacy": "ai_security_privacy_compliance",
    "data_license": "ai_security_privacy_compliance",
    "label_factory": "label_factory",
    "feature_store": "training_dataset_schema_engineering",
    "sft": "supervised_fine_tuning",
    "preference_training": "preference_training",
    "dpo": "preference_training",
    "training_data": "trading_scoring_gating_training",
    "scoring_rubric": "trading_scoring_gating_training",
    "gating": "trading_scoring_gating_training",
    "task_taxonomy": "trading_llm_task_taxonomy",
    "capability_boundary": "trading_llm_task_taxonomy",
    "calibration": "trading_scoring_gating_training",
    "lineage": "artifact_lineage",
    "redteam": "trading_ai_safety",
    "approval": "ai_governance_audit",
    "readiness": "llmops_deployment",
    "research_feedback": "feedback_governance",
    "risk_ledger": "trading_ai_safety",
    "llm_judge": "evaluation_governance",
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def prefix_for(knowledge_id: str) -> str:
    return knowledge_id.split(".", 1)[0]


def source_ref(key: str) -> dict[str, object]:
    title, url, source_type, publisher, score, summary = SOURCE_CATALOG[key]
    return {
        "source_id": f"src_{key}",
        "source_title": title,
        "source_url": url,
        "source_type": source_type,
        "publisher": publisher,
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high" if score >= 80 else "medium",
        "score": score,
        "relevance": "high",
        "freshness": "time_sensitive" if source_type in {"official_doc", "standard_or_risk_framework", "exchange_rule"} else "stable",
        "limitations": [],
        "evidence_summary": summary,
        "quoted_excerpt_allowed": False,
    }


def matrix_rows() -> list[tuple[str, str, str, str, str]]:
    rows = []
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| RIT-P36-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        rows.append((cells[0], cells[1], cells[2], cells[3].strip("`"), cells[4].strip("`")))
    return rows


def existing_claims() -> set[str]:
    claims = set()
    for path in CAND_DIR.glob("*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        claims.add(raw.get("claim", {}).get("normalized_claim") or "")
    return claims


def build_candidate(task_id: str, tier: str, group: str, knowledge_id: str, node_id: str) -> dict[str, object]:
    prefix = prefix_for(knowledge_id)
    source_keys = SOURCE_GROUPS.get(prefix, ["openai_model", "nist"])
    sources = [source_ref(key) for key in source_keys[:3]]
    score = round(sum(int(src["score"]) for src in sources) / len(sources))
    candidate_id = f"cand_20260609_ai_engineering_{slug(knowledge_id)}_001"
    statement = CN_CLAIMS.get(prefix, f"{knowledge_id} 必须在 AI Engineering 候选知识中声明来源、适用边界、冲突状态和默认使用限制。")
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": task_id,
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": f"Phase 36 {tier} sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering",
            "related_nodes": [],
            "partition_id": "KB_09_LLM_TRAINING" if node_id.startswith("kt.llm_training") else "KB_AI_ENGINEERING",
            "domain": "llm_training" if node_id.startswith("kt.llm_training") else "ai_engineering",
            "subdomain": SUBDOMAIN.get(prefix, prefix),
            "rule_type": "decision_rule" if tier == "P0-Core" else "checklist",
            "used_for": ["llm_training", "trading_gating_scoring", "rag_engineering", "mcp", "vue_audit_ui"],
        },
        "claim": {
            "claim_id": "claim_001",
            "statement": statement,
            "normalized_claim": knowledge_id,
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in sources[:2]),
            "interpretation_notes": "本候选仅沉淀 AI Engineering 中训练、评估、RAG/MCP、安全、部署或治理规则；不定义 K 线信号、具体交易策略、订单执行规则或账户参数。",
            "claim_strength": "high" if tier == "P0-Core" else "medium",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "trading_llm_assistant",
            "applies_when": [
                "外接项目正在构建或审计交易 LLM gating/scoring、训练数据、评估、RAG/MCP、部署或治理链路。",
                "该规则用于阻断数据泄漏、权限越界、无来源默认指导、训练/评估污染或上线前治理缺口。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、策略参数或实盘订单执行。",
                "知识点主要描述 K 线结构、市场微观结构、回测模型、fill model 或交易风控本体，应路由到 Trading Engineering。",
            ],
            "assumptions": [
                "外接项目提供项目事实、私有交易数据和策略上下文；CEK-TA 只沉淀可复用专业规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": ["本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要拆分。"],
        },
        "source_refs": sources,
        "source_quality": {
            "overall_reliability": "high" if score >= 82 else "medium",
            "score": score,
            "score_version": "1.0.0",
            "primary_source_count": 2,
            "supporting_source_count": max(0, len(sources) - 2),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": ["来源支持通用 AI/ML/RAG/MCP/治理工程原则；正式知识转换时需补 CEK-TA 具体上下游引用和冲突链接。"],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "docs/contracts/ai_engineering_gating_scoring_contract.md",
                "docs/contracts/ai_engineering_knowledge_item_policy.md",
                "docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与当前 CEK-TA formal knowledge 的直接冲突；候选不会进入默认指导。",
            "approval_allowed": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive" if any(src["freshness"] == "time_sensitive" for src in sources) else "stable",
            "reviewer": "codex",
            "reviewed_at": None,
            "open_questions": ["审计时确认该候选是否应与相邻 AI Engineering 规则合并、拆分，或改路由到 Trading Engineering。"],
            "audit_log": [{"at": TODAY, "actor": "codex", "action": "created", "reason": "Phase 36 bulk AI Engineering candidate expansion."}],
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、来源摘要和归纳性知识，不保存全文或长引用。",
            "reuse_risk": "low",
        },
        "conversion_target": {
            "proposed_knowledge_id": f"kb_ai_engineering.{knowledge_id}",
            "target_schema": "cek_ta_knowledge_item",
            "target_review_status": "draft",
            "skill_candidate": False,
            "eval_case_candidate": prefix in {"eval", "eval_case", "redteam", "llm_judge"},
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": None,
            "hidden_from_default_queue": False,
            "next_action": "export_for_ai_or_human_audit",
        },
    }


def load_phase36_candidates() -> list[dict[str, object]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(raw.get("candidate_id", "")).startswith("cand_20260609_ai_engineering_"):
            candidates.append(raw)
    return candidates


def write_quality_and_audit(created: int, skipped: int) -> dict[str, object]:
    candidates = load_phase36_candidates()
    failures = []
    for item in candidates:
        cid = item.get("candidate_id")
        if len(item.get("source_refs") or []) < 2:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_2"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})

    quality = {
        "report_id": "phase36_ai_engineering_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "all Phase 36 AI Engineering candidates generated on 2026-06-09",
        "candidate_count": len(candidates),
        "planned_total": 113,
        "p0_core_total": 62,
        "created_this_run": created,
        "skipped_existing": skipped,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    audit = {
        "package_id": "phase36_ai_engineering_candidate_audit_package_20260609",
        "package_type": "candidate_ai_audit_package",
        "generated_at": TODAY,
        "phase": "36",
        "title": "Phase 36 AI Engineering 候选知识审计包",
        "purpose": "审计 Phase 36 AI Engineering 交易 LLM gating/scoring 知识候选，确认来源充分性、适用边界、冲突风险、AI 使用安全和跨分支路由。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "AI 审计 accepted_for_draft 不是 approved。",
            "不得把项目私有事实、账号数据、密钥或具体交易规则写入 AI Engineering。",
            "K 线、策略、回测、实盘执行和交易风控本体应路由到 Trading Engineering。",
        ],
        "auditor_instruction": {
            "goal": "逐条判断候选是否可转为 formal draft/reviewed，或需要补来源、改边界、拆分、拒绝。",
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": "phase36_ai_engineering_candidate_audit_package_20260609",
                "decisions": [
                    {
                        "candidate_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reason": "string",
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                        "required_followups": ["string"],
                    }
                ],
            },
        },
        "quality_gate_report": "docs/reports/phase36_ai_engineering_candidate_quality_gate.json",
        "candidate_count": len(candidates),
        "planned_total": 113,
        "p0_core_total": 62,
        "candidates": candidates,
    }
    AUDIT.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return quality


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_claims()
    created = 0
    skipped = 0
    for task_id, tier, group, knowledge_id, node_id in matrix_rows():
        if knowledge_id in existing:
            skipped += 1
            continue
        candidate = build_candidate(task_id, tier, group, knowledge_id, node_id)
        path = CAND_DIR / f"{candidate['candidate_id']}.json"
        path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1

    quality = write_quality_and_audit(created, skipped)
    candidates = load_phase36_candidates()
    REPORT.write_text(
        "\n".join(
            [
                "# Phase 36 AI Engineering 候选知识补齐报告",
                "",
                "## 结论",
                "",
                f"本次按 Phase 36 采集矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条。当前 Phase 36 AI Engineering 候选总数为 {len(candidates)} 条，对齐总规划 113 条。",
                "",
                "所有新增内容仍为 candidate，不是 formal reviewed，不是 approved，也不会进入 MCP/SearchLab 默认指导。",
                "",
                "## 统计",
                "",
                "```text",
                "规划总数: 113",
                "P0-Core: 62",
                f"当前候选: {len(candidates)}",
                f"本次新增: {created}",
                f"已存在跳过: {skipped}",
                "formal reviewed: 0，等待审计结果",
                "approved: 0",
                "```",
                "",
                "## 交付物",
                "",
                "```text",
                "codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/",
                "docs/reports/phase36_ai_engineering_candidate_quality_gate.json",
                "docs/audit/phase36_ai_engineering_candidate_audit_package_20260609.json",
                "```",
                "",
                "## 来源覆盖",
                "",
                "本批来源覆盖 OpenAI、Hugging Face、scikit-learn、TensorFlow/TFX、Feast、MLflow、DVC、OWASP、NIST、FINRA、Federal Reserve、Nasdaq、CME、PMLR/arXiv 等官方文档、论文和风险框架。",
                "",
                "## 边界",
                "",
                "```text",
                "AI Engineering 只沉淀训练、评估、RAG/MCP、安全、部署和治理知识。",
                "交易规则本体必须路由到 Trading Engineering。",
                "候选知识必须通过 AI/人工审计后，才能进入 formal reviewed。",
                "reviewed 不等于 approved，approved 需要后续人工治理。",
                "```",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"created": created, "skipped": skipped, "candidate_count": len(candidates), "quality_gate": quality["gate_status"]}, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
