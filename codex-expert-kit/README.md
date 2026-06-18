# Codex Expert Kit

This directory contains the reusable CEK-TA capability package.

It is intentionally separated from project-level docs:

```text
docs/
  Project management, requirements, task cards, and governance documents.

codex-expert-kit/
  Reusable Codex expert rules, domains, skills, templates, RAG schemas, MCP tools, and install scripts.
```

Current completed capability layers:

```text
Phase 1: expert kit skeleton.
Phase 2: RAG knowledge partitions, metadata schema, chunking rules, retrieval policy.
Phase 2.5: knowledge item schema, conflict detection rules, source quality rules, research task template.
Phase 3: Knowledge MCP server spec and dependency-free draft tools.
Phase 4: unified trading interface, ExecutionAdapter, and FillModel contracts.
Phase 5: trade result schema, bad trade taxonomy, and trade-quality analyst skill.
Phase 6: LLM training domain, dataset/eval templates, and training workflow skills.
Phase 7: Vue3 audit UI in `../ui/`.
Phase 8: external project AGENTS, adapter, and MCP config templates.
Phase 9: knowledge contribution task, contribution schema, sanitization rules, and contribution queue.
```

Do not place project-specific facts here. Business projects must keep their facts in their own repositories and connect to CEK-TA through adapters, AGENTS.md, Skills, MCP/RAG, or Plugin packaging.

Key RAG and audit contracts:

- [rag/kb_partitions.md](./rag/kb_partitions.md)
- [rag/metadata_schema.md](./rag/metadata_schema.md)
- [rag/chunking_rules.md](./rag/chunking_rules.md)
- [rag/retrieval_policy.md](./rag/retrieval_policy.md)
- [rag/knowledge_item_schema.md](./rag/knowledge_item_schema.md)
- [rag/conflict_detection_rules.md](./rag/conflict_detection_rules.md)
- [rag/source_quality_rules.md](./rag/source_quality_rules.md)
- [templates/research_task_card.md](./templates/research_task_card.md)
- [mcp/mcp_server_spec.md](./mcp/mcp_server_spec.md)
- [mcp/search_expert_knowledge.py](./mcp/search_expert_knowledge.py)
- [mcp/get_knowledge_item.py](./mcp/get_knowledge_item.py)
- [mcp/get_conflict_audit.py](./mcp/get_conflict_audit.py)
- [mcp/get_source_profile.py](./mcp/get_source_profile.py)
- [mcp/list_kb_partitions.py](./mcp/list_kb_partitions.py)
- [templates/interface_contract.md](./templates/interface_contract.md)
- [templates/execution_adapter_spec.md](./templates/execution_adapter_spec.md)
- [templates/fill_model_spec.md](./templates/fill_model_spec.md)
- [templates/trade_result_schema.md](./templates/trade_result_schema.md)
- [domains/trade_analysis/knowledge/bad_trade_taxonomy.md](./domains/trade_analysis/knowledge/bad_trade_taxonomy.md)
- [skills/trade-quality-analyst/SKILL.md](./skills/trade-quality-analyst/SKILL.md)
- [domains/llm_training/README.md](./domains/llm_training/README.md)
- [templates/dataset_card.md](./templates/dataset_card.md)
- [templates/eval_report.md](./templates/eval_report.md)
- [skills/llm-data-curator/SKILL.md](./skills/llm-data-curator/SKILL.md)
- [skills/sft-engineer/SKILL.md](./skills/sft-engineer/SKILL.md)
- [skills/eval-engineer/SKILL.md](./skills/eval-engineer/SKILL.md)
- [templates/external_project_AGENTS.md](./templates/external_project_AGENTS.md)
- [templates/project_adapter.md](./templates/project_adapter.md)
- [templates/codex_config_mcp.toml](./templates/codex_config_mcp.toml)
- [templates/knowledge_contribution_task.md](./templates/knowledge_contribution_task.md)
- [rag/contribution_schema.md](./rag/contribution_schema.md)
- [rag/sanitization_rules.md](./rag/sanitization_rules.md)
