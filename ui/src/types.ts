export type ReviewStatus = 'draft' | 'reviewed' | 'approved' | 'rejected' | 'deprecated'
export type ConflictStatus = 'none' | 'potential' | 'confirmed' | 'resolved' | 'deprecated_by_conflict'
export type Freshness = 'stable' | 'time_sensitive' | 'deprecated'
export type Confidence = 'high' | 'medium' | 'low'
export type CandidateReviewStatus =
  | 'candidate_ready'
  | 'proposed'
  | 'sanitized'
  | 'sourced'
  | 'classified'
  | 'conflict_checked'
  | 'reviewed'
  | 'accepted'
  | 'accepted_for_draft'
  | 'formalized_reviewed'
  | 'formalized'
  | 'rejected'
  | 'needs_more_evidence'
export type CandidateIngestionDecision =
  | 'candidate_ready'
  | 'pending'
  | 'pending_external_audit'
  | 'blocked'
  | 'hold'
  | 'accept_candidate'
  | 'needs_more_evidence'
  | 'reject'
  | 'accepted_for_draft'
  | 'accepted_for_reviewed_caveat_only'
  | 'formal_reviewed_created'
  | 'ready_for_reaudit'
  | 'ready_for_inline_contract_reaudit'
  | 'hold_for_metadata_clarification'
  | 'convert_to_knowledge_item'
  | 'convert_to_skill'
  | 'convert_to_skill_and_knowledge'
  | 'convert_to_eval_case'
export type CandidateAuditStatus =
  | 'candidate_ready'
  | 'needs_more_evidence'
  | 'blocked'
  | 'accepted_for_draft'
  | 'accepted_for_reviewed_caveat_only'
  | 'rejected'
export type CandidateWorkflowStage =
  | 'pending_review'
  | 'ai_audited'
  | 'needs_more_evidence'
  | 'supplemented_for_inline_contract_reaudit'
  | 'rejected'
  | 'rebuilt_archived'
  | 'formalized_draft'
  | 'formalized_reviewed'
  | 'approval_requested'
  | 'approved'
export type CandidateWorkflowQueueGroup =
  | 'pending'
  | 'ai_passed'
  | 'needs_more_evidence'
  | 'formalized'
  | 'rebuilt_archived'
  | 'rejected'
export type CandidateWorkflowNextAction =
  | 'export_ai_audit'
  | 'apply_ai_audit_patch'
  | 'external_ai_or_human_inline_contract_reaudit'
  | 'review_formal_knowledge'
  | 'request_human_approval'
  | 'none'
export type CoverageStatus = 'empty' | 'partial' | 'covered' | 'overgrown'
export type NodeReviewStatus = 'draft' | 'reviewed' | 'approved' | 'needs_review' | 'deprecated'
export type FreshnessStatus = 'stable' | 'time_sensitive' | 'stale' | 'deprecated'
export type NodeConflictStatus = 'none' | 'potential' | 'confirmed' | 'resolved' | 'unchecked'
export type SourceType =
  | 'official_doc'
  | 'official_repo'
  | 'paper'
  | 'exchange_rule'
  | 'framework_doc'
  | 'cloud_provider_doc'
  | 'book'
  | 'research_report'
  | 'research_paper'
  | 'standard_doc'
  | 'security_standard'
  | 'regulator_release'
  | 'regulator_review'
  | 'standard_or_risk_framework'
  | 'governance_framework'
  | 'engineering_article'
  | 'internal_report'
  | 'internal_contract'
  | 'internal_runbook'
  | 'task_card'
  | 'code_doc'
  | 'runbook'
  | 'other'
export type ClaimType =
  | 'methodological_constraint'
  | 'risk_boundary_rule'
  | 'execution_safety_rule'
  | 'data_quality_rule'
  | 'backtest_validity_rule'
  | 'rag_governance_rule'
  | 'mcp_contract_rule'
  | 'knowledge_governance_rule'
  | 'project_integration_rule'
  | 'llm_training_rule'
  | 'llm_eval_rule'
  | 'training_data_schema_rule'
  | 'ai_security_rule'
  | 'ai_governance_rule'
  | 'llmops_release_rule'
export type MachineGateDefaultGuidance = 'allow' | 'caveat_only' | 'deny'

export interface LlmUsagePolicy {
  allowed: string[]
  not_allowed: string[]
  required_context: string[]
  fallback_behavior: 'deny' | 'ask_for_context' | 'cite_with_caveat'
}

