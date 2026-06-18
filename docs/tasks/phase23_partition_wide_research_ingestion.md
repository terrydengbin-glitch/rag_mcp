# Phase 23: 13 分区全网专业知识采集

## Phase 目标

围绕 `kb_partitions_v2.md` 中 13 个正式分区，建立可持续的全网专业知识采集任务体系。Phase 23 不直接把搜索结果写入 approved 知识库，而是把每个分区拆成可审计的 ResearchIngestionTask、来源种子、候选知识包和质量验收结果。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-097 | P0 | done | 定义 13 分区采集矩阵 | `docs/research/phase23_partition_collection_plan.md` |
| CEK-TA-098 | P0 | done | 建立首批可信来源种子库 | `docs/research/phase23_source_seed_catalog.md` |
| CEK-TA-099 | P0 | done | 为 13 分区生成 ResearchIngestionTask 队列 | `docs/research/phase23_research_task_queue.md` |
| CEK-TA-100 | P1 | done | 按队列执行首批联网采集并生成候选包 | `codex-expert-kit/rag/candidates/` |
| CEK-TA-101 | P1 | done | 对候选包执行来源评分、冲突检测和人工审计问题整理 | `docs/reports/phase23_candidate_quality_report.md` |
| CEK-TA-102 | P1 | done | 将 accepted 候选转换为正式知识 draft 并重建索引 | `codex-expert-kit/rag/knowledge/`、`codex-expert-kit/rag/indexes/knowledge_items.json` |

## 上游输入

```text
1. codex-expert-kit/rag/kb_partitions_v2.md
2. codex-expert-kit/rag/knowledge_tree_v2.md
3. codex-expert-kit/rag/ingestion_candidate_schema.md
4. codex-expert-kit/templates/research_ingestion_runbook.md
5. codex-expert-kit/rag/source_quality_rules.md
6. codex-expert-kit/rag/conflict_detection_rules.md
7. codex-expert-kit/rag/quality_metrics.md
8. AGENTS.md 路径 resolver、UTF-8、知识入库规范
```

## 下游输出

```text
1. 13 分区采集矩阵，供后续联网采集调度。
2. 可信来源种子库，供 Codex 搜索、引用和来源评分。
3. ResearchIngestionTask 队列，供每轮采集生成候选包。
4. IngestionCandidate 候选包，供 Vue3 审计工作台、质量评测和人工审核。
5. accepted 候选转换出的正式知识 draft，供 MCP/RAG 检索。
```

## 输入契约

每个分区采集任务必须包含：

```yaml
research_task_id: string
partition_id: KB_XX_...
canonical_root: string
target_node_id: string
topic: string
question_set: []
source_policy:
  preferred_source_types: []
  minimum_reliability: medium | high
freshness_requirement: stable | time_sensitive
conflict_check_scope: []
expected_outputs: []
forbidden_content: []
```

## 输出契约

每次联网采集只能输出：

```text
1. SourceRef 来源记录。
2. 结构化 claim。
3. IngestionCandidate 候选知识包。
4. 冲突审计记录。
5. 人工审计问题。
6. 质量报告。
```

禁止直接输出：

```text
1. approved 知识。
2. 无来源知识。
3. 没有适用边界的交易规则。
4. 未解决冲突的默认指导。
5. 行情数据、K线原始数据、订单簿原始数据。
6. 项目私有策略阈值、账户配置、密钥或未脱敏交易记录。
```

## 边界范围

范围内：

```text
1. 采集专业交易工程、AI 工程、项目接入和知识治理知识。
2. 使用全网公开资料、官方文档、论文、框架文档、交易所规则、工程文章和内部 runbook。
3. 为每条候选知识建立来源、适用范围、不适用场景、冲突状态和审计状态。
4. 按 13 个 KB 分区组织任务和候选包。
```

范围外：

