# Phase 40 Review Budget Threshold Policy Contract

生成日期：2026-06-10
状态：contract draft
对应任务：CEK-TA-317

## 目标

本文定义交易 AI gating/scoring 持续学习闭环中的阈值策略、人审预算、队列容量和溢出处理契约。

本契约补充：

```text
docs/contracts/phase40_drift_retraining_recalibration_contract.md
docs/contracts/phase40_feedback_dataset_contract.md
```

核心原则：

```text
阈值不是裸概率。
阈值策略必须绑定成本矩阵、校准器版本、人审预算和 owner 审批。
人审预算不足不能被解释为自动 allow 或自动 block 的许可。
超预算只能进入降级、排队、冻结或人工审批链路。
```

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| `RecalibrationReport` | CEK-TA-301 | 确认概率校准是否可用于阈值判断 |
| `ThresholdStabilityReport` | CEK-TA-301 | 记录阈值压力、临界样本和关键切片稳定性 |
| `FinalGateDecision` | CEK-TA-300 | 记录 allow/block/human_review/skip 决策 |
| `HumanReviewRecord` | 外接项目 | 记录人工复核结果、时延和队列状态 |
| `CostMatrixPolicy` | 外接项目/风险治理 | 记录 false allow、false block、人审成本和机会成本 |

## 下游输出

| 输出 | 消费者 |
| --- | --- |
| `ReviewBudgetPolicy` | final gate、Vue3 审计、SearchLab |
| `ReviewQueueCapacitySnapshot` | 监控、threshold review、release review |
| `ThresholdPolicyReviewBudgetBinding` | MCP/SearchLab、外接项目 AI IDE |
| `ThresholdOverflowDecision` | 人工审批、降级策略、发布冻结 |

## ReviewBudgetPolicy 契约

最小字段：

```yaml
review_budget_policy_id: string
schema_version: phase40_review_budget_policy_v1
created_at: iso8601
policy_status: draft | reviewed | approved | frozen | retired

scope:
  strategy_versions: list[string]
  symbols: list[string]
  market_regimes: list[string]
  decision_roles: list[numeric_scorer | llm_audit_assistant | final_gate]

budget:
  max_reviews_per_hour: integer
  max_reviews_per_day: integer
  max_review_latency_seconds: integer
  min_reviewer_count: integer
  reviewer_skill_requirements: list[string]

cost_policy:
  cost_matrix_version: string
  false_allow_cost_ref: string
  false_block_cost_ref: string
  human_review_cost_ref: string
  opportunity_cost_ref: string | null

approval:
  owner: string
  approval_ref: string
  review_at: iso8601
```

硬门：

```text
缺少 cost_matrix_version -> block_threshold_policy
缺少 max_reviews_per_hour 或 max_reviews_per_day -> needs_review
缺少 owner 或 approval_ref -> block_threshold_policy
reviewer_skill_requirements 缺失且用于 live-impacting final gate -> needs_review
```

## ReviewQueueCapacitySnapshot 契约

最小字段：

```yaml
review_queue_capacity_snapshot_id: string
schema_version: phase40_review_queue_capacity_snapshot_v1
created_at: iso8601
review_budget_policy_ref: string

queue_state:
  pending_review_count: integer
  active_reviewer_count: integer
  estimated_wait_seconds_p50: integer | null
  estimated_wait_seconds_p95: integer | null
  queue_pressure: low | medium | high | saturated | unknown

slice_breakdown:
  by_strategy_version: object
  by_risk_bucket: object
  by_decision_reason_code: object

decision:
  capacity_status: pass | warning | saturated | unknown
  recommended_action: keep_threshold | collect_more_evidence | route_to_manual_owner | freeze_threshold_change | degrade_to_safe_mode
```

禁止：

```text
queue_pressure=high 或 saturated 时自动放宽 allow 阈值。
用“人审忙不过来”替代风险审批。
把 review capacity 当作交易 alpha 或收益指标。
```

## ThresholdPolicyReviewBudgetBinding 契约

最小字段：

```yaml
threshold_policy_review_budget_binding_id: string
schema_version: phase40_threshold_review_budget_binding_v1
created_at: iso8601

threshold_policy:
  threshold_policy_version: string
  calibrator_version: string
  score_model_version: string
  final_gate_policy_version: string

bindings:
  cost_matrix_version: string
  review_budget_policy_ref: string
  review_queue_capacity_snapshot_ref: string
  threshold_stability_report_ref: string
  owner_approval_ref: string

overflow_policy:
  on_budget_warning: keep_threshold | collect_more_evidence | raise_review_priority | owner_review
  on_budget_saturated: freeze_threshold_change | safe_mode | owner_review
  allow_auto_allow_on_overflow: false
  allow_auto_block_on_overflow: false
```

硬门：

```text
allow_auto_allow_on_overflow != false -> block_threshold_policy
allow_auto_block_on_overflow != false -> needs_review
缺少 review_budget_policy_ref -> block_threshold_policy
缺少 review_queue_capacity_snapshot_ref -> needs_review
缺少 owner_approval_ref -> block_threshold_policy
```

## ThresholdOverflowDecision 契约

最小字段：

```yaml
threshold_overflow_decision_id: string
schema_version: phase40_threshold_overflow_decision_v1
created_at: iso8601
triggering_snapshot_ref: string
related_threshold_policy_version: string
decision: freeze_threshold_change | safe_mode | collect_more_evidence | owner_review
reason_codes: list[string]
owner: string
approval_ref: string | null
```

## 与 MCP/SearchLab/Vue3 的关系

| 组件 | 使用方式 |
| --- | --- |
| MCP | 只读返回阈值、人审预算和溢出边界，不执行阈值变更 |
| SearchLab | 验证“人审预算不足能否自动 allow/block”等问题必须命中阻断规则 |
| Vue3 | 展示阈值策略、预算、队列压力、审批和 open gaps |

## 与 Trading Engineering 的边界

本契约不定义：

```text
交易信号有效性
仓位和杠杆
实盘风控阈值本体
fill model
滑点、手续费和交易所订单状态
```

这些只能作为 `cost_policy_ref`、`execution_cost_ref` 或外接项目事实引用。

## DoD

```text
1. 已定义 ReviewBudgetPolicy。
2. 已定义 ReviewQueueCapacitySnapshot。
3. 已定义 ThresholdPolicyReviewBudgetBinding。
4. 已定义 ThresholdOverflowDecision。
5. 已明确超预算不能自动 allow/block。
6. 已明确阈值策略必须绑定成本矩阵、校准器、人审预算和 owner 审批。
7. UTF-8 无乱码。
```
