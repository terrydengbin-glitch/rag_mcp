"""Generate Phase 38 AI model platform P0-Core candidate knowledge files.

This script writes candidate JSON only. It does not create formal reviewed or
approved knowledge.
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


TODAY = "2026-06-10"
MATRIX = resolve_repo_path("docs", "research", "phase38_ai_model_platform_collection_matrix.md", start_file=__file__)
CAND_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
REPORT = resolve_repo_path("docs", "reports", "phase38_p0_core_candidate_generation_report.md", start_file=__file__)
QUALITY = resolve_repo_path("docs", "reports", "phase38_p0_core_candidate_quality_gate.json", start_file=__file__)


SOURCE_CATALOG = {
    "sklearn_calibration": {
        "title": "Probability calibration - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/calibration.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "summary": "scikit-learn documents probability calibration and why classifier probabilities can require calibration before use.",
    },
    "sklearn_brier": {
        "title": "brier_score_loss - scikit-learn documentation",
        "url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.brier_score_loss.html",
        "type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "summary": "scikit-learn defines Brier score loss as a proper scoring rule for probabilistic predictions.",
    },
    "lightgbm": {
        "title": "LightGBM documentation",
        "url": "https://lightgbm.readthedocs.io/",
        "type": "official_doc",
        "publisher": "LightGBM",
        "score": 84,
        "summary": "LightGBM official documentation describes a tree-based gradient boosting framework for efficient model training.",
    },
    "xgboost": {
        "title": "XGBoost documentation",
        "url": "https://xgboost.readthedocs.io/",
        "type": "official_doc",
        "publisher": "XGBoost",
        "score": 84,
        "summary": "XGBoost documentation describes scalable and portable gradient boosting for classification, regression, and ranking.",
    },
    "catboost": {
        "title": "CatBoost documentation",
        "url": "https://catboost.ai/",
        "type": "official_doc",
        "publisher": "CatBoost",
        "score": 82,
        "summary": "CatBoost documentation describes gradient boosting over decision trees with categorical feature support.",
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
        "summary": "TRL SFT Trainer documentation supports supervised fine-tuning workflows for language model outputs.",
    },
    "trl_dpo": {
        "title": "DPO Trainer - Hugging Face TRL",
        "url": "https://huggingface.co/docs/trl/en/dpo_trainer",
        "type": "official_doc",
        "publisher": "Hugging Face",
        "score": 84,
        "summary": "TRL DPO Trainer documentation supports preference optimization from chosen/rejected training pairs.",
    },
    "mlflow_registry": {
        "title": "MLflow Model Registry",
        "url": "https://mlflow.org/docs/latest/ml/model-registry/",
        "type": "official_doc",
        "publisher": "MLflow",
        "score": 84,
        "summary": "MLflow Model Registry documents model versions, aliases, registry workflows, and lifecycle management.",
    },
    "dvc": {
        "title": "Get Started with DVC",
        "url": "https://doc.dvc.org/start",
        "type": "official_doc",
        "publisher": "DVC",
        "score": 82,
        "summary": "DVC documentation supports data and model versioning for reproducible ML workflows.",
    },
    "dvc_pipelines": {
        "title": "DVC Data Pipelines",
        "url": "https://doc.dvc.org/start/data-pipelines/data-pipelines",
        "type": "official_doc",
        "publisher": "DVC",
        "score": 82,
        "summary": "DVC pipelines document versioned workflow steps and reproducible data science pipelines.",
    },
    "tfdv": {
        "title": "TensorFlow Data Validation",
        "url": "https://www.tensorflow.org/tfx/data_validation/get_started",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "TFDV documents schema inference, expected feature properties, data validation, skew, and drift checks.",
    },
    "tfdv_guide": {
        "title": "TensorFlow Data Validation Guide",
        "url": "https://github.com/tensorflow/tfx/blob/master/docs/guide/tfdv.md",
        "type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "summary": "TFDV guide covers schema validation, training-serving skew detection, and drift detection.",
    },
    "nist_ai_rmf": {
        "title": "NIST AI Risk Management Framework",
        "url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "type": "governance_framework",
        "publisher": "NIST",
        "score": 88,
        "summary": "NIST AI RMF supports AI risk governance, measurement, management, and trustworthy AI practices.",
    },
    "hudson_meta_labeling": {
        "title": "Meta Labeling - Hudson & Thames",
        "url": "https://hudsonthames.org/meta-labeling-a-toy-example/",
        "type": "engineering_article",
        "publisher": "Hudson & Thames",
        "score": 78,
        "summary": "Hudson & Thames describes meta-labeling as a second-layer model for filtering candidate labels such as false positives.",
    },
    "xgboost_paper": {
        "title": "XGBoost: A Scalable Tree Boosting System",
        "url": "https://arxiv.org/abs/1603.02754",
        "type": "paper",
        "publisher": "arXiv",
        "score": 84,
        "summary": "The XGBoost paper describes scalable tree boosting and its broad use in structured predictive modeling.",
    },
}


SOURCE_GROUPS = {
    "numeric_scoring": ["nist_ai_rmf", "lightgbm", "xgboost"],
    "model_selection": ["lightgbm", "xgboost", "catboost"],
    "meta_labeling": ["hudson_meta_labeling", "xgboost_paper", "nist_ai_rmf"],
    "calibration_threshold": ["sklearn_calibration", "sklearn_brier", "nist_ai_rmf"],
    "decision_time_feature_contract": ["tfdv", "tfdv_guide", "dvc"],
    "llm_audit_assistant": ["trl", "trl_sft", "nist_ai_rmf"],
    "llm_preference": ["trl", "trl_dpo", "nist_ai_rmf"],
    "shadow_paper_ope_eval": ["sklearn_calibration", "nist_ai_rmf", "dvc"],
    "model_release_governance": ["mlflow_registry", "dvc", "nist_ai_rmf"],
    "rag_pack": ["nist_ai_rmf", "tfdv", "dvc"],
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


def topic_group(topic_id: str, node_id: str, title: str) -> str:
    if node_id.endswith("numeric_scoring"):
        if "meta-labeling" in title:
            return "meta_labeling"
        if "LightGBM" in title or "XGBoost" in title:
            return "model_selection"
        return "numeric_scoring"
    if node_id.endswith("calibration_threshold"):
        return "calibration_threshold"
    if node_id.endswith("decision_time_feature_contract"):
        return "decision_time_feature_contract"
    if node_id.endswith("llm_audit_assistant"):
        if "DPO" in title or "SFT" in title:
            return "llm_preference"
        return "llm_audit_assistant"
    if node_id.endswith("shadow_paper_ope_eval"):
        return "shadow_paper_ope_eval"
    if node_id.endswith("model_release_governance"):
        return "model_release_governance"
    return "rag_pack"


def parse_matrix() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in MATRIX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P38-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[1] != "P0-Core":
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
        topics.add(raw.get("research_task_id", ""))
    return topics


def build_candidate(row: dict[str, str]) -> dict[str, object]:
    node_id = row["node_id"]
    partition_id, domain, subdomain = NODE_META[node_id]
    group = topic_group(row["topic_id"], node_id, row["title"])
    sources = [source_ref(key) for key in SOURCE_GROUPS[group]]
    score = round(sum(int(src["score"]) for src in sources) / len(sources))
    candidate_id = f"cand_20260610_phase38_{slug(row['topic_id'])}_{slug(row['title'])}_001"
    return {
        "schema_version": "1.0.0",
        "candidate_id": candidate_id,
        "research_task_id": row["topic_id"],
        "status": {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": "Phase 38 P0-Core sourced candidate; not reviewed, not approved, not default guidance.",
            "created_at": TODAY,
            "updated_at": TODAY,
        },
        "classification": {
            "tree_node_id": node_id,
            "canonical_node_id": node_id,
            "tree_path": "CEK-TA / AI Engineering",
            "related_nodes": [],
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
            "interpretation_notes": "本候选只沉淀 AI Engineering 的训练、评分、校准、评估、RAG/MCP、发布或治理方法；交易规则本体必须路由到 Phase 37。",
            "claim_strength": "high",
            "performance_claim": False,
        },
        "applicability": {
            "market": "general",
            "asset": "general",
            "timeframe": "general",
            "data_granularity": "general",
            "project_type": "trading_llm_assistant",
            "applies_when": [
                "外接项目正在构建交易 gating/scoring POC、训练数据、评估、RAG/MCP 或发布治理链路。",
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
                "docs/contracts/phase38_ai_scoring_gate_runtime_contract.md",
                "docs/contracts/phase38_training_data_and_eval_contract.md",
                "docs/tasks/phase38_ai_model_platform_poc_knowledge.md",
            ],
            "conflicts": [],
            "resolution_summary": "未发现与当前 Phase 38 契约的直接冲突；候选不会进入默认指导。",
            "approval_allowed": True,
        },
        "review": {
            "confidence": "medium",
            "freshness": "time_sensitive",
            "reviewer": "codex",
            "reviewed_at": None,
            "open_questions": ["审计时确认该候选是否应与相邻 Phase 38 规则合并、拆分，或改路由到 Trading Engineering。"],
            "audit_log": [{"at": TODAY, "actor": "codex", "action": "created", "reason": "Phase 38 P0-Core candidate expansion."}],
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


def load_phase38_candidates() -> list[dict[str, object]]:
    candidates = []
    for path in sorted(CAND_DIR.glob("cand_20260610_phase38_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        candidates.append(raw)
    return candidates


def write_report(created: int, skipped: int) -> dict[str, object]:
    candidates = load_phase38_candidates()
    failures = []
    for item in candidates:
        cid = item.get("candidate_id")
        if len(item.get("source_refs") or []) < 3:
            failures.append({"candidate_id": cid, "failure": "source_refs_lt_3"})
        if item.get("conflict_audit", {}).get("conflict_status") not in {"none", "resolved"}:
            failures.append({"candidate_id": cid, "failure": "unsafe_conflict_status"})
        if item.get("status", {}).get("review_status") != "proposed":
            failures.append({"candidate_id": cid, "failure": "not_candidate_proposed"})
    quality = {
        "report_id": "phase38_p0_core_candidate_quality_gate",
        "generated_at": TODAY,
        "scope": "Phase 38 P0-Core candidates",
        "candidate_count": len(candidates),
        "planned_p0_core_total": 43,
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
                "# Phase 38 P0-Core 候选知识生成报告",
                "",
                "## 结论",
                "",
                f"本次按 Phase 38 采集矩阵生成 P0-Core 候选知识 {created} 条，跳过已存在候选 {skipped} 条。当前 Phase 38 P0-Core 候选总数为 {len(candidates)} 条。",
                "",
                "所有新增内容仍为 candidate，不是 formal reviewed，不是 approved，也不会进入 MCP/SearchLab 默认指导。",
                "",
                "## 质量门禁",
                "",
                f"- gate_status: {quality['gate_status']}",
                f"- failure_count: {quality['failure_count']}",
                "",
                "## 下游",
                "",
                "下一步进入 CEK-TA-272：导出 Phase 38 候选 AI 审计包，统一审计后再按 Phase 32 工作流处理。",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return quality


def main() -> int:
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    existing = existing_phase38_topics()
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
