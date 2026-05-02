/**
 * AnalysisPanel — Muestra análisis léxico, sintáctico y semántico en 3 columnas.
 */
import SectionHd from './common/SectionHd'
import SemTbl from './common/SemTbl'
import ChkItem from './common/ChkItem'
import { S } from '../styles/appStyles'

export default function AnalysisPanel({ tokens, symbols, errors }) {
  const KW_TYPES = new Set(['LET','DEF','IF','ELSE','WHILE','RETURN','PRINT','AND','OR','NOT'])
  const OP_TYPES = new Set(['+','-','*','/','%','^','==','!=','<','>','<=','>=','='])
  const DEL_TYPES = new Set(['(',')','{','}',',',';'])

  const counts = {}
  tokens.forEach(t => { if(t.type!=='EOF') counts[t.type]=(counts[t.type]||0)+1 })

  const cats = [
    ['palabras reservadas', [...KW_TYPES]],
    ['identificadores',     ['ID']],
    ['números',             ['NUM']],
    ['cadenas',             ['STR']],
    ['booleanos',           ['BOOL']],
    ['operadores',          [...OP_TYPES]],
    ['delimitadores',       [...DEL_TYPES]],
    ['errores léxicos',     ['ERROR']],
  ]

  const lexErrors = errors.filter(e => e.phase === 'léxico')
  const synErrors = errors.filter(e => e.phase === 'sintáctico')
  const semErrors = errors.filter(e => e.phase === 'semántico')
  const runErrors = errors.filter(e => e.phase === 'ejecución')

  const thStyle = { textAlign:'left', color:'var(--txt3)', fontWeight:400, fontSize:10, padding:'4px 6px', borderBottom:'1px solid var(--border)', letterSpacing:'0.07em' }
  const tdStyle = { padding:'5px 6px', color:'var(--txt)', borderBottom:'1px solid var(--bg3)' }

  return (
    <div style={S.analysisCols}>
      {/* LEX */}
      <div style={S.aCol}>
        <div style={S.aColHead}><b>léxico</b> — categorías</div>
        <div style={S.aColScroll}>
          {tokens.length === 0 ? (
            <div style={{ ...S.empty, height:100 }}>ejecuta primero</div>
          ) : (
            <>
              <SectionHd style={{ marginTop:0 }}>resumen de categorías</SectionHd>
              <SemTbl>
                <thead><tr><th style={thStyle}>categoría</th><th style={thStyle}>cantidad</th></tr></thead>
                <tbody>
                  {cats.map(([lbl, types]) => {
                    const n = types.reduce((s,t)=>s+(counts[t]||0),0)
                    if (n===0 && lbl!=='errores léxicos') return null
                    return (
                      <tr key={lbl}>
                        <td style={tdStyle}>{lbl}</td>
                        <td style={{ ...tdStyle, color: lbl==='errores léxicos'&&n>0?'var(--err)':undefined }}>{n}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </SemTbl>
              <SectionHd style={{ marginTop:12 }}>estado</SectionHd>
              <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
                {lexErrors.length>0
                  ? lexErrors.map((e,i) => <ChkItem key={i} status="err" text={`línea ${e.line}: ${e.msg}`} />)
                  : <ChkItem status="ok" text="sin errores léxicos" />
                }
              </div>
            </>
          )}
        </div>
      </div>

      {/* SYN */}
      <div style={S.aCol}>
        <div style={S.aColHead}><b>sintáctico</b> — gramática</div>
        <div style={S.aColScroll}>
          <SectionHd style={{ marginTop:0 }}>gramática BNF (fragmento)</SectionHd>
          <div style={{ background:'var(--bg2)', border:'1px solid var(--border)', borderRadius:3, padding:10, fontFamily:"'JetBrains Mono', monospace", fontSize:11, lineHeight:2, color:'var(--txt)' }}>
            <span style={{color:'var(--fn)'}}>prog</span>   ::= stmt*{'\n'}
            <span style={{color:'var(--fn)'}}>stmt</span>   ::= letDecl | funcDef{'\n'}
            {'             '}| ifStmt | whileStmt{'\n'}
            <span style={{color:'var(--fn)'}}>expr</span>   ::= term ((+|-) term)*{'\n'}
            <span style={{color:'var(--fn)'}}>term</span>   ::= power ((*|/) power)*{'\n'}
            <span style={{color:'var(--fn)'}}>power</span>  ::= unary (^ unary)*{'\n'}
            <span style={{color:'var(--fn)'}}>unary</span>  ::= - unary | atom{'\n'}
            <span style={{color:'var(--fn)'}}>atom</span>   ::= NUM | STR | BOOL{'\n'}
            {'             '}| ID | call | (expr)
          </div>
          <SectionHd style={{ marginTop:14 }}>precedencia de operadores</SectionHd>
          <table style={{ width:'100%', borderCollapse:'collapse', fontSize:11, fontFamily:"'JetBrains Mono', monospace" }}>
            <tbody>
              {[['or','baja'],['and',''],['not',''],['== != < > <= >=',''],['+ -',''],['* / %',''],['^ (derecha)',''],['- (unario)','alta']].map(([op,note])=>(
                <tr key={op}>
                  <td style={{ padding:'4px 6px', borderBottom:'1px solid var(--bg3)', color:'var(--op)' }}>{op}</td>
                  <td style={{ padding:'4px 6px', borderBottom:'1px solid var(--bg3)', color:'var(--txt3)', textAlign:'right' }}>{note}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <SectionHd style={{ marginTop:14 }}>verificaciones</SectionHd>
          <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
            {synErrors.length > 0
              ? synErrors.map((e,i) => <ChkItem key={i} status="err" text={`línea ${e.line}: ${e.msg}`} />)
              : tokens.length > 0 ? <>
                  <ChkItem status="ok" text="gramática válida" />
                  <ChkItem status="ok" text="llaves y paréntesis balanceados" />
                  <ChkItem status="ok" text="AST construido correctamente" />
                </> : <ChkItem status="ok" text="ejecuta para verificar" />
            }
          </div>
        </div>
      </div>

      {/* SEM */}
      <div style={{ ...S.aCol, borderRight:'none' }}>
        <div style={S.aColHead}><b>semántico</b> — tabla de símbolos</div>
        <div style={S.aColScroll}>
          {symbols.length === 0 ? (
            <div style={{ ...S.empty, height:80 }}>ejecuta primero</div>
          ) : (
            <>
              <SectionHd style={{ marginTop:0 }}>tabla de símbolos</SectionHd>
              <SemTbl>
                <thead><tr>
                  {['nombre','tipo','alcance'].map(h=>(
                    <th key={h} style={thStyle}>{h}</th>
                  ))}
                </tr></thead>
                <tbody>
                  {symbols.map((s,i)=>(
                    <tr key={i}>
                      <td style={tdStyle}>{s.name}</td>
                      <td style={tdStyle}>{s.type}</td>
                      <td style={tdStyle}>{s.scope}</td>
                    </tr>
                  ))}
                </tbody>
              </SemTbl>
              <SectionHd style={{ marginTop:12 }}>estado semántico</SectionHd>
              <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
                {semErrors.length > 0
                  ? semErrors.map((e,i) => <ChkItem key={i} status="err" text={`línea ${e.line}: ${e.msg}`} />)
                  : <><ChkItem status="ok" text="tipos consistentes" /><ChkItem status="ok" text="variables declaradas correctamente" /></>
                }
              </div>
              {runErrors.length > 0 && (
                <>
                  <SectionHd style={{ marginTop:12 }}>errores de ejecución</SectionHd>
                  <div style={{ display:'flex', flexDirection:'column', gap:5 }}>
                    {runErrors.map((e,i) => <ChkItem key={i} status="err" text={e.msg} />)}
                  </div>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
