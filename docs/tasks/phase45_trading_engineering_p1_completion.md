# Phase 45: Trading Engineering P1 专业知识补全

## Phase 目标

Phase 45 基于 Phase 37 已完成的 96 条 Trading Engineering P0 知识，继续补齐机构级交易系统需要的 P1/P2 知识缺口。

本 Phase 重点补齐：

```text
1. 交易执行与 TCA。
2. 监管级时间同步与审计追踪。
3. 分层风控、信用、保证金和 pre-trade controls。
4. 交易系统韧性、事故恢复和日志治理。
5. 压力测试、情景分析和尾部风险。
6. 订单类型、TIF 和交易所语义。
7. 市场数据授权、reference data 和 point-in-time 元数据。
8. Crypto perpetual 特有交易风险。
```

本 Phase 不推翻 Phase 37 P0，而是在其上扩展 P1/P2。所有新增知识必须继续走 candidate -> 审计 -> reviewed/caveat_only 的治理链路，不得直接进入 approved、default guidance 或 hard gate。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-452 | P0 | done | 定义 Phase 45 Trading Engineering P1/P2 知识范围、分区、canonical node 和边界 | `docs/research/phase45_trading_engineering_p1_knowledge_scope.md`、`codex-expert-kit/rag/knowledge_tree.md` | CEK-TA-451 |
| CEK-TA-453 | P0 | done | 定义 Execution TCA、Audit Trail、Layered Risk、Resilience、Stress、Order Semantics 的跨分支契约 | `docs/contracts/phase45_trading_engineering_p1_runtime_contract.md` | CEK-TA-452 |
| CEK-TA-454 | P0 | done | 创建 Phase 45 ResearchIngestionTask 队列和来源种子库 | `docs/research/phase45_trading_engineering_p1_research_task_queue.md`、`docs/research/phase45_trading_engineering_p1_source_seed.md` | CEK-TA-453 |
| CEK-TA-455 | P0 | done | 生成 Phase 45 知识范围审计 JSON，供外部 AI/人工先审分支、边界、知识点数量和优先级 | `docs/audit/phase45_trading_engineering_p1_knowledge_scope_for_audit.json` | CEK-TA-454 |
| CEK-TA-456 | P1 | done | 采集 Execution TCA 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_07_TRADE_ANALYSIS/`、`docs/research/phase45_execution_tca_candidate_research.md` | CEK-TA-455 |
| CEK-TA-457 | P1 | done | 导出 Execution TCA 候选审计包并运行质量门禁 | `docs/audit/phase45_execution_tca_candidate_audit_package_20260612.json`、`docs/reports/phase45_execution_tca_candidate_audit_package_quality_gate.json` | CEK-TA-456 |
| CEK-TA-458 | P1 | done | 按审计结果处理 Execution TCA 候选，补证并沉淀 formal reviewed/caveat_only | `codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_07_TRADE_ANALYSIS/`、`docs/reports/phase45_execution_tca_import_report.json` | CEK-TA-457 |
| CEK-TA-459 | P1 | done | 采集 Audit Trail / Clock Sync 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/`、`docs/research/phase45_trade_audit_candidate_research.md` | CEK-TA-455 |
| CEK-TA-460 | P1 | done | 导出 Audit Trail / Clock Sync 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `docs/audit/phase45_trade_audit_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_trade_audit_p45_b_20260612_external_strict_v1.json`、`docs/audit/phase45_trade_audit_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_trade_audit_supplemental_reaudit_20260612_v1.json`、`docs/audit/phase45_trade_audit_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_trade_audit_reviewed_caveat_only_preparation_20260612_v1.json`、`docs/reports/phase45_trade_audit_formal_import_report.json`、`docs/contracts/phase45_trade_audit_clock_sync_contract.md`、`codex-expert-kit/rag/knowledge/` | CEK-TA-459 |
| CEK-TA-461 | P1 | done | 采集 Layered Risk Controls / Credit / Margin 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase45_layered_risk_candidate_research.md`、`docs/reports/phase45_layered_risk_candidate_generation_report.json` | CEK-TA-455 |
| CEK-TA-462 | P1 | done | 导出 Layered Risk 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `docs/audit/phase45_layered_risk_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_layered_risk_p45_c_20260612_external_strict_v1.json`、`docs/audit/phase45_layered_risk_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_layered_risk_supplemental_reaudit_20260612_v1.json`、`docs/contracts/phase45_layered_risk_controls_contract.md`、`docs/audit/phase45_layered_risk_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_layered_risk_reviewed_caveat_only_preparation_20260612_v1.json`、`docs/reports/phase45_layered_risk_formal_import_report.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/` | CEK-TA-461 |
| CEK-TA-463 | P1 | done | 采集 Resilience / Incident / Log Management 6 条 P1 候选知识 | `codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/candidates/KB_AI_26_DATABASE_STORAGE/`、`docs/research/phase45_resilience_incident_log_candidate_research.md`、`docs/reports/phase45_resilience_incident_log_candidate_generation_report.json` | CEK-TA-455 |
| CEK-TA-464 | P1 | done | 导出 Resilience / Incident / Log 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `docs/audit/phase45_resilience_incident_log_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_20260612_external_strict_v1.json`、`docs/contracts/phase45_resilience_incident_log_runtime_contract.md`、`docs/audit/phase45_resilience_incident_log_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_supplemental_reaudit_20260612_v1.json`、`docs/reports/phase45_resilience_incident_log_audit_import_report.json`、`docs/reports/phase45_resilience_incident_log_supplemental_reaudit_import_report.json`、`docs/audit/phase45_resilience_incident_log_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_reviewed_preparation_20260612.json`、`docs/reports/phase45_resilience_incident_log_reviewed_preparation_gap_report.json`、`docs/reports/phase45_resilience_incident_log_formal_import_report.json`、`docs/audit/phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_20260612.json`、`docs/reports/phase45_resilience_incident_log_reviewed_blocked_supplemental_reaudit_gate.json`、`docs/reports/phase45_resilience_incident_log_blocked_supplemental_reaudit_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/`、`codex-expert-kit/rag/knowledge/KB_AI_26_DATABASE_STORAGE/` | CEK-TA-463 |
| CEK-TA-465 | P1 | done | 采集 Stress Testing / Scenario Risk 6 条 P1 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_stress_scenario_candidates.py`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase45_stress_scenario_candidate_research.md`、`docs/reports/phase45_stress_scenario_candidate_generation_report.json`、`docs/reports/phase45_stress_scenario_candidate_quality_gate.json` | CEK-TA-455 |
| CEK-TA-466 | P1 | done | 导出 Stress Testing / Scenario Risk 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/export_phase45_stress_scenario_candidate_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_stress04_margin_funding_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress_scenario_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_stress02_market_liquidity_reaudit_result.py`、`codex-expert-kit/rag/scripts/validate_phase45_runtime_linkage.py`、`docs/contracts/phase45_stress_scenario_risk_contract.md`、`docs/audit/phase45_stress_scenario_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_stress_scenario_candidate_20260612_external_strict.json`、`docs/audit/audit_phase45_stress_scenario_supplemental_reaudit_20260612.json`、`docs/audit/audit_phase45_stress04_margin_funding_reaudit_20260612.json`、`docs/audit/audit_phase45_stress_scenario_reviewed_preparation_20260612.json`、`docs/audit/phase45_stress_scenario_reviewed_preparation_audit_package_20260612.json`、`docs/audit/phase45_stress_scenario_stress02_market_liquidity_reaudit_package_20260612.json`、`docs/audit/audit_phase45_stress02_market_liquidity_reaudit_20260612.json`、`docs/reports/phase45_stress_scenario_candidate_audit_package_quality_gate.json`、`docs/reports/phase45_stress_scenario_candidate_audit_import_report.json`、`docs/reports/phase45_stress_scenario_supplemental_reaudit_import_report.json`、`docs/reports/phase45_stress_scenario_stress04_margin_funding_reaudit_import_report.json`、`docs/reports/phase45_stress_scenario_reviewed_preparation_gap_report.json`、`docs/reports/phase45_stress_scenario_reviewed_preparation_import_report.json`、`docs/reports/phase45_stress_scenario_stress02_market_liquidity_reaudit_gate.json`、`docs/reports/phase45_stress02_market_liquidity_reaudit_import_report.json`、`docs/reports/phase45_runtime_linkage_report.json`、`docs/research/phase45_stress_scenario_supplemental_research.md`、`docs/research/phase45_stress_scenario_stress04_margin_funding_research.md`、`docs/research/phase45_stress_scenario_stress02_market_liquidity_research.md`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/` | CEK-TA-465 |
| CEK-TA-467 | P1 | done | 采集 Order Type / TIF / Venue Semantics 6 条 P1 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_order_semantics_candidates.py`、`codex-expert-kit/rag/candidates/KB_06_LIVE_EXECUTION/`、`docs/research/phase45_order_semantics_candidate_research.md`、`docs/reports/phase45_order_semantics_candidate_generation_report.json`、`docs/reports/phase45_order_semantics_candidate_quality_gate.json` | CEK-TA-455 |
| CEK-TA-468 | P1 | done | 导出 Order Semantics 审计包、处理审计结果并沉淀 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/export_phase45_order_semantics_candidate_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase45_order_semantics_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_order_semantics_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_order_semantics_ord05_supplemental_reaudit_result.py`、`docs/contracts/phase45_order_semantics_runtime_contract.md`、`docs/audit/phase45_order_semantics_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_order_semantics_candidate_20260612_external_strict.json`、`docs/audit/phase45_order_semantics_reviewed_preparation_audit_package_20260612.json`、`docs/audit/audit_phase45_order_semantics_reviewed_preparation_20260612.json`、`docs/audit/phase45_order_semantics_ord05_supplemental_reaudit_package_20260612.json`、`docs/audit/audit_phase45_order_semantics_ord05_supplemental_reaudit_20260612.json`、`docs/research/phase45_order_semantics_ord05_supplemental_research.md`、`docs/reports/phase45_order_semantics_candidate_audit_package_quality_gate.json`、`docs/reports/phase45_order_semantics_candidate_audit_import_report.json`、`docs/reports/phase45_order_semantics_reviewed_preparation_gap_report.json`、`docs/reports/phase45_order_semantics_ord05_supplemental_reaudit_gate.json`、`docs/reports/phase45_order_semantics_import_report.json`、`docs/reports/phase45_order_semantics_ord05_formal_import_report.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.order_type_semantics_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.time_in_force_semantics_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.post_only_reduce_only_boundary.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.self_trade_prevention_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.exchange_specific_order_type_caveat.v1.json`、`codex-expert-kit/rag/knowledge/KB_06_LIVE_EXECUTION/kb_phase45_order_semantics.maker_taker_fee_order_type_boundary.v1.json` | CEK-TA-467 |
| CEK-TA-469 | P2 | done | 采集 Market Data Entitlement / Reference Data 6 条 P2 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_reference_data_entitlement_candidates.py`、`codex-expert-kit/rag/candidates/KB_02_DATA_ENGINEERING/`、`docs/research/phase45_reference_data_entitlement_candidate_research.md`、`docs/reports/phase45_reference_data_entitlement_candidate_generation_report.json`、`docs/reports/phase45_reference_data_entitlement_candidate_quality_gate.json` | CEK-TA-468 |
| CEK-TA-470 | P2 | done | 采集 Crypto Perpetual 特有风险 5 条 P2 候选知识 | `codex-expert-kit/rag/scripts/generate_phase45_crypto_perp_candidates.py`、`codex-expert-kit/rag/candidates/KB_03_MARKET_MICROSTRUCTURE/`、`codex-expert-kit/rag/candidates/KB_07_RISK_MANAGEMENT/`、`docs/research/phase45_crypto_perp_candidate_research.md`、`docs/reports/phase45_crypto_perp_candidate_generation_report.json`、`docs/reports/phase45_crypto_perp_candidate_quality_gate.json` | CEK-TA-469 |
| CEK-TA-471 | P2 | done | 导出 P2 候选审计包、处理审计结果并沉淀 11 条 formal reviewed/caveat_only | `codex-expert-kit/rag/scripts/export_phase45_p2_candidate_audit_package.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_candidate_audit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_supplemental_reaudit_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_reviewed_preparation_result.py`、`codex-expert-kit/rag/scripts/apply_phase45_p2_blocked_supplemental_reaudit_result.py`、`docs/audit/phase45_p2_candidate_audit_package_20260612.json`、`docs/audit/audit_phase45_p2_reviewed_blocked_supplemental_reaudit_20260612.json`、`docs/reports/phase45_p2_reviewed_blocked_supplemental_import_report.json`、`codex-expert-kit/rag/knowledge/KB_02_DATA_ENGINEERING/kb_phase45_p2.dataset_coverage_universe_declaration_required.v1.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_p2.maintenance_margin_liquidation_boundary.v1.json`、`codex-expert-kit/rag/knowledge/KB_07_RISK_MANAGEMENT/kb_phase45_p2.exchange_outage_and_clawback_risk.v1.json`；P2-G/P2-H 共 11 条已全部沉淀 formal reviewed/caveat_only，未创建 approved/default guidance/hard gate | CEK-TA-470 |
| CEK-TA-472 | P1 | done | 重建 knowledge_items、Vue3 fixture、知识树，并验证 MCP/SearchLab/KnowledgeTree 能命中、引用和阻断 Phase 45 知识 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`ui/src/data/phase23Candidates.ts`、`ui/src/data/knowledgeTreeNodes.ts`、`codex-expert-kit/rag/scripts/validate_phase45_runtime_linkage.py`、`docs/reports/phase45_runtime_linkage_report.json`；Phase 45 47 条均为 reviewed/caveat_only，default guidance/approved/hard gate 均未开启 | CEK-TA-471 |
| CEK-TA-473 | P1 | done | 生成 Phase 45 验收报告并更新索引 | `docs/reports/phase45_trading_engineering_p1_completion_report.md`；Phase 45 状态已更新为 done | CEK-TA-472 |

