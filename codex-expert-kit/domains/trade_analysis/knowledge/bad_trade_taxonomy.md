# CEK-TA Bad Trade Taxonomy

This taxonomy classifies trade-quality failures for post-trade analysis, replay, strategy iteration, and LLM training.

It labels process quality, not only PnL. A profitable trade can still be bad quality, and a losing trade can be acceptable if it followed the plan and risk contract.

## Taxonomy Version

```yaml
taxonomy_name: cek_ta_bad_trade_taxonomy
taxonomy_version: 1.0.0
encoding: UTF-8
domain: trade_analysis
```

## Label Object

```json
{
  "label_code": "string",
  "category": "data | signal | entry | risk | execution | fill_model | exit | review | psychology | unknown",
  "severity": "info | warning | error | critical",
  "definition": "string",
  "evidence_required": [],
  "not_this_when": [],
  "repair_action": []
}
```

## Top-Level Categories

| Category | Meaning |
| --- | --- |
| `data` | Market data, feature data, gaps, ordering, or quality caused unreliable decision/fill. |
| `signal` | Direction or setup logic was wrong, stale, overfit, or unsupported. |
| `entry` | Direction may be reasonable, but entry trigger, timing, or price was poor. |
| `risk` | SL, TP, sizing, exposure, cooldown, or risk gate failed. |
| `execution` | Adapter, order type, rejection, latency, partial fill, or reconciliation issue. |
| `fill_model` | Simulated fill assumption made result misleading. |
| `exit` | Exit was inconsistent with plan, invalidation, or risk state. |
| `review` | Missing audit trail, missing metrics, or insufficient evidence. |
| `psychology` | Manual or discretionary action violated plan. |
| `unknown` | Evidence is insufficient. |

## Labels

### DATA_GAP

```yaml
label_code: DATA_GAP
category: data
severity: error
definition: Required market data was missing, duplicated, delayed, or out of order.
evidence_required:
  - data_quality_flags
  - source_event_ids
  - affected time window
not_this_when:
  - strategy failed despite complete and ordered data
repair_action:
  - improve_data
  - rerun_backtest
```

### LOOKAHEAD_OR_LEAKAGE

```yaml
label_code: LOOKAHEAD_OR_LEAKAGE
category: data
severity: critical
definition: Decision or feature used future-derived information.
evidence_required:
  - feature timestamp
  - event_time vs processing_time
  - source feature lineage
not_this_when:
  - only a reporting timestamp is late but features were valid
repair_action:
  - improve_data
  - rerun_backtest
  - human_review
```

### WRONG_DIRECTION

```yaml
label_code: WRONG_DIRECTION
category: signal
severity: error
definition: Strategy direction contradicted market structure or its own signal rules.
evidence_required:
  - signal_frame
  - trend_state
  - reason_codes
not_this_when:
  - direction was valid but entry timing was poor
repair_action:
  - adjust_signal
  - replay_trade
```

### NO_CLEAR_SETUP

```yaml
label_code: NO_CLEAR_SETUP
category: signal
severity: warning
definition: Trade was opened without a valid setup type or reason code.
evidence_required:
  - entry_setup
  - decision reason_codes
not_this_when:
  - setup exists but trigger is too early or late
repair_action:
  - adjust_signal
  - human_review
```

### EARLY_ENTRY

```yaml
label_code: EARLY_ENTRY
category: entry
severity: warning
definition: Direction or setup may be valid, but entry occurred before trigger confirmation.
evidence_required:
  - planned trigger
  - actual entry time
  - market context after entry
not_this_when:
  - trigger was confirmed but fill slipped badly
repair_action:
  - adjust_entry
  - replay_trade
```

### LATE_ENTRY

```yaml
label_code: LATE_ENTRY
category: entry
severity: warning
definition: Entry occurred after the favorable movement, reducing RR or increasing stop risk.
evidence_required:
  - planned entry
  - executed entry
  - planned_rr vs realized setup RR
not_this_when:
  - strategy intentionally enters continuation after confirmation
repair_action:
  - adjust_entry
  - validation_metric: entry_slippage_to_plan
```

### INVALID_SL

```yaml
label_code: INVALID_SL
category: risk
severity: error
definition: Stop loss did not map to a valid structure invalidation or max-loss rule.
evidence_required:
  - invalidation_level
  - planned_stop_loss
  - max_loss
not_this_when:
  - SL was valid but normal market noise hit it
repair_action:
  - adjust_risk
```

### UNREACHABLE_TP

```yaml
label_code: UNREACHABLE_TP
category: risk
severity: warning
definition: Take profit target was not realistically reachable under market context, costs, or liquidity.
evidence_required:
  - planned_take_profit
  - mfe
  - tp_reach_rate
  - cost_impact
not_this_when:
  - TP was reachable but exit logic closed early
repair_action:
  - adjust_risk
  - replay_trade
```

