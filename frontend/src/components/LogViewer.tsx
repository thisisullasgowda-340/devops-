export default function LogViewer({ lines }: { lines: string[] }) {
  const c = (l: string) => l.includes('ERROR') ? '#f87171' : l.includes('WARN') ? '#fbbf24' : '#94a3b8'
  return <pre style={{ margin: 0, maxHeight: 220, overflow: 'auto', fontSize: 12, background: '#020617', padding: 12, borderRadius: 8 }}>
    {lines.length ? lines.map((l, i) => <div key={i} style={{ color: c(l) }}>{l}</div>) : <span style={{ color: '#64748b' }}>No logs collected yet.</span>}
  </pre>
}
