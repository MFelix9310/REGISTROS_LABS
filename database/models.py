from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Table
from sqlalchemy.orm import relationship
from .database import Base

# Tabla de relación entre Docentes y Laboratorios (muchos a muchos)
docente_laboratorio = Table(
    'docente_laboratorio',
    Base.metadata,
    Column('docente_id', Integer, ForeignKey('docentes.id'), primary_key=True),
    Column('laboratorio_id', Integer, ForeignKey('laboratorios.id'), primary_key=True)
)

class Carrera(Base):
    __tablename__ = "carreras"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    
    # Relaciones
    docentes = relationship("Docente", back_populates="carrera")
    laboratorios = relationship("Laboratorio", back_populates="carrera")

class Laboratorio(Base):
    __tablename__ = "laboratorios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="laboratorios")
    docentes = relationship("Docente", secondary=docente_laboratorio, back_populates="laboratorios")
    registros = relationship("RegistroUso", back_populates="laboratorio")

class Docente(Base):
    __tablename__ = "docentes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    carrera_id = Column(Integer, ForeignKey("carreras.id"))
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="docentes")
    laboratorios = relationship("Laboratorio", secondary=docente_laboratorio, back_populates="docentes")
    registros = relationship("RegistroUso", back_populates="docente")

class Periodo(Base):
    __tablename__ = "periodos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    
    # Relaciones
    registros = relationship("RegistroUso", back_populates="periodo")

class RegistroUso(Base):
    __tablename__ = "registros_uso"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora_entrada = Column(Time)
    hora_salida = Column(Time)
    actividad = Column(String)
    
    # Claves foráneas
    docente_id = Column(Integer, ForeignKey("docentes.id"))
    laboratorio_id = Column(Integer, ForeignKey("laboratorios.id"))
    periodo_id = Column(Integer, ForeignKey("periodos.id"))
    
    # Relaciones
    docente = relationship("Docente", back_populates="registros")
    laboratorio = relationship("Laboratorio", back_populates="registros")
    periodo = relationship("Periodo", back_populates="registros") 