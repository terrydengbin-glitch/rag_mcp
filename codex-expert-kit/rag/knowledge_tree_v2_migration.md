# CEK-TA Knowledge Tree v2 Migration Strategy

本文件定义知识树从 v1 分类骨架升级到 v2 治理体系的兼容迁移策略。v2 目标是支持 canonical path、alias 兼容、状态治理、冲突策略、安全检索路由和多项目继承。

## Migration Goal

```text
1. 保留现有 v1 node_id，避免破坏 RAG/MCP/Vue3 和外部项目引用。
2. 新增 v2 canonical_node_id，让节点路径继承父节点并支持前缀过滤。
3. 使用 alias 映射把 v1 node_id、v1 path 和 v2 canonical_node_id 连接起来。
4. 让正式知识、候选知识、MCP 查询、Vue3 审计逐步支持 canonical path。
5. 在未完成兼容测试前，不切换默认知识树入口。
```

## Compatibility Principle

```text
v1 knowledge_tree.md 是当前默认生产树
v2 knowledge_tree_v2.md 是治理升级草案
knowledge_tree_aliases.md 是 v1/v2 兼容索引
任何正式知识条目继续允许使用 v1 tree_node_id
任何新 v2 字段必须有回退字段
任何检索默认行为不得因为 v2 草案改变
```

## Migration Phases

### Stage 0: Contract Only

状态：

```text
current_stage: stage_0_contract_only
default_tree: codex-expert-kit/rag/knowledge_tree.md
v2_tree: not_default
write_mode: v1_only
read_mode: v1_only
```

动作：

```text
1. 定义迁移策略。
2. 定义 v2 节点 schema。
3. 定义 v1 -> v2 alias 映射。
4. 不修改现有知识条目。
5. 不修改 MCP 默认参数。
6. 不修改 Vue3 信息架构。
```

### Stage 1: Alias Supported

状态：

```text
write_mode: v1_primary
read_mode: v1_with_alias_lookup
```

动作：

```text
1. MCP/RAG 读取 v1 node_id 时，可解析 canonical_node_id。
2. Vue3 可显示 canonical path，但仍以 v1 node_id 作为主键。
3. 候选知识包可附带 canonical_node_id。
4. 所有 alias 命中必须写入 retrieval audit。
```

### Stage 2: Canonical Ready

状态：

```text
write_mode: dual_write
read_mode: canonical_preferred_with_v1_fallback
```

动作：

```text
1. 新知识条目同时写 tree_node_id 和 canonical_node_id。
2. 检索支持 canonical_tree_path_prefix。
3. v1 node_id 继续可查。
4. 质量评测验证 v1/v2 返回一致性。
```

### Stage 3: Downstream Migrated

状态：

```text
write_mode: canonical_primary
read_mode: canonical_primary_with_alias
```

动作：

```text
1. MCP/RAG 默认使用 canonical_node_id。
2. Vue3 默认展示 canonical path。
3. v1 node_id 仅作为 alias 和历史兼容字段。
4. 外部项目接入指南更新迁移说明。
```

### Stage 4: Deprecated Alias

状态：

```text
write_mode: canonical_only
read_mode: canonical_with_legacy_alias_warning
```

动作：

```text
1. 新知识禁止只写 v1 node_id。
2. v1 alias 继续可解析但产生 deprecated_alias warning。
3. 不删除历史 v1 node_id。
```

## Canonical ID Rules

v2 `canonical_node_id` 必须继承父节点路径：

```text
kt.<major_area>.<capability>.<topic>.<specialized_topic>
```

示例：

```text
kt.backtest.bias
  -> kt.trading_engineering.backtest.bias

kt.replay_simulation.fill_model
  -> kt.trading_engineering.replay_simulation.fill_model

kt.mcp.knowledge_tools
  -> kt.ai_engineering.mcp_engineering.knowledge_tools
```

规则：

```text
1. root 保持 kt。
2. 一级主枝保持 kt.trading_engineering、kt.ai_engineering、kt.project_integration。
3. 新增 kt.knowledge_governance。
4. 所有交易工程子节点必须位于 kt.trading_engineering.*。
5. 所有 AI 工程子节点必须位于 kt.ai_engineering.*。
6. 所有项目接入节点必须位于 kt.project_integration.*。
7. 知识治理节点必须位于 kt.knowledge_governance.*。
```

