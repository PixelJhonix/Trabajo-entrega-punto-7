# Aquí se registra el médico o enfermera con sus datos.

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, Field
import uuid


class Profesional(Base):
    __tablename__ = "profesionales"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, unique=True)
    categoria_profesional = Column(String)

    citas = relationship("Citas", back_populates="profesional", cascade="all, delete")

    def __repr__(self):
        return f"Profesional(id={self.id}, nombre='{self.nombre}', categoria_profesional='{self.categoria_profesional}')"


class ProfesionalCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    categoria_profesional: str = Field(..., pattern="^(doctor|enfermera)$")
