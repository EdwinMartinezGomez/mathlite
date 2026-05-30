"""
MathLite Análisis Semántico
Tabla de símbolos, inferencia de tipos y validaciones semánticas.
"""
from .lexer import BUILTINS


def analyze(ast: dict):
    """
    Recorre el AST, construye la tabla de símbolos y reporta errores semánticos.
    Retorna (symbols: list[dict], errors: list[dict])
    """
    errors  = []
    symbols = []
    scope   = 'global'
    in_func = False

    def add_sym(name, typ, line):
        existing = next((s for s in symbols if s['name'] == name and s['scope'] == scope), None)
        if existing:
            errors.append({'msg': f"'{name}' ya fue declarado en este alcance", 'line': line, 'phase': 'semántico'})
        else:
            symbols.append({'name': name, 'type': typ, 'scope': scope, 'line': line})

    def lookup(name):
        return next(
            (s for s in reversed(symbols) if s['name'] == name and s['scope'] in (scope, 'global')),
            None
        )

    def infer(node):
        if not node:
            return '?'
        t = node.get('type')

        if t == 'NumberNode':
            return 'Real' if isinstance(node['value'], float) and not node['value'].is_integer() else 'Int'
        if t == 'StringNode':  return 'String'
        if t == 'BoolNode':    return 'Bool'

        if t == 'VarNode':
            s = lookup(node['name'])
            if not s:
                errors.append({'msg': f"variable '{node['name']}' no declarada", 'line': node.get('line', 0), 'phase': 'semántico'})
                return '?'
            return s['type']

        if t == 'BinOp':
            op = node['op']
            lt = infer(node['left'])
            rt = infer(node['right'])
            if op in ('and', 'or'):   return 'Bool'
            if op in ('==', '!=', '<', '>', '<=', '>='): return 'Bool'
            if lt == 'String' or rt == 'String':
                if op != '+':
                    errors.append({
                        'msg': f"operación '{op}' inválida entre String y {rt if lt == 'String' else lt}",
                        'line': node['left'].get('line', 0),
                        'phase': 'semántico',
                    })
                return 'String'
            if lt in ('Int', 'Real') and rt in ('Int', 'Real'):
                return 'Real' if (lt == 'Real' or rt == 'Real') else 'Int'
            return '?'

        if t == 'UnaryOp':
            if node['op'] == 'not': return 'Bool'
            return infer(node['operand'])

        if t == 'FuncCall':
            if node['name'] in BUILTINS:
                for a in node.get('args', []): infer(a)
                return 'Real'
            fn = next((s for s in symbols if s['name'] == node['name'] and s['type'].startswith('func')), None)
            if not fn:
                errors.append({'msg': f"función '{node['name']}' no definida", 'line': node.get('line', 0), 'phase': 'semántico'})
                return '?'
            arity = int(fn['type'].split('/')[1])
            given = len(node.get('args', []))
            if given != arity:
                errors.append({
                    'msg': f"'{node['name']}' espera {arity} arg(s), se dieron {given}",
                    'line': node.get('line', 0),
                    'phase': 'semántico',
                })
            for a in node.get('args', []): infer(a)
            return '?'

        return '?'

    def walk_stmt(node):
        nonlocal scope, in_func
        if not node: return
        t = node.get('type')

        if t == 'LetDecl':
            typ = infer(node['value'])
            add_sym(node['name'], typ, node.get('line', 0))

        elif t == 'FuncDef':
            arity = len(node.get('params', []))
            add_sym(node['name'], f"func/{arity}", node.get('line', 0))
            prev_scope, prev_fn = scope, in_func
            scope  = node['name']
            in_func = True
            for p in node.get('params', []):
                symbols.append({'name': p, 'type': '?', 'scope': scope, 'line': node.get('line', 0)})
            walk_block(node['body'])
            scope  = prev_scope
            in_func = prev_fn

        elif t == 'IfStmt':
            typ = infer(node['cond'])
            if typ not in ('Bool', '?'):
                errors.append({'msg': 'condición de if debe ser booleana', 'line': node.get('line', 0), 'phase': 'semántico'})
            walk_block(node['then'])
            if node.get('alt'):
                if node['alt'].get('type') == 'IfStmt':
                    walk_stmt(node['alt'])
                else:
                    walk_block(node['alt'])

        elif t == 'WhileStmt':
            typ = infer(node['cond'])
            if typ not in ('Bool', '?'):
                errors.append({'msg': 'condición de while debe ser booleana', 'line': node.get('line', 0), 'phase': 'semántico'})
            walk_block(node['body'])

        elif t == 'ReturnStmt':
            if not in_func:
                errors.append({'msg': 'return fuera del cuerpo de una función', 'line': node.get('line', 0), 'phase': 'semántico'})
            infer(node['value'])

        elif t == 'PrintStmt':
            infer(node['value'])

        elif t == 'ExprStmt':
            infer(node.get('expr'))

    def walk_block(block):
        if not block: return
        for s in block.get('body', []):
            walk_stmt(s)

    for s in ast.get('body', []):
        walk_stmt(s)

    return symbols, errors
