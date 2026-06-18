# Phase 37 Replay / Simulation Execution Assumption Contract

生成日期：2026-06-12

## 1. 契约目标

本契约用于支撑 Phase 37 Replay / Simulation 中 3 条 reviewed-preparation 阻断候选：

```text
P37-F-R02 replay.ohlc_same_bar_tp_sl_ordering_required.v1
P37-F-R10 replay.simulation_live_gap_report_required.v1
P37-F-R12 replay.execution_cost_consistency_required.v1
```

它定义 CEK-TA 内部逻辑 schema、字段本体、owner 边界和审计要求，用于外部 AI/人工判断这 3 条候选是否可以进入 formal reviewed/caveat_only。

## 2. 强制边界

```text
1. candidate 不是正式知识。
2. 本契约只支撑 reviewed/caveat_only 准备，不支撑 approved。
3. 本契约不允许 default guidance。
4. 本契约不允许 hard gate。
5. 本契约不生成买卖点、仓位、杠杆、止损止盈或实盘执行建议。
6. Replay / Simulation 只负责模拟假设、差异审计和证据边界。
7. 真实下单、真实成交、账户同步、API 权限、拒单处理和安全停机归 Live Execution / Risk Management owner。
```

## 3. Owner 边界

| 领域 | Owner | 本契约中的职责 |
| --- | --- | --- |
| Backtest | Backtest owner | 记录历史假设、回测成本模型、评价时间和指标上下文 |
| Replay / Simulation | Replay owner | 定义事件时钟、fill model、latency model、同根 K 处理、模拟成交和 gap report |
| Paper Trading | Paper owner | 记录 paper broker、虚拟账户、paper 成交和模拟/实盘差异 |
| Live Execution | Execution owner | 提供真实订单、真实成交、真实费用、真实订单状态和 broker/exchange API 事实 |
| Risk Management | Risk owner | 提供风控触发、阻断、降仓、停机等真实风控事件 |
| Data Engineering | Data owner | 提供数据版本、时间戳、tick/quote/order event 可用性和质量报告 |
| Market Microstructure | Market owner | 提供 session、auction、halt、rollover、liquidity regime 和 venue 状态 |

## 4. same_bar_fill_ordering

### 4.1 目标

当只有 OHLC bar，而同一根 K 内 high/low 同时触及 take-profit 和 stop-loss 时，系统不能声称知道真实先后顺序。必须声明成交排序假设，或者使用更细粒度的 tick/order event 证据。

### 4.2 字段契约

```json
{
  "same_bar_fill_ordering": {
    "schema_version": "1.0.0",
    "ordering_policy_id": "string, required",
    "ordering_policy_version": "string, required",
    "market": "string, required",
    "venue": "string, required",
    "instrument_id": "string, required",
    "timeframe": "string, required",
    "bar_id": "string, required",
    "bar_start_time": "ISO-8601 timestamp, required",
    "bar_end_time": "ISO-8601 timestamp, required",
    "bar_open": "number, required",
    "bar_high": "number, required",
    "bar_low": "number, required",
    "bar_close": "number, required",
    "entry_event_time": "ISO-8601 timestamp|null, required",
    "entry_price": "number|null, required",
    "stop_loss_price": "number|null, required",
    "take_profit_price": "number|null, required",
    "touches_stop_loss": "boolean, required",
    "touches_take_profit": "boolean, required",
    "same_bar_both_touched": "boolean, required",
    "intrabar_path_available": "boolean, required",
    "intrabar_evidence_type": "enum[tick, quote, order_event, exchange_fill, unavailable], required",
    "intrabar_evidence_ref": "string|null, required",
    "ordering_mode": "enum[tick_replay, conservative, optimistic, next_bar_only, unknown_ordering_blocked], required",
    "tie_break_policy": "string, required",
    "assumption_reason": "string, required",
    "owner": "Replay / Simulation",
    "created_at": "ISO-8601 timestamp, required",
    "audit_trace_id": "string, required"
  }
}
```

### 4.3 判定规则

```text
1. 如果 intrabar_path_available=true 且 intrabar_evidence_type 为 tick、quote、order_event 或 exchange_fill，优先使用 tick_replay。
2. 如果只有 OHLC bar，且 same_bar_both_touched=true，必须选择 conservative、optimistic、next_bar_only 或 unknown_ordering_blocked。
3. conservative 表示在不确定时按更不利于策略表现的成交顺序解释。
4. optimistic 表示在不确定时按更有利于策略表现的成交顺序解释，必须在报告中显著标注。
5. next_bar_only 表示同根 K 内不执行 TP/SL 触发，下一根可成交 bar 再处理。
6. unknown_ordering_blocked 表示该样本不能作为成交质量、交易质量或可交易性证据。
7. 任何 OHLC-only same-bar 处理都不得声称还原真实市场事件顺序。
```

## 5. simulation_live_gap_report

### 5.1 目标

从 simulation / paper 进入 live 前，必须比较模拟结果与真实订单/成交/费用/风控事件之间的差异。该报告用于审计模拟证据，不等于实盘许可。

### 5.2 字段契约

