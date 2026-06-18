import { computed, reactive, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  KnowledgeDataClientError,
  loadCandidateFixture,
  loadFormalKnowledgeFixture,
  loadKnowledgeTreeScopeIndex,
  loadKnowledgeTreeFixture
} from '../services/knowledgeDataClient'
import { checkKnowledgeTreeApiHealth, getKnowledgeTreeApiBaseUrl } from '../services/knowledgeTreeApi'
import {
  conflicts,
  contributions,
  ingestionCandidates as mockIngestionCandidates,
  knowledgeItems as mockKnowledgeItems,
  knowledgeTreeNodes as mockKnowledgeTreeNodes,
  projectAdapters,
  sources,
  tasks
} from '../data/mockData'
import { runtimeSearchCases } from '../data/runtimeSearchData'
import type {
  AuditFilter,
  CandidateCoverageSummary,
  IngestionCandidate,
  KnowledgeCardDetail,
  KnowledgeCardSummary,
  KnowledgeItem,
  KnowledgeTreeScopeIndex,
  KnowledgeTreeNode,
  KnowledgeTreeScope,
  KnowledgeTreeScopeSummary,
  KnowledgeTreeThreeLevelViewModel,
  PagedResult
} from '../types'
import type { KnowledgeTreeApiHealth } from '../services/knowledgeTreeApi'

const initialFilter: AuditFilter = {
  query: '',
  domain: 'all',
  source_type: 'all',
  freshness: 'all',
  review_status: 'all',
  confidence: 'all',
  conflict_status: 'all'
}

