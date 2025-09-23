# Genera factura con lo que necesitaba el paciente y descripción.
from uuid import UUID
from typing import (
    Any,
)  # esta diciendo que una variable o argumento puede ser de cualquier tipo de dato.


from sqlalchemy import UUID, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Factura(Base):
    __tablename__ = "facturas"
    id = Column(UUID, primary_key=True)
    usuario_id = Column(UUID, ForeignKey("usuarios.id"))
    descripcion = Column(String)
    monto = Column(Float)

    usuario = relationship("Usuario", back_populates="facturas")

    def __repr__(self):
        return f"Factura(id={self.id}, usuario_id={self.usuario_id}, descripcion='{self.descripcion}', monto={self.monto})"

    def mostrar_factura(self):
        print(
            f"Factura para {self.usuario.nombre}: {self.descripcion} - Monto: {self.monto}"
        )
