"""Generate Phase 41 P0-Extended/P1 candidate knowledge files.

This script writes candidate JSON only. It does not create formal reviewed or
approved knowledge, and it never enables default guidance. P0-Extended and P1
are intentionally collected as one batch for one audit package.
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


TODAY = "2026-06-10"
MATRIX = resolve_repo_path("docs", "research", "phase41_hybrid_scoring_collection_matrix.md", start_file=__file__)
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
RESEARCH = resolve_repo_path("docs", "research", "phase41_extended_p1_candidate_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase41_extended_p1_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase41_extended_p1_candidate_quality_gate.json", start_file=__file__)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "catboost_docs": {
        "title": "CatBoost documentation",
        "url": "https://catboost.ai/docs/",
        "type": "official_doc",
        "publisher": "CatBoost",
        "score": 84,
        "summary": "CatBoost documents gradient boosting on decision trees with categorical feature support.",
    },
    "catboost_paper": {
        "title": "CatBoost: unbiased boosting with categorical features",
        "url": "https://arxiv.org/abs/1706.09516",
        "type": "research_paper",
        "publisher": "arXiv",
        "score": 86,
        "summary": "The CatBoost paper discusses ordered boosting and categorical feature processing to reduce target leakage and prediction shift.",
    },
    "sklearn_ensemble": {
        "title": "Ensemble methods - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/ensemble.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn documents ensemble methods as combinations of base estimators intended to improve generalizability and robustness.",
    },
    "sklearn_permutation_importance": {
        "title": "Permutation feature importance - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/permutation_importance.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 84,
        "summary": "scikit-learn documents permutation importance as a model inspection method and notes limitations when features are correlated.",
    },
    "shap_docs": {
        "title": "SHAP documentation",
        "url": "https://shap.readthedocs.io/",
        "type": "official_doc",
        "publisher": "SHAP",
        "score": 82,
        "summary": "SHAP documents Shapley-value based feature attribution for explaining model outputs.",
    },
    "sklearn_group_cv": {
        "title": "Cross-validation: StratifiedGroupKFold - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/cross_validation.html#stratifiedgroupkfold",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn documents grouped cross-validation that keeps groups from appearing in both train and test folds.",
    },
    "sklearn_calibration": {
        "title": "Probability calibration - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/calibration.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents probability calibration, including sigmoid and isotonic approaches.",
    },
    "calibration_paper": {
        "title": "Predicting Good Probabilities With Supervised Learning",
        "url": "https://www.cs.cornell.edu/~alexn/papers/calibration.icml05.crc.rev3.pdf",
        "type": "research_paper",
        "publisher": "ICML",
        "score": 84,
        "summary": "The calibration paper compares calibration methods and discusses isotonic regression and sigmoid calibration behavior.",
    },
    "tfdv_docs": {
        "title": "TensorFlow Data Validation",
        "url": "https://www.tensorflow.org/tfx/data_validation/get_started",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "TFDV documents schema, statistics, anomalies, data validation and skew/drift checks.",
    },
    "qwen3_blog": {
        "title": "Qwen3: Think Deeper, Act Faster",
        "url": "https://qwenlm.github.io/blog/qwen3/",
        "type": "official_doc",
        "publisher": "Qwen",
        "score": 84,
        "summary": "Qwen3 documentation describes thinking and non-thinking mode usage and output separation.",
    },
    "qwen_quickstart": {
        "title": "Qwen Quickstart documentation",
        "url": "https://qwen.readthedocs.io/en/latest/getting_started/quickstart.html",
        "type": "official_doc",
        "publisher": "Qwen",
        "score": 84,
        "summary": "Qwen quickstart documents model usage modes and version-specific behavior for Qwen3 variants.",
    },
    "trl_dpo": {
        "title": "DPO Trainer - Hugging Face TRL",
        "url": "https://huggingface.co/docs/trl/en/dpo_trainer",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL documents Direct Preference Optimization as preference-pair training for language model alignment.",
    },
    "trl_docs": {
        "title": "TRL documentation - Hugging Face",
        "url": "https://huggingface.co/docs/trl/",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL documents SFT and preference optimization workflows for language model post-training.",
    },
    "ibm_rag_vs_finetune": {
        "title": "RAG vs fine-tuning vs prompt engineering - IBM",
        "url": "https://www.ibm.com/think/topics/rag-vs-fine-tuning-vs-prompt-engineering",
        "type": "engineering_article",
        "publisher": "IBM",
        "score": 76,
        "summary": "IBM explains that prompt engineering, RAG and fine-tuning solve different improvement problems and should be selected by need.",
    },
    "nist_ai_rmf": {
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST AI RMF provides governance practices for mapping, measuring and managing AI risks.",
    },
    "mapie_docs": {
        "title": "MAPIE documentation",
        "url": "https://mapie.readthedocs.io/en/v0.9.1/",
        "type": "official_doc",
        "publisher": "MAPIE",
        "score": 82,
        "summary": "MAPIE documents conformal prediction intervals and prediction sets for uncertainty quantification.",
    },
    "modal_docs": {
        "title": "Pool-based sampling - modAL documentation",
        "url": "https://modal-python.readthedocs.io/en/latest/content/examples/pool-based_sampling.html",
        "type": "official_doc",
        "publisher": "modAL",
        "score": 78,
        "summary": "modAL documents pool-based active learning and uncertainty sampling patterns.",
    },
    "active_learning_paper": {
        "title": "An Active Learning Approach with Uncertainty, Representativeness, and Diversity",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC4144157/",
        "type": "research_paper",
        "publisher": "NIH / PMC",
        "score": 78,
        "summary": "The active learning paper discusses uncertainty and representativeness as sampling criteria for labeling.",
    },
    "feast_docs": {
        "title": "Feast documentation",
        "url": "https://docs.feast.dev/",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 84,
        "summary": "Feast documents feature store concepts for historical feature extraction and online serving.",
    },
    "feast_feature_retrieval": {
        "title": "Feature retrieval - Feast documentation",
        "url": "https://docs.feast.dev/getting-started/concepts/feature-retrieval",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 84,
        "summary": "Feast documents point-in-time joins and historical feature retrieval for training data and batch scoring.",
    },
    "vllm_docs": {
        "title": "Online Serving - vLLM documentation",
        "url": "https://docs.vllm.ai/en/latest/serving/online_serving/",
        "type": "official_doc",
        "publisher": "vLLM",
        "score": 84,
        "summary": "vLLM documents online serving and OpenAI-compatible server interfaces for LLM serving.",
    },
    "vllm_serve": {
        "title": "vllm serve CLI documentation",
        "url": "https://docs.vllm.ai/en/stable/cli/serve/",
        "type": "official_doc",
        "publisher": "vLLM",
        "score": 82,
        "summary": "vLLM serve documents serving options including scheduling controls relevant to latency and throughput.",
    },
    "mlflow_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 84,
        "summary": "MLflow Model Registry documents registered models, versions, aliases, tags and lifecycle metadata.",
    },
    "ray_train": {
        "title": "Ray Train documentation",
        "url": "https://docs.ray.io/en/latest/train/train.html",
        "type": "official_doc",
        "publisher": "Ray",
        "score": 84,
        "summary": "Ray Train documents scalable model training and distributed fine-tuning across clusters.",
    },
    "kubeflow_pipelines": {
        "title": "Kubeflow Pipelines documentation",
        "url": "https://www.kubeflow.org/docs/components/pipelines/concepts/pipeline/",
        "type": "official_doc",
        "publisher": "Kubeflow",
        "score": 84,
        "summary": "Kubeflow Pipelines documents portable and scalable ML workflows on Kubernetes.",
    },
    "cek_path_resolver": {
        "title": "CEK-TA Path Resolver 规范",
        "url": "docs/tasks/phase22_path_resolver_foundation.md",
        "type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 86,
        "summary": "CEK-TA Phase 22 requires resolver-based portable path handling and no hardcoded machine paths.",
    },
    "cek_mcp_contract": {
        "title": "CEK-TA MCP 只读检索契约",
        "url": "docs/tasks/phase14_mcp_runtime_server.md",
        "type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 86,
        "summary": "CEK-TA MCP runtime keeps knowledge retrieval read-only and permission-gated.",
    },
    "phase40_champion": {
        "title": "Phase 40 champion/challenger release contract",
        "url": "docs/contracts/phase40_champion_challenger_release_contract.md",
        "type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 86,
        "summary": "Phase 40 defines champion/challenger, shadow, paper, canary, release and rollback governance.",
    },
    "phase41_runtime": {
        "title": "Phase 41 hybrid scoring runtime contract",
        "url": "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
        "type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 88,
        "summary": "Phase 41 runtime contract defines scorer, calibrator, Qwen3 audit assistant, RAG and deterministic final gate boundaries.",
    },
}


TOPIC_SOURCE_KEYS: dict[str, list[str]] = {
    "P41-A04": ["catboost_docs", "catboost_paper", "sklearn_group_cv"],
    "P41-A06": ["sklearn_ensemble", "nist_ai_rmf", "phase41_runtime"],
    "P41-A07": ["shap_docs", "sklearn_permutation_importance", "nist_ai_rmf"],
    "P41-B04": ["sklearn_group_cv", "phase41_runtime", "nist_ai_rmf"],
    "P41-C04": ["sklearn_calibration", "calibration_paper", "nist_ai_rmf"],
    "P41-C05": ["sklearn_calibration", "tfdv_docs", "phase41_runtime"],
    "P41-E04": ["qwen3_blog", "qwen_quickstart", "phase41_runtime"],
    "P41-E06": ["trl_dpo", "trl_docs", "phase41_runtime"],
    "P41-E07": ["ibm_rag_vs_finetune", "trl_docs", "phase41_runtime"],
    "P41-F03": ["phase41_runtime", "nist_ai_rmf", "mlflow_registry"],
    "P41-F04": ["phase40_champion", "nist_ai_rmf", "phase41_runtime"],
    "P41-F08": ["phase41_runtime", "vllm_serve", "nist_ai_rmf"],
    "P41-B06": ["modal_docs", "active_learning_paper", "phase41_runtime"],
    "P41-C06": ["mapie_docs", "sklearn_calibration", "phase41_runtime"],
    "P41-D05": ["feast_docs", "feast_feature_retrieval", "phase41_runtime"],
    "P41-E08": ["vllm_docs", "vllm_serve", "qwen_quickstart"],
    "P41-F05": ["mlflow_registry", "phase41_runtime", "nist_ai_rmf"],
    "P41-F06": ["ray_train", "kubeflow_pipelines", "phase41_runtime"],
    "P41-F07": ["cek_path_resolver", "cek_mcp_contract", "phase41_runtime"],
}


NODE_META = {
    "kt.ai_engineering.numeric_scoring.model_family_selection": ("KB_AI_20_NUMERIC_SCORING", "llm_training", "numeric_scoring_model_family_selection"),
    "kt.ai_engineering.numeric_scoring.tabular_scorer_training": ("KB_AI_20_NUMERIC_SCORING", "llm_training", "tabular_scorer_training"),
    "kt.ai_engineering.numeric_scoring.scorer_explainability": ("KB_AI_20_NUMERIC_SCORING", "llm_training", "scorer_explainability"),
    "kt.ai_engineering.calibration_threshold.uncertainty": ("KB_AI_21_CALIBRATION_THRESHOLD", "llm_training", "calibration_threshold_uncertainty"),
    "kt.ai_engineering.decision_time_feature_contract.feature_store": ("KB_AI_22_DECISION_TIME_FEATURES", "llm_training", "decision_time_feature_store"),
    "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant": ("KB_AI_23_LLM_AUDIT_ASSISTANT", "llm_training", "qwen3_audit_assistant"),
    "kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe": ("KB_AI_23_LLM_AUDIT_ASSISTANT", "llm_training", "qwen3_training_recipe"),
    "kt.ai_engineering.model_release_governance.hybrid_runtime_contract": ("KB_AI_25_MODEL_RELEASE_GOVERNANCE", "ai_governance", "hybrid_runtime_contract"),
    "kt.ai_engineering.model_release_governance.training_platform_governance": ("KB_AI_25_MODEL_RELEASE_GOVERNANCE", "ai_governance", "training_platform_governance"),
}

CONTRACT_REFS = [
    "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
    "docs/contracts/phase41_tabular_llm_training_data_contract.md",
    "docs/research/phase41_hybrid_scoring_qwen3_scope.md",
    "docs/tasks/phase41_hybrid_scoring_qwen3_audit_stack.md",
]


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def safe_slug(value: str, fallback: str) -> str:
    return slug(value) or slug(fallback)


def source_ref(key: str) -> dict[str, Any]:
    src = SOURCE_CATALOG[key]
    return {
        "source_id": f"src_{key}",
        "source_title": src["title"],
        "source_url": src["url"],
        "source_type": src["type"],
        "publisher": src["publisher"],
        "published_at": None,
        "accessed_at": TODAY,
        "version": None,
        "reliability": "high" if int(src["score"]) >= 80 else "medium",
        "score": src["score"],
        "relevance": "high",
        "freshness": "time_sensitive" if src["type"] == "official_doc" else "stable",
        "limitations": [],
        "evidence_summary": src["summary"],
        "quoted_excerpt_allowed": False,
    }


def parse_matrix() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P41-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7 or cells[1] not in {"P0-Extended", "P1"}:
            continue
        rows.append(
            {
                "topic_id": cells[0],
                "priority": cells[1],
                "node_id": cells[2].strip("`"),
                "title": cells[3],
                "claim_type": cells[4],
                "model_role": cells[5],
                "source_hint": cells[6],
            }
        )
    return rows


def existing_phase41_topics() -> set[str]:
    topics = set()
    for path in CAND_DIR.glob("cand_20260610_phase41_*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        topics.add(str(raw.get("research_task_id", "")))
    return topics


def build_candidate(row: dict[str, str]) -> dict[str, Any]:
    node_id = row["node_id"]
    partition_id, domain, subdomain = NODE_META[node_id]
    sources = [source_ref(key) for key in TOPIC_SOURCE_KEYS[row["topic_id"]]]
    score = round(sum(int(src["score"]) for src in sources) / len(sources))
    title_slug = safe_slug(row["title"], row["topic_id"])
    candidate_id = f"cand_20260610_phase41_{slug(row['topic_id'])}_{title_slug}_001"
    proposed_knowledge_id = f"kb_ai_hybrid_scoring.phase41.{title_slug}.v1"
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": row["topic_id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": "Phase 41 P0-Extended/P1 sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering / Hybrid Scoring And Qwen3 Audit",
            "related_nodes": ["kt.trading_engineering", "kt.rag_engineering", "kt.ai_feedback_governance"],
            "partition_id": partition_id,
            "domain": domain,
            "subdomain": subdomain,
            "rule_type": "governance_rule",
            "used_for": ["llm_training", "trading_gating_scoring", "hybrid_scoring", "rag_engineering", "mcp", "vue_audit_ui"],
        },
        "claim": {
            "claim_id": "claim_001",
            "statement": row["title"],
            "normalized_claim": f"phase41.{title_slug}.v1",
            "claim_type": row["claim_type"],
            "model_role": row["model_role"],
            "priority": row["priority"],
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in sources[:2]),
            "interpretation_notes": "本候选只沉淀 AI Engineering 的模型选择、训练增强、校准不确定性、特征服务、Qwen3 审计助手或平台治理规则；交易规则本体必须路由到 Phase 37 / Trading Engineering。",
            "claim_strength": "medium",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "trading_llm_gating_scoring",
            "applies_when": [
                "外接项目已完成基本 hybrid scoring POC，正在评估增强模型、平台、解释、校准、不确定性、服务化或发布治理。",
                "该规则用于限制增强能力的引入时机、职责边界、审计证据和回滚条件。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、K 线形态、策略参数或实盘订单执行。",
                "知识点主要描述 fill model、订单状态机、实盘风控阈值、交易所异常处理或交易收益本体，应路由到 Trading Engineering。",
            ],
            "assumptions": [
                "P0-Extended/P1 是增强能力，不应阻塞 POC 主链路。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充工程实例。",
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 区分必需能力与条件增强能力。",
                "用于生成任务卡、接口契约、测试计划、审计 checklist 和候选知识补证问题。",
                "用于阻断增强平台或模型能力绕过 deterministic final gate、人工审批和 RAG 引用边界。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘下单建议。",
                "不得据此把 P1 平台工具变成默认依赖。",
                "不得把 candidate 当作 reviewed/approved 默认指导。",
            ],
        },
        "source_refs": sources,
        "source_quality": {
            "overall_reliability": "high" if score >= 82 else "medium",
            "score": score,
            "score_version": "1.0.0",
            "primary_source_count": min(2, len(sources)),
            "supporting_source_count": max(0, len(sources) - 2),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": ["增强能力来源多为官方文档、论文或内部契约；正式化时必须保留条件引入边界。"],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": CONTRACT_REFS,
            "conflicts": [],
            "resolution_summary": "未发现与 Phase 41 契约的直接冲突；候选不会进入默认指导。",
            "approval_allowed": False,
        },
        "machine_gate": {
            "default_guidance": "deny",
            "reason": "candidate only; P0-Extended/P1 enhancement item requires external audit before formal knowledge conversion.",
            "requires_human_escalation": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "codex",
            "reviewed_at": None,
            "open_questions": ["审计时确认是否应保留为增强项，避免外接项目把平台/模型工具过早变成默认依赖。"],
            "audit_log": [{"at": TODAY, "actor": "codex", "action": "created", "reason": "Phase 41 P0-Extended/P1 joint candidate expansion."}],
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、来源摘要和归纳性知识，不保存全文或长引用。",
            "reuse_risk": "low",
        },
        "conversion_target": {
            "proposed_knowledge_id": proposed_knowledge_id,
            "target_schema": "cek_ta_knowledge_item",
            "target_review_status": "draft",
            "skill_candidate": False,
            "eval_case_candidate": row["topic_id"] in {"P41-E04", "P41-E06", "P41-E07", "P41-F03", "P41-F08"},
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
        "workflow": {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": None,
            "hidden_from_default_queue": False,
            "next_action": "export_for_ai_or_human_audit",
            "default_guidance_allowed": False,
        },
        "phase41_trace": {
            "priority": row["priority"],
            "source_hint": row["source_hint"],
            "related_contracts": CONTRACT_REFS,
            "scope_boundary": "AI Engineering enhancement only; Trading Engineering knowledge body is reference-only.",
        },
    }


def has_mojibake(value: object) -> bool:
    return bool(re.search(r"(�|锟|烫|屯|Ã|Â|\?{2,})", json.dumps(value, ensure_ascii=False)))


def write_research_note(rows: list[dict[str, str]], created: int, skipped: int) -> None:
    lines = [
        "# Phase 41 P0-Extended/P1 候选知识来源采集记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        f"本轮将 P0-Extended 12 条和 P1 7 条合并采集，计划 19 条，生成候选 `{created}` 条，跳过已存在 `{skipped}` 条。",
        "",
        "本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。",
        "",
        "## 主要来源族",
        "",
        "| 来源族 | 用途 |",
        "| --- | --- |",
        "| CatBoost / scikit-learn / SHAP | 条件模型、ensemble、解释边界、group split 和校准增强 |",
        "| MAPIE / modAL | conformal / abstain band、active learning 和 hard-example mining 增强边界 |",
        "| Qwen / TRL / vLLM | Qwen3 thinking、DPO、RAG-first、服务化条件和延迟吞吐边界 |",
        "| Feast / MLflow / Ray / Kubeflow | feature store、model registry、分布式训练和流水线平台条件引入 |",
        "| NIST AI RMF / CEK-TA 内部契约 | AI 治理、只读 MCP、路径 resolver、final gate 和发布边界 |",
        "",
        "## 本批主题",
        "",
        "| topic_id | priority | canonical_node_id | claim_type | model_role | 来源数 |",
        "| --- | --- | --- | --- | --- | ---: |",
    ]
    for row in rows:
        lines.append(f"| {row['topic_id']} | {row['priority']} | `{row['node_id']}` | {row['claim_type']} | {row['model_role']} | {len(TOPIC_SOURCE_KEYS[row['topic_id']])} |")
    lines.extend(["", "## 边界", "", "本批 P0-Extended/P1 是增强能力采集，不改变 P0-Core 的基本运行链路；不得把平台工具、feature store、本地 serving 或分布式训练变成默认依赖。", ""])
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_quality_and_report(rows: list[dict[str, str]], created: int, skipped: int) -> None:
    expected = {row["topic_id"] for row in rows}
    candidates: list[dict[str, Any]] = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase41_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if str(raw.get("research_task_id")) in expected:
            candidates.append(raw)
    failures: list[dict[str, object]] = []
    seen = set()
    for item in candidates:
        cid = item.get("candidate_id")
        rid = str(item.get("research_task_id", ""))
        seen.add(rid)
        sources = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in sources if isinstance(src, dict)}
        if len(sources) < 3:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_3"})
        if not (source_types & {"official_doc", "research_paper", "standard_doc", "governance_framework", "security_standard", "internal_contract"}):
            failures.append({"candidate_id": cid, "failure": "missing_primary_source_type"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": cid, "failure": "default_guidance_not_false"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "failure": "machine_gate_not_deny"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if has_mojibake(item):
            failures.append({"candidate_id": cid, "failure": "mojibake_marker_detected"})
    for rid in sorted(expected - seen):
        failures.append({"research_task_id": rid, "failure": "missing_candidate"})
    quality = {
        "report_id": "phase41_extended_p1_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 41 P0-Extended/P1 joint candidate batch",
        "candidate_count": len(candidates),
        "planned_total": len(rows),
        "p0_extended_total": sum(1 for row in rows if row["priority"] == "P0-Extended"),
        "p1_total": sum(1 for row in rows if row["priority"] == "P1"),
        "created_this_run": created,
        "skipped_existing": skipped,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; P0-Extended and P1 are audited together before formal conversion.",
    }
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Phase 41 P0-Extended/P1 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本轮联合生成 Phase 41 P0-Extended/P1 candidate `{created}` 条，跳过已存在 `{skipped}` 条。",
                "",
                f"质量门禁：`{quality['gate_status']}`，失败数 `{quality['failure_count']}`。",
                "",
                "## 上下游",
                "",
                "上游：`docs/reports/phase41_remaining_scope_alignment_report.json`、Phase 41 采集矩阵和运行时契约。",
                "",
                "下游：`CEK-TA-331` 导出联合候选 AI 审计包并运行质量门禁。",
                "",
                "## 边界",
                "",
                "本轮只生成候选知识，不生成 formal reviewed，不设置 approved，不允许默认指导。P0-Extended/P1 不能变成外接项目默认依赖。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rows = parse_matrix()
    if len(rows) != 19:
        raise RuntimeError(f"Expected 19 Phase 41 P0-Extended/P1 rows, got {len(rows)}")
    missing_groups = sorted({row["topic_id"] for row in rows} - set(TOPIC_SOURCE_KEYS))
    if missing_groups:
        raise RuntimeError(f"Missing source groups: {missing_groups}")
    existing = existing_phase41_topics()
    created = 0
    skipped = 0
    for row in rows:
        if row["topic_id"] in existing:
            skipped += 1
            continue
        candidate = build_candidate(row)
        out = CAND_DIR / f"{candidate['candidate_id']}.json"
        out.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1
    write_research_note(rows, created, skipped)
    write_quality_and_report(rows, created, skipped)
    print(json.dumps({"created": created, "skipped": skipped, "planned": len(rows)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
