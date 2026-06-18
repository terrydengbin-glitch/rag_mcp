# Phase 45 Trading Engineering P1/P2 知识范围

## 目标

Phase 45 承接 Phase 37 完成后缺口审计，补齐机构级交易系统需要的交易工程知识。Phase 37 P0 已完成 96 条 reviewed/caveat_only；Phase 45 不重做 P0，而是补充 P1/P2。

## 范围总览

| 组别 | 主题 | 数量 | 优先级 | 主要分区 |
| --- | --- | ---: | --- | --- |
| P45-A | Execution TCA / 执行成本分析 | 6 | P1 | `KB_06_LIVE_EXECUTION`、`KB_07_TRADE_ANALYSIS` |
| P45-B | Audit Trail / Clock Sync / 审计追踪与时钟同步 | 6 | P1 | `KB_02_DATA_ENGINEERING`、`KB_06_LIVE_EXECUTION` |
| P45-C | Layered Risk / Credit / Margin / 分层风控 | 6 | P1 | `KB_07_RISK_MANAGEMENT` |
| P45-D | Resilience / Incident / Log / 系统韧性与日志 | 6 | P1 | `KB_06_LIVE_EXECUTION`、`KB_AI_26_DATABASE_STORAGE` |
| P45-E | Stress Testing / Scenario Risk / 压力测试 | 6 | P1 | `KB_07_RISK_MANAGEMENT` |
| P45-F | Order Type / TIF / Venue Semantics / 订单语义 | 6 | P1 | `KB_06_LIVE_EXECUTION`、`KB_05_REPLAY_SIMULATION` |
| P45-G | Market Data Entitlement / Reference Data / 数据授权与参考数据 | 6 | P2 | `KB_02_DATA_ENGINEERING` |
| P45-H | Crypto Perpetual / 永续合约特有风险 | 5 | P2 | `KB_03_MARKET_MICROSTRUCTURE`、`KB_07_RISK_MANAGEMENT` |

合计：47 条。

## Canonical Node 设计

Phase 45 只补 Trading Engineering 的 P1/P2 扩展能力。每组知识必须挂到明确的 Level 3 节点，不能因为与 AI、数据库或记忆系统有关就迁移到 AI Engineering。

| 组别 | canonical_node_id | 上游 owner | 下游消费方 | 分类边界 |
| --- | --- | --- | --- | --- |
| P45-A | `kt.live_execution.execution_tca`、`kt.trade_analysis.execution_tca_review` | Live Execution、Trade Analysis | 外接交易项目执行层、复盘层、AI scoring reason code | TCA 解释执行质量和成本，不证明策略 edge，不生成交易许可 |
| P45-B | `kt.trading_engineering.data_engineering.audit_clock`、`kt.live_execution.audit_trail` | Data Engineering、Live Execution、Database/Storage | 审计链、订单回放、监管式事件追踪 | 时钟、事件序列和 retention 是证据链，不是策略信号 |
| P45-C | `kt.risk_management.layered_controls` | Risk Management | 实盘前置风控、AI reason code、审计 UI | 信用、保证金、price collar、throttle 是 project policy 输入，不给阈值数值 |
| P45-D | `kt.live_execution.resilience_incident`、`kt.ai_engineering.database_storage_engineering` | Live Execution、Database/Storage | 事故复盘、日志治理、系统恢复 | BCDR、日志和 incident 不等于 hard gate 或自动停机策略 |
| P45-E | `kt.risk_management.stress_scenario` | Risk Management | 风控复核、模型评估、情景分析 | stress test 是风险分析，不是交易放行、仓位或阈值建议 |
| P45-F | `kt.live_execution.order_semantics`、`kt.replay_simulation.order_semantics` | Live Execution、Replay/Simulation | 订单适配器、模拟 fill、paper/live gap | 订单语义必须 venue-specific，不能泛化为所有交易所 |
| P45-G | `kt.trading_engineering.data_engineering.reference_data_entitlement` | Data Engineering | 数据摄取、特征工程、审计回放 | reference data 是数据契约，不是 feature signal 或策略条件 |
| P45-H | `kt.market_microstructure.crypto_perpetual`、`kt.risk_management.crypto_perpetual_risk` | Market Microstructure、Risk Management | crypto perp 数据/风控/执行项目 | crypto perpetual 规则必须交易所和产品限定，不得混入通用股票/期货规则 |

## 47 条知识点归类矩阵

