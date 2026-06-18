# CEK-TA Unified Trading Interface Contract

This template defines shared trading semantics for backtest, replay, simulation, and live trading projects.

It is a contract, not an implementation. Project-specific field names must be mapped through a project adapter instead of being copied into CEK-TA.

## Contract Version

```yaml
contract_name: cek_ta_trading_interface
contract_version: 1.0.0
encoding: UTF-8
scope: strategy_semantics
```

## Design Principle

```text
Strategy logic should produce the same Decision and OrderIntent under the same inputs.
Backtest, replay, simulation, and live trading should differ only through DataSource, ExecutionAdapter, and FillModel.
```

## Layer Boundary

```text
DataSource
  -> MarketEvent
  -> FeatureBuilder
  -> FeatureFrame
  -> SignalEngine
  -> SignalFrame
  -> StrategyDecision
  -> RiskGate
  -> OrderIntent
  -> ExecutionAdapter
  -> OrderRequest / FillEvent / ExecutionReport
```

Strategy code must not directly call exchange APIs, database write APIs, notification services, or account secrets.

## Core Objects

### ClockState

```json
{
  "event_time": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "processing_time": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "timezone": "UTC",
  "sequence": 0,
  "mode": "backtest | replay | simulation | live"
}
```

Rules:

```text
1. event_time is market time.
2. processing_time is system time.
3. Backtest logic must not use future event_time.
4. Replay must preserve event sequence.
```

### MarketEvent

```json
{
  "event_id": "string",
  "event_type": "kline | trade | order_book | funding | account | timer",
  "symbol": "string",
  "market": "crypto | futures | spot | stock | general",
  "timeframe": "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general",
  "data_granularity": "tick | trade | order_book | second | kline | account_event | general",
  "clock": "ClockState",
  "payload": {}
}
```

Rules:

```text
1. payload must be schema-versioned by event_type.
2. Missing OHLCV fields must be explicit, not silently filled.
3. Data gaps must be represented as events or quality flags.
```

### Kline

```json
{
  "symbol": "string",
  "open_time": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "close_time": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "timeframe": "1m",
  "open": "decimal string",
  "high": "decimal string",
  "low": "decimal string",
  "close": "decimal string",
  "volume": "decimal string",
  "is_closed": true,
  "source": "string",
  "quality_flags": []
}
```

Rules:

```text
1. Decimal values should be strings at boundaries to avoid binary float drift.
2. A strategy must declare whether it can use an open candle.
3. Same-candle TP/SL behavior cannot be inferred from OHLC alone.
```

### FeatureFrame

```json
{
  "feature_frame_id": "string",
  "symbol": "string",
  "clock": "ClockState",
  "features": {},
  "lookback_window": {
    "start": "YYYY-MM-DDTHH:mm:ss.sssZ",
    "end": "YYYY-MM-DDTHH:mm:ss.sssZ",
    "bars": 0
  },
  "quality_flags": [],
  "source_event_ids": []
}
```

Rules:

```text
1. FeatureFrame must declare source_event_ids for audit.
2. Features must not include future data.
3. Feature names are project-specific and must be mapped by adapter when contributed back to CEK-TA.
```

### SignalFrame

```json
{
  "signal_frame_id": "string",
  "symbol": "string",
  "clock": "ClockState",
  "direction": "long | short | flat | no_trade",
  "strength": "decimal string | null",
  "reason_codes": [],
  "invalid_when": [],
  "source_feature_frame_id": "string"
}
```

Rules:

```text
1. Direction and entry permission are separate.
2. Signal strength is not a position size unless explicitly mapped by risk logic.
3. reason_codes must be deterministic and audit-friendly.
```

### PositionSnapshot

```json
{
  "position_id": "string | null",
  "symbol": "string",
  "side": "long | short | flat",
  "qty": "decimal string",
  "entry_price": "decimal string | null",
  "mark_price": "decimal string | null",
  "unrealized_pnl": "decimal string | null",
  "realized_pnl": "decimal string | null",
  "leverage": "decimal string | null",
  "updated_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "source": "backtest | replay | simulation | exchange | manual"
}
```

