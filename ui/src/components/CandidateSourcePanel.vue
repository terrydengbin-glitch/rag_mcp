<script setup lang="ts">
import StatusBadge from './StatusBadge.vue'
import type { IngestionCandidate } from '../types'

defineProps<{
  candidate: IngestionCandidate
}>()
</script>

<template>
  <section class="audit-subpanel">
    <div class="subpanel-title-row">
      <div>
        <h3>Source Evidence</h3>
        <p class="muted-line">
          {{ candidate.source_count }} sources / score {{ candidate.source_quality_score }}
        </p>
      </div>
      <StatusBadge :value="candidate.source_quality?.overall_reliability || candidate.confidence" tone="confidence" />
    </div>

    <dl class="meta-grid compact-meta-grid">
      <dt>primary</dt>
      <dd>{{ candidate.source_quality?.primary_source_count ?? 0 }}</dd>
      <dt>supporting</dt>
      <dd>{{ candidate.source_quality?.supporting_source_count ?? 0 }}</dd>
      <dt>low</dt>
      <dd>{{ candidate.source_quality?.low_reliability_source_count ?? 0 }}</dd>
      <dt>version</dt>
      <dd>{{ candidate.source_quality?.score_version || '-' }}</dd>
    </dl>

    <div v-if="candidate.source_refs?.length" class="evidence-list">
      <article v-for="source in candidate.source_refs" :key="source.source_id" class="evidence-row">
        <div>
          <strong>{{ source.title }}</strong>
          <small>{{ source.publisher || '-' }} / {{ source.accessed_at }}</small>
          <p>{{ source.evidence_summary }}</p>
          <a v-if="source.url" :href="source.url" target="_blank" rel="noreferrer">{{ source.url }}</a>
        </div>
        <div class="badge-row evidence-badges">
          <StatusBadge :value="source.source_type" />
          <StatusBadge :value="source.reliability" tone="confidence" />
          <StatusBadge :value="source.freshness" tone="freshness" />
          <small>score {{ source.score }}</small>
        </div>
      </article>
    </div>
    <div v-else class="empty-state">
      <strong>No source refs</strong>
      <span>This candidate must stay out of draft conversion until evidence is attached.</span>
    </div>
  </section>
</template>
