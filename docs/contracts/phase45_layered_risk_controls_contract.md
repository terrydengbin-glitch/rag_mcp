# Phase 45 Layered Risk / Credit / Margin Contract

## 目标

本契约定义 P45-C Layered Risk / Credit / Margin 候选进入 `formal reviewed/caveat_only` 前必须具备的内部字段边界。

本契约只服务知识审计和外接项目设计提醒，不输出任何风险阈值、信用额度、保证金比例、资金充足性结论、下单许可或实盘执行建议。

## Owner 边界

| 领域 | Owner | 只读引用方 | 禁止越界 |
| --- | --- | --- | --- |
| pre-trade controls taxonomy | Risk Management | Live Execution、AI Engineering | 不得由 AI Engineering 启用 hard gate |
| credit / capital / clearing exposure | Risk Management、Broker/Clearing Adapter | Strategy Engineering、Trade Analysis | 不得混同策略亏损阈值 |
| order size / price collar / fat-finger | Risk Management、Live Execution | Strategy Engineering | 不得被策略信号强度绕过 |
| message throttle / cancel-rate | Live Execution、Risk Management | Market Microstructure、Audit Trail | 不得解释为 alpha 或 PnL 风险 |
| margin / collateral / available funds | Risk Management、Broker/Venue Adapter | AI Engineering、Trade Analysis | 不得默认为可交易现金 |
| post-trade surveillance | Trade Analysis、Risk Management | Live Execution、Compliance/Audit | 不得替代 pre-trade controls |

## 分层风控字段契约

`layered_pre_trade_control` 至少包含：

```json
{
  "control_id": "string",
  "control_layer": "order | account | strategy | instrument | venue | credit | margin | system",
  "owner": "risk_management | live_execution | broker_adapter | venue_adapter | clearing_adapter",
  "control_purpose": "financial_exposure | erroneous_order | market_integrity | message_pressure | operational_safety",
  "evidence_source_id": "string",
  "policy_version": "string",
  "effective_time": "datetime",
  "observed_time": "datetime",
  "decision_time": "datetime",
  "result": "pass | fail | review_required | unavailable | stale | unknown",
  "action_semantics": "evidence_only | review_required | external_project_gate",
  "exception_policy_id": "string | null",
  "audit_trace_id": "string"
}
```

硬规则：

```text
1. 单一 allow/block 布尔值不得替代分层 control、owner、证据和例外流程。
2. `external_project_gate` 只能由外接项目自己的 Risk/Live owner 启用，CEK-TA 知识项不得默认启用。
3. `unavailable`、`stale`、`unknown` 不得静默当作 pass。
```

## Credit / Capital / Exposure 字段契约

`credit_exposure_boundary` 至少包含：

```json
{
  "credit_scope": "broker | clearing_member | account | product_group | venue | strategy_budget",
  "limit_owner": "broker | clearing | risk_management | strategy_owner",
  "exposure_measure_id": "string",
  "account_id_ref": "string",
  "product_group_ref": "string | null",
  "policy_version": "string",
  "source_system": "string",
  "source_timestamp": "datetime",
  "snapshot_id": "string",
  "staleness_status": "fresh | stale | unknown",
  "unit": "currency | contract | notional | risk_unit",
  "semantic_boundary": "credit_limit | strategy_loss_limit | capital_budget | clearing_exposure",
  "audit_trace_id": "string"
}
```

硬规则：

```text
1. credit limit 不等于 strategy loss limit。
2. clearing / broker / venue 字段不得被泛化成所有市场通用字段。
3. 本契约不定义任何具体额度数值。
```

## Order Size / Price Collar 字段契约

`order_admission_control` 至少包含：

```json
{
  "order_control_id": "string",
  "control_type": "max_order_size | price_collar | price_band | fat_finger | duplicate_order | self_match",
  "venue": "string",
  "instrument_id": "string",
  "product_group": "string | null",
  "control_version": "string",
  "market_state_ref": "string",
  "input_order_id": "string",
  "observed_at": "datetime",
  "result": "pass | fail | review_required | unavailable | stale",
  "source_document_ref": "string",
  "audit_trace_id": "string"
}
```

硬规则：

```text
1. 策略信号强度不得绕过 order admission control。
2. price band / collar 来源必须注明 venue、product 和版本。
3. 本契约不输出 price band、max order size 或 fat-finger 阈值。
```

## Message Throttle / Cancel Rate 字段契约

`message_pressure_control` 至少包含：

