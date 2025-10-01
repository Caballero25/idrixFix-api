# repositories.py (Añadir las siguientes importaciones y la clase)
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import func
from datetime import date, datetime
from typing import List, Optional

# Importaciones de los modelos, entidades, schemas y puertos
from src.modules.management_service.src.infrastructure.db.models import WorkerMovementORM
from src.modules.management_service.src.domain.entities import WorkerMovement
from src.modules.management_service.src.infrastructure.api.schemas.movimientos_operario import (
    WorkerMovementCreate,
    WorkerMovementUpdate,
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