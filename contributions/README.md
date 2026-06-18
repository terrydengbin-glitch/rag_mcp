# CEK-TA Contributions Queue

This directory is the file-based queue for knowledge contribution tasks from business projects.

## Status Folders

Runtime folders:

```text
proposed/
sanitized/
sourced/
classified/
conflict_checked/
reviewed/
accepted/
rejected/
needs_more_evidence/
```

External projects must submit new files to:

```text
contributions/proposed/
```

## Rules

```text
1. Do not place secrets, account data, raw orders, or private logs here.
2. Contributions must start as proposed.
3. Accepted contributions must reference source evidence and conflict checks.
4. Rejected contributions should keep rejection reason for audit.
5. Do not manually promote a contribution to approved CEK-TA knowledge without review.
6. Moving a file between status folders means the review status changed and must be recorded in the contribution file.
```

Use:

```text
codex-expert-kit/templates/contribution_from_project.md
codex-expert-kit/templates/knowledge_contribution_task.md
codex-expert-kit/rag/contribution_schema.md
codex-expert-kit/rag/sanitization_rules.md
```

## Runtime Flow

```text
external project
  -> create contribution_from_project.md
  -> sanitize private data
  -> submit to contributions/proposed/
  -> CEK-TA review moves it through the status folders
  -> accepted contributions can generate approved knowledge only after review
```
