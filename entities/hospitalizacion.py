"""
Entidad Hospitalizacion - Sistema Hospitalario
Modelo ORM para la gestión de hospitalizaciones
"""

import uuid
from sqlalchemy import Column, DateTime, String, Date, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Hospitalizacion(Base):
    """Modelo de Hospitalizacion para el sistema hospitalario"""

    __tablename__ = "hospitalizaciones"

    # Clave primaria
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Claves foráneas
    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )
    medico_responsable_id = Column(
        UUID(as_uuid=True), ForeignKey("medicos.id"), nullable=False, index=True
    )
    enfermera_asignada_id = Column(
        UUID(as_uuid=True), ForeignKey("enfermeras.id"), nullable=True, index=True
    )

    # Datos de la hospitalización
    tipo_cuidado = Column(String(50), nullable=False)  # Intensivo, Intermedio, Básico
    descripcion = Column(Text, nullable=False)
    numero_habitacion = Column(String(10), nullable=False)
    tipo_habitacion = Column(String(20), nullable=False)  # Individual, Compartida, VIP
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    estado = Column(
        String(20), nullable=False, default="Activa", index=True
    )  # Activa, Finalizada, Trasladada

    # Auditoría automática
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relaciones
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
