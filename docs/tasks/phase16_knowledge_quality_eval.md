# Phase 16: 知识质量与评测体系任务卡

## Phase 目标

建立 CEK-TA 知识库质量评测体系，用覆盖率、来源质量、冲突率、过期率、检索命中率、引用完整率、外部项目复用率等指标判断知识库是否真正有价值、可复用、可优化。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-062 | P0 | done | 定义知识质量指标体系 | `codex-expert-kit/rag/quality_metrics.md` |
| CEK-TA-063 | P1 | done | 定义检索与问答评测集 | `codex-expert-kit/rag/eval_sets/` |
| CEK-TA-064 | P1 | done | 定义质量报告模板 | `codex-expert-kit/templates/knowledge_quality_report.md` |

## 上游输入

```text
codex-expert-kit/rag/knowledge_tree.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/search_result_contract.md
codex-expert-kit/templates/eval_report.md
codex-expert-kit/rag/knowledge_tree_v2.md
codex-expert-kit/rag/knowledge_tree_aliases.md
codex-expert-kit/rag/tree_routing_policy.md
docs/knowledge_tree_v2_integration_plan.md
```

## 下游输出

```text
Vue3 质量看板
知识采集优先级
RAG 检索优化
MCP 查询质量验收
首批知识资产验收
```

## 输入契约

评测输入必须包含：

```text
knowledge_items
knowledge_tree_nodes
source_profiles
conflict_audits
retrieval_test_cases
external_project_usage_logs
```

## 输出契约

质量报告必须包含：

```text
report_id
period
coverage_score
source_quality_score
conflict_rate
staleness_rate
retrieval_hit_rate
citation_completeness
review_pass_rate
reuse_count
contribution_acceptance_rate
top_gaps
recommended_actions
```

## 边界范围

范围内：

```text
定义质量指标
定义评测集结构
定义质量报告模板
定义人工评测和自动评测边界
```

范围外：

```text
不做模型训练
不引入外部评测服务
不把低分知识自动删除
不自动批准知识更新
```

## 涉及组件

```text
codex-expert-kit/rag/
codex-expert-kit/templates/
ui/src/views/
codex-expert-kit/mcp/
```

## 涉及数据结构

```text
QualityMetric
EvalSet
RetrievalEvalCase
KnowledgeQualityReport
QualityRecommendation
TreeRoutingEvalCase
KnowledgeQualityGate
```

## 涉及数据库/存储

第一阶段使用文件化评测集和 Markdown 报告模板。若需要记录历史质量指标，可后续定义本地 JSON/SQLite 存储。

## 实施步骤

1. 定义知识质量指标。
2. 创建 eval_sets 目录规范。
3. 创建检索评测样例结构。
4. 创建知识质量报告模板。
5. 对齐 Vue3 质量看板需求。
6. 更新索引。
7. 纳入 v1/v2 知识树路由一致性、alias mismatch 阻断和 split target 默认检索阻断评测。

## Definition of Done

```text
质量指标定义清楚
每个指标有计算口径
评测集目录存在
报告模板存在
指标能反映覆盖率、冲突、来源、检索、复用
不会自动删除或批准知识
UTF-8 中文无乱码
```

## 测试与验收

```text
检查 quality_metrics.md 存在
检查 eval_sets 目录存在
检查报告模板字段完整
检查至少包含 K线、回测、风控、执行、LLM/RAG 评测类别
检查包含 v1/v2 route consistency、alias mismatch、split target default block 用例
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
指标过多导致无法执行
指标无法从现有数据中计算
质量分被误用为自动批准依据
```

回滚：

```text
先保留 P0 指标
P1/P2 指标可以延后
质量报告只作为审计参考
```

## 需要开发者确认的问题

```text
是否需要优先做自动化评分脚本
是否需要接入外部项目使用日志
是否需要设置最低入库质量门槛
```

当前阶段先不引入自动化评分脚本、不接入外部项目真实使用日志、不设置自动批准门槛。所有质量分只作为审计、采集优先级和回归判断依据。

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase16_knowledge_quality_eval.md
```

## 进度记录

```yaml
current_status: done
completed_tasks:
  - CEK-TA-062
  - CEK-TA-063
  - CEK-TA-064
deliverables:
  - codex-expert-kit/rag/quality_metrics.md
  - codex-expert-kit/rag/eval_sets/README.md
  - codex-expert-kit/rag/eval_sets/retrieval_eval_cases.json
  - codex-expert-kit/rag/eval_sets/qa_eval_cases.json
  - codex-expert-kit/rag/eval_sets/tree_routing_eval_cases.json
  - codex-expert-kit/templates/knowledge_quality_report.md
remaining_tasks: []
notes:
  - Phase 16 已把 Phase 18 的 v2 canonical_node_id、alias、routing_policy 纳入评测体系。
  - 本阶段未引入数据库、外部评测服务或自动化审批。
  - 本阶段未采集实时行情、K线或订单数据。
```
