# Phase 50: Vue3 大 Fixture 拆包与懒加载

## Phase 目标

把当前直接打进 Vue3 首包的候选知识、正式知识和知识树大 fixture，改造为可分页、可缓存、可按需加载的数据访问层，降低首包体积、刷新白屏风险和 Vite dev server 压力。

本 Phase 承接 Phase 49 的根因修复。Phase 49 已通过原子写入和 Vite watcher 降低半写模块缓存风险；Phase 50 进一步从架构上减少大体量 `ui/src/data/*.ts` 被直接 import 到首包的问题。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-499 | P0 | done | 定义 Vue3 fixture 拆包与懒加载数据契约 | `docs/contracts/phase50_vue3_data_loading_contract.md` |
| CEK-TA-500 | P0 | done | 拆分候选、正式知识、知识树静态数据输出格式 | `ui/public/data/*.json` 或等价数据目录、生成脚本改造方案 |
| CEK-TA-501 | P0 | done | 实现 Vue3 数据访问 adapter，替代页面直接 import 大 fixture | `ui/src/services/knowledgeDataClient.ts`、相关 composables |
| CEK-TA-502 | P1 | done | 优化候选页、知识树页、SearchLab 页 loading/empty/error 与分页状态 | `ui/src/views/*`、相关组件 |
| CEK-TA-503 | P1 | done | 增加大数据量刷新、分页、过滤和离线 fallback 的 Playwright 验收 | `ui/tests/e2e/fixture-lazy-loading.spec.ts` |
| CEK-TA-504 | P1 | done | 增加首包体积、白屏、模块导出和中文文案回归门禁 | `docs/reports/phase50_vue3_lazy_loading_validation_report.json` |
| CEK-TA-505 | P1 | done | 生成 Phase 50 验收报告并更新任务索引 | `docs/reports/phase50_vue3_fixture_lazy_loading_report.md` |

## 上游输入

```text
1. Phase 49 白屏根因报告和稳定性验收报告。
2. 当前 Vue3 fixture 生成脚本：
   - codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
   - codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
   - codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
3. 当前前端数据文件：
   - ui/src/data/phase23Candidates.ts
   - ui/src/data/formalKnowledgeItems.ts
   - ui/src/data/knowledgeTreeNodes.ts
4. 当前前端页面：
   - IngestionReview
   - KnowledgeTreeView
   - SearchLab
5. Phase 25/28/47/49 的 Vue3 实机验收规则。
```

## 下游输出

```text
1. 可按需加载的数据契约。
2. 不再把大型知识数据全部打进首包的 Vue3 数据访问层。
3. 候选页、知识树页、SearchLab 页可在 loading/empty/error/pagination 状态下稳定渲染。
4. Playwright 桌面与移动端刷新验收。
5. 首包体积和白屏风险验证报告。
```

## 输入契约

数据源仍以 CEK-TA 正式文件为唯一事实来源：

```text
codex-expert-kit/rag/candidates/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge_tree.md
```

允许生成前端消费数据：

```text
ui/public/data/candidates.index.json
ui/public/data/candidates.page.{n}.json
ui/public/data/formal_knowledge.index.json
ui/public/data/formal_knowledge.page.{n}.json
ui/public/data/knowledge_tree.json
```

具体路径可在 CEK-TA-499 契约中调整，但必须满足：

```text
1. 不依赖开发机绝对路径。
2. 运行时路径由相对 URL、环境变量或 resolver 生成。
3. 生成脚本继续使用 UTF-8 和原子写入。
4. 页面不能直接 import 5 MB 级别数据文件进首包。
```

## 输出契约

前端数据 client 必须提供稳定接口：

```text
listCandidates(params): Promise<PagedResult<IngestionCandidateSummary>>
getCandidate(candidateId): Promise<IngestionCandidateDetail>
listKnowledgeItems(params): Promise<PagedResult<KnowledgeItemSummary>>
getKnowledgeItem(knowledgeId): Promise<KnowledgeItemDetail>
getKnowledgeTree(): Promise<KnowledgeTreeNode[]>
searchLocalKnowledge(params): Promise<SearchResult>
```

分页返回结构：

