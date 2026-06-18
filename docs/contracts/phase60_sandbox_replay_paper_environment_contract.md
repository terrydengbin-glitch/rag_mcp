# Phase 60 Sandbox / Replay / Paper Environment Contract

生成日期：2026-06-17

## 1. 契约目标

本契约定义 CEK-TA 用于描述沙盒、测试网、历史回放、实时模拟执行、模拟盘 / paper trading、live canary 和 live 环境事实的 `environment_manifest`。

目标是让外接项目在比较回放、模拟盘、paper 和 live 结果之前，先说明当前环境的：

```text
数据来源
时钟策略
执行 adapter
账户范围
API endpoint 范围
成交模型
费用模型
延迟模型
market impact 假设
订单状态映射
风控策略引用
审计 trace
```

本契约不证明策略有效，不允许实盘，不创建 approved、default guidance 或 hard gate。

## 2. 强制边界

```text
1. candidate 不是正式知识。
2. accepted_for_draft 不等于 reviewed。
3. reviewed/caveat_only 不等于 approved。
4. 本契约不允许 default guidance。
5. 本契约不允许 hard gate。
6. 本契约不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
7. environment_manifest 只能说明环境事实和模拟假设，不得被解释为 live permission。
8. 平台文档、交易所文档、broker 文档和框架文档只能作为 implementation pattern 或 supporting source。
```

## 3. Environment Type

```json
{
  "environment_type": "enum[static_api_sandbox, exchange_testnet, historical_replay, realtime_simulation, paper_trading, live_canary, live]"
}
```

语义：

| environment_type | 用途 | 不能证明 |
| --- | --- | --- |
| static_api_sandbox | 验证 API contract、字段格式、鉴权、mocked request/response | 市场行为、真实成交、真实账户、真实流动性 |
| exchange_testnet | 验证 testnet endpoint、adapter、订单生命周期、环境隔离 | 生产环境流动性、生产账户、真实费用、实盘可成交性 |
| historical_replay | 验证事件时钟、fill model、latency model、成本和回放路径 | 订单能改变市场、真实队列位置、真实 market impact |
| realtime_simulation | 验证实时行情输入和模拟执行链条 | 真实路由、真实成交、真实账户权益 |
| paper_trading | 使用实时行情和虚拟资金演练端到端链条 | live-ready、真实滑点、真实队列、真实费用、策略优势 |
| live_canary | 小范围真实资金/真实订单验证模拟环境无法覆盖的 live gap | 放大实盘许可、默认策略有效、风险阈值 |
| live | 真实账户、真实订单、真实成交、真实费用和真实风控事实 | 不在本契约中授权任何交易动作 |

## 4. Owner 边界

| Owner | 职责 |
| --- | --- |
| Replay / Simulation | historical_replay、realtime_simulation、fill/latency/fee 假设、simulation gap |
| Live Execution | static API sandbox、exchange testnet、paper/live adapter、订单状态、真实订单事实 |
| Risk Management | 风控 policy 引用、risk rehearsal、promotion blocker、live canary 风险边界 |
| Data Engineering | 数据版本、available_time、数据质量、时区、快照和 replay 数据源 |
| Market Microstructure | session、halt、auction、rollover、tick/lot/min-notional、liquidity regime |
| AI Engineering | 只能消费 manifest 做审计解释、RAG 检索和 scoring 上下文，不拥有阈值或执行动作 |

## 5. EnvironmentManifest 字段契约

