"""
MathLite AST Printer — Visualización del árbol en múltiples formatos
  - print_ast:          texto indentado con líneas unicode (original)
  - print_ast_markdown: Markdown jerárquico con listas indentadas
  - print_ast_visual:   árbol visual tipo binario para expresiones
"""


def print_ast(node, indent='', last=True) -> str:
    """Genera una representación textual del AST (formato árbol de texto)."""
    if not node:
        return ''

    branch = indent + ('└─ ' if last else '├─ ')
    child  = indent + ('   ' if last else '│  ')
    t = node.get('type', '?')
    out = ''

    if t == 'Program':
        out = 'Program\n'
        for i, n in enumerate(node.get('body', [])):
            out += print_ast(n, child, i == len(node['body']) - 1)

    elif t == 'LetDecl':
        out = branch + f"let {node['name']}\n"
        out += print_ast(node.get('value'), child, True)

    elif t == 'FuncDef':
        params = ', '.join(node.get('params', []))
        out = branch + f"def {node['name']}({params})\n"
        out += print_ast(node.get('body'), child, True)

    elif t == 'Block':
        body = node.get('body', [])
        out = branch + f"Block[{len(body)}]\n"
        for i, n in enumerate(body):
            out += print_ast(n, child, i == len(body) - 1)

    elif t == 'IfStmt':
        out = branch + 'if\n'
        has_alt = bool(node.get('alt'))
        out += print_ast(node.get('cond'), child, False)
        out += print_ast(node.get('then'), child, not has_alt)
        if has_alt:
            out += print_ast(node['alt'], child, True)

    elif t == 'WhileStmt':
        out = branch + 'while\n'
        out += print_ast(node.get('cond'), child, False)
        out += print_ast(node.get('body'), child, True)

    elif t == 'ReturnStmt':
        out = branch + 'return\n'
        out += print_ast(node.get('value'), child, True)

    elif t == 'PrintStmt':
        out = branch + 'print\n'
        out += print_ast(node.get('value'), child, True)

    elif t == 'ExprStmt':
        out = print_ast(node.get('expr'), indent, last)

    elif t == 'BinOp':
        out = branch + f"{node['op']}\n"
        out += print_ast(node.get('left'),  child, False)
        out += print_ast(node.get('right'), child, True)

    elif t == 'UnaryOp':
        out = branch + f"{node['op']} (unario)\n"
        out += print_ast(node.get('operand'), child, True)

    elif t == 'FuncCall':
        args = node.get('args', [])
        out = branch + f"{node['name']}({len(args)} args)\n"
        for i, a in enumerate(args):
            out += print_ast(a, child, i == len(args) - 1)

    elif t == 'NumberNode':
        out = branch + f"{node['value']}\n"

    elif t == 'StringNode':
        out = branch + f'"{node["value"]}"\n'

    elif t == 'BoolNode':
        out = branch + f"{str(node['value']).lower()}\n"

    elif t == 'VarNode':
        out = branch + f"{node['name']}\n"

    else:
        out = branch + t + '\n'

    return out


def count_nodes(node) -> int:
    if not node:
        return 0
    count = 1
    for v in node.values():
        if isinstance(v, dict) and 'type' in v:
            count += count_nodes(v)
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict) and 'type' in item:
                    count += count_nodes(item)
    return count


# ─── Fase 6: Nuevos formatos de visualización ─────────────────────────────────

def _node_label(node) -> str:
    """Genera la etiqueta de un nodo para los formatos markdown y visual."""
    if not node:
        return '?'
    t = node.get('type', '?')
    if t == 'Program':     return 'Program'
    if t == 'LetDecl':     return f"LetDecl ({node['name']})"
    if t == 'FuncDef':     return f"FuncDef ({node['name']})"
    if t == 'Block':       return f"Block[{len(node.get('body', []))}]"
    if t == 'IfStmt':      return 'IfStmt'
    if t == 'WhileStmt':   return 'WhileStmt'
    if t == 'ReturnStmt':  return 'ReturnStmt'
    if t == 'PrintStmt':   return 'PrintStmt'
    if t == 'ExprStmt':    return 'ExprStmt'
    if t == 'BinOp':       return f"BinOp ({node['op']})"
    if t == 'UnaryOp':     return f"UnaryOp ({node['op']})"
    if t == 'FuncCall':    return f"FuncCall ({node['name']})"
    if t == 'NumberNode':  return f"Number ({node['value']})"
    if t == 'StringNode':  return f'String ("{node["value"]}")'
    if t == 'BoolNode':    return f"Bool ({str(node['value']).lower()})"
    if t == 'VarNode':     return f"Var ({node['name']})"
    return t


def _get_children(node) -> list:
    """Retorna la lista de nodos hijos de un nodo AST."""
    if not node:
        return []
    t = node.get('type', '?')
    children = []

    if t == 'Program':
        children = node.get('body', [])
    elif t == 'LetDecl':
        if node.get('value'): children.append(node['value'])
    elif t == 'FuncDef':
        if node.get('body'): children.append(node['body'])
    elif t == 'Block':
        children = node.get('body', [])
    elif t == 'IfStmt':
        if node.get('cond'): children.append(node['cond'])
        if node.get('then'): children.append(node['then'])
        if node.get('alt'):  children.append(node['alt'])
    elif t == 'WhileStmt':
        if node.get('cond'): children.append(node['cond'])
        if node.get('body'): children.append(node['body'])
    elif t == 'ReturnStmt':
        if node.get('value'): children.append(node['value'])
    elif t == 'PrintStmt':
        if node.get('value'): children.append(node['value'])
    elif t == 'ExprStmt':
        if node.get('expr'): children.append(node['expr'])
    elif t == 'BinOp':
        if node.get('left'):  children.append(node['left'])
        if node.get('right'): children.append(node['right'])
    elif t == 'UnaryOp':
        if node.get('operand'): children.append(node['operand'])
    elif t == 'FuncCall':
        children = node.get('args', [])

    return children


