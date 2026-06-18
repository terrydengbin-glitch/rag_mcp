<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import {
  AlertTriangle,
  ChevronDown,
  ChevronRight,
  Clipboard,
  Database,
  FileSearch,
  GitBranch,
  Search,
  ShieldCheck
} from '@lucide/vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useDebouncedRef } from '../composables/useDebouncedRef'
import { useAuditStore } from '../stores/auditStore'
import type { IngestionCandidate, KnowledgeCardSummary, KnowledgeItem, KnowledgeTreeNode } from '../types'

const store = useAuditStore()
const route = useRoute()
const router = useRouter()

const expandedNodeIds = ref<Set<string>>(new Set())
const selectedCardId = ref<string>('')
const scopeQuery = ref('')
const statusFilter = ref('all')
const conflictFilter = ref('all')
const freshnessFilter = ref('all')
const sortMode = ref('relevance')
const pageSize = ref(20)
const currentPage = ref(1)
const debouncedScopeQuery = useDebouncedRef(scopeQuery, 250)
const virtualListRef = ref<HTMLElement | null>(null)
const virtualScrollTop = ref(0)
const viewportWidth = ref(typeof window === 'undefined' ? 1440 : window.innerWidth)
const virtualRowHeight = 116
const virtualBufferRows = 2

onMounted(() => {
  void store.initializeKnowledgeTreeApi()
  window.addEventListener('resize', updateViewportWidth)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateViewportWidth)
})

function queryValue(value: unknown) {
  return Array.isArray(value) ? String(value[0] || '') : String(value || '')
}

const treeView = computed(() =>
  store.resolveTreeSelection({
    l1: queryValue(route.query.l1) || null,
    l2: queryValue(route.query.l2) || null,
    l3: queryValue(route.query.l3) || null,
    node_id: queryValue(route.query.node_id) || null
  })
)

const currentNode = computed(() => {
  const scope = treeView.value.current_scope
  return scope ? store.findTreeNode(scope.node_id) || null : null
})

const effectiveNode = computed(() => currentNode.value || store.findTreeNode('kt') || null)
const rootNodes = computed(() => treeView.value.level1_nodes)
const activeScopeQuery = computed(() => {
  const value = debouncedScopeQuery.value.trim()
  return value.length >= 2 ? value : ''
})
const searchTooShort = computed(() => {
  const value = scopeQuery.value.trim()
  return value.length > 0 && value.length < 2
})

const selectedChain = computed(() =>
  currentNode.value ? [...store.getTreeAncestors(currentNode.value.node_id), currentNode.value] : []
)

watch(
  () => selectedChain.value.map((item) => item.node_id).join('|'),
  () => {
    const next = new Set(expandedNodeIds.value)
    for (const item of selectedChain.value) {
      if (item.level <= 2) next.add(item.node_id)
    }
    expandedNodeIds.value = next
  },
  { immediate: true }
)

const scopeCandidates = computed(() => store.getCandidatesForScope(effectiveNode.value?.node_id || null))
const scopeKnowledgeItems = computed(() => store.getKnowledgeItemsForScope(effectiveNode.value?.node_id || null))
const scopeGaps = computed(() => {
  if (!effectiveNode.value) return []
  return [effectiveNode.value, ...store.getNodeDescendants(effectiveNode.value)].flatMap((node) =>
    node.open_gaps.map((gap) => ({ node, gap }))
  )
})

const currentSummary = computed(() => store.getTreeScopeSummary(effectiveNode.value?.node_id || null))
const treeSidebarSummary = computed(() => {
  const level1Count = store.knowledgeTreeNodes.filter((item) => item.level === 1).length
  const level2Count = store.knowledgeTreeNodes.filter((item) => item.level === 2).length
  const level3Count = store.knowledgeTreeNodes.filter((item) => item.level >= 3).length
  return `${level1Count} 主枝 / ${level2Count} 二级分区 / ${level3Count} 专题叶子`
})

function formalKnowledgeCount(nodeId: string) {
  const summary = store.getTreeScopeSummary(nodeId)
  return summary.approved_item_count + summary.reviewed_item_count
}

const formalizedCandidates = computed(() => scopeCandidates.value.filter((item) => item.workflow?.queue_group === 'formalized'))
const pendingCandidates = computed(() => scopeCandidates.value.filter((item) => item.workflow?.queue_group !== 'formalized'))