export interface MachineGate {
  default_guidance: MachineGateDefaultGuidance
  reason: string
  requires_human_escalation: boolean
  blocking_reasons: string[]
  checked_at: string
  gate_version: string
}

export interface SourceProfile {
  source_id: string
  title: string
  url: string | null
  source_type: string
  publisher: string
  published_at: string | null
  accessed_at: string
  reliability: Confidence
  score: number
  cited_by: string[]
  stale: boolean
}

export interface ConflictRecord {
  conflict_id: string
  conflict_type: string
  severity: 'blocking' | 'warning' | 'informational'
  left_id: string
  right_id: string
  left_source_reliability: Confidence
  right_source_reliability: Confidence
  scope_compare: string
  version_compare: string
  resolution: string
  review_decision: 'pending' | 'resolved' | 'blocked'
}

export interface CandidateSourceRef {
  source_id: string
  title: string
  url: string | null
  source_type: SourceType
  publisher: string | null
  published_at: string | null
  accessed_at: string
  version: string | null
  reliability: Confidence
  score: number
  relevance: Confidence
  freshness: Freshness
  limitations: string[]
  evidence_summary: string
  quoted_excerpt_allowed: boolean
}

export interface CandidateSourceQuality {
  overall_reliability: Confidence
  score: number
  score_version: string
  primary_source_count: number
  supporting_source_count: number
  low_reliability_source_count: number
  mandatory_downgrades: string[]
  limitations: string[]
}

export interface CandidateConflictItem {
  knowledge_id: string
  conflict_type: string
  severity: 'blocking' | 'warning' | 'informational'
  overlap_scope: {
    domain: string
    subdomain: string
    market: string
    timeframe: string
    data_granularity: string
  }
  candidate_claim: string
  existing_claim: string
  resolution: string
  default_recommendation: string | null
  requires_human_review: boolean
}

export interface CandidateConflictAudit {
  conflict_status: ConflictStatus | 'unchecked'
  checked_against: string[]
  conflicts: CandidateConflictItem[]
  resolution_summary: string
  approval_allowed: boolean
}

export interface CandidateConversionTarget {
  proposed_knowledge_id: string
  target_schema: string
  target_review_status: 'draft'
  skill_candidate: boolean
  eval_case_candidate: boolean
}

export interface CandidateKnowledgePreview {
  proposed_knowledge_id: string
  target_review_status: 'draft'
  domain: string
  subdomain: string
  tree_node_id: string
  canonical_node_id: string
  source_count: number
  conflict_status: ConflictStatus | 'unchecked'
  missing_fields: string[]
  blocking_issues: string[]
}

export interface CandidateWorkflow {
  stage: CandidateWorkflowStage
  queue_group: CandidateWorkflowQueueGroup
  formal_knowledge_id: string | null
  formal_review_status: ReviewStatus | null
  ai_audit_result_id: string | null
  hidden_from_default_queue: boolean
  next_action: CandidateWorkflowNextAction
  replacement_candidate_id?: string | null
  replacement_candidate_path?: string | null
  replacement_formal_knowledge_id?: string | null
  archive_reason?: string | null
}

export interface ReviewDecisionDraft {
  candidate_id: string
  decision: 'accepted_for_draft' | 'needs_more_evidence' | 'rejected'
  reviewer: string
  decision_reason: string
  required_followups: string[]
  created_at: string
}

export interface KnowledgeItem {
  knowledge_id: string
  title: string
  domain: string
  subdomain: string
  tree_node_id?: string
  tree_path?: string
  canonical_node_id?: string
  canonical_tree_path?: string
  rule_type: string
  claim_type?: ClaimType
  classification_notes?: string
  source_type: string
  statement: string
  rationale: string
  applies_to: {
    market: string
    asset: string
    timeframe: string
    data_granularity: string
    project_type: string
  }
  assumptions: string[]
  not_applicable_when: string[]
  sources: SourceProfile[]
  conflicts: ConflictRecord[]
  resolution: string
  confidence: Confidence
  freshness: Freshness
  review_status: ReviewStatus
  conflict_status: ConflictStatus
  llm_usage_policy?: LlmUsagePolicy
  machine_gate?: MachineGate
  recommended_extra_sources_count?: number
  updated_at: string
  version_history: Array<
    | string
    | {
        version?: string
        created_at?: string
        actor?: string
        change?: string
        audit_result_id?: string
      }
  >
}