def print_ast_markdown(node, indent=0) -> str:
    """
    Genera representación Markdown jerárquica con listas indentadas.
    Ejemplo:
      - **BinOp** (`+`)
        - **Number** (`3`)
        - **Number** (`5`)
    """
    if not node:
        return ''

    t = node.get('type', '?')
    prefix = '  ' * indent + '- '
    out = ''

    # Para ExprStmt, saltar directamente al hijo
    if t == 'ExprStmt':
        return print_ast_markdown(node.get('expr'), indent)

    label = _node_label(node)
    out = prefix + f"**{label}**\n"

    for child in _get_children(node):
        out += print_ast_markdown(child, indent + 1)

    return out


def print_ast_visual(node) -> str:
    """
    Genera un árbol visual tipo binario para expresiones.
    Ejemplo para 3 + 5:
        +
       / \\
      3   5
    """
    if not node:
        return ''

    lines, _, _, _ = _build_visual(node)
    return '\n'.join(lines)


def _visual_label(node) -> str:
    """Etiqueta corta para el árbol visual."""
    if not node:
        return '?'
    t = node.get('type', '?')
    if t == 'NumberNode':  return str(node['value'])
    if t == 'StringNode':  return f'"{node["value"]}"'
    if t == 'BoolNode':    return str(node['value']).lower()
    if t == 'VarNode':     return node['name']
    if t == 'BinOp':       return node['op']
    if t == 'UnaryOp':     return node['op']
    if t == 'FuncCall':    return f"{node['name']}()"
    if t == 'LetDecl':     return f"let {node['name']}"
    if t == 'PrintStmt':   return 'print'
    if t == 'ReturnStmt':  return 'return'
    if t == 'IfStmt':      return 'if'
    if t == 'WhileStmt':   return 'while'
    if t == 'Block':       return 'Block'
    if t == 'FuncDef':     return f"def {node['name']}"
    if t == 'Program':     return 'Program'
    if t == 'ExprStmt':
        return _visual_label(node.get('expr'))
    return t


def _build_visual(node):
    """
    Construye líneas para el árbol visual.
    Retorna (lines, width, center, height).
    """
    if not node:
        return ['?'], 1, 0, 1

    t = node.get('type', '?')

    # ExprStmt: saltar al hijo
    if t == 'ExprStmt':
        return _build_visual(node.get('expr'))

    label = _visual_label(node)
    children = _get_children(node)

    # Nodo hoja
    if not children:
        return [label], len(label), len(label) // 2, 1

    # Un solo hijo
    if len(children) == 1:
        child_lines, cw, cc, ch = _build_visual(children[0])
        lw = len(label)
        w = max(lw, cw)

        # Centrar label
        label_pad = (w - lw) // 2
        line0 = ' ' * label_pad + label + ' ' * (w - label_pad - lw)

        # Centrar pipe
        pipe_pos = label_pad + lw // 2
        line1 = ' ' * pipe_pos + '|' + ' ' * (w - pipe_pos - 1)

        # Centrar hijo
        child_pad = (w - cw) // 2
        result = [line0, line1]
        for cl in child_lines:
            result.append(' ' * child_pad + cl + ' ' * (w - child_pad - len(cl)))

        center = label_pad + lw // 2
        return result, w, center, ch + 2

    # Dos hijos (caso binario más común)
    if len(children) == 2:
        ll, lw, lc, lh = _build_visual(children[0])
        rl, rw, rc, rh = _build_visual(children[1])

        gap = 3
        lw_label = len(label)

        total_w = lw + gap + rw
        total_w = max(total_w, lw_label + 2)

        # Posiciones de los subárboles
        left_start = 0
        right_start = lw + gap

        # Centro del label
        label_center = (left_start + lc + right_start + rc) // 2
        label_pad = max(0, label_center - lw_label // 2)

        line0 = ' ' * label_pad + label
        w = max(total_w, label_pad + lw_label)

        # Líneas de conexión / \
        slash_pos = left_start + lc + 1
        backslash_pos = right_start + rc - 1
        if backslash_pos <= slash_pos:
            backslash_pos = slash_pos + 2

        line1 = [' '] * w
        line1_mid = (slash_pos + backslash_pos) // 2
        for p in range(slash_pos, line1_mid + 1):
            if p < w:
                line1[p] = '/'
                break
        for p in range(backslash_pos, line1_mid, -1):
            if p < w:
                line1[p] = '\\'
                break

        conn = ' ' * max(0, slash_pos) + '/' + ' ' * max(0, backslash_pos - slash_pos - 1) + '\\'
        conn = conn.ljust(w)

        # Combinar hijos línea por línea
        max_h = max(lh, rh)
        result = [line0.ljust(w), conn]
        for i in range(max_h):
            left_line = ll[i] if i < lh else ''
            right_line = rl[i] if i < rh else ''
            combined = left_line.ljust(lw) + ' ' * gap + right_line
            result.append(combined.ljust(w))

        return result, w, label_center, max_h + 2

    # Más de 2 hijos: usar formato lista simple
    lines = [label]
    for i, child in enumerate(children):
        cl, cw, cc, ch = _build_visual(child)
        prefix = '├─ ' if i < len(children) - 1 else '└─ '
        cont   = '│  ' if i < len(children) - 1 else '   '
        for j, line in enumerate(cl):
            if j == 0:
                lines.append(prefix + line)
            else:
                lines.append(cont + line)

    max_w = max(len(l) for l in lines)
    return lines, max_w, max_w // 2, len(lines)
