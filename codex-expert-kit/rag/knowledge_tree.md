# CEK-TA Knowledge Tree

This file defines the first-version professional knowledge tree for CEK-TA.

It is a taxonomy and audit scaffold, not a collection of approved trading rules. Detailed professional claims must still be created as source-backed knowledge items.

## Tree Contract

```text
schema: codex-expert-kit/rag/knowledge_tree_schema.md
root_node_id: kt
version: 1.0.0
encoding: UTF-8
created_at: 2026-06-08
updated_at: 2026-06-08
```

## Global Mapping Rules

```text
1. Every accepted knowledge item should map to exactly one primary tree node.
2. A knowledge item may list related_nodes for secondary navigation.
3. Market, asset, timeframe, data_granularity, and project_type remain applicability fields, not separate first-version root trees.
4. A node can be reviewed before its mapped knowledge is fully covered.
5. Node coverage must not imply investment advice or live-trading permission.
6. AI Engineering may reference trading knowledge, but K-line, strategy, backtest, replay, simulation, execution, risk, and trade-analysis rules must live in Trading Engineering branches as their primary nodes.
```

## Root

```yaml
node_id: kt
parent_id: null
path: CEK-TA
title: CEK-TA Knowledge Tree
domain: root
subdomain: root
level: 0
summary: Root node for reusable trading engineering, quantitative research, execution, RAG, MCP, and LLM training knowledge.
key_concepts:
  - reusable knowledge
  - auditability
  - source-backed rules
expected_knowledge_types:
  - schema
coverage_status: partial
review_status: reviewed
freshness_status: stable
conflict_status: none
source_policy:
  required: false
  preferred_source_types: []
  minimum_reliability: medium
related_nodes: []
```

## Level 1 Nodes

```yaml
- node_id: kt.trading_engineering
  parent_id: kt
  path: CEK-TA / Trading Engineering
  title: Trading Engineering
  domain: quant_trading
  subdomain: trading_engineering
  level: 1
  summary: End-to-end reusable knowledge for strategy design, market data, backtest, replay, simulation, execution, risk, and trade analysis.
  key_concepts: [strategy, market data, backtest, execution, risk, trade analysis]
  expected_knowledge_types: [definition, principle, procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked
  source_policy:
    required: true
    preferred_source_types: [paper, book, official_doc, framework_doc, engineering_article]
    minimum_reliability: medium

- node_id: kt.ai_engineering
  parent_id: kt
  path: CEK-TA / AI Engineering
  title: AI Engineering
  domain: rag_engineering
  subdomain: ai_engineering
  level: 1
  summary: Reusable knowledge for RAG, MCP, LLM dataset design, evaluation, training loops, deployment, and AI governance. Trading rules may be referenced here, but their primary nodes belong to Trading Engineering.
  key_concepts: [RAG, MCP, dataset, eval, SFT, deployment, governance, boundary]
  expected_knowledge_types: [schema, procedure, checklist, eval_case, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  source_policy:
    required: true
    preferred_source_types: [official_doc, framework_doc, paper, engineering_article]
    minimum_reliability: medium

- node_id: kt.project_integration
  parent_id: kt
  path: CEK-TA / Project Integration
  title: Project Integration
  domain: project_runbooks
  subdomain: project_integration
  level: 1
  summary: Knowledge for connecting external projects, keeping project facts separate, running health checks, and contributing sanitized knowledge back.
  key_concepts: [Project Adapter, AGENTS.md, healthcheck, contribution, sanitization]
  expected_knowledge_types: [schema, procedure, checklist, adapter_rule]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none
  source_policy:
    required: true
    preferred_source_types: [runbook, task_card, code_doc, internal_report]
    minimum_reliability: medium
```

## Trading Engineering Branch

