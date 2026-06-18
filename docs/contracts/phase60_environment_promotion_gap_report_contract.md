# Phase 60 Environment Promotion Decision 与 Gap Report Contract

生成日期：2026-06-17

## 1. 契约目标

本契约定义从一个交易测试环境推进到下一环境时必须保留的 `environment_promotion_decision` 与 `sandbox_paper_live_gap_report`。

目标是防止：

```text
1. sandbox API 测试通过就直接认为 paper/live 可用。
2. paper trading 盈利就直接认为 live-ready。
3. replay 成交可得就认为真实市场也能成交。
4. 缺少订单状态、费用、延迟、账户、风控差异时仍推进实盘。
```

## 2. 强制边界

```text
1. promotion decision 不是实盘许可。
2. gap report 不是 hard gate。
3. reviewed/caveat_only 不是 approved。
4. 不得生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
5. 不得把任何平台的 sandbox / paper 行为泛化为全部市场。
```

## 3. EnvironmentPromotionDecision

```json
{
  "promotion_decision_id": "string, required",
  "schema_version": "string, required",
  "from_environment": "enum[static_api_sandbox, exchange_testnet, historical_replay, realtime_simulation, paper_trading, live_canary], required",
  "to_environment": "enum[exchange_testnet, historical_replay, realtime_simulation, paper_trading, live_canary, live], required",
  "environment_manifest_refs": "array[string], required",
  "required_evidence": "array[string], required",
  "gap_report_id": "string, required",
  "open_blockers": "array[string], required",
  "manual_review_required": "boolean, required",
  "decision_owner": "enum[replay_owner, live_execution_owner, risk_owner, data_owner, governance_owner], required",
  "decision_timestamp": "ISO-8601 timestamp, required",
  "promotion_decision": "enum[promote, hold, block, needs_more_evidence], required",
  "promotion_not_live_permission": "boolean, required",
  "rollback_plan_ref": "string|null, required",
  "audit_trace_id": "string, required"
}
```

规则：

```text
1. manual_review_required 默认必须为 true。
2. promotion_not_live_permission 必须为 true。
3. promotion_decision=promote 只表示可以进入下一测试环境，不表示实盘授权。
4. to_environment=live 时，必须由外接项目自己的 live/risk/governance 流程另行授权，CEK-TA 不输出许可。
5. open_blockers 非空时，不得 promote。
```

## 4. SandboxPaperLiveGapReport

```json
{
  "gap_report_id": "string, required",
  "schema_version": "string, required",
  "environment_pair": "string, required",
  "source_environment_manifest_id": "string, required",
  "target_environment_manifest_id": "string, required",
  "data_gap": "object, required",
  "clock_gap": "object, required",
  "fill_gap": "object, required",
  "fee_gap": "object, required",
  "slippage_gap": "object, required",
  "latency_gap": "object, required",
  "market_impact_gap": "object, required",
  "order_state_gap": "object, required",
  "risk_policy_gap": "object, required",
  "account_or_margin_gap": "object, required",
  "unsupported_order_type": "array[string], required",
  "known_simulation_limitation": "array[string], required",
  "severity": "enum[info, warning, blocker, unresolved], required",
  "owner": "enum[replay_owner, live_execution_owner, risk_owner, data_owner, market_owner, governance_owner], required",
  "resolution_status": "enum[open, accepted_caveat, resolved, blocked, needs_more_evidence], required",
  "audit_trace_id": "string, required"
}
```

## 5. Gap 维度规则

### 5.1 data_gap

```text
必须记录 historical / realtime / mocked / broker feed 的差异、数据版本、available_time、缺失数据、延迟数据、重复数据和数据修复策略。
```

### 5.2 clock_gap

```text
必须记录 exchange_event_time、local_receive_time、decision_time、order_send_time、ack_time、fill_time 的差异。
```

### 5.3 fill_gap

```text
必须记录 simulated fill、paper fill、testnet fill 和 live fill 的来源、模型、数量、价格、部分成交和未知结果策略。
```

### 5.4 fee / slippage / latency / market impact gap

```text
费用、滑点、延迟和 market impact 不得静默为 0。
缺失时必须标记 unknown_component_present、needs_more_evidence 或 blocker。
```

### 5.5 order_state_gap

```text
必须记录 New、Accepted、PartiallyFilled、Filled、Canceled、Rejected、Expired、PendingCancel、PendingReplace 等状态的跨环境映射。
如果使用 REST/WebSocket/broker-specific 状态，必须映射到内部 order lifecycle。
```

### 5.6 risk_policy_gap

```text
必须记录 sandbox/paper 风控 rehearsal 与 live risk policy 的差异。
模拟环境中的 risk pass 不得被解释为 live hard gate 通过。
```

## 6. 推荐晋级证据

| 推进阶段 | 必需证据 |
| --- | --- |
| static_api_sandbox -> exchange_testnet | API contract、endpoint scope、鉴权隔离、mocked response caveat |
| exchange_testnet -> historical_replay | venue adapter、订单状态映射、testnet/live endpoint 差异 |
| historical_replay -> realtime_simulation | replay clock、fill/latency/fee/slippage model、market impact caveat |
| realtime_simulation -> paper_trading | realtime data source、virtual account、paper adapter、risk rehearsal |
| paper_trading -> live_canary | paper/live gap report、订单状态 reconciliation、费用/滑点/延迟差异、risk owner review |
| live_canary -> live | 外接项目自己的 live/risk/governance 授权；CEK-TA 只提供审计上下文 |

## 7. Machine Gate

```json
{
  "default_guidance": "deny",
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "trade_execution_advice_allowed": false,
  "risk_threshold_advice_allowed": false,
  "requires_human_escalation": true
}
```

## 8. 不做什么

```text
1. 不定义实盘准入阈值。
2. 不定义自动晋级。
3. 不定义自动拒单或自动停机。
4. 不定义订单路由、费用优化或仓位建议。
5. 不把 paper/live gap 的 accepted_caveat 写成无风险。
```
