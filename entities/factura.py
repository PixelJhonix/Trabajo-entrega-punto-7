import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Factura(Base):
    """
    Entidad que representa una factura.
    
    Atributos:
        estado: Estado de la factura. Valores posibles: pendiente, pagada, vencida, cancelada
    """

    __tablename__ = "tbl_facturas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    numero_factura = Column(String(50), unique=True, index=True, nullable=False)
    fecha_emision = Column(DateTime, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    impuestos = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), default="pendiente")
    notas = Column(String(500), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_pacientes.id"), nullable=False
    )

    paciente = relationship("Paciente", back_populates="facturas")
    detalles = relationship(
        "FacturaDetalle", back_populates="factura", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Factura(id={self.id}, numero='{self.numero_factura}', total={self.total})>"
