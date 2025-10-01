from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.shared.base import get_db
from src.shared.common.responses import success_response, error_response
# Importar el repositorio y casos de uso del movimiento
from src.modules.management_service.src.infrastructure.db.repositories.movimientos_operario import (
    WorkerMovementRepository,
)
from src.modules.management_service.src.application.use_cases.movimientos_operario import (
    WorkerMovementUseCases,
)
# Importar los schemas del movimiento
from src.modules.management_service.src.infrastructure.api.schemas.movimientos_operario import (
    WorkerMovementCreate,
    WorkerMovementUpdate,
    WorkerMovementResponse,
)

router = APIRouter()

# Definir la función de dependencia para los nuevos casos de uso
def get_movement_use_cases(db: Session = Depends(get_db)) -> WorkerMovementUseCases:
    repository = WorkerMovementRepository(db)
    return WorkerMovementUseCases(repository)


@router.post("/", response_model=WorkerMovementResponse, status_code=status.HTTP_201_CREATED)
def create_movement(
    movement_data: WorkerMovementCreate,
    use_cases: WorkerMovementUseCases = Depends(get_movement_use_cases),
):
    new_data = use_cases.create_movement(movement_data)
    return success_response(
        data=WorkerMovementResponse.model_validate(new_data).model_dump(mode="json"),
        message="Movimiento creado",
        status_code=201,
    )


@router.get(
    "/{movement_id}", response_model=WorkerMovementResponse, status_code=status.HTTP_200_OK
)
def get_movement_by_id(
    movement_id: int, use_cases: WorkerMovementUseCases = Depends(get_movement_use_cases)
):
    data = use_cases.get_movement_by_id(movement_id)
    if not data:
        return error_response(
            message="Movimiento no encontrado", status_code=status.HTTP_404_NOT_FOUND
        )
    return success_response(
        data=WorkerMovementResponse.model_validate(data).model_dump(mode="json"),
        message="Movimiento obtenido",
    )