const legacyTreeNodeAliases: Record<string, string> = {
  'kt.trading_engineering.quant_foundation': 'kt.quant_foundation',
  'kt.trading_engineering.strategy_engineering': 'kt.kline_strategy',
  'kt.trading_engineering.strategy_engineering.signal_boundary': 'kt.kline_strategy.indicators',
  'kt.trading_engineering.backtest': 'kt.backtest',
  'kt.trading_engineering.backtest.bias': 'kt.backtest.bias',
  'kt.trading_engineering.backtest.fill_assumption': 'kt.backtest.bias',
  'kt.trading_engineering.replay_simulation': 'kt.replay_simulation',
  'kt.trading_engineering.replay_simulation.fill_model': 'kt.replay_simulation.fill_model',
  'kt.trading_engineering.replay_simulation.execution_semantics': 'kt.replay_simulation.fill_model',
  'kt.trading_engineering.live_execution': 'kt.live_execution',
  'kt.trading_engineering.live_execution.order_state_machine': 'kt.live_execution',
  'kt.trading_engineering.risk_management': 'kt.risk_management',
  'kt.trading_engineering.risk_management.kill_switch': 'kt.risk_management.pre_trade_gates',
  'kt.trading_engineering.risk_management.risk_gate': 'kt.risk_management.pre_trade_gates',
  'kt.trading_engineering.risk_management.position_sizing': 'kt.quant_foundation.position_sizing',
  'kt.trading_engineering.risk_management.crypto_perpetual_risk': 'kt.risk_management.crypto_perpetual_risk',
  'kt.trading_engineering.market_microstructure.crypto_perpetual': 'kt.market_microstructure.crypto_perpetual',
  'kt.trading_engineering.trade_analysis': 'kt.trade_analysis',
  'kt.risk_management.layered_risk_controls': 'kt.risk_management.layered_controls',
  'kt.live_execution.execution_tca': 'kt.trading_engineering.execution_tca',
  'kt.live_execution.audit_trail': 'kt.trading_engineering.trade_audit',
  'kt.live_execution.resilience_incident': 'kt.trading_engineering.resilience_incident_log',
  'kt.live_execution.resilience_incident_log': 'kt.trading_engineering.resilience_incident_log',
  'kt.live_execution.order_semantics': 'kt.trading_engineering.order_semantics',
  'kt.project_support': 'kt.project_integration',
  'kt.knowledge_governance': 'kt.ai_governance_audit',
  'kt.knowledge_governance.status_lifecycle': 'kt.ai_governance_audit',
  'kt.llm_training': 'kt.ai_engineering.llm_training',
  'kt.llm_training.model_training_engineering': 'kt.ai_engineering.llm_training.model_training_engineering',
  'kt.llm_training.trading_scoring_gating_training': 'kt.ai_engineering.llm_training.trading_scoring_gating_training',
  'kt.llm_training.training_dataset_schema_engineering': 'kt.ai_engineering.llm_training.training_dataset_schema_engineering',
  'kt.llm_training.trading_llm_task_taxonomy': 'kt.ai_engineering.llm_training.trading_llm_task_taxonomy',
  'kt.llm_training.training_method_selection': 'kt.ai_engineering.llm_training.training_method_selection',
  'kt.rag_engineering': 'kt.ai_engineering.rag_engineering',
  'kt.rag_engineering.source_quality': 'kt.ai_engineering.rag_engineering.machine_gate_filtering',
  'kt.rag_engineering.machine_gate_filtering': 'kt.ai_engineering.rag_engineering.machine_gate_filtering',
  'kt.rag_engineering.retrieval_policy': 'kt.ai_engineering.rag_engineering.retrieval_policy',
  'kt.rag_engineering.trading_scoring_rag_pack': 'kt.ai_engineering.rag_engineering.trading_scoring_rag_pack',
  'kt.mcp': 'kt.ai_engineering.mcp_engineering',
  'kt.mcp.knowledge_tools': 'kt.ai_engineering.mcp_engineering.tool_contract',
  'kt.mcp.tool_permission_enforcement': 'kt.ai_engineering.mcp_engineering.tool_permission_enforcement',
  'kt.ai_engineering.decision_time_feature_contract': 'kt.ai_engineering.decision_time_features',
  'kt.ai_engineering.decision_time_feature_contract.feature_store': 'kt.ai_engineering.decision_time_features.feature_store',
  'kt.ai_engineering.shadow_paper_ope_eval': 'kt.ai_engineering.shadow_paper_ope',
  'kt.ai_engineering.external_project_memory': 'kt.ai_engineering.project_memory',
  'kt.ai_engineering.external_project_memory.memory_boundary': 'kt.ai_engineering.project_memory.memory_boundary',
  'kt.ai_engineering.external_project_memory.memory_mcp_api_contract': 'kt.ai_engineering.project_memory.memory_mcp_api_contract',
  'kt.ai_engineering.external_project_memory.memory_schema_lifecycle': 'kt.ai_engineering.project_memory.memory_schema_lifecycle',
  'kt.ai_engineering.external_project_memory.memory_event_log': 'kt.ai_engineering.project_memory.memory_event_log',
  'kt.ai_engineering.external_project_memory.memory_write_gate': 'kt.ai_engineering.project_memory.memory_write_gate',
  'kt.ai_engineering.external_project_memory.memory_retrieval_context': 'kt.ai_engineering.project_memory.memory_retrieval_context',
  'kt.ai_engineering.external_project_memory.memory_security_governance': 'kt.ai_engineering.project_memory.memory_security_governance',
  'kt.ai_engineering.external_project_memory.memory_retention_privacy': 'kt.ai_engineering.project_memory.memory_retention_privacy',
  'kt.ai_engineering.external_project_memory.memory_adapter_selection': 'kt.ai_engineering.project_memory.memory_adapter_selection',
  'kt.ai_engineering.external_project_memory.memory_evaluation_regression': 'kt.ai_engineering.project_memory.memory_evaluation_regression',
  'kt.ai_feedback_governance': 'kt.ai_engineering.continuous_learning',
  'kt.ai_feedback_governance.feedback_logging': 'kt.ai_engineering.continuous_learning.feedback_logging',
  'kt.ai_feedback_governance.label_refresh': 'kt.ai_engineering.continuous_learning.label_refresh',
  'kt.ai_feedback_governance.drift_monitoring': 'kt.ai_engineering.continuous_learning.drift_monitoring',
  'kt.ai_feedback_governance.retraining_trigger': 'kt.ai_engineering.continuous_learning.retraining_trigger',
  'kt.ai_feedback_governance.recalibration_loop': 'kt.ai_engineering.continuous_learning.recalibration_loop',
  'kt.ai_feedback_governance.champion_challenger': 'kt.ai_engineering.continuous_learning.champion_challenger',
  'kt.ai_feedback_governance.shadow_paper_canary': 'kt.ai_engineering.continuous_learning.shadow_paper_canary',
  'kt.ai_feedback_governance.rollback_governance': 'kt.ai_engineering.continuous_learning.rollback_governance',
  'kt.ai_feedback_governance.llm_prompt_rag_sft_loop': 'kt.ai_engineering.continuous_learning.llm_prompt_rag_sft_loop',
  'kt.ai_feedback_governance.feedback_loop_risk': 'kt.ai_engineering.continuous_learning.feedback_loop_risk'
}

