"""
Entidad Cita - Sistema Hospitalario
Modelo ORM para la gestión de citas médicas
"""

import uuid
from sqlalchemy import Column, DateTime, String, Date, Time, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Cita(Base):
    __tablename__ = "citas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Claves foráneas
    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )
    medico_id = Column(
        UUID(as_uuid=True), ForeignKey("medicos.id"), nullable=False, index=True
    )

    # Datos de la cita
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(Text, nullable=False)
    estado = Column(String(20), nullable=False, default="Agendada", index=True)
    observaciones = Column(Text, nullable=True)

    # Auditoría automática
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
    factura_detalles = relationship("FacturaDetalle", back_populates="cita")
    entradas_historial = relationship("HistorialEntrada", back_populates="cita")

    def __repr__(self):
        return f"<Cita(id={self.id}, paciente_id={self.paciente_id}, medico_id={self.medico_id}, fecha={self.fecha}, hora={self.hora}, estado='{self.estado}')>"
