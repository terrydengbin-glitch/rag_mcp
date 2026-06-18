# Phase 33 Knowledge Pollution Cleanup Report

## Summary

Phase 33 cleaned the formal CEK-TA knowledge base and added a quality gate to prevent mock/demo/test/internal-only items from entering runtime knowledge.

## Cleanup Result

Formal knowledge before cleanup:

```text
18 items
```

Formal knowledge after cleanup:

```text
17 items
```

Removed polluted formal item:

```text
kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1
```

Reason:

```text
internal_only_non_governance
cek_only_non_governance
approved_without_external_professional_source
```

This item was an early seed/internal-report knowledge point. It had no external professional source and was marked approved, so it was removed from formal knowledge.

## Files Updated

```text
docs/contracts/knowledge_pollution_cleanup_contract.md
docs/tasks/phase33_knowledge_pollution_cleanup.md
codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
codex-expert-kit/rag/knowledge/KB_07_TRADE_ANALYSIS/kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/indexes/knowledge_index.json
codex-expert-kit/rag/indexes/source_index.json
codex-expert-kit/rag/indexes/conflict_index.json
codex-expert-kit/rag/eval_sets/runtime_ranking_eval_cases.json
codex-expert-kit/mcp/tests/test_seed_runtime_validation.py
ui/src/data/formalKnowledgeItems.ts
```

## Boundary

UI fallback fixtures and historical reports were not treated as formal knowledge. The official runtime knowledge path is:

```text
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/formalKnowledgeItems.ts
```

## Validation

Executed:

```text
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python -m pytest codex-expert-kit/api/tests codex-expert-kit/mcp/tests
npm run build
npm run test:e2e
```

Results:

```text
Knowledge pollution gate: pass, 0 polluted items
Candidate to reviewed gate: pass, 0 failures
API + MCP tests: 36 passed
Vue build: passed
Playwright: 18 passed
```

Additional check:

```text
kb_07_trade_analysis.bad_trade_taxonomy.root_cause_separation.v1
```

No longer appears in:

```text
codex-expert-kit/rag/knowledge
codex-expert-kit/rag/indexes
codex-expert-kit/rag/eval_sets
ui/src/data/formalKnowledgeItems.ts
codex-expert-kit/mcp/tests
```

## DoD

| Item | Status |
| --- | --- |
| Pollution contract exists | done |
| Scan report exists | done |
| Polluted item removed | done |
| Official indexes rebuilt | done |
| Vue3 formal fixture rebuilt | done |
| Pollution gate passes | done |
| Candidate/reviewed workflow gate still passes | done |
| API/MCP/Vue/Playwright validation passes | done |

