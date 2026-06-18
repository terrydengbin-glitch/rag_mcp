# KnowledgeTree Reading API Contract

## 目标

本文定义 Phase 28 `CEK-TA-126` 的 FastAPI 只读接口契约，用于把 Vue3 知识树阅读页面接到稳定的数据服务。

该 API 只服务 CEK-TA 审计工作台，不替代 MCP，不对外提供知识写入、审批、删除、回灌或交易能力。

## 上游

```text
1. docs/tasks/phase28_knowledge_tree_vue_fastapi_delivery.md
2. docs/prototypes/knowledge_tree_reading_ui_prototype.html
3. codex-expert-kit/rag/kb_partitions_v2.md
4. codex-expert-kit/rag/indexes/knowledge_items.json
5. codex-expert-kit/core/path_resolver.py
6. ui/src/views/KnowledgeTreeView.vue
7. ui/src/stores/auditStore.ts
8. ui/src/types.ts
9. ui/src/data/mockData.ts
10. ui/src/data/phase23Candidates.ts
```

## 下游

```text
1. Vue3 KnowledgeTreeView 页面读取知识树节点、知识点列表、知识详情和审计摘要。
2. SearchLab 通过 canonical_node_id / tree_node_id 接收跳转参数。
3. IngestionReview 通过 tree_node_id 接收候选知识过滤参数。
4. Playwright 验收通过该契约验证页面过滤、跳转和详情渲染。
5. Phase 36 AI Engineering 候选知识通过 tree_node_id / canonical_node_id 进入候选审计页。
```

## 权限边界

允许：

```text
1. 读取知识树节点。
2. 读取节点下知识点分页列表。
3. 读取单条知识详情。
4. 读取节点审计摘要。
5. 读取 API 健康状态。
```

禁止：

```text
1. 写入知识。
2. 审批知识。
3. 删除知识。
4. 触发知识回灌。
5. 自动把 candidate/draft 改成 approved。
6. 修改 MCP tool 权限。
7. 暴露交易、实盘、订单、账户、密钥能力。
```

## 路径解析规则

```text
1. Python 服务定位仓库文件必须使用 codex-expert-kit/core/path_resolver.py。
2. 默认知识索引路径为 codex-expert-kit/rag/indexes/knowledge_items.json。
3. 可通过 CEK_TA_KNOWLEDGE_ITEMS_PATH 覆盖正式知识索引路径。
4. 可通过 CEK_TA_ROOT 指定 CEK-TA 根目录。
5. 禁止在运行时代码中硬编码 E:\collector\rag 或任何开发机绝对路径。
6. 禁止依赖当前工作目录推导数据文件位置。
```

## 通用响应 envelope

成功响应：

```json
{
  "ok": true,
  "data": {},
  "meta": {
    "request_id": "req_20260608_000001",
    "served_at": "2026-06-08T12:00:00+08:00",
    "data_version": "knowledge_items.json:sha256-or-mtime",
    "source": "knowledge_items_index"
  }
}
```

错误响应：

```json
{
  "ok": false,
  "error": {
    "error_code": "NODE_NOT_FOUND",
    "message": "Knowledge tree node not found.",
    "details": {
      "node_id": "kt.unknown"
    },
    "request_id": "req_20260608_000002"
  }
}
```

## 通用错误码

| error_code | HTTP | 说明 |
| --- | --- | --- |
| `INVALID_QUERY` | 400 | query、page、page_size、status 等参数不合法 |
| `NODE_NOT_FOUND` | 404 | 节点不存在，且 alias 无法解析 |
| `ITEM_NOT_FOUND` | 404 | 知识条目不存在 |
| `INDEX_NOT_FOUND` | 503 | 正式知识索引不存在或不可读取 |
| `INDEX_INVALID` | 503 | 知识索引 JSON 无法解析或字段缺失 |
| `SERVICE_DEGRADED` | 503 | 服务降级，只能返回部分数据 |
| `INTERNAL_ERROR` | 500 | 未分类内部错误 |

## 数据模型

### KnowledgeTreeNode

