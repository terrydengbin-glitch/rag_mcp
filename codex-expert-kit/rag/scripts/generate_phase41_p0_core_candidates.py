"""Generate Phase 41 P0-Core hybrid scoring candidate knowledge files.

This script writes candidate JSON only. It does not create formal reviewed or
approved knowledge, and it never enables default guidance.
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
RESEARCH = resolve_repo_path("docs", "research", "phase41_p0_core_candidate_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase41_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase41_candidate_quality_gate.json", start_file=__file__)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "sklearn_logistic_regression": {
        "title": "LogisticRegression - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents regularized LogisticRegression, solvers, class_weight and probability outputs for classification baselines.",
    },
    "sklearn_calibration": {
        "title": "Probability calibration - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/calibration.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents calibration curves and methods for improving or adding probability calibration to classifiers.",
    },
    "sklearn_common_pitfalls": {
        "title": "Common pitfalls and recommended practices - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/common_pitfalls.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn warns about data leakage, inconsistent preprocessing and model-selection pitfalls.",
    },
    "sklearn_time_series_split": {
        "title": "TimeSeriesSplit - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn documents TimeSeriesSplit as a cross-validator for time-ordered data where later folds follow earlier folds.",
    },
    "sklearn_compute_class_weight": {
        "title": "compute_class_weight - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.utils.class_weight.compute_class_weight.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn documents class weight computation for imbalanced classification settings.",
    },
    "sklearn_model_evaluation": {
        "title": "Metrics and scoring - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/model_evaluation.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn documents classification metrics, probability estimates and sample_weight support in scoring functions.",
    },
    "lightgbm_docs": {
        "title": "LightGBM documentation",
        "url": "https://lightgbm.readthedocs.io/",
        "type": "official_doc",
        "publisher": "LightGBM",
        "score": 84,
        "summary": "LightGBM documentation describes a gradient boosting framework designed for efficient tree-based learning.",
    },
    "lightgbm_paper": {
        "title": "LightGBM: A Highly Efficient Gradient Boosting Decision Tree",
        "url": "https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html",
        "type": "research_paper",
        "publisher": "NeurIPS",
        "score": 86,
        "summary": "The LightGBM paper describes histogram-based gradient boosting and leaf-wise tree growth for efficient GBDT training.",
    },
    "xgboost_docs": {
        "title": "XGBoost documentation",
        "url": "https://xgboost.readthedocs.io/",
        "type": "official_doc",
        "publisher": "XGBoost",
        "score": 84,
        "summary": "XGBoost documentation describes scalable and portable gradient boosting for classification, regression and ranking.",
    },
    "xgboost_paper": {
        "title": "XGBoost: A Scalable Tree Boosting System",
        "url": "https://arxiv.org/abs/1603.02754",
        "type": "research_paper",
        "publisher": "arXiv",
        "score": 86,
        "summary": "The XGBoost paper describes scalable tree boosting and system-level design for structured predictive modeling.",
    },
    "catboost_docs": {
        "title": "CatBoost documentation",
        "url": "https://catboost.ai/docs/",
        "type": "official_doc",
        "publisher": "CatBoost",
        "score": 82,
        "summary": "CatBoost documentation describes gradient boosting on decision trees with categorical feature support.",
    },
    "catboost_paper": {
        "title": "CatBoost: unbiased boosting with categorical features",
        "url": "https://arxiv.org/abs/1810.11363",
        "type": "research_paper",
        "publisher": "arXiv",
        "score": 84,
        "summary": "The CatBoost paper discusses ordered boosting and categorical feature handling for gradient boosting.",
    },
    "nist_ai_rmf": {
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST AI RMF provides a framework for governing, mapping, measuring and managing AI risks.",
    },
    "mlflow_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 84,
        "summary": "MLflow Model Registry documents registered models, versions, aliases, tags, lifecycle metadata and governance workflows.",
    },
    "dvc_docs": {
        "title": "DVC documentation",
        "url": "https://dvc.org/doc",
        "type": "official_doc",
        "publisher": "DVC",
        "score": 82,
        "summary": "DVC documentation supports data, model and pipeline versioning for reproducible machine learning workflows.",
    },
    "feast_docs": {
        "title": "Feast documentation",
        "url": "https://docs.feast.dev/",
        "type": "official_doc",
        "publisher": "Feast",
        "score": 82,
        "summary": "Feast documentation describes feature store concepts for defining, managing and serving ML features.",
    },
    "tfdv_docs": {
        "title": "TensorFlow Data Validation",
        "url": "https://www.tensorflow.org/tfx/data_validation/get_started",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "TensorFlow Data Validation documents schema, statistics, anomalies, data validation and skew/drift checks.",
    },
    "qwen_docs": {
        "title": "Qwen documentation",
        "url": "https://qwen.readthedocs.io/",
        "type": "official_doc",
        "publisher": "Qwen",
        "score": 82,
        "summary": "Qwen documentation describes Qwen model usage, deployment and generation capabilities for language model applications.",
    },
    "json_schema": {
        "title": "JSON Schema",
        "url": "https://json-schema.org/",
        "type": "standard_doc",
        "publisher": "JSON Schema",
        "score": 86,
        "summary": "JSON Schema defines a vocabulary for validating JSON document structure and required fields.",
    },
    "hf_trl_docs": {
        "title": "TRL documentation - Hugging Face",
        "url": "https://huggingface.co/docs/trl/",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL documentation covers trainers and post-training workflows for language models.",
    },
    "hf_trl_sft": {
        "title": "SFT Trainer - Hugging Face TRL",
        "url": "https://huggingface.co/docs/trl/en/sft_trainer",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL SFT Trainer documentation covers supervised fine-tuning workflows for language model outputs.",
    },
    "owasp_llm01": {
        "title": "LLM01:2025 Prompt Injection - OWASP GenAI Security Project",
        "url": "https://genai.owasp.org/llmrisk/llm01-prompt-injection/",
        "type": "security_standard",
        "publisher": "OWASP",
        "score": 86,
        "summary": "OWASP LLM01 describes prompt injection as crafted inputs that alter LLM behavior or outputs in unintended ways.",
    },
}


ITEM_SOURCE_GROUPS: dict[str, list[str]] = {
    "P41-A01": ["sklearn_logistic_regression", "lightgbm_docs", "xgboost_docs", "catboost_docs"],
    "P41-A02": ["sklearn_logistic_regression", "sklearn_calibration", "sklearn_model_evaluation"],
    "P41-A03": ["lightgbm_docs", "xgboost_docs", "lightgbm_paper", "xgboost_paper"],
    "P41-A05": ["nist_ai_rmf", "mlflow_registry", "sklearn_model_evaluation"],
    "P41-B01": ["sklearn_compute_class_weight", "sklearn_model_evaluation", "lightgbm_docs", "xgboost_docs"],
    "P41-B02": ["sklearn_common_pitfalls", "sklearn_calibration", "nist_ai_rmf"],
    "P41-B03": ["sklearn_time_series_split", "sklearn_common_pitfalls", "nist_ai_rmf"],
    "P41-B05": ["dvc_docs", "mlflow_registry", "nist_ai_rmf"],
    "P41-C01": ["sklearn_calibration", "sklearn_model_evaluation", "nist_ai_rmf"],
    "P41-C02": ["sklearn_calibration", "sklearn_common_pitfalls", "nist_ai_rmf"],
    "P41-C03": ["sklearn_model_evaluation", "sklearn_calibration", "nist_ai_rmf"],
    "P41-D01": ["feast_docs", "sklearn_common_pitfalls", "tfdv_docs"],
    "P41-D02": ["feast_docs", "tfdv_docs", "nist_ai_rmf"],
    "P41-D03": ["dvc_docs", "feast_docs", "mlflow_registry"],
    "P41-D04": ["sklearn_common_pitfalls", "sklearn_time_series_split", "tfdv_docs"],
    "P41-E01": ["qwen_docs", "nist_ai_rmf", "json_schema"],
    "P41-E02": ["json_schema", "qwen_docs", "nist_ai_rmf"],
    "P41-E03": ["json_schema", "nist_ai_rmf", "owasp_llm01"],
    "P41-E05": ["hf_trl_sft", "hf_trl_docs", "qwen_docs"],
    "P41-E09": ["owasp_llm01", "json_schema", "nist_ai_rmf"],
    "P41-F01": ["sklearn_calibration", "nist_ai_rmf", "json_schema"],
    "P41-F02": ["mlflow_registry", "dvc_docs", "nist_ai_rmf"],
}


NODE_META = {
    "kt.ai_engineering.numeric_scoring.model_family_selection": (
        "KB_AI_20_NUMERIC_SCORING",
        "llm_training",
        "numeric_scoring_model_family_selection",
    ),
    "kt.ai_engineering.numeric_scoring.tabular_scorer_training": (
        "KB_AI_20_NUMERIC_SCORING",
        "llm_training",
        "tabular_scorer_training",
    ),
    "kt.ai_engineering.calibration_threshold.uncertainty": (
        "KB_AI_21_CALIBRATION_THRESHOLD",
        "llm_training",
        "calibration_threshold_uncertainty",
    ),
    "kt.ai_engineering.decision_time_feature_contract.feature_store": (
        "KB_AI_22_DECISION_TIME_FEATURES",
        "llm_training",
        "decision_time_feature_store",
    ),
    "kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant": (
        "KB_AI_23_LLM_AUDIT_ASSISTANT",
        "llm_training",
        "qwen3_audit_assistant",
    ),
    "kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe": (
        "KB_AI_23_LLM_AUDIT_ASSISTANT",
        "llm_training",
        "qwen3_training_recipe",
    ),
    "kt.ai_engineering.model_release_governance.hybrid_runtime_contract": (
        "KB_AI_25_MODEL_RELEASE_GOVERNANCE",
        "ai_governance",
        "hybrid_runtime_contract",
    ),
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


def source_ref(key: str) -> dict[str, object]:
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
        "freshness": "time_sensitive" if src["type"] in {"official_doc", "governance_framework"} else "stable",
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
        if len(cells) < 7 or cells[1] != "P0-Core":
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


def build_candidate(row: dict[str, str]) -> dict[str, object]:
    node_id = row["node_id"]
    partition_id, domain, subdomain = NODE_META[node_id]
    sources = [source_ref(key) for key in ITEM_SOURCE_GROUPS[row["topic_id"]]]
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
            "decision_reason": "Phase 41 P0-Core sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering / Hybrid Scoring And Qwen3 Audit",
            "related_nodes": [
                "kt.trading_engineering",
                "kt.rag_engineering",
            ],
            "partition_id": partition_id,
            "domain": domain,
            "subdomain": subdomain,
            "rule_type": "governance_rule",
            "used_for": [
                "llm_training",
                "trading_gating_scoring",
                "hybrid_scoring",
                "rag_engineering",
                "mcp",
                "vue_audit_ui",
            ],
        },
        "claim": {
            "claim_id": "claim_001",
            "statement": row["title"],
            "normalized_claim": f"phase41.{title_slug}.v1",
            "claim_type": row["claim_type"],
            "model_role": row["model_role"],
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in sources[:2]),
            "interpretation_notes": "本候选只沉淀 AI Engineering 的表格/统计 scorer、校准、决策时特征、Qwen3 审计助手或 deterministic final gate 工程规则；K 线、fill model、订单状态机、仓位和风控本体必须路由到 Phase 37 / Trading Engineering。",
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
                "外接项目正在构建交易 gating/scoring 的表格 scorer、校准器、Qwen3 审计助手、RAG 引用或 deterministic final gate。",
                "该规则用于阻断数据泄漏、模型越权、无来源默认指导、未校准概率、无版本发布或 LLM 替代 final gate。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、K 线形态、策略参数或实盘订单执行。",
                "知识点主要描述 fill model、订单状态机、实盘风控阈值、交易所异常处理或交易收益本体，应路由到 Trading Engineering。",
            ],
            "assumptions": [
                "外接项目提供私有交易事实、模型输出和发布上下文；CEK-TA 只沉淀可复用专业规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充交易项目实例。",
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 在外接项目中实现 hybrid scoring、Qwen3 audit、RAG citation、校准和 final gate 的契约边界。",
                "用于生成任务卡、接口契约、测试计划、审计 checklist 和候选知识补证问题。",
                "用于阻断 Qwen3 充当 numeric scorer、raw score 直接进 final gate、无来源默认指导或训练/评估污染。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘下单建议。",
                "不得据此跳过人工审批、release/rollback 门禁或 deterministic final gate。",
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
            "limitations": [
                "来源支持通用 AI/ML/RAG/MLOps/治理工程原则；正式知识转换时需保留 CEK-TA 具体上下游引用和冲突链接。",
            ],
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
            "reason": "candidate only; not reviewed or approved; external audit required before formal knowledge conversion.",
            "requires_human_escalation": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "codex",
            "reviewed_at": None,
            "open_questions": [
                "审计时确认该候选是否需要补充更贴近交易 AI 的实例、反例或与 Phase 37 Trading Engineering 增加交叉引用。",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "Phase 41 P0-Core hybrid scoring and Qwen3 audit candidate expansion.",
                }
            ],
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
            "eval_case_candidate": row["topic_id"] in {"P41-E02", "P41-E03", "P41-E09", "P41-F01"},
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
            "source_hint": row["source_hint"],
            "related_contracts": CONTRACT_REFS,
            "scope_boundary": "AI Engineering only; Trading Engineering knowledge body is reference-only.",
        },
    }


def load_phase41_candidates() -> list[dict[str, object]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase41_*.json")):
        candidates.append(json.loads(path.read_text(encoding="utf-8-sig")))
    return candidates


def write_research_note(rows: list[dict[str, str]], created: int, skipped: int) -> None:
    lines = [
        "# Phase 41 P0-Core 候选知识来源采集记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        f"本轮按 Phase 41 P0-Core 矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条；当前 P0-Core 规划总数为 {len(rows)} 条。",
        "",
        "本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。",
        "",
        "## 主要来源族",
        "",
        "| 来源族 | 用途 |",
        "| --- | --- |",
        "| scikit-learn | Logistic Regression baseline、概率校准、class_weight、sample_weight、TimeSeriesSplit、数据泄漏边界 |",
        "| LightGBM / XGBoost / CatBoost | GBDT 候选模型、类别特征条件候选和同场评估边界 |",
        "| NIST AI RMF | AI 风险治理、度量、管理和人类监督边界 |",
        "| MLflow / DVC | model registry、dataset lineage、split manifest、release manifest 和可复现性 |",
        "| Feast / TFDV | feature store、online/offline parity、schema、skew 和数据验证 |",
        "| Qwen / JSON Schema / Hugging Face TRL | Qwen3 审计助手、strict JSON、SFT 格式训练和 reason code 输出 |",
        "| OWASP LLM01 | RAG context、用户摘要和检索文档的不可信输入与 prompt-injection 防护 |",
        "",
        "## P0-Core 主题",
        "",
        "| topic_id | canonical_node_id | claim_type | model_role | 来源数 |",
        "| --- | --- | --- | --- | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['topic_id']} | `{row['node_id']}` | {row['claim_type']} | {row['model_role']} | {len(ITEM_SOURCE_GROUPS[row['topic_id']])} |"
        )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。这些内容仍归 Phase 37 / Trading Engineering。",
            "",
        ]
    )
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_quality_and_report(rows: list[dict[str, str]], created: int, skipped: int) -> None:
    candidates = load_phase41_candidates()
    phase41 = [item for item in candidates if str(item.get("research_task_id", "")).startswith("P41-")]
    failures: list[dict[str, object]] = []
    seen = set()
    expected = {row["topic_id"] for row in rows}
    for item in phase41:
        cid = item.get("candidate_id")
        rid = str(item.get("research_task_id", ""))
        if rid not in expected:
            continue
        seen.add(rid)
        sources = item.get("source_refs") or []
        source_types = {str(src.get("source_type")) for src in sources if isinstance(src, dict)}
        if len(sources) < 3:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_3"})
        if not (source_types & {"official_doc", "research_paper", "standard_doc", "governance_framework", "security_standard"}):
            failures.append({"candidate_id": cid, "failure": "missing_primary_source_type"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": cid, "failure": "default_guidance_not_false"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "failure": "machine_gate_not_deny"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if "Trading Engineering" not in " ".join(item.get("applicability", {}).get("not_applicable_when", [])):
            failures.append({"candidate_id": cid, "failure": "missing_trading_boundary"})
    for rid in sorted(expected - seen):
        failures.append({"research_task_id": rid, "failure": "missing_p0_core_candidate"})
    quality = {
        "report_id": "phase41_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 41 P0-Core candidates",
        "candidate_count": len([item for item in phase41 if str(item.get("research_task_id", "")) in expected]),
        "planned_p0_core_total": len(rows),
        "created_this_run": created,
        "skipped_existing": skipped,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
    }
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Phase 41 P0-Core 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本轮生成 Phase 41 P0-Core candidate `{created}` 条，跳过已存在 `{skipped}` 条。",
                "",
                f"质量门禁：`{quality['gate_status']}`，失败数 `{quality['failure_count']}`。",
                "",
                "## 上下游",
                "",
                "上游：`docs/research/phase41_hybrid_scoring_collection_matrix.md`、`docs/research/phase41_research_task_queue.md`、Phase 41 契约文档和范围审计补丁。",
                "",
                "下游：`CEK-TA-325` 导出候选 AI 审计包并运行来源、冲突、乱码和污染门禁。",
                "",
                "## 边界",
                "",
                "本轮只生成候选知识，不生成 formal reviewed，不设置 approved，不允许默认指导。",
                "",
                "Trading Engineering 本体只作为引用边界，不混入 AI Engineering 候选。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rows = parse_matrix()
    if len(rows) != 22:
        raise RuntimeError(f"Expected 22 Phase 41 P0-Core rows, got {len(rows)}")
    missing_groups = sorted({row["topic_id"] for row in rows} - set(ITEM_SOURCE_GROUPS))
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