```json
{
  "simulation_live_gap_report": {
    "schema_version": "1.0.0",
    "gap_report_id": "string, required",
    "simulation_run_id": "string, required",
    "paper_run_id": "string|null, optional",
    "live_reference_id": "string, required",
    "strategy_id": "string, required",
    "strategy_rule_version": "string, required",
    "data_version": "string, required",
    "market": "string, required",
    "venue": "string, required",
    "instrument_id": "string, required",
    "order_id": "string, required",
    "client_order_id": "string|null, optional",
    "simulation_order_event_ref": "string, required",
    "live_order_event_ref": "string, required",
    "simulation_event_time": "ISO-8601 timestamp, required",
    "live_event_time": "ISO-8601 timestamp, required",
    "simulation_fill_price": "number|null, required",
    "live_fill_price": "number|null, required",
    "simulation_fill_qty": "number|null, required",
    "live_fill_qty": "number|null, required",
    "simulation_fee": "number|null, required",
    "live_fee": "number|null, required",
    "simulation_slippage": "number|null, required",
    "live_slippage": "number|null, required",
    "latency_delta_ms": "number|null, required",
    "fill_price_delta": "number|null, required",
    "fill_qty_delta": "number|null, required",
    "fee_delta": "number|null, required",
    "slippage_delta": "number|null, required",
    "spread_delta": "number|null, optional",
    "reject_cancel_delta": "object, required",
    "order_state_delta": "object, required",
    "risk_trigger_delta": "object, required",
    "missing_live_fields": "array[string], required",
    "missing_simulation_fields": "array[string], required",
    "acceptable_gap_policy_id": "string, required",
    "gap_classification": "enum[within_expected_range, requires_review, invalidates_simulation_evidence, unresolved], required",
    "owner": "Replay / Simulation",
    "generated_at": "ISO-8601 timestamp, required",
    "audit_trace_id": "string, required"
  }
}
```

### 5.3 生成规则

```text
1. gap report 必须在 paper-to-live、simulation-to-live 或 post-live-review 阶段生成。
2. Live Execution 负责真实订单、真实成交、真实拒单、真实费用和真实订单状态。
3. Replay / Simulation 负责模拟成交、模拟费用、模拟延迟和模拟订单状态。
4. Risk Management 负责真实和模拟风控触发事件的归因。
5. 缺失字段必须写入 missing_live_fields 或 missing_simulation_fields，不得静默填 0。
6. gap_classification=invalidates_simulation_evidence 只表示模拟证据失效，不等于自动拒单、停机或风险 hard gate。
```

## 6. execution_cost_mapping

### 6.1 目标

Backtest、Replay、Paper 和 Live 之间必须对费用、spread、slippage、market impact 和 fill model 版本进行映射。成本口径不一致时，不能直接比较收益、胜率、PnL、R/R 或执行质量。

### 6.2 字段契约

```json
{
  "execution_cost_mapping": {
    "schema_version": "1.0.0",
    "cost_mapping_id": "string, required",
    "scope": "enum[strategy, portfolio, venue, instrument, account, project], required",
    "market": "string, required",
    "venue": "string, required",
    "instrument_id": "string|null, optional",
    "backtest_cost_model_version": "string, required",
    "replay_fill_model_version": "string, required",
    "paper_brokerage_model_version": "string|null, optional",
    "live_fee_schedule_version": "string|null, required_when_live_available",
    "spread_model_version": "string, required",
    "slippage_model_version": "string, required",
    "market_impact_model_version": "string|null, optional",
    "commission_currency": "string, required",
    "cost_components": {
      "commission": "object, required",
      "exchange_fee": "object, optional",
      "clearing_fee": "object, optional",
      "spread_cost": "object, required",
      "slippage_cost": "object, required",
      "borrow_or_funding_cost": "object, optional",
      "market_impact_cost": "object, optional",
      "tax_or_stamp_duty": "object, optional"
    },
    "component_mapping_status": "enum[complete, partial, unknown_component_present, unresolved], required",
    "owner_mapping": {
      "backtest": "Backtest owner records model versions and metric context",
      "replay": "Replay owner simulates fill/cost assumptions",
      "paper": "Paper owner records paper broker model and virtual account fills",
      "live": "Live Execution owner records actual fee/fill/order facts",
      "risk": "Risk owner records risk-triggered reduce/block/kill events"
    },
    "valid_from": "ISO-8601 timestamp, required",
    "valid_to": "ISO-8601 timestamp|null, optional",
    "created_at": "ISO-8601 timestamp, required",
    "audit_trace_id": "string, required"
  }
}
```

### 6.3 映射规则

```text
1. 每个成本组件必须标明来源、版本、币种和 owner。
2. 未映射组件必须标记为 unknown_component_present 或 unresolved，不得静默当作 0。
3. Backtest 可以记录 cost model version，但不拥有真实费用事实。
4. Replay 可以模拟 fill/cost，但不拥有 live fill truth。
5. Paper 可以记录 paper broker 行为，但不等价于 live execution。
6. Live Execution 提供真实费用、真实成交和真实订单状态事实。
7. 成本口径不一致时，不得直接比较 Backtest / Replay / Paper / Live 的表现。
```

## 7. RAG / MCP 使用边界

```text
1. MCP/SearchLab 可以检索本契约并返回来源。
2. 返回内容必须带 source、citation、review_status 和 caveat_only 边界。
3. 本契约不得进入 default guidance queue。
4. 本契约不得被解释为交易许可、策略有效性证明或风控 hard gate。
5. 外接项目可用自身字段映射本契约，不要求完全复制 CEK-TA 物理字段名。
```

## 8. 测试与验收

```text
1. 三条候选的再审包必须内联本契约全文。
2. 再审包必须包含 same_bar_fill_ordering、simulation_live_gap_report 和 execution_cost_mapping 的 schema extract。
3. 再审包必须明确 reviewed/caveat_only 是最高允许状态。
4. 质量门禁必须检查 approved_allowed=false、default_guidance_allowed=false、hard_gate_allowed=false。
5. UTF-8 文档不得出现乱码。
```
