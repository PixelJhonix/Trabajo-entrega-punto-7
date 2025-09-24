"""Módulo para la gestión de facturas en el sistema de salud.

Este módulo define el modelo Factura para almacenar los detalles de las facturas y el
modelo Pydantic FacturaCreate para validar los datos de creación de facturas.
"""

from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .base import Base
from pydantic import BaseModel, Field
import uuid


class Factura(Base):
    """Modelo SQLAlchemy que representa una factura por servicios médicos.

    Atributos:
        id (UUID): Identificador único de la factura.
        usuario_id (UUID): Clave foránea que referencia al usuario.
        descripcion (str): Descripción de los servicios o ítems facturados.
        monto (float): Monto total de la factura.
        usuario (Usuario): Relación con el usuario asociado.
    """

    __tablename__ = "facturas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"))
    descripcion = Column(String)
    monto = Column(Float)

    usuario = relationship("Usuario", back_populates="facturas")

    def __repr__(self):
        """Representación en cadena de la instancia de Factura."""
        return f"Factura(id={self.id}, usuario_id={self.usuario_id}, descripcion='{self.descripcion}', monto={self.monto})"

    def mostrar_factura(self):
        """Imprime los detalles de la factura, incluyendo nombre del usuario, descripción y monto."""
        print(
            f"Factura para {self.usuario.nombre}: {self.descripcion} - Monto: {self.monto}"
        )


class FacturaCreate(BaseModel):
    """Modelo Pydantic para validar los datos de creación de facturas.

    Atributos:
        usuario_nombre (str): Nombre del usuario asociado a la factura.
        descripcion (str): Descripción de los servicios o ítems facturados.
        monto (float): Monto total de la factura (debe ser positivo).
    """

    usuario_nombre: str = Field(..., min_length=1)
    descripcion: str = Field(..., min_length=1)
    monto: float = Field(..., gt=0)
