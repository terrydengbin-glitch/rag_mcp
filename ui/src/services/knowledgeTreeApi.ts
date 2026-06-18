export type KnowledgeTreeApiHealthState = 'unchecked' | 'healthy' | 'fixture_fallback' | 'error'

export interface KnowledgeTreeApiHealth {
  state: KnowledgeTreeApiHealthState
  baseUrl: string
  readOnly: boolean
  message: string
  checkedAt: string | null
}

type HealthResponse = {
  ok?: boolean
  data?: {
    status?: string
    read_only?: boolean
    index_loaded?: boolean
  }
}

const DEFAULT_API_BASE_URL = ''

export function getKnowledgeTreeApiBaseUrl() {
  return import.meta.env.VITE_CEK_TA_API_BASE_URL || DEFAULT_API_BASE_URL
}

export async function checkKnowledgeTreeApiHealth(baseUrl = getKnowledgeTreeApiBaseUrl()): Promise<KnowledgeTreeApiHealth> {
  if (!baseUrl) {
    return {
      state: 'fixture_fallback',
      baseUrl: 'fixture',
      readOnly: true,
      message: '未配置 FastAPI 地址，已使用本地 fixture 数据',
      checkedAt: new Date().toISOString()
    }
  }

  const controller = new AbortController()
  const timer = window.setTimeout(() => controller.abort(), 3000)
  const checkedAt = new Date().toISOString()

  try {
    const response = await fetch(`${baseUrl.replace(/\/$/, '')}/api/health`, {
      method: 'GET',
      signal: controller.signal
    })
    const payload = (await response.json()) as HealthResponse
    const readOnly = Boolean(payload.data?.read_only)
    if (response.ok && payload.ok !== false && readOnly) {
      return {
        state: 'healthy',
        baseUrl,
        readOnly,
        message: payload.data?.index_loaded === false ? 'FastAPI 可用，但索引未加载' : 'FastAPI 只读接口可用',
        checkedAt
      }
    }

    return {
      state: 'fixture_fallback',
      baseUrl,
      readOnly,
      message: 'FastAPI 未确认 read_only=true，已使用本地 fixture 数据',
      checkedAt
    }
  } catch {
    return {
      state: 'fixture_fallback',
      baseUrl,
      readOnly: true,
      message: 'FastAPI 不可用，已使用本地 fixture 数据',
      checkedAt
    }
  } finally {
    window.clearTimeout(timer)
  }
}
