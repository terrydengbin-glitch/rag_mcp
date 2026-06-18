import type { CandidateAuditHandoff, CandidateKnowledgePreview, IngestionCandidate } from '../types'

type HandoffDecision = 'accepted_for_draft' | 'needs_more_evidence' | 'rejected'

function previewForCandidate(candidate: IngestionCandidate): CandidateKnowledgePreview {
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

function decisionForCandidate(candidate: IngestionCandidate): HandoffDecision {
  const preview = previewForCandidate(candidate)
  if (candidate.candidate_status === 'rejected' || candidate.review_status === 'rejected') return 'rejected'
  if (candidate.candidate_status === 'blocked' || preview.blocking_issues.length) return 'rejected'
  if (preview.missing_fields.length) return 'needs_more_evidence'
  if (candidate.candidate_status === 'candidate_ready' || candidate.candidate_status === 'accepted_for_draft') return 'accepted_for_draft'
  return 'needs_more_evidence'
}

function reasonForCandidate(candidate: IngestionCandidate, decision: HandoffDecision) {
  const preview = previewForCandidate(candidate)
  if (decision === 'accepted_for_draft') {
    return 'Candidate has sources, applicability boundaries, non-blocking conflict audit, and draft-only conversion preview.'
  }
  if (decision === 'rejected') {
    return preview.blocking_issues.length
      ? `Blocked by ${preview.blocking_issues.join(', ')}.`
      : 'Rejected candidate must not enter CEK-TA-102 draft conversion.'
  }
  return preview.missing_fields.length
    ? `Needs missing fields: ${preview.missing_fields.join(', ')}.`
    : 'Needs reviewer confirmation or additional evidence before draft conversion.'
}

export function buildCandidateAuditHandoff(
  candidates: IngestionCandidate[],
  generatedAt = new Date().toISOString()
): CandidateAuditHandoff {
  return {
    handoff_id: `phase24_candidate_audit_${generatedAt.slice(0, 10).replace(/-/g, '')}`,
    phase: '24',
    target_task_id: 'CEK-TA-102',
    generated_at: generatedAt,
    candidates: candidates.map((candidate) => {
      const decision = decisionForCandidate(candidate)
      const preview = previewForCandidate(candidate)
      return {
        candidate_id: candidate.candidate_id,
        decision,
        reason: reasonForCandidate(candidate, decision),
        missing_fields: preview.missing_fields,
        blocking_issues: preview.blocking_issues,
        target_knowledge_preview: preview
      }
    })
  }
}

export function renderCandidateAuditHandoffMarkdown(handoff: CandidateAuditHandoff) {
  const rows = handoff.candidates
    .map((item) => {
      const preview = item.target_knowledge_preview
      return [
        item.candidate_id,
        item.decision,
        preview.proposed_knowledge_id,
        preview.domain,
        preview.subdomain,
        preview.source_count,
        preview.conflict_status,
        item.missing_fields.length ? item.missing_fields.join(', ') : '-',
        item.blocking_issues.length ? item.blocking_issues.join(', ') : '-'
      ].join(' | ')
    })
    .join('\n')

  return `# Phase 24 Candidate Audit Handoff

handoff_id: ${handoff.handoff_id}
phase: ${handoff.phase}
target_task_id: ${handoff.target_task_id}
generated_at: ${handoff.generated_at}

This handoff is generated from the Vue3 candidate audit workbench. It is a draft conversion handoff, not approved knowledge.

| candidate_id | decision | proposed_knowledge_id | domain | subdomain | sources | conflict | missing_fields | blocking_issues |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
${rows}
`
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

export function downloadCandidateAuditHandoffJson(handoff: CandidateAuditHandoff) {
  downloadText(`${handoff.handoff_id}.json`, JSON.stringify(handoff, null, 2), 'application/json;charset=utf-8')
}

export function downloadCandidateAuditHandoffMarkdown(handoff: CandidateAuditHandoff) {
  downloadText(`${handoff.handoff_id}.md`, renderCandidateAuditHandoffMarkdown(handoff), 'text/markdown;charset=utf-8')
}
