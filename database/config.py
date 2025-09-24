"""
Configuración de la base de datos PostgreSQL con Neon.

Este módulo realiza las siguientes tareas:
- Carga las variables de entorno desde el archivo .env.
- Obtiene la URL de conexión a la base de datos desde la variable de entorno DATABASE_URL.
- Crea el motor de SQLAlchemy para gestionar la conexión con la base de datos.
- Define la clase base para los modelos ORM.
- Proporciona funciones para obtener sesiones de base de datos y crear tablas.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Cambiar a True para ver consultas SQL
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
    connect_args={"sslmode": "require"},  # Asegurar conexión SSL
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """Generador de sesiones de base de datos.

    Yields:
        db (Session): Sesión de base de datos para operaciones ORM.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos ORM.

    Utiliza la metadata de la clase Base para crear las tablas en la base de datos.
    """
    Base.metadata.create_all(bind=engine)
