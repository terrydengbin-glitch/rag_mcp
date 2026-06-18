# CEK-TA Knowledge Tree v2 Draft

This file defines the v2 canonical knowledge tree draft for CEK-TA.

It is not the default production tree yet. The current default remains `knowledge_tree.md`. v2 nodes are used for governance design, alias migration, future RAG/MCP routing, and Vue3 audit enhancement.

## Tree Contract

```text
schema: codex-expert-kit/rag/knowledge_tree_node_v2_schema.md
alias_map: codex-expert-kit/rag/knowledge_tree_aliases.md
root_node_id: kt
version: 2.0.0-draft
encoding: UTF-8
created_at: 2026-06-08
updated_at: 2026-06-08
default_tree: false
```

## Global Rules

```text
1. v1 node_id remains valid through knowledge_tree_aliases.md.
2. canonical_node_id is preferred for new v2 routing and future metadata.
3. Node approval does not approve knowledge items under the node.
4. Empty and partial nodes must not be displayed as professional guidance.
5. Market, asset, timeframe, data_granularity, project_type, fee, slippage, latency, and execution assumptions remain applicability fields.
6. No node may contain project-private facts as general CEK-TA knowledge.
7. No node implies investment advice, live-trading permission, or strategy profitability.
```

## Root

```yaml
- node_id: kt
  canonical_node_id: kt
  parent_id: null
  canonical_parent_id: null
  aliases: []
  path: CEK-TA
  canonical_path: CEK-TA
  title: CEK-TA Knowledge Tree
  domain: root
  capability: root
  topic: root
  subdomain: root
  level: 0
  summary: Root node for reusable trading engineering, AI engineering, project integration, and knowledge governance.
  scope: CEK-TA reusable professional knowledge taxonomy and governance.
  out_of_scope: Project-private facts, raw market data, raw order data, secrets, and investment advice.
  key_concepts: [reusable knowledge, auditability, source-backed rules, governance]
  expected_knowledge_types: [schema, procedure, checklist]
  status:
    node_status: reviewing
    coverage_status: partial
    review_status: reviewed
    freshness_status: stable
    conflict_status: none
    migration_status: canonical_ready
    maturity: v2
  routing:
    kb_partition: null
    used_for: [rag_engineering, mcp, vue_audit_ui]
    default_retrieval_allowed: false
    allowed_review_statuses_for_default: [approved]
    allowed_conflict_statuses_for_default: [none, resolved]
    include_children_default: true
    routing_policy: include_children
  governance:
    risk_level: medium
    project_binding: governance_only
    evidence_required: [source_evidence, review_status, conflict_status]
    source_policy:
      required: false
      preferred_source_types: [runbook, task_card, code_doc]
      minimum_reliability: medium
    conflict_policy: governance_only
    default_policy: null
    approval_policy: node_approval_only
  relations:
    related_nodes: []
    split_targets: []
    merged_from: []
    supersedes: []
    superseded_by: []
  ownership:
    owner: governance
    approved_by: null
    created_at: 2026-06-08
    updated_at: 2026-06-08
    version: 2026-06
```

## Level 1 Branches

