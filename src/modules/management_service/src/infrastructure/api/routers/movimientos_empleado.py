from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from src.shared.base import get_db
from src.shared.common.responses import success_response, error_response
from src.shared.exceptions import RepositoryError, NotFoundError
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
    WorkerMovementFilters,
    WorkerMovementPagination,
    WorkerMovementPaginatedResponse
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

# 1. Controlador para EDITAR (PUT)
@router.put(
    "/{movement_id}", response_model=WorkerMovementResponse, status_code=status.HTTP_200_OK
)
def update_movement_controller(
    movement_id: int,
    movement_data: WorkerMovementUpdate,
    use_cases: WorkerMovementUseCases = Depends(get_movement_use_cases),
):
    try:
        updated_data = use_cases.update_movement(movement_id, movement_data)
        return success_response(
            data=WorkerMovementResponse.model_validate(updated_data).model_dump(mode="json"),
            message="Movimiento actualizado",
        )
    except NotFoundError as e:
        return error_response(
            message=str(e), status_code=status.HTTP_404_NOT_FOUND
        )
    except RepositoryError as e:
        return error_response(
            message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 2. Controlador para ELIMINAR (DELETE - Hard Delete)
@router.delete("/{movement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movement_controller(
    movement_id: int, use_cases: WorkerMovementUseCases = Depends(get_movement_use_cases)
):
    try:
        use_cases.delete_movement(movement_id)
        # El código 204 indica que la petición fue exitosa y no hay contenido a retornar
        return success_response(
            data=None,
            message="Movimiento eliminado permanentemente",
            status_code=status.HTTP_204_NO_CONTENT,
        )
    except NotFoundError as e:
        # Aquí puedes decidir si 404 o 500, pero 404 es común para indicar que el recurso no existe
        return error_response(
            message=str(e), status_code=status.HTTP_404_NOT_FOUND
        )
    except RepositoryError as e:
        return error_response(
            message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 3. Controlador para OBTENER EL TOTAL DE REGISTROS POR FILTROS (POST)
# Usamos POST para pasar los filtros en el cuerpo de la petición.
@router.post("/total", status_code=status.HTTP_200_OK)
def get_total_movements_by_filters(
    filters: WorkerMovementFilters,
    use_cases: WorkerMovementUseCases = Depends(get_movement_use_cases),
):
    try:
        total_records = use_cases.count_movements_by_filters(filters)
        return success_response(
            data=total_records,
            message="Total de movimientos obtenido",
        )
    except RepositoryError as e:
        return error_response(
            message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 4. Controlador para OBTENER REGISTROS PAGINADOS POR FILTROS (POST)
# Usamos POST para pasar los filtros y parámetros de paginación en el cuerpo.
@router.post("/paginated", status_code=status.HTTP_200_OK)
def get_movements_paginated(
    pagination_params: WorkerMovementPagination,
    use_cases: WorkerMovementUseCases = Depends(get_movement_use_cases),
):
    try:
        pagination_result = use_cases.get_movements_paginated_by_filters(pagination_params)
        
        # Mapeamos las entidades de dominio ('data') a los schemas de respuesta
        response_data = [
            WorkerMovementResponse.model_validate(d).model_dump(mode="json")
            for d in pagination_result["data"]
        ]
        
        # Construimos la respuesta final, incluyendo los metadatos de paginación
        response_data_with_meta = {
            "total_records": pagination_result["total_records"],
            "total_pages": pagination_result["total_pages"],
            "page": pagination_result["page"],
            "page_size": pagination_result["page_size"],
            "data": response_data,
        }
        
        return success_response(
            data=response_data_with_meta,
            message="Movimientos paginados obtenidos",
        )
    except RepositoryError as e:
        return error_response(
            message=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )