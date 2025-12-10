from math import ceil
from typing import Optional

from src.modules.administracion_service.src.application.ports.detalle_produccion import IDetalleProduccionRepository
from src.modules.administracion_service.src.domain.entities import DetalleProduccion
from src.modules.administracion_service.src.infrastructure.api.schemas.detalle_produccion import (
    DetalleProduccionPagination, DetalleProduccionUpdate
)
from src.shared.exceptions import NotFoundError


class DetalleProduccionUseCase:
    def __init__(self, repo: IDetalleProduccionRepository):
        self.repo = repo

    def get_paginated_by_filters(self, pagination: DetalleProduccionPagination):
        data, total_records = self.repo.get_paginated_by_filters(pagination)

        total_pages = ceil(total_records / pagination.page_size) if total_records > 0 else 0

        return {
            "total_records": total_records,
            "total_pages": total_pages,
            "page": pagination.page,
            "page_size": pagination.page_size,
            "data": data
        }

    def get_by_id(self, id: int) -> Optional[DetalleProduccion]:
        record = self.repo.get_by_id(id)
        if not record:
            raise NotFoundError("El registro no existe")
        return record

    def update(self, id: int, data: DetalleProduccionUpdate) -> DetalleProduccion:
        if not self.repo.exists_by_id(id):
            raise NotFoundError("No existe el registro")
        return self.repo.update(id, data)

    def remove(self, id: int) -> bool:
        if not self.repo.exists_by_id(id):
            raise NotFoundError("No existe el registro")
        return self.repo.remove(id)
