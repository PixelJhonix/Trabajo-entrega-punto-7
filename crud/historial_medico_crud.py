"""Operaciones CRUD para HistorialMedico."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from entities.historial_medico import HistorialMedico
from entities.paciente import Paciente
from sqlalchemy.orm import Session


class HistorialMedicoCRUD:
    """CRUD para gestión de historiales médicos."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_fecha_pasada(self, fecha: str) -> bool:
        """Validar que la fecha sea pasada o presente."""
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_obj <= datetime.now().date()
        except ValueError:
            return False

    def crear_historial(
        self,
        paciente_id: UUID,
        numero_historial: str,
        fecha_apertura: str,
        id_usuario_creacion: UUID,
        estado: str = "Activo",
    ) -> HistorialMedico:
        """
        Crear un nuevo historial médico con validaciones.

        Args:
            paciente_id: UUID del paciente
            numero_historial: Número único del historial
            fecha_apertura: Fecha de apertura (YYYY-MM-DD)
            id_usuario_creacion: UUID del usuario que crea
            estado: Estado del historial (default: Activo)

        Returns:
            HistorialMedico creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validar que el paciente existe
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        if not numero_historial or len(numero_historial.strip()) == 0:
            raise ValueError("El número de historial es obligatorio")

        if len(numero_historial) > 50:
            raise ValueError("El número de historial no puede exceder 50 caracteres")

        if self.obtener_historial_por_numero(numero_historial):
            raise ValueError("El número de historial ya existe")

        if not fecha_apertura or not self._validar_fecha_pasada(fecha_apertura):
            raise ValueError("La fecha de apertura debe ser válida (YYYY-MM-DD)")

        estados_validos = ["Activo", "Cerrado", "Archivado"]
        if estado not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")

        # Verificar que el paciente no tenga ya un historial activo
        historial_existente = (
            self.db.query(HistorialMedico)
            .filter(
                HistorialMedico.paciente_id == paciente_id,
                HistorialMedico.estado == "Activo",
            )
            .first()
        )
        if historial_existente:
            raise ValueError("El paciente ya tiene un historial médico activo")

        historial = HistorialMedico(
            paciente_id=paciente_id,
            numero_historial=numero_historial.strip(),
            fecha_apertura=fecha_apertura,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(historial)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def obtener_historial(self, historial_id: UUID) -> Optional[HistorialMedico]:
        """
        Obtener un historial por ID.

        Args:
            historial_id: UUID del historial

        Returns:
            HistorialMedico encontrado o None
        """
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.id == historial_id)
            .first()
        )

    def obtener_historial_por_numero(
        self, numero_historial: str
    ) -> Optional[HistorialMedico]:
        """
        Obtener un historial por número.

        Args:
            numero_historial: Número del historial

        Returns:
            HistorialMedico encontrado o None
        """
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.numero_historial == numero_historial.strip())
            .first()
        )

    def obtener_historial_por_paciente(
        self, paciente_id: UUID
    ) -> Optional[HistorialMedico]:
        """
        Obtener historial por paciente.

        Args:
            paciente_id: UUID del paciente

        Returns:
            HistorialMedico del paciente o None
        """
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.paciente_id == paciente_id)
            .first()
        )

    def obtener_historiales(
        self, skip: int = 0, limit: int = 100
    ) -> List[HistorialMedico]:
        """
        Obtener lista de historiales con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de historiales
        """
        return self.db.query(HistorialMedico).offset(skip).limit(limit).all()

    def obtener_historiales_por_estado(self, estado: str) -> List[HistorialMedico]:
        """
        Obtener historiales por estado.

        Args:
            estado: Estado de los historiales

        Returns:
            Lista de historiales del estado
        """
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.estado == estado)
            .all()
        )

    def buscar_historiales_por_numero(self, numero: str) -> List[HistorialMedico]:
        """
        Buscar historiales por número.

        Args:
            numero: Texto a buscar en el número

        Returns:
            Lista de historiales que coinciden
        """
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.numero_historial.contains(numero))
            .all()
        )

    def actualizar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[HistorialMedico]:
        """
        Actualizar un historial con validaciones.

        Args:
            historial_id: UUID del historial
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            HistorialMedico actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        historial = self.obtener_historial(historial_id)
        if not historial:
            return None

        if "numero_historial" in kwargs:
            numero_historial = kwargs["numero_historial"]
            if not numero_historial or len(numero_historial.strip()) == 0:
                raise ValueError("El número de historial es obligatorio")
            if len(numero_historial) > 50:
                raise ValueError(
                    "El número de historial no puede exceder 50 caracteres"
                )
            if (
                self.obtener_historial_por_numero(numero_historial)
                and self.obtener_historial_por_numero(numero_historial).id
                != historial_id
            ):
                raise ValueError("El número de historial ya existe")
            kwargs["numero_historial"] = numero_historial.strip()

        if "fecha_apertura" in kwargs:
            fecha_apertura = kwargs["fecha_apertura"]
            if not fecha_apertura or not self._validar_fecha_pasada(fecha_apertura):
                raise ValueError("La fecha de apertura debe ser válida (YYYY-MM-DD)")

        if "estado" in kwargs:
            estado = kwargs["estado"]
            estados_validos = ["Activo", "Cerrado", "Archivado"]
            if estado not in estados_validos:
                raise ValueError(
                    f"El estado debe ser uno de: {', '.join(estados_validos)}"
                )

        historial.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(historial, key):
                setattr(historial, key, value)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def cerrar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[HistorialMedico]:
        """
        Cerrar un historial médico.

        Args:
            historial_id: UUID del historial
            id_usuario_edicion: UUID del usuario que cierra

        Returns:
            HistorialMedico cerrado o None
        """
        return self.actualizar_historial(
            historial_id, id_usuario_edicion, estado="Cerrado"
        )

    def archivar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[HistorialMedico]:
        """
        Archivar un historial médico.

        Args:
            historial_id: UUID del historial
            id_usuario_edicion: UUID del usuario que archiva

        Returns:
            HistorialMedico archivado o None
        """
        return self.actualizar_historial(
            historial_id, id_usuario_edicion, estado="Archivado"
        )

    def eliminar_historial(self, historial_id: UUID) -> bool:
        """
        Eliminar un historial médico.

        Args:
            historial_id: UUID del historial

        Returns:
            True si se eliminó, False si no existe
        """
        historial = self.obtener_historial(historial_id)
        if historial:
            self.db.delete(historial)
            self.db.commit()
            return True
        return False
