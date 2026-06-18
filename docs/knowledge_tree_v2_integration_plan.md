# CEK-TA Knowledge Tree v2 Integration Plan

本文定义知识树 v2 与 RAG、MCP、Vue3、采集流水线、外部项目接入的兼容改造清单。本计划不直接修改运行时代码，不切换默认知识树。

## 目标

```text
1. 让现有 v1 tree_node_id 继续可用。
2. 让 v2 canonical_node_id 可逐步进入 RAG/MCP/Vue3。
3. 让检索支持 alias、status、conflict、freshness、project_binding 过滤。
4. 让审计界面看到迁移状态和风险。
5. 不破坏现有默认树、MCP 权限和 Vue3 信息架构。
```

## 当前状态

```text
default_tree: codex-expert-kit/rag/knowledge_tree.md
v2_tree: codex-expert-kit/rag/knowledge_tree_v2.md
alias_map: codex-expert-kit/rag/knowledge_tree_aliases.md
v2_schema: codex-expert-kit/rag/knowledge_tree_node_v2_schema.md
routing_policy: codex-expert-kit/rag/tree_routing_policy.md
```

## 集成原则

```text
1. 先读兼容，后写 canonical。
2. 先 audit 展示，后 default guidance。
3. 先工具只读，后考虑审计动作。
4. 先追加字段，不删除 v1 字段。
5. 任何默认切换都必须经过 Phase 16 质量评测。
```

## RAG 数据层改造清单

### Metadata Additions

追加字段：

```text
metadata.canonical_node_id
metadata.canonical_tree_path
metadata.tree_aliases
metadata.tree_migration_status
metadata.node_status
metadata.risk_level
metadata.routing_policy
```

保留字段：

```text
metadata.tree_node_id
metadata.tree_path
metadata.partition_id
metadata.domain
metadata.subdomain
metadata.review_status
metadata.conflict_status
```

### Index Additions

新增或扩展索引：

```text
indexes/tree_aliases.json
indexes/canonical_nodes.json
indexes/node_status_index.json
indexes/risk_level_index.json
```

### Acceptance Criteria

```text
1. v1 tree_node_id 查询结果不变。
2. canonical_node_id 查询能找到 alias 兼容项。
3. v1 与 canonical 同时传入时，必须一致。
4. split_targets 不进入 default guidance。
5. rejected/deprecated/conflicted/unsourced 不进入 default guidance。
```

## MCP 改造清单

### Affected Tools

```text
browse_knowledge_tree
search_expert_knowledge
get_knowledge_item
get_conflict_audit
list_kb_partitions
```

### Input Additions

可选新增：

```text
canonical_node_id
canonical_tree_path_prefix
include_aliases
include_migration_status
node_status
risk_level
mode: default_guidance | audit | browse | ingestion_classification | quality_eval
```

### Output Additions

追加：

```text
routing.input_tree_node_id
routing.resolved_tree_node_id
routing.canonical_node_id
routing.alias_used
routing.migration_status
routing.warnings
```

### Permission Boundary

```text
1. MCP 仍默认只读。
2. 不新增写入知识库工具。
3. 不新增审批工具。
4. 不改变现有 tool 权限。
5. 审计动作如需写入，必须另建 Phase 并确认。
```

### Acceptance Criteria

```text
1. 旧请求继续可用。
2. 新 canonical 参数是可选项。
3. alias mismatch 返回 schema_mismatch 或 unsupported_filter。
4. browse 模式可展示 v2 节点。
5. default_guidance 模式阻断不安全状态。
```

## Vue3 改造清单

### Affected Views

```text
KnowledgeTreeView.vue
SearchLab.vue
IngestionReview.vue
KnowledgeDetail.vue
ConflictReview.vue
```

### KnowledgeTreeView

新增展示：

```text
canonical_node_id
aliases
migration_status
node_status
risk_level
kb_partition
default_retrieval_allowed
```

新增状态：

```text
alias warning
candidate node
conditional node
potential conflict node
critical risk node
deprecated alias
```

边界：

```text
不改变现有主导航结构。
不把 v2 candidate 节点显示成 approved 指导。
不隐藏 v1 node_id。
```

### SearchLab

新增输入：

```text
canonical_node_id
canonical_tree_path_prefix
mode
include_aliases
```

