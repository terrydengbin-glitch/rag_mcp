# Candidate To Reviewed Workflow Contract

## Purpose

This contract defines the repeatable CEK-TA workflow for moving audited candidate knowledge into formal `reviewed` knowledge while keeping `reviewed` separate from `approved`.

The workflow supports:

1. candidate queue grouping in Vue3;
2. AI audit result import and backwrite;
3. formal knowledge back-links to candidate and AI audit result;
4. quality gates before rebuilding indexes;
5. runtime validation through knowledge tree, SearchLab, and MCP.

## State Machine

Candidate workflow states:

| stage | queue_group | Meaning | Next action |
| --- | --- | --- | --- |
| `pending_review` | `pending` | Candidate still needs audit. | `export_ai_audit` |
| `ai_audited` | `ai_passed` | AI audit accepted the candidate, but formal knowledge is not reviewed yet. | `apply_ai_audit_patch` or `review_formal_knowledge` |
| `needs_more_evidence` | `needs_more_evidence` | Candidate cannot move forward until sources, scope, classification, or conflict review are fixed. | `export_ai_audit` |
| `rejected` | `rejected` | Candidate is not suitable for CEK-TA reuse. | `none` |
| `formalized_reviewed` | `formalized` | Candidate is linked to formal knowledge with `review.review_status = reviewed`. | `request_human_approval` |
| `approval_requested` | `formalized` | Formal knowledge is reviewed and waiting for explicit human approval. | `request_human_approval` |
| `approved` | `formalized` | Formal knowledge was explicitly approved by a later governance task. | `none` |

Hard boundary:

```text
accepted_for_draft != approved
reviewed != approved
Only a later human governance task may set approved/default guidance.
```

## Candidate Schema Extension

Every generated candidate fixture must expose:

```yaml
workflow:
  stage: pending_review | ai_audited | needs_more_evidence | rejected | formalized_reviewed | approval_requested | approved
  queue_group: pending | ai_passed | needs_more_evidence | formalized | rejected
  formal_knowledge_id: string | null
  formal_review_status: draft | reviewed | approved | rejected | deprecated | null
  ai_audit_result_id: string | null
  hidden_from_default_queue: boolean
  next_action: export_ai_audit | apply_ai_audit_patch | review_formal_knowledge | request_human_approval | none
```

Default queue rule:

```text
Vue3 candidate page defaults to workflow.queue_group = pending.
Formalized/reviewed candidates remain visible in the formalized group and all group.
Tree-filtered candidate links may show non-pending candidates to preserve traceability.
```

## Formal Knowledge Back-Link Extension

Formal knowledge `review` must include:

```yaml
review:
  source_candidate_id: string | null
  ai_audit_result_id: string | null
  approval_status: not_requested | requested | approved | rejected
  default_guidance_allowed: boolean
```

Rules:

1. `source_candidate_id` must point to the candidate JSON that produced or refined the item.
2. `ai_audit_result_id` must point to the imported audit result.
3. `default_guidance_allowed` may be true only when `review_status = approved` and `approval_status = approved`.
4. Phase 32 import scripts must not set `review_status = approved`.

## Batch AI Audit Import

The import script must:

1. read a structured AI audit result from `docs/audit/`;
2. update candidate `review.ai_audit`;
3. update candidate `workflow`;
4. update formal knowledge `review.ai_audit`;
5. update formal knowledge back-links;
6. write a machine-readable backwrite report under `docs/reports/`;
7. never delete candidate source files;
8. never promote reviewed knowledge to approved.

## Quality Gate

The Phase 32 quality gate fails if:

1. a candidate has no normalized `workflow`;
2. `workflow.queue_group = formalized` but no formal knowledge back-link exists;
3. formal reviewed knowledge has no `source_candidate_id`;
4. formal reviewed knowledge has no `ai_audit_result_id`;
5. any reviewed or approved knowledge has no source evidence;
6. any reviewed or approved knowledge has unresolved `confirmed` or `unchecked` conflict;
7. any reviewed item has `default_guidance_allowed = true`;
8. any item becomes `approved` without `approval_status = approved`.

## Runtime Read Boundary

Knowledge tree, SearchLab, and MCP read from the formal knowledge index:

```text
codex-expert-kit/rag/indexes/knowledge_items.json
```

They do not treat the candidate queue as default knowledge. Candidate data is only used for audit traceability, review grouping, and source back-links.

## Downstream Consumers

| Consumer | Reads | Writes | Boundary |
| --- | --- | --- | --- |
| Vue3 candidate page | `phase23Candidates.ts` | none | Shows queue groups and export packages only. |
| Vue3 knowledge tree | formal index plus candidate counts | none | Links to candidate traceability. |
| SearchLab | formal index | none | May show `reviewed`; must not label it `approved`. |
| MCP | formal index | none | Read-only retrieval only. |
| AI audit import script | audit result, candidates, formal knowledge | candidate/formal JSON and report | No approved promotion. |

