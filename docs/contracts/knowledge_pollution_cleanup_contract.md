# Knowledge Pollution Cleanup Contract

## Purpose

This contract defines what CEK-TA treats as polluted formal knowledge and how polluted items are removed from the official knowledge base.

## Formal Knowledge Scope

The official knowledge base is:

```text
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
```

The following are not official knowledge by themselves:

```text
ui/src/data/mockData.ts
ui/tests/**
codex-expert-kit/**/tests/**
docs/prototypes/**
docs/reports/**
```

They may be used for UI fallback or testing, but they must not be treated as source-of-truth professional knowledge.

## Pollution Rules

An item is polluted and must be removed from formal knowledge if any hard rule matches:

1. Its `knowledge_id`, title, statement, or source evidence declares the item as `mock`, `demo`, `fixture`, `sample`, `test-only`, `placeholder`, `fake`, or `synthetic`.
2. All source evidence is CEK-TA internal-only material such as `internal_report`, `task_card`, `runbook`, or `code_doc`, and the item is not clearly scoped as a project governance rule.
3. The item is based on UI/test artifacts, screenshots, Playwright, pytest, local fixtures, or generated mock data.
4. The item has no external professional source and is marked `approved`.
5. The item describes project implementation mechanics rather than reusable trading, RAG, MCP, LLM, integration, or governance knowledge.

## Keep Rules

An item may stay in formal knowledge if:

1. It has at least one external professional source such as official documentation, paper, exchange rule, framework documentation, recognized standards, or reputable technical documentation.
2. It is a CEK-TA governance rule with explicit project-support scope and does not claim external authority.
3. It is `reviewed` but not `approved`, has clear source gaps, and is visible as non-default guidance only.

## Output Report

Pollution scans must write:

```yaml
report_id: phase33_knowledge_pollution_scan
scanned_count: number
polluted_count: number
polluted_items:
  - knowledge_id: string
    path: string
    reasons: string[]
    action: remove_from_formal_knowledge | keep
kept_internal_items:
  - knowledge_id: string
    reasons: string[]
```

## Required Regeneration

After removal:

```text
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
```

## Boundary

Pollution cleanup does not delete candidate source files, audit packages, reports, tests, or UI fallback fixtures. It only controls what enters the official knowledge base and runtime knowledge index.

