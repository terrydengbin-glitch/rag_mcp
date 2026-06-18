# Phase 40 Drift Retraining Recalibration Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-301

## 目标

本文定义交易 AI gating/scoring 持续学习闭环中的漂移检测、再训练触发、再校准和阈值稳定性契约。

本契约承接：

```text
CEK-TA-300: FeedbackRecord、LabelUpdateRecord、DatasetVersionManifest、AuditTraceRecord
```

并向下游输出：

```text
CEK-TA-302: champion/challenger、shadow/paper/canary、release/rollback 契约
```

核心原则：

```text
漂移报警不是再训练命令。
再训练触发不是上线许可。
再训练后必须重新校准。
阈值变化必须有成本策略和人工审批。
任何触发都必须可回放、可解释、可阻断。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `FeedbackRecord` | CEK-TA-300 | 统计候选、阻断、执行、人工复核和错误分布 |
| `LabelUpdateRecord` | CEK-TA-300 | 监控标签分布、标签质量和人工修正变化 |
| `DatasetVersionManifest` | CEK-TA-300 | 明确训练、校准、评估、shadow 和 incident 数据版本 |
| `FeedbackQualityGateReport` | CEK-TA-300 | 防止低质量 feedback 进入 drift/retraining |
| `CalibrationReport` | Phase 38 / 本契约 | 监控概率可靠性和分组校准质量 |
| `ThresholdPolicyReport` | Phase 38 / 本契约 | 监控阈值策略、人工复核预算和 false allow/block 成本 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `DriftReport` | 再训练触发、人工审计、Vue3 审计摘要 |
| `RetrainingTriggerDecision` | 训练流水线、实验登记、人工审批 |
| `CandidateModelTrainingRequest` | 训练平台或外接项目模型训练任务 |
| `RecalibrationReport` | threshold policy、champion/challenger 对比 |
| `ThresholdStabilityReport` | final gate、release 审批、rollback 治理 |

## 漂移类型

Phase 40 至少区分以下漂移，不能混成一个“数据漂移”标签：

| 类型 | 说明 | 常见处理 |
| --- | --- | --- |
| `feature_drift` | 决策时特征分布变化 | 检查数据源、特征工程、市场 regime |
| `label_drift` | 标签分布、人工修正率、good loss/bad win 比例变化 | 检查标签策略和真实业务变化 |
| `score_distribution_drift` | scorer 分数分布变化 | 检查模型稳定性、输入分布、阈值压力 |
| `calibration_drift` | 预测概率和真实结果的可靠性变化 | 触发再校准或阻断 hard gate |
| `threshold_pressure_drift` | 阈值附近样本聚集、人工复核量超预算 | 检查阈值策略和 review capacity |
| `strategy_version_drift` | 策略版本或参数族变化 | 分策略版本切片评估 |
| `symbol_regime_drift` | 标的、周期、市场 regime 分布变化 | 检查泛化边界 |
| `execution_cost_drift` | 费用、滑点、延迟、成交质量变化 | 路由到 Trading Engineering 解释执行本体 |
| `rag_retrieval_drift` | RAG no-hit、低来源、冲突命中变化 | 路由到 RAG/知识库补齐 |
| `llm_output_drift` | LLM schema、reason code、citation、abstain 行为变化 | 优先 prompt/RAG 修复 |

## DriftReport 契约

最小字段：

```yaml
drift_report_id: string
schema_version: phase40_drift_report_v1
created_at: iso8601
scope:
  dataset_version_id: string
  feedback_record_count: integer
  label_update_count: integer
  time_range:
    start: iso8601
    end: iso8601
  baseline_window_ref: string
  current_window_ref: string

drift_checks:
  feature_drift:
    status: pass | warning | fail | not_applicable
    metrics: object
    affected_features: list[string]
  label_drift:
    status: pass | warning | fail | not_applicable
    metrics: object
    affected_labels: list[string]
  score_distribution_drift:
    status: pass | warning | fail | not_applicable
    metrics: object
  calibration_drift:
    status: pass | warning | fail | not_applicable
    metrics: object
  threshold_pressure_drift:
    status: pass | warning | fail | not_applicable
    metrics: object
  strategy_version_drift:
    status: pass | warning | fail | not_applicable
    affected_strategy_versions: list[string]
  symbol_regime_drift:
    status: pass | warning | fail | not_applicable
    affected_symbols: list[string]
    affected_regimes: list[string]
  execution_cost_drift:
    status: pass | warning | fail | not_applicable
    trading_engineering_refs: list[string]

