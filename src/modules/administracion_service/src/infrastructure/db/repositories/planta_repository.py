from typing import Optional, List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.modules.administracion_service.src.application.ports.planta import IPlantaRepository
from src.modules.administracion_service.src.domain.entities import Planta
from src.modules.auth_service.src.infrastructure.db.models import PlantaORM
from src.shared.exceptions import NotFoundError, RepositoryError


class PlantaRepository(IPlantaRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: Optional[int]) -> Optional[Planta]:
        if id is None:
            return None

        try:
            planta_orm = (
                self.db.query(PlantaORM)
                .filter(PlantaORM.PLAN_ID == id)
                .first()
            )

            if planta_orm is None:
                return None  # si no existe la planta, devolvemos None

            return Planta(
                plan_id=planta_orm.PLAN_ID,
                plan_nombre=planta_orm.PLAN_NOMBRE,
                plan_estado=planta_orm.PLAN_ESTADO,
                plan_feccre=planta_orm.PLAN_FECCRE,
                plan_fecmod=planta_orm.PLAN_FECMOD
            )
        except SQLAlchemyError:
            raise RepositoryError("Error al consultar la existencia de la planta")

    def get_all(self) -> List[Planta]:
        try:
            planta_orm = (
                self.db.query(PlantaORM)
                .filter(PlantaORM.PLAN_ESTADO == "ACTIVO")
                .all()
            )

            return [
                Planta (
                    plan_id=p.PLAN_ID,
                    plan_nombre=p.PLAN_NOMBRE,
                    plan_estado=p.PLAN_ESTADO,
                    plan_feccre=p.PLAN_FECCRE,
                    plan_fecmod=p.PLAN_FECMOD
            )
                for p in planta_orm
            ]
        except SQLAlchemyError as e:
            raise RepositoryError("Error al obtener las plantas") from e