```text
items
total
page
page_size
has_next
filters
generated_at
source_version
```

错误返回必须区分：

```text
data_not_found
schema_mismatch
network_error
stale_fixture
empty_result
```

## 边界范围

范围内：

```text
1. 拆分前端 fixture 输出。
2. 增加 Vue3 数据访问 adapter。
3. 让页面从 adapter 读取数据。
4. 增加 loading/empty/error/pagination 状态。
5. 验证刷新后不白屏。
6. 验证用户可见文案中文化。
```

范围外：

```text
1. 不新增专业知识。
2. 不改变候选、reviewed、approved 状态语义。
3. 不启用 default guidance 或 hard gate。
4. 不改变 MCP tool 权限。
5. 不引入新数据库。
6. 不要求立即引入 FastAPI；可优先用静态 JSON，后续再接 API。
7. 不关闭其他项目端口。
```

## 涉及组件

```text
codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
codex-expert-kit/rag/scripts/build_ui_knowledge_fixture.py
codex-expert-kit/rag/scripts/build_ui_knowledge_tree_fixture.py
ui/src/services/
ui/src/views/IngestionReview.vue
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
ui/src/types.ts
ui/tests/e2e/
```

## 涉及数据结构

```text
IngestionCandidate
KnowledgeItem
KnowledgeTreeNode
PagedResult
DataClientError
SearchResult
```

## 涉及数据库/存储

不引入数据库。默认使用本地生成的静态 JSON 作为第一阶段存储形态。

如果后续改为 FastAPI 动态接口，必须另开子任务并补充 API 输入输出契约、错误契约、缓存策略和测试。

## 实施步骤

```text
1. 统计当前 ui/src/data/*.ts 体积、build chunk 体积和页面首屏加载行为。
2. 定义 Phase 50 数据加载契约。
3. 将大 fixture 输出拆成 index + page/detail JSON。
4. 实现数据访问 adapter，支持静态 JSON fallback。
5. 改造候选页、知识树页、SearchLab 页读取 adapter。
6. 增加 loading/empty/error/pagination 中文文案。
7. 增加 Playwright 桌面/移动端刷新验收。
8. 执行 build、e2e、乱码检查和白屏检查。
9. 生成 Phase 50 验收报告并更新索引。
```

## Definition of Done

```text
1. Phase 50 任务卡和索引存在。
2. 数据加载契约存在。
3. 大型知识数据不再直接进入 Vue3 首包。
4. 候选、正式知识、知识树能按需加载。
5. 页面 loading/empty/error 状态中文化。
6. 刷新 /dashboard、/knowledge-tree、/ingestion、/search-lab 不白屏。
7. Playwright 桌面和移动端通过。
8. npm --prefix ui run build 通过。
9. UTF-8 乱码检查通过。
10. 不改变知识治理状态和 MCP 权限。
11. 如有风险，报告中写明回滚方案。
```

## 测试与验收

必须执行：

```text
npm --prefix ui run build
npm --prefix ui run test:e2e
python codex-expert-kit/rag/scripts/validate_no_mojibake.py
```

建议新增：

```text
1. 检查首包 JS 体积低于 Phase 49 基线。
2. 检查关键路由刷新后 body 和 #app 非空。
3. 检查断网或静态 JSON 缺失时显示中文错误状态。
4. 检查分页、过滤、详情点击不触发整页白屏。
```

## 风险与回滚

风险：

```text
1. 静态 JSON 拆包后，页面可能出现异步加载时序 bug。
2. SearchLab 当前若依赖内存全量数据，需改为局部索引或延迟加载。
3. 若部署路径不是根路径，public data URL 需要处理 base path。
```

回滚：

```text
1. 保留 Phase 49 原子写入后的 TS fixture 生成能力。
2. 如懒加载 adapter 出现阻断问题，可临时切回 direct import。
3. 回滚前必须确认不会重新引入半写模块白屏风险。
```

## 需要开发者确认的问题

```text
1. Phase 50 第一阶段是否只使用静态 JSON，不接 FastAPI。
2. 是否设置首包体积硬阈值，例如主 JS gzip 小于 500 KB。
3. SearchLab 是否允许改成“先加载索引，再按需加载详情”的交互。
```
