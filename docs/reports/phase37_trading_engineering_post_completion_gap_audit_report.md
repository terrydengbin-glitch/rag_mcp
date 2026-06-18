# Phase 37 Trading Engineering 完成后缺口审计报告

生成日期：2026-06-12  
任务 ID：CEK-TA-451  
审计对象：Phase 37 Trading Engineering P0 已沉淀的 96 条 formal reviewed/caveat_only 知识。

## 审计结论

Phase 37 P0 已覆盖交易系统开发的主要地基：量化基础、数据工程、K 线与策略工程、市场微观结构、回测、回放模拟、实盘执行、风险管理和交易复盘。

但从专业资料、监管要求、交易基础设施案例和数据工程实践对照看，当前 96 条更偏“策略研发与交易质量审计地基”，还没有完整覆盖“机构级交易系统”的若干工程侧、合规侧和运营侧知识。建议新增 Phase 37 P1/P2 补充任务，不直接把这些缺口写入 approved/default guidance。

## 外部资料对照

本次审计参考了以下专业来源方向：

| 来源 | 用途 |
| --- | --- |
| CFA Institute Trade Strategy and Execution | 支撑 TCA、implementation shortfall、执行质量、交易成本和 benchmark 评估 |
| SEC Rule 15c3-5 / Market Access Rule FAQ | 支撑 pre-trade/post-trade 风控、市场准入、监管合规和 supervisory controls |
| FIA Best Practices for Automated Trading Risk Controls | 支撑 kill switch、分层 pre-trade controls、credit controls、自动交易风险控制 |
| FIX Execution Report 文档 | 支撑订单生命周期、订单状态、成交、拒单、费用和状态机事件 |
| SEC Rule 613 / CAT 与 MiFID II RTS 25 | 支撑交易事件时间戳、clock synchronization、监管审计追踪 |
| Databento instrument definitions / symbology / corporate actions | 支撑 point-in-time reference data、合约定义、symbology、公司行动与数据源元数据 |
| CME Globex Credit Controls | 支撑交易所/清算层 pre-execution credit 和 quantity controls |
| SEC Regulation SCI / NIST SP 800-92 | 支撑交易系统韧性、BC/DR、系统事件、日志管理和审计日志生命周期 |
| Basel / Federal Reserve stress testing guidance | 支撑压力测试、情景分析、流动性和尾部风险治理 |

## 主要遗漏

### 1. 交易执行与 TCA 知识仍偏薄

当前已有 slippage、execution quality、market impact、trade review 等条目，但缺少独立的执行策略和 TCA 知识：

```text
implementation shortfall / arrival price
VWAP / TWAP / POV / IS algorithm 适用边界
execution benchmark selection
opportunity cost / delay cost / market impact cost 分解
best execution 与 routing disclosure 边界
```

建议新增分支：

```text
KB_06_LIVE_EXECUTION / execution_tca
KB_07_TRADE_ANALYSIS / execution_tca_review
```

P1 知识点建议：

```text
execution_tca.implementation_shortfall_required.v1
execution_tca.execution_benchmark_selection_boundary.v1
execution_tca.vwap_twap_pov_is_algorithm_scope.v1
execution_tca.delay_market_impact_opportunity_cost_decomposition.v1
execution_tca.best_execution_routing_context_required.v1
execution_tca.algorithmic_execution_not_strategy_edge.v1
```

### 2. 监管级时间同步与审计追踪不足

当前有 timestamp alignment、event clock、order/fill log，但缺少监管级时钟同步、审计链和事件顺序证据。

P1 知识点建议：

```text
trade_audit.clock_synchronization_required.v1
trade_audit.order_event_causality_trace_required.v1
trade_audit.client_exchange_order_id_mapping_required.v1
trade_audit.event_sequence_and_idempotency_required.v1
trade_audit.audit_trail_retention_and_integrity_required.v1
trade_audit.manual_vs_electronic_order_timestamp_boundary.v1
```

边界：这些知识只能作为审计、回放、监管对齐和数据质量规则，不能输出买卖建议。

### 3. 风控缺少“分层控制”和信用/保证金控制

当前已有单笔风险、日亏损、组合暴露、连续亏损、hard risk gate、kill switch，但还缺：

```text
broker / exchange / clearing / strategy 四层风险控制边界
credit limit 与 strategy risk limit 的区别
max order size / price collar / message throttle / fat finger controls
clearing margin / collateral / available buying power 约束
pre-trade controls 与 post-trade surveillance 的职责分离
```

P1 知识点建议：

```text
risk_management.layered_pre_trade_controls_required.v1
risk_management.credit_limit_not_strategy_risk_limit.v1
risk_management.max_order_size_and_price_collar_required.v1
risk_management.message_throttle_and_cancel_rate_controls.v1
risk_management.margin_collateral_available_funds_boundary.v1
risk_management.post_trade_surveillance_not_pre_trade_gate.v1
```

### 4. 系统韧性、BC/DR、事故恢复知识不足