```json
{
  "message_control_id": "string",
  "venue": "string",
  "session_id": "string",
  "connection_id": "string",
  "message_type": "new | replace | cancel | quote | mass_cancel | heartbeat",
  "control_type": "message_rate | cancel_rate | burst | volume_ratio | duplicate_message",
  "window_policy_id": "string",
  "measurement_source": "gateway | venue_report | internal_order_router",
  "observed_at": "datetime",
  "result": "pass | fail | review_required | unavailable | stale",
  "recovery_policy_ref": "string",
  "audit_trace_id": "string"
}
```

硬规则：

```text
1. message pressure 是系统/venue risk，不是成交风险、PnL 风险或策略 alpha。
2. CME、broker 或交易所文档只支撑其自身 venue 语义，不定义 CEK-TA 通用阈值。
3. 超限动作必须由外接项目运行时契约定义。
```

## Point-in-time Account / Margin / Collateral Evidence

`account_margin_collateral_evidence` 至少包含：

```json
{
  "evidence_id": "string",
  "account_ref": "string",
  "broker_or_venue": "string",
  "product_scope": "equity | futures | crypto_futures | fx | options | multi_asset",
  "account_mode": "cash | margin | portfolio_margin | cross_margin | isolated_margin | multi_assets",
  "field_name": "available_funds | buying_power | excess_liquidity | wallet_balance | available_balance | margin_balance | collateral | performance_bond | initial_margin | maintenance_margin",
  "field_value_ref": "numeric_reference_or_hash",
  "currency_or_asset": "string",
  "source_endpoint_or_report": "string",
  "source_timestamp": "datetime",
  "receive_timestamp": "datetime",
  "decision_timestamp": "datetime",
  "snapshot_id": "string",
  "schema_version": "string",
  "staleness_status": "fresh | stale | unknown",
  "semantic_boundary": "clearing_margin | broker_available_funds | broker_buying_power | crypto_available_balance | collateral | strategy_budget",
  "owner": "risk_management | broker_adapter | venue_adapter | clearing_adapter",
  "audit_trace_id": "string"
}
```

硬规则：

```text
1. `available_funds`、`buying_power`、`excess_liquidity`、`wallet_balance`、`available_balance`、`margin_balance`、`collateral` 和 `performance_bond` 不得互相等同。
2. 任一账户字段都不能被默认解释为可交易现金。
3. 资金充足性 claim 必须引用 point-in-time 证据、broker/venue/account-mode 语义、数据时间和 owner。
4. 缺失、过期或语义未知的 account/margin/collateral 证据不得静默视为资金充足。
5. 本契约不输出保证金比例、信用额度、可用资金判断或下单许可。
```

## Post-trade Surveillance 字段契约

`post_trade_surveillance_event` 至少包含：

```json
{
  "surveillance_event_id": "string",
  "source_event_id": "string",
  "event_type": "execution_review | exception_review | compliance_review | anomaly_review | risk_review",
  "detected_at": "datetime",
  "related_order_ids": ["string"],
  "related_fill_ids": ["string"],
  "classification": "informational | review_required | incident_candidate | policy_violation_candidate",
  "owner": "trade_analysis | risk_management | compliance_audit | live_execution",
  "pre_trade_control_refs": ["string"],
  "finding_summary": "string",
  "recommended_followup": "string",
  "audit_trace_id": "string"
}
```

硬规则：

```text
1. post-trade surveillance 只能发现、解释和复盘已发生事件。
2. 它不能替代 pre-trade controls。
3. 如果外接项目需要拒单、停机、撤单或解锁，必须由 Risk Management / Live Execution owner 另行定义 deterministic gate。
```

## Reviewed/Caveat-only 机器门控

若 P45-C 知识进入 formal reviewed，机器门控必须保持：

```json
{
  "review_status": "reviewed",
  "default_guidance": "caveat_only",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "risk_threshold_advice_allowed": false,
  "hidden_from_default_queue": true,
  "visible_in_default_guidance_queue": false
}
```

## 不做什么

```text
1. 不定义任何风险阈值数值。
2. 不定义信用额度。
3. 不定义保证金比例。
4. 不判断账户资金是否足够下单。
5. 不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
6. 不把 SEC、CME、IBKR、Binance、FIA 或任意 vendor 文档泛化为所有市场。
```

## 冲突处理

```text
1. 若与 Phase 37 Risk Management hard-gate 知识冲突，以外接项目运行时 Risk Management owner 的 deterministic policy 为准。
2. 若与 Live Execution 订单状态机冲突，以 Live Execution 的真实订单、成交、拒单、撤单和 broker API 事实为准。
3. 若与 AI Engineering scoring 冲突，AI Engineering 只能引用 reason code 和 evidence，不拥有阈值或执行动作。
4. 若与 Database/Storage 字段冲突，Database/Storage 只拥有存储、索引、审计日志和生命周期，不拥有风险含义。
```
