from sqlalchemy import create_engine, Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from .config import settings

# Configuración específica para SQL Server
engine = create_engine(
    settings.database_url,
    echo=settings.DEBUG,
    # Configuraciones específicas para SQL Server
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "timeout": 30,
        "autocommit": False,
    },
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa
_Base = declarative_base()