"""
Configuración centralizada de CORS para todos los microservicios.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings


def configure_cors(app: FastAPI, service_name: str = "API") -> None:
    """
    Configura CORS para una aplicación FastAPI usando las variables de entorno.

    Args:
        app: Instancia de FastAPI
        service_name: Nombre del servicio para los logs
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.cors_methods_list,
        allow_headers=settings.cors_headers_list,
    )

    # Log de configuración CORS
    print(f"[{service_name}] CORS configurado:")
    print(f"  - Orígenes: {settings.cors_origins_list}")
    print(f"  - Métodos: {settings.cors_methods_list}")
    print(f"  - Headers: {settings.cors_headers_list}")
    print(f"  - Credenciales: {settings.CORS_ALLOW_CREDENTIALS}")


def get_cors_config() -> dict:
    """
    Retorna la configuración CORS como diccionario para uso manual.

    Returns:
        dict: Configuración CORS
    """
    return {
        "allow_origins": settings.cors_origins_list,
        "allow_credentials": settings.CORS_ALLOW_CREDENTIALS,
        "allow_methods": settings.cors_methods_list,
        "allow_headers": settings.cors_headers_list,
    }