```yaml
- node_id: kt.trading_engineering
  canonical_node_id: kt.trading_engineering
  parent_id: kt
  canonical_parent_id: kt
  aliases: []
  path: CEK-TA / Trading Engineering
  canonical_path: CEK-TA / Trading Engineering
  title: Trading Engineering
  domain: trading_engineering
  capability: trading_engineering
  topic: trading_engineering
  subdomain: trading_engineering
  level: 1
  summary: End-to-end trading engineering knowledge for data, quant foundations, strategy, backtest, replay, execution, risk, and trade analysis.
  scope: Professional trading engineering knowledge, not raw market data collection.
  out_of_scope: Investment advice, project-only strategy thresholds, secrets, account configuration.
  key_concepts: [data engineering, strategy, backtest, replay, execution, risk, trade analysis]
  expected_knowledge_types: [definition, principle, procedure, checklist, anti_pattern, eval_case]
  status:
    node_status: reviewing
    coverage_status: partial
    review_status: reviewed
    freshness_status: stable
    conflict_status: unchecked
    migration_status: canonical_ready
    maturity: v2
  routing:
    kb_partition: null
    used_for: [strategy_design, code_review, backtest_review, simulation, live_trading, trade_analysis]
    default_retrieval_allowed: false
    allowed_review_statuses_for_default: [approved]
    allowed_conflict_statuses_for_default: [none, resolved]
    include_children_default: true
    routing_policy: include_children
  governance:
    risk_level: high
    project_binding: none
    evidence_required: [market, timeframe, data_granularity, applicability_boundary, source_evidence]
    source_policy:
      required: true
      preferred_source_types: [paper, book, official_doc, exchange_rule, framework_doc, engineering_article]
      minimum_reliability: medium
    conflict_policy: block_unresolved
    default_policy: prefer explicit applicability boundaries over broad trading claims
    approval_policy: item_approval_required
  relations:
    related_nodes: [kt.knowledge_governance.evidence_policy, kt.knowledge_governance.conflict_resolution]
    split_targets: []
    merged_from: [kt.quant_foundation, kt.kline_strategy, kt.market_microstructure, kt.backtest, kt.replay_simulation, kt.live_execution, kt.trade_analysis]
    supersedes: []
    superseded_by: []
  ownership:
    owner: trading
    approved_by: null
    created_at: 2026-06-08
    updated_at: 2026-06-08
    version: 2026-06

- node_id: kt.ai_engineering
  canonical_node_id: kt.ai_engineering
  parent_id: kt
  canonical_parent_id: kt
  aliases: []
  path: CEK-TA / AI Engineering
  canonical_path: CEK-TA / AI Engineering
  title: AI Engineering
  domain: ai_engineering
  capability: ai_engineering
  topic: ai_engineering
  subdomain: ai_engineering
  level: 1
  summary: Reusable knowledge for LLM training, RAG, MCP, and agent engineering.
  scope: AI engineering knowledge used to support Codex and downstream trading projects.
  out_of_scope: Unlicensed training data, private prompts with secrets, unsourced model claims.
  key_concepts: [LLM, RAG, MCP, agent, dataset, eval]
  expected_knowledge_types: [schema, procedure, checklist, eval_case, anti_pattern]
  status:
    node_status: reviewing
    coverage_status: partial
    review_status: reviewed
    freshness_status: time_sensitive
    conflict_status: unchecked
    migration_status: canonical_ready
    maturity: v2
  routing:
    kb_partition: null
    used_for: [llm_training, rag_engineering, mcp, code_review, vue_audit_ui]
    default_retrieval_allowed: false
    allowed_review_statuses_for_default: [approved]
    allowed_conflict_statuses_for_default: [none, resolved]
    include_children_default: true
    routing_policy: include_children
  governance:
    risk_level: medium
    project_binding: none
    evidence_required: [source_evidence, version, freshness, license_or_policy_when_applicable]
    source_policy:
      required: true
      preferred_source_types: [official_doc, framework_doc, paper, engineering_article]
      minimum_reliability: medium
    conflict_policy: prefer_official_source
    default_policy: require version and freshness for APIs, models, frameworks, and tools
    approval_policy: item_approval_required
  relations:
    related_nodes: [kt.knowledge_governance.source_quality, kt.knowledge_governance.versioning]
    split_targets: []
    merged_from: [kt.llm_training, kt.rag_engineering, kt.mcp]
    supersedes: []
    superseded_by: []
  ownership:
    owner: ai
    approved_by: null
    created_at: 2026-06-08
    updated_at: 2026-06-08
    version: 2026-06

- node_id: kt.project_integration
  canonical_node_id: kt.project_integration
  parent_id: kt
  canonical_parent_id: kt
  aliases: []
  path: CEK-TA / Project Integration
  canonical_path: CEK-TA / Project Integration
  title: Project Integration
  domain: project_integration
  capability: project_integration
  topic: project_integration
  subdomain: project_integration
  level: 1
  summary: Knowledge for external project connection, fact boundaries, field mapping, health checks, and contributions.
  scope: Cross-project integration and contribution governance.
  out_of_scope: Raw project secrets, private order/account data, project-only facts as general CEK-TA rules.
  key_concepts: [adapter, truth boundary, field mapping, healthcheck, contribution]
  expected_knowledge_types: [schema, procedure, checklist, adapter_rule, anti_pattern]
  status:
    node_status: reviewing
    coverage_status: partial
    review_status: reviewed
    freshness_status: stable
    conflict_status: none
    migration_status: canonical_ready
    maturity: v2
  routing:
    kb_partition: KB_12_PROJECT_INTEGRATION
    used_for: [project_integration, knowledge_contribution, mcp, vue_audit_ui]
    default_retrieval_allowed: false
    allowed_review_statuses_for_default: [approved]
    allowed_conflict_statuses_for_default: [none, resolved]
    include_children_default: true
    routing_policy: include_children
  governance:
    risk_level: high
    project_binding: none
    evidence_required: [project_binding, truth_boundary, sanitization_status]
    source_policy:
      required: true
      preferred_source_types: [runbook, task_card, code_doc, internal_report]
      minimum_reliability: medium
    conflict_policy: block_unresolved
    default_policy: keep project facts in the external project unless sanitized and reviewed
    approval_policy: item_approval_required
  relations:
    related_nodes: [kt.knowledge_governance.contribution_review]
    split_targets: []
    merged_from: []
    supersedes: []
    superseded_by: []
  ownership:
    owner: project_integration
    approved_by: null
    created_at: 2026-06-08
    updated_at: 2026-06-08
    version: 2026-06

- node_id: kt.knowledge_governance
  canonical_node_id: kt.knowledge_governance
  parent_id: kt
  canonical_parent_id: kt
  aliases: []
  path: CEK-TA / Knowledge Governance
  canonical_path: CEK-TA / Knowledge Governance
  title: Knowledge Governance
  domain: knowledge_governance
  capability: knowledge_governance
  topic: knowledge_governance
  subdomain: knowledge_governance
  level: 1
  summary: Governance knowledge for status lifecycle, evidence policy, conflict resolution, source quality, versioning, deprecation, and contribution review.
  scope: Rules that decide whether knowledge can be trusted, retrieved, reused, deprecated, or contributed.
  out_of_scope: Trading rules themselves, project-private evidence, raw source dumps.
  key_concepts: [status, evidence, conflict, source quality, versioning, deprecation]
  expected_knowledge_types: [schema, procedure, checklist, anti_pattern]
  status:
    node_status: reviewing
    coverage_status: partial
    review_status: reviewed
    freshness_status: stable
    conflict_status: none
    migration_status: canonical_ready
    maturity: v2
  routing:
    kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
    used_for: [rag_engineering, mcp, vue_audit_ui, project_integration, knowledge_contribution]
    default_retrieval_allowed: false
    allowed_review_statuses_for_default: [approved]
    allowed_conflict_statuses_for_default: [none, resolved]
    include_children_default: true
    routing_policy: governance_only
  governance:
    risk_level: critical
    project_binding: governance_only
    evidence_required: [policy_source, audit_log, reviewer]
    source_policy:
      required: true
      preferred_source_types: [runbook, task_card, official_doc, framework_doc]
      minimum_reliability: medium
    conflict_policy: governance_only
    default_policy: never treat candidate, conflicted, deprecated, or unsourced knowledge as default guidance
    approval_policy: node_approval_only
  relations:
    related_nodes: [kt.project_integration.contribution, kt.ai_engineering.rag_engineering.source_quality]
    split_targets: []
    merged_from: []
    supersedes: []
    superseded_by: []
  ownership:
    owner: governance
    approved_by: null
    created_at: 2026-06-08
    updated_at: 2026-06-08
    version: 2026-06
```

