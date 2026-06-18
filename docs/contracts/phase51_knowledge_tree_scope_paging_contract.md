# Phase 51 知识树范围分页与详情懒加载契约

## 契约目标

让 Vue3 KnowledgeTree 页面在大分支场景下只处理当前节点、当前页、当前可见窗口的数据，避免一次性生成全量知识卡片。

## 数据来源

```text
ui/public/data/knowledgeTreeNodes.json
ui/public/data/formalKnowledgeItems.json
ui/public/data/phase23Candidates.json
ui/public/data/knowledgeTreeScopeIndex.json
```

`knowledgeTreeScopeIndex.json` 是由 CEK-TA 本地脚本从正式知识、候选知识和知识树节点生成的派生索引，不是知识事实源。

## 范围索引结构

```json
{
  "schema_version": "phase51.scope_index.v1",
  "generated_at": "2026-06-13T00:00:00+00:00",
  "source": "ui/public/data/*.json",
  "source_version": {
    "knowledge_tree": "sha256",
    "formal_knowledge": "sha256",
    "candidates": "sha256"
  },
  "count": 121,
  "nodes": {
    "kt.trading_engineering": {
      "node_id": "kt.trading_engineering",
      "descendant_node_ids": ["kt.backtest"],
      "knowledge_ids": ["knowledge_id"],
      "candidate_ids": ["candidate_id"],
      "counts": {
        "knowledge_total": 0,
        "candidate_total": 0,
        "reviewed": 0,
        "approved": 0,
        "accepted_for_draft": 0,
        "needs_more_evidence": 0,
        "rejected": 0,
        "source_count": 0,
        "open_gap_count": 0,
        "conflict_count": 0
      }
    }
  }
}
```

## 分页读取契约

输入：

```text
node_id: string | null
kind: formal | candidate | all
query: string
status: string
conflict_status: string
freshness: string
sort: relevance | source_count_desc | status | updated_desc
page: number
page_size: number
```

输出：

```text
items: KnowledgeCardSummary[]
total: number
page: number
page_size: number
has_next: boolean
source_version: string
generated_at: string
```

## 摘要卡结构

```text
id
kind
title
subtitle
summary
status
tree_node_id
canonical_node_id
source_count
conflict_status
freshness_status
default_guidance
```

摘要卡不得携带完整 `source_evidence`、完整 `llm_usage_policy` 或完整候选审计日志。

## 详情加载契约

输入：

```text
kind: knowledge | candidate
id: string
```

输出：

```text
id
kind
summary
raw
loaded_from
loaded_at
```

详情可以从已加载的静态 JSON 中按 ID 查找。后续若改成 FastAPI，必须保持同一结构。

## 搜索契约

```text
1. 用户输入先进入原始 query。
2. debounce 后才进入列表过滤。
3. 少于 2 个字符时，不触发大范围搜索。
4. 少于最小长度时，页面显示中文提示。
5. 搜索范围只限当前 node_id 范围索引命中的 ID。
```

## 性能预算

```text
1. 知识树首屏 2 秒内出现可交互目录和当前范围摘要列表。
2. 切换大分支时不白屏，`#app` 不为空。
3. 当前 DOM 中 `.knowledge-point-card` 数量不得超过当前虚拟窗口和缓冲区。
4. 默认每页 20 条，允许 50/100，但 100 条也必须窗口化渲染。
```

## 边界

```text
1. 本契约只优化前端展示，不改变正式知识、候选知识和审计状态。
2. 本契约不授权候选知识作为默认指导。
3. 本契约不改变 MCP、SearchLab 或 FastAPI 的权限。
4. 范围索引只用于 UI 快速定位，不作为 RAG 检索排序事实源。
```
