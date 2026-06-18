<script setup lang="ts">
import { Download, RotateCcw, Search } from '@lucide/vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()

function exportFilter() {
  const payload = JSON.stringify({ filter: store.filter, result_count: store.filteredKnowledge.length }, null, 2)
  navigator.clipboard?.writeText(payload)
}
</script>

<template>
  <div class="filter-bar">
    <label class="search-box">
      <Search :size="17" />
      <input v-model="store.filter.query" placeholder="搜索知识 ID、标题、规则" />
    </label>
    <select v-model="store.filter.domain">
      <option value="all">domain</option>
      <option v-for="domain in store.domains" :key="domain" :value="domain">{{ domain }}</option>
    </select>
    <select v-model="store.filter.source_type">
      <option value="all">source</option>
      <option v-for="sourceType in store.sourceTypes" :key="sourceType" :value="sourceType">{{ sourceType }}</option>
    </select>
    <select v-model="store.filter.freshness">
      <option value="all">freshness</option>
      <option value="stable">stable</option>
      <option value="time_sensitive">time_sensitive</option>
      <option value="deprecated">deprecated</option>
    </select>
    <select v-model="store.filter.review_status">
      <option value="all">review</option>
      <option value="draft">draft</option>
      <option value="reviewed">reviewed</option>
      <option value="approved">approved</option>
      <option value="rejected">rejected</option>
      <option value="deprecated">deprecated</option>
    </select>
    <select v-model="store.filter.confidence">
      <option value="all">confidence</option>
      <option value="high">high</option>
      <option value="medium">medium</option>
      <option value="low">low</option>
    </select>
    <select v-model="store.filter.conflict_status">
      <option value="all">conflict</option>
      <option value="none">none</option>
      <option value="potential">potential</option>
      <option value="confirmed">confirmed</option>
      <option value="resolved">resolved</option>
    </select>
    <button class="icon-button" title="重置筛选" @click="store.resetFilter()"><RotateCcw :size="17" /></button>
    <button class="icon-button" title="复制筛选结果" @click="exportFilter"><Download :size="17" /></button>
  </div>
</template>
