# Trade Analysis Domain Rules

Use this domain when reviewing executed trades, backtest trades, replay cases, simulation fills, paper-trading cases, or live-vs-sim gaps.

## Required Separation

Always separate:

```text
planned trade
executed trade
market context
fill assumptions
outcome metrics
quality labels
root cause
repair action
training use
```

## Hard Rules

```text
1. Bad PnL does not automatically mean bad trade quality.
2. Good PnL does not automatically mean good trade quality.
3. Do not blame signal when the failure is entry timing, fill, cost, or data quality.
4. Do not use raw private trades as reusable CEK-TA knowledge.
5. Any trade case used for LLM training must be sanitized and reviewed.
```

## Output Requirements

```text
trade_quality
primary_label
secondary_labels
evidence
root_cause_chain
repair_action
validation_metric
training_use
open_questions
```
