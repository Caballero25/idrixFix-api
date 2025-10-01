from pydantic import BaseModel, Field
from typing import Optional
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