## Alias Resolution Contract

alias resolver 输入：

```json
{
  "input_node_id": "kt.backtest.bias",
  "input_path": "CEK-TA / Trading Engineering / Backtest / Bias",
  "lookup_mode": "exact | alias | canonical | any"
}
```

输出：

```json
{
  "status": "ok | warning | error",
  "input_node_id": "kt.backtest.bias",
  "canonical_node_id": "kt.trading_engineering.backtest.bias",
  "v1_node_id": "kt.backtest.bias",
  "migration_status": "alias_supported",
  "warnings": [],
  "errors": []
}
```

解析顺序：

```text
1. exact canonical_node_id
2. exact v1_node_id
3. aliases[]
4. v1_path
5. canonical_path
6. no_match
```

冲突规则：

```text
1. 一个 v1_node_id 只能映射到一个 primary canonical_node_id。
2. 一个 canonical_node_id 可以有多个 aliases。
3. 如果 v1 节点被拆分为多个 v2 节点，primary 映射必须指向最安全的上层节点，并列出 split_targets。
4. split_targets 不得自动用于默认检索，除非用户显式 include_children。
```

## Required Metadata Additions

知识条目 metadata 可逐步增加：

```text
tree_node_id: v1 stable node id
canonical_node_id: v2 canonical node id
tree_path: v1 display path
canonical_tree_path: v2 display path
tree_aliases: legacy aliases used for lookup
tree_migration_status: v1_only | alias_supported | canonical_ready | downstream_migrated | deprecated_alias
```

候选知识包 classification 可逐步增加：

```text
canonical_node_id
canonical_tree_path
alias_resolution_status
classification_confidence
```

检索请求 filters 可逐步增加：

```text
canonical_node_id
canonical_tree_path_prefix
include_aliases
tree_migration_status
```

## Routing Rules

默认检索：

```text
1. review_status 默认 approved。
2. conflict_status 默认 none 或 resolved。
3. v1 tree_node_id 和 canonical_node_id 都可作为过滤条件。
4. 同时给出 v1 和 canonical 时，两者必须在 alias 表中一致。
5. alias 不一致时返回 unsupported_filter 或 schema_mismatch。
```

审计检索：

```text
1. 可以返回 draft、reviewed、candidate。
2. 必须展示 migration_status。
3. 必须展示 conflict_status 和 freshness。
4. alias 命中的结果必须给出 warning。
```

## Downstream Impact

### RAG Data Layer

影响字段：

```text
metadata.tree_node_id
metadata.tree_path
metadata.partition_id
metadata.domain
metadata.subdomain
indexes/tree_nodes.json
```

兼容要求：

```text
1. 不移除 v1 字段。
2. v2 字段只追加。
3. 检索索引可以按 alias 表生成附加索引。
```

### MCP

影响工具：

```text
browse_knowledge_tree
search_expert_knowledge
get_knowledge_item
get_conflict_audit
```

兼容要求：

```text
1. 不改变 tool 权限。
2. 不改变默认 tree_path。
3. 新增 canonical 过滤时必须保持可选。
4. 错误 schema 继续使用 search_result_contract.md。
```

### Vue3

影响视图：

```text
KnowledgeTreeView
SearchLab
IngestionReview
```

兼容要求：

```text
1. 不改变当前信息架构。
2. 可新增 canonical path、migration badge、alias warning。
3. 不把 v2 草案节点展示为 approved 指导。
```

### External Projects

兼容要求：

```text
1. 外部项目仍可使用 v1 tree_node_id。
2. 健康检查可提示 canonical_node_id。
3. 回灌贡献必须保留原项目引用和 canonical 分类结果。
```

## Rollback Plan

```text
1. 默认树保持 knowledge_tree.md。
2. 删除或禁用 knowledge_tree_v2.md 不影响 v1。
3. alias 表只读，禁用后检索回到 v1。
4. 正式知识不批量迁移，避免不可逆变更。
5. MCP/Vue3 未完成兼容前，不切换默认 canonical path。
```

## DoD

```text
1. 明确 v1 不删除。
2. 明确 v2 只追加 canonical 和治理字段。
3. 明确 alias 解析顺序和冲突规则。
4. 明确 RAG/MCP/Vue3 兼容影响。
5. 明确阶段状态和回滚路径。
6. UTF-8 中文可读。
```

