# Phase 58 Environment Equivalence Manifest Contract

生成日期：2026-06-16

## 1. 契约目标

本契约定义 CEK-TA 内部用于审计同一策略在 `backtest`、`replay`、`paper/sandbox` 和 `live` 环境之间是否具备可比性的 `environment_equivalence_manifest`。

该契约支撑候选知识：

```text
cand_20260616_phase58_backtest_sim_live_equivalent_chain_001
```

目标不是证明策略有效，也不是允许实盘，而是要求外接项目在声称不同环境结果可比较前，必须证明共同核心、共同执行语义，或提供字段级版本映射、差异报告和 reconciliation 证据。

## 2. 强制边界

```text
1. candidate 不是正式知识。
2. accepted_for_draft 不等于 reviewed。
3. reviewed/caveat_only 准备不等于 approved。
4. 本契约不允许 default guidance。
5. 本契约不允许 hard gate。
6. 本契约不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
7. environment_gap_report 只能作为证据审计与推进评审材料，不得直接触发自动下单、自动拒单、自动停机或自动风控动作。
8. 平台文档、框架文档和 broker 文档只能作为 implementation pattern 或 supporting source，不得被写成所有交易系统的强制物理实现。
```

## 3. Owner 边界

| 领域 | Owner | 本契约职责 |
| --- | --- | --- |
| Backtest | Backtest owner | 提供 backtest_run_manifest、策略版本、参数版本、数据版本、回测成本/fill 假设和复现信息 |
| Replay / Simulation | Replay owner | 提供 replay clock、事件路径、模拟成交、延迟模型、gap report 和模拟证据边界 |
| Paper / Sandbox | Paper owner | 提供 paper broker、实时数据、虚拟账户、模拟成交、paper/live 差异和 paper run manifest |
| Live Execution | Live Execution owner | 提供真实订单、真实成交、真实拒单、撤单、费用、订单状态、broker/exchange API 事实和 reconciliation |
| Risk Management | Risk owner | 提供事前风控、账户限制、保证金/暴露/风险状态和风险事件 |
| Data Engineering | Data owner | 提供数据来源、版本、available_time、symbol mapping、contract spec、质量报告和时区策略 |
| Market Microstructure | Market owner | 提供 session、auction、halt、rollover、liquidity regime、tick size、lot size 和 venue 状态 |
| Trade Analysis | Trade Analysis owner | 只能消费结果做事后归因、质量复盘、reason code 和研究标签，不拥有执行许可 |
| AI Engineering | AI Engineering owner | 只能引用 manifest 和 gap report 做 scoring/audit explanation，不拥有交易执行、阈值或 hard gate |

## 4. 逻辑对象

```text
EnvironmentEquivalenceManifest:
  manifest_identity
  environment_scope
  strategy_identity
  market_instrument_identity
  data_time_identity
  signal_decision_identity
  risk_chain_identity
  order_intent_identity
  order_state_identity
  execution_assumption_identity
  account_cost_identity
  data_quality_identity
  venue_adapter_identity
  reconciliation_identity
  gap_report_identity
  promotion_decision_policy
  owner_mapping
  missing_field_policy
  audit_trace
```

## 5. 字段契约

### 5.1 manifest_identity

```json
{
  "manifest_id": "string, required",
  "schema_version": "string, required",
  "created_at": "ISO-8601 timestamp, required",
  "created_by": "human | codex | ci | external_project, required",
  "project_id": "string, required",
  "purpose": "enum[promotion_review, environment_comparison, ai_training_dataset_audit, post_live_reconciliation], required",
  "review_mode": "enum[draft_only, reviewed_caveat_only_preparation], required"
}
```

规则：

```text
1. review_mode=draft_only 时，只能用于候选草稿审计。
2. review_mode=reviewed_caveat_only_preparation 时，只能用于 reviewed/caveat_only 准备审计。
3. 任意 review_mode 都不得表示 approved、default guidance 或 hard gate。
```

### 5.2 environment_scope

```json
{
  "source_environment": "enum[backtest, replay, paper, sandbox, shadow, live], required",
  "target_environment": "enum[replay, paper, sandbox, shadow, live], required",
  "comparison_window_start": "ISO-8601 timestamp, required",
  "comparison_window_end": "ISO-8601 timestamp, required",
  "promotion_stage": "enum[research_to_replay, replay_to_paper, paper_to_live, shadow_to_live, post_live_review], required",
  "claim_scope": "enum[result_comparable, execution_semantics_comparable, data_pipeline_comparable, not_comparable], required"
}
```

