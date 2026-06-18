<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { AlertTriangle, ClipboardCheck, Download, FileText, FileWarning, Filter, Search, ShieldAlert } from '@lucide/vue'
import CandidateAuditChecklistPanel from '../components/CandidateAuditChecklistPanel.vue'
import CandidateConflictPanel from '../components/CandidateConflictPanel.vue'
import CandidateConversionPanel from '../components/CandidateConversionPanel.vue'
import CandidateGovernancePanel from '../components/CandidateGovernancePanel.vue'
import CandidateSourcePanel from '../components/CandidateSourcePanel.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { downloadCandidateAiAuditPackage } from '../data/candidateAuditPackage'
import {
  buildCandidateAuditHandoff,
  downloadCandidateAuditHandoffJson,
  downloadCandidateAuditHandoffMarkdown
} from '../data/candidateHandoff'
import { useAuditStore } from '../stores/auditStore'
import type { CandidateWorkflowQueueGroup, IngestionCandidate } from '../types'

type QueueGroupFilter = CandidateWorkflowQueueGroup | 'all'

const store = useAuditStore()
const route = useRoute()
const router = useRouter()

const query = ref('')
const partition = ref('all')
const candidateStatus = ref('all')
const queueGroup = ref<QueueGroupFilter>('pending')
const conflictStatus = ref('all')
const reliability = ref('all')
const riskLevelFilter = ref('all')
const pageSize = ref(50)
const currentPage = ref(1)
const selectedId = ref(store.ingestionCandidates[0]?.candidate_id || '')

const activeTreeNodeId = computed(() => {
  const value = route.query.tree_node_id
  return typeof value === 'string' ? value : ''
})

const activeTreeNode = computed(() => (activeTreeNodeId.value ? store.findTreeNode(activeTreeNodeId.value) : null))

const partitions = computed(() =>
  Array.from(new Set(store.ingestionCandidates.map((item) => item.partition_id).filter(Boolean))).sort()
)

const candidateStatuses = computed(() =>
  Array.from(new Set(store.ingestionCandidates.map((item) => item.candidate_status || 'needs_more_evidence'))).sort()
)

const conflictStatuses = computed(() =>
  Array.from(new Set(store.ingestionCandidates.map((item) => item.conflict_status))).sort()
)

const reliabilityOptions = computed(() =>
  Array.from(new Set(store.ingestionCandidates.map((item) => item.source_quality?.overall_reliability || item.confidence))).sort()
)

const riskLevelOptions = ['risk_blocked', 'risk_high', 'risk_medium', 'risk_low']

function workflowGroup(item: IngestionCandidate): CandidateWorkflowQueueGroup {
  if (item.workflow?.queue_group) return item.workflow.queue_group
  if (item.candidate_status === 'accepted_for_draft') return 'ai_passed'
  if (item.candidate_status === 'rejected') return 'rejected'
  if (item.candidate_status === 'needs_more_evidence' || item.candidate_status === 'blocked') return 'needs_more_evidence'
  return 'pending'
}

function workflowLabel(value: QueueGroupFilter) {
  const labels: Record<QueueGroupFilter, string> = {
    pending: '待审计',
    ai_passed: 'AI 已通过',
    needs_more_evidence: '需补证据',
    formalized: '已沉淀知识',
    rebuilt_archived: '已重建归档',
    rejected: '已拒绝',
    all: '全部'
  }
  return labels[value]
}

const summary = computed(() => {
  const total = store.ingestionCandidates.length
  const pending = store.ingestionCandidates.filter((item) => workflowGroup(item) === 'pending').length
  const aiPassed = store.ingestionCandidates.filter((item) => workflowGroup(item) === 'ai_passed').length
  const moreEvidence = store.ingestionCandidates.filter((item) => workflowGroup(item) === 'needs_more_evidence').length
  const formalized = store.ingestionCandidates.filter((item) => workflowGroup(item) === 'formalized').length
  const rebuiltArchived = store.ingestionCandidates.filter((item) => workflowGroup(item) === 'rebuilt_archived').length
  const rejected = store.ingestionCandidates.filter((item) => workflowGroup(item) === 'rejected').length
  const conflicts = store.ingestionCandidates.filter((item) => item.conflict_status !== 'none').length
  return { total, pending, aiPassed, moreEvidence, formalized, rebuiltArchived, rejected, conflicts }
})

