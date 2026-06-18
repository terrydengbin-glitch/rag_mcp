# Phase 45 Trading Engineering P1/P2 ResearchIngestionTask 队列

## 执行顺序

| 批次 | 分组 | 数量 | 状态 | 说明 |
| --- | --- | ---: | --- | --- |
| P45-A | Execution TCA / 执行成本分析 | 6 | formal_reviewed | P1 第一批，已沉淀 formal reviewed/caveat_only |
| P45-B | Audit Trail / Clock Sync / 审计追踪与时钟同步 | 6 | formal_reviewed | P1 第二批，已沉淀 formal reviewed/caveat_only |
| P45-C | Layered Risk / Credit / Margin / 分层风控 | 6 | formal_reviewed | P1 第三批，已沉淀 formal reviewed/caveat_only |
| P45-D | Resilience / Incident / Log / 系统韧性与日志 | 6 | formal_reviewed | P1 第四批，6 条已沉淀 formal reviewed/caveat_only |
| P45-E | Stress Testing / Scenario Risk / 压力测试 | 6 | supplemental_reaudit_pending | P1 第五批，3 条 accepted_for_draft，3 条补证后等待再审 |
| P45-F | Order Type / TIF / Venue Semantics / 订单语义 | 6 | done | P1 第六批，6 条已全部沉淀 formal reviewed/caveat_only；不创建 approved/default guidance/hard gate |
| P45-G | Market Data Entitlement / Reference Data / 数据授权与参考数据 | 6 | supplemental_reaudit_pending | P2，5 条 accepted_for_draft；DATA05 已补 internal lineage contract 和外部血缘来源，等待二审 |
| P45-H | Crypto Perpetual / 永续合约特有风险 | 5 | supplemental_reaudit_pending | P2，4 条 accepted_for_draft；CRYPTO05 已补 API/WebSocket/maintenance/ADL 证据，等待二审 |

## ResearchIngestionTask 契约

```json
{
  "research_task_id": "P45-A-TCA01",
  "knowledge_slug": "execution_tca.implementation_shortfall_required.v1",
  "primary_partition": "KB_06_LIVE_EXECUTION",
  "canonical_node_id": "kt.trading_engineering.live_execution.execution_tca",
  "priority": "P1",
  "status": "todo | candidate_ready | needs_more_evidence | accepted_for_draft | formal_reviewed",
  "minimum_source_count": 2,
  "required_source_types": [
    "regulatory_doc",
    "official_doc",
    "professional_research",
    "framework_doc"
  ],
  "must_define": [
    "applicability",
    "not_applicable_when",
    "assumptions",
    "conflict_audit",
    "llm_usage_policy",
    "machine_gate"
  ]
}
```

## P45-A Execution TCA

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-A-TCA01 | execution_tca.implementation_shortfall_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-A-TCA02 | execution_tca.execution_benchmark_selection_boundary.v1 | KB_07_TRADE_ANALYSIS | formal_reviewed |
| P45-A-TCA03 | execution_tca.vwap_twap_pov_is_algorithm_scope.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-A-TCA04 | execution_tca.delay_market_impact_opportunity_cost_decomposition.v1 | KB_07_TRADE_ANALYSIS | formal_reviewed |
| P45-A-TCA05 | execution_tca.best_execution_routing_context_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-A-TCA06 | execution_tca.algorithmic_execution_not_strategy_edge.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |

## P45-B Audit Trail / Clock Sync

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-B-AUD01 | trade_audit.clock_synchronization_required.v1 | KB_02_DATA_ENGINEERING | formal_reviewed |
| P45-B-AUD02 | trade_audit.order_event_causality_trace_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-B-AUD03 | trade_audit.client_exchange_order_id_mapping_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-B-AUD04 | trade_audit.event_sequence_and_idempotency_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-B-AUD05 | trade_audit.audit_trail_retention_and_integrity_required.v1 | KB_AI_26_DATABASE_STORAGE | formal_reviewed |
| P45-B-AUD06 | trade_audit.manual_vs_electronic_order_timestamp_boundary.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |

## P45-C Layered Risk / Credit / Margin

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-C-RISK01 | risk_management.layered_pre_trade_controls_required.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-C-RISK02 | risk_management.credit_limit_not_strategy_risk_limit.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-C-RISK03 | risk_management.max_order_size_and_price_collar_required.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-C-RISK04 | risk_management.message_throttle_and_cancel_rate_controls.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-C-RISK05 | risk_management.margin_collateral_available_funds_boundary.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-C-RISK06 | risk_management.post_trade_surveillance_not_pre_trade_gate.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |

