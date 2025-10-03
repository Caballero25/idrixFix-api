# repositories.py (Añadir las siguientes importaciones y la clase)
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func, and_
from datetime import date, datetime
from typing import List, Optional, Tuple

# Importaciones de los modelos, entidades, schemas y puertos
from src.modules.management_service.src.infrastructure.db.models import WorkerMovementORM
from src.modules.management_service.src.domain.entities import WorkerMovement
from src.modules.management_service.src.infrastructure.api.schemas.movimientos_operario import (
    WorkerMovementCreate,
    WorkerMovementUpdate,
    WorkerMovementFilters
)
from src.modules.management_service.src.application.ports.movimientos_operario import (
    IWorkerMovementRepository,
)

# Importar las excepciones de tu capa de aplicación
from src.shared.exceptions import AlreadyExistsError, NotFoundError, RepositoryError


class WorkerMovementRepository(IWorkerMovementRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain_entity(self, orm_model: WorkerMovementORM) -> WorkerMovement:
        """Mapea un objeto ORM a una entidad de Dominio."""
        return WorkerMovement(
            id=orm_model.id,
            linea=orm_model.linea,
            fecha_p=orm_model.fecha_p,
            tipo_movimiento=orm_model.tipo_movimiento,
            motivo=orm_model.motivo,
            codigo_operario=orm_model.codigo_operario,
            destino=orm_model.destino,
            hora=orm_model.hora,
            observacion=orm_model.observacion,
        )

    def get_by_id(self, movement_id: int) -> Optional[WorkerMovement]:
        try:
            movement_orm = (
                self.db.query(WorkerMovementORM)
                .filter(WorkerMovementORM.id == movement_id)
                .first()
            )
            if not movement_orm:
                return None
            return self._to_domain_entity(movement_orm)
        except SQLAlchemyError as e:
            raise RepositoryError("Error al consultar el movimiento.") from e

    def get_all_by_date(self, start_date: date, end_date: date) -> List[WorkerMovement]:
        try:
            orm_list = (
                self.db.query(WorkerMovementORM)
                .filter(
                    WorkerMovementORM.fecha_p >= start_date,
                    WorkerMovementORM.fecha_p <= end_date,
                )
                .order_by(WorkerMovementORM.fecha_p.desc())
                .all()
            )
            return [self._to_domain_entity(orm) for orm in orm_list]
        except SQLAlchemyError as e:
            raise RepositoryError("Error al obtener los movimientos.") from e

    def create(self, movement_data: WorkerMovementCreate) -> WorkerMovement:
        try:
            # Pydantic V2: usa model_dump()
            new_movement_orm = WorkerMovementORM(**movement_data.model_dump())
            self.db.add(new_movement_orm)
            self.db.commit()
            self.db.refresh(new_movement_orm)
            return self._to_domain_entity(new_movement_orm)
        except IntegrityError as e:
            self.db.rollback()
            raise RepositoryError("Ya existe un movimiento con esas características.") from e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Error en la base de datos al crear el movimiento.") from e

    def update(
        self, movement_id: int, movement_data: WorkerMovementUpdate
    ) -> Optional[WorkerMovement]:
        movement_orm = self.db.query(WorkerMovementORM).get(movement_id)
        if not movement_orm:
            raise NotFoundError(f"Movimiento con id={movement_id} no encontrado.")
            
        update_data = movement_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(movement_orm, key, value)
            
        try:
            self.db.commit()
            self.db.refresh(movement_orm)
            return self._to_domain_entity(movement_orm)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Error al actualizar el movimiento.") from e

    def delete(self, movement_id: int) -> bool:
        movement_orm = self.db.query(WorkerMovementORM).get(movement_id)
        if not movement_orm:
            raise NotFoundError(f"Movimiento con id={movement_id} no encontrado.")
        
        try:
            self.db.delete(movement_orm)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("No se pudo eliminar el movimiento.") from e
    def _apply_filters(self, query, filters: WorkerMovementFilters):
        """Función auxiliar para aplicar filtros comunes a consultas de conteo y selección."""
        conditions = []
        
        # Filtro por rango de fecha_p
        if filters.fecha_inicial and filters.fecha_final:
            conditions.append(
                WorkerMovementORM.fecha_p.between(filters.fecha_inicial, filters.fecha_final)
            )
        
        # Filtro por codigo_operario
        if filters.codigo_operario:
            conditions.append(
                WorkerMovementORM.codigo_operario == filters.codigo_operario
            )
        
        if conditions:
            query = query.filter(and_(*conditions))
            
        return query

    def count_by_filters(self, filters: WorkerMovementFilters) -> int:
        try:
            query = self.db.query(WorkerMovementORM)
            query = self._apply_filters(query, filters)
            
            # Usar count() en SQLAlchemy
            return query.count()
        except SQLAlchemyError as e:
            raise RepositoryError("Error al contar los movimientos por filtros.") from e

    def get_paginated_by_filters(
        self, filters: WorkerMovementFilters, page: int, page_size: int
    ) -> Tuple[List[WorkerMovement], int]:
        try:
            base_query = self.db.query(WorkerMovementORM)
            
            # 1. Obtener el conteo total con los filtros
            count_query = self._apply_filters(base_query.session.query(func.count(WorkerMovementORM.id)), filters)
            total_records = count_query.scalar()
            
            if total_records == 0:
                return [], 0
            
            # 2. Aplicar filtros, paginación y ordenamiento para los datos
            data_query = self._apply_filters(base_query, filters)
            
            # Ordenar por hora/fecha para paginación consistente (asumiendo descendente como en tu ejemplo)
            data_query = data_query.order_by(WorkerMovementORM.fecha_p.desc(), WorkerMovementORM.hora.desc())
            
            # Aplicar paginación
            offset = (page - 1) * page_size
            data_query = data_query.limit(page_size).offset(offset)
            
            orm_list = data_query.all()
            
            domain_entities = [self._to_domain_entity(orm) for orm in orm_list]
            
            return domain_entities, total_records
        except SQLAlchemyError as e:
            raise RepositoryError("Error al obtener movimientos paginados.") from e