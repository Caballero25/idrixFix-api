from fastapi import Request
from src.shared.exceptions import (
    DomainError,
    NotFoundError,
    AlreadyExistsError,
    ValidationError,
    RepositoryError,
)
from src.shared.common.responses import error_response


async def domain_exception_handler(request: Request, exc: DomainError):
    if isinstance(exc, NotFoundError):
        return error_response(str(exc), status_code=404)
    elif isinstance(exc, AlreadyExistsError):
        return error_response(str(exc), status_code=400)
    elif isinstance(exc, ValidationError):
        return error_response(str(exc), status_code=422)
    if isinstance(exc, RepositoryError):
        response_data = {
            "error": "Error en la base de datos",
            "status_code": 500
        }
        
        if True:
            response_data["debug_info"] = {
                "message": str(exc),
                "exception_type": exc.__class__.__name__,
                "traceback": getattr(exc, "__traceback__", None)
            }
        
        return error_response(str(response_data), response_data['status_code'])
    else:
        return error_response("Error interno en el servidor", status_code=500)
