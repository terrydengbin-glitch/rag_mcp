# Phase 2 任务卡：RAGFlow 知识库接入

## 基本信息

| 字段 | 内容 |
| --- | --- |
| Phase | Phase 2 |
| 名称 | RAGFlow 知识库接入 |
| 当前状态 | done |
| 主目标 | 定义 CEK-TA 专业知识库分区、metadata、chunking 和 retrieval policy，使 Codex 后续可以通过 RAG/MCP 检索专业知识 |
| 上游 Phase | Phase 1 Codex Expert Kit 骨架 |
| 下游 Phase | Phase 2.5 知识采集与冲突审计、Phase 3 Knowledge MCP、Phase 7 Vue3 审计界面 |

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-006 | P0 | done | 定义知识库分区 | `codex-expert-kit/rag/kb_partitions.md` |
| CEK-TA-007 | P0 | done | 定义 metadata schema | `codex-expert-kit/rag/metadata_schema.md` |
| CEK-TA-008 | P1 | done | 定义 chunking rules | `codex-expert-kit/rag/chunking_rules.md` |
| CEK-TA-009 | P1 | done | 定义 retrieval policy | `codex-expert-kit/rag/retrieval_policy.md` |

## 上游输入

| 输入 | 来源 | 用途 |
| --- | --- | --- |
| 项目治理规范 | `AGENTS.md` | 约束任务卡、契约、DoD、UTF-8 |
| Phase 1 骨架 | `codex-expert-kit/` | 提供 `rag/` 承载目录 |
| 知识采集规范 | `docs/知识库采集与审计规范.md` | 定义来源、冲突、审计要求 |
| 总体框架 | `docs/需求框架.md` | 定义知识库目标和推荐 KB 分区 |

## 下游输出

| 输出 | 消费方 | 用途 |
| --- | --- | --- |
| `kb_partitions.md` | CEK-TA-007、Phase 3、Vue3 UI | 决定 metadata domain、检索过滤和 UI 分类 |
| `metadata_schema.md` | Phase 2.5、Phase 3 | 约束知识条目结构 |
| `chunking_rules.md` | RAG ingestion | 约束文档切分 |
| `retrieval_policy.md` | MCP 检索工具 | 约束搜索、过滤、rerank、citation |

## 输入契约

Phase 2 不采集具体专业知识，只定义知识库结构契约。

```text
1. 不写入具体交易理论细节。
2. 不写入业务项目私有字段。
3. 不连接真实 RAGFlow/Qdrant。
4. 不引入数据库或外部服务。
5. 所有分区必须能映射到 domain/subdomain metadata。
```

## 输出契约

CEK-TA-006 完成后必须存在：

```text
codex-expert-kit/rag/kb_partitions.md
```

该文件必须包含：

```text
分区 ID
分区名称
domain
用途
允许内容
禁止内容
典型 source_type
适用下游
审计要求
```

CEK-TA-007 完成后必须存在：

```text
codex-expert-kit/rag/metadata_schema.md
```

该文件必须定义：

```text
knowledge_id
partition_id
domain/subdomain
source/source_type
project_binding
applies_to
used_for
assumptions
not_applicable_when
conflict_status
confidence
freshness
review_status
created_at/updated_at
```

CEK-TA-008 完成后必须存在：

```text
codex-expert-kit/rag/chunking_rules.md
```

该文件必须定义 Markdown、schema、code、task card/runbook 和 conflict-aware chunking 规则。

CEK-TA-009 完成后必须存在：

```text
codex-expert-kit/rag/retrieval_policy.md
```

该文件必须定义 domain routing、metadata filter、review/freshness/conflict/project binding policy 和 retrieval result contract。

## 边界

### CEK-TA-006 范围内

```text
1. 定义知识库分区。
2. 明确每个分区能放什么、不能放什么。
3. 明确分区和 domain 的映射。
4. 明确分区被哪些下游使用。
5. 更新索引和任务卡状态。
```

### CEK-TA-007 范围内

```text
1. 定义知识条目 metadata schema。
2. 明确 required fields。
3. 明确 review_status、freshness、project_binding、conflict_status 语义。
4. 明确 MCP/RAG retrieval 最小返回字段。
```

### CEK-TA-008 范围内

```text
1. 定义默认 chunk size 和 overlap。
2. 定义 Markdown、schema、code、task card/runbook 的切分规则。
3. 定义冲突感知切分规则。
4. 明确禁止丢失 source、review_status、freshness、conflict_status。
```

### CEK-TA-009 范围内

```text
1. 定义 retrieval 默认流程。
2. 定义 domain routing。
3. 定义 metadata filters。
4. 定义 review/freshness/conflict/project binding policy。
5. 定义 retrieval result contract。
```

### Phase 2 当前范围外

