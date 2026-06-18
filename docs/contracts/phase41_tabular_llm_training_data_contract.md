# Phase 41 表格模型与 Qwen3 审计助手训练数据契约

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-321

## 目标

本文定义外接交易 LLM gating/scoring 项目中，表格/统计模型、校准器、Qwen3 审计助手、阈值策略和模型 registry 之间的数据契约。

核心目标是保证：

```text
训练数据只使用决策时可见事实。
标签和事后结果与模型输入物理或逻辑隔离。
表格 scorer 训练样本、校准样本、Qwen3 审计样本和 final gate 策略样本分开治理。
每个模型、校准器、阈值策略、prompt、RAG index 和 release manifest 都能追溯到数据版本。
```

本文不定义交易策略，不采集 K 线、fill model、风控或执行规则本体，不引入数据库或外部训练平台。

## 上下游链条

| 环节 | 输入 | 输出 | 消费方 |
| --- | --- | --- | --- |
| Raw Trade Event | 交易项目原始事实 | 原始事件归档引用 | 数据清洗任务 |
| Trade Candidate Snapshot | 决策时候选事实 | 候选快照 | scorer / Qwen3 audit |
| Decision-Time Feature Frame | 决策前可见特征 | 表格特征帧 | tabular scorer |
| Outcome Record | 事后结果 | 标签观察依据 | label builder |
| Label Record | outcome + policy | 训练标签 | scorer / eval / calibration |
| Numeric Scorer Dataset | feature + label | 表格训练集 | Logistic Regression / LightGBM / XGBoost / CatBoost |
| Calibration Dataset | scorer output + label | 校准集 | calibrator |
| Qwen3 Audit Dataset | 快照 + RAG + 审计答案 | SFT/DPO/eval 样本 | Qwen3 audit assistant |
| Threshold Policy Dataset | 校准概率 + 成本矩阵 | 阈值策略版本 | final gate |
| Model Registry Record | 数据、模型、参数、指标 | 可追踪模型条目 | release manifest |

## 时间字段硬契约

每个样本必须保留：

```text
event_time: 市场或系统事件发生时间。
feature_timestamp: 特征对应事实的时间。
feature_available_time: 特征在真实系统中可被读取的时间。
decision_time: 候选交易被打分、审计或 gate 的时间。
label_observation_start_time: 标签观察窗口开始时间。
label_observation_end_time: 标签合法完成观察的时间。
ingestion_time: 数据进入训练/评估资产池的时间。
audit_time: 人工或 AI 审计发生时间。
```

硬门：

```text
feature_available_time > decision_time -> block_sample
label_observation_end_time <= decision_time -> suspicious_label
outcome 字段进入 scorer features -> block_sample
human_review_result 字段进入 scorer features -> block_sample
Qwen3 审计结论进入 scorer features -> block_sample
release 后才产生的字段进入训练输入 -> block_sample
```

## Trade Candidate Snapshot 契约

```json
{
  "schema_version": "trade_candidate_snapshot_v1",
  "candidate_id": "string",
  "project_adapter_id": "string",
  "source_mode": "research | backtest | replay | paper | live",
  "decision_time": "ISO-8601",
  "strategy_version_ref": "string",
  "market_context_ref": "string",
  "risk_context_ref": "string",
  "execution_context_ref": "string",
  "available_rule_refs": ["string"],
  "feature_schema_version": "string",
  "label_policy_version": "string",
  "sanitization_profile": "string"
}
```

禁止包含：

```text
realized_pnl
future_return
exit_price
MFE
MAE
post_trade_review
human_audit_result
final_gate_decision
account_id
api_key
私有策略源码
```

## Decision-Time Feature Frame 契约

