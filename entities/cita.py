"""
Entidad Cita - Sistema de gestión hospitalaria
"""

import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Cita(Base):
    """Modelo de Cita para el sistema hospitalario"""

    __tablename__ = "tbl_citas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fecha_cita = Column(DateTime, nullable=False)
    motivo = Column(String(255), nullable=False)
    estado = Column(
        String(20), default="programada"
    )  # programada, completada, cancelada
    notas = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_pacientes.id"), nullable=False
    )
    medico_id = Column(UUID(as_uuid=True), ForeignKey("tbl_medicos.id"), nullable=False)

    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")

    def __repr__(self):
        return (
            f"<Cita(id={self.id}, fecha='{self.fecha_cita}', estado='{self.estado}')>"
        )