规则：

```text
1. claim_scope=result_comparable 只能表示结果可在同一边界下比较，不等于策略有效。
2. claim_scope=not_comparable 时，必须输出阻断原因和缺失字段。
3. target_environment=live 时，必须补 live_execution_owner 和 risk_owner 证据。
```

### 5.3 strategy_identity

```json
{
  "strategy_id": "string, required",
  "strategy_code_version": "string, required",
  "strategy_code_commit": "string|null, required",
  "strategy_config_hash": "string, required",
  "parameter_set_id": "string|null, required",
  "feature_switch_hash": "string|null, required",
  "strategy_entrypoint_ref": "string, required",
  "shared_core_evidence": "enum[same_code, same_core_different_adapter, field_level_mapping, not_shared], required",
  "shared_core_notes": "string, required"
}
```

规则：

```text
1. 同名 strategy_id 不足以证明同一策略链条。
2. shared_core_evidence=not_shared 时，不得声称环境等效。
3. shared_core_evidence=field_level_mapping 时，必须提供字段级映射表和差异报告。
```

### 5.4 market_instrument_identity

```json
{
  "market": "string, required",
  "venue_id": "string, required",
  "broker_id": "string|null, required",
  "instrument_id": "string, required",
  "symbol": "string, required",
  "symbol_mapping_version": "string, required",
  "contract_spec_version": "string, required",
  "tick_size": "number|string, required",
  "lot_size": "number|string, required",
  "min_notional": "number|string|null, required",
  "price_precision": "integer|null, required",
  "qty_precision": "integer|null, required",
  "session_calendar_version": "string, required",
  "liquidity_regime_ref": "string|null, required"
}
```

规则：

```text
1. symbol 相同不代表 instrument_id 相同。
2. contract_spec_version 缺失时，不得比较期货、期权、perpetual、margin 或有最小交易单位约束的订单结果。
3. tick_size、lot_size、min_notional、precision 不一致时，必须写入 environment_gap_report。
```

### 5.5 data_time_identity

```json
{
  "data_source_id": "string, required",
  "data_version": "string, required",
  "data_quality_report_id": "string|null, required",
  "data_available_time_policy_id": "string, required",
  "exchange_event_time": "ISO-8601 timestamp|null, required",
  "local_receive_time": "ISO-8601 timestamp|null, required",
  "decision_time": "ISO-8601 timestamp, required",
  "order_send_time": "ISO-8601 timestamp|null, required",
  "ack_time": "ISO-8601 timestamp|null, required",
  "fill_time": "ISO-8601 timestamp|null, required",
  "timezone_policy": "string, required",
  "bar_build_policy": "string|null, required",
  "resampling_policy": "string|null, required",
  "lookahead_guard_version": "string, required",
  "warmup_state_snapshot_id": "string|null, required"
}
```

规则：

```text
1. decision_time 必须晚于或等于策略可见数据的 available_time。
2. exchange_event_time、local_receive_time、decision_time、order_send_time、ack_time、fill_time 不得混用。
3. bar_build_policy 或 resampling_policy 不一致时，不得直接比较信号触发点。
4. lookahead_guard_version 缺失时，不得用于 AI 训练标签或实盘推进评审。
```

### 5.6 signal_decision_identity

```json
{
  "signal_schema_version": "string, required",
  "decision_policy_version": "string, required",
  "signal_event_id": "string, required",
  "decision_event_id": "string, required",
  "order_intent_id": "string|null, required",
  "input_feature_set_version": "string|null, required",
  "feature_available_time_policy_id": "string|null, required",
  "forbidden_future_fields_checked": "boolean, required"
}
```

规则：

```text
1. order_intent_id 必须能追溯到 decision_event_id。
2. input_feature_set_version 缺失时，只能做人工审计，不得做训练样本等效声明。
3. forbidden_future_fields_checked=false 时，不得声称回测和 live 决策等效。
```

### 5.7 risk_chain_identity

