"""
MathLite Intérprete — Evaluación del AST
Recorrido del árbol con entorno de ejecución mutable.
"""
import math

# ─── Funciones integradas ──────────────────────────────────────────────────────
_BUILTINS = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'sqrt': math.sqrt, 'log': math.log,
    'abs': abs, 'floor': math.floor, 'ceil': math.ceil,
}


class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


def format_val(v) -> str:
    """Convierte un valor Python al formato de salida MathLite."""
    if v is None:
        return 'null'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        # Hasta 6 decimales significativos
        s = f"{v:.6f}".rstrip('0').rstrip('.')
        return s
    return str(v)


class Interpreter:
    def __init__(self, ast: dict):
        self.ast       = ast
        self.global_env: dict = {}
        self.func_defs: dict  = {}
        self.errors:    list  = []
        self.output:    list  = []

        # Pre-cargar definiciones de funciones
        for node in ast.get('body', []):
            if node.get('type') == 'FuncDef':
                self.func_defs[node['name']] = node

    # ── API pública ────────────────────────────────────────────────────────────
    def run(self):
        for stmt in self.ast.get('body', []):
            try:
                if stmt.get('type') == 'WhileStmt':
                    self._exec_mut(stmt, self.global_env)
                else:
                    self._exec(stmt, self.global_env)
            except ReturnSignal:
                pass
            except Exception as e:
                self.errors.append({'msg': str(e), 'line': 0, 'phase': 'ejecución'})
                break
        return self.output, self.errors

    # ── Evaluación inmutable (para if/func) ────────────────────────────────────
    def _eval(self, node, env: dict):
        if node is None:
            return None
        t = node['type']

        if t == 'NumberNode': return node['value']
        if t == 'StringNode': return node['value']
        if t == 'BoolNode':   return node['value']

        if t == 'VarNode':
            name = node['name']
            if name in env:         return env[name]
            if name in self.global_env: return self.global_env[name]
            raise RuntimeError(f"variable '{name}' no definida (línea {node.get('line','?')})")

        if t == 'UnaryOp':
            v = self._eval(node['operand'], env)
            if node['op'] == '-':   return -v
            if node['op'] == 'not': return not v

        if t == 'BinOp':
            op = node['op']
            if op == 'and': return self._eval(node['left'], env) and self._eval(node['right'], env)
            if op == 'or':  return self._eval(node['left'], env) or  self._eval(node['right'], env)
            l = self._eval(node['left'],  env)
            r = self._eval(node['right'], env)
            return self._apply_op(op, l, r, node)

        if t == 'FuncCall':
            return self._call(node, env, mutable=False)

        return None

    # ── Evaluación mutable (para while) ───────────────────────────────────────
    def _eval_mut(self, node, env: dict):
        if node is None:
            return None
        t = node['type']

        if t == 'NumberNode': return node['value']
        if t == 'StringNode': return node['value']
        if t == 'BoolNode':   return node['value']

        if t == 'VarNode':
            name = node['name']
            if name in env:             return env[name]
            if name in self.global_env: return self.global_env[name]
            raise RuntimeError(f"variable '{name}' no definida (línea {node.get('line','?')})")

        if t == 'UnaryOp':
            v = self._eval_mut(node['operand'], env)
            if node['op'] == '-':   return -v
            if node['op'] == 'not': return not v

        if t == 'BinOp':
            op = node['op']
            if op == 'and': return self._eval_mut(node['left'], env) and self._eval_mut(node['right'], env)
            if op == 'or':  return self._eval_mut(node['left'], env) or  self._eval_mut(node['right'], env)
            l = self._eval_mut(node['left'],  env)
            r = self._eval_mut(node['right'], env)
            return self._apply_op(op, l, r, node)

        if t == 'FuncCall':
            return self._call(node, env, mutable=True)

        return None

    def _apply_op(self, op, l, r, node):
        if op == '+':  return l + r
        if op == '-':  return l - r
        if op == '*':  return l * r
        if op == '/':
            if r == 0:
                raise RuntimeError(f"división por cero (línea {node.get('line', node['left'].get('line','?'))})")
            return l / r
        if op == '%':  return l % r
        if op == '^':  return l ** r
        if op == '==': return l == r
        if op == '!=': return l != r
        if op == '<':  return l <  r
        if op == '>':  return l >  r
        if op == '<=': return l <= r
        if op == '>=': return l >= r
        return None

    def _call(self, node, env, mutable: bool):
        name = node['name']
        ev   = self._eval_mut if mutable else self._eval
        args = [ev(a, env) for a in node.get('args', [])]

        if name in _BUILTINS:
            return _BUILTINS[name](args[0])

        fn = self.func_defs.get(name)
        if not fn:
            raise RuntimeError(f"función '{name}' no definida (línea {node.get('line','?')})")
        if len(args) != len(fn['params']):
            raise RuntimeError(f"aridad incorrecta en '{name}'")

        local = dict(zip(fn['params'], args))
        try:
            self._exec_block(fn['body'], local)
        except ReturnSignal as rs:
            return rs.value
        return None

    # ── Ejecución inmutable ────────────────────────────────────────────────────
    def _exec(self, node, env: dict):
        if node is None: return
        t = node['type']

        if t == 'LetDecl':
            v = self._eval(node['value'], env)
            env[node['name']] = v
            if env is self.global_env:
                self.global_env[node['name']] = v

        elif t == 'FuncDef':
            self.func_defs[node['name']] = node

        elif t == 'PrintStmt':
            v = self._eval(node['value'], env)
            s = format_val(v)
            self.output.append(s)

        elif t == 'ReturnStmt':
            raise ReturnSignal(self._eval(node['value'], env))

        elif t == 'IfStmt':
            if self._eval(node['cond'], env):
                self._exec_block(node['then'], dict(env))
            elif node.get('alt'):
                alt = node['alt']
                if alt['type'] == 'IfStmt':
                    self._exec(alt, env)
                else:
                    self._exec_block(alt, dict(env))

        elif t == 'WhileStmt':
            self._exec_mut(node, env)   # while siempre mutable

        elif t == 'ExprStmt':
            self._eval(node.get('expr'), env)

    def _exec_block(self, block, env: dict):
        for s in block.get('body', []):
            self._exec(s, env)

    # ── Ejecución mutable (while) ──────────────────────────────────────────────
    def _exec_mut(self, node, env: dict):
        if node is None: return
        t = node['type']

        if t == 'LetDecl':
            env[node['name']] = self._eval_mut(node['value'], env)

        elif t == 'FuncDef':
            self.func_defs[node['name']] = node

        elif t == 'PrintStmt':
            v = self._eval_mut(node['value'], env)
            self.output.append(format_val(v))

        elif t == 'ReturnStmt':
            raise ReturnSignal(self._eval_mut(node['value'], env))

        elif t == 'IfStmt':
            if self._eval_mut(node['cond'], env):
                self._exec_block_mut(node['then'], dict(env))
            elif node.get('alt'):
                alt = node['alt']
                if alt['type'] == 'IfStmt':
                    self._exec_mut(alt, env)
                else:
                    self._exec_block_mut(alt, dict(env))

        elif t == 'WhileStmt':
            guard = 0
            while self._eval_mut(node['cond'], env):
                guard += 1
                if guard > 10_000:
                    raise RuntimeError('límite de iteraciones alcanzado (posible ciclo infinito)')
                self._exec_block_mut(node['body'], env)

        elif t == 'ExprStmt':
            self._eval_mut(node.get('expr'), env)

    def _exec_block_mut(self, block, env: dict):
        for s in block.get('body', []):
            self._exec_mut(s, env)
