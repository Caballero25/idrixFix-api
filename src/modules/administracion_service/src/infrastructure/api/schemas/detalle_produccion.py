from datetime import date
from typing import Optional

from pydantic import BaseModel, conint

from src.modules.administracion_service.src.infrastructure.api.schemas.shared import TurnoEnum, LineaEnum


class DetalleProduccionResponse(BaseModel):
    dpro_id: int
    dpro_fecprod: Optional[date] = None
    dpro_lote: Optional[str] = None
    dpro_pmiga: Optional[float] = None
    dpro_ppanza: Optional[float] = None
    dpro_pdesperdicio: Optional[float] = None
    dpro_linea: int
    dpro_turnox: Optional[int] = None

    class Config:
        from_attributes = True

class DetalleProduccionUpdate(BaseModel):
    dpro_pmiga: Optional[float] = None
    dpro_ppanza: Optional[float] = None
    dpro_pdesperdicio: Optional[float] = None
    dpro_linea: Optional[LineaEnum] = None
    dpro_turnox: Optional[TurnoEnum] = None

class DetalleProduccionFilters(BaseModel):
    fecprod: date

class DetalleProduccionPagination(DetalleProduccionFilters):
    page: conint(ge=1) = 1
    page_size: conint(ge=1) = 20