export interface KnowledgeTreeNode {
  node_id: string
  parent_id: string | null
  path: string
  title: string
  domain: string
  subdomain: string
  level: number
  summary: string
  coverage_status: CoverageStatus
  review_status: NodeReviewStatus
  freshness_status: FreshnessStatus
  conflict_status: NodeConflictStatus
  approved_item_count: number
  reviewed_item_count: number
  source_count: number
  open_gaps: string[]
  related_nodes: string[]
  sort_order?: number
}

export type KnowledgeTreeLevel = 1 | 2 | 3

export interface KnowledgeTreeScope {
  level: KnowledgeTreeLevel
  node_id: string
  title: string
  path: string
}

export interface KnowledgeTreeScopeSummary {
  node_count: number
  approved_item_count: number
  reviewed_item_count: number
  candidate_count: number
  draft_count: number
  source_count: number
  open_gap_count: number
  conflict_count: number
}

export interface KnowledgeTreeThreeLevelViewModel {
  selected_level1_id: string | null
  selected_level2_id: string | null
  selected_level3_id: string | null
  level1_nodes: KnowledgeTreeNode[]
  level2_nodes: KnowledgeTreeNode[]
  level3_nodes: KnowledgeTreeNode[]
  current_scope: KnowledgeTreeScope | null
  ancestor_chain: KnowledgeTreeNode[]
  scope_summary: KnowledgeTreeScopeSummary
}

export interface KnowledgeTreeScopeIndexCounts {
  knowledge_total: number
  candidate_total: number
  reviewed: number
  approved: number
  accepted_for_draft: number
  needs_more_evidence: number
  rejected: number
  source_count: number
  open_gap_count: number
  conflict_count: number
}

export interface KnowledgeTreeScopeIndexNode {
  node_id: string
  descendant_node_ids: string[]
  knowledge_ids: string[]
  candidate_ids: string[]
  counts: KnowledgeTreeScopeIndexCounts
}

export interface KnowledgeTreeScopeIndex {
  schema_version: 'phase51.scope_index.v1'
  generated_at: string
  source: string
  source_version: Record<string, string>
  count: number
  nodes: Record<string, KnowledgeTreeScopeIndexNode>
}

export interface KnowledgeCardSummary {
  id: string
  title: string
  subtitle: string
  summary: string
  status: string
  kind: 'knowledge' | 'candidate'
  tree_node_id: string
  canonical_node_id: string
  source_count: number
  conflict_status: string
  freshness_status: string
  default_guidance: string
}

export interface KnowledgeCardDetail {
  id: string
  kind: 'knowledge' | 'candidate'
  summary: string
  raw: KnowledgeItem | IngestionCandidate
  loaded_from: 'formalKnowledgeItems' | 'phase23Candidates'
  loaded_at: string
}

export interface PagedResult<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
  source_version: string
  generated_at: string
}

export interface IngestionCandidate {
  candidate_id: string
  research_task_id: string
  partition_id?: string
  tree_node_id: string
  tree_path?: string
  canonical_node_id?: string
  claim: string
  title?: string
  normalized_claim?: string
  evidence_summary?: string
  interpretation_notes?: string
  domain?: string
  subdomain?: string
  rule_type?: string
  used_for?: string[]
  source_count: number
  source_quality_score: number
  source_refs?: CandidateSourceRef[]
  source_quality?: CandidateSourceQuality
  applicable_scope: string
  not_applicable_scope: string[]
  applies_when?: string[]
  not_applicable_when?: string[]
  assumptions?: string[]
  limitations?: string[]
  conflict_status: NodeConflictStatus | ConflictStatus
  conflict_audit?: CandidateConflictAudit
  confidence: Confidence
  freshness: Freshness
  review_status: CandidateReviewStatus
  ingestion_decision: CandidateIngestionDecision
  candidate_status?: CandidateAuditStatus
  workflow?: CandidateWorkflow
  decision_reason?: string
  reviewer?: string | null
  reviewed_at?: string | null
  open_questions?: string[]
  audit_log?: Array<{
    at: string
    actor: string
    action: string
    reason: string
    audit_result_id?: string
    knowledge_id?: string
    formal_knowledge_id?: string
    research_doc?: string
    audit_package?: string
    supplemental_reaudit_package_id?: string
    source_ids?: string[]
    contract_sha256?: string
    patch_notes?:
      | string[]
      | {
          source?: string[]
          content?: string[]
          boundary?: string[]
          conflict?: string[]
          [key: string]: unknown
        }
    [key: string]: unknown
  }>
  conversion_target?: CandidateConversionTarget
  knowledge_preview?: CandidateKnowledgePreview
  copyright?: {
    stores_full_text: boolean
    stores_long_quote: boolean
    summary_only: boolean
    license_notes: string | null
    reuse_risk: 'low' | 'medium' | 'high'
  }
  source_path?: string
  updated_at: string
}

