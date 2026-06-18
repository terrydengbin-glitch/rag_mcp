# CEK-TA Chunking Rules

This file defines how CEK-TA documents should be split for RAG ingestion.

Chunking must preserve source, applicability, and conflict context. Do not create chunks that lose the rule's assumptions or source.

## Global Chunk Contract

Every chunk must retain:

```text
knowledge_id
chunk_id
title
partition_id
domain
subdomain
source
review_status
confidence
freshness
conflict_status
section_path
```

## Default Sizes

```text
target_chunk_size: 400-800 tokens
max_chunk_size: 1200 tokens
overlap: 80-150 tokens
```

Use smaller chunks for checklists and schemas. Use larger chunks only when splitting would remove assumptions or evidence.

## Markdown Rules

```text
1. Split by heading hierarchy.
2. Keep a heading with its first explanatory paragraph.
3. Do not separate a rule from its assumptions.
4. Do not separate a checklist item from its parent checklist title.
5. Do not split tables unless they exceed max chunk size.
6. Keep source/citation notes with the chunk they support.
```

## Schema Rules

For JSON/YAML schemas:

```text
1. Keep the full object schema together when possible.
2. If too large, split by top-level object sections.
3. Preserve required/optional meaning.
4. Preserve enum values with the field they belong to.
5. Add section_path showing the schema path.
```

## Code Rules

For code or pseudocode:

```text
1. Chunk by class, function, or tool definition.
2. Keep signature, docstring/comment, and return contract together.
3. Do not split input schema from output schema.
4. Do not ingest secrets, tokens, or credentials.
```

## Task Card / Runbook Rules

For task cards and runbooks:

```text
1. Chunk by task ID or major section.
2. Keep upstream, downstream, contract, DoD, and tests together when possible.
3. Mark project_binding correctly.
4. Sanitized project cases must retain contribution status.
```

## Conflict-Aware Chunking

If content discusses conflicting rules:

```text
1. Keep both sides of the conflict in the same chunk when possible.
2. Preserve conflict_type and resolution.
3. Do not let an unresolved conflict chunk be retrieved as an approved default rule.
```

## Forbidden Chunking

```text
1. Do not chunk source-less claims as reusable knowledge.
2. Do not chunk project-private fields into general partitions.
3. Do not remove freshness or review_status metadata.
4. Do not merge different markets or timeframes into one rule without applicability metadata.
```
