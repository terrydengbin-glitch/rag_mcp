# Phase 29: 候选知识人工审核阅读体验优化

## Phase 目标

把现有候选知识审计页升级为更适合人工阅读、判断和交接的审核工作台。当前 Phase 不改变候选知识生命周期，不开放浏览器写正式知识库，不改变 MCP 只读权限；重点优化候选页面的信息架构、阅读密度、审核步骤、风险提示、来源核查、冲突核查和 CEK-TA-102 交接可读性。

本 Phase 的目标是让审计员能快速回答：

```text
1. 这条候选知识讲的是什么？
2. 它来自哪里，来源是否可靠？
3. 是否有冲突、过期、无来源或边界不清问题？
4. 应该归到知识树哪个节点？
5. 是否可以进入 accepted_for_draft？
6. 如果不能，缺什么证据或需要什么人工动作？
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-134 | P0 | done | 创建 Phase 29 任务卡并登记任务索引 | `docs/tasks/phase29_candidate_audit_readability_workbench.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-135 | P0 | done | 对齐候选审核页上下游、状态流和人工审核契约 | `docs/contracts/candidate_audit_readability_contract.md` |
| CEK-TA-136 | P0 | done | 重构候选页为“队列、正文、证据、审计动作”阅读布局 | `ui/src/views/IngestionReview.vue`、`ui/src/styles.css`、必要组件 |
| CEK-TA-137 | P0 | done | 增加候选审核 DoD 检查清单和阻断原因可视化 | `ui/src/components/`、`ui/src/views/IngestionReview.vue` |
| CEK-TA-138 | P1 | done | 增强候选筛选、批量阅读、分页和上千候选预留 | `ui/src/views/IngestionReview.vue`、`ui/src/stores/auditStore.ts` |
| CEK-TA-139 | P1 | done | 对齐 FastAPI/fixture 候选读取入口和只读错误契约 | `codex-expert-kit/api/`、`ui/src/services/`、`docs/contracts/candidate_audit_readability_contract.md` |
| CEK-TA-140 | P1 | done | 增加 Vue3 build、Playwright 桌面/移动端和审核链路验收 | `ui/tests/e2e/audit-workbench.spec.ts`、`docs/reports/phase29_candidate_audit_readability_report.md` |

## 上游输入

```text
1. docs/tasks/phase23_partition_wide_research_ingestion.md
2. docs/tasks/phase24_vue3_candidate_audit_workbench_v2.md
3. docs/reports/phase23_candidate_quality_report.md
4. docs/reports/phase24_candidate_audit_handoff.md
5. codex-expert-kit/rag/candidates/**/*.json
6. codex-expert-kit/rag/ingestion_candidate_schema.md
7. codex-expert-kit/rag/knowledge_item_schema.md
8. codex-expert-kit/rag/source_quality_rules.md
9. codex-expert-kit/rag/conflict_detection_rules.md
10. codex-expert-kit/rag/knowledge_tree_v2.md
11. codex-expert-kit/rag/indexes/knowledge_items.json
12. docs/contracts/knowledge_tree_reading_api_contract.md
13. docs/contracts/knowledge_tree_fastapi_runtime_plan.md
14. ui/src/views/IngestionReview.vue
15. ui/src/data/phase23Candidates.ts
16. ui/src/data/candidateHandoff.ts
17. AGENTS.md 中的 UTF-8、path resolver、Vue3、MCP/API 只读和知识入库规则
```

## 下游输出

```text
1. 人工审核员可以更高效阅读候选知识、证据、冲突、边界和转 draft 预览。
2. CEK-TA-102 可以继续消费 accepted_for_draft handoff，不需要改变正式入库脚本。
3. KnowledgeTreeView 可以继续通过 tree_node_id 跳转候选页查看对应候选。
4. SearchLab/MCP 验证链路继续只消费正式知识或指定测试输入，不把 candidate 当 approved。
5. 后续如果引入候选只读 API，有清晰的输入、输出和错误契约。
6. Playwright 可以回归候选页桌面端、移动端和过滤跳转可用性。
```

## 输入契约

### CandidateReadableViewModel

候选页可以继续从 `IngestionCandidate` 派生阅读型 view model，但不能丢失原始审计字段。

