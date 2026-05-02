/**
 * ConsoleLine — Una línea individual de la consola.
 */
export default function ConsoleLine({ text, cls }) {
  const colors = {
    'c-dim':   '#555', 'c-ok':    '#66CC88', 'c-warn': '#DDAA44',
    'c-val':   '#FFDD88', 'c-err': '#FF8888', 'c-w':   '#EEEEEE',
    'c-print': '#AADDFF',
  }
  return (
    <div style={{
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: 12,
      lineHeight: 1.6,
      whiteSpace: 'pre-wrap',
      wordBreak: 'break-all',
      color: colors[cls] || '#EEEEEE',
    }}>
      {text}
    </div>
  )
}
