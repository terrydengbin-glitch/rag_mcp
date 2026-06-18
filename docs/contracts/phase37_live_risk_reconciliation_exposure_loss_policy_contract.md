# Phase 37 Live/Risk Reconciliation Exposure Loss Policy Contract

生成日期：2026-06-12

## 目标

本契约为 `CEK-TA-440` 服务，只补齐 Phase 37 Live Execution / Risk Management 三条候选的内部字段本体：

```text
P37-G-L03 live_execution.position_reconciliation_required
P37-G-L10 risk_management.portfolio_exposure_limit_required
P37-G-L11 risk_management.consecutive_loss_stop_required
```

本契约只允许支持候选进入 `formal reviewed/caveat_only` 再审，不允许创建 `approved`、`default guidance` 或可执行 `hard gate`。

## 硬边界

```text
1. 本契约不提供任何风险阈值数值。
2. 本契约不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
3. 本契约不直接触发拒单、停机、撤单、解锁或资金划转。
4. 本契约只定义字段、owner、状态和审计追踪。
5. 外接项目必须把自己的 broker、venue、account、strategy、instrument、risk_policy_id 和 execution system 映射到这些逻辑字段。
```

## Owner 边界

| Owner | 职责 |
| --- | --- |
| Live Execution | 真实 API/session 权限、订单状态、真实订单、真实成交、真实费用、broker/account position truth、适配器错误、执行日志 |
| Risk Management | deterministic pre-trade policy、风险限额、组合暴露、连续亏损停止、kill/stop policy、最终风险状态 |
| Data Engineering | reference data、instrument master、价格源、数据版本、lineage、stale/unknown 标记 |
| Market Microstructure | venue、session、calendar、contract、roll/expiry、liquidity regime 语义 |
| AI Engineering | 只能引用这些规则和 reason code，不拥有实盘真相、阈值或执行动作 |

## position_reconciliation

### 目的

定义本地状态与 broker、exchange、account statement 或 clearing source 的仓位对账字段。`reconciliation_required` 是证据/控制状态，不是交易建议或风险阈值。

### 必填字段

| 字段 | 类型 | Owner | 说明 |
| --- | --- | --- | --- |
| reconciliation_id | string | Live Execution | 对账记录唯一 ID |
| account_id_ref | string | Live Execution | 脱敏账户引用，不存真实密钥或敏感账户事实 |
| strategy_id | string | Risk Management | 策略或账户策略域引用 |
| instrument_id | string | Data/Market | 标准化合约或标的 ID |
| local_position_ref | string | Live Execution | 本地仓位快照引用 |
| broker_position_ref | string | Live Execution | broker/API 仓位快照引用 |
| account_statement_ref | string|null | Live Execution | statement / clearing / custodian 记录引用 |
| local_qty | decimal | Live Execution | 本地数量 |
| broker_qty | decimal | Live Execution | broker 数量 |
| local_notional | decimal|null | Live Execution | 本地名义金额 |
| broker_notional | decimal|null | Live Execution | broker 名义金额 |
| mismatch_qty | decimal | Live Execution | 数量差异 |
| mismatch_notional | decimal|null | Live Execution | 名义金额差异 |
| discrepancy_type | enum | Live Execution | 差异类型 |
| source_priority | array[string] | Live Execution | broker、statement、clearing、本地状态优先级 |
| local_snapshot_time | timestamp | Live Execution | 本地快照时间 |
| broker_snapshot_time | timestamp | Live Execution | broker 快照时间 |
| stale_source | array[string] | Live Execution/Data | stale 的来源 |
| unknown_source | array[string] | Live Execution/Data | 不可得来源 |
| reconciliation_status | enum | Live Execution | 对账状态 |
| reconciliation_action | enum | Live/Risk | 后续动作标签 |
| owner | enum | Live Execution | 主 owner |
| consumed_by_risk | boolean | Risk Management | 风控是否消费该状态 |
| audit_trace_id | string | Live/Risk | 审计链路 |
| created_at | timestamp | Live Execution | 生成时间 |

### 枚举

```text
discrepancy_type:
  none
  local_ahead
  broker_ahead
  missing_local_position
  missing_broker_position
  quantity_mismatch
  notional_mismatch
  stale_local
  stale_broker
  unknown

reconciliation_status:
  reconciled
  reconciliation_required
  unresolved
  stale_source
  missing_source

reconciliation_action:
  record_only
  require_manual_review
  block_new_orders_until_project_policy_resolves
  refresh_state
  escalate_to_owner
```

### 校验规则

```text
1. missing_source 不得静默当作仓位为 0。
2. reconciliation_required 只表示证据状态，不等于 CEK-TA 自动拒单或 hard gate。
3. Live Execution 拥有 broker/account position truth；Risk Management 可以消费 reconciliation_status，但不拥有 broker 真相。
4. 风控是否阻断新订单必须由外接项目 risk_policy_id 决定，本契约不提供阈值。
```

## portfolio_exposure_limit

### 目的

定义组合暴露的分类、价格源、聚合规则和审计字段。该对象描述“需要有暴露治理字段”，不提供任何暴露上限数值。

### 必填字段

