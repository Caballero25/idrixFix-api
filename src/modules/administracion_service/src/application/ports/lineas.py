from abc import ABC, abstractmethod
from typing import Optional

from src.modules.administracion_service.src.domain.entities import Linea
from src.modules.administracion_service.src.infrastructure.api.schemas.linea import LineaCreate, LineaUpdate


class ILineaRepository(ABC):

    @abstractmethod
    def exists_by_id(self, id: int) -> bool:
        pass

    @abstractmethod
    def exists_by_nombre(self, nombre: str) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Linea]:
        pass

    @abstractmethod
    def get_all(self) -> list[Linea]:
        pass

    @abstractmethod
    def create(self, data: LineaCreate) -> Linea:
        pass

    @abstractmethod
    def update(self, data: LineaUpdate, id: int) -> Optional[Linea]:
        pass

    @abstractmethod
    def soft_delete(self, id: int) -> bool:
        pass

