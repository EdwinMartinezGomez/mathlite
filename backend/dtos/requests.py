"""
DTOs de entrada — Esquemas de petición.
"""
from pydantic import BaseModel


class RunRequest(BaseModel):
    """Cuerpo de la petición POST /api/run."""
    code: str
