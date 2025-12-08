from abc import ABC, abstractmethod
from typing import Optional, List

from src.modules.administracion_service.src.domain.entities import Planta


class IPlantaRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Planta]:
        pass

    @abstractmethod
    def get_all(self) ->List[Planta]:
        pass