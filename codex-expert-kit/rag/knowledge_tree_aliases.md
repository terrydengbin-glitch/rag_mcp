# CEK-TA Knowledge Tree v1 to v2 Alias Mapping

本文件定义当前 v1 `node_id` 到 v2 `canonical_node_id` 的兼容映射。它是迁移索引，不是正式知识树本体。

## Contract

```text
schema_name: cek_ta_knowledge_tree_aliases
schema_version: 1.0.0
encoding: UTF-8
source_tree: codex-expert-kit/rag/knowledge_tree.md
target_schema: codex-expert-kit/rag/knowledge_tree_node_v2_schema.md
created_at: 2026-06-08
updated_at: 2026-06-08
```

## Resolution Rules

```text
1. v1_node_id 必须保持可解析。
2. canonical_node_id 是 v2 推荐路径。
3. migration_status 初始为 alias_supported。
4. split_targets 只能用于审计和 include_children，不用于默认检索。
5. 若 canonical_node_id 尚未在 knowledge_tree_v2.md 中创建，仍可作为规划路径。
```

## Alias Records

```yaml
- v1_node_id: kt
  canonical_node_id: kt
  v1_parent_id: null
  canonical_parent_id: null
  v1_path: CEK-TA
  canonical_path: CEK-TA
  title: CEK-TA Knowledge Tree
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets: []

- v1_node_id: kt.trading_engineering
  canonical_node_id: kt.trading_engineering
  v1_parent_id: kt
  canonical_parent_id: kt
  v1_path: CEK-TA / Trading Engineering
  canonical_path: CEK-TA / Trading Engineering
  title: Trading Engineering
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets: []

- v1_node_id: kt.ai_engineering
  canonical_node_id: kt.ai_engineering
  v1_parent_id: kt
  canonical_parent_id: kt
  v1_path: CEK-TA / AI Engineering
  canonical_path: CEK-TA / AI Engineering
  title: AI Engineering
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets: []

- v1_node_id: kt.project_integration
  canonical_node_id: kt.project_integration
  v1_parent_id: kt
  canonical_parent_id: kt
  v1_path: CEK-TA / Project Integration
  canonical_path: CEK-TA / Project Integration
  title: Project Integration
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets: []

- v1_node_id: kt.quant_foundation
  canonical_node_id: kt.trading_engineering.quant_foundation
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering
  v1_path: CEK-TA / Trading Engineering / Quant Foundation
  canonical_path: CEK-TA / Trading Engineering / Quant Foundation
  title: Quant Foundation
  migration_status: alias_supported
  primary: true
  aliases: [kt.quant_foundation]
  split_targets: []

- v1_node_id: kt.quant_foundation.signal_flow
  canonical_node_id: kt.trading_engineering.quant_foundation.signal_flow
  v1_parent_id: kt.quant_foundation
  canonical_parent_id: kt.trading_engineering.quant_foundation
  v1_path: CEK-TA / Trading Engineering / Quant Foundation / Signal Flow
  canonical_path: CEK-TA / Trading Engineering / Quant Foundation / Signal Flow
  title: Signal Flow
  migration_status: alias_supported
  primary: true
  aliases: [kt.quant_foundation.signal_flow]
  split_targets: []

- v1_node_id: kt.quant_foundation.position_sizing
  canonical_node_id: kt.trading_engineering.quant_foundation.position_sizing_theory
  v1_parent_id: kt.quant_foundation
  canonical_parent_id: kt.trading_engineering.quant_foundation
  v1_path: CEK-TA / Trading Engineering / Quant Foundation / Position Sizing
  canonical_path: CEK-TA / Trading Engineering / Quant Foundation / Position Sizing Theory
  title: Position Sizing
  migration_status: alias_supported
  primary: true
  aliases: [kt.quant_foundation.position_sizing]
  split_targets:
    - kt.trading_engineering.risk_management.position_sizing

- v1_node_id: kt.kline_strategy
  canonical_node_id: kt.trading_engineering.strategy_engineering.kline_strategy
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering.strategy_engineering
  v1_path: CEK-TA / Trading Engineering / Kline Strategy
  canonical_path: CEK-TA / Trading Engineering / Strategy Engineering / Kline Strategy
  title: Kline Strategy
  migration_status: alias_supported
  primary: true
  aliases: [kt.kline_strategy]
  split_targets: []

- v1_node_id: kt.kline_strategy.market_structure
  canonical_node_id: kt.trading_engineering.strategy_engineering.kline_strategy.market_structure
  v1_parent_id: kt.kline_strategy
  canonical_parent_id: kt.trading_engineering.strategy_engineering.kline_strategy
  v1_path: CEK-TA / Trading Engineering / Kline Strategy / Market Structure
  canonical_path: CEK-TA / Trading Engineering / Strategy Engineering / Kline Strategy / Market Structure
  title: Market Structure
  migration_status: alias_supported
  primary: true
  aliases: [kt.kline_strategy.market_structure]
  split_targets: []

- v1_node_id: kt.kline_strategy.entry_exit
  canonical_node_id: kt.trading_engineering.strategy_engineering.kline_strategy.entry_exit
  v1_parent_id: kt.kline_strategy
  canonical_parent_id: kt.trading_engineering.strategy_engineering.kline_strategy
  v1_path: CEK-TA / Trading Engineering / Kline Strategy / Entry And Exit
  canonical_path: CEK-TA / Trading Engineering / Strategy Engineering / Kline Strategy / Entry And Exit
  title: Entry And Exit
  migration_status: alias_supported
  primary: true
  aliases: [kt.kline_strategy.entry_exit]
  split_targets:
    - kt.trading_engineering.strategy_engineering.entry_model
    - kt.trading_engineering.strategy_engineering.exit_model

- v1_node_id: kt.kline_strategy.indicators
  canonical_node_id: kt.trading_engineering.strategy_engineering.kline_strategy.indicators
  v1_parent_id: kt.kline_strategy
  canonical_parent_id: kt.trading_engineering.strategy_engineering.kline_strategy
  v1_path: CEK-TA / Trading Engineering / Kline Strategy / Indicator Boundaries
  canonical_path: CEK-TA / Trading Engineering / Strategy Engineering / Kline Strategy / Indicator Boundaries
  title: Indicator Boundaries
  migration_status: alias_supported
  primary: true
  aliases: [kt.kline_strategy.indicators]
  split_targets: []

- v1_node_id: kt.market_microstructure
  canonical_node_id: kt.trading_engineering.strategy_engineering.market_microstructure
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering.strategy_engineering
  v1_path: CEK-TA / Trading Engineering / Market Microstructure
  canonical_path: CEK-TA / Trading Engineering / Strategy Engineering / Market Microstructure
  title: Market Microstructure
  migration_status: alias_supported
  primary: true
  aliases: [kt.market_microstructure]
  split_targets: []

- v1_node_id: kt.market_microstructure.order_flow
  canonical_node_id: kt.trading_engineering.strategy_engineering.market_microstructure.order_flow
  v1_parent_id: kt.market_microstructure
  canonical_parent_id: kt.trading_engineering.strategy_engineering.market_microstructure
  v1_path: CEK-TA / Trading Engineering / Market Microstructure / Order Flow
  canonical_path: CEK-TA / Trading Engineering / Strategy Engineering / Market Microstructure / Order Flow
  title: Order Flow
  migration_status: alias_supported
  primary: true
  aliases: [kt.market_microstructure.order_flow]
  split_targets:
    - kt.trading_engineering.strategy_engineering.market_microstructure.cvd
    - kt.trading_engineering.strategy_engineering.market_microstructure.ofi

- v1_node_id: kt.backtest
  canonical_node_id: kt.trading_engineering.backtest
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering
  v1_path: CEK-TA / Trading Engineering / Backtest
  canonical_path: CEK-TA / Trading Engineering / Backtest
  title: Backtest
  migration_status: alias_supported
  primary: true
  aliases: [kt.backtest]
  split_targets: []

- v1_node_id: kt.backtest.bias
  canonical_node_id: kt.trading_engineering.backtest.bias
  v1_parent_id: kt.backtest
  canonical_parent_id: kt.trading_engineering.backtest
  v1_path: CEK-TA / Trading Engineering / Backtest / Bias
  canonical_path: CEK-TA / Trading Engineering / Backtest / Bias
  title: Backtest Bias
  migration_status: alias_supported
  primary: true
  aliases: [kt.backtest.bias]
  split_targets: []

- v1_node_id: kt.backtest.data_quality
  canonical_node_id: kt.trading_engineering.backtest.data_quality
  v1_parent_id: kt.backtest
  canonical_parent_id: kt.trading_engineering.backtest
  v1_path: CEK-TA / Trading Engineering / Backtest / Data Quality
  canonical_path: CEK-TA / Trading Engineering / Backtest / Data Quality
  title: Data Quality
  migration_status: alias_supported
  primary: true
  aliases: [kt.backtest.data_quality]
  split_targets:
    - kt.trading_engineering.data_engineering.data_quality

- v1_node_id: kt.backtest.metrics
  canonical_node_id: kt.trading_engineering.backtest.metrics
  v1_parent_id: kt.backtest
  canonical_parent_id: kt.trading_engineering.backtest
  v1_path: CEK-TA / Trading Engineering / Backtest / Metrics
  canonical_path: CEK-TA / Trading Engineering / Backtest / Metrics
  title: Backtest Metrics
  migration_status: alias_supported
  primary: true
  aliases: [kt.backtest.metrics]
  split_targets: []

- v1_node_id: kt.replay_simulation
  canonical_node_id: kt.trading_engineering.replay_simulation
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering
  v1_path: CEK-TA / Trading Engineering / Replay And Simulation
  canonical_path: CEK-TA / Trading Engineering / Replay And Simulation
  title: Replay And Simulation
  migration_status: alias_supported
  primary: true
  aliases: [kt.replay_simulation]
  split_targets: []

- v1_node_id: kt.replay_simulation.fill_model
  canonical_node_id: kt.trading_engineering.replay_simulation.fill_model
  v1_parent_id: kt.replay_simulation
  canonical_parent_id: kt.trading_engineering.replay_simulation
  v1_path: CEK-TA / Trading Engineering / Replay And Simulation / Fill Model
  canonical_path: CEK-TA / Trading Engineering / Replay And Simulation / Fill Model
  title: Fill Model
  migration_status: alias_supported
  primary: true
  aliases: [kt.replay_simulation.fill_model]
  split_targets:
    - kt.trading_engineering.backtest.fill_assumption
    - kt.trading_engineering.replay_simulation.fidelity_level

- v1_node_id: kt.live_execution
  canonical_node_id: kt.trading_engineering.live_execution
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering
  v1_path: CEK-TA / Trading Engineering / Live Execution
  canonical_path: CEK-TA / Trading Engineering / Live Execution
  title: Live Execution
  migration_status: alias_supported
  primary: true
  aliases: [kt.live_execution]
  split_targets: []

- v1_node_id: kt.live_execution.risk_control
  canonical_node_id: kt.trading_engineering.live_execution.risk_control
  v1_parent_id: kt.live_execution
  canonical_parent_id: kt.trading_engineering.live_execution
  v1_path: CEK-TA / Trading Engineering / Live Execution / Risk Control
  canonical_path: CEK-TA / Trading Engineering / Live Execution / Risk Control
  title: Live Risk Control
  migration_status: alias_supported
  primary: true
  aliases: [kt.live_execution.risk_control]
  split_targets:
    - kt.trading_engineering.risk_management.kill_switch
    - kt.trading_engineering.risk_management.risk_gate

- v1_node_id: kt.trade_analysis
  canonical_node_id: kt.trading_engineering.trade_analysis
  v1_parent_id: kt.trading_engineering
  canonical_parent_id: kt.trading_engineering
  v1_path: CEK-TA / Trading Engineering / Trade Analysis
  canonical_path: CEK-TA / Trading Engineering / Trade Analysis
  title: Trade Analysis
  migration_status: alias_supported
  primary: true
  aliases: [kt.trade_analysis]
  split_targets: []

- v1_node_id: kt.trade_analysis.bad_case_taxonomy
  canonical_node_id: kt.trading_engineering.trade_analysis.bad_case_taxonomy
  v1_parent_id: kt.trade_analysis
  canonical_parent_id: kt.trading_engineering.trade_analysis
  v1_path: CEK-TA / Trading Engineering / Trade Analysis / Bad Case Taxonomy
  canonical_path: CEK-TA / Trading Engineering / Trade Analysis / Bad Case Taxonomy
  title: Bad Case Taxonomy
  migration_status: alias_supported
  primary: true
  aliases: [kt.trade_analysis.bad_case_taxonomy]
  split_targets: []

- v1_node_id: kt.llm_training
  canonical_node_id: kt.ai_engineering.llm_training
  v1_parent_id: kt.ai_engineering
  canonical_parent_id: kt.ai_engineering
  v1_path: CEK-TA / AI Engineering / LLM Training
  canonical_path: CEK-TA / AI Engineering / LLM Training
  title: LLM Training
  migration_status: alias_supported
  primary: true
  aliases: [kt.llm_training]
  split_targets: []

- v1_node_id: kt.llm_training.dataset_design
  canonical_node_id: kt.ai_engineering.llm_training.dataset_design
  v1_parent_id: kt.llm_training
  canonical_parent_id: kt.ai_engineering.llm_training
  v1_path: CEK-TA / AI Engineering / LLM Training / Dataset Design
  canonical_path: CEK-TA / AI Engineering / LLM Training / Dataset Design
  title: Dataset Design
  migration_status: alias_supported
  primary: true
  aliases: [kt.llm_training.dataset_design]
  split_targets: []

- v1_node_id: kt.llm_training.eval_design
  canonical_node_id: kt.ai_engineering.llm_training.eval_design
  v1_parent_id: kt.llm_training
  canonical_parent_id: kt.ai_engineering.llm_training
  v1_path: CEK-TA / AI Engineering / LLM Training / Eval Design
  canonical_path: CEK-TA / AI Engineering / LLM Training / Eval Design
  title: Eval Design
  migration_status: alias_supported
  primary: true
  aliases: [kt.llm_training.eval_design]
  split_targets: []

- v1_node_id: kt.rag_engineering
  canonical_node_id: kt.ai_engineering.rag_engineering
  v1_parent_id: kt.ai_engineering
  canonical_parent_id: kt.ai_engineering
  v1_path: CEK-TA / AI Engineering / RAG Engineering
  canonical_path: CEK-TA / AI Engineering / RAG Engineering
  title: RAG Engineering
  migration_status: alias_supported
  primary: true
  aliases: [kt.rag_engineering]
  split_targets:
    - kt.ai_engineering.mcp_engineering

- v1_node_id: kt.rag_engineering.retrieval_policy
  canonical_node_id: kt.ai_engineering.rag_engineering.retrieval_policy
  v1_parent_id: kt.rag_engineering
  canonical_parent_id: kt.ai_engineering.rag_engineering
  v1_path: CEK-TA / AI Engineering / RAG Engineering / Retrieval Policy
  canonical_path: CEK-TA / AI Engineering / RAG Engineering / Retrieval Policy
  title: Retrieval Policy
  migration_status: alias_supported
  primary: true
  aliases: [kt.rag_engineering.retrieval_policy]
  split_targets: []

- v1_node_id: kt.rag_engineering.source_quality
  canonical_node_id: kt.ai_engineering.rag_engineering.source_quality
  v1_parent_id: kt.rag_engineering
  canonical_parent_id: kt.ai_engineering.rag_engineering
  v1_path: CEK-TA / AI Engineering / RAG Engineering / Source Quality
  canonical_path: CEK-TA / AI Engineering / RAG Engineering / Source Quality
  title: Source Quality
  migration_status: alias_supported
  primary: true
  aliases: [kt.rag_engineering.source_quality]
  split_targets:
    - kt.knowledge_governance.source_quality

- v1_node_id: kt.mcp
  canonical_node_id: kt.ai_engineering.mcp_engineering
  v1_parent_id: kt.ai_engineering
  canonical_parent_id: kt.ai_engineering
  v1_path: CEK-TA / AI Engineering / MCP
  canonical_path: CEK-TA / AI Engineering / MCP Engineering
  title: MCP
  migration_status: alias_supported
  primary: true
  aliases: [kt.mcp]
  split_targets: []

- v1_node_id: kt.mcp.knowledge_tools
  canonical_node_id: kt.ai_engineering.mcp_engineering.knowledge_tools
  v1_parent_id: kt.mcp
  canonical_parent_id: kt.ai_engineering.mcp_engineering
  v1_path: CEK-TA / AI Engineering / MCP / Knowledge Tools
  canonical_path: CEK-TA / AI Engineering / MCP Engineering / Knowledge Tools
  title: Knowledge Tools
  migration_status: alias_supported
  primary: true
  aliases: [kt.mcp.knowledge_tools]
  split_targets: []

- v1_node_id: kt.project_integration.adapter
  canonical_node_id: kt.project_integration.adapter
  v1_parent_id: kt.project_integration
  canonical_parent_id: kt.project_integration
  v1_path: CEK-TA / Project Integration / Project Adapter
  canonical_path: CEK-TA / Project Integration / Project Adapter
  title: Project Adapter
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets:
    - kt.project_integration.truth_boundary
    - kt.project_integration.field_mapping

- v1_node_id: kt.project_integration.healthcheck
  canonical_node_id: kt.project_integration.healthcheck
  v1_parent_id: kt.project_integration
  canonical_parent_id: kt.project_integration
  v1_path: CEK-TA / Project Integration / Healthcheck
  canonical_path: CEK-TA / Project Integration / Healthcheck
  title: External Project Healthcheck
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets: []

- v1_node_id: kt.project_integration.contribution
  canonical_node_id: kt.project_integration.contribution
  v1_parent_id: kt.project_integration
  canonical_parent_id: kt.project_integration
  v1_path: CEK-TA / Project Integration / Knowledge Contribution
  canonical_path: CEK-TA / Project Integration / Knowledge Contribution
  title: Knowledge Contribution
  migration_status: canonical_ready
  primary: true
  aliases: []
  split_targets:
    - kt.knowledge_governance.contribution_review
```