```json
{
  "id": "kt.trading_engineering.backtest.bias",
  "canonical_node_id": "kt.trading_engineering.backtest.bias",
  "parent_id": "KB_04_BACKTEST",
  "level": 3,
  "title": "Backtest Bias",
  "subtitle": "lookahead / leakage / overfitting",
  "summary": "回测偏差专题，覆盖前视偏差、数据泄漏、过拟合和样本外验证。",
  "keywords": ["backtest", "bias", "data leakage", "overfitting"],
  "children_count": 0,
  "knowledge_count": 12,
  "candidate_count": 3,
  "open_gap_count": 2,
  "coverage_status": "partial",
  "review_status": "reviewed",
  "freshness_status": "fresh",
  "conflict_status": "none",
  "aliases": ["kt.backtest.bias"],
  "sort_order": 410
}
```

### KnowledgeItemCard

```json
{
  "id": "ki_same_candle_tp_sl_fill_ordering",
  "title": "Same-candle TP/SL must declare fill ordering",
  "tree_node_id": "kt.trading_engineering.replay_simulation.fill_model",
  "canonical_node_id": "kt.trading_engineering.replay_simulation.fill_model",
  "claim_type": "backtest_validity_rule",
  "classification_notes": "UI tree node and canonical classification are aligned.",
  "status": "approved",
  "source_count": 2,
  "conflict_status": "none",
  "freshness_status": "fresh",
  "llm_usage_policy": {
    "allowed": ["用于审计当前知识范围内的专业边界。"],
    "not_allowed": ["不得据此生成买卖点、仓位、杠杆或实盘执行指令。"],
    "required_context": ["project_type", "market", "timeframe"],
    "fallback_behavior": "cite_with_caveat"
  },
  "machine_gate": {
    "default_guidance": "allow",
    "reason": "approved; default_guidance_allowed=true; sources, conflict, freshness, and privacy gates passed.",
    "requires_human_escalation": false,
    "blocking_reasons": [],
    "checked_at": "2026-06-09",
    "gate_version": "1.0.0"
  },
  "recommended_extra_sources_count": 0,
  "summary": "OHLC-only backtests must explicitly declare same-candle TP/SL ordering.",
  "updated_at": "2026-06-08T12:00:00+08:00"
}
```

### KnowledgeItemDetail

```json
{
  "id": "ki_same_candle_tp_sl_fill_ordering",
  "title": "Same-candle TP/SL must declare fill ordering",
  "summary": "OHLC-only backtests must explicitly declare same-candle TP/SL ordering.",
  "content": "Without intrabar path data, the system cannot claim the true order of TP and SL events.",
  "tree_node_id": "kt.trading_engineering.replay_simulation.fill_model",
  "canonical_node_id": "kt.trading_engineering.replay_simulation.fill_model",
  "claim_type": "backtest_validity_rule",
  "classification_notes": "UI tree node and canonical classification are aligned.",
  "applicable_scope": "OHLC-only backtest, no trusted tick path.",
  "not_applicable_scope": "Exchange fill events or trusted tick replay prove ordering.",
  "llm_usage_policy": {
    "allowed": ["用于审计当前知识范围内的专业边界。"],
    "not_allowed": ["不得据此生成买卖点、仓位、杠杆或实盘执行指令。"],
    "required_context": ["project_type", "market", "timeframe"],
    "fallback_behavior": "cite_with_caveat"
  },
  "machine_gate": {
    "default_guidance": "allow",
    "reason": "approved; default_guidance_allowed=true; sources, conflict, freshness, and privacy gates passed.",
    "requires_human_escalation": false,
    "blocking_reasons": [],
    "checked_at": "2026-06-09",
    "gate_version": "1.0.0"
  },
  "recommended_extra_sources_count": 0,
  "sources": [
    {
      "source_id": "src_internal_fill_model_notes",
      "title": "Fill model behavior notes",
      "url": null,
      "source_type": "internal_report",
      "quality_score": 0.82,
      "citation": "2 sources / internal report + framework behavior notes."
    }
  ],
  "conflict_handling": "Resolved by separating OHLC-only assumptions from tick-path replay assumptions.",
  "status": "approved",
  "review_notes": ["No known direct conflict."]
}
```

### AuditSummary

