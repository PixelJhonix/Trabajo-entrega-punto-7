from typing import List, Optional
from uuid import UUID

from entities.factura_detalle import FacturaDetalle
from sqlalchemy.orm import Session


class FacturaDetalleCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_detalle(
        self,
        descripcion: str,
        cantidad: float,
        precio_unitario: float,
        subtotal: float,
        factura_id: UUID,
        id_usuario_creacion: Optional[UUID] = None,
    ) -> FacturaDetalle:
        """Crear un nuevo detalle de factura."""
        from entities.factura import Factura

        factura = self.db.query(Factura).filter(Factura.id == factura_id).first()
        if not factura:
            raise ValueError("La factura especificada no existe")

        if not descripcion or len(descripcion.strip()) == 0:
            raise ValueError("La descripción es obligatoria")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
        if precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo")
        if subtotal < 0:
            raise ValueError("El subtotal no puede ser negativo")

        detalle = FacturaDetalle(
            descripcion=descripcion.strip(),
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

    def obtener_detalles(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[FacturaDetalle]:
        """Obtener todos los detalles de factura con opción de incluir inactivos."""
        query = self.db.query(FacturaDetalle)
        if not include_inactive:
            query = query.filter(FacturaDetalle.activo == True)
        return query.offset(skip).limit(limit).all()

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
            .filter(
                FacturaDetalle.factura_id == factura_id, FacturaDetalle.activo == True
            )
            .all()
        )

    def actualizar_detalle(
        self, detalle_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[FacturaDetalle]:
        """Actualizar un detalle de factura."""
        detalle = self.obtener_detalle(detalle_id)
        if detalle:
            for key, value in kwargs.items():
                if hasattr(detalle, key):
                    setattr(detalle, key, value)
            if id_usuario_edicion:
                detalle.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(detalle)
        return detalle

    def inactivar_detalle(self, detalle_id: UUID) -> bool:
        """Inactivar un detalle de factura (soft delete)."""
        detalle = self.obtener_detalle(detalle_id)
        if not detalle:
            return False
        if not detalle.activo:
            return True
        detalle.activo = False
        self.db.commit()
        return True

    def reactivar_detalle(self, detalle_id: UUID) -> bool:
        """Reactivar un detalle de factura inactivo."""
        detalle = self.obtener_detalle(detalle_id)
        if not detalle:
            return False
        if detalle.activo:
            return True
        detalle.activo = True
        self.db.commit()
        return True

    def eliminar_detalle_permanente(self, detalle_id: UUID) -> bool:
        """Eliminar un detalle de factura permanentemente de la base de datos."""
        import logging
        try:
            detalle = self.obtener_detalle(detalle_id)
            if not detalle:
                raise ValueError(f"Detalle de factura con ID {detalle_id} no encontrado")
            
            self.db.delete(detalle)
            self.db.commit()
            
            logging.info(f"Detalle de factura {detalle_id} eliminado permanentemente")
            return True
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error al eliminar detalle de factura permanentemente {detalle_id}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError(f"Error al eliminar detalle de factura: {str(e)}")

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        """Eliminar un detalle de factura (soft delete) - mantiene compatibilidad."""
        return self.inactivar_detalle(detalle_id)
