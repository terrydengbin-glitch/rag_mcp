# Phase 55: MCP/SearchLab/Vue3 全链路运行时验收与知识库基线

## Phase 目标

Phase 55 用于在 Phase 54 完成历史 schema 和候选回链回填之后，对当前正式知识库做一次全链路运行时验收和基线固化。

本 Phase 的目标是确认：

```text
1. 正式知识索引、候选 fixture、知识树 fixture 与 Vue3 页面使用同一批可追踪数据。
2. MCP 只读工具可以查询正式知识、返回来源、返回 machine gate，并阻断写权限。
3. SearchLab 等价检索场景能命中 AI Engineering 与 Trading Engineering 关键知识。
4. Vue3 KnowledgeTree 和候选页能读取当前 fixture，统计口径不再明显漂移。
5. reviewed / approved / caveat_only / default guidance / hard gate 语义仍保持隔离。
6. 输出一份当前知识库基线报告，作为后续继续扩充知识库的对照点。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 | 依赖 |
| --- | --- | --- | --- | --- | --- |
| CEK-TA-534 | P0 | done | 创建 Phase 55 任务卡、索引入口和运行时验收契约 | `docs/tasks/phase55_runtime_acceptance_baseline.md`、`docs/index_tasks.md`、`docs/tasks/README.md` | CEK-TA-533 |
| CEK-TA-535 | P0 | done | 生成正式知识库基线统计报告 | `docs/reports/phase55_knowledge_base_baseline_report.json` | CEK-TA-534 |
| CEK-TA-536 | P0 | done | 验证 MCP 只读查询、来源返回和权限阻断 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-535 |
| CEK-TA-537 | P0 | done | 验证 SearchLab 等价检索命中 AI/Trading 关键知识 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-536 |
| CEK-TA-538 | P0 | done | 验证 Vue3 KnowledgeTree、候选页和 fixture 数据一致性 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-537 |
| CEK-TA-539 | P0 | done | 验证 reviewed/approved/default guidance/hard gate 语义一致性 | `docs/reports/phase55_runtime_acceptance_report.json` | CEK-TA-538 |
| CEK-TA-540 | P1 | done | 生成 Phase 55 验收报告并更新任务状态 | `docs/reports/phase55_runtime_acceptance_baseline_report.md` | CEK-TA-539 |

## 上游输入

```text
docs/reports/phase54_historical_reviewed_schema_workflow_backfill_report.md
docs/reports/phase54_validation_report.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge/**/*.json
codex-expert-kit/rag/candidates/**/*.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/phase23Candidates.json
ui/public/data/knowledgeTreeNodes.json
codex-expert-kit/mcp/search_expert_knowledge.py
codex-expert-kit/mcp/get_knowledge_item.py
codex-expert-kit/mcp/browse_knowledge_tree.py
```

## 下游输出

```text
1. 当前正式知识库基线统计报告。
2. MCP/SearchLab/Vue3 运行时验收 JSON 报告。
3. Phase 55 人类可读验收报告。
4. 更新后的 docs/index_tasks.md、docs/tasks/README.md 和本任务卡状态。
```

## 输入契约

### 正式知识索引

`knowledge_items.json` 必须包含：

```text
items[]
items[].knowledge_id
items[].metadata.partition_id
items[].metadata.canonical_node_id
items[].metadata.domain
items[].metadata.subdomain
items[].review.review_status
items[].review.default_guidance_allowed
items[].review.approved_allowed
items[].review.hard_gate_allowed
items[].machine_gate.default_guidance
items[].source_evidence[]
items[].conflict_audit.conflict_status
```

### 候选 Fixture

`phase23Candidates.json` 必须包含：

```text
items[]
items[].candidate_id
items[].review_status
items[].workflow.queue_group
items[].workflow.formal_knowledge_id
items[].workflow.formal_review_status
```

### MCP Tool 契约

只读工具必须保持：

```text
search_expert_knowledge(request) -> results[] / blocked_results[] / warnings[] / errors[]
get_knowledge_item(request) -> item / errors[]
browse_knowledge_tree(request) -> nodes[] / errors[]
```

返回结果必须带：

```text
knowledge_id
source_refs 或 source/citation
review_status
conflict_status
machine_gate
acceptance_level
recommended_next_action
```

## 输出契约

### `phase55_knowledge_base_baseline_report.json`

必须包含：

```text
report_id
generated_at
task_id
knowledge_totals
review_status_counts
machine_gate_counts
domain_counts
partition_counts
l1_counts
l2_counts
l3_counts
source_quality_summary
candidate_totals
candidate_queue_counts
top_nodes_by_knowledge_count
warnings
gate_status
```

### `phase55_runtime_acceptance_report.json`

必须包含：

```text
report_id
generated_at
task_id
mcp_tests
searchlab_tests
vue_fixture_tests
permission_tests
governance_tests
errors
warnings
gate_status
```

## 边界范围

范围内：

```text
1. 读取正式知识索引和 Vue3 fixture 做统计。
2. 调用现有 MCP Python tool 做只读 smoke test。
3. 用固定 query 验证 AI Engineering、Trading Engineering、RAG、MCP、Trade Analysis 等关键路径。
4. 验证 default_guidance_only 不会返回 caveat_only reviewed 知识。
5. 验证 forbidden permissions 会被 MCP tool 阻断。
6. 运行现有 schema/workflow/乱码/知识树/前端构建/Playwright smoke 测试。
7. 输出报告并更新任务状态。
```

范围外：

```text
1. 不新增专业知识。
2. 不修改知识 claim、来源、适用边界。
3. 不把 reviewed 升级 approved。
4. 不启用 default guidance。
5. 不启用 hard gate。
6. 不改变 MCP tool 权限。
7. 不改变 Vue3 信息架构。
8. 不引入数据库、新后端框架或外部服务依赖。
9. 不生成买卖点、仓位、杠杆、止损止盈、风险阈值或实盘执行建议。
```

## 涉及组件

```text
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/scripts/
codex-expert-kit/mcp/
ui/public/data/
ui/tests/e2e/
docs/reports/
docs/index_tasks.md
docs/tasks/README.md
```

## 涉及数据结构

```text
KnowledgeItem schema v1.1
CandidateWorkflow
MCPSearchResponse
MCPGetKnowledgeItemResponse
KnowledgeTreeNode
Phase55BaselineReport
Phase55RuntimeAcceptanceReport
```

## 涉及数据库/存储

不引入数据库，不改变存储架构。继续使用文件化 JSON 正式知识、候选 JSON、聚合索引和 Vue3 fixture。

## 实施步骤

```text
1. 创建 Phase 55 任务卡并更新索引入口。
2. 实现 Phase 55 基线与运行时验收脚本。
3. 运行脚本生成 baseline 和 runtime acceptance 报告。
4. 运行 schema/workflow/乱码/知识树/污染门禁。
5. 运行 npm build 和 Vue3 Playwright smoke 测试。
6. 生成 Phase 55 验收报告。
7. 更新任务卡、docs/index_tasks.md 和 docs/tasks/README.md 状态。
```

## Definition of Done

```text
1. Phase 55 任务卡存在并写入 docs/index_tasks.md 和 docs/tasks/README.md。
2. phase55_knowledge_base_baseline_report.json 存在。
3. phase55_runtime_acceptance_report.json 存在且 gate_status=pass。
4. MCP search/get/browse smoke test 通过。
5. MCP forbidden permission 阻断测试通过。
6. SearchLab 等价检索命中 AI/Trading 关键知识并返回来源。
7. Vue3 fixture 与正式索引数量和关键 ID 对齐。
8. reviewed/caveat_only 没有被错误暴露为 approved/default/hard gate。
9. schema/workflow/乱码/知识树/污染门禁通过。
10. npm --prefix ui run build 通过。
11. 关键 Playwright smoke test 通过。
12. Phase 55 验收报告存在。
13. 任务状态已更新。
```

## 测试与验收

必须执行：

```text
python codex-expert-kit/rag/scripts/validate_phase55_runtime_acceptance.py
python codex-expert-kit/rag/scripts/validate_knowledge_item_schema_v1_1.py
python codex-expert-kit/rag/scripts/validate_candidate_to_reviewed_workflow.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_knowledge_pollution.py
npm --prefix ui run build
npx playwright test tests/e2e/audit-workbench.spec.ts tests/e2e/knowledge-tree-performance.spec.ts
```

如 Playwright 因本机服务未启动或端口冲突失败，必须记录失败原因和可复跑命令，不得静默标记前端实机验收通过。

## 风险与回滚

风险：

```text
1. MCP 轻量 lexical search 不是最终向量检索，搜索命中只能作为运行时 smoke test。
2. Vue3 fixture 可能与正式索引生成时点不一致。
3. Playwright 依赖本机前端服务，可能受端口或缓存影响。
```

回滚：

```text
1. Phase 55 只新增报告和只读脚本，不改知识语义，可直接删除报告重新生成。
2. 如果发现 fixture 不一致，回滚路径是重建正式知识索引和 UI fixture。
3. 如果发现 MCP 权限异常，不在本 Phase 直接改权限，另开 MCP 权限修复任务。
```

## 需要开发者确认的问题

```text
1. 若 Phase 55 发现需要改变 MCP tool 权限，需要另行确认。
2. 若 Phase 55 发现需要改变 Vue3 信息架构，需要另行确认。
3. 若 Phase 55 发现 reviewed 知识应升级 approved/default guidance/hard gate，不在本 Phase 内处理，必须另开人工审批任务。
```
