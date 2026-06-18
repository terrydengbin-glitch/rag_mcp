# Phase 32: 候选到 reviewed 知识的批量审计工作流

## Phase 目标

建立一套可重复、可批量、可审计的候选知识沉淀工作流，让后续大量专业交易知识可以快速从候选进入正式 `reviewed` 知识，同时避免把未最终人工批准的内容误当成 `approved` 默认指导。

本 Phase 要解决 Phase 31 暴露出的产品和工程问题：

```text
1. AI 审计通过的候选不应继续挤在默认待审计队列。
2. 候选、AI 审计结果、正式 reviewed 知识之间必须有稳定回链。
3. 后续批量审计通过/优化任务必须能复用固定流程，而不是每次临时处理。
4. Vue3 候选页必须支持“待审计 / AI 已通过 / 需补证据 / 已沉淀知识”等分组。
5. MCP/SearchLab/知识树必须读取正式 reviewed 知识，而不是依赖候选队列。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-151 | P0 | done | 定义候选审计流水线状态机 | `docs/contracts/candidate_to_reviewed_workflow_contract.md`、`codex-expert-kit/rag/ingestion_candidate_schema.md` |
| CEK-TA-152 | P0 | done | 扩展 candidate workflow 字段和 formal knowledge 回链字段 | `codex-expert-kit/rag/candidates/**/*.json`、`codex-expert-kit/rag/knowledge/**/*.json`、`ui/src/types.ts` |
| CEK-TA-153 | P0 | done | 优化候选页分组和默认队列 | `ui/src/views/IngestionReview.vue`、`ui/src/stores/auditStore.ts`、`ui/src/data/phase23Candidates.ts` |
| CEK-TA-154 | P0 | done | 标准化批量 AI 审计结果导入与回写报告 | `codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py`、`docs/audit/`、`docs/reports/` |
| CEK-TA-155 | P1 | done | 增加批量质量门禁 | `codex-expert-kit/rag/scripts/`、`codex-expert-kit/rag/indexes/knowledge_items.json`、`docs/reports/` |
| CEK-TA-156 | P1 | done | 增加知识树、SearchLab、MCP 联动验证 | `ui/tests/e2e/audit-workbench.spec.ts`、`codex-expert-kit/api/tests/`、`codex-expert-kit/mcp/tests/` |
| CEK-TA-157 | P1 | done | 生成 Phase 32 验收报告 | `docs/reports/phase32_candidate_to_reviewed_workflow_report.md` |
| CEK-TA-494 | P1 | done | 将已重建且已有 formal reviewed 替代知识的 rejected 候选拆分为“已重建归档” | `codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py`、`ui/src/views/IngestionReview.vue`、`ui/src/types.ts`、`ui/src/data/phase23Candidates.ts`、`docs/reports/phase32_rebuilt_archived_candidate_ui_report.json` |

## 上游输入

```text
1. Phase 23 候选采集和 CEK-TA-102 候选转 draft 流程。
2. Phase 29 候选知识人工审核阅读工作台。
3. Phase 30 AI 审计包导出能力。
4. Phase 31 AI 审计结果回写脚本和审计结果契约。
5. 正式知识聚合索引 `knowledge_items.json`。
6. Vue3 知识树、候选页、SearchLab 和 FastAPI 只读数据服务。
```

## 下游输出

```text
1. 候选页默认只显示待审计候选。
2. AI 审计通过的候选进入“AI 已通过 / 已沉淀知识”分组。
3. 正式 reviewed 知识在知识树、SearchLab 和 MCP 中可追踪到来源候选和 AI 审计结果。
4. 后续批量知识沉淀可以复用同一套导出、审计、导入、修正、重建索引、验证和报告流程。
5. 人工 approved 治理仍然是单独边界，不由本 Phase 自动完成。
```

## 输入契约

候选输入必须至少包含：

```yaml
candidate_id: string
status.review_status: proposed | sanitized | sourced | classified | conflict_checked | accepted | rejected | needs_more_evidence | blocked
review.ai_audit?: object
conversion_target.proposed_knowledge_id?: string
workflow?: object
```

正式知识输入必须至少包含：

```yaml
knowledge_id: string
metadata.source_candidate_id?: string
review.review_status: draft | reviewed | approved | rejected | deprecated
review.ai_audit?: object
review.approval_status?: not_requested | requested | approved | rejected
```

## 输出契约

候选新增/规范化 workflow 字段：

```yaml
workflow:
  stage: pending_review | ai_audited | needs_more_evidence | rejected | formalized_reviewed | approval_requested | approved
  queue_group: pending | ai_passed | needs_more_evidence | formalized | rejected
  formal_knowledge_id: string | null
  formal_review_status: draft | reviewed | approved | rejected | deprecated | null
  ai_audit_result_id: string | null
  hidden_from_default_queue: boolean
  next_action: export_ai_audit | apply_ai_audit_patch | review_formal_knowledge | request_human_approval | none
```

正式知识新增/规范化回链字段：

```yaml
review:
  source_candidate_id: string | null
  ai_audit_result_id: string | null
  approval_status: not_requested | requested | approved | rejected
  default_guidance_allowed: boolean
```

Vue3 候选页分组契约：

```text
待审计:
  workflow.queue_group == pending

AI 已通过:
  workflow.queue_group == ai_passed

需补证据:
  workflow.queue_group == needs_more_evidence

已沉淀知识:
  workflow.queue_group == formalized

