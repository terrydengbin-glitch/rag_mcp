<script setup lang="ts">
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>来源审计</h1>
        <p>{{ store.sources.length }} sources</p>
      </div>
    </header>
    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>来源</th>
            <th>类型</th>
            <th>发布方</th>
            <th>发布时间</th>
            <th>访问时间</th>
            <th>可靠性</th>
            <th>引用</th>
            <th>过期</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="source in store.sources" :key="source.source_id">
            <td>
              <strong>{{ source.title }}</strong>
              <small>{{ source.url || source.source_id }}</small>
            </td>
            <td>{{ source.source_type }}</td>
            <td>{{ source.publisher }}</td>
            <td>{{ source.published_at || 'unknown' }}</td>
            <td>{{ source.accessed_at }}</td>
            <td><StatusBadge :value="source.reliability" tone="confidence" /></td>
            <td>{{ source.cited_by.length }}</td>
            <td><StatusBadge :value="source.stale ? 'stale' : 'current'" tone="freshness" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
