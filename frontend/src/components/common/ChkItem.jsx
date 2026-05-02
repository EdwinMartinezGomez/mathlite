/**
 * ChkItem — Elemento de checklist con estado (ok, warn, err).
 */
export default function ChkItem({ status, text }) {
  const colors = { ok:'var(--ok)', warn:'var(--warn)', err:'var(--err)' }
  return (
    <div style={{ display:'flex', gap:8, fontSize:12, fontFamily:"'JetBrains Mono', monospace", alignItems:'flex-start' }}>
      <span style={{ color: colors[status], flexShrink:0 }}>{status}</span>
      <span style={{ color:'var(--txt2)' }}>{text}</span>
    </div>
  )
}
