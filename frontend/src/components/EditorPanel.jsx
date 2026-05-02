/**
 * EditorPanel — Editor de código con números de línea y panel de errores.
 */
import { useRef } from 'react'
import { S } from '../styles/appStyles'

export default function EditorPanel({ code, onCodeChange, onRun, running, errors, onClear }) {
  const editorRef = useRef(null)

  const lineCount = code.split('\n').length
  const lineNums  = Array.from({ length: lineCount }, (_, i) => i + 1).join('\n')

  const syncScroll = () => {
    if (editorRef.current) {
      const lns = editorRef.current.previousSibling
      if (lns) lns.scrollTop = editorRef.current.scrollTop
    }
  }

  return (
    <>
      <div style={S.editorHeader}>
        <span style={S.panelLabel}><b>editor</b> — main.ml</span>
        <div style={S.editorActions}>
          <button style={S.btn('primary')} onClick={onRun} disabled={running}>
            {running ? '⏳ ejecutando…' : '▶ ejecutar'}
          </button>
          <button style={S.btn('danger')} onClick={onClear}>
            limpiar
          </button>
        </div>
      </div>

      <div style={S.editorWrap}>
        <div style={S.lineNums}>{lineNums}</div>
        <textarea
          ref={editorRef}
          style={S.textarea}
          value={code}
          onChange={e => onCodeChange(e.target.value)}
          onScroll={syncScroll}
          spellCheck={false}
          placeholder={"-- escribe tu programa MathLite aquí\u000alet x = 5\u000aprint(x)"}
        />
      </div>

      {/* ERROR PANEL */}
      <div style={S.errPanel}>
        {errors.length === 0 ? (
          <div style={S.noErrors}>sin errores</div>
        ) : errors.map((e, i) => (
          <div key={i} style={S.errLine}>
            <span style={S.errPhase}>[{e.phase}]</span>
            <span>línea {e.line ?? '?'}: {e.msg}</span>
          </div>
        ))}
      </div>
    </>
  )
}
