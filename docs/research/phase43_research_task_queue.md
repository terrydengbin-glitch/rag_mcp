# Phase 43 ResearchIngestionTask Queue

## 队列规则

```text
1. 所有任务先生成 candidate，不直接生成 formal knowledge。
2. 每条候选必须至少 3 个来源方向，且至少 1 个为官方文档、论文、安全组织资料或数据库官方资料。
3. 所有候选必须写明适用边界、不适用场景、冲突审计和 LLM 使用限制。
4. 所有候选默认 reviewed_allowed=false，等待外部审计。
5. 禁止创建 approved/default guidance/hard gate。
```

| task_id | topic_id | priority | status | source_focus |
| --- | --- | --- | --- | --- |
| P43-RIT-001 | P43-P0-001 | P0 | planned | RAG knowledge vs project memory boundary |
| P43-RIT-002 | P43-P0-002 | P0 | planned | knowledge contamination and private project memory boundary |
| P43-RIT-003 | P43-P0-003 | P0 | planned | memory contract ownership and data privacy |
| P43-RIT-004 | P43-P0-004 | P0 | planned | CEK-TA MCP plus Project Memory MCP retrieval protocol |
| P43-RIT-005 | P43-P0-005 | P0 | planned | memory types and compact schema design |
| P43-RIT-006 | P43-P0-006 | P0 | planned | process event log vs long-term memory |
| P43-RIT-007 | P43-P0-007 | P0 | planned | future plan as task lifecycle |
| P43-RIT-008 | P43-P0-008 | P0 | planned | error as lesson and postmortem fields |
| P43-RIT-009 | P43-P0-009 | P0 | planned | memory source provenance, hash, trust, write origin |
| P43-RIT-010 | P43-P0-010 | P0 | planned | memory supersede and versioning |
| P43-RIT-011 | P43-P0-011 | P0 | planned | deprecated memory retrieval boundary |
| P43-RIT-012 | P43-P0-012 | P0 | planned | AI propose-only write governance |
| P43-RIT-013 | P43-P0-013 | P0 | planned | source, secret, injection, poisoning, visibility, conflict checks |
| P43-RIT-014 | P43-P0-014 | P0 | planned | data minimization and no auto-save-all-chat |
| P43-RIT-015 | P43-P0-015 | P0 | planned | long-term memory whitelist |
| P43-RIT-016 | P43-P0-016 | P0 | planned | long-term memory blacklist |
| P43-RIT-017 | P43-P0-017 | P0 | planned | Project Memory MCP/API minimal permission contract |
| P43-RIT-018 | P43-P0-018 | P0 | planned | memory retention, deletion, export, privacy minimization |
| P43-RIT-019 | P43-P0-019 | P0 | planned | memory conflict resolution contract |
| P43-RIT-020 | P43-P0-020 | P0 | planned | prompt injection and memory poisoning |
| P43-RIT-021 | P43-P0-021 | P0 | planned | rollback and integrity check |
| P43-RIT-022 | P43-P0-022 | P0 | planned | PostgreSQL JSONB canonical memory store |
| P43-RIT-023 | P43-P0E-001 | P0E | planned | project scoped retrieval and token budget |
| P43-RIT-024 | P43-P0E-002 | P0E | planned | default memory injection scope |
| P43-RIT-025 | P43-P0E-003 | P0E | planned | explicit retrieval for logs and audit history |
| P43-RIT-026 | P43-P0E-004 | P0E | planned | memory quality regression tests |
| P43-RIT-027 | P43-P1-001 | P1 | planned | third-party memory engine adapter boundary |
| P43-RIT-028 | P43-P1-002 | P1 | planned | pgvector optional semantic index |
| P43-RIT-029 | P43-P1-003 | P1 | planned | adapter portability test |
