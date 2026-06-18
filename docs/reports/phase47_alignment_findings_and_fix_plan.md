# Phase 47 AI/Trading Engineering 对齐审计问题清单与修复建议

## 总结

- 生成时间：2026-06-12T15:41:53+00:00
- 问题总数：4
- error：0
- warning：4

本报告只记录审计发现，不直接修改知识本体、不升级 approved、不启用 default guidance 或 hard gate。

## 子报告

- `phase47_tree_alignment_audit`：`pass`
- `phase47_formal_knowledge_classification_audit`：`warning`
- `phase47_candidate_formal_linkage_audit`：`pass`
- `phase47_vue3_display_alignment`：`pass`
- `phase47_mcp_runtime_alignment`：`pass`

## 发现项

### PH47-001 `warning` formal_knowledge

- 对象：`kb_02_kline_strategy.stop_loss_requires_invalidation_logic.v1`
- 预期：Reviewed/approved formal knowledge should have none/resolved conflict status.
- 实际：conflict_status=visible_context_no_conflict
- 影响：检索时需要人工关注潜在冲突。
- 建议修复：补冲突审计结论或降级为 draft/needs review。
- 归属：Phase 16/47

### PH47-002 `warning` formal_knowledge

- 对象：`kb_02_kline_strategy.strategy_rule_version_required.v1`
- 预期：Reviewed/approved formal knowledge should have none/resolved conflict status.
- 实际：conflict_status=visible_context_no_conflict
- 影响：检索时需要人工关注潜在冲突。
- 建议修复：补冲突审计结论或降级为 draft/needs review。
- 归属：Phase 16/47

### PH47-003 `warning` formal_knowledge

- 对象：`kb_02_kline_strategy.take_profit_requires_reachability_check.v1`
- 预期：Reviewed/approved formal knowledge should have none/resolved conflict status.
- 实际：conflict_status=visible_context_no_conflict
- 影响：检索时需要人工关注潜在冲突。
- 建议修复：补冲突审计结论或降级为 draft/needs review。
- 归属：Phase 16/47

### PH47-004 `warning` formal_knowledge

- 对象：`kb_02_kline_strategy.volume_confirmation_boundary.v1`
- 预期：Reviewed/approved formal knowledge should have none/resolved conflict status.
- 实际：conflict_status=visible_context_no_conflict
- 影响：检索时需要人工关注潜在冲突。
- 建议修复：补冲突审计结论或降级为 draft/needs review。
- 归属：Phase 16/47

