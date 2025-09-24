"""Módulo para la gestión de profesionales médicos en el sistema de salud.

Este módulo define el modelo Profesional para almacenar información de los profesionales
y el modelo Pydantic ProfesionalCreate para validar los datos de creación de profesionales.
"""

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, Field
import uuid


class Profesional(Base):
    """Modelo SQLAlchemy que representa un profesional médico.

    Atributos:
        id (UUID): Identificador único del profesional.
        nombre (str): Nombre único del profesional.
        categoria_profesional (str): Tipo de profesional ('doctor' o 'enfermera').
        citas (List[Citas]): Relación con las citas del profesional.
    """

    __tablename__ = "profesionales"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, unique=True)
    categoria_profesional = Column(String)

    citas = relationship("Citas", back_populates="profesional", cascade="all, delete")

    def __repr__(self):
        """Representación en cadena de la instancia de Profesional."""
        return f"Profesional(id={self.id}, nombre='{self.nombre}', categoria_profesional='{self.categoria_profesional}')"


class ProfesionalCreate(BaseModel):
    """Modelo Pydantic para validar los datos de creación de profesionales.

    Atributos:
        nombre (str): Nombre del profesional (no debe estar vacío).
        categoria_profesional (str): Tipo de profesional ('doctor' o 'enfermera').
    """

    nombre: str = Field(..., min_length=1)
    categoria_profesional: str = Field(..., pattern="^(doctor|enfermera)$")