```yaml
- node_id: kt.quant_foundation
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Quant Foundation
  title: Quant Foundation
  domain: quant_trading
  subdomain: foundation
  level: 2
  summary: General trading system concepts: signal separation, expected value, risk-reward, costs, sizing, and decision flow.
  key_concepts: [signal, decision, EV, R multiple, cost, sizing]
  expected_knowledge_types: [definition, principle, formula, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_01_QUANT_FOUNDATION
    allowed_domains: [quant_trading]
    allowed_subdomains: [foundation, signal_flow, sizing, risk_reward, cost, risk_normalized_metrics]

- node_id: kt.quant_foundation.signal_flow
  parent_id: kt.quant_foundation
  path: CEK-TA / Trading Engineering / Quant Foundation / Signal Flow
  title: Signal Flow
  domain: quant_trading
  subdomain: signal_flow
  level: 3
  summary: Separation of market events, features, signals, decisions, order intents, execution reports, and trade results.
  key_concepts: [MarketEvent, FeatureFrame, SignalFrame, Decision, OrderIntent, ExecutionReport, TradeResult]
  expected_knowledge_types: [definition, schema, procedure, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none

- node_id: kt.quant_foundation.position_sizing
  parent_id: kt.quant_foundation
  path: CEK-TA / Trading Engineering / Quant Foundation / Position Sizing
  title: Position Sizing
  domain: quant_trading
  subdomain: position_sizing
  level: 3
  summary: Reusable sizing concepts, risk units, exposure limits, and failure modes.
  key_concepts: [risk per trade, exposure, leverage, drawdown, Kelly caveats]
  expected_knowledge_types: [principle, formula, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.quant_foundation.risk_normalized_metrics
  parent_id: kt.quant_foundation
  path: CEK-TA / Trading Engineering / Quant Foundation / Risk Normalized Metrics
  title: Risk Normalized Metrics
  domain: quant_trading
  subdomain: risk_normalized_metrics
  level: 3
  summary: Risk-unit normalized trade result metrics such as R-multiple, expectancy in R, and audit boundaries for comparing trade outcomes without replacing costs, slippage, drawdown, sample-size, or out-of-sample checks.
  key_concepts: [R multiple, initial risk, risk unit, expectancy in R, trade result normalization]
  expected_knowledge_types: [definition, formula, boundary_rule, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.trading_engineering.data_engineering
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Data Engineering
  title: Data Engineering
  domain: trading_engineering
  subdomain: data_engineering
  level: 2
  summary: Market data engineering rules for timestamp alignment, timezone policy, missing and duplicate records, OHLCV schemas, feature availability, data versioning, symbol normalization, adjustments, outlier checks, raw/adjusted boundaries, and data quality reports.
  key_concepts: [timestamp, timezone, missing bar, duplicate event, OHLCV, feature timestamp, data version, symbol normalization, adjustment, outlier, raw data, data quality report]
  expected_knowledge_types: [schema, data_quality_rule, procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none
  item_mapping:
    partition_id: KB_02_DATA_ENGINEERING
    allowed_domains: [trading_engineering]
    allowed_subdomains: [timestamp_alignment, timezone_policy, data_quality, ohlcv_schema, feature_timestamp, data_versioning, symbology, adjustment_rollover, raw_adjusted_boundary, data_quality_report]

- node_id: kt.trading_engineering.data_engineering.audit_clock
  parent_id: kt.trading_engineering.data_engineering
  path: CEK-TA / Trading Engineering / Data Engineering / Audit Clock And Event Time
  title: Audit Clock And Event Time
  domain: trading_engineering
  subdomain: audit_clock
  level: 3
  summary: Business-clock synchronization, event timestamp granularity, order-event causality, idempotency, and audit time boundaries for trading data.
  key_concepts: [clock sync, UTC, timestamp granularity, event causality, idempotency, audit trail]
  expected_knowledge_types: [regulatory_rule_summary, schema, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_engineering.data_engineering.reference_data_entitlement
  parent_id: kt.trading_engineering.data_engineering
  path: CEK-TA / Trading Engineering / Data Engineering / Reference Data And Entitlement
  title: Reference Data And Entitlement
  domain: trading_engineering
  subdomain: reference_data_entitlement
  level: 3
  summary: Market-data entitlement, point-in-time instrument definitions, tick size, lot size, price limit metadata, coverage universe, and vendor schema version boundaries.
  key_concepts: [market data license, instrument definition, tick size, lot size, price limit, coverage universe, vendor schema]
  expected_knowledge_types: [schema, data_quality_rule, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.kline_strategy
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Kline Strategy
  title: Kline Strategy
  domain: kline_strategy
  subdomain: kline_strategy
  level: 2
  summary: K-line structure, multi-timeframe analysis, entry/exit design, indicator boundaries, and setup validation.
  key_concepts: [trend, structure, breakout, pullback, reversal, ATR, RSI, volume]
  expected_knowledge_types: [definition, principle, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_02_KLINE_STRATEGY
    allowed_domains: [kline_strategy]
    allowed_subdomains: [trend, setup, indicator, risk_reward, multi_timeframe]

- node_id: kt.kline_strategy.market_structure
  parent_id: kt.kline_strategy
  path: CEK-TA / Trading Engineering / Kline Strategy / Market Structure
  title: Market Structure
  domain: kline_strategy
  subdomain: market_structure
  level: 3
  summary: Higher high/lower low structure, ranges, trend breaks, support/resistance, and invalidation logic.
  key_concepts: [trend structure, range, support, resistance, invalidation]
  expected_knowledge_types: [definition, principle, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.kline_strategy.entry_exit
  parent_id: kt.kline_strategy
  path: CEK-TA / Trading Engineering / Kline Strategy / Entry And Exit
  title: Entry And Exit
  domain: kline_strategy
  subdomain: entry_exit
  level: 3
  summary: Breakout, pullback, continuation, reversal, stop-loss invalidation, and take-profit reachability.
  key_concepts: [entry trigger, stop loss, take profit, invalidation, reachability]
  expected_knowledge_types: [principle, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.kline_strategy.indicators
  parent_id: kt.kline_strategy
  path: CEK-TA / Trading Engineering / Kline Strategy / Indicator Boundaries
  title: Indicator Boundaries
  domain: kline_strategy
  subdomain: indicators
  level: 3
  summary: Proper and improper use of ATR, RSI, moving averages, volume, and derived indicators under explicit market/timeframe assumptions.
  key_concepts: [ATR, RSI, moving average, volume, lag, threshold]
  expected_knowledge_types: [definition, principle, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.market_microstructure
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Market Microstructure
  title: Market Microstructure
  domain: market_microstructure
  subdomain: market_microstructure
  level: 2
  summary: Order flow, liquidity, spread, order book, trade prints, and microstructure feature caveats.
  key_concepts: [order book, spread, liquidity, order flow, CVD, OFI]
  expected_knowledge_types: [definition, principle, procedure, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_03_MARKET_MICROSTRUCTURE
    allowed_domains: [market_microstructure]
    allowed_subdomains: [order_flow, liquidity, order_book, trade_prints, funding_open_interest]

- node_id: kt.market_microstructure.order_flow
  parent_id: kt.market_microstructure
  path: CEK-TA / Trading Engineering / Market Microstructure / Order Flow
  title: Order Flow
  domain: market_microstructure
  subdomain: order_flow
  level: 3
  summary: Interpretation boundaries for OFI, CVD, aggressive trades, and order-flow proxies.
  key_concepts: [OFI, CVD, aggressive trade, proxy, causality]
  expected_knowledge_types: [definition, principle, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.market_microstructure.crypto_perpetual
  parent_id: kt.market_microstructure
  path: CEK-TA / Trading Engineering / Market Microstructure / Crypto Perpetual
  title: Crypto Perpetual Market Structure
  domain: market_microstructure
  subdomain: crypto_perpetual
  level: 3
  summary: Crypto perpetual-specific market structure boundaries including mark price, index price, last price, funding interval, exchange outages, and venue-specific caveats.
  key_concepts: [mark price, index price, last price, funding, perpetual swap, venue outage]
  expected_knowledge_types: [definition, official_rule_summary, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.backtest
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Backtest
  title: Backtest
  domain: backtest
  subdomain: backtest
  level: 2
  summary: Credibility, data quality, bias detection, metrics, cost modeling, and reproducibility for strategy backtests.
  key_concepts: [bias, data quality, metric, slippage, fee, reproducibility]
  expected_knowledge_types: [definition, principle, procedure, checklist, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_04_BACKTEST
    allowed_domains: [backtest]
    allowed_subdomains: [bias, data_quality, metrics, cost_model, reproducibility]

- node_id: kt.backtest.bias
  parent_id: kt.backtest
  path: CEK-TA / Trading Engineering / Backtest / Bias
  title: Backtest Bias
  domain: backtest
  subdomain: bias
  level: 3
  summary: Lookahead, survivorship, selection, leakage, overfitting, and hidden parameter search risks.
  key_concepts: [lookahead, survivorship, leakage, overfitting, selection bias]
  expected_knowledge_types: [definition, checklist, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.backtest.data_quality
  parent_id: kt.backtest
  path: CEK-TA / Trading Engineering / Backtest / Data Quality
  title: Data Quality
  domain: backtest
  subdomain: data_quality
  level: 3
  summary: Missing bars, duplicate events, timezone errors, corporate actions, symbol continuity, and sample definition.
  key_concepts: [missing data, duplicate, timezone, corporate action, sample]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.backtest.metrics
  parent_id: kt.backtest
  path: CEK-TA / Trading Engineering / Backtest / Metrics
  title: Backtest Metrics
  domain: backtest
  subdomain: metrics
  level: 3
  summary: Interpretation boundaries for win rate, profit factor, drawdown, expectancy, R multiples, and cost impact.
  key_concepts: [win rate, profit factor, max drawdown, expectancy, R multiple]
  expected_knowledge_types: [definition, formula, principle, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked

- node_id: kt.replay_simulation
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Replay And Simulation
  title: Replay And Simulation
  domain: replay_simulation
  subdomain: replay_simulation
  level: 2
  summary: Event replay, simulation clock, fill models, paper trading fidelity, latency, and live-readiness gaps.
  key_concepts: [event replay, simulation clock, fill model, latency, paper trading]
  expected_knowledge_types: [schema, principle, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: stable
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_05_REPLAY_SIMULATION
    allowed_domains: [replay_simulation]
    allowed_subdomains: [replay_clock, fill_model, paper_trading, latency, live_gap]

- node_id: kt.replay_simulation.fill_model
  parent_id: kt.replay_simulation
  path: CEK-TA / Trading Engineering / Replay And Simulation / Fill Model
  title: Fill Model
  domain: replay_simulation
  subdomain: fill_model
  level: 3
  summary: Deterministic fill assumptions, same-candle TP/SL ordering, partial fills, slippage, and fee modeling.
  key_concepts: [fill, same-candle, slippage, fee, partial fill]
  expected_knowledge_types: [principle, procedure, schema, anti_pattern, eval_case]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: potential

- node_id: kt.replay_simulation.order_semantics
  parent_id: kt.replay_simulation
  path: CEK-TA / Trading Engineering / Replay And Simulation / Order Semantics
  title: Simulated Order Semantics
  domain: replay_simulation
  subdomain: order_semantics
  level: 3
  summary: Simulation boundaries for order type, time-in-force, post-only, reduce-only, maker/taker, self-trade prevention, and venue-specific order behavior.
  key_concepts: [order type, TIF, post only, reduce only, maker taker, self-trade prevention]
  expected_knowledge_types: [schema, principle, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.live_execution
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Live Execution
  title: Live Execution
  domain: live_trading
  subdomain: live_execution
  level: 2
  summary: Live readiness, order state machines, exchange adapters, reconciliation, kill switches, and incident response.
  key_concepts: [order state, exchange adapter, reconciliation, kill switch, incident]
  expected_knowledge_types: [official_rule_summary, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_06_LIVE_EXECUTION
    allowed_domains: [live_trading]
    allowed_subdomains: [order_state, exchange_adapter, risk_control, reconciliation, incident_response]

- node_id: kt.live_execution.risk_control
  parent_id: kt.live_execution
  path: CEK-TA / Trading Engineering / Live Execution / Risk Control
  title: Live Risk Control
  domain: live_trading
  subdomain: risk_control
  level: 3
  summary: Risk gates, kill switches, max loss controls, live permission boundaries, and emergency stop procedures.
  key_concepts: [risk gate, kill switch, max loss, permission, emergency stop]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_engineering.execution_tca
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Execution TCA
  title: Execution TCA
  domain: live_trading
  subdomain: execution_tca
  level: 3
  summary: Execution cost decomposition, implementation shortfall, benchmark selection, routing context, and algorithmic execution boundaries.
  key_concepts: [TCA, implementation shortfall, benchmark, VWAP, TWAP, market impact, opportunity cost]
  expected_knowledge_types: [definition, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_engineering.trade_audit
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Trade Audit
  title: Execution Audit Trail
  domain: live_trading
  subdomain: audit_trail
  level: 3
  summary: Client/exchange order-id mapping, order-event traceability, electronic/manual order timestamp boundaries, retention, and integrity checks.
  key_concepts: [audit trail, client order id, exchange order id, event sequence, timestamp, retention]
  expected_knowledge_types: [schema, regulatory_rule_summary, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_engineering.resilience_incident_log
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Resilience Incident Log
  title: Resilience And Incident
  domain: live_trading
  subdomain: resilience_incident
  level: 3
  summary: Business continuity, disaster recovery, degraded or read-only modes, failover, recovery replay, incident taxonomy, and post-incident review.
  key_concepts: [BCDR, degraded mode, readonly mode, failover, incident, post incident review]
  expected_knowledge_types: [procedure, checklist, incident_taxonomy, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_engineering.order_semantics
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Order Semantics
  title: Live Order Semantics
  domain: live_trading
  subdomain: order_semantics
  level: 3
  summary: Live venue-specific semantics for order type, time-in-force, post-only, reduce-only, self-trade prevention, maker/taker fees, and exchange constraints.
  key_concepts: [order type, TIF, post only, reduce only, STP, maker taker fee]
  expected_knowledge_types: [official_rule_summary, schema, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.risk_management
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Risk Management
  title: Risk Management
  domain: risk_management
  subdomain: risk_management
  level: 2
  summary: Single-trade risk, daily loss limits, portfolio exposure, open-position limits, consecutive-loss stops, and pre-trade hard risk gates.
  key_concepts: [single trade risk, daily loss, exposure, open positions, hard gate]
  expected_knowledge_types: [official_rule_summary, procedure, checklist, anti_pattern, schema]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_07_RISK_MANAGEMENT
    allowed_domains: [risk_management]
    allowed_subdomains: [single_trade_risk, daily_loss, position_limit, exposure_limit, loss_streak, hard_gate]

- node_id: kt.risk_management.pre_trade_gates
  parent_id: kt.risk_management
  path: CEK-TA / Trading Engineering / Risk Management / Pre-trade Risk Gates
  title: Pre-trade Risk Gates
  domain: risk_management
  subdomain: hard_gate
  level: 3
  summary: Deterministic risk checks that must run before order submission, including size, exposure, loss, permissions, and emergency blocking.
  key_concepts: [pre-trade risk, deterministic gate, max size, exposure, kill switch]
  expected_knowledge_types: [procedure, checklist, schema, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.risk_management.layered_controls
  parent_id: kt.risk_management
  path: CEK-TA / Trading Engineering / Risk Management / Layered Controls
  title: Layered Risk Controls
  domain: risk_management
  subdomain: layered_controls
  level: 3
  summary: Layered pre-trade controls, credit limits, max order size, price collars, message throttles, margin/collateral boundaries, and post-trade surveillance separation.
  key_concepts: [pre-trade control, credit limit, price collar, message throttle, margin, surveillance]
  expected_knowledge_types: [regulatory_rule_summary, schema, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.risk_management.stress_scenario
  parent_id: kt.risk_management
  path: CEK-TA / Trading Engineering / Risk Management / Stress And Scenario
  title: Stress And Scenario Risk
  domain: risk_management
  subdomain: stress_scenario
  level: 3
  summary: Stress testing, liquidity stress, correlation breakdown, gap and overnight risk, tail-loss review, and scenario limitations.
  key_concepts: [stress test, scenario, liquidity stress, correlation breakdown, gap risk, tail loss]
  expected_knowledge_types: [procedure, checklist, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.risk_management.crypto_perpetual_risk
  parent_id: kt.risk_management
  path: CEK-TA / Trading Engineering / Risk Management / Crypto Perpetual Risk
  title: Crypto Perpetual Risk
  domain: risk_management
  subdomain: crypto_perpetual_risk
  level: 3
  summary: Crypto perpetual-specific risk boundaries for funding, maintenance margin, liquidation, auto-deleveraging, insurance funds, outages, and clawback caveats.
  key_concepts: [funding, maintenance margin, liquidation, ADL, insurance fund, clawback]
  expected_knowledge_types: [official_rule_summary, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trade_analysis
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Trade Analysis
  title: Trade Analysis
  domain: trade_analysis
  subdomain: trade_analysis
  level: 2
  summary: Trade quality, bad-case taxonomy, realized versus planned R, timing errors, and strategy iteration loops.
  key_concepts: [bad case, realized R, MAE, MFE, timing, iteration]
  expected_knowledge_types: [definition, procedure, checklist, eval_case, taxonomy]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none
  item_mapping:
    partition_id: KB_07_TRADE_ANALYSIS
    allowed_domains: [trade_analysis]
    allowed_subdomains: [bad_case, trade_quality, realized_r, timing, iteration_loop]

- node_id: kt.trade_analysis.bad_case_taxonomy
  parent_id: kt.trade_analysis
  path: CEK-TA / Trading Engineering / Trade Analysis / Bad Case Taxonomy
  title: Bad Case Taxonomy
  domain: trade_analysis
  subdomain: bad_case_taxonomy
  level: 3
  summary: Generic labels for poor trades, avoidable losses, missed exits, invalid entries, noise stops, and execution failures.
  key_concepts: [bad trade, label, avoidable loss, missed exit, noise stop]
  expected_knowledge_types: [taxonomy, definition, checklist, eval_case]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none

- node_id: kt.trade_analysis.execution_tca_review
  parent_id: kt.trade_analysis
  path: CEK-TA / Trading Engineering / Trade Analysis / Execution TCA Review
  title: Execution TCA Review
  domain: trade_analysis
  subdomain: execution_tca_review
  level: 3
  summary: Post-trade execution quality review, benchmark context, implementation shortfall decomposition, routing context, and algorithmic execution caveats.
  key_concepts: [execution quality, TCA review, benchmark, implementation shortfall, routing, algorithmic execution]
  expected_knowledge_types: [procedure, checklist, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_engineering.market_conduct
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Market Conduct
  title: Market Conduct
  domain: trading_engineering
  subdomain: market_conduct
  level: 2
  summary: Market conduct surveillance taxonomy, alert review, jurisdiction caveats, and manual escalation boundaries for trading systems.
  key_concepts: [spoofing, layering, wash trade, momentum ignition, surveillance taxonomy, manual review]
  expected_knowledge_types: [regulatory_rule_summary, taxonomy, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_08_TRADE_ANALYSIS
    allowed_domains: [trading_engineering]
    allowed_subdomains: [market_conduct, surveillance_taxonomy, alert_review_workflow]

- node_id: kt.trading_engineering.market_conduct.surveillance_taxonomy
  parent_id: kt.trading_engineering.market_conduct
  path: CEK-TA / Trading Engineering / Market Conduct / Surveillance Taxonomy
  title: Surveillance Taxonomy
  domain: trading_engineering
  subdomain: market_conduct
  level: 3
  summary: Surveillance labels and reason-code boundaries for spoofing, layering, wash/self-trade, momentum ignition, marking the close, and front-running without turning labels into legal findings or hard gates.
  key_concepts: [surveillance label, reason code, legal owner, manual escalation, evidence]
  expected_knowledge_types: [taxonomy, boundary_rule, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.trading_engineering.market_access
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Market Access
  title: Market Access
  domain: live_trading
  subdomain: market_access
  level: 2
  summary: Market access, DEA, sponsored access, pre-trade controls, jurisdiction caveats, recordkeeping, and owner boundaries.
  key_concepts: [market access, DEA, sponsored access, pre-trade control, recordkeeping, jurisdiction]
  expected_knowledge_types: [regulatory_rule_summary, checklist, boundary_rule, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_06_LIVE_EXECUTION
    allowed_domains: [live_trading, trading_engineering]
    allowed_subdomains: [market_access, regulatory_boundary, direct_electronic_access]

- node_id: kt.trading_engineering.market_access.regulatory_boundary
  parent_id: kt.trading_engineering.market_access
  path: CEK-TA / Trading Engineering / Market Access / Regulatory Boundary
  title: Regulatory Boundary
  domain: live_trading
  subdomain: market_access
  level: 3
  summary: Jurisdiction-specific market access and DEA control evidence boundaries; not a legal opinion, compliance satisfaction statement, threshold rule, or trading permission.
  key_concepts: [SEC 15c3-5, MiFID II, DEA, control evidence, owner boundary]
  expected_knowledge_types: [regulatory_rule_summary, boundary_rule, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.trading_engineering.audit_trace
  parent_id: kt.trading_engineering
  path: CEK-TA / Trading Engineering / Audit Trace
  title: Audit Trace
  domain: trading_engineering
  subdomain: audit_trace
  level: 2
  summary: Audit trace, timestamp ordering, clock source, synchronization status, drift policy, event causality, and cross-system trace references.
  key_concepts: [audit trace, clock source, sync status, timestamp precision, drift, event ordering]
  expected_knowledge_types: [schema, checklist, boundary_rule, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_06_LIVE_EXECUTION
    allowed_domains: [trading_engineering, live_trading]
    allowed_subdomains: [audit_trace, time_synchronization, event_ordering]

- node_id: kt.trading_engineering.audit_trace.time_synchronization
  parent_id: kt.trading_engineering.audit_trace
  path: CEK-TA / Trading Engineering / Audit Trace / Time Synchronization
  title: Time Synchronization
  domain: trading_engineering
  subdomain: audit_trace
  level: 3
  summary: Clock source, sync status, timestamp precision, timezone, drift policy, last sync evidence, and ordering caveats for market data, orders, fills, risk events, model inference, and RAG/MCP audit logs.
  key_concepts: [clock sync, timestamp precision, drift policy, ordering unknown, audit evidence]
  expected_knowledge_types: [schema, checklist, boundary_rule, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none
```