| research_task_id | knowledge_slug | canonical_node_id | primary_partition | 优先级 |
| --- | --- | --- | --- | --- |
| P45-A-TCA01 | `execution_tca.implementation_shortfall_required.v1` | `kt.trade_analysis.execution_tca_review` | `KB_07_TRADE_ANALYSIS` | P1 |
| P45-A-TCA02 | `execution_tca.execution_benchmark_selection_boundary.v1` | `kt.trade_analysis.execution_tca_review` | `KB_07_TRADE_ANALYSIS` | P1 |
| P45-A-TCA03 | `execution_tca.vwap_twap_pov_is_algorithm_scope.v1` | `kt.live_execution.execution_tca` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-A-TCA04 | `execution_tca.delay_market_impact_opportunity_cost_decomposition.v1` | `kt.trade_analysis.execution_tca_review` | `KB_07_TRADE_ANALYSIS` | P1 |
| P45-A-TCA05 | `execution_tca.best_execution_routing_context_required.v1` | `kt.live_execution.execution_tca` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-A-TCA06 | `execution_tca.algorithmic_execution_not_strategy_edge.v1` | `kt.live_execution.execution_tca` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-B-AUD01 | `trade_audit.clock_synchronization_required.v1` | `kt.trading_engineering.data_engineering.audit_clock` | `KB_02_DATA_ENGINEERING` | P1 |
| P45-B-AUD02 | `trade_audit.order_event_causality_trace_required.v1` | `kt.live_execution.audit_trail` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-B-AUD03 | `trade_audit.client_exchange_order_id_mapping_required.v1` | `kt.live_execution.audit_trail` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-B-AUD04 | `trade_audit.event_sequence_and_idempotency_required.v1` | `kt.live_execution.audit_trail` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-B-AUD05 | `trade_audit.audit_trail_retention_and_integrity_required.v1` | `kt.live_execution.audit_trail` | `KB_AI_26_DATABASE_STORAGE` | P1 |
| P45-B-AUD06 | `trade_audit.manual_vs_electronic_order_timestamp_boundary.v1` | `kt.live_execution.audit_trail` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-C-RISK01 | `risk_management.layered_pre_trade_controls_required.v1` | `kt.risk_management.layered_controls` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-C-RISK02 | `risk_management.credit_limit_not_strategy_risk_limit.v1` | `kt.risk_management.layered_controls` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-C-RISK03 | `risk_management.max_order_size_and_price_collar_required.v1` | `kt.risk_management.layered_controls` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-C-RISK04 | `risk_management.message_throttle_and_cancel_rate_controls.v1` | `kt.risk_management.layered_controls` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-C-RISK05 | `risk_management.margin_collateral_available_funds_boundary.v1` | `kt.risk_management.layered_controls` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-C-RISK06 | `risk_management.post_trade_surveillance_not_pre_trade_gate.v1` | `kt.risk_management.layered_controls` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-D-OPS01 | `live_execution.business_continuity_disaster_recovery_required.v1` | `kt.live_execution.resilience_incident` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-D-OPS02 | `live_execution.degraded_mode_and_readonly_mode_required.v1` | `kt.live_execution.resilience_incident` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-D-OPS03 | `live_execution.failover_recovery_replay_boundary.v1` | `kt.live_execution.resilience_incident` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-D-OPS04 | `live_execution.incident_taxonomy_required.v1` | `kt.live_execution.resilience_incident` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-D-OPS05 | `live_execution.post_incident_review_required.v1` | `kt.live_execution.resilience_incident` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-D-OPS06 | `audit_log.log_retention_integrity_required.v1` | `kt.live_execution.resilience_incident` | `KB_AI_26_DATABASE_STORAGE` | P1 |
| P45-E-STRESS01 | `risk_management.scenario_stress_test_required.v1` | `kt.risk_management.stress_scenario` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-E-STRESS02 | `risk_management.liquidity_stress_boundary.v1` | `kt.risk_management.stress_scenario` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-E-STRESS03 | `risk_management.correlation_breakdown_caveat.v1` | `kt.risk_management.stress_scenario` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-E-STRESS04 | `risk_management.gap_and_overnight_risk_required.v1` | `kt.risk_management.stress_scenario` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-E-STRESS05 | `risk_management.tail_loss_review_required.v1` | `kt.risk_management.stress_scenario` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-E-STRESS06 | `risk_management.stress_test_not_trade_permission.v1` | `kt.risk_management.stress_scenario` | `KB_07_RISK_MANAGEMENT` | P1 |
| P45-F-ORD01 | `live_execution.order_type_semantics_required.v1` | `kt.live_execution.order_semantics` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-F-ORD02 | `live_execution.time_in_force_semantics_required.v1` | `kt.live_execution.order_semantics` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-F-ORD03 | `live_execution.post_only_reduce_only_boundary.v1` | `kt.live_execution.order_semantics` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-F-ORD04 | `live_execution.self_trade_prevention_required.v1` | `kt.live_execution.order_semantics` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-F-ORD05 | `live_execution.exchange_specific_order_type_caveat.v1` | `kt.replay_simulation.order_semantics` | `KB_05_REPLAY_SIMULATION` | P1 |
| P45-F-ORD06 | `live_execution.maker_taker_fee_order_type_boundary.v1` | `kt.live_execution.order_semantics` | `KB_06_LIVE_EXECUTION` | P1 |
| P45-G-DATA01 | `data_engineering.market_data_entitlement_boundary.v1` | `kt.trading_engineering.data_engineering.reference_data_entitlement` | `KB_02_DATA_ENGINEERING` | P2 |
| P45-G-DATA02 | `data_engineering.point_in_time_instrument_definition_required.v1` | `kt.trading_engineering.data_engineering.reference_data_entitlement` | `KB_02_DATA_ENGINEERING` | P2 |
| P45-G-DATA03 | `data_engineering.tick_size_lot_size_price_limit_metadata_required.v1` | `kt.trading_engineering.data_engineering.reference_data_entitlement` | `KB_02_DATA_ENGINEERING` | P2 |
| P45-G-DATA04 | `data_engineering.dataset_coverage_universe_declaration_required.v1` | `kt.trading_engineering.data_engineering.reference_data_entitlement` | `KB_02_DATA_ENGINEERING` | P2 |
| P45-G-DATA05 | `data_engineering.vendor_schema_version_required.v1` | `kt.trading_engineering.data_engineering.reference_data_entitlement` | `KB_02_DATA_ENGINEERING` | P2 |
| P45-G-DATA06 | `data_engineering.reference_data_not_feature_signal.v1` | `kt.trading_engineering.data_engineering.reference_data_entitlement` | `KB_02_DATA_ENGINEERING` | P2 |
| P45-H-CRYPTO01 | `crypto_perp.mark_price_index_price_last_price_boundary.v1` | `kt.market_microstructure.crypto_perpetual` | `KB_03_MARKET_MICROSTRUCTURE` | P2 |
| P45-H-CRYPTO02 | `crypto_perp.funding_interval_accounting_required.v1` | `kt.market_microstructure.crypto_perpetual` | `KB_03_MARKET_MICROSTRUCTURE` | P2 |
| P45-H-CRYPTO03 | `crypto_perp.maintenance_margin_liquidation_boundary.v1` | `kt.risk_management.crypto_perpetual_risk` | `KB_07_RISK_MANAGEMENT` | P2 |
| P45-H-CRYPTO04 | `crypto_perp.adl_insurance_fund_caveat.v1` | `kt.risk_management.crypto_perpetual_risk` | `KB_07_RISK_MANAGEMENT` | P2 |
| P45-H-CRYPTO05 | `crypto_perp.exchange_outage_and_clawback_risk.v1` | `kt.risk_management.crypto_perpetual_risk` | `KB_07_RISK_MANAGEMENT` | P2 |

## 硬边界

```text
1. 本范围不是正式知识卡，不能被 MCP/SearchLab 当作默认指导。
2. 新增知识必须先进入 candidate。
3. reviewed 不等于 approved。
4. 不得生成买卖点、仓位、杠杆、止损止盈、风险阈值数值或实盘执行许可。
5. 不得把监管、交易所、broker 或 vendor 文档写成所有市场通用规则。
6. TCA、订单语义、风控、日志和 crypto 风险均需声明市场、venue、产品、时效和适用边界。
```

## 来源优先级

```text
P0 来源：监管文件、交易所/清算所官方文档、协议官方文档、CFA/专业协会资料、NIST/标准组织资料。
P1 来源：成熟平台/框架文档、公开技术报告、数据商文档。
P2 来源：教育材料、厂商博客、产品说明，仅作 supporting source。
```

## 下游联动

```text
1. 外接交易项目 AI IDE 可通过 MCP/SearchLab 引用 reviewed/caveat_only。
2. AI Engineering 可引用 Phase 45 知识做 reason code、eval case、审计解释和 RAG 检索。
3. Database/Storage 分支可引用日志、retention、reference data、audit trail 字段。
4. Risk/Live Execution 分支仍拥有最终执行与风控边界。
```