```yaml
candidate_id: string
title: string
claim: string
summary: string
partition_id: string
tree_node_id: string
canonical_node_id: string
tree_path: string
candidate_status: candidate_ready | needs_more_evidence | blocked | accepted_for_draft | rejected
review_status: proposed | sanitized | sourced | classified | conflict_checked | reviewed | accepted | rejected
ingestion_decision: accepted_for_draft | needs_more_evidence | rejected | blocked
risk_level: low | medium | high | blocked
risk_reasons: string[]
source_count: number
source_quality_score: number
source_reliability: low | medium | high
conflict_status: none | potential | confirmed | resolved | unchecked
freshness: stable | time_sensitive | deprecated
applies_when: string[]
not_applicable_when: string[]
assumptions: string[]
limitations: string[]
missing_fields: string[]
blocking_issues: string[]
conversion_preview:
  proposed_knowledge_id: string
  target_review_status: draft
  can_convert_to_draft: boolean
```

### CandidateAuditChecklist

每条候选知识必须展示人工审核 checklist，供审计员判断是否满足进入 draft 的最低条件。

```yaml
candidate_id: string
checks:
  - key: has_sources
    label: string
    status: pass | warning | fail
    reason: string
  - key: source_quality
    label: string
    status: pass | warning | fail
    reason: string
  - key: conflict_checked
    label: string
    status: pass | warning | fail
    reason: string
  - key: scope_defined
    label: string
    status: pass | warning | fail
    reason: string
  - key: tree_classified
    label: string
    status: pass | warning | fail
    reason: string
  - key: draft_ready
    label: string
    status: pass | warning | fail
    reason: string
```

## 输出契约

### UI 审核输出

本 Phase 不要求浏览器真正写入候选 JSON。前端可以继续下载或预览 handoff。

```yaml
handoff_id: string
target_task_id: CEK-TA-102
generated_at: string
filters:
  partition_id: string | all
  tree_node_id: string | null
  candidate_status: string | all
  conflict_status: string | all
  risk_level: string | all
candidates:
  - candidate_id: string
    decision: accepted_for_draft | needs_more_evidence | rejected | blocked
    decision_reason: string
    blocking_issues: string[]
    missing_fields: string[]
    target_knowledge_preview:
      proposed_knowledge_id: string
      review_status: draft
      canonical_node_id: string
```

### API/Fixture 只读错误契约

如果本 Phase 对齐 FastAPI 候选读取入口，接口必须只读，并返回稳定错误结构。

```yaml
error:
  code: string
  message: string
  details: object
  retryable: boolean
```

## 边界范围

范围内：

```text
1. 优化候选页信息架构和视觉阅读体验。
2. 增加候选正文、证据、冲突、边界、归类、转换预览的分区展示。
3. 增加审核 checklist、阻断原因和下一步动作提示。
4. 支持从知识树带 tree_node_id 跳转后快速查看候选。
5. 保留 JSON/Markdown handoff 导出能力。
6. 为上千候选预留分页、搜索、排序、批量阅读或虚拟列表结构。
7. 对齐 FastAPI/fixture 只读候选读取入口和错误契约。
8. 增加桌面端和移动端 Playwright 验收。
```

范围外：

```text
1. 不把候选知识直接写入正式 knowledge 目录。
2. 不把 candidate、proposed、draft 展示为 approved。
3. 不改变 CEK-TA-102 转 draft 的核心规则。
4. 不开放 MCP 写权限。
5. 不引入数据库。
6. 不引入新的外部服务。
7. 不采集行情、K 线、订单簿或交易原始数据。
8. 不改变知识树主枝、分区和专题的治理规则。
```

## 涉及组件

```text
ui/src/views/IngestionReview.vue
ui/src/components/CandidateSourcePanel.vue
ui/src/components/CandidateConflictPanel.vue
ui/src/components/CandidateGovernancePanel.vue
ui/src/components/CandidateConversionPanel.vue
ui/src/stores/auditStore.ts
ui/src/types.ts
ui/src/data/phase23Candidates.ts
ui/src/data/candidateHandoff.ts
ui/src/services/
ui/src/styles.css
ui/tests/e2e/audit-workbench.spec.ts
codex-expert-kit/api/
docs/contracts/
docs/reports/
```

## 涉及数据结构

```text
IngestionCandidate
CandidateReadableViewModel
CandidateAuditChecklist
SourceRef
ConflictAudit
KnowledgeItemPreview
CandidateAuditHandoff
KnowledgeTreeNode
CandidateCoverageSummary
```

## 涉及数据库/存储

当前 Phase 不引入数据库。候选数据仍来自文件化存储、fixture 或只读 API。

```text
codex-expert-kit/rag/candidates/
ui/src/data/phase23Candidates.ts
docs/reports/
```

运行时代码访问仓库路径必须使用：

```text
codex-expert-kit/core/path_resolver.py
```

禁止在运行时代码中硬编码 `E:\collector\rag` 等开发机绝对路径。

## 实施步骤

