---
name: trade-quality-analyst
description: Analyze executed trades, backtest trades, replay cases, simulation fills, paper trades, and live-vs-sim gaps for trade quality, realized-vs-planned R, bad-case labels, root cause, repair actions, and LLM/RAG training suitability.
---

# Trade Quality Analyst

## Use When

Use this skill when reviewing:

```text
single trade result
batch trade samples
bad trade cases
live-vs-backtest gaps
paper trading fills
replay cases
trade labels for LLM training
strategy iteration evidence
```

## Workflow

1. Load the trade context: market, symbol, timeframe, strategy version, mode.
2. Link Decision, OrderIntent, ExecutionReport, FillEvent, PositionSnapshot, RiskState, and AuditTrace.
3. Separate planned trade from executed trade.
4. Compute or inspect outcome metrics: net PnL, realized R, MAE, MFE, holding time, TP reach, SL reach, cost impact.
5. Check fill assumptions: same-candle ordering, slippage, fees, latency, partial fill, ambiguous fills.
6. Label trade quality using `bad_trade_taxonomy.md`.
7. Build root cause chain from earliest causal stage to final outcome.
8. Propose repair action with validation metric and rollback path.
9. Decide whether the case is allowed for RAG, Skill update, LLM train/eval, or requires sanitization.

## Required Inputs

```text
trade_result or equivalent fields
Decision
OrderIntent
ExecutionReport
FillEvent
PositionSnapshot
RiskState
AuditTrace
FillAssumption
market context
strategy version
```

If required inputs are missing, label the gap explicitly instead of inventing evidence.

## Hard Rules

```text
Bad PnL does not automatically mean bad trade quality.
Good PnL does not automatically mean good trade quality.
Direction, entry, risk, execution, fill model, and exit must be separated.
Do not use raw private trades as reusable CEK-TA knowledge.
Do not approve a sample for LLM training unless it is sanitized and reviewed.
Ambiguous fills must not be treated as normal wins or losses.
Single-trade conclusions must not be promoted to general strategy rules.
```

## Output

```json
{
  "trade_result_id": "",
  "trade_quality": "good | acceptable | bad | ambiguous | unreviewed",
  "primary_label": "",
  "secondary_labels": [],
  "severity": "info | warning | error | critical",
  "confidence": "high | medium | low",
  "evidence": [],
  "root_cause_chain": [
    {
      "stage": "data | signal | entry | risk | execution | fill_model | exit | review",
      "cause_code": "",
      "evidence": "",
      "fix_hint": ""
    }
  ],
  "repair_action": {
    "action_type": "no_change | rerun_backtest | replay_trade | adjust_signal | adjust_entry | adjust_risk | adjust_execution | improve_data | human_review",
    "description": "",
    "validation_metric": [],
    "rollback_path": ""
  },
  "training_use": {
    "allowed_for_llm_training": false,
    "allowed_for_rag": false,
    "allowed_for_skill_update": false,
    "requires_sanitization": true,
    "label_quality": "gold | silver | bronze | unverified"
  },
  "open_questions": []
}
```

## Minimum Metrics

```text
net_pnl
realized_r
mae
mfe
holding_seconds
tp_reached
sl_reached
exit_reason
cost_impact
```

## Review Checklist

```text
1. Does the trade link back to strategy decision and execution report?
2. Was the plan valid before the trade?
3. Did execution preserve the plan?
4. Did fill assumptions distort the result?
5. Was risk respected?
6. Is the bad-case label supported by evidence?
7. Is the proposed repair testable?
8. Is the case safe for RAG or LLM training?
```
