---
name: strategy-auditor
description: Audit trading strategies for architecture, edge, signal/entry/SL/TP separation, risk gates, RR/EV/cost impact, data quality, validation, and rollback. Use when reviewing strategy code, strategy specs, signal rules, risk filters, or proposed trading-system changes.
---

# Strategy Auditor

## Workflow

1. Identify the strategy's intended edge.
2. Separate direction, entry, SL, TP, sizing, risk, execution, and data quality.
3. Map inputs and outputs.
4. Check whether gates improve EV or only reduce frequency.
5. Check SL invalidation and TP reachability.
6. Check cost, slippage, and liquidity assumptions.
7. Define validation metrics and rollback.

## Mandatory Questions

```text
What edge is being captured?
Which inputs produce the signal?
Which module owns direction?
Which module owns entry?
Where is invalidation?
What makes TP reachable?
How does this affect win rate, RR, EV, drawdown, cost, and holding time?
How will the change be verified?
```

## Output

```text
findings
main risks
affected modules
contract gaps
minimum fix path
validation plan
rollback plan
open questions
```
