import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Agrega la raíz del proyecto al path para encontrar los módulos
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

# Importa tu configuración centralizada y la Base declarativa
from src.shared.config import settings
from src.shared.database import Base

from src.modules.management_service.db.models import (
    WorkerMovementORM
)

# Configura la URL de la base de datos desde tu archivo de configuración central
config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpreta el archivo de configuración para el logging de Python.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# El `target_metadata` apunta a la Base de tus modelos para la autogeneración de migraciones
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # Configuraciones específicas para SQL Server
        connect_args={
            "timeout": 30,
            "autocommit": False,
        },
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
