# Phase 50 Vue3 数据加载契约

## 目标

将 Vue3 审计工作台使用的候选知识、正式知识和知识树数据，从首包内直接 import 的 TypeScript 大数组，改为静态 JSON 按需加载的数据访问层。

本契约只定义前端只读数据加载方式，不改变候选、reviewed、approved、default guidance 或 MCP 权限语义。

## 上游事实源

```text
codex-expert-kit/rag/candidates/**/*.json
codex-expert-kit/rag/indexes/knowledge_items.json
codex-expert-kit/rag/knowledge_tree.md
```

## 前端发布数据

第一阶段使用静态 JSON，不引入 FastAPI 或数据库：

```text
ui/public/data/phase23Candidates.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/knowledgeTreeNodes.json
```

每个 JSON 文件必须满足：

```json
{
  "schema_version": "phase50.static_fixture.v1",
  "generated_at": "ISO-8601 UTC timestamp",
  "source": "human readable source path",
  "count": 0,
  "items": []
}
```

## 前端数据 Client

前端通过 `ui/src/services/knowledgeDataClient.ts` 读取数据，不允许页面直接 import 大型 `ui/src/data/*.ts` fixture。

接口：

```ts
loadCandidateFixture(): Promise<LazyFixturePayload<IngestionCandidate>>
loadFormalKnowledgeFixture(): Promise<LazyFixturePayload<KnowledgeItem>>
loadKnowledgeTreeFixture(): Promise<LazyFixturePayload<KnowledgeTreeNode>>
```

返回结构：

```ts
type LazyFixturePayload<T> = {
  schema_version: string
  generated_at: string
  source: string
  count: number
  items: T[]
}
```

错误必须被归一化为：

```ts
type DataClientErrorCode =
  | 'data_not_found'
  | 'schema_mismatch'
  | 'network_error'
  | 'empty_result'
```

## Store 状态契约

`auditStore` 必须暴露：

```text
dataState.state: idle/loading/ready/error
dataState.message: 中文状态说明
dataState.loadedAt: 加载完成时间
dataState.fixtureGeneratedAt: fixture 生成时间
initializeFixtureData(): Promise<void>
```

页面必须能处理：

```text
1. loading：显示中文加载状态。
2. ready：正常展示。
3. error：显示中文错误状态，并保留 mock fallback。
4. empty_result：显示中文空状态。
```

## 边界

允许：

```text
1. 静态 JSON 由现有生成脚本同步生成。
2. 旧 TS fixture 暂时保留作为回滚和兼容路径。
3. SearchLab 继续使用小型 runtimeSearchData fixture。
```

禁止：

```text
1. 页面直接 import 大型候选、正式知识或知识树数组进入首包。
2. 引入数据库或新后端框架。
3. 改变候选、reviewed、approved 或 default guidance 状态语义。
4. 因加载失败把候选或正式知识状态自动升级。
5. 暴露英文 demo/loading/error 文案给用户。
```

## 验收

```text
1. 构建后的主 JS chunk 明显低于 Phase 49 基线 7.3 MB。
2. 刷新 /dashboard、/knowledge-tree、/ingestion、/search-lab 不白屏。
3. Playwright 桌面与移动端通过。
4. UTF-8 乱码检查通过。
```