```json
{
  "schema_version": "decision_time_feature_frame_v1",
  "candidate_id": "string",
  "decision_time": "ISO-8601",
  "feature_schema_version": "string",
  "features": [
    {
      "feature_name": "string",
      "feature_value": "number | string | boolean | null",
      "feature_type": "numeric | categorical | boolean | text_ref",
      "feature_timestamp": "ISO-8601",
      "feature_available_time": "ISO-8601",
      "source_object_ref": "string",
      "lineage_ref": "string",
      "missing_policy": "keep_null | impute_train_only | reject",
      "is_decision_time_safe": true
    }
  ],
  "forbidden_fields_scan": {
    "contains_post_trade_field": false,
    "contains_target_field": false,
    "contains_human_label": false,
    "contains_llm_audit_output": false
  }
}
```

质量门禁：

```text
任何 feature 缺少 feature_available_time -> block_sample
任何 feature 的 source_object_ref 缺失 -> needs_lineage_review
missing_policy 未声明 -> block_sample
contains_post_trade_field == true -> block_sample
contains_target_field == true -> block_sample
contains_llm_audit_output == true -> block_sample
```

## Label Record 契约

标签不是单一 PnL 字段，必须绑定标签策略版本。

```json
{
  "schema_version": "label_record_v1",
  "candidate_id": "string",
  "label_policy_version": "string",
  "label_observation_start_time": "ISO-8601",
  "label_observation_end_time": "ISO-8601",
  "primary_label": "good_trade | bad_trade | neutral | unknown",
  "secondary_labels": {
    "false_allow": false,
    "false_block": false,
    "risk_violation": false,
    "execution_cost_exceeded": false,
    "rule_compliance_failure": false,
    "data_quality_failure": false
  },
  "outcome_refs": ["string"],
  "human_review_ref": "string | null",
  "label_confidence": "low | medium | high",
  "label_notes": "string"
}
```

硬门：

```text
label_policy_version 缺失 -> block_dataset_build
label_observation_end_time 缺失 -> block_label
primary_label == unknown -> 可进入 eval/review pool，不进入 supervised training
human_review_ref 缺失但 label_confidence == high -> needs_label_audit
```

## Numeric Scorer Dataset 契约

```json
{
  "schema_version": "numeric_scorer_dataset_v1",
  "dataset_id": "string",
  "dataset_version": "string",
  "feature_schema_version": "string",
  "label_policy_version": "string",
  "time_split_policy": "walk_forward | expanding_window | rolling_window | blocked_time_split",
  "entity_group_policy": "strategy_symbol_timeframe_grouped | strategy_grouped | custom",
  "rows": [
    {
      "candidate_id": "string",
      "feature_frame_ref": "string",
      "label_record_ref": "string",
      "sample_weight": 1.0,
      "class_weight_policy_ref": "string",
      "split": "train | validation | calibration | holdout | shadow | paper | incident"
    }
  ],
  "dataset_hash": "string",
  "lineage_manifest_ref": "string"
}
```

分割规则：

```text
HPO 只能读取 train/validation。
calibration 只能读取独立 calibration。
最终评估只能读取 holdout/shadow/paper。
incident pool 只能做专项复盘，不能自动回灌训练。
同一 candidate_id 不得跨 split 重复。
同一交易事件族应按 entity_group_policy 保持在同一 split 或按时间切断。
```

### TrainingDatasetManifest 契约

`TrainingDatasetManifest` 是 Phase 41 表格 scorer 训练资产的最小可审计清单。它不保存交易明细，不保存 K 线、fill model、仓位或收益本体，只保存训练数据版本、切分、特征 schema、标签策略和来源血缘的可追踪引用。

```json
{
  "schema_version": "phase41_training_dataset_manifest_v1",
  "dataset_id": "string",
  "dataset_version": "string",
  "dataset_hash": "string",
  "split_manifest_hash": "string",
  "feature_schema_version": "string",
  "label_policy_version": "string",
  "lineage_manifest_ref": "string",
  "source_snapshot_refs": ["string"],
  "row_count_by_split": {
    "train": 0,
    "validation": 0,
    "calibration": 0,
    "holdout": 0,
    "shadow": 0,
    "paper": 0,
    "incident": 0
  },
  "time_range": {
    "min_decision_time": "ISO-8601",
    "max_decision_time": "ISO-8601",
    "max_label_observation_end_time": "ISO-8601"
  },
  "forbidden_fields_scan_ref": "string",
  "owner": "string",
  "created_at": "ISO-8601"
}
```

