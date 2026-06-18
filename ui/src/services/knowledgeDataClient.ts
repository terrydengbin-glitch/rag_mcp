import type { IngestionCandidate, KnowledgeItem, KnowledgeTreeNode, KnowledgeTreeScopeIndex } from '../types'

export type DataClientErrorCode =
  | 'data_not_found'
  | 'schema_mismatch'
  | 'network_error'
  | 'empty_result'
  | 'index_not_loaded'
  | 'node_not_found'
  | 'detail_not_found'

export interface LazyFixturePayload<T> {
  schema_version: string
  generated_at: string
  source: string
  count: number
  items: T[]
}

export class KnowledgeDataClientError extends Error {
  code: DataClientErrorCode
  url: string

  constructor(code: DataClientErrorCode, message: string, url: string) {
    super(message)
    this.name = 'KnowledgeDataClientError'
    this.code = code
    this.url = url
  }
}

function dataUrl(fileName: string) {
  const base = import.meta.env.BASE_URL || '/'
  const normalizedBase = base.endsWith('/') ? base : `${base}/`
  return `${normalizedBase}data/${fileName}`
}

async function fetchFixture<T>(fileName: string): Promise<LazyFixturePayload<T>> {
  const url = dataUrl(fileName)
  let response: Response
  try {
    response = await fetch(url, { cache: 'no-cache' })
  } catch (error) {
    throw new KnowledgeDataClientError('network_error', `无法读取前端静态数据：${fileName}`, url)
  }

  if (!response.ok) {
    throw new KnowledgeDataClientError('data_not_found', `未找到前端静态数据：${fileName}`, url)
  }

  const payload = await response.json().catch(() => null)
  if (!payload || typeof payload !== 'object' || !Array.isArray(payload.items)) {
    throw new KnowledgeDataClientError('schema_mismatch', `前端静态数据结构不符合契约：${fileName}`, url)
  }
  if (payload.count !== payload.items.length) {
    throw new KnowledgeDataClientError('schema_mismatch', `前端静态数据 count 与 items 数量不一致：${fileName}`, url)
  }
  if (payload.items.length === 0) {
    throw new KnowledgeDataClientError('empty_result', `前端静态数据为空：${fileName}`, url)
  }

  return payload as LazyFixturePayload<T>
}

async function fetchJsonFixture<T>(fileName: string): Promise<T> {
  const url = dataUrl(fileName)
  let response: Response
  try {
    response = await fetch(url, { cache: 'no-cache' })
  } catch (error) {
    throw new KnowledgeDataClientError('network_error', `无法读取前端静态数据：${fileName}`, url)
  }

  if (!response.ok) {
    throw new KnowledgeDataClientError('data_not_found', `未找到前端静态数据：${fileName}`, url)
  }

  const payload = await response.json().catch(() => null)
  if (!payload || typeof payload !== 'object') {
    throw new KnowledgeDataClientError('schema_mismatch', `前端静态数据结构不符合契约：${fileName}`, url)
  }

  return payload as T
}

export function loadCandidateFixture() {
  return fetchFixture<IngestionCandidate>('phase23Candidates.json')
}

export function loadFormalKnowledgeFixture() {
  return fetchFixture<KnowledgeItem>('formalKnowledgeItems.json')
}

export function loadKnowledgeTreeFixture() {
  return fetchFixture<KnowledgeTreeNode>('knowledgeTreeNodes.json')
}

export function loadKnowledgeTreeScopeIndex() {
  return fetchJsonFixture<KnowledgeTreeScopeIndex>('knowledgeTreeScopeIndex.json')
}
