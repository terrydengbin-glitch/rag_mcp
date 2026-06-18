# CEK-TA Knowledge Base Partitions v2

This file defines v2 KB partitions for canonical knowledge tree routing.

It is not the default partition contract yet. The default remains `kb_partitions.md` until RAG/MCP/Vue3 compatibility work is complete.

## Partition Contract

```text
partition_id
name
canonical_root
domain
purpose
allowed_content
forbidden_content
typical_source_type
downstream_used_for
review_requirements
migration_notes
```

## Global Rules

```text
1. v2 partitions are additive and do not delete v1 partitions.
2. v1 partition_id remains valid through alias routing.
3. Project facts stay in business projects unless sanitized and reviewed.
4. Every accepted/approved knowledge item must have source, applicability, confidence, freshness, review_status, and conflict_status.
5. No approved knowledge may be unsourced, project-private, or unresolved-conflicted.
6. v2 partition changes must not change MCP permissions.
```

## Partition List

| Partition | Name | Canonical Root | Status |
| --- | --- | --- | --- |
| `KB_01_QUANT_FOUNDATION` | Quant Foundation | `kt.trading_engineering.quant_foundation` | retained |
| `KB_02_DATA_ENGINEERING` | Data Engineering | `kt.trading_engineering.data_engineering` | new |
| `KB_03_STRATEGY_ENGINEERING` | Strategy Engineering | `kt.trading_engineering.strategy_engineering` | expanded |
| `KB_04_BACKTEST` | Backtest | `kt.trading_engineering.backtest` | retained |
| `KB_05_REPLAY_SIMULATION` | Replay and Simulation | `kt.trading_engineering.replay_simulation` | retained |
| `KB_06_LIVE_EXECUTION` | Live Execution | `kt.trading_engineering.live_execution` | retained |
| `KB_07_RISK_MANAGEMENT` | Risk Management | `kt.trading_engineering.risk_management` | new |
| `KB_08_TRADE_ANALYSIS` | Trade Analysis | `kt.trading_engineering.trade_analysis` | retained-renumbered |
| `KB_09_LLM_TRAINING` | LLM Training | `kt.ai_engineering.llm_training` | retained-renumbered |
| `KB_10_RAG_ENGINEERING` | RAG Engineering | `kt.ai_engineering.rag_engineering` | retained-renumbered |
| `KB_11_MCP_ENGINEERING` | MCP and Agent Engineering | `kt.ai_engineering.mcp_engineering` | split-new |
| `KB_12_PROJECT_INTEGRATION` | Project Integration | `kt.project_integration` | expanded |
| `KB_13_KNOWLEDGE_GOVERNANCE` | Knowledge Governance | `kt.knowledge_governance` | new |

## Partitions

