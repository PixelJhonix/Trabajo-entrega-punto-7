"""Módulo para la gestión de datos de usuarios (pacientes) en el sistema de salud.

Este módulo define el modelo Usuario para almacenar información de los pacientes y
modelos Pydantic para validar los datos de creación y actualización de usuarios.
"""

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, Field
import uuid


class Usuario(Base):
    """Modelo SQLAlchemy que representa un usuario (paciente) en el sistema.

    Atributos:
        id (UUID): Identificador único del usuario.
        nombre (str): Nombre único del usuario.
        edad (str): Edad del usuario.
        diagnostico (str): Diagnóstico médico del usuario.
        necesita (str): Tipo de profesional necesario ('doctor' o 'enfermera').
        historial (HistorialMedico): Relación con el historial médico del usuario.
        citas (List[Citas]): Relación con las citas del usuario.
        facturas (List[Factura]): Relación con las facturas del usuario.
    """

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
        """Representación en cadena de la instancia de Usuario."""
        return f"Usuario(id={self.id}, nombre='{self.nombre}', edad={self.edad}, diagnostico='{self.diagnostico}', necesita='{self.necesita}')"


class UsuarioCreate(BaseModel):
    """Modelo Pydantic para validar los datos de creación de usuarios.

    Atributos:
        nombre (str): Nombre del usuario (no debe estar vacío).
        edad (int): Edad del usuario (debe ser no negativa).
        diagnostico (str): Diagnóstico médico (no debe estar vacío).
        necesita (str): Tipo de profesional necesario ('doctor' o 'enfermera').
    """

    nombre: str = Field(..., min_length=1)
    edad: int = Field(..., ge=0)
    diagnostico: str = Field(..., min_length=1)
    necesita: str = Field(..., pattern="^(doctor|enfermera)$")


class UsuarioUpdate(BaseModel):
    """Modelo Pydantic para validar los datos de actualización de usuarios.

    Atributos:
        nombre (str, opcional): Nombre actualizado del usuario.
        edad (int, opcional): Edad actualizada del usuario.
        diagnostico (str, opcional): Diagnóstico médico actualizado.
        necesita (str, opcional): Tipo de profesional necesario ('doctor' o 'enfermera').
    """

    nombre: str | None = Field(None, min_length=1)
    edad: int | None = Field(None, ge=0)
    diagnostico: str | None = Field(None, min_length=1)
    necesita: str | None = Field(None, pattern="^(doctor|enfermera)$")