已重建归档:
  workflow.queue_group == rebuilt_archived
  原候选 status.review_status == rejected
  原候选因 slug / normalized_claim / ID 结构缺陷被拒绝
  已存在替代候选和 formal reviewed 知识回链

全部:
  不过滤 workflow.queue_group
```

## 边界

范围内：

```text
1. 规范候选到 reviewed 正式知识的批量流水线。
2. 扩展文件化 JSON schema 和 Vue3 类型。
3. 优化候选页默认分组与状态呈现。
4. 让 AI 审计通过候选从默认待审计队列移出。
5. 重建索引、fixture 和验证报告。
6. 将已重建且已有 formal reviewed 替代知识的 rejected 候选从普通“已拒绝”视觉队列拆出。
```

范围外：

```text
1. 不自动把 reviewed 升级为 approved。
2. 不新增数据库。
3. 不改变 MCP tool 权限。
4. 不引入外部 AI API 调用。
5. 不删除候选源文件，候选必须保留审计追踪。
6. 不让候选队列替代正式知识索引。
7. 不修改 rejected 原始审计结论，不把已重建归档误标为 reviewed/approved。
```

## 涉及组件

```text
1. docs/contracts/candidate_to_reviewed_workflow_contract.md
2. codex-expert-kit/rag/ingestion_candidate_schema.md
3. codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py
4. codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py
5. codex-expert-kit/rag/scripts/build_knowledge_items_index.py
6. codex-expert-kit/rag/candidates/
7. codex-expert-kit/rag/knowledge/
8. codex-expert-kit/rag/indexes/knowledge_items.json
9. ui/src/types.ts
10. ui/src/views/IngestionReview.vue
11. ui/src/stores/auditStore.ts
12. ui/tests/e2e/audit-workbench.spec.ts
13. .agents/skills/cek-ta-development-workflow/SKILL.md
14. AGENTS.md
15. codex-expert-kit/core/AGENTS.md
```

## 实施步骤

```text
1. 定义 `candidate_to_reviewed_workflow_contract.md`。
2. 扩展 candidate 和 formal knowledge 的 workflow / review 回链字段。
3. 更新 `apply_candidate_ai_audit_result.py`，让回写时自动设置 workflow。
4. 更新 `build_ui_candidate_fixture.py`，把 workflow 输出到 Vue3 fixture。
5. 改造候选页为 Tab/分组模式，默认显示待审计队列。
6. AI 审计包导出默认只导出待审计或当前分组候选。
7. 已沉淀知识分组显示 target knowledge id、formal review_status 和跳转入口。
8. 增加批量质量门禁脚本或校验逻辑。
9. 跑索引、API、Vue build、Playwright/MCP/SearchLab 验证。
10. 生成 Phase 32 验收报告。
11. 对 rejected + replacement formal reviewed 的历史候选输出 `rebuilt_archived` 分组。
```

## Definition of Done

```text
1. Phase 32 已登记到 `docs/index_tasks.md` 和 `docs/tasks/README.md`。
2. 任务卡存在并明确上下游、契约、边界和 DoD。
3. CEK-TA Skill 和 AGENTS 规则已写入候选审计优化工作流。
4. workflow contract 存在。
5. 7 条 Phase 31 候选可按 workflow 分入“已沉淀知识”或“AI 已通过”分组。
6. 候选页默认不再显示已通过/已沉淀候选。
7. 正式 reviewed 知识可以回链 source_candidate_id 和 ai_audit_result_id。
8. 重建索引和 fixture 后无类型错误。
9. API/Vue/Playwright/MCP/SearchLab 相关验证通过或记录未执行原因。
10. 没有任何自动 approved 行为。
11. 生成验收报告。
12. “已重建归档”分组能显示替代 formal knowledge id，普通“已拒绝”不再包含这些已闭环归档项。
```

## 测试与验收

```text
1. UTF-8 文档读取无乱码。
2. JSON schema/字段存在性校验通过。
3. `python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py` 通过。
4. `python codex-expert-kit/rag/scripts/build_knowledge_items_index.py` 通过。
5. `python -m pytest codex-expert-kit/api/tests` 通过。
6. `npm run build` 通过。
7. Playwright 验证候选页默认队列、已通过分组和跳转入口。
8. MCP/SearchLab 验证 reviewed 知识可检索且不被误标为 approved。
```

## 风险与回滚

风险：

```text
1. 候选仍保留在文件中，用户可能误以为未完成；需要通过 UI 分组和文案明确状态。
2. reviewed 被误读为 approved；必须在 workflow 和 UI 上保留边界。
3. 批量回写时可能部分候选缺少 formal knowledge id；必须进入 needs_more_evidence 或 blocked 分组。
4. 大批量候选会让前端列表变慢；需要分页、过滤和虚拟列表预留。
```

回滚：

```text
1. 保留原候选 JSON，不删除历史文件。
2. 回退 workflow 字段和 UI 分组逻辑。
3. 重建 `phase23Candidates.ts` 和 `knowledge_items.json`。
4. 候选页可退回全量 `all` 显示模式。
```

## 需要开发者确认的问题

```text
1. Phase 32 默认是否把已通过候选归入“已沉淀知识”，还是先放“AI 已通过”再由人工触发“沉淀完成”？
2. reviewed 知识是否允许在 SearchLab 默认展示，但明确标注“非 approved”？
3. 候选页 AI 审计包导出是否默认只导出“待审计”，还是导出当前筛选分组？
```
