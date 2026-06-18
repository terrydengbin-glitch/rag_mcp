<script setup lang="ts">
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>冲突审计</h1>
        <p>{{ store.conflicts.length }} conflicts</p>
      </div>
    </header>
    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>类型</th>
            <th>双方</th>
            <th>来源等级</th>
            <th>适用范围</th>
            <th>版本</th>
            <th>消解</th>
            <th>结论</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="conflict in store.conflicts" :key="conflict.conflict_id">
            <td>
              <StatusBadge :value="conflict.conflict_type" tone="conflict" />
              <small>{{ conflict.severity }}</small>
            </td>
            <td>
              <RouterLink :to="`/knowledge/${conflict.left_id}`">{{ conflict.left_id }}</RouterLink>
              <span class="muted-line">{{ conflict.right_id }}</span>
            </td>
            <td>{{ conflict.left_source_reliability }} / {{ conflict.right_source_reliability }}</td>
            <td>{{ conflict.scope_compare }}</td>
            <td>{{ conflict.version_compare }}</td>
            <td>{{ conflict.resolution }}</td>
            <td><StatusBadge :value="conflict.review_decision" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
