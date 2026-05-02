"""
MathLite Lexer — Análisis Léxico
Tokeniza el código fuente en una secuencia de tokens con posición (línea, columna).
"""

# ─── Tipos de Token ────────────────────────────────────────────────────────────
class TK:
    NUM     = 'NUM';    STR    = 'STR';    BOOL   = 'BOOL';  ID     = 'ID'
    LET     = 'LET';    DEF    = 'DEF';    IF     = 'IF';    ELSE   = 'ELSE'
    WHILE   = 'WHILE';  RETURN = 'RETURN'; PRINT  = 'PRINT'; AND    = 'AND'
    OR      = 'OR';     NOT    = 'NOT'
    PLUS    = '+';      MINUS  = '-';      STAR   = '*';     SLASH  = '/'
    PERCENT = '%';      CARET  = '^'
    EQ      = '==';     NEQ    = '!=';     LT     = '<';     GT     = '>'
    LE      = '<=';     GE     = '>='
    ASSIGN  = '=';      LPAREN = '(';      RPAREN = ')'
    LBRACE  = '{';      RBRACE = '}';      COMMA  = ',';     SEMI   = ';'
    EOF     = 'EOF';    ERROR  = 'ERROR'

KEYWORDS = {
    'let': TK.LET,  'def': TK.DEF,   'if': TK.IF,    'else': TK.ELSE,
    'while': TK.WHILE, 'return': TK.RETURN, 'print': TK.PRINT,
    'and': TK.AND,  'or': TK.OR,     'not': TK.NOT,
    'true': TK.BOOL, 'false': TK.BOOL,
}

BUILTINS = {'sin', 'cos', 'tan', 'sqrt', 'log', 'abs', 'floor', 'ceil'}

SIMPLE_OPS = {
    '=': TK.ASSIGN, '+': TK.PLUS, '-': TK.MINUS, '*': TK.STAR,
    '/': TK.SLASH,  '%': TK.PERCENT, '^': TK.CARET,
    '(': TK.LPAREN, ')': TK.RPAREN, '{': TK.LBRACE, '}': TK.RBRACE,
    ',': TK.COMMA,  '<': TK.LT, '>': TK.GT, ';': TK.SEMI,
}


def tokenize(src: str):
    """
    Convierte el código fuente en una lista de tokens.
    Retorna (tokens: list[dict], errors: list[dict])
    """
    tokens = []
    errors = []
    i = 0
    line = 1
    col  = 1

    def peek(off=0):
        idx = i + off
        return src[idx] if idx < len(src) else ''

    def advance():
        nonlocal i, line, col
        ch = src[i]; i += 1
        if ch == '\n':
            line += 1; col = 1
        else:
            col += 1
        return ch

    def mk(typ, lex, l, c):
        return {'type': typ, 'lex': lex, 'line': l, 'col': c}

    while i < len(src):
        l, c, ch = line, col, src[i]

        # ── Espacios en blanco
        if ch in ' \t\r\n':
            advance(); continue

        # ── Comentarios de línea  --
        if ch == '-' and peek(1) == '-':
            while i < len(src) and src[i] != '\n':
                advance()
            continue

        # ── Cadenas  "..."
        if ch == '"':
            advance(); s = ''
            while i < len(src) and src[i] != '"' and src[i] != '\n':
                s += advance()
            if i >= len(src) or src[i] == '\n':
                errors.append({'msg': 'cadena sin cerrar', 'line': l, 'col': c, 'phase': 'léxico'})
            else:
                advance()  # comilla de cierre
            tokens.append(mk(TK.STR, f'"{s}"', l, c))
            continue

        # ── Números
        if ch.isdigit():
            n = ''
            while i < len(src) and src[i].isdigit():
                n += advance()
            if i < len(src) and src[i] == '.' and i+1 < len(src) and src[i+1].isdigit():
                n += advance()
                while i < len(src) and src[i].isdigit():
                    n += advance()
            tokens.append(mk(TK.NUM, n, l, c))
            continue

        # ── Identificadores / palabras reservadas
        if ch.isalpha() or ch == '_':
            id_str = ''
            while i < len(src) and (src[i].isalnum() or src[i] == '_'):
                id_str += advance()
            kw = KEYWORDS.get(id_str)
            tokens.append(mk(kw or TK.ID, id_str, l, c))
            continue

        # ── Operadores de dos caracteres
        two = ch + peek(1)
        two_ops = {'==': TK.EQ, '!=': TK.NEQ, '<=': TK.LE, '>=': TK.GE}
        if two in two_ops:
            advance(); advance()
            tokens.append(mk(two_ops[two], two, l, c))
            continue

        # ── Operadores / delimitadores simples
        if ch in SIMPLE_OPS:
            advance()
            tokens.append(mk(SIMPLE_OPS[ch], ch, l, c))
            continue

        # ── Error léxico
        errors.append({'msg': f"carácter inválido '{ch}'", 'line': l, 'col': c, 'phase': 'léxico'})
        advance()
        tokens.append(mk(TK.ERROR, ch, l, c))

    tokens.append(mk(TK.EOF, 'EOF', line, col))
    return tokens, errors
