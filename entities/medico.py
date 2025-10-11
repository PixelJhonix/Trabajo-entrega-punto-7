"""
Entidad Medico - Sistema de gestión hospitalaria
"""

import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Medico(Base):
    """Modelo de Medico para el sistema hospitalario"""

    __tablename__ = "tbl_medicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    especialidad = Column(String(100), nullable=False)
    numero_licencia = Column(String(50), unique=True, index=True, nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    citas = relationship("Cita", back_populates="medico")
    hospitalizaciones = relationship("Hospitalizacion", back_populates="medico")
    historiales_entrada = relationship("HistorialEntrada", back_populates="medico")

    def __repr__(self):
        return f"<Medico(id={self.id}, nombre='{self.nombre} {self.apellido}', especialidad='{self.especialidad}')>"
