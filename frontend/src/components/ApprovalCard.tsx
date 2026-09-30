import type { Incident } from '../api'
export default function ApprovalCard({ inc, onApprove, onReject }: { inc: Incident; onApprove: () => void; onReject: () => void }) {
  return <div style={{ border: '1px solid #f59e0b', background: '#451a03', borderRadius: 12, padding: 20, display: 'flex', flexDirection: 'column', gap: 12 }}>
    <strong style={{ color: '#fbbf24' }}>{inc.action?.risk} — Human approval required</strong>
    <span>{inc.diagnosis?.proposed_fix}</span>
    <div style={{ display: 'flex', gap: 8 }}>
      <button onClick={onApprove} style={{ background: '#16a34a', color: 'white', border: 0, padding: '10px 16px', borderRadius: 8, fontWeight: 600, cursor: 'pointer' }}>{inc.action?.label}</button>
      <button onClick={onReject} style={{ background: 'transparent', color: '#e2e8f0', border: '1px solid #475569', padding: '10px 16px', borderRadius: 8, cursor: 'pointer' }}>Reject</button>
    </div>
  </div>
}
