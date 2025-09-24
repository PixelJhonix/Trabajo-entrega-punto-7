"""Operaciones CRUD para Factura."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from entities.factura import Factura
from entities.paciente import Paciente
from sqlalchemy.orm import Session


class FacturaCRUD:
    """CRUD para gestión de facturas."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_fecha_pasada(self, fecha: str) -> bool:
        """Validar que la fecha sea pasada o presente."""
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_obj <= datetime.now().date()
        except ValueError:
            return False

    def _validar_fecha_futura(self, fecha: str) -> bool:
        """Validar que la fecha sea futura."""
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_obj > datetime.now().date()
        except ValueError:
            return False

    def crear_factura(
        self,
        paciente_id: UUID,
        numero_factura: str,
        fecha_emision: str,
        fecha_limite_pago: str,
        total: Decimal,
        id_usuario_creacion: UUID,
        estado: str = "Pendiente",
        metodo_pago: str = None,
    ) -> Factura:
        """
        Crear una nueva factura con validaciones.

        Args:
            paciente_id: UUID del paciente
            numero_factura: Número único de factura
            fecha_emision: Fecha de emisión (YYYY-MM-DD)
            fecha_limite_pago: Fecha límite de pago (YYYY-MM-DD)
            total: Total de la factura
            id_usuario_creacion: UUID del usuario que crea
            estado: Estado de la factura (default: Pendiente)
            metodo_pago: Método de pago (opcional)

        Returns:
            Factura creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validar que el paciente existe
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        if not numero_factura or len(numero_factura.strip()) == 0:
            raise ValueError("El número de factura es obligatorio")

        if len(numero_factura) > 50:
            raise ValueError("El número de factura no puede exceder 50 caracteres")

        if self.obtener_factura_por_numero(numero_factura):
            raise ValueError("El número de factura ya existe")

        if not fecha_emision or not self._validar_fecha_pasada(fecha_emision):
            raise ValueError("La fecha de emisión debe ser válida (YYYY-MM-DD)")

        if not fecha_limite_pago or not self._validar_fecha_futura(fecha_limite_pago):
            raise ValueError("La fecha límite de pago debe ser futura (YYYY-MM-DD)")

        if total <= 0:
            raise ValueError("El total debe ser mayor a 0")

        if total > Decimal("999999.99"):
            raise ValueError("El total no puede exceder 999,999.99")

        estados_validos = ["Pendiente", "Pagada", "Vencida", "Cancelada"]
        if estado not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")

        if metodo_pago and len(metodo_pago) > 50:
            raise ValueError("El método de pago no puede exceder 50 caracteres")

        factura = Factura(
            paciente_id=paciente_id,
            numero_factura=numero_factura.strip(),
            fecha_emision=fecha_emision,
            fecha_limite_pago=fecha_limite_pago,
            total=total,
            estado=estado,
            metodo_pago=metodo_pago.strip() if metodo_pago else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def obtener_factura(self, factura_id: UUID) -> Optional[Factura]:
        """
        Obtener una factura por ID.

        Args:
            factura_id: UUID de la factura

        Returns:
            Factura encontrada o None
        """
        return self.db.query(Factura).filter(Factura.id == factura_id).first()

    def obtener_factura_por_numero(self, numero_factura: str) -> Optional[Factura]:
        """
        Obtener una factura por número.

        Args:
            numero_factura: Número de factura

        Returns:
            Factura encontrada o None
        """
        return (
            self.db.query(Factura)
            .filter(Factura.numero_factura == numero_factura.strip())
            .first()
        )

    def obtener_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        """
        Obtener lista de facturas con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de facturas
        """
        return self.db.query(Factura).offset(skip).limit(limit).all()

    def obtener_facturas_por_paciente(self, paciente_id: UUID) -> List[Factura]:
        """
        Obtener facturas por paciente.

        Args:
            paciente_id: UUID del paciente

        Returns:
            Lista de facturas del paciente
        """
        return self.db.query(Factura).filter(Factura.paciente_id == paciente_id).all()

    def obtener_facturas_por_estado(self, estado: str) -> List[Factura]:
        """
        Obtener facturas por estado.

        Args:
            estado: Estado de las facturas

        Returns:
            Lista de facturas del estado
        """
        return self.db.query(Factura).filter(Factura.estado == estado).all()

    def obtener_facturas_por_fecha(self, fecha: str) -> List[Factura]:
        """
        Obtener facturas por fecha de emisión.

        Args:
            fecha: Fecha de emisión (YYYY-MM-DD)

        Returns:
            Lista de facturas de la fecha
        """
        return self.db.query(Factura).filter(Factura.fecha_emision == fecha).all()

    def obtener_facturas_vencidas(self) -> List[Factura]:
        """
        Obtener facturas vencidas.

        Returns:
            Lista de facturas vencidas
        """
        fecha_actual = datetime.now().date()
        return (
            self.db.query(Factura)
            .filter(
                Factura.fecha_limite_pago < fecha_actual, Factura.estado == "Pendiente"
            )
            .all()
        )

    def actualizar_factura(
        self, factura_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Factura]:
        """
        Actualizar una factura con validaciones.

        Args:
            factura_id: UUID de la factura
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Factura actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        factura = self.obtener_factura(factura_id)
        if not factura:
            return None

        if "numero_factura" in kwargs:
            numero_factura = kwargs["numero_factura"]
            if not numero_factura or len(numero_factura.strip()) == 0:
                raise ValueError("El número de factura es obligatorio")
            if len(numero_factura) > 50:
                raise ValueError("El número de factura no puede exceder 50 caracteres")
            if (
                self.obtener_factura_por_numero(numero_factura)
                and self.obtener_factura_por_numero(numero_factura).id != factura_id
            ):
                raise ValueError("El número de factura ya existe")
            kwargs["numero_factura"] = numero_factura.strip()

        if "fecha_emision" in kwargs:
            fecha_emision = kwargs["fecha_emision"]
            if not fecha_emision or not self._validar_fecha_pasada(fecha_emision):
                raise ValueError("La fecha de emisión debe ser válida (YYYY-MM-DD)")

        if "fecha_limite_pago" in kwargs:
            fecha_limite_pago = kwargs["fecha_limite_pago"]
            if not fecha_limite_pago or not self._validar_fecha_futura(
                fecha_limite_pago
            ):
                raise ValueError("La fecha límite de pago debe ser futura (YYYY-MM-DD)")

        if "total" in kwargs:
            total = kwargs["total"]
            if total <= 0:
                raise ValueError("El total debe ser mayor a 0")
            if total > Decimal("999999.99"):
                raise ValueError("El total no puede exceder 999,999.99")

        if "estado" in kwargs:
            estado = kwargs["estado"]
            estados_validos = ["Pendiente", "Pagada", "Vencida", "Cancelada"]
            if estado not in estados_validos:
                raise ValueError(
                    f"El estado debe ser uno de: {', '.join(estados_validos)}"
                )

        if "metodo_pago" in kwargs and kwargs["metodo_pago"]:
            metodo_pago = kwargs["metodo_pago"]
            if len(metodo_pago) > 50:
                raise ValueError("El método de pago no puede exceder 50 caracteres")
            kwargs["metodo_pago"] = metodo_pago.strip()

        factura.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(factura, key):
                setattr(factura, key, value)
        self.db.commit()
        self.db.refresh(factura)
        return factura

    def pagar_factura(
        self, factura_id: UUID, metodo_pago: str, id_usuario_edicion: UUID
    ) -> Optional[Factura]:
        """
        Marcar una factura como pagada.

        Args:
            factura_id: UUID de la factura
            metodo_pago: Método de pago utilizado
            id_usuario_edicion: UUID del usuario que registra el pago

        Returns:
            Factura pagada o None
        """
        return self.actualizar_factura(
            factura_id, id_usuario_edicion, estado="Pagada", metodo_pago=metodo_pago
        )

    def cancelar_factura(
        self, factura_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[Factura]:
        """
        Cancelar una factura.

        Args:
            factura_id: UUID de la factura
            id_usuario_edicion: UUID del usuario que cancela

        Returns:
            Factura cancelada o None
        """
        return self.actualizar_factura(
            factura_id, id_usuario_edicion, estado="Cancelada"
        )

    def marcar_facturas_vencidas(self) -> int:
        """
        Marcar facturas vencidas automáticamente.

        Returns:
            Número de facturas marcadas como vencidas
        """
        fecha_actual = datetime.now().date()
        facturas_vencidas = (
            self.db.query(Factura)
            .filter(
                Factura.fecha_limite_pago < fecha_actual, Factura.estado == "Pendiente"
            )
            .all()
        )

        for factura in facturas_vencidas:
            factura.estado = "Vencida"

        self.db.commit()
        return len(facturas_vencidas)

    def eliminar_factura(self, factura_id: UUID) -> bool:
        """
        Eliminar una factura.

        Args:
            factura_id: UUID de la factura

        Returns:
            True si se eliminó, False si no existe
        """
        factura = self.obtener_factura(factura_id)
        if factura:
            self.db.delete(factura)
            self.db.commit()
            return True
        return False