export interface CandidateCoverageSummary {
  partition_id: string
  tree_node_id: string
  candidate_count: number
  accepted_for_draft_count: number
  needs_more_evidence_count: number
  blocked_count: number
  source_count: number
  conflict_count: number
}

export interface CandidateAuditHandoff {
  handoff_id: string
  phase: '24'
  target_task_id: 'CEK-TA-102'
  generated_at: string
  candidates: Array<{
    candidate_id: string
    decision: 'accepted_for_draft' | 'needs_more_evidence' | 'rejected'
    reason: string
    missing_fields: string[]
    blocking_issues: string[]
    target_knowledge_preview: CandidateKnowledgePreview
  }>
}

export interface SearchMatch {
  item_id: string
  title: string
  claim: string
  tree_node_id: string
  tree_path: string
  canonical_node_id?: string
  canonical_tree_path?: string
  domain: string
  source_count: number
  confidence: Confidence
  freshness: Freshness
  review_status: ReviewStatus
  conflict_status: ConflictStatus
  score: number
  recommended_next_action: string
  claim_type?: ClaimType
  llm_usage_policy?: LlmUsagePolicy
  machine_gate?: MachineGate
  recommended_extra_sources_count?: number
  why_matched?: {
    score: number
    reasons: string[]
  }
}

export interface BlockedSearchResult {
  item_id: string
  knowledge_id: string
  title: string
  blocked_reason: string
  review_status: ReviewStatus
  conflict_status: ConflictStatus
  freshness: Freshness
  has_source_refs: boolean
  tree_node_id: string
  canonical_node_id: string
  recommended_fix: string
  machine_gate?: MachineGate
}

export interface RuntimeAuditSummary {
  retrieval_policy_version: string
  result_count: number
  blocked_count: number
  returned_review_statuses: ReviewStatus[]
  returned_conflict_statuses: ConflictStatus[]
}

export interface SearchTestCase {
  test_id: string
  request_id?: string
  query: string
  task_type: string
  filters: {
    tree_node_id?: string
    canonical_node_id?: string
    domain?: string
    tree_path_prefix?: string
    canonical_tree_path_prefix?: string
  }
  status: 'pass' | 'warning' | 'fail'
  runtime_status?: 'ok' | 'warning' | 'error'
  warnings: string[]
  matches: SearchMatch[]
  blocked_results?: BlockedSearchResult[]
  audit?: RuntimeAuditSummary
}

export interface ProjectAdapterStatus {
  project_id: string
  project_name: string
  project_type: string
  adapter_status: 'pass' | 'warn' | 'fail'
  healthcheck_result: 'pass' | 'warn' | 'fail'
  missing_fields: string[]
  unsupported_modes: string[]
  allowed_tools: string[]
  blocked_tools: string[]
  project_fact_boundary: 'clear' | 'unclear'
  knowledge_query_scope: 'clear' | 'unclear'
  contribution_entrypoint: string
  updated_at: string
}

export interface TaskRecord {
  task_id: string
  question: string
  queries: string[]
  sources_used: string[]
  added_knowledge: string[]
  modified_knowledge: string[]
  conflicts_found: string[]
  human_confirmations: string[]
  executed_at: string
  status: 'done' | 'review' | 'blocked'
}

export interface ContributionRecord {
  contribution_id: string
  source_project: string
  project_type: string
  contribution_type: string
  status: 'proposed' | 'sanitized' | 'sourced' | 'classified' | 'conflict_checked' | 'reviewed' | 'accepted' | 'rejected' | 'needs_more_evidence'
  sanitization_status: 'proposed' | 'sanitized' | 'rejected'
  source_status: 'missing' | 'partial' | 'complete'
  conflict_status: ConflictStatus
  target_domain: string
  target_subdomain: string
  generalized_rule: string
  residual_risk: 'low' | 'medium' | 'high'
  review_decision: 'pending' | 'accepted' | 'rejected' | 'needs_more_evidence'
  updated_at: string
}

export interface AuditFilter {
  query: string
  domain: string
  source_type: string
  freshness: string
  review_status: string
  confidence: string
  conflict_status: string
}
