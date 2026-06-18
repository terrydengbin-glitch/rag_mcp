# External Project AGENTS.md Template

Copy this template into a business project as `AGENTS.md` when the project uses CEK-TA as its support layer.

Business projects provide project facts. CEK-TA provides reusable trading and AI expertise.

## CEK-TA Location

Set one:

```text
local_path: E:\collector\rag
submodule_path: .codex-expert-kit
plugin: <plugin-name-if-installed>
```

## Required First Reads

Before trading, backtest, replay, simulation, live risk, RAG, LLM, or Codex Skill work, read:

```text
<cek_ta_path>/AGENTS.md
<cek_ta_path>/docs/index_tasks.md
<cek_ta_path>/codex-expert-kit/core/AGENTS.md
```

Read project facts from this repository before using CEK-TA general knowledge.

## Project Identity

```yaml
project_name: ""
project_type: "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | custom"
market: "crypto | futures | spot | stock | general"
symbols: []
primary_timeframes: []
strategy_version: ""
environment: "research | backtest | replay | simulation | paper | live"
```

## Enabled CEK-TA Domains

```text
quant_trading
kline_strategy
backtest_replay_simulation
trade_analysis
llm_training
rag_engineering
```

Only enable domains that match the project.

## Project Fact Documents

Project facts must stay in this repository:

```text
docs/project_overview.md
docs/current_pipeline.md
docs/current_config.md
docs/data_schema.md
docs/reason_codes.md
docs/runbook.md
docs/recent_audit.md
docs/risk_limits.md
```

If a file is missing, Codex must ask or state the assumption before changing behavior.

## Project Adapter

Maintain a project adapter file:

```text
docs/project_adapter.md
```

It maps project-specific names to CEK-TA contracts:

```text
MarketEvent
FeatureFrame
SignalFrame
Decision
OrderIntent
ExecutionReport
TradeResult
ReasonCode
```

## Hard Rules

```text
1. Project facts override CEK-TA general knowledge.
2. Do not copy CEK-TA knowledge into this project as local truth.
3. Do not write project-private fields into CEK-TA reusable knowledge.
4. Professional claims must use CEK-TA knowledge, project facts, or source-backed evidence.
5. Conflicting knowledge must be labeled with applicability boundaries before use.
6. Trading changes must state inputs, outputs, affected modules, metrics, risk impact, and rollback.
7. Live trading changes require explicit project approval and live readiness checks.
8. Knowledge contributions back to CEK-TA must use a contribution task and sanitization.
```

## Task Routing

```text
strategy design/review:
  use CEK-TA strategy-auditor and quant_trading

K-line entries:
  use kline-strategy-engineer and kline_strategy

backtest/replay/simulation:
  use backtest-reviewer and backtest_replay_simulation

trade diagnosis:
  use trade-quality-analyst and trade_analysis

dataset/eval/training:
  use llm-data-curator, sft-engineer, eval-engineer

knowledge lookup:
  use Knowledge MCP or CEK-TA RAG docs
```

## MCP / RAG

If configured, CEK-TA Knowledge MCP is read-only:

```text
search_expert_knowledge
get_knowledge_item
get_conflict_audit
get_source_profile
list_kb_partitions
```

MCP must not place trades, read secrets, read account data, approve knowledge, or write knowledge.

## Active Retrieval Protocol

When the project task involves trading, backtest, replay, simulation, live execution, risk, trade analysis, RAG, MCP, LLM training, knowledge governance, or contribution/backflow, the AI must actively call CEK-TA `search_expert_knowledge` before giving professional guidance or changing code.

Copy the detailed rules from:

```text
<cek_ta_path>/codex-expert-kit/templates/external_project_active_retrieval_AGENTS.md
```

Minimum rules:

```text
1. Do not answer professional CEK-TA topics from model memory only.
2. Use scoped search with task_type, domain/tree_node_id filters, top_k=5.
3. Use only machine_gate.default_guidance=allow as default guidance.
4. Cite knowledge_id, machine_gate, review_status, conflict_status, source_count, and applicability boundary.
5. If no allow result exists, report caveat/blocked/no-hit and create a gap or research task instead of inventing a rule.
```

## Validation Before Done

Before marking any task done:

```text
1. List project facts used.
2. List CEK-TA domains or Skills used.
3. State source-backed knowledge or assumptions.
4. State changed inputs and outputs.
5. State validation metrics.
6. State tests run.
7. State rollback path.
8. State whether knowledge contribution is needed.
```

## Knowledge Contribution Boundary

If this project discovers reusable knowledge:

```text
1. Create a knowledge contribution task in this project.
2. Sanitize private fields, orders, account data, logs, and config.
3. Add sources and evidence.
4. Map project fields to generic CEK-TA concepts.
5. Check conflicts against CEK-TA.
6. Submit to CEK-TA contribution queue.
```

Never write directly into CEK-TA approved knowledge.
