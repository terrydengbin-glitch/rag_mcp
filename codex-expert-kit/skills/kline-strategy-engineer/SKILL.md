---
name: kline-strategy-engineer
description: Design and audit K-line trading strategies, including trend state, multi-timeframe alignment, entry setup, SL/TP structure, RR, ATR/RSI/volume evidence, and K-line data quality. Use for K-line strategy specs, signal rules, chart-based entries, or trend/entry disputes.
---

# Kline Strategy Engineer

## Workflow

1. Identify market, symbol, trend timeframe, and entry timeframe.
2. Classify trend state: uptrend, downtrend, range, or transition.
3. Separate direction evidence from entry trigger.
4. Classify setup: breakout, pullback, continuation, reversal, or none.
5. Place invalidation before SL/TP.
6. Check TP reachability and RR after costs.
7. List evidence and risk notes.

## Hard Rules

```text
Trend judgment is not entry judgment.
Correct direction does not imply reasonable entry.
RR being attractive does not imply TP is reachable.
Indicator crosses are supporting evidence, not standalone orders.
SL must map to structure invalidation.
```

## Output

```json
{
  "symbol": "",
  "timeframe_trend": "",
  "timeframe_entry": "",
  "trend_state": "",
  "entry_setup": "",
  "direction": "",
  "entry_trigger": "",
  "invalid_level": null,
  "stop_loss": null,
  "take_profit": null,
  "rr": null,
  "confidence": null,
  "evidence": [],
  "risk_notes": []
}
```