```text
1. 不采集实时行情、K线数据或订单流原始数据。
2. 不生成投资建议、推荐杠杆、推荐标的或收益承诺。
3. 不接入新的数据库、外部采集服务或付费数据源。
4. 不改变 MCP 权限，不开放写入工具。
5. 不把候选知识直接作为其他项目默认指导。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase23_partition_wide_research_ingestion.md
docs/research/phase23_partition_collection_plan.md
docs/research/phase23_source_seed_catalog.md
docs/research/phase23_research_task_queue.md
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/views/IngestionReview.vue
ui/src/views/SearchLab.vue
```

## 涉及数据结构

```text
ResearchIngestionTask
IngestionCandidate
SourceRef
KnowledgeItem
SearchResult
QualityReport
```

## 涉及数据库/存储

当前 Phase 不引入数据库。候选包和任务队列先使用文件化存储。

```text
docs/research/
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/knowledge/
codex-expert-kit/rag/indexes/
```

## 实施步骤

```text
1. 创建 Phase 23 任务卡。
2. 更新 docs/index_tasks.md 和 docs/tasks/README.md。
3. 创建 13 分区采集矩阵。
4. 建立首批可信来源种子库。
5. 生成 13 分区 ResearchIngestionTask 队列。
6. 从 P0 分区开始执行联网采集。
7. 每个任务生成候选包，不直接 approved。
8. 执行来源评分、冲突检测、质量评测。
9. 人工审核后把 accepted 候选转换为正式知识 draft。
10. 重建 knowledge_items.json 并运行 MCP/SearchLab 回归。
```

## Definition of Done

```text
1. Phase 23 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记任务卡。
3. 13 个 KB 分区均有采集目标、来源策略、禁采内容和验收条件。
4. 首批来源种子库覆盖交易工程、AI 工程、项目接入和治理。
5. ResearchIngestionTask 队列至少覆盖每个分区 1 个 P0/P1 任务。
6. 候选知识不自动进入 approved。
7. 所有中文文档保持 UTF-8。
8. 如进入正式知识 draft，必须重建索引并运行 MCP/SearchLab 检索测试。
```

## 测试与验收

文档验收：

```text
1. UTF-8 读取无乱码。
2. docs/index_tasks.md 包含 Phase 23。
3. docs/tasks/README.md 包含 Phase 23。
4. 采集矩阵覆盖 13 个分区。
5. 队列中的 partition_id 都存在于 kb_partitions_v2.md。
6. 队列中的 target_node_id 能映射到 knowledge_tree_v2.md。
```

候选包验收：

```text
1. 每个候选包符合 ingestion_candidate_schema.md。
2. source_refs 非空。
3. applies_when、not_applicable_when、assumptions 非空。
4. conflict_audit 已执行。
5. review_status 不得直接为 approved。
```

正式知识验收：

```text
1. draft/reviewed/approved 状态流正确。
2. source_evidence、source_quality、conflict_audit 完整。
3. knowledge_items.json 重建成功。
4. MCP/SearchLab 能命中并返回来源。
5. 无来源、冲突、过期、rejected 知识被阻断。
```

## 风险与回滚

风险：

```text
1. 全网资料质量不一，容易引入低质量经验贴。
2. 交易知识存在市场、周期、成本、数据粒度差异，容易产生伪通用规则。
3. time_sensitive 官方文档可能过期。
4. 版权资料不能大段复制。
```

回滚：

```text
1. 删除或隔离候选包，不影响正式知识库。
2. 将问题候选状态改为 rejected 或 needs_more_evidence。
3. 如正式知识 draft 有误，移出 knowledge 目录并重建索引。
4. 保留采集任务和审计记录，便于复盘。
```

## 需要开发者确认的问题

```text
1. 是否允许后续引入外部搜索 API 或采集服务？当前 Phase 默认不引入。
2. 是否需要为人工审计指定 reviewer 名称？当前默认 reviewer 为 mixed/human 待确认。
3. 是否优先采集交易工程 8 个分区，还是 13 个分区并行推进？当前任务队列按 P0/P1 分批推进。
```

## 状态更新要求

完成任一子任务后必须更新：

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. 本任务卡任务列表状态
4. docs/research/phase23_research_task_queue.md 对应任务状态
5. 如生成正式知识，重建 codex-expert-kit/rag/indexes/knowledge_items.json
```
