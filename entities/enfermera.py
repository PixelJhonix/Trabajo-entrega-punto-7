"""Entidad Enfermera: modelo ORM para enfermeras."""

import uuid
from sqlalchemy import Column, DateTime, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Enfermera(Base):
    """Modelo ORM de enfermera."""

    __tablename__ = "enfermeras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    primer_nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100), nullable=True)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    especialidad = Column(String(100), nullable=True)
    numero_licencia = Column(String(50), unique=True, nullable=False)
    turno = Column(String(20), nullable=False)  # Mañana, Tarde, Noche
    telefono = Column(String(20), nullable=False)
    email = Column(String(150), nullable=True)
    direccion = Column(String(500), nullable=False)

    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    hospitalizaciones_asignadas = relationship(
        "Hospitalizacion", back_populates="enfermera_asignada"
    )

    def __repr__(self):
        return f"<Enfermera(id={self.id}, nombre='{self.primer_nombre} {self.apellido}', turno='{self.turno}')>"
