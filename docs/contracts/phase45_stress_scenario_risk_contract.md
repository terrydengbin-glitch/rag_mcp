# Phase 45 Stress / Scenario Risk Contract

## 目标

本契约定义 Phase 45 `P45-E Stress Testing / Scenario Risk` 知识在候选、审计、formal reviewed/caveat_only 和外接项目引用时的字段边界。

本契约只服务风险复核、场景设计、证据审计和 AI IDE 设计提醒，不提供风险阈值、仓位、杠杆、止损止盈、交易许可或实盘执行建议。

## Owner 边界

| 对象 | 主 owner | 可引用 owner | 不允许越界 |
| --- | --- | --- | --- |
| stress_scenario_event | Risk Management | Data Engineering、Market Microstructure | 不得生成交易许可或 hard gate |
| liquidity_stress_context | Risk Management | Live Execution、Market Microstructure | 不得输出可成交数量、清仓阈值或流动性阈值 |
| correlation_stress_assumption | Risk Management | Quant Foundation、Trade Analysis | 不得输出相关性阈值、降仓或拒单 |
| session_gap_risk | Risk Management | Market Microstructure、Live Execution、Data Engineering | 不得输出隔夜持仓建议或 session 风险阈值 |
| tail_loss_review | Risk Management | Trade Analysis、AI Engineering | 不得输出 VaR/ES 阈值或交易许可 |
| stress_result_governance | Risk Management | AI Engineering、Project Integration | 不得把 stress test pass 当作默认放行 |

## stress_scenario_event

```json
{
  "scenario_id": "string",
  "scenario_name": "string",
  "scenario_type": "historical | hypothetical | reverse | liquidity | correlation | gap | tail_loss",
  "owner": "risk_management",
  "market": "string",
  "asset_class": "string",
  "venue": "string | null",
  "instrument_scope": ["string"],
  "start_time": "datetime | null",
  "end_time": "datetime | null",
  "source_refs": ["source_id"],
  "scenario_assumption_version": "string",
  "data_version": "string",
  "calendar_or_session_version": "string | null",
  "created_at": "datetime",
  "review_owner": "string",
  "audit_trace_id": "string"
}
```

## liquidity_stress_context

```json
{
  "liquidity_context_id": "string",
  "market_depth_source_id": "string | null",
  "spread_source_id": "string | null",
  "venue_availability_source_id": "string | null",
  "funding_source_id": "string | null",
  "collateral_source_id": "string | null",
  "settlement_source_id": "string | null",
  "clearing_source_id": "string | null",
  "liquidity_horizon_policy_ref": "string | null",
  "unknown_component_policy": "mark_unknown_not_zero",
  "owner": "risk_management",
  "audit_trace_id": "string"
}
```

## correlation_stress_assumption

```json
{
  "correlation_assumption_id": "string",
  "assumption_type": "correlation_increase | correlation_structure_change | correlation_reversal | wrong_way_risk | concentration",
  "normal_sample_window_ref": "string | null",
  "stress_window_ref": "string | null",
  "assumption_source_refs": ["source_id"],
  "not_a_threshold": true,
  "not_a_trade_action": true,
  "owner": "risk_management",
  "audit_trace_id": "string"
}
```

## session_gap_risk

```json
{
  "session_gap_risk_id": "string",
  "market_type": "traditional_exchange | futures_session | crypto_24_7 | other",
  "venue": "string",
  "session_timezone": "string",
  "close_time": "datetime | null",
  "open_time": "datetime | null",
  "halt_or_pause_event_ref": "string | null",
  "auction_or_reopen_event_ref": "string | null",
  "holiday_or_early_close_calendar_ref": "string | null",
  "order_acceptance_rule_ref": "string | null",
  "margin_or_performance_bond_source_ref": "string | null",
  "broker_account_field_source_ref": "string | null",
  "funding_interval_source_ref": "string | null",
  "funding_fee_event_source_ref": "string | null",
  "data_availability_boundary": "string",
  "field_version": "string",
  "not_position_advice": true,
  "not_stop_loss_take_profit": true,
  "not_hard_gate": true,
  "owner": "risk_management",
  "audit_trace_id": "string"
}
```

## tail_loss_review

```json
{
  "tail_loss_review_id": "string",
  "risk_measure": "VaR | ExpectedShortfall | scenario_loss | max_single_day_loss | max_multi_day_loss | liquidity_adjusted_loss | other",
  "measure_definition_ref": "source_id",
  "liquidity_horizon_ref": "source_id | null",
  "sample_window_ref": "string",
  "out_of_sample_ref": "string | null",
  "model_exception_notes": "string",
  "not_a_threshold": true,
  "not_trade_permission": true,
  "not_hard_gate": true,
  "owner": "risk_management",
  "audit_trace_id": "string"
}
```

## stress_result_governance

```json
{
  "stress_result_id": "string",
  "scenario_id": "string",
  "result_summary": "string",
  "risk_review_input": true,
  "owner_decision_input": true,
  "scenario_backlog_input": true,
  "trade_permission": false,
  "hard_gate": false,
  "default_guidance": false,
  "review_status": "candidate | reviewed_caveat_only | deprecated",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "risk_threshold_advice_allowed": false,
  "audit_trace_id": "string"
}
```

## 校验规则

```text
1. 所有 scenario、stress、tail-loss 字段必须携带 source_refs 或内部 policy/ref。
2. 缺失 market、venue、session、account-mode、clearing 或 funding 来源时，不得把该维度写成已验证事实。
3. unknown_component 必须显式标记 unknown，不得静默当作 0、normal 或 safe。
4. stress_test_passed 不得进入 execution permission、order admission 或 hard gate 字段。
5. 风险 owner 可以使用 stress result 做人工复核输入，但 CEK-TA 不提供默认风险阈值。
6. 外接项目若要启用实盘阻断，必须在自身 Risk Management / Live Execution 契约内另行定义。
```

## reviewed/caveat_only 边界

```text
1. reviewed/caveat_only 表示可作为审计上下文、设计提醒、schema review 和 RAG 引用。
2. reviewed/caveat_only 不等于 approved。
3. reviewed/caveat_only 不进入 default guidance。
4. reviewed/caveat_only 不启用 hard gate。
5. reviewed/caveat_only 不提供风险阈值、交易许可、仓位或止损止盈。
```

