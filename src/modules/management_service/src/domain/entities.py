from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class TipoMovimiento(Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"

class EstadoEnum(Enum):
    ACTIVO = "ACTIVO"
    INACTIVO = "INACTIVO"


@dataclass
class WorkerMovement:
    """Entidad para representar un movimiento de operario (cambio de línea, puesto, etc.)"""
    
    id: int
    linea: str
    fecha_p: date
    # Se actualiza el tipo a TipoMovimiento
    tipo_movimiento: TipoMovimiento
    motivo: str
    codigo_operario: str
    hora: datetime
    destino: Optional[str] = None
    observacion: Optional[str] = None

    def es_movimiento_valido(self) -> bool:
        """Valida que los campos obligatorios del movimiento no estén vacíos."""
        # La validación de tipo_movimiento se hace automáticamente al crear la entidad
        return (
            bool(self.linea.strip())
            and bool(self.motivo.strip())
            and bool(self.codigo_operario.strip())
        )

@dataclass
class RefMotivo:
    """Entidad de dominio para una referencia de motivo de movimiento."""
    id_motivo: Optional[int] = None
    descripcion: str = ""
    tipo_motivo: str = ""
    es_justificado: bool = False
    estado: str = EstadoEnum.ACTIVO.value

    def is_active(self) -> bool:
        return self.estado == EstadoEnum.ACTIVO.value


@dataclass
class RefDestinoMotivo:
    """Entidad de dominio para un destino asociado a un motivo."""
    id_destino: Optional[int] = None
    id_motivo: int = 0
    nombre_destino: str = ""
    descripcion: Optional[str] = None
    estado: str = EstadoEnum.ACTIVO.value

    def is_active(self) -> bool:
        return self.estado == EstadoEnum.ACTIVO.value