## 上游输入

```text
docs/reports/phase37_trading_engineering_post_completion_gap_audit_report.md
docs/reports/phase37_trading_engineering_knowledge_expansion_report.md
docs/research/phase37_trading_engineering_knowledge_scope.md
docs/contracts/trading_ai_cross_branch_knowledge_contract.md
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_item_schema.md
docs/contracts/knowledge_item_schema_v1_1_contract.md
```

## 下游输出

```text
1. Phase 45 P1/P2 知识范围、采集队列和来源种子库。
2. 47 条候选知识：P1 36 条，P2 11 条。
3. AI/人工审计包、补证包和导入报告。
4. formal reviewed/caveat_only 知识。
5. 重建后的 knowledge_items.json、Vue3 fixture 和知识树统计。
6. MCP/SearchLab/KnowledgeTree 运行时验证报告。
```

## 输入契约

每条候选知识必须包含：

```text
research_task_id
knowledge_slug
primary_partition
canonical_node_id
priority
source_evidence
source_quality
content.statement
applies_when
not_applicable_when
assumptions
anti_patterns
validation
risk_notes
conflict_audit
review
llm_usage_policy
machine_gate
```

## 输出契约

Phase 45 formal knowledge 必须满足：

```text
review.review_status = reviewed
machine_gate.default_guidance = caveat_only
review.approved_allowed = false
review.default_guidance_allowed = false
review.hard_gate_allowed = false
review.risk_threshold_advice_allowed = false
candidate.workflow.formal_knowledge_id 已回链
source_evidence 至少包含 2 个可审计来源
若依赖内部契约，必须内联 contract 摘要、schema extract 或 hash
```

