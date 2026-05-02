/**
 * TokensPanel — Muestra el flujo de tokens con categorías.
 */
import SectionHd from './common/SectionHd'
import SemTbl from './common/SemTbl'
import { S } from '../styles/appStyles'
import { TK_CATS } from '../helpers/utils'

export default function TokensPanel({ tokens }) {
  if (!tokens || tokens.length === 0) {
    return (
      <div style={{ ...S.tokenScroll }}>
        <div style={S.empty}><span>ejecuta un programa para ver los tokens</span></div>
      </div>
    )
  }

  const filtered = tokens.filter(t => t.type !== 'EOF')
  const KW_TYPES = new Set(['LET','DEF','IF','ELSE','WHILE','RETURN','PRINT','AND','OR','NOT'])
  const OP_TYPES = new Set(['+','-','*','/','%','^','==','!=','<','>','<=','>=','='])
  const DEL_TYPES = new Set(['(',')','{','}',',',';'])

  const groups = {
    'palabras reservadas': filtered.filter(t => KW_TYPES.has(t.type)),
    'identificadores':     filtered.filter(t => t.type === 'ID'),
    'literales':           filtered.filter(t => ['NUM','STR','BOOL'].includes(t.type)),
    'operadores':          filtered.filter(t => OP_TYPES.has(t.type)),
    'delimitadores':       filtered.filter(t => DEL_TYPES.has(t.type)),
    'errores':             filtered.filter(t => t.type === 'ERROR'),
  }

  const tokStyle = (type) => {
    const cls = TK_CATS[type] || 't-del'
    const colors = {
      't-kw': 'var(--kw)', 't-id': 'var(--fn)', 't-num': 'var(--num)',
      't-str': 'var(--str)', 't-bool': 'var(--kw)', 't-err-tok': 'var(--err)',
    }
    return colors[cls] || 'var(--txt2)'
  }

  const tokBg = (type) => type === 'ERROR' ? '#FFF5F5' : 'var(--bg2)'
  const tokBorder = (type) => type === 'ERROR' ? '#FFAAAA' : 'var(--border)'

  return (
    <div style={S.tokenScroll}>
      <div style={{ fontSize:10, letterSpacing:'0.09em', color:'var(--txt3)', fontFamily:"'JetBrains Mono', monospace", marginBottom:8 }}>
        flujo completo de tokens
      </div>
      <div style={{ display:'flex', flexWrap:'wrap', gap:6 }}>
        {filtered.map((t, i) => {
          const lex = t.lex.length > 14 ? t.lex.slice(0,13) + '…' : t.lex
          return (
            <div key={i} style={{
              display:'inline-flex', flexDirection:'column', alignItems:'center',
              border:`1px solid ${tokBorder(t.type)}`,
              borderRadius:3, padding:'4px 8px 3px',
              background: tokBg(t.type), gap:1,
              fontFamily:"'JetBrains Mono', monospace",
            }}>
              <span style={{ fontSize:12.5, fontWeight:500, color: tokStyle(t.type) }}>{lex}</span>
              <span style={{ fontSize:9, color:'var(--txt3)', letterSpacing:'0.06em' }}>{t.type}</span>
              <span style={{ fontSize:9, color:'var(--txt3)' }}>{t.line}:{t.col}</span>
            </div>
          )
        })}
      </div>

      {Object.entries(groups).map(([label, toks]) => {
        if (toks.length === 0) return null
        return (
          <div key={label}>
            <SectionHd style={{ marginTop:14 }}>{label} ({toks.length})</SectionHd>
            <SemTbl>
              <thead>
                <tr>
                  {['lexema','tipo','línea','col'].map(h => (
                    <th key={h} style={{ textAlign:'left', color:'var(--txt3)', fontWeight:400, fontSize:10, padding:'4px 6px', borderBottom:'1px solid var(--border)', letterSpacing:'0.07em' }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {toks.map((t,i) => (
                  <tr key={i}>
                    {[t.lex, t.type, t.line, t.col].map((v,j) => (
                      <td key={j} style={{ padding:'5px 6px', color:'var(--txt)', borderBottom:'1px solid var(--bg3)' }}>{v}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </SemTbl>
          </div>
        )
      })}
    </div>
  )
}
