"""Entidad Hospitalizacion: modelo ORM para hospitalizaciones."""

import uuid
from sqlalchemy import Column, DateTime, String, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Hospitalizacion(Base):
    """Modelo ORM de hospitalización."""

    __tablename__ = "hospitalizaciones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )
    medico_responsable_id = Column(
        UUID(as_uuid=True), ForeignKey("medicos.id"), nullable=False, index=True
    )
    enfermera_asignada_id = Column(
        UUID(as_uuid=True), ForeignKey("enfermeras.id"), nullable=True, index=True
    )

    tipo_cuidado = Column(String(50), nullable=False)
    descripcion = Column(Text, nullable=False)
    numero_habitacion = Column(String(10), nullable=False)
    tipo_habitacion = Column(String(20), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(String(20), nullable=False, default="Activa", index=True)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    paciente = relationship("Paciente", back_populates="hospitalizaciones")
    medico_responsable = relationship(
        "Medico", back_populates="hospitalizaciones_responsable"
    )
    enfermera_asignada = relationship(
        "Enfermera", back_populates="hospitalizaciones_asignadas"
    )
    factura_detalles = relationship("FacturaDetalle", back_populates="hospitalizacion")

    def __repr__(self):
        return f"<Hospitalizacion(id={self.id}, paciente_id={self.paciente_id}, habitacion='{self.numero_habitacion}', estado='{self.estado}')>"
