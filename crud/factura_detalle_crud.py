"""Operaciones CRUD para FacturaDetalle."""

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
        factura_id: UUID,
        descripcion: str,
        cantidad: int,
        precio_unitario: float,
        id_usuario_creacion: UUID,
        cita_id: UUID = None,
        hospitalizacion_id: UUID = None,
    ) -> FacturaDetalle:
        """
        Crear un nuevo detalle de factura.

        Args:
            factura_id: UUID de la factura
            descripcion: Descripción del servicio
            cantidad: Cantidad del servicio
            precio_unitario: Precio por unidad
            id_usuario_creacion: UUID del usuario que crea
            cita_id: UUID de la cita (opcional)
            hospitalizacion_id: UUID de la hospitalización (opcional)

        Returns:
            FacturaDetalle creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not descripcion or len(descripcion.strip()) == 0:
            raise ValueError("La descripción es obligatoria")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        if precio_unitario <= 0:
            raise ValueError("El precio unitario debe ser mayor a 0")

        if not cita_id and not hospitalizacion_id:
            raise ValueError("Debe especificar cita_id o hospitalizacion_id")

        if cita_id and hospitalizacion_id:
            raise ValueError(
                "No puede especificar cita_id y hospitalizacion_id al mismo tiempo"
            )

        subtotal = cantidad * precio_unitario

        detalle = FacturaDetalle(
            factura_id=factura_id,
            cita_id=cita_id,
            hospitalizacion_id=hospitalizacion_id,
            descripcion=descripcion.strip(),
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            subtotal=subtotal,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def obtener_detalle(self, detalle_id: UUID) -> Optional[FacturaDetalle]:
        """
        Obtener un detalle por ID.

        Args:
            detalle_id: UUID del detalle

        Returns:
            FacturaDetalle encontrado o None
        """
        return (
            self.db.query(FacturaDetalle)
            .filter(FacturaDetalle.id == detalle_id)
            .first()
        )

    def obtener_detalles_por_factura(self, factura_id: UUID) -> List[FacturaDetalle]:
        """
        Obtener todos los detalles de una factura.

        Args:
            factura_id: UUID de la factura

        Returns:
            Lista de detalles
        """
        return (
            self.db.query(FacturaDetalle)
            .filter(FacturaDetalle.factura_id == factura_id)
            .all()
        )

    def obtener_detalles(self, skip: int = 0, limit: int = 100) -> List[FacturaDetalle]:
        """
        Obtener lista de detalles con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de detalles
        """
        return self.db.query(FacturaDetalle).offset(skip).limit(limit).all()

    def actualizar_detalle(
        self, detalle_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[FacturaDetalle]:
        """
        Actualizar un detalle.

        Args:
            detalle_id: UUID del detalle
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            FacturaDetalle actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        detalle = self.obtener_detalle(detalle_id)
        if not detalle:
            return None

        if "descripcion" in kwargs:
            descripcion = kwargs["descripcion"]
            if not descripcion or len(descripcion.strip()) == 0:
                raise ValueError("La descripción es obligatoria")
            kwargs["descripcion"] = descripcion.strip()

        if "cantidad" in kwargs:
            cantidad = kwargs["cantidad"]
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")
            kwargs["cantidad"] = cantidad

        if "precio_unitario" in kwargs:
            precio_unitario = kwargs["precio_unitario"]
            if precio_unitario <= 0:
                raise ValueError("El precio unitario debe ser mayor a 0")
            kwargs["precio_unitario"] = precio_unitario

        # Recalcular subtotal si cambió cantidad o precio
        if "cantidad" in kwargs or "precio_unitario" in kwargs:
            cantidad = kwargs.get("cantidad", detalle.cantidad)
            precio_unitario = kwargs.get("precio_unitario", detalle.precio_unitario)
            kwargs["subtotal"] = cantidad * precio_unitario

        detalle.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(detalle, key):
                setattr(detalle, key, value)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def eliminar_detalle(self, detalle_id: UUID) -> bool:
        """
        Eliminar un detalle.

        Args:
            detalle_id: UUID del detalle

        Returns:
            True si se eliminó, False si no existe
        """
        detalle = self.obtener_detalle(detalle_id)
        if detalle:
            self.db.delete(detalle)
            self.db.commit()
            return True
        return False
