# Phase 12: 专业知识采集流水线任务卡

## Phase 目标

建立 Codex 联网搜索、来源评估、观点抽取、结构化归类、冲突检测、候选入库和人工审计的专业知识采集流水线，让大量有价值的交易、回测、风控、执行、LLM/RAG 知识可以持续沉淀到 CEK-TA。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-050 | P0 | done | 定义研究采集任务运行规范 | `codex-expert-kit/templates/research_ingestion_runbook.md` |
| CEK-TA-051 | P0 | done | 定义候选知识入库包结构 | `codex-expert-kit/rag/ingestion_candidate_schema.md` |
| CEK-TA-052 | P1 | done | 创建首批专业主题采集 backlog | `docs/knowledge_research_backlog.md` |

## 上游输入

```text
codex-expert-kit/templates/research_task_card.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/knowledge_tree.md
docs/知识库采集与审计规范.md
```

## 下游输出

```text
候选知识入库包
Vue3 候选知识审计队列
Phase 13 RAG 数据层
Phase 16 知识质量评测
Phase 17 首批知识资产
```

## 输入契约

采集任务必须声明：

```text
research_task_id
topic
target_node_id
domain
question_set
source_policy
freshness_requirement
must_include_sources
must_exclude_sources
conflict_check_scope
reviewer
```

## 输出契约

候选知识包必须包含：

```text
candidate_id
research_task_id
tree_node_id
claim
evidence_summary
source_refs
source_quality_score
applicable_scope
not_applicable_scope
conflict_candidates
confidence
freshness
review_status
ingestion_decision
```

## 边界范围

范围内：

```text
定义采集流程
定义候选知识结构
定义专业主题 backlog
定义来源与冲突审计步骤
```

范围外：

```text
不把联网搜索结果直接写入 approved
不采集无来源内容
不采集行情数据、K线数据或订单流原始数据
不复制大段版权内容
不采集项目私有数据
不绕过人工审计
```

## 涉及组件

```text
codex-expert-kit/templates/
codex-expert-kit/rag/
docs/
contributions/
ui/src/views/
```

## 涉及数据结构

```text
ResearchIngestionTask
IngestionCandidate
SourceRef
ExtractedClaim
ConflictCandidate
ReviewDecision
```

## 涉及数据库/存储

第一阶段使用文件化候选包。候选包不得直接进入正式知识库。若后续接入 RAGFlow、向量库或数据库，需要 Phase 13 单独定义存储契约。

## 实施步骤

1. 编写采集 runbook，明确搜索、阅读、摘要、抽取、归类、冲突检测流程。
2. 定义候选知识入库包 schema。
3. 创建第一批专业主题 backlog。
4. 将采集流程与知识树节点绑定。
5. 更新任务索引。

## Definition of Done

```text
采集流程可重复执行
候选知识包字段完整
每个候选知识必须有来源
每个候选知识必须绑定知识树节点
每个候选知识必须有适用和不适用范围
冲突检测入口明确
版权与引用边界明确
UTF-8 中文无乱码
```

## 测试与验收

```text
检查 runbook 章节完整
检查 candidate schema 字段完整
检查 backlog 至少覆盖回测知识、K线交易知识、风控知识、执行知识、LLM/RAG 知识
使用一个样例主题走通纸面流程
检查无 approved 自动入库路径
使用 Get-Content -Encoding UTF8 检查中文显示
```

## 风险与回滚

风险：

```text
搜索来源质量不稳定
不同资料存在理论冲突
采集内容过多但不可审计
版权内容引用过长
```

回滚：

```text
候选知识保持 proposed/review 状态
不进入正式 RAG 索引
删除候选包不影响已批准知识
```

## 需要开发者确认的问题

```text
是否允许 Codex 按 backlog 主动联网采集
是否指定优先知识来源类型
是否需要先限制第一批主题数量
```

## 状态更新要求

完成后更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase12_research_ingestion_pipeline.md
```

## 完成记录

```text
completed_at: 2026-06-08
completed_tasks:
  - CEK-TA-050
  - CEK-TA-051
  - CEK-TA-052
deliverables:
  - codex-expert-kit/templates/research_ingestion_runbook.md
  - codex-expert-kit/rag/ingestion_candidate_schema.md
  - docs/knowledge_research_backlog.md
validation:
  - 检查 runbook、candidate schema、backlog 文件存在
  - 检查 candidate schema 必要字段、状态流和无自动 approved 路径
  - 检查 backlog 覆盖回测知识、K线交易知识、风控知识、执行知识、LLM/RAG 知识
  - 使用 UTF-8 读取中文文档
notes:
  - 本 Phase 只建立专业交易知识采集流水线和候选包契约，未采集行情/K线数据，未创建 approved 知识
```
