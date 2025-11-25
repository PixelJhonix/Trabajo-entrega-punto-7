import uuid

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class FacturaDetalle(Base):
    """Entidad que representa un detalle de factura."""

    __tablename__ = "tbl_factura_detalles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    descripcion = Column(String(255), nullable=False)
    cantidad = Column(Numeric(10, 2), nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(UUID(as_uuid=True), nullable=True)
    id_usuario_edicion = Column(UUID(as_uuid=True), nullable=True)

    factura_id = Column(
        UUID(as_uuid=True), ForeignKey("tbl_facturas.id"), nullable=False
    )

    factura = relationship("Factura", back_populates="detalles")

    def __repr__(self):
        return f"<FacturaDetalle(id={self.id}, descripcion='{self.descripcion}', cantidad={self.cantidad})>"
