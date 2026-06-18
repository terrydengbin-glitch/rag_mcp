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
        <h3>Draft Conversion Preview</h3>
        <p class="muted-line">{{ candidate.conversion_target?.target_schema || 'cek_ta_knowledge_item' }}</p>
      </div>
      <StatusBadge :value="candidate.conversion_target?.target_review_status || 'draft'" />
    </div>

    <dl class="meta-grid compact-meta-grid">
      <dt>knowledge_id</dt>
      <dd>{{ candidate.knowledge_preview?.proposed_knowledge_id || candidate.conversion_target?.proposed_knowledge_id || '-' }}</dd>
      <dt>domain</dt>
      <dd>{{ candidate.knowledge_preview?.domain || candidate.domain || '-' }}</dd>
      <dt>subdomain</dt>
      <dd>{{ candidate.knowledge_preview?.subdomain || candidate.subdomain || '-' }}</dd>
      <dt>tree_node</dt>
      <dd>{{ candidate.knowledge_preview?.tree_node_id || candidate.tree_node_id }}</dd>
      <dt>canonical</dt>
      <dd>{{ candidate.knowledge_preview?.canonical_node_id || candidate.canonical_node_id || '-' }}</dd>
      <dt>source_count</dt>
      <dd>{{ candidate.knowledge_preview?.source_count ?? candidate.source_count }}</dd>
    </dl>

    <div class="detail-section-grid single-gap">
      <section>
        <h3>Applies When</h3>
        <ul>
          <li v-for="item in candidate.applies_when" :key="item">{{ item }}</li>
        </ul>
      </section>
      <section>
        <h3>Not Applicable</h3>
        <ul>
          <li v-for="item in candidate.not_applicable_when" :key="item">{{ item }}</li>
        </ul>
      </section>
      <section>
        <h3>Assumptions</h3>
        <ul>
          <li v-for="item in candidate.assumptions" :key="item">{{ item }}</li>
        </ul>
      </section>
      <section>
        <h3>Conversion Flags</h3>
        <div class="inline-token-list">
          <span>skill {{ candidate.conversion_target?.skill_candidate ? 'yes' : 'no' }}</span>
          <span>eval {{ candidate.conversion_target?.eval_case_candidate ? 'yes' : 'no' }}</span>
          <span>review_status draft</span>
        </div>
      </section>
    </div>
  </section>
</template>
