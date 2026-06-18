# CEK-TA Conflict Detection Rules

This file defines how CEK-TA detects, classifies, blocks, and resolves conflicts between professional knowledge items.

## Purpose

Knowledge conflict detection protects CEK-TA from returning contradictory trading, backtest, simulation, live execution, RAG, or LLM training guidance as if it were a single universal rule.

## Conflict Types

| Type | Meaning | Approval Impact |
| --- | --- | --- |
| `direct_conflict` | Two rules reach opposite conclusions under the same scope. | Blocking until resolved. |
| `scope_conflict` | Rules may both be valid, but the applicable scope is not explicit. | Blocking until boundaries are written. |
| `version_conflict` | A newer version of a rule, API, exchange rule, or framework behavior differs from an older one. | Blocking for time-sensitive items. |
| `market_conflict` | Rules differ by market, such as crypto, spot, futures, stock, or derivatives. | Blocking unless market boundaries are explicit. |
| `granularity_conflict` | Rules differ by data granularity, such as tick, trade, order book, 1m K-line, or daily bar. | Blocking unless granularity boundaries are explicit. |
| `assumption_conflict` | Rules depend on different fees, slippage, latency, liquidity, fill, or model assumptions. | Blocking unless assumptions are explicit. |

## Input Contract

Conflict detection receives:

```json
{
  "candidate_item": "knowledge_item",
  "comparison_set": ["knowledge_item"],
  "required_match_fields": [
    "domain",
    "subdomain",
    "rule_type"
  ],
  "optional_scope_fields": [
    "market",
    "asset",
    "timeframe",
    "data_granularity",
    "project_type",
    "source_type",
    "published_at",
    "version"
  ]
}
```

## Candidate Selection

Compare a candidate knowledge item against existing items when any condition is true:

```text
1. Same domain and subdomain.
2. Same rule_type and overlapping used_for.
3. Same market and timeframe but different conclusion.
4. Same source family but different version.
5. Same professional concept appears in title, statement, tags, or evidence_summary.
```

Do not compare only by keyword. Metadata overlap and applicability overlap must be checked.

## Detection Workflow

```text
1. Normalize metadata:
   - partition_id
   - domain
   - subdomain
   - rule_type
   - market
   - timeframe
   - data_granularity
   - assumptions
   - source version and dates

2. Normalize the claim:
   - identify the main statement
   - identify whether it is prescriptive, descriptive, procedural, formulaic, or a warning
   - identify the conclusion polarity when possible

3. Check scope overlap:
   - same market or one side says general
   - same timeframe or one side says general
   - same data_granularity or one side says general
   - same project_type or one side says general

4. Check evidence:
   - source_type
   - source reliability
   - source version
   - accessed_at
   - whether source supports the exact scope

5. Classify conflict:
   - direct
   - scope
   - version
   - market
   - granularity
   - assumption

6. Decide severity:
   - blocking
   - warning
   - informational

7. Write resolution:
   - boundary split
   - preferred default
   - deprecated old rule
   - needs human review
```

## Conflict Matrix

| Signal | Likely Conflict Type | Example Pattern |
| --- | --- | --- |
| Same scope, opposite rule | `direct_conflict` | Rule A says use fill-first, Rule B says use stop-first under the same bar model. |
| One rule says general, another limits scope | `scope_conflict` | General claim lacks timeframe while evidence only covers 1m K-line. |
| Same API or exchange rule, different version | `version_conflict` | Old behavior conflicts with current official documentation. |
| Futures vs spot behavior differs | `market_conflict` | Funding, liquidation, margin, or order rules differ by product. |
| Tick data vs K-line data differs | `granularity_conflict` | Same-candle ordering cannot be inferred from OHLC alone. |
| Different fill, fee, latency, liquidity model | `assumption_conflict` | Backtest conclusion changes under different slippage model. |

## Resolution Order

When conflicts appear, resolve in this order:

```text
1. Source level:
   official_doc / exchange_rule / paper usually outrank unsourced or informal notes.

2. Exact applicability:
   exact market, timeframe, and granularity outrank a broad general claim.

3. Version and freshness:
   newer official or framework behavior outranks older behavior for time-sensitive knowledge.

4. Assumptions:
   explicit assumptions outrank hidden assumptions.

5. Safety:
   for live trading and risk control, choose the more conservative default when evidence is incomplete.

6. Branching:
   preserve multiple valid rules as separate branches when scopes differ.

7. Human review:
   if two high-quality sources disagree under the same scope, block approval and require human review.
```

## Output Contract

```json
{
  "candidate_knowledge_id": "string",
  "conflict_status": "none | potential | confirmed | resolved | deprecated_by_conflict",
  "checked_against": ["knowledge_id"],
  "conflicts": [
    {
      "knowledge_id": "string",
      "conflict_type": "direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict",
      "severity": "blocking | warning | informational",
      "overlap_scope": {
        "domain": "string",
        "subdomain": "string",
        "market": "string",
        "timeframe": "string",
        "data_granularity": "string"
      },
      "candidate_claim": "string",
      "existing_claim": "string",
      "resolution": "string",
      "default_recommendation": "string | null",
      "requires_human_review": true
    }
  ],
  "resolution_summary": "string",
  "approval_allowed": false
}
```

## Approval Blocking Conditions

Approval is blocked when:

```text
1. conflict_status is confirmed.
2. any conflict severity is blocking and resolution is empty.
3. a rule claims general applicability but evidence is market-specific or granularity-specific.
4. a time-sensitive conflict has no current source check.
5. two approved items would produce opposite default guidance for the same downstream task.
```

## Non-Blocking Cases

These can proceed with warnings:

```text
1. Same concept, different markets, and both boundaries are explicit.
2. Same concept, different data granularity, and both boundaries are explicit.
3. Old item is already deprecated.
4. Candidate is a case study, not a default rule.
5. Candidate is draft and marked for audit only.
```

## Test Checklist

Every conflict audit must answer:

```text
1. Which existing items were checked?
2. Which fields overlapped?
3. Which conflict type was found?
4. Is approval allowed?
5. If approved, what exact boundary prevents contradiction?
6. If blocked, who must review it and what evidence is missing?
```
