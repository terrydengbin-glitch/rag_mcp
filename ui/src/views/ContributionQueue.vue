<script setup lang="ts">
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>知识倒灌队列</h1>
        <p>{{ store.contributions.length }} contributions / read-only mock</p>
      </div>
    </header>
    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>贡献</th>
            <th>来源项目</th>
            <th>类型</th>
            <th>状态</th>
            <th>脱敏</th>
            <th>来源</th>
            <th>冲突</th>
            <th>目标</th>
            <th>残余风险</th>
            <th>审计结论</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in store.contributions" :key="item.contribution_id">
            <td>
              <strong>{{ item.contribution_id }}</strong>
              <small>{{ item.generalized_rule }}</small>
            </td>
            <td>
              {{ item.source_project }}
              <small>{{ item.project_type }}</small>
            </td>
            <td>{{ item.contribution_type }}</td>
            <td><StatusBadge :value="item.status" /></td>
            <td><StatusBadge :value="item.sanitization_status" /></td>
            <td><StatusBadge :value="item.source_status" tone="confidence" /></td>
            <td><StatusBadge :value="item.conflict_status" tone="conflict" /></td>
            <td>{{ item.target_domain }} / {{ item.target_subdomain }}</td>
            <td><StatusBadge :value="item.residual_risk" tone="confidence" /></td>
            <td>
              <StatusBadge :value="item.review_decision" />
              <small>{{ item.updated_at }}</small>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