const queueTabs = computed(() => [
  { value: 'pending' as const, label: workflowLabel('pending'), count: summary.value.pending },
  { value: 'ai_passed' as const, label: workflowLabel('ai_passed'), count: summary.value.aiPassed },
  { value: 'needs_more_evidence' as const, label: workflowLabel('needs_more_evidence'), count: summary.value.moreEvidence },
  { value: 'formalized' as const, label: workflowLabel('formalized'), count: summary.value.formalized },
  { value: 'rebuilt_archived' as const, label: workflowLabel('rebuilt_archived'), count: summary.value.rebuiltArchived },
  { value: 'rejected' as const, label: workflowLabel('rejected'), count: summary.value.rejected },
  { value: 'all' as const, label: workflowLabel('all'), count: summary.value.total }
])

const activeQueueLabel = computed(() => (activeTreeNodeId.value ? '知识树追踪' : workflowLabel(queueGroup.value)))

const exportScopeLabel = computed(() => `${activeQueueLabel.value} / ${filteredCandidates.value.length} 条`)

function shouldShowByQueue(item: IngestionCandidate) {
  if (activeTreeNodeId.value) return true
  return queueGroup.value === 'all' || workflowGroup(item) === queueGroup.value
}

function riskScore(item: IngestionCandidate) {
  let score = 0
  if (item.candidate_status === 'blocked') score += 100
  if (item.candidate_status === 'needs_more_evidence') score += 70
  if (item.conflict_status === 'confirmed') score += 60
  if (item.conflict_status === 'potential') score += 45
  if (item.conflict_status === 'resolved') score += 15
  if ((item.source_quality?.overall_reliability || item.confidence) === 'low') score += 35
  if (item.freshness === 'time_sensitive') score += 20
  score += item.knowledge_preview?.missing_fields.length || 0
  score += item.knowledge_preview?.blocking_issues.length || 0
  return score
}

const filteredCandidates = computed(() => {
  const q = query.value.trim().toLowerCase()
  return store.ingestionCandidates
    .filter((item) => {
      const reliabilityValue = item.source_quality?.overall_reliability || item.confidence
      const text = [
        item.candidate_id,
        item.research_task_id,
        item.partition_id,
        item.tree_node_id,
        item.tree_path,
        item.domain,
        item.subdomain,
        item.claim,
        item.evidence_summary
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
      return (
        (!q || text.includes(q)) &&
        (partition.value === 'all' || item.partition_id === partition.value) &&
        shouldShowByQueue(item) &&
        (candidateStatus.value === 'all' || item.candidate_status === candidateStatus.value) &&
        (conflictStatus.value === 'all' || item.conflict_status === conflictStatus.value) &&
        (reliability.value === 'all' || reliabilityValue === reliability.value) &&
        (riskLevelFilter.value === 'all' || riskLevel(item) === riskLevelFilter.value) &&
        (!activeTreeNodeId.value || store.candidateMatchesTreeNodeId(item, activeTreeNodeId.value))
      )
    })
    .sort((left, right) => riskScore(right) - riskScore(left) || right.source_quality_score - left.source_quality_score)
})

const pageCount = computed(() => Math.max(1, Math.ceil(filteredCandidates.value.length / pageSize.value)))

const paginatedCandidates = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredCandidates.value.slice(start, start + pageSize.value)
})

const pageRange = computed(() => {
  if (!filteredCandidates.value.length) return '0-0'
  const start = (currentPage.value - 1) * pageSize.value + 1
  const end = Math.min(filteredCandidates.value.length, start + pageSize.value - 1)
  return `${start}-${end}`
})

const selectedCandidate = computed(() => {
  return filteredCandidates.value.find((item) => item.candidate_id === selectedId.value) || filteredCandidates.value[0] || null
})