## AI Engineering Branch

```yaml
- node_id: kt.ai_engineering.llm_training
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / LLM Training
  title: LLM Training
  domain: llm_training
  subdomain: llm_training
  level: 2
  summary: General model training engineering, trade-data-to-training-schema conversion, trading LLM task taxonomy, method selection, and trading-specific scoring/gating constraints.
  key_concepts: [training objective, dataset, SFT, DPO, eval, trade schema, task taxonomy, method selection, scoring, gating]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_09_LLM_TRAINING
    allowed_domains: [llm_training]
    allowed_subdomains: [model_training_engineering, training_dataset_schema_engineering, trading_llm_task_taxonomy, training_method_selection, trading_scoring_gating_training, dataset, sft, dpo, eval, preference, training_serving_consistency]

- node_id: kt.ai_engineering.llm_training.model_training_engineering
  parent_id: kt.ai_engineering.llm_training
  path: CEK-TA / AI Engineering / LLM Training / Model Training Engineering
  title: Model Training Engineering
  domain: llm_training
  subdomain: model_training_engineering
  level: 3
  summary: General LLM/ML training engineering: task definition, dataset construction, leakage prevention, SFT, DPO, PEFT, evals, run management, safety, and training-serving consistency.
  key_concepts: [task definition, dataset card, leakage, SFT, DPO, LoRA, eval, run config, training-serving skew]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_training.trading_scoring_gating_training
  parent_id: kt.ai_engineering.llm_training
  path: CEK-TA / AI Engineering / LLM Training / Trading Scoring And Gating Training
  title: Trading Scoring And Gating Training
  domain: llm_training
  subdomain: trading_scoring_gating_training
  level: 3
  summary: Trading-specific LLM training boundaries for trade candidate schema, labels, leakage controls, scoring rubrics, calibration, and risk gate behavior.
  key_concepts: [trade candidate, label leakage, R/R, false allow, false block, calibration, hard risk gate]
  expected_knowledge_types: [schema, procedure, checklist, eval_case, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_training.eval_and_risk
  parent_id: kt.ai_engineering.llm_training
  path: CEK-TA / AI Engineering / LLM Training / Eval And Risk
  title: Eval And Risk
  domain: llm_training
  subdomain: eval_and_risk
  level: 3
  summary: LLM/RAG evaluation and risk boundaries for source-backed outputs, unsupported claim handling, human escalation, and trading-project safety caveats.
  key_concepts: [eval, unsupported claim, source boundary, human escalation, risk caveat]
  expected_knowledge_types: [eval_case, boundary_rule, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.ai_engineering.hybrid_scoring
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Hybrid Scoring
  title: Hybrid Scoring
  domain: ai_engineering
  subdomain: hybrid_scoring
  level: 2
  summary: Hybrid scoring architecture for combining tabular/statistical scorers, calibration, Qwen-style audit explanation, RAG citations, and deterministic final gates without turning language models into numeric scorers.
  key_concepts: [tabular scorer, calibration, Qwen audit assistant, final gate, reason code]
  expected_knowledge_types: [architecture_rule, schema, boundary_rule, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none
  item_mapping:
    partition_id: KB_AI_ENGINEERING
    allowed_domains: [ai_engineering]
    allowed_subdomains: [hybrid_scoring, numeric_scoring, calibration_threshold, llm_audit_assistant, final_gate]

- node_id: kt.ai_engineering.numeric_scoring
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Numeric Scoring And Meta Labeling
  title: Numeric Scoring And Meta Labeling
  domain: llm_training
  subdomain: numeric_scoring
  level: 2
  summary: Numeric scoring, risk ranking, meta-labeling, model comparison, review priority, and scorer-not-executor boundaries for trading AI POC systems.
  key_concepts: [numeric scorer, meta labeling, logistic regression, LightGBM, XGBoost, CatBoost, review priority]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_20_NUMERIC_SCORING
    allowed_domains: [llm_training, ai_governance]
    allowed_subdomains: [numeric_scoring, meta_labeling, model_selection, scorer_boundary, review_priority]

- node_id: kt.ai_engineering.numeric_scoring.model_family_selection
  parent_id: kt.ai_engineering.numeric_scoring
  path: CEK-TA / AI Engineering / Numeric Scoring And Meta Labeling / Model Family Selection
  title: Model Family Selection
  domain: llm_training
  subdomain: model_family_selection
  level: 3
  summary: Model-family selection for trading numeric scoring: rule baseline, Logistic Regression, LightGBM, XGBoost, and CatBoost must be compared with time-aware validation, calibration, business cost, latency, and governance boundaries.
  key_concepts: [rule baseline, Logistic Regression, LightGBM, XGBoost, CatBoost, model comparison]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.numeric_scoring.tabular_scorer_training
  parent_id: kt.ai_engineering.numeric_scoring
  path: CEK-TA / AI Engineering / Numeric Scoring And Meta Labeling / Tabular Scorer Training
  title: Tabular Scorer Training
  domain: llm_training
  subdomain: tabular_scorer_training
  level: 3
  summary: Training rules for tabular scorers in trading gating/scoring systems: class imbalance, sample weights, time split, HPO leakage controls, category handling, and scorer-not-executor boundaries.
  key_concepts: [class imbalance, sample weight, time split, HPO, leakage control, scorer boundary]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.numeric_scoring.scorer_explainability
  parent_id: kt.ai_engineering.numeric_scoring
  path: CEK-TA / AI Engineering / Numeric Scoring And Meta Labeling / Scorer Explainability
  title: Scorer Explainability
  domain: llm_training
  subdomain: scorer_explainability
  level: 3
  summary: Explainability boundaries for trading numeric scorers: SHAP, feature importance, local/global explanations, non-causal interpretation, audit usage, and unsupported trading-claim blocking.
  key_concepts: [SHAP, feature importance, explanation boundary, non-causal, audit only]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.calibration_threshold
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Calibration And Threshold Policy
  title: Calibration And Threshold Policy
  domain: llm_training
  subdomain: calibration_threshold
  level: 2
  summary: Probability calibration, independent calibration holdout, Brier/ECE checks, cost matrix, threshold policy, and false allow/false block governance.
  key_concepts: [calibration, Brier score, ECE, cost matrix, threshold policy, false allow, false block]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_21_CALIBRATION_THRESHOLD
    allowed_domains: [llm_training, ai_governance]
    allowed_subdomains: [calibration, threshold_policy, cost_matrix, false_allow_policy, false_block_policy]

- node_id: kt.ai_engineering.calibration_threshold.uncertainty
  parent_id: kt.ai_engineering.calibration_threshold
  path: CEK-TA / AI Engineering / Calibration And Threshold Policy / Calibration Uncertainty
  title: Calibration Uncertainty
  domain: llm_training
  subdomain: calibration_uncertainty
  level: 3
  summary: Calibration and uncertainty controls for trading scorers: independent calibration holdout, Platt scaling, isotonic regression, Brier/ECE, regime calibration, uncertainty buckets, abstain bands, and cost-sensitive thresholds.
  key_concepts: [calibration holdout, Platt scaling, isotonic regression, Brier score, ECE, abstain band]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.decision_time_features
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Decision-Time Feature And Leakage Gate
  title: Decision-Time Feature And Leakage Gate
  domain: llm_training
  subdomain: decision_time_feature_contract
  level: 2
  summary: Decision-time feature contracts, timestamp lineage, leakage unit tests, training-serving parity, schema validation, and post-trade field separation.
  key_concepts: [decision time, feature availability, leakage, label observation, schema validation, training serving parity]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_22_DECISION_TIME_FEATURES
    allowed_domains: [llm_training, ai_governance]
    allowed_subdomains: [decision_time_features, leakage_gate, feature_schema, label_observation, training_serving_parity]

- node_id: kt.ai_engineering.decision_time_features.feature_store
  parent_id: kt.ai_engineering.decision_time_features
  path: CEK-TA / AI Engineering / Decision-Time Feature And Leakage Gate / Decision-Time Feature Store
  title: Decision-Time Feature Store
  domain: llm_training
  subdomain: decision_time_feature_store
  level: 3
  summary: Decision-time feature-store boundaries for trading AI: point-in-time joins, offline/online parity, feature lineage, schema versioning, label observation windows, and post-trade-field separation.
  key_concepts: [point-in-time join, offline online parity, feature lineage, schema version, label window]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_audit_assistant
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / LLM Audit Assistant
  title: LLM Audit Assistant
  domain: llm_training
  subdomain: llm_audit_assistant
  level: 2
  summary: LLM audit assistant boundaries: strict schema output, reason codes, citation resolver, unsupported claim detection, no-source abstain, and non-final-gate semantics.
  key_concepts: [strict schema, reason code, citation resolver, unsupported claim, abstain, recommendation]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_23_LLM_AUDIT_ASSISTANT
    allowed_domains: [llm_training, rag_engineering, ai_governance]
    allowed_subdomains: [strict_schema, citation_resolver, unsupported_claim, no_source_abstain, reason_code]

- node_id: kt.ai_engineering.llm_audit_assistant.qwen3_audit_assistant
  parent_id: kt.ai_engineering.llm_audit_assistant
  path: CEK-TA / AI Engineering / LLM Audit Assistant / Qwen3 Audit Assistant
  title: Qwen3 Audit Assistant
  domain: llm_training
  subdomain: qwen3_audit_assistant
  level: 3
  summary: Qwen3 audit-assistant boundaries for trading gating/scoring systems: reason codes, missing-field checks, RAG citation, unsupported-claim detection, prompt-injection and untrusted-context guards, strict JSON, no-hit abstain, and non-final-gate semantics.
  key_concepts: [Qwen3, audit assistant, reason code, strict JSON, citation, abstain, prompt injection]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_audit_assistant.qwen3_training_recipe
  parent_id: kt.ai_engineering.llm_audit_assistant
  path: CEK-TA / AI Engineering / LLM Audit Assistant / Qwen3 Training Recipe
  title: Qwen3 Training Recipe
  domain: llm_training
  subdomain: qwen3_training_recipe
  level: 3
  summary: Qwen3 training recipe boundaries for audit assistants: RAG-first, prompt updates, SFT/LoRA/DPO conditions, schema eval, reason-code eval, citation eval, and no training of trading probabilities.
  key_concepts: [RAG-first, SFT, LoRA, DPO, schema eval, reason code]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.shadow_paper_ope
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Shadow Paper And Off-Policy Evaluation
  title: Shadow Paper And Off-Policy Evaluation
  domain: ai_governance
  subdomain: shadow_paper_ope_eval
  level: 2
  summary: Offline, shadow, paper/replay, and off-policy evaluation boundaries for scorer/gate policies before live or hard-gate promotion.
  key_concepts: [offline eval, shadow mode, paper replay, off-policy evaluation, counterfactual, human review precision]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_24_SHADOW_PAPER_OPE
    allowed_domains: [ai_governance, llm_training]
    allowed_subdomains: [offline_eval, shadow_eval, paper_eval, off_policy_evaluation, counterfactual_eval]

- node_id: kt.ai_engineering.model_release_governance
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Model Release Governance
  title: Model Release Governance
  domain: ai_governance
  subdomain: model_release_governance
  level: 2
  summary: Release manifest, artifact lineage, registry, approval workflow, rollback, kill switch, and incident freeze requirements for trading AI models.
  key_concepts: [release manifest, model registry, artifact hash, approval, rollback, kill switch, incident freeze]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_25_MODEL_RELEASE_GOVERNANCE
    allowed_domains: [ai_governance, llm_training]
    allowed_subdomains: [release_manifest, model_registry, artifact_lineage, approval_workflow, rollback, kill_switch]

- node_id: kt.ai_engineering.model_release_governance.hybrid_runtime_contract
  parent_id: kt.ai_engineering.model_release_governance
  path: CEK-TA / AI Engineering / Model Release Governance / Hybrid Runtime Contract
  title: Hybrid Runtime Contract
  domain: ai_governance
  subdomain: hybrid_runtime_contract
  level: 3
  summary: Runtime contract for hybrid trading scoring systems: scorer output, calibrator output, Qwen3 audit output, RAG references, deterministic final-gate output, trace IDs, version pinning, latency budget, timeout, fallback, and release manifest linkage.
  key_concepts: [scorer output, Qwen3 audit output, final gate output, trace ID, version pinning, fallback]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.model_release_governance.training_platform_governance
  parent_id: kt.ai_engineering.model_release_governance
  path: CEK-TA / AI Engineering / Model Release Governance / Training Platform Governance
  title: Training Platform Governance
  domain: ai_governance
  subdomain: training_platform_governance
  level: 3
  summary: Conditional adoption rules for MLflow, Ray, Kubeflow, Feast, vLLM, and related platforms in trading AI POC systems, with POC-first simplicity and explicit governance before external service dependencies.
  key_concepts: [MLflow, Ray, Kubeflow, Feast, vLLM, platform boundary]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_training.training_dataset_schema_engineering
  parent_id: kt.ai_engineering.llm_training
  path: CEK-TA / AI Engineering / LLM Training / Training Dataset Schema Engineering
  title: Training Dataset Schema Engineering
  domain: llm_training
  subdomain: training_dataset_schema_engineering
  level: 3
  summary: Conversion rules from raw trade records to candidate snapshots, decision-time features, outcome records, labels, SFT examples, preference pairs, and eval cases.
  key_concepts: [raw trade, candidate snapshot, decision-time feature, outcome separation, label schema, SFT example, preference pair, eval case]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_training.trading_llm_task_taxonomy
  parent_id: kt.ai_engineering.llm_training
  path: CEK-TA / AI Engineering / LLM Training / Trading LLM Task Taxonomy
  title: Trading LLM Task Taxonomy
  domain: llm_training
  subdomain: trading_llm_task_taxonomy
  level: 3
  summary: Task taxonomy for trading LLM systems: scoring, gating, risk violation detection, data quality audit, strategy compliance audit, post-trade review, incident explanation, and research suggestions.
  key_concepts: [pre-trade scoring, gating, risk violation, data audit, rule compliance, post-trade review, incident, research hypothesis]
  expected_knowledge_types: [taxonomy, schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.llm_training.training_method_selection
  parent_id: kt.ai_engineering.llm_training
  path: CEK-TA / AI Engineering / LLM Training / Training Method Selection
  title: Training Method Selection
  domain: llm_training
  subdomain: training_method_selection
  level: 3
  summary: Decision rules for RAG-first baseline, SFT, preference/DPO, eval baseline before fine-tuning, and blocking training when data or schema problems remain.
  key_concepts: [RAG first, SFT boundary, DPO boundary, eval baseline, data problem, no premature fine-tune]
  expected_knowledge_types: [procedure, checklist, anti_pattern, decision_rule]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.rag_engineering
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / RAG Engineering
  title: RAG Engineering
  domain: rag_engineering
  subdomain: rag_engineering
  level: 2
  summary: Retrieval governance for metadata, machine gates, token budgets, citation, conflict-aware retrieval, and trading scoring RAG packs.
  key_concepts: [retrieval decision, machine gate, token budget, citation, source quality, conflict]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern, eval_case]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none
  item_mapping:
    partition_id: KB_10_RAG_ENGINEERING
    allowed_domains: [rag_engineering]
    allowed_subdomains: [retrieval_policy, metadata, machine_gate, token_budget, citation, source_quality, scoring_rag_pack]

- node_id: kt.ai_engineering.rag_engineering.source_quality
  parent_id: kt.ai_engineering.rag_engineering
  path: CEK-TA / AI Engineering / RAG Engineering / Source Quality
  title: Source Quality
  domain: rag_engineering
  subdomain: source_quality
  level: 3
  summary: Source quality gates for blocking unsourced knowledge from default professional guidance and preserving citations, conflict status, freshness, and evidence boundaries.
  key_concepts: [source evidence, citation, no source block, conflict status, freshness]
  expected_knowledge_types: [source_policy, checklist, anti_pattern, boundary_rule]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none

- node_id: kt.ai_engineering.rag_engineering.retrieval_policy
  parent_id: kt.ai_engineering.rag_engineering
  path: CEK-TA / AI Engineering / RAG Engineering / Retrieval Policy
  title: Retrieval Policy
  domain: rag_engineering
  subdomain: retrieval_policy
  level: 3
  summary: Domain routing, metadata filters, tree path filters, review-status filters, conflict/freshness warnings, and retrieval output contract.
  key_concepts: [domain routing, metadata filter, tree path, review status, conflict warning]
  expected_knowledge_types: [schema, procedure, checklist, eval_case]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.ai_engineering.rag_engineering.machine_gate_filtering
  parent_id: kt.ai_engineering.rag_engineering
  path: CEK-TA / AI Engineering / RAG Engineering / Metadata And Machine Gate Filtering
  title: Metadata And Machine Gate Filtering
  domain: rag_engineering
  subdomain: machine_gate_filtering
  level: 3
  summary: Review status, source evidence, freshness, conflict status, machine_gate, and llm_usage_policy filters for safe default guidance.
  key_concepts: [review status, machine gate, llm usage policy, conflict status, freshness]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none

- node_id: kt.ai_engineering.rag_engineering.trading_scoring_rag_pack
  parent_id: kt.ai_engineering.rag_engineering
  path: CEK-TA / AI Engineering / RAG Engineering / Trading Scoring RAG Pack
  title: Trading Scoring RAG Pack
  domain: rag_engineering
  subdomain: trading_scoring_rag_pack
  level: 3
  summary: Context packing for trade candidate scoring: project facts, market context, risk context, execution context, retrieved knowledge refs, and audit trace.
  key_concepts: [trade candidate, context pack, knowledge refs, reason codes, audit trace]
  expected_knowledge_types: [schema, procedure, checklist, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.mcp_engineering
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / MCP And Agent Engineering
  title: MCP And Agent Engineering
  domain: rag_engineering
  subdomain: mcp_agent_engineering
  level: 2
  summary: MCP tool contracts, server-side permissions, external AI calling protocol, agent flow, degradation behavior, and non-delegation boundaries.
  key_concepts: [MCP tool, permission, server-side enforcement, agent flow, no-hit, conflict, non-delegation]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none
  item_mapping:
    partition_id: KB_11_MCP_ENGINEERING
    allowed_domains: [rag_engineering, mcp_engineering]
    allowed_subdomains: [mcp_tools, tool_permission, external_ai_calling_protocol, agent_flow, degradation, non_delegation]

- node_id: kt.ai_engineering.mcp_engineering.tool_contract
  parent_id: kt.ai_engineering.mcp_engineering
  path: CEK-TA / AI Engineering / MCP And Agent Engineering / MCP Tool Contract
  title: MCP Tool Contract
  domain: rag_engineering
  subdomain: mcp_tools
  level: 3
  summary: Read-only expert knowledge search, source profile, conflict audit, item lookup, and partition browsing tools.
  key_concepts: [search_expert_knowledge, get_knowledge_item, get_conflict_audit, get_source_profile]
  expected_knowledge_types: [schema, procedure, checklist]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.ai_engineering.mcp_engineering.tool_permission_enforcement
  parent_id: kt.ai_engineering.mcp_engineering
  path: CEK-TA / AI Engineering / MCP And Agent Engineering / Tool Permission Enforcement
  title: Tool Permission Enforcement
  domain: rag_engineering
  subdomain: tool_permission_enforcement
  level: 3
  summary: Server-side read-only enforcement, no write endpoints, no order execution, no secret access, and audit-only export boundaries.
  key_concepts: [read-only, server-side enforcement, no order execution, no secret access]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.llmops_deployment
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / LLMOps And Deployment
  title: LLMOps And Deployment
  domain: llm_training
  subdomain: llmops_deployment
  level: 2
  summary: Offline evaluation, shadow/paper/live rollout, artifact lineage, release control, monitoring, drift, rollback, and incident response.
  key_concepts: [offline eval, shadow mode, paper mode, artifact lineage, release control, drift, rollback]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_12_LLMOPS_DEPLOYMENT
    allowed_domains: [llm_training, ai_governance]
    allowed_subdomains: [offline_eval, rollout, artifact_lineage, release_control, monitoring, rollback]

- node_id: kt.llmops_deployment.artifact_lineage
  parent_id: kt.llmops_deployment
  path: CEK-TA / AI Engineering / LLMOps And Deployment / Artifact Lineage
  title: Artifact Lineage
  domain: llm_training
  subdomain: artifact_lineage
  level: 3
  summary: Model version, prompt version, RAG snapshot, dataset hash, strategy version, eval report, and feature schema version tracking.
  key_concepts: [model version, prompt version, rag snapshot, dataset hash, eval report]
  expected_knowledge_types: [schema, procedure, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.llmops_deployment.monitoring_drift
  parent_id: kt.llmops_deployment
  path: CEK-TA / AI Engineering / LLMOps And Deployment / Monitoring And Drift
  title: Monitoring And Drift
  domain: llm_training
  subdomain: monitoring_drift
  level: 3
  summary: Score distribution drift, confidence drift, reason-code drift, retrieval no-hit drift, conflict-hit drift, latency, human override, and post-trade disagreement.
  key_concepts: [score drift, confidence drift, reason code, no-hit, latency, human override]
  expected_knowledge_types: [procedure, checklist, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_governance_audit
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / AI Governance And Audit
  title: AI Governance And Audit
  domain: ai_governance
  subdomain: ai_governance_audit
  level: 2
  summary: Training data governance, knowledge usage permission, human review, external contribution backflow, model output audit, dataset/model cards, and incident governance.
  key_concepts: [data governance, permission, human review, contribution, model card, incident]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_13_GOVERNANCE_AUDIT
    allowed_domains: [ai_governance, llm_training, rag_engineering]
    allowed_subdomains: [data_governance, knowledge_permission, human_review, contribution, output_audit, model_card, incident]

- node_id: kt.ai_governance_audit.dataset_model_card
  parent_id: kt.ai_governance_audit
  path: CEK-TA / AI Engineering / AI Governance And Audit / Dataset And Model Card
  title: Dataset And Model Card
  domain: ai_governance
  subdomain: dataset_model_card
  level: 3
  summary: Dataset and model documentation for intended use, out-of-scope use, data sources, known limitations, eval summary, and governance status.
  key_concepts: [dataset card, model card, intended use, limitations, eval summary]
  expected_knowledge_types: [schema, procedure, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_governance_audit.incident_governance
  parent_id: kt.ai_governance_audit
  path: CEK-TA / AI Engineering / AI Governance And Audit / Incident Governance
  title: Incident Governance
  domain: ai_governance
  subdomain: incident_governance
  level: 3
  summary: Severity levels, incident ownership, model/prompt/RAG freeze, postmortem, and required knowledge backfill after AI scoring incidents.
  key_concepts: [severity, owner, freeze, postmortem, backfill]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_ai_safety
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Trading AI Safety And Risk Control
  title: Trading AI Safety And Risk Control
  domain: ai_governance
  subdomain: trading_ai_safety
  level: 2
  summary: Safety and risk-control boundaries for trading AI: deterministic risk gate precedence, false allow/block cost policy, kill switch, human escalation, and live-trading permissions.
  key_concepts: [risk gate, false allow, false block, kill switch, human escalation, live permission]
  expected_knowledge_types: [principle, procedure, checklist, anti_pattern, eval_case]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_14_TRADING_AI_SAFETY
    allowed_domains: [ai_governance, live_trading, llm_training]
    allowed_subdomains: [risk_gate_precedence, false_allow_policy, kill_switch, human_escalation, live_permission]

- node_id: kt.trading_ai_safety.risk_gate_precedence
  parent_id: kt.trading_ai_safety
  path: CEK-TA / AI Engineering / Trading AI Safety And Risk Control / Risk Gate Precedence
  title: Risk Gate Precedence
  domain: ai_governance
  subdomain: risk_gate_precedence
  level: 3
  summary: Deterministic risk engine must remain the final hard gate; LLM scoring can only add caution, review, or explanation.
  key_concepts: [deterministic risk engine, hard gate, LLM cannot override, fallback]
  expected_knowledge_types: [principle, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.trading_ai_safety.false_allow_block_policy
  parent_id: kt.trading_ai_safety
  path: CEK-TA / AI Engineering / Trading AI Safety And Risk Control / False Allow And False Block Policy
  title: False Allow And False Block Policy
  domain: ai_governance
  subdomain: false_allow_block_policy
  level: 3
  summary: Cost-sensitive evaluation and release policy for false_allow and false_block in trading gating/scoring systems.
  key_concepts: [false allow, false block, cost weighting, opportunity cost, safety margin]
  expected_knowledge_types: [principle, eval_case, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_business_objective
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Business Objective And Acceptance Criteria
  title: Business Objective And Acceptance Criteria
  domain: ai_governance
  subdomain: business_objective
  level: 2
  summary: Business acceptance criteria for trading LLM systems: role definition, quality improvement metrics, business cost metrics, and live readiness criteria.
  key_concepts: [acceptance criteria, success metric, quality improvement, business cost, live readiness]
  expected_knowledge_types: [principle, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_15_BUSINESS_OBJECTIVE
    allowed_domains: [ai_governance, llm_training, quant_trading]
    allowed_subdomains: [acceptance_criteria, quality_metric, business_cost, live_readiness]

- node_id: kt.ai_label_factory
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Label Factory And Annotation Workflow
  title: Label Factory And Annotation Workflow
  domain: ai_governance
  subdomain: label_factory
  level: 2
  summary: Annotation workflow for trading AI datasets: auto labels, human labels, conflict resolution, gold sets, and label quality scores.
  key_concepts: [auto label, human label, conflict resolution, gold set, label quality]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_16_LABEL_FACTORY
    allowed_domains: [ai_governance, llm_training]
    allowed_subdomains: [auto_label, human_label, conflict_resolution, gold_set, label_quality]

- node_id: kt.ai_data_asset_management
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Data Asset Management
  title: Data Asset Management
  domain: ai_governance
  subdomain: data_asset_management
  level: 2
  summary: Dataset pool governance for trading AI: research, training, eval, gold, shadow, and incident pools.
  key_concepts: [research pool, training pool, eval pool, gold pool, shadow pool, incident pool]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_17_DATA_ASSET_MANAGEMENT
    allowed_domains: [ai_governance, llm_training]
    allowed_subdomains: [research_pool, training_pool, eval_pool, gold_pool, shadow_pool, incident_pool]

- node_id: kt.ai_engineering.continuous_learning
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance
  title: Continuous Learning And Feedback Governance
  domain: ai_governance
  subdomain: feedback_governance
  level: 2
  summary: Governance boundaries for continuous feedback, retraining dataset releases, drift monitoring, recalibration, champion/challenger promotion, controlled rollout, knowledge backfill, and feedback-loop overfitting risk.
  key_concepts: [continuous feedback, retraining release, drift monitoring, recalibration, champion challenger, controlled rollout, knowledge backfill, feedback loop, self-labeling risk]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_18_FEEDBACK_GOVERNANCE
    allowed_domains: [ai_governance, llm_training, rag_engineering]
    allowed_subdomains: [feedback_logging, label_refresh, drift_monitoring, retraining_trigger, recalibration_loop, champion_challenger, shadow_paper_canary, rollback_governance, llm_prompt_rag_sft_loop, feedback_loop_risk, live_feedback, retraining_release, knowledge_backfill]

- node_id: kt.ai_engineering.continuous_learning.feedback_logging
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Feedback Logging
  title: Feedback Logging
  domain: ai_governance
  subdomain: feedback_logging
  level: 3
  summary: Feedback logging rules for all trade candidates, including allowed, blocked, skipped, and human-review decisions, with decision-time feature, scorer, LLM audit, final gate, and outcome references.
  key_concepts: [trade candidate snapshot, decision log, blocked candidate, human review, outcome reference]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.label_refresh
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Label Refresh
  title: Label Refresh
  domain: ai_governance
  subdomain: label_refresh
  level: 3
  summary: Label refresh governance for multi-dimensional trading AI labels, human correction, good loss and bad win review, false allow/block cost, and label policy versioning.
  key_concepts: [label policy, human correction, good loss, bad win, false allow, false block]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.drift_monitoring
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Drift Monitoring
  title: Drift Monitoring
  domain: ai_governance
  subdomain: drift_monitoring
  level: 3
  summary: Drift monitoring for features, labels, score distributions, calibration, regime mix, strategy versions, symbol distribution, and execution-cost changes.
  key_concepts: [feature drift, label drift, score drift, calibration drift, regime drift, strategy drift]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.retraining_trigger
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Retraining Trigger
  title: Retraining Trigger
  domain: ai_governance
  subdomain: retraining_trigger
  level: 3
  summary: Retraining trigger rules for periodic, drift-driven, sample-threshold, and incident-driven candidate model training without automatic champion replacement.
  key_concepts: [periodic retraining, drift trigger, sample threshold, incident trigger, candidate model]
  expected_knowledge_types: [procedure, checklist, policy, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.recalibration_loop
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Recalibration Loop
  title: Recalibration Loop
  domain: ai_governance
  subdomain: recalibration_loop
  level: 3
  summary: Recalibration loop requirements for probability scores, threshold stability, independent calibration sets, Brier/ECE checks, and cost-sensitive threshold review.
  key_concepts: [probability calibration, threshold stability, calibration set, Brier score, ECE, cost-sensitive threshold]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.champion_challenger
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Champion Challenger
  title: Champion Challenger
  domain: ai_governance
  subdomain: champion_challenger
  level: 3
  summary: Champion/challenger governance for comparing candidate models against the current production reference across offline, shadow, paper, soft-gate, and approval stages.
  key_concepts: [champion model, challenger model, offline evaluation, shadow evaluation, promotion review]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.shadow_paper_canary
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Shadow Paper Canary
  title: Shadow Paper Canary
  domain: ai_governance
  subdomain: shadow_paper_canary
  level: 3
  summary: Controlled rollout stages for shadow mode, paper or replay validation, soft gate, small-scope canary, live monitoring, and stop conditions.
  key_concepts: [shadow mode, paper validation, soft gate, canary rollout, stop condition]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.rollback_governance
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Rollback Governance
  title: Rollback Governance
  domain: ai_governance
  subdomain: rollback_governance
  level: 3
  summary: Rollback governance for release manifests, rollback targets, kill switches, incident freezes, approval trails, and post-incident knowledge backfill.
  key_concepts: [release manifest, rollback target, kill switch, incident freeze, approval trail]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.llm_prompt_rag_sft_loop
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / LLM Prompt RAG SFT Loop
  title: LLM Prompt RAG SFT Loop
  domain: llm_training
  subdomain: llm_prompt_rag_sft_loop
  level: 3
  summary: LLM continuous improvement route that prefers RAG knowledge updates and prompt changes before SFT/LoRA, with eval evidence required before changing model weights.
  key_concepts: [RAG update, prompt update, SFT trigger, LoRA trigger, eval evidence, citation quality]
  expected_knowledge_types: [procedure, checklist, eval_case, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.continuous_learning.feedback_loop_risk
  parent_id: kt.ai_engineering.continuous_learning
  path: CEK-TA / AI Engineering / Continuous Learning And Feedback Governance / Feedback Loop Risk
  title: Feedback Loop Risk
  domain: ai_governance
  subdomain: feedback_loop_risk
  level: 3
  summary: Feedback-loop risk controls for self-labeling, model-generated labels, selective logging bias, automation bias, and overfitting to recent review decisions.
  key_concepts: [self-labeling risk, selective logging bias, automation bias, feedback loop, recent overfit]
  expected_knowledge_types: [principle, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_security_privacy_compliance
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / AI Security Privacy And Compliance
  title: AI Security Privacy And Compliance
  domain: ai_governance
  subdomain: ai_security_privacy_compliance
  level: 2
  summary: Security, privacy, and compliance boundaries for AI/RAG/MCP systems: prompt injection, untrusted retrieved context, untrusted tool output, secret redaction, trade data sanitization, market data license, third-party permission, and training export approval.
  key_concepts: [prompt injection, untrusted context, tool output, secret redaction, market data license, training export]
  expected_knowledge_types: [procedure, checklist, anti_pattern, policy]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_19_SECURITY_PRIVACY_COMPLIANCE
    allowed_domains: [ai_governance, rag_engineering, llm_training]
    allowed_subdomains: [prompt_injection, rag_security, tool_output_security, data_privacy, data_license, training_export]

- node_id: kt.ai_engineering.security_governance
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Security Governance
  title: Security Governance
  domain: ai_engineering
  subdomain: security_governance
  level: 2
  summary: Trading AI agent threat modeling, prompt injection, tool misuse, memory poisoning, excessive agency, overreliance, sensitive information disclosure, and final-gate non-bypass boundaries.
  key_concepts: [agent threat model, prompt injection, tool misuse, memory poisoning, excessive agency, final gate]
  expected_knowledge_types: [security_boundary, checklist, anti_pattern, governance_rule]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_ENGINEERING
    allowed_domains: [ai_engineering]
    allowed_subdomains: [security_governance, agent_threat_model]

- node_id: kt.ai_engineering.security_governance.agent_threat_model
  parent_id: kt.ai_engineering.security_governance
  path: CEK-TA / AI Engineering / Security Governance / Agent Threat Model
  title: Agent Threat Model
  domain: ai_engineering
  subdomain: security_governance
  level: 3
  summary: Threat-model and governance boundary for AI IDE, RAG, MCP, tools and project memory in trading AI systems; not a security-pass claim, exploit guide, trading permission, or hard gate.
  key_concepts: [threat surface, MCP permission, memory write policy, RAG source trust, final gate bypass denied]
  expected_knowledge_types: [security_boundary, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.ai_engineering.supply_chain_governance
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Supply Chain Governance
  title: Supply Chain Governance
  domain: ai_engineering
  subdomain: supply_chain_governance
  level: 2
  summary: AI SBOM, Model SBOM, dataset inventory, dependency inventory, model/prompt/RAG release artifacts, source confidentiality, and supply-chain audit boundaries.
  key_concepts: [AI SBOM, ML-BOM, model SBOM, dataset provenance, artifact manifest, license]
  expected_knowledge_types: [schema, checklist, governance_rule, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_ENGINEERING
    allowed_domains: [ai_engineering]
    allowed_subdomains: [supply_chain_governance, ai_sbom]

- node_id: kt.ai_engineering.supply_chain_governance.ai_sbom
  parent_id: kt.ai_engineering.supply_chain_governance
  path: CEK-TA / AI Engineering / Supply Chain Governance / AI SBOM
  title: AI SBOM
  domain: ai_engineering
  subdomain: supply_chain_governance
  level: 3
  summary: AI/ML inventory boundary for model, dataset, dependency, prompt, RAG snapshot, calibrator, threshold/final-gate policy, release manifest, artifact URI/hash and source confidentiality.
  key_concepts: [CycloneDX ML-BOM, SPDX AI Profile, model inventory, dataset inventory, artifact lineage]
  expected_knowledge_types: [schema, checklist, governance_rule, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: none

- node_id: kt.ai_engineering.database_storage_engineering
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering
  title: Database Data Contract And Storage Engineering
  domain: storage_engineering
  subdomain: database_storage_engineering
  level: 2
  summary: Database, data contract, audit ledger, vector retrieval storage, migration, backup, lifecycle, and access-control knowledge for trading AI systems.
  key_concepts: [PostgreSQL, canonical store, data contract, audit ledger, vector index, migration, backup, lifecycle]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern, policy]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_26_DATABASE_STORAGE
    allowed_domains: [storage_engineering, ai_governance, rag_engineering]
    allowed_subdomains: [relational_core_schema, data_contract_lineage, migration_versioning, indexing_query_performance, audit_log_ledger, feature_store_storage, vector_store_retrieval_storage, model_registry_release_storage, runtime_observability_trace, data_lifecycle_retention, security_privacy_access_control, backup_restore_disaster_recovery]

- node_id: kt.ai_engineering.database_storage_engineering.relational_core_schema
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Relational Core Schema
  title: Relational Core Schema
  domain: storage_engineering
  subdomain: relational_core_schema
  level: 3
  summary: Core relational schema boundaries for trade candidates, score results, LLM audit results, final gate ledgers, manifests, keys, constraints, and idempotency.
  key_concepts: [primary key, unique key, foreign key, constraint, JSONB, idempotency]
  expected_knowledge_types: [schema, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.data_contract_lineage
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Data Contract Lineage
  title: Data Contract Lineage
  domain: storage_engineering
  subdomain: data_contract_lineage
  level: 3
  summary: Data contracts for decision_time visibility, event_time, ingestion_time, label_time, schema hashes, dataset hashes, and lineage references.
  key_concepts: [decision_time, event_time, ingestion_time, label_time, schema hash, dataset hash, lineage]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.migration_versioning
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Migration Versioning
  title: Migration Versioning
  domain: storage_engineering
  subdomain: migration_versioning
  level: 3
  summary: Migration governance for reviewed, reversible, compatible schema changes, rollback plans, and controlled use of migration autogeneration.
  key_concepts: [Alembic, migration review, reversible migration, rollback, compatibility]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.indexing_query_performance
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Indexing Query Performance
  title: Indexing Query Performance
  domain: storage_engineering
  subdomain: indexing_query_performance
  level: 3
  summary: Query-pattern driven indexing, unique indexes, composite indexes, partitioning, pagination, and slow-query audit boundaries for trading AI storage.
  key_concepts: [index, composite index, unique index, partition, pagination, slow query]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.audit_log_ledger
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Audit Log Ledger
  title: Audit Log Ledger
  domain: storage_engineering
  subdomain: audit_log_ledger
  level: 3
  summary: Append-only audit ledger rules for final gate decisions, human reviews, permission changes, actor/reason fields, trace IDs, and tamper-evidence.
  key_concepts: [append-only, ledger, actor, reason, audit_trace_id, row_hash, prev_hash]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.feature_store_storage
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Feature Store Storage
  title: Feature Store Storage
  domain: storage_engineering
  subdomain: feature_store_storage
  level: 3
  summary: Storage boundaries for offline and online feature parity, feature snapshots, feature manifests, point-in-time joins, and conditional feature-store adoption.
  key_concepts: [feature store, offline-online parity, feature snapshot, point-in-time join, feature manifest]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.vector_store_retrieval_storage
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Vector Store Retrieval Storage
  title: Vector Store Retrieval Storage
  domain: storage_engineering
  subdomain: vector_store_retrieval_storage
  level: 3
  summary: Vector retrieval storage boundaries for pgvector, Qdrant, embeddings, chunk metadata, source provenance, payload filters, and index versioning.
  key_concepts: [pgvector, Qdrant, embedding_model_version, chunk_version, payload metadata, source provenance]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.model_registry_release_storage
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Model Registry Release Storage
  title: Model Registry Release Storage
  domain: storage_engineering
  subdomain: model_registry_release_storage
  level: 3
  summary: Storage rules for model release manifests, scorer, calibrator, threshold, prompt, RAG index, rollback target, and conditional model registry adoption.
  key_concepts: [model release manifest, model registry, rollback target, prompt version, rag index version]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.runtime_observability_trace
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Runtime Observability Trace
  title: Runtime Observability Trace
  domain: storage_engineering
  subdomain: runtime_observability_trace
  level: 3
  summary: Runtime trace storage for request IDs, audit trace IDs, latency, timeout, fallback, retrieval hits, citation completeness, and error records.
  key_concepts: [request_id, audit_trace_id, latency, timeout, fallback, error record]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.data_lifecycle_retention
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Data Lifecycle Retention
  title: Data Lifecycle Retention
  domain: storage_engineering
  subdomain: data_lifecycle_retention
  level: 3
  summary: Data lifecycle governance for retention, archival, deletion, cold storage, dataset freezes, incident freezes, and audit replay continuity.
  key_concepts: [retention, archival, deletion, cold storage, incident freeze, audit replay]
  expected_knowledge_types: [policy, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.security_privacy_access_control
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Security Privacy Access Control
  title: Security Privacy Access Control
  domain: storage_engineering
  subdomain: security_privacy_access_control
  level: 3
  summary: Storage security boundaries for least privilege, RLS, pgAudit, secret exclusion, PII/private field redaction, and audited write actions.
  key_concepts: [least privilege, RLS, pgAudit, secret redaction, PII, audited write]
  expected_knowledge_types: [policy, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.database_storage_engineering.backup_restore_disaster_recovery
  parent_id: kt.ai_engineering.database_storage_engineering
  path: CEK-TA / AI Engineering / Database Data Contract And Storage Engineering / Backup Restore Disaster Recovery
  title: Backup Restore Disaster Recovery
  domain: storage_engineering
  subdomain: backup_restore_disaster_recovery
  level: 3
  summary: Backup and restore governance for RPO, RTO, restore drills, disaster recovery evidence, and recovery failure handling.
  key_concepts: [backup, restore drill, RPO, RTO, disaster recovery, recovery evidence]
  expected_knowledge_types: [procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory
  parent_id: kt.ai_engineering
  path: CEK-TA / AI Engineering / External Project AI Memory Layer
  title: External Project AI Memory Layer
  domain: ai_governance
  subdomain: external_project_memory
  level: 2
  summary: Project memory contracts, memory lifecycle, write gates, retrieval budgets, security governance, and adapter selection for external AI projects using CEK-TA.
  key_concepts: [project memory, MemoryItem, memory event log, write gate, retrieval budget, adapter, memory security]
  expected_knowledge_types: [schema, policy, procedure, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
  item_mapping:
    partition_id: KB_AI_27_PROJECT_MEMORY
    allowed_domains: [ai_governance, rag_engineering, storage_engineering, llm_training]
    allowed_subdomains: [memory_boundary, memory_mcp_api_contract, memory_schema_lifecycle, memory_event_log, memory_write_gate, memory_retrieval_context, memory_security_governance, memory_retention_privacy, memory_adapter_selection, memory_evaluation_regression]

- node_id: kt.ai_engineering.project_memory.memory_boundary
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Boundary
  title: Memory Boundary
  domain: ai_governance
  subdomain: memory_boundary
  level: 3
  summary: Boundaries between CEK-TA professional knowledge, external project memory, private project facts, and runtime task context.
  key_concepts: [RAG knowledge, project memory, private facts, boundary, contamination]
  expected_knowledge_types: [policy, anti_pattern, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_mcp_api_contract
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory MCP API Contract
  title: Memory MCP API Contract
  domain: ai_governance
  subdomain: memory_mcp_api_contract
  level: 3
  summary: Minimal-permission Project Memory MCP/API contracts, read/write/admin tool boundaries, error schema, audit events, and write-gate enforcement.
  key_concepts: [Project Memory MCP, minimal permission, propose_memory, update_status, audit event, write gate]
  expected_knowledge_types: [schema, policy, procedure, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_schema_lifecycle
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Schema Lifecycle
  title: Memory Schema Lifecycle
  domain: ai_governance
  subdomain: memory_schema_lifecycle
  level: 3
  summary: MemoryItem schema, memory types, lifecycle states, supersede semantics, deprecation, and review status for external project memory.
  key_concepts: [MemoryItem, goal, task, decision, artifact, lesson, boundary, lifecycle]
  expected_knowledge_types: [schema, procedure, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_event_log
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Event Log
  title: Memory Event Log
  domain: ai_governance
  subdomain: memory_event_log
  level: 3
  summary: Append-only memory event log rules for process records, source events, trace IDs, source hashes, and audit history.
  key_concepts: [append-only log, source event, trace id, source hash, audit event]
  expected_knowledge_types: [schema, procedure, policy]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_write_gate
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Write Gate
  title: Memory Write Gate
  domain: ai_governance
  subdomain: memory_write_gate
  level: 3
  summary: Rules for AI-proposed memory, source checks, secret scans, visibility checks, conflict checks, and human or rule review before active memory.
  key_concepts: [propose only, write gate, source check, secret scan, conflict check, review]
  expected_knowledge_types: [policy, procedure, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_retrieval_context
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Retrieval Context
  title: Memory Retrieval Context
  domain: rag_engineering
  subdomain: memory_retrieval_context
  level: 3
  summary: Project memory recall rules for project_id, visibility, status, top-k, token budget, default injection, and explicit audit history retrieval.
  key_concepts: [recall, project_id, visibility, top-k, token budget, context injection]
  expected_knowledge_types: [policy, procedure, checklist]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_security_governance
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Security Governance
  title: Memory Security Governance
  domain: ai_governance
  subdomain: memory_security_governance
  level: 3
  summary: Prompt injection, memory poisoning, private data, rollback, integrity check, and visibility governance for long-term project memory.
  key_concepts: [memory poisoning, prompt injection, private data, rollback, integrity, visibility]
  expected_knowledge_types: [policy, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_retention_privacy
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Retention Privacy
  title: Memory Retention Privacy
  domain: ai_governance
  subdomain: memory_retention_privacy
  level: 3
  summary: Retention, deletion, export, privacy minimization, tombstone, and lifecycle evidence policies for external project memory.
  key_concepts: [retention, deletion, export, privacy minimization, tombstone, data lifecycle]
  expected_knowledge_types: [policy, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_adapter_selection
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Adapter Selection
  title: Memory Adapter Selection
  domain: storage_engineering
  subdomain: memory_adapter_selection
  level: 3
  summary: Adapter selection boundaries for PostgreSQL JSONB, optional pgvector, LangGraph, Letta, Mem0, Zep/Graphiti, and custom external project memory services.
  key_concepts: [PostgreSQL JSONB, pgvector, LangGraph, Letta, Mem0, Zep, adapter]
  expected_knowledge_types: [policy, checklist, anti_pattern]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked

- node_id: kt.ai_engineering.project_memory.memory_evaluation_regression
  parent_id: kt.ai_engineering.project_memory
  path: CEK-TA / AI Engineering / External Project AI Memory Layer / Memory Evaluation Regression
  title: Memory Evaluation Regression
  domain: ai_governance
  subdomain: memory_evaluation_regression
  level: 3
  summary: Evaluation and regression tests for memory retrieval quality, stale memory, poisoning resistance, permission boundaries, and rollback.
  key_concepts: [retrieval regression, stale memory test, poisoning test, permission test, rollback test]
  expected_knowledge_types: [procedure, checklist, quality_gate]
  coverage_status: empty
  review_status: reviewed
  freshness_status: time_sensitive
  conflict_status: unchecked
```

