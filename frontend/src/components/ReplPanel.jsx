/**
 * ReplPanel — Modo interactivo por línea para MathLite.
 */
import { useEffect, useRef, useState } from 'react'
import ConsoleLine from './common/ConsoleLine'
import { S } from '../styles/appStyles'

export default function ReplPanel({ onExecuteSource }) {
  const [input, setInput] = useState('')
  const [lines, setLines] = useState([
    { text: '-- REPL MathLite. Escribe una sentencia y presiona Enter.', cls: 'c-dim' },
  ])
  const [context, setContext] = useState('')
  const [prevOutLen, setPrevOutLen] = useState(0)
  const [running, setRunning] = useState(false)

  const inputRef = useRef(null)
  const outputRef = useRef(null)

  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight
    }
  }, [lines])

  function add(text, cls) {
    setLines(prev => [...prev, { text, cls: cls || 'c-w' }])
  }

  async function handleRun(e) {
    if (e?.preventDefault) e.preventDefault()

    const line = input.trim()
    if (!line || running) return

    const nextContext = context ? `${context}\n${line}` : line
    const previousLineCount = context ? context.split('\n').length : 0

    add(`❯ ${line}`, 'c-dim')
    setInput('')
    setRunning(true)

    try {
      const data = await onExecuteSource(nextContext)
      const output = Array.isArray(data?.output) ? data.output : []
      const errors = Array.isArray(data?.errors) ? data.errors : []

      const newOutput = output.slice(prevOutLen)
      const newErrors = errors.filter(e => (e.line ?? 0) > previousLineCount)

      if (newOutput.length > 0) {
        newOutput.forEach(o => add(o, 'c-print'))
      } else if (newErrors.length === 0) {
        add('-- (ok)', 'c-dim')
      }

      newErrors.forEach(e => {
        add(`[${e.phase}] línea ${e.line ?? '?'}: ${e.msg}`, 'c-err')
      })

      const hasRuntimeError = errors.some(e => e.phase === 'ejecución')
      if (!hasRuntimeError) {
        setContext(nextContext)
        setPrevOutLen(output.length)
      }
    } catch (err) {
      add(`Error de conexión: ${err.message}`, 'c-err')
    } finally {
      setRunning(false)
      setTimeout(() => inputRef.current?.focus(), 50)
    }
  }

  function handleReset() {
    setContext('')
    setPrevOutLen(0)
    setLines([{ text: '-- contexto reiniciado.', cls: 'c-dim' }])
    setInput('')
    setTimeout(() => inputRef.current?.focus(), 50)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      <div style={S.editorHeader}>
        <span style={S.panelLabel}><b>repl</b> — modo interactivo</span>
        <div style={S.editorActions}>
          <button style={S.btn('danger')} onClick={handleReset}>reiniciar contexto</button>
        </div>
      </div>

      <div
        ref={outputRef}
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '10px 16px',
          display: 'flex',
          flexDirection: 'column',
          gap: 3,
          minHeight: 0,
          fontFamily: "'JetBrains Mono', monospace",
          fontSize: 12.5,
        }}
      >
        {lines.map((l, i) => <ConsoleLine key={i} text={l.text} cls={l.cls} />)}
      </div>

      <form
        onSubmit={handleRun}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '10px 14px',
          borderTop: '1px solid var(--border)',
          flexShrink: 0,
          background: 'var(--bg2)',
        }}
      >
        <span style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 13 }}>❯</span>
        <input
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          disabled={running}
          placeholder="let x = 5   |   print(x)   |   def f(n) { return n * 2 }"
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            fontFamily: "'JetBrains Mono', monospace",
            fontSize: 13,
          }}
          autoFocus
        />
        <button type="submit" style={S.btn('primary')} disabled={running}>
          {running ? '⏳' : 'Enter'}
        </button>
      </form>

    </div>
  )
}