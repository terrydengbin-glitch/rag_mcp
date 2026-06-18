# Phase 18: 知识树 v2 治理升级任务卡

## Phase 目标

在不破坏现有 v1 `tree_node_id`、RAG 数据层、MCP 查询和 Vue3 审计界面的前提下，把知识树从“分类目录”升级为“可路由、可审批、可检索、可冲突治理、可跨项目继承”的 v2 治理体系。

本 Phase 采用兼容迁移：

```text
v1 node_id 保留可用
v2 canonical_node_id 新增
v1 -> v2 alias 映射
RAG/MCP/Vue3 同时支持 old_id 与 canonical_id
完成评测后再逐步迁移正式知识
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-068 | P0 | done | 定义知识树 v2 迁移与兼容策略 | `codex-expert-kit/rag/knowledge_tree_v2_migration.md` |
| CEK-TA-069 | P0 | done | 定义知识树 v2 节点治理 schema | `codex-expert-kit/rag/knowledge_tree_node_v2_schema.md` |
| CEK-TA-070 | P0 | done | 定义 v1 到 v2 的 alias 映射表 | `codex-expert-kit/rag/knowledge_tree_aliases.md` |
| CEK-TA-071 | P1 | done | 创建知识树 v2 主干草案 | `codex-expert-kit/rag/knowledge_tree_v2.md` |
| CEK-TA-072 | P1 | done | 定义 v2 KB 分区与路由策略 | `codex-expert-kit/rag/kb_partitions_v2.md`、`codex-expert-kit/rag/tree_routing_policy.md` |
| CEK-TA-073 | P2 | done | 定义叶子知识内容包模板 | `codex-expert-kit/templates/knowledge_leaf_package_template.md` |
| CEK-TA-074 | P2 | done | 定义 RAG/MCP/Vue3 兼容改造清单 | `docs/knowledge_tree_v2_integration_plan.md` |

## 上游输入

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/knowledge_tree_schema.md
codex-expert-kit/rag/knowledge_tree_audit_rules.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/storage_layout.md
codex-expert-kit/rag/search_result_contract.md
codex-expert-kit/rag/ingestion_candidate_schema.md
codex-expert-kit/mcp/server.py
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
ui/src/views/IngestionReview.vue
docs/knowledge_research_backlog.md
```

## 下游输出

```text
知识树 v2 canonical path
v1/v2 alias 兼容映射
RAG metadata filter
MCP tree path routing
Vue3 知识树浏览与审计
Phase 16 质量评测
Phase 17 首批知识资产
外部项目接入和知识倒灌分类
```

## 输入契约

迁移任务必须读取并保留：

```text
v1_node_id
v1_path
current_partition_id
current_domain
current_subdomain
current_review_status
current_conflict_status
downstream_consumers
```

任何 v2 设计必须声明：

```text
canonical_node_id
parent_canonical_node_id
aliases
kb_partition
node_status
project_binding
conflict_policy
routing_policy
migration_status
rollback_path
```

## 输出契约

v2 节点至少包含：

```text
node_id
canonical_node_id
parent_id
canonical_parent_id
aliases
title
domain
capability
topic
level
summary
status
maturity
scope
out_of_scope
used_for
risk_level
evidence_required
conflict_policy
default_policy
related_nodes
project_binding
kb_partition
version
owner
approved_by
migration_status
```

推荐状态：

```text
draft
candidate
reviewing
approved
conditional
potential_conflict
conflicted
deprecated
archived
```

推荐迁移状态：

```text
v1_only
alias_supported
canonical_ready
downstream_migrated
deprecated_alias
```

## 边界范围

范围内：

```text
定义 v2 canonical 路径体系
定义 v1/v2 alias 兼容策略
定义节点治理 metadata
定义知识状态和冲突策略
新增 knowledge_governance 主枝
规划 data_engineering、risk_management、strategy_engineering、derivatives_flow
拆分 rag_engineering 与 mcp_engineering
定义 RAG/MCP/Vue3 改造清单
```

范围外：

```text
不直接删除 v1 node_id
不直接批量改写正式知识条目
不改变 MCP tool 权限
不改变 Vue3 信息架构
不引入数据库
不创建 approved 知识
不把项目私有经验提升为通用知识
不采集行情数据、K线数据或订单流原始数据
```

## v2 一级结构建议

```text
kt
├── kt.trading_engineering
├── kt.ai_engineering
├── kt.project_integration
└── kt.knowledge_governance
```

## v2 交易工程主干建议

```text
kt.trading_engineering
├── data_engineering
├── quant_foundation
├── strategy_engineering
├── backtest
├── replay_simulation
├── live_execution
├── risk_management
└── trade_analysis
```

## v2 AI 工程主干建议

