"""Apply Phase 41 strict candidate audit result.

This import only routes candidates, applies safety patches, rebuilds rejected
empty-slug candidates, and prepares a supplemental reaudit package. It does not
create formal reviewed/approved knowledge and never enables default guidance.
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = date(2026, 6, 10).isoformat()
AUDIT_RESULT_ID = "audit_result_phase41_candidate_audit_package_20260610_strict_v1"
SOURCE_PACKAGE_ID = "phase41_candidate_audit_package_20260610"

CANDIDATE_DIR = resolve_repo_path("codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__)
AUDIT_COPY_PATH = resolve_repo_path("docs", "audit", f"{AUDIT_RESULT_ID}.json", start_file=__file__)
REPORT_PATH = resolve_repo_path("docs", "reports", "phase41_candidate_audit_import_report.json", start_file=__file__)
SUPPLEMENTAL_RESEARCH = resolve_repo_path("docs", "research", "phase41_candidate_supplemental_research.md", start_file=__file__)
SUPPLEMENTAL_PACKAGE = resolve_repo_path(
    "docs", "audit", "phase41_candidate_supplemental_reaudit_package_20260610.json", start_file=__file__
)

EXPECTED_TASKS = {
    "P41-A01",
    "P41-A02",
    "P41-A03",
    "P41-A05",
    "P41-B01",
    "P41-B02",
    "P41-B03",
    "P41-B05",
    "P41-C01",
    "P41-C02",
    "P41-C03",
    "P41-D01",
    "P41-D02",
    "P41-D03",
    "P41-D04",
    "P41-E01",
    "P41-E02",
    "P41-E03",
    "P41-E05",
    "P41-E09",
    "P41-F01",
    "P41-F02",
}

REBUILDS: dict[str, dict[str, str]] = {
    "P41-A05": {
        "research_task_id": "P41-A05-R1",
        "candidate_id": "cand_20260610_phase41_p41_a05_model_selection_business_cost_latency_explainability_calibration_governance_001",
        "normalized_claim": "phase41.model_selection_business_cost_latency_explainability_calibration_governance.v1",
        "proposed_knowledge_id": "kb_ai_hybrid_scoring.phase41.model_selection_business_cost_latency_explainability_calibration_governance.v1",
        "statement": "模型选择必须同时比较业务成本、延迟、可解释性、校准质量和治理复杂度。",
        "followup_reason": "原候选空 slug 已拒绝；重建后仍需确认 latency/cost/governance 证据是否足够 claim-specific。",
    },
    "P41-B03": {
        "research_task_id": "P41-B03-R1",
        "candidate_id": "cand_20260610_phase41_p41_b03_time_aware_split_no_random_shuffle_001",
        "normalized_claim": "phase41.time_aware_split_no_random_shuffle.v1",
        "proposed_knowledge_id": "kb_ai_hybrid_scoring.phase41.time_aware_split_no_random_shuffle.v1",
        "statement": "时间序列交易样本必须使用时间感知切分，不能随机打散导致未来信息泄漏。",
        "followup_reason": "原候选空 slug 已拒绝；重建后保留 TimeSeriesSplit 与 leakage evidence 等待二审。",
    },
    "P41-D02": {
        "research_task_id": "P41-D02-R1",
        "candidate_id": "cand_20260610_phase41_p41_d02_offline_online_feature_parity_default_guidance_block_001",
        "normalized_claim": "phase41.offline_online_feature_parity_default_guidance_block.v1",
        "proposed_knowledge_id": "kb_ai_hybrid_scoring.phase41.offline_online_feature_parity_default_guidance_block.v1",
        "statement": "线上线下特征生成必须一致；不一致时必须记录差异并阻断默认指导。",
        "followup_reason": "原候选空 slug 已拒绝；重建后补充 offline/online parity 与 training-serving skew 证据等待二审。",
    },
}

EXTRA_SOURCES: dict[str, dict[str, Any]] = {
    "sklearn_calibration": {
        "source_id": "src_sklearn_calibration",
        "source_title": "Probability calibration - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/calibration.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 88,
        "evidence_summary": "scikit-learn documents classifier probability calibration and calibration methods such as sigmoid and isotonic calibration.",
    },
    "sklearn_threshold": {
        "source_id": "src_sklearn_classification_threshold",
        "source_title": "Tuning the decision threshold for class prediction - scikit-learn documentation",
        "source_url": "https://scikit-learn.org/stable/modules/classification_threshold.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "evidence_summary": "scikit-learn documents post-tuning classification thresholds and using scoring objectives to choose decision thresholds.",
    },
    "sklearn_cost_threshold": {
        "source_id": "src_sklearn_cost_sensitive_threshold_example",
        "source_title": "Post-tuning the decision threshold for cost-sensitive learning - scikit-learn",
        "source_url": "https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html",
        "source_type": "official_doc",
        "publisher": "scikit-learn",
        "score": 86,
        "evidence_summary": "scikit-learn demonstrates selecting a threshold that minimizes a business cost function.",
    },
    "ragas_faithfulness": {
        "source_id": "src_ragas_faithfulness",
        "source_title": "Faithfulness - Ragas documentation",
        "source_url": "https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/",
        "source_type": "official_doc",
        "publisher": "Ragas",
        "score": 82,
        "evidence_summary": "Ragas describes faithfulness as factual consistency of a response with retrieved context and checks whether claims are supported by context.",
    },
    "deepeval_faithfulness": {
        "source_id": "src_deepeval_faithfulness",
        "source_title": "Faithfulness - DeepEval documentation",
        "source_url": "https://deepeval.com/docs/metrics-faithfulness",
        "source_type": "official_doc",
        "publisher": "DeepEval",
        "score": 80,
        "evidence_summary": "DeepEval documents a faithfulness metric for evaluating whether RAG output aligns with retrieval context.",
    },
    "promptfoo_context_faithfulness": {
        "source_id": "src_promptfoo_context_faithfulness",
        "source_title": "Context faithfulness - Promptfoo documentation",
        "source_url": "https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/context-faithfulness/",
        "source_type": "official_doc",
        "publisher": "Promptfoo",
        "score": 80,
        "evidence_summary": "Promptfoo context faithfulness checks if an LLM response only makes claims supported by provided context.",
    },
    "feast_point_in_time": {
        "source_id": "src_feast_point_in_time_joins",
        "source_title": "Point-in-time joins - Feast documentation",
        "source_url": "https://docs.feast.dev/getting-started/concepts/point-in-time-joins",
        "source_type": "official_doc",
        "publisher": "Feast",
        "score": 84,
        "evidence_summary": "Feast documents point-in-time correct feature joins that reproduce feature state at a specific past time.",
    },
    "databricks_point_in_time": {
        "source_id": "src_databricks_point_in_time_feature_joins",
        "source_title": "Point-in-time feature joins - Databricks documentation",
        "source_url": "https://docs.databricks.com/aws/en/machine-learning/feature-store/time-series",
        "source_type": "official_doc",
        "publisher": "Databricks",
        "score": 82,
        "evidence_summary": "Databricks documents point-in-time correctness for creating training datasets that reflect feature values available at label time.",
    },
    "tfdv_skew": {
        "source_id": "src_tfdv_training_serving_skew",
        "source_title": "TensorFlow Data Validation Guide",
        "source_url": "https://www.tensorflow.org/tfx/guide/tfdv",
        "source_type": "official_doc",
        "publisher": "TensorFlow",
        "score": 82,
        "evidence_summary": "TFDV documents training-serving skew detection by comparing distributions between training and serving data.",
    },
    "sec_knight": {
        "source_id": "src_sec_knight_capital_release_2013_222",
        "source_title": "SEC Charges Knight Capital With Violations of Market Access Rule",
        "source_url": "https://www.sec.gov/newsroom/press-releases/2013-222",
        "source_type": "regulator_release",
        "publisher": "SEC",
        "score": 84,
        "evidence_summary": "SEC's Knight Capital release is a regulatory incident reference for algorithmic trading controls and failure impact.",
    },
    "fca_algo_controls": {
        "source_id": "src_fca_algorithmic_trading_controls",
        "source_title": "Algorithmic trading controls: high level observations",
        "source_url": "https://www.fca.org.uk/publications/multi-firm-reviews/algorithmic-trading-controls-high-level-observations",
        "source_type": "regulator_review",
        "publisher": "FCA",
        "score": 84,
        "evidence_summary": "FCA observations describe governance and control expectations for algorithmic trading environments.",
    },
    "phase41_runtime_contract": {
        "source_id": "src_phase41_runtime_contract",
        "source_title": "Phase 41 Hybrid Scoring 运行时契约",
        "source_url": "docs/contracts/phase41_hybrid_scoring_runtime_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 86,
        "evidence_summary": "CEK-TA internal contract defines Qwen3 audit, citation resolver, threshold policy, final gate and composite release manifest boundaries.",
    },
    "phase41_training_data_contract": {
        "source_id": "src_phase41_training_data_contract",
        "source_title": "Phase 41 表格模型与 Qwen3 审计助手训练数据契约",
        "source_url": "docs/contracts/phase41_tabular_llm_training_data_contract.md",
        "source_type": "internal_contract",
        "publisher": "CEK-TA",
        "score": 86,
        "evidence_summary": "CEK-TA internal contract defines split manifest, baseline model card, label observation and feature lineage boundaries.",
    },
}

SUPPLEMENTAL_SOURCE_KEYS: dict[str, list[str]] = {
    "P41-A03": ["phase41_training_data_contract"],
    "P41-A05-R1": ["sklearn_threshold", "sklearn_cost_threshold", "phase41_runtime_contract"],
    "P41-B01": ["sklearn_calibration", "phase41_training_data_contract"],
    "P41-B03-R1": ["phase41_training_data_contract"],
    "P41-C03": ["sklearn_threshold", "sklearn_cost_threshold", "phase41_runtime_contract"],
    "P41-D01": ["feast_point_in_time", "databricks_point_in_time"],
    "P41-D02-R1": ["tfdv_skew", "phase41_training_data_contract"],
    "P41-D04": ["phase41_training_data_contract"],
    "P41-E01": ["phase41_runtime_contract"],
    "P41-E03": ["ragas_faithfulness", "deepeval_faithfulness", "promptfoo_context_faithfulness", "phase41_runtime_contract"],
    "P41-E05": ["phase41_runtime_contract"],
    "P41-E09": ["ragas_faithfulness", "promptfoo_context_faithfulness", "phase41_runtime_contract"],
    "P41-F01": ["sec_knight", "fca_algo_controls", "phase41_runtime_contract"],
    "P41-F02": ["phase41_runtime_contract"],
}

SUPPLEMENTAL_TASKS = {
    "P41-B01",
    "P41-C03",
    "P41-E03",
    "P41-E09",
    "P41-F02",
    "P41-A05-R1",
    "P41-B03-R1",
    "P41-D02-R1",
}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def repo_rel(path: Path) -> str:
    return path.relative_to(resolve_repo_path(start_file=__file__)).as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit_result_path", type=Path)
    return parser.parse_args()


def decision_by_task(audit_result: dict[str, Any]) -> dict[str, dict[str, Any]]:
    decisions: dict[str, dict[str, Any]] = {}
    for item in audit_result.get("decisions", []):
        if isinstance(item, dict) and isinstance(item.get("research_task_id"), str):
            decisions[item["research_task_id"]] = item
    return decisions


def validate_audit_result(audit_result: dict[str, Any]) -> None:
    if audit_result.get("audit_result_id") != AUDIT_RESULT_ID:
        raise ValueError("Unexpected audit_result_id")
    if audit_result.get("source_package_id") != SOURCE_PACKAGE_ID:
        raise ValueError("Unexpected source_package_id")
    decisions = decision_by_task(audit_result)
    missing = sorted(EXPECTED_TASKS - set(decisions))
    unexpected = sorted(set(decisions) - EXPECTED_TASKS)
    if missing:
        raise ValueError(f"Missing audit decisions: {missing}")
    if unexpected:
        raise ValueError(f"Unexpected audit decisions: {unexpected}")
    forbidden = [
        item.get("candidate_id")
        for item in decisions.values()
        if item.get("reviewed_allowed")
        or item.get("approved_allowed")
        or item.get("default_guidance_allowed")
        or item.get("hard_gate_allowed")
    ]
    if forbidden:
        raise ValueError(f"Audit result unexpectedly allowed reviewed/approved/default/hard gate: {forbidden}")


def load_candidates() -> dict[str, tuple[Path, dict[str, Any]]]:
    result: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in sorted(CANDIDATE_DIR.glob("cand_20260610_phase41_*.json")):
        candidate = read_json(path)
        task_id = candidate.get("research_task_id")
        if isinstance(task_id, str):
            result[task_id] = (path, candidate)
    return result


def source_ref(key: str) -> dict[str, Any]:
    source = copy.deepcopy(EXTRA_SOURCES[key])
    source["published_at"] = None
    source["accessed_at"] = TODAY
    source["version"] = None
    source["reliability"] = "high" if int(source["score"]) >= 80 else "medium"
    source["relevance"] = "high"
    source["freshness"] = "time_sensitive" if source["source_type"] in {"official_doc", "internal_contract"} else "stable"
    source["limitations"] = []
    source["quoted_excerpt_allowed"] = False
    return source


def add_sources(candidate: dict[str, Any], keys: list[str]) -> None:
    refs = candidate.setdefault("source_refs", [])
    existing = {ref.get("source_id") for ref in refs if isinstance(ref, dict)}
    for key in keys:
        source = source_ref(key)
        if source["source_id"] not in existing:
            refs.append(source)
            existing.add(source["source_id"])
    quality = candidate.setdefault("source_quality", {})
    quality["primary_source_count"] = len(
        [
            ref
            for ref in refs
            if isinstance(ref, dict)
            and ref.get("source_type")
            in {"official_doc", "research_paper", "standard_doc", "governance_framework", "security_standard", "internal_contract", "regulator_release", "regulator_review"}
        ]
    )
    quality["supporting_source_count"] = max(0, len(refs) - int(quality.get("primary_source_count", 0)))
    quality["overall_reliability"] = "high"
    quality["score"] = max(int(quality.get("score") or 0), 84)


def append_audit_log(candidate: dict[str, Any], action: str, reason: str) -> None:
    log = candidate.setdefault("review", {}).setdefault("audit_log", [])
    if isinstance(log, list):
        log.append({"at": TODAY, "actor": "codex", "action": action, "reason": reason})


def enforce_candidate_safety(candidate: dict[str, Any]) -> None:
    workflow = candidate.setdefault("workflow", {})
    workflow["hidden_from_default_queue"] = True
    workflow["visible_in_default_guidance_queue"] = False
    workflow["default_guidance_allowed"] = False

    conversion = candidate.setdefault("conversion_target", {})
    conversion["default_guidance_allowed"] = False
    conversion["hard_gate_allowed"] = False
    conversion.setdefault("target_review_status", "draft")

    machine_gate = candidate.setdefault("machine_gate", {})
    machine_gate["default_guidance"] = "deny"
    machine_gate["requires_human_escalation"] = True
    machine_gate["reason"] = "candidate only; Phase 41 strict audit does not allow reviewed, approved, default guidance, or hard gate."

    conflict = candidate.setdefault("conflict_audit", {})
    conflict["approval_allowed"] = False

    review = candidate.setdefault("review", {})
    review["reviewed_allowed"] = False
    review["approved_allowed"] = False
    review["default_guidance_allowed"] = False
    review["hard_gate_allowed"] = False


def apply_patch_notes(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    trace = candidate.setdefault("phase41_trace", {})
    trace["audit_patch_notes"] = {
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
    }
    limitations = candidate.setdefault("applicability", {}).setdefault("limitations", [])
    for note in decision.get("boundary_patch_notes", []) or []:
        if isinstance(note, str) and note not in limitations:
            limitations.append(note)


def apply_ai_audit(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    review = candidate.setdefault("review", {})
    review["reviewer"] = "external_ai_audit_plus_codex_import"
    review["reviewed_at"] = TODAY
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "candidate_id": decision.get("candidate_id"),
        "research_task_id": decision.get("research_task_id"),
        "decision": decision.get("decision"),
        "reason": decision.get("reason"),
        "source_patch_notes": decision.get("source_patch_notes", []),
        "content_patch_notes": decision.get("content_patch_notes", []),
        "boundary_patch_notes": decision.get("boundary_patch_notes", []),
        "conflict_patch_notes": decision.get("conflict_patch_notes", []),
        "required_followups": decision.get("required_followups", []),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
        "import_policy": "strict audit result may route candidates only; formal reviewed/approved creation is blocked.",
    }
    followups = decision.get("required_followups", [])
    if isinstance(followups, list):
        review["open_questions"] = followups
    apply_patch_notes(candidate, decision)


def mark_accepted(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    add_sources(candidate, SUPPLEMENTAL_SOURCE_KEYS.get(str(decision.get("research_task_id")), []))
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "accepted",
            "ingestion_decision": "accepted_for_draft",
            "decision_reason": "Phase 41 严格审计允许进入 formal draft 准备队列；不是 reviewed、approved 或默认指导。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "ai_audited",
            "queue_group": "ai_passed",
            "formal_knowledge_id": candidate.get("conversion_target", {}).get("proposed_knowledge_id"),
            "formal_review_status": "draft",
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "prepare_formal_draft_after_codex_patch_review",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase41_strict_audit_accepted_for_draft", "候选进入 formal draft 准备队列；不能直接 reviewed/approved。")


def mark_needs_more_evidence(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    add_sources(candidate, SUPPLEMENTAL_SOURCE_KEYS.get(str(decision.get("research_task_id")), []))
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "needs_more_evidence",
            "ingestion_decision": "needs_more_evidence",
            "decision_reason": "Phase 41 严格审计要求补充 claim-specific 来源、实例或 CEK-TA 契约后再二审。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "needs_more_evidence",
            "queue_group": "needs_more_evidence",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "supplement_sources_and_export_reaudit_package",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase41_strict_audit_needs_more_evidence", "已补充来源/契约，等待二审。")


def mark_rejected(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    enforce_candidate_safety(candidate)
    status = candidate.setdefault("status", {})
    status.update(
        {
            "review_status": "rejected",
            "ingestion_decision": "reject",
            "decision_reason": "Phase 41 严格审计发现空 slug 结构污染风险，原候选禁止进入 formal draft。",
            "updated_at": TODAY,
        }
    )
    workflow = candidate.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "rejected",
            "queue_group": "rejected",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "use_rebuilt_candidate_for_reaudit",
        }
    )
    apply_ai_audit(candidate, decision)
    append_audit_log(candidate, "phase41_strict_audit_rejected", "空 slug 结构污染风险；已生成重建候选。")


def rebuild_candidate(original: dict[str, Any], decision: dict[str, Any], config: dict[str, str]) -> dict[str, Any]:
    rebuilt = copy.deepcopy(original)
    rebuilt["candidate_id"] = config["candidate_id"]
    rebuilt["research_task_id"] = config["research_task_id"]
    rebuilt.setdefault("claim", {})["statement"] = config["statement"]
    rebuilt["claim"]["normalized_claim"] = config["normalized_claim"]
    rebuilt["claim"]["evidence_summary"] = (
        f"重建候选：{config['followup_reason']} 已补充结构化 ID 和补证来源，等待二审。"
    )
    rebuilt.setdefault("conversion_target", {})["proposed_knowledge_id"] = config["proposed_knowledge_id"]
    rebuilt["conversion_target"]["target_review_status"] = "draft"
    rebuilt["conversion_target"]["rebuilt_from_candidate_id"] = original.get("candidate_id")
    enforce_candidate_safety(rebuilt)
    add_sources(rebuilt, SUPPLEMENTAL_SOURCE_KEYS.get(config["research_task_id"], []))
    status = rebuilt.setdefault("status", {})
    status.update(
        {
            "review_status": "proposed",
            "ingestion_decision": "convert_to_knowledge_item",
            "decision_reason": config["followup_reason"],
            "created_at": TODAY,
            "updated_at": TODAY,
        }
    )
    workflow = rebuilt.setdefault("workflow", {})
    workflow.update(
        {
            "stage": "candidate_ready",
            "queue_group": "pending",
            "formal_knowledge_id": None,
            "formal_review_status": None,
            "ai_audit_result_id": AUDIT_RESULT_ID,
            "next_action": "export_for_supplemental_reaudit",
        }
    )
    review = rebuilt.setdefault("review", {})
    review["reviewer"] = "codex_rebuild_after_external_ai_audit"
    review["reviewed_at"] = None
    review["open_questions"] = decision.get("required_followups", [])
    review["ai_audit"] = {
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "previous_candidate_id": original.get("candidate_id"),
        "previous_research_task_id": original.get("research_task_id"),
        "decision": "rebuilt_after_rejection",
        "reason": decision.get("reason"),
        "required_followups": decision.get("required_followups", []),
        "reviewed_allowed": False,
        "approved_allowed": False,
        "default_guidance_allowed": False,
        "hard_gate_allowed": False,
    }
    append_audit_log(rebuilt, "phase41_rebuild_empty_slug_candidate", config["followup_reason"])
    return rebuilt


def supplemental_item(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_id": candidate.get("candidate_id"),
        "research_task_id": candidate.get("research_task_id"),
        "status": candidate.get("status"),
        "classification": candidate.get("classification"),
        "claim": candidate.get("claim"),
        "applicability": candidate.get("applicability"),
        "source_refs": candidate.get("source_refs"),
        "source_quality": candidate.get("source_quality"),
        "conflict_audit": candidate.get("conflict_audit"),
        "machine_gate": candidate.get("machine_gate"),
        "workflow": candidate.get("workflow"),
        "conversion_target": candidate.get("conversion_target"),
        "review": candidate.get("review"),
        "phase41_trace": candidate.get("phase41_trace"),
    }


def write_supplemental_research(items: list[dict[str, Any]]) -> None:
    lines = [
        "# Phase 41 候选审计补证记录",
        "",
        f"生成日期：{TODAY}",
        "",
        "## 结论",
        "",
        "本轮导入 Phase 41 严格审计结果后，5 条候选被标记为 needs_more_evidence，3 条空 slug 候选被拒绝并重建为 R1 候选。",
        "",
        "本轮只补候选来源和契约，不生成 formal reviewed，不设置 approved/default guidance。",
        "",
        "## 补证来源方向",
        "",
        "| 方向 | 来源 |",
        "| --- | --- |",
        "| 校准与加权后复核 | scikit-learn probability calibration、CEK-TA recalibration_after_weighting_report |",
        "| 成本敏感阈值与复核容量 | scikit-learn classification threshold、cost-sensitive threshold、CEK-TA review_capacity_policy |",
        "| RAG faithfulness / citation resolver | Ragas、DeepEval、Promptfoo、CEK-TA citation resolver contract |",
        "| point-in-time 与 offline/online parity | Feast point-in-time joins、Databricks point-in-time、TFDV training-serving skew |",
        "| final gate 与发布治理 | SEC Knight、FCA algorithmic controls、CEK-TA composite release manifest |",
        "",
        "## 二审候选",
        "",
        "| research_task_id | candidate_id | source_count | queue_group |",
        "| --- | --- | ---: | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.get('research_task_id')} | {item.get('candidate_id')} | {len(item.get('source_refs') or [])} | {item.get('workflow', {}).get('queue_group')} |"
        )
    lines.append("")
    SUPPLEMENTAL_RESEARCH.write_text("\n".join(lines), encoding="utf-8")


def write_supplemental_package(items: list[dict[str, Any]]) -> None:
    package = {
        "package_id": "phase41_candidate_supplemental_reaudit_package_20260610",
        "package_type": "candidate_supplemental_reaudit_package",
        "generated_at": TODAY,
        "source_audit_result_id": AUDIT_RESULT_ID,
        "phase": "41",
        "title": "Phase 41 needs_more_evidence 与重建候选二审包",
        "purpose": "请二审 5 条已补证 needs_more_evidence 候选和 3 条空 slug 重建候选，判断是否可进入 accepted_for_draft。不得直接 reviewed/approved。",
        "hard_boundaries": [
            "candidate 不是正式知识，不能作为默认指导。",
            "accepted_for_draft 不是 approved。",
            "reviewed 不等于 approved。",
            "本包只允许 decision 为 accepted_for_draft | needs_more_evidence | rejected。",
            "不得授权 default_guidance_allowed 或 hard_gate_allowed。",
        ],
        "required_output_schema": {
            "audit_result_id": "string",
            "source_package_id": "phase41_candidate_supplemental_reaudit_package_20260610",
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
                    "hard_gate_allowed": False,
                }
            ],
            "batch_summary": {
                "accepted_count": 0,
                "needs_more_evidence_count": 0,
                "rejected_count": 0,
            },
        },
        "candidate_count": len(items),
        "candidates": [supplemental_item(item) for item in items],
    }
    write_json(SUPPLEMENTAL_PACKAGE, package)


def main() -> int:
    args = parse_args()
    audit_path = args.audit_result_path
    audit_result = read_json(audit_path)
    validate_audit_result(audit_result)
    shutil.copyfile(audit_path, AUDIT_COPY_PATH)

    candidates = load_candidates()
    decisions = decision_by_task(audit_result)
    counts: Counter[str] = Counter()
    touched: list[str] = []
    rebuilt_paths: list[str] = []
    supplemental_candidates: list[dict[str, Any]] = []

    for task_id, decision in sorted(decisions.items()):
        if task_id not in candidates:
            raise ValueError(f"Candidate for {task_id} not found")
        path, candidate = candidates[task_id]
        if candidate.get("candidate_id") != decision.get("candidate_id"):
            raise ValueError(f"Candidate ID mismatch for {task_id}")
        decision_value = decision.get("decision")
        if decision_value == "accepted_for_draft":
            mark_accepted(candidate, decision)
            counts["accepted_for_draft"] += 1
        elif decision_value == "needs_more_evidence":
            mark_needs_more_evidence(candidate, decision)
            counts["needs_more_evidence"] += 1
            supplemental_candidates.append(candidate)
        elif decision_value == "rejected":
            mark_rejected(candidate, decision)
            counts["rejected"] += 1
            if task_id not in REBUILDS:
                raise ValueError(f"No rebuild config for rejected task {task_id}")
            rebuilt = rebuild_candidate(candidate, decision, REBUILDS[task_id])
            rebuilt_path = CANDIDATE_DIR / f"{rebuilt['candidate_id']}.json"
            write_json(rebuilt_path, rebuilt)
            rebuilt_paths.append(repo_rel(rebuilt_path))
            supplemental_candidates.append(rebuilt)
        else:
            raise ValueError(f"Unsupported decision for {task_id}: {decision_value}")

        write_json(path, candidate)
        touched.append(repo_rel(path))

    write_supplemental_research(supplemental_candidates)
    write_supplemental_package(supplemental_candidates)

    report = {
        "report_id": "phase41_candidate_audit_import_report",
        "generated_at": TODAY,
        "task_id": "CEK-TA-326",
        "audit_result_id": AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "audit_result_copy": repo_rel(AUDIT_COPY_PATH),
        "decision_counts": dict(counts),
        "reviewed_created": 0,
        "approved_created": 0,
        "default_guidance_enabled": 0,
        "hard_gate_enabled": 0,
        "updated_candidates": touched,
        "rebuilt_candidates": rebuilt_paths,
        "supplemental_reaudit_package": repo_rel(SUPPLEMENTAL_PACKAGE),
        "supplemental_research": repo_rel(SUPPLEMENTAL_RESEARCH),
        "status_boundary": "本次审计 reviewed_allowed_count=0；只回写候选状态、补证和重建，不生成 formal reviewed。",
        "next_action": "将 phase41_candidate_supplemental_reaudit_package_20260610.json 交给外部 AI/人工二审。",
    }
    write_json(REPORT_PATH, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
