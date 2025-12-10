from datetime import datetime
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.modules.administracion_service.src.application.ports.lineas import ILineaRepository
from src.modules.administracion_service.src.domain.entities import Linea
from src.modules.administracion_service.src.infrastructure.api.schemas.linea import LineaCreate, LineaUpdate, \
    EstadoLineaEnum
from src.modules.auth_service.src.infrastructure.db.models import LineaORM
from src.shared.exceptions import RepositoryError, NotFoundError


class LineaRepository(ILineaRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Linea]:
        try:
            linea_orm = (
                self.db.query(LineaORM)
                .filter(LineaORM.LINE_ESTADO == "ACTIVO")
                .all()
            )

            return [
                Linea(
                    line_id=l.LINE_ID,
                    line_nombre=l.LINE_NOMBRE,
                    line_estado=l.LINE_ESTADO,
                    line_feccre=l.LINE_FECCRE,
                    line_fecmod=l.LINE_FECMOD,
                    line_planta=l.LINE_PLANTA
                )
                for l in linea_orm
            ]
        except SQLAlchemyError as e:
            raise RepositoryError("Error al obtener las lineas") from e

    def get_by_id(self, id: int) -> Optional[Linea]:
        try:
            linea_orm = (
                self.db.query(LineaORM)
                .filter(LineaORM.LINE_ID == id)
                .first()
            )

            if linea_orm is None:
                raise RepositoryError("Error al obtener linea")

            return Linea(
                line_id=linea_orm.LINE_ID,
                line_nombre=linea_orm.LINE_NOMBRE,
                line_estado=linea_orm.LINE_ESTADO,
                line_feccre=linea_orm.LINE_FECCRE,
                line_fecmod=linea_orm.LINE_FECMOD,
                line_planta=linea_orm.LINE_PLANTA
            )

        except SQLAlchemyError as e:
            raise RepositoryError("Error al obtener la linea") from e

    def exists_by_nombre(self, nombre: str) -> bool:
        try:
            linea_orm = (
                self.db.query(LineaORM)
                .filter(LineaORM.LINE_NOMBRE == nombre)
                .first()
            )

            return linea_orm is not None
        except SQLAlchemyError as e:
            raise RepositoryError("Error al consultar existencia de la linea.")

    def exists_by_id(self, id: int) -> bool:
        try:
            linea_orm = (
                self.db.query(LineaORM)
                .filter(LineaORM.LINE_ID == id)
                .first()
            )

            return linea_orm is not None
        except SQLAlchemyError as e:
            raise RepositoryError("Error al consultar existencia de la linea.") from e

    def create(self, data: LineaCreate) -> Linea:
        try:
            linea_orm = LineaORM(
                LINE_NOMBRE=data.line_nombre,
                LINE_PLANTA=data.line_planta
            )

            self.db.add(linea_orm)
            self.db.commit()
            self.db.refresh(linea_orm)
            return Linea(
                line_id=linea_orm.LINE_ID,
                line_nombre=linea_orm.LINE_NOMBRE,
                line_estado=linea_orm.LINE_ESTADO,
                line_feccre=linea_orm.LINE_FECCRE,
                line_fecmod=linea_orm.LINE_FECMOD,
                line_planta=linea_orm.LINE_PLANTA
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Error al crear la linea.") from e

    def update(self, data: LineaUpdate, id: int) -> Optional[Linea]:
        linea_orm = self.db.query(LineaORM).get(id)
        if linea_orm is None:
            raise NotFoundError("La linea no existe")

        if data.line_nombre is not None:
            linea_orm.LINE_NOMBRE = data.line_nombre

        if data.line_planta is not None:
            linea_orm.LINE_PLANTA = data.line_planta

        linea_orm.LINE_FECMOD = datetime.now()

        try:
            self.db.commit()
            self.db.refresh(linea_orm)
            return Linea(
                line_id=linea_orm.LINE_ID,
                line_nombre=linea_orm.LINE_NOMBRE,
                line_estado=linea_orm.LINE_ESTADO,
                line_feccre=linea_orm.LINE_FECCRE,
                line_fecmod=linea_orm.LINE_FECMOD,
                line_planta=linea_orm.LINE_PLANTA
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Error al actualizar la linea.") from e

    def soft_delete(self, id: int) -> bool:
        linea_orm = self.db.query(LineaORM).get(id)
        try:
            linea_orm.LINE_ESTADO = EstadoLineaEnum.INACTIVO
            self.db.commit()
            self.db.refresh(linea_orm)

            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RepositoryError("Error al eliminar la linea.") from e
