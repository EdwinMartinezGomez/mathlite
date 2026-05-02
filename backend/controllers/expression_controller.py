"""
Controlador de expresiones — Recibe peticiones y delega al servicio.
"""
from dtos import RunRequest
from services import ExpressionService


class ExpressionController:
    """Controlador que recibe la entrada y retorna el resultado."""

    @staticmethod
    def run_program(req: RunRequest) -> dict:
        """Ejecuta un programa MathLite y retorna los resultados."""
        return ExpressionService.execute(req.code)

    @staticmethod
    def health() -> dict:
        """Verifica que el servicio esté activo."""
        return {'status': 'ok', 'service': 'MathLite API'}
