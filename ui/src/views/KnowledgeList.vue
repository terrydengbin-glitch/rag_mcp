<script setup lang="ts">
import FilterBar from '../components/FilterBar.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>知识检索</h1>
        <p>{{ store.filteredKnowledge.length }} / {{ store.knowledgeItems.length }}</p>
      </div>
    </header>
    <FilterBar />
    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>知识</th>
            <th>domain</th>
            <th>source</th>
            <th>freshness</th>
            <th>review</th>
            <th>confidence</th>
            <th>conflict</th>
            <th>updated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in store.filteredKnowledge" :key="item.knowledge_id">
            <td>
              <RouterLink class="primary-link" :to="`/knowledge/${item.knowledge_id}`">{{ item.title }}</RouterLink>
              <small>{{ item.knowledge_id }}</small>
            </td>
            <td>{{ item.domain }} / {{ item.subdomain }}</td>
            <td>{{ item.source_type }}</td>
            <td><StatusBadge :value="item.freshness" tone="freshness" /></td>
            <td><StatusBadge :value="item.review_status" /></td>
            <td><StatusBadge :value="item.confidence" tone="confidence" /></td>
            <td><StatusBadge :value="item.conflict_status" tone="conflict" /></td>
            <td>{{ item.updated_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
