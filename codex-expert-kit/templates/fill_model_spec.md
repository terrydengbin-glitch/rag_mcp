# CEK-TA FillModel Spec

This template defines fill assumptions for backtest, replay, and simulation. It also defines what must be disclosed when comparing simulated results with live trading.

FillModel is not strategy logic. It belongs to execution modeling.

## Spec Version

```yaml
spec_name: cek_ta_fill_model
spec_version: 1.0.0
encoding: UTF-8
scope: execution_assumptions
```

## Purpose

A FillModel answers:

```text
Would an OrderIntent become filled?
At what price?
At what quantity?
With what fee and slippage?
At what time?
Under which assumptions?
```

## FillAssumption

```json
{
  "assumption_id": "string",
  "name": "string",
  "mode": "backtest | replay | simulation",
  "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
  "market": "crypto | futures | spot | stock | general",
  "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
  "same_candle_ordering": "stop_first | target_first | entry_first | open_high_low_close | open_low_high_close | pessimistic | optimistic | no_intrabar_inference | tick_path",
  "slippage_model": "none | fixed_bps | fixed_ticks | spread_based | volatility_based | order_book_based | custom",
  "fee_model": "none | fixed_bps | maker_taker | exchange_schedule | custom",
  "latency_model": "none | fixed_ms | sampled_distribution | event_delay | custom",
  "partial_fill_model": "none | proportional_volume | order_book_depth | custom",
  "limitations": [],
  "not_applicable_when": []
}
```

Rules:

```text
1. Every backtest, replay, or simulation result must reference assumption_id.
2. OHLC K-line data cannot prove intrabar order path.
3. If same-candle TP and SL are both touched, ordering must be explicit.
4. Live comparison must disclose any fill model that is not exchange-event based.
```

## Same-Candle TP/SL Policy

When an entry, stop loss, and take profit can interact inside the same candle:

```text
tick_path:
  Use actual tick/trade path when available and trusted.

no_intrabar_inference:
  Do not decide ordering from OHLC alone; mark outcome ambiguous or skip fill.

pessimistic:
  Choose the less favorable valid outcome for the strategy.

optimistic:
  Choose the more favorable valid outcome; allowed only for sensitivity analysis, not default performance claims.

stop_first:
  Stop loss is assumed to trigger before take profit when both are touched.

target_first:
  Take profit is assumed to trigger before stop loss when both are touched.

open_high_low_close / open_low_high_close:
  Synthetic intrabar path assumption. Must be disclosed.
```

Default recommendation:

```text
For OHLC-only backtests, use pessimistic or no_intrabar_inference for default credibility, and run sensitivity analysis against alternative assumptions.
```

## FillModel Input

```json
{
  "order_intent": "OrderIntent",
  "market_event_window": [],
  "position_snapshot_before": "PositionSnapshot | null",
  "assumption": "FillAssumption",
  "clock": "ClockState"
}
```

## FillModel Output

```json
{
  "fill_model_id": "string",
  "assumption_id": "string",
  "intent_id": "string",
  "status": "not_filled | partially_filled | filled | ambiguous | rejected",
  "fills": [
    {
      "fill_id": "string",
      "qty": "decimal string",
      "price": "decimal string",
      "fee": "decimal string | null",
      "fee_asset": "string | null",
      "slippage": "decimal string | null",
      "liquidity": "maker | taker | unknown",
      "filled_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
    }
  ],
  "warnings": [],
  "calculation_trace": {}
}
```

## Price Rules

Market order:

```text
1. tick/trade/order_book data: use executable path according to data and latency.
2. OHLC K-line: use open, next open, close, or assumption-specific price; disclose.
3. Slippage must be applied after base executable price is chosen.
```

Limit order:

```text
1. Buy limit can fill when market trades at or below limit under the model.
2. Sell limit can fill when market trades at or above limit under the model.
3. Touching a price is not enough if the model requires queue or volume assumptions.
```

Stop order:

```text
1. Trigger condition and fill price must be separate.
2. Stop-market can trigger at stop_price and fill at modeled executable price.
3. Stop-limit can trigger but remain unfilled if limit constraints fail.
```

## Slippage Model

```json
{
  "slippage_model": "fixed_bps",
  "params": {
    "bps": "decimal string",
    "side_adjustment": "adverse | favorable | symmetric"
  }
}
```

Rules:

```text
1. Default performance claims must include non-zero cost assumptions unless project proves otherwise.
2. Favorable slippage must not be used as default without evidence.
3. Slippage model changes can alter EV and must be recorded as experiment changes.
```

## Fee Model

```json
{
  "fee_model": "maker_taker",
  "params": {
    "maker_bps": "decimal string",
    "taker_bps": "decimal string",
    "fee_asset": "quote | base | exchange_specific"
  }
}
```

Rules:

```text
1. Fees must be included in realized PnL and trade result analysis.
2. Maker/taker classification must be explicit or unknown.
3. Exchange-specific fee schedules are time-sensitive knowledge and must be sourced in the business project or RAG.
```

## Latency Model

```json
{
  "latency_model": "fixed_ms",
  "params": {
    "submit_latency_ms": 0,
    "ack_latency_ms": 0,
    "market_data_latency_ms": 0
  }
}
```

Rules:

```text
1. Latency can change fill price and missed-fill probability.
2. Replay and simulation should model event order under latency.
3. Backtests that ignore latency must disclose that limitation.
```

## Partial Fill Model

```text
none:
  Fill all or nothing.

proportional_volume:
  Fill up to a percentage of observed volume.

order_book_depth:
  Fill according to available depth and queue assumptions.

custom:
  Must define calculation_trace.
```

Rules:

```text
1. Partial fills must emit multiple FillEvent entries or one partially_filled state.
2. Strategy logic must be tested against partial fills before live use.
3. Ignoring partial fills is an optimistic assumption for many live systems.
```

## Ambiguity Rules

Return `ambiguous` when:

```text
1. OHLC data cannot determine intrabar ordering and assumption says no_intrabar_inference.
2. Data gap overlaps trigger or fill range.
3. Limit touch occurs without volume or queue assumption required by the model.
4. Order book data is stale or missing when order_book_based model is required.
```

Ambiguous fills cannot be treated as normal wins or losses without an explicit resolution rule.

## Validation Metrics

```text
fill_rate
partial_fill_rate
average_slippage
fee_per_trade
ambiguous_fill_count
same_candle_conflict_count
missed_fill_count
live_vs_sim_fill_delta
```

## Audit Checklist

```text
1. Is assumption_id recorded in every simulated FillEvent?
2. Is same-candle TP/SL policy explicit?
3. Are fees and slippage included?
4. Are latency and partial fills considered or explicitly excluded?
5. Are ambiguous fills separated from normal fills?
6. Does the model avoid using future data?
7. Can the same strategy be re-run with alternative assumptions for sensitivity analysis?
```

## Forbidden Claims

```text
1. Do not claim live equivalence from OHLC-only fills.
2. Do not hide optimistic same-candle assumptions.
3. Do not report performance without fee and slippage disclosure.
4. Do not treat ambiguous fills as resolved without a stated rule.
5. Do not place FillModel logic inside signal generation.
```
