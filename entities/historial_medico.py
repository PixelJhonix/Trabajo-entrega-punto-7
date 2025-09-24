# Muestra todo lo que se le ha hecho al paciente.

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from typing import List
import uuid


class HistorialMedico(Base):
    __tablename__ = "historiales"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    registros = Column(JSON)  # Lista de strings con eventos

    paciente = relationship("Usuario", back_populates="historial")

    def __repr__(self):
        return f"HistorialMedico(id={self.id}, paciente_id={self.paciente_id}, registros={self.registros})"

    def mostrar_historial(self):
        print(f"Historial de {self.paciente.nombre}:")
        for r in self.registros:
            print(r)


class HistorialMedicoCreate(BaseModel):
    paciente_id: str
    registros: List[str] = []
