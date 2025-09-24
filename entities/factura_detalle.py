"""
Entidad FacturaDetalle - Sistema Hospitalario
Modelo ORM para los detalles de las facturas
"""

import uuid
from sqlalchemy import (
    Column,
    DateTime,
    String,
    ForeignKey,
    Text,
    Integer,
    Numeric,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class FacturaDetalle(Base):
    """Modelo de FacturaDetalle para el sistema hospitalario"""

    __tablename__ = "factura_detalles"

    # Clave primaria
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Clave foránea principal
    factura_id = Column(
        UUID(as_uuid=True), ForeignKey("facturas.id"), nullable=False, index=True
    )

    # Claves foráneas opcionales (solo una debe estar presente)
    cita_id = Column(
        UUID(as_uuid=True), ForeignKey("citas.id"), nullable=True, index=True
    )
    hospitalizacion_id = Column(
        UUID(as_uuid=True),
        ForeignKey("hospitalizaciones.id"),
        nullable=True,
        index=True,
    )

    # Datos del detalle
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Auditoría automática
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relaciones
    factura = relationship("Factura", back_populates="detalles")
    cita = relationship("Cita", back_populates="factura_detalles")
    hospitalizacion = relationship("Hospitalizacion", back_populates="factura_detalles")

    # Constraint para asegurar que solo una FK de servicio esté presente
    __table_args__ = (
        CheckConstraint(
            "(cita_id IS NOT NULL AND hospitalizacion_id IS NULL) OR (cita_id IS NULL AND hospitalizacion_id IS NOT NULL)",
            name="check_solo_un_servicio",
        ),
    )

    def __repr__(self):
        return f"<FacturaDetalle(id={self.id}, factura_id={self.factura_id}, descripcion='{self.descripcion[:30]}...', subtotal={self.subtotal})>"
