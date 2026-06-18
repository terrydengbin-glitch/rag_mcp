# Candidate AI Audit Package Contract

## 目标

候选知识 AI 审计包是给外部审计 AI 使用的 JSON 文件。它不是正式知识库，不是入库指令，也不是 approved 结果。审计 AI 必须根据包内候选知识、来源、冲突、边界和规则，输出结构化审计结论。

## 使用者

```text
1. 外部审计 AI。
2. 人工审核员。
3. CEK-TA 后续候选复审流程。
```

## 导出范围

默认导出候选页当前过滤结果。后续可扩展为导出当前页或选中候选。

## 顶层 JSON 契约

```yaml
package_id: string
package_type: cek_ta_candidate_ai_audit_package
schema_version: string
generated_at: string
language: zh-CN
purpose: string
strict_boundaries: string[]
audit_instructions: string[]
audit_checklist:
  - key: string
    question: string
    pass_condition: string
    fail_condition: string
required_output_schema:
  type: object
  required: string[]
  properties: object
candidates:
  - candidate_id: string
    candidate_status: string
    review_status: string
    risk_level: string
    claim: string
    evidence_summary: string
    classification: object
    applicability: object
    sources: []
    source_quality: object
    conflict_audit: object
    conversion_preview: object
    known_missing_fields: string[]
    known_blocking_issues: string[]
```

## 审计 AI 必须检查

```text
1. source_refs 是否存在、可追踪、质量足够。
2. claim 是否被来源支持，不能超出来源可支持范围。
3. applies_when、not_applicable_when、assumptions、limitations 是否完整。
4. conflict_audit 是否已做，冲突是否 resolved 或 none。
5. tree_node_id 和 canonical_node_id 是否合理。
6. freshness 是否需要复审。
7. 是否存在版权、长引用、项目私有污染或泛化不足。
8. 是否允许进入 accepted_for_draft。
```

## 审计 AI 禁止事项

```text
1. 禁止把 candidate/draft 当作 approved。
2. 禁止无来源通过。
3. 禁止忽略 confirmed/unchecked conflict。
4. 禁止直接输出正式知识库写入指令。
5. 禁止要求执行交易、调用实盘、访问密钥。
6. 禁止凭空补来源或编造引用。
```

## 审计 AI 输出结果契约

审计 AI 必须输出 JSON：

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
    confidence: high | medium | low
    reasons: string[]
    source_audit:
      status: pass | warning | fail
      notes: string[]
    conflict_audit:
      status: pass | warning | fail
      notes: string[]
    scope_audit:
      status: pass | warning | fail
      notes: string[]
    classification_audit:
      status: pass | warning | fail
      notes: string[]
    required_followups: string[]
    proposed_handoff_patch:
      missing_fields: string[]
      blocking_issues: string[]
      review_notes: string[]
```

## 边界

```text
1. 本 JSON 只用于审计，不用于直接入库。
2. 审计结果必须回到 CEK-TA 人工流程。
3. accepted_for_draft 只表示可交给 CEK-TA-102 转 draft。
4. approved 只能由后续正式治理流程产生。
```
