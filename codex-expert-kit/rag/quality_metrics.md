# CEK-TA Knowledge Quality Metrics

本文定义 CEK-TA 知识库的质量指标、计算口径、门槛、输入输出契约和回归规则。它用于评估知识是否有价值、可复用、可审计、可检索，并用于 Phase 17 首批真实知识资产的验收。

## 目标

```text
1. 让知识库质量可量化，而不是只靠主观感觉。
2. 让知识树覆盖、来源质量、冲突状态、时效性、检索质量和外部项目复用都可追踪。
3. 让 v1 tree_node_id 与 v2 canonical_node_id 的路由一致性可评测。
4. 阻止无来源、无边界、冲突未消解、检索不可追踪的知识进入默认指导。
5. 为 Vue3 质量看板、MCP 查询验收、RAG 检索优化和采集优先级提供统一口径。
```

## 输入契约

质量评测读取以下数据集合：

```json
{
  "knowledge_items": ["KnowledgeItem"],
  "knowledge_tree_nodes": ["KnowledgeTreeNode"],
  "knowledge_tree_v2_nodes": ["KnowledgeTreeNodeV2 optional"],
  "tree_aliases": ["TreeAlias optional"],
  "source_profiles": ["SourceProfile"],
  "conflict_audits": ["ConflictAudit"],
  "retrieval_test_cases": ["RetrievalEvalCase"],
  "qa_test_cases": ["QAEvalCase"],
  "routing_test_cases": ["TreeRoutingEvalCase"],
  "external_project_usage_logs": ["ExternalUsageLog optional"],
  "contribution_records": ["ContributionRecord optional"]
}
```

最低必需字段：

```text
knowledge_id
partition_id
tree_node_id
tree_path
canonical_node_id optional during migration
canonical_tree_path optional during migration
domain
subdomain
rule_type
source_refs or source
applicable_scope or applies_to
not_applicable_scope or not_applicable_when
confidence
freshness
review_status
conflict_status
project_binding
updated_at
```

## 输出契约

质量评测输出 `KnowledgeQualityReport`：

```json
{
  "report_id": "string",
  "period": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "scope": {
    "tree_version": "v1 | v2 | mixed",
    "partitions": ["string"],
    "domains": ["string"],
    "node_ids": ["string"]
  },
  "scores": {
    "overall_quality_score": 0.0,
    "coverage_score": 0.0,
    "source_quality_score": 0.0,
    "conflict_safety_score": 0.0,
    "freshness_score": 0.0,
    "retrieval_quality_score": 0.0,
    "citation_completeness_score": 0.0,
    "boundary_quality_score": 0.0,
    "review_readiness_score": 0.0,
    "reuse_score": 0.0,
    "tree_routing_score": 0.0
  },
  "rates": {
    "conflict_rate": 0.0,
    "staleness_rate": 0.0,
    "retrieval_hit_rate": 0.0,
    "citation_completeness": 0.0,
    "review_pass_rate": 0.0,
    "contribution_acceptance_rate": 0.0,
    "v1_v2_route_consistency_rate": 0.0,
    "unsafe_default_guidance_rate": 0.0
  },
  "counts": {
    "knowledge_item_count": 0,
    "approved_item_count": 0,
    "reviewed_item_count": 0,
    "draft_item_count": 0,
    "source_count": 0,
    "reuse_count": 0,
    "blocking_issue_count": 0
  },
  "top_gaps": [],
  "blocking_issues": [],
  "recommended_actions": []
}
```

## 指标分组

### 1. Knowledge Coverage

衡量知识树节点是否有足够的可用知识。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `leaf_coverage_rate` | covered 或 partial 的叶子节点数 / 全部叶子节点数 | >= 0.6 for seed scope |
| `approved_leaf_rate` | 至少有 1 条 approved 知识的叶子节点数 / 目标叶子节点数 | >= 0.4 for seed scope |
| `required_type_coverage` | 已满足 required knowledge types 的数量 / required knowledge types 总数 | >= 0.6 |
| `empty_critical_node_count` | risk_level 为 high/critical 且没有 reviewed/approved 知识的节点数 | 越低越好 |
| `overgrown_node_rate` | overgrown 节点数 / 已覆盖节点数 | <= 0.1 |

