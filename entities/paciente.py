import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, Date, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Paciente(Base):
    """Entidad que representa un paciente."""

    __tablename__ = "tbl_pacientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    fecha_nacimiento = Column(Date, nullable=False)
    direccion = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    citas = relationship("Cita", back_populates="paciente")
    hospitalizaciones = relationship("Hospitalizacion", back_populates="paciente")
    facturas = relationship("Factura", back_populates="paciente")
    historiales_medicos = relationship("HistorialMedico", back_populates="paciente")

    def __repr__(self):
        return f"<Paciente(id={self.id}, nombre='{self.nombre} {self.apellido}', email='{self.email}')>"
