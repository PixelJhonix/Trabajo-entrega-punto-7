"""Entidad Medico: modelo ORM para médicos."""

import uuid
from sqlalchemy import Column, DateTime, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Medico(Base):
    """Modelo ORM de médico."""

    __tablename__ = "medicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    primer_nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100), nullable=True)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    especialidad = Column(String(100), nullable=False)
    numero_licencia = Column(String(50), unique=True, nullable=False)
    consultorio = Column(String(50), nullable=True)
    telefono = Column(String(20), nullable=False)
    email = Column(String(150), nullable=True)
    direccion = Column(String(500), nullable=False)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    citas = relationship("Cita", back_populates="medico")
    hospitalizaciones_responsable = relationship(
        "Hospitalizacion", back_populates="medico_responsable"
    )
    entradas_historial = relationship("HistorialEntrada", back_populates="medico")

    def __repr__(self):
        return f"<Medico(id={self.id}, nombre='Dr. {self.primer_nombre} {self.apellido}', especialidad='{self.especialidad}')>"