## 知识点范围

### P1-A Execution TCA

```text
execution_tca.implementation_shortfall_required.v1
execution_tca.execution_benchmark_selection_boundary.v1
execution_tca.vwap_twap_pov_is_algorithm_scope.v1
execution_tca.delay_market_impact_opportunity_cost_decomposition.v1
execution_tca.best_execution_routing_context_required.v1
execution_tca.algorithmic_execution_not_strategy_edge.v1
```

### P1-B Audit Trail / Clock Sync

```text
trade_audit.clock_synchronization_required.v1
trade_audit.order_event_causality_trace_required.v1
trade_audit.client_exchange_order_id_mapping_required.v1
trade_audit.event_sequence_and_idempotency_required.v1
trade_audit.audit_trail_retention_and_integrity_required.v1
trade_audit.manual_vs_electronic_order_timestamp_boundary.v1
```

### P1-C Layered Risk Controls / Credit / Margin

```text
risk_management.layered_pre_trade_controls_required.v1
risk_management.credit_limit_not_strategy_risk_limit.v1
risk_management.max_order_size_and_price_collar_required.v1
risk_management.message_throttle_and_cancel_rate_controls.v1
risk_management.margin_collateral_available_funds_boundary.v1
risk_management.post_trade_surveillance_not_pre_trade_gate.v1
```

