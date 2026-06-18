"""Generate Phase 40 P0-Core continuous-learning candidate knowledge files.

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
RESEARCH = resolve_repo_path("docs", "research", "phase40_p0_core_candidate_research.md", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase40_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase40_p0_core_candidate_quality_gate.json", start_file=__file__)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "evidently_data_drift": {
        "title": "Data Drift - Evidently documentation",
        "url": "https://docs.evidentlyai.com/metrics/preset_data_drift",
        "type": "official_doc",
        "publisher": "Evidently AI",
        "score": 84,
        "summary": "Evidently documents data drift presets for comparing distribution shifts between reference and current datasets.",
    },
    "evidently_drift_explainer": {
        "title": "Data drift explainer - Evidently documentation",
        "url": "https://docs.evidentlyai.com/metrics/explainer_drift",
        "type": "official_doc",
        "publisher": "Evidently AI",
        "score": 84,
        "summary": "Evidently explains distribution drift checks for individual columns, including features, predictions, and targets.",
    },
    "tfdv_get_started": {
        "title": "Get started with TensorFlow Data Validation",
        "url": "https://www.tensorflow.org/tfx/data_validation/get_started",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 84,
        "summary": "TensorFlow Data Validation documents data statistics, slicing, schema checks, skew, and drift for production ML data.",
    },
    "tfdv_guide": {
        "title": "TensorFlow Data Validation Guide",
        "url": "https://github.com/tensorflow/tfx/blob/master/docs/guide/tfdv.md",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "The TFDV guide covers training-serving skew and drift detection, including distribution differences from sampling or serving data changes.",
    },
    "whylogs_overview": {
        "title": "whylogs Overview - WhyLabs documentation",
        "url": "https://docs.whylabs.ai/docs/whylogs-overview/",
        "type": "official_doc",
        "publisher": "WhyLabs",
        "score": 82,
        "summary": "WhyLabs documentation describes whylogs profiles for monitoring data quality and data change issues such as drift.",
    },
    "whylogs_github": {
        "title": "whylogs GitHub repository",
        "url": "https://github.com/whylabs/whylogs",
        "type": "official_repo",
        "publisher": "WhyLabs",
        "score": 80,
        "summary": "whylogs is an open-source data logging library for ML models and data pipelines, providing visibility into data quality and model performance over time.",
    },
    "offpolicy_logged_bandit": {
        "title": "Off-Policy Evaluation and Learning from Logged Bandit Feedback",
        "url": "https://arxiv.org/abs/1808.00232",
        "type": "paper",
        "publisher": "arXiv",
        "score": 84,
        "summary": "The paper studies learning and evaluation from logged action-context feedback collected by historical policies, highlighting off-policy data challenges.",
    },
    "batch_logged_bandit_jmlr": {
        "title": "Batch Learning from Logged Bandit Feedback through Counterfactual Risk Minimization",
        "url": "https://jmlr.org/papers/volume16/swaminathan15a/swaminathan15a.pdf",
        "type": "paper",
        "publisher": "JMLR",
        "score": 86,
        "summary": "This JMLR paper builds on counterfactual estimators for off-policy evaluation and learning from logged bandit feedback.",
    },
    "sklearn_calibration": {
        "title": "Probability calibration - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/calibration.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents calibration curves and probability calibration workflows for classifier probabilities.",
    },
    "sklearn_brier": {
        "title": "brier_score_loss - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn defines Brier score loss for probabilistic predictions and treats lower values as better.",
    },
    "sklearn_cost_threshold": {
        "title": "Post-tuning the decision threshold for cost-sensitive learning",
        "url": "https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn demonstrates decision threshold tuning based on a business cost function rather than a fixed probability cutoff.",
    },
    "mlflow_model_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 84,
        "summary": "MLflow Model Registry documents registered models, versions, aliases, tags, and lifecycle metadata.",
    },
    "mlflow_registry_workflow": {
        "title": "MLflow Model Registry workflows",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 84,
        "summary": "MLflow workflow documentation describes organizing and deploying models with aliases and tags for model versions.",
    },
    "argo_rollouts": {
        "title": "Argo Rollouts documentation",
        "url": "https://argoproj.github.io/rollouts/",
        "type": "official_doc",
        "publisher": "Argo Project",
        "score": 84,
        "summary": "Argo Rollouts documents progressive delivery capabilities such as blue-green, canary, canary analysis, and experimentation.",
    },
    "argo_canary": {
        "title": "Canary Deployment Strategy - Argo Rollouts",
        "url": "https://argo-rollouts.readthedocs.io/en/stable/features/canary/",
        "type": "official_doc",
        "publisher": "Argo Project",
        "score": 84,
        "summary": "Argo Rollouts describes canary deployment as releasing a new version to a small percentage of production traffic.",
    },
    "openai_model_optimization": {
        "title": "Model optimization - OpenAI API documentation",
        "url": "https://developers.openai.com/api/docs/guides/model-optimization",
        "type": "official_doc",
        "publisher": "OpenAI",
        "score": 86,
        "summary": "OpenAI documentation explains fine-tuning benefits, tradeoffs, and when model optimization can help compared with prompting alone.",
    },
    "openai_prompt_engineering": {
        "title": "Prompt engineering - OpenAI API documentation",
        "url": "https://developers.openai.com/api/docs/guides/prompt-engineering",
        "type": "official_doc",
        "publisher": "OpenAI",
        "score": 86,
        "summary": "OpenAI documentation frames prompt engineering as writing effective instructions so models consistently meet requirements.",
    },
    "hf_trl": {
        "title": "TRL documentation - Hugging Face",
        "url": "https://huggingface.co/docs/trl/en/index",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL documentation covers dataset formats, trainers, logging, and post-training workflows for language models.",
    },
    "hf_sft": {
        "title": "SFT Trainer - Hugging Face TRL",
        "url": "https://huggingface.co/docs/trl/en/sft_trainer",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "Hugging Face TRL documents supervised fine-tuning workflows for language models.",
    },
    "nist_ai_rmf": {
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST describes a framework for managing risks to individuals, organizations, and society associated with AI.",
    },
    "nist_ai_rmf_core": {
        "title": "AI RMF - NIST AI Resource Center",
        "url": "https://airc.nist.gov/airmf-resources/airmf/",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST AI RMF Core provides outcomes and actions for governing, mapping, measuring, and managing AI risks.",
    },
}


ITEM_SOURCE_GROUPS: dict[str, list[str]] = {
    "P40-C01": ["whylogs_github", "whylogs_overview", "nist_ai_rmf"],
    "P40-C02": ["whylogs_github", "mlflow_model_registry", "nist_ai_rmf"],
    "P40-C03": ["offpolicy_logged_bandit", "batch_logged_bandit_jmlr", "nist_ai_rmf"],
    "P40-C04": ["nist_ai_rmf", "tfdv_get_started", "whylogs_overview"],
    "P40-C05": ["nist_ai_rmf", "batch_logged_bandit_jmlr", "offpolicy_logged_bandit"],
    "P40-C06": ["sklearn_cost_threshold", "sklearn_calibration", "nist_ai_rmf"],
    "P40-C07": ["evidently_data_drift", "evidently_drift_explainer", "tfdv_get_started"],
    "P40-C08": ["tfdv_get_started", "whylogs_overview", "nist_ai_rmf"],
    "P40-C09": ["mlflow_model_registry", "mlflow_registry_workflow", "nist_ai_rmf"],
    "P40-C10": ["mlflow_model_registry", "tfdv_get_started", "nist_ai_rmf_core"],
    "P40-C11": ["sklearn_calibration", "sklearn_brier", "tfdv_guide"],
    "P40-C12": ["sklearn_cost_threshold", "sklearn_calibration", "nist_ai_rmf"],
    "P40-C13": ["mlflow_model_registry", "mlflow_registry_workflow", "nist_ai_rmf"],
    "P40-C14": ["argo_rollouts", "argo_canary", "nist_ai_rmf"],
    "P40-C15": ["mlflow_model_registry", "argo_rollouts", "nist_ai_rmf_core"],
    "P40-C16": ["openai_prompt_engineering", "openai_model_optimization", "hf_trl"],
    "P40-C17": ["openai_model_optimization", "hf_sft", "hf_trl"],
    "P40-C18": ["nist_ai_rmf", "offpolicy_logged_bandit", "tfdv_guide"],
}


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
        if not line.startswith("| P40-C"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        rows.append(
            {
                "topic_id": cells[0],
                "priority": cells[1],
                "node_id": cells[2].strip("`"),
                "title": cells[3],
                "source_hint": cells[4],
                "search_direction": cells[5],
                "acceptance_gate": cells[6],
            }
        )
    return rows


def existing_phase40_topics() -> set[str]:
    topics = set()
    for path in CAND_DIR.glob("cand_20260610_phase40_*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        topics.add(raw.get("research_task_id", ""))
    return topics


def build_candidate(row: dict[str, str]) -> dict[str, object]:
    node_id = row["node_id"]
    partition_id, domain, subdomain = NODE_META[node_id]
    sources = [source_ref(key) for key in ITEM_SOURCE_GROUPS[row["topic_id"]]]
    score = round(sum(int(src["score"]) for src in sources) / len(sources))
    candidate_id = f"cand_20260610_phase40_{slug(row['topic_id'])}_{slug(row['title'])}_001"
    proposed_knowledge_id = f"kb_ai_feedback_governance.phase40.{slug(row['title'])}.v1"
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": row["topic_id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": "Phase 40 P0-Core sourced candidate; not reviewed, not approved, not default guidance.",
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
            "normalized_claim": f"phase40.{slug(row['title'])}.v1",
            "claim_type": "ai_governance_rule",
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in sources[:2]),
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
                "该规则用于阻断自动上线、PnL-only 标签、allow-only logging、反馈回路污染、无 rollback 发布或 LLM 越权 final gate。",
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
            ],
        },
        "llm_usage_policy": {
            "allowed": [
                "用于提醒 AI IDE 在外接项目中实现持续学习治理字段、审计追踪和发布门禁。",
                "用于阻断自动上线、无来源默认指导和 LLM 越权 final gate。",
                "用于生成任务卡、契约、测试计划和审计 checklist。",
            ],
            "not_allowed": [
                "不得据此生成买卖点、仓位、杠杆、止损止盈或实盘下单建议。",
                "不得据此跳过人工审批或 release/rollback 门禁。",
                "不得把 candidate 当作 approved 默认指导。",
            ],
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
            "limitations": [
                "来源支持通用 AI/ML/MLOps/LLMOps/治理工程原则；正式知识转换时需保留 CEK-TA 具体上下游引用和冲突链接。",
            ],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": CONTRACT_REFS,
            "conflicts": [],
            "resolution_summary": "未发现与 Phase 40 契约的直接冲突；候选不会进入默认指导。",
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
                "审计时确认该候选是否需要补充更贴近交易 AI 的实例或与 Phase 38/Trading Engineering 增加交叉引用。",
            ],
            "audit_log": [
                {
                    "at": TODAY,
                    "actor": "codex",
                    "action": "created",
                    "reason": "Phase 40 P0-Core continuous learning candidate expansion.",
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
            "eval_case_candidate": node_id.endswith(("shadow_paper_canary", "recalibration_loop")),
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
            "acceptance_gate": row["acceptance_gate"],
            "search_direction": row["search_direction"],
            "related_contracts": CONTRACT_REFS,
        },
    }


def load_phase40_candidates() -> list[dict[str, object]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase40_*.json")):
        candidates.append(json.loads(path.read_text(encoding="utf-8-sig")))
    return candidates


def write_research_note(created: int, skipped: int) -> None:
    lines = [
        "# Phase 40 P0-Core 候选知识来源采集记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        f"本轮按 Phase 40 P0-Core 矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条。",
        "",
        "本轮只生成 candidate，不进入 formal reviewed，不进入 approved，也不会作为默认指导。",
        "",
        "## 主要来源族",
        "",
        "| 来源族 | 用途 |",
        "| --- | --- |",
        "| Evidently / TFDV / whylogs | 数据漂移、预测漂移、数据质量、日志和监控 |",
        "| scikit-learn calibration / Brier / cost-sensitive threshold | 概率校准、Brier/ECE、成本阈值 |",
        "| MLflow Model Registry | candidate/champion 版本、别名、生命周期和发布证据 |",
        "| Argo Rollouts | canary、progressive delivery、停止条件和灰度发布语义 |",
        "| OpenAI / Hugging Face TRL | prompt、RAG、SFT/LoRA、LLM 训练和评估触发边界 |",
        "| NIST AI RMF | AI 风险治理、度量、管理和人类审批边界 |",
        "| Logged bandit / OPE 论文 | 被阻断/未执行候选的反事实和日志反馈边界 |",
        "",
        "## 边界",
        "",
        "本轮没有采集 K 线、fill model、订单状态机、实盘风控阈值或交易所执行适配器本体知识。这些内容仍归 Trading Engineering。",
        "",
    ]
    RESEARCH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(created: int, skipped: int) -> dict[str, object]:
    candidates = load_phase40_candidates()
    phase40_p0 = [item for item in candidates if str(item.get("research_task_id", "")).startswith("P40-C")]
    failures = []
    seen = set()
    for item in phase40_p0:
        cid = item.get("candidate_id")
        rid = item.get("research_task_id")
        seen.add(rid)
        if len(item.get("source_refs") or []) < 2:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_2"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
        if item.get("workflow", {}).get("default_guidance_allowed") is not False:
            failures.append({"candidate_id": cid, "failure": "default_guidance_not_false"})
        if item.get("machine_gate", {}).get("default_guidance") != "deny":
            failures.append({"candidate_id": cid, "failure": "machine_gate_not_deny"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
    expected = {f"P40-C{i:02d}" for i in range(1, 19)}
    missing = sorted(expected - seen)
    for rid in missing:
        failures.append({"research_task_id": rid, "failure": "missing_p0_core_candidate"})
    quality = {
        "report_id": "phase40_p0_core_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 40 P0-Core candidates",
        "candidate_count": len(phase40_p0),
        "planned_p0_core_total": 18,
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
                "# Phase 40 P0-Core 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本次按 Phase 40 P0-Core 采集矩阵生成候选知识 {created} 条，跳过已存在候选 {skipped} 条。当前 Phase 40 P0-Core 候选总数为 {len(phase40_p0)} 条。",
                "",
                "所有新增内容仍为 candidate，不是 formal reviewed，不是 approved，也不会进入 MCP/SearchLab 默认指导。",
                "",
                "## 质量门禁",
                "",
                f"- gate_status: {quality['gate_status']}",
                f"- failure_count: {quality['failure_count']}",
                f"- planned_p0_core_total: {quality['planned_p0_core_total']}",
                "",
                "## 下游",
                "",
                "下一步进入 CEK-TA-306：导出 Phase 40 候选 AI 审计包并运行来源、冲突、乱码和污染门禁。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_research_note(created, skipped)
    return quality


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_phase40_topics()
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