Rules:

```text
1. PositionSnapshot is an observation, not an instruction.
2. Live trading must reconcile adapter position with exchange position.
3. Backtest position must use the same side and qty semantics as live adapter.
```

### RiskState

```json
{
  "risk_state_id": "string",
  "daily_realized_pnl": "decimal string | null",
  "open_risk": "decimal string | null",
  "consecutive_losses": 0,
  "cooldown_until": "YYYY-MM-DDTHH:mm:ss.sssZ | null",
  "kill_switch_active": false,
  "limits": {
    "max_position_qty": "decimal string | null",
    "max_single_trade_loss": "decimal string | null",
    "max_daily_loss": "decimal string | null"
  }
}
```

Rules:

```text
1. RiskState must be checked before OrderIntent becomes OrderRequest.
2. Live trading must have kill switch support.
3. Risk rejection must emit reason_codes.
```

### Decision

```json
{
  "decision_id": "string",
  "symbol": "string",
  "clock": "ClockState",
  "action": "enter | exit | reduce | hold | cancel | no_trade",
  "side": "long | short | flat | null",
  "confidence": "high | medium | low | null",
  "reason_codes": [],
  "source_signal_frame_id": "string",
  "audit_trace_id": "string"
}
```

Rules:

```text
1. Decision is strategy intent before order details.
2. A hold or no_trade decision must still be explainable.
3. Changing Decision semantics is a strategy change and needs validation.
```

### OrderIntent

```json
{
  "intent_id": "string",
  "decision_id": "string",
  "symbol": "string",
  "side": "buy | sell",
  "position_effect": "open | close | reduce | flip",
  "order_type": "market | limit | stop | stop_limit | take_profit | take_profit_limit",
  "qty": "decimal string",
  "limit_price": "decimal string | null",
  "stop_price": "decimal string | null",
  "time_in_force": "GTC | IOC | FOK | GTX | DAY | null",
  "reduce_only": false,
  "post_only": false,
  "client_order_id": "string | null",
  "risk": {
    "stop_loss": "decimal string | null",
    "take_profit": "decimal string | null",
    "max_loss": "decimal string | null"
  },
  "reason_codes": [],
  "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
}
```

Rules:

```text
1. OrderIntent is exchange-neutral.
2. ExecutionAdapter maps OrderIntent to environment-specific OrderRequest.
3. The same OrderIntent must be valid for backtest, replay, simulation, and live unless adapter rejects it with explicit reason.
4. reduce_only and position_effect must not contradict each other.
```

### AuditTrace

```json
{
  "audit_trace_id": "string",
  "source_event_ids": [],
  "feature_frame_id": "string",
  "signal_frame_id": "string",
  "decision_id": "string",
  "intent_id": "string | null",
  "knowledge_ids": [],
  "assumptions": [],
  "warnings": []
}
```

Rules:

```text
1. Every tradeable decision should be traceable to inputs and assumptions.
2. knowledge_ids can reference CEK-TA knowledge used during review or generation.
3. AuditTrace must not contain secrets or raw private account data.
```

## Strategy Change Contract

Any strategy change must state:

```text
1. Input fields changed.
2. Output fields changed.
3. Affected modules.
4. Whether trade frequency may change.
5. Whether win rate, RR, EV, drawdown, cost, or holding time may change.
6. Validation metrics.
7. Rollback path.
```

## Compatibility Rules

```text
1. Required fields cannot be removed without a new contract_version.
2. Optional fields can be added if downstream readers ignore unknown fields.
3. Project-private fields must live in project adapter mapping.
4. Decimal boundary fields should use strings.
5. Timestamps should use ISO-8601 UTC unless project adapter declares otherwise.
```

## Validation Checklist

```text
1. Can the same StrategyDecision produce the same OrderIntent in all modes?
2. Is every OrderIntent traceable to source events and reason codes?
3. Are risk gates separated from signal generation?
4. Are live-only constraints represented as adapter rejection reasons?
5. Are fill assumptions outside strategy logic?
6. Are project-specific fields isolated behind adapter mapping?
```
