export type Event = { ts: string; agent: string; message: string }
export type Incident = {
  id: string; status: string; created_at: string
  alert: { service: string; severity: string; title: string }
  timeline: Event[]; logs: string[]
  diagnosis?: { root_cause_summary: string; evidence_list: string[]; proposed_fix: string; confidence_score: number; diff: string; source: string }
  action?: { label: string; risk: string; target: string }
  metrics: { t: number; error_rate: number }[]; postmortem?: string
}
const j = (r: Response) => r.json()
export const api = {
  list: (): Promise<Incident[]> => fetch('/api/v1/incidents').then(j),
  trigger: (): Promise<Incident> => fetch('/api/v1/alerts', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' }).then(j),
  approve: (id: string) => fetch(`/api/v1/incidents/${id}/approve`, { method: 'POST' }).then(j),
  reject: (id: string) => fetch(`/api/v1/incidents/${id}/reject`, { method: 'POST' }).then(j),
}
