from sqlalchemy import (
    Column,
    String,
    Date,
    ForeignKey,
    BigInteger,
    Integer,
    Boolean,
    DateTime,
    UniqueConstraint,
    Index,
    Enum as SQLEnum
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.shared.database import _BaseMain
from src.modules.management_service.src.domain.entities import TipoMovimiento
from src.modules.auth_service.src.infrastructure.db.models import LineaORM
from datetime import date, datetime
from typing import List


class WorkerMovementORM(_BaseMain):
    __tablename__ = "fm_movimientos_operarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    linea = Column(String(255), nullable=False)
    fecha_p = Column(Date, nullable=False)
    tipo_movimiento = Column(SQLEnum(TipoMovimiento), nullable=False) 
    motivo = Column(String(255), nullable=False)
    codigo_operario = Column(String(255), nullable=False)
    destino = Column(String(255))
    hora = Column(DateTime, nullable=False)
    observacion = Column(String(255))

    __table_args__ = (Index('idx_fecha_p_linea_operario', 'fecha_p', 'linea', 'codigo_operario'),)

class RefMotivosORM(_BaseMain):
    __tablename__ = "ref_motivos"

    id_motivo = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False)
    tipo_motivo = Column(String(10), nullable=False)
    es_justificado = Column(Boolean, nullable=False, default=False)
    estado = Column(String(10), nullable=False, default="ACTIVO")


class RefDestinosMotivosORM(_BaseMain):
    __tablename__ = "ref_destinos_motivos"

    id_destino = Column(Integer, primary_key=True, autoincrement=True)
    id_motivo = Column(Integer, nullable=False)
    nombre_destino = Column(String(100), nullable=False)
    descripcion = Column(String(200), nullable=True)
    estado = Column(String(10), nullable=False, default="ACTIVO")

## TURNOS
class CtrlDefectosORM(_BaseMain):
    __tablename__ = 'fm_ctrl_defectos'

    CDEF_ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    CDEF_LOTE: Mapped[str] = mapped_column(String(20), nullable=False)
    CDEF_NBANDEJA: Mapped[int] = mapped_column(Integer, nullable=False)
    CDEF_CANTIDAD: Mapped[int] = mapped_column(Integer, nullable=False)
    
    ROL_USUARIO: Mapped[str] = mapped_column(String(50), nullable=False)
    ID_USUARIO: Mapped[int] = mapped_column(Integer, nullable=False)
    FECHA_P: Mapped[date] = mapped_column(Date, nullable=False)

    LINE_ID: Mapped[int] = mapped_column(ForeignKey("fm_lineas_operarios.LINE_ID"), nullable=False)
    OPER_ID: Mapped[int] = mapped_column(ForeignKey("fm_gestion_operarios.OPER_ID"), nullable=False)

    # Relacion con LineaORM (muchos a uno)
    #linea: Mapped['LineaORM'] = relationship("LineaORM", back_populates="defectos")
    # Relacion con OperariosORM (muchos a uno)
    #operario: Mapped['OperariosORM'] = relationship("OperariosORM", back_populates="defectos")

class OperariosORM(_BaseMain):
    __tablename__ = "fm_gestion_operarios"

    OPER_ID = Column(Integer, primary_key=True, autoincrement=True)
    OPER_CODIGO = Column(String(50))
    
    OPER_ESTADO = Column(String(20), default="ACTIVO")
    OPER_FECCRE = Column(DateTime, default=datetime.now)

    # Relaciones de uno a uno
    OPER_TURNO = Column(Integer, ForeignKey('fm_turnos_operarios.TURN_ID'))
    OPER_AREA = Column(Integer, ForeignKey('fm_area_operarios.AREA_ID'))
    OPER_LINEA = Column(Integer, ForeignKey('fm_lineas_operarios.LINE_ID'))
    
    # Relacion Operaro - Linea -> 1 Operario trabaja 1 Linea
    linea = relationship("LineaORM", backref="operario", uselist=False)
    # Relacion con CtrlDefectosORM (uno a muchos)
    #defectos: Mapped[List["CtrlDefectosORM"]] = relationship("CtrlDefectosORM", back_populates="operario")