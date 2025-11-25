import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Hospitalizacion(Base):
    """
    Entidad que representa una hospitalización.
    
    Atributos:
        estado: Estado de la hospitalización. Valores posibles: activa, completada, cancelada
    """

    __tablename__ = "tbl_hospitalizaciones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fecha_ingreso = Column(DateTime, nullable=False)
    fecha_salida = Column(DateTime, nullable=True)
    motivo = Column(String(255), nullable=False)
    numero_habitacion = Column(String(10), nullable=False)
    estado = Column(String(20), default="activa")
    notas = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_pacientes.id"), nullable=False
    )
    medico_id = Column(UUID(as_uuid=True), ForeignKey("tbl_medicos.id"), nullable=False)
    enfermera_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_enfermeras.id"), nullable=True
    )

    paciente = relationship("Paciente", back_populates="hospitalizaciones")
    medico = relationship("Medico", back_populates="hospitalizaciones")
    enfermera = relationship("Enfermera", back_populates="hospitalizaciones")

    def __repr__(self):
        return f"<Hospitalizacion(id={self.id}, habitacion='{self.numero_habitacion}', estado='{self.estado}')>"
