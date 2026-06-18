# Phase 38 Training Data And Evaluation Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-268

## 目标

本文定义交易 gating/scoring POC 的训练数据、决策时特征、标签、校准集、评估集、shadow/paper/OPE 和发布前质量门禁契约。

核心原则：

```text
交易日志不能直接变成训练输入。
决策时可见信息和事后结果必须物理或逻辑隔离。
数值 scorer 数据集和 LLM audit 训练样本必须分开。
校准集、评估集、gold set 和 shadow pool 不得污染训练集。
```

## 数据链路

```text
Raw Trade Record
  -> Trade Candidate Snapshot
  -> Decision-Time Feature Frame
  -> Outcome / Post-Trade Record
  -> Labeling Record
  -> Numeric Scorer Dataset
  -> LLM Audit SFT Example / Preference Pair / Eval Case
  -> Calibration Set
  -> Offline Eval Set
  -> Shadow / Paper / Incident Pool
```

## 时间字段契约

每个样本必须显式保留：

```text
event_time: 市场或系统事件发生时间。
feature_available_time: 特征在真实系统中可被模型读取的时间。
decision_time: 外接项目做交易候选打分或门控建议的时间。
ingestion_time: 数据被写入训练/评估资产池的时间。
label_observation_end_time: 标签可被合法观察的最晚时间。
```

硬门：

```text
feature_available_time > decision_time -> block_sample
label_observation_end_time <= decision_time -> suspicious_label
outcome field exists in model input -> block_sample
human_review_outcome exists in scorer input -> block_sample
```

## Raw Trade Record

允许：

```text
完整交易生命周期记录
订单、成交、费用、滑点、退出、PnL、MFE/MAE、复盘结论
```

禁止：

```text
直接作为模型输入
直接作为 LLM prompt 原文
保存账户密钥、账号、客户标识或私有策略正文
```

## Trade Candidate Snapshot

必须包含：

```text
candidate_id
strategy_version_ref
source_mode: backtest | replay | paper | live | research
decision_time
market_context_ref
risk_context_ref
execution_context_ref
available_rule_refs
```

禁止包含：

```text
future_return
realized_pnl
exit_price
post_trade_review
MFE
MAE
final_outcome
```

## Decision-Time Feature Frame

每个特征必须包含：

```text
feature_name
feature_value
feature_timestamp
feature_available_time
source_object
lineage
feature_schema_version
```

质量门禁：

```text
字段名黑名单扫描
lineage post_trade 扫描
available_time 扫描
target-derived feature 扫描
训练服务一致性扫描
```

## Labeling Record

标签不能只看 PnL，必须至少支持：

```text
bad_trade_flag
good_loss_bad_win_category
rule_compliance_quality
risk_quality
execution_quality
setup_quality
market_regime_fit
label_reason_codes
label_source: rule | human | hybrid | postmortem
```

阻断规则：

```text
label based only on PnL -> block_label
blocked trade labeled as loss without counterfactual evidence -> block_label
missing label_reason_codes for supervised training -> needs_review
model output used as own label -> block_feedback_sample
```

## Numeric Scorer Dataset

输入：

```text
decision_time_features
strategy_version_ref
market_context_ref
risk_context_ref
execution_context_ref
allowed_trading_knowledge_refs
```

目标：

```text
bad_trade_flag
bad_trade_risk
quality_bucket
review_priority
false_allow_cost_bucket
false_block_cost_bucket
```

不允许：

```text
post_trade outcome
LLM natural-language explanation as numeric feature
future market movement
unreviewed private strategy text
```

## LLM Audit Dataset

LLM 审计助手训练样本必须和 numeric scorer 数据集分离。

SFT example：

```json
{
  "input": {
    "candidate_summary": {},
    "numeric_scorer_output": {},
    "retrieved_knowledge": [],
    "missing_fields": []
  },
  "target_output": {
    "schema_version": "llm_audit_v1",
    "recommendation": "needs_human_review",
    "reason_codes": [],
    "knowledge_refs": [],
    "unsupported_claims": []
  }
}
```

Preference pair：

```text
chosen/rejected 必须来自同一 prompt。
不能只按 PnL 选择 chosen。
必须解释 citation completeness、schema completeness、risk conservatism 和 unsupported claims。
```

## Split Manifest

必须包含：

```text
split_manifest_id
dataset_hash
train_split_id
calibration_split_id
validation_split_id
test_split_id
gold_set_id
shadow_pool_id
time_range
strategy_version_range
market_regime_range
embargo_policy
dedup_policy
```

阻断规则：

```text
calibration set overlaps scorer train set -> block_calibration
eval set overlaps train set -> block_eval
gold set used for training -> block_release
shadow pool used before frozen evaluation -> needs_review
```

## Calibration Contract

必须记录：

```text
calibrator_type: platt | isotonic | temperature | other
calibration_holdout_set_id
brier_score
reliability_diagram_ref
ece
mce
calibration_slope
calibration_intercept
strategy_regime_slices
```

硬门：

```text
no independent calibration holdout -> block_hard_gate_promotion
poor calibration in critical slice -> caveat_only or block_hard_gate_promotion
threshold fixed at 0.5 without cost policy -> block_hard_gate_promotion
```

## Threshold Policy

阈值必须来自成本策略，而不是裸概率。

最小字段：

```text
threshold_policy_version
false_allow_cost
false_block_cost
review_cost
risk_bucket_thresholds
strategy_scope
market_regime_scope
approval_owner
effective_from
rollback_target
```

## Evaluation Contract

离线评估：

```text
只能评估已执行交易上的 scorer 表现。
不能声称准确知道被阻断交易的真实收益。
```

Shadow 评估：

```text
只记录建议，不改变真实交易。
记录建议分布、延迟、人工复核命中率、no-hit、冲突命中和 citation completeness。
```

Paper / replay 评估：

```text
用于估计 false block opportunity 和 false allow cost。
必须声明 fill model、滑点、费用和延迟假设来自 Trading Engineering。
```

OPE：

```text
必须声明行为策略、目标策略、propensity 或其他反事实估计假设。
OPE 结果只能作为评估证据，不等于真实实盘收益承诺。
```

## Release Manifest

每次 POC 发布或 shadow 版本冻结必须生成：

```text
release_manifest_id
dataset_hash
feature_schema_version
split_manifest_hash
label_policy_version
model_code_hash
model_artifact_hash
calibrator_hash
threshold_policy_version
eval_report_hash
prompt_version
rag_index_version
llm_model_version
approval_record
rollback_target
kill_switch_policy
```

## Definition of Done

```text
1. 数据链路分层明确。
2. 决策时特征和事后结果隔离明确。
3. numeric scorer dataset 与 LLM audit dataset 分离明确。
4. split、calibration、threshold、eval、release 契约明确。
5. 硬门和阻断规则明确。
6. 中文 UTF-8 无乱码。
```