### P1-D Resilience / Incident / Log Management

```text
live_execution.business_continuity_disaster_recovery_required.v1
live_execution.degraded_mode_and_readonly_mode_required.v1
live_execution.failover_recovery_replay_boundary.v1
live_execution.incident_taxonomy_required.v1
live_execution.post_incident_review_required.v1
audit_log.log_retention_integrity_required.v1
```

### P1-E Stress Testing / Scenario Risk

```text
risk_management.scenario_stress_test_required.v1
risk_management.liquidity_stress_boundary.v1
risk_management.correlation_breakdown_caveat.v1
risk_management.gap_and_overnight_risk_required.v1
risk_management.tail_loss_review_required.v1
risk_management.stress_test_not_trade_permission.v1
```

### P1-F Order Type / TIF / Venue Semantics

```text
live_execution.order_type_semantics_required.v1
live_execution.time_in_force_semantics_required.v1
live_execution.post_only_reduce_only_boundary.v1
live_execution.self_trade_prevention_required.v1
live_execution.exchange_specific_order_type_caveat.v1
live_execution.maker_taker_fee_order_type_boundary.v1
```

### P2-G Market Data Entitlement / Reference Data

```text
data_engineering.market_data_entitlement_boundary.v1
data_engineering.point_in_time_instrument_definition_required.v1
data_engineering.tick_size_lot_size_price_limit_metadata_required.v1
data_engineering.dataset_coverage_universe_declaration_required.v1
data_engineering.vendor_schema_version_required.v1
data_engineering.reference_data_not_feature_signal.v1
```

