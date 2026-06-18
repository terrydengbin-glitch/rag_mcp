<script setup lang="ts">
const statusLabels: Record<string, string> = {
  accepted_for_draft: '草稿已采纳',
  accepted_for_reviewed_caveat_only: '可入库-仅审计',
  approved: '已批准',
  blocked: '已阻断',
  candidate_only: '仅候选',
  candidate_ready: '待审计',
  convert_to_knowledge_item: '转正式知识',
  current: '当前',
  deny: '拒绝',
  draft: '草稿',
  draft_only: '仅草稿',
  fail: '失败',
  high: '高',
  hold: '挂起',
  human_review: '人工复核',
  low: '低',
  medium: '中',
  medium_high: '中高',
  mock_data: '模拟数据',
  needs_more_evidence: '需补证',
  needs_review: '需复核',
  none: '无冲突',
  partial: '部分覆盖',
  pass: '通过',
  pending: '待处理',
  pending_external_audit: '待外部审计',
  potential: '潜在冲突',
  read_only: '只读',
  ready_for_inline_contract_reaudit: '内联契约待再审',
  ready_for_reaudit: '待再审',
  rebuilt_archived: '已重建归档',
  rejected: '已拒绝',
  reviewed: '已审计',
  stable: '稳定',
  time_sensitive: '时效敏感',
}

const props = defineProps<{
  value: string
  tone?: 'status' | 'conflict' | 'freshness' | 'confidence'
}>()
</script>

<template>
  <span class="badge" :class="[`badge-${tone || 'status'}`, `is-${value}`]">
    {{ statusLabels[props.value] || props.value }}
  </span>
</template>
