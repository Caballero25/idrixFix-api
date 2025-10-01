from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class TipoMovimiento(Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"


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