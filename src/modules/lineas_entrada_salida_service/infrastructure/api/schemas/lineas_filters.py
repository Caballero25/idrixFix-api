from datetime import date
from typing import Optional

from pydantic import BaseModel, conint


class LineasFilters(BaseModel):
    fecha_inicial: Optional[date] = None
    fecha_final: Optional[date] = None

class LineasPagination(LineasFilters):
    page: conint(ge=1) = 1
    page_size: conint(ge=1) = 20