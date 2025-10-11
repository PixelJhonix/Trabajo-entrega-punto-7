"""
Operaciones CRUD para Factura
"""

from typing import List, Optional
from uuid import UUID

from entities.factura import Factura
from sqlalchemy.orm import Session


class FacturaCRUD:
    """CRUD para gestión de facturas."""

    def __init__(self, db: Session):
        self.db = db

    def crear_factura(
        self,
        numero_factura: str,
        fecha_emision,
        fecha_vencimiento,
        subtotal: float,
        total: float,
        paciente_id: UUID,
        id_usuario_creacion: UUID,
        impuestos: float = 0,
        notas: str = None,
    ) -> Factura:
        """Crear una nueva factura."""
        factura = Factura(
            numero_factura=numero_factura,
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            subtotal=subtotal,
            impuestos=impuestos,
            total=total,
            paciente_id=paciente_id,
            notas=notas,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        """Obtener todas las facturas."""
        return (
            self.db.query(Factura)
            .filter(Factura.activo)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def obtener_factura(self, factura_id: UUID) -> Optional[Factura]:
        """Obtener una factura por ID."""
        return self.db.query(Factura).filter(Factura.id == factura_id).first()

    def obtener_factura_por_numero(self, numero_factura: str) -> Optional[Factura]:
        """Obtener una factura por número."""
        return (
            self.db.query(Factura)
            .filter(Factura.numero_factura == numero_factura)
            .first()
        )

    def obtener_facturas_por_paciente(self, paciente_id: UUID) -> List[Factura]:
        """Obtener facturas por paciente."""
        return (
            self.db.query(Factura)
            .filter(Factura.paciente_id == paciente_id, Factura.activo)
            .all()
        )

    def obtener_facturas_por_estado(self, estado: str) -> List[Factura]:
        """Obtener facturas por estado."""
        return (
            self.db.query(Factura)
            .filter(Factura.estado == estado, Factura.activo)
            .all()
        )

    def obtener_facturas_por_fecha(self, fecha) -> List[Factura]:
        """Obtener facturas por fecha."""
        return (
            self.db.query(Factura)
            .filter(Factura.fecha_emision.date() == fecha, Factura.activo)
            .all()
        )

    def obtener_facturas_vencidas(self) -> List[Factura]:
        """Obtener facturas vencidas."""
        from datetime import datetime

        return (
            self.db.query(Factura)
            .filter(
                Factura.fecha_vencimiento < datetime.now(),
                Factura.estado == "pendiente",
                Factura.activo,
            )
            .all()
        )

    def actualizar_factura(
        self, factura_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Factura]:
        """Actualizar una factura."""
        factura = self.obtener_factura(factura_id)
        if factura:
            for key, value in kwargs.items():
                if hasattr(factura, key):
                    setattr(factura, key, value)
            factura.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(factura)
        return factura

    def pagar_factura(
        self, factura_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[Factura]:
        """Marcar factura como pagada."""
        return self.actualizar_factura(factura_id, id_usuario_edicion, estado="pagada")

    def cancelar_factura(
        self, factura_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[Factura]:
        """Cancelar una factura."""
        return self.actualizar_factura(
            factura_id, id_usuario_edicion, estado="cancelada"
        )

    def marcar_vencida(
        self, factura_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[Factura]:
        """Marcar factura como vencida."""
        return self.actualizar_factura(factura_id, id_usuario_edicion, estado="vencida")

    def eliminar_factura(self, factura_id: UUID) -> bool:
        """Eliminar una factura (soft delete)."""
        factura = self.obtener_factura(factura_id)
        if factura:
            factura.activo = False
            self.db.commit()
            return True
        return False