decision:
  drift_status: none | potential | confirmed | insufficient_data
  severity: low | medium | high | critical
  recommended_action: monitor | investigate | recalibrate | retrain_candidate | freeze_release | rollback_review
  human_review_required: true | false
```

硬门：

```text
baseline_window_ref 缺失 -> needs_review
current_window_ref 缺失 -> needs_review
feature_schema_version 不一致且未解释 -> block_trigger
label_policy_version 不一致且未解释 -> block_trigger
只给总体 drift 分数、不分类型 -> needs_review
把 execution cost drift 解释为模型错误且无 Trading 引用 -> needs_review
```

## RetrainingTriggerDecision 契约

再训练触发必须是一个可审计决策，而不是脚本自动判断。

最小字段：

```yaml
retraining_trigger_decision_id: string
schema_version: phase40_retraining_trigger_v1
created_at: iso8601
trigger_type: scheduled | drift | sample_threshold | incident | manual | rejected
trigger_status: proposed | reviewed | approved_for_candidate_training | rejected | deferred

evidence_refs:
  drift_report_ids: list[string]
  feedback_quality_gate_report_ids: list[string]
  dataset_version_ids: list[string]
  incident_report_refs: list[string]

scope:
  target_model_role: numeric_scorer | llm_audit_assistant | calibrator | threshold_policy
  target_strategy_versions: list[string]
  target_symbols: list[string]
  target_market_regimes: list[string]
  time_range:
    start: iso8601
    end: iso8601

decision:
  action: no_action | collect_more_data | recalibrate_only | retrain_candidate_model | prompt_or_rag_update | human_review
  reason_codes: list[string]
  expected_outputs: list[string]
  reviewer: string | null
  approval_ref: string | null
```

禁止事项：

```text
trigger_status = approved_for_candidate_training 不等于可上线。
retrain_candidate_model 不得自动替换 champion。
incident 触发不得绕过数据质量和 lineage 检查。
LLM audit assistant 的失败优先走 prompt/RAG 更新，不能默认 SFT/LoRA。
```

阻断规则：

```text
missing drift_report and not scheduled/manual -> block_trigger
missing dataset_version_id -> block_trigger
feedback_quality_gate failed -> block_trigger
label_policy_version changed without migration note -> block_trigger
target_model_role missing -> block_trigger
approval_ref missing for live-impacting retraining -> needs_review
```

## CandidateModelTrainingRequest 契约

再训练触发通过后，只能生成候选模型训练请求。

最小字段：

```yaml
candidate_training_request_id: string
trigger_decision_id: string
created_at: iso8601
model_role: numeric_scorer | llm_audit_assistant | calibrator
training_dataset_version_id: string
validation_dataset_version_id: string
calibration_dataset_version_id: string | null
test_dataset_version_id: string
gold_set_id: string | null
feature_schema_version: string
label_policy_version: string
knowledge_index_version: string
expected_artifacts:
  candidate_model_manifest: true
  eval_report: true
  calibration_report: true | false
  threshold_stability_report: true | false
promotion_allowed: false
```

硬门：

```text
promotion_allowed 必须为 false。
缺少 test_dataset_version_id -> block_candidate_training
training/calibration/test 数据集重叠 -> block_candidate_training
缺少 feature_schema_version -> block_candidate_training
缺少 label_policy_version -> block_candidate_training
```

## RecalibrationReport 契约

每次再训练后必须重新校准；即使只更新数据或阈值，也必须确认校准是否仍然可用。

最小字段：

```yaml
recalibration_report_id: string
schema_version: phase40_recalibration_report_v1
created_at: iso8601
model_role: numeric_scorer | calibrator
candidate_model_manifest_ref: string | null
calibration_dataset_version_id: string
calibration_method: platt | isotonic | temperature | beta | none_with_reason

