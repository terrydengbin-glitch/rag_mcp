---
name: backtest-reviewer
description: Review trading backtests for credibility, lookahead bias, data gaps, fill assumptions, fees, slippage, same-candle TP/SL handling, metrics, train/test split, version reproducibility, and live-trading reliability. Use when auditing backtest reports, engines, result tables, or live-vs-backtest gaps.
---

# Backtest Reviewer

## Workflow

1. Check data scope, gaps, time alignment, and symbol universe.
2. Check for lookahead bias and future-derived features.
3. Inspect order and fill semantics.
4. Inspect fees, slippage, minimum notional, and partial fills.
5. Inspect same-candle TP/SL ordering.
6. Review train/test split and strategy version reproducibility.
7. Review metrics beyond total return.
8. Produce a minimum fix and rerun plan.

## Required Metrics

```text
win rate
average R
profit factor
max drawdown
consecutive losses
holding time
time bucket performance
cost impact
TP reach rate
noise stop rate
```

## Output

```text
credibility rating
main biases
high-risk assumptions
fill/cost issues
metric gaps
minimum fix path
rerun requirements
live reliability notes
```
