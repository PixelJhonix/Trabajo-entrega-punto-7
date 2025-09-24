"""Módulo para la gestión del historial médico de los pacientes.

Este módulo define el modelo HistorialMedico para almacenar los registros del historial
médico y el modelo Pydantic HistorialMedicoCreate para validar los datos de creación.
"""

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel
from typing import List
import uuid


class HistorialMedico(Base):
    """Modelo SQLAlchemy que representa el historial médico de un paciente.

    Atributos:
        id (UUID): Identificador único del registro de historial.
        paciente_id (UUID): Clave foránea que referencia al paciente.
        registros (JSON): Lista de cadenas con eventos médicos.
        paciente (Usuario): Relación con el paciente asociado.
    """

    __tablename__ = "historiales"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    registros = Column(JSON)  # Lista de strings con eventos

    paciente = relationship("Usuario", back_populates="historial")

    def __repr__(self):
        """Representación en cadena de la instancia de HistorialMedico."""
        return f"HistorialMedico(id={self.id}, paciente_id={self.paciente_id}, registros={self.registros})"

    def mostrar_historial(self):
        """Imprime los registros del historial médico del paciente."""
        print(f"Historial de {self.paciente.nombre}:")
        for r in self.registros:
            print(r)


class HistorialMedicoCreate(BaseModel):
    """Modelo Pydantic para validar los datos de creación del historial médico.

    Atributos:
        paciente_id (str): UUID del paciente.
        registros (List[str]): Lista de descripciones de eventos médicos (opcional).
    """

    paciente_id: str
    registros: List[str] = []