计算来源：

```text
knowledge_tree_audit_rules.md
knowledge_tree.md
knowledge_tree_v2.md
knowledge_items[].rule_type
knowledge_items[].review_status
```

### 2. Source Quality

衡量知识来源是否足以支撑专业结论。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `source_presence_rate` | 有 source_refs/source 的知识条目数 / 知识条目数 | 1.0 for reviewed/approved |
| `medium_high_source_rate` | 至少有 medium/high 来源的 reviewed/approved 条目数 / reviewed/approved 条目数 | >= 0.95 |
| `primary_source_rate` | 有 primary evidence 的条目数 / reviewed/approved 条目数 | >= 0.5 |
| `source_scope_match_rate` | 来源适用范围匹配知识适用范围的条目数 / reviewed/approved 条目数 | >= 0.9 |
| `low_only_approved_count` | 仅由 low 来源支撑且 review_status=approved 的条目数 | 必须为 0 |

批准阻断：

```text
1. reviewed/approved 知识缺来源。
2. approved 知识只有 low reliability 来源。
3. 来源不覆盖知识声明的 market/timeframe/data_granularity/project_type。
4. 性能类声明缺样本、成本、偏差控制或复现说明。
```

### 3. Conflict Safety

衡量知识是否存在未消解矛盾。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `conflict_rate` | potential/confirmed/resolved 冲突条目数 / 知识条目数 | 越低越好 |
| `unresolved_confirmed_conflict_count` | confirmed 且无 resolution 的条目数 | 必须为 0 |
| `approved_unchecked_conflict_count` | approved 但 conflict_status 缺失或 unchecked 的条目数 | 必须为 0 |
| `scope_boundary_resolution_rate` | scope/market/granularity/assumption 冲突中已有明确边界的数量 / 对应冲突数量 | >= 0.95 |
| `unsafe_default_guidance_rate` | 默认检索返回阻断状态知识的次数 / 默认检索用例数 | 必须为 0 |

### 4. Freshness

衡量时间敏感知识是否足够新。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `time_sensitive_review_rate` | time_sensitive 且 accessed_at/reviewed_at 在窗口内的条目数 / time_sensitive 条目数 | >= 0.9 |
| `staleness_rate` | stale 或超出 review window 的条目数 / time_sensitive 条目数 | <= 0.1 |
| `high_impact_stale_count` | live_trading、risk_review、exchange_adapter、model_api 中 stale 条目数 | 必须为 0 for default guidance |
| `deprecated_return_rate` | 默认检索返回 deprecated 条目的次数 / 默认检索用例数 | 必须为 0 |

### 5. Retrieval Quality

衡量 RAG/MCP 是否能按任务找到正确、可引用、有边界的知识。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `retrieval_hit_rate` | top_k 中包含 expected_knowledge_ids 或 expected_node_ids 的用例数 / 用例数 | >= 0.8 |
| `top1_node_accuracy` | top1 命中 expected_node_ids 的用例数 / 用例数 | >= 0.7 |
| `citation_completeness` | 返回结果包含 source_refs 且字段完整的结果数 / 返回结果数 | >= 0.95 |
| `boundary_preservation_rate` | 返回结果保留适用/不适用边界的用例数 / 用例数 | >= 0.95 |
| `recommended_action_accuracy` | 推荐动作符合阻断/警告规则的用例数 / 用例数 | >= 0.9 |

检索回归阻断：

```text
1. 默认指导返回 draft/rejected/deprecated/unsourced/confirmed unresolved conflict。
2. live_trading 或 risk_review 返回 stale 高影响知识且无 warning。
3. 查询要求具体 timeframe/data_granularity，但返回 general 规则且无边界提示。
4. source_refs 缺失导致无法引用。
```

### 6. Tree Routing Quality

