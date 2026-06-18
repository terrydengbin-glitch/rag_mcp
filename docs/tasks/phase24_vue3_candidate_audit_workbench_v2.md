# Phase 24: Vue3 候选知识审计工作台 v2

## Phase 目标

把现有 Vue3 审计界面升级为可承接 Phase 23 大规模候选知识的审计工作台。前端需要支持候选知识查看、来源证据核查、冲突审计、知识树覆盖联动、候选转正式知识 draft 预览、审计决策导出和 SearchLab/MCP 验证衔接。

本 Phase 不把候选知识直接写入正式知识库，不开放 MCP 写权限，不引入数据库或新的后端服务。核心目标是让人工审核能稳定判断：哪些候选可以进入 `CEK-TA-102` 转 draft，哪些需要补证据，哪些必须拒绝或阻断。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-103 | P0 | done | 定义 Vue3 候选审计数据契约与字段映射 | `ui/src/types.ts`、`docs/tasks/phase24_vue3_candidate_audit_workbench_v2.md` |
| CEK-TA-104 | P0 | done | 生成 Phase 23 candidate 前端数据 fixture | `codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`ui/src/data/phase23Candidates.ts` |
| CEK-TA-105 | P0 | done | 重构候选知识审计台 | `ui/src/views/IngestionReview.vue`、必要的局部组件 |
| CEK-TA-106 | P1 | done | 增加来源、冲突、治理、转换预览面板 | `ui/src/components/`、`ui/src/views/IngestionReview.vue` |
| CEK-TA-107 | P1 | done | 增强知识树覆盖联动 | `ui/src/views/KnowledgeTreeView.vue`、`ui/src/stores/auditStore.ts` |
| CEK-TA-108 | P1 | done | 增加审计决策导出与 CEK-TA-102 交接契约 | `ui/src/data/`、`docs/reports/phase24_candidate_audit_handoff.md` |
| CEK-TA-109 | P1 | done | 执行 Vue3 构建、布局和审计链路验收 | `docs/reports/phase24_vue3_candidate_audit_report.md` |

## 上游输入

```text
1. docs/tasks/phase23_partition_wide_research_ingestion.md
2. docs/research/phase23_research_task_queue.md
3. docs/reports/phase23_candidate_quality_report.md
4. codex-expert-kit/rag/candidates/**/*.json
5. codex-expert-kit/rag/ingestion_candidate_schema.md
6. codex-expert-kit/rag/knowledge_item_schema.md
7. codex-expert-kit/rag/source_quality_rules.md
8. codex-expert-kit/rag/conflict_detection_rules.md
9. codex-expert-kit/rag/knowledge_tree_v2.md
10. codex-expert-kit/rag/kb_partitions_v2.md
11. codex-expert-kit/rag/indexes/knowledge_items.json
12. docs/searchlab_mcp_runtime_contract.md
13. AGENTS.md 中的 UTF-8、路径 resolver、Vue3、知识入库和 MCP 只读规范
```

## 下游输出

```text
1. Vue3 审计工作台可加载 Phase 23 候选知识。
2. 人工审核可以按候选、来源、冲突、知识树节点、分区和状态查看。
3. 审计决策可以输出为 CEK-TA-102 使用的 handoff 记录。
4. accepted_for_draft 候选可以进入正式知识 draft 转换流程。
5. draft/approved 后续可进入 MCP/SearchLab 检索验证。
6. 质量报告可以追踪本轮前端是否满足审计链路要求。
```

## 输入契约

### Candidate Fixture 输入

前端候选 fixture 必须从候选 JSON 聚合生成，不能手工维护与候选包矛盾的数据。输入字段至少包含：

```yaml
candidate_id: string
research_task_id: string
partition_id: string
tree_node_id: string
canonical_node_id: string
title: string
claim: string
domain: string
subdomain: string
source_refs: []
source_quality:
  score: number
  reliability: low | medium | high
