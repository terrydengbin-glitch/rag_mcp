# Phase 51: Vue3 KnowledgeTree 大分支性能优化

## Phase 目标

优化知识树页面在“大分支、上千知识点、候选与正式知识混合显示”场景下的加载、筛选、切换和详情查看性能。

本 Phase 承接 Phase 49 的前端白屏稳定性修复和 Phase 50 的大 fixture 拆包与懒加载。Phase 51 不改变知识治理状态、不新增知识、不改变 MCP 权限，重点是让知识树页面从“前端一次性全量生成卡片”改成“预计算索引 + 分页/虚拟滚动 + 摘要优先 + 详情按需加载”。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-506 | P0 | done | 定义知识树大分支性能预算与当前基线 | `docs/reports/phase51_knowledge_tree_performance_baseline.json` |
| CEK-TA-507 | P0 | done | 给知识树数据增加 `node_id -> knowledge_ids/candidate_ids` 预计算索引 | `ui/public/data/knowledgeTreeScopeIndex.json`、相关生成脚本 |
| CEK-TA-508 | P0 | done | 定义知识树范围分页、摘要卡和详情懒加载契约 | `docs/contracts/phase51_knowledge_tree_scope_paging_contract.md` |
| CEK-TA-509 | P0 | done | 将知识树页面列表改成范围分页读取，不一次生成全量卡片 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/services/knowledgeDataClient.ts` |
| CEK-TA-510 | P1 | done | 将知识点卡片改成摘要卡，点击后再加载详情 | `ui/src/components/`、知识详情加载逻辑 |
| CEK-TA-511 | P1 | done | 大列表接入虚拟滚动，搜索输入增加 debounce 和最小搜索长度 | `ui/src/components/`、`ui/src/composables/` |
| CEK-TA-512 | P1 | done | 增加 Playwright 大分支性能验收 | `ui/tests/e2e/knowledge-tree-performance.spec.ts`、`docs/reports/phase51_knowledge_tree_large_scope_performance_report.json` |
| CEK-TA-513 | P1 | done | 生成 Phase 51 验收报告并更新任务索引 | `docs/reports/phase51_knowledge_tree_large_scope_performance_report.md` |

## 上游输入

```text
1. Phase 49 Vue3 白屏与 Dev Server 稳定性修复。
2. Phase 50 Vue3 大 fixture 拆包与懒加载数据访问层。
3. 当前知识树页面：
   - ui/src/views/KnowledgeTreeView.vue
4. 当前数据访问层：
   - ui/src/services/knowledgeDataClient.ts
   - ui/public/data/phase23Candidates.json
   - ui/public/data/formalKnowledgeItems.json
   - ui/public/data/knowledgeTreeNodes.json
5. 当前正式知识索引：
   - codex-expert-kit/rag/indexes/knowledge_items.json
6. 当前候选知识目录：
   - codex-expert-kit/rag/candidates/**/*.json