```yaml
- partition_id: KB_01_QUANT_FOUNDATION
  name: Quant Foundation
  canonical_root: kt.trading_engineering.quant_foundation
  domain: quant_trading
  purpose: Signal flow, EV/RR/cost, probability, expectancy, position sizing theory, and trade lifecycle.
  allowed_content: [definitions, formulas, principles, checklists, anti_patterns]
  forbidden_content: [project_private_thresholds, account_config, unverified_strategy_claims]
  typical_source_type: [paper, book, engineering_article, framework_doc]
  downstream_used_for: [strategy_design, code_review, trade_analysis]
  review_requirements: [source_required, applicability_required, conflict_check_required]
  migration_notes: Retains v1 KB_01_QUANT_FOUNDATION.

- partition_id: KB_02_DATA_ENGINEERING
  name: Data Engineering
  canonical_root: kt.trading_engineering.data_engineering
  domain: data_engineering
  purpose: Market data schemas, time alignment, data quality, feature pipelines, versioning, and observability.
  allowed_content: [schema, procedure, checklist, anti_pattern, eval_case]
  forbidden_content: [raw_market_data, raw_order_data, private_vendor_keys, project_only_field_names_without_mapping]
  typical_source_type: [official_doc, exchange_rule, framework_doc, engineering_article]
  downstream_used_for: [backtest_review, feature_engineering, simulation, live_trading]
  review_requirements: [data_granularity_required, freshness_required_when_api_related, source_required]
  migration_notes: New v2 partition; v1 backtest.data_quality remains scoped to backtest.

- partition_id: KB_03_STRATEGY_ENGINEERING
  name: Strategy Engineering
  canonical_root: kt.trading_engineering.strategy_engineering
  domain: strategy_engineering
  purpose: Signal, direction, entry, exit, scoring gates, regime detection, K-line strategy, microstructure, and derivatives flow.
  allowed_content: [definition, principle, procedure, checklist, anti_pattern, eval_case]
  forbidden_content: [profit_guarantees, project_only_thresholds, unsourced_indicator_folklore, raw_kline_data]
  typical_source_type: [book, paper, research_report, engineering_article, framework_doc]
  downstream_used_for: [strategy_design, code_review, backtest_review, trade_analysis]
  review_requirements: [market_required, timeframe_required, assumptions_required, no_investment_advice]
  migration_notes: Absorbs v1 KB_02_KLINE_STRATEGY and KB_03_MARKET_MICROSTRUCTURE as strategy capabilities.

- partition_id: KB_04_BACKTEST
  name: Backtest
  canonical_root: kt.trading_engineering.backtest
  domain: backtest
  purpose: Backtest credibility, bias, scenario data quality, fill assumptions, cost model, metrics, walk-forward, reproducibility.
  allowed_content: [definition, procedure, checklist, anti_pattern, eval_case]
  forbidden_content: [performance_claims_without_sample, hidden_parameter_search, project_backtest_as_general_truth]
  typical_source_type: [paper, book, framework_doc, engineering_article]
  downstream_used_for: [backtest_review, strategy_iteration, simulation]
  review_requirements: [sample_scope_required, assumptions_required, conflict_check_required]
  migration_notes: Retains v1 KB_04_BACKTEST.

- partition_id: KB_05_REPLAY_SIMULATION
  name: Replay and Simulation
  canonical_root: kt.trading_engineering.replay_simulation
  domain: replay_simulation
  purpose: Replay clocks, event replay, market state reconstruction, fill/slippage/latency models, fidelity levels, paper trading.
  allowed_content: [schema, principle, procedure, checklist, anti_pattern, eval_case]
  forbidden_content: [unstated_fill_ordering, unverified_live_equivalence, project_only_simulator_behavior_as_default]
  typical_source_type: [framework_doc, engineering_article, official_doc, internal_report]
  downstream_used_for: [replay, simulation, backtest_review, live_readiness]
  review_requirements: [data_granularity_required, fill_assumptions_required, fidelity_level_required]
  migration_notes: Retains v1 KB_05_REPLAY_SIMULATION.

- partition_id: KB_06_LIVE_EXECUTION
  name: Live Execution
  canonical_root: kt.trading_engineering.live_execution
  domain: live_trading
  purpose: Exchange adapters, order state machines, position reconciliation, account safety, incident response, kill switches.
  allowed_content: [official_rule_summary, procedure, checklist, anti_pattern, incident]
  forbidden_content: [api_keys, account_config, unsafe_shortcuts, stale_exchange_rules_without_warning]
  typical_source_type: [official_doc, exchange_rule, engineering_article, internal_report]
  downstream_used_for: [live_trading, exchange_adapter_review, risk_review]
  review_requirements: [freshness_required, official_source_preferred, safety_impact_required]
  migration_notes: Retains v1 KB_06_LIVE_EXECUTION.

- partition_id: KB_07_RISK_MANAGEMENT
  name: Risk Management
  canonical_root: kt.trading_engineering.risk_management
  domain: risk_management
  purpose: Risk gates, position sizing, drawdown control, leverage policy, exposure control, daily loss limits, ruin risk.
  allowed_content: [principle, formula, procedure, checklist, anti_pattern]
  forbidden_content: [recommended_leverage, account_specific_limits, investment_advice]
  typical_source_type: [paper, book, exchange_rule, official_doc, engineering_article]
  downstream_used_for: [risk_review, live_trading, strategy_design, code_review]
  review_requirements: [risk_scope_required, assumptions_required, conservative_default_required]
  migration_notes: New v2 partition; splits engineering risk from quant foundation and live execution.

- partition_id: KB_08_TRADE_ANALYSIS
  name: Trade Analysis
  canonical_root: kt.trading_engineering.trade_analysis
  domain: trade_analysis
  purpose: Trade quality, labels, bad-case taxonomy, R/R decomposition, cost decomposition, bucket analysis, iteration loops.
  allowed_content: [taxonomy, definition, procedure, checklist, eval_case]
  forbidden_content: [raw_private_trades, account_pnl_as_general_evidence, project_only_labels_without_mapping]
  typical_source_type: [internal_report, research_report, engineering_article]
  downstream_used_for: [trade_analysis, strategy_iteration, llm_training]
  review_requirements: [sanitization_required_for_contributions, label_definition_required, applicability_required]
  migration_notes: v1 KB_07_TRADE_ANALYSIS becomes v2 KB_08_TRADE_ANALYSIS.

- partition_id: KB_09_LLM_TRAINING
  name: LLM Training
  canonical_root: kt.ai_engineering.llm_training
  domain: llm_training
  purpose: RAG-vs-finetune decisions, dataset design, SFT/LoRA/QLoRA, preference training, eval design, model release, safety boundaries.
  allowed_content: [schema, procedure, checklist, eval_case, anti_pattern]
  forbidden_content: [unlicensed_data, secrets, private_prompts_with_credentials, market_facts_as_finetune_targets]
  typical_source_type: [official_doc, framework_doc, paper, engineering_article]
  downstream_used_for: [llm_training, eval, rag_engineering]
  review_requirements: [license_required_when_applicable, train_eval_split_required, eval_metric_required]
  migration_notes: v1 KB_08_LLM_TRAINING becomes v2 KB_09_LLM_TRAINING.

- partition_id: KB_10_RAG_ENGINEERING
  name: RAG Engineering
  canonical_root: kt.ai_engineering.rag_engineering
  domain: rag_engineering
  purpose: Metadata, chunking, retrieval, rerank, citation, source quality, conflict-aware retrieval, freshness policy.
  allowed_content: [schema, procedure, checklist, anti_pattern, eval_case]
  forbidden_content: [untraceable_snippets, dropped_source_metadata, unsafe_write_tools]
  typical_source_type: [official_doc, framework_doc, paper, engineering_article]
  downstream_used_for: [rag_engineering, vue_audit_ui, quality_eval]
  review_requirements: [source_traceability_required, retrieval_eval_recommended, citation_required]
  migration_notes: v1 KB_09_RAG_ENGINEERING splits into v2 KB_10_RAG_ENGINEERING and KB_11_MCP_ENGINEERING.

- partition_id: KB_11_MCP_ENGINEERING
  name: MCP and Agent Engineering
  canonical_root: kt.ai_engineering.mcp_engineering
  domain: mcp_engineering
  purpose: MCP tool contracts, permission boundaries, runtime config, errors, observability, cross-project query, read-only policy, agent routing.
  allowed_content: [schema, procedure, checklist, anti_pattern, runbook]
  forbidden_content: [unsafe_write_permissions_without_review, secrets, hidden_tool_side_effects]
  typical_source_type: [official_doc, framework_doc, code_doc, runbook]
  downstream_used_for: [mcp, code_review, project_integration, vue_audit_ui]
  review_requirements: [permission_boundary_required, error_schema_required, read_only_default_required]
  migration_notes: New v2 split from v1 KB_09_RAG_ENGINEERING.

- partition_id: KB_12_PROJECT_INTEGRATION
  name: Project Integration
  canonical_root: kt.project_integration
  domain: project_integration
  purpose: Adapters, truth boundary, field mapping, health checks, contribution flow, and sanitized project integration.
  allowed_content: [schema, procedure, checklist, adapter_rule, runbook]
  forbidden_content: [raw_secrets, unsanitized_account_data, private_field_dictionary_without_mapping]
  typical_source_type: [runbook, task_card, code_doc, internal_report]
  downstream_used_for: [project_integration, knowledge_contribution, audit]
  review_requirements: [truth_boundary_required, sanitization_required, project_binding_required]
  migration_notes: Expands v1 KB_10_PROJECT_RUNBOOKS project integration content.

- partition_id: KB_13_KNOWLEDGE_GOVERNANCE
  name: Knowledge Governance
  canonical_root: kt.knowledge_governance
  domain: knowledge_governance
  purpose: Status lifecycle, evidence policy, conflict resolution, source quality, versioning, deprecation, contribution review.
  allowed_content: [schema, procedure, checklist, anti_pattern, audit_rule]
  forbidden_content: [trading_signal_claims, project_private_facts, unsourced_policy_changes]
  typical_source_type: [runbook, task_card, official_doc, framework_doc, code_doc]
  downstream_used_for: [rag_engineering, mcp, vue_audit_ui, quality_eval, project_integration]
  review_requirements: [policy_source_required, audit_log_required, human_review_required_for_major_policy_change]
  migration_notes: New v2 governance partition.
```

