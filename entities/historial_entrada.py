"""
Entidad HistorialEntrada - Sistema de gestión hospitalaria
"""

import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class HistorialEntrada(Base):
    """Modelo de HistorialEntrada para el sistema hospitalario"""

    __tablename__ = "tbl_historial_entradas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fecha_consulta = Column(DateTime, nullable=False)
    diagnostico = Column(String(500), nullable=False)
    tratamiento = Column(String(500), nullable=True)
    observaciones = Column(String(1000), nullable=True)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    historial_medico_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_historiales_medicos.id"), nullable=False
    )
    medico_id = Column(UUID(as_uuid=True), ForeignKey("tbl_medicos.id"), nullable=False)

    historial_medico = relationship("HistorialMedico", back_populates="entradas")
    medico = relationship("Medico", back_populates="historiales_entrada")

    def __repr__(self):
        return f"<HistorialEntrada(id={self.id}, diagnostico='{self.diagnostico[:50]}...', fecha='{self.fecha_consulta}')>"
