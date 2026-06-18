# Phase 40 Decision Cost Dashboard Metric Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-313

## 目标

本文定义交易 AI gating/scoring 持续学习闭环中的 decision cost、false allow/block、人审成本和看板指标契约。

本契约只定义 AI Engineering 的观测、审计和发布治理字段，不定义交易收益、K 线、fill model、滑点、手续费、仓位或实盘风控阈值本体。

核心原则：

```text
看板指标是观测信号，不是自动上线许可。
false allow/block 必须有成本口径和样本来源。
人审成本必须与 review queue 和人工审批容量绑定。
交易执行成本只能引用 Trading Engineering 或外接项目字段。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `FeedbackRecord` | `docs/contracts/phase40_feedback_dataset_contract.md` | 统计 allow/block/review/outcome 分布 |
| `DriftReport` | `docs/contracts/phase40_drift_retraining_recalibration_contract.md` | 提供 drift、score、calibration 和 threshold pressure 状态 |
| `ChampionChallengerReview` | `docs/contracts/phase40_champion_challenger_release_contract.md` | 比较 champion/challenger 的风险切片 |
| `TradingCostContextRef` | Trading Engineering 或外接项目 | 引用 fee/slippage/fill/spread/latency/cost 模型版本 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `DecisionCostMetricSet` | champion/challenger、发布审批、Vue3 审计摘要 |
| `ContinuousLearningDashboardSnapshot` | Vue3 知识审计、SearchLab、MCP |
| `HumanReviewCostMetric` | review queue、人工审批、release gate |

## DecisionCostMetricSet 契约

最小字段：

```yaml
decision_cost_metric_set_id: string
schema_version: phase40_decision_cost_metric_set_v1
created_at: iso8601
scope:
  model_role: numeric_scorer | llm_audit_assistant | calibrator | threshold_policy
  release_manifest_ref: string | null
  dataset_version_ref: string
  time_range:
    start: iso8601
    end: iso8601
  slice_keys:
    strategy_version_ref: string | null
    symbol_group: string | null
    market_regime_ref: string | null
    trading_cost_context_ref: string | null

counts:
  candidate_count: integer
  allow_count: integer
  block_count: integer
  human_review_count: integer
  abstain_count: integer

false_decision_metrics:
  false_allow_rate: number | null
  false_block_rate: number | null
  false_allow_cost: string | null
  false_block_cost: string | null
  tail_loss_proxy_ref: string | null
  drawdown_proxy_ref: string | null

calibration_metrics:
  brier_score: number | null
  ece: number | null
  reliability_diagram_ref: string | null

review_cost:
  review_queue_pressure: low | medium | high | unknown
  human_review_minutes: number | null
  review_capacity_policy_ref: string | null
```

硬门：

```text
缺少 dataset_version_ref -> block_metric_snapshot
false_allow_cost 或 false_block_cost 没有成本口径 -> needs_more_evidence
trading_cost_context_ref 缺失时不得解释 PnL、滑点、成交质量或实盘收益
review_queue_pressure=high 且无 review_capacity_policy_ref -> needs_review
指标看板不得自动触发 hard gate 或 release approval
```

## ContinuousLearningDashboardSnapshot 契约

最小字段：

```yaml
continuous_learning_dashboard_snapshot_id: string
schema_version: phase40_continuous_learning_dashboard_snapshot_v1
created_at: iso8601
scope_ref: string
panels:
  drift_panel_ref: string
  calibration_panel_ref: string
  decision_cost_metric_set_ref: string
  human_review_cost_metric_ref: string
  release_status_ref: string
  rollback_status_ref: string
status:
  observability_status: pass | warning | fail | insufficient_data
  recommended_action: monitor | investigate | collect_more_evidence | retraining_review | release_freeze | rollback_review
  human_review_required: true | false
```

## 与外部来源的关系

外部 MLOps/ML 监控来源可支撑 drift、calibration、performance、data quality 和 custom metrics；本契约把它们落到 CEK-TA 的交易 AI gating/scoring 场景。

专业来源只证明通用监控方法；交易成本、收益、drawdown、fill/slippage/latency 等语义必须引用 Trading Engineering 或外接项目事实。

## DoD

```text
1. 已定义 DecisionCostMetricSet。
2. 已定义 ContinuousLearningDashboardSnapshot。
3. 已明确 false allow/block、人审成本和 decision cost 的字段。
4. 已明确看板指标不是自动 hard gate。
5. 已明确 Trading Engineering 边界。
6. UTF-8 无乱码。
```