```text
1. 创建 Phase 29 任务卡并更新 docs/index_tasks.md、docs/tasks/README.md。
2. 创建候选审核阅读体验契约文档，明确 view model、checklist、handoff、错误结构。
3. 梳理 IngestionReview 当前布局，确认哪些信息放在队列、正文、证据、审计动作区。
4. 重构候选页阅读布局：左侧队列，中间候选正文和来源证据，右侧审核摘要和动作。
5. 增加审核 checklist、阻断原因、缺失字段和下一步动作提示。
6. 优化筛选、分页、排序和上千候选场景的空间占用。
7. 对齐 KnowledgeTreeView 跳转候选页的 query 参数。
8. 如涉及 FastAPI 候选读取，补齐只读 API 和错误契约测试。
9. 更新 Playwright，覆盖候选页桌面/移动端、过滤、跳转、导出按钮可见性。
10. 运行 Vue3 build、API 测试和 Playwright 验收。
11. 生成 Phase 29 验收报告并更新任务状态。
```

## Definition of Done

```text
1. Phase 29 已登记到 docs/index_tasks.md。
2. docs/tasks/README.md 已登记 Phase 29。
3. 本任务卡包含上下游、契约、边界、DoD 和测试。
4. 候选页能清晰展示候选知识正文、来源、冲突、边界、归类和转换预览。
5. 审计 checklist 可以明确告诉审核员是否能进入 accepted_for_draft。
6. blocked、needs_more_evidence、unchecked conflict、无来源候选有醒目但不刺眼的提示。
7. candidate/draft 不会被展示为 approved 或默认指导。
8. handoff 导出仍然可用，且目标仍为 CEK-TA-102。
9. 知识树跳转候选页的 tree_node_id 过滤可用。
10. `npm run build` 通过。
11. Playwright 桌面端和移动端候选页验收通过，或明确记录无法执行原因。
12. 如果新增/修改 API，FastAPI 契约测试通过。
13. 中文文档和界面文案保持 UTF-8，无乱码。
```

## 测试与验收

文档验收：

```text
1. UTF-8 读取无乱码。
2. docs/index_tasks.md 包含 Phase 29。
3. docs/tasks/README.md 包含 Phase 29。
4. 本任务卡章节完整。
5. 如新增契约文档，docs/index_tasks.md 文档入口可追踪。
```

Vue3 验收：

```text
1. `npm run build` 通过。
2. 候选列表、候选正文、来源证据、冲突审计、治理检查和转换预览均可渲染。
3. 搜索、partition、candidate_status、conflict_status、reliability 或 risk_level 过滤可用。
4. 知识树跳转到 `/ingestion?tree_node_id=...` 后能过滤候选。
5. 桌面端无重叠、无横向溢出、无大面积空白。
6. 移动端可以按 Tabs 或纵向折叠方式完成阅读和审核。
7. 导出 JSON/Markdown handoff 按钮存在且不误导为正式入库。
```

API/数据验收：

```text
1. candidate_id 唯一。
2. 无 source_refs 的候选不能显示为 accepted_for_draft ready。
3. conflict_status 为 confirmed 或 unchecked 时必须出现阻断或警告。
4. applies_when、not_applicable_when、assumptions 缺失时必须提示缺口。
5. 如果引入候选只读 API，错误响应符合统一错误契约。
```

## 风险与回滚

风险：

```text
1. 信息密度过高会让候选页难读，需要控制卡片和面板层级。
2. 过度弱化风险颜色可能导致审核员漏看阻断项。
3. 如果前端暗示 candidate 可直接使用，会污染后续项目决策。
4. 如果同时改 API 和 UI，问题定位会变复杂。
```

回滚：

```text
1. 回退 IngestionReview.vue 和相关组件到 Phase 24 版本。
2. 保留 candidateHandoff.ts，不影响 CEK-TA-102 交接。
3. 如果新增候选 API 有问题，前端回退到 phase23Candidates fixture。
4. 不修改 codex-expert-kit/rag/candidates/ 原始候选包。
5. 不修改 codex-expert-kit/rag/knowledge/ 正式知识目录。
```

## 需要开发者确认的问题

```text
1. 第一版是否继续只做本地 fixture/只读 API，不引入数据库？当前默认是。
2. 审核动作是否只导出 handoff，不在浏览器内持久化？当前默认是。
3. 候选页是否采用“左队列 + 中正文/证据 + 右审核摘要”的三栏布局？当前默认是。
4. 是否需要批量标记候选状态？当前默认不做，避免误操作。
```

## 状态更新要求

完成任一子任务后必须更新：

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. 本任务卡任务列表状态
4. 如新增契约或报告，更新 docs/index_tasks.md 文档入口
5. 如改动 Vue3，执行并记录 build/Playwright 结果
6. 如改动 FastAPI，执行并记录 API 测试结果
```