```json
{
  "risk_check_chain_version": "string, required",
  "pre_trade_risk_policy_id": "string|null, required",
  "position_limit_policy_id": "string|null, required",
  "exposure_limit_policy_id": "string|null, required",
  "account_mode": "string|null, required",
  "margin_mode": "string|null, required",
  "leverage_policy_version": "string|null, required",
  "risk_decision_event_id": "string|null, required",
  "risk_owner_approval_ref": "string|null, optional"
}
```

规则：

```text
1. risk_check_chain_version 不一致时，不得声称环境执行链条等效。
2. leverage_policy_version 只记录政策版本，不得输出杠杆建议。
3. risk_owner_approval_ref 不等于实盘许可；它只表示该证据由 Risk owner 审核过。
```

### 5.8 order_intent_identity

```json
{
  "order_intent_schema_version": "string, required",
  "order_intent_id": "string, required",
  "side": "enum[buy, sell, reduce, close, unknown], required",
  "quantity_policy_ref": "string, required",
  "order_type": "string, required",
  "time_in_force": "string|null, required",
  "post_only": "boolean|null, required",
  "reduce_only": "boolean|null, required",
  "client_order_id_policy": "string, required",
  "cancel_replace_policy": "string|null, required",
  "routing_context_ref": "string|null, required",
  "adapter_mapping_ref": "string, required"
}
```

规则：

```text
1. quantity_policy_ref 只能指向策略/风险定义，不得在本契约中给出仓位建议。
2. order_type、time_in_force、post_only、reduce_only 必须按 venue/broker adapter 解释。
3. adapter_mapping_ref 缺失时，不得声称 paper/live 订单语义等效。
```

### 5.9 order_state_identity

```json
{
  "order_state_machine_version": "string, required",
  "venue_order_status_mapping_version": "string, required",
  "reject_code_mapping_version": "string|null, required",
  "partial_fill_policy": "string, required",
  "cancel_ack_policy": "string|null, required",
  "unknown_outcome_policy": "enum[blocked_for_equivalence, manual_review_required, unresolved], required",
  "live_order_event_source_ref": "string|null, required"
}
```

规则：

```text
1. unknown_outcome_policy 只能表示证据状态，不得直接触发自动撤单、自动拒单或停机。
2. venue_order_status_mapping_version 缺失时，不得比较 order lifecycle。
3. reject_code_mapping_version 缺失时，不得将 paper/simulation 拒单语义等同 live 拒单。
```

### 5.10 execution_assumption_identity

```json
{
  "fill_model_version": "string, required",
  "fee_model_version": "string, required",
  "fee_schedule_version": "string|null, required",
  "maker_taker_flag_policy": "string|null, required",
  "slippage_model_version": "string, required",
  "latency_model_version": "string, required",
  "spread_model_version": "string|null, required",
  "market_impact_model_version": "string|null, required",
  "funding_or_borrow_cost_model_version": "string|null, required",
  "settlement_model_version": "string|null, required",
  "cost_component_mapping_ref": "string, required"
}
```

规则：

```text
1. 任一成本组件缺失时，必须标记 unresolved 或 unknown_component_present。
2. market_impact_model_version 缺失时，不得把 replay large order fill 解释为 live 可得成交。
3. funding_or_borrow_cost_model_version 缺失时，不得比较 perpetual、margin、borrow 或 financing-sensitive 策略结果。
```

### 5.11 account_cost_identity

```json
{
  "position_account_source_policy": "string, required",
  "cash_source_policy": "string|null, required",
  "collateral_currency": "string|null, required",
  "account_snapshot_id": "string|null, required",
  "fee_currency_policy": "string|null, required",
  "settlement_state_ref": "string|null, required",
  "account_reconciliation_report_id": "string|null, required"
}
```

规则：

```text
1. account_snapshot_id 缺失时，不得比较 live account truth 与 paper account state。
2. fee_currency_policy 缺失时，不得把费用按 0 或默认币种处理。
3. account_reconciliation_report_id 只表示账户事实审计，不表示交易许可。
```

### 5.12 reconciliation_identity

### 5.12 data_quality_identity

```json
{
  "data_quality_report_id": "string, required",
  "missing_data_policy": "string, required",
  "duplicate_event_policy": "string, required",
  "out_of_order_event_policy": "string, required",
  "stale_data_policy": "string, required",
  "data_gap_fill_policy": "string, required",
  "clock_skew_policy": "string, required",
  "source_priority_policy": "string, required"
}
```

规则：

