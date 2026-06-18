# CEK-TA Source Quality Rules

This file defines source quality scoring for CEK-TA knowledge collection, audit, retrieval, MCP output, and Vue3 review.

## Purpose

Source quality scoring answers:

```text
Can this source support a professional rule?
Can this rule become approved?
Does the source apply to the same market, data granularity, timeframe, and software version as the knowledge item?
Does the source need refresh before use?
```

## Source Reliability Levels

| Reliability | Typical Sources | Usage |
| --- | --- | --- |
| `high` | Official docs, exchange rules, standard protocols, original papers, authoritative framework docs. | Can support approved knowledge if applicability and conflicts are clear. |
| `medium` | Professional books, research reports, engineering articles, documented internal reports, well-maintained open-source project docs. | Can support approved knowledge when evidence is specific and conflict-free. |
| `low` | Blogs, forums, social posts, undocumented notes, copied summaries, unverifiable opinions. | Supporting context only. Cannot alone support approved knowledge. |

## Source Type Policy

| source_type | Default Reliability | Notes |
| --- | --- | --- |
| `official_doc` | high | Best for product, API, library, and model behavior. Time-sensitive. |
| `exchange_rule` | high | Best for order, margin, contract, risk, and live execution rules. Time-sensitive. |
| `paper` | high | Strong for theory, metrics, methodology, and microstructure definitions. Check assumptions. |
| `framework_doc` | high | Strong for backtest/RAG/LLM framework behavior. Time-sensitive. |
| `book` | medium | Strong for stable principles. Usually weak for current APIs or exchange behavior. |
| `research_report` | medium | Useful for market or strategy analysis. Check sample, period, and bias. |
| `engineering_article` | medium | Useful for implementation patterns. Check author, reproducibility, and version. |
| `internal_report` | medium | Useful after sanitization and evidence review. Not automatically general. |
| `task_card` | medium | Useful for workflow history. Needs source evidence before becoming general knowledge. |
| `code_doc` | medium | Useful for local behavior. Usually project-bound unless generalized. |
| `runbook` | medium | Useful for operations. Needs sanitization and scope. |

## Scoring Dimensions

Score each source from 0 to 100:

| Dimension | Max | Meaning |
| --- | ---: | --- |
| Authority | 20 | Publisher or author is primary, official, or professionally credible. |
| Specificity | 15 | Source directly addresses the exact claim, market, timeframe, or API behavior. |
| Applicability | 15 | Source scope matches the knowledge item's applicability fields. |
| Freshness | 15 | Source is current enough for its domain and time sensitivity. |
| Reproducibility | 10 | Claim can be tested, computed, or traced to clear data/methods. |
| Primary Evidence | 10 | Source is primary rather than a second-hand summary. |
| Conflict History | 10 | Source does not conflict with stronger approved knowledge, or conflict is resolved. |
| License / Reuse Safety | 5 | Source can be summarized and cited safely. |

## Score Bands

```text
85-100: high reliability
60-84: medium reliability
0-59: low reliability
```

The score band can be downgraded by policy even when the numeric score is high.

## Mandatory Downgrades

Downgrade source reliability when:

```text
1. The source is not primary and contradicts a primary source.
2. The source does not cover the candidate item's market or data granularity.
3. The source is stale for exchange rules, model/API behavior, or library behavior.
4. The source lacks enough context to reproduce a claim.
5. The source is a blog/forum/social post used as the only evidence.
6. The source contains project-private facts that have not been sanitized.
7. The source makes performance claims without sample definition, costs, or bias controls.
```

## Freshness Windows

These are default review windows, not automatic truth rules:

| Knowledge Area | Default Freshness | Recheck Guidance |
| --- | --- | --- |
| Exchange rules and live execution | time_sensitive | Recheck before high-impact use; prefer current official docs. |
| Model/API/library behavior | time_sensitive | Recheck when versions change or before implementation. |
| Backtest methodology and bias concepts | stable | Recheck if tied to a specific framework or data vendor. |
| Market microstructure concepts | stable or time_sensitive | Stable for definitions, time-sensitive for exchange-specific behavior. |
| K-line strategy heuristics | stable with caveats | Review assumptions, sample, and market regime. |
| LLM/RAG engineering | time_sensitive | Recheck framework and model behavior. |
| Project runbooks and internal reports | time_sensitive | Recheck when project architecture or adapter behavior changes. |

## Knowledge Approval Policy

```text
1. Approved knowledge needs at least one high or medium reliability source.
2. Low reliability sources can supplement, but cannot be the only basis for approval.
3. A high-quality source outside the item's applicability scope cannot approve the item.
4. Performance claims require sample definition, costs, bias controls, and reproducibility notes.
5. Live trading and risk-control rules prefer official or exchange sources.
6. If sources disagree, conflict_detection_rules.md decides approval blocking.
```

## Source Record Contract

Every source record must include:

```json
{
  "source_id": "src_001",
  "source_title": "string",
  "source_url": "string | null",
  "source_type": "official_doc | paper | exchange_rule | framework_doc | book | research_report | engineering_article | internal_report | task_card | code_doc | runbook",
  "publisher": "string | null",
  "published_at": "YYYY-MM-DD | null",
  "accessed_at": "YYYY-MM-DD",
  "version": "string | null",
  "reliability": "high | medium | low",
  "score": 0,
  "relevance": "high | medium | low",
  "freshness": "stable | time_sensitive | deprecated",
  "limitations": ["string"]
}
```

## Vue3 Audit Fields

Vue3 review UI should expose:

```text
source_type
publisher
published_at
accessed_at
version
reliability
score
relevance
freshness
limitations
primary_source_count
supporting_source_count
```

## Test Checklist

For every new or updated source:

```text
1. Is the source URL or bibliographic record traceable?
2. Is accessed_at present?
3. Is the source primary or secondary?
4. Does the source support the exact claim?
5. Does it apply to the stated market/timeframe/granularity?
6. Is it fresh enough?
7. Does it conflict with stronger approved knowledge?
8. Can it be cited or summarized safely?
```