```text
kt.ai_engineering
├── llm_training
├── rag_engineering
├── mcp_engineering
└── agent_engineering
```

## v2 项目接入主干建议

```text
kt.project_integration
├── adapter
├── truth_boundary
├── field_mapping
├── healthcheck
└── contribution
```

## v2 知识治理主干建议

```text
kt.knowledge_governance
├── status_lifecycle
├── evidence_policy
├── conflict_resolution
├── source_quality
├── versioning
├── deprecation
└── contribution_review
```

## 涉及组件

```text
codex-expert-kit/rag/
codex-expert-kit/mcp/
codex-expert-kit/templates/
docs/
ui/src/views/
```

## 涉及数据结构

```text
KnowledgeTreeNodeV2
KnowledgeTreeAlias
CanonicalNodePath
NodeGovernanceStatus
TreeRoutingPolicy
KBPartitionV2
LeafKnowledgePackage
IntegrationImpactReport
```

## 涉及数据库/存储

本 Phase 不引入数据库。第一阶段使用文件化 Markdown/JSON-like 契约和本地索引。后续如需数据库或向量库 schema 迁移，必须单独创建任务并向开发者确认。

## 实施步骤

1. 编写 v2 迁移策略，明确兼容、回滚、下游影响。
2. 定义 v2 节点 schema，补齐 canonical、aliases、status、risk、evidence、conflict、project_binding。
3. 创建 v1 到 v2 alias 映射表。
4. 创建 v2 主干草案，先覆盖一级和二级主枝。
5. 定义 v2 KB 分区和路由策略，支持 path/status/conflict/project/freshness filter。
6. 定义叶子知识内容包模板。
7. 编写 RAG/MCP/Vue3 兼容改造清单。
8. 更新任务索引。

## Definition of Done

```text
Phase 18 任务卡存在并被索引
v2 迁移策略交付物路径明确
v2 节点 schema 交付物路径明确
alias 映射表交付物路径明确
v2 主干草案交付物路径明确
RAG/MCP/Vue3 兼容影响已列明
不破坏 v1 node_id 的边界明确
回滚方案明确
测试与验收方法明确
UTF-8 中文无乱码
```

## 测试与验收

```text
检查 docs/index_tasks.md 存在 Phase 18
检查 docs/tasks/README.md 存在 Phase 18
检查本任务卡存在且章节完整
检查任务 ID CEK-TA-068 到 CEK-TA-074 不与现有 ID 冲突
检查交付路径明确
检查边界包含不删除 v1 node_id、不改变 MCP 权限、不改变 Vue3 信息架构
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
v2 路径迁移影响已有 RAG 样例和 MCP 查询
Vue3 知识树视图依赖旧 node_id
外部项目可能已引用 v1 tree_node_id
分区变更导致检索路由不一致
一次性拆分过细导致知识沉淀成本上升
```

回滚：

```text
保留 v1 knowledge_tree.md 为主索引
v2 仅作为草案文件存在
所有正式知识继续使用 v1 node_id
alias 映射可禁用但不删除
RAG/MCP/Vue3 在未完成兼容前不切换默认 canonical path
```

## 需要开发者确认的问题

```text
是否确认 Phase 18 放在 Phase 17 之后作为结构升级阶段
是否采用 13 个 KB 分区而不是 12 个或 17 个
是否允许后续阶段更新 Vue3 知识树展示信息架构
是否允许后续阶段拆分 MCP 与 RAG 分区
```

## 状态更新要求

完成本任务卡创建后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase18_knowledge_tree_v2_governance.md
```

## 进度记录

```text
started_at: 2026-06-08
current_status: done
completed_tasks:
  - CEK-TA-068
  - CEK-TA-069
  - CEK-TA-070
  - CEK-TA-071
  - CEK-TA-072
  - CEK-TA-073
  - CEK-TA-074
deliverables:
  - codex-expert-kit/rag/knowledge_tree_v2_migration.md
  - codex-expert-kit/rag/knowledge_tree_node_v2_schema.md
  - codex-expert-kit/rag/knowledge_tree_aliases.md
  - codex-expert-kit/rag/knowledge_tree_v2.md
  - codex-expert-kit/rag/kb_partitions_v2.md
  - codex-expert-kit/rag/tree_routing_policy.md
  - codex-expert-kit/templates/knowledge_leaf_package_template.md
  - docs/knowledge_tree_v2_integration_plan.md
remaining_tasks: []
notes:
  - P0 建立兼容迁移、schema 和 alias 映射
  - P1 建立 v2 主干草案、v2 KB 分区和树路由策略
  - P2 建立叶子知识内容包模板和 RAG/MCP/Vue3 兼容改造清单
  - 不切换默认知识树
  - 未修改 MCP 权限、Vue3 信息架构或正式知识条目
```