新增结果字段：

```text
routing.alias_used
routing.migration_status
routing.warnings
recommended_next_action
```

### IngestionReview

新增候选分类字段：

```text
canonical_node_id
canonical_tree_path
alias_resolution_status
classification_confidence
node_status
risk_level
```

### Acceptance Criteria

```text
1. 页面仍能读取 v1 数据。
2. v2 字段缺失时显示空态，不报错。
3. alias warning 清晰可审计。
4. critical/high risk 节点有明显审计提示。
5. 移动端和桌面端文本不溢出。
```

## 采集流水线改造清单

### Research Task

新增：

```text
canonical_target_node_id
canonical_tree_path
alias_resolution_status
node_risk_level
required_evidence_by_node
```

### Ingestion Candidate

新增：

```text
classification.canonical_node_id
classification.canonical_tree_path
classification.aliases
classification.node_status
classification.risk_level
classification.routing_policy
```

### Acceptance Criteria

```text
1. 候选仍必须有 v1 tree_node_id 或 canonical_node_id 可解析。
2. accepted 候选必须完成 alias resolution。
3. critical/high risk 候选必须有更严格 evidence_required。
4. project_private 贡献不得映射 project_binding = none。
```

## 外部项目接入改造清单

### Adapter

新增健康检查：

```text
cek_ta_tree_version
supports_canonical_node_id
supports_v1_alias
project_truth_boundary_defined
field_mapping_status
contribution_classification_mode
```

### Contribution

新增：

```text
source_project_tree_node_id
cek_ta_v1_node_id
cek_ta_canonical_node_id
truth_boundary_review
alias_resolution_status
```

### Acceptance Criteria

```text
1. 其他项目可以继续使用 v1 node_id。
2. 新项目优先写 canonical_node_id。
3. 回灌贡献必须保留项目来源和 CEK-TA 分类映射。
4. 项目事实不得进入通用知识节点。
```

## 测试计划

### Contract Tests

```text
1. v1 node_id -> canonical_node_id 解析。
2. canonical_node_id -> v1 alias 解析。
3. alias mismatch 阻断。
4. split_targets 默认不返回。
5. v2 partition_id 均能映射 canonical_root。
```

### Retrieval Tests

```text
1. v1 查询结果不变。
2. canonical 查询返回相同或兼容结果。
3. default_guidance 阻断 draft/rejected/deprecated/conflicted/unsourced。
4. audit 模式允许展示 candidate/deprecated，但必须有 warning。
5. project_binding mismatch 阻断默认指导。
```

### Vue Tests

```text
1. v1 树视图仍可渲染。
2. v2 canonical 字段缺失不崩溃。
3. alias warning 展示。
4. risk_level badge 展示。
5. build 通过。
```

### MCP Tests

```text
1. 旧输入 schema 兼容。
2. 新 canonical 字段可选。
3. browse_knowledge_tree 可加载 v1 默认树。
4. v2 browse 需要显式 tree_path 指向 knowledge_tree_v2.md。
5. 权限仍为只读。
```

## Rollback Plan

```text
1. 保留 knowledge_tree.md 为默认树。
2. 禁用 canonical filters。
3. alias 表仅作为文档保留。
4. MCP 不加载 v2 文件。
5. Vue 隐藏 v2 字段。
6. 正式知识条目继续使用 v1 tree_node_id。
```

## 不做什么

```text
1. 不直接修改 MCP 权限。
2. 不直接改变 Vue3 信息架构。
3. 不引入数据库。
4. 不批量迁移正式知识。
5. 不删除 v1 node_id。
6. 不创建 approved 知识。
```

## 建议实施顺序

```text
1. Phase 16 增加 v1/v2 路由一致性评测。
2. MCP 增加只读 alias resolver。
3. RAG 索引追加 canonical metadata。
4. Vue3 增加 canonical/migration/risk 展示。
5. Phase 17 首批知识资产双写 v1 和 canonical 字段。
6. 评测稳定后再考虑 canonical 默认化。
```

## DoD

```text
1. RAG、MCP、Vue3、采集、外部项目接入影响已列明。
2. 输入输出字段明确。
3. 权限和边界明确。
4. 测试计划明确。
5. 回滚路径明确。
6. UTF-8 中文可读。
```