## Planned New v2 Nodes

这些节点没有 v1 对应节点，后续在 `knowledge_tree_v2.md` 中创建：

```text
kt.knowledge_governance
kt.knowledge_governance.status_lifecycle
kt.knowledge_governance.evidence_policy
kt.knowledge_governance.conflict_resolution
kt.knowledge_governance.source_quality
kt.knowledge_governance.versioning
kt.knowledge_governance.deprecation
kt.knowledge_governance.contribution_review
kt.trading_engineering.data_engineering
kt.trading_engineering.data_engineering.market_data_schema
kt.trading_engineering.data_engineering.time_alignment
kt.trading_engineering.data_engineering.data_quality
kt.trading_engineering.data_engineering.feature_pipeline
kt.trading_engineering.data_engineering.versioning
kt.trading_engineering.data_engineering.observability
kt.trading_engineering.strategy_engineering
kt.trading_engineering.strategy_engineering.signal_design
kt.trading_engineering.strategy_engineering.direction_model
kt.trading_engineering.strategy_engineering.entry_model
kt.trading_engineering.strategy_engineering.exit_model
kt.trading_engineering.strategy_engineering.scoring_gate_guard
kt.trading_engineering.strategy_engineering.regime_detection
kt.trading_engineering.strategy_engineering.multi_strategy_fusion
kt.trading_engineering.strategy_engineering.derivatives_flow
kt.trading_engineering.strategy_engineering.derivatives_flow.open_interest
kt.trading_engineering.strategy_engineering.derivatives_flow.funding
kt.trading_engineering.strategy_engineering.derivatives_flow.basis
kt.trading_engineering.strategy_engineering.derivatives_flow.liquidation
kt.trading_engineering.strategy_engineering.derivatives_flow.crowding
kt.trading_engineering.risk_management
kt.trading_engineering.risk_management.risk_gate
kt.trading_engineering.risk_management.position_sizing
kt.trading_engineering.risk_management.drawdown_control
kt.trading_engineering.risk_management.leverage_policy
kt.trading_engineering.risk_management.exposure_control
kt.trading_engineering.risk_management.daily_loss_limit
kt.trading_engineering.risk_management.ruin_risk
kt.ai_engineering.agent_engineering
```

## Test Checklist

```text
1. 每个 v1_node_id 唯一。
2. 每个 v1_node_id 有 canonical_node_id。
3. 每个非 root canonical_node_id 继承一级主枝。
4. split_targets 只作为审计提示，不作为默认检索。
5. 不删除 v1 node_id。
6. UTF-8 中文可读。
```

