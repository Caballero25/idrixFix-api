from pydantic import BaseModel, Field, conint
from typing import Optional, List
from datetime import date, datetime
from src.modules.management_service.src.domain.entities import TipoMovimiento

class WorkerMovementBase(BaseModel):
    linea: str = Field(..., max_length=255)
    fecha_p: date
    # Usamos el Enum directamente en Pydantic para validación
    tipo_movimiento: TipoMovimiento 
    motivo: str = Field(..., max_length=255)
    codigo_operario: str = Field(..., max_length=255)
    destino: Optional[str] = Field(None, max_length=255)
    hora: datetime 
    observacion: Optional[str] = Field(None, max_length=255)


class WorkerMovementCreate(WorkerMovementBase):
    pass


class WorkerMovementUpdate(BaseModel):
    # Permite actualizar cualquier campo, todos opcionales
    linea: Optional[str] = Field(None, max_length=255)
    fecha_p: Optional[date] = None
    tipo_movimiento: Optional[str] = Field(None, max_length=50)
    motivo: Optional[str] = Field(None, max_length=255)
    codigo_operario: Optional[str] = Field(None, max_length=255)
    destino: Optional[str] = Field(None, max_length=255)
    hora: Optional[datetime] = None
    observacion: Optional[str] = Field(None, max_length=255)


class WorkerMovementResponse(WorkerMovementBase):
    id: int
    class Config:
        from_attributes = True # Pydantic V2 (o alias en V1)
# Schema para la entrada de filtros (para conteo y paginación)
class WorkerMovementFilters(BaseModel):
    fecha_inicial: Optional[date] = None
    fecha_final: Optional[date] = None
    codigo_operario: Optional[str] = Field(None, max_length=255)


# Schema para la paginación
class WorkerMovementPagination(WorkerMovementFilters):
    page: conint(ge=1) = 1 # Página actual (mínimo 1)
    page_size: conint(ge=1) = 20 # Tamaño de página (mínimo 1)


# Schema de respuesta para la paginación (útil para el front-end)
class WorkerMovementPaginatedResponse(BaseModel):
    total_records: int
    total_pages: int
    page: int
    page_size: int
    data: List[WorkerMovementResponse]