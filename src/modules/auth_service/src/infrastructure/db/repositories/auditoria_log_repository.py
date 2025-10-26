from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any
from src.modules.auth_service.src.application.ports.auditoria_log_repository import IAuditoriaLogRepository
from src.modules.auth_service.src.infrastructure.db.models import AuditoriaLogORM
from src.shared.exceptions import RepositoryError

class AuditoriaLogRepository(IAuditoriaLogRepository):
    
    def __init__(self, db: Session):
        self.db = db # Esta es la sesión de la DB interna (auth)

    def create_log(self, log_data: Dict[str, Any]) -> bool:
        """
        Crea un nuevo registro de log en la base de datos.
        'log_data' es un diccionario que coincide con las columnas de AuditoriaLogORM.
        """
        try:
            db_log = AuditoriaLogORM(**log_data)
            self.db.add(db_log)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            # Loguear este error es importante, pero no deberíamos
            # fallar la petición principal del usuario si el log falla.
            print(f"Error al escribir en log de auditoría: {e}")
            return False