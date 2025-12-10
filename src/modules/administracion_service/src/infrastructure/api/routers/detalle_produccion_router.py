import logging
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.modules.administracion_service.src.application.use_case.detalle_produccion_use_case import DetalleProduccionUseCase
from src.modules.administracion_service.src.application.ports.detalle_produccion import IDetalleProduccionRepository
from src.modules.administracion_service.src.infrastructure.api.schemas.detalle_produccion import (
    DetalleProduccionPagination, DetalleProduccionResponse, DetalleProduccionUpdate
)
from src.modules.administracion_service.src.infrastructure.db.repositories.detalle_produccion_repository import DetalleProduccionRepository
from src.shared.base import get_db
from src.shared.common.responses import success_response, error_response
from src.shared.exceptions import RepositoryError

router = APIRouter()

def get_detalle_produccion_use_case(db: Session = Depends(get_db)) -> DetalleProduccionUseCase:
    repo: IDetalleProduccionRepository = DetalleProduccionRepository(db)
    return DetalleProduccionUseCase(repo)

@router.get("/{detalle_id}", response_model=DetalleProduccionResponse, status_code=status.HTTP_200_OK)
def get_by_id(
    detalle_id: int,
    use_case: DetalleProduccionUseCase = Depends(get_detalle_produccion_use_case)
):
    try:
        record = use_case.get_by_id(detalle_id)
        return success_response(
            data=record,
            message="Registro obtenido"
        )
    except RepositoryError as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/paginated", status_code=status.HTTP_200_OK)
def get_paginated(
    pagination_params: DetalleProduccionPagination,
    use_case: DetalleProduccionUseCase = Depends(get_detalle_produccion_use_case)
):
    try:
        pagination_result = use_case.get_paginated_by_filters(pagination_params)

        response_data = [
            DetalleProduccionResponse.model_validate(d).model_dump(mode="json")
            for d in pagination_result["data"]
        ]

        response_with_meta = {
            "total_records": pagination_result["total_records"],
            "total_pages": pagination_result["total_pages"],
            "page": pagination_result["page"],
            "page_size": pagination_result["page_size"],
            "data": response_data
        }

        return success_response(
            data=response_with_meta,
            message="Registros obtenidos"
        )
    except RepositoryError as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.patch("/{detalle_id}", response_model=DetalleProduccionResponse, status_code=status.HTTP_200_OK)
def update_record(
    detalle_id: int,
    data: DetalleProduccionUpdate,
    use_case: DetalleProduccionUseCase = Depends(get_detalle_produccion_use_case)
):
    try:
        updated = use_case.update(detalle_id, data)
        return success_response(
            data=updated,
            message="Registro actualizado"
        )
    except RepositoryError as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.delete("/{detalle_id}", status_code=status.HTTP_200_OK)
def delete_record(
    detalle_id: int,
    use_case: DetalleProduccionUseCase = Depends(get_detalle_produccion_use_case)
):
    try:
        use_case.remove(detalle_id)
        return success_response(
            data=f"Registro con id {detalle_id} eliminado",
            message="Registro eliminado correctamente"
        )
    except RepositoryError as e:
        return error_response(
            message=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
