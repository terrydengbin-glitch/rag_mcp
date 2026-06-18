# Phase 37 Trading Engineering 知识库扩展范围

## 目标

Phase 37 用于把 Phase 36 中不应放入 AI Engineering 的交易专业规则本体，重新落到 Trading Engineering 知识分支。它先记录需要完善的知识点范围、边界、上下游和审计要求，防止后续采集时遗漏或错放。

本文件不是正式知识卡，不得作为 MCP、SearchLab、外部项目 AI 的默认指导。后续每条知识点必须经过联网采集、来源评分、冲突审计、候选审核、formal reviewed/approved 治理流程。

## 跨分支边界

Trading Engineering 负责：

```text
量化基础、交易数学、市场数据工程、K 线与策略规则、市场微观结构、回测可信度、回放模拟、实盘执行、风险管理、交易复盘。
```

AI Engineering 负责：

```text
如何检索、引用、转换、训练、评估、部署和治理这些交易知识；不重写交易规则本体。
```

硬边界：

```text
1. K 线形态、指标解释、策略规则、止损止盈、仓位、回测、fill model、实盘风控、交易复盘规则，主分类必须在 Trading Engineering。
2. AI Engineering 只能通过 knowledge_refs、retrieved_knowledge、label_schema、eval_case、gate_policy 引用交易规则。
3. 外部项目私有策略参数、账户事实、实盘配置、密钥、交易样本细节不得进入通用 CEK-TA 知识库。
4. 本范围只定义“要收集什么”，不代表这些规则已经被验证、通过审计或可默认指导。
```

## P0 分区总览

| 分组 | 主题 | 数量 | 主要下游 |
| --- | --- | ---: | --- |
| A | Quant Foundation / 量化基础 | 12 | 策略评估、风险、LLM scoring 标签 |
| B | Data Engineering / 市场数据工程 | 12 | 回测、特征工程、训练样本构造 |
| C | Kline / Strategy Engineering / K线与策略工程 | 12 | 交易决策、策略开发、信号审计 |
| D | Market Microstructure / 市场微观结构 | 12 | 成本、滑点、执行、短周期策略 |
| E | Backtest / 回测可信度 | 12 | 策略验收、反过拟合、SearchLab 回归 |
| F | Replay / Simulation / 回放与模拟 | 12 | 模拟盘、fill model、交易样本可信度 |
| G | Live Execution / Risk Management / 实盘执行与风控 | 12 | 实盘安全、订单状态机、风控闸门 |
| H | Trade Analysis / 交易复盘 | 12 | 交易质量归因、坏例 taxonomy、LLM 标签 |

合计：96 条 P0 待采集知识点。

## A. Quant Foundation / 量化基础 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| Q01 | quant_foundation.expected_value_definition.v1 | KB_01_QUANT_FOUNDATION |
| Q02 | quant_foundation.r_multiple_definition.v1 | KB_01_QUANT_FOUNDATION |
| Q03 | quant_foundation.risk_reward_boundary.v1 | KB_01_QUANT_FOUNDATION |
| Q04 | quant_foundation.cost_adjusted_expectancy_required.v1 | KB_01_QUANT_FOUNDATION |
| Q05 | quant_foundation.win_rate_not_enough.v1 | KB_01_QUANT_FOUNDATION |
| Q06 | quant_foundation.position_sizing_requires_risk_unit.v1 | KB_01_QUANT_FOUNDATION |
| Q07 | quant_foundation.leverage_amplifies_drawdown.v1 | KB_01_QUANT_FOUNDATION |
| Q08 | quant_foundation.signal_decision_execution_separation.v1 | KB_01_QUANT_FOUNDATION |
| Q09 | quant_foundation.trade_frequency_vs_quality_boundary.v1 | KB_01_QUANT_FOUNDATION |
| Q10 | quant_foundation.edge_requires_out_of_sample_evidence.v1 | KB_01_QUANT_FOUNDATION |
| Q11 | quant_foundation.sample_size_and_regime_caveat.v1 | KB_01_QUANT_FOUNDATION |
| Q12 | quant_foundation.no_profit_claim_without_costs.v1 | KB_01_QUANT_FOUNDATION |

## B. Data Engineering / 市场数据工程 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| D01 | data_engineering.timestamp_alignment_required.v1 | KB_02_DATA_ENGINEERING |
| D02 | data_engineering.timezone_policy_required.v1 | KB_02_DATA_ENGINEERING |
| D03 | data_engineering.missing_bar_detection_required.v1 | KB_02_DATA_ENGINEERING |
| D04 | data_engineering.duplicate_event_detection_required.v1 | KB_02_DATA_ENGINEERING |
| D05 | data_engineering.ohlcv_schema_required.v1 | KB_02_DATA_ENGINEERING |
| D06 | data_engineering.feature_timestamp_required.v1 | KB_02_DATA_ENGINEERING |
| D07 | data_engineering.data_versioning_required.v1 | KB_02_DATA_ENGINEERING |
| D08 | data_engineering.symbol_contract_normalization_required.v1 | KB_02_DATA_ENGINEERING |
| D09 | data_engineering.corporate_action_or_contract_rollover_policy.v1 | KB_02_DATA_ENGINEERING |
| D10 | data_engineering.outlier_detection_required.v1 | KB_02_DATA_ENGINEERING |
| D11 | data_engineering.raw_vs_adjusted_data_boundary.v1 | KB_02_DATA_ENGINEERING |
| D12 | data_engineering.data_quality_report_required.v1 | KB_02_DATA_ENGINEERING |

