import type { components } from './schema'

export type Complaint = components['schemas']['Complaint']
export type ComplaintCreate = components['schemas']['ComplaintCreate']
export type ComplaintPage = components['schemas']['ComplaintPage']
export type Category = components['schemas']['Category']
export type Priority = components['schemas']['Priority']
export type Status = components['schemas']['Status']
export type Stats = components['schemas']['Stats']
export type ProvidersMeta = components['schemas']['ProvidersMeta']
export type ApiErrorBody = components['schemas']['ApiError']

export type ComplaintFilters = {
  page?: number
  page_size?: number
  category?: Category
  priority?: Priority
  status?: Status
}

export class ApiError extends Error {
  constructor(
    readonly status: number,
    readonly body: ApiErrorBody | null,
    readonly retryAfter: string | null = null,
  ) {
    super(body?.error.message ?? `Request failed (${status})`)
    this.name = 'ApiError'
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<{ data: T; response: Response }> {
  const response = await fetch(path, {
    ...init,
    headers: { Accept: 'application/json', ...init?.headers },
  })
  const body: unknown = await response.json().catch(() => null)
  if (!response.ok) {
    const errorBody = isApiErrorBody(body) ? body : null
    throw new ApiError(response.status, errorBody, response.headers.get('Retry-After'))
  }
  return { data: body as T, response }
}

function isApiErrorBody(value: unknown): value is ApiErrorBody {
  if (typeof value !== 'object' || value === null || !('error' in value)) return false
  const error = value.error
  return typeof error === 'object' && error !== null &&
    'message' in error && typeof error.message === 'string' &&
    'code' in error && typeof error.code === 'string'
}

export async function createComplaint(input: ComplaintCreate): Promise<Complaint> {
  return (await request<Complaint>('/api/complaints', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })).data
}

export async function getComplaint(id: string): Promise<Complaint> {
  return (await request<Complaint>(`/api/complaints/${encodeURIComponent(id)}`)).data
}

export async function listComplaints(filters: ComplaintFilters = {}): Promise<ComplaintPage> {
  const params = new URLSearchParams()
  for (const [key, value] of Object.entries(filters)) {
    if (value !== undefined) params.set(key, String(value))
  }
  const query = params.size ? `?${params}` : ''
  return (await request<ComplaintPage>(`/api/complaints${query}`)).data
}

export async function updateStatus(id: string, status: Status): Promise<Complaint> {
  return (await request<Complaint>(`/api/complaints/${encodeURIComponent(id)}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status } satisfies components['schemas']['StatusUpdate']),
  })).data
}

export async function getStats(): Promise<{ stats: Stats; cache: 'HIT' | 'MISS' | null }> {
  const { data, response } = await request<Stats>('/api/stats')
  const header = response.headers.get('X-Cache')
  return { stats: data, cache: header === 'HIT' || header === 'MISS' ? header : null }
}

export async function getProviders(): Promise<ProvidersMeta> {
  return (await request<ProvidersMeta>('/api/meta/providers')).data
}
