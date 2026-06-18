# Phase 39: 知识树单一数据源与统计对齐

## Phase 目标

修复知识树在 MCP、FastAPI、Vue3 和正式知识索引之间的节点漂移问题，让 `codex-expert-kit/rag/knowledge_tree.md` 成为知识树唯一结构源，并让前端显示的 L1/L2/L3 节点、正式知识数、候选知识数、来源数、缺口数和冲突数都来自同一套可验证统计口径。

本 Phase 不新增专业知识，不改变 candidate/reviewed/approved 状态，不把 reviewed 自动升级 approved。核心是让已经沉淀的知识能被正确挂载、正确统计、正确展示。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-291 | P0 | done | 创建 Phase 39 任务卡并登记索引 | `docs/tasks/phase39_knowledge_tree_single_source_stats_alignment.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-292 | P0 | done | 将 FastAPI 知识树节点源切换为 `knowledge_tree.md` 解析结果 | `codex-expert-kit/api/codex_expert_kit_api/services.py`、`codex-expert-kit/api/tests/` |
| CEK-TA-293 | P0 | done | 统一知识节点归类匹配和 legacy alias 兼容 | `codex-expert-kit/api/codex_expert_kit_api/services.py`、`ui/src/stores/auditStore.ts` |
| CEK-TA-294 | P0 | done | 生成 Vue3 知识树 fixture，替代手写静态节点 | `codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py`、`ui/src/data/knowledgeTreeNodes.ts` |
| CEK-TA-295 | P0 | done | 修复 Vue3 知识树统计口径和目录数字显示 | `ui/src/stores/auditStore.ts`、`ui/src/views/KnowledgeTreeView.vue` |
| CEK-TA-296 | P0 | done | 增加知识树覆盖与统计一致性验证脚本 | `codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py`、`docs/reports/phase39_knowledge_tree_alignment_report.json` |
| CEK-TA-297 | P1 | done | 运行 FastAPI、Vue3 build 和知识树对齐验收 | `codex-expert-kit/api/tests/`、`ui` build、验收报告 |
| CEK-TA-401 | P0 | done | 修复 Trading Engineering 下 Data Engineering L2 节点缺失和错误 alias，确保 Data Engineering 知识显示在 Trading Engineering 子页面 | `codex-expert-kit/rag/knowledge_tree.md`、`codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py`、`codex-expert-kit/api/codex_expert_kit_api/services.py`、`ui/src/stores/auditStore.ts`、`ui/src/data/knowledgeTreeNodes.ts` |

## 上游输入

```text
1. codex-expert-kit/rag/knowledge_tree.md
2. codex-expert-kit/rag/indexes/knowledge_items.json
3. codex-expert-kit/rag/candidates/**/*.json
4. ui/src/data/formalKnowledgeItems.ts
5. ui/src/data/phase23Candidates.ts
6. ui/src/data/mockData.ts
7. ui/src/stores/auditStore.ts
8. ui/src/views/KnowledgeTreeView.vue
9. codex-expert-kit/api/codex_expert_kit_api/services.py
10. codex-expert-kit/mcp/browse_knowledge_tree.py
11. docs/tasks/phase28_knowledge_tree_vue_fastapi_delivery.md
12. docs/tasks/phase38_ai_model_platform_poc_knowledge.md
```

## 下游输出

```text
1. Vue3 知识树页面显示完整 L1/L2/L3 节点。
2. FastAPI children、knowledge、audit-summary 与 MCP knowledge_tree.md 节点一致。
3. 知识树每个节点的正式知识数按 reviewed + approved 真实计算。
4. 候选知识数按候选 workflow 分组真实计算。
5. Phase 36/38 旧节点和新增节点都能被知识树承接。
6. SearchLab、候选页、知识树页使用同一个 canonical node 口径。
```

## 输入契约

### KnowledgeTree Source

```text
primary_source: codex-expert-kit/rag/knowledge_tree.md
encoding: UTF-8
node_id: string
parent_id: string | null
path: string
title: string
domain: string
subdomain: string
level: 0 | 1 | 2 | 3
summary: string
coverage_status: empty | partial | covered | overgrown
review_status: draft | reviewed | approved | needs_review | deprecated
freshness_status: stable | time_sensitive | stale | deprecated
conflict_status: none | potential | confirmed | resolved | unchecked
```

### Formal Knowledge Count

```text
formal_knowledge_count = reviewed_count + approved_count + draft_count
default_visible_formal_count = reviewed_count + approved_count
approved_count = review.review_status == approved
reviewed_count = review.review_status == reviewed
draft_count = review.review_status == draft
source_count = sum(source_evidence)
conflict_count = conflict_status not in [none, resolved]
```

### Candidate Count

```text
candidate_count = all candidates in current node scope
pending_count = workflow.queue_group in [pending, needs_more_evidence, ai_passed]
formalized_candidate_count = workflow.queue_group == formalized
rejected_candidate_count = workflow.queue_group == rejected
accepted_for_draft 不等于 approved
formalized candidate 不等于新增正式知识，正式知识仍以 knowledge_items.json 为准
```

## 输出契约

### FastAPI KnowledgeTreeNode

```text
id: string
canonical_node_id: string
node_id: string
parent_id: string | null
level: number
title: string
subtitle: string
summary: string
path: string
domain: string
subdomain: string
children_count: number
knowledge_count: number
approved_item_count: number
reviewed_item_count: number
candidate_count: number
source_count: number
open_gap_count: number
coverage_status: string
review_status: string
freshness_status: string
conflict_status: string
aliases: string[]
sort_order: number
```

### Vue3 KnowledgeTreeNode

```text
node_id: string
parent_id: string | null
path: string
title: string
domain: string
subdomain: string
level: number
summary: string
coverage_status: string
review_status: string
freshness_status: string
conflict_status: string
approved_item_count: number
reviewed_item_count: number
source_count: number
open_gaps: string[]
related_nodes: string[]
```

### 验证报告

```text
tree_node_count
api_node_count
ui_node_count
formal_knowledge_count
candidate_count
formal_uncovered_count
candidate_uncovered_count
node_count_mismatches
status: pass | fail
errors: string[]
```

## 边界范围

范围内：

```text
1. 统一知识树结构源。
2. 修复 FastAPI 节点解析、children、descendants、filter_items、audit-summary。
3. 修复 Vue3 知识树 fixture 和统计口径。
4. 增加覆盖验证脚本。
5. 运行 API 测试、Vue3 build 和 UTF-8/乱码检查。
```

范围外：

```text
1. 不新增专业知识。
2. 不改变候选知识审计结论。
3. 不把 reviewed 或 accepted_for_draft 升级为 approved。
4. 不引入数据库。
5. 不改变 MCP tool 权限。
6. 不改变知识树信息架构，只统一现有结构源和统计。
```

## 涉及组件

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/scripts/
codex-expert-kit/api/codex_expert_kit_api/services.py
codex-expert-kit/api/codex_expert_kit_api/main.py
codex-expert-kit/api/tests/
ui/src/data/knowledgeTreeNodes.ts
ui/src/data/formalKnowledgeItems.ts
ui/src/data/phase23Candidates.ts
ui/src/stores/auditStore.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/types.ts
```

