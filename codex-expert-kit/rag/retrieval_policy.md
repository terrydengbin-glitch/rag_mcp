# CEK-TA Retrieval Policy

This file defines how CEK-TA knowledge should be retrieved for Codex, MCP tools, and Vue3 audit workflows.

## Retrieval Goals

```text
1. Return source-backed professional knowledge.
2. Prefer approved knowledge.
3. Preserve applicability boundaries.
4. Expose conflict and freshness status.
5. Avoid leaking project-private facts into unrelated projects.
```

## Default Flow

```text
query
  -> task/domain router
  -> metadata filter
  -> dense search + sparse/BM25 search
  -> fusion
  -> rerank
  -> source quality filter
  -> conflict/freshness filter
  -> return top_k with citation metadata
```

## Domain Routing

Route by task:

```text
strategy design -> KB_01_QUANT_FOUNDATION, KB_02_KLINE_STRATEGY
K-line strategy -> KB_02_KLINE_STRATEGY
microstructure -> KB_03_MARKET_MICROSTRUCTURE
backtest review -> KB_04_BACKTEST, KB_05_REPLAY_SIMULATION
replay/simulation -> KB_05_REPLAY_SIMULATION
live trading -> KB_06_LIVE_EXECUTION
trade analysis -> KB_07_TRADE_ANALYSIS
LLM training -> KB_08_LLM_TRAINING
RAG/MCP design -> KB_09_RAG_ENGINEERING
project adapter/runbook -> KB_10_PROJECT_RUNBOOKS
```

## Required Filters

Use metadata filters whenever possible:

```text
tree_node_id
tree_path
tree_path_prefix
partition_id
domain
subdomain
used_for
review_status
freshness
confidence
project_binding
market
timeframe
data_granularity
source_type
```

## Knowledge Tree Routing

When a query can be mapped to a knowledge tree node, retrieval should use the node before broad keyword search:

```text
query
  -> task/domain router
  -> knowledge tree router
  -> tree_node_id or tree_path_prefix filter
  -> metadata filter
  -> dense search + sparse/BM25 search
  -> fusion and rerank
```

Tree routing rules:

```text
1. Exact tree_node_id is the strongest scope signal.
2. tree_path_prefix is used for browsing or broad topic search.
3. If a knowledge item has no tree_node_id, infer mapping only for audit and return a warning.
4. Empty nodes return coverage warnings and suggested research tasks, not professional guidance.
5. Conflicted or stale nodes must expose conflict/freshness warnings in the retrieval output.
```

## Review Status Policy

```text
approved: can be used as default guidance
reviewed: can be cited with caveat
draft: only for internal review, not default guidance
rejected: never use
deprecated: only use for historical comparison
```

## Freshness Policy

```text
stable: safe for normal retrieval
time_sensitive: retrieve with recheck warning
deprecated: do not use except for historical context
```

For exchange rules, current model/API behavior, library behavior, or live-trading requirements, time-sensitive knowledge must be verified before high-impact use.

## Conflict Policy

```text
none: safe if approved
potential: return with warning
confirmed: do not use as default guidance
resolved: return with resolution
deprecated_by_conflict: do not use except history
```

If two retrieved rules conflict, Codex must state the conflict and compare applicability instead of merging them.

## Project Binding Policy

```text
none: reusable across projects
project_name: only return when the active project matches
sanitized_project_case: return as example/case, not default rule
```

Never use project-private facts as general CEK-TA knowledge.

## Ranking Defaults

Recommended ranking priority:

```text
1. review_status = approved
2. source.reliability = high
3. exact domain/subdomain match
4. exact used_for match
5. exact market/timeframe/data_granularity match
6. freshness not deprecated
7. recent accessed_at for time_sensitive items
```

## Return Contract

Every retrieval result must include:

```json
{
  "knowledge_id": "",
  "title": "",
  "partition_id": "",
  "tree_node_id": "",
  "tree_path": "",
  "domain": "",
  "subdomain": "",
  "summary": "",
  "source": {
    "title": "",
    "url": null,
    "source_type": "",
    "reliability": ""
  },
  "confidence": "",
  "freshness": "",
  "review_status": "",
  "conflict_status": "",
  "applicability": {},
  "score": 0
}
```

## Refusal / Escalation Conditions

Do not return as authoritative guidance when:

```text
1. no source exists
2. review_status is rejected
3. conflict_status is confirmed without resolution
4. item is deprecated
5. project_binding does not match active project
6. time_sensitive item is stale and high-impact decision depends on it
```

In those cases, return an audit warning and ask for source refresh or human review.