applies_when: []
not_applicable_when: []
assumptions: []
limitations: []
conflict_audit:
  status: none | potential | confirmed | resolved | unchecked
  checked_against: []
  resolution: string
confidence: low | medium | high
freshness: stable | time_sensitive | deprecated
review_status: proposed | sanitized | sourced | classified | conflict_checked | reviewed | accepted | rejected
candidate_status: candidate_ready | needs_more_evidence | blocked | accepted_for_draft | rejected
updated_at: string
```

### SourceRef 输入

```yaml
source_id: string
title: string
url: string
source_type: official_doc | paper | framework_doc | exchange_rule | engineering_article | internal_runbook | other
publisher: string
published_at: string | null
accessed_at: string
reliability: low | medium | high
score: number
evidence_summary: string
limitations: []
```

### ReviewDecisionDraft 输入

```yaml
candidate_id: string
decision: accepted_for_draft | needs_more_evidence | rejected
reviewer: string
decision_reason: string
required_followups: []
created_at: string
```

## 输出契约

### UI 审计输出

本 Phase 前端只输出审计决策草案，不直接修改候选 JSON 或正式知识库。

```yaml
handoff_id: string
phase: "24"
target_task_id: "CEK-TA-102"
generated_at: string
candidates:
  - candidate_id: string
    decision: accepted_for_draft | needs_more_evidence | rejected
    reason: string
    missing_fields: []
    blocking_issues: []
    target_knowledge_preview:
      proposed_knowledge_id: string
      review_status: draft
      domain: string
      subdomain: string
      tree_node_id: string
      canonical_node_id: string
