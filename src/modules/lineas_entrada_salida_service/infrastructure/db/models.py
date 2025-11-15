from sqlalchemy import Column, Integer, Date, DateTime, Float, String, Time

from src.shared.database import _BaseAuth, _BaseMain

#Linea Uno
class LineaUnoEntradaORM(_BaseMain):
    __tablename__ = "reg_linea_uno_entrad"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    turno = Column(Integer)
    codigo_secuencia = Column(String(255))
    codigo_parrilla = Column(String(255))
    p_lote = Column(String(100))
    hora_inicio = Column(Time)
    guid = Column(String(255))

class LineaUnoSalidaORM(_BaseMain):
    __tablename__ = "reg_linea_uno_salid"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    codigo_bastidor = Column(String(255))
    p_lote = Column(String(100))
    codigo_parrilla = Column(String(255))
    codigo_obrero = Column(String(255))
    guid = Column(String(255))

#Linea Dos
class LineaDosEntradaORM(_BaseMain):
    __tablename__ = "reg_linea_dos_entrad"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    turno = Column(Integer)
    codigo_secuencia = Column(String(255))
    codigo_parrilla = Column(String(255))
    p_lote = Column(String(100))
    hora_inicio = Column(Time)
    guid = Column(String(255))

#Linea Tres
class LineaTresEntradaORM(_BaseMain):
    __tablename__ = "reg_linea_tres_entrad"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    turno = Column(Integer)
    codigo_secuencia = Column(String(255))
    codigo_parrilla = Column(String(255))
    p_lote = Column(String(100))
    hora_inicio = Column(Time)
    guid = Column(String(255))

#Linea Cuatro
class LineaCuatroEntradaORM(_BaseMain):
    __tablename__ = "reg_linea_cuatro_entrad"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    turno = Column(Integer)
    codigo_secuencia = Column(String(255))
    codigo_parrilla = Column(String(255))
    p_lote = Column(String(100))
    hora_inicio = Column(Time)
    guid = Column(String(255))

#Linea Cinco
class LineaCincoEntradaORM(_BaseMain):
    __tablename__ = "reg_linea_cinco_entrad"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    turno = Column(Integer)
    codigo_secuencia = Column(String(255))
    codigo_parrilla = Column(String(255))
    p_lote = Column(String(100))
    hora_inicio = Column(Time)
    guid = Column(String(255))

#Linea Seis
class LineaSeisEntradaORM(_BaseMain):
    __tablename__ = "reg_linea_seis_entrad"

    id = Column(Integer, primary_key=True)
    fecha_p = Column(Date)
    fecha = Column(DateTime)
    peso_kg = Column(Float)
    turno = Column(Integer)
    codigo_secuencia = Column(String(255))
    codigo_parrilla = Column(String(255))
    p_lote = Column(String(100))
    hora_inicio = Column(Time)
    guid = Column(String(255))