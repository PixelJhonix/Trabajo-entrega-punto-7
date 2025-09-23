# Muestra todo lo que se le ha hecho al paciente.
from uuid import UUID
from typing import (
    Any,
)  # esta diciendo que una variable o argumento puede ser de cualquier tipo de dato.


from sqlalchemy import Column, UUID, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from .base import Base


class HistorialMedico(Base):
    __tablename__ = "historiales"

    id = Column(UUID, primary_key=True)
    paciente_id = Column(UUID, ForeignKey("usuarios.id"))
    registros = Column(JSON)  # Lista de strings con eventos

    paciente = relationship("Usuario", back_populates="historial")

    def __repr__(self):
        return f"HistorialMedico(id={self.id}, paciente_id={self.paciente_id}, registros={self.registros})"

    def mostrar_historial(self):
        print(f"Historial de {self.paciente.nombre}:")
        for r in self.registros:
            print(r)
