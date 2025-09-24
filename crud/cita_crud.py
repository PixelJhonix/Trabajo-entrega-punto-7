"""Operaciones CRUD para Cita."""

from datetime import datetime, time
from typing import List, Optional
from uuid import UUID

from entities.cita import Cita
from entities.paciente import Paciente
from entities.medico import Medico
from sqlalchemy.orm import Session


class CitaCRUD:
    """CRUD para gestión de citas médicas."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_fecha_futura(self, fecha: str) -> bool:
        """Validar que la fecha sea futura."""
        try:
            fecha_cita = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_cita >= datetime.now().date()
        except ValueError:
            return False

    def _validar_hora_laboral(self, hora: str) -> bool:
        """Validar que la hora esté en horario laboral."""
        try:
            hora_obj = datetime.strptime(hora, "%H:%M:%S").time()
            hora_inicio = time(8, 0)
            hora_fin = time(17, 0)
            return hora_inicio <= hora_obj <= hora_fin
        except ValueError:
            return False

    def crear_cita(
        self,
        paciente_id: UUID,
        medico_id: UUID,
        fecha: str,
        hora: str,
        motivo: str,
        id_usuario_creacion: UUID,
        estado: str = "Agendada",
        observaciones: str = None,
    ) -> Cita:
        """
        Crear una nueva cita médica con validaciones.

        Args:
            paciente_id: UUID del paciente
            medico_id: UUID del médico
            fecha: Fecha de la cita (YYYY-MM-DD)
            hora: Hora de la cita (HH:MM:SS)
            motivo: Motivo de la consulta
            id_usuario_creacion: UUID del usuario que crea
            estado: Estado de la cita (default: Agendada)
            observaciones: Observaciones opcionales

        Returns:
            Cita creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validar que el paciente existe
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        # Validar que el médico existe
        medico = self.db.query(Medico).filter(Medico.id == medico_id).first()
        if not medico:
            raise ValueError("El médico especificado no existe")

        if not fecha or not self._validar_fecha_futura(fecha):
            raise ValueError("La fecha debe ser futura y válida (YYYY-MM-DD)")

        if not hora or not self._validar_hora_laboral(hora):
            raise ValueError("La hora debe estar entre 8:00 y 17:00 (HH:MM:SS)")

        if not motivo or len(motivo.strip()) < 5:
            raise ValueError("El motivo debe tener al menos 5 caracteres")

        if len(motivo) > 200:
            raise ValueError("El motivo no puede exceder 200 caracteres")

        estados_validos = [
            "Agendada",
            "Confirmada",
            "En Progreso",
            "Completada",
            "Cancelada",
        ]
        if estado not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")

        # Verificar disponibilidad del médico en esa fecha y hora
        cita_existente = (
            self.db.query(Cita)
            .filter(
                Cita.medico_id == medico_id,
                Cita.fecha == fecha,
                Cita.hora == hora,
                Cita.estado.in_(["Agendada", "Confirmada", "En Progreso"]),
            )
            .first()
        )
        if cita_existente:
            raise ValueError("El médico ya tiene una cita en esa fecha y hora")

        cita = Cita(
            paciente_id=paciente_id,
            medico_id=medico_id,
            fecha=fecha,
            hora=hora,
            motivo=motivo.strip(),
            estado=estado,
            observaciones=observaciones.strip() if observaciones else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def obtener_cita(self, cita_id: UUID) -> Optional[Cita]:
        """
        Obtener una cita por ID.

        Args:
            cita_id: UUID de la cita

        Returns:
            Cita encontrada o None
        """
        return self.db.query(Cita).filter(Cita.id == cita_id).first()

    def obtener_citas(self, skip: int = 0, limit: int = 100) -> List[Cita]:
        """
        Obtener lista de citas con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de citas
        """
        return self.db.query(Cita).offset(skip).limit(limit).all()

    def obtener_citas_por_paciente(self, paciente_id: UUID) -> List[Cita]:
        """
        Obtener citas por paciente.

        Args:
            paciente_id: UUID del paciente

        Returns:
            Lista de citas del paciente
        """
        return self.db.query(Cita).filter(Cita.paciente_id == paciente_id).all()

    def obtener_citas_por_medico(self, medico_id: UUID) -> List[Cita]:
        """
        Obtener citas por médico.

        Args:
            medico_id: UUID del médico

        Returns:
            Lista de citas del médico
        """
        return self.db.query(Cita).filter(Cita.medico_id == medico_id).all()

    def obtener_citas_por_fecha(self, fecha: str) -> List[Cita]:
        """
        Obtener citas por fecha.

        Args:
            fecha: Fecha de las citas (YYYY-MM-DD)

        Returns:
            Lista de citas de la fecha
        """
        return self.db.query(Cita).filter(Cita.fecha == fecha).all()

    def obtener_citas_por_estado(self, estado: str) -> List[Cita]:
        """
        Obtener citas por estado.

        Args:
            estado: Estado de las citas

        Returns:
            Lista de citas del estado
        """
        return self.db.query(Cita).filter(Cita.estado == estado).all()

    def actualizar_cita(
        self, cita_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Cita]:
        """
        Actualizar una cita con validaciones.

        Args:
            cita_id: UUID de la cita
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Cita actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        cita = self.obtener_cita(cita_id)
        if not cita:
            return None

        if "fecha" in kwargs:
            fecha = kwargs["fecha"]
            if not fecha or not self._validar_fecha_futura(fecha):
                raise ValueError("La fecha debe ser futura y válida (YYYY-MM-DD)")

        if "hora" in kwargs:
            hora = kwargs["hora"]
            if not hora or not self._validar_hora_laboral(hora):
                raise ValueError("La hora debe estar entre 8:00 y 17:00 (HH:MM:SS)")

        if "motivo" in kwargs:
            motivo = kwargs["motivo"]
            if not motivo or len(motivo.strip()) < 5:
                raise ValueError("El motivo debe tener al menos 5 caracteres")
            if len(motivo) > 200:
                raise ValueError("El motivo no puede exceder 200 caracteres")
            kwargs["motivo"] = motivo.strip()

        if "estado" in kwargs:
            estado = kwargs["estado"]
            estados_validos = [
                "Agendada",
                "Confirmada",
                "En Progreso",
                "Completada",
                "Cancelada",
            ]
            if estado not in estados_validos:
                raise ValueError(
                    f"El estado debe ser uno de: {', '.join(estados_validos)}"
                )

        if "observaciones" in kwargs and kwargs["observaciones"]:
            kwargs["observaciones"] = kwargs["observaciones"].strip()

        cita.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(cita, key):
                setattr(cita, key, value)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def cancelar_cita(self, cita_id: UUID, id_usuario_edicion: UUID) -> Optional[Cita]:
        """
        Cancelar una cita.

        Args:
            cita_id: UUID de la cita
            id_usuario_edicion: UUID del usuario que cancela

        Returns:
            Cita cancelada o None
        """
        return self.actualizar_cita(cita_id, id_usuario_edicion, estado="Cancelada")

    def completar_cita(self, cita_id: UUID, id_usuario_edicion: UUID) -> Optional[Cita]:
        """
        Marcar una cita como completada.

        Args:
            cita_id: UUID de la cita
            id_usuario_edicion: UUID del usuario que completa

        Returns:
            Cita completada o None
        """
        return self.actualizar_cita(cita_id, id_usuario_edicion, estado="Completada")

    def eliminar_cita(self, cita_id: UUID) -> bool:
        """
        Eliminar una cita.

        Args:
            cita_id: UUID de la cita

        Returns:
            True si se eliminó, False si no existe
        """
        cita = self.obtener_cita(cita_id)
        if cita:
            self.db.delete(cita)
            self.db.commit()
            return True
        return False
