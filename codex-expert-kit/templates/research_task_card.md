# CEK-TA Research Task Card Template

Use this template when Codex needs to collect professional knowledge from the network before adding or updating CEK-TA knowledge.

All Chinese content must be read and written as UTF-8.

## Basic Info

```yaml
task_id: CEK-TA-RESEARCH-YYYYMMDD-001
status: draft
owner: codex
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
question: ""
reason: ""
```

## Classification

```yaml
partition_id: ""
domain: ""
subdomain: ""
rule_type: ""
used_for:
  - ""
candidate_knowledge_id: ""
```

## Research Question

Write the exact professional question:

```text
Example:
For 1m OHLC backtests, when TP and SL are both touched inside the same candle, what deterministic fill-order assumptions are professionally acceptable, and what must be disclosed?
```

## Scope

```yaml
market: "crypto | futures | spot | stock | general"
asset: "BTC | ETH | multi | general"
timeframe: "tick | 1s | 1m | 3m | 15m | 1h | 4h | 1d | general"
data_granularity: "tick | trade | order_book | second | kline | account_event | general"
project_type: ""
applies_when:
  - ""
not_applicable_when:
  - ""
assumptions:
  - ""
```

## Required Source Types

Prefer sources in this order:

```text
P0:
  official_doc
  exchange_rule
  standard protocol
  original paper
  authoritative data source

P1:
  framework_doc
  open-source project official docs
  engineering whitepaper

P2:
  professional book
  course
  research report
  industry article

P3:
  blog
  forum
  experience post
```

P3 sources cannot independently approve a professional rule.

## Search Plan

```text
1. Search primary sources first.
2. Search framework or implementation docs second.
3. Search papers or professional reports for theory and methodology.
4. Search engineering discussions only to discover edge cases.
5. Compare sources by market, timeframe, data granularity, assumptions, version, and date.
```

## Candidate Queries

```text
query_1:
query_2:
query_3:
query_4:
```

## Source Log

```json
[
  {
    "source_id": "src_001",
    "source_title": "",
    "source_url": "",
    "source_type": "",
    "publisher": "",
    "published_at": null,
    "accessed_at": "YYYY-MM-DD",
    "version": null,
    "reliability": "",
    "score": 0,
    "relevance": "",
    "freshness": "",
    "limitations": []
  }
]
```

## Extracted Claims

For each claim, keep the statement separate from interpretation:

```yaml
claims:
  - claim_id: claim_001
    statement: ""
    source_ids:
      - src_001
    applicability:
      market: ""
      timeframe: ""
      data_granularity: ""
    assumptions:
      - ""
    limitations:
      - ""
```

## Conflict Check

```yaml
checked_against:
  - knowledge_id: ""
    title: ""
conflicts:
  - conflict_type: "direct_conflict | scope_conflict | version_conflict | market_conflict | granularity_conflict | assumption_conflict"
    severity: "blocking | warning | informational"
    candidate_claim: ""
    existing_claim: ""
    resolution: ""
    approval_allowed: false
```

## Proposed Knowledge Item

```yaml
knowledge_id: ""
title: ""
statement: ""
rationale: ""
procedure:
  - ""
examples:
  - ""
anti_patterns:
  - ""
validation:
  - ""
risk_notes:
  - ""
confidence: "high | medium | low"
freshness: "stable | time_sensitive | deprecated"
review_status: "draft | reviewed | approved | rejected | deprecated"
```

## RAG / Skill Decision

```text
Enter RAG when:
1. The item is source-backed.
2. The item has explicit applicability and conflict status.
3. It is useful as retrievable professional context.

Enter Skill when:
1. The item defines a repeated workflow Codex should execute.
2. The steps are stable enough to become operating procedure.
3. The workflow can be generalized beyond one project.
```

## Audit Output

Codex must report:

```text
1. Sources used.
2. Source quality scores.
3. Claims extracted.
4. Conflicts found.
5. Resolution or blocking reason.
6. Proposed knowledge item fields.
7. Whether it should enter RAG, Skill, both, or neither.
8. Human review questions.
```

## Definition of Done

```text
1. Research question is precise.
2. Sources are logged with accessed_at and source_type.
3. Source quality is scored.
4. Claims are separated from interpretation.
5. Applicability and assumptions are explicit.
6. Conflict check is completed.
7. Proposed knowledge item follows knowledge_item_schema.md.
8. Approval status is justified.
9. UTF-8 content is readable.
```

## Human Review Questions

```text
1.
2.
3.
```
