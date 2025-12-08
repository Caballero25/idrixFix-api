from typing import List

from src.modules.administracion_service.src.application.ports.planta import IPlantaRepository
from src.modules.administracion_service.src.domain.entities import Planta


class PlantaUseCase:
    def __init__(self, planta_repository: IPlantaRepository):
        self.planta_repository = planta_repository

    def get_all_plantas(self) -> List[Planta]:
        return self.planta_repository.get_all()