const pagedCards = computed(() => store.listKnowledgeCardsForScope({
  nodeId: effectiveNode.value?.node_id || null,
  kind: 'formal',
  query: activeScopeQuery.value,
  status: statusFilter.value,
  conflictStatus: conflictFilter.value,
  freshness: freshnessFilter.value,
  sort: sortMode.value,
  page: currentPage.value,
  pageSize: pageSize.value
}))

watch(
  () => [
    effectiveNode.value?.node_id || 'kt',
    activeScopeQuery.value,
    statusFilter.value,
    conflictFilter.value,
    freshnessFilter.value,
    sortMode.value,
    pageSize.value
  ],
  () => {
    currentPage.value = 1
  }
)

const totalPages = computed(() => Math.max(1, Math.ceil(pagedCards.value.total / pageSize.value)))
const visibleCards = computed(() => pagedCards.value.items)

const selectedCard = computed(() => {
  if (selectedCardId.value) {
    const selected = visibleCards.value.find((item) => item.id === selectedCardId.value)
    if (selected) return selected
  }
  return visibleCards.value[0] || null
})

watch(
  () => visibleCards.value.map((item) => item.id).join('|'),
  () => {
    if (!selectedCard.value && visibleCards.value[0]) selectedCardId.value = visibleCards.value[0].id
    if (selectedCardId.value && !visibleCards.value.some((item) => item.id === selectedCardId.value)) {
      selectedCardId.value = visibleCards.value[0]?.id || ''
    }
  },
  { immediate: true }
)

const selectedCardDetail = computed(() =>
  selectedCard.value ? store.getKnowledgeCardDetail(selectedCard.value.kind, selectedCard.value.id) : null
)
const selectedKnowledgeItem = computed(() =>
  selectedCardDetail.value?.kind === 'knowledge' ? selectedCardDetail.value.raw as KnowledgeItem : null
)
const selectedCandidate = computed(() =>
  selectedCardDetail.value?.kind === 'candidate' ? selectedCardDetail.value.raw as IngestionCandidate : null
)

const virtualColumnCount = computed(() => {
  if (viewportWidth.value <= 560) return 1
  if (viewportWidth.value <= 1100) return 2
  return 5
})
const virtualRows = computed(() => {
  const rows: KnowledgeCardSummary[][] = []
  for (let index = 0; index < visibleCards.value.length; index += virtualColumnCount.value) {
    rows.push(visibleCards.value.slice(index, index + virtualColumnCount.value))
  }
  return rows
})
const virtualViewportRows = computed(() => Math.max(1, Math.ceil(420 / virtualRowHeight)))
const virtualStartRow = computed(() => Math.max(0, Math.floor(virtualScrollTop.value / virtualRowHeight) - virtualBufferRows))
const virtualEndRow = computed(() =>
  Math.min(virtualRows.value.length, virtualStartRow.value + virtualViewportRows.value + virtualBufferRows * 2)
)
const virtualTopPadding = computed(() => virtualStartRow.value * virtualRowHeight)
const virtualBottomPadding = computed(() => Math.max(0, (virtualRows.value.length - virtualEndRow.value) * virtualRowHeight))
const virtualCards = computed(() => virtualRows.value.slice(virtualStartRow.value, virtualEndRow.value).flat())

watch(
  () => visibleCards.value.map((item) => item.id).join('|'),
  () => {
    virtualScrollTop.value = 0
    if (virtualListRef.value) virtualListRef.value.scrollTop = 0
  }
)

function updateViewportWidth() {
  viewportWidth.value = window.innerWidth
}

function handleVirtualScroll() {
  virtualScrollTop.value = virtualListRef.value?.scrollTop || 0
}

function isExpanded(nodeId: string) {
  return expandedNodeIds.value.has(nodeId)
}

function toggleExpanded(nodeId: string) {
  const next = new Set(expandedNodeIds.value)
  if (next.has(nodeId)) next.delete(nodeId)
  else next.add(nodeId)
  expandedNodeIds.value = next
}

function selectNode(node: KnowledgeTreeNode) {
  const resolved = store.resolveTreeSelection({ node_id: node.node_id })
  const query: Record<string, string> = {}
  if (resolved.selected_level1_id) query.l1 = resolved.selected_level1_id
  if (resolved.selected_level2_id) query.l2 = resolved.selected_level2_id
  if (resolved.selected_level3_id) query.l3 = resolved.selected_level3_id
  const nextExpanded = new Set<string>()
  if (resolved.selected_level1_id) nextExpanded.add(resolved.selected_level1_id)
  if (resolved.selected_level2_id) nextExpanded.add(resolved.selected_level2_id)
  expandedNodeIds.value = nextExpanded
  router.push({ path: '/knowledge-tree', query })
}

