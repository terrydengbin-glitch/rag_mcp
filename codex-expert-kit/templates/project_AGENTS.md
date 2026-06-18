# Project AGENTS.md Template

Use this file in a business project that calls CEK-TA.

````md
# AGENTS.md

This project uses CEK-TA as its reusable Trading + AI expert support layer.

## CEK-TA Reference

Set one of these:

```text
local_path: <path-to-cek-ta>
submodule_path: .codex-expert-kit
plugin: <plugin-name-if-installed>
```

## Project Type

```text
adapter: <kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | custom>
```

## Enabled Domains

```text
- quant_trading
- kline_strategy
- backtest_replay_simulation
- trade_analysis
```

## Project Facts

Project facts must stay in this repository.

```text
market:
symbols:
timeframe_trend:
timeframe_entry:
data_sources:
strategy_version:
current_pipeline:
current_config:
run_commands:
known_risks:
```

## Local Fact Documents

```text
docs/project_overview.md
docs/current_pipeline.md
docs/current_config.md
docs/reason_codes.md
docs/data_schema.md
docs/recent_audit.md
```

## Hard Rules

```text
1. Project facts override CEK-TA general knowledge.
2. Do not copy general CEK-TA knowledge into this project.
3. Do not write project-private fields into CEK-TA reusable knowledge.
4. Trading changes must state input, output, affected modules, validation metrics, and rollback path.
5. Professional claims must use CEK-TA knowledge, source-backed evidence, or explicit assumptions.
6. Conflicting knowledge must be labeled with applicability boundaries before use.
7. Knowledge contributed back to CEK-TA must go through a contribution task and sanitization.
```

## Validation

Before marking work done:

```text
1. Confirm the task's CEK-TA domain/Skill.
2. Confirm project facts used.
3. Confirm source-backed knowledge used.
4. Confirm tests or validation metrics.
5. Confirm rollback path.
```
````
