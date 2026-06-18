# Phase 45 Order Semantics Runtime Contract

## 目标

本契约服务 CEK-TA Phase 45 / P45-F Order Type / TIF / Venue Semantics。它定义外接交易项目在建模 live execution adapter、订单状态机、TIF、post-only/reduce-only、STP/SMP、venue-specific order type 和 maker/taker fee 时必须保留的字段边界。

本契约不是交易策略，不给买卖点、仓位、杠杆、止损止盈、路由建议、费用优化建议、订单提交许可或 hard gate。

## 上游输入

```text
order_intent
venue_order_request
venue_order_ack
execution_report
fill_event
reject_event
cancel_or_replace_event
expire_event
fee_event
position_snapshot
venue_fee_schedule_snapshot
market_session_calendar
```

## 输出契约

### order_semantics_identity

```json
{
  "order_semantics_id": "string",
  "venue": "string",
  "product_type": "spot | futures | options | perpetual | equity | other",
  "api_or_protocol": "FIX | REST | websocket | native | broker_sdk | other",
  "api_version": "string",
  "rulebook_or_spec_ref": "string",
  "adapter_version": "string",
  "semantics_version": "string"
}
```

### order_type_mapping

```json
{
  "internal_order_type": "string",
  "venue_order_type": "string",
  "ord_type_or_api_field": "string",
  "trigger_condition": "string | null",
  "price_fields": ["limit_price", "stop_price", "protection_price"],
  "allowed_sessions": ["string"],
  "partial_fill_policy": "string",
  "reject_reason_mapping": "string",
  "execution_report_mapping": "string",
  "not_applicable_when": ["string"]
}
```

### time_in_force_mapping

```json
{
  "internal_tif": "GTC | GTD | GTT | IOC | FOK | DAY | SESSION | OTHER",
  "venue_tif": "string",
  "session_calendar_ref": "string",
  "expire_time": "timestamp | null",
  "expire_time_precision": "string",
  "clock_source": "string",
  "partial_fill_behavior": "string",
  "cancel_or_expire_event_ref": "string"
}
```

### post_reduce_constraints

```json
{
  "post_only_flag": "boolean | null",
  "reduce_only_flag": "boolean | null",
  "position_source_ref": "string | null",
  "existing_open_orders_policy": "string",
  "venue_reject_cancel_reprice_behavior": "string",
  "failure_event_ref": "string"
}
```

### stp_smp_mapping

```json
{
  "stp_smp_enabled": "boolean",
  "scope": "account | firm | group | venue_specific",
  "mode": "cancel_newest | cancel_oldest | cancel_both | decrement | reject | venue_specific",
  "mode_source_ref": "string",
  "event_mapping_ref": "string",
  "compliance_boundary": "not_a_market_abuse_conclusion"
}
```

### fee_evidence

```json
{
  "venue_fee_schedule_ref": "string",
  "fee_schedule_version": "string",
  "fill_event_ref": "string",
  "liquidity_flag": "maker | taker | mixed | unknown",
  "transaction_type": "string",
  "fee_tier_source": "string | null",
  "fee_amount_source": "execution_report | venue_statement | clearing_statement | unknown"
}
```

## Owner 边界

```text
Live Execution: adapter、order state machine、venue order truth、execution report、fill/reject/expire event。
Replay / Simulation: 模拟订单语义映射和 fill model 假设，不拥有 live venue truth。
Risk Management: 是否允许提交/撤单/改单/降低仓位的 deterministic policy。
Execution TCA: fee、slippage、benchmark、maker/taker attribution 的事后分析，不拥有订单许可。
Trade Audit: event sequence、idempotency、timestamp、retention 和审计链。
```

## 禁止事项

```text
1. 不得从 order type、TIF、post-only、reduce-only、STP/SMP 或 maker/taker fee 生成交易信号。
2. 不得输出订单提交许可、自动撤单、自动改单、强制 reduce 或路由建议。
3. 不得把某个 venue 的订单语义泛化成所有市场通用规则。
4. 不得把 maker/taker fee 写成策略 alpha、费用套利或成交质量保证。
5. 不得把 STP/SMP 写成防操纵合规结论。
```
