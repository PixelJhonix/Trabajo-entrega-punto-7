"""Entidad HistorialMedico: modelo ORM para historiales médicos."""

import uuid
from sqlalchemy import Column, DateTime, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class HistorialMedico(Base):
    """Modelo ORM de historial médico."""

    __tablename__ = "historiales_medicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )

    numero_historial = Column(String(50), unique=True, nullable=False, index=True)
    fecha_apertura = Column(Date, nullable=False)
    estado = Column(String(20), nullable=False, default="Activo", index=True)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    paciente = relationship("Paciente", back_populates="historial")
    entradas = relationship(
        "HistorialEntrada", back_populates="historial", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<HistorialMedico(id={self.id}, numero='{self.numero_historial}', paciente_id={self.paciente_id}, estado='{self.estado}')>"
