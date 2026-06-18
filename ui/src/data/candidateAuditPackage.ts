import type { IngestionCandidate } from '../types'

type AuditDecision = 'accepted_for_draft' | 'needs_more_evidence' | 'rejected' | 'blocked'

function previewForCandidate(candidate: IngestionCandidate) {
  return (
    candidate.knowledge_preview || {
      proposed_knowledge_id: candidate.conversion_target?.proposed_knowledge_id || candidate.candidate_id,
      target_review_status: 'draft',
      domain: candidate.domain || '',
      subdomain: candidate.subdomain || '',
      tree_node_id: candidate.tree_node_id,
      canonical_node_id: candidate.canonical_node_id || candidate.tree_node_id,
      source_count: candidate.source_count,
      conflict_status: candidate.conflict_status,
      missing_fields: [],
      blocking_issues: []
    }
  )
}

function candidateRiskLevel(candidate: IngestionCandidate) {
  const preview = previewForCandidate(candidate)
  const reliability = candidate.source_quality?.overall_reliability || candidate.confidence
  const conflict = String(candidate.conflict_status)
  if (candidate.candidate_status === 'blocked' || conflict === 'confirmed' || conflict === 'unchecked' || candidate.source_count === 0) {
    return 'risk_blocked'
  }
  if (candidate.candidate_status === 'needs_more_evidence' || reliability === 'low' || preview.missing_fields.length || preview.blocking_issues.length) {
    return 'risk_high'
  }
  if (conflict === 'potential' || candidate.freshness === 'time_sensitive') return 'risk_medium'
  return 'risk_low'
}

function normalizeCandidate(candidate: IngestionCandidate) {
  const preview = previewForCandidate(candidate)
  return {
    candidate_id: candidate.candidate_id,
    research_task_id: candidate.research_task_id,
    candidate_status: candidate.candidate_status || 'needs_more_evidence',
    workflow: candidate.workflow || {
      stage: 'pending_review',
      queue_group: 'pending',
      formal_knowledge_id: null,
      formal_review_status: null,
      ai_audit_result_id: null,
      hidden_from_default_queue: false,
      next_action: 'export_ai_audit'
    },
    review_status: candidate.review_status,
    ingestion_decision: candidate.ingestion_decision,
    risk_level: candidateRiskLevel(candidate),
    claim: candidate.claim,
    evidence_summary: candidate.evidence_summary || '',
    interpretation_notes: candidate.interpretation_notes || '',
    classification: {
      partition_id: candidate.partition_id || '',
      tree_node_id: candidate.tree_node_id,
      canonical_node_id: candidate.canonical_node_id || candidate.tree_node_id,
      tree_path: candidate.tree_path || '',
      domain: candidate.domain || '',
      subdomain: candidate.subdomain || '',
      rule_type: candidate.rule_type || '',
      used_for: candidate.used_for || []
    },
    applicability: {
      applicable_scope: candidate.applicable_scope,
      applies_when: candidate.applies_when || [],
      not_applicable_when: candidate.not_applicable_when || candidate.not_applicable_scope || [],
      assumptions: candidate.assumptions || [],
      limitations: candidate.limitations || []
    },
    sources: candidate.source_refs || [],
    source_quality: candidate.source_quality || {
      overall_reliability: candidate.confidence,
      score: candidate.source_quality_score,
      limitations: []
    },
    conflict_audit: candidate.conflict_audit || {
      conflict_status: candidate.conflict_status,
      checked_against: [],
      conflicts: [],
      resolution_summary: '',
      approval_allowed: false
    },
    conversion_preview: preview,
    known_missing_fields: preview.missing_fields,
    known_blocking_issues: preview.blocking_issues,
    copyright: candidate.copyright || null,
    source_path: candidate.source_path || '',
    updated_at: candidate.updated_at
  }
}

