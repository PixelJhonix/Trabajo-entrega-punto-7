import uuid
from sqlalchemy import Column, DateTime, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    primer_nombre = Column(String(100), nullable=False)
    segundo_nombre = Column(String(100), nullable=True)
    apellido = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(150), nullable=True)
    direccion = Column(String(500), nullable=False)
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=False)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    citas = relationship("Cita", back_populates="paciente")
    hospitalizaciones = relationship("Hospitalizacion", back_populates="paciente")
    facturas = relationship("Factura", back_populates="paciente")
    historial = relationship(
        "HistorialMedico", back_populates="paciente", uselist=False
    )

    def __repr__(self):
        return (
            f"<Paciente(id={self.id}, nombre='{self.primer_nombre} {self.apellido}')>"
        )
