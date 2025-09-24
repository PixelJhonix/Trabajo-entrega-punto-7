"""Operaciones CRUD para Hospitalizacion."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from entities.hospitalizacion import Hospitalizacion
from entities.paciente import Paciente
from entities.medico import Medico
from entities.enfermera import Enfermera
from sqlalchemy.orm import Session


class HospitalizacionCRUD:
    """CRUD para gestión de hospitalizaciones."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_fecha_futura(self, fecha: str) -> bool:
        """Validar que la fecha sea futura."""
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_obj >= datetime.now().date()
        except ValueError:
            return False

    def _validar_fecha_pasada(self, fecha: str) -> bool:
        """Validar que la fecha sea pasada o presente."""
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
            return fecha_obj <= datetime.now().date()
        except ValueError:
            return False

    def crear_hospitalizacion(
        self,
        paciente_id: UUID,
        medico_responsable_id: UUID,
        tipo_cuidado: str,
        descripcion: str,
        numero_habitacion: str,
        tipo_habitacion: str,
        fecha_inicio: str,
        id_usuario_creacion: UUID,
        enfermera_asignada_id: UUID = None,
        fecha_fin: str = None,
        estado: str = "Activa",
    ) -> Hospitalizacion:
        """
        Crear una nueva hospitalización con validaciones.

        Args:
            paciente_id: UUID del paciente
            medico_responsable_id: UUID del médico responsable
            tipo_cuidado: Tipo de cuidado (Intensivo, Intermedio, Básico)
            descripcion: Descripción de la hospitalización
            numero_habitacion: Número de habitación
            tipo_habitacion: Tipo de habitación (Individual, Compartida, ICU)
            fecha_inicio: Fecha de inicio (YYYY-MM-DD)
            id_usuario_creacion: UUID del usuario que crea
            enfermera_asignada_id: UUID de la enfermera asignada (opcional)
            fecha_fin: Fecha de fin (opcional)
            estado: Estado de la hospitalización (default: Activa)

        Returns:
            Hospitalizacion creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validar que el paciente existe
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        # Validar que el médico existe
        medico = (
            self.db.query(Medico).filter(Medico.id == medico_responsable_id).first()
        )
        if not medico:
            raise ValueError("El médico especificado no existe")

        # Validar que la enfermera existe (si se proporciona)
        if enfermera_asignada_id:
            enfermera = (
                self.db.query(Enfermera)
                .filter(Enfermera.id == enfermera_asignada_id)
                .first()
            )
            if not enfermera:
                raise ValueError("La enfermera especificada no existe")

        if not tipo_cuidado or len(tipo_cuidado.strip()) == 0:
            raise ValueError("El tipo de cuidado es obligatorio")

        if len(tipo_cuidado) > 50:
            raise ValueError("El tipo de cuidado no puede exceder 50 caracteres")

        if not descripcion or len(descripcion.strip()) < 10:
            raise ValueError("La descripción debe tener al menos 10 caracteres")

        if not numero_habitacion or len(numero_habitacion.strip()) == 0:
            raise ValueError("El número de habitación es obligatorio")

        if len(numero_habitacion) > 10:
            raise ValueError("El número de habitación no puede exceder 10 caracteres")

        if not tipo_habitacion or len(tipo_habitacion.strip()) == 0:
            raise ValueError("El tipo de habitación es obligatorio")

        if len(tipo_habitacion) > 20:
            raise ValueError("El tipo de habitación no puede exceder 20 caracteres")

        if not fecha_inicio or not self._validar_fecha_pasada(fecha_inicio):
            raise ValueError("La fecha de inicio debe ser válida (YYYY-MM-DD)")

        if fecha_fin and not self._validar_fecha_pasada(fecha_fin):
            raise ValueError("La fecha de fin debe ser válida (YYYY-MM-DD)")

        estados_validos = ["Activa", "Completada", "Cancelada"]
        if estado not in estados_validos:
            raise ValueError(f"El estado debe ser uno de: {', '.join(estados_validos)}")

        # Verificar disponibilidad de la habitación
        hospitalizacion_existente = (
            self.db.query(Hospitalizacion)
            .filter(
                Hospitalizacion.numero_habitacion == numero_habitacion,
                Hospitalizacion.estado == "Activa",
            )
            .first()
        )
        if hospitalizacion_existente:
            raise ValueError("La habitación ya está ocupada")

        hospitalizacion = Hospitalizacion(
            paciente_id=paciente_id,
            medico_responsable_id=medico_responsable_id,
            enfermera_asignada_id=enfermera_asignada_id,
            tipo_cuidado=tipo_cuidado.strip(),
            descripcion=descripcion.strip(),
            numero_habitacion=numero_habitacion.strip(),
            tipo_habitacion=tipo_habitacion.strip(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(hospitalizacion)
        self.db.commit()
        self.db.refresh(hospitalizacion)
        return hospitalizacion

    def obtener_hospitalizacion(
        self, hospitalizacion_id: UUID
    ) -> Optional[Hospitalizacion]:
        """
        Obtener una hospitalización por ID.

        Args:
            hospitalizacion_id: UUID de la hospitalización

        Returns:
            Hospitalizacion encontrada o None
        """
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.id == hospitalizacion_id)
            .first()
        )

    def obtener_hospitalizaciones(
        self, skip: int = 0, limit: int = 100
    ) -> List[Hospitalizacion]:
        """
        Obtener lista de hospitalizaciones con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de hospitalizaciones
        """
        return self.db.query(Hospitalizacion).offset(skip).limit(limit).all()

    def obtener_hospitalizaciones_por_paciente(
        self, paciente_id: UUID
    ) -> List[Hospitalizacion]:
        """
        Obtener hospitalizaciones por paciente.

        Args:
            paciente_id: UUID del paciente

        Returns:
            Lista de hospitalizaciones del paciente
        """
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.paciente_id == paciente_id)
            .all()
        )

    def obtener_hospitalizaciones_por_medico(
        self, medico_id: UUID
    ) -> List[Hospitalizacion]:
        """
        Obtener hospitalizaciones por médico responsable.

        Args:
            medico_id: UUID del médico

        Returns:
            Lista de hospitalizaciones del médico
        """
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.medico_responsable_id == medico_id)
            .all()
        )

    def obtener_hospitalizaciones_por_estado(
        self, estado: str
    ) -> List[Hospitalizacion]:
        """
        Obtener hospitalizaciones por estado.

        Args:
            estado: Estado de las hospitalizaciones

        Returns:
            Lista de hospitalizaciones del estado
        """
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.estado == estado)
            .all()
        )

    def obtener_hospitalizaciones_por_habitacion(
        self, numero_habitacion: str
    ) -> List[Hospitalizacion]:
        """
        Obtener hospitalizaciones por habitación.

        Args:
            numero_habitacion: Número de habitación

        Returns:
            Lista de hospitalizaciones de la habitación
        """
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.numero_habitacion == numero_habitacion)
            .all()
        )

    def actualizar_hospitalizacion(
        self, hospitalizacion_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Hospitalizacion]:
        """
        Actualizar una hospitalización con validaciones.

        Args:
            hospitalizacion_id: UUID de la hospitalización
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Hospitalizacion actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        hospitalizacion = self.obtener_hospitalizacion(hospitalizacion_id)
        if not hospitalizacion:
            return None

        if "tipo_cuidado" in kwargs:
            tipo_cuidado = kwargs["tipo_cuidado"]
            if not tipo_cuidado or len(tipo_cuidado.strip()) == 0:
                raise ValueError("El tipo de cuidado es obligatorio")
            if len(tipo_cuidado) > 50:
                raise ValueError("El tipo de cuidado no puede exceder 50 caracteres")
            kwargs["tipo_cuidado"] = tipo_cuidado.strip()

        if "descripcion" in kwargs:
            descripcion = kwargs["descripcion"]
            if not descripcion or len(descripcion.strip()) < 10:
                raise ValueError("La descripción debe tener al menos 10 caracteres")
            kwargs["descripcion"] = descripcion.strip()

        if "numero_habitacion" in kwargs:
            numero_habitacion = kwargs["numero_habitacion"]
            if not numero_habitacion or len(numero_habitacion.strip()) == 0:
                raise ValueError("El número de habitación es obligatorio")
            if len(numero_habitacion) > 10:
                raise ValueError(
                    "El número de habitación no puede exceder 10 caracteres"
                )
            kwargs["numero_habitacion"] = numero_habitacion.strip()

        if "tipo_habitacion" in kwargs:
            tipo_habitacion = kwargs["tipo_habitacion"]
            if not tipo_habitacion or len(tipo_habitacion.strip()) == 0:
                raise ValueError("El tipo de habitación es obligatorio")
            if len(tipo_habitacion) > 20:
                raise ValueError("El tipo de habitación no puede exceder 20 caracteres")
            kwargs["tipo_habitacion"] = tipo_habitacion.strip()

        if "fecha_inicio" in kwargs:
            fecha_inicio = kwargs["fecha_inicio"]
            if not fecha_inicio or not self._validar_fecha_pasada(fecha_inicio):
                raise ValueError("La fecha de inicio debe ser válida (YYYY-MM-DD)")

        if "fecha_fin" in kwargs and kwargs["fecha_fin"]:
            fecha_fin = kwargs["fecha_fin"]
            if not self._validar_fecha_pasada(fecha_fin):
                raise ValueError("La fecha de fin debe ser válida (YYYY-MM-DD)")

        if "estado" in kwargs:
            estado = kwargs["estado"]
            estados_validos = ["Activa", "Completada", "Cancelada"]
            if estado not in estados_validos:
                raise ValueError(
                    f"El estado debe ser uno de: {', '.join(estados_validos)}"
                )

        hospitalizacion.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(hospitalizacion, key):
                setattr(hospitalizacion, key, value)
        self.db.commit()
        self.db.refresh(hospitalizacion)
        return hospitalizacion

    def completar_hospitalizacion(
        self, hospitalizacion_id: UUID, fecha_fin: str, id_usuario_edicion: UUID
    ) -> Optional[Hospitalizacion]:
        """
        Completar una hospitalización.

        Args:
            hospitalizacion_id: UUID de la hospitalización
            fecha_fin: Fecha de fin (YYYY-MM-DD)
            id_usuario_edicion: UUID del usuario que completa

        Returns:
            Hospitalizacion completada o None
        """
        return self.actualizar_hospitalizacion(
            hospitalizacion_id,
            id_usuario_edicion,
            fecha_fin=fecha_fin,
            estado="Completada",
        )

    def cancelar_hospitalizacion(
        self, hospitalizacion_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[Hospitalizacion]:
        """
        Cancelar una hospitalización.

        Args:
            hospitalizacion_id: UUID de la hospitalización
            id_usuario_edicion: UUID del usuario que cancela

        Returns:
            Hospitalizacion cancelada o None
        """
        return self.actualizar_hospitalizacion(
            hospitalizacion_id, id_usuario_edicion, estado="Cancelada"
        )

    def eliminar_hospitalizacion(self, hospitalizacion_id: UUID) -> bool:
        """
        Eliminar una hospitalización.

        Args:
            hospitalizacion_id: UUID de la hospitalización

        Returns:
            True si se eliminó, False si no existe
        """
        hospitalizacion = self.obtener_hospitalizacion(hospitalizacion_id)
        if hospitalizacion:
            self.db.delete(hospitalizacion)
            self.db.commit()
            return True
        return False
