# Aquí se registra el médico o enfermera con sus datos.
from uuid import UUID
from typing import (
    Any,
)  # esta diciendo que una variable o argumento puede ser de cualquier tipo de dato.


from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import relationship
from .base import Base


class Profesional(Base):
    __tablename__ = "profesionales"
    id = Column(UUID, primary_key=True)
    nombre = Column(String, unique=True)
    categoria_profesional = Column(String)

    citas = relationship("Citas", back_populates="profesional", cascade="all, delete")

    def __repr__(self):
        return f"Profesional(id={self.id}, nombre='{self.nombre}', categoria_profesional='{self.categoria_profesional}')"