```json
{
  "node_id": "kt.trading_engineering",
  "approved_count": 2,
  "candidate_count": 7,
  "source_count": 3,
  "open_gap_count": 6,
  "conflict_count": 1,
  "stale_count": 2,
  "next_actions": [
    {
      "label": "查看候选",
      "target": "/ingestion?tree_node_id=kt.trading_engineering",
      "kind": "route"
    },
    {
      "label": "带入 SearchLab 检索测试",
      "target": "/searchlab?canonical_node_id=kt.trading_engineering",
      "kind": "route"
    }
  ],
  "manual_review_hints": [
    "draft/candidate 不可作为默认指导",
    "外部项目回灌不可直写"
  ]
}
```

## Phase 36 AI Engineering 只读展示要求

AI Engineering 新节点和候选知识必须沿用同一套只读契约：

```text
1. KnowledgeTreeView 能展示 `kt.ai_engineering` 下的 L2/L3 节点，包括 `kt.ai_security_privacy_compliance`。
2. FastAPI `/api/candidates?tree_node_id=kt.ai_security_privacy_compliance` 必须能返回 Phase 36 的 AI Security / Privacy / Compliance 候选。
3. FastAPI `/api/candidates?tree_node_id=kt.llm_training` 必须能返回 LLM Training 子树候选。
4. CandidateCard 必须返回 source_count、conflict_status、candidate_status、workflow、source_refs 和 blocking_issues。
5. SearchLab 跳转只携带查询过滤条件，不写知识、不审批、不转换 candidate。
6. candidate/reviewed 不得在知识树中被展示成 approved 默认指导。
```

Phase 36 AI Engineering 候选卡最少字段：

```json
{
  "candidate_id": "cand_20260609_ai_engineering_security_rag_context_is_untrusted_input_v1_001",
  "research_task_id": "RIT-P36-N-04",
  "partition_id": "KB_AI_19_SECURITY_PRIVACY_COMPLIANCE",
  "tree_node_id": "kt.ai_security_privacy_compliance",
  "candidate_status": "candidate_ready",
  "source_count": 3,
  "conflict_status": "none",
  "workflow": {
    "stage": "candidate_ready",
    "queue_group": "pending",
    "next_action": "export_for_ai_or_human_audit"
  }
}
```

