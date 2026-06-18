"""Supplement Phase 36 batch 10 needs-more-evidence candidates.

This script keeps the four candidates in the second-review queue, adds direct
evidence, rewrites the placeholder claims, and exports an AI audit package.
"""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[2] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from path_resolver import resolve_repo_path  # noqa: E402


TODAY = "2026-06-09"
PACKAGE_ID = "phase36_batch10_strategy_training_example_supplemental_audit_package_20260609"
SOURCE_AUDIT_RESULT_ID = "audit_result_phase36_ai_engineering_batch_10_of_10_20260609_gpt55_pro_strict_sources"
SOURCE_PACKAGE_ID = "phase36_ai_engineering_candidate_audit_batch_10_of_10_20260609"

CANDIDATE_DIR = resolve_repo_path(
    "codex-expert-kit", "rag", "candidates", "KB_AI_ENGINEERING", start_file=__file__
)
RESEARCH_PATH = resolve_repo_path(
    "docs", "research", "phase36_batch10_strategy_training_example_supplemental_research.md", start_file=__file__
)
AUDIT_PACKAGE_PATH = resolve_repo_path(
    "docs",
    "audit",
    "phase36_batch10_strategy_training_example_supplemental_audit_package_20260609.json",
    start_file=__file__,
)


def source(
    source_id: str,
    title: str,
    url: str,
    source_type: str,
    publisher: str,
    reliability: str,
    score: int,
    relevance: str,
    freshness: str,
    summary: str,
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
        "reliability": reliability,
        "score": score,
        "relevance": relevance,
        "freshness": freshness,
        "limitations": limitations or [],
        "evidence_summary": summary,
        "quoted_excerpt_allowed": False,
    }


SOURCES = {
    "mlflow_tracking": source(
        "src_mlflow_tracking_2026",
        "MLflow Tracking",
        "https://mlflow.org/docs/latest/ml/tracking/",
        "official_doc",
        "MLflow",
        "high",
        88,
        "high",
        "time_sensitive",
        "MLflow Tracking records parameters, code versions, metrics, output files, run metadata, artifacts, and dataset-linked metrics, supporting run and release lineage for ML systems.",
    ),
    "dvc_files": source(
        "src_dvc_files_2026",
        ".dvc Files | Data Version Control",
        "https://dvc.org/doc/user-guide/project-structure/dvc-files",
        "official_doc",
        "DVC",
        "high",
        86,
        "high",
        "time_sensitive",
        "DVC .dvc files act as Git-versioned placeholders containing the metadata needed to track target data over time.",
    ),
    "datasheets": source(
        "src_datasheets_for_datasets_2018",
        "Datasheets for Datasets",
        "https://arxiv.org/abs/1803.09010",
        "paper",
        "arXiv",
        "high",
        88,
        "high",
        "stable",
        "Datasheets for Datasets supports documenting dataset motivation, composition, collection process, recommended uses, maintenance, and limitations for transparency and accountability.",
    ),
    "sklearn_leakage": source(
        "src_sklearn_common_pitfalls_data_leakage_2026",
        "Common pitfalls and recommended practices | scikit-learn",
        "https://scikit-learn.org/stable/common_pitfalls.html",
        "official_doc",
        "scikit-learn",
        "high",
        88,
        "high",
        "time_sensitive",
        "scikit-learn defines data leakage as using information unavailable at prediction time and recommends splitting data before preprocessing and fitting transformations only on training data.",
    ),
    "trl_sft": source(
        "src_huggingface_trl_sft_trainer_2026",
        "SFT Trainer | Hugging Face TRL",
        "https://huggingface.co/docs/trl/en/sft_trainer",
        "official_doc",
        "Hugging Face",
        "high",
        86,
        "high",
        "time_sensitive",
        "TRL SFTTrainer documents standard and conversational language modeling and prompt-completion dataset formats, including separate prompt and completion fields and completion-only training options.",
    ),
    "openai_structured_outputs": source(
        "src_openai_structured_outputs_2026",
        "Structured model outputs | OpenAI API",
        "https://platform.openai.com/docs/guides/structured-outputs",
        "official_doc",
        "OpenAI",
        "high",
        86,
        "high",
        "time_sensitive",
        "OpenAI Structured Outputs supports JSON Schema constrained outputs, schema design, type-safe parsing, and downstream validation handling.",
    ),
    "json_schema": source(
        "src_json_schema_specification_2026",
        "JSON Schema Specification",
        "https://json-schema.org/specification",
        "standard_or_risk_framework",
        "JSON Schema",
        "high",
        86,
        "high",
        "stable",
        "JSON Schema provides a formal validation vocabulary and meta-schema foundation for validating structured JSON data.",
    ),
    "tfdv_anomalies": source(
        "src_tensorflow_data_validation_anomalies_2026",
        "TensorFlow Data Validation Anomalies Reference",
        "https://www.tensorflow.org/tfx/data_validation/anomalies",
        "official_doc",
        "TensorFlow",
        "high",
        84,
        "medium",
        "time_sensitive",
        "TensorFlow Data Validation documents schema and statistics based anomaly checks, including missing type, missing value, dataset-size, drift, and version comparator anomalies.",
    ),
    "openai_model_optimization": source(
        "src_openai_model_optimization_2026",
        "Model optimization | OpenAI API",
        "https://platform.openai.com/docs/guides/model-optimization",
        "official_doc",
        "OpenAI",
        "high",
        84,
        "medium",
        "time_sensitive",
        "OpenAI model optimization guidance supports task definition, choosing prompting/RAG/fine-tuning approaches, and evaluating quality before model changes.",
        ["OpenAI platform guidance changes over time; keep as supporting source, not the only source."],
    ),
}


