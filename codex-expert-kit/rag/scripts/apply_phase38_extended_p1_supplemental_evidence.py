"""Supplement Phase 38 P0-Extended / P1 evidence and export re-audit package.

This script updates 13 needs-more-evidence candidates plus the rebuilt C10-R1
candidate. It prepares them for second audit only; it does not create reviewed,
approved, default-guidance, or hard-gate knowledge.
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
SOURCE_AUDIT_RESULT_ID = "audit_result_phase38_extended_p1_20260610_strict_v1"
PACKAGE_ID = "phase38_extended_p1_supplemental_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase38_extended_p1_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs", "audit", f"{PACKAGE_ID}.json", start_file=__file__
)
REPORT_PATH = resolve_repo_path(
    "docs", "reports", "phase38_extended_p1_supplemental_evidence_report.json", start_file=__file__
)


SOURCES: dict[str, dict[str, Any]] = {
    "shap_causal_warning": {
        "source_id": "src_shap_causal_warning",
        "source_title": "Be careful when interpreting predictive models in search of causal insights",
        "source_url": "https://shap.readthedocs.io/en/latest/example_notebooks/overviews/Be%20careful%20when%20interpreting%20predictive%20models%20in%20search%20of%20causal%20insights.html",
        "source_type": "official_doc",
        "publisher": "SHAP",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "SHAP documentation explicitly warns that explaining correlations learned by predictive models does not make them causal.",
        "quoted_excerpt_allowed": False,
    },
    "causal_inference_book": {
        "source_id": "src_pearl_causal_inference_primer",
        "source_title": "Causal Inference in Statistics: A Primer",
        "source_url": "http://bayes.cs.ucla.edu/PRIMER/",
        "source_type": "book",
        "publisher": "UCLA Causality Lab",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "Causal inference requires explicit causal assumptions and intervention/counterfactual reasoning, not only predictive feature attribution.",
        "quoted_excerpt_allowed": False,
    },
    "sklearn_ndcg": {
        "source_id": "src_sklearn_ndcg_score",
        "source_title": "sklearn.metrics.ndcg_score",
        "source_url": "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.ndcg_score.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "scikit-learn documents NDCG as a ranking quality metric, supporting review-priority ranking evaluation.",
        "quoted_excerpt_allowed": False,
    },
    "lightgbm_lambdarank": {
        "source_id": "src_lightgbm_lambdarank",
        "source_title": "LightGBM Parameters - lambdarank objective",
        "source_url": "https://lightgbm.readthedocs.io/en/latest/Parameters.html",
        "source_type": "official_doc",
        "publisher": "LightGBM",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "LightGBM documents ranking objectives such as lambdarank, supporting ranking-model use when the target is ordered review priority.",
        "quoted_excerpt_allowed": False,
    },
    "conformal_tutorial": {
        "source_id": "src_conformal_prediction_tutorial",
        "source_title": "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification",
        "source_url": "https://arxiv.org/abs/2107.07511",
        "source_type": "paper",
        "publisher": "arXiv",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "Conformal prediction provides distribution-free uncertainty sets under explicit assumptions, supporting its use as an uncertainty enhancement layer.",
        "quoted_excerpt_allowed": False,
    },
    "sklearn_calibration": {
        "source_id": "src_sklearn_probability_calibration",
        "source_title": "Probability calibration",
        "source_url": "https://scikit-learn.org/stable/modules/calibration.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "scikit-learn documents probability calibration and calibration curves, supporting separation of score estimation and calibration.",
        "quoted_excerpt_allowed": False,
    },
    "openai_model_optimization": {
        "source_id": "src_openai_model_optimization",
        "source_title": "Model optimization",
        "source_url": "https://developers.openai.com/api/docs/guides/model-optimization",
        "source_type": "official_doc",
        "publisher": "OpenAI",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "OpenAI model optimization guidance distinguishes prompt engineering, retrieval/context, and fine-tuning as different optimization levers.",
        "quoted_excerpt_allowed": False,
    },
    "rag_paper": {
        "source_id": "src_rag_original_paper",
        "source_title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "source_url": "https://arxiv.org/abs/2005.11401",
        "source_type": "paper",
        "publisher": "arXiv",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "The RAG paper supports retrieval-augmented generation as a distinct mechanism for grounding generation in external knowledge.",
        "quoted_excerpt_allowed": False,
    },
    "hf_peft_lora": {
        "source_id": "src_hf_peft_lora",
        "source_title": "LoRA - Hugging Face PEFT",
        "source_url": "https://huggingface.co/docs/peft/package_reference/lora",
        "source_type": "official_doc",
        "publisher": "Hugging Face",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Hugging Face PEFT documents LoRA as parameter-efficient fine-tuning by adapting low-rank matrices instead of full model weights.",
        "quoted_excerpt_allowed": False,
    },
    "hf_structured_output": {
        "source_id": "src_hf_structured_output",
        "source_title": "Structured Outputs with Inference Providers",
        "source_url": "https://huggingface.co/docs/inference-providers/en/guides/structured-output",
        "source_type": "official_doc",
        "publisher": "Hugging Face",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Hugging Face structured output docs support using JSON Schema to obtain predictable, parsable model responses.",
        "quoted_excerpt_allowed": False,
    },
    "json_schema": {
        "source_id": "src_json_schema_docs",
        "source_title": "JSON Schema Documentation",
        "source_url": "https://json-schema.org/docs",
        "source_type": "official_doc",
        "publisher": "JSON Schema",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "JSON Schema supports declarative validation of JSON object structure, required fields, types, and enum constraints.",
        "quoted_excerpt_allowed": False,
    },
    "ragas_faithfulness": {
        "source_id": "src_ragas_faithfulness",
        "source_title": "Faithfulness - Ragas",
        "source_url": "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/",
        "source_type": "official_doc",
        "publisher": "Ragas",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Ragas faithfulness evaluates whether generated answers are factually consistent with retrieved context.",
        "quoted_excerpt_allowed": False,
    },
    "langfuse_llm_judge": {
        "source_id": "src_langfuse_llm_as_judge",
        "source_title": "LLM-as-a-Judge Evaluation",
        "source_url": "https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge",
        "source_type": "official_doc",
        "publisher": "Langfuse",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 80,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Langfuse documents LLM-as-a-judge for evaluation, including RAG faithfulness and relevance metrics, which should be treated as evaluators rather than factual sources.",
        "quoted_excerpt_allowed": False,
    },
    "pykeen_ablation": {
        "source_id": "src_pykeen_ablation_study",
        "source_title": "Running an Ablation Study",
        "source_url": "https://pykeen.readthedocs.io/en/latest/tutorial/running_ablation.html",
        "source_type": "official_doc",
        "publisher": "PyKEEN",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 80,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "PyKEEN documentation defines ablation studies as controlled experiments that remove or replace components to measure their impact.",
        "quoted_excerpt_allowed": False,
    },
    "mlflow_tracking": {
        "source_id": "src_mlflow_tracking",
        "source_title": "MLflow Tracking",
        "source_url": "https://mlflow.org/docs/latest/ml/tracking/",
        "source_type": "official_doc",
        "publisher": "MLflow",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "medium",
        "freshness": "time_sensitive",
        "evidence_summary": "MLflow Tracking supports recording experiment parameters, metrics, artifacts, and lineage needed for isolated ablation comparisons.",
        "quoted_excerpt_allowed": False,
    },
    "open_bandit_pipeline": {
        "source_id": "src_open_bandit_pipeline",
        "source_title": "Open Bandit Pipeline documentation",
        "source_url": "https://zr-obp.readthedocs.io/en/latest/",
        "source_type": "official_doc",
        "publisher": "Open Bandit Pipeline",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Open Bandit Pipeline supports off-policy evaluation using logged bandit feedback to estimate target policy performance without direct deployment.",
        "quoted_excerpt_allowed": False,
    },
    "deep_active_learning_survey": {
        "source_id": "src_deep_active_learning_survey",
        "source_title": "A Survey of Deep Active Learning",
        "source_url": "https://arxiv.org/abs/2009.00236",
        "source_type": "paper",
        "publisher": "arXiv",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "The survey covers active learning query strategies such as uncertainty, diversity, and expected model change, and notes sampling-bias risks.",
        "quoted_excerpt_allowed": False,
    },
    "llm_compression_survey": {
        "source_id": "src_llm_compression_survey",
        "source_title": "A Survey on Model Compression for Large Language Models",
        "source_url": "https://arxiv.org/abs/2308.07633",
        "source_type": "paper",
        "publisher": "arXiv",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "The survey covers LLM compression methods including quantization, pruning, and knowledge distillation.",
        "quoted_excerpt_allowed": False,
    },
    "model_compression_survey": {
        "source_id": "src_model_compression_survey_frontiers",
        "source_title": "A survey of model compression techniques: past, present, and future",
        "source_url": "https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2025.1518965/full",
        "source_type": "paper",
        "publisher": "Frontiers in Robotics and AI",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "The survey classifies model compression into pruning, low-rank decomposition, quantization, and distillation.",
        "quoted_excerpt_allowed": False,
    },
    "feast_point_in_time": {
        "source_id": "src_feast_point_in_time_joins",
        "source_title": "Point-in-time joins",
        "source_url": "https://docs.feast.dev/getting-started/concepts/point-in-time-joins",
        "source_type": "official_doc",
        "publisher": "Feast",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 86,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "Feast point-in-time joins support reproducing historical feature state without leaking future feature values.",
        "quoted_excerpt_allowed": False,
    },
    "tfdv_skew": {
        "source_id": "src_tfdv_training_serving_skew",
        "source_title": "TensorFlow Data Validation: Checking and analyzing your data",
        "source_url": "https://www.tensorflow.org/tfx/guide/tfdv",
        "source_type": "official_doc",
        "publisher": "TensorFlow",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 84,
        "relevance": "high",
        "freshness": "time_sensitive",
        "evidence_summary": "TFDV documents training-serving skew detection and drift checks between training and serving data.",
        "quoted_excerpt_allowed": False,
    },
    "domain_adaptation_intro": {
        "source_id": "src_domain_adaptation_transfer_learning_intro",
        "source_title": "An introduction to domain adaptation and transfer learning",
        "source_url": "https://arxiv.org/abs/1812.11806",
        "source_type": "paper",
        "publisher": "arXiv",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 82,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "Domain adaptation literature explains how models can fail when source and target data distributions differ, supporting revalidation across markets/domains.",
        "quoted_excerpt_allowed": False,
    },
    "phase35_active_retrieval": {
        "source_id": "src_cek_ta_phase35_active_retrieval_protocol",
        "source_title": "CEK-TA Phase 35 External AI Active Retrieval Protocol",
        "source_url": "docs/contracts/external_ai_active_retrieval_protocol.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "CEK-TA Phase 35 defines active retrieval triggers, citation requirements, and no-hit handling for external project AI.",
        "quoted_excerpt_allowed": False,
    },
    "phase38_rag_contract": {
        "source_id": "src_cek_ta_phase38_rag_citation_reason_contract",
        "source_title": "Phase 38 RAG 引用、Reason Taxonomy 与默认指导门禁契约",
        "source_url": "docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 90,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "CEK-TA Phase 38 contract defines citation completeness, no-hit handling, machine_gate eligibility, reason taxonomy, and context budget boundaries.",
        "quoted_excerpt_allowed": False,
    },
    "phase37_fill_cost_boundary": {
        "source_id": "src_cek_ta_phase37_fill_cost_boundary",
        "source_title": "CEK-TA Phase 37 Trading Engineering knowledge expansion",
        "source_url": "docs/tasks/phase37_trading_engineering_knowledge_expansion.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "accessed_at": TODAY,
        "reliability": "high",
        "score": 88,
        "relevance": "high",
        "freshness": "stable",
        "evidence_summary": "CEK-TA Phase 37 owns K-line, fill model, cost model, replay/paper trading and Trading Engineering rule-body knowledge.",
        "quoted_excerpt_allowed": False,
    },
}


PATCHES: dict[str, dict[str, Any]] = {
    "P38-A09": {
        "sources": ["shap_causal_warning", "causal_inference_book"],
        "patch": "feature attribution 只能解释模型输出贡献或相关性模式，不能替代因果识别；若要写 causal explanation，必须另有 causal graph、干预或反事实设计。",
    },
    "P38-A10": {
        "sources": ["sklearn_ndcg", "lightgbm_lambdarank"],
        "patch": "ranking model 可用于 review_priority 排序增强，但输出只决定人工复核优先级，不得作为交易 gate 或收益承诺；必须用 NDCG/MAP 等排序指标独立评估。",
    },
    "P38-B10": {
        "sources": ["conformal_tutorial", "sklearn_calibration"],
        "patch": "conformal / Bayesian calibration 只能作为不确定性或校准增强层；必须声明假设、校准集和覆盖率/校准指标，不能替代 deterministic final gate。",
    },
    "P38-D07": {
        "sources": ["openai_model_optimization", "rag_paper"],
        "patch": "RAG/prompt baseline 应先建立可审计基线；只有当检索、提示和结构化输出仍无法稳定满足 schema/reason code 时，才考虑 SFT/LoRA。",
    },
    "P38-D08": {
        "sources": ["hf_peft_lora", "hf_structured_output", "json_schema"],
        "patch": "SFT LoRA 仅用于稳定输出 schema、reason code 和审计格式；格式约束仍应由 JSON Schema/structured output 校验，LoRA 不提供事实来源。",
    },
    "P38-D10": {
        "sources": ["ragas_faithfulness", "langfuse_llm_judge", "phase38_rag_contract"],
        "patch": "teacher model 可作审计 baseline 或 judge 辅助，但事实必须来自 citation resolver 和 formal knowledge；teacher 输出不得作为无来源事实。",
    },
    "P38-E07": {
        "sources": ["pykeen_ablation", "mlflow_tracking"],
        "patch": "RAG、prompt、model、threshold 的改动必须通过隔离 ablation 比较；每次只改变一个主要变量，并记录参数、指标、artifact 和版本。",
    },
    "P38-E08": {
        "sources": ["ragas_faithfulness", "phase38_rag_contract"],
        "patch": "shadow 记录必须包含 no-hit、conflict、citation completeness 和 faithfulness 相关字段，用于发现 RAG 覆盖缺口，不得自动放行交易。",
    },
    "P38-E09": {
        "sources": ["open_bandit_pipeline", "phase37_fill_cost_boundary"],
        "patch": "false block opportunity 可用 paper/replay/OPE/人工复核估计，但 fill、slippage、fee、latency 和成本假设必须引用 Trading Engineering，不得由 AI Engineering 自行定义。",
    },
    "P38-E10": {
        "sources": ["deep_active_learning_survey"],
        "patch": "active learning review sampling 只能用于提高人工标注/复核效率；采样策略要平衡 uncertainty、diversity 和代表性，不能用作收益承诺或自动 gate。",
    },
    "P38-F10": {
        "sources": ["llm_compression_survey", "model_compression_survey"],
        "patch": "model compression、quantization、distillation 只能在不破坏 schema、citation、校准、latency 和审计指标后考虑；压缩模型必须重新跑评估和回滚预案。",
    },
    "P38-G05": {
        "sources": ["ragas_faithfulness", "phase38_rag_contract"],
        "patch": "citation completeness 应进入 shadow 指标，衡量每条审计结论是否能解析到正式知识和来源；低完整率必须触发 no-hit/补证/人工复核。",
    },
    "P38-G06": {
        "sources": ["phase35_active_retrieval", "phase38_rag_contract"],
        "patch": "no-hit query 必须进入知识缺口队列，并记录 query、scope、requested_decision、missing_node 和下游影响；不得由 AI 现场编造规则。",
    },
    "P38-C10-R1": {
        "sources": ["feast_point_in_time", "tfdv_skew", "domain_adaptation_intro"],
        "patch": "跨市场迁移必须重新检查 point-in-time 特征可用性、training-serving skew、target domain 分布差异和 feature store AS-OF join；通过前不得进入 formal draft。",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    indexed: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase38_*.json")):
        item = read_json(path)
        task_id = item.get("research_task_id")
        if isinstance(task_id, str):
            indexed[task_id] = (path, item)
    return indexed


def add_sources(candidate: dict[str, Any], source_keys: list[str]) -> None:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for key in source_keys:
        source = dict(SOURCES[key])
        if source["source_id"] not in existing:
            refs.append(source)
            existing.add(source["source_id"])

    quality = candidate.setdefault("source_quality", {})
    high_count = len([ref for ref in refs if isinstance(ref, dict) and ref.get("reliability") == "high"])
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score", 0) or 0), 86)
    quality["primary_source_count"] = high_count
    quality["supporting_source_count"] = max(len(refs) - high_count, 0)
    limitations = quality.setdefault("limitations", [])
    note = "已按 Phase 38 P0-Extended/P1 严格审计补充 claim-specific 来源和 CEK-TA 内部契约；仍需二审后才能进入 formal draft。"
    if isinstance(limitations, list) and note not in limitations:
        limitations.append(note)


def block_default_guidance(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False
    review = candidate.setdefault("review", {})
    review["default_guidance_allowed"] = False
    conversion = candidate.setdefault("conversion_target", {})
    conversion["target_review_status"] = "draft"
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False


def patch_candidate(task_id: str, path: Path, candidate: dict[str, Any]) -> dict[str, Any]:
    patch = PATCHES[task_id]
    add_sources(candidate, patch["sources"])
    block_default_guidance(candidate)

    claim = candidate.setdefault("claim", {})
    claim["evidence_summary"] = patch["patch"]
    claim["interpretation_notes"] = (
        "本条只补 AI Engineering 方法和审计边界；交易规则本体、fill/cost/risk/execution 仍由 Trading Engineering 提供。"
    )

    status = candidate.setdefault("status", {})
    status["review_status"] = "needs_more_evidence"
    status["ingestion_decision"] = "ready_for_reaudit"
    status["decision_reason"] = "已按严格审计补充 claim-specific 来源，等待二审；不是 reviewed、approved 或 default guidance。"
    status["updated_at"] = TODAY

    workflow = candidate.setdefault("workflow", {})
    workflow["stage"] = "needs_more_evidence"
    workflow["queue_group"] = "needs_more_evidence"
    workflow["formal_knowledge_id"] = None
    workflow["formal_review_status"] = None
    workflow["next_action"] = "export_ai_audit"

    review = candidate.setdefault("review", {})
    review["reviewer"] = "codex_supplemental_evidence"
    review["reviewed_at"] = TODAY
    review["confidence"] = "medium"
    review["open_questions"] = ["补证已完成，等待外部 AI/人工二审确认是否可进入 formal draft。"]
    ai_audit = review.setdefault("ai_audit", {})
    if isinstance(ai_audit, dict):
        ai_audit["supplemental_evidence_status"] = "ready_for_reaudit"
        ai_audit["reviewed_allowed"] = False
        ai_audit["approved_allowed"] = False
        ai_audit["default_guidance_allowed"] = False
        ai_audit["hard_gate_allowed"] = False

    log = review.setdefault("audit_log", [])
    if isinstance(log, list):
        log.append(
            {
                "at": TODAY,
                "actor": "codex",
                "action": "extended_p1_supplemental_evidence_added",
                "reason": patch["patch"],
            }
        )

    checked = candidate.setdefault("conflict_audit", {}).setdefault("checked_against", [])
    if isinstance(checked, list):
        for contract in [
            "docs/contracts/phase38_rag_citation_and_reason_taxonomy_contract.md",
            "docs/tasks/phase37_trading_engineering_knowledge_expansion.md",
        ]:
            if contract not in checked:
                checked.append(contract)

    write_json(path, candidate)
    return {
        "candidate_id": candidate["candidate_id"],
        "research_task_id": task_id,
        "claim": claim.get("statement"),
        "normalized_claim": claim.get("normalized_claim"),
        "source_count": len(candidate.get("source_refs", [])),
        "patch_summary": patch["patch"],
        "source_ids": [SOURCES[key]["source_id"] for key in patch["sources"]],
        "path": rel(path),
    }


def write_research_doc(items: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 38 P0-Extended / P1 补证采集记录",
        "",
        "## 目标",
        "",
        "根据 Phase 38 P0-Extended / P1 严格审计报告，为 13 条 needs_more_evidence 候选和 C10-R1 重建候选补充 claim-specific 来源。本记录只用于二审准备，不代表 reviewed、approved、default guidance 或 hard gate。",
        "",
        "## 补证结果",
        "",
    ]
    for item in items:
        lines.extend(
            [
                f"### {item['research_task_id']} - {item['candidate_id']}",
                "",
                f"- 补丁摘要：{item['patch_summary']}",
                f"- 来源数量：{item['source_count']}",
                f"- 来源 ID：{', '.join(item['source_ids'])}",
                f"- 候选路径：`{item['path']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## 边界",
            "",
            "```text",
            "1. 补证完成不等于审计通过。",
            "2. 本批候选仍停留在 needs_more_evidence / ready_for_reaudit。",
            "3. 二审通过后才允许进入 formal draft 队列。",
            "4. 任何候选都不能直接进入 reviewed、approved、default guidance 或 hard gate。",
            "5. fill、成本、风控、执行、K 线结构等交易规则本体继续路由到 Trading Engineering。",
            "```",
        ]
    )
    RESEARCH_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_audit_package(items: list[dict[str, Any]]) -> None:
    candidates = [read_json(resolve_repo_path(item["path"], start_file=__file__)) for item in items]
    package = {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_ai_reaudit_package",
        "generated_at": TODAY,
        "phase": "38",
        "task_id": "CEK-TA-287",
        "source_audit_result_id": SOURCE_AUDIT_RESULT_ID,
        "title": "Phase 38 P0-Extended / P1 补证后二审包",
        "purpose": "请复审 13 条 needs_more_evidence 和 C10-R1 补证候选，判断是否可升级为 accepted_for_draft。不得直接标记 reviewed、approved、default guidance 或 hard gate。",
        "candidate_count": len(candidates),
        "hard_boundaries": [
            "candidate 不是正式知识。",
            "accepted_for_draft 不是 reviewed，也不是 approved。",
            "本包不允许 direct reviewed、direct approved、default guidance 或 hard gate。",
            "本包只审 AI Engineering 方法；交易规则本体仍路由到 Trading Engineering。",
        ],
        "auditor_instruction": {
            "goal": "逐条判断补证是否足以从 needs_more_evidence 升级为 accepted_for_draft。",
            "allowed_decisions": ["accepted_for_draft", "needs_more_evidence", "rejected"],
            "required_output_schema": {
                "audit_result_id": "string",
                "source_package_id": PACKAGE_ID,
                "decisions": [
                    {
                        "candidate_id": "string",
                        "research_task_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reason": "string",
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                        "required_followups": ["string"],
                        "reviewed_allowed": False,
                        "approved_allowed": False,
                        "default_guidance_allowed": False,
                        "hard_gate_allowed": False
                    }
                ],
                "batch_summary": {
                    "accepted_for_draft_count": 0,
                    "needs_more_evidence_count": 0,
                    "rejected_count": 0,
                    "direct_reviewed_count": 0,
                    "direct_approved_count": 0,
                    "default_guidance_allowed_count": 0,
                    "hard_gate_allowed_count": 0
                }
            },
        },
        "supplemental_items": items,
        "candidates": candidates,
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def main() -> int:
    indexed = load_candidates()
    missing = sorted(set(PATCHES) - set(indexed))
    if missing:
        raise SystemExit(f"Missing candidates for supplemental evidence: {missing}")

    results = []
    for task_id in sorted(PATCHES):
        path, candidate = indexed[task_id]
        results.append(patch_candidate(task_id, path, candidate))

    write_research_doc(results)
    write_audit_package(results)

    report = {
        "report_id": "phase38_extended_p1_supplemental_evidence_report",
        "generated_at": TODAY,
        "supplemented_count": len(results),
        "research_path": rel(RESEARCH_PATH),
        "audit_package_path": rel(AUDIT_PACKAGE_PATH),
        "items": results,
        "boundary": {
            "formal_reviewed_created": False,
            "approved_created": False,
            "default_guidance_allowed": False,
            "hard_gate_allowed": False,
        },
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
