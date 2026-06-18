# CEK-TA Knowledge Base Partitions

This file defines the top-level knowledge partitions for CEK-TA RAG ingestion and retrieval.

It defines structure only. Do not place detailed professional rules here.

## Partition Contract

Each partition must define:

```text
partition_id
name
domain
purpose
allowed_content
forbidden_content
typical_source_type
downstream_used_for
review_requirements
```

## Global Rules

```text
1. Project facts stay in business projects.
2. Reusable professional knowledge goes into CEK-TA.
3. Every knowledge item must have source, applicability, confidence, freshness, and review_status metadata.
4. Time-sensitive rules must be marked time_sensitive.
5. Conflicting rules cannot both be approved unless applicability boundaries are explicit.
6. No secrets, account data, API keys, raw private order data, or unreviewed project-specific fields are allowed.
```

## KB_01_QUANT_FOUNDATION

```yaml
partition_id: KB_01_QUANT_FOUNDATION
name: Quant Foundation
domain: quant_trading
purpose: General trading-system architecture, signal flow, risk, sizing, RR/EV, costs, and execution principles.
allowed_content:
  - strategy architecture principles
  - signal / feature / decision separation
  - position sizing concepts
  - risk gate design
  - RR, EV, fee, and slippage analysis
  - execution basics
forbidden_content:
  - project-private field names
  - live account configuration
  - unverified strategy claims
  - exchange secrets or credentials
typical_source_type:
  - paper
  - book
  - official_doc
  - engineering_article
downstream_used_for:
  - strategy_design
  - code_review
  - live_trading
  - trade_analysis
review_requirements:
  - source required
  - applicability required
  - conflict check required
```

## KB_02_KLINE_STRATEGY

```yaml
partition_id: KB_02_KLINE_STRATEGY
name: Kline Strategy
domain: kline_strategy
purpose: K-line trend, entry timing, multi-timeframe alignment, structure levels, ATR/RSI/volume usage, SL/TP design.
allowed_content:
  - trend structure rules
  - multi-timeframe analysis
  - breakout / pullback / continuation / reversal setup logic
  - SL invalidation concepts
  - TP reachability concepts
  - indicator interpretation boundaries
forbidden_content:
  - chart screenshots without analysis
  - project-only thresholds
  - unsupported indicator folklore
  - rules without timeframe applicability
typical_source_type:
  - book
  - research_report
  - engineering_article
  - internal_report
downstream_used_for:
  - strategy_design
  - kline_strategy_review
  - backtest_review
review_requirements:
  - timeframe applicability required
  - market applicability required
  - assumptions required
```

## KB_03_MARKET_MICROSTRUCTURE

```yaml
partition_id: KB_03_MARKET_MICROSTRUCTURE
name: Market Microstructure
domain: market_microstructure
purpose: Order flow, OFI, CVD, liquidity, spreads, order book behavior, trade prints, and microstructure feature interpretation.
allowed_content:
  - OFI / CVD definitions
  - order book and trade print interpretation
  - liquidity and spread concepts
  - funding / open interest interpretation boundaries
  - microstructure feature caveats
forbidden_content:
  - fake order-flow proxies without caveats
  - project-specific feature names
  - unsupported claims about causal direction
typical_source_type:
  - paper
  - official_doc
  - exchange_rule
  - research_report
downstream_used_for:
  - strategy_design
  - feature_engineering
  - trade_analysis
review_requirements:
  - source quality high or medium
  - data granularity required
  - market applicability required
```

## KB_04_BACKTEST

```yaml
partition_id: KB_04_BACKTEST
name: Backtest
domain: backtest
purpose: Backtest credibility, bias detection, data quality, train/test split, metrics, costs, and reproducibility.
allowed_content:
  - lookahead bias patterns
  - data quality checks
  - fill assumptions
  - cost and slippage modeling
  - backtest metric interpretation
  - version reproducibility practices
forbidden_content:
  - performance claims without sample definition
  - unreviewed project backtest results as general truth
  - hidden parameter search conclusions
typical_source_type:
  - paper
  - book
  - framework_doc
  - internal_report
downstream_used_for:
  - backtest_review
  - simulation
  - strategy_iteration
review_requirements:
  - sample scope required
  - assumptions required
  - conflict check required
```

## KB_05_REPLAY_SIMULATION

```yaml
partition_id: KB_05_REPLAY_SIMULATION
name: Replay and Simulation
domain: replay_simulation
purpose: Market replay, replay clocks, event-driven simulation, fill models, same-candle TP/SL ordering, and paper-trading fidelity.
allowed_content:
  - replay engine design
  - event bus and replay clock semantics
  - fill model design
  - same-candle TP/SL rules
  - slippage and latency assumptions
  - live-vs-simulation gap analysis
forbidden_content:
  - unstated fill ordering rules
  - unverified live equivalence claims
  - project-only simulator behavior as general default
typical_source_type:
  - framework_doc
  - engineering_article
  - internal_report
  - official_doc
downstream_used_for:
  - replay_engineering
  - simulation
  - backtest_review
  - live_readiness
review_requirements:
  - data granularity required
  - execution assumptions required
  - deterministic rule required
```

