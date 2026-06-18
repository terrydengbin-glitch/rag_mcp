# Phase 32 Candidate To Reviewed Workflow Report

## Summary

Phase 32 is complete. CEK-TA now has a repeatable workflow for moving AI-audited candidates into formal `reviewed` knowledge while preserving the boundary that `reviewed` is not `approved`.

## Delivered

1. Added workflow contract:
   - `docs/contracts/candidate_to_reviewed_workflow_contract.md`
2. Extended candidate schema:
   - `codex-expert-kit/rag/ingestion_candidate_schema.md`
3. Extended candidate and formal knowledge data:
   - 7 candidates now include `workflow.queue_group = formalized`.
   - 7 formal knowledge items now include `review.source_candidate_id`, `review.ai_audit_result_id`, `review.approval_status`, and `review.default_guidance_allowed`.
   - 11 legacy approved items were normalized with explicit `approval_status = approved` and `default_guidance_allowed = true`.
4. Updated batch import and reporting:
   - `codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py`
   - `docs/reports/phase32_candidate_ai_audit_backwrite_report.json`
5. Added quality gate:
   - `codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py`
   - `docs/reports/phase32_candidate_to_reviewed_quality_gate.json`
6. Updated Vue3 candidate UI:
   - `ui/src/views/IngestionReview.vue`
   - `ui/src/types.ts`
   - `ui/src/data/candidateAuditPackage.ts`
   - `ui/src/styles.css`
7. Rebuilt runtime data:
   - `codex-expert-kit/rag/indexes/knowledge_items.json`
   - `ui/src/data/phase23Candidates.ts`

## Workflow Result

Current candidate grouping:

```text
pending: 0
ai_passed: 0
needs_more_evidence: 0
formalized: 7
rejected: 0
```

The Vue3 candidate page now defaults to the pending queue. Since the current 7 candidates are already formalized, they appear under `已沉淀知识` and remain available for traceability, export, source review, conflict review, and formal knowledge back-link inspection.

## Boundary

Phase 32 did not create any new `approved` knowledge. The 7 imported AI-audited items are formal `reviewed` knowledge with:

```text
default_guidance_allowed = false
approval_status = not_requested
```

Existing legacy approved items remain approved, but now carry explicit approval fields.

## Validation

Executed:

```text
python codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py --dry-run
python codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py --report-path docs/reports/phase32_candidate_ai_audit_backwrite_report.json
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python -m pytest codex-expert-kit/api/tests
python -m pytest codex-expert-kit/mcp/tests
npm run build
npm run test:e2e
```

Results:

```text
Quality gate: pass, 0 failures, 0 warnings
API tests: 15 passed
MCP tests: 21 passed
Vue build: passed
Playwright: 18 passed
```

## DoD

| Item | Status |
| --- | --- |
| State machine contract exists | done |
| Candidate workflow fields exist | done |
| Formal knowledge back-links exist | done |
| Candidate UI defaults to pending queue | done |
| Formalized candidates remain visible in their own group | done |
| Batch AI audit backwrite report exists | done |
| Quality gate exists and passes | done |
| Knowledge tree/SearchLab/MCP validation passes through tests | done |
| No automatic approved promotion | done |

## Rollback

To rollback Phase 32 behavior:

1. Revert candidate `workflow` fields.
2. Revert formal knowledge `review.source_candidate_id`, `review.ai_audit_result_id`, `review.approval_status`, and `review.default_guidance_allowed` additions.
3. Rebuild `knowledge_items.json` and `phase23Candidates.ts`.
4. Restore candidate page queue filtering to the pre-Phase 32 status-based view.

