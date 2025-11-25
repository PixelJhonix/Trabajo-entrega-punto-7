import uuid
from datetime import datetime

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class HistorialMedico(Base):
    """
    Entidad que representa un historial médico.
    
    Atributos:
        estado: Estado del historial. Valores posibles: abierto, cerrado, archivado
    """

    __tablename__ = "tbl_historiales_medicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    numero_historial = Column(String(50), unique=True, index=True, nullable=False)
    estado = Column(String(20), default="abierto")
    notas_generales = Column(String(1000), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_pacientes.id"), nullable=False
    )

    paciente = relationship("Paciente", back_populates="historiales_medicos")
    entradas = relationship(
        "HistorialEntrada",
        back_populates="historial_medico",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<HistorialMedico(id={self.id}, numero='{self.numero_historial}', estado='{self.estado}')>"
