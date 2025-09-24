"""
Entidad HistorialMedico - Sistema Hospitalario
Modelo ORM para la gestión de historiales médicos
"""

import uuid
from sqlalchemy import Column, DateTime, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class HistorialMedico(Base):
    """Modelo de HistorialMedico para el sistema hospitalario"""

    __tablename__ = "historiales_medicos"

    # Clave primaria
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Clave foránea
    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )

    # Datos del historial
    numero_historial = Column(String(50), unique=True, nullable=False, index=True)
    fecha_apertura = Column(Date, nullable=False)
    estado = Column(
        String(20), nullable=False, default="Activo", index=True
    )  # Activo, Cerrado, Archivado

    # Auditoría automática
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="historial")
    entradas = relationship(
        "HistorialEntrada", back_populates="historial", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<HistorialMedico(id={self.id}, numero='{self.numero_historial}', paciente_id={self.paciente_id}, estado='{self.estado}')>"
