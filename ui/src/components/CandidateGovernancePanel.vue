<script setup lang="ts">
import { computed } from 'vue'
import StatusBadge from './StatusBadge.vue'
import type { IngestionCandidate } from '../types'

const props = defineProps<{
  candidate: IngestionCandidate
}>()

const gates = computed(() => [
  {
    label: 'source_refs',
    pass: Boolean(props.candidate.source_refs?.length),
    detail: `${props.candidate.source_refs?.length || 0} source refs`
  },
  {
    label: 'source_reliability',
    pass: ['high', 'medium'].includes(props.candidate.source_quality?.overall_reliability || props.candidate.confidence),
    detail: props.candidate.source_quality?.overall_reliability || props.candidate.confidence
  },
  {
    label: 'applicability',
    pass: Boolean(props.candidate.applies_when?.length && props.candidate.not_applicable_when?.length && props.candidate.assumptions?.length),
    detail: 'applies / not_applicable / assumptions'
  },
  {
    label: 'conflict_gate',
    pass: ['none', 'resolved'].includes(String(props.candidate.conflict_status)) && Boolean(props.candidate.conflict_audit?.approval_allowed),
    detail: String(props.candidate.conflict_status)
  },
  {
    label: 'copyright',
    pass: Boolean(
      props.candidate.copyright?.summary_only &&
        !props.candidate.copyright?.stores_full_text &&
        !props.candidate.copyright?.stores_long_quote
    ),
    detail: props.candidate.copyright?.reuse_risk || '-'
  },
  {
    label: 'draft_only',
    pass: props.candidate.conversion_target?.target_review_status === 'draft',
    detail: props.candidate.conversion_target?.target_review_status || '-'
  }
])
</script>

<template>
  <section class="audit-subpanel">
    <div class="subpanel-title-row">
      <div>
        <h3>Governance Gates</h3>
        <p class="muted-line">candidate cannot become approved from this view</p>
      </div>
      <StatusBadge :value="candidate.candidate_status || 'needs_more_evidence'" />
    </div>

    <div class="gate-list">
      <div v-for="gate in gates" :key="gate.label" class="gate-row">
        <strong>{{ gate.label }}</strong>
        <span>{{ gate.detail }}</span>
        <StatusBadge :value="gate.pass ? 'pass' : 'fail'" />
      </div>
    </div>

    <div class="detail-section-grid single-gap">
      <section>
        <h3>Missing Fields</h3>
        <ul v-if="candidate.knowledge_preview?.missing_fields.length">
          <li v-for="item in candidate.knowledge_preview.missing_fields" :key="item">{{ item }}</li>
        </ul>
        <p v-else class="muted-line">No missing fields in generated preview.</p>
      </section>
      <section>
        <h3>Blocking Issues</h3>
        <ul v-if="candidate.knowledge_preview?.blocking_issues.length">
          <li v-for="item in candidate.knowledge_preview.blocking_issues" :key="item">{{ item }}</li>
        </ul>
        <p v-else class="muted-line">No blocking issues in generated preview.</p>
      </section>
    </div>
  </section>
</template>
