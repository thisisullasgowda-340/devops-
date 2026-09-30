import type { Event } from '../api'
const colors: Record<string, string> = { Supervisor: '#94a3b8', Collector: '#38bdf8', Analyzer: '#a78bfa', Guard: '#fbbf24', Verifier: '#34d399', Reporter: '#34d399' }
export default function IncidentTimeline({ events }: { events: Event[] }) {
  return <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
    {events.map((e, i) => <div key={i} style={{ display: 'flex', gap: 12, fontSize: 14 }}>
      <span style={{ color: '#64748b', fontFamily: 'monospace' }}>{e.ts.slice(11, 19)}</span>
      <span style={{ color: colors[e.agent], fontWeight: 600, minWidth: 80 }}>{e.agent}</span>
      <span>{e.message}</span></div>)}
  </div>
}
