/**
 * ConsolePanel — Consola de salida con auto-scroll.
 */
import { useRef, useEffect } from 'react'
import { S } from '../styles/appStyles'
import ConsoleLine from './common/ConsoleLine'

export default function ConsolePanel({ conLines, onClear }) {
  const consoleRef = useRef(null)

  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight
    }
  }, [conLines])

  return (
    <div style={S.console}>
      <div style={S.consoleHeader}>
        <span style={S.consoleLabel}>consola</span>
        <button style={S.conClear} onClick={onClear}>limpiar</button>
      </div>
      <div ref={consoleRef} style={S.consoleOutput}>
        {conLines.map((l, i) => <ConsoleLine key={i} text={l.text} cls={l.cls} />)}
      </div>
    </div>
  )
}
