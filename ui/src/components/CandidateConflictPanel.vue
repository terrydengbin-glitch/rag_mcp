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
        <h3>Conflict Audit</h3>
        <p class="muted-line">
          {{ candidate.conflict_audit?.checked_against.length || 0 }} checked / {{ candidate.conflict_audit?.conflicts.length || 0 }} records
        </p>
      </div>
      <div class="badge-row">
        <StatusBadge :value="candidate.conflict_status" tone="conflict" />
        <StatusBadge :value="candidate.conflict_audit?.approval_allowed ? 'approval_allowed' : 'approval_blocked'" />
      </div>
    </div>

    <p class="detail-note">{{ candidate.conflict_audit?.resolution_summary || 'No conflict summary recorded.' }}</p>

    <div v-if="candidate.conflict_audit?.checked_against.length" class="inline-token-list">
      <span v-for="item in candidate.conflict_audit.checked_against" :key="item">{{ item }}</span>
    </div>

    <div v-if="candidate.conflict_audit?.conflicts.length" class="evidence-list">
      <article v-for="conflict in candidate.conflict_audit.conflicts" :key="conflict.knowledge_id" class="evidence-row">
        <div>
          <strong>{{ conflict.knowledge_id }}</strong>
          <small>{{ conflict.conflict_type }} / {{ conflict.overlap_scope.domain }}.{{ conflict.overlap_scope.subdomain }}</small>
          <p>{{ conflict.resolution }}</p>
        </div>
        <div class="badge-row evidence-badges">
          <StatusBadge :value="conflict.severity" />
          <StatusBadge :value="conflict.requires_human_review ? 'human_review' : 'auto_clear'" />
          <small>{{ conflict.default_recommendation || '-' }}</small>
        </div>
      </article>
    </div>
    <div v-else class="empty-state">
      <strong>No conflict records</strong>
      <span>Conflict status still depends on the generated audit summary.</span>
    </div>
  </section>
</template>
