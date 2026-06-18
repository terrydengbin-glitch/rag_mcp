# CEK-TA Trade Result Schema

This template defines a structured trade result object for post-trade analysis, strategy iteration, RAG retrieval, knowledge contribution, and LLM training.

It must not contain raw private account data, secrets, or unsanitized project-private fields.

## Schema Version

```yaml
schema_name: cek_ta_trade_result
schema_version: 1.0.0
encoding: UTF-8
scope: post_trade_analysis
```

## Required Object

```json
{
  "schema_version": "1.0.0",
  "trade_result_id": "string",
  "project_binding": {
    "project_name": "string | null",
    "project_type": "kline_trend_strategy | abnormal_move_strategy | high_fidelity_simulator | live_binance_futures | trading_llm_assistant | general",
    "sanitization_status": "raw_project_only | sanitized | not_applicable"
  },
  "identity": {
    "symbol": "string",
    "market": "crypto | futures | spot | stock | general",
    "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
    "strategy_version": "string",
    "mode": "backtest | replay | simulation | live",
    "opened_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
    "closed_at": "YYYY-MM-DDTHH:mm:ss.sssZ | null"
  },
  "links": {
    "decision_id": "string",
    "intent_id": "string",
    "execution_report_id": "string",
    "audit_trace_id": "string",
    "source_event_ids": [],
    "knowledge_ids": []
  },
  "planned_trade": {
    "direction": "long | short",
    "entry_plan": "string",
    "planned_entry_price": "decimal string | null",
    "planned_stop_loss": "decimal string | null",
    "planned_take_profit": "decimal string | null",
    "planned_rr": "decimal string | null",
    "planned_risk": "decimal string | null",
    "reason_codes": [],
    "invalidation_level": "decimal string | null"
  },
  "executed_trade": {
    "entry_price": "decimal string | null",
    "exit_price": "decimal string | null",
    "qty": "decimal string",
    "notional": "decimal string | null",
    "fees": "decimal string | null",
    "slippage": "decimal string | null",
    "fills": [],
    "position_snapshot_before": "PositionSnapshot | null",
    "position_snapshot_after": "PositionSnapshot | null"
  },
  "outcome_metrics": {
    "gross_pnl": "decimal string | null",
    "net_pnl": "decimal string | null",
    "realized_r": "decimal string | null",
    "mae": "decimal string | null",
    "mfe": "decimal string | null",
    "holding_seconds": 0,
    "tp_reached": false,
    "sl_reached": false,
    "exit_reason": "take_profit | stop_loss | signal_exit | risk_exit | manual_exit | timeout | liquidation | adapter_reject | ambiguous | unknown",
    "cost_impact": "decimal string | null"
  },
  "context": {
    "market_regime": "trend_up | trend_down | range | transition | high_volatility | low_liquidity | unknown",
    "trend_state": "uptrend | downtrend | range | transition | unknown",
    "entry_setup": "breakout | pullback | continuation | reversal | mean_reversion | no_setup | unknown",
    "data_quality_flags": [],
    "fill_assumption": {
      "assumption_id": "string | null",
      "same_candle_ordering": "string | null",
      "slippage_model": "string | null",
      "fee_model": "string | null",
      "latency_model": "string | null",
      "partial_fill_model": "string | null"
    }
  },
  "quality_labels": {
    "trade_quality": "good | acceptable | bad | ambiguous | unreviewed",
    "primary_label": "string",
    "secondary_labels": [],
    "severity": "info | warning | error | critical",
    "confidence": "high | medium | low",
    "review_status": "draft | reviewed | approved | rejected | deprecated"
  },
  "root_cause_chain": [
    {
      "stage": "data | signal | entry | risk | execution | fill_model | exit | review",
      "cause_code": "string",
      "evidence": "string",
      "fix_hint": "string"
    }
  ],
  "repair_action": {
    "action_type": "no_change | rerun_backtest | replay_trade | adjust_signal | adjust_entry | adjust_risk | adjust_execution | improve_data | human_review",
    "description": "string",
    "validation_metric": [],
    "rollback_path": "string"
  },
  "training_use": {
    "allowed_for_llm_training": false,
    "allowed_for_rag": false,
    "allowed_for_skill_update": false,
    "requires_sanitization": true,
    "dataset_split": "train | eval | holdout | not_applicable",
    "label_quality": "gold | silver | bronze | unverified"
  },
  "review": {
    "reviewer": "codex | human | mixed | null",
    "reviewed_at": "YYYY-MM-DD | null",
    "open_questions": [],
    "decision_log": []
  },
  "created_at": "YYYY-MM-DD",
  "updated_at": "YYYY-MM-DD"
}
```

## Required Fields

```text
schema_version
trade_result_id
project_binding
identity
links
planned_trade
executed_trade
outcome_metrics
context
quality_labels
root_cause_chain
repair_action
training_use
review
created_at
updated_at
```

## Field Rules

```text
1. trade_result_id must be unique inside the business project.
2. Project-private raw trades must use sanitization_status = raw_project_only and cannot enter CEK-TA as reusable knowledge.
3. Decimal values should be strings at boundaries.
4. Missing values must be null or explicit unknown, not silently filled.
5. root_cause_chain can be empty only when trade_quality = unreviewed.
6. allowed_for_llm_training requires sanitization and reviewed or approved labels.
7. allowed_for_rag requires source traceability and no private account data.
```

## Outcome Metrics

Minimum metrics for review:

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

Batch analysis should also compute:

```text
win_rate
average_r
profit_factor
max_drawdown
consecutive_losses
tp_reach_rate
noise_stop_rate
time_bucket_performance
cost_per_trade
bad_case_rate_by_label
```

## Review Status Rules

```text
draft:
  created but not reviewed

reviewed:
  checked by Codex or human, not approved for training

approved:
  approved as a reliable labeled sample

rejected:
  not valid as sample

deprecated:
  retained for history, not recommended for training
```

## Training Use Rules

```text
1. Raw live trades are never training-ready by default.
2. Training samples must be sanitized.
3. Labels must be reviewed or approved.
4. The sample must preserve enough context to avoid teaching false causality.
5. Ambiguous trades can be useful eval cases but must be labeled ambiguous.
6. Single-trade outcomes cannot be promoted to general strategy rules without aggregation and source review.
```

## Validation Checklist

```text
1. Does the result link back to Decision, OrderIntent, ExecutionReport, and AuditTrace?
2. Are planned and executed prices separated?
3. Are fees, slippage, and fill assumptions recorded?
4. Is bad-case labeling separated from net PnL?
5. Is the root cause supported by evidence?
6. Is the repair action testable?
7. Is training/RAG use blocked until sanitization and review?
```
