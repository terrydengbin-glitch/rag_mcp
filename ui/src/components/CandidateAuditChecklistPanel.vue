<script setup lang="ts">
import { computed } from 'vue'
import StatusBadge from './StatusBadge.vue'
import type { IngestionCandidate } from '../types'

const props = defineProps<{
  candidate: IngestionCandidate
}>()

type CheckStatus = 'pass' | 'warning' | 'fail'

function checkStatus(pass: boolean, warning = false): CheckStatus {
  if (pass) return 'pass'
  return warning ? 'warning' : 'fail'
}

const missingFields = computed(() => props.candidate.knowledge_preview?.missing_fields || [])
const blockingIssues = computed(() => props.candidate.knowledge_preview?.blocking_issues || [])
const reliability = computed(() => props.candidate.source_quality?.overall_reliability || props.candidate.confidence)
const conflictStatus = computed(() => String(props.candidate.conflict_status))
const hasScope = computed(() =>
  Boolean(
    props.candidate.applies_when?.length &&
      props.candidate.not_applicable_when?.length &&
      props.candidate.assumptions?.length
  )
)
const conflictAllowsDraft = computed(() =>
  ['none', 'resolved'].includes(conflictStatus.value) && Boolean(props.candidate.conflict_audit?.approval_allowed)
)
const canAcceptForDraft = computed(() =>
  Boolean(
    props.candidate.source_refs?.length &&
      ['high', 'medium'].includes(reliability.value) &&
      conflictAllowsDraft.value &&
      hasScope.value &&
      props.candidate.tree_node_id &&
      !missingFields.value.length &&
      !blockingIssues.value.length &&
      props.candidate.conversion_target?.target_review_status === 'draft'
  )
)

const nextActions = computed(() => {
  const actions: string[] = []
  if (!props.candidate.source_refs?.length) actions.push('补充至少一个可追踪来源')
  if (!['high', 'medium'].includes(reliability.value)) actions.push('提高来源质量或补充更权威来源')
  if (['confirmed', 'unchecked'].includes(conflictStatus.value)) actions.push('完成冲突审计并写明消解结论')
  if (!hasScope.value) actions.push('补齐适用范围、不适用范围和假设')
  if (!props.candidate.canonical_node_id) actions.push('确认 canonical_node_id 和知识树归类')
  missingFields.value.forEach((field) => actions.push(`补齐字段：${field}`))
  blockingIssues.value.forEach((issue) => actions.push(`处理阻断项：${issue}`))
  return actions.length ? actions : ['可进入 CEK-TA-102 handoff，仍需人工复核来源原文']
})

const checks = computed(() => [
  {
    key: 'has_sources',
    label: '有可追踪来源',
    status: checkStatus(Boolean(props.candidate.source_refs?.length)),
    reason: `${props.candidate.source_count} sources`
  },
  {
    key: 'source_quality',
    label: '来源质量足够',
    status: checkStatus(['high', 'medium'].includes(reliability.value), reliability.value === 'low'),
    reason: `reliability ${reliability.value} / score ${props.candidate.source_quality_score}`
  },
  {
    key: 'conflict_checked',
    label: '冲突已审计',
    status: checkStatus(conflictAllowsDraft.value, conflictStatus.value === 'potential'),
    reason: props.candidate.conflict_audit?.resolution_summary || conflictStatus.value
  },
  {
    key: 'scope_defined',
    label: '适用边界完整',
    status: checkStatus(hasScope.value),
    reason: 'applies / not applicable / assumptions'
  },
  {
    key: 'tree_classified',
    label: '知识树归类明确',
    status: checkStatus(Boolean(props.candidate.tree_node_id && props.candidate.canonical_node_id)),
    reason: props.candidate.canonical_node_id || props.candidate.tree_node_id || 'missing tree node'
  },
  {
    key: 'draft_ready',
    label: '可进入 draft 交接',
    status: checkStatus(canAcceptForDraft.value, props.candidate.candidate_status === 'needs_more_evidence'),
    reason: canAcceptForDraft.value ? 'ready for CEK-TA-102 handoff' : 'must resolve warnings or blockers first'
  }
])
</script>

<template>
  <section class="audit-subpanel checklist-panel">
    <div class="subpanel-title-row">
      <div>
        <h3>人工审核 Checklist</h3>
        <p class="muted-line">只判断能否交接 CEK-TA-102，不做正式入库</p>
      </div>
      <StatusBadge :value="canAcceptForDraft ? 'accepted_for_draft' : 'needs_review'" />
    </div>

    <div class="checklist-list">
      <div v-for="check in checks" :key="check.key" class="checklist-row" :class="`check-${check.status}`">
        <StatusBadge :value="check.status" />
        <div>
          <strong>{{ check.label }}</strong>
          <span>{{ check.reason }}</span>
        </div>
      </div>
    </div>

    <div v-if="missingFields.length || blockingIssues.length" class="blocker-box">
      <strong>阻断和缺口</strong>
      <ul>
        <li v-for="item in blockingIssues" :key="`blocking-${item}`">{{ item }}</li>
        <li v-for="item in missingFields" :key="`missing-${item}`">{{ item }}</li>
      </ul>
    </div>

    <div class="next-action-box">
      <strong>下一步动作</strong>
      <ul>
        <li v-for="item in nextActions" :key="item">{{ item }}</li>
      </ul>
    </div>
  </section>
</template>
