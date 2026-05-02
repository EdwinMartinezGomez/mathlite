/**
 * ASTPanel — Muestra el árbol de sintaxis abstracta.
 */
import { S } from '../styles/appStyles'

export default function ASTPanel({ astText, nodeCount }) {
  if (!astText) {
    return (
      <div style={S.astWrap}>
        <div style={S.empty}>ejecuta un programa para ver el AST</div>
      </div>
    )
  }
  return (
    <div style={S.astWrap}>
      <pre style={{ fontFamily:"'JetBrains Mono', monospace", fontSize:12, lineHeight:1.7, whiteSpace:'pre', color:'var(--txt)' }}>
        {astText}
      </pre>
    </div>
  )
}
