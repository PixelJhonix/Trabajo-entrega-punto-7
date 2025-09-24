"""
Entidad HistorialEntrada - Sistema Hospitalario
Modelo ORM para las entradas del historial médico
"""

import uuid
from sqlalchemy import Column, DateTime, String, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class HistorialEntrada(Base):
    """Modelo de HistorialEntrada para el sistema hospitalario"""

    __tablename__ = "historial_entradas"

    # Clave primaria
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Claves foráneas
    historial_id = Column(
        UUID(as_uuid=True),
        ForeignKey("historiales_medicos.id"),
        nullable=False,
        index=True,
    )
    medico_id = Column(
        UUID(as_uuid=True), ForeignKey("medicos.id"), nullable=False, index=True
    )
    cita_id = Column(
        UUID(as_uuid=True), ForeignKey("citas.id"), nullable=True, index=True
    )

    # Datos de la entrada
    diagnostico = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=False)
    notas = Column(Text, nullable=True)
    fecha_registro = Column(Date, nullable=False)
    firma_digital = Column(Text, nullable=True)

    # Auditoría automática
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relaciones
    historial = relationship("HistorialMedico", back_populates="entradas")
    medico = relationship("Medico", back_populates="entradas_historial")
    cita = relationship("Cita", back_populates="entradas_historial")

    def __repr__(self):
        return f"<HistorialEntrada(id={self.id}, historial_id={self.historial_id}, medico_id={self.medico_id}, fecha={self.fecha_registro})>"