## Project Integration Branch

```yaml
- node_id: kt.project_integration.adapter
  parent_id: kt.project_integration
  path: CEK-TA / Project Integration / Project Adapter
  title: Project Adapter
  domain: project_runbooks
  subdomain: project_adapter
  level: 2
  summary: External project identity, fact boundaries, field mapping, runtime modes, permissions, and contribution policy.
  key_concepts: [adapter, project facts, field mapping, runtime mode, permission]
  expected_knowledge_types: [schema, procedure, checklist, adapter_rule]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none
  item_mapping:
    partition_id: KB_12_PROJECT_INTEGRATION
    allowed_domains: [project_runbooks]
    allowed_subdomains: [project_adapter, healthcheck, contribution]

- node_id: kt.project_integration.healthcheck
  parent_id: kt.project_integration
  path: CEK-TA / Project Integration / Healthcheck
  title: External Project Healthcheck
  domain: project_runbooks
  subdomain: healthcheck
  level: 2
  summary: Checks for CEK-TA path, project facts, runtime modes, field mapping, permissions, MCP config, contribution readiness, and rollback.
  key_concepts: [healthcheck, pass, warn, fail, boundary]
  expected_knowledge_types: [procedure, checklist, adapter_rule]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none

- node_id: kt.project_integration.contribution
  parent_id: kt.project_integration
  path: CEK-TA / Project Integration / Knowledge Contribution
  title: Knowledge Contribution
  domain: project_runbooks
  subdomain: contribution
  level: 2
  summary: Sanitized proposed contributions from external projects, review status flow, evidence requirements, and conflict checks.
  key_concepts: [proposed, sanitization, source, conflict, accepted]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  coverage_status: partial
  review_status: reviewed
  freshness_status: stable
  conflict_status: none
```

