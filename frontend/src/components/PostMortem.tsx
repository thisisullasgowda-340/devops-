export default function PostMortem({ md }: { md: string }) {
  const inline = (s: string) => s.split(/(\*\*[^*]+\*\*|`[^`]+`)/).map((p, i) =>
    p.startsWith('**') ? <strong key={i}>{p.slice(2, -2)}</strong> : p.startsWith('`') ? <code key={i} style={{ color: '#94a3b8' }}>{p.slice(1, -1)}</code> : p)
  return <div style={{ lineHeight: 1.6, fontSize: 14 }}>{md.split('\n').map((l, i) =>
    l.startsWith('# ') ? <h2 key={i} style={{ margin: '0 0 8px' }}>{l.slice(2)}</h2>
    : l.startsWith('## ') ? <h3 key={i} style={{ margin: '16px 0 4px', color: '#38bdf8' }}>{l.slice(3)}</h3>
    : l.startsWith('- ') ? <div key={i} style={{ paddingLeft: 16 }}>• {inline(l.slice(2))}</div>
    : l.trim() ? <div key={i}>{inline(l)}</div> : null)}
    <button onClick={() => navigator.clipboard?.writeText(md)} style={{ marginTop: 16, background: '#1e293b', color: '#e2e8f0', border: '1px solid #334155', padding: '8px 14px', borderRadius: 8, cursor: 'pointer' }}>Copy Markdown</button>
  </div>
}
