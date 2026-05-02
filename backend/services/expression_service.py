"""
Servicio de expresiones — Orquesta el pipeline completo del intérprete MathLite.

Flujo: código fuente → lexer → parser → semantic → interpreter → ast_printer → resultado
"""
from core import tokenize, TK, parse, analyze, Interpreter
from core import print_ast, print_ast_markdown, print_ast_visual, count_nodes


class ExpressionService:
    """Orquesta las fases del compilador/intérprete MathLite."""

    @staticmethod
    def execute(code: str) -> dict:
        """
        Ejecuta el pipeline completo de MathLite sobre el código fuente.
        Retorna un diccionario con tokens, AST, símbolos, salida y errores.
        """
        # ── Fase 1: Análisis Léxico ──────────────────────────────────────────
        tokens, lex_errors = tokenize(code)

        # ── Fase 2: Análisis Sintáctico ─────────────────────────────────────
        filtered = [t for t in tokens if t['type'] != TK.ERROR]
        ast, syn_errors = parse(filtered)

        # ── Fase 3: Análisis Semántico ──────────────────────────────────────
        symbols, sem_errors = analyze(ast)

        # ── Fase 4: Interpretación ──────────────────────────────────────────
        interp = Interpreter(ast)
        output, run_errors = interp.run()

        # ── Visualización del AST ───────────────────────────────────────────
        ast_text     = print_ast(ast)
        ast_markdown = print_ast_markdown(ast)
        ast_visual   = print_ast_visual(ast)
        node_count   = count_nodes(ast)

        all_errors = lex_errors + syn_errors + sem_errors + run_errors

        return {
            'tokens':       tokens,
            'ast':          ast,
            'ast_text':     ast_text,
            'ast_markdown': ast_markdown,
            'ast_visual':   ast_visual,
            'node_count':   node_count,
            'symbols':      symbols,
            'output':       output,
            'errors':       all_errors,
            'lex_errors':   lex_errors,
            'syn_errors':   syn_errors,
            'sem_errors':   sem_errors,
            'run_errors':   run_errors,
        }
