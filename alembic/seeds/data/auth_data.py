"""
Datos iniciales para el sistema de autenticación
"""
from datetime import datetime
import hashlib
import secrets

def hash_password(password: str) -> str:
    """Genera hash del password usando el mismo método que el value object"""
    salt = secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac('sha256', 
                                      password.encode('utf-8'), 
                                      salt.encode('utf-8'), 
                                      100000)
    return f"{salt}:{password_hash.hex()}"

# Roles iniciales
ROLES_DATA = [
    {
        "nombre": "Administrador",
        "descripcion": "Acceso completo al sistema",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Supervisor",
        "descripcion": "Supervisor de planta con acceso limitado",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "nombre": "Operario",
        "descripcion": "Operario de planta con acceso básico",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Usuarios iniciales
USUARIOS_DATA = [
    {
        "username": "admin",
        "password_hash": hash_password("Admin123!"),
        "id_rol": 1,  # Administrador
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "username": "supervisor",
        "password_hash": hash_password("Super123!"),
        "id_rol": 2,  # Supervisor
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Permisos de módulo para Administrador (acceso completo)
PERMISOS_ADMIN_DATA = [
    {
        "id_rol": 1,
        "modulo": "PRODUCCION",
        "permisos": ["read", "write"],
        "ruta": "/produccion",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 1,
        "modulo": "INVENTARIO",
        "permisos": ["read", "write"],
        "ruta": "/inventario",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 1,
        "modulo": "EMPLEADOS",
        "permisos": ["read", "write"],
        "ruta": "/empleados",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 1,
        "modulo": "PLANTA",
        "permisos": ["read", "write"],
        "ruta": "/planta",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 1,
        "modulo": "REPORTES",
        "permisos": ["read", "write"],
        "ruta": "/reportes",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 1,
        "modulo": "CONFIGURACION",
        "permisos": ["read", "write"],
        "ruta": "/configuracion",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Permisos de módulo para Supervisor (acceso limitado)
PERMISOS_SUPERVISOR_DATA = [
    {
        "id_rol": 2,
        "modulo": "PRODUCCION",
        "permisos": ["read", "write"],
        "ruta": "/produccion",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 2,
        "modulo": "INVENTARIO",
        "permisos": ["read"],
        "ruta": "/inventario",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 2,
        "modulo": "EMPLEADOS",
        "permisos": ["read"],
        "ruta": "/empleados",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id_rol": 2,
        "modulo": "REPORTES",
        "permisos": ["read"],
        "ruta": "/reportes",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Permisos de módulo para Operario (solo lectura básica)
PERMISOS_OPERARIO_DATA = [
    {
        "id_rol": 3,
        "modulo": "PRODUCCION",
        "permisos": ["read"],
        "ruta": "/produccion",
        "is_active": True,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

# Combinar todos los permisos
PERMISOS_MODULO_DATA = PERMISOS_ADMIN_DATA + PERMISOS_SUPERVISOR_DATA + PERMISOS_OPERARIO_DATA
