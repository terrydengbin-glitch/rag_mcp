# Phase 48: 知识树 canonical alias 与 reviewed schema backfill 修复

## Phase 目标

Phase 48 用于承接 Phase 47 的审计发现，先修复 AI Engineering 与 Trading Engineering 知识树中缺失的 `canonical_node_id` / alias 映射，再对历史 `reviewed/caveat_only` 正式知识补齐显式权限字段。

本 Phase 的目标是让：

```text
1. 知识树、Vue3 fixture、SearchLab 和 MCP 使用一致的 canonical/alias 口径。
2. AI Engineering 与 Trading Engineering 的必备 L2/L3 节点能在前端知识树中正确展示、统计和过滤。
3. 历史 reviewed 知识明确携带 approved/default guidance/hard gate 禁用字段。
4. 不改变知识内容语义，不升级 approved，不启用 default guidance，不启用 hard gate。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-487 | P0 | done | 创建 Phase 48 任务卡、索引入口和修复契约 | `docs/tasks/phase48_tree_alias_schema_backfill.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-486 |
| CEK-TA-488 | P0 | done | 建立 canonical node / alias 修复计划 | `docs/reports/phase48_tree_alias_repair_plan.json` | CEK-TA-487 |
| CEK-TA-489 | P0 | done | 实现知识树 canonical/alias 修复脚本并重建 Vue3 知识树 fixture | `codex-expert-kit/rag/scripts/repair_phase48_tree_aliases.py`、`ui/src/data/knowledgeTreeNodes.ts`、`docs/reports/phase48_tree_alias_repair_report.json` | CEK-TA-488 |
| CEK-TA-490 | P0 | done | 运行知识树、Vue3、MCP/SearchLab 联动回归验证 | `docs/reports/phase48_tree_alias_validation_report.json` | CEK-TA-489 |
| CEK-TA-491 | P0 | done | 实现历史 reviewed schema 权限字段 backfill | `codex-expert-kit/rag/scripts/backfill_phase48_reviewed_permissions.py`、`docs/reports/phase48_reviewed_schema_backfill_report.json` | CEK-TA-490 |
| CEK-TA-492 | P0 | done | 重建正式知识索引和前端 fixture，验证无权限升级 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/formalKnowledgeItems.ts`、`docs/reports/phase48_runtime_permission_validation_report.json` | CEK-TA-491 |
| CEK-TA-493 | P1 | done | 生成 Phase 48 验收报告并更新状态 | `docs/reports/phase48_tree_alias_schema_backfill_report.md` | CEK-TA-492 |

## 上游输入

```text
docs/reports/phase47_tree_alignment_audit_report.json
docs/reports/phase47_vue3_display_alignment_report.json
docs/reports/phase47_formal_knowledge_classification_audit.json
docs/reports/phase47_alignment_findings_and_fix_plan.md
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/knowledgeTreeNodes.ts
ui/src/data/formalKnowledgeItems.ts
codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
codex-expert-kit/rag/scripts/build_knowledge_items_index.py
```

## 下游输出

```text
1. canonical node / alias 修复计划。
2. 修复后的知识树源文件或生成脚本 alias 映射。
3. 重建后的 Vue3 知识树 fixture。
4. 历史 reviewed 知识权限字段 backfill 报告。
5. 重建后的正式知识聚合索引和前端 formal fixture。
6. Phase 47/46/污染/乱码/前端 build 回归结果。
7. Phase 48 验收报告。
```

## 输入契约

Phase 48 读取的正式知识条目必须至少包含：

```text
knowledge_id
metadata.canonical_node_id
metadata.tree_node_id
metadata.partition_id
review.review_status
review.*
machine_gate.default_guidance
source_evidence
conflict_audit.conflict_status
```

知识树节点输入必须至少包含：

```text
node_id
parent_id
path
title
domain
subdomain
level
summary
review_status
coverage_status
conflict_status
item_mapping（如有）
```

Phase 47 报告输入必须至少读取：

```text
missing_required_nodes
orphan_canonical_nodes
formal reviewed 缺失 permission fields 的 finding
```

## 输出契约

`phase48_tree_alias_repair_plan.json` 必须包含：

```text
report_id
generated_at
task_id
missing_required_nodes
orphan_canonical_nodes
actions[]
status
```

每个 `actions[]` 必须包含：

```text
node_id
action_type: add_tree_node | add_alias | verify_existing
target_node_id
reason
affected_formal_item_count
```

`phase48_reviewed_schema_backfill_report.json` 必须包含：

```text
report_id
generated_at
task_id
scanned_count
reviewed_count
updated_count
skipped_approved_count
updated_items[]
status
```

`updated_items[]` 必须包含：

```text
knowledge_id
source_path
fields_added
fields_preserved
machine_gate_before
machine_gate_after
```

## 边界范围

范围内：

```text
1. 补齐知识树必备 L2/L3 节点。
2. 建立历史 canonical_node_id 到现行知识树节点的 alias 映射。
3. 修复 Vue3 知识树节点统计和过滤所需的 canonical/alias 口径。
4. 对 review_status=reviewed 且 machine_gate.default_guidance=caveat_only 的正式知识补齐显式 false 字段。
5. 重建 knowledge_items.json、formalKnowledgeItems.ts、knowledgeTreeNodes.ts。
6. 运行只读 MCP/SearchLab 同构验证和前端 build。
```

范围外：

```text
1. 不新增专业知识。
2. 不修改知识 claim、statement、procedure、source_evidence 或适用边界。
3. 不把 reviewed 升级为 approved。
4. 不启用 default guidance。
5. 不启用 hard gate。
6. 不改变 MCP tool 权限。
7. 不改变 Vue3 信息架构，只修数据源、节点和统计口径。
8. 不引入数据库或新后端框架。
9. 不删除候选或正式知识。
10. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/search_expert_knowledge.py
ui/src/data/knowledgeTreeNodes.ts
ui/src/data/formalKnowledgeItems.ts
docs/reports/
```

## 涉及数据结构

```text
KnowledgeTreeNode
FormalKnowledgeItem
ReviewGovernanceFields
MachineGate
CanonicalAliasAction
Phase48BackfillReport
```

## 涉及数据库/存储

不引入数据库，不修改存储架构。继续使用文件化 JSON 正式知识、聚合索引和 Vue3 fixture。

## 实施步骤

```text
1. 从 Phase 47 报告提取缺失必备节点、孤儿 canonical 节点和 reviewed 权限字段缺口。
2. 对 knowledge_tree.md 和 build_ui_knowledge_tree_fixture.py 的现有节点、alias 进行比对。
3. 生成 canonical node / alias 修复计划。
4. 先补知识树节点或 alias 映射，重建 knowledgeTreeNodes.ts。
5. 运行 Phase 47 审计脚本，确认 knowledge_tree/vue3_display 相关缺口下降或清零。
6. 对正式知识源 JSON 执行 reviewed 权限字段 backfill。
7. 重建 knowledge_items.json 和 formalKnowledgeItems.ts。
8. 验证 approved/default guidance/hard gate 未被意外启用。
9. 运行污染、乱码、Trading 回归、MCP/SearchLab 和 Vue3 build 验证。
10. 生成 Phase 48 验收报告并更新索引状态。
```

## Definition of Done

```text
1. Phase 48 任务卡存在并已写入 docs/index_tasks.md 和 docs/tasks/README.md。
2. canonical node / alias 修复计划存在。
3. 修复脚本存在并使用 path_resolver。
4. Vue3 知识树 fixture 已重建。
5. reviewed schema backfill 脚本存在并生成报告。
6. knowledge_items.json 和 formalKnowledgeItems.ts 已重建。
7. reviewed 条目未升级 approved/default guidance/hard gate。
8. Phase 47 审计重新执行，并记录剩余 warning。
9. UTF-8 乱码检查通过。
10. 知识污染检查通过。
11. Trading Engineering 回归通过。
12. Vue3 build 通过。
13. Phase 48 验收报告存在。
14. 任务状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/repair_phase48_tree_aliases.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
python codex-expert-kit/rag/scripts/audit_ai_trade_engineering_tree_alignment.py
python codex-expert-kit/rag/scripts/backfill_phase48_reviewed_permissions.py
python codex-expert-kit/rag/scripts/build_knowledge_items_index.py
python codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
python codex-expert-kit/rag/scripts/validate_trading_engineering_regression.py
npm --prefix ui run build
```

如已有脚本名称不同，必须在验收报告中记录实际执行命令。

## 风险与回滚

风险：

```text
1. 历史 canonical_node_id 与现行知识树存在双轨命名，直接改正式知识可能破坏审计追踪。
2. alias 映射如果过宽，可能导致前端统计重复或过滤范围过大。
3. reviewed 字段 backfill 如果误作用于 approved，可能污染已批准知识治理字段。
4. 手工修改生成文件可能导致后续重建覆盖。
```

回滚：

```text
1. 所有正式知识 JSON 改动必须由 backfill 报告列出源路径和新增字段。
2. 若 alias 修复误报，回滚 repair 脚本和 knowledge_tree.md 对应改动后重建 fixture。
3. 若 reviewed backfill 误改 approved，按报告路径恢复对应 JSON。
4. 生成文件可通过 build 脚本从源重新生成。
```

## 需要开发者确认的问题

```text
1. 若发现需要永久迁移正式知识 canonical_node_id，而不是 alias 兼容，是否另开迁移 Phase。
2. 若发现 reviewed 知识需要升级 approved/default guidance/hard gate，是否进入单独人工治理任务。
3. 若发现 Vue3 信息架构需要改变，不在本 Phase 内直接修改，需另行确认。
```
