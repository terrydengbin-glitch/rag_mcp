# Phase 13: RAG 数据层与检索质量任务卡

## Phase 目标

把 CEK-TA 的知识 schema、知识树、候选知识和来源审计规则落成可索引、可检索、可测试、可追踪的 RAG 数据层，让其他项目通过 Codex/MCP 查询时得到结构化、带引用、带边界、带冲突提示的专业结果。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-053 | P0 | done | 定义正式知识存储目录与索引格式 | `codex-expert-kit/rag/storage_layout.md` |
| CEK-TA-054 | P0 | done | 定义检索结果契约 | `codex-expert-kit/rag/search_result_contract.md` |
| CEK-TA-055 | P1 | done | 创建样例知识数据与检索测试集 | `codex-expert-kit/rag/examples/` |

## 上游输入

```text
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/knowledge_tree_schema.md
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/retrieval_policy.md
codex-expert-kit/rag/ingestion_candidate_schema.md
```

## 下游输出

```text
Phase 14 MCP runtime server
Phase 15 Vue3 检索测试台
Phase 16 检索质量评测
外部项目知识查询
```

## 输入契约

正式知识数据必须来自：

```text
accepted knowledge item
reviewed contribution
approved research candidate
manually approved seed asset
```

禁止来源：

```text
未审计 proposed 内容
无来源内容
项目私有字段
未处理冲突的规则
```

## 输出契约

检索结果必须返回：

```text
query
matched_items
item_id
title
claim
summary
tree_path
domain
applicable_scope
not_applicable_scope
source_refs
confidence
freshness
review_status
conflict_status
why_matched
recommended_next_action
```

## 边界范围

范围内：

```text
定义文件化数据层
定义索引格式
定义检索结果返回结构
定义样例数据
定义检索测试集
```

范围外：

```text
不引入生产数据库
不接入外部向量数据库
不做大规模 embedding 构建
不改变 MCP 权限
```

## 涉及组件

```text
codex-expert-kit/rag/
codex-expert-kit/mcp/
ui/src/stores/
ui/src/views/
```

## 涉及数据结构

```text
KnowledgeStoreLayout
KnowledgeIndexRecord
SearchResult
SearchMatchReason
RetrievalTestCase
```

## 涉及数据库/存储

第一阶段使用本地文件存储，建议目录分为：

```text
knowledge/
indexes/
examples/
tests/
```

如需引入 RAGFlow、向量库、SQLite、Postgres 或其他后端，必须先经过开发者确认。

## 实施步骤

1. 定义 `storage_layout.md`。
2. 定义 `search_result_contract.md`。
3. 创建样例知识数据。
4. 创建检索测试集。
5. 对齐 MCP tool 返回结构。
6. 更新索引。

## Definition of Done

```text
正式知识与候选知识边界清楚
检索结果契约完整
样例数据可被 MCP 草案读取
检索结果包含引用、置信度、适用边界和冲突状态
不引入未确认数据库
UTF-8 中文无乱码
```

## 测试与验收

```text
检查 storage layout 文档存在
检查 search result contract 字段完整
检查 examples 目录存在
用样例 query 验证返回结构
检查 proposed 内容不会进入正式检索
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
文件结构过早绑定未来数据库设计
样例数据与正式知识边界混淆
检索返回缺少风险提示
```

回滚：

```text
保留 schema 文档
样例数据放在 examples 中，不影响正式知识目录
未确认数据库方案前不做迁移
```

## 需要开发者确认的问题

```text
是否保持文件化存储作为 MVP
是否后续接入 RAGFlow 或其他向量库
是否允许引入 SQLite 作为本地索引层
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase13_rag_data_layer.md
```

## 完成记录

```text
completed_at: 2026-06-08
status: done
```

已完成：

```text
1. 定义文件化 RAG 存储布局。
2. 定义检索结果契约。
3. 创建 knowledge、indexes、examples、tests 目录。
4. 创建样例知识数据、样例索引、样例请求、样例结果和检索测试集。
5. 更新 MCP 草案 common.py，使其支持 tree_node_id、tree_path、tree_path_prefix。
6. 更新任务索引状态。
```

边界说明：

```text
1. 本阶段不引入数据库、向量库或 RAGFlow 运行依赖。
2. examples/ 是开发样例，不是生产知识真相。
3. proposed 倒灌内容不能进入默认正式检索。
4. Phase 12 的 ingestion_candidate_schema.md 尚未创建，本阶段只预留候选来源接口。
```

测试：

```text
1. 检查 storage layout 文档存在。
2. 检查 search result contract 字段完整。
3. 检查 examples 和 tests 目录存在。
4. 使用样例数据调用 search_expert_knowledge。
5. 检查 tree_node_id 过滤和 tree_path 返回。
6. 使用 Get-Content -Encoding UTF8 检查中文显示。
```
