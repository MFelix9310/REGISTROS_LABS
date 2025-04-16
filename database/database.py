from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Crear la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./registros_laboratorios.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Proporciona una sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    finally:
        db.close() 