## P45-D Resilience / Incident / Log

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-D-OPS01 | live_execution.business_continuity_disaster_recovery_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-D-OPS02 | live_execution.degraded_mode_and_readonly_mode_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-D-OPS03 | live_execution.failover_recovery_replay_boundary.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-D-OPS04 | live_execution.incident_taxonomy_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-D-OPS05 | live_execution.post_incident_review_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed |
| P45-D-OPS06 | audit_log.log_retention_integrity_required.v1 | KB_AI_26_DATABASE_STORAGE | formal_reviewed |

## P45-E Stress Testing / Scenario Risk

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-E-STRESS01 | risk_management.scenario_stress_test_required.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-E-STRESS02 | risk_management.liquidity_stress_boundary.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-E-STRESS03 | risk_management.correlation_breakdown_caveat.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-E-STRESS04 | risk_management.gap_and_overnight_risk_required.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-E-STRESS05 | risk_management.tail_loss_review_required.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |
| P45-E-STRESS06 | risk_management.stress_test_not_trade_permission.v1 | KB_07_RISK_MANAGEMENT | formal_reviewed |

## P45-F Order Type / TIF / Venue Semantics

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-F-ORD01 | live_execution.order_type_semantics_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed_caveat_only |
| P45-F-ORD02 | live_execution.time_in_force_semantics_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed_caveat_only |
| P45-F-ORD03 | live_execution.post_only_reduce_only_boundary.v1 | KB_06_LIVE_EXECUTION | formal_reviewed_caveat_only |
| P45-F-ORD04 | live_execution.self_trade_prevention_required.v1 | KB_06_LIVE_EXECUTION | formal_reviewed_caveat_only |
| P45-F-ORD05 | live_execution.exchange_specific_order_type_caveat.v1 | KB_06_LIVE_EXECUTION | formal_reviewed_caveat_only |
| P45-F-ORD06 | live_execution.maker_taker_fee_order_type_boundary.v1 | KB_06_LIVE_EXECUTION | formal_reviewed_caveat_only |

## P45-G Market Data Entitlement / Reference Data

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-G-DATA01 | data_engineering.market_data_entitlement_boundary.v1 | KB_02_DATA_ENGINEERING | accepted_for_draft |
| P45-G-DATA02 | data_engineering.point_in_time_instrument_definition_required.v1 | KB_02_DATA_ENGINEERING | accepted_for_draft |
| P45-G-DATA03 | data_engineering.tick_size_lot_size_price_limit_metadata_required.v1 | KB_02_DATA_ENGINEERING | accepted_for_draft |
| P45-G-DATA04 | data_engineering.dataset_coverage_universe_declaration_required.v1 | KB_02_DATA_ENGINEERING | accepted_for_draft |
| P45-G-DATA05 | data_engineering.vendor_schema_version_required.v1 | KB_02_DATA_ENGINEERING | needs_more_evidence_supplemented |
| P45-G-DATA06 | data_engineering.reference_data_not_feature_signal.v1 | KB_02_DATA_ENGINEERING | accepted_for_draft |

## P45-H Crypto Perpetual

| ID | knowledge_slug | primary_partition | 状态 |
| --- | --- | --- | --- |
| P45-H-CRYPTO01 | crypto_perp.mark_price_index_price_last_price_boundary.v1 | KB_03_MARKET_MICROSTRUCTURE | accepted_for_draft |
| P45-H-CRYPTO02 | crypto_perp.funding_interval_accounting_required.v1 | KB_03_MARKET_MICROSTRUCTURE | accepted_for_draft |
| P45-H-CRYPTO03 | crypto_perp.maintenance_margin_liquidation_boundary.v1 | KB_07_RISK_MANAGEMENT | accepted_for_draft |
| P45-H-CRYPTO04 | crypto_perp.adl_insurance_fund_caveat.v1 | KB_07_RISK_MANAGEMENT | accepted_for_draft |
| P45-H-CRYPTO05 | crypto_perp.exchange_outage_and_clawback_risk.v1 | KB_07_RISK_MANAGEMENT | needs_more_evidence_supplemented |