```text
1. data_quality_report_id 缺失时，不得声称 backtest、replay、paper/sandbox 和 live 数据链条等效。
2. missing_data_policy、duplicate_event_policy、out_of_order_event_policy 和 stale_data_policy 必须显式记录，不得静默丢弃或默认修复。
3. data_gap_fill_policy 只能说明缺口处理方法，不得把填补后的数据当作真实交易所事实。
4. clock_skew_policy 必须说明 exchange_event_time、local_receive_time、decision_time 和 order_send_time 的时钟偏差处理。
5. source_priority_policy 必须说明多个数据源冲突时哪个来源拥有事实优先级。
```

### 5.13 venue_adapter_identity

```json
{
  "adapter_id": "string, required",
  "adapter_version": "string, required",
  "api_version": "string, required",
  "endpoint_mapping_version": "string, required",
  "websocket_stream_mapping_version": "string, required",
  "rate_limit_policy": "string, required",
  "retry_policy": "string, required",
  "idempotency_policy": "string, required",
  "disconnect_recovery_policy": "string, required"
}
```

规则：

```text
1. adapter_version、api_version、endpoint_mapping_version 或 websocket_stream_mapping_version 缺失时，不得声称 paper/live 或 replay/live 订单语义等效。
2. rate_limit_policy 和 retry_policy 只能说明适配器行为，不得被解释为订单路由建议。
3. idempotency_policy 必须说明重复提交、超时重试和未知结果的处理边界。
4. disconnect_recovery_policy 必须说明断线、重连、补单、补成交、补状态的审计方式。
5. venue_adapter_identity 是 venue/broker-specific 证据，不得泛化为所有交易所或经纪商通用行为。
```

### 5.14 reconciliation_identity

```json
{
  "reconciliation_policy_id": "string, required",
  "reconciliation_tolerance_policy": "string, required",
  "position_reconciliation_report_id": "string|null, required",
  "order_reconciliation_report_id": "string|null, required",
  "missing_event_policy": "enum[manual_review_required, blocked_for_equivalence, unresolved], required",
  "external_order_policy": "enum[exclude, include_with_flag, manual_review_required], required",
  "gap_classification": "enum[within_expected_range, requires_review, invalidates_equivalence_claim, unresolved], required"
}
```

规则：

```text
1. gap_classification=within_expected_range 只表示差异在预先定义范围内，不表示策略有效。
2. gap_classification=invalidates_equivalence_claim 时，不得声称环境结果等效。
3. missing_event_policy 不得静默填充缺失事件。
4. external_order_policy=include_with_flag 时，必须记录 external_order_ref。
```

### 5.15 gap_report_identity

```json
{
  "environment_gap_report_id": "string, required",
  "data_time_gap": "object, required",
  "event_clock_gap": "object, required",
  "risk_check_gap": "object, required",
  "order_intent_gap": "object, required",
  "order_state_gap": "object, required",
  "fill_cost_latency_gap": "object, required",
  "position_account_gap": "object, required",
  "reconciliation_gap": "object, required",
  "venue_adapter_gap": "object, required",
  "audit_trace_gap": "object, required",
  "known_non_equivalence": "array[string], required"
}
```

规则：

```text
1. gap report 必须列出缺失字段和不可等效字段。
2. 只给收益曲线、胜率、PnL 或 R/R，不能替代 gap report。
3. gap report 不得直接生成实盘执行许可。
```

### 5.16 promotion_decision_policy

```json
{
  "promotion_decision_id": "string, required",
  "promotion_evidence_refs": "array[string], required",
  "promotion_blockers": "array[string], required",
  "human_reviewer_required": "boolean, required",
  "promotion_not_live_permission": "boolean, required"
}
```

规则：

```text
1. promotion_decision_policy 只能说明从 research/backtest/replay/paper/shadow 向下一环境推进时需要哪些证据。
2. promotion_evidence_refs 必须引用 manifest、gap report、reconciliation、risk review 或人工审计记录。
3. promotion_blockers 必须列出阻断推进的缺失字段或不可解释差异。
4. human_reviewer_required 必须为 true，除非外接项目有独立 human governance 契约。
5. promotion_not_live_permission 必须为 true；该字段明确 reviewed/caveat_only 不等于实盘许可。
```

### 5.17 missing_field_policy

