# Phase 30: 候选知识 AI 审计包导出

## Phase 目标

在 Vue3 候选知识审计页增加“一键导出 AI 审计包”功能。导出的 JSON 必须让外部审计 AI 明确知道：

```text
1. 本次审计目标是什么。
2. 需要审计哪些候选知识。
3. 审计时必须检查哪些来源、冲突、边界、治理和入库规则。
4. 哪些行为禁止，例如不能把 candidate 当 approved。
5. 审计 AI 必须输出什么 JSON 结果。
```

本 Phase 不改变候选生命周期，不写正式知识库，不替代人工审核，不开放 MCP/API 写权限。

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-141 | P0 | done | 创建 Phase 30 任务卡并登记任务索引 | `docs/tasks/phase30_candidate_ai_audit_package_export.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-142 | P0 | done | 定义 AI 审计包 JSON 契约 | `docs/contracts/candidate_ai_audit_package_contract.md` |
| CEK-TA-143 | P0 | done | 实现候选页一键导出 AI 审计包 JSON | `ui/src/data/candidateAuditPackage.ts`、`ui/src/views/IngestionReview.vue` |
| CEK-TA-144 | P1 | done | 增加构建和 Playwright 导出按钮验收 | `ui/tests/e2e/audit-workbench.spec.ts` |

## 上游输入

```text
1. Phase 23 候选知识包。
2. Phase 24 candidate fixture 和 handoff。
3. Phase 29 候选审核页、checklist、只读 API 和阅读体验契约。
4. AGENTS.md 中的知识入库、UTF-8、MCP/API 只读和边界规则。
```

## 下游输出

```text
1. 用户可下载 JSON 审计包。
2. 外部 AI 可根据 JSON 中的 instructions、audit_checklist、output_schema 审计候选知识。
3. 用户可把外部 AI 的审计结果带回候选页或 CEK-TA 后续流程。
```

## 输入契约

输入候选使用 `IngestionCandidate[]`，来源为当前候选页过滤结果。

## 输出契约

导出 JSON 必须包含：

```yaml
package_id: string
package_type: cek_ta_candidate_ai_audit_package
schema_version: string
generated_at: string
language: zh-CN
purpose: string
strict_boundaries: string[]
audit_instructions: string[]
audit_checklist: []
required_output_schema: object
candidates: []
```

## 边界

范围内：

```text
1. 导出当前过滤范围内的候选。
2. JSON 内包含审计任务说明、检查项、输出 schema 和候选数据。
3. 下载 JSON 文件。
```

范围外：

```text
1. 不自动调用外部 AI。
2. 不接收或写入外部 AI 审计结果。
3. 不把候选转为 approved。
4. 不写正式知识库。
5. 不引入数据库。
```

## Definition of Done

```text
1. Phase 30 已登记到任务索引。
2. 契约文档已创建。
3. 候选页存在“一键导出 AI 审计包”按钮。
4. 导出 JSON 含 instructions、checklist、output_schema、candidates。
5. `npm run build` 通过。
6. Playwright 验收按钮可见。
```

## 测试与验收

```text
1. UTF-8 文档读取无乱码。
2. Vue build 通过。
3. Playwright 候选页能看到导出按钮。
4. 导出功能不改变正式知识库和候选源文件。
```

## 风险与回滚

风险：

```text
1. 审计包过大，后续可增加只导出当前页或选中候选。
2. 外部 AI 误解 candidate 状态，因此 JSON 中必须反复声明 candidate 不等于 approved。
```

回滚：

```text
1. 移除候选页导出按钮。
2. 删除 `candidateAuditPackage.ts` 引用。
3. 保留原 handoff 导出能力。
```
