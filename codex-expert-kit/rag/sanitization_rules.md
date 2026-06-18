# CEK-TA Sanitization and De-Projectization Rules

These rules define how business project findings are sanitized before they can be contributed to CEK-TA.

## Purpose

Sanitization protects:

```text
secrets
accounts
raw orders
private configs
project-private field dictionaries
people / organization-sensitive data
strategy-specific implementation details
```

De-projectization extracts the reusable professional rule from project facts.

## Must Remove

```text
API keys
secret keys
tokens
account IDs
wallet addresses when private
raw order IDs
raw fill IDs
raw trade logs
customer / team / user identities
private repository paths
private infrastructure names
exact live position or balance data
unpublished strategy parameters
```

## Must Generalize

| Project Fact | Generic Concept |
| --- | --- |
| project-specific feature field | feature category |
| project-specific reason code | generic reason code |
| local pipeline command | pipeline stage |
| exact strategy version | versioned strategy context |
| exchange account config | risk or adapter constraint |
| private dataset name | dataset class |

## Keep When Needed

Keep only sanitized evidence needed to preserve causal meaning:

```text
market type
timeframe
data granularity
strategy class
fill assumption
risk limit category
error category
bad-case label
source summary
```

## Sanitization Workflow

```text
1. Identify private data.
2. Remove secrets and account data.
3. Replace project field names with generic concepts.
4. Preserve evidence needed for causality.
5. Mark residual risk.
6. Verify no raw project data remains.
7. Map to CEK-TA domain/subdomain.
8. Run source and conflict checks.
```

## Residual Risk

```text
low:
  no private data remains and rule is generic

medium:
  some project context remains but cannot identify secrets/accounts/private config

high:
  sensitive data may remain or rule cannot be separated from project facts
```

High residual risk blocks contribution acceptance.

## De-Projectization Examples

```text
Bad:
  Field micro_fast in project v3.2 predicted false buy pressure after run_backtest.py --fast.

Good:
  A price-only proxy should not be treated as evidence of active buy pressure when order-flow data is unavailable.
```

```text
Bad:
  Account 123 was liquidated after Binance key X failed.

Good:
  Live adapters must fail closed when account reconciliation cannot verify position and open orders.
```

## Forbidden Transformations

```text
1. Do not hash secrets and keep them.
2. Do not keep raw account IDs as "examples".
3. Do not replace project field names while leaving private config values.
4. Do not remove so much context that the label becomes unsupported.
5. Do not convert a one-project workaround into a general rule.
```

## Acceptance Checklist

```text
1. No secrets remain.
2. No account data remains.
3. No raw orders remain.
4. Project-private fields are removed or mapped.
5. Applicability is explicit.
6. Sources are present.
7. Conflict check is complete.
8. Residual risk is low or medium.
9. Review decision is recorded.
```