export function buildCandidateAiAuditPackage(candidates: IngestionCandidate[], generatedAt = new Date().toISOString()) {
  const packageId = `cek_ta_candidate_ai_audit_${generatedAt.slice(0, 10).replace(/-/g, '')}`
  return {
    package_id: packageId,
    package_type: 'cek_ta_candidate_ai_audit_package',
    schema_version: '1.0.0',
    generated_at: generatedAt,
    language: 'zh-CN',
    purpose:
      '请审计 CEK-TA 当前导出范围内的候选知识是否具备进入 CEK-TA-102 转正式知识 draft/reviewed 流程的条件。candidate 不是 approved，reviewed 也不是 approved，审计结果必须回到人工流程。',
    strict_boundaries: [
      '候选知识不是正式知识，不得作为默认指导。',
      'workflow.formalized 只代表已回链 reviewed 知识，不代表 approved。',
      '不得把 candidate、proposed 或 draft 判定为 approved。',
      '不得无来源通过；不得编造来源或引用。',
      'confirmed 或 unchecked conflict 必须阻断或要求补充审计。',
      '只能输出结构化审计结果，不能写入 CEK-TA 正式知识库。',
      '不得要求执行交易、调用实盘、访问密钥或操作外部账户。'
    ],
    audit_instructions: [
      '逐条检查 claim 是否被 sources 和 evidence_summary 支撑。',
      '检查 source_refs 的可靠性、source_type、publisher、accessed_at、score 和 limitations。',
      '检查 applies_when、not_applicable_when、assumptions、limitations 是否足以定义使用边界。',
      '检查 conflict_audit 是否为 none 或 resolved；如为 potential/confirmed/unchecked，说明阻断原因。',
      '检查 tree_node_id/canonical_node_id 是否与 domain/subdomain/rule_type 匹配。',
      '检查 freshness、copyright、项目私有污染和泛化风险。',
      '只在来源、边界、冲突、分类都满足最低条件时输出 accepted_for_draft。'
    ],
    audit_checklist: [
      {
        key: 'source_support',
        question: '候选 claim 是否被可靠来源直接或合理支持？',
        pass_condition: '至少一个可靠来源可追踪，且 claim 没有超出来源边界。',
        fail_condition: '无来源、来源低质、来源无法支撑 claim 或疑似编造。'
      },
      {
        key: 'scope_boundary',
        question: '适用范围、不适用范围、假设和限制是否完整？',
        pass_condition: 'applies_when、not_applicable_when、assumptions、limitations 足以阻止误用。',
        fail_condition: '边界缺失、泛化过度或容易被其他项目误用。'
      },
      {
        key: 'conflict_gate',
        question: '是否存在未解决冲突？',
        pass_condition: 'conflict_status 为 none/resolved，且 resolution_summary 清楚。',
        fail_condition: 'conflict_status 为 confirmed/unchecked，或 potential 但没有人工复核要求。'
      },
      {
        key: 'draft_readiness',
        question: '是否可交给 CEK-TA-102 转 draft？',
        pass_condition: '来源、边界、冲突、分类全部满足最低条件。',
        fail_condition: '存在 blocking_issues、missing_fields 或 candidate_status=blocked/rejected。'
      }
    ],
    required_output_schema: {
      type: 'object',
      required: ['audit_result_id', 'auditor', 'audited_at', 'package_id', 'summary', 'candidate_results'],
      properties: {
        audit_result_id: 'string',
        auditor: 'string',
        audited_at: 'ISO-8601 string',
        package_id: packageId,
        summary: {
          total: 'number',
          accepted_for_draft: 'number',
          needs_more_evidence: 'number',
          rejected: 'number',
          blocked: 'number'
        },
        candidate_results: [
          {
            candidate_id: 'string',
            decision: 'accepted_for_draft | needs_more_evidence | rejected | blocked',
            confidence: 'high | medium | low',
            reasons: ['string'],
            source_audit: { status: 'pass | warning | fail', notes: ['string'] },
            conflict_audit: { status: 'pass | warning | fail', notes: ['string'] },
            scope_audit: { status: 'pass | warning | fail', notes: ['string'] },
            classification_audit: { status: 'pass | warning | fail', notes: ['string'] },
            required_followups: ['string'],
            proposed_handoff_patch: {
              missing_fields: ['string'],
              blocking_issues: ['string'],
              review_notes: ['string']
            }
          }
        ]
      }
    },
    candidates: candidates.map(normalizeCandidate)
  }
}

function downloadText(filename: string, text: string, mimeType: string) {
  const blob = new Blob([text], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  URL.revokeObjectURL(url)
}

export function downloadCandidateAiAuditPackage(candidates: IngestionCandidate[]) {
  const auditPackage = buildCandidateAiAuditPackage(candidates)
  downloadText(`${auditPackage.package_id}.json`, JSON.stringify(auditPackage, null, 2), 'application/json;charset=utf-8')
}
