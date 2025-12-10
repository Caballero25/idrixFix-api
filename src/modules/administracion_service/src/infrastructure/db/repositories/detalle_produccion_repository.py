from typing import Tuple, List, Optional

from sqlalchemy import func, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.modules.administracion_service.src.application.ports.detalle_produccion import IDetalleProduccionRepository
from src.modules.administracion_service.src.domain.entities import DetalleProduccion
from src.modules.administracion_service.src.infrastructure.api.schemas.detalle_produccion import (
    DetalleProduccionUpdate, DetalleProduccionPagination, DetalleProduccionFilters
)
from src.modules.administracion_service.src.infrastructure.db.models import DetalleProduccionORM
from src.shared.exceptions import RepositoryError, NotFoundError


class DetalleProduccionRepository(IDetalleProduccionRepository):
    def __init__(self, db: Session):
        self.db = db

    def _apply_filters(self, query, filters: DetalleProduccionFilters):
        conditions = []

        if filters.fecprod:
            conditions.append(DetalleProduccionORM.DPRO_FECPROD == filters.fecprod)

        if getattr(filters, "linea", None):
            conditions.append(DetalleProduccionORM.DPRO_LINEA == filters.linea)

        if getattr(filters, "lote", None):
            conditions.append(DetalleProduccionORM.DPRO_LOTE == filters.lote)

        if conditions:
            query = query.filter(and_(*conditions))
        return query

    def _count_by_filters(self, filters: DetalleProduccionFilters) -> int:
        try:
            query = self.db.query(func.count(DetalleProduccionORM.DPRO_ID))
            query = self._apply_filters(query, filters)
            return query.scalar() or 0
        except SQLAlchemyError as e:
            raise RepositoryError("Error al contar registros.") from e

    def exists_by_id(self, id: int) -> bool:
        try:
            return (
                self.db.query(DetalleProduccionORM.DPRO_ID)
                .filter(DetalleProduccionORM.DPRO_ID == id)
                .first()
            ) is not None
        except SQLAlchemyError as e:
            raise RepositoryError("Error al validar existencia.") from e

    def get_by_id(self, id: int) -> Optional[DetalleProduccion]:
        try:
            orm = (
                self.db.query(DetalleProduccionORM)
                .filter(DetalleProduccionORM.DPRO_ID == id)
                .first()
            )
            if not orm:
                return None

            return DetalleProduccion(
                dpro_id=orm.DPRO_ID,
                dpro_fecprod=orm.DPRO_FECPROD,
                dpro_lote=orm.DPRO_LOTE,
                dpro_pmiga=orm.DPRO_PMIGA,
                dpro_ppanza=orm.DPRO_PPANZA,
                dpro_pdesperdicio=orm.DPRO_PDESPERDICIO,
                dpro_linea=orm.DPRO_LINEA,
                dpro_turnox=orm.DPRO_TURNOX
            )
        except SQLAlchemyError as e:
            raise RepositoryError("Error al obtener registro.") from e

    def get_paginated_by_filters(self, paginated_filters: DetalleProduccionPagination) -> Tuple[List[DetalleProduccion], int]:
        filters = DetalleProduccionFilters(
            fecprod=paginated_filters.fecprod
        )

        try:
            total_records = self._count_by_filters(filters)
            if total_records == 0:
                return [], 0

            query = self.db.query(DetalleProduccionORM)
            query = self._apply_filters(query, filters)

            query = query.order_by(
                DetalleProduccionORM.DPRO_FECPROD.desc(),
                DetalleProduccionORM.DPRO_LINEA.asc()
            )

            offset = (paginated_filters.page - 1) * paginated_filters.page_size
            rows = query.limit(paginated_filters.page_size).offset(offset).all()

            entities = [
                DetalleProduccion(
                    dpro_id=r.DPRO_ID,
                    dpro_fecprod=r.DPRO_FECPROD,
                    dpro_lote=r.DPRO_LOTE,
                    dpro_pmiga=r.DPRO_PMIGA,
                    dpro_ppanza=r.DPRO_PPANZA,
                    dpro_pdesperdicio=r.DPRO_PDESPERDICIO,
                    dpro_linea=r.DPRO_LINEA,
                    dpro_turnox=r.DPRO_TURNOX
                )
                for r in rows
            ]

            return entities, total_records

        except SQLAlchemyError as e:
            raise RepositoryError("Error en paginación.") from e

    def update(self, id: int, data: DetalleProduccionUpdate) -> Optional[DetalleProduccion]:
        orm = self.db.query(DetalleProduccionORM).get(id)

        if not orm:
            raise NotFoundError("Registro no encontrado.")

        new_data = data.model_dump(exclude_unset=True)
        for k, v in new_data.items():
            setattr(orm, k.upper(), v)  # mapeo a columnas con mayúsculas

        try:
            self.db.commit()
            self.db.refresh(orm)
            return DetalleProduccion(
                dpro_id=orm.DPRO_ID,
                dpro_fecprod=orm.DPRO_FECPROD,
                dpro_lote=orm.DPRO_LOTE,
                dpro_pmiga=orm.DPRO_PMIGA,
                dpro_ppanza=orm.DPRO_PPANZA,
                dpro_pdesperdicio=orm.DPRO_PDESPERDICIO,
                dpro_linea=orm.DPRO_LINEA,
                dpro_turnox=orm.DPRO_TURNOX
            )
        except SQLAlchemyError:
            self.db.rollback()
            raise RepositoryError("Error al actualizar registro.")

    def remove(self, id: int) -> bool:
        orm = (
            self.db.query(DetalleProduccionORM)
            .filter(DetalleProduccionORM.DPRO_ID == id)
            .first()
        )

        if not orm:
            raise NotFoundError("Registro no encontrado.")

        try:
            self.db.delete(orm)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise RepositoryError("Error al eliminar registro.")
