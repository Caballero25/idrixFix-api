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
    elif isinstance(exc, RepositoryError):
        return error_response("Error en la base de datos", status_code=500)
    else:
        return error_response("Error interno en el servidor", status_code=500)