硬门：

```text
dataset_hash 缺失 -> reject_dataset_manifest
split_manifest_hash 缺失 -> reject_dataset_manifest
feature_schema_version 缺失 -> reject_dataset_manifest
label_policy_version 缺失 -> reject_dataset_manifest
lineage_manifest_ref 缺失 -> needs_lineage_review
forbidden_fields_scan_ref 缺失 -> needs_data_leakage_review
source_snapshot_refs 为空 -> reject_dataset_manifest
dataset_hash 与实际导出文件不一致 -> reject_training_run
同一模型比较使用不同 TrainingDatasetManifest -> reject_model_comparison
```

审计说明：

```text
1. dataset_hash 用于确认训练数据内容没有被静默替换。
2. split_manifest_hash 用于确认 train/validation/calibration/holdout/shadow/paper/incident 池没有被模型选择或 HPO 偷看。
3. feature_schema_version 用于确认离线训练特征和线上决策特征的字段、类型、缺失策略一致。
4. label_policy_version 用于确认 bad_trade、false_allow、false_block 等标签口径没有被 PnL 单字段或事后解释污染。
5. TrainingDatasetManifest 只能作为 AI Engineering 的训练资产治理契约，不定义交易收益、fill、滑点、手续费、仓位或风控本体。
```

### Split Manifest 契约

同一轮模型比较必须使用同一个 split manifest 和 metric set，不能让模型家族各自选择有利切分。

```json
{
  "schema_version": "phase41_split_manifest_v1",
  "split_manifest_hash": "string",
  "split_policy": "walk_forward | expanding_window | rolling_window | blocked_time_split",
  "train_window": "string",
  "validation_window": "string",
  "calibration_window": "string",
  "holdout_window": "string",
  "entity_group_policy": "string",
  "metric_set_version": "string",
  "label_policy_version": "string",
  "forbidden_pool_access": ["holdout", "calibration", "shadow", "paper", "incident"]
}
```

硬门：

```text
split_manifest_hash 缺失 -> reject_training_run
模型比较使用不同 split_manifest_hash -> reject_model_comparison
metric_set_version 缺失 -> reject_model_comparison
HPO 读取 forbidden_pool_access 中任一数据池 -> reject_training_run
```

### Baseline Model Card 契约

Logistic Regression baseline 必须作为透明性和校准对照，不允许被描述为稳定收益最优模型。

```json
{
  "schema_version": "phase41_baseline_model_card_v1",
  "model_family": "logistic_regression",
  "coefficients_available": true,
  "calibration_baseline": true,
  "linear_boundary_limitations": ["string"],
  "feature_scaling_policy_ref": "string",
  "class_weight_policy_ref": "string",
  "comparison_split_manifest_hash": "string"
}
```

硬门：

```text
coefficients_available == false -> baseline_explainability_degraded
comparison_split_manifest_hash 缺失 -> reject_model_comparison
baseline 被描述为 best_performance_claim -> reject_claim
```

## 模型家族训练契约

每个模型训练任务必须声明：

```json
{
  "schema_version": "tabular_model_training_run_v1",
  "training_run_id": "string",
  "model_family": "rule_baseline | logistic_regression | lightgbm | xgboost | catboost",
  "dataset_version": "string",
  "training_code_version": "string",
  "hyperparameter_search_space_ref": "string",
  "hpo_policy": {
    "uses_test_or_holdout": false,
    "max_trials": 0,
    "selection_metric": "string",
    "early_stopping_policy": "string"
  },
  "class_imbalance_policy": {
    "sample_weight_enabled": true,
    "class_weight_enabled": true,
    "false_allow_cost_weight": 1.0,
    "false_block_cost_weight": 1.0
  },
  "training_output_ref": "string"
}
```