```

### KnowledgeItem 转换预览

候选转正式知识 draft 的预览必须明确：

```text
1. source_refs 是否完整。
2. applies_when、not_applicable_when、assumptions 是否非空。
3. conflict_audit 是否为 none 或 resolved。
4. freshness 是否需要后续复审。
5. review_status 只能预览为 draft，不能预览为 approved。
```

## 边界范围

范围内：

```text
1. Vue3 展示真实候选知识、来源、冲突和知识树覆盖。
2. 用 fixture 或本地静态数据承接文件化候选包。
3. 建立候选审计到 CEK-TA-102 的 handoff 契约。
4. 增强 SearchLab/MCP 验证前的可视化准备。
5. 增加 loading、empty、error、筛选、排序、移动端和桌面端布局。
```

范围外：

```text
1. 不引入数据库。
2. 不引入新的后端框架。
3. 不开放 MCP 写权限。
4. 不让浏览器直接写入 codex-expert-kit/rag/candidates/ 或 knowledge/。
5. 不把候选知识直接变成 approved。
6. 不采集行情、K 线、订单簿或任何交易原始数据。
7. 不接入外部搜索 API 或付费数据源。
```

## 涉及组件

```text
ui/src/types.ts
ui/src/stores/auditStore.ts
ui/src/data/phase23Candidates.ts
ui/src/views/IngestionReview.vue
ui/src/views/KnowledgeTreeView.vue
ui/src/views/SearchLab.vue
ui/src/components/
codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
docs/reports/phase24_candidate_audit_handoff.md
docs/reports/phase24_vue3_candidate_audit_report.md
```

## 涉及数据结构

```text
IngestionCandidate
SourceRef
ConflictAudit
KnowledgeTreeNode
CandidateCoverageSummary
ReviewDecisionDraft
CandidateAuditHandoff
KnowledgeItemPreview
```

## 涉及数据库/存储

当前 Phase 不引入数据库。数据仍使用文件化存储和前端静态 fixture。

```text
codex-expert-kit/rag/candidates/
codex-expert-kit/rag/indexes/knowledge_items.json
ui/src/data/
docs/reports/
```

新增脚本读取仓库路径时必须使用：

```text
codex-expert-kit/core/path_resolver.py
```

禁止在脚本或配置中硬编码开发机绝对路径。

## 实施步骤

```text
1. 补齐 Phase 24 任务卡、docs/index_tasks.md 和 docs/tasks/README.md。
2. 对齐 candidate JSON、KnowledgeItem、SourceRef、ConflictAudit 与 Vue3 类型。
3. 实现 candidate fixture 生成脚本，使用 path resolver 定位输入和输出。
4. 让 auditStore 加载真实 Phase 23 候选 fixture。
5. 重构 IngestionReview 为候选审计台：列表、详情、筛选、排序、风险提示。
6. 增加来源证据、冲突审计、治理检查、转换预览面板。
7. 增强 KnowledgeTreeView，展示正式知识和候选知识覆盖。
8. 增加审计决策导出或 handoff 文档生成规则。
9. 运行 Vue3 build、fixture 生成和基本数据校验。
10. 生成 Phase 24 验收报告。
```

## Definition of Done

```text
1. Phase 24 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 24。
3. 本任务卡已创建，包含上下游、契约、边界、DoD 和测试。
4. Vue3 能展示 Phase 23 的真实候选知识。
5. 审计员能查看来源、冲突、适用边界、不适用场景和转换预览。
6. 候选知识不会被 UI 展示为 approved 或默认 MCP 指导。
7. 审计决策能交给 CEK-TA-102。
8. `npm run build` 通过，或明确记录无法执行原因。
9. fixture 生成脚本使用 path resolver，无硬编码绝对路径。
10. 中文文档和界面文案保持 UTF-8，无乱码。
```

## 测试与验收

文档验收：

```text
1. UTF-8 读取无乱码。
2. docs/index_tasks.md 包含 Phase 24。
3. docs/tasks/README.md 包含 Phase 24。
4. 本任务卡包含规定章节。
```

数据验收：

```text
1. candidate fixture 可以从 codex-expert-kit/rag/candidates/ 生成。
2. candidate_id 唯一。
3. source_refs 非空候选才能进入 accepted_for_draft。
4. conflict_audit 为 confirmed 或 unchecked 时不能进入 accepted_for_draft。
5. applies_when、not_applicable_when、assumptions 缺失时必须提示补齐。
```

Vue3 验收：

```text
1. `npm run build` 通过。
2. 候选列表、详情、来源、冲突、转换预览均可渲染。
3. loading、empty、error 状态可展示。
4. 桌面端和移动端布局不出现文字重叠。
5. 知识树节点可以联动候选筛选。
6. SearchLab 不把 candidate 当作 approved 默认检索结果。
```

## 风险与回滚

风险：

```text
1. 候选 JSON 字段和现有 Vue3 类型不一致，导致类型映射复杂。
2. 前端如果直接展示候选为可用知识，可能误导其他项目。
3. fixture 手工维护会和候选包产生漂移。
4. 过早引入后端或数据库会扩大边界。
```

回滚：

```text
1. 移除 ui/src/data/phase23Candidates.ts，恢复 mockData 展示。
2. 回退 IngestionReview、KnowledgeTreeView、auditStore 的 Phase 24 改动。
3. 删除或隔离错误 handoff 报告，不影响正式知识库。
4. 保留候选包原文件，不修改 codex-expert-kit/rag/candidates/。
```

## 需要开发者确认的问题

```text
1. Phase 24 第一版是否只做静态 fixture 和审计导出，不引入后端？当前默认是。
2. 审计决策 reviewer 是否需要固定用户名，还是允许前端填写？当前默认允许填写。
3. CEK-TA-102 接收 handoff 时，是读取 Markdown 报告还是 JSON 文件？当前默认先生成 Markdown 报告，后续可补 JSON。
4. 是否允许在后续版本增加本地只读 API 服务？当前 Phase 默认不引入。
```

## 状态更新要求

完成任一子任务后必须更新：

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. 本任务卡任务列表状态
4. 如新增报告，更新 docs/index_tasks.md 文档入口
5. 如改动前端，执行并记录 Vue3 build 结果
```