### OVERSIZED_RISK

```yaml
label_code: OVERSIZED_RISK
category: risk
severity: critical
definition: Position size or exposure exceeded declared risk limits.
evidence_required:
  - RiskState
  - planned_risk
  - actual notional
not_this_when:
  - loss exceeded expectation because of gap or slippage despite valid sizing
repair_action:
  - adjust_risk
  - human_review
```

### ADAPTER_REJECTED

```yaml
label_code: ADAPTER_REJECTED
category: execution
severity: error
definition: OrderIntent was rejected by adapter or exchange constraints.
evidence_required:
  - OrderAck
  - ErrorEvent
  - reject_reason
not_this_when:
  - order was accepted but filled poorly
repair_action:
  - adjust_execution
```

### POOR_FILL

```yaml
label_code: POOR_FILL
category: execution
severity: warning
definition: Execution price or partial fill materially worsened planned RR or outcome.
evidence_required:
  - FillEvent
  - planned_entry_price
  - slippage
  - partial_fill_model
not_this_when:
  - fill matched model and loss came from strategy logic
repair_action:
  - adjust_execution
  - improve_data
```

### AMBIGUOUS_SIM_FILL

```yaml
label_code: AMBIGUOUS_SIM_FILL
category: fill_model
severity: error
definition: Simulated result depends on an unresolved fill ordering or missing path assumption.
evidence_required:
  - assumption_id
  - same_candle_ordering
  - ambiguous_fill_count
not_this_when:
  - tick path or exchange fills prove order sequence
repair_action:
  - rerun_backtest
  - replay_trade
```

### BAD_EXIT_DISCIPLINE

```yaml
label_code: BAD_EXIT_DISCIPLINE
category: exit
severity: warning
definition: Exit violated the planned invalidation, TP, risk, or signal exit rules.
evidence_required:
  - exit_reason
  - planned_stop_loss
  - planned_take_profit
  - signal exit rule
not_this_when:
  - risk gate correctly forced exit
repair_action:
  - adjust_exit
  - human_review
```

### MISSING_AUDIT_TRACE

```yaml
label_code: MISSING_AUDIT_TRACE
category: review
severity: error
definition: Trade cannot be reliably analyzed because decision, intent, fills, or source events are missing.
evidence_required:
  - missing field list
not_this_when:
  - all required IDs exist but label is uncertain
repair_action:
  - improve_data
  - human_review
```

### MANUAL_RULE_VIOLATION

```yaml
label_code: MANUAL_RULE_VIOLATION
category: psychology
severity: error
definition: Manual intervention violated the declared strategy or risk plan.
evidence_required:
  - manual action log
  - rule violated
not_this_when:
  - manual action followed incident recovery or kill switch protocol
repair_action:
  - human_review
```

### UNKNOWN_INSUFFICIENT_EVIDENCE

```yaml
label_code: UNKNOWN_INSUFFICIENT_EVIDENCE
category: unknown
severity: info
definition: Evidence is insufficient for a confident label.
evidence_required:
  - missing evidence list
not_this_when:
  - enough evidence exists for a specific label
repair_action:
  - human_review
  - improve_data
```

## Root Cause Chain Rules

```text
1. Prefer the earliest causal stage that explains the failure.
2. Do not assign signal failure when data leakage or data gaps caused the signal.
3. Do not assign entry failure when adapter rejection prevented execution.
4. Do not assign risk failure when the trade followed a valid planned loss.
5. Multiple labels are allowed, but one primary_label must be selected.
```

## Quality vs Outcome

```text
good:
  followed plan, risk, execution assumptions, and audit trace; outcome may be win or loss

acceptable:
  minor issue, still useful as normal strategy sample

bad:
  process failure or invalid assumption materially affected trade quality

ambiguous:
  insufficient path, fill, or evidence to judge normally

unreviewed:
  not labeled yet
```

## Repair Action Mapping

| Label Family | Common Repair |
| --- | --- |
| data | improve_data, rerun_backtest |
| signal | adjust_signal, replay_trade |
| entry | adjust_entry, replay_trade |
| risk | adjust_risk, rerun_backtest |
| execution | adjust_execution, reconciliation review |
| fill_model | rerun_backtest with alternative assumptions |
| exit | adjust_exit, replay_trade |
| review | improve_data, human_review |

## Forbidden Mislabels

```text
1. Do not label every losing trade as bad.
2. Do not label every winning trade as good.
3. Do not blame direction when entry or execution caused the loss.
4. Do not use raw PnL without planned R and cost impact.
5. Do not approve training labels without review.
```