metrics:
  brier_score: number | null
  ece: number | null
  mce: number | null
  calibration_slope: number | null
  calibration_intercept: number | null

slices:
  by_strategy_version: object
  by_symbol: object
  by_market_regime: object
  by_risk_bucket: object

decision:
  calibration_status: pass | warning | fail | insufficient_data
  hard_gate_allowed: true | false
  caveats: list[string]
  required_followups: list[string]
```

硬门：

```text
no independent calibration dataset -> hard_gate_allowed=false
critical slice calibration fail -> hard_gate_allowed=false
calibration method changed without comparison -> needs_review
calibration_status insufficient_data -> hard_gate_allowed=false
```

## ThresholdStabilityReport 契约

阈值不是裸概率，不得因为模型分数变化自动移动。

最小字段：

```yaml
threshold_stability_report_id: string
schema_version: phase40_threshold_stability_v1
created_at: iso8601
threshold_policy_version: string
related_recalibration_report_id: string
cost_policy_ref: string
review_capacity_policy_ref: string

checks:
  false_allow_cost_change: low | medium | high | unknown
  false_block_cost_change: low | medium | high | unknown
  review_queue_pressure: low | medium | high | unknown
  threshold_near_boundary_volume: low | medium | high | unknown
  critical_slice_stability: pass | warning | fail | insufficient_data

decision:
  threshold_action: keep | adjust_candidate | human_review | block_hard_gate
  proposed_threshold_policy_version: string | null
  reason_codes: list[string]
  approval_required: true | false
```

硬门：

```text
threshold_action = adjust_candidate 且无 cost_policy_ref -> block_threshold_change
review_queue_pressure = high 且无人工复核预算说明 -> needs_review
critical_slice_stability = fail -> block_hard_gate
threshold fixed at 0.5 without cost policy -> block_hard_gate
```

## 触发决策流

```text
FeedbackRecord / LabelUpdateRecord / DatasetVersionManifest
  -> FeedbackQualityGateReport
  -> DriftReport
  -> RetrainingTriggerDecision
  -> CandidateModelTrainingRequest
  -> RecalibrationReport
  -> ThresholdStabilityReport
  -> Champion/Challenger Review
```

关键边界：

```text
DriftReport 可以建议 investigate/recalibrate/retrain，但不能训练。
RetrainingTriggerDecision 可以批准 candidate training，但不能上线。
CandidateModelTrainingRequest 可以训练 candidate model，但 promotion_allowed 必须为 false。
RecalibrationReport 可以证明概率可靠性，但不能直接改 final gate。
ThresholdStabilityReport 可以提出 candidate threshold，但必须进入 CEK-TA-302 的发布治理链路。
```

## 与 LLM 持续改进的分流

LLM audit assistant 的问题先分三类：

| 问题 | 优先处理 |
| --- | --- |
| no-hit、引用不足、知识缺口 | RAG 知识补齐和检索评测 |
| schema 不稳定、reason code 不稳定 | prompt 修正和 eval set 回归 |
| 长期稳定失败且 prompt/RAG 无法修复 | SFT/LoRA 候选任务，但必须先审计 |

禁止：

```text
把 LLM audit assistant 的输出漂移直接解释为交易信号漂移。
用 LLM 自评结果触发 SFT。
跳过 RAG/prompt 修复直接改模型权重。
```

## 与 Trading Engineering 的边界

以下漂移只在本契约中记录引用，不解释本体原因：

```text
fill model 变化
滑点、手续费、延迟变化
订单状态机变化
交易所异常
实盘仓位同步问题
风控阈值变化
```

这些必须路由到 Trading Engineering，由对应分支提供解释或修正知识。

## CEK-TA-301 DoD

```text
1. 本契约文件存在。
2. 已定义 DriftReport、RetrainingTriggerDecision、CandidateModelTrainingRequest、RecalibrationReport、ThresholdStabilityReport。
3. 已明确漂移报警不等于再训练命令。
4. 已明确再训练触发不等于上线许可。
5. 已明确再训练后必须重新校准。
6. 已明确阈值变化需要成本策略和审批。
7. 已写清 LLM prompt/RAG/SFT 分流和 Trading Engineering 边界。
8. UTF-8 无乱码。
```
