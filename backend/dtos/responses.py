"""
DTOs de salida — Esquemas de respuesta.
"""
from pydantic import BaseModel
from typing import Any


class RunResponse(BaseModel):
    """Estructura de respuesta de POST /api/run."""
    tokens:       list[dict[str, Any]]
    ast:          dict[str, Any]
    ast_text:     str
    ast_markdown: str
    ast_visual:   str
    node_count:   int
    symbols:      list[dict[str, Any]]
    output:       list[str]
    errors:       list[dict[str, Any]]
    lex_errors:   list[dict[str, Any]]
    syn_errors:   list[dict[str, Any]]
    sem_errors:   list[dict[str, Any]]
    run_errors:   list[dict[str, Any]]
