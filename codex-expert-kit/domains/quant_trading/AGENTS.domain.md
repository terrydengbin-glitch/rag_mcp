# Quant Trading Domain

Use this domain for strategy architecture, signal flow, risk, sizing, RR/EV, cost, execution, and trade-result interpretation.

## Scope

```text
strategy architecture
signal / feature / decision separation
risk gates
position sizing
RR / EV / cost analysis
execution basics
trade result feedback loop
```

## Required Checks

```text
1. What edge is the strategy trying to capture?
2. Are direction, entry, SL, TP, sizing, and execution separated?
3. Does the change affect frequency, win rate, RR, EV, drawdown, cost, or holding time?
4. Is validation defined before implementation?
5. Is rollback possible?
```

## Output Contract

```text
conclusion
affected modules
input fields
output fields
risk impact
validation metrics
rollback path
open questions
```