function riskLevel(item: IngestionCandidate) {
  const reliabilityValue = item.source_quality?.overall_reliability || item.confidence
  const conflictValue = String(item.conflict_status)
  if (
    item.candidate_status === 'blocked' ||
    conflictValue === 'confirmed' ||
    conflictValue === 'unchecked' ||
    item.source_count === 0 ||
    item.freshness === 'deprecated'
  ) {
    return 'risk_blocked'
  }
  if (
    item.candidate_status === 'needs_more_evidence' ||
    reliabilityValue === 'low' ||
    item.source_quality_score < 0.6 ||
    Boolean(item.knowledge_preview?.missing_fields.length) ||
    Boolean(item.knowledge_preview?.blocking_issues.length)
  ) {
    return 'risk_high'
  }
  if (conflictValue === 'potential' || item.freshness === 'time_sensitive' || !item.assumptions?.length || !item.limitations?.length) {
    return 'risk_medium'
  }
  return 'risk_low'
}

function riskReasons(item: IngestionCandidate) {
  const reasons: string[] = []
  const reliabilityValue = item.source_quality?.overall_reliability || item.confidence
  const conflictValue = String(item.conflict_status)
  if (item.source_count === 0) reasons.push('缺少来源，不能转 draft')
  if (reliabilityValue === 'low') reasons.push('来源可靠性偏低')
  if (['confirmed', 'unchecked'].includes(conflictValue)) reasons.push(`冲突状态为 ${conflictValue}`)
  if (item.candidate_status === 'blocked') reasons.push('候选状态已阻断')
  if (item.candidate_status === 'needs_more_evidence') reasons.push('需要补充证据')
  if (item.freshness === 'time_sensitive') reasons.push('时效敏感，需要复核日期')
  if (item.freshness === 'deprecated') reasons.push('已过期，不能作为可复用知识')
  item.knowledge_preview?.missing_fields.forEach((field) => reasons.push(`缺少字段：${field}`))
  item.knowledge_preview?.blocking_issues.forEach((issue) => reasons.push(`阻断项：${issue}`))
  if (!item.applies_when?.length || !item.not_applicable_when?.length || !item.assumptions?.length) {
    reasons.push('适用边界、非适用边界或假设不完整')
  }
  return reasons.length ? reasons : ['未发现阻断项，仍需人工复核来源和边界']
}

const selectedRiskLevel = computed(() => (selectedCandidate.value ? riskLevel(selectedCandidate.value) : 'risk_low'))
const selectedRiskReasons = computed(() => (selectedCandidate.value ? riskReasons(selectedCandidate.value) : []))

const selectedScope = computed(() => {
  const item = selectedCandidate.value
  if (!item) return { applies: [], notApplicable: [], assumptions: [], limitations: [] }
  return {
    applies: item.applies_when?.length ? item.applies_when : [item.applicable_scope || '未填写适用范围'],
    notApplicable: item.not_applicable_when?.length ? item.not_applicable_when : item.not_applicable_scope,
    assumptions: item.assumptions || [],
    limitations: item.limitations || []
  }
})

function candidateQueueTitle(item: IngestionCandidate) {
  const domain = [item.domain, item.subdomain].filter(Boolean).join('.')
  return domain || item.partition_id || item.tree_node_id
}

function candidateQueueSubtitle(item: IngestionCandidate) {
  return item.partition_id ? `${item.partition_id} / ${item.tree_node_id}` : item.tree_node_id
}

const handoff = computed(() => buildCandidateAuditHandoff(filteredCandidates.value))

const handoffSummary = computed(() => {
  const accepted = handoff.value.candidates.filter((item) => item.decision === 'accepted_for_draft').length
  const needsMoreEvidence = handoff.value.candidates.filter((item) => item.decision === 'needs_more_evidence').length
  const rejected = handoff.value.candidates.filter((item) => item.decision === 'rejected').length
  return { accepted, needsMoreEvidence, rejected }
})

watch(filteredCandidates, (items) => {
  if (currentPage.value > pageCount.value) {
    currentPage.value = pageCount.value
  }
  if (!items.some((item) => item.candidate_id === selectedId.value)) {
    selectedId.value = items[0]?.candidate_id || ''
  }
})

watch([query, partition, queueGroup, candidateStatus, conflictStatus, reliability, riskLevelFilter, pageSize], () => {
  currentPage.value = 1
})

function clearTreeFilter() {
  const nextQuery = { ...route.query }
  delete nextQuery.tree_node_id
  router.replace({ query: nextQuery })
}

function exportHandoffJson() {
  downloadCandidateAuditHandoffJson(handoff.value)
}

