---
name: cek-ta-development-workflow
description: Follow the CEK-TA support-layer development workflow. Use when working in this repository on tasks, docs, AGENTS.md, phase task cards, knowledge schemas, Skills, MCP/RAG, Vue3 audit UI, external project integration, knowledge contribution/backflow, candidate knowledge audit, AI audit result backwrite, candidate-to-reviewed workflow, or reviewed/approved governance. Enforces reading AGENTS.md, aligning docs/index_tasks.md and docs/tasks, defining upstream/downstream contracts and boundaries, requiring DoD and tests, preserving UTF-8, and keeping candidate/reviewed/approved states distinct.
---

# CEK-TA Development Workflow

## Required First Step

Before changing this repository, read:

```text
AGENTS.md
docs/index_tasks.md
docs/tasks/README.md
```

If the work maps to a Phase, read that Phase task card from `docs/tasks/`.

## Workflow

1. Identify the Phase and task ID in `docs/index_tasks.md`.
2. Confirm the task has a task card. If missing, create or update the task card before implementation.
3. Read upstream inputs and downstream outputs from the task card.
4. Define or verify contracts before implementation:
   - document structure
   - schemas
   - API/MCP input and output
   - Vue component props/events
   - database/storage model
   - status flow
   - error handling
   - UTF-8 encoding for Chinese documents
5. Confirm boundaries: what is in scope and what is out of scope.
6. Implement the smallest change that satisfies the task.
7. Run the task's tests or document why a test cannot run.
8. Verify Definition of Done.
9. Update indexes and task statuses:
   - `docs/index_tasks.md`
   - `docs/tasks/README.md`
   - the related Phase task card
   - `README.md` if a new top-level document was added

## Candidate Knowledge Audit Workflow

Use this workflow whenever the user asks to process candidate knowledge, import AI audit results, optimize knowledge after audit, move candidates out of the pending queue, or prepare reviewed knowledge for MCP/SearchLab/knowledge tree.

1. Treat candidates as source-tracked audit artifacts, not formal default guidance.
2. Keep the lifecycle explicit:
   - `candidate_ready` / `needs_more_evidence` / `blocked`: pending audit queue.
   - `accepted_for_draft` or candidate `status.review_status = accepted`: AI/human audit passed for draft/reviewed processing.
   - formal knowledge `review.review_status = reviewed`: usable for audit/search with clear boundary, but not default approved guidance.
   - formal knowledge `review.review_status = approved`: only a later human governance task may set this.
3. For AI audit packages:
   - export only the selected/current pending scope unless the user asks for all.
   - require sources, conflict status, applicability, non-applicability, freshness, and patch notes.
   - never let external AI output directly create `approved`.
4. For AI audit result backwrite:
   - structure the audit result under `docs/audit/`.
   - update candidate `review.ai_audit` and formal knowledge `review.ai_audit`.
   - apply patch notes to the formal knowledge content, source versions, risk notes, boundaries, and open questions.
   - rebuild `knowledge_items.json` and `ui/src/data/phase23Candidates.ts`.
5. For Vue3 candidate UI:
   - default view should show pending audit candidates, not already formalized/reviewed candidates.
   - group candidates as `pending`, `ai_passed`, `needs_more_evidence`, `formalized`, and `rejected`.
   - show target `knowledge_id`, formal review status, AI audit result id, and jump links for formalized candidates.
6. For quality gates:
   - verify no source-less or unresolved-conflict item enters reviewed/approved.
   - verify reviewed knowledge is not mislabeled as approved.
   - verify MCP/SearchLab/knowledge tree read formal knowledge from the official index, not from the candidate queue.

Preferred Phase 32 order:

```text
CEK-TA-151 state machine and contract
CEK-TA-152 candidate workflow and formal knowledge back-links
CEK-TA-153 Vue3 grouped candidate queue
CEK-TA-154 batch AI audit import/backwrite report
CEK-TA-155 quality gate
CEK-TA-156 knowledge tree/SearchLab/MCP validation
CEK-TA-157 report
```

## Decision Gate

Ask the developer before:

```text
introducing a database
introducing a backend framework
changing Phase order
changing task IDs or status rules
deleting or deprecating approved rules
promoting project-private experience into general CEK-TA knowledge
accepting conflicting theory into approved knowledge
changing Vue3 information architecture
changing MCP tool permissions
adding external service dependencies
performing irreversible migrations
promoting reviewed knowledge to approved/default guidance
changing candidate/reviewed/approved status semantics
```

## DoD Gate

Do not mark a task `done` unless:

```text
deliverables exist
indexes are updated
upstream/downstream are documented
contracts are documented
boundaries are documented
tests ran or test gaps are stated
links are traceable
risks and rollback are documented when relevant
Chinese documents were read and written as UTF-8 without mojibake
```

## Output

When finishing, report:

```text
what changed
where the deliverables are
what was tested
any remaining gaps
next useful step
```
