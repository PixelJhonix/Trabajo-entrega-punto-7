# Registro de datos del usuario, diagnóstico y decisión de profesional needed.

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, Field
import uuid


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String, unique=True)
    edad = Column(String)
    diagnostico = Column(String)
    necesita = Column(String)  # 'doctor' o 'enfermera'

    historial = relationship(
        "HistorialMedico",
        back_populates="paciente",
        uselist=False,
        cascade="all, delete-orphan",
    )
    citas = relationship("Citas", back_populates="usuario", cascade="all, delete")
    facturas = relationship("Factura", back_populates="usuario", cascade="all, delete")

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', edad={self.edad}, diagnostico='{self.diagnostico}', necesita='{self.necesita}')"


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., ge=0)
    diagnostico: str = Field(..., min_length=1)
    necesita: str = Field(..., pattern="^(doctor|enfermera)$")


class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1)
    edad: int | None = Field(None, ge=0)
    diagnostico: str | None = Field(None, min_length=1)
    necesita: str | None = Field(None, pattern="^(doctor|enfermera)$")
