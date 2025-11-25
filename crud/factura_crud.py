from typing import List, Optional
from uuid import UUID

from entities.factura import Factura
from sqlalchemy.orm import Session


class FacturaCRUD:
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
        id_usuario_creacion: Optional[UUID] = None,
        impuestos: float = 0,
        notas: str = None,
    ) -> Factura:
        """Crear una nueva factura."""
        from entities.paciente import Paciente

        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        if not numero_factura or len(numero_factura.strip()) == 0:
            raise ValueError("El número de factura es obligatorio")

        factura_existente = self.obtener_factura_por_numero(numero_factura)
        if factura_existente:
            raise ValueError("El número de factura ya está registrado")

        if subtotal < 0:
            raise ValueError("El subtotal no puede ser negativo")
        if impuestos < 0:
            raise ValueError("Los impuestos no pueden ser negativos")
        if total < 0:
            raise ValueError("El total no puede ser negativo")

        factura = Factura(
            numero_factura=numero_factura.strip(),
            fecha_emision=fecha_emision,
            fecha_vencimiento=fecha_vencimiento,
            subtotal=subtotal,
            impuestos=impuestos,
            total=total,
            paciente_id=paciente_id,
            notas=notas.strip() if notas else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_facturas(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[Factura]:
        """Obtener todas las facturas con opción de incluir inactivas."""
        query = self.db.query(Factura)
        if not include_inactive:
            query = query.filter(Factura.activo == True)
        return query.offset(skip).limit(limit).all()

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
            .filter(Factura.paciente_id == paciente_id, Factura.activo == True)
            .all()
        )

    def obtener_facturas_por_estado(self, estado: str) -> List[Factura]:
        """Obtener facturas por estado."""
        return (
            self.db.query(Factura)
            .filter(Factura.estado == estado, Factura.activo == True)
            .all()
        )

    def obtener_facturas_por_fecha(self, fecha) -> List[Factura]:
        """Obtener facturas por fecha."""
        return (
            self.db.query(Factura)
            .filter(Factura.fecha_emision.date() == fecha, Factura.activo == True)
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
                Factura.activo == True,
            )
            .all()
        )

    def actualizar_factura(
        self, factura_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Factura]:
        """Actualizar una factura."""
        factura = self.obtener_factura(factura_id)
        if factura:
            for key, value in kwargs.items():
                if hasattr(factura, key):
                    setattr(factura, key, value)
            if id_usuario_edicion:
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

    def inactivar_factura(self, factura_id: UUID) -> bool:
        """Inactivar una factura (soft delete)."""
        factura = self.obtener_factura(factura_id)
        if not factura:
            return False
        if not factura.activo:
            return True
        factura.activo = False
        self.db.commit()
        return True

    def reactivar_factura(self, factura_id: UUID) -> bool:
        """Reactivar una factura inactiva."""
        factura = self.obtener_factura(factura_id)
        if not factura:
            return False
        if factura.activo:
            return True
        factura.activo = True
        self.db.commit()
        return True

    def eliminar_factura_permanente(self, factura_id: UUID) -> bool:
        """Eliminar una factura permanentemente de la base de datos."""
        import logging
        try:
            factura = self.obtener_factura(factura_id)
            if not factura:
                raise ValueError(f"Factura con ID {factura_id} no encontrada")
            
            # Los detalles de factura se eliminan automáticamente por cascade
            # pero los eliminamos explícitamente para asegurarnos
            from entities.factura_detalle import FacturaDetalle
            detalles = self.db.query(FacturaDetalle).filter(FacturaDetalle.factura_id == factura_id).all()
            for detalle in detalles:
                self.db.delete(detalle)
            
            self.db.delete(factura)
            self.db.commit()
            
            logging.info(f"Factura {factura_id} eliminada permanentemente")
            return True
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error al eliminar factura permanentemente {factura_id}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError(f"Error al eliminar factura: {str(e)}")

    def eliminar_factura(self, factura_id: UUID) -> bool:
        """Eliminar una factura (soft delete) - mantiene compatibilidad."""
        return self.inactivar_factura(factura_id)