| 字段 | 类型 | Owner | 说明 |
| --- | --- | --- | --- |
| exposure_check_id | string | Risk Management | 暴露检查 ID |
| risk_policy_id | string | Risk Management | 外接项目风控政策引用 |
| account_id_ref | string | Risk Management | 脱敏账户引用 |
| strategy_id | string | Risk Management | 策略引用 |
| instrument_id | string | Data/Market | 标准化品种 |
| venue | string | Market Microstructure | 交易场所 |
| asset_class | string | Data Engineering | 资产类别 |
| sector_or_theme | string|null | Data Engineering | 行业/主题 |
| direction | enum | Risk Management | long/short/net/flat/unknown |
| correlated_group_id | string|null | Risk/Data | 相关资产分组 |
| exposure_dimension | enum | Risk Management | 暴露维度 |
| gross_exposure | decimal|null | Risk Management | gross 暴露 |
| net_exposure | decimal|null | Risk Management | net 暴露 |
| directional_exposure | decimal|null | Risk Management | 方向暴露 |
| price_source_id | string | Data Engineering | 价格源 |
| price_timestamp | timestamp | Data Engineering | 价格时间 |
| price_staleness_status | enum | Data Engineering | 价格新鲜度 |
| aggregation_rule_id | string | Risk Management | 聚合规则 |
| exposure_status | enum | Risk Management | 暴露检查状态 |
| policy_threshold_ref | string | Risk Management | 阈值引用，只存 policy ref，不存推荐数值 |
| owner | enum | Risk Management | 主 owner |
| audit_trace_id | string | Risk Management | 审计链路 |
| created_at | timestamp | Risk Management | 生成时间 |

### 枚举

```text
exposure_dimension:
  account
  strategy
  instrument
  venue
  asset_class
  sector_or_theme
  correlated_group
  direction
  currency

price_staleness_status:
  fresh
  stale
  unknown
  missing

exposure_status:
  within_policy
  review_required
  unresolved
  policy_missing
  stale_price
  missing_reference_data
```

### 校验规则

```text
1. price_staleness_status=stale|unknown|missing 时不得静默通过为 within_policy。
2. QuantConnect 等平台示例只能作为 supporting source，不能替代 CEK-TA exposure taxonomy。
3. policy_threshold_ref 只引用外接项目政策，不存 CEK-TA 推荐阈值。
4. Market/Data owner 提供 instrument grouping、reference data、price source；Risk owner 负责暴露政策和聚合解释。
```

## consecutive_loss_stop_policy

### 目的

定义连续亏损停止规则的事件口径、窗口、重置、冻结、人工复核和解锁字段。该对象描述政策 schema，不提供连续亏损次数或亏损金额建议。

### 必填字段

| 字段 | 类型 | Owner | 说明 |
| --- | --- | --- | --- |
| loss_stop_policy_id | string | Risk Management | 连续亏损停止政策 ID |
| risk_policy_id | string | Risk Management | 外接项目风控政策引用 |
| account_id_ref | string | Risk Management | 脱敏账户引用 |
| strategy_id | string | Risk Management | 策略引用 |
| loss_event_basis | enum | Risk Management | 亏损事件口径 |
| loss_event_source | string | Risk/Live | 亏损事件来源 |
| time_window_policy_ref | string | Risk Management | 时间窗口政策引用，不存推荐窗口 |
| streak_count_source | string | Risk Management | 连续亏损计数来源 |
| reset_condition | enum | Risk Management | 重置条件 |
| freeze_action | enum | Risk/Live | 冻结动作标签 |
| manual_review_required | boolean | Risk Management | 是否需要人工复核 |
| unlock_process_ref | string | Risk Management | 解锁流程引用 |
| priority_order_ref | string | Risk Management | 与其他 gate 的优先级引用 |
| interaction_with_single_trade_risk | string | Risk Management | 与单笔风险关系 |
| interaction_with_daily_loss | string | Risk Management | 与日亏损关系 |
| interaction_with_portfolio_exposure | string | Risk Management | 与组合暴露关系 |
| policy_status | enum | Risk Management | 策略状态 |
| owner | enum | Risk Management | 主 owner |
| audit_trace_id | string | Risk Management | 审计链路 |
| created_at | timestamp | Risk Management | 生成时间 |

### 枚举

```text
loss_event_basis:
  realized_trade_pnl
  realized_r_multiple
  rule_violation_loss
  risk_adjusted_loss_event
  project_defined

reset_condition:
  next_session
  manual_reset
  project_policy_reset
  after_review
  unresolved

freeze_action:
  record_only
  require_manual_review
  freeze_new_entries_until_project_policy_resolves
  reduce_to_review_only
  escalate_to_owner

policy_status:
  configured
  policy_missing
  review_required
  unresolved
```

### 校验规则

```text
1. 连续亏损停止不能替代单笔风险、日亏损或组合暴露限制。
2. freeze_action 是政策状态标签，不等于 CEK-TA 直接执行停机或拒单。
3. time_window_policy_ref 和 priority_order_ref 只能引用外接项目政策，不写推荐数值。
4. 解锁必须经过 unlock_process_ref 或人工复核流程，不能由 AI scoring 自动解锁。
```

## 再审输出要求

外部审计返回结果时必须使用：

```text
accepted_for_reviewed_caveat_only
needs_more_evidence
rejected
blocked
```

不得返回：

```text
approved
default_guidance
hard_gate
risk_threshold_advice_allowed=true
```
