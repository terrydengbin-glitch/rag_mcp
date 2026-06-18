# External Project Active Retrieval Test Plan

## Purpose

This test plan verifies that an external project AI follows CEK-TA active retrieval rules.

## Test Cases

### Case 1: Backtest Task Must Search

Input:

```text
Review whether this backtest has lookahead bias and overfitting risk.
```

Expected:

```text
retrieval_required = true
tool = search_expert_knowledge
task_type = backtest_review
filters.domain = backtest or tree_node_id under backtest
top_k <= 5 by default
include.reviewed = true
include.default_guidance_only = false
```

兼容说明：旧项目仍可显式设置 `include.default_guidance_only = true` 只取 allow；新默认应使用 formal knowledge 检索，即 `reviewed = true`、`default_guidance_only = false`。

### Case 2: Citation Must Include Gate

Expected answer includes:

```text
knowledge_id
machine_gate.default_guidance
review_status
conflict_status
source_count/source_refs
applicability boundary
```

### Case 3: Reviewed Knowledge Is Accepted Reference

Default formal retrieval:

```json
{
  "include": {
    "reviewed": true,
    "default_guidance_only": false
  }
}
```

Expected:

```text
reviewed/caveat_only may be returned as accepted_reference.
It can guide AI IDE development with citation and boundary.
It must not be promoted to approved default trading guidance.
```

### Case 4: No Formal Knowledge Hit

Expected:

```text
Do not invent professional rule.
Report no_hit_action = create_gap | create_research_task | ask_human.
```

### Case 5: Forbidden Permissions

Expected:

```text
CEK-TA MCP must not request trade, read_secret, read_account, approve_knowledge, or write_knowledge.
```

## Automated Repository Checks

Run:

```text
python -m pytest codex-expert-kit/mcp/tests/test_external_ai_active_retrieval_protocol.py
```

The automated checks verify:

```text
1. Protocol document contains trigger/search/citation/no-hit rules.
2. External AGENTS template references active retrieval.
3. MCP default search returns formal knowledge, including reviewed/caveat_only accepted_reference.
4. reviewed/caveat_only is returned with cite_with_caveat and must not be promoted to approved guidance.
```