```text
1. 不部署 RAGFlow。
2. 不配置 Qdrant。
3. 不实现检索代码。
4. 不采集专业知识。
5. 不批准任何知识条目。
6. 不实现 Vue3 页面。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase2_ragflow_knowledge_base.md
codex-expert-kit/rag/kb_partitions.md
```

## 涉及数据结构

本任务定义 KB partition 结构，不定义完整 metadata schema。完整 schema 属于 CEK-TA-007。

## 涉及数据库/存储

本任务不引入数据库，不创建 RAGFlow/Qdrant 实例，不创建迁移。

## Definition of Done

CEK-TA-006 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/rag/kb_partitions.md` 存在。
2. 至少定义 quant、kline、microstructure、backtest、replay、simulation、live、trade_analysis、llm_training、rag_engineering、project_runbooks 分区。
3. 每个分区包含用途、允许内容、禁止内容、source_type、下游用途和审计要求。
4. 不包含具体未经来源审计的专业知识。
5. `docs/index_tasks.md` 中 Phase 2 状态为 doing。
6. `docs/index_tasks.md` 中 CEK-TA-006 状态为 done。
7. `docs/tasks/README.md` 中 Phase 2 任务卡状态为 doing。
8. 本任务卡中 CEK-TA-006 状态为 done。
9. UTF-8 读取无乱码。
```

CEK-TA-007 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/rag/metadata_schema.md` 存在。
2. schema 覆盖来源、适用范围、冲突、置信度、时效性、审计状态。
3. schema 支持 project_binding，避免业务项目事实污染通用知识。
4. 定义 retrieval output minimum。
5. `docs/index_tasks.md` 和本任务卡中 CEK-TA-007 状态为 done。
```

CEK-TA-008 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/rag/chunking_rules.md` 存在。
2. 规则覆盖 Markdown、schema、code、task card/runbook。
3. 规则要求保留 source、review_status、freshness、conflict_status。
4. `docs/index_tasks.md` 和本任务卡中 CEK-TA-008 状态为 done。
```

CEK-TA-009 只有满足以下条件才能标记 `done`：

```text
1. `codex-expert-kit/rag/retrieval_policy.md` 存在。
2. policy 覆盖 domain routing、metadata filters、ranking、return contract。
3. policy 明确 review_status、freshness、conflict 和 project_binding 使用规则。
4. `docs/index_tasks.md` 和本任务卡中 CEK-TA-009 状态为 done。
```

Phase 2 只有满足以下条件才能标记 `done`：

```text
1. CEK-TA-006 到 CEK-TA-009 均为 done。
2. `docs/index_tasks.md` 中 Phase 2 状态为 done。
3. `docs/tasks/README.md` 中 Phase 2 状态为 done。
4. 本任务卡当前状态为 done。
5. 未部署外部 RAGFlow/Qdrant，未越界实现 Phase 3。
```

## 测试与验收

### 文件存在性测试

```powershell
Test-Path .\docs\tasks\phase2_ragflow_knowledge_base.md
Test-Path .\codex-expert-kit\rag\kb_partitions.md
Test-Path .\codex-expert-kit\rag\metadata_schema.md
Test-Path .\codex-expert-kit\rag\chunking_rules.md
Test-Path .\codex-expert-kit\rag\retrieval_policy.md
```

### 内容完整性测试

检查 `kb_partitions.md` 是否包含：

```text
KB_01_QUANT_FOUNDATION
KB_02_KLINE_STRATEGY
KB_03_MARKET_MICROSTRUCTURE
KB_04_BACKTEST
KB_05_REPLAY_SIMULATION
KB_06_LIVE_EXECUTION
KB_07_TRADE_ANALYSIS
KB_08_LLM_TRAINING
KB_09_RAG_ENGINEERING
KB_10_PROJECT_RUNBOOKS
```

### UTF-8 测试

```powershell
Get-Content -LiteralPath .\docs\tasks\phase2_ragflow_knowledge_base.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\rag\kb_partitions.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\rag\metadata_schema.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\rag\chunking_rules.md -Encoding UTF8
Get-Content -LiteralPath .\codex-expert-kit\rag\retrieval_policy.md -Encoding UTF8
```

## 风险与回滚

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| 分区过细 | 检索和维护复杂 | Phase 2 只定义主分区，subdomain 留给 metadata |
| 分区过粗 | 检索结果混杂 | 每个分区明确允许/禁止内容 |
| 混入业务项目事实 | 污染通用知识库 | 明确禁止内容和 project_binding |

回滚方式：

```text
1. 删除或修订 `kb_partitions.md`。
2. 将 CEK-TA-006 状态改回 todo。
3. 同步回滚 `docs/index_tasks.md` 和本任务卡。
```

## 需要开发者确认的问题

当前无阻塞问题。本任务只定义文档契约，不引入数据库、后端框架、外部服务或不可逆迁移。

## 状态更新要求

完成 Phase 2 后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase2_ragflow_knowledge_base.md
```
