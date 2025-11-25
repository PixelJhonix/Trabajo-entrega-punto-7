import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Enfermera(Base):
    """
    Entidad que representa una enfermera.
    
    Atributos:
        turno: Turno de trabajo. Valores posibles: mañana, tarde, noche
    """

    __tablename__ = "tbl_enfermeras"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    numero_licencia = Column(String(50), unique=True, index=True, nullable=False)
    turno = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    hospitalizaciones = relationship("Hospitalizacion", back_populates="enfermera")

    def __repr__(self):
        return f"<Enfermera(id={self.id}, nombre='{self.nombre} {self.apellido}', turno='{self.turno}')>"
