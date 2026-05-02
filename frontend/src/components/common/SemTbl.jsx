/**
 * SemTbl — Tabla semántica con estilo mono.
 */
export default function SemTbl({ children }) {
  return (
    <table style={{ width:'100%', borderCollapse:'collapse', fontSize:11.5, fontFamily:"'JetBrains Mono', monospace" }}>
      {children}
    </table>
  )
}
