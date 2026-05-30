/**
 * TestsPanel — Lista de casos de prueba con vista de detalle.
 */
import { useState } from 'react'
import { S } from '../styles/appStyles'

export default function TestsPanel({ tests = [], onLoadAndRun, onLoad }) {
  const [selected, setSelected] = useState(null)
  const t = tests.find(x => x.id === selected)
  const catColors = { 'cat-ok':'var(--ok)', 'cat-err':'var(--err)', 'cat-warn':'var(--warn)' }

  return (
    <div style={S.testsWrap}>
      <div style={S.testsList}>
        {tests.map(tc => (
          <div key={tc.id} style={S.testItem(selected===tc.id)} onClick={()=>setSelected(tc.id)}>
            <div style={S.testName}>{tc.name}</div>
            <div style={{ fontSize:10, fontFamily:"'JetBrains Mono', monospace", letterSpacing:'0.06em', color:catColors[tc.catClass] }}>{tc.cat}</div>
          </div>
        ))}
      </div>
      <div style={S.testDetail}>
        {tests.length === 0 ? (
          <div style={S.empty}>cargando casos desde MongoDB...</div>
        ) : !t ? (
          <div style={S.empty}>selecciona un caso de prueba</div>
        ) : (
          <>
            <div>
              <div style={{ fontSize:13, fontWeight:500, color:'var(--txt)', marginBottom:4 }}>{t.name}</div>
              <div style={{ fontSize:12, color:'var(--txt2)', fontFamily:"'JetBrains Mono', monospace" }}>{t.desc}</div>
            </div>
            <div>
              <div style={{ fontSize:10, letterSpacing:'0.09em', color:'var(--txt3)', fontFamily:"'JetBrains Mono', monospace", marginBottom:8 }}>código</div>
              <pre style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:4, padding:12, fontFamily:"'JetBrains Mono', monospace", fontSize:12, lineHeight:1.8, overflowX:'auto' }}>{t.code}</pre>
            </div>
            <div>
              <div style={{ fontSize:10, letterSpacing:'0.09em', color:'var(--txt3)', fontFamily:"'JetBrains Mono', monospace", marginBottom:4 }}>resultado esperado</div>
              <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:4, padding:10, fontFamily:"'JetBrains Mono', monospace", fontSize:12 }}>
                <div style={{ fontSize:10, letterSpacing:'0.07em', color:'var(--txt3)', marginBottom:4 }}>EXPECT</div>
                {t.expect}
              </div>
            </div>
            <div style={{ display:'flex', gap:8 }}>
              <button style={S.btn('primary')} onClick={()=>onLoadAndRun(t.id)}>▶ cargar y ejecutar</button>
              <button style={S.btn('')} onClick={()=>onLoad(t.id)}>cargar en editor</button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
