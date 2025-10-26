from typing import List, Optional, Dict, Any # <-- Añadido Dict y Any
from datetime import date, datetime
from math import ceil
from src.shared.exceptions import NotFoundError

# Importar el puerto y los schemas
from src.modules.management_service.src.application.ports.movimientos_operario import (
    IWorkerMovementRepository, IRefMotivoRepository, IRefDestinoMotivoRepository
)
from src.modules.management_service.src.infrastructure.api.schemas.movimientos_operario import (
    WorkerMovementCreate,
    WorkerMovementUpdate,
    WorkerMovementPagination,
    WorkerMovementFilters,
    WorkerMovementPaginatedResponse,
    WorkerMovementResponse, # Aunque Use Case retorna la entidad, la importo por contexto
    RefMotivoPagination, 
    RefDestinoMotivoPagination, 
    RefMotivoFilters, 
    RefDestinoMotivoFilters

)
from src.modules.management_service.src.domain.entities import WorkerMovement, RefMotivo, RefDestinoMotivo


# Importar el CASO DE USO de auditoría del otro módulo
from src.modules.auth_service.src.application.use_cases.audit_use_case import AuditUseCase

class WorkerMovementUseCases:
    def __init__(self, repository: IWorkerMovementRepository, audit_use_case: AuditUseCase):
        self.repository = repository
        self.audit_use_case = audit_use_case
    def get_movement_by_id(self, movement_id: int) -> Optional[WorkerMovement]:
        return self.repository.get_by_id(movement_id)

    def get_movements_by_date_range(
        self, start_date: date, end_date: date
    ) -> List[WorkerMovement]:
        return self.repository.get_all_by_date(start_date, end_date)

    def create_movement(self, movement_data: WorkerMovementCreate, user_data: Dict[str, Any]) -> WorkerMovement:
        new_movement = self.repository.create(movement_data)
        self.audit_use_case.log_action(
            accion="CREATE",
            user_id=user_data.get("user_id"),
            modelo="WorkerMovementORM",
            entidad_id=new_movement.id,
            datos_nuevos=movement_data.model_dump(mode="json")
        )
        return new_movement

    def update_movement(
            self, 
            movement_id: int, 
            movement_data: WorkerMovementUpdate,
            user_data: Dict[str, Any] # <-- Nuevo
        ) -> Optional[WorkerMovement]:
            
            # 1. Obtener datos "antes" (desde la entidad de dominio)
            old_movement_entity = self.repository.get_by_id(movement_id)
            if not old_movement_entity:
                raise NotFoundError(f"Movimiento con id={movement_id} no encontrado.")
            
            # Convertir entidad de dataclass a dict para el log
            datos_anteriores = WorkerMovementResponse.model_validate(old_movement_entity).model_dump(mode="json")
            
            # 2. Actualizar el registro
            updated_movement = self.repository.update(movement_id, movement_data)

            # 3. Registrar en auditoría
            self.audit_use_case.log_action(
                accion="UPDATE",
                user_id=user_data.get("user_id"),
                modelo="WorkerMovementORM",
                entidad_id=movement_id,
                datos_nuevos=movement_data.model_dump(exclude_unset=True, mode="json"),
                datos_anteriores=datos_anteriores
            )
            
            # 4. Retornar
            return updated_movement

    def delete_movement(self, movement_id: int, user_data: Dict[str, Any]) -> bool:
        old_movement_entity = self.repository.get_by_id(movement_id)
        if not old_movement_entity:
            raise NotFoundError(f"Movimiento con id={movement_id} no encontrado.")
        datos_anteriores = WorkerMovementResponse.model_validate(old_movement_entity).model_dump(mode="json")
        delete_movement = self.repository.delete(movement_id)

        self.audit_use_case.log_action(
            accion="DELETE",
            user_id=user_data.get("user_id"),
            modelo="WorkerMovementORM",
            entidad_id=movement_id,
            datos_anteriores=datos_anteriores
        )
        return delete_movement

    def count_movements_by_filters(
        self, filters: WorkerMovementFilters, allowed_lines: List[int]
    ) -> int:
        """Caso de uso para contar movimientos, filtrado por líneas permitidas."""

        if not allowed_lines:
            return 0
            
        allowed_lines_str = [str(line_id) for line_id in allowed_lines]

        return self.repository.count_by_filters(filters, allowed_lines_str)

    def get_movements_paginated_by_filters(
        self, filters: WorkerMovementPagination, allowed_lines: List[int]
    ) -> WorkerMovementPaginatedResponse:
        """Caso de uso para obtener movimientos paginados con metadatos, filtrado por líneas permitidas."""
        
        if not allowed_lines:
            return {
                "total_records": 0,
                "total_pages": 0,
                "page": filters.page,
                "page_size": filters.page_size,
                "data": [],
            }
        
        allowed_lines_str = [str(line_id) for line_id in allowed_lines]

        data, total_records = self.repository.get_paginated_by_filters(
            filters=filters, 
            page=filters.page, 
            page_size=filters.page_size,
            allowed_lines=allowed_lines_str  # <-- Nuevo argumento
        )
        
        total_pages = ceil(total_records / filters.page_size) if total_records > 0 else 0

        return {
            "total_records": total_records,
            "total_pages": total_pages,
            "page": filters.page,
            "page_size": filters.page_size,
            "data": data, # Lista de entidades de dominio
        }

class RefMotivoUseCases:
    def __init__(self, repository: IRefMotivoRepository):
        self.repository = repository
        
    def count_active_motives(self, filters: RefMotivoFilters) -> int:
        """Cuenta el total de motivos activos (el filtro ACTIVO es implícito en el repo)."""
        _, total_records = self.repository.get_paginated_active(page=1, page_size=1)
        return total_records

    def get_active_paginated_motives(self, pagination_params: RefMotivoPagination) -> List[RefMotivo]:
        """Obtiene una lista de motivos activos paginados (solo data)."""
        
        data, _ = self.repository.get_paginated_active(
            page=pagination_params.page, 
            page_size=pagination_params.page_size
        )
        # Solo retornamos la lista de entidades
        return data


class RefDestinoMotivoUseCases:
    def __init__(self, repository: IRefDestinoMotivoRepository):
        self.repository = repository
        
    def count_destinations_by_motivo(self, filters: RefDestinoMotivoFilters) -> int:
        """Cuenta el total de destinos asociados a un id_motivo específico."""
        # Obtenemos el total de registros usando una paginación mínima.
        _, total_records = self.repository.get_paginated_by_motivo(
            id_motivo=filters.id_motivo, 
            page=1, 
            page_size=1
        )
        return total_records

    def get_destinations_paginated_by_motivo(self, pagination_params: RefDestinoMotivoPagination) -> List[RefDestinoMotivo]:
        """Obtiene una lista de destinos paginados por ID de motivo (solo data)."""

        data, _ = self.repository.get_paginated_by_motivo(
            id_motivo=pagination_params.id_motivo, 
            page=pagination_params.page, 
            page_size=pagination_params.page_size
        )
        # Solo retornamos la lista de entidades
        return data