## Trading Engineering Branch

```yaml
- canonical_node_id: kt.trading_engineering.data_engineering
  parent: kt.trading_engineering
  title: Data Engineering
  kb_partition: KB_02_DATA_ENGINEERING
  domain: data_engineering
  capability: data_engineering
  level: 2
  node_status: candidate
  risk_level: high
  summary: Market data contracts, time alignment, quality checks, feature pipelines, versioning, and observability.
  children:
    - kt.trading_engineering.data_engineering.market_data_schema
    - kt.trading_engineering.data_engineering.time_alignment
    - kt.trading_engineering.data_engineering.data_quality
    - kt.trading_engineering.data_engineering.feature_pipeline
    - kt.trading_engineering.data_engineering.versioning
    - kt.trading_engineering.data_engineering.observability

- canonical_node_id: kt.trading_engineering.quant_foundation
  aliases: [kt.quant_foundation]
  parent: kt.trading_engineering
  title: Quant Foundation
  kb_partition: KB_01_QUANT_FOUNDATION
  domain: quant_trading
  capability: quant_foundation
  level: 2
  node_status: reviewing
  risk_level: medium
  summary: Signal flow, EV/RR/cost, probability and expectancy, position sizing theory, and trade lifecycle.
  children:
    - kt.trading_engineering.quant_foundation.signal_flow
    - kt.trading_engineering.quant_foundation.ev_rr_cost
    - kt.trading_engineering.quant_foundation.probability_expectancy
    - kt.trading_engineering.quant_foundation.position_sizing_theory
    - kt.trading_engineering.quant_foundation.trade_lifecycle

- canonical_node_id: kt.trading_engineering.strategy_engineering
  parent: kt.trading_engineering
  title: Strategy Engineering
  kb_partition: KB_03_STRATEGY_ENGINEERING
  domain: strategy_engineering
  capability: strategy_engineering
  level: 2
  node_status: candidate
  risk_level: high
  summary: Signal, direction, entry, exit, scoring gates, regime detection, multi-strategy fusion, K-line strategy, microstructure, and derivatives flow.
  children:
    - kt.trading_engineering.strategy_engineering.signal_design
    - kt.trading_engineering.strategy_engineering.direction_model
    - kt.trading_engineering.strategy_engineering.entry_model
    - kt.trading_engineering.strategy_engineering.exit_model
    - kt.trading_engineering.strategy_engineering.scoring_gate_guard
    - kt.trading_engineering.strategy_engineering.regime_detection
    - kt.trading_engineering.strategy_engineering.multi_strategy_fusion
    - kt.trading_engineering.strategy_engineering.kline_strategy
    - kt.trading_engineering.strategy_engineering.market_microstructure
    - kt.trading_engineering.strategy_engineering.derivatives_flow

- canonical_node_id: kt.trading_engineering.strategy_engineering.kline_strategy
  aliases: [kt.kline_strategy]
  parent: kt.trading_engineering.strategy_engineering
  title: Kline Strategy
  kb_partition: KB_03_STRATEGY_ENGINEERING
  domain: strategy_engineering
  capability: kline_strategy
  level: 3
  node_status: conditional
  risk_level: medium
  summary: Professional K-line trading knowledge about structure, entries/exits, indicators, and multi-timeframe reasoning. Not raw K-line data collection.
  children:
    - kt.trading_engineering.strategy_engineering.kline_strategy.market_structure
    - kt.trading_engineering.strategy_engineering.kline_strategy.entry_exit
    - kt.trading_engineering.strategy_engineering.kline_strategy.indicators
    - kt.trading_engineering.strategy_engineering.kline_strategy.multi_timeframe

- canonical_node_id: kt.trading_engineering.strategy_engineering.market_microstructure
  aliases: [kt.market_microstructure]
  parent: kt.trading_engineering.strategy_engineering
  title: Market Microstructure
  kb_partition: KB_03_STRATEGY_ENGINEERING
  domain: strategy_engineering
  capability: market_microstructure
  level: 3
  node_status: conditional
  risk_level: high
  summary: Order flow, CVD, OFI, depth, liquidity, spread, and microstructure feature caveats.
  children:
    - kt.trading_engineering.strategy_engineering.market_microstructure.order_flow
    - kt.trading_engineering.strategy_engineering.market_microstructure.cvd
    - kt.trading_engineering.strategy_engineering.market_microstructure.ofi
    - kt.trading_engineering.strategy_engineering.market_microstructure.depth
    - kt.trading_engineering.strategy_engineering.market_microstructure.liquidity

- canonical_node_id: kt.trading_engineering.strategy_engineering.derivatives_flow
  parent: kt.trading_engineering.strategy_engineering
  title: Derivatives Flow
  kb_partition: KB_03_STRATEGY_ENGINEERING
  domain: strategy_engineering
  capability: derivatives_flow
  level: 3
  node_status: candidate
  risk_level: high
  summary: Open interest, funding, basis, liquidation, crowding, squeeze and flush interpretation boundaries.
  children:
    - kt.trading_engineering.strategy_engineering.derivatives_flow.open_interest
    - kt.trading_engineering.strategy_engineering.derivatives_flow.funding
    - kt.trading_engineering.strategy_engineering.derivatives_flow.basis
    - kt.trading_engineering.strategy_engineering.derivatives_flow.liquidation
    - kt.trading_engineering.strategy_engineering.derivatives_flow.crowding

- canonical_node_id: kt.trading_engineering.backtest
  aliases: [kt.backtest]
  parent: kt.trading_engineering
  title: Backtest
  kb_partition: KB_04_BACKTEST
  domain: backtest
  capability: backtest
  level: 2
  node_status: reviewing
  risk_level: high
  summary: Backtest credibility, bias, scenario data quality, fill assumptions, costs, metrics, walk-forward, and reproducibility.
  children:
    - kt.trading_engineering.backtest.bias
    - kt.trading_engineering.backtest.data_quality
    - kt.trading_engineering.backtest.fill_assumption
    - kt.trading_engineering.backtest.cost_model
    - kt.trading_engineering.backtest.metrics
    - kt.trading_engineering.backtest.walk_forward
    - kt.trading_engineering.backtest.reproducibility

- canonical_node_id: kt.trading_engineering.replay_simulation
  aliases: [kt.replay_simulation]
  parent: kt.trading_engineering
  title: Replay and Simulation
  kb_partition: KB_05_REPLAY_SIMULATION
  domain: replay_simulation
  capability: replay_simulation
  level: 2
  node_status: reviewing
  risk_level: high
  summary: Replay clock, event replay, market state reconstruction, fill model, slippage, latency, fidelity levels, and paper trading.
  children:
    - kt.trading_engineering.replay_simulation.replay_clock
    - kt.trading_engineering.replay_simulation.event_replay
    - kt.trading_engineering.replay_simulation.market_state_reconstruction
    - kt.trading_engineering.replay_simulation.fill_model
    - kt.trading_engineering.replay_simulation.slippage_model
    - kt.trading_engineering.replay_simulation.latency_model
    - kt.trading_engineering.replay_simulation.fidelity_level
    - kt.trading_engineering.replay_simulation.paper_trading

- canonical_node_id: kt.trading_engineering.live_execution
  aliases: [kt.live_execution]
  parent: kt.trading_engineering
  title: Live Execution
  kb_partition: KB_06_LIVE_EXECUTION
  domain: live_trading
  capability: live_execution
  level: 2
  node_status: reviewing
  risk_level: critical
  summary: Exchange adapters, order state machines, position reconciliation, account safety, incident response, and kill switches.
  children:
    - kt.trading_engineering.live_execution.exchange_adapter
    - kt.trading_engineering.live_execution.order_state_machine
    - kt.trading_engineering.live_execution.position_reconciliation
    - kt.trading_engineering.live_execution.account_safety
    - kt.trading_engineering.live_execution.incident_response
    - kt.trading_engineering.live_execution.kill_switch

- canonical_node_id: kt.trading_engineering.risk_management
  parent: kt.trading_engineering
  title: Risk Management
  kb_partition: KB_07_RISK_MANAGEMENT
  domain: risk_management
  capability: risk_management
  level: 2
  node_status: candidate
  risk_level: critical
  summary: Risk gates, position sizing, drawdown control, leverage policy, exposure control, daily loss limits, and ruin risk.
  children:
    - kt.trading_engineering.risk_management.risk_gate
    - kt.trading_engineering.risk_management.position_sizing
    - kt.trading_engineering.risk_management.drawdown_control
    - kt.trading_engineering.risk_management.leverage_policy
    - kt.trading_engineering.risk_management.exposure_control
    - kt.trading_engineering.risk_management.daily_loss_limit
    - kt.trading_engineering.risk_management.ruin_risk

- canonical_node_id: kt.trading_engineering.trade_analysis
  aliases: [kt.trade_analysis]
  parent: kt.trading_engineering
  title: Trade Analysis
  kb_partition: KB_08_TRADE_ANALYSIS
  domain: trade_analysis
  capability: trade_analysis
  level: 2
  node_status: reviewing
  risk_level: medium
  summary: Trade quality metrics, bad-case taxonomy, label schema, R/R decomposition, cost decomposition, time/setup buckets, and iteration loops.
  children:
    - kt.trading_engineering.trade_analysis.trade_quality_metrics
    - kt.trading_engineering.trade_analysis.bad_case_taxonomy
    - kt.trading_engineering.trade_analysis.label_schema
    - kt.trading_engineering.trade_analysis.rr_decomposition
    - kt.trading_engineering.trade_analysis.cost_decomposition
    - kt.trading_engineering.trade_analysis.time_bucket_analysis
    - kt.trading_engineering.trade_analysis.setup_bucket_analysis
    - kt.trading_engineering.trade_analysis.iteration_loop
```