硬门：

```text
uses_test_or_holdout == true -> reject_training_run
model_family 缺少 rule_baseline 对照 -> needs_baseline
class_imbalance_policy 缺失 -> needs_training_audit
training_code_version 缺失 -> reject_registry
```

### Class Weight / Sample Weight 后校准报告

少数类、false_allow 或 bad_trade 加权后，必须重新检查概率校准，不能沿用旧校准结论。

```json
{
  "schema_version": "phase41_recalibration_after_weighting_report_v1",
  "training_run_id": "string",
  "class_weight_policy_ref": "string",
  "sample_weight_policy_ref": "string",
  "calibration_dataset_version": "string",
  "calibration_report_id": "string",
  "brier_score_ref": "string",
  "ece_ref": "string",
  "calibration_curve_ref": "string",
  "calibration_changed_after_weighting": true
}
```

硬门：

```text
class_weight_policy_ref 或 sample_weight_policy_ref 变更后缺少 calibration_report_id -> block_model_promotion
calibration_dataset_version 与训练集相同 -> reject_calibration
brier_score_ref/ece_ref/calibration_curve_ref 全部缺失 -> needs_calibration_audit
```

### FeatureLineageRecord 契约

每个上线可用特征必须有来源、版本、缺失策略和废弃策略。`FeatureLineageRecord` 是 Phase 41 的最小可审计特征血缘记录；它只证明特征在决策时可见、来源可追踪、schema 可复现，不证明特征具有因果交易价值。

```json
{
  "schema_version": "phase41_feature_lineage_record_v1",
  "feature_id": "string",
  "feature_name": "string",
  "source_object_ref": "string",
  "lineage_ref": "string",
  "feature_schema_version": "string",
  "missing_value_policy": "keep_null | impute_train_only | reject",
  "feature_timestamp_field": "string",
  "feature_available_time_policy": "string",
  "online_offline_parity_check_ref": "string",
  "owner": "string",
  "deprecation_policy": "string",
  "created_at": "ISO-8601"
}
```

硬门：

```text
feature_id 缺失 -> block_feature
source_object_ref 缺失 -> block_feature
lineage_ref 缺失 -> block_feature
feature_schema_version 缺失 -> block_feature
missing_value_policy 缺失 -> block_feature
feature_available_time_policy 缺失 -> needs_time_safety_review
online_offline_parity_check_ref 缺失 -> needs_parity_review
owner 缺失 -> needs_feature_owner_review
deprecation_policy 缺失 -> needs_feature_lifecycle_review
missing_value_policy == impute_train_only 且无训练期 imputation artifact -> block_feature
FeatureLineageRecord 缺失时，该 feature 不得进入 paper/live scorer。
```

审计说明：

```text
1. source_object_ref 指向原始事实对象或清洗后事实对象的稳定引用。
2. lineage_ref 指向生成该特征的 pipeline、代码版本、参数版本或数据处理记录。
3. feature_schema_version 对齐 Decision-Time Feature Frame 和 TrainingDatasetManifest。
4. missing_value_policy 必须说明缺失值是保留、只用训练集拟合填充器，还是直接拒绝样本。
5. owner 和 deprecation_policy 用于防止无人维护特征长期留在 scorer 输入中。
6. FeatureLineageRecord 不替代 Trading Engineering 的 K 线结构、fill model、风控或执行规则。
```

## Calibration Dataset 契约

```json
{
  "schema_version": "calibration_dataset_v1",
  "calibration_dataset_version": "string",
  "source_dataset_version": "string",
  "scorer_version": "string",
  "label_policy_version": "string",
  "rows": [
    {
      "candidate_id": "string",
      "raw_score_ref": "string",
      "label_record_ref": "string",
      "regime_key": {
        "market_regime": "string",
        "strategy_family": "string",
        "timeframe": "string"
      }
    }
  ],
  "calibration_split_policy": "independent_holdout | rolling_forward",
  "dataset_hash": "string"
}
```

