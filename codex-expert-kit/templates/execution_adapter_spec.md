# CEK-TA ExecutionAdapter Spec

This template defines how a project maps exchange-neutral `OrderIntent` objects into environment-specific execution behavior.

An ExecutionAdapter can represent a backtest engine, replay engine, paper trading environment, or live exchange adapter. The strategy layer should not know which one is active.

## Spec Version

```yaml
spec_name: cek_ta_execution_adapter
spec_version: 1.0.0
encoding: UTF-8
permission_default: contract_only_no_live_permission_granted
```

## Adapter Types

```text
backtest_adapter
replay_adapter
simulation_adapter
live_exchange_adapter
manual_review_adapter
```

Phase 4 defines the contract only. It does not grant live trading permission.

## Responsibilities

ExecutionAdapter must:

```text
1. Validate OrderIntent.
2. Apply environment constraints.
3. Convert OrderIntent to OrderRequest.
4. Submit or simulate the order according to adapter type.
5. Emit OrderAck, OrderState, FillEvent, ExecutionReport, and ErrorEvent.
6. Preserve idempotency through client_order_id or adapter_order_id.
7. Record audit fields for replay and trade analysis.
```

ExecutionAdapter must not:

```text
1. Generate strategy signals.
2. Change strategy direction.
3. Hide risk rejection.
4. Read secrets unless the live project explicitly owns and authorizes that adapter.
5. Place live orders from CEK-TA support-layer templates.
```

## Input: OrderIntent

See `interface_contract.md`.

Minimum required fields:

```text
intent_id
decision_id
symbol
side
position_effect
order_type
qty
reason_codes
created_at
```

## Output: OrderRequest

```json
{
  "request_id": "string",
  "intent_id": "string",
  "adapter_type": "backtest_adapter | replay_adapter | simulation_adapter | live_exchange_adapter | manual_review_adapter",
  "symbol": "string",
  "side": "buy | sell",
  "order_type": "market | limit | stop | stop_limit | take_profit | take_profit_limit",
  "qty": "decimal string",
  "limit_price": "decimal string | null",
  "stop_price": "decimal string | null",
  "time_in_force": "GTC | IOC | FOK | GTX | DAY | null",
  "reduce_only": false,
  "post_only": false,
  "client_order_id": "string",
  "adapter_params": {},
  "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
}
```

Rules:

```text
1. adapter_params are project-bound and must not become CEK-TA general knowledge.
2. client_order_id must be deterministic or persisted enough for idempotency.
3. Unsupported order flags must cause rejection, not silent removal.
```

## Output: OrderAck

```json
{
  "ack_id": "string",
  "request_id": "string",
  "intent_id": "string",
  "adapter_order_id": "string | null",
  "status": "accepted | rejected",
  "reject_reason": "string | null",
  "accepted_at": "YYYY-MM-DDTHH:mm:ss.sssZ | null",
  "raw_ref": "string | null"
}
```

Rules:

```text
1. rejected must include reject_reason.
2. raw_ref must not expose secrets or private account identifiers.
```

## Output: OrderState

```json
{
  "adapter_order_id": "string",
  "client_order_id": "string",
  "intent_id": "string",
  "symbol": "string",
  "state": "new | partially_filled | filled | canceled | rejected | expired | unknown",
  "filled_qty": "decimal string",
  "remaining_qty": "decimal string",
  "avg_fill_price": "decimal string | null",
  "last_update_time": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "source": "backtest | replay | simulation | exchange"
}
```

## Output: FillEvent

```json
{
  "fill_id": "string",
  "adapter_order_id": "string",
  "client_order_id": "string",
  "intent_id": "string",
  "symbol": "string",
  "side": "buy | sell",
  "qty": "decimal string",
  "price": "decimal string",
  "fee": "decimal string | null",
  "fee_asset": "string | null",
  "liquidity": "maker | taker | unknown",
  "filled_at": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "fill_model_id": "string | null",
  "assumption_id": "string | null"
}
```

## Output: ExecutionReport

```json
{
  "execution_report_id": "string",
  "intent_id": "string",
  "request_id": "string",
  "adapter_type": "string",
  "final_state": "filled | partially_filled | canceled | rejected | expired | unknown",
  "fills": [],
  "order_states": [],
  "position_snapshot_before": "PositionSnapshot | null",
  "position_snapshot_after": "PositionSnapshot | null",
  "errors": [],
  "warnings": [],
  "audit_trace_id": "string | null"
}
```

## ErrorEvent

```json
{
  "error_id": "string",
  "intent_id": "string | null",
  "request_id": "string | null",
  "code": "invalid_intent | risk_rejected | unsupported_order_type | unsupported_flag | min_qty_violation | price_filter_violation | insufficient_balance | adapter_unavailable | timeout | reconciliation_failed | permission_denied | unknown",
  "message": "string",
  "severity": "info | warning | error | critical",
  "retryable": false,
  "created_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
}
```

## State Machine

```text
created
  -> validated
  -> request_created
  -> accepted
  -> partially_filled
  -> filled

accepted
  -> canceled
accepted
  -> expired
created / validated / request_created
  -> rejected
any_state
  -> unknown
```

Rules:

```text
1. Every terminal state must emit ExecutionReport.
2. unknown requires reconciliation before next live decision can rely on position.
3. Backtest and replay adapters must emit deterministic order states.
```

## Validation Rules

Before accepting an OrderIntent:

```text
1. Required fields exist.
2. qty > 0.
3. side is buy or sell.
4. order_type is supported by adapter.
5. limit_price exists for limit orders.
6. stop_price exists for stop orders.
7. reduce_only does not conflict with position_effect.
8. symbol is supported.
9. min_qty, tick_size, lot_size, and price filters pass when known.
10. RiskState allows the action.
```

## Permission Boundary

```text
backtest_adapter:
  no external permission

replay_adapter:
  no external permission unless reading external data

simulation_adapter:
  paper environment only

live_exchange_adapter:
  must be implemented in business project, not in CEK-TA templates
  must use least-privilege API keys
  must support kill switch and reconciliation
```

## Idempotency

```text
1. Duplicate OrderIntent with same client_order_id must not create duplicate live orders.
2. Adapter must expose duplicate handling behavior.
3. Retry behavior must be explicit.
```

## Reconciliation

Live adapters must reconcile:

```text
1. open orders
2. recent fills
3. position snapshot
4. account risk limits
5. unknown order states
```

If reconciliation fails, live trading must stop or degrade to manual review.

## Test Cases

```text
1. Valid market order intent -> accepted -> filled or simulated fill.
2. Missing qty -> invalid_intent.
3. Unsupported order_type -> unsupported_order_type.
4. reduce_only open order -> invalid_intent or risk_rejected.
5. Duplicate client_order_id -> no duplicate order.
6. Unknown state -> reconciliation required.
7. Live permission request from CEK-TA template -> permission_denied.
```

## Audit Checklist

```text
1. Does adapter preserve strategy OrderIntent semantics?
2. Are rejections explicit?
3. Are fills traceable to fill model or exchange event?
4. Are partial fills represented?
5. Are live-only failures represented without changing strategy logic?
6. Is rollback possible by swapping adapter or disabling live adapter?
```