```

## 下游输出

```text
1. 知识树节点范围索引，支持按 node_id 快速定位正式知识和候选知识。
2. 知识树页面分页读取当前范围内的知识点，不在前端一次性生成全量卡片。
3. 知识点列表默认显示摘要卡，详情在点击后按需加载。
4. 大列表使用虚拟滚动或等价窗口化渲染，只渲染当前屏及缓冲区。
5. 搜索输入具备 debounce 和最小长度限制，避免每个按键触发全量筛选。
6. Playwright 可验证大分支首屏、切分支和搜索不会白屏或卡死。
```

## 输入契约

数据源仍以 CEK-TA 正式文件和 Phase 50 静态 JSON 为输入，不直接读取开发机绝对路径：

```text
ui/public/data/knowledgeTreeNodes.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/phase23Candidates.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/candidates/**/*.json
```

新增索引生成必须满足：

```text
1. Python 脚本使用 UTF-8 读写。
2. 仓库路径使用 path_resolver 或已有生成脚本的 resolver 能力。
3. 输出文件使用原子写入，避免 Vite 读取半写 JSON。
4. `node_id` 必须兼容 canonical node 和 alias 归一化结果。
5. 不改变正式知识和候选知识源文件本体。
```

## 输出契约

### 知识树范围索引

目标文件：

```text
ui/public/data/knowledgeTreeScopeIndex.json
```

结构：

```json
{
  "schema_version": "phase51.scope_index.v1",
  "generated_at": "2026-06-13T00:00:00+08:00",
  "source_version": {
    "knowledge_items": "hash-or-generated-at",
    "candidates": "hash-or-generated-at",
    "knowledge_tree": "hash-or-generated-at"
  },
  "nodes": {
    "kt.trading_engineering.backtest": {
      "node_id": "kt.trading_engineering.backtest",
      "descendant_node_ids": [],
      "knowledge_ids": [],
      "candidate_ids": [],
      "counts": {
        "knowledge_total": 0,
        "candidate_total": 0,
        "reviewed": 0,
        "approved": 0,
        "accepted_for_draft": 0,
        "needs_more_evidence": 0,
        "rejected": 0,
        "open_gap_count": 0,
        "conflict_count": 0
      }
    }
  }
}
```

### 前端数据访问接口

`knowledgeDataClient` 或等价 service 需要提供：

```text
getKnowledgeTreeScopeIndex(): Promise<KnowledgeTreeScopeIndex>
listKnowledgeCardsByNode(params): Promise<PagedResult<KnowledgeCardSummary>>
getKnowledgeCardDetail(params): Promise<KnowledgeCardDetail>
```

分页参数：

```text
node_id
kind: formal | candidate | all
status
conflict_status
freshness
query
page
page_size
sort
```

分页返回：

```text
items
total
page
page_size
has_next
filters
source_version
generated_at
```

详情加载：

```text
id
kind
title
statement
applicability
not_applicable_when
source_evidence
review
machine_gate
conflict_audit
links
```

错误状态：

```text
index_not_loaded
node_not_found
detail_not_found
schema_mismatch
network_error
empty_result
```

## 边界范围

范围内：

```text
1. 预计算 node_id 到知识 ID 的范围索引。
2. 知识树页面分页、摘要、详情懒加载。
3. 大列表窗口化/虚拟滚动。
4. 搜索 debounce 和最小搜索长度限制。
5. Playwright 性能验收和白屏回归验收。
6. 用户可见文案中文化。
```

范围外：

```text
1. 不新增、删除或修改专业知识内容。
2. 不改变 candidate/reviewed/approved/default guidance/hard gate 状态语义。
3. 不改变 MCP tool 权限。
4. 不引入新数据库。
5. 不要求后端 FastAPI 必须实现分页；第一阶段可用静态索引和前端 adapter 完成。
6. 不关闭或误杀其他项目端口。
7. 不把候选知识当作默认正式知识读取。
```

## 涉及组件

```text
codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
ui/public/data/
ui/src/services/knowledgeDataClient.ts
ui/src/views/KnowledgeTreeView.vue
ui/src/components/
ui/src/composables/
ui/tests/e2e/
docs/contracts/
docs/reports/
```

## 涉及数据结构

```text
KnowledgeTreeNode
KnowledgeTreeScopeIndex
KnowledgeTreeScopeNode
KnowledgeCardSummary
KnowledgeCardDetail
PagedResult
DataClientError
```

## 涉及数据库/存储

不引入数据库。第一阶段使用 Phase 50 已建立的 `ui/public/data/*.json` 静态 JSON 存储形态，并新增一个范围索引 JSON。

如果后续需要把分页下沉到 FastAPI 或数据库，必须另开任务卡，定义 API/数据库表、索引、迁移、缓存和回滚策略。

## 实施步骤

```text
1. 复测当前大分支性能，记录首屏、切分支、搜索和详情点击基线。
2. 定义 Phase 51 知识树范围分页与详情懒加载契约。
3. 扩展数据生成脚本，输出 node_id -> knowledge_ids/candidate_ids 范围索引。
4. 改造 knowledgeDataClient，增加范围索引读取、分页摘要和详情按需加载接口。
5. 改造 KnowledgeTreeView，切分支时只读取当前 node_id 的当前页摘要。
6. 将知识点卡片压缩为摘要卡，点击后加载详情区或抽屉。
7. 大列表接入虚拟滚动或等价窗口化渲染。
8. 搜索输入增加 debounce，少于最小长度时只做本页/当前范围提示，不触发大范围筛选。
9. 增加 Playwright 大分支性能验收。
10. 执行 build、e2e、乱码检查，生成验收报告并更新索引。
```

## Definition of Done

```text
1. Phase 51 任务卡和索引存在。
2. `knowledgeTreeScopeIndex.json` 或等价范围索引存在，并能按 node_id 找到正式知识和候选知识 ID。
3. 知识树页面不再一次性生成当前分支下所有知识卡片。
4. 当前范围列表支持分页读取。
5. 知识点卡片默认是摘要卡，详情点击后加载。
6. 大分支列表使用虚拟滚动或窗口化渲染，DOM 中不堆积上千张卡片。
7. 搜索具备 debounce 和最小搜索长度限制。
8. 首屏 2 秒内可交互，切换大分支不白屏。
9. Playwright 性能验收通过。
10. `npm --prefix ui run build` 通过。
11. UTF-8 乱码检查通过。
12. 不改变知识治理状态和 MCP 权限。
13. 风险和回滚方案写入报告。
```

## 测试与验收

必须执行：

```text
npm --prefix ui run build
npm --prefix ui run test:e2e
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
```

新增 Playwright 验收建议：

```text
1. 打开知识树页面，首屏 2 秒内出现可交互的知识树和当前范围摘要列表。
2. 选择知识点最多的 L1/L2/L3 节点，页面不白屏，列表在 2 秒内可滚动。
3. 切换大分支时 `#app` 不为空，页面显示中文 loading 或当前范围数据。
4. 当前 DOM 中知识卡片数量不超过当前页/虚拟窗口数量加缓冲区。
5. 搜索少于最小长度时不触发全量筛选，并显示中文提示。
6. 搜索 debounce 后结果稳定，未出现连续重渲染导致卡顿。
7. 点击摘要卡后详情可加载，返回列表不丢失分页和滚动位置。
```

## 风险与回滚

风险：

```text
1. 预计算索引与正式知识/候选数据不同步，导致统计数字不一致。
2. 虚拟滚动可能影响键盘可访问性、滚动定位和移动端触控体验。
3. 摘要与详情分离后，详情加载失败可能被误认为知识缺失。
4. 搜索最小长度可能让用户以为搜索不可用，需要中文提示。
```

回滚：

```text
1. 保留 Phase 50 的 JSON 懒加载数据访问层。
2. 如虚拟滚动出现阻断，可先回滚到分页摘要卡，不回到全量卡片渲染。
3. 如范围索引异常，可临时使用 Phase 50 原始 `knowledgeTreeNodes.json` 和 `formalKnowledgeItems.json` 计算当前页。
4. 回滚时不得恢复直接 import 大 fixture 到首包。
```

## 需要开发者确认的问题

```text
1. 搜索最小长度是否采用 2 个中文字符或 3 个英文字符。
2. 知识详情使用右侧详情区、抽屉还是下方详情面板。
3. Playwright 性能阈值是否以本地 dev server 为准，还是另设生产 build 预览阈值。
```

## 状态更新要求

完成每个任务后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase51_knowledge_tree_large_scope_performance.md
```

如新增契约、报告、测试文件，还必须在 Phase 51 验收报告中列出路径和测试结果。