禁止：

```text
使用训练集直接校准。
使用未来窗口更新当前窗口校准器。
把未校准 raw_score 声明为概率。
```

## Calibrator Registry 契约

```json
{
  "schema_version": "calibrator_registry_record_v1",
  "calibrator_version": "string",
  "scorer_version": "string",
  "calibration_dataset_version": "string",
  "calibration_method": "platt | isotonic | beta | none",
  "target": "bad_trade | false_allow | expected_quality | custom",
  "metrics": {
    "brier_score": 0.0,
    "ece": 0.0,
    "sample_count": 0,
    "regime_coverage": "string"
  },
  "approval_status": "draft | reviewed | approved | deprecated",
  "artifact_hash": "string"
}
```

## Threshold Policy 契约

阈值策略不是模型参数，必须单独版本化。

```json
{
  "schema_version": "threshold_policy_v1",
  "threshold_policy_version": "string",
  "calibrator_version": "string",
  "risk_policy_version": "string",
  "business_cost_matrix_ref": "string",
  "rules": [
    {
      "risk_bucket": "low | medium | high | critical",
      "uncertainty_bucket": "low | medium | high | unknown",
      "action": "allow | needs_human_review | block | skip",
      "max_position_permission": "none | capped | project_policy_default",
      "requires_human_approval": false
    }
  ],
  "false_allow_budget": "string",
  "false_block_budget": "string",
  "review_capacity_budget": "string",
  "approval_status": "draft | reviewed | approved | deprecated"
}
```

硬门：

```text
threshold_policy_version 缺失 -> final_gate_block
business_cost_matrix_ref 缺失 -> threshold_policy_review_required
uncertainty_bucket == unknown 且 action == allow -> reject_policy
approval_status != approved 且 mode 为 paper/live -> final_gate_block
```

## Qwen3 Audit Dataset 契约

Qwen3 审计助手训练样本必须与 numeric scorer 数据集分离。

```json
{
  "schema_version": "qwen3_audit_dataset_v1",
  "dataset_id": "string",
  "dataset_version": "string",
  "task_type": "missing_field_check | reason_code | citation_audit | unsupported_claim_detection | review_summary",
  "input_refs": {
    "trade_candidate_snapshot_ref": "string",
    "scorer_output_ref": "string",
    "calibrator_output_ref": "string",
    "rag_citation_response_ref": "string"
  },
  "target_output_schema_version": "qwen3_audit_output_v1",
  "target_output_ref": "string",
  "split": "sft_train | sft_validation | preference_train | eval | gold | incident",
  "data_sanitization_profile": "string",
  "private_data_removed": true
}
```

硬门：

```text
target_output_ref 缺失 -> block_sft_sample
rag_citation_response_ref 缺失 -> citation_task_must_abstain
private_data_removed != true -> block_export
split == eval 或 gold 的样本不得进入 sft_train。
Qwen3 样本不得包含账户密钥、客户标识或私有策略正文。
```

## Preference Pair / DPO 契约

```json
{
  "schema_version": "qwen3_preference_pair_v1",
  "pair_id": "string",
  "input_ref": "string",
  "chosen_output_ref": "string",
  "rejected_output_ref": "string",
  "preference_reason": "better_citation | better_schema | safer_abstain | better_reason_code | fewer_unsupported_claims",
  "reviewer_ref": "human | ai_assisted",
  "quality_gate": {
    "chosen_has_valid_json": true,
    "chosen_has_supported_citations": true,
    "rejected_failure_mode": "string"
  }
}
```

禁止：

```text
用 PnL 高低直接构造 Qwen3 preference。
用无来源输出作为 chosen。
让 DPO 学习绕过 final gate。
```

## Model Registry 契约

