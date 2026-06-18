# Phase 11: 知识树体系任务卡

## Phase 目标

把 CEK-TA 知识库从分散文档升级为可浏览、可检索、可审计、可度量覆盖率的专业知识树，让用户和其他项目都能清楚看到当前系统掌握了哪些知识、缺哪些知识、哪些知识存在冲突或过期风险。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-047 | P0 | done | 定义知识树节点 schema | `codex-expert-kit/rag/knowledge_tree_schema.md` |
| CEK-TA-048 | P0 | done | 创建交易与 AI 专业知识树主干 | `codex-expert-kit/rag/knowledge_tree.md` |
| CEK-TA-049 | P1 | done | 定义知识树覆盖率与审计规则 | `codex-expert-kit/rag/knowledge_tree_audit_rules.md` |

## 上游输入

```text
codex-expert-kit/rag/kb_partitions.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/conflict_detection_rules.md
docs/知识库采集与审计规范.md
```

## 下游输出

```text
Phase 12 采集流水线归类目标
Phase 13 RAG 数据层路径索引
Phase 15 Vue3 知识树视图
Phase 16 知识覆盖率评测
外部项目按知识树定位查询
```

## 输入契约

知识节点必须能关联现有知识条目字段：

```text
domain
subdomain
topic
knowledge_type
review_status
conflict_status
source_refs
related_items
```

## 输出契约

知识树节点必须包含：

```text
node_id
parent_id
path
title
domain
subdomain
level
summary
key_concepts
expected_knowledge_types
coverage_status
review_status
freshness_status
conflict_status
source_policy
related_nodes
```

## 边界范围

范围内：

```text
定义树结构 schema
定义第一版知识树主干
定义节点覆盖率规则
定义节点与知识条目的映射关系
```

范围外：

```text
不批量采集真实知识
不改写已存在知识条目 schema 的核心字段
不引入图数据库
不做复杂知识图谱推理
```

## 涉及组件

```text
codex-expert-kit/rag/
ui/src/views/
codex-expert-kit/mcp/
```

## 涉及数据结构

```text
KnowledgeTreeNode
KnowledgeTreePath
CoverageStatus
NodeAuditResult
NodeRelation
```

## 涉及数据库/存储

第一版用 Markdown 定义知识树主干，用结构化字段描述节点。后续如需要 JSON/YAML 或数据库存储，必须在 Phase 13 中定义。

## 实施步骤

1. 定义 `knowledge_tree_schema.md`。
2. 创建 `knowledge_tree.md`，覆盖交易、回测、风控、执行、LLM、RAG、MCP 等主干。
3. 定义覆盖率、冲突、过期、来源质量审计规则。
4. 更新 RAG 检索策略中关于树路径检索的约束。
5. 更新任务索引。

## Definition of Done

```text
知识树 schema 存在
知识树主干覆盖核心领域
每个一级节点有 node_id 和 path
每个节点能关联知识条目
覆盖率规则可被 Vue3 和评测系统消费
边界和不做事项明确
UTF-8 中文无乱码
```

## 测试与验收

```text
检查知识树文件存在
检查 node_id 唯一性
检查 parent_id 可以追溯
检查至少覆盖交易、回测、风控、执行、LLM/RAG
检查 schema 字段完整
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
知识树过细导致维护成本高
知识树过粗导致检索价值低
节点命名不稳定影响后续引用
```

回滚：

```text
保留第一版节点 ID
新增节点只能追加
如需重命名，必须维护 alias 或 migration 说明
```

## 需要开发者确认的问题

```text
是否接受第一版知识树覆盖交易工程和 LLM/RAG 两条主线
是否需要为股票、期货、加密货币拆独立一级节点
是否需要后续引入图数据库或保持文件存储
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase11_knowledge_tree.md
```

## 完成记录

```text
completed_at: 2026-06-08
status: done
```

已完成：

```text
1. 创建知识树节点 schema。
2. 创建交易工程、AI 工程、项目接入三条主干的第一版知识树。
3. 创建覆盖率、来源、冲突、时效、映射质量审计规则。
4. 更新 retrieval policy，增加 tree_node_id、tree_path 和 tree_path_prefix 检索约束。
5. 更新任务索引状态。
```

边界说明：

```text
1. 本阶段只定义树和审计规则，不批量采集真实专业知识。
2. 不引入图数据库。
3. 不把节点 reviewed 视为知识条目 approved。
4. 股票、期货、加密货币暂作为 applicability 过滤维度，不拆成独立一级树。
```

测试：

```text
1. 检查文件存在。
2. 检查 schema 必填字段存在。
3. 检查 knowledge_tree 覆盖交易、回测、风控、执行、LLM/RAG。
4. 检查 node_id 唯一性和 parent_id 可追溯。
5. 使用 Get-Content -Encoding UTF8 检查中文显示。
```