## AI Engineering Branch

```yaml
- canonical_node_id: kt.ai_engineering.llm_training
  aliases: [kt.llm_training]
  parent: kt.ai_engineering
  title: LLM Training
  kb_partition: KB_09_LLM_TRAINING
  domain: llm_training
  capability: llm_training
  level: 2
  node_status: reviewing
  risk_level: high
  summary: RAG vs finetune, dataset design, SFT/LoRA/QLoRA, preference training, eval design, bad-case regression, model release, and safety boundaries.
  children:
    - kt.ai_engineering.llm_training.rag_vs_finetune
    - kt.ai_engineering.llm_training.dataset_design
    - kt.ai_engineering.llm_training.sft_lora_qlora
    - kt.ai_engineering.llm_training.preference_training
    - kt.ai_engineering.llm_training.eval_design
    - kt.ai_engineering.llm_training.bad_case_regression
    - kt.ai_engineering.llm_training.model_release
    - kt.ai_engineering.llm_training.safety_boundary

- canonical_node_id: kt.ai_engineering.rag_engineering
  aliases: [kt.rag_engineering]
  parent: kt.ai_engineering
  title: RAG Engineering
  kb_partition: KB_10_RAG_ENGINEERING
  domain: rag_engineering
  capability: rag_engineering
  level: 2
  node_status: reviewing
  risk_level: high
  summary: Metadata, chunking, retrieval, rerank, citation, source quality, conflict-aware retrieval, and freshness policy.
  children:
    - kt.ai_engineering.rag_engineering.metadata_schema
    - kt.ai_engineering.rag_engineering.chunking_policy
    - kt.ai_engineering.rag_engineering.retrieval_policy
    - kt.ai_engineering.rag_engineering.rerank_policy
    - kt.ai_engineering.rag_engineering.citation_policy
    - kt.ai_engineering.rag_engineering.source_quality
    - kt.ai_engineering.rag_engineering.conflict_aware_retrieval
    - kt.ai_engineering.rag_engineering.freshness_policy

- canonical_node_id: kt.ai_engineering.mcp_engineering
  aliases: [kt.mcp]
  parent: kt.ai_engineering
  title: MCP Engineering
  kb_partition: KB_11_MCP_ENGINEERING
  domain: mcp_engineering
  capability: mcp_engineering
  level: 2
  node_status: reviewing
  risk_level: high
  summary: Tool contracts, permission boundaries, runtime config, errors, observability, cross-project query, and read-only policy.
  children:
    - kt.ai_engineering.mcp_engineering.tool_contract
    - kt.ai_engineering.mcp_engineering.permission_boundary
    - kt.ai_engineering.mcp_engineering.runtime_config
    - kt.ai_engineering.mcp_engineering.error_schema
    - kt.ai_engineering.mcp_engineering.observability
    - kt.ai_engineering.mcp_engineering.cross_project_query
    - kt.ai_engineering.mcp_engineering.read_only_policy
    - kt.ai_engineering.mcp_engineering.knowledge_tools

- canonical_node_id: kt.ai_engineering.agent_engineering
  parent: kt.ai_engineering
  title: Agent Engineering
  kb_partition: KB_11_MCP_ENGINEERING
  domain: agent_engineering
  capability: agent_engineering
  level: 2
  node_status: candidate
  risk_level: medium
  summary: Agent role design, skill routing, tool-use policy, memory policy, and human review gates.
  children:
    - kt.ai_engineering.agent_engineering.agent_role_design
    - kt.ai_engineering.agent_engineering.skill_routing
    - kt.ai_engineering.agent_engineering.tool_use_policy
    - kt.ai_engineering.agent_engineering.memory_policy
    - kt.ai_engineering.agent_engineering.human_review
```