## KB_06_LIVE_EXECUTION

```yaml
partition_id: KB_06_LIVE_EXECUTION
name: Live Execution
domain: live_trading
purpose: Live readiness, exchange adapters, order state machines, kill switches, reconciliation, latency, incident response.
allowed_content:
  - exchange API rule summaries
  - order state machine design
  - risk limits
  - kill switch design
  - position reconciliation
  - incident response practices
forbidden_content:
  - API keys or credentials
  - account-specific configuration
  - unsafe live execution shortcuts
  - outdated exchange rules without freshness marker
typical_source_type:
  - official_doc
  - exchange_rule
  - internal_report
  - engineering_article
downstream_used_for:
  - live_trading
  - risk_review
  - exchange_adapter_review
review_requirements:
  - freshness required
  - official source preferred
  - safety impact required
```

## KB_07_TRADE_ANALYSIS

```yaml
partition_id: KB_07_TRADE_ANALYSIS
name: Trade Analysis
domain: trade_analysis
purpose: Trade-quality metrics, bad-case taxonomy, labels, realized R, timing errors, failure modes, and strategy iteration loops.
allowed_content:
  - bad trade taxonomy
  - trade labels
  - realized vs planned R analysis
  - TP reachability analysis
  - time bucket analysis
  - strategy iteration loop patterns
forbidden_content:
  - raw private trades without sanitization
  - account PnL as general evidence
  - project-only labels without generic mapping
typical_source_type:
  - internal_report
  - research_report
  - engineering_article
downstream_used_for:
  - trade_analysis
  - strategy_iteration
  - llm_training
review_requirements:
  - sanitization required for contributed data
  - label definition required
  - applicability required
```

## KB_08_LLM_TRAINING

```yaml
partition_id: KB_08_LLM_TRAINING
name: LLM Training
domain: llm_training
purpose: RAG vs SFT vs DPO vs Eval decisions, dataset cards, preference data, bad-case regression, training/eval workflow.
allowed_content:
  - RAG/SFT/DPO/Eval decision rules
  - dataset design
  - eval design
  - preference data guidelines
  - bad-case regression practices
forbidden_content:
  - latest market facts as fine-tune targets
  - secrets or private prompts with credentials
  - unlicensed data
  - unreviewed preference rules
typical_source_type:
  - official_doc
  - framework_doc
  - paper
  - internal_report
downstream_used_for:
  - llm_training
  - rag_engineering
  - eval
review_requirements:
  - data license required when applicable
  - train/eval split required
  - evaluation metric required
```

## KB_09_RAG_ENGINEERING

```yaml
partition_id: KB_09_RAG_ENGINEERING
name: RAG Engineering
domain: rag_engineering
purpose: Metadata schemas, chunking rules, retrieval policy, source quality, reranking, citation, MCP integration.
allowed_content:
  - metadata schema design
  - chunking strategy
  - hybrid search policy
  - rerank policy
  - source quality scoring
  - citation requirements
forbidden_content:
  - untraceable retrieved snippets
  - ingestion rules that drop source metadata
  - unsafe write tools without review gate
typical_source_type:
  - official_doc
  - framework_doc
  - engineering_article
  - internal_report
downstream_used_for:
  - rag_engineering
  - mcp
  - vue_audit_ui
review_requirements:
  - source traceability required
  - retrieval eval recommended
  - citation required
```

## KB_10_PROJECT_RUNBOOKS

```yaml
partition_id: KB_10_PROJECT_RUNBOOKS
name: Project Runbooks
domain: project_runbooks
purpose: Sanitized project adapters, historical task cards, audit reports, incident summaries, contribution records, and reusable runbooks.
allowed_content:
  - sanitized task cards
  - audit summaries
  - incident reports
  - project adapter summaries
  - knowledge contribution records
forbidden_content:
  - raw secrets
  - unsanitized account/order data
  - project-private field dictionaries without generic mapping
  - unresolved conflict rules marked approved
typical_source_type:
  - internal_report
  - task_card
  - runbook
  - code_doc
downstream_used_for:
  - project_integration
  - knowledge_contribution
  - audit
  - llm_training
review_requirements:
  - sanitization required
  - project_binding required
  - contribution status required
```

## Domain Mapping Summary

| Partition | Domain |
| --- | --- |
| KB_01_QUANT_FOUNDATION | quant_trading |
| KB_02_KLINE_STRATEGY | kline_strategy |
| KB_03_MARKET_MICROSTRUCTURE | market_microstructure |
| KB_04_BACKTEST | backtest |
| KB_05_REPLAY_SIMULATION | replay_simulation |
| KB_06_LIVE_EXECUTION | live_trading |
| KB_07_TRADE_ANALYSIS | trade_analysis |
| KB_08_LLM_TRAINING | llm_training |
| KB_09_RAG_ENGINEERING | rag_engineering |
| KB_10_PROJECT_RUNBOOKS | project_runbooks |
