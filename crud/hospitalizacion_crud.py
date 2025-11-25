from datetime import datetime
from typing import List, Optional
from uuid import UUID

from entities.enfermera import Enfermera
from entities.hospitalizacion import Hospitalizacion
from entities.medico import Medico
from entities.paciente import Paciente
from sqlalchemy.orm import Session


class HospitalizacionCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_hospitalizacion(
        self,
        paciente_id: UUID,
        medico_id: UUID,
        fecha_ingreso: datetime,
        motivo: str,
        numero_habitacion: str,
        id_usuario_creacion: Optional[UUID] = None,
        enfermera_id: Optional[UUID] = None,
        fecha_salida: Optional[datetime] = None,
        notas: Optional[str] = None,
    ) -> Hospitalizacion:
        """Crear una nueva hospitalización."""
        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        medico = self.db.query(Medico).filter(Medico.id == medico_id).first()
        if not medico:
            raise ValueError("El médico especificado no existe")

        if enfermera_id:
            enfermera = (
                self.db.query(Enfermera).filter(Enfermera.id == enfermera_id).first()
            )
            if not enfermera:
                raise ValueError("La enfermera especificada no existe")

        if not motivo or len(motivo.strip()) == 0:
            raise ValueError("El motivo es obligatorio")
        if len(motivo) > 255:
            raise ValueError("El motivo no puede exceder 255 caracteres")

        if not numero_habitacion or len(numero_habitacion.strip()) == 0:
            raise ValueError("El número de habitación es obligatorio")
        if len(numero_habitacion) > 10:
            raise ValueError("El número de habitación no puede exceder 10 caracteres")

        hospitalizacion_existente = (
            self.db.query(Hospitalizacion)
            .filter(
                Hospitalizacion.numero_habitacion == numero_habitacion,
                Hospitalizacion.estado == "activa",
                Hospitalizacion.activo == True,
            )
            .first()
        )
        if hospitalizacion_existente:
            raise ValueError("La habitación ya está ocupada")

        hospitalizacion = Hospitalizacion(
            paciente_id=paciente_id,
            medico_id=medico_id,
            enfermera_id=enfermera_id,
            fecha_ingreso=fecha_ingreso,
            fecha_salida=fecha_salida,
            motivo=motivo.strip(),
            numero_habitacion=numero_habitacion.strip(),
            notas=notas.strip() if notas else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(hospitalizacion)
        self.db.commit()
        self.db.refresh(hospitalizacion)
        return hospitalizacion

    def obtener_hospitalizaciones(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[Hospitalizacion]:
        """Obtener todas las hospitalizaciones con opción de incluir inactivas."""
        query = self.db.query(Hospitalizacion)
        if not include_inactive:
            query = query.filter(Hospitalizacion.activo == True)
        return query.offset(skip).limit(limit).all()

    def obtener_hospitalizacion(
        self, hospitalizacion_id: UUID
    ) -> Optional[Hospitalizacion]:
        """Obtener una hospitalización por ID."""
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.id == hospitalizacion_id)
            .first()
        )

    def obtener_hospitalizaciones_por_paciente(
        self, paciente_id: UUID
    ) -> List[Hospitalizacion]:
        """Obtener hospitalizaciones por paciente."""
        return (
            self.db.query(Hospitalizacion)
            .filter(
                Hospitalizacion.paciente_id == paciente_id,
                Hospitalizacion.activo == True,
            )
            .all()
        )

    def obtener_hospitalizaciones_por_medico(
        self, medico_id: UUID
    ) -> List[Hospitalizacion]:
        """Obtener hospitalizaciones por médico."""
        return (
            self.db.query(Hospitalizacion)
            .filter(
                Hospitalizacion.medico_id == medico_id, Hospitalizacion.activo == True
            )
            .all()
        )

    def obtener_hospitalizaciones_por_habitacion(
        self, numero_habitacion: str
    ) -> List[Hospitalizacion]:
        """Obtener hospitalizaciones por número de habitación."""
        return (
            self.db.query(Hospitalizacion)
            .filter(
                Hospitalizacion.numero_habitacion == numero_habitacion,
                Hospitalizacion.activo == True,
            )
            .all()
        )

    def obtener_hospitalizaciones_por_estado(
        self, estado: str
    ) -> List[Hospitalizacion]:
        """Obtener hospitalizaciones por estado."""
        return (
            self.db.query(Hospitalizacion)
            .filter(Hospitalizacion.estado == estado, Hospitalizacion.activo == True)
            .all()
        )

    def actualizar_hospitalizacion(
        self,
        hospitalizacion_id: UUID,
        id_usuario_edicion: Optional[UUID] = None,
        **kwargs
    ) -> Optional[Hospitalizacion]:
        """Actualizar una hospitalización."""
        hospitalizacion = self.obtener_hospitalizacion(hospitalizacion_id)
        if not hospitalizacion:
            return None

        if "motivo" in kwargs:
            motivo = kwargs["motivo"]
            if not motivo or len(motivo.strip()) == 0:
                raise ValueError("El motivo es obligatorio")
            if len(motivo) > 255:
                raise ValueError("El motivo no puede exceder 255 caracteres")
            kwargs["motivo"] = motivo.strip()

        if "numero_habitacion" in kwargs:
            numero_habitacion = kwargs["numero_habitacion"]
            if not numero_habitacion or len(numero_habitacion.strip()) == 0:
                raise ValueError("El número de habitación es obligatorio")
            if len(numero_habitacion) > 10:
                raise ValueError(
                    "El número de habitación no puede exceder 10 caracteres"
                )
            kwargs["numero_habitacion"] = numero_habitacion.strip()

        if id_usuario_edicion:
            hospitalizacion.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(hospitalizacion, key):
                setattr(hospitalizacion, key, value)
        self.db.commit()
        self.db.refresh(hospitalizacion)
        return hospitalizacion

    def completar_hospitalizacion(
        self, hospitalizacion_id: UUID, fecha_salida: datetime, id_usuario_edicion: UUID
    ) -> Optional[Hospitalizacion]:
        """Completar una hospitalización."""
        return self.actualizar_hospitalizacion(
            hospitalizacion_id,
            id_usuario_edicion,
            fecha_salida=fecha_salida,
            estado="completada",
        )

    def cancelar_hospitalizacion(
        self, hospitalizacion_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[Hospitalizacion]:
        """Cancelar una hospitalización."""
        return self.actualizar_hospitalizacion(
            hospitalizacion_id, id_usuario_edicion, estado="cancelada"
        )

    def inactivar_hospitalizacion(self, hospitalizacion_id: UUID) -> bool:
        """Inactivar una hospitalización (soft delete)."""
        hospitalizacion = self.obtener_hospitalizacion(hospitalizacion_id)
        if not hospitalizacion:
            return False
        if not hospitalizacion.activo:
            return True
        hospitalizacion.activo = False
        self.db.commit()
        return True

    def reactivar_hospitalizacion(self, hospitalizacion_id: UUID) -> bool:
        """Reactivar una hospitalización inactiva."""
        hospitalizacion = self.obtener_hospitalizacion(hospitalizacion_id)
        if not hospitalizacion:
            return False
        if hospitalizacion.activo:
            return True
        hospitalizacion.activo = True
        self.db.commit()
        return True

    def eliminar_hospitalizacion_permanente(self, hospitalizacion_id: UUID) -> bool:
        """Eliminar una hospitalización permanentemente de la base de datos."""
        import logging
        try:
            hospitalizacion = self.obtener_hospitalizacion(hospitalizacion_id)
            if not hospitalizacion:
                raise ValueError(f"Hospitalización con ID {hospitalizacion_id} no encontrada")
            
            self.db.delete(hospitalizacion)
            self.db.commit()
            
            logging.info(f"Hospitalización {hospitalizacion_id} eliminada permanentemente")
            return True
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error al eliminar hospitalización permanentemente {hospitalizacion_id}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError(f"Error al eliminar hospitalización: {str(e)}")

    def eliminar_hospitalizacion(self, hospitalizacion_id: UUID) -> bool:
        """Eliminar una hospitalización (soft delete) - mantiene compatibilidad."""
        return self.inactivar_hospitalizacion(hospitalizacion_id)
