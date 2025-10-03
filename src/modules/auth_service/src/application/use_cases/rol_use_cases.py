from typing import List, Optional
from src.modules.auth_service.src.application.ports.roles import IRolRepository
from src.modules.auth_service.src.application.ports.permisos_modulo import IPermisoModuloRepository
from src.modules.auth_service.src.infrastructure.api.schemas.roles import RolCreate, RolUpdate
from src.modules.auth_service.src.infrastructure.api.schemas.permisos_modulo import PermisoModuloCreate
from src.modules.auth_service.src.infrastructure.db.models import Rol
from src.modules.auth_service.src.domain.entities import ModuloEnum, PermisoEnum
from src.shared.exceptions import AlreadyExistsError, NotFoundError, ValidationError


class RolUseCase:
    def __init__(
        self,
        rol_repository: IRolRepository,
        permiso_repository: IPermisoModuloRepository,
    ):
        self.rol_repository = rol_repository
        self.permiso_repository = permiso_repository

    def get_all_roles(self) -> List[Rol]:
        """Obtiene todos los roles"""
        return self.rol_repository.get_all()

    def get_rol_by_id(self, rol_id: int) -> Optional[Rol]:
        """Obtiene un rol por ID"""
        return self.rol_repository.get_by_id(rol_id)

    def get_rol_with_permisos(self, rol_id: int) -> Optional[Rol]:
        """Obtiene un rol con sus permisos"""
        return self.rol_repository.get_with_permisos(rol_id)

    def create_rol(self, rol_data: RolCreate) -> Rol:
        """Crea un nuevo rol"""
        # Validar que el nombre no exista
        existing_rol = self.rol_repository.get_by_nombre(rol_data.nombre)
        if existing_rol:
            raise AlreadyExistsError(f"Ya existe un rol con el nombre '{rol_data.nombre}'.")

        # Validar datos básicos
        if not rol_data.nombre or len(rol_data.nombre.strip()) < 2:
            raise ValidationError("El nombre del rol debe tener al menos 2 caracteres.")

        return self.rol_repository.create(rol_data)

    def update_rol(self, rol_id: int, rol_data: RolUpdate) -> Optional[Rol]:
        """Actualiza un rol existente"""
        # Verificar que el rol existe
        existing_rol = self.rol_repository.get_by_id(rol_id)
        if not existing_rol:
            raise NotFoundError(f"Rol con id={rol_id} no encontrado.")

        # Si se actualiza el nombre, verificar que no exista
        if rol_data.nombre and rol_data.nombre != existing_rol.nombre:
            nombre_exists = self.rol_repository.get_by_nombre(rol_data.nombre)
            if nombre_exists:
                raise AlreadyExistsError(f"Ya existe un rol con el nombre '{rol_data.nombre}'.")

        # Validar datos básicos si se proporciona nombre
        if rol_data.nombre and len(rol_data.nombre.strip()) < 2:
            raise ValidationError("El nombre del rol debe tener al menos 2 caracteres.")

        return self.rol_repository.update(rol_id, rol_data)

    def delete_rol(self, rol_id: int) -> Optional[Rol]:
        """Elimina (desactiva) un rol"""
        rol = self.rol_repository.get_by_id(rol_id)
        if not rol:
            raise NotFoundError(f"Rol con id={rol_id} no encontrado.")

        return self.rol_repository.soft_delete(rol_id)

    def assign_permisos_to_rol(self, rol_id: int, permisos_data: List[dict]) -> bool:
        """Asigna permisos de módulos a un rol"""
        # Verificar que el rol existe
        rol = self.rol_repository.get_by_id(rol_id)
        if not rol:
            raise NotFoundError(f"Rol con id={rol_id} no encontrado.")

        # Obtener TODOS los permisos existentes del rol (activos e inactivos)
        # Esto evita conflictos con el constraint único cuando hay permisos inactivos
        permisos_existentes = self.permiso_repository.get_all_by_rol_id(rol_id)
        # Normalizar a string para comparación consistente
        modulos_existentes = {}
        for p in permisos_existentes:
            modulo_key = p.modulo.value if hasattr(p.modulo, 'value') else p.modulo
            modulos_existentes[modulo_key] = p

        # Crear o actualizar permisos
        for permiso_data in permisos_data:
            try:
                # Validar módulo
                modulo = ModuloEnum(permiso_data["modulo"])
                
                # Validar permisos
                permisos = []
                for p in permiso_data["permisos"]:
                    permisos.append(PermisoEnum(p))

                # Verificar si ya existe un permiso para este módulo (comparar por valor string)
                if modulo.value in modulos_existentes:
                    # Actualizar permiso existente
                    permiso_existente = modulos_existentes[modulo.value]
                    from src.modules.auth_service.src.infrastructure.api.schemas.permisos_modulo import PermisoModuloUpdate
                    permiso_update = PermisoModuloUpdate(
                        permisos=permisos,
                        is_active=True
                    )
                    self.permiso_repository.update(permiso_existente.id_permiso_modulo, permiso_update)
                    # Remover de la lista para saber cuáles desactivar después
                    del modulos_existentes[modulo.value]
                else:
                    # Crear nuevo permiso
                    permiso_create = PermisoModuloCreate(
                        id_rol=rol_id,
                        modulo=modulo,
                        permisos=permisos
                    )
                    self.permiso_repository.create(permiso_create)

            except ValueError as e:
                raise ValidationError(f"Datos de permiso inválidos: {str(e)}")

        # Desactivar los permisos que no están en la nueva lista
        for permiso_sobrante in modulos_existentes.values():
            self.permiso_repository.soft_delete(permiso_sobrante.id_permiso_modulo)

        return True

    def get_available_modulos(self) -> List[dict]:
        """Obtiene la lista de módulos disponibles"""
        modulos = []
        for modulo in ModuloEnum:
            modulos.append({
                "nombre": modulo.value,
                "permisos_disponibles": [p.value for p in PermisoEnum]
            })
        return modulos

    def get_rol_permisos_summary(self, rol_id: int) -> Optional[dict]:
        """Obtiene un resumen de los permisos de un rol"""
        rol = self.rol_repository.get_with_permisos(rol_id)
        if not rol:
            return None

        modulos = []
        for permiso_modulo in rol.permisos_modulo or []:
            if permiso_modulo.is_active:
                # Manejar módulo (puede ser enum o string)
                nombre_modulo = (
                    permiso_modulo.modulo.value 
                    if hasattr(permiso_modulo.modulo, "value") 
                    else permiso_modulo.modulo
                )
                
                # Manejar permisos (pueden ser enums o strings)
                permisos_lista = [
                    p.value if hasattr(p, "value") else p 
                    for p in permiso_modulo.permisos
                ]
                
                modulos.append({
                    "nombre": nombre_modulo,
                    "permisos": permisos_lista
                })

        return {
            "id_rol": rol.id_rol,
            "nombre": rol.nombre,
            "descripcion": rol.descripcion,
            "is_active": rol.is_active,
            "modulos": modulos
        }
