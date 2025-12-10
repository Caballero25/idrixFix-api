from abc import ABC, abstractmethod
from typing import Optional, Tuple, List

from src.modules.administracion_service.src.domain.entities import DetalleProduccion
from src.modules.administracion_service.src.infrastructure.api.schemas.detalle_produccion import \
    DetalleProduccionUpdate, DetalleProduccionPagination


class IDetalleProduccionRepository(ABC):
    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[DetalleProduccion]:
        pass

    @abstractmethod
    def update(self, id: int, detalle: DetalleProduccionUpdate) -> DetalleProduccion:
        pass

    @abstractmethod
    def remove(self, id: int) -> bool:
        pass

    @abstractmethod
    def get_paginated_by_filters(self, pagination: DetalleProduccionPagination) -> Tuple[List[DetalleProduccion], int]:
        pass
