from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PlantaResponse(BaseModel):
    plan_id: int
    plan_nombre: str
    plan_estado: Optional[str] = None
    plan_feccre: Optional[datetime] = None
    plan_fecmod: Optional[datetime] = None

    class Config:
        from_attributes = True