## Primary Partition Mapping

| Tree Node | Primary Partition |
| --- | --- |
| `kt.quant_foundation` | `KB_01_QUANT_FOUNDATION` |
| `kt.kline_strategy` | `KB_02_KLINE_STRATEGY` |
| `kt.market_microstructure` | `KB_03_MARKET_MICROSTRUCTURE` |
| `kt.backtest` | `KB_04_BACKTEST` |
| `kt.replay_simulation` | `KB_05_REPLAY_SIMULATION` |
| `kt.live_execution` | `KB_06_LIVE_EXECUTION` |
| `kt.trade_analysis` | `KB_07_TRADE_ANALYSIS` |
| `kt.ai_engineering.llm_training` | `KB_09_LLM_TRAINING` |
| `kt.ai_engineering.rag_engineering` | `KB_10_RAG_ENGINEERING` |
| `kt.ai_engineering.mcp_engineering` | `KB_11_MCP_ENGINEERING` |
| `kt.llmops_deployment` | `KB_AI_12_LLMOPS_DEPLOYMENT` |
| `kt.ai_governance_audit` | `KB_AI_13_GOVERNANCE_AUDIT` |
| `kt.trading_ai_safety` | `KB_AI_14_TRADING_AI_SAFETY` |
| `kt.ai_business_objective` | `KB_AI_15_BUSINESS_OBJECTIVE` |
| `kt.ai_label_factory` | `KB_AI_16_LABEL_FACTORY` |
| `kt.ai_data_asset_management` | `KB_AI_17_DATA_ASSET_MANAGEMENT` |
| `kt.ai_engineering.continuous_learning` | `KB_AI_18_FEEDBACK_GOVERNANCE` |
| `kt.ai_security_privacy_compliance` | `KB_AI_19_SECURITY_PRIVACY_COMPLIANCE` |
| `kt.ai_engineering.numeric_scoring` | `KB_AI_20_NUMERIC_SCORING` |
| `kt.ai_engineering.calibration_threshold` | `KB_AI_21_CALIBRATION_THRESHOLD` |
| `kt.ai_engineering.decision_time_features` | `KB_AI_22_DECISION_TIME_FEATURES` |
| `kt.ai_engineering.llm_audit_assistant` | `KB_AI_23_LLM_AUDIT_ASSISTANT` |
| `kt.ai_engineering.shadow_paper_ope` | `KB_AI_24_SHADOW_PAPER_OPE` |
| `kt.ai_engineering.model_release_governance` | `KB_AI_25_MODEL_RELEASE_GOVERNANCE` |
| `kt.ai_engineering.database_storage_engineering` | `KB_AI_26_DATABASE_STORAGE` |
| `kt.ai_engineering.project_memory` | `KB_AI_27_PROJECT_MEMORY` |
| `kt.project_integration` | `KB_12_PROJECT_INTEGRATION` |

## First-Version Coverage Notes

```text
1. partial means CEK-TA already has schemas, templates, or domain scaffolds but not enough approved source-backed knowledge items.
2. empty means the node is intentionally created as a target for Phase 12 and Phase 17.
3. potential conflict on fill_model exists because fill ordering depends on data granularity and simulation assumptions.
4. time_sensitive nodes must be rechecked when they depend on exchange APIs, libraries, model APIs, or MCP runtime behavior.
```
