# Registro de datos del usuario, diagnóstico y decisión de profesional needed.
from uuid import UUID
from typing import (
    Any,
)  # esta diciendo que una variable o argumento puede ser de cualquier tipo de dato.


from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(UUID, primary_key=True)
    nombre = Column(String, unique=True)
    edad = Column(Integer)
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
