<script setup lang="ts">
import { computed } from 'vue'
import { AlertTriangle, CheckCircle2, Clock3, Database, FileWarning } from '@lucide/vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()

function getKnowledgeTimestamp(updatedAt: string) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(updatedAt)) {
    return Date.parse(`${updatedAt}T00:00:00+08:00`)
  }
  const parsed = Date.parse(updatedAt || '')
  return Number.isNaN(parsed) ? 0 : parsed
}

function padTimePart(value: number) {
  return String(value).padStart(2, '0')
}

function formatAddedTime(updatedAt: string) {
  const timestamp = getKnowledgeTimestamp(updatedAt)
  if (!timestamp) return '添加时间：未知'
  const utc8 = new Date(timestamp + 8 * 60 * 60 * 1000)
  const year = utc8.getUTCFullYear()
  const month = padTimePart(utc8.getUTCMonth() + 1)
  const day = padTimePart(utc8.getUTCDate())
  const hour = padTimePart(utc8.getUTCHours())
  const minute = padTimePart(utc8.getUTCMinutes())
  return `添加时间：${year}-${month}-${day} ${hour}:${minute} UTC+8`
}

const recentKnowledgeItems = computed(() =>
  [...store.knowledgeItems].sort((left, right) => {
    const byUpdatedAt = getKnowledgeTimestamp(right.updated_at) - getKnowledgeTimestamp(left.updated_at)
    if (byUpdatedAt !== 0) return byUpdatedAt
    return right.knowledge_id.localeCompare(left.knowledge_id)
  }),
)
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>知识审计工作台</h1>
        <p>Phase 7 / local audit dataset</p>
      </div>
      <StatusBadge value="mock_data" tone="freshness" />
    </header>

    <div class="metric-grid">
      <div class="metric-panel">
        <Database :size="20" />
        <span>知识条目</span>
        <strong>{{ store.summary.total }}</strong>
      </div>
      <div class="metric-panel">
        <CheckCircle2 :size="20" />
        <span>已批准</span>
        <strong>{{ store.summary.approved }}</strong>
      </div>
      <div class="metric-panel">
        <AlertTriangle :size="20" />
        <span>待处理冲突</span>
        <strong>{{ store.summary.conflictsOpen }}</strong>
      </div>
      <div class="metric-panel">
        <Clock3 :size="20" />
        <span>时间敏感</span>
        <strong>{{ store.summary.timeSensitive }}</strong>
      </div>
      <div class="metric-panel">
        <FileWarning :size="20" />
        <span>过期来源</span>
        <strong>{{ store.summary.stale }}</strong>
      </div>
    </div>

    <div class="two-column">
      <section class="panel">
        <h2>Domain 分布</h2>
        <div class="bar-list">
          <div v-for="domain in store.domains" :key="domain" class="bar-row">
            <span>{{ domain }}</span>
            <div><i :style="{ width: `${store.knowledgeItems.filter((item) => item.domain === domain).length * 34}%` }" /></div>
            <b>{{ store.knowledgeItems.filter((item) => item.domain === domain).length }}</b>
          </div>
        </div>
      </section>
      <section class="panel">
        <h2>最近更新</h2>
        <div class="compact-list recent-update-list">
          <RouterLink v-for="item in recentKnowledgeItems" :key="item.knowledge_id" :to="`/knowledge/${item.knowledge_id}`">
            <span class="recent-update-copy">
              <strong>{{ item.title }}</strong>
              <small>{{ formatAddedTime(item.updated_at) }}</small>
            </span>
            <StatusBadge :value="item.review_status" />
          </RouterLink>
        </div>
      </section>
    </div>
  </section>
</template>
