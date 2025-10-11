"""
Operaciones CRUD para FacturaDetalle
"""

from typing import List, Optional
from uuid import UUID

from entities.factura_detalle import FacturaDetalle
from sqlalchemy.orm import Session


class FacturaDetalleCRUD:
    """CRUD para gestión de detalles de factura."""

    def __init__(self, db: Session):
        self.db = db

    def crear_detalle(
        self,
        descripcion: str,
        cantidad: float,
        precio_unitario: float,
        subtotal: float,
        factura_id: UUID,
        id_usuario_creacion: UUID,
    ) -> FacturaDetalle:
        """Crear un nuevo detalle de factura."""
        detalle = FacturaDetalle(
            descripcion=descripcion,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
            factura_id=factura_id,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalles(self, skip: int = 0, limit: int = 100) -> List[FacturaDetalle]:
        """Obtener todos los detalles de factura."""
        return (
            self.db.query(FacturaDetalle)
            .filter(FacturaDetalle.activo)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_detalle(self, detalle_id: UUID) -> Optional[FacturaDetalle]:
        """Obtener un detalle por ID."""
        return (
            self.db.query(FacturaDetalle)
            .filter(FacturaDetalle.id == detalle_id)
            .first()
        )

    def obtener_detalles_por_factura(self, factura_id: UUID) -> List[FacturaDetalle]:
        """Obtener detalles por factura."""
        return (
            self.db.query(FacturaDetalle)
            .filter(FacturaDetalle.factura_id == factura_id, FacturaDetalle.activo)
            .all()
        )

    def actualizar_detalle(
        self, detalle_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[FacturaDetalle]:
        """Actualizar un detalle de factura."""
        detalle = self.obtener_detalle(detalle_id)
        if detalle:
            for key, value in kwargs.items():
                if hasattr(detalle, key):
                    setattr(detalle, key, value)
            detalle.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(detalle)
        return detalle

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        """Eliminar un detalle de factura (soft delete)."""
        detalle = self.obtener_detalle(detalle_id)
        if detalle:
            detalle.activo = False
            self.db.commit()
            return True
        return False
