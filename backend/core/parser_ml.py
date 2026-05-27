"""
MathLite Parser — Análisis Sintáctico
Parser recursivo descendente (LL(1)) que construye el AST.
"""
from .lexer import TK


def parse(tokens: list):
    """
    Construye el AST a partir de la lista de tokens.
    Retorna (ast: dict, errors: list[dict])
    """
    pos = 0
    errors = []

    # ── Helpers ────────────────────────────────────────────────────────────────
    def cur():
        return tokens[pos] if pos < len(tokens) else {'type': TK.EOF, 'lex': 'EOF', 'line': 0, 'col': 0}

    def peek(off=1):
        idx = pos + off
        return tokens[idx] if idx < len(tokens) else {'type': TK.EOF}

    def eat(typ):
        nonlocal pos
        if cur()['type'] == typ:
            t = tokens[pos]; pos += 1; return t
        t = cur()
        errors.append({
            'msg': f"se esperaba '{typ}' pero se encontró '{t['lex']}'",
            'line': t['line'], 'col': t['col'], 'phase': 'sintáctico'
        })
        return None

    def match(*types):
        nonlocal pos
        if cur()['type'] in types:
            t = tokens[pos]; pos += 1; return t
        return None

    def check(*types):
        return cur()['type'] in types

    # ── Gramática ──────────────────────────────────────────────────────────────
    def parse_program():
        stmts = []
        while not check(TK.EOF):
            try:
                s = parse_stmt()
                if s:
                    stmts.append(s)
            except Exception as e:
                errors.append({'msg': str(e), 'line': cur()['line'], 'col': cur()['col'], 'phase': 'sintáctico'})
                # recuperación de errores: avanzar hasta fin de línea o delimitador
                start_line = cur()['line']
                while not check(TK.EOF) and not check(TK.SEMI) and not check(TK.RBRACE):
                    if cur()['line'] != start_line:
                        break
                    nonlocal pos  # noqa: F821
                    pos += 1
                match(TK.SEMI)
        return {'type': 'Program', 'body': stmts}

    def parse_stmt():
        match(TK.SEMI)  # semicolons opcionales
        if check(TK.LET):    return parse_let()
        if check(TK.DEF):    return parse_def()
        if check(TK.IF):     return parse_if()
        if check(TK.WHILE):  return parse_while()
        if check(TK.RETURN): return parse_return()
        if check(TK.PRINT):  return parse_print()
        e = parse_expr()
        match(TK.SEMI)
        return {'type': 'ExprStmt', 'expr': e}

    def parse_let():
        t = eat(TK.LET)
        name_tok = eat(TK.ID)
        eat(TK.ASSIGN)
        val = parse_expr()
        match(TK.SEMI)
        return {
            'type': 'LetDecl',
            'name': name_tok['lex'] if name_tok else '?',
            'value': val,
            'line': t['line'] if t else 0,
        }

    def parse_def():
        t = eat(TK.DEF)
        name_tok = eat(TK.ID)
        eat(TK.LPAREN)
        params = []
        if not check(TK.RPAREN):
            p = eat(TK.ID)
            if p: params.append(p['lex'])
            while match(TK.COMMA):
                p = eat(TK.ID)
                if p: params.append(p['lex'])
        eat(TK.RPAREN)
        body = parse_block()
        return {
            'type': 'FuncDef',
            'name': name_tok['lex'] if name_tok else '?',
            'params': params,
            'body': body,
            'line': t['line'] if t else 0,
        }

    def parse_if():
        t = eat(TK.IF)
        if check(TK.LBRACE):
            errors.append({'msg': 'falta condición en if', 'line': t['line'] if t else 0, 'col': t['col'] if t and 'col' in t else 0, 'phase': 'sintáctico'})
            cond = {'type': 'BoolNode', 'value': False, 'line': t['line'] if t else 0}
        else:
            cond = parse_expr()
            if not check(TK.LBRACE):
                errors.append({'msg': 'se esperaba { después de condición if', 'line': t['line'] if t else 0, 'col': 0, 'phase': 'sintáctico'})
        then = parse_block()
        alt = None
        if match(TK.ELSE):
            alt = parse_if() if check(TK.IF) else parse_block()
        return {'type': 'IfStmt', 'cond': cond, 'then': then, 'alt': alt, 'line': t['line'] if t else 0}

    def parse_while():
        t = eat(TK.WHILE)
        cond = parse_expr()
        body = parse_block()
        return {'type': 'WhileStmt', 'cond': cond, 'body': body, 'line': t['line'] if t else 0}

    def parse_return():
        t = eat(TK.RETURN)
        val = parse_expr()
        match(TK.SEMI)
        return {'type': 'ReturnStmt', 'value': val, 'line': t['line'] if t else 0}

    def parse_print():
        t = eat(TK.PRINT)
        eat(TK.LPAREN)
        val = parse_expr()
        eat(TK.RPAREN)
        match(TK.SEMI)
        return {'type': 'PrintStmt', 'value': val, 'line': t['line'] if t else 0}

    def parse_block():
        eat(TK.LBRACE)
        stmts = []
        while not check(TK.RBRACE) and not check(TK.EOF):
            try:
                s = parse_stmt()
                if s: stmts.append(s)
            except Exception as e:
                errors.append({'msg': str(e), 'line': cur()['line'], 'col': cur()['col'], 'phase': 'sintáctico'})
                nonlocal pos  # noqa
                pos += 1
        eat(TK.RBRACE)
        return {'type': 'Block', 'body': stmts}

    # ── Expresiones (por precedencia ascendente) ───────────────────────────────
    def parse_expr():  return parse_or()

    def parse_or():
        l = parse_and()
        while match(TK.OR):
            r = parse_and()
            l = {'type': 'BinOp', 'op': 'or', 'left': l, 'right': r}
        return l

    def parse_and():
        l = parse_not()
        while match(TK.AND):
            r = parse_not()
            l = {'type': 'BinOp', 'op': 'and', 'left': l, 'right': r}
        return l

    def parse_not():
        if match(TK.NOT):
            return {'type': 'UnaryOp', 'op': 'not', 'operand': parse_not()}
        return parse_compare()

    def parse_compare():
        nonlocal pos
        l = parse_add()
        while check(TK.EQ, TK.NEQ, TK.LT, TK.GT, TK.LE, TK.GE):
            op = tokens[pos]['lex']; pos += 1
            r = parse_add()
            l = {'type': 'BinOp', 'op': op, 'left': l, 'right': r}
        return l

    def parse_add():
        nonlocal pos
        l = parse_mul()
        while check(TK.PLUS, TK.MINUS):
            op = tokens[pos]['lex']; pos += 1
            r = parse_mul()
            l = {'type': 'BinOp', 'op': op, 'left': l, 'right': r}
        return l

    def parse_mul():
        nonlocal pos
        l = parse_pow()
        while check(TK.STAR, TK.SLASH, TK.PERCENT):
            op = tokens[pos]['lex']; pos += 1
            r = parse_pow()
            l = {'type': 'BinOp', 'op': op, 'left': l, 'right': r}
        return l

    def parse_pow():
        b = parse_unary()
        if match(TK.CARET):
            e = parse_pow()  # asociatividad derecha
            return {'type': 'BinOp', 'op': '^', 'left': b, 'right': e}
        return b

    def parse_unary():
        if match(TK.MINUS):
            return {'type': 'UnaryOp', 'op': '-', 'operand': parse_unary()}
        return parse_atom()

    def parse_atom():
        nonlocal pos
        t = cur()
        # Número
        if match(TK.NUM):
            raw = t['lex']
            val = float(raw) if '.' in raw else int(raw)
            return {'type': 'NumberNode', 'value': val, 'raw': raw, 'line': t['line']}
        # Cadena
        if match(TK.STR):
            return {'type': 'StringNode', 'value': t['lex'][1:-1], 'line': t['line']}
        # Booleano
        if match(TK.BOOL):
            return {'type': 'BoolNode', 'value': t['lex'] == 'true', 'line': t['line']}
        # Llamada a función
        if check(TK.ID) and peek().get('type') == TK.LPAREN:
            name = tokens[pos]['lex']; pos += 1
            eat(TK.LPAREN)
            args = []
            if not check(TK.RPAREN):
                args.append(parse_expr())
                while match(TK.COMMA):
                    args.append(parse_expr())
            eat(TK.RPAREN)
            return {'type': 'FuncCall', 'name': name, 'args': args, 'line': t['line']}
        # Identificador
        if match(TK.ID):
            return {'type': 'VarNode', 'name': t['lex'], 'line': t['line']}
        # Agrupación
        if match(TK.LPAREN):
            e = parse_expr()
            eat(TK.RPAREN)
            return e
        raise Exception(f"expresión inesperada '{t['lex']}' en línea {t['line']}")

    ast = parse_program()
    return ast, errors