```json
{
  "environment_id": "string, required",
  "schema_version": "string, required",
  "environment_type": "enum[static_api_sandbox, exchange_testnet, historical_replay, realtime_simulation, paper_trading, live_canary, live], required",
  "created_at": "ISO-8601 timestamp, required",
  "created_by": "human | codex | ci | external_project, required",
  "project_id": "string, required",
  "strategy_id": "string|null, required",
  "strategy_version_ref": "string|null, required",
  "venue_id": "string|null, required",
  "broker_id": "string|null, required",
  "market": "string, required",
  "instrument_scope": "array[string], required",
  "data_source_type": "enum[mocked_response, historical_market_data, realtime_market_data, broker_paper_feed, exchange_testnet_feed, live_venue_feed], required",
  "market_data_realtime_or_historical": "enum[mocked, historical, realtime, mixed], required",
  "clock_policy": "string, required",
  "execution_adapter_type": "enum[none, mocked_api, simulated_matching, broker_paper, exchange_testnet, live_broker, live_exchange], required",
  "venue_adapter_ref": "string|null, required",
  "account_scope": "enum[none, mock_account, testnet_account, paper_account, live_canary_account, live_account], required",
  "api_endpoint_scope": "object, required",
  "fill_model_ref": "string|null, required",
  "latency_model_ref": "string|null, required",
  "fee_model_ref": "string|null, required",
  "slippage_model_ref": "string|null, required",
  "market_impact_assumption": "enum[not_applicable, no_market_impact, simulated_market_impact, live_market_impact_observed, unknown], required",
  "order_state_mapping_ref": "string|null, required",
  "risk_policy_ref": "string|null, required",
  "data_quality_report_ref": "string|null, required",
  "environment_gap_report_ref": "string|null, optional",
  "audit_trace_id": "string, required",
  "not_valid_for": "array[string], required"
}
```

## 6. 字段规则

### 6.1 static_api_sandbox

```text
1. data_source_type 必须是 mocked_response 或明确标注 mock。
2. market_impact_assumption 必须是 not_applicable。
3. not_valid_for 必须包含 live_fill_quality、market_behavior、strategy_profitability。
4. 如果 API sandbox 响应是 mocked response，不得把响应当作真实账户、真实订单或真实成交。
```

### 6.2 exchange_testnet

```text
1. api_endpoint_scope 必须记录 testnet/demo base URL 或 endpoint profile。
2. account_scope 必须是 testnet_account。
3. 必须标注 key/account 与生产环境隔离。
4. 不得把 testnet acceptance、testnet balance 或 testnet fills 写成生产环境事实。
```

### 6.3 historical_replay

```text
1. 必须声明 historical data version、event clock、latency model 和 fill model。
2. market_impact_assumption 缺失或 unknown 时，不得比较大订单 live 可成交性。
3. no_market_impact 时，必须在 not_valid_for 中标注 live_market_impact_proof。
4. OHLC-only、tick replay、order book replay 的数据粒度必须显式记录。
```

### 6.4 realtime_simulation / paper_trading

```text
1. 必须说明实时行情来源、虚拟账户、模拟成交和费用模型。
2. 必须记录 paper/simulation 与 live 的已知差异。
3. 不得把 paper trading 盈亏、胜率、PnL、R/R 或成交率写成 live-ready。
4. 如果使用 broker paper account，必须记录 broker-specific caveat。
```

### 6.5 live_canary

```text
1. live_canary 只表示有限范围真实环境验证，不等于放大实盘许可。
2. 必须引用 risk_policy_ref、rollback_plan_ref 和 manual_review_ref。
3. 不得在 CEK-TA 知识中写出资金规模、风险阈值、仓位或杠杆建议。
```

## 7. Machine Gate

```json
{
  "default_guidance": "deny",
  "reviewed_allowed": false,
  "approved_allowed": false,
  "default_guidance_allowed": false,
  "hard_gate_allowed": false,
  "trade_execution_advice_allowed": false,
  "risk_threshold_advice_allowed": false,
  "requires_human_escalation": true
}
```

规则：

```text
1. 候选阶段 default_guidance 必须为 deny。
2. formal reviewed/caveat_only 后也不得进入 default guidance queue。
3. 本契约不得被外接项目解释为自动放行、自动拒单、自动停机或自动晋级。
```

## 8. 与 Phase 58 的关系

```text
Phase 58 解决不同环境结果是否可比。
Phase 60 解决每个环境自身是什么、如何记录、如何晋级、如何报告差异。
Phase 60 的 environment_manifest 可以作为 Phase 58 environment_equivalence_manifest 的输入证据之一。
```

## 9. 不做什么

```text
1. 不接入真实 API。
2. 不创建 API key。
3. 不运行 testnet/paper/live 交易。
4. 不创建数据库迁移。
5. 不输出交易信号或执行建议。
6. 不证明策略收益。
```
