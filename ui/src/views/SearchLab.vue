<script setup lang="ts">
import { SearchCheck, TestTube2 } from '@lucide/vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useAuditStore } from '../stores/auditStore'

const store = useAuditStore()
</script>

<template>
  <section class="view-stack">
    <header class="view-header">
      <div>
        <h1>检索测试台</h1>
        <p>{{ store.searchTestCases.length }} 个运行时测试用例 / Phase 20 MCP 契约</p>
      </div>
      <StatusBadge value="mcp_runtime_fixture" />
    </header>

    <div class="data-load-banner panel" :class="`is-${store.dataState.state}`">
      <strong>{{ store.dataState.state === 'ready' ? '知识数据已加载' : store.dataState.state === 'error' ? '知识数据加载异常' : '正在加载知识数据' }}</strong>
      <span>{{ store.dataState.message }}</span>
    </div>

    <div class="two-column">
      <section v-for="test in store.searchTestCases" :key="test.test_id" class="panel search-lab-panel">
        <div class="panel-title-row">
          <div>
            <h2>{{ test.test_id }}</h2>
            <p class="muted-line">{{ test.request_id || '-' }} / {{ test.task_type }}</p>
          </div>
          <StatusBadge :value="test.runtime_status || test.status" />
        </div>
        <div class="query-box">
          <SearchCheck :size="18" />
          <strong>{{ test.query }}</strong>
        </div>
        <dl class="meta-grid">
          <dt>树节点</dt>
          <dd>{{ test.filters.tree_node_id || '-' }}</dd>
          <dt>规范节点</dt>
          <dd>{{ test.filters.canonical_node_id || '-' }}</dd>
          <dt>领域</dt>
          <dd>{{ test.filters.domain || '-' }}</dd>
          <dt>阻断数</dt>
          <dd>{{ test.audit?.blocked_count ?? test.blocked_results?.length ?? 0 }}</dd>
        </dl>
        <div v-if="test.warnings.length" class="warning-list">
          <strong>告警</strong>
          <ul>
            <li v-for="warning in test.warnings" :key="warning">{{ warning }}</li>
          </ul>
        </div>
        <div class="match-list">
          <h3>命中结果</h3>
          <div v-for="match in test.matches" :key="match.item_id" class="match-row">
            <TestTube2 :size="17" />
            <div>
              <strong>{{ match.title }}</strong>
              <small>{{ match.item_id }}</small>
              <small>{{ match.tree_path }}</small>
              <small>{{ match.canonical_tree_path || match.canonical_node_id || '-' }}</small>
              <small>得分 {{ match.why_matched?.score ?? match.score }} / 来源 {{ match.source_count }}</small>
              <small>{{ match.machine_gate?.default_guidance || 'deny' }} / {{ match.machine_gate?.reason || '-' }}</small>
              <small v-if="match.llm_usage_policy?.required_context.length">
                必需上下文 {{ match.llm_usage_policy.required_context.join(', ') }}
              </small>
              <small v-if="match.why_matched?.reasons.length">{{ match.why_matched.reasons.join(', ') }}</small>
            </div>
            <div class="badge-row">
              <StatusBadge :value="match.review_status" />
              <StatusBadge :value="match.conflict_status" tone="conflict" />
              <StatusBadge :value="match.machine_gate?.default_guidance || 'deny'" />
              <StatusBadge :value="match.recommended_next_action" />
            </div>
          </div>
        </div>
        <div v-if="test.blocked_results?.length" class="match-list blocked-list">
          <h3>阻断结果</h3>
          <div v-for="blocked in test.blocked_results" :key="blocked.knowledge_id" class="match-row">
            <TestTube2 :size="17" />
            <div>
              <strong>{{ blocked.title }}</strong>
              <small>{{ blocked.knowledge_id }}</small>
              <small>{{ blocked.blocked_reason }} / {{ blocked.recommended_fix }}</small>
              <small>{{ blocked.machine_gate?.default_guidance || 'deny' }} / {{ blocked.machine_gate?.blocking_reasons.join(', ') }}</small>
              <small>来源引用 {{ blocked.has_source_refs ? '存在' : '缺失' }}</small>
            </div>
            <div class="badge-row">
              <StatusBadge :value="blocked.review_status" />
              <StatusBadge :value="blocked.conflict_status" tone="conflict" />
              <StatusBadge :value="blocked.freshness" />
            </div>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>
