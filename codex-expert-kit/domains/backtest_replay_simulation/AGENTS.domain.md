# Backtest / Replay / Simulation Domain

Use this domain for backtest credibility, market replay, simulation, fill models, fees, slippage, same-candle TP/SL handling, and live-vs-backtest gaps.

## Scope

```text
historical data quality
event-driven backtest semantics
replay clock and event bus
fill model
fee model
slippage model
same-candle TP/SL ordering
simulation/live gap
metrics and bad buckets
```

## Required Checks

```text
1. Is there lookahead bias?
2. Are data gaps and time alignment handled?
3. Are costs, slippage, and fills explicit?
4. Is same-candle TP/SL ordering deterministic?
5. Is the train/test split clear?
6. Is strategy version reproducible?
7. Are metrics beyond total return reviewed?
```

## Output Contract

```text
credibility rating
main biases
high-risk assumptions
minimum fix path
required rerun metrics
live reliability notes
```
