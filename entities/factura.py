"""
Entidad Factura - Sistema Hospitalario
Modelo ORM para la gestión de facturas
"""

import uuid
from sqlalchemy import Column, DateTime, String, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.config import Base


class Factura(Base):
    """Modelo de Factura para el sistema hospitalario"""

    __tablename__ = "facturas"

    # Clave primaria
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Clave foránea
    paciente_id = Column(
        UUID(as_uuid=True), ForeignKey("pacientes.id"), nullable=False, index=True
    )

    # Datos de la factura
    numero_factura = Column(String(50), unique=True, nullable=False, index=True)
    fecha_emision = Column(Date, nullable=False)
    fecha_limite_pago = Column(Date, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(
        String(20), nullable=False, default="Pendiente", index=True
    )  # Pendiente, Pagada, Vencida, Cancelada
    metodo_pago = Column(String(50), nullable=True)

    # Auditoría automática
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relaciones
    paciente = relationship("Paciente", back_populates="facturas")
    detalles = relationship(
        "FacturaDetalle", back_populates="factura", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Factura(id={self.id}, numero='{self.numero_factura}', total={self.total}, estado='{self.estado}')>"
