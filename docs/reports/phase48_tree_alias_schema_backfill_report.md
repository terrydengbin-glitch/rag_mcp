# Phase 48 知识树 canonical alias 与 reviewed schema backfill 验收报告

## 总结

Phase 48 已完成。本轮先修复 AI Engineering / Trading Engineering 知识树 canonical node 与历史 alias，再对历史 `reviewed/caveat_only` 正式知识补齐显式权限字段。

本轮没有新增专业知识，没有改写知识 claim、来源、适用边界或 procedure，也没有把任何 reviewed 知识升级为 approved、default guidance 或 hard gate。

## 交付物

- `codex-expert-kit/rag/knowledge_tree_aliases.json`
- `codex-expert-kit/rag/scripts/tree_alias_contract.py`
- `codex-expert-kit/rag/scripts/repair_phase48_tree_aliases.py`
- `codex-expert-kit/rag/scripts/backfill_phase48_reviewed_permissions.py`
- `codex-expert-kit/rag/scripts/validate_phase48_runtime_permissions.py`
- `docs/reports/phase48_tree_alias_repair_plan.json`
- `docs/reports/phase48_tree_alias_repair_report.json`
- `docs/reports/phase48_tree_alias_validation_report.json`
- `docs/reports/phase48_reviewed_schema_backfill_report.json`
- `docs/reports/phase48_runtime_permission_validation_report.json`
- `codex-expert-kit/rag/indexes/knowledge_items.json`
- `ui/src/data/knowledgeTreeNodes.ts`
- `ui/src/data/formalKnowledgeItems.ts`

## 修复结果

知识树修复：

- 必需 AI/Trading 节点缺失数：`0`
- orphan canonical node 数：`0`
- Vue3 缺失 tree node 数：`0`
- MCP runtime 代表查询：通过
- default_guidance_only 泄漏：`0`

Reviewed schema backfill：

- 扫描正式知识：`479`
- reviewed/caveat_only：`469`
- 补齐显式权限字段文件：`308`
- unsafe reviewed：`0`
- approved 数量保持：`10`

## 测试

已执行并通过：

- `python codex-expert-kit/rag/scripts/repair_phase48_tree_aliases.py`
- `python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py`
- `python codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py`
- `python codex-expert-kit/rag/scripts/backfill_phase48_reviewed_permissions.py`
- `python codex-expert-kit/rag/scripts/build_knowledge_items_index.py`
- `python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py`
- `python codex-expert-kit/rag/scripts/validate_phase48_runtime_permissions.py`
- `python codex-expert-kit/rag/scripts/validate_no_mojibake.py`
- `python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py`
- `python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py`
- `python codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py`
- `npm --prefix ui run build`

Vue3 build 通过，但 Vite 仍提示 bundle chunk 大于 500 kB；这是体积优化提示，不是 Phase 48 功能阻断。

## 剩余提示

Phase47 复审仍有 4 条历史 warning，均为 K-line Strategy 知识的 `conflict_status=visible_context_no_conflict` 未被当前审计脚本视为完全通过状态。该问题不属于本轮 canonical alias 或 reviewed schema backfill 范围，未影响 MCP 检索、Vue3 展示或权限安全。

## DoD

- 任务卡、索引入口已更新。
- 知识树、Vue3 fixture、MCP/SearchLab 口径已对齐。
- reviewed 权限字段已补齐。
- 无 approved/default guidance/hard gate 意外升级。
- UTF-8/乱码检查通过。
- 污染检查通过。
- Trading Engineering 回归通过。
- Vue3 build 通过。

状态：`done`
