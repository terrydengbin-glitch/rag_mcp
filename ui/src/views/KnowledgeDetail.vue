<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const route = useRoute()
const store = useAuditStore()
const item = computed(() => store.findKnowledge(String(route.params.id)))

type VersionHistoryEntry = NonNullable<typeof item.value>['version_history'][number]

function versionHistoryKey(history: VersionHistoryEntry, index: number) {
  if (typeof history === 'string') return `${history}-${index}`
  return `${history.version || 'version'}-${history.created_at || 'date'}-${history.audit_result_id || index}`
}

function versionHistoryText(history: VersionHistoryEntry) {
  if (typeof history === 'string') return history
  const parts = [
    history.version,
    history.created_at,
    history.actor,
    history.change,
    history.audit_result_id ? `审计：${history.audit_result_id}` : ''
  ].filter(Boolean)
  return parts.join(' / ')
}
</script>

<template>
  <section v-if="item" class="view-stack">
    <header class="view-header">
      <div>
        <h1>{{ item.title }}</h1>
        <p>{{ item.knowledge_id }}</p>
      </div>
      <div class="badge-row">
        <StatusBadge :value="item.review_status" />
        <StatusBadge :value="item.conflict_status" tone="conflict" />
        <StatusBadge :value="item.freshness" tone="freshness" />
        <StatusBadge :value="item.machine_gate?.default_guidance || 'deny'" />
      </div>
    </header>

    <section class="panel detail-panel">
      <h2>规则内容</h2>
      <p class="statement">{{ item.statement }}</p>
      <p>{{ item.rationale }}</p>
    </section>

    <div class="two-column">
      <section class="panel">
        <h2>AI 使用门控</h2>
        <dl class="meta-grid">
          <dt>claim_type</dt><dd>{{ item.claim_type || 'methodological_constraint' }}</dd>
          <dt>默认指导</dt><dd>{{ item.machine_gate?.default_guidance || 'deny' }}</dd>
          <dt>门控原因</dt><dd>{{ item.machine_gate?.reason || '暂无机器门控原因。' }}</dd>
          <dt>必须上下文</dt><dd>{{ item.llm_usage_policy?.required_context.join(' / ') }}</dd>
          <dt>补充来源</dt><dd>{{ item.recommended_extra_sources_count || 0 }}</dd>
        </dl>
        <h3>AI 可用方式</h3>
        <ul><li v-for="entry in item.llm_usage_policy?.allowed || []" :key="entry">{{ entry }}</li></ul>
        <h3>AI 禁止方式</h3>
        <ul><li v-for="entry in item.llm_usage_policy?.not_allowed || []" :key="entry">{{ entry }}</li></ul>
      </section>
      <section class="panel">
        <h2>分类说明</h2>
        <p>{{ item.classification_notes || 'UI 知识树节点与 canonical 分类已对齐。' }}</p>
        <h3>阻断原因</h3>
        <ul><li v-for="entry in item.machine_gate?.blocking_reasons || []" :key="entry">{{ entry }}</li></ul>
      </section>
    </div>

    <div class="two-column">
      <section class="panel">
        <h2>适用范围</h2>
        <dl class="meta-grid">
          <dt>市场</dt><dd>{{ item.applies_to.market }}</dd>
          <dt>资产</dt><dd>{{ item.applies_to.asset }}</dd>
          <dt>周期</dt><dd>{{ item.applies_to.timeframe }}</dd>
          <dt>数据粒度</dt><dd>{{ item.applies_to.data_granularity }}</dd>
          <dt>项目类型</dt><dd>{{ item.applies_to.project_type }}</dd>
        </dl>
      </section>
      <section class="panel">
        <h2>假设与边界</h2>
        <h3>前置假设</h3>
        <ul><li v-for="entry in item.assumptions" :key="entry">{{ entry }}</li></ul>
        <h3>不适用场景</h3>
        <ul><li v-for="entry in item.not_applicable_when" :key="entry">{{ entry }}</li></ul>
      </section>
    </div>

    <section class="panel">
      <h2>来源</h2>
      <div class="source-grid">
        <div v-for="source in item.sources" :key="source.source_id" class="source-row">
          <strong>{{ source.title }}</strong>
          <span>{{ source.source_type }} / {{ source.publisher }}</span>
          <StatusBadge :value="source.reliability" tone="confidence" />
          <b>{{ source.score }}</b>
        </div>
      </div>
    </section>

    <section class="panel">
      <h2>冲突与版本</h2>
      <p>{{ item.resolution || '无已知冲突。' }}</p>
      <div class="compact-list">
        <span
          v-for="(history, index) in item.version_history"
          :key="versionHistoryKey(history, index)"
        >
          {{ versionHistoryText(history) }}
        </span>
      </div>
    </section>
  </section>
  <section v-else class="view-stack">
    <h1>未找到知识项</h1>
  </section>
</template>
