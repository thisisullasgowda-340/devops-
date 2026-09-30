import { useEffect, useState } from 'react'
import { api, type Incident } from '../api'
import IncidentTimeline from '../components/IncidentTimeline'
import LogViewer from '../components/LogViewer'
import ApprovalCard from '../components/ApprovalCard'
import PostMortem from '../components/PostMortem'

const STAGES = ['INIT', 'COLLECTING', 'ANALYZING', 'APPROVAL_PENDING', 'REMEDIATING', 'VERIFYING', 'CLOSED']
const card: React.CSSProperties = { background: '#0f172a', border: '1px solid #1e293b', borderRadius: 12, padding: 20, display: 'flex', flexDirection: 'column', gap: 12 }

export default function Dashboard() {
  const [incs, setIncs] = useState<Incident[]>([])
  const [error, setError] = useState('')
  const refresh = () => api.list().then(d => { setIncs(d); setError('') }).catch(() => setError('Backend unreachable'))
  useEffect(() => { refresh(); const t = setInterval(refresh, 1000); return () => clearInterval(t) }, [])
  const inc = incs[0]
  const stage = inc ? STAGES.indexOf(inc.status) : -1
  const closed = inc?.status === 'CLOSED'

  return <div style={{ maxWidth: 1200, margin: '0 auto', padding: 24, display: 'flex', flexDirection: 'column', gap: 20 }}>
    <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <div><h1 style={{ margin: 0, fontSize: 24 }}>DevOps Copilot</h1><span style={{ color: '#94a3b8', fontSize: 14 }}>AI Incident Response Command Center</span></div>
      <button onClick={() => api.trigger().then(refresh)} style={{ background: '#dc2626', color: 'white', border: 0, padding: '10px 18px', borderRadius: 8, fontWeight: 600, cursor: 'pointer' }}>Simulate payment_db_timeout</button>
    </header>
    {error && <div style={{ color: '#f87171' }}>{error}</div>}
    {!inc ? <div style={{ ...card, alignItems: 'center', padding: 64, color: '#94a3b8' }}>All systems operational. Trigger a simulated incident to watch the agents respond.</div> : <>
      <div style={{ ...card, borderColor: closed ? '#16a34a' : '#dc2626', background: closed ? '#052e16' : '#450a0a' }}>
        <strong style={{ fontSize: 18 }}>{closed ? 'RESOLVED' : inc.alert.severity} - {inc.alert.title}</strong>
        <span style={{ color: '#cbd5e1', fontSize: 13 }}>Incident {inc.id} · {inc.alert.service}</span>
      </div>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {STAGES.map((s, i) => <span key={s} style={{ flex: 1, textAlign: 'center', fontSize: 11, padding: '8px 4px', borderRadius: 6, fontWeight: 600,
          background: i < stage || closed ? '#14532d' : i === stage ? '#1d4ed8' : '#1e293b', color: i <= stage ? 'white' : '#64748b' }}>{s}</span>)}
      </div>
      {inc.status === 'APPROVAL_PENDING' && <ApprovalCard inc={inc} onApprove={() => api.approve(inc.id).then(refresh)} onReject={() => api.reject(inc.id).then(refresh)} />}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: 20 }}>
        <div style={card}><h3 style={{ margin: 0 }}>Agent Execution Trace</h3><IncidentTimeline events={inc.timeline} /></div>
        <div style={card}>
          <h3 style={{ margin: 0 }}>Root Cause Diagnosis</h3>
          {inc.diagnosis ? <>
            <div style={{ fontSize: 32, fontWeight: 700, color: '#a78bfa' }}>{inc.diagnosis.confidence_score}% <span style={{ fontSize: 13, color: '#94a3b8', fontWeight: 400 }}>confidence · {inc.diagnosis.source}</span></div>
            <span>{inc.diagnosis.root_cause_summary}</span>
            <ul style={{ margin: 0, paddingLeft: 20, color: '#cbd5e1', fontSize: 14 }}>{inc.diagnosis.evidence_list.map(e => <li key={e}>{e}</li>)}</ul>
            <pre style={{ margin: 0, background: '#020617', padding: 12, borderRadius: 8, fontSize: 12 }}>{inc.diagnosis.diff.split('\n').map((l, i) =>
              <div key={i} style={{ color: l.startsWith('+') ? '#4ade80' : l.startsWith('-') ? '#f87171' : '#94a3b8' }}>{l}</div>)}</pre>
          </> : <span style={{ color: '#64748b' }}>Analysis pending...</span>}
        </div>
      </div>
      <div style={card}><h3 style={{ margin: 0 }}>Logs</h3><LogViewer lines={inc.logs} /></div>
      {inc.metrics.length > 0 && <div style={card}><h3 style={{ margin: 0 }}>Verification: error rate %</h3>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 6, height: 80 }}>{inc.metrics.map(m =>
          <div key={m.t} title={`${m.error_rate}%`} style={{ flex: 1, height: `${Math.max(2, m.error_rate * 2)}%`, background: m.error_rate > 0 ? '#f87171' : '#34d399', borderRadius: 3 }} />)}</div></div>}
      {inc.postmortem && <div style={card}><PostMortem md={inc.postmortem} /></div>}
    </>}
  </div>
}