衡量知识树 v1/v2 迁移期间的兼容性。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `v1_v2_route_consistency_rate` | v1 与 canonical 查询返回兼容节点/条目的用例数 / 路由用例数 | >= 0.95 |
| `alias_resolution_success_rate` | alias 可解析用例数 / alias 用例数 | >= 0.95 |
| `alias_mismatch_block_rate` | v1/canonical 不一致时被阻断的用例数 / mismatch 用例数 | 1.0 |
| `split_target_default_block_rate` | split_targets 未进入 default_guidance 的用例数 / split_targets 用例数 | 1.0 |
| `routing_warning_completeness` | alias、migration、risk warning 完整返回的用例数 / 需要 warning 的用例数 | >= 0.95 |

### 7. Review Readiness

衡量知识是否方便人工审计。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `metadata_completeness_rate` | 必需 metadata 完整条目数 / 条目数 | >= 0.95 |
| `applicability_boundary_rate` | 有 applicable 和 not_applicable 边界的条目数 / 条目数 | >= 0.95 |
| `review_pass_rate` | 审计通过条目数 / 审计条目数 | 持续追踪 |
| `blocking_issue_close_rate` | 已关闭阻断问题数 / 阻断问题总数 | >= 0.8 per cycle |

### 8. Reuse And Backflow

衡量知识是否真正被其他项目复用并反哺。

| Metric | 口径 | 默认门槛 |
| --- | --- | --- |
| `reuse_count` | 外部项目引用 CEK-TA 知识的次数 | 持续追踪 |
| `reuse_project_count` | 发生引用的不同项目数量 | 持续追踪 |
| `contribution_acceptance_rate` | accepted 回灌数 / reviewed 回灌数 | 持续追踪 |
| `rejected_private_fact_rate` | 因项目私有事实被阻断的回灌数 / 回灌数 | 持续追踪 |
| `post_reuse_issue_rate` | 复用后被标记为错误/过期/冲突的次数 / 复用次数 | 越低越好 |

## 总分计算

默认总分仅用于排序和趋势观察，不能自动批准知识。

```text
overall_quality_score =
  coverage_score * 0.15 +
  source_quality_score * 0.18 +
  conflict_safety_score * 0.18 +
  freshness_score * 0.10 +
  retrieval_quality_score * 0.17 +
  citation_completeness_score * 0.08 +
  boundary_quality_score * 0.08 +
  tree_routing_score * 0.06
```

硬阻断优先于总分：

```text
1. unsafe_default_guidance_rate > 0
2. unresolved_confirmed_conflict_count > 0 for approved/default scope
3. low_only_approved_count > 0
4. source_presence_rate < 1.0 for reviewed/approved
5. alias_mismatch_block_rate < 1.0
```

## 评测级别

```text
smoke:
  少量用例，验证契约和阻断规则是否还在。

regression:
  覆盖核心节点、检索、引用、边界、v1/v2 路由，作为每次知识库结构或检索策略变更后的必跑评测。

release:
  覆盖目标知识资产范围，用于 Phase 17 accepted 知识资产验收。

audit:
  面向人工审计，输出 top_gaps、blocking_issues 和 recommended_actions。
```

## Vue3 显示映射

Vue3 质量看板可以按以下颜色展示：

```text
red:
  有硬阻断、unsafe default guidance、confirmed unresolved conflict、source missing、alias mismatch 未阻断。

amber:
  coverage partial、source mixed、time_sensitive warning、routing warning、review gaps。

green:
  无硬阻断，关键指标达到门槛，检索和引用通过。

gray:
  空节点或尚未进入当前评测范围。
```

## 不做什么

```text
1. 不根据质量分自动删除知识。
2. 不根据质量分自动批准知识。
3. 不引入外部评测服务。
4. 不引入数据库。
5. 不把实时市场数据或 K 线行情作为本系统采集目标。
6. 不把项目私有事实直接提升为通用知识。
```

## DoD

```text
1. 每个指标有清晰口径。
2. 每个硬阻断有明确条件。
3. 指标覆盖知识树、来源、冲突、时效、检索、引用、边界、复用、v1/v2 路由。
4. 指标可被文件化评测集和质量报告模板消费。
5. UTF-8 中文可读，无乱码。
```