## Project Integration Branch

```yaml
- canonical_node_id: kt.project_integration.adapter
  parent: kt.project_integration
  title: Project Adapter
  kb_partition: KB_12_PROJECT_INTEGRATION
  domain: project_integration
  capability: adapter
  level: 2
  node_status: reviewing
  risk_level: high
  summary: External project identity, facts, runtime modes, permissions, and contribution policy.

- canonical_node_id: kt.project_integration.truth_boundary
  parent: kt.project_integration
  title: Truth Boundary
  kb_partition: KB_12_PROJECT_INTEGRATION
  domain: project_integration
  capability: truth_boundary
  level: 2
  node_status: candidate
  risk_level: critical
  summary: Separates general CEK-TA knowledge, project facts, historical facts, current config, deprecated logic, reusable contributions, and local-only data.

- canonical_node_id: kt.project_integration.field_mapping
  parent: kt.project_integration
  title: Field Mapping
  kb_partition: KB_12_PROJECT_INTEGRATION
  domain: project_integration
  capability: field_mapping
  level: 2
  node_status: candidate
  risk_level: high
  summary: Maps project-specific fields into generic CEK-TA contracts without leaking private implementation details.

- canonical_node_id: kt.project_integration.healthcheck
  parent: kt.project_integration
  title: Healthcheck
  kb_partition: KB_12_PROJECT_INTEGRATION
  domain: project_integration
  capability: healthcheck
  level: 2
  node_status: reviewing
  risk_level: medium
  summary: Checks CEK-TA path, project facts, runtime modes, field mapping, permissions, MCP config, contribution readiness, and rollback.

- canonical_node_id: kt.project_integration.contribution
  parent: kt.project_integration
  title: Knowledge Contribution
  kb_partition: KB_12_PROJECT_INTEGRATION
  domain: project_integration
  capability: contribution
  level: 2
  node_status: reviewing
  risk_level: high
  summary: Sanitized contribution flow from project case to evidence, classification, conflict check, review, and publication.
```

