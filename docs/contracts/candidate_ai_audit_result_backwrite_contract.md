# Candidate AI Audit Result Backwrite Contract

## 目标

本契约定义外部 AI 审计结果如何回写到 CEK-TA 候选知识和正式知识 draft。

它解决的是 Phase 30 的下游问题：AI 审计包导出后，外部 AI 返回的结论必须回到 CEK-TA 人工治理链路，不能直接写成 approved，也不能绕过来源、冲突、边界和补丁审查。

## 状态语义

```text
accepted_for_draft:
  外部 AI 认为候选可以进入 draft 或 reviewed draft 流程。
  不是 approved。

candidate status.accepted:
  候选已通过本轮 AI 审计和人工对齐，可作为正式知识 draft/reviewed 的来源。
  不是默认指导。

formal review.reviewed:
  正式知识已完成本轮审计修正，可被审计界面和检索层读取。
  是否进入默认指导由 MCP/SearchLab 的 review_status 过滤策略决定。

formal review.approved:
  本契约不产生 approved。
  approved 必须由后续人工治理任务单独完成。
```

## 输入 JSON

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
overall_conclusion: string
candidate_results:
  - candidate_id: string
    proposed_knowledge_id: string
    decision: accepted_for_draft | needs_more_evidence | rejected | blocked
    confidence: high | medium-high | medium | low
    reasons: string[]
    required_followups: string[]
    patch_notes: string[]
```

## 回写规则

候选：

```text
1. decision == accepted_for_draft:
   status.review_status = accepted
   review.ai_audit.decision = accepted_for_draft

2. decision == needs_more_evidence:
   status.review_status = needs_more_evidence

3. decision == rejected:
   status.review_status = rejected

4. decision == blocked:
   status.review_status = blocked
```

正式知识：

```text
1. 仅处理已经由 CEK-TA-102 转换出的正式 draft。
2. accepted_for_draft 对应正式知识设置为 review.review_status = reviewed。
3. needs_more_evidence/rejected/blocked 不升级正式知识状态。
4. 回写必须追加 decision_log，不覆盖历史记录。
5. 所有补丁必须写入内容字段、来源字段、risk_notes、not_applicable_when 或 open_questions。
```

## 禁止事项

```text
1. 禁止直接设置 review.review_status = approved。
2. 禁止无来源补充知识。
3. 禁止把外部 AI 的判断当成唯一来源。
4. 禁止用外部 AI 审计结果覆盖原始 source_evidence。
5. 禁止绕过 conflict_audit。
```

## 输出验证

```text
1. 7 条候选均有 review.ai_audit。
2. 7 条正式知识均有 review.ai_audit。
3. 7 条正式知识 review.review_status 均为 reviewed。
4. knowledge_items.json item_count 不减少。
5. phase23Candidates.ts 能反映候选 accepted 状态。
```