function clearSelection() {
  router.push({ path: '/knowledge-tree' })
}

function selectCard(card: KnowledgeCardSummary) {
  selectedCardId.value = card.id
}

function setPage(page: number) {
  currentPage.value = Math.min(Math.max(page, 1), totalPages.value)
}

async function copyCanonicalNodeId() {
  const nodeId = effectiveNode.value?.node_id || 'kt'
  await navigator.clipboard?.writeText(nodeId)
}

function level2Nodes(rootId: string) {
  return store.getLevel2Nodes(rootId)
}

function level3Nodes(level2Id: string) {
  return store.getLevel3Nodes(level2Id)
}
</script>

<template>
  <section class="view-stack knowledge-tree-reader-view">
    <div class="tree-reader-filterbar panel">
      <label class="search-box tree-reader-search" aria-label="搜索知识树">
        <Search :size="17" />
        <input v-model="scopeQuery" type="search" placeholder="搜索当前范围知识点，例如回测、成交、MCP、回灌" />
      </label>
      <span v-if="searchTooShort" class="filter-hint">请输入至少 2 个字符后搜索</span>
      <select v-model="statusFilter" aria-label="覆盖状态">
        <option value="all">全部覆盖状态</option>
        <option value="approved">已批准</option>
        <option value="reviewed">已复审</option>
        <option value="draft">草稿</option>
      </select>
      <select v-model="conflictFilter" aria-label="冲突状态">
        <option value="all">全部冲突状态</option>
        <option value="none">无冲突</option>
        <option value="potential">潜在冲突</option>
        <option value="confirmed">已确认冲突</option>
        <option value="unchecked">未检查</option>
      </select>
      <select v-model="freshnessFilter" aria-label="时效状态">
        <option value="all">全部时效</option>
        <option value="stable">稳定</option>
        <option value="time_sensitive">时效敏感</option>
        <option value="stale">已过期</option>
      </select>
    </div>

    <div class="tree-api-status panel" :class="`is-${store.knowledgeTreeApi.state}`">
      <span>
        <strong>{{ store.knowledgeTreeApi.state === 'healthy' ? '知识树 API 正常' : '静态数据兜底' }}</strong>
        <small>{{ store.knowledgeTreeApi.message }} / {{ store.knowledgeTreeApi.baseUrl }}</small>
      </span>
      <StatusBadge :value="store.knowledgeTreeApi.readOnly ? 'read_only' : 'not_read_only'" />
    </div>

    <div class="data-load-banner panel" :class="`is-${store.dataState.state}`">
      <strong>{{ store.dataState.state === 'ready' ? '知识树数据已加载' : store.dataState.state === 'error' ? '知识树数据加载异常' : '正在加载知识树数据' }}</strong>
      <span>{{ store.dataState.message }}</span>
    </div>

    <div class="knowledge-tree-reading-shell">
      <aside class="panel tree-reader-sidebar" aria-label="知识树目录">
        <div class="tree-sidebar-header">
          <div>
            <h1>知识树</h1>
            <p>{{ treeSidebarSummary }}</p>
          </div>
          <StatusBadge value="read_only" />
        </div>

        <div class="tree-reader-list">
          <div v-for="root in rootNodes" :key="root.node_id" class="tree-nav-group">
            <button
              type="button"
              class="tree-nav-row level-one"
              :class="{ 'is-active': treeView.selected_level1_id === root.node_id }"
              @click="selectNode(root)"
              @dblclick="toggleExpanded(root.node_id)"
            >
              <span class="tree-row-main">
                <small>L1 主枝</small>
                <strong>{{ root.title }}</strong>
                <em>{{ root.summary }}</em>
              </span>
              <span class="tree-row-side">
                <span class="tree-toggle-button" role="button" tabindex="0" @click.stop="toggleExpanded(root.node_id)">
                  <ChevronDown v-if="isExpanded(root.node_id)" :size="14" />
                  <ChevronRight v-else :size="14" />
                </span>
                <b>{{ level2Nodes(root.node_id).length }}</b>
              </span>
            </button>

            <div v-if="isExpanded(root.node_id)" class="tree-nav-children">
              <div v-for="level2 in level2Nodes(root.node_id)" :key="level2.node_id">
                <button
                  type="button"
                  class="tree-nav-row level-two"
                  :class="{ 'is-active': treeView.selected_level2_id === level2.node_id }"
                  @click="selectNode(level2)"
                  @dblclick="toggleExpanded(level2.node_id)"
                >
                  <span class="tree-row-main">
                    <small>L2 分区</small>
                    <strong>{{ level2.title }}</strong>
                    <em>{{ level2.summary }}</em>
                  </span>
                  <span class="tree-row-side">
                    <span class="tree-toggle-button" role="button" tabindex="0" @click.stop="toggleExpanded(level2.node_id)">
                      <ChevronDown v-if="isExpanded(level2.node_id)" :size="14" />
                      <ChevronRight v-else :size="14" />
                    </span>
                    <b>{{ formalKnowledgeCount(level2.node_id) }}</b>
                  </span>
                </button>

                <div v-if="isExpanded(level2.node_id)" class="tree-nav-children level-three-wrap">
                  <button
                    v-for="level3 in level3Nodes(level2.node_id)"
                    :key="level3.node_id"
                    type="button"
                    class="tree-nav-row level-three"
                    :class="{ 'is-active': treeView.selected_level3_id === level3.node_id }"
                    @click="selectNode(level3)"
                  >
                    <span class="tree-row-main">
                      <small>L3 专题</small>
                      <strong>{{ level3.title }}</strong>
                      <em>{{ level3.summary }}</em>
                    </span>
                    <span class="tree-row-side">
                      <b>{{ formalKnowledgeCount(level3.node_id) }}</b>
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <main class="tree-reader-main">
        <section class="panel tree-scope-hero">
          <div>
            <p class="tree-breadcrumb-line">
              <button type="button" class="inline-breadcrumb" @click="clearSelection">CEK-TA</button>
              <template v-for="node in selectedChain" :key="node.node_id">
                <ChevronRight :size="14" />
                <button type="button" class="inline-breadcrumb" @click="selectNode(node)">
                  {{ node.title }}
                </button>
              </template>
            </p>
            <h2>{{ effectiveNode?.title || 'CEK-TA Knowledge Tree' }}</h2>
            <p>{{ effectiveNode?.summary || '选择目录后查看节点范围内的知识点、候选、缺口和边界。' }}</p>
          </div>
          <div class="badge-row">
            <StatusBadge :value="effectiveNode?.coverage_status || 'partial'" />
            <StatusBadge :value="effectiveNode?.review_status || 'reviewed'" />
            <StatusBadge :value="effectiveNode?.conflict_status || 'none'" tone="conflict" />
          </div>
        </section>

        <section class="panel knowledge-point-section">
          <div class="panel-title-row">
            <div>
              <h2>当前范围的知识点</h2>
              <p class="muted-line">
                显示 {{ visibleCards.length ? (pagedCards.page - 1) * pageSize + 1 : 0 }}-{{ (pagedCards.page - 1) * pageSize + visibleCards.length }} /
                {{ pagedCards.total }} 个正式知识点
              </p>
            </div>
            <div class="tree-list-controls">
              <span>只展示正式知识；候选和缺口在下方单独审计；详情点击后加载</span>
              <select v-model="sortMode" aria-label="排序">
                <option value="relevance">相关度</option>
                <option value="source_count_desc">来源数</option>
                <option value="status">状态</option>
                <option value="updated_desc">更新时间</option>
              </select>
              <select v-model.number="pageSize" aria-label="每页数量">
                <option :value="20">20 / 页</option>
                <option :value="50">50 / 页</option>
                <option :value="100">100 / 页</option>
              </select>
            </div>
          </div>

          <div
            v-if="visibleCards.length"
            ref="virtualListRef"
            class="knowledge-card-virtual-list"
            data-testid="knowledge-card-virtual-list"
            @scroll="handleVirtualScroll"
          >
            <div :style="{ height: `${virtualTopPadding}px` }"></div>
            <div class="knowledge-card-grid is-virtualized">
              <button
                v-for="card in virtualCards"
                :key="card.id"
                type="button"
                class="knowledge-point-card"
                :class="{ 'is-selected-row': selectedCard?.id === card.id }"
                @click="selectCard(card)"
              >
                <strong>{{ card.title }}</strong>
                <small>{{ card.subtitle }}</small>
                <span>{{ card.source_count }} 个来源 / {{ card.default_guidance }}</span>
                <StatusBadge :value="card.status" />
              </button>
            </div>
            <div :style="{ height: `${virtualBottomPadding}px` }"></div>
          </div>
          <div v-else class="empty-state">
            <strong>当前过滤条件下没有知识点</strong>
            <span>请放宽状态、冲突或时效过滤。</span>
          </div>

          <div class="pagination-row">
            <span>当前页 {{ visibleCards.length }} 条，当前窗口渲染 {{ virtualCards.length }} 张摘要卡。</span>
            <div>
              <button type="button" class="text-button" :disabled="currentPage <= 1" @click="setPage(currentPage - 1)">上一页</button>
              <button
                v-for="page in Math.min(totalPages, 3)"
                :key="page"
                type="button"
                class="text-button"
                :class="{ 'is-current-scope': currentPage === page }"
                @click="setPage(page)"
              >
                {{ page }}
              </button>
              <button type="button" class="text-button" :disabled="currentPage >= totalPages" @click="setPage(currentPage + 1)">下一页</button>
            </div>
          </div>
        </section>

        <section class="panel knowledge-point-detail">
          <div class="panel-title-row">
            <div>
              <h2>知识点内容</h2>
              <p class="muted-line">详情优先展示，Open Gaps 和使用边界放在下方。</p>
            </div>
            <StatusBadge v-if="selectedCard" :value="selectedCard.status" />
          </div>

          <article v-if="selectedCard" class="knowledge-detail-card">
            <h3>{{ selectedCard.title }}</h3>
            <p>{{ selectedCard.summary }}</p>
            <dl class="meta-grid compact-meta-grid">
              <dt>claim_type</dt>
              <dd v-if="selectedKnowledgeItem">{{ selectedKnowledgeItem.claim_type || 'methodological_constraint' }}</dd>
              <dd v-else>not_formal_knowledge</dd>
              <dt>默认指导</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ selectedKnowledgeItem.machine_gate?.default_guidance || 'deny' }} /
                {{ selectedKnowledgeItem.machine_gate?.reason || 'No machine gate reason.' }}
              </dd>
              <dd v-else>deny</dd>
              <dt>tree_node_id</dt>
              <dd>{{ selectedCard.tree_node_id }}</dd>
              <dt>适用范围</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ selectedKnowledgeItem.applies_to.project_type }},
                {{ selectedKnowledgeItem.applies_to.data_granularity }}
              </dd>
              <dd v-else-if="selectedCandidate">{{ selectedCandidate.applicable_scope }}</dd>
              <dd v-else>需要补充来源、适用范围和冲突检查后才能入库。</dd>
              <dt>不适用</dt>
              <dd v-if="selectedKnowledgeItem">{{ selectedKnowledgeItem.not_applicable_when.join(' / ') }}</dd>
              <dd v-else-if="selectedCandidate">
                {{ selectedCandidate.not_applicable_scope.join(' / ') }}
              </dd>
              <dd v-else>不可作为默认专业指导。</dd>
              <dt>来源</dt>
              <dd>{{ selectedCard.source_count }} sources</dd>
              <dt>AI 可用</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ (selectedKnowledgeItem.llm_usage_policy?.allowed || []).slice(0, 2).join(' / ') }}
              </dd>
              <dd v-else>需要先进入正式知识审计。</dd>
              <dt>AI 禁止</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ (selectedKnowledgeItem.llm_usage_policy?.not_allowed || []).slice(0, 2).join(' / ') }}
              </dd>
              <dd v-else>不可作为默认指导。</dd>
              <dt>必需上下文</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ (selectedKnowledgeItem.llm_usage_policy?.required_context || []).join(' / ') }}
              </dd>
              <dd v-else>n/a</dd>
              <dt>分类说明</dt>
              <dd v-if="selectedKnowledgeItem">{{ selectedKnowledgeItem.classification_notes }}</dd>
              <dd v-else>n/a</dd>
              <dt>补充来源</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ selectedKnowledgeItem.recommended_extra_sources_count || 0 }} proposed
              </dd>
              <dd v-else>n/a</dd>
              <dt>冲突处理</dt>
              <dd v-if="selectedKnowledgeItem">
                {{ selectedKnowledgeItem.resolution || 'No known direct conflict.' }}
              </dd>
              <dd v-else-if="selectedCandidate">
                {{ selectedCandidate.conflict_audit?.resolution_summary || 'Candidate still needs review.' }}
              </dd>
              <dd v-else>缺口需要进入采集和人工审核。</dd>
            </dl>
          </article>
          <div v-else class="empty-state">
            <strong>暂无可展示知识点</strong>
            <span>该范围仍需要采集和审计。</span>
          </div>
        </section>

        <section class="tree-lower-panels">
          <div class="panel">
            <h2>范围内候选</h2>
            <div v-if="formalizedCandidates.length || pendingCandidates.length" class="compact-list">
              <span>
                <span>
                  <strong>已沉淀候选</strong>
                  <small>已回链到正式 reviewed 知识，不再进入待补证队列</small>
                </span>
                <StatusBadge :value="`${formalizedCandidates.length}`" />
              </span>
              <span>
                <span>
                  <strong>待处理候选</strong>
                  <small>仍需补证、审计或转换，不作为当前正式知识点展示</small>
                </span>
                <StatusBadge :value="`${pendingCandidates.length}`" />
              </span>
            </div>
            <div v-else class="empty-state">
              <strong>暂无候选</strong>
              <span>该范围当前没有候选审计项。</span>
            </div>
          </div>

          <div class="panel">
            <h2>待补缺口</h2>
            <div v-if="scopeGaps.length" class="compact-list">
              <span v-for="item in scopeGaps.slice(0, 6)" :key="`${item.node.node_id}-${item.gap}`">
                <span>
                  <strong>{{ item.gap }}</strong>
                  <small>{{ item.node.title }}</small>
                </span>
                <StatusBadge value="gap" />
              </span>
            </div>
            <div v-else class="empty-state">
              <strong>暂无显式缺口</strong>
              <span>仍需通过来源和冲突审计确认质量。</span>
            </div>
          </div>

          <div class="panel">
            <h2>使用边界</h2>
            <div class="compact-list">
              <span>
                <span>
                  <strong>MCP</strong>
                  <small>只读检索，不写知识、不审批、不交易</small>
                </span>
                <StatusBadge value="read_only" />
              </span>
              <span>
                <span>
                  <strong>回灌</strong>
                  <small>其他项目只能进入 contributions/proposed</small>
                </span>
                <StatusBadge value="proposed" />
              </span>
            </div>
          </div>
        </section>
      </main>

      <aside class="panel tree-audit-rail" aria-label="审计摘要">
        <div class="rail-header">
          <h2>审计摘要</h2>
          <p>{{ effectiveNode?.node_id || 'kt' }}</p>
        </div>
        <div class="audit-stat-grid">
          <span>
            <small>正式知识</small>
            <strong>{{ currentSummary.approved_item_count + currentSummary.reviewed_item_count }}</strong>
          </span>
          <span>
            <small>候选知识</small>
            <strong>{{ currentSummary.candidate_count }}</strong>
          </span>
          <span>
            <small>来源</small>
            <strong>{{ currentSummary.source_count }}</strong>
          </span>
          <span>
            <small>缺口</small>
            <strong>{{ currentSummary.open_gap_count }}</strong>
          </span>
          <span>
            <small>冲突</small>
            <strong>{{ currentSummary.conflict_count }}</strong>
          </span>
          <span>
            <small>时效</small>
            <strong>{{ store.treeSummary.stale }}</strong>
          </span>
        </div>

        <h3>下一步动作</h3>
        <div class="rail-action-list">
          <RouterLink class="text-button" :to="{ path: '/ingestion', query: { tree_node_id: effectiveNode?.node_id || 'kt' } }">
            <FileSearch :size="15" />
            查看候选
          </RouterLink>
          <RouterLink
            class="text-button"
            :to="{ path: '/search-lab', query: { canonical_node_id: effectiveNode?.node_id || 'kt' } }"
          >
            <Database :size="15" />
            带入 SearchLab
          </RouterLink>
          <button type="button" class="text-button" @click="copyCanonicalNodeId">
            <Clipboard :size="15" />
            复制 canonical_node_id
          </button>
        </div>

        <h3>人工审核提醒</h3>
        <div class="rail-hint-list">
          <span>
            <strong>draft/candidate 不可作为默认指导</strong>
            <small>必须经过来源、冲突、适用边界审计</small>
          </span>
          <span>
            <strong>外部项目回灌不可直写</strong>
            <small>必须 proposed -> reviewed -> accepted</small>
          </span>
          <span>
            <strong>无来源/冲突/过期知识要阻断</strong>
            <small>MCP 与 Vue3 都要保持一致提示</small>
          </span>
        </div>
      </aside>
    </div>
  </section>
</template>
