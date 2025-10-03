from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import date, datetime

# Asumo que importas estas clases
from src.modules.management_service.src.domain.entities import WorkerMovement
from src.modules.management_service.src.infrastructure.api.schemas.movimientos_operario import (
    WorkerMovementCreate,
    WorkerMovementUpdate,
    WorkerMovementFilters
)

class IWorkerMovementRepository(ABC):
    """Puerto para la gestión de movimientos de operarios."""
    
    @abstractmethod
    def get_by_id(self, movement_id: int) -> Optional[WorkerMovement]:
        pass

    @abstractmethod
    def get_all_by_date(self, start_date: date, end_date: date) -> List[WorkerMovement]:
        pass
    
    @abstractmethod
    def create(self, movement_data: WorkerMovementCreate) -> WorkerMovement:
        pass
        
    @abstractmethod
    def update(
        self, movement_id: int, movement_data: WorkerMovementUpdate
    ) -> Optional[WorkerMovement]:
        pass
    
    @abstractmethod
    def delete(self, movement_id: int) -> bool:
        pass
    @abstractmethod
    def count_by_filters(self, filters: WorkerMovementFilters) -> int:
        """Cuenta el total de registros WorkerMovement según los filtros."""
        pass
    
    @abstractmethod
    def get_paginated_by_filters(
        self, filters: WorkerMovementFilters, page: int, page_size: int
    ) -> Tuple[List[WorkerMovement], int]:
        """Obtiene una página de registros WorkerMovement y el conteo total."""
        pass