from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from src.modules.administracion_service.src.infrastructure.api.schemas.planta import PlantaResponse


class LineaResponse(BaseModel):
    line_id: int
    line_nombre: str
    line_estado: Optional[str] = None
    line_feccre: Optional[datetime] = None
    line_fecmod: Optional[datetime] = None
    line_planta: Optional[PlantaResponse] = None

    class Config:
        from_attributes = True

class EstadoLineaEnum(str, Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"

class LineaCreate(BaseModel):
    line_nombre: str
    line_planta: Optional[int] = None


class LineaUpdate(BaseModel):
    line_nombre: Optional[str] = None
    line_planta: Optional[int] = None