```json
{
  "schema_version": "model_registry_record_v1",
  "model_version": "string",
  "model_role": "rule_baseline | tabular_scorer | calibrator | qwen3_audit_assistant | final_gate_policy",
  "model_family": "rule_baseline | logistic_regression | lightgbm | xgboost | catboost | qwen3 | deterministic_policy",
  "training_run_id": "string",
  "dataset_version": "string",
  "feature_schema_version": "string",
  "label_policy_version": "string",
  "calibration_dataset_version": "string | null",
  "prompt_version": "string | null",
  "rag_index_version": "string | null",
  "reason_taxonomy_version": "string | null",
  "metrics_report_ref": "string",
  "model_card_ref": "string",
  "artifact_hash": "string",
  "approval_status": "draft | reviewed | approved | deprecated",
  "created_at": "ISO-8601"
}
```

硬门：

```text
artifact_hash 缺失 -> reject_registry
metrics_report_ref 缺失 -> reject_registry
model_card_ref 缺失 -> needs_model_card
approval_status != approved -> 不能进入 paper/live release manifest
qwen3_audit_assistant 缺少 prompt_version 或 reason_taxonomy_version -> reject_registry
tabular_scorer 缺少 dataset_version 或 feature_schema_version -> reject_registry
```

## Release Manifest 数据绑定契约

```json
{
  "schema_version": "hybrid_scoring_release_manifest_v1",
  "release_manifest_version": "string",
  "scorer_version": "string",
  "calibrator_version": "string",
  "threshold_policy_version": "string",
  "qwen_model_version": "string",
  "prompt_version": "string",
  "rag_index_version": "string",
  "reason_taxonomy_version": "string",
  "risk_policy_version": "string",
  "rollback_target_manifest_version": "string",
  "kill_switch_policy_ref": "string",
  "approval_ref": "string",
  "artifact_hashes": []
}
```

硬门：

```text
release_manifest_version 缺失 -> paper/live final_gate_block
rollback_target_manifest_version 缺失 -> reject_release
kill_switch_policy_ref 缺失 -> reject_release
任一 artifact_hash 缺失 -> reject_release
approval_ref 缺失 -> reject_release
```

## 存储边界

```text
1. 本 Phase 只定义文件化契约，不引入数据库。
2. 外接项目可以把上述对象映射到本地文件、对象存储、MLflow、Feast 或数据库，但 CEK-TA 不要求运行时依赖。
3. CEK-TA 正式知识仍使用 JSON knowledge item 和 knowledge_items.json 聚合索引。
4. 任何真实平台接入必须另起实现 Phase 并由开发者确认。
```

## 与 Phase 41 运行时契约的字段对齐

| 本契约字段 | Phase 41 runtime 字段 |
| --- | --- |
| `feature_schema_version` | `feature_schema_version` |
| `label_policy_version` | `label_policy_version` |
| `dataset_version` | `dataset_version` / `lineage_manifest_ref` |
| `scorer_version` | `scorer_version` |
| `calibrator_version` | `calibrator_version` |
| `calibration_dataset_version` | `calibration_dataset_version` |
| `threshold_policy_version` | `threshold_policy_version` |
| `qwen_model_version` | `qwen_model_version` |
| `prompt_version` | `prompt_version` |
| `rag_index_version` | `rag_index_version` |
| `reason_taxonomy_version` | `reason_taxonomy_version` |
| `release_manifest_version` | `release_manifest_version` |

## Definition of Done

```text
1. 明确 raw trade event、candidate snapshot、feature frame、label record、numeric scorer dataset、calibration dataset、Qwen3 audit dataset、threshold policy、model registry 和 release manifest。
2. 明确 point-in-time feature、label observation window、训练/校准/评估隔离和 HPO 防泄漏。
3. 明确 Qwen3 audit dataset 与 numeric scorer dataset 分离。
4. 明确 model registry 和 release manifest 必须绑定数据版本、模型版本、prompt、RAG index 和 artifact hash。
5. 不引入数据库、不部署训练平台、不改变 Phase 41 runtime 权限。
6. 文档以 UTF-8 保存，无乱码。
```
