/**
 * Utilidades y helpers del frontend MathLite.
 */

/**
 * Escapa HTML para prevenir XSS.
 */
export function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/**
 * Mapa de tipo de token → clase CSS para coloreado.
 */
export const TK_CATS = {
  LET:'t-kw', DEF:'t-kw', IF:'t-kw', ELSE:'t-kw', WHILE:'t-kw',
  RETURN:'t-kw', PRINT:'t-kw', AND:'t-kw', OR:'t-kw', NOT:'t-kw',
  ID:'t-id', NUM:'t-num', STR:'t-str', BOOL:'t-bool', ERROR:'t-err-tok',
}
