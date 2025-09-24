# Genera factura con lo que necesitaba el paciente y descripción.

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, Field
import uuid


class Factura(Base):
    __tablename__ = "facturas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    descripcion = Column(String)
    monto = Column(Float)

    usuario = relationship("Usuario", back_populates="facturas")

    def __repr__(self):
        return f"Factura(id={self.id}, usuario_id={self.usuario_id}, descripcion='{self.descripcion}', monto={self.monto})"

    def mostrar_factura(self):
        print(
            f"Factura para {self.usuario.nombre}: {self.descripcion} - Monto: {self.monto}"
        )


class FacturaCreate(BaseModel):
    usuario_nombre: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    monto: float = Field(..., gt=0)