## 涉及存储

```text
1. 知识树结构：codex-expert-kit/rag/knowledge_tree.md
2. 正式知识索引：codex-expert-kit/rag/indexes/knowledge_items.json
3. 候选知识源：codex-expert-kit/rag/candidates/**/*.json
4. Vue3 生成 fixture：ui/src/data/knowledgeTreeNodes.ts
```

## 实施步骤

```text
1. 创建 Phase 39 任务卡并更新索引。
2. 在 FastAPI services 中解析 knowledge_tree.md，生成节点 view model。
3. 用同一套 descendants 和 node matching 逻辑过滤正式知识。
4. 用候选目录统计 candidate_count。
5. 增加 Vue3 知识树 fixture 生成脚本。
6. 将 auditStore 的 knowledgeTreeNodes 来源切换为生成 fixture。
7. 修复 Vue3 左侧目录和右侧摘要统计，避免使用静态 approved_item_count 代替真实正式知识数。
8. 增加 validate_knowledge_tree_alignment.py。
9. 重建 fixture，运行测试和 build。
10. 更新任务状态和验收报告。
```

## Definition of Done

```text
1. Phase 39 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 39。
3. FastAPI、Vue3、MCP 使用同一个 knowledge_tree.md 节点全集。
4. 正式知识和候选知识 uncovered_count 均为 0。
5. Vue3 左侧 L1/L2/L3 数字能反映当前范围真实正式知识数。
6. 右侧审计摘要正式知识、候选知识、来源、缺口、冲突口径一致。
7. Phase 36/38 AI Engineering 历史节点和新节点都能在 UI 中显示。
8. API 测试通过。
9. Vue3 build 通过。
10. 中文文档和生成文件 UTF-8 无乱码。
```

## 测试与验收

```text
python codex-expert-kit/rag/scripts/validate_knowledge_tree_alignment.py
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
python -m pytest codex-expert-kit/api/tests
cd ui && npm run build
```

## 风险与回滚

| 风险 | 处理 |
| --- | --- |
| Markdown 解析不完整 | 验证脚本检查节点数、字段缺失、父子链完整性 |
| 前端树节点突增影响阅读 | 保持 L3 默认收起，搜索和分页不变 |
| 旧节点与新 canonical node 并存 | 先按 knowledge_tree.md 完整承接，不做破坏性迁移 |
| 统计变大导致用户误解 | UI 文案区分正式知识、候选知识、已沉淀候选 |
| FastAPI 与 MCP 解析差异 | 后续可抽公共解析器；本 Phase 先用同一源和验证脚本对齐 |

回滚方式：

```text
1. 保留原 mockData.ts，不删除旧 fixture。
2. 如生成 fixture 异常，auditStore 可临时回退到 mockData 的 knowledgeTreeNodes。
3. 如 FastAPI 解析异常，可回退 services.py 的静态 TREE_NODES。
4. 不修改正式知识内容，因此不会影响 MCP 知识本体。
```

## 需要开发者确认的问题

```text
本 Phase 不涉及重大架构变更、不引入数据库、不改变 MCP 权限、不改变 approved 语义，按当前用户确认直接执行。
```

## 状态更新要求

完成任一任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase39_knowledge_tree_single_source_stats_alignment.md
docs/reports/phase39_knowledge_tree_alignment_report.json
```
