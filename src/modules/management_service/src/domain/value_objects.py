from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class CodigoEmpleado:
    """Objeto de valor para el código del empleado"""

    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("El código del empleado no puede estar vacío")
        if len(self.value) > 10:
            raise ValueError(
                "El código del empleado no puede tener más de 10 caracteres"
            )
        # Validar que solo contenga caracteres alfanuméricos
        if not re.match(r"^[A-Za-z0-9]+$", self.value):
            raise ValueError(
                "El código del empleado solo puede contener letras y números"
            )

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class Identificacion:
    """Objeto de valor para la identificación del empleado"""

    value: str

    def __post_init__(self):
        if self.value is not None:
            if len(self.value.strip()) == 0:
                raise ValueError("La identificación no puede estar vacía")
            if len(self.value) > 10:
                raise ValueError(
                    "La identificación no puede tener más de 10 caracteres"
                )
            # Validar que solo contenga números
            if not re.match(r"^\d+$", self.value):
                raise ValueError("La identificación solo puede contener números")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class NombreCompleto:
    """Objeto de valor para el nombre completo del empleado"""

    nombres: str
    apellidos: str

    def __post_init__(self):
        if not self.nombres or len(self.nombres.strip()) == 0:
            raise ValueError("Los nombres no pueden estar vacíos")
        if not self.apellidos or len(self.apellidos.strip()) == 0:
            raise ValueError("Los apellidos no pueden estar vacíos")
        if len(self.nombres) > 50:
            raise ValueError("Los nombres no pueden tener más de 50 caracteres")
        if len(self.apellidos) > 50:
            raise ValueError("Los apellidos no pueden tener más de 50 caracteres")

    def nombre_completo(self) -> str:
        """Retorna el nombre completo formateado"""
        return f"{self.nombres.strip()} {self.apellidos.strip()}"

    def __str__(self) -> str:
        return self.nombre_completo()


@dataclass(frozen=True)
class SalarioBase:
    """Objeto de valor para el salario base"""

    valor: float

    def __post_init__(self):
        if self.valor < 0:
            raise ValueError("El salario base no puede ser negativo")
        if self.valor > 99999999.99:  # Limite razonable
            raise ValueError("El salario base excede el límite permitido")

    def __str__(self) -> str:
        return f"${self.valor:,.2f}"
