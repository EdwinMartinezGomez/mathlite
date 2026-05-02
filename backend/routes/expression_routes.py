"""
Rutas de expresiones — Endpoints FastAPI.
"""
from fastapi import APIRouter
from dtos import RunRequest
from controllers import ExpressionController

router = APIRouter(prefix='/api', tags=['expressions'])


@router.post('/run')
def run_program(req: RunRequest):
    """Ejecuta un programa MathLite."""
    return ExpressionController.run_program(req)


@router.get('/health')
def health():
    """Health check del servicio."""
    return ExpressionController.health()