## C. Kline / Strategy Engineering / K线与策略工程 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| K01 | kline_strategy.trend_structure_boundary.v1 | KB_03_STRATEGY_ENGINEERING |
| K02 | kline_strategy.market_structure_requires_timeframe.v1 | KB_03_STRATEGY_ENGINEERING |
| K03 | kline_strategy.entry_signal_not_equal_trade_decision.v1 | KB_03_STRATEGY_ENGINEERING |
| K04 | kline_strategy.stop_loss_requires_invalidation_logic.v1 | KB_03_STRATEGY_ENGINEERING |
| K05 | kline_strategy.take_profit_requires_reachability_check.v1 | KB_03_STRATEGY_ENGINEERING |
| K06 | kline_strategy.multi_timeframe_context_required.v1 | KB_03_STRATEGY_ENGINEERING |
| K07 | kline_strategy.indicator_lag_boundary.v1 | KB_03_STRATEGY_ENGINEERING |
| K08 | kline_strategy.atr_volatility_context_required.v1 | KB_03_STRATEGY_ENGINEERING |
| K09 | kline_strategy.rsi_threshold_not_universal.v1 | KB_03_STRATEGY_ENGINEERING |
| K10 | kline_strategy.volume_confirmation_boundary.v1 | KB_03_STRATEGY_ENGINEERING |
| K11 | kline_strategy.signal_generalization_forbidden_without_market_scope.v1 | KB_03_STRATEGY_ENGINEERING |
| K12 | kline_strategy.strategy_rule_version_required.v1 | KB_03_STRATEGY_ENGINEERING |

## D. Market Microstructure / 市场微观结构 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| M01 | microstructure.spread_liquidity_context_required.v1 | KB_03_STRATEGY_ENGINEERING |
| M02 | microstructure.order_book_depth_boundary.v1 | KB_03_STRATEGY_ENGINEERING |
| M03 | microstructure.trade_prints_aggressor_caveat.v1 | KB_03_STRATEGY_ENGINEERING |
| M04 | microstructure.order_flow_proxy_boundary.v1 | KB_03_STRATEGY_ENGINEERING |
| M05 | microstructure.cvd_interpretation_caveat.v1 | KB_03_STRATEGY_ENGINEERING |
| M06 | microstructure.funding_open_interest_context_required.v1 | KB_03_STRATEGY_ENGINEERING |
| M07 | microstructure.liquidity_regime_required.v1 | KB_03_STRATEGY_ENGINEERING |
| M08 | microstructure.market_impact_cost_required.v1 | KB_03_STRATEGY_ENGINEERING |
| M09 | microstructure.high_frequency_signal_latency_boundary.v1 | KB_03_STRATEGY_ENGINEERING |
| M10 | microstructure.slippage_regime_caveat.v1 | KB_03_STRATEGY_ENGINEERING |
| M11 | microstructure.thin_market_execution_risk.v1 | KB_03_STRATEGY_ENGINEERING |
| M12 | microstructure.microstructure_feature_not_universal.v1 | KB_03_STRATEGY_ENGINEERING |

## E. Backtest / 回测可信度 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| B01 | backtest.lookahead_bias_block.v1 | KB_04_BACKTEST |
| B02 | backtest.data_leakage_block.v1 | KB_04_BACKTEST |
| B03 | backtest.survivorship_selection_bias_check.v1 | KB_04_BACKTEST |
| B04 | backtest.parameter_search_separate_from_final_eval.v1 | KB_04_BACKTEST |
| B05 | backtest.walk_forward_validation_required.v1 | KB_04_BACKTEST |
| B06 | backtest.out_of_sample_required.v1 | KB_04_BACKTEST |
| B07 | backtest.cost_model_required.v1 | KB_04_BACKTEST |
| B08 | backtest.slippage_fee_spread_required.v1 | KB_04_BACKTEST |
| B09 | backtest.metric_interpretation_boundary.v1 | KB_04_BACKTEST |
| B10 | backtest.profit_factor_drawdown_context_required.v1 | KB_04_BACKTEST |
| B11 | backtest.reproducibility_package_required.v1 | KB_04_BACKTEST |
| B12 | backtest.strategy_version_and_data_version_required.v1 | KB_04_BACKTEST |

