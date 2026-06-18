<script setup lang="ts">
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>Codex 任务记录</h1>
        <p>{{ store.tasks.length }} tasks</p>
      </div>
    </header>
    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>任务</th>
            <th>问题</th>
            <th>关键词</th>
            <th>来源</th>
            <th>新增</th>
            <th>修改</th>
            <th>冲突</th>
            <th>人工确认</th>
            <th>时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="task in store.tasks" :key="task.task_id">
            <td>
              <strong>{{ task.task_id }}</strong>
              <StatusBadge :value="task.status" />
            </td>
            <td>{{ task.question }}</td>
            <td>{{ task.queries.join(', ') }}</td>
            <td>{{ task.sources_used.join(', ') }}</td>
            <td>{{ task.added_knowledge.length }}</td>
            <td>{{ task.modified_knowledge.length }}</td>
            <td>{{ task.conflicts_found.join(', ') || 'none' }}</td>
            <td>{{ task.human_confirmations.join('; ') || 'none' }}</td>
            <td>{{ task.executed_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
