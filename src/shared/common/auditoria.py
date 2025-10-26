## INICIO BLOQUE DE AUDITORIA
from fastapi import Depends
from sqlalchemy.orm import Session
from src.modules.auth_service.src.application.use_cases.audit_use_case import AuditUseCase
from src.modules.auth_service.src.infrastructure.db.repositories.auditoria_log_repository import AuditoriaLogRepository
from src.modules.auth_service.src.infrastructure.db.repositories.usuario_repository import UsuarioRepository
from src.shared.base import get_auth_db
def get_audit_use_case(
    db_auth: Session = Depends(get_auth_db)
) -> AuditUseCase:
    """Dependencia para el caso de uso de Auditoría"""
    return AuditUseCase(
        log_repository=AuditoriaLogRepository(db_auth),
        user_repository=UsuarioRepository(db_auth)
    )