## Knowledge Governance Branch

```yaml
- canonical_node_id: kt.knowledge_governance.status_lifecycle
  parent: kt.knowledge_governance
  title: Status Lifecycle
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: status_lifecycle
  level: 2
  node_status: candidate
  risk_level: critical
  summary: Draft, candidate, reviewing, approved, conditional, conflicted, deprecated, and archived lifecycle rules.

- canonical_node_id: kt.knowledge_governance.evidence_policy
  parent: kt.knowledge_governance
  title: Evidence Policy
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: evidence_policy
  level: 2
  node_status: candidate
  risk_level: critical
  summary: Source, applicability, freshness, citation, and audit evidence requirements.

- canonical_node_id: kt.knowledge_governance.conflict_resolution
  parent: kt.knowledge_governance
  title: Conflict Resolution
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: conflict_resolution
  level: 2
  node_status: candidate
  risk_level: critical
  summary: Rules for direct, scope, version, market, granularity, and assumption conflicts.

- canonical_node_id: kt.knowledge_governance.source_quality
  parent: kt.knowledge_governance
  title: Source Quality
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: source_quality
  level: 2
  node_status: candidate
  risk_level: high
  summary: Source reliability scoring, mandatory downgrades, freshness windows, and reuse safety.

- canonical_node_id: kt.knowledge_governance.versioning
  parent: kt.knowledge_governance
  title: Versioning
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: versioning
  level: 2
  node_status: candidate
  risk_level: high
  summary: Version policy for knowledge nodes, items, aliases, partitions, schemas, and migrations.

- canonical_node_id: kt.knowledge_governance.deprecation
  parent: kt.knowledge_governance
  title: Deprecation
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: deprecation
  level: 2
  node_status: candidate
  risk_level: high
  summary: Deprecation and archival rules for stale, superseded, unsafe, or conflicted knowledge.

- canonical_node_id: kt.knowledge_governance.contribution_review
  parent: kt.knowledge_governance
  title: Contribution Review
  kb_partition: KB_13_KNOWLEDGE_GOVERNANCE
  domain: knowledge_governance
  capability: contribution_review
  level: 2
  node_status: candidate
  risk_level: high
  summary: Review gate for external project knowledge contributions before they can become reusable CEK-TA knowledge.
```

