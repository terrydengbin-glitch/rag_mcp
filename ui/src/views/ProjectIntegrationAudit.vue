<script setup lang="ts">
import { PlugZap, ShieldOff } from '@lucide/vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>项目接入审计</h1>
        <p>{{ store.projectAdapters.length }} adapters / Phase 10 healthcheck</p>
      </div>
    </header>

    <div class="table-shell">
      <table>
        <thead>
          <tr>
            <th>项目</th>
            <th>状态</th>
            <th>事实边界</th>
            <th>查询范围</th>
            <th>缺失字段</th>
            <th>不支持模式</th>
            <th>允许工具</th>
            <th>阻断工具</th>
            <th>倒灌入口</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="adapter in store.projectAdapters" :key="adapter.project_id">
            <td>
              <strong>{{ adapter.project_name }}</strong>
              <small>{{ adapter.project_id }}</small>
              <small>{{ adapter.project_type }}</small>
            </td>
            <td>
              <StatusBadge :value="adapter.adapter_status" />
              <small>healthcheck: {{ adapter.healthcheck_result }}</small>
            </td>
            <td><StatusBadge :value="adapter.project_fact_boundary" /></td>
            <td><StatusBadge :value="adapter.knowledge_query_scope" /></td>
            <td>
              <ul v-if="adapter.missing_fields.length">
                <li v-for="field in adapter.missing_fields" :key="field">{{ field }}</li>
              </ul>
              <span v-else>-</span>
            </td>
            <td>
              <ul v-if="adapter.unsupported_modes.length">
                <li v-for="mode in adapter.unsupported_modes" :key="mode">{{ mode }}</li>
              </ul>
              <span v-else>-</span>
            </td>
            <td>
              <div class="tool-list">
                <span v-for="tool in adapter.allowed_tools" :key="tool"><PlugZap :size="13" />{{ tool }}</span>
              </div>
            </td>
            <td>
              <div class="tool-list blocked">
                <span v-for="tool in adapter.blocked_tools" :key="tool"><ShieldOff :size="13" />{{ tool }}</span>
              </div>
            </td>
            <td>
              {{ adapter.contribution_entrypoint }}
              <small>{{ adapter.updated_at }}</small>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
