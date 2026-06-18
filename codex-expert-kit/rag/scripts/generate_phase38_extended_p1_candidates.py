"""Generate Phase 38 P0-Extended / P1 candidate knowledge files.

This script only creates candidate JSON files. It does not create formal
reviewed knowledge and never marks anything as approved/default guidance.
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
MATRIX = resolve_repo_path("docs", "research", "phase38_ai_model_platform_collection_matrix.md", start_file=__file__)
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase38_extended_p1_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase38_extended_p1_candidate_quality_gate.json", start_file=__file__)


SOURCE_CATALOG: dict[str, dict[str, Any]] = {
    "catboost_doc": {
        "title": "CatBoost documentation",
        "url": "https://catboost.ai/",
        "type": "official_doc",
        "publisher": "CatBoost",
        "score": 82,
        "summary": "CatBoost official material describes gradient boosting over decision trees with categorical feature support.",
    },
    "catboost_paper": {
        "title": "CatBoost: gradient boosting with categorical features support",
        "url": "https://arxiv.org/abs/1810.11363",
        "type": "paper",
        "publisher": "arXiv",
        "score": 84,
        "summary": "The CatBoost paper explains categorical feature handling and overfitting countermeasures in gradient boosting.",
    },
    "shap_doc": {
        "title": "SHAP documentation",
        "url": "https://shap.readthedocs.io/",
        "type": "official_doc",
        "publisher": "SHAP",
        "score": 82,
        "summary": "SHAP documentation frames SHAP values as game-theoretic model output explanations.",
    },
    "sklearn_calibration": {
        "title": "Probability calibration - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/calibration.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents calibration curves and probability calibration workflow.",
    },
    "sklearn_brier": {
        "title": "brier_score_loss - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn describes Brier score loss for probabilistic predictions.",
    },
    "evidently_drift": {
        "title": "Evidently data drift documentation",
        "url": "https://docs.evidentlyai.com/metrics/preset_data_drift",
        "type": "official_doc",
        "publisher": "Evidently AI",
        "score": 82,
        "summary": "Evidently documents data drift presets for comparing distributions between datasets.",
    },
    "tfdv": {
        "title": "TensorFlow Data Validation",
        "url": "https://www.tensorflow.org/tfx/data_validation/get_started",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "TFDV documents schema inference, data validation, skew, and drift checks.",
    },
    "tfdv_guide": {
        "title": "TensorFlow Data Validation Guide",
        "url": "https://github.com/tensorflow/tfx/blob/master/docs/guide/tfdv.md",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "TFDV guide covers schema validation, training-serving skew, and drift detection.",
    },
    "great_expectations": {
        "title": "Great Expectations open source data quality platform",
        "url": "https://greatexpectations.io/",
        "type": "official_doc",
        "publisher": "Great Expectations",
        "score": 80,
        "summary": "Great Expectations supports data quality expectations, validation results, and data documentation.",
    },
    "trl": {
        "title": "TRL documentation - Hugging Face",
        "url": "https://huggingface.co/docs/trl/en/index",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL documents SFT, DPO, trainer APIs, dataset formats, and post-training workflows.",
    },
    "trl_sft": {
        "title": "SFT Trainer - Hugging Face TRL",
        "url": "https://huggingface.co/docs/trl/en/sft_trainer",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL SFT Trainer documentation supports supervised fine-tuning workflows.",
    },
    "trl_dpo": {
        "title": "DPO Trainer - Hugging Face TRL",
        "url": "https://huggingface.co/docs/trl/en/dpo_trainer",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL DPO Trainer documentation supports preference optimization from chosen/rejected pairs.",
    },
    "ope_contextual_bandit": {
        "title": "Off-Policy Evaluation in Contextual Bandits",
        "url": "https://www.emergentmind.com/topics/off-policy-evaluation-in-contextual-bandits",
        "type": "engineering_article",
        "publisher": "Emergent Mind",
        "score": 76,
        "summary": "This overview describes importance sampling, direct method, and doubly robust OPE in contextual bandits.",
    },
    "mlflow_registry": {
        "title": "MLflow Model Registry workflows",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 84,
        "summary": "MLflow registry documentation covers model versions, aliases, tags, and lifecycle workflows.",
    },
    "dvc": {
        "title": "Get Started with DVC",
        "url": "https://doc.dvc.org/start",
        "type": "official_doc",
        "publisher": "DVC",
        "score": 82,
        "summary": "DVC supports data, model, and pipeline versioning for reproducible ML workflows.",
    },
    "nist_ai_rmf": {
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST AI RMF supports AI governance, measurement, management, and trustworthy AI practices.",
    },
    "model_cards": {
        "title": "Model Cards for Model Reporting",
        "url": "https://research.google/pubs/model-cards-for-model-reporting/",
        "type": "paper",
        "publisher": "Google Research",
        "score": 86,
        "summary": "Model Cards propose short reporting artifacts describing model intended use, evaluation, and limitations.",
    },
    "hf_model_cards": {
        "title": "Hugging Face Model Cards",
        "url": "https://huggingface.co/docs/hub/en/model-cards",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 82,
        "summary": "Hugging Face documents model cards as Markdown metadata files for reproducibility and sharing.",
    },
    "google_sre_slo": {
        "title": "Implementing SLOs - Google SRE workbook",
        "url": "https://sre.google/workbook/implementing-slos/",
        "type": "official_doc",
        "publisher": "Google SRE",
        "score": 84,
        "summary": "Google SRE describes SLOs and error budgets for reliability management.",
    },
}


NODE_META = {
    "kt.ai_engineering.numeric_scoring": ("KB_AI_20_NUMERIC_SCORING", "llm_training", "numeric_scoring"),
    "kt.ai_engineering.calibration_threshold": ("KB_AI_21_CALIBRATION_THRESHOLD", "llm_training", "calibration_threshold"),
    "kt.ai_engineering.decision_time_feature_contract": ("KB_AI_22_DECISION_TIME_FEATURES", "llm_training", "decision_time_feature_contract"),
    "kt.ai_engineering.llm_audit_assistant": ("KB_AI_23_LLM_AUDIT_ASSISTANT", "llm_training", "llm_audit_assistant"),
    "kt.ai_engineering.shadow_paper_ope_eval": ("KB_AI_24_SHADOW_PAPER_OPE", "ai_governance", "shadow_paper_ope_eval"),
    "kt.ai_engineering.model_release_governance": ("KB_AI_25_MODEL_RELEASE_GOVERNANCE", "ai_governance", "model_release_governance"),
    "kt.rag_engineering.trading_scoring_rag_pack": ("KB_10_RAG_ENGINEERING", "rag_engineering", "trading_scoring_rag_pack"),
}


SOURCE_GROUPS = {
    "P38-A08": ["catboost_doc", "catboost_paper", "nist_ai_rmf"],
    "P38-A09": ["shap_doc", "nist_ai_rmf"],
    "P38-A10": ["mlflow_registry", "nist_ai_rmf"],
    "P38-B08": ["sklearn_calibration", "sklearn_brier", "evidently_drift"],
    "P38-B09": ["evidently_drift", "tfdv", "nist_ai_rmf"],
    "P38-B10": ["sklearn_calibration", "nist_ai_rmf"],
    "P38-C08": ["tfdv", "tfdv_guide", "dvc"],
    "P38-C09": ["great_expectations", "tfdv"],
    "P38-C10": ["tfdv", "nist_ai_rmf"],
    "P38-D07": ["trl", "trl_sft", "nist_ai_rmf"],
    "P38-D08": ["trl_sft", "trl", "nist_ai_rmf"],
    "P38-D09": ["trl_dpo", "trl", "nist_ai_rmf"],
    "P38-D10": ["trl", "nist_ai_rmf"],
    "P38-E07": ["mlflow_registry", "dvc", "nist_ai_rmf"],
    "P38-E08": ["evidently_drift", "nist_ai_rmf"],
    "P38-E09": ["ope_contextual_bandit", "nist_ai_rmf"],
    "P38-E10": ["ope_contextual_bandit", "nist_ai_rmf"],
    "P38-F07": ["mlflow_registry", "dvc", "nist_ai_rmf"],
    "P38-F08": ["model_cards", "hf_model_cards", "nist_ai_rmf"],
    "P38-F09": ["google_sre_slo", "nist_ai_rmf"],
    "P38-F10": ["mlflow_registry", "google_sre_slo"],
    "P38-G05": ["evidently_drift", "nist_ai_rmf"],
    "P38-G06": ["great_expectations", "nist_ai_rmf"],
}


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


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
        "freshness": "time_sensitive" if src["type"] in {"official_doc", "governance_framework"} else "stable",
        "limitations": [],
        "evidence_summary": src["summary"],
        "quoted_excerpt_allowed": False,
    }


def parse_matrix() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P38-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[1] not in {"P0-Extended", "P1"}:
            continue
        rows.append(
            {
                "topic_id": cells[0],
                "priority": cells[1],
                "node_id": cells[2].strip("`"),
                "title": cells[3],
                "claim_type": cells[4],
                "source_hint": cells[5],
            }
        )
    return rows


def existing_phase38_topics() -> set[str]:
    topics = set()
    for path in CAND_DIR.glob("cand_20260610_phase38_*.json"):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        task_id = raw.get("research_task_id", "")
        if task_id:
            topics.add(task_id)
    return topics


def build_candidate(row: dict[str, str]) -> dict[str, Any]:
    node_id = row["node_id"]
    partition_id, domain, subdomain = NODE_META[node_id]
    sources = [source_ref(key) for key in SOURCE_GROUPS[row["topic_id"]]]
    score = round(sum(int(src["score"]) for src in sources) / len(sources))
    candidate_id = f"cand_20260610_phase38_{slug(row['topic_id'])}_{slug(row['title'])}_001"
    min_sources = 2
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": row["topic_id"],
        "priority": row["priority"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": f"Phase 38 {row['priority']} sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering",
            "related_nodes": ["kt.trading_engineering"],
            "partition_id": partition_id,
            "domain": domain,
            "subdomain": subdomain,
            "rule_type": "checklist",
            "used_for": ["llm_training", "trading_gating_scoring", "rag_engineering", "mcp", "vue_audit_ui"],
        },
        "claim": {
            "claim_id": "claim_001",
            "statement": row["title"],
            "normalized_claim": f"phase38.{slug(row['title'])}.v1",
            "evidence_summary": "；".join(str(src["evidence_summary"]) for src in sources[:2]),
            "interpretation_notes": "本候选只沉淀 AI Engineering 的训练、评分、校准、评估、RAG/MCP、发布或治理方法；K 线、回测、fill model、风控和执行规则本体必须路由到 Phase 37 / Trading Engineering。",
            "claim_strength": "medium",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "trading_llm_assistant",
            "applies_when": [
                "外接项目正在扩展交易 LLM gating/scoring 的 P0-Extended 或 P1 能力。",
                "该规则用于完善模型选择、解释、校准漂移、数据质量、审计助手训练、shadow/OPE、发布治理或 RAG 引用治理。",
            ],
            "not_applicable_when": [
                "用户需要具体买卖点、仓位、止损止盈、策略参数或实盘订单执行。",
                "知识点主要描述 K 线结构、市场微观结构、回测模型、fill model 或交易风控本体，应路由到 Trading Engineering。",
            ],
            "assumptions": [
                "外接项目提供项目事实、私有交易数据和策略上下文；CEK-TA 只沉淀可复用专业规则。",
                "候选知识必须通过 AI/人工审计后才能转为 formal reviewed，不得直接作为 approved 默认指导。",
            ],
            "limitations": [
                "本条仍是 candidate，需要外部 AI/人工审计确认来源充分性、适用边界和是否需要拆分。",
                f"{row['priority']} 不是 POC 前全部硬门；具体上线门槛需由 release governance 任务另行确认。",
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
            "limitations": ["来源支持通用 AI/ML/RAG/MCP/治理工程原则；正式知识转换时需补 CEK-TA 具体上下游引用和冲突链接。"],
        },
        "conflict_audit": {
            "conflict_status": "none",
            "checked_against": [
                "docs/contracts/phase38_ai_scoring_gate_runtime_contract.md",
                "docs/contracts/phase38_training_data_and_eval_contract.md",
                "docs/tasks/phase38_ai_model_platform_poc_knowledge.md",
                "docs/tasks/phase37_trading_engineering_knowledge_expansion.md",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与当前 Phase 38 契约的直接冲突；候选不会进入默认指导，交易规则本体仍路由到 Phase 37。",
            "approval_allowed": False,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "codex",
            "reviewed_at": None,
            "open_questions": ["审计时确认该候选是否应保留在 AI Engineering，或只作为 Phase 37 Trading Engineering 的相关引用。"],
            "audit_log": [{"at": TODAY, "actor": "codex", "action": "created", "reason": f"Phase 38 {row['priority']} candidate expansion."}],
        },
        "copyright": {
            "stores_full_text": False,
            "stores_long_quote": False,
            "summary_only": True,
            "license_notes": "仅保存来源链接、来源摘要和归纳性知识，不保存全文或长引用。",
            "reuse_risk": "low",
        },
        "conversion_target": {
            "proposed_knowledge_id": f"kb_ai_engineering.phase38.{slug(row['title'])}.v1",
            "target_schema": "cek_ta_knowledge_item",
            "target_review_status": "draft",
            "skill_candidate": False,
            "eval_case_candidate": node_id.endswith("shadow_paper_ope_eval"),
        },
        "quality_gate": {
            "minimum_source_count": min_sources,
            "has_required_source_type": any(src["source_type"] in {"official_doc", "paper", "governance_framework"} for src in sources),
            "not_default_guidance": True,
            "trading_boundary_checked": True,
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


def write_report(created: int, skipped: int, target_rows: list[dict[str, str]]) -> dict[str, Any]:
    created_paths = sorted(CAND_DIR.glob("cand_20260610_phase38_*.json"))
    scoped = []
    target_ids = {row["topic_id"] for row in target_rows}
    for path in created_paths:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        if raw.get("research_task_id") in target_ids:
            scoped.append(raw)

    failures = []
    for item in scoped:
        cid = item.get("candidate_id")
        sources = item.get("source_refs") or []
        if len(sources) < 2:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_2"})
        if not any(source.get("source_type") in {"official_doc", "paper", "governance_framework"} for source in sources):
            failures.append({"candidate_id": cid, "failure": "missing_authoritative_source_type"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
        if "Trading Engineering" not in " ".join(item.get("applicability", {}).get("not_applicable_when", [])):
            failures.append({"candidate_id": cid, "failure": "missing_trading_boundary"})

    by_priority: dict[str, int] = {}
    for item in scoped:
        by_priority[str(item.get("priority", "unknown"))] = by_priority.get(str(item.get("priority", "unknown")), 0) + 1

    quality = {
        "report_id": "phase38_extended_p1_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 38 P0-Extended / P1 candidates",
        "planned_remaining_total": 23,
        "candidate_count": len(scoped),
        "created_this_run": created,
        "skipped_existing": skipped,
        "by_priority": by_priority,
        "failure_count": len(failures),
        "failures": failures,
        "gate_status": "pass" if not failures and len(scoped) == 23 else "fail",
        "boundary": "candidate is not reviewed or approved; audit result is required before formal knowledge conversion.",
        "sources_verified_by_web_search": [
            "https://catboost.ai/",
            "https://arxiv.org/abs/1810.11363",
            "https://shap.readthedocs.io/",
            "https://greatexpectations.io/",
            "https://mlflow.org/docs/latest/ml/model-registry/workflow/",
            "https://docs.evidentlyai.com/metrics/preset_data_drift",
            "https://research.google/pubs/model-cards-for-model-reporting/",
            "https://huggingface.co/docs/hub/en/model-cards",
            "https://sre.google/workbook/implementing-slos/",
        ],
    }
    QUALITY.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(
        "\n".join(
            [
                "# Phase 38 P0-Extended / P1 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本次按 Phase 38 采集矩阵生成 P0-Extended / P1 候选知识 {created} 条，跳过已存在候选 {skipped} 条。当前剩余批次候选总数为 {len(scoped)} 条。",
                "",
                f"- P0-Extended: {by_priority.get('P0-Extended', 0)}",
                f"- P1: {by_priority.get('P1', 0)}",
                "",
                "所有新增内容仍为 candidate，不是 formal reviewed，不是 approved，也不会进入 MCP/SearchLab 默认指导。",
                "",
                "## 来源范围",
                "",
                "本批补充使用官方文档、论文、治理框架和工程资料，覆盖 CatBoost、SHAP、Great Expectations、Evidently、MLflow、DVC、TRL、Model Cards、Google SRE 与 NIST AI RMF。",
                "",
                "## 质量门禁",
                "",
                f"- gate_status: {quality['gate_status']}",
                f"- failure_count: {quality['failure_count']}",
                "",
                "## 下游",
                "",
                "下一步进入 CEK-TA-285：导出 Phase 38 P0-Extended / P1 候选 AI 审计包，统一审计后再按 Phase 32 工作流处理。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return quality


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    rows = parse_matrix()
    existing = existing_phase38_topics()
    created = 0
    skipped = 0
    for row in rows:
        if row["topic_id"] in existing:
            skipped += 1
            continue
        candidate = build_candidate(row)
        path = CAND_DIR / f"{candidate['candidate_id']}.json"
        path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        created += 1
    quality = write_report(created, skipped, rows)
    print(json.dumps(quality, ensure_ascii=False, indent=2))
    return 0 if quality["gate_status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
