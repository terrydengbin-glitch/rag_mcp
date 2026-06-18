# Phase 2.5 知识采集与冲突审计任务卡

## Phase 目标

建立 CEK-TA 知识进入 RAG 之前的审计契约，确保每条专业知识都满足：

```text
有来源
有分类
有适用边界
有来源质量评分
有冲突检测结果
有审计状态
```

Phase 2.5 是 Phase 2 RAG 知识库结构和 Phase 3 Knowledge MCP、Phase 7 Vue3 审计界面、Phase 9 知识倒灌之间的质量闸门。

## 任务列表

| ID | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- |
| CEK-TA-022 | done | 建立知识采集与审计规范 | `docs/知识库采集与审计规范.md` |
| CEK-TA-023 | done | 定义知识条目结构化 schema | `codex-expert-kit/rag/knowledge_item_schema.md` |
| CEK-TA-024 | done | 定义冲突检测规则 | `codex-expert-kit/rag/conflict_detection_rules.md` |
| CEK-TA-025 | done | 定义来源质量评分 | `codex-expert-kit/rag/source_quality_rules.md` |
| CEK-TA-026 | done | 定义 Codex 联网采集任务模板 | `codex-expert-kit/templates/research_task_card.md` |

## 上游输入

```text
docs/知识库采集与审计规范.md
codex-expert-kit/rag/kb_partitions.md
codex-expert-kit/rag/metadata_schema.md
codex-expert-kit/rag/chunking_rules.md
codex-expert-kit/rag/retrieval_policy.md
docs/知识倒灌与反哺规范.md
```

## 下游输出

```text
Phase 3 Knowledge MCP:
  使用 knowledge_item_schema、conflict_detection_rules、source_quality_rules 作为 MCP 返回值和过滤依据。

Phase 7 Vue3 知识审计界面:
  使用知识条目字段、冲突审计状态、来源评分字段渲染审计工作台。

Phase 9 知识倒灌与反哺:
  使用同一套 schema、来源评分和冲突规则判断项目经验能否进入通用知识库。

业务项目接入:
  使用 research_task_card 模板发起联网采集和知识反哺任务。
```

## 输入契约

新增知识或倒灌知识进入 Phase 2.5 时，必须提供：

```text
1. 明确的问题或规则候选。
2. domain、subdomain、partition_id 候选。
3. 至少一个可追踪来源。
4. 适用市场、资产、周期、数据粒度和项目类型。
5. 前置假设和不适用场景。
6. 与已有知识的候选冲突列表，或说明尚未检索。
```

## 输出契约

Phase 2.5 输出的知识审计结果必须包含：

```text
1. 标准知识条目对象。
2. 来源质量评分。
3. 冲突检测结果。
4. 适用边界和默认推荐规则。
5. review_status。
6. 是否可进入 RAG、Skill、MCP、Vue3 审计界面。
7. 未解决问题和人工确认项。
```

## 边界范围

本 Phase 做：

```text
1. 定义知识条目 schema。
2. 定义冲突检测分类、流程和输出格式。
3. 定义来源质量评分规则。
4. 定义联网采集任务模板。
5. 回写任务索引和任务卡状态。
```

本 Phase 不做：

```text
1. 不实际采集某一条交易专业知识。
2. 不实现数据库。
3. 不实现 MCP server。
4. 不实现 Vue3 页面。
5. 不改变 Phase 顺序和任务 ID。
6. 不接受存在未消解理论冲突的 approved 知识。
```

## 涉及组件

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase2_5_knowledge_audit.md
codex-expert-kit/rag/knowledge_item_schema.md
codex-expert-kit/rag/conflict_detection_rules.md
codex-expert-kit/rag/source_quality_rules.md
codex-expert-kit/templates/research_task_card.md
```

## 涉及数据结构

```text
knowledge_item
source_evidence
source_quality_score
conflict_audit
review_state
research_task
```

## 涉及数据库/存储

当前 Phase 不引入数据库。所有契约先以 Markdown + JSON 示例形式落地，后续如进入数据库设计，必须在新 Phase 或新任务卡中定义主键、索引、迁移和回滚。

## 实施步骤

```text
1. 创建 Phase 2.5 任务卡。
2. 定义 knowledge_item_schema。
3. 定义 conflict_detection_rules。
4. 定义 source_quality_rules。
5. 定义 research_task_card 模板。
6. 更新 docs/index_tasks.md 与 docs/tasks/README.md。
7. 执行文件存在性、关键章节、状态一致性和 UTF-8 读取检查。
```

## Definition of Done

```text
1. Phase 2.5 任务卡存在，并包含上下游、契约、边界、DoD 和测试。
2. knowledge_item_schema.md 存在，并能覆盖 metadata、content、evidence、audit、conflict、contribution。
3. conflict_detection_rules.md 存在，并定义冲突类型、检测流程、消解规则和输出格式。
4. source_quality_rules.md 存在，并定义来源等级、评分维度、降级规则和刷新要求。
5. research_task_card.md 存在，并能指导 Codex 做联网采集、来源记录、冲突检查和入库建议。
6. docs/index_tasks.md 和 docs/tasks/README.md 状态一致。
7. 中文文档 UTF-8 读取无乱码。
8. 未引入数据库、后端框架、外部服务或不可逆迁移。
```

## 测试与验收

文档任务测试：

```text
1. Test-Path 检查全部交付物存在。
2. Select-String 检查关键章节存在。
3. Get-Content -Encoding UTF8 检查中文文档可读。
4. 检查 Phase 2.5 在 docs/index_tasks.md 与 docs/tasks/README.md 中均为 done。
5. 检查 CEK-TA-023 到 CEK-TA-026 均为 done。
```

## 风险与回滚

风险：

```text
1. schema 过宽会导致 Vue3 和 MCP 难以实现。
2. schema 过窄会导致知识倒灌时信息丢失。
3. 来源评分如果不区分适用边界，会把权威但不适用的资料误判为高质量规则。
```

回滚：

```text
1. 文档型变更可通过版本控制回退。
2. 如后续数据库实现发现字段不合理，先新增 schema version，不直接破坏已有 knowledge_id。
3. 已批准知识不得因 schema 改版直接删除，只能 deprecated 或迁移。
```

## 需要开发者确认的问题

当前 Phase 不涉及重大决策，无需确认。后续如要把这些 schema 固化为数据库表、MCP 写接口或 Vue3 信息架构，需要单独向开发者确认。

## 状态更新要求

完成后必须更新：

```text
docs/index_tasks.md
docs/tasks/README.md
docs/tasks/phase2_5_knowledge_audit.md
```