## v1 to v2 Partition Compatibility

| v1 Partition | v2 Primary Mapping | Notes |
| --- | --- | --- |
| `KB_01_QUANT_FOUNDATION` | `KB_01_QUANT_FOUNDATION` | retained |
| `KB_02_KLINE_STRATEGY` | `KB_03_STRATEGY_ENGINEERING` | K-line strategy becomes a strategy capability |
| `KB_03_MARKET_MICROSTRUCTURE` | `KB_03_STRATEGY_ENGINEERING` | microstructure becomes a strategy capability |
| `KB_04_BACKTEST` | `KB_04_BACKTEST` | retained |
| `KB_05_REPLAY_SIMULATION` | `KB_05_REPLAY_SIMULATION` | retained |
| `KB_06_LIVE_EXECUTION` | `KB_06_LIVE_EXECUTION` | retained |
| `KB_07_TRADE_ANALYSIS` | `KB_08_TRADE_ANALYSIS` | renumbered |
| `KB_08_LLM_TRAINING` | `KB_09_LLM_TRAINING` | renumbered |
| `KB_09_RAG_ENGINEERING` | `KB_10_RAG_ENGINEERING`, `KB_11_MCP_ENGINEERING` | split |
| `KB_10_PROJECT_RUNBOOKS` | `KB_12_PROJECT_INTEGRATION`, `KB_13_KNOWLEDGE_GOVERNANCE` | split by integration vs governance |

## DoD

```text
1. All v2 partitions have canonical roots.
2. v1 partitions have compatibility mappings.
3. Project-private facts remain forbidden.
4. Risk, evidence, and review requirements are explicit.
5. UTF-8 Chinese display remains readable.
```

