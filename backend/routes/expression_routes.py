"""
Rutas de expresiones — Endpoints FastAPI.
"""
from fastapi import APIRouter, HTTPException
from dtos import RunRequest
from controllers import ExpressionController
from services.testcase_service import list_tests

router = APIRouter(prefix='/api', tags=['expressions'])


@router.post('/run')
def run_program(req: RunRequest):
    """Ejecuta un programa MathLite."""
    return ExpressionController.run_program(req)


@router.get('/health')
def health():
    """Health check del servicio."""
    return ExpressionController.health()


@router.get('/tests')
def get_tests():
    """Devuelve los casos de prueba guardados en MongoDB."""
    try:
        return list_tests()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
