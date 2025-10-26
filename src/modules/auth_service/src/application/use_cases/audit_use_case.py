from typing import Dict, Any, Optional
from src.modules.auth_service.src.application.ports.auditoria_log_repository import IAuditoriaLogRepository
from src.modules.auth_service.src.application.ports.usuarios import IUsuarioRepository
from src.modules.auth_service.src.infrastructure.api.schemas.usuarios import UsuarioResponse

class AuditUseCase:
    
    def __init__(
        self, 
        log_repository: IAuditoriaLogRepository,
        user_repository: IUsuarioRepository
    ):
        self.log_repository = log_repository
        self.user_repository = user_repository

    def _get_user_snapshot(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un snapshot JSON simple del usuario que realiza la acción."""
        try:
            # Usamos el repositorio de usuarios para obtener el objeto
            usuario = self.user_repository.get_by_id(user_id)
            if usuario:
                # Usamos el schema 'UsuarioResponse' para convertirlo a un JSON limpio
                return UsuarioResponse.model_validate(usuario).model_dump(mode="json")
        except Exception:
            return None # No fallar si el usuario no se encuentra

    def log_action(
        self,
        accion: str,
        user_id: int,
        modelo: str,
        entidad_id: str,
        datos_nuevos: Optional[Dict[str, Any]] = None,
        datos_anteriores: Optional[Dict[str, Any]] = None
    ):
        """
        Método principal para registrar una acción de auditoría.
        """
        # Obtenemos el snapshot del usuario
        user_snapshot = self._get_user_snapshot(user_id)
        
        log_data = {
            "modelo": modelo,
            "entidad_id": str(entidad_id),
            "accion": accion,
            "datos_anteriores": datos_anteriores,
            "datos_nuevos": datos_nuevos,
            "ejecutado_por_id": user_id,
            "ejecutado_por_json": user_snapshot
        }
        
        # Enviamos a la base de datos
        self.log_repository.create_log(log_data)