当前 kill switch 与 live execution 事故边界已有基础，但缺少交易系统韧性：

```text
trading system incident taxonomy
business continuity / disaster recovery
degraded mode / read-only mode
failover and replay recovery
log retention, integrity checking, archival
post-incident review and corrective action
```

P1 知识点建议：

```text
live_execution.business_continuity_disaster_recovery_required.v1
live_execution.degraded_mode_and_readonly_mode_required.v1
live_execution.failover_recovery_replay_boundary.v1
live_execution.incident_taxonomy_required.v1
live_execution.post_incident_review_required.v1
audit_log.log_retention_integrity_required.v1
```

### 5. 压力测试、情景分析和尾部风险覆盖不足

当前覆盖回测、样本外、成本、风险限额，但缺少系统化 stress/scenario：

```text
historical scenario
hypothetical scenario
liquidity stress
correlation breakdown
gap risk / overnight risk
portfolio tail loss review
```

P1 知识点建议：

```text
risk_management.scenario_stress_test_required.v1
risk_management.liquidity_stress_boundary.v1
risk_management.correlation_breakdown_caveat.v1
risk_management.gap_and_overnight_risk_required.v1
risk_management.tail_loss_review_required.v1
risk_management.stress_test_not_trade_permission.v1
```

### 6. 订单类型、TIF、交易所语义仍需补强

当前有订单状态机、fill、reject/cancel、exchange rule simulation，但缺少 order type 本体：

```text
market / limit / stop / stop-limit / post-only
IOC / FOK / GTC / day order
reduce-only / close-only
maker-taker fee behavior
self-trade prevention
exchange-specific order type caveat
```

P1 知识点建议：

```text
live_execution.order_type_semantics_required.v1
live_execution.time_in_force_semantics_required.v1
live_execution.post_only_reduce_only_boundary.v1
live_execution.self_trade_prevention_required.v1
live_execution.exchange_specific_order_type_caveat.v1
live_execution.maker_taker_fee_order_type_boundary.v1
```

### 7. 市场数据授权、reference data 和 point-in-time 元数据需要加强

当前有 OHLCV、data version、symbology、corporate action/rollover、raw/adjusted，但还缺：

```text
market data entitlement / license boundary
point-in-time instrument definition
tick size / lot size / price limit metadata
dataset coverage / survivorship universe declaration
vendor schema version and entitlement audit
```

P1 知识点建议：

```text
data_engineering.market_data_entitlement_boundary.v1
data_engineering.point_in_time_instrument_definition_required.v1
data_engineering.tick_size_lot_size_price_limit_metadata_required.v1
data_engineering.dataset_coverage_universe_declaration_required.v1
data_engineering.vendor_schema_version_required.v1
data_engineering.reference_data_not_feature_signal.v1
```

### 8. Crypto / perpetual 特有交易风险只覆盖了一部分

当前有 funding / open interest context，但如果外接项目涉及 crypto perpetuals，还需要：

```text
funding interval and mark price
index price / mark price / last price distinction
maintenance margin and liquidation
ADL / insurance fund
exchange outage and clawback caveat
```

P2 知识点建议：

```text
crypto_perp.mark_price_index_price_last_price_boundary.v1
crypto_perp.funding_interval_accounting_required.v1
crypto_perp.maintenance_margin_liquidation_boundary.v1
crypto_perp.adl_insurance_fund_caveat.v1
crypto_perp.exchange_outage_and_clawback_risk.v1
```

## 优先级建议

建议先补 P1，共 36 条：

```text
1. execution_tca：6 条
2. trade_audit / clock / audit trail：6 条
3. layered risk controls / credit / margin：6 条
4. resilience / incident / logs：6 条
5. stress testing / scenario risk：6 条
6. order type / TIF / venue semantics：6 条
```

P2 再补 11 条：

```text
1. market data entitlement / reference data：6 条
2. crypto perpetual 特有风险：5 条
```

## 与现有 96 条的关系

这些不是推翻 Phase 37 P0，而是扩展：

```text
P0 = 策略研发、回测、模拟、执行、风控、复盘的基础规则。
P1 = 机构级执行、监管审计、系统韧性、分层风控、压力测试。
P2 = 特定市场和数据授权细节，例如 crypto perpetuals、vendor entitlement、reference data 细节。
```

新增知识仍必须遵循：

```text
candidate -> AI/人工审计 -> needs_more_evidence/accepted_for_draft -> reviewed/caveat_only -> 人工另行决定 approved
```

不得直接进入 approved、default guidance 或 hard gate。

## 建议下一步

创建 Phase 37.1 或 Phase 45：

```text
Phase 37.1: Trading Engineering P1 专业知识补全
```

首批执行顺序：

```text
1. Execution TCA
2. Audit Trail / Clock Sync
3. Layered Risk Controls
4. Resilience / Incident / Log Management
5. Stress Testing / Scenario Risk
6. Order Type / Venue Semantics
```
