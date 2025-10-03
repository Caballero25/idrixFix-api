# use_cases.py (Añadir las siguientes importaciones y la clase)
from typing import List, Optional
from datetime import date, datetime
from math import ceil

# Importar el puerto y los schemas
from src.modules.management_service.src.application.ports.movimientos_operario import (
    IWorkerMovementRepository,
)
from src.modules.management_service.src.infrastructure.api.schemas.movimientos_operario import (
    WorkerMovementCreate,
    WorkerMovementUpdate,
    WorkerMovementPagination,
    WorkerMovementFilters,
    WorkerMovementPaginatedResponse,
    WorkerMovementResponse, # Aunque Use Case retorna la entidad, la importo por contexto
)
from src.modules.management_service.src.domain.entities import WorkerMovement


class WorkerMovementUseCases:
    def __init__(self, repository: IWorkerMovementRepository):
        self.repository = repository

    def get_movement_by_id(self, movement_id: int) -> Optional[WorkerMovement]:
        # El caso de uso puede aplicar lógica de negocio (e.g., permisos) antes de llamar al repositorio
        return self.repository.get_by_id(movement_id)

    def get_movements_by_date_range(
        self, start_date: date, end_date: date
    ) -> List[WorkerMovement]:
        # Aquí podría ir una validación de rango de fechas
        return self.repository.get_all_by_date(start_date, end_date)

    def create_movement(self, movement_data: WorkerMovementCreate) -> WorkerMovement:
        # Aquí se podría validar la entidad de dominio si fuera más compleja
        return self.repository.create(movement_data)

    def update_movement(
        self, movement_id: int, movement_data: WorkerMovementUpdate
    ) -> Optional[WorkerMovement]:
        # Aquí podría ir lógica de negocio: ¿quién puede actualizar un movimiento?
        return self.repository.update(movement_id, movement_data)

    def delete_movement(self, movement_id: int) -> bool:
        # Se elimina permanentemente, no hay soft delete en este modelo
        return self.repository.delete(movement_id)
    
    def count_movements_by_filters(self, filters: WorkerMovementFilters) -> int:
        """Caso de uso para contar movimientos."""
        return self.repository.count_by_filters(filters)
    def get_movements_paginated_by_filters(
        self, filters: WorkerMovementPagination
    ) -> WorkerMovementPaginatedResponse:
        """Caso de uso para obtener movimientos paginados con metadatos."""
        
        data, total_records = self.repository.get_paginated_by_filters(
            filters=filters, page=filters.page, page_size=filters.page_size
        )
        
        total_pages = ceil(total_records / filters.page_size) if total_records > 0 else 0

        # Retornamos un DTO con la información de paginación
        return {
            "total_records": total_records,
            "total_pages": total_pages,
            "page": filters.page,
            "page_size": filters.page_size,
            "data": data, # Lista de entidades de dominio
        }