### PaginatedKnowledgeItems

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 1284,
  "total_pages": 65,
  "sort": "relevance",
  "has_next": true,
  "has_prev": false
}
```

## API 端点

### GET /api/health

用途：Vue3 判断 API 是否可用，决定是否进入 fixture fallback。

响应：

```json
{
  "ok": true,
  "data": {
    "service": "cek-ta-knowledge-tree-api",
    "status": "healthy",
    "read_only": true,
    "index_loaded": true,
    "knowledge_items_path": "codex-expert-kit/rag/indexes/knowledge_items.json",
    "resolver": "codex-expert-kit/core/path_resolver.py"
  },
  "meta": {
    "request_id": "req_20260608_000003",
    "served_at": "2026-06-08T12:00:00+08:00",
    "data_version": "knowledge_items.json:sha256-or-mtime",
    "source": "healthcheck"
  }
}
```

### GET /api/knowledge-tree/roots

用途：读取 L1 主枝列表。当前应覆盖 3 个主枝：

```text
Trading Engineering
AI Engineering
Project Support
```

响应 data：

```json
{
  "roots": []
}
```

### GET /api/knowledge-tree/nodes/{node_id}

用途：读取单个节点详情。`node_id` 可以是 canonical id 或 alias。

参数：

```text
node_id: string
```

响应 data：

```json
{
  "node": {}
}
```

### GET /api/knowledge-tree/nodes/{node_id}/children

用途：读取节点子节点，用于左侧树展开。

查询参数：

```text
depth: integer, default 1, min 1, max 2
include_l3: boolean, default false
```

响应 data：

```json
{
  "node_id": "kt.trading_engineering",
  "children": []
}
```

约束：

```text
1. L3 默认不随 L2 一起返回，除非 include_l3=true。
2. Vue3 左侧树默认展示 L1/L2，L3 默认收起。
```

### GET /api/knowledge-tree/nodes/{node_id}/knowledge

用途：读取当前节点范围内的知识点分页列表。

查询参数：

```text
query: string, optional
status: all | draft | candidate | reviewed | approved | rejected | gap
conflict_status: all | none | potential | conflict
freshness_status: all | fresh | aging | stale | unknown
sort: relevance | updated_desc | status | source_count_desc
page: integer, default 1, min 1
page_size: integer, default 20, allowed 20 | 50 | 100
include_descendants: boolean, default true
```

响应 data：

```json
{
  "node": {},
  "knowledge": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 1284,
    "total_pages": 65,
    "sort": "relevance",
    "has_next": true,
    "has_prev": false
  }
}
```

约束：

```text
1. 默认包含子节点知识，保证点击 L2 能看到树下所有知识点。
2. 对上千知识点场景必须分页，不允许一次性返回全部。
3. page_size 最大 100。
4. draft/candidate/gap 可以展示，但 UI 必须明确标识，不可作为默认指导。
5. knowledge item card 必须返回 claim_type、llm_usage_policy、machine_gate 和 recommended_extra_sources_count。
```

### GET /api/knowledge-items/{knowledge_id}

用途：读取单条知识详情。

参数：

```text
knowledge_id: string
```

响应 data：

```json
{
  "item": {}
}
```

约束：

```text
1. 返回必须包含 sources、applicable_scope、not_applicable_scope、conflict_handling。
2. 若来源不足，status 不得被提升为 approved。
3. 返回必须包含 Schema v1.1 AI 使用门控字段；缺字段时使用安全默认值而不是返回 500。
```

### GET /api/knowledge-tree/nodes/{node_id}/audit-summary

用途：读取右侧审计摘要。

参数：

```text
node_id: string
```

响应 data：

```json
{
  "summary": {}
}
```

## Vue3 调用约定

```text
1. 页面启动时先请求 GET /api/health。
2. API healthy 时使用 FastAPI adapter。
3. API unavailable 时使用 fixture fallback，并在页面状态中标注 degraded fixture fallback。
4. 路由 query 支持 tree_node_id、canonical_node_id、item_id、query、status、conflict_status、freshness_status。
5. 点击知识点后调用 GET /api/knowledge-items/{knowledge_id}，详情展示在 Open Gaps 之前。
6. 点击查看候选跳转 /ingestion?tree_node_id=...
7. 点击 SearchLab 跳转 /searchlab?canonical_node_id=...
```

## 审计与安全规则

```text
1. API 返回 draft/candidate/gap 时，Vue3 必须显示非默认指导提示。
2. conflict_status=conflict 的知识不得作为默认指导。
3. source_count=0 的知识不得作为默认指导。
4. freshness_status=stale 的知识必须提示需要复核。
5. API 不返回任何实盘、账户、密钥、订单操作能力。
```

## 测试要求

契约测试至少覆盖：

```text
1. /api/health 返回 read_only=true。
2. /api/knowledge-tree/roots 返回 3 个 L1 主枝。
3. /api/knowledge-tree/nodes/{node_id}/children 默认不展开 L3。
4. /api/knowledge-tree/nodes/{node_id}/knowledge 支持分页，page_size 超限返回 INVALID_QUERY。
5. /api/knowledge-items/{knowledge_id} 返回 sources 和适用边界。
6. /api/knowledge-items/{knowledge_id} 返回 machine_gate、llm_usage_policy 和 claim_type。
7. 未知 node_id 返回 NODE_NOT_FOUND。
8. 未知 knowledge_id 返回 ITEM_NOT_FOUND。
9. 索引路径缺失时返回 INDEX_NOT_FOUND 或 SERVICE_DEGRADED。
```

Vue3 验收至少覆盖：

```text
1. API healthy 时走 FastAPI adapter。
2. API unavailable 时走 fixture fallback。
3. 桌面端知识点网格一行最多 5 个。
4. L3 默认收起，点击 L1/L2 可展开/收起。
5. 知识详情显示在 Open Gaps 之前。
6. 右侧审计摘要显示 approved/candidate/source/gap/conflict/stale 统计。
7. 移动端无横向溢出。
```

## DoD

```text
1. 本契约文档存在。
2. Phase 28 任务卡 CEK-TA-126 标记为 done。
3. docs/index_tasks.md 中 CEK-TA-126 标记为 done。
4. 契约覆盖上游、下游、权限、路径 resolver、API、错误、测试。
5. 未引入 FastAPI 依赖，未新增后端代码。
6. 中文文档 UTF-8 读取正常。
```