```json
{
  "required_field_missing_action": "enum[blocked_for_equivalence, manual_review_required], required",
  "optional_field_missing_action": "enum[warn, manual_review_required], required",
  "unknown_value_action": "enum[do_not_assume_zero, manual_review_required, blocked_for_equivalence], required",
  "default_value_allowed": "boolean, required",
  "default_value_justification": "string|null, required"
}
```

规则：

```text
1. 缺失字段不得静默填 0、false、empty string 或默认可交易状态。
2. default_value_allowed=true 时，必须写 default_value_justification。
3. required 字段缺失时，默认 blocked_for_equivalence。
```

### 5.18 audit_trace

```json
{
  "audit_trace_id": "string, required",
  "source_artifacts": "array[string], required",
  "source_hashes": "array[string], required",
  "created_by": "string, required",
  "reviewed_by": "string|null, optional",
  "review_status": "enum[draft, reviewed_caveat_only_preparation], required",
  "candidate_id": "string, required",
  "knowledge_id": "string|null, optional",
  "decision_log": "array[object], required"
}
```

规则：

```text
1. review_status=draft 时，不得进入 formal reviewed。
2. reviewed_caveat_only_preparation 仍不等于 approved。
3. source_hashes 缺失时，不得声称契约已完整审计。
```

## 6. Machine Gate

```json
{
  "default_guidance": "deny",
  "reviewed_allowed": true,
  "reviewed_mode": "caveat_only",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "trade_execution_advice_allowed": false,
  "risk_threshold_advice_allowed": false,
  "review_visibility": "candidate_or_reviewed_caveat_only",
  "requires_human_escalation": true
}
```

规则：

```text
1. 本契约只允许 candidate 或 reviewed/caveat_only 准备审计。
2. 即使后续 formal reviewed，也只能作为审计上下文、项目方案 review、RAG 检索和差异报告解释。
3. 不允许进入 default guidance queue。
4. reviewed_allowed=true 只表示 reviewed/caveat_only 可见性，不表示 approved、默认指导、实盘许可或 hard gate。
```

## 7. 与已有分支的关系

```text
KB_04_BACKTEST:
  提供回测复现、数据版本、参数版本、成本/fill 假设和指标上下文。

KB_05_REPLAY_SIMULATION:
  提供回放、模拟成交、事件时钟、同根 K 处理、simulation-live gap report 和执行成本映射。

KB_06_LIVE_EXECUTION:
  提供真实订单、真实成交、拒单、撤单、账户同步、API 状态和 live reconciliation。

KB_07_RISK_MANAGEMENT:
  提供事前风控、风险状态、暴露、保证金、连续亏损停止和风险事件。

KB_02_DATA_ENGINEERING:
  提供数据版本、available_time、symbol mapping、contract spec、质量报告和数据血缘。

KB_03_STRATEGY_ENGINEERING:
  提供策略规则、信号定义、参数身份和策略变更边界。

KB_08_TRADE_ANALYSIS:
  只消费结果做事后复盘、reason code、标签和 research hypothesis，不拥有实盘许可。

KB_AI_ENGINEERING:
  只能引用 manifest 和 gap report 设计 scoring/audit explanation，不能拥有交易执行或 hard gate。
```

## 8. 不做什么

```text
1. 不定义任何买卖点。
2. 不定义任何仓位、杠杆、止损止盈或实盘执行参数。
3. 不定义自动下单许可。
4. 不定义自动拒单、自动停机或 hard gate。
5. 不把 paper/sandbox、replay 或 backtest 结果写成 live truth。
6. 不要求外接项目必须使用 NautilusTrader、QuantConnect、HftBacktest 或任何单一框架。
```

## 9. Reviewed / Caveat-only 准备条件

候选进入 formal reviewed/caveat_only 前，至少需要：

```text
1. 外部 AI/人工确认本契约字段足以支撑候选 claim。
2. 确认字段契约没有与现有 KB_04、KB_05、KB_06、KB_07、KB_02、KB_03、KB_08 和 KB_AI_ENGINEERING owner 边界冲突。
3. 确认所有来源都只作为 implementation pattern / supporting source，不被写成 universal market law。
4. 确认 machine gate 保持 approved_allowed=false、default_guidance_allowed=false、hard_gate_allowed=false。
5. 确认 manifest 和 gap report 不被外接项目解释为实盘许可。
6. 确认 data_quality_identity、venue_adapter_identity 和 promotion_decision_policy 已作为独立逻辑对象写入 formal knowledge。
```
