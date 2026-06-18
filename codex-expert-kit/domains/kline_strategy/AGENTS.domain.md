# Kline Strategy Domain

Use this domain for K-line trend, multi-timeframe alignment, breakout/pullback/reversal setups, SL/TP structure, ATR/RSI/volume interpretation, and entry timing.

## Scope

```text
trend state
market regime
multi-timeframe direction and entry
breakout / pullback / continuation / reversal setups
SL invalidation level
TP reachability
RR after costs
K-line data quality
```

## Required Rules

```text
1. Trend judgment is not entry judgment.
2. Correct direction does not imply good entry.
3. Attractive RR does not imply reachable TP.
4. Indicator crossovers are evidence, not standalone orders.
5. SL must map to invalidation, not random noise.
```

## Output Contract

```json
{
  "symbol": "",
  "timeframe_trend": "",
  "timeframe_entry": "",
  "trend_state": "uptrend | downtrend | range | transition",
  "entry_setup": "breakout | pullback | reversal | continuation | none",
  "direction": "long | short | none",
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
