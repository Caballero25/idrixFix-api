from fastapi import APIRouter, Depends, status
from typing import List, Dict, Any
from src.modules.auth_service.src.application.use_cases.rol_use_cases import RolUseCase
from src.modules.auth_service.src.infrastructure.api.schemas.roles import (
    RolCreate,
    RolUpdate,
    RolResponse,
    RolWithPermisosResponse,
    AsignPermisosRequest,
    ModulosDisponiblesResponse,
)
from src.modules.auth_service.src.infrastructure.db.repositories.rol_repository import RolRepository
from src.modules.auth_service.src.infrastructure.db.repositories.permiso_modulo_repository import PermisoModuloRepository
from src.shared.exceptions import DomainError
from src.shared.common.responses import success_response, error_response
from sqlalchemy.orm import Session
from src.shared.base import get_auth_db
#Auditoria
from src.modules.auth_service.src.application.use_cases.audit_use_case import AuditUseCase
from src.shared.security import get_current_user_data
from src.shared.common.auditoria import get_audit_use_case

router = APIRouter()


def get_rol_use_case(db: Session = Depends(get_auth_db), audit_uc: AuditUseCase = Depends(get_audit_use_case)) -> RolUseCase:
    """Dependency para obtener el caso de uso de roles"""
    return RolUseCase(
        rol_repository=RolRepository(db),
        permiso_repository=PermisoModuloRepository(db),
        audit_use_case=audit_uc
    )


@router.get("/", response_model=List[RolResponse], status_code=status.HTTP_200_OK)
def get_roles(rol_use_case: RolUseCase = Depends(get_rol_use_case)):
    """Obtiene lista de todos los roles"""
    data = rol_use_case.get_all_roles()
    return success_response(
        data=[RolResponse.model_validate(d).model_dump(mode="json") for d in data],
        message="Roles obtenidos"
    )


@router.get("/{rol_id}", response_model=RolResponse, status_code=status.HTTP_200_OK)
def get_rol(
    rol_id: int,
    rol_use_case: RolUseCase = Depends(get_rol_use_case)
):
    """Obtiene un rol por ID"""
    data = rol_use_case.get_rol_by_id(rol_id)
    if not data:
        return error_response(
            message="Rol no encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )
    return success_response(
        data=RolResponse.model_validate(data).model_dump(mode="json"),
        message="Rol obtenido"
    )


@router.get("/{rol_id}/permisos", response_model=RolWithPermisosResponse, status_code=status.HTTP_200_OK)
def get_rol_with_permisos(
    rol_id: int,
    rol_use_case: RolUseCase = Depends(get_rol_use_case)
):
    """Obtiene un rol con sus permisos"""
    data = rol_use_case.get_rol_permisos_summary(rol_id)
    if not data:
        return error_response(
            message="Rol no encontrado",
            status_code=status.HTTP_404_NOT_FOUND
        )
    return success_response(
        data=data,
        message="Rol con permisos obtenido"
    )


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
def create_rol(
    rol_data: RolCreate,
    rol_use_case: RolUseCase = Depends(get_rol_use_case),
    user_data: Dict[str, Any] = Depends(get_current_user_data)
):
    """Crea un nuevo rol"""
    new_data = rol_use_case.create_rol(rol_data, user_data)
    return success_response(
        data=RolResponse.model_validate(new_data).model_dump(mode="json"),
        message="Rol creado",
        status_code=201
    )


@router.put("/{rol_id}", response_model=RolResponse, status_code=status.HTTP_200_OK)
def update_rol(
    rol_id: int,
    rol_data: RolUpdate,
    rol_use_case: RolUseCase = Depends(get_rol_use_case),
    user_data: Dict[str, Any] = Depends(get_current_user_data)
):
    """Actualiza un rol existente"""
    updated_data = rol_use_case.update_rol(rol_id, rol_data, user_data)
    if not updated_data:
        return error_response(
            message="Rol no encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )
    return success_response(
        data=RolResponse.model_validate(updated_data).model_dump(mode="json"),
        message="Rol actualizado"
    )


@router.delete("/{rol_id}", status_code=status.HTTP_200_OK)
def delete_rol(
    rol_id: int, 
    rol_use_case: RolUseCase = Depends(get_rol_use_case),
    user_data: Dict[str, Any] = Depends(get_current_user_data)
):
    """Elimina (desactiva) un rol"""
    deleted_data = rol_use_case.delete_rol(rol_id, user_data)
    if not deleted_data:
        return error_response(
            message="Rol no encontrado", 
            status_code=status.HTTP_404_NOT_FOUND
        )
    return success_response(
        data={"id_rol_eliminado": deleted_data.id_rol},
        message="Rol marcado como inactivo"
    )


@router.post("/{rol_id}/permisos", status_code=status.HTTP_200_OK)
def assign_permisos_to_rol(
    rol_id: int,
    permisos_data: AsignPermisosRequest,
    rol_use_case: RolUseCase = Depends(get_rol_use_case),
    user_data: Dict[str, Any] = Depends(get_current_user_data)
):
    """Asigna permisos a un rol"""
    # Convertir los objetos Pydantic a diccionarios
    permisos_list = [p.model_dump() for p in permisos_data.permisos]
    rol_use_case.assign_permisos_to_rol(rol_id, permisos_list, user_data)
    return success_response(
        data={"permisos_asignados": True, "rol_id": rol_id},
        message="Permisos asignados exitosamente"
    )


@router.get("/modulos/disponibles", response_model=ModulosDisponiblesResponse, status_code=status.HTTP_200_OK)
def get_modulos_disponibles(rol_use_case: RolUseCase = Depends(get_rol_use_case)):
    """Obtiene la lista de módulos disponibles"""
    modulos = rol_use_case.get_available_modulos()
    return success_response(
        data={"modulos": modulos},
        message="Módulos disponibles obtenidos"
    )
