"""
database.py
-----------
Configuración de la base de datos usando SQLAlchemy.
Implementa el patrón de conexión con SQLite para persistencia.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a SQLite (archivo local)
DATABASE_URL = "sqlite:///./quicktask.db"

# Engine: gestiona la conexión con la BD
# check_same_thread=False es necesario para SQLite con FastAPI (multi-threading)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal: factory para crear sesiones de BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase base para los modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependency para inyectar sesión de BD en endpoints.
    Se cierra automáticamente después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