### P2-H Crypto Perpetual

```text
crypto_perp.mark_price_index_price_last_price_boundary.v1
crypto_perp.funding_interval_accounting_required.v1
crypto_perp.maintenance_margin_liquidation_boundary.v1
crypto_perp.adl_insurance_fund_caveat.v1
crypto_perp.exchange_outage_and_clawback_risk.v1
```

## 涉及组件

```text
docs/research/
docs/contracts/
docs/audit/
docs/reports/
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
ui/src/data/
MCP/SearchLab/FastAPI 只读检索链路
```

## 涉及数据结构

```text
ResearchIngestionTask
CandidateKnowledgeItem
FormalKnowledgeItem
source_evidence
source_quality
conflict_audit
review
llm_usage_policy
machine_gate
candidate.workflow
knowledge_tree node
```

## 涉及数据库/存储

本 Phase 默认继续使用文件化知识库：

```text
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/*.ts
```

不引入新数据库，不迁移存储层。若后续要引入数据库或向量库写入，必须另立任务并经过开发者确认。

## 边界范围

范围内：

```text
1. 采集专业资料、监管资料、交易所/协议文档、框架文档和公开案例。
2. 生成候选知识、审计包、补证包和 formal reviewed/caveat_only。
3. 更新知识树、索引、Vue3 fixture 和运行时验证。
4. 明确 Trading Engineering 与 AI Engineering、Database、Memory 的引用边界。
```