## Primary Partition Mapping

| Canonical Node | Primary Partition |
| --- | --- |
| `kt.trading_engineering.quant_foundation` | `KB_01_QUANT_FOUNDATION` |
| `kt.trading_engineering.data_engineering` | `KB_02_DATA_ENGINEERING` |
| `kt.trading_engineering.strategy_engineering` | `KB_03_STRATEGY_ENGINEERING` |
| `kt.trading_engineering.backtest` | `KB_04_BACKTEST` |
| `kt.trading_engineering.replay_simulation` | `KB_05_REPLAY_SIMULATION` |
| `kt.trading_engineering.live_execution` | `KB_06_LIVE_EXECUTION` |
| `kt.trading_engineering.risk_management` | `KB_07_RISK_MANAGEMENT` |
| `kt.trading_engineering.trade_analysis` | `KB_08_TRADE_ANALYSIS` |
| `kt.ai_engineering.llm_training` | `KB_09_LLM_TRAINING` |
| `kt.ai_engineering.rag_engineering` | `KB_10_RAG_ENGINEERING` |
| `kt.ai_engineering.mcp_engineering`、`kt.ai_engineering.agent_engineering` | `KB_11_MCP_ENGINEERING` |
| `kt.project_integration` | `KB_12_PROJECT_INTEGRATION` |
| `kt.knowledge_governance` | `KB_13_KNOWLEDGE_GOVERNANCE` |

## v2 Coverage Notes

```text
1. This file is a v2 draft, not the default tree.
2. Nodes marked candidate need review before default routing.
3. Critical and high risk nodes require explicit evidence, conflict status, and applicability boundaries before guidance use.
4. Kline Strategy means professional K-line trading knowledge; CEK-TA does not collect raw K-line market data.
5. Derivatives Flow requires strict caveats: funding positive is not bullish by itself, OI increase does not guarantee trend continuation, and crowding signals are conditional.
```

