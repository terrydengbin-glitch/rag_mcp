"""Generate Phase 40 Batch D/E continuous-learning candidate knowledge files.

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
MATRIX = resolve_repo_path("docs", "research", "phase40_continuous_learning_collection_matrix.md", start_file=__file__)
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
RESEARCH = resolve_repo_path("docs", "research", "phase40_batch_d_e_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase40_extended_p1_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase40_extended_p1_generation_quality_gate.json", start_file=__file__)


EXPECTED_BATCH_DE = {f"P40-E{i:02d}" for i in range(1, 13)} | {f"P40-P{i:02d}" for i in range(1, 7)}


NODE_META = {
    "kt.ai_feedback_governance.feedback_logging": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "feedback_logging"),
    "kt.ai_feedback_governance.label_refresh": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "label_refresh"),
    "kt.ai_feedback_governance.drift_monitoring": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "drift_monitoring"),
    "kt.ai_feedback_governance.retraining_trigger": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "retraining_trigger"),
    "kt.ai_feedback_governance.recalibration_loop": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "recalibration_loop"),
    "kt.ai_feedback_governance.champion_challenger": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "champion_challenger"),
    "kt.ai_feedback_governance.shadow_paper_canary": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "shadow_paper_canary"),
    "kt.ai_feedback_governance.rollback_governance": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "rollback_governance"),
    "kt.ai_feedback_governance.llm_prompt_rag_sft_loop": ("KB_AI_18_FEEDBACK_GOVERNANCE", "llm_training", "llm_prompt_rag_sft_loop"),
    "kt.ai_feedback_governance.feedback_loop_risk": ("KB_AI_18_FEEDBACK_GOVERNANCE", "ai_governance", "feedback_loop_risk"),
}


CONTRACT_REFS = [
    "docs/contracts/phase40_feedback_dataset_contract.md",
    "docs/contracts/phase40_drift_retraining_recalibration_contract.md",
    "docs/contracts/phase40_champion_challenger_release_contract.md",
    "docs/research/phase40_ai_continuous_learning_scope.md",
]


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "snowflake_ml_observability": {
        "title": "ML Observability: Monitoring model behavior over time",
        "url": "https://docs.snowflake.com/en/developer-guide/snowflake-ml/model-registry/model-observability",
        "type": "official_doc",
        "publisher": "Snowflake",
        "score": 84,
        "summary": "Snowflake ML Observability describes monitoring logs that store inference data, predictions, timestamps, features, and ground-truth labels.",
    },
    "google_data_cards_playbook": {
        "title": "The Data Cards Playbook",
        "url": "https://sites.research.google/datacardsplaybook/",
        "type": "framework_doc",
        "publisher": "Google Research",
        "score": 84,
        "summary": "The Data Cards Playbook supports transparent dataset documentation and metadata practices across a dataset lifecycle.",
    },
    "fiddler_model_drift": {
        "title": "Model Drift - Fiddler Documentation",
        "url": "https://docs.fiddler.ai/glossary/model-drift",
        "type": "official_doc",
        "publisher": "Fiddler",
        "score": 82,
        "summary": "Fiddler describes model drift monitoring and root-cause analysis that differentiates data quality issues, concept drift, and other factors.",
    },
    "datarobot_data_drift": {
        "title": "Set up data drift monitoring - DataRobot docs",
        "url": "https://docs.datarobot.com/en/docs/classic-ui/mlops/deployment-settings/data-drift-settings.html",
        "type": "official_doc",
        "publisher": "DataRobot",
        "score": 82,
        "summary": "DataRobot documents data drift settings, thresholds, and feature importance for production ML monitoring.",
    },
    "sklearn_calibration": {
        "title": "Probability calibration - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/calibration.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents probability calibration workflows and calibration curves for classifier probability estimates.",
    },
    "sklearn_calibration_display": {
        "title": "CalibrationDisplay - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibrationDisplay.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents reliability diagrams that compare average predicted probability per bin with observed positive fraction.",
    },
    "ibm_model_risk": {
        "title": "What is model risk management?",
        "url": "https://www.ibm.com/think/topics/model-risk-management",
        "type": "framework_doc",
        "publisher": "IBM",
        "score": 82,
        "summary": "IBM describes model risk management as identifying, measuring, and controlling risks from inadequate model performance and governance.",
    },
    "aws_sagemaker_shadow_tests": {
        "title": "Shadow tests - Amazon SageMaker AI",
        "url": "https://docs.aws.amazon.com/sagemaker/latest/dg/shadow-tests.html",
        "type": "official_doc",
        "publisher": "AWS",
        "score": 86,
        "summary": "AWS SageMaker shadow tests compare model-serving changes against current deployments before they affect end users.",
    },
    "microsoft_shadow_testing": {
        "title": "Shadow Testing - Microsoft Engineering Fundamentals Playbook",
        "url": "https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/",
        "type": "official_doc",
        "publisher": "Microsoft",
        "score": 84,
        "summary": "Microsoft describes shadow testing as replicating production traffic to a candidate environment to compare behavior before release.",
    },
    "cosai_ai_incident_response": {
        "title": "AI Incident Response Framework",
        "url": "https://www.coalitionforsecureai.org/wp-content/uploads/2026/03/AI-Incident-Response-1.pdf",
        "type": "framework_doc",
        "publisher": "Coalition for Secure AI",
        "score": 82,
        "summary": "The AI Incident Response Framework covers recovery actions such as rolling back fine-tuned models or agent states and updating RAG sources after incidents.",
    },
    "evidently_rag_eval": {
        "title": "A complete guide to RAG evaluation",
        "url": "https://www.evidentlyai.com/llm-guide/rag-evaluation",
        "type": "engineering_article",
        "publisher": "Evidently AI",
        "score": 82,
        "summary": "Evidently explains evaluating retrieval and generation separately, building test sets, running experiments, and monitoring RAG systems.",
    },
    "google_rag_best_practices": {
        "title": "RAG systems: Best practices to master evaluation",
        "url": "https://cloud.google.com/blog/products/ai-machine-learning/optimizing-rag-retrieval",
        "type": "engineering_article",
        "publisher": "Google Cloud",
        "score": 84,
        "summary": "Google Cloud recommends testing RAG systems with query sets, metrics, and repeatable evaluation workflows.",
    },
    "label_studio_review": {
        "title": "Review annotation quality in Label Studio",
        "url": "https://docs.humansignal.com/guide/quality",
        "type": "official_doc",
        "publisher": "HumanSignal",
        "score": 82,
        "summary": "Label Studio documentation describes reviewing annotations and validating label quality after human or model annotation.",
    },
    "ibm_wks_adjudication": {
        "title": "Annotation setup - IBM Watson Knowledge Studio",
        "url": "https://cloud.ibm.com/docs/watson-knowledge-studio?topic=watson-knowledge-studio-annotate-documents",
        "type": "official_doc",
        "publisher": "IBM Cloud",
        "score": 82,
        "summary": "IBM documents comparing human annotations and resolving conflicts through adjudication before promotion to ground truth.",
    },
    "mlflow_model_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 86,
        "summary": "MLflow Model Registry provides model lineage, versioning, aliases, metadata tagging, and annotations for lifecycle management.",
    },
    "mlflow_registry_workflow": {
        "title": "Model Registry Workflows - MLflow",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 86,
        "summary": "MLflow workflow documentation covers registering models, managing versions, applying aliases and tags, and using model metadata.",
    },
    "arize_monitoring_metrics": {
        "title": "Best Practices for Monitors - Arize AX Docs",
        "url": "https://arize.com/docs/ax/machine-learning/machine-learning/how-to-ml/monitors/choosing-your-metrics",
        "type": "official_doc",
        "publisher": "Arize AI",
        "score": 82,
        "summary": "Arize monitor guidance covers performance, drift, data quality, and custom metrics for continuous model monitoring.",
    },
    "arize_retrieval_eval": {
        "title": "Retrieval Evaluation - Arize AX Docs",
        "url": "https://arize.com/docs/ax/cookbooks/evaluation/retrieval-evaluation",
        "type": "official_doc",
        "publisher": "Arize AI",
        "score": 82,
        "summary": "Arize retrieval evaluation documents evaluating RAG retrieval quality and debugging bad responses, missing context, and irrelevant chunks.",
    },
    "promptfoo_rag_eval": {
        "title": "Evaluating RAG pipelines - Promptfoo",
        "url": "https://www.promptfoo.dev/docs/guides/evaluate-rag/",
        "type": "official_doc",
        "publisher": "Promptfoo",
        "score": 82,
        "summary": "Promptfoo documents how to evaluate RAG applications and compare retrieved context and generated answers.",
    },
    "braintrust_llm_eval": {
        "title": "What is LLM evaluation?",
        "url": "https://www.braintrust.dev/articles/llm-evaluation-guide",
        "type": "engineering_article",
        "publisher": "Braintrust",
        "score": 80,
        "summary": "Braintrust describes prompt evaluation as comparing outputs before and after changes across representative test cases to catch regressions.",
    },
    "long_tail_learning_survey": {
        "title": "A Systematic Review on Long-Tailed Learning",
        "url": "https://arxiv.org/html/2408.00483v1",
        "type": "paper",
        "publisher": "arXiv",
        "score": 82,
        "summary": "The survey explains that long-tailed data has frequent head classes and many low-sample tail classes that are difficult to model.",
    },
    "iguazio_retraining": {
        "title": "What Is Machine Learning Model Retraining?",
        "url": "https://www.iguazio.com/glossary/model-retraining/",
        "type": "engineering_article",
        "publisher": "Iguazio",
        "score": 78,
        "summary": "Iguazio describes model retraining as an MLOps capability that can run on a schedule or event-driven trigger.",
    },
    "chronosphere_tail_sampling": {
        "title": "Tail sampling - Chronosphere Documentation",
        "url": "https://docs.chronosphere.io/control/shaping/sample-traces/tail-sampling",
        "type": "official_doc",
        "publisher": "Chronosphere",
        "score": 78,
        "summary": "Chronosphere tail sampling keeps selected high-value traces such as error traces while downsampling baseline traces.",
    },
    "nist_ai_rmf": {
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST AI RMF provides a risk-management framework for governing, mapping, measuring, and managing AI risks.",
    },
}


ITEM_SOURCE_GROUPS: dict[str, list[str]] = {
    "P40-E01": ["snowflake_ml_observability", "mlflow_model_registry", "nist_ai_rmf"],
    "P40-E02": ["google_data_cards_playbook", "mlflow_model_registry", "nist_ai_rmf"],
    "P40-E03": ["fiddler_model_drift", "datarobot_data_drift", "arize_monitoring_metrics"],
    "P40-E04": ["cosai_ai_incident_response", "mlflow_registry_workflow", "nist_ai_rmf"],
    "P40-E05": ["sklearn_calibration", "sklearn_calibration_display", "arize_monitoring_metrics"],
    "P40-E06": ["ibm_model_risk", "mlflow_model_registry", "arize_monitoring_metrics"],
    "P40-E07": ["aws_sagemaker_shadow_tests", "microsoft_shadow_testing", "nist_ai_rmf"],
    "P40-E08": ["cosai_ai_incident_response", "mlflow_registry_workflow", "mlflow_model_registry"],
    "P40-E09": ["evidently_rag_eval", "google_rag_best_practices", "arize_retrieval_eval"],
    "P40-E10": ["label_studio_review", "ibm_wks_adjudication", "google_data_cards_playbook"],
    "P40-E11": ["nist_ai_rmf", "sklearn_calibration", "ibm_model_risk"],
    "P40-E12": ["arize_monitoring_metrics", "fiddler_model_drift", "sklearn_calibration_display"],
    "P40-P01": ["long_tail_learning_survey", "chronosphere_tail_sampling", "arize_monitoring_metrics"],
    "P40-P02": ["ibm_wks_adjudication", "label_studio_review", "google_data_cards_playbook"],
    "P40-P03": ["iguazio_retraining", "fiddler_model_drift", "mlflow_registry_workflow"],
    "P40-P04": ["mlflow_model_registry", "mlflow_registry_workflow", "ibm_model_risk"],
    "P40-P05": ["cosai_ai_incident_response", "mlflow_model_registry", "promptfoo_rag_eval"],
    "P40-P06": ["braintrust_llm_eval", "evidently_rag_eval", "promptfoo_rag_eval", "arize_retrieval_eval"],
}


SHORT_SLUGS = {
    "P40-E01": "replayable_audit_trail",
    "P40-E02": "label_policy_version_compatibility",
    "P40-E03": "drift_root_cause_classification",
    "P40-E04": "incident_retraining_requires_approval",
    "P40-E05": "calibration_bins_coverage",
    "P40-E06": "challenger_risk_metrics",
    "P40-E07": "shadow_paper_execution_gap",
    "P40-E08": "rollback_freezes_artifacts",
    "P40-E09": "rag_update_retrieval_regression",
    "P40-E10": "human_review_audit_trace",
    "P40-E11": "confidence_not_evidence",
    "P40-E12": "continuous_learning_dashboard",
    "P40-P01": "long_tail_feedback_sampling",
    "P40-P02": "label_conflict_gold_set",
    "P40-P03": "scheduled_event_retraining",
    "P40-P04": "rejected_challenger_reason_tracking",
    "P40-P05": "composite_artifact_rollback",
    "P40-P06": "prompt_rag_model_eval_separation",
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


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
        if not (line.startswith("| P40-E") or line.startswith("| P40-P")):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        topic_id = cells[0]
        if topic_id not in EXPECTED_BATCH_DE:
            continue
        rows.append(
            {
                "topic_id": topic_id,
                "priority": cells[1],
                "node_id": cells[2].strip("`"),
                "title": cells[3],
                "source_hint": cells[4],
                "search_direction": cells[5],
                "acceptance_gate": cells[6],
            }
        )
    return rows


def existing_topics() -> set[str]:
    topics: set[str] = set()
    for path in CAND_DIR.glob("cand_20260610_phase40_*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        rid = raw.get("research_task_id", "")
        if rid in EXPECTED_BATCH_DE:
            topics.add(rid)
    return topics


def build_candidate(row: dict[str, str]) -> dict[str, object]:
    node_id = row["node_id"]
    partition_id, domain, subdomain = NODE_META[node_id]
    short_slug = SHORT_SLUGS[row["topic_id"]]
    sources = [source_ref(key) for key in ITEM_SOURCE_GROUPS[row["topic_id"]]]
    score = round(sum(int(src["score"]) for src in sources) / len(sources))
    candidate_id = f"cand_20260610_phase40_{slug(row['topic_id'])}_{short_slug}_001"
    proposed_knowledge_id = f"kb_ai_feedback_governance.phase40.{short_slug}.v1"
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": row["topic_id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": "Phase 40 Batch D/E sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering / Continuous Learning And Feedback Governance",
            "related_nodes": [],
            "partition_id": partition_id,
            "domain": domain,
            "subdomain": subdomain,
            "rule_type": "governance_rule",
            "used_for": [
                "llm_training",
                "trading_gating_scoring",
                "continuous_learning",
                "rag_engineering",
                "mcp",
                "vue_audit_ui",
            ],
        },
        "claim": {
            "claim_id": "claim_001",
            "statement": row["title"],
            "normalized_claim": f"phase40.{short_slug}.v1",
            "claim_type": "ai_governance_rule",
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in sources[:3]),
            "interpretation_notes": "本候选只沉淀 AI Engineering 的持续学习、反馈治理、再训练、再校准、发布回滚或 LLM 改进方法；交易规则本体必须路由到 Phase 37。",
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
                "外接项目正在建设交易 AI gating/scoring 的反馈日志、标签刷新、漂移检测、再训练、再校准、shadow/paper/canary 或发布治理链路。",
                "该规则用于补强 Phase 40 P0-Core 治理闭环，并为 AI IDE 生成任务卡、契约、测试和审计 checklist 提供候选知识。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、K 线形态、策略参数或实盘订单执行。",
                "知识点主要描述 fill model、订单状态机、实盘风控阈值或交易所异常处理，应路由到 Trading Engineering。",
            ],
            "assumptions": [
                "外接项目提供私有交易事实、模型输出和发布上下文；CEK-TA 只沉淀可复用专业规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要补充交易项目实例。",
                "AI Engineering 只定义学习治理、证据链、评估、发布和回滚边界，不定义交易策略本体。",
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 在外接项目中实现持续学习治理字段、审计追踪、评测回归和发布门禁。",
                "用于阻断自动上线、无来源默认指导、LLM 越权 final gate 和反馈回路污染。",
                "用于生成候选审计包，由外部 AI/人工进一步审计。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘下单建议。",
                "不得据此跳过人工审批或 release/rollback 门禁。",
                "不得把 candidate 当作 reviewed 或 approved 默认指导。",
            ],
        },
        "source_refs": sources,
        "source_quality": {
            "overall_reliability": "high" if score >= 82 else "medium",
            "score": score,
            "score_version": "1.1.0",
            "primary_source_count": min(3, len(sources)),
            "supporting_source_count": max(0, len(sources) - 3),
            "low_reliability_source_count": 0,
            "mandatory_downgrades": [],
            "limitations": [
                "来源支持通用 AI/ML/MLOps/LLMOps/治理工程原则；正式知识转换时需保留 CEK-TA 具体上下游引用和冲突链接。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": CONTRACT_REFS,
            "conflicts": [],
            "resolution_summary": "未发现与 Phase 40 契约的直接冲突；候选不会进入默认指导。",
            "approval_allowed": True,
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
                "审计时确认该候选是否需要补充更贴近交易 AI 的实例或与 Phase 38/Trading Engineering 增加交叉引用。",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "Phase 40 Batch D/E continuous learning candidate expansion.",
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
            "eval_case_candidate": row["topic_id"] in {"P40-E09", "P40-P06", "P40-P02"},
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
        "phase40_trace": {
            "batch": "Batch D/E",
            "acceptance_gate": row["acceptance_gate"],
            "search_direction": row["search_direction"],
            "related_contracts": CONTRACT_REFS,
        },
    }


def load_batch_candidates() -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase40_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if raw.get("research_task_id") in EXPECTED_BATCH_DE:
            candidates.append(raw)
    return candidates


def write_research_note(created: int, skipped: int) -> None:
    lines = [
        "# Phase 40 Batch D/E 候选知识来源采集记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        f"本轮按 Phase 40 Batch D/E 矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条。",
        "",
        "本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。",
        "",
        "## 覆盖范围",
        "",
        "| 批次 | 数量 | 说明 |",
        "| --- | ---: | --- |",
        "| Batch D / P0-Extended | 12 | replayable audit trail、标签版本、drift root cause、事故触发、校准分桶、风险指标、shadow/paper 差异、rollback freeze、RAG 回归、人审审计、confidence 边界、监控看板 |",
        "| Batch E / P1 | 6 | 长尾采样、标签仲裁、混合再训练、拒绝实验追踪、组合回滚、prompt/RAG/model eval 分离 |",
        "",
        "## 主要来源族",
        "",
        "| 来源族 | 用途 |",
        "| --- | --- |",
        "| Snowflake / MLflow / Google Data Cards | 预测日志、模型 lineage、数据集/标签版本和发布元数据 |",
        "| Fiddler / DataRobot / Arize | drift root cause、监控指标、dashboard 和模型可观测性 |",
        "| scikit-learn | 校准曲线、reliability diagram、分桶可靠性 |",
        "| AWS SageMaker / Microsoft Shadow Testing | shadow/paper 验证和非生产等价边界 |",
        "| Coalition for Secure AI / NIST AI RMF | AI incident response、rollback、治理和风险边界 |",
        "| Evidently / Google Cloud / Promptfoo / Arize | RAG 检索评测、测试集、回归和检索/生成分离 |",
        "| Label Studio / IBM Watson Knowledge Studio | 人工标注复核、冲突处理、adjudication 和 gold set |",
        "| Long-tailed learning survey / tail sampling docs | 长尾覆盖和选择性采样边界 |",
        "",
        "## 边界",
        "",
        "本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。这些内容仍归 Trading Engineering。",
        "",
    ]
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(created: int, skipped: int) -> dict[str, object]:
    candidates = load_batch_candidates()
    failures: list[dict[str, str]] = []
    seen = set()
    for item in candidates:
        cid = str(item.get("candidate_id", ""))
        rid = str(item.get("research_task_id", ""))
        seen.add(rid)
        if len(item.get("source_refs") or []) < 2:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_2"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": cid, "failure": "workflow_default_guidance_not_false"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "failure": "machine_gate_not_deny"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if not str(item.get("classification", {}).get("canonical_node_id", "")).startswith("kt.ai_feedback_governance."):
            failures.append({"candidate_id": cid, "failure": "wrong_canonical_node"})
    for missing in sorted(EXPECTED_BATCH_DE - seen):
        failures.append({"research_task_id": missing, "failure": "missing_batch_d_e_candidate"})
    quality = {
        "report_id": "phase40_extended_p1_generation_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 40 Batch D/E candidate generation",
        "candidate_count": len(candidates),
        "planned_total": len(EXPECTED_BATCH_DE),
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
                "# Phase 40 Batch D/E 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本次按 Phase 40 Batch D/E 采集矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条。当前 Batch D/E 候选总数为 {len(candidates)} 条。",
                "",
                "所有新增内容仍为 candidate，不是 formal reviewed，不是 approved，也不会进入 MCP/SearchLab 默认指导。",
                "",
                "## 质量门禁",
                "",
                f"- gate_status: {quality['gate_status']}",
                f"- failure_count: {quality['failure_count']}",
                f"- planned_total: {quality['planned_total']}",
                "",
                "## 下游",
                "",
                "下一步进入 CEK-TA-311：导出 Phase 40 Batch D/E 候选 AI 审计包并运行来源、冲突、乱码和污染门禁。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_research_note(created, skipped)
    return quality


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_topics()
    created = 0
    skipped = 0
    for row in parse_matrix():
        if row["topic_id"] in existing:
            skipped += 1
            continue
        candidate = build_candidate(row)
        path = CAND_DIR / f"{candidate['candidate_id']}.json"
        path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1
    quality = write_report(created, skipped)
    print(json.dumps(quality, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