范围外：

```text
1. 不生成买卖点、仓位、杠杆、止损止盈价格。
2. 不生成风险阈值数值。
3. 不把 reviewed 升级为 approved。
4. 不启用 default guidance 或 hard gate。
5. 不写入外部项目私有账户、订单、策略参数或密钥。
6. 不指定某个 broker、交易所、数据商、执行算法为通用唯一标准。
```

## 实施步骤

```text
1. 创建 Phase 45 知识范围、节点和任务队列。
2. 先执行 P1-A 到 P1-F，每组 6 条。
3. 每组先候选采集，再导出审计包。
4. 按外部/人工审计结果分流 accepted_for_draft、needs_more_evidence、rejected。
5. 对 needs_more_evidence 补证后再审。
6. 通过 reviewed-preparation 后再沉淀 formal reviewed/caveat_only。
7. P1 完成后再执行 P2-G/P2-H。
8. 最后重建索引和 Vue3 fixture，运行 MCP/SearchLab/KnowledgeTree 验证。
```

## Definition of Done

```text
1. Phase 45 任务卡、范围文档、任务队列和来源种子库存在。
2. 47 条知识点均至少进入 candidate。
3. 每条 candidate 均有来源、边界、冲突审计和 machine gate。
4. 审计通过的条目沉淀为 formal reviewed/caveat_only。
5. 未通过条目保留 needs_more_evidence/rejected 状态和审计原因。
6. knowledge_items.json、Vue3 fixture、知识树统计已重建。
7. MCP/SearchLab/KnowledgeTree 能命中并保持阻断边界。
8. approved/default guidance/hard gate/risk threshold advice 均未开启。
9. 中文文档 UTF-8 无乱码。
10. 任务索引和任务卡状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
python codex-expert-kit/rag/scripts/validate_phase45_runtime_linkage.py
npm --prefix ui run build
```

如果某个验证脚本尚不存在，必须先在对应任务中创建。

## 风险与回滚

风险：

```text
1. 监管/交易所资料具有市场、地域和时间适用边界。
2. 执行算法和 TCA 可能被误写成策略 edge。
3. 风控规则可能被误读成 CEK-TA hard gate。
4. Crypto perpetual 知识容易混入交易所私有规则或过期规则。
```

回滚：

```text
1. 不删除候选源文件。
2. 将有问题 formal knowledge 降回 draft 或 deprecated。
3. 将 machine_gate.default_guidance 设为 deny。
4. 将 candidate workflow 回到 needs_more_evidence。
5. 重建 knowledge_items.json 和 Vue3 fixture。
6. 重新执行 validate_phase45_runtime_linkage.py。
```

## 需要开发者确认的问题

```text
1. Phase 45 是否优先只做 P1 36 条，P2 11 条暂缓？
2. Crypto perpetual 是否是当前外接项目的优先市场；如果不是，可放到 P2 后段。
3. TCA 是否需要独立创建 KB_08_EXECUTION_TCA 分区，还是挂在 Live Execution / Trade Analysis 下？
```

默认建议：

```text
先做 P1 36 条，不新增新分区；TCA 分别挂在 Live Execution 和 Trade Analysis；P2 等 P1 审计完成后再做。
```