## F. Replay / Simulation / 回放与模拟 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| R01 | replay.event_clock_required.v1 | KB_05_REPLAY_SIMULATION |
| R02 | replay.ohlc_same_bar_tp_sl_ordering_required.v1 | KB_05_REPLAY_SIMULATION |
| R03 | replay.fill_model_assumption_required.v1 | KB_05_REPLAY_SIMULATION |
| R04 | replay.partial_fill_policy_required.v1 | KB_05_REPLAY_SIMULATION |
| R05 | replay.latency_model_required.v1 | KB_05_REPLAY_SIMULATION |
| R06 | replay.paper_trading_not_equal_live.v1 | KB_05_REPLAY_SIMULATION |
| R07 | replay.exchange_rule_simulation_required.v1 | KB_05_REPLAY_SIMULATION |
| R08 | replay.minimum_order_size_required.v1 | KB_05_REPLAY_SIMULATION |
| R09 | replay.order_reject_and_cancel_policy_required.v1 | KB_05_REPLAY_SIMULATION |
| R10 | replay.simulation_live_gap_report_required.v1 | KB_05_REPLAY_SIMULATION |
| R11 | replay.tick_replay_vs_ohlc_boundary.v1 | KB_05_REPLAY_SIMULATION |
| R12 | replay.execution_cost_consistency_required.v1 | KB_05_REPLAY_SIMULATION |

## G. Live Execution / Risk Management / 实盘执行与风控 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| L01 | live_execution.least_privilege_api_required.v1 | KB_06_LIVE_EXECUTION |
| L02 | live_execution.order_state_machine_required.v1 | KB_06_LIVE_EXECUTION |
| L03 | live_execution.position_reconciliation_required.v1 | KB_06_LIVE_EXECUTION |
| L04 | live_execution.kill_switch_required.v1 | KB_06_LIVE_EXECUTION |
| L05 | live_execution.exchange_adapter_error_contract_required.v1 | KB_06_LIVE_EXECUTION |
| L06 | live_execution.order_fill_trade_log_required.v1 | KB_06_LIVE_EXECUTION |
| L07 | risk_management.single_trade_risk_limit_required.v1 | KB_07_RISK_MANAGEMENT |
| L08 | risk_management.daily_loss_limit_required.v1 | KB_07_RISK_MANAGEMENT |
| L09 | risk_management.max_open_positions_required.v1 | KB_07_RISK_MANAGEMENT |
| L10 | risk_management.portfolio_exposure_limit_required.v1 | KB_07_RISK_MANAGEMENT |
| L11 | risk_management.consecutive_loss_stop_required.v1 | KB_07_RISK_MANAGEMENT |
| L12 | risk_management.hard_risk_gate_precedes_execution.v1 | KB_07_RISK_MANAGEMENT |

## H. Trade Analysis / 交易复盘 P0

| ID | 知识点 | 归属节点 |
| --- | --- | --- |
| T01 | trade_analysis.planned_vs_realized_r_required.v1 | KB_08_TRADE_ANALYSIS |
| T02 | trade_analysis.mae_mfe_for_post_trade_only.v1 | KB_08_TRADE_ANALYSIS |
| T03 | trade_analysis.bad_trade_taxonomy_required.v1 | KB_08_TRADE_ANALYSIS |
| T04 | trade_analysis.good_loss_bad_win_distinction.v1 | KB_08_TRADE_ANALYSIS |
| T05 | trade_analysis.entry_quality_review_required.v1 | KB_08_TRADE_ANALYSIS |
| T06 | trade_analysis.exit_quality_review_required.v1 | KB_08_TRADE_ANALYSIS |
| T07 | trade_analysis.risk_quality_review_required.v1 | KB_08_TRADE_ANALYSIS |
| T08 | trade_analysis.execution_quality_review_required.v1 | KB_08_TRADE_ANALYSIS |
| T09 | trade_analysis.rule_compliance_review_required.v1 | KB_08_TRADE_ANALYSIS |
| T10 | trade_analysis.regime_fit_review_required.v1 | KB_08_TRADE_ANALYSIS |
| T11 | trade_analysis.reason_code_required.v1 | KB_08_TRADE_ANALYSIS |
| T12 | trade_analysis.research_hypothesis_requires_validation.v1 | KB_08_TRADE_ANALYSIS |

## 后续采集要求

每个知识点进入候选前必须满足：

```text
1. 至少 2 个来源，优先官方文档、交易所规则、学术论文、权威书籍、成熟开源框架文档。
2. 必须声明适用范围、不适用场景、假设、风险、冲突处理。
3. 不得把交易建议、具体买卖点、项目私有参数写成通用规则。
4. 有争议的技术分析或策略知识必须标注证据级别和市场/周期/样本边界。
5. 回测、回放、模拟盘、实盘执行相关知识必须明确数据时钟、成本、滑点、延迟和状态机边界。
6. 所有候选必须先进入 candidate，不能直接进入 reviewed 或 approved。
```

## 下游联动

```text
知识树：展示 Trading Engineering 主枝下的 L2/L3 节点和知识数量。
SearchLab：按 canonical_node_id、domain、subdomain、machine_gate 过滤检索。
MCP：只读检索，返回来源、review 状态、machine_gate，不写知识。
FastAPI：给 Vue3 提供只读知识树、候选、正式知识和审计摘要。
Vue3：在知识树和候选页区分待采集、candidate、reviewed、approved。
AI Engineering：通过 knowledge_refs 引用这些交易知识，不复制规则本体。
```