PATCHES: dict[str, dict[str, Any]] = {
    "cand_20260609_ai_engineering_trade_data_strategy_id_and_version_required_v1_001.json": {
        "statement": "用于 LLM training、eval、RAG、preference data 或 gate/scoring review 的 trade data 必须包含 strategy_id、strategy_version_ref 和 strategy_owner_ref；这些字段只能引用 Trading Engineering 或外接项目的策略注册表，不得把策略逻辑、参数、K 线规则或执行规则写入 AI Engineering。缺失或无法解析时必须 block_training、exclude_from_eval 或标记 needs_more_evidence。",
        "evidence_summary": "MLflow Tracking 支持记录参数、代码版本、指标、输出文件、run metadata、artifacts 和数据集关联指标；DVC .dvc 文件支持用 Git 版本化数据占位元数据；Datasheets for Datasets 支持记录数据集组成、用途和限制。这些来源共同支撑 trade data 必须保存可追踪的策略版本引用，而不是保存策略本体。",
        "interpretation_notes": "本条只定义 AI Engineering 可保存的策略引用字段和缺失字段处理；策略本体、K 线逻辑、买卖条件、仓位、止损止盈、回测和执行规则必须归 Trading Engineering 或外接项目策略注册表管理。",
        "applies_when": [
            "交易记录、候选交易、复盘记录或打分样本将被转换为 LLM 训练、评估、RAG 检索、偏好数据或 gating/scoring 审核数据。",
            "样本、数据集或评估结果依赖具体策略版本、策略 owner、策略注册表或 release manifest 做解释和回溯。",
            "外接项目需要证明某个训练样本、eval case 或 gate 决策绑定到了明确策略版本。"
        ],
        "not_applicable_when": [
            "任务是在定义策略逻辑、K 线形态、入场出场条件、仓位公式、止损止盈或订单执行规则；这些内容应进入 Trading Engineering。",
            "样本完全不依赖策略版本，例如纯通用数据格式校验示例。",
            "用户试图把策略参数或私有交易规则正文写入 CEK-TA 通用 AI Engineering 知识库。"
        ],
        "limitations": [
            "本条仍是 needs_more_evidence 候选，等待二次审计确认字段命名、来源充分性和是否需要与 training_data.strategy_version_required 父子化。",
            "CEK-TA 当前只定义引用字段，不提供真实 strategy registry 实现。"
        ],
        "source_keys": ["mlflow_tracking", "dvc_files", "datasheets", "openai_model_optimization"],
        "source_quality": (86, 3, 1),
        "followup": "请重点审计 strategy_id/strategy_version_ref/strategy_owner_ref 是否应作为 trade_data 层字段，是否需要和 training_data.strategy_version_required 合并或父子化。",
    },
    "cand_20260609_ai_engineering_training_data_strategy_version_required_v1_001.json": {
        "statement": "每条 strategy-dependent training sample 必须携带 strategy_version_ref、strategy_registry_ref 或 lineage_manifest_id，并把 dataset_version、eval_run 和 release manifest 与该引用绑定；策略版本变化必须触发 dataset version 更新或 eval rerun。AI Engineering 只保存引用、hash、owner 和审计字段，不保存策略本体、阈值或执行规则。",
        "evidence_summary": "MLflow Tracking 支持 run、model、dataset、metrics 和 artifact 的关联追踪；DVC 支持数据占位元数据随 Git 版本化；Datasheets for Datasets 强调数据组成、用途和维护说明；scikit-learn 的 data leakage 指南强调建模时不能使用预测时不可得的信息。这些来源共同支撑 strategy-dependent training sample 必须有版本和 lineage 绑定。",
        "interpretation_notes": "本条是 training sample 层规则：样本依赖策略版本时必须可回溯；但策略版本的语义、策略本体和交易规则仍由 Trading Engineering 或外接项目注册表负责。",
        "applies_when": [
            "训练样本、评估样本、偏好样本或 gating/scoring 样本的 label、reason_code 或适用性依赖某个策略版本。",
            "外接项目准备训练、重训、评估或发布交易 LLM gate/scorer，并需要回溯 dataset_version、model_version 和 strategy_version 的绑定关系。",
            "策略版本、prompt、RAG 索引、数据集或模型其中任一项发生变化，需要判断是否重跑评估。"
        ],
        "not_applicable_when": [
            "样本用于纯通用 LLM 格式测试，不涉及策略依赖。",
            "任务是在定义具体策略规则、策略参数或交易执行行为；这些应路由到 Trading Engineering。",
            "策略版本引用会泄露私有策略逻辑或账户配置，必须只保留不可逆 hash 或外部 registry 引用。"
        ],
        "limitations": [
            "本条仍是 needs_more_evidence 候选，等待二次审计确认与 trade_data.strategy_id_and_version_required 的边界。",
            "需要外接项目提供真实 strategy registry 或 release manifest 契约后才能落地字段校验。"
        ],
        "source_keys": ["mlflow_tracking", "dvc_files", "datasheets", "sklearn_leakage"],
        "source_quality": (87, 4, 0),
        "followup": "请审计 strategy_version_ref 缺失时是否应统一 block_training、exclude_from_eval，还是部分通用样本允许降级为 needs_review。",
    },
    "cand_20260609_ai_engineering_training_example_input_target_separation_v1_001.json": {
        "statement": "训练样本必须把 input、prompt 或 decision-time features 与 target、completion、label、post-trade outcome 和 outcome_context 分离；label、future_return、fill result、exit result、人工复盘结论和事后交易结果不得出现在 input 或 RAG context 中。缺少 input_target_separation_check 时，不得进入 SFT、DPO、preference training 或 eval pool。",
        "evidence_summary": "scikit-learn 明确 data leakage 是使用预测时不可得信息并会导致过度乐观评估；TRL SFTTrainer 文档区分 prompt-completion 数据格式并支持 completion-only training；TFDV 文档说明可基于 schema 和统计检测数据异常；OpenAI Structured Outputs 和 JSON Schema 支持结构化字段约束与验证。这些来源共同支撑训练样本必须显式分离输入与目标字段并做 schema 检查。",
        "interpretation_notes": "本条只定义 training example 的字段角色和泄漏阻断规则；交易标签语义、PnL/outcome 解释和订单事实由 Trading Engineering 或项目 owner 提供。",
        "applies_when": [
            "交易记录、候选交易、复盘记录或标注记录被转换为 SFT example、preference pair、eval case 或 scoring/gating 训练样本。",
            "样本包含 prompt/messages/features、completion/assistant target、label、outcome_context 或 post-trade fields。",
            "外接项目需要检查 label、未来信息或事后结果是否泄漏到模型输入。"
        ],
        "not_applicable_when": [
            "任务只是保存原始完整交易日志，且该日志不会直接作为模型 input 或 RAG context。",
            "任务是在解释具体交易结果、K 线规则或订单执行事实；这些属于 Trading Engineering 或项目事实。",
            "completion 或 label 作为训练目标存在时，不应误判为泄漏；只有回流到 input/RAG context 才阻断。"
        ],
        "limitations": [
            "本条仍是 needs_more_evidence 候选，等待二次审计确认字段命名和 eval cases 是否充分。",
            "不同训练框架对 messages/prompt/completion 字段要求不同，正式知识需保留 vendor-neutral schema。"
        ],
        "source_keys": ["sklearn_leakage", "trl_sft", "tfdv_anomalies", "openai_structured_outputs", "json_schema"],
        "source_quality": (88, 5, 0),
        "followup": "请审计 input/target 字段分离是否覆盖 SFT、DPO、preference pair、eval case，并确认 completion-only 训练目标不会被误判为 input 泄漏。",
    },
    "cand_20260609_ai_engineering_training_example_sft_schema_required_v1_001.json": {
        "statement": "SFT example 必须使用版本化 schema，至少包含 sft_example_id、messages_or_prompt、completion_or_assistant_target、output_schema_id、schema_version、split_id、source_ids、field_role_check_id 和 schema_validation_report_id；schema validation 通过不等于可上线，仍需 held-out eval、RAG/prompt baseline、privacy/license check 和 leakage check。",
        "evidence_summary": "TRL SFTTrainer 文档支持 standard/conversational language modeling 与 prompt-completion 格式；OpenAI Structured Outputs 支持 JSON Schema 约束和类型安全解析；JSON Schema 提供 validation vocabulary 和 meta-schema；TFDV 文档说明 schema/statistics 可检测异常；OpenAI model optimization 支持先定义任务、评估质量再选择 fine-tuning。以上来源共同支撑 SFT example 需要版本化 schema、字段角色和验证报告。",
        "interpretation_notes": "本条定义 SFT example schema、schema validation、split 和 audit 字段；具体交易样本、策略语义、真值标签、订单和账户事实由 Trading Engineering 或 project owner 管理。",
        "applies_when": [
            "外接项目把交易审计、交易质量解释、gating/scoring reason code 或复盘任务构造成 SFT training example。",
            "样本使用 messages、prompt-completion、assistant target、结构化输出 target 或 schema-constrained target。",
            "训练集、验证集、测试集或 gold set 需要按 schema_version、split_id 和 source_ids 做审计。"
        ],
        "not_applicable_when": [
            "任务是在定义 DPO/preference pair 的 chosen/rejected 结构；该场景应使用 preference_pair schema。",
            "任务是在定义具体交易策略、买卖点、仓位、止损止盈或实盘订单执行规则。",
            "用户只需要运行时 structured output，不涉及 SFT 数据集构造；该场景应路由到 runtime output schema。"
        ],
        "limitations": [
            "本条仍是 needs_more_evidence 候选，等待二次审计确认与 sft.output_schema_consistency_required、sft.when_to_use_and_not_use 的父子关系。",
            "不同 SFT 框架对数据格式有差异，正式知识必须保留 vendor-neutral 字段和框架适配说明。"
        ],
        "source_keys": ["trl_sft", "openai_structured_outputs", "json_schema", "tfdv_anomalies", "openai_model_optimization"],
        "source_quality": (87, 5, 0),
        "followup": "请审计该 schema 是否足够支持 vendor-neutral SFT 样本、结构化输出目标、split 管理和 schema validation 报告。",
    },
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def update_candidate(path: Path, patch: dict[str, Any]) -> dict[str, Any]:
    candidate = load_json(path)
    candidate["status"]["review_status"] = "needs_more_evidence"
    candidate["status"]["ingestion_decision"] = "needs_more_evidence"
    candidate["status"]["decision_reason"] = (
        "已按第十批审计意见重写 statement 并补充直接来源，等待二次审计；该状态不是 accepted、reviewed 或 approved。"
    )
    candidate["status"]["updated_at"] = TODAY

    candidate["claim"]["statement"] = patch["statement"]
    candidate["claim"]["evidence_summary"] = patch["evidence_summary"]
    candidate["claim"]["interpretation_notes"] = patch["interpretation_notes"]
    candidate["claim"]["claim_strength"] = "medium"
    candidate["claim"]["performance_claim"] = False

    candidate["applicability"]["applies_when"] = patch["applies_when"]
    candidate["applicability"]["not_applicable_when"] = patch["not_applicable_when"]
    candidate["applicability"]["limitations"] = patch["limitations"]

    candidate["source_refs"] = [deepcopy(SOURCES[key]) for key in patch["source_keys"]]
    score, primary_count, supporting_count = patch["source_quality"]
    candidate["source_quality"] = {
        "overall_reliability": "high",
        "score": score,
        "score_version": "1.0.0",
        "primary_source_count": primary_count,
        "supporting_source_count": supporting_count,
        "low_reliability_source_count": 0,
        "mandatory_downgrades": [],
        "limitations": [
            "补证来源支持字段、lineage、schema、leakage 或 SFT 数据格式原则；二次审计前仍不得转 reviewed 或 approved。",
            "AI Engineering 只保存训练数据 schema、引用和审计规则；交易规则本体必须路由到 Trading Engineering。"
        ],
    }

    candidate["conflict_audit"]["conflict_status"] = "none"
    candidate["conflict_audit"]["resolution_summary"] = (
        "补证后未发现与当前 CEK-TA formal knowledge 的直接冲突；仍需二次审计确认是否与相邻规则合并或父子化。候选不会进入默认指导。"
    )
    candidate["conflict_audit"]["approval_allowed"] = False

    review = candidate.setdefault("review", {})
    review["confidence"] = "medium"
    review["freshness"] = "time_sensitive"
    review["reviewed_at"] = TODAY
    review["open_questions"] = [
        patch["followup"],
        "二次审计通过后只能进入 accepted_for_draft -> formal reviewed；不得直接进入 approved 或 machine_gate allow。"
    ]
    review["supplemental_research"] = {
        "package_id": PACKAGE_ID,
        "research_doc": "docs/research/phase36_batch10_strategy_training_example_supplemental_research.md",
        "summary": "已补 MLflow、DVC、Datasheets、scikit-learn data leakage、Hugging Face TRL SFTTrainer、OpenAI Structured Outputs、JSON Schema 与 TFDV 等直接来源，并重写元治理占位 statement。",
        "source_count": len(candidate["source_refs"]),
        "status_after_supplement": "needs_more_evidence",
    }
    audit_log = review.setdefault("audit_log", [])
    audit_log[:] = [
        entry for entry in audit_log
        if not (
            entry.get("action") == "phase36_batch10_supplemental_evidence_added"
            and entry.get("audit_package") == PACKAGE_ID
        )
    ]
    audit_log.append(
        {
            "at": TODAY,
            "actor": "codex",
            "action": "phase36_batch10_supplemental_evidence_added",
            "reason": "按第十批审计意见补直接来源、重写 statement、明确 AI Engineering 与 Trading Engineering 边界，导出二审包。",
            "audit_package": PACKAGE_ID,
        }
    )

    ai_audit = review.setdefault("ai_audit", {})
    ai_audit["decision"] = "needs_more_evidence"
    ai_audit["supplemental_package_id"] = PACKAGE_ID
    ai_audit["supplemental_status"] = "ready_for_second_audit"
    ai_audit["boundary"] = "accepted_for_draft 不是 approved；reviewed 不会进入默认指导。"

    candidate["workflow"] = {
        "stage": "needs_more_evidence",
        "queue_group": "needs_more_evidence",
        "formal_knowledge_id": None,
        "formal_review_status": None,
        "ai_audit_result_id": SOURCE_AUDIT_RESULT_ID,
        "hidden_from_default_queue": False,
        "next_action": "export_ai_audit",
    }

    write_json(path, candidate)
    return candidate


def write_research_doc(updated: list[dict[str, Any]]) -> None:
    rows = []
    for candidate in updated:
        source_titles = "；".join(source["source_title"] for source in candidate["source_refs"])
        rows.append(
            f"| `{candidate['candidate_id']}` | `{candidate['claim']['normalized_claim']}` | {len(candidate['source_refs'])} | {source_titles} |"
        )

    content = f"""# Phase 36 第十批 strategy/training example 补证采集记录

## 任务信息

```text
Phase: Phase 36 AI Engineering 交易 LLM Gating/Scoring 知识扩展
任务: CEK-TA-255 / CEK-TA-256
日期: {TODAY}
来源审计结果: {SOURCE_AUDIT_RESULT_ID}
二审包: {PACKAGE_ID}
```

## 上游输入

```text
docs/audit/audit_result_phase36_ai_engineering_batch_10_of_10_20260609_gpt55_pro_strict_sources.json
codex-expert-kit/rag/candidates/KB_AI_ENGINEERING/
docs/tasks/phase36_ai_engineering_gating_scoring_knowledge.md
docs/contracts/ai_engineering_gating_scoring_contract.md
```

## 下游输出

```text
4 条候选仍保留 needs_more_evidence 状态，等待二次审计。
docs/audit/phase36_batch10_strategy_training_example_supplemental_audit_package_20260609.json
ui/src/data/phase23Candidates.ts
```

## 边界

```text
本次只补证和导出二审包。
不创建 formal reviewed 知识。
不设置 approved。
不设置 machine_gate allow。
不把策略本体、K 线规则、买卖条件、仓位、止损止盈或订单执行规则写入 AI Engineering。
```

## 补证来源摘要

```text
MLflow Tracking: 支持参数、代码版本、指标、artifacts、run metadata、dataset-linked metrics 和模型/数据追踪。
DVC .dvc files: 支持用 Git 版本化数据占位元数据并跟踪数据目标。
Datasheets for Datasets: 支持数据集动机、组成、采集过程、推荐用途、维护和限制的透明记录。
scikit-learn common pitfalls: 支持 data leakage 风险和先 split 后 fit 的训练/测试隔离。
Hugging Face TRL SFTTrainer: 支持 standard/conversational、language modeling 和 prompt-completion SFT 数据格式。
OpenAI Structured Outputs + JSON Schema: 支持结构化输出 schema、字段说明、解析和验证。
TensorFlow Data Validation: 支持基于 schema 和统计的异常检测、缺失类型、缺失值、版本/漂移比较。
```

## 候选补证清单

| candidate_id | normalized_claim | 来源数 | 主要来源 |
| --- | --- | --- | --- |
{chr(10).join(rows)}

## 二次审计重点

```text
1. strategy_id / strategy_version_ref / strategy_owner_ref 是否应在 trade_data 层和 training_data 层分别保留，还是合并为父子规则。
2. training sample 的 strategy_version_ref 缺失时，是否统一 block_training / exclude_from_eval。
3. input / target / label / outcome_context 分离规则是否覆盖 SFT、DPO、preference pair 和 eval case。
4. SFT example schema 是否足够 vendor-neutral，并能支持 schema validation、split_id、source_ids 和 held-out eval。
5. 所有条目通过二审后也只能进入 accepted_for_draft -> formal reviewed，不得直接 approved。
```
"""
    RESEARCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESEARCH_PATH.write_text(content, encoding="utf-8", newline="\n")


def write_audit_package(updated: list[dict[str, Any]]) -> None:
    package = {
        "package_id": PACKAGE_ID,
        "package_type": "candidate_ai_audit_package",
        "created_at": TODAY,
        "created_by": "codex",
        "phase": "Phase 36",
        "task_ids": ["CEK-TA-255", "CEK-TA-256"],
        "source_audit_result_id": SOURCE_AUDIT_RESULT_ID,
        "source_package_id": SOURCE_PACKAGE_ID,
        "purpose": "第十批 4 条 needs_more_evidence 候选已补直接来源并重写 statement，请进行二次审计，判断是否 accepted_for_draft、仍需补证或 rejected。",
        "workflow_boundary": {
            "candidate_is_not_formal_knowledge": True,
            "accepted_for_draft_is_not_approved": True,
            "reviewed_is_not_approved": True,
            "do_not_set_machine_gate_allow": True,
            "do_not_promote_to_approved": True,
            "formalization_after_acceptance": "只有二审 accepted_for_draft 后，Codex 才能按 Phase 32 流程生成 formal reviewed 知识。"
        },
        "auditor_instructions": {
            "language": "zh-CN",
            "audit_focus": [
                "statement 是否已经从元治理占位句改成真实专业规则。",
                "source_refs 是否能直接支撑 claim。",
                "AI Engineering 与 Trading Engineering 边界是否清晰。",
                "是否存在字段重叠，需要合并或父子化。",
                "是否存在无来源、冲突、过宽泛、无法执行或会误导外接项目 AI 的表达。"
            ],
            "allowed_decisions": [
                "accepted_for_draft",
                "needs_more_evidence",
                "rejected"
            ],
            "required_output_schema": {
                "audit_result_id": "string",
                "auditor": "string",
                "audited_at": "YYYY-MM-DD",
                "source_package_id": PACKAGE_ID,
                "items": [
                    {
                        "candidate_id": "string",
                        "decision": "accepted_for_draft | needs_more_evidence | rejected",
                        "reason": "string",
                        "source_patch_notes": ["string"],
                        "content_patch_notes": ["string"],
                        "boundary_patch_notes": ["string"],
                        "conflict_patch_notes": ["string"],
                        "required_followups": ["string"]
                    }
                ],
                "global_notes": ["string"]
            }
        },
        "candidates": updated,
    }
    write_json(AUDIT_PACKAGE_PATH, package)


def main() -> None:
    updated: list[dict[str, Any]] = []
    for file_name, patch in PATCHES.items():
        updated.append(update_candidate(CANDIDATE_DIR / file_name, patch))
    write_research_doc(updated)
    write_audit_package(updated)
    print(
        json.dumps(
            {
                "updated_candidates": len(updated),
                "research_path": str(RESEARCH_PATH),
                "audit_package_path": str(AUDIT_PACKAGE_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
