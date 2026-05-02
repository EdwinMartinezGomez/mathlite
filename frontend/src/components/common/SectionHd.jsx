/**
 * SectionHd — Encabezado de sección con estilo mono.
 */
export default function SectionHd({ children, style }) {
  return (
    <div style={{
      fontSize: 10, letterSpacing: '0.09em', color: 'var(--txt3)',
      fontFamily: "'JetBrains Mono', monospace",
      marginBottom: 8, marginTop: 16, ...(style || {}),
    }}>
      {children}
    </div>
  )
}