export const useAuditStore = defineStore('audit', () => {
  const filter = reactive<AuditFilter>({ ...initialFilter })
  const ingestionCandidates = reactive<IngestionCandidate[]>([])
  const knowledgeItems = reactive<KnowledgeItem[]>([])
  const knowledgeTreeNodes = reactive<KnowledgeTreeNode[]>([])
  const knowledgeTreeScopeIndex = ref<KnowledgeTreeScopeIndex | null>(null)
  const phase23CandidateFixtureGeneratedAt = ref('')
  const dataState = reactive({
    state: 'idle' as 'idle' | 'loading' | 'ready' | 'error',
    message: '静态知识数据尚未加载',
    loadedAt: '',
    fixtureGeneratedAt: ''
  })
  let fixtureLoadPromise: Promise<void> | null = null
  const knowledgeTreeApi = reactive<KnowledgeTreeApiHealth>({
    state: 'unchecked',
    baseUrl: getKnowledgeTreeApiBaseUrl(),
    readOnly: true,
    message: 'API healthcheck has not run',
    checkedAt: null
  })

  function replaceArray<T>(target: T[], items: T[]) {
    target.splice(0, target.length, ...items)
  }

  async function initializeFixtureData() {
    if (fixtureLoadPromise) return fixtureLoadPromise
    fixtureLoadPromise = (async () => {
      dataState.state = 'loading'
      dataState.message = '正在加载知识库静态数据'
      try {
        const [candidateFixture, knowledgeFixture, treeFixture, scopeIndex] = await Promise.all([
          loadCandidateFixture(),
          loadFormalKnowledgeFixture(),
          loadKnowledgeTreeFixture(),
          loadKnowledgeTreeScopeIndex()
        ])
        replaceArray(ingestionCandidates, candidateFixture.items)
        replaceArray(knowledgeItems, knowledgeFixture.items)
        replaceArray(knowledgeTreeNodes, treeFixture.items)
        knowledgeTreeScopeIndex.value = scopeIndex
        phase23CandidateFixtureGeneratedAt.value = candidateFixture.generated_at
        dataState.state = 'ready'
        dataState.loadedAt = new Date().toISOString()
        dataState.fixtureGeneratedAt = candidateFixture.generated_at
        dataState.message = `已加载 ${candidateFixture.count} 条候选、${knowledgeFixture.count} 条正式知识、${treeFixture.count} 个知识树节点、${scopeIndex.count} 个范围索引`
      } catch (error) {
        replaceArray(ingestionCandidates, mockIngestionCandidates)
        replaceArray(knowledgeItems, mockKnowledgeItems)
        replaceArray(knowledgeTreeNodes, mockKnowledgeTreeNodes)
        knowledgeTreeScopeIndex.value = null
        phase23CandidateFixtureGeneratedAt.value = 'mock fallback'
        dataState.state = 'error'
        dataState.loadedAt = new Date().toISOString()
        dataState.fixtureGeneratedAt = 'mock fallback'
        dataState.message = error instanceof KnowledgeDataClientError
          ? `${error.message}，已切换到内置备用数据`
          : '静态知识数据加载失败，已切换到内置备用数据'
      }
    })()
    return fixtureLoadPromise
  }

  void initializeFixtureData()

  const filteredKnowledge = computed(() => {
    const q = filter.query.trim().toLowerCase()
    return knowledgeItems.filter((item) => {
      const text = `${item.title} ${item.knowledge_id} ${item.statement} ${item.domain} ${item.subdomain}`.toLowerCase()
      return (
        (!q || text.includes(q)) &&
        (filter.domain === 'all' || item.domain === filter.domain) &&
        (filter.source_type === 'all' || item.source_type === filter.source_type) &&
        (filter.freshness === 'all' || item.freshness === filter.freshness) &&
        (filter.review_status === 'all' || item.review_status === filter.review_status) &&
        (filter.confidence === 'all' || item.confidence === filter.confidence) &&
        (filter.conflict_status === 'all' || item.conflict_status === filter.conflict_status)
      )
    })
  })

  const summary = computed(() => {
    const total = knowledgeItems.length
    const approved = knowledgeItems.filter((item) => item.review_status === 'approved').length
    const conflictsOpen = conflicts.filter((item) => item.review_decision !== 'resolved').length
    const stale = sources.filter((item) => item.stale).length
    const timeSensitive = knowledgeItems.filter((item) => item.freshness === 'time_sensitive').length
    return { total, approved, conflictsOpen, stale, timeSensitive }
  })

  const domains = computed(() => Array.from(new Set(knowledgeItems.map((item) => item.domain))).sort())
  const sourceTypes = computed(() => Array.from(new Set(sources.map((item) => item.source_type))).sort())
  const knowledgeById = computed(() => new Map(knowledgeItems.map((item) => [item.knowledge_id, item])))
  const candidateById = computed(() => new Map(ingestionCandidates.map((item) => [item.candidate_id, item])))
  const treeSummary = computed(() => {
    const total = knowledgeTreeNodes.length
    const empty = knowledgeTreeNodes.filter((item) => item.coverage_status === 'empty').length
    const partial = knowledgeTreeNodes.filter((item) => item.coverage_status === 'partial').length
    const conflicted = knowledgeTreeNodes.filter((item) => item.conflict_status === 'potential' || item.conflict_status === 'confirmed').length
    const stale = knowledgeTreeNodes.filter((item) => item.freshness_status === 'stale' || item.freshness_status === 'time_sensitive').length
    const candidateTotal = ingestionCandidates.length
    const candidateBlocked = ingestionCandidates.filter((item) => item.candidate_status === 'blocked').length
    const candidateReady = ingestionCandidates.filter((item) => item.candidate_status === 'candidate_ready').length
    return { total, empty, partial, conflicted, stale, candidateTotal, candidateBlocked, candidateReady }
  })

  function findTreeNode(nodeId: string) {
    return knowledgeTreeNodes.find((item) => item.node_id === nodeId) ||
      knowledgeTreeNodes.find((item) => item.node_id === legacyTreeNodeAliases[nodeId])
  }

  function normalizeTreePath(value?: string) {
    return (value || '').toLowerCase().replace(/\s+/g, ' ').trim()
  }

  function sortTreeNodes(nodes: KnowledgeTreeNode[]) {
    return [...nodes].sort((left, right) => {
      if (left.level !== right.level) return left.level - right.level
      return (left.sort_order || 0) - (right.sort_order || 0) || left.title.localeCompare(right.title)
    })
  }

  function getNodeChildren(nodeId: string) {
    return sortTreeNodes(knowledgeTreeNodes.filter((item) => item.parent_id === nodeId))
  }

  function getNodeDescendants(node: KnowledgeTreeNode) {
    const descendants = new Set<string>()
    const queue = [node.node_id]
    while (queue.length) {
      const current = queue.shift()!
      for (const child of knowledgeTreeNodes.filter((item) => item.parent_id === current)) {
        descendants.add(child.node_id)
        queue.push(child.node_id)
      }
    }

    const normalizedPath = normalizeTreePath(node.path)
    for (const item of knowledgeTreeNodes) {
      if (item.node_id !== node.node_id && normalizeTreePath(item.path).startsWith(`${normalizedPath} /`)) {
        descendants.add(item.node_id)
      }
    }

    return sortTreeNodes(knowledgeTreeNodes.filter((item) => descendants.has(item.node_id)))
  }

  function getScopeNodes(node: KnowledgeTreeNode) {
    return [node, ...getNodeDescendants(node)]
  }

  function getLevel1Nodes() {
    return sortTreeNodes(
      knowledgeTreeNodes.filter((item) => item.level === 1 || item.parent_id === 'kt')
    )
  }

  function getLevel2Nodes(level1Id: string | null) {
    if (!level1Id) return []
    const level1 = findTreeNode(level1Id)
    if (!level1) return []
    const normalizedPath = normalizeTreePath(level1.path)
    return sortTreeNodes(
      knowledgeTreeNodes.filter((item) => {
        if (item.node_id === level1.node_id) return false
        if (item.parent_id === level1.node_id && item.level <= 2) return true
        return item.level === 2 && normalizeTreePath(item.path).startsWith(`${normalizedPath} /`)
      })
    )
  }

  function getLevel3Nodes(level2Id: string | null) {
    if (!level2Id) return []
    const level2 = findTreeNode(level2Id)
    if (!level2) return []
    const normalizedPath = normalizeTreePath(level2.path)
    return sortTreeNodes(
      knowledgeTreeNodes.filter((item) => {
        if (item.node_id === level2.node_id) return false
        if (item.parent_id === level2.node_id) return true
        return item.level >= 3 && normalizeTreePath(item.path).startsWith(`${normalizedPath} /`)
      })
    )
  }

  function getTreeAncestors(nodeId: string) {
    const node = findTreeNode(nodeId)
    if (!node) return []
    const ancestors: KnowledgeTreeNode[] = []
    let current = node
    while (current.parent_id) {
      const parent = findTreeNode(current.parent_id)
      if (!parent) break
      if (parent.node_id !== 'kt') ancestors.unshift(parent)
      current = parent
    }
    return ancestors
  }

  function findNodeByPath(path: string) {
    const normalizedPath = normalizeTreePath(path)
    return knowledgeTreeNodes.find((item) => normalizeTreePath(item.path) === normalizedPath)
  }

  function resolveNodeAlias(nodeId: string) {
    const direct = findTreeNode(nodeId)
    if (direct) return direct

    const candidate = ingestionCandidates.find((item) => item.tree_node_id === nodeId || item.canonical_node_id === nodeId)
    if (candidate?.tree_path) {
      const byPath = findNodeByPath(candidate.tree_path)
      if (byPath) return byPath
    }

    return knowledgeTreeNodes.find((item) => nodeId.startsWith(`${item.node_id}.`) || nodeId === item.node_id)
  }

  function getThreeLevelIdsForNode(node: KnowledgeTreeNode) {
    const chain = [...getTreeAncestors(node.node_id), node].filter((item) => item.node_id !== 'kt')
    const level1 = chain.find((item) => item.level === 1) || chain[0] || null
    const level2 = [...chain].reverse().find((item) => item.level === 2) || null
    const level3 = node.level >= 3 ? node : null
    return {
      selected_level1_id: level1?.node_id || null,
      selected_level2_id: level2?.node_id || null,
      selected_level3_id: level3?.node_id || null
    }
  }

  function resolveTreeSelection(query: {
    l1?: string | null
    l2?: string | null
    l3?: string | null
    node_id?: string | null
  }): KnowledgeTreeThreeLevelViewModel {
    let selectedLevel1Id = query.l1 || null
    let selectedLevel2Id = query.l2 || null
    let selectedLevel3Id = query.l3 || null

    if (query.node_id) {
      const node = resolveNodeAlias(query.node_id)
      if (node) {
        const resolved = getThreeLevelIdsForNode(node)
        selectedLevel1Id = resolved.selected_level1_id
        selectedLevel2Id = resolved.selected_level2_id
        selectedLevel3Id = resolved.selected_level3_id
      }
    }

    const level1Nodes = getLevel1Nodes()
    if (selectedLevel1Id && !findTreeNode(selectedLevel1Id)) selectedLevel1Id = null
    if (selectedLevel2Id && !findTreeNode(selectedLevel2Id)) selectedLevel2Id = null
    if (selectedLevel3Id && !findTreeNode(selectedLevel3Id)) selectedLevel3Id = null

    const level2Nodes = getLevel2Nodes(selectedLevel1Id)
    if (selectedLevel2Id && !level2Nodes.some((item) => item.node_id === selectedLevel2Id)) {
      selectedLevel2Id = null
      selectedLevel3Id = null
    }

    const level3Nodes = getLevel3Nodes(selectedLevel2Id)
    if (selectedLevel3Id && !level3Nodes.some((item) => item.node_id === selectedLevel3Id)) {
      selectedLevel3Id = null
    }

    const currentNode = selectedLevel3Id
      ? findTreeNode(selectedLevel3Id)
      : selectedLevel2Id
        ? findTreeNode(selectedLevel2Id)
        : selectedLevel1Id
          ? findTreeNode(selectedLevel1Id)
          : null

    const currentScope: KnowledgeTreeScope | null = currentNode
      ? {
          level: Math.min(Math.max(currentNode.level, 1), 3) as 1 | 2 | 3,
          node_id: currentNode.node_id,
          title: currentNode.title,
          path: currentNode.path
        }
      : null

    return {
      selected_level1_id: selectedLevel1Id,
      selected_level2_id: selectedLevel2Id,
      selected_level3_id: selectedLevel3Id,
      level1_nodes: level1Nodes,
      level2_nodes: level2Nodes,
      level3_nodes: level3Nodes,
      current_scope: currentScope,
      ancestor_chain: currentNode ? getTreeAncestors(currentNode.node_id) : [],
      scope_summary: currentNode ? getTreeScopeSummary(currentNode.node_id) : getTreeScopeSummary(null)
    }
  }

  function candidateMatchesTreeNode(candidate: IngestionCandidate, node: KnowledgeTreeNode) {
    const candidateTreeNodeId = legacyTreeNodeAliases[candidate.tree_node_id] || candidate.tree_node_id
    const candidateCanonicalNodeId = candidate.canonical_node_id
      ? legacyTreeNodeAliases[candidate.canonical_node_id] || candidate.canonical_node_id
      : undefined
    return (
      candidateTreeNodeId === node.node_id ||
      candidateCanonicalNodeId === node.node_id ||
      candidateTreeNodeId.startsWith(`${node.node_id}.`) ||
      Boolean(candidateCanonicalNodeId?.startsWith(`${node.node_id}.`)) ||
      Boolean(candidate.tree_path && candidate.tree_path.startsWith(node.path))
    )
  }

  function candidateMatchesTreeNodeId(candidate: IngestionCandidate, nodeId: string) {
    const resolvedNodeId = legacyTreeNodeAliases[nodeId] || nodeId
    const node = findTreeNode(resolvedNodeId)
    if (!node) {
      const candidateTreeNodeId = legacyTreeNodeAliases[candidate.tree_node_id] || candidate.tree_node_id
      const candidateCanonicalNodeId = candidate.canonical_node_id
        ? legacyTreeNodeAliases[candidate.canonical_node_id] || candidate.canonical_node_id
        : undefined
      return candidateTreeNodeId === resolvedNodeId || candidateCanonicalNodeId === resolvedNodeId
    }
    return candidateMatchesTreeNode(candidate, node)
  }

  function candidateMatchesTreeScope(candidate: IngestionCandidate, node: KnowledgeTreeNode) {
    return getScopeNodes(node).some((scopeNode) => candidateMatchesTreeNode(candidate, scopeNode))
  }

  function knowledgeItemMatchesTreeNode(item: { tree_node_id?: string; canonical_node_id?: string; tree_path?: string; canonical_tree_path?: string; domain: string; subdomain: string }, node: KnowledgeTreeNode) {
    const itemTreeNodeId = item.tree_node_id ? legacyTreeNodeAliases[item.tree_node_id] || item.tree_node_id : ''
    const itemCanonicalNodeId = item.canonical_node_id ? legacyTreeNodeAliases[item.canonical_node_id] || item.canonical_node_id : ''
    return (
      itemTreeNodeId === node.node_id ||
      itemCanonicalNodeId === node.node_id ||
      itemTreeNodeId.startsWith(`${node.node_id}.`) ||
      itemCanonicalNodeId.startsWith(`${node.node_id}.`) ||
      Boolean(item.tree_path && normalizeTreePath(item.tree_path).startsWith(normalizeTreePath(node.path))) ||
      Boolean(item.canonical_tree_path && normalizeTreePath(item.canonical_tree_path).startsWith(normalizeTreePath(node.path)))
    )
  }

  function getScopeIndexNode(nodeId: string | null) {
    if (!knowledgeTreeScopeIndex.value) return null
    const resolvedNodeId = nodeId ? legacyTreeNodeAliases[nodeId] || nodeId : 'kt'
    return knowledgeTreeScopeIndex.value.nodes[resolvedNodeId] ||
      knowledgeTreeScopeIndex.value.nodes[nodeId || ''] ||
      null
  }

  function getCandidatesForScopeByScan(nodeId: string | null) {
    if (!nodeId) return ingestionCandidates
    const node = findTreeNode(nodeId)
    if (!node) return []
    return ingestionCandidates.filter((item) => candidateMatchesTreeScope(item, node))
  }

  function getKnowledgeItemsForScopeByScan(nodeId: string | null) {
    if (!nodeId) return knowledgeItems
    const node = findTreeNode(nodeId)
    if (!node) return []
    const scopeNodes = getScopeNodes(node)
    return knowledgeItems.filter((item) => scopeNodes.some((scopeNode) => knowledgeItemMatchesTreeNode(item, scopeNode)))
  }

  function getCandidatesForScope(nodeId: string | null) {
    const indexed = getScopeIndexNode(nodeId)
    if (!indexed) return getCandidatesForScopeByScan(nodeId)
    return indexed.candidate_ids
      .map((id) => candidateById.value.get(id))
      .filter((item): item is IngestionCandidate => Boolean(item))
  }

  function getKnowledgeItemsForScope(nodeId: string | null) {
    const indexed = getScopeIndexNode(nodeId)
    if (!indexed) return getKnowledgeItemsForScopeByScan(nodeId)
    return indexed.knowledge_ids
      .map((id) => knowledgeById.value.get(id))
      .filter((item): item is KnowledgeItem => Boolean(item))
  }

  function makeKnowledgeCardSummary(item: KnowledgeItem): KnowledgeCardSummary {
    const node =
      findTreeNode(item.canonical_node_id || '') ||
      findTreeNode(item.tree_node_id || '') ||
      knowledgeTreeNodes.find((treeNode) => treeNode.domain === item.domain && treeNode.subdomain === item.subdomain) ||
      knowledgeTreeNodes.find((treeNode) => treeNode.domain === item.domain)
    const treeNodeId = node?.node_id || item.canonical_node_id || item.tree_node_id || item.subdomain || item.domain
    return {
      id: item.knowledge_id,
      title: item.title,
      subtitle: `${item.review_status} / ${treeNodeId}`,
      summary: item.statement,
      status: item.review_status,
      kind: 'knowledge',
      tree_node_id: treeNodeId,
      canonical_node_id: item.canonical_node_id || treeNodeId,
      source_count: item.sources.length,
      conflict_status: item.conflict_status,
      freshness_status: item.freshness,
      default_guidance: item.machine_gate?.default_guidance || 'deny',
    }
  }

  function makeCandidateCardSummary(item: IngestionCandidate): KnowledgeCardSummary {
    const status = item.workflow?.queue_group === 'formalized' ? 'accepted_for_draft' : item.candidate_status || item.review_status
    const canonicalNodeId = item.canonical_node_id || item.tree_node_id
    return {
      id: item.candidate_id,
      title: item.title || item.claim,
      subtitle: `${status} / ${canonicalNodeId}`,
      summary: item.claim,
      status,
      kind: 'candidate',
      tree_node_id: item.tree_node_id,
      canonical_node_id: canonicalNodeId,
      source_count: item.source_count,
      conflict_status: item.conflict_status,
      freshness_status: item.freshness,
      default_guidance: 'deny',
    }
  }

  function canSearchScope(query: string) {
    return query.trim().length >= 2
  }

  function listKnowledgeCardsForScope(params: {
    nodeId: string | null
    kind?: 'formal' | 'candidate' | 'all'
    query?: string
    status?: string
    conflictStatus?: string
    freshness?: string
    sort?: string
    page?: number
    pageSize?: number
  }): PagedResult<KnowledgeCardSummary> {
    const kind = params.kind || 'formal'
    const pageSize = Math.max(1, params.pageSize || 20)
    const query = (params.query || '').trim().toLowerCase()
    const searchEnabled = !query || canSearchScope(query)
    const formalCards = kind === 'candidate' ? [] : getKnowledgeItemsForScope(params.nodeId).map(makeKnowledgeCardSummary)
    const candidateCards = kind === 'formal' ? [] : getCandidatesForScope(params.nodeId).map(makeCandidateCardSummary)
    const filtered = [...formalCards, ...candidateCards].filter((item) => {
      const text = `${item.title} ${item.summary} ${item.subtitle} ${item.tree_node_id}`.toLowerCase()
      return (
        searchEnabled &&
        (!query || text.includes(query)) &&
        (!params.status || params.status === 'all' || item.status === params.status || item.kind === params.status) &&
        (!params.conflictStatus || params.conflictStatus === 'all' || item.conflict_status === params.conflictStatus) &&
        (!params.freshness || params.freshness === 'all' || item.freshness_status === params.freshness)
      )
    })

    const sorted = [...filtered].sort((left, right) => {
      if (params.sort === 'source_count_desc') return right.source_count - left.source_count
      if (params.sort === 'status') return left.status.localeCompare(right.status)
      if (params.sort === 'updated_desc') return right.id.localeCompare(left.id)
      if (left.kind !== right.kind) return left.kind.localeCompare(right.kind)
      return right.source_count - left.source_count
    })
    const total = sorted.length
    const page = Math.min(Math.max(params.page || 1, 1), Math.max(1, Math.ceil(total / pageSize)))
    const start = (page - 1) * pageSize
    return {
      items: sorted.slice(start, start + pageSize),
      total,
      page,
      page_size: pageSize,
      has_next: start + pageSize < total,
      source_version: knowledgeTreeScopeIndex.value?.source_version.formal_knowledge || 'fallback_scan',
      generated_at: knowledgeTreeScopeIndex.value?.generated_at || '',
    }
  }

  function getKnowledgeCardDetail(kind: 'knowledge' | 'candidate', id: string): KnowledgeCardDetail | null {
    if (kind === 'knowledge') {
      const item = knowledgeById.value.get(id)
      return item
        ? {
            id,
            kind,
            summary: item.statement,
            raw: item,
            loaded_from: 'formalKnowledgeItems',
            loaded_at: new Date().toISOString(),
          }
        : null
    }
    const candidate = candidateById.value.get(id)
    return candidate
      ? {
          id,
          kind,
          summary: candidate.claim,
          raw: candidate,
          loaded_from: 'phase23Candidates',
          loaded_at: new Date().toISOString(),
        }
      : null
  }

  function getTreeScopeSummary(nodeId: string | null): KnowledgeTreeScopeSummary {
    const scopeNodes = nodeId
      ? findTreeNode(nodeId)
        ? getScopeNodes(findTreeNode(nodeId)!)
        : []
      : knowledgeTreeNodes
    const candidates = getCandidatesForScope(nodeId)
    const formalItems = getKnowledgeItemsForScope(nodeId)
    return {
      node_count: scopeNodes.length,
      approved_item_count: formalItems.filter((item) => item.review_status === 'approved').length,
      reviewed_item_count: formalItems.filter((item) => item.review_status === 'reviewed').length,
      candidate_count: candidates.length,
      draft_count: candidates.filter((item) => item.candidate_status === 'accepted_for_draft').length,
      source_count: formalItems.reduce((total, item) => total + item.sources.length, 0) +
        candidates.reduce((total, item) => total + item.source_count, 0),
      open_gap_count: scopeNodes.reduce((total, item) => total + item.open_gaps.length, 0),
      conflict_count: formalItems.filter((item) => !['none', 'resolved'].includes(item.conflict_status)).length +
        candidates.filter((item) => item.conflict_status !== 'none').length
    }
  }

  function getCandidateCoverageForNode(node: KnowledgeTreeNode): CandidateCoverageSummary {
    const candidates = ingestionCandidates.filter((item) => candidateMatchesTreeScope(item, node))
    return {
      partition_id: Array.from(new Set(candidates.map((item) => item.partition_id || 'unknown'))).join(', ') || '-',
      tree_node_id: node.node_id,
      candidate_count: candidates.length,
      accepted_for_draft_count: candidates.filter((item) => item.candidate_status === 'accepted_for_draft').length,
      needs_more_evidence_count: candidates.filter((item) => item.candidate_status === 'needs_more_evidence').length,
      blocked_count: candidates.filter((item) => item.candidate_status === 'blocked').length,
      source_count: candidates.reduce((total, item) => total + item.source_count, 0),
      conflict_count: candidates.filter((item) => item.conflict_status !== 'none').length
    }
  }

  function resetFilter() {
    Object.assign(filter, initialFilter)
  }

  function findKnowledge(id: string) {
    return knowledgeItems.find((item) => item.knowledge_id === id)
  }

  async function initializeKnowledgeTreeApi() {
    const result = await checkKnowledgeTreeApiHealth(knowledgeTreeApi.baseUrl)
    Object.assign(knowledgeTreeApi, result)
  }

  return {
    filter,
    dataState,
    knowledgeTreeApi,
    knowledgeTreeScopeIndex,
    knowledgeItems,
    filteredKnowledge,
    conflicts,
    sources,
    tasks,
    contributions,
    knowledgeTreeNodes,
    ingestionCandidates,
    phase23CandidateFixtureGeneratedAt,
    searchTestCases: runtimeSearchCases,
    projectAdapters,
    summary,
    treeSummary,
    domains,
    sourceTypes,
    initializeFixtureData,
    resetFilter,
    findKnowledge,
    findTreeNode,
    getLevel1Nodes,
    getLevel2Nodes,
    getLevel3Nodes,
    getTreeAncestors,
    getNodeDescendants,
    resolveTreeSelection,
    getTreeScopeSummary,
    getCandidatesForScope,
    getKnowledgeItemsForScope,
    listKnowledgeCardsForScope,
    getKnowledgeCardDetail,
    candidateMatchesTreeNodeId,
    getCandidateCoverageForNode,
    initializeKnowledgeTreeApi
  }
})
