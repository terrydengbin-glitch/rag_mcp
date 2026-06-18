# Phase 31: 候选知识 AI 审计结果回写

## Phase 目标

把外部 AI 对 Phase 30 审计包返回的审计结果，按 CEK-TA 知识治理规则回写到候选知识和正式 draft 知识中。

本 Phase 的核心目标不是重新采集知识，而是完成：

```text
1. 解析外部 AI 审计结论。
2. 对齐人工审核边界：accepted_for_draft 不等于 approved。
3. 按补丁点优化正式 draft 内容。
4. 将候选设置为 accepted，将正式知识设置为 reviewed。
5. 重建正式知识索引和候选前端 fixture。
6. 生成可追踪的验收报告。
```

## 任务列表

| ID | 优先级 | 状态 | 任务 | 交付物 |
| --- | --- | --- | --- | --- |
| CEK-TA-145 | P0 | done | 创建 Phase 31 任务卡并登记任务索引 | `docs/tasks/phase31_candidate_ai_audit_result_backwrite.md`、`docs/index_tasks.md`、`docs/tasks/README.md` |
| CEK-TA-146 | P0 | done | 定义 AI 审计结果回写契约 | `docs/contracts/candidate_ai_audit_result_backwrite_contract.md` |
| CEK-TA-147 | P0 | done | 落地外部 AI 审计结果 JSON | `docs/audit/phase31_candidate_ai_audit_result_20260609.json` |
| CEK-TA-148 | P0 | done | 实现审计结果回写脚本 | `codex-expert-kit/rag/scripts/apply_candidate_ai_audit_result.py` |
| CEK-TA-149 | P0 | done | 修正 7 条知识并标记审计通过 | `codex-expert-kit/rag/candidates/**/*.json`、`codex-expert-kit/rag/knowledge/**/*.json` |
| CEK-TA-150 | P1 | done | 重建索引、fixture 并跑验证 | `codex-expert-kit/rag/indexes/knowledge_items.json`、`ui/src/data/phase23Candidates.ts`、`docs/reports/phase31_candidate_ai_audit_result_backwrite_report.md` |

## 上游输入

```text
1. Phase 23 生成的 7 条候选知识。
2. Phase 23 CEK-TA-102 转换出的正式 draft 知识。
3. Phase 30 导出的 AI 审计包契约。
4. 外部 AI 返回的审计结果与补丁建议。
5. AGENTS.md 的知识入库、状态流、UTF-8、resolver 和 approved 边界规则。
```

## 下游输出

```text
1. Vue3 候选页可看到候选已 accepted_for_draft。
2. 知识树和 SearchLab 可读取 7 条 reviewed 正式知识。
3. MCP 默认索引包含修正后的 reviewed 知识，但仍不得把 reviewed 当 approved。
4. 后续人工治理流程可继续决定是否升级 approved。
```

## 输入契约

输入审计结果必须满足：

```yaml
audit_result_id: string
auditor: string
audited_at: string
package_id: string
summary:
  total: number
  accepted_for_draft: number
  needs_more_evidence: number
  rejected: number
  blocked: number
candidate_results:
  - candidate_id: string
    decision: accepted_for_draft | needs_more_evidence | rejected | blocked
    confidence: high | medium-high | medium | low
    reasons: string[]
    required_followups: string[]
    patch_notes: string[]
```

## 输出契约

候选知识回写：

```yaml
status.review_status: accepted | rejected | needs_more_evidence | blocked
status.updated_at: YYYY-MM-DD
review.ai_audit: object
review.audit_log: append-only
```

正式知识回写：

```yaml
review.review_status: reviewed | draft | rejected
review.reviewed_at: YYYY-MM-DD
review.updated_at: YYYY-MM-DD
review.ai_audit: object
review.decision_log: append-only
```

## 边界

范围内：

```text
1. 将 accepted_for_draft 的候选标记为 accepted。
2. 将已存在的正式 draft 知识标记为 reviewed。
3. 根据审计补丁修正来源版本、适用边界、风险说明和反模式。
4. 重建索引和前端 fixture。
```

范围外：

```text
1. 不把任何条目直接升级为 approved。
2. 不新增交易策略参数、仓位建议、杠杆建议或实盘操作建议。
3. 不让外部 AI 审计结果直接替代人工最终批准。
4. 不引入数据库或写 API。
5. 不修改 MCP 权限为可写。
```

## 涉及组件

```text
1. docs/index_tasks.md
2. docs/tasks/README.md
3. docs/contracts/
4. docs/audit/
5. codex-expert-kit/rag/candidates/
6. codex-expert-kit/rag/knowledge/
7. codex-expert-kit/rag/scripts/
8. codex-expert-kit/rag/indexes/knowledge_items.json
9. ui/src/data/phase23Candidates.ts
```

## Definition of Done

```text
1. Phase 31 已登记到任务索引和任务卡目录。
2. 回写契约存在并说明 accepted_for_draft != approved。
3. 外部 AI 审计结果已结构化保存。
4. 7 条候选均写入 ai_audit 并标记 accepted。
5. 7 条正式 draft 均写入 ai_audit 并标记 reviewed。
6. 5 个补丁点已体现在对应正式知识中。
7. 正式知识索引已重建。
8. Vue3 candidate fixture 已重建。
9. 测试通过或明确说明未执行原因。
10. 验收报告已生成。
```

## 测试与验收

```text
1. Python 回写脚本 dry-run 和实际执行通过。
2. `python codex-expert-kit/rag/scripts/build_knowledge_items_index.py` 通过。
3. `python codex-expert-kit/rag/scripts/build_ui_candidate_fixture.py` 通过。
4. API/RAG 相关 pytest 通过。
5. `npm run build` 通过。
```

## 风险与回滚

风险：

```text
1. 外部 AI 审计结果不是完整 JSON，需要人工结构化后再回写。
2. reviewed 可能被下游误读为 approved，因此索引和知识内容必须保留边界说明。
3. MCP/RAG 外部规范会继续更新，time_sensitive 知识仍需后续 freshness 复审。
```

回滚：

```text
1. 用 git diff 定位本 Phase 修改的 candidate、knowledge、index 和 fixture。
2. 回退 Phase 31 新增文档和脚本。
3. 重建 `knowledge_items.json` 与 `phase23Candidates.ts`。
```