function exportHandoffMarkdown() {
  downloadCandidateAuditHandoffMarkdown(handoff.value)
}

function exportAiAuditPackage() {
  downloadCandidateAiAuditPackage(filteredCandidates.value)
}

function previousPage() {
  currentPage.value = Math.max(1, currentPage.value - 1)
}

function nextPage() {
  currentPage.value = Math.min(pageCount.value, currentPage.value + 1)
}
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>候选知识审计</h1>
        <p>{{ store.ingestionCandidates.length }} 条候选 / 生成时间 {{ store.phase23CandidateFixtureGeneratedAt || '加载中' }}</p>
      </div>
      <div class="header-actions">
        <StatusBadge value="candidate_only" />
        <button class="text-button" type="button" @click="exportAiAuditPackage">
          <Download :size="16" />
          <span>AI 审计包</span>
        </button>
        <button class="text-button" type="button" @click="exportHandoffJson">
          <Download :size="16" />
          <span>JSON</span>
        </button>
        <button class="text-button" type="button" @click="exportHandoffMarkdown">
          <FileText :size="16" />
          <span>Markdown</span>
        </button>
      </div>
    </header>

    <div class="data-load-banner panel" :class="`is-${store.dataState.state}`">
      <strong>{{ store.dataState.state === 'ready' ? '静态数据已加载' : store.dataState.state === 'error' ? '静态数据加载异常' : '正在加载静态数据' }}</strong>
      <span>{{ store.dataState.message }}</span>
    </div>

    <div class="metric-grid">
      <div class="metric-panel">
        <ClipboardCheck :size="20" />
        <span>候选</span>
        <strong>{{ summary.total }}</strong>
      </div>
      <div class="metric-panel">
        <ClipboardCheck :size="20" />
        <span>待审计</span>
        <strong>{{ summary.pending }}</strong>
      </div>
      <div class="metric-panel">
        <ShieldAlert :size="20" />
        <span>AI 已通过</span>
        <strong>{{ summary.aiPassed }}</strong>
      </div>
      <div class="metric-panel">
        <AlertTriangle :size="20" />
        <span>需补证据</span>
        <strong>{{ summary.moreEvidence }}</strong>
      </div>
      <div class="metric-panel">
        <FileWarning :size="20" />
        <span>已沉淀</span>
        <strong>{{ summary.formalized }}</strong>
      </div>
      <div class="metric-panel">
        <Download :size="20" />
        <span>交接 draft</span>
        <strong>{{ handoffSummary.accepted }}</strong>
        <small>{{ summary.conflicts }} 个冲突 / {{ summary.rebuiltArchived }} 条已重建归档 / {{ summary.rejected }} 条拒绝</small>
      </div>
    </div>

    <div class="candidate-filter-bar">
      <div class="search-box">
        <Search :size="17" />
        <input v-model="query" type="search" placeholder="搜索候选、声明或知识树节点" />
      </div>
      <select v-model="partition" aria-label="partition">
        <option value="all">全部分区</option>
        <option v-for="item in partitions" :key="item" :value="item">{{ item }}</option>
      </select>
      <select v-model="candidateStatus" aria-label="candidate status">
        <option value="all">全部候选状态</option>
        <option v-for="item in candidateStatuses" :key="item" :value="item">{{ item }}</option>
      </select>
      <select v-model="conflictStatus" aria-label="conflict status">
        <option value="all">全部冲突</option>
        <option v-for="item in conflictStatuses" :key="item" :value="item">{{ item }}</option>
      </select>
      <select v-model="reliability" aria-label="source reliability">
        <option value="all">全部可靠性</option>
        <option v-for="item in reliabilityOptions" :key="item" :value="item">{{ item }}</option>
      </select>
      <select v-model="riskLevelFilter" aria-label="risk level">
        <option value="all">全部风险</option>
        <option v-for="item in riskLevelOptions" :key="item" :value="item">{{ item }}</option>
      </select>
      <select v-model.number="pageSize" aria-label="page size">
        <option :value="20">20 / 页</option>
        <option :value="50">50 / 页</option>
        <option :value="100">100 / 页</option>
      </select>
      <button class="icon-button" type="button" title="Filters are local to this audit view">
        <Filter :size="17" />
      </button>
    </div>

    <div v-if="activeTreeNodeId" class="tree-filter-banner">
      <div>
        <strong>{{ activeTreeNode?.title || activeTreeNodeId }}</strong>
        <span>{{ activeTreeNode?.path || activeTreeNodeId }}</span>
      </div>
      <button type="button" @click="clearTreeFilter">Clear</button>
    </div>

    <div class="candidate-workbench candidate-audit-workbench">
      <section class="candidate-queue panel">
        <div class="panel-title-row">
          <div>
            <h2>审计队列</h2>
            <p class="muted-line">{{ activeQueueLabel }} / {{ pageRange }} / {{ filteredCandidates.length }} visible / risk sorted</p>
          </div>
        </div>

        <div v-if="!activeTreeNodeId" class="queue-tab-row">
          <button
            v-for="tab in queueTabs"
            :key="tab.value"
            type="button"
            class="queue-tab"
            :class="{ 'is-active': queueGroup === tab.value }"
            @click="queueGroup = tab.value"
          >
            <span>{{ tab.label }}</span>
            <strong>{{ tab.count }}</strong>
          </button>
        </div>

        <div v-if="!filteredCandidates.length" class="empty-state">
          <strong>当前分组没有候选</strong>
          <span>可切换到“已沉淀知识”或“全部”查看已通过审计并回链的候选。</span>
        </div>

        <button
          v-for="item in paginatedCandidates"
          :key="item.candidate_id"
          class="candidate-row"
          :class="{ 'is-selected-row': item.candidate_id === selectedCandidate?.candidate_id }"
          type="button"
          @click="selectedId = item.candidate_id"
        >
          <div class="candidate-row-main">
            <strong :title="item.title || item.claim">{{ candidateQueueTitle(item) }}</strong>
            <span :title="item.candidate_id">{{ item.candidate_id }}</span>
            <small :title="candidateQueueSubtitle(item)">{{ candidateQueueSubtitle(item) }}</small>
            <p :title="item.claim">{{ item.claim }}</p>
          </div>
          <div class="candidate-row-meta">
            <StatusBadge :value="riskLevel(item)" />
            <StatusBadge :value="workflowGroup(item)" />
            <StatusBadge :value="item.candidate_status || 'needs_more_evidence'" />
            <StatusBadge :value="item.conflict_status" tone="conflict" />
            <small>{{ item.source_count }} src / score {{ item.source_quality_score }}</small>
          </div>
        </button>

        <div v-if="filteredCandidates.length" class="queue-pagination">
          <button type="button" :disabled="currentPage === 1" @click="previousPage">上一页</button>
          <span>{{ currentPage }} / {{ pageCount }}</span>
          <button type="button" :disabled="currentPage === pageCount" @click="nextPage">下一页</button>
        </div>
      </section>

      <section v-if="selectedCandidate" class="candidate-reading-column">
        <article class="panel candidate-detail-panel candidate-reading-card">
          <div class="panel-title-row">
            <div>
              <p class="eyebrow-line">{{ selectedCandidate.partition_id }} / {{ selectedCandidate.domain }}.{{ selectedCandidate.subdomain }}</p>
              <h2>{{ selectedCandidate.title || selectedCandidate.claim }}</h2>
              <p class="muted-line">{{ selectedCandidate.candidate_id }}</p>
            </div>
            <div class="badge-row">
              <StatusBadge :value="selectedRiskLevel" />
              <StatusBadge :value="workflowGroup(selectedCandidate)" />
              <StatusBadge :value="selectedCandidate.review_status" />
              <StatusBadge :value="selectedCandidate.ingestion_decision" />
            </div>
          </div>

          <p class="statement">{{ selectedCandidate.claim }}</p>
          <p class="detail-note">{{ selectedCandidate.evidence_summary || selectedCandidate.interpretation_notes || '未记录证据摘要。' }}</p>

          <dl class="meta-grid detail-meta-grid">
            <dt>知识树</dt>
            <dd>{{ selectedCandidate.tree_node_id }}</dd>
            <dt>规范节点</dt>
            <dd>{{ selectedCandidate.canonical_node_id || '-' }}</dd>
            <dt>路径</dt>
            <dd>{{ selectedCandidate.tree_path || '-' }}</dd>
            <dt>来源</dt>
            <dd>
              {{ selectedCandidate.source_count }} 个来源 / {{ selectedCandidate.source_quality?.overall_reliability || selectedCandidate.confidence }}
            </dd>
            <dt>目标知识</dt>
            <dd>{{ selectedCandidate.conversion_target?.proposed_knowledge_id || '-' }}</dd>
            <dt>工作流</dt>
            <dd>{{ selectedCandidate.workflow?.stage || workflowGroup(selectedCandidate) }}</dd>
            <dt>正式知识</dt>
            <dd>{{ selectedCandidate.workflow?.formal_knowledge_id || '-' }} / {{ selectedCandidate.workflow?.formal_review_status || '-' }}</dd>
            <dt>替代候选</dt>
            <dd>{{ selectedCandidate.workflow?.replacement_candidate_id || '-' }}</dd>
            <dt>AI 审计</dt>
            <dd>{{ selectedCandidate.workflow?.ai_audit_result_id || '-' }}</dd>
            <dt>下一步</dt>
            <dd>{{ selectedCandidate.workflow?.next_action || '-' }}</dd>
          </dl>

          <div class="scope-review-grid">
            <section>
              <h3>适用范围</h3>
              <ul>
                <li v-for="item in selectedScope.applies" :key="item">{{ item }}</li>
              </ul>
            </section>
            <section>
              <h3>不适用</h3>
              <ul>
                <li v-for="item in selectedScope.notApplicable" :key="item">{{ item }}</li>
              </ul>
            </section>
            <section>
              <h3>假设</h3>
              <ul v-if="selectedScope.assumptions.length">
                <li v-for="item in selectedScope.assumptions" :key="item">{{ item }}</li>
              </ul>
              <p v-else class="muted-line">缺少 assumptions，不能跳过人工复核。</p>
            </section>
            <section>
              <h3>限制</h3>
              <ul v-if="selectedScope.limitations.length">
                <li v-for="item in selectedScope.limitations" :key="item">{{ item }}</li>
              </ul>
              <p v-else class="muted-line">暂无 limitations。</p>
            </section>
          </div>
        </article>

        <div class="candidate-panel-grid">
          <CandidateSourcePanel :candidate="selectedCandidate" />
          <CandidateConflictPanel :candidate="selectedCandidate" />
          <CandidateConversionPanel :candidate="selectedCandidate" />
        </div>
      </section>

      <aside v-if="selectedCandidate" class="candidate-audit-rail">
        <CandidateAuditChecklistPanel :candidate="selectedCandidate" />

        <section class="audit-subpanel">
          <div class="subpanel-title-row">
            <div>
              <h3>风险摘要</h3>
              <p class="muted-line">人工审核优先看这里</p>
            </div>
            <StatusBadge :value="selectedRiskLevel" />
          </div>
          <ul class="risk-reason-list">
            <li v-for="reason in selectedRiskReasons" :key="reason">{{ reason }}</li>
          </ul>
        </section>

        <CandidateGovernancePanel :candidate="selectedCandidate" />

        <section class="audit-subpanel handoff-panel">
          <div class="subpanel-title-row">
            <div>
              <h3>CEK-TA-102 交接</h3>
              <p class="muted-line">当前导出范围：{{ exportScopeLabel }}</p>
            </div>
            <StatusBadge value="draft_only" />
          </div>
          <dl class="meta-grid compact-meta-grid">
            <dt>accepted</dt>
            <dd>{{ handoffSummary.accepted }}</dd>
            <dt>more</dt>
            <dd>{{ handoffSummary.needsMoreEvidence }}</dd>
            <dt>rejected</dt>
            <dd>{{ handoffSummary.rejected }}</dd>
          </dl>
          <div class="handoff-actions">
            <button class="text-button" type="button" @click="exportAiAuditPackage">
              <Download :size="16" />
              <span>一键导出 AI 审计包 JSON</span>
            </button>
            <button class="text-button" type="button" @click="exportHandoffJson">
              <Download :size="16" />
              <span>JSON handoff</span>
            </button>
            <button class="text-button" type="button" @click="exportHandoffMarkdown">
              <FileText :size="16" />
              <span>Markdown handoff</span>
            </button>
          </div>
        </section>
      </aside>
    </div>
  </section>
</template>
