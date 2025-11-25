from typing import List, Optional
from uuid import UUID

from entities.cita import Cita
from sqlalchemy.orm import Session


class CitaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cita(
        self,
        fecha_cita,
        motivo: str,
        paciente_id: UUID,
        medico_id: UUID,
        id_usuario_creacion: Optional[UUID] = None,
        notas: str = None,
    ) -> Cita:
        """Crear una nueva cita."""
        from entities.medico import Medico
        from entities.paciente import Paciente

        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        medico = self.db.query(Medico).filter(Medico.id == medico_id).first()
        if not medico:
            raise ValueError("El médico especificado no existe")

        if not motivo or len(motivo.strip()) == 0:
            raise ValueError("El motivo es obligatorio")
        if len(motivo) > 255:
            raise ValueError("El motivo no puede exceder 255 caracteres")

        cita = Cita(
            fecha_cita=fecha_cita,
            motivo=motivo.strip(),
            paciente_id=paciente_id,
            medico_id=medico_id,
            notas=notas.strip() if notas else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(cita)
        self.db.commit()
        self.db.refresh(cita)
        return cita

    def obtener_citas(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[Cita]:
        """Obtener todas las citas con opción de incluir inactivas."""
        query = self.db.query(Cita)
        if not include_inactive:
            query = query.filter(Cita.activo == True)
        return query.offset(skip).limit(limit).all()

    def obtener_cita(self, cita_id: UUID) -> Optional[Cita]:
        """Obtener una cita por ID."""
        return self.db.query(Cita).filter(Cita.id == cita_id).first()

    def obtener_citas_por_paciente(self, paciente_id: UUID) -> List[Cita]:
        """Obtener citas por paciente."""
        return (
            self.db.query(Cita)
            .filter(Cita.paciente_id == paciente_id, Cita.activo == True)
            .all()
        )

    def obtener_citas_por_medico(self, medico_id: UUID) -> List[Cita]:
        """Obtener citas por médico."""
        return (
            self.db.query(Cita)
            .filter(Cita.medico_id == medico_id, Cita.activo == True)
            .all()
        )

    def obtener_citas_por_fecha(self, fecha) -> List[Cita]:
        """Obtener citas por fecha."""
        return (
            self.db.query(Cita)
            .filter(Cita.fecha_cita.date() == fecha, Cita.activo == True)
            .all()
        )

    def obtener_citas_por_estado(self, estado: str) -> List[Cita]:
        """Obtener citas por estado."""
        return (
            self.db.query(Cita).filter(Cita.estado == estado, Cita.activo == True).all()
        )

    def actualizar_cita(
        self, cita_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Cita]:
        """Actualizar una cita."""
        cita = self.obtener_cita(cita_id)
        if cita:
            for key, value in kwargs.items():
                if hasattr(cita, key):
                    setattr(cita, key, value)
            if id_usuario_edicion:
                cita.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(cita)
        return cita

    def cancelar_cita(self, cita_id: UUID, id_usuario_edicion: UUID) -> Optional[Cita]:
        """Cancelar una cita."""
        return self.actualizar_cita(cita_id, id_usuario_edicion, estado="cancelada")

    def completar_cita(self, cita_id: UUID, id_usuario_edicion: UUID) -> Optional[Cita]:
        """Completar una cita."""
        return self.actualizar_cita(cita_id, id_usuario_edicion, estado="completada")

    def inactivar_cita(self, cita_id: UUID) -> bool:
        """Inactivar una cita (soft delete)."""
        cita = self.obtener_cita(cita_id)
        if not cita:
            return False
        if not cita.activo:
            return True
        cita.activo = False
        self.db.commit()
        return True

    def reactivar_cita(self, cita_id: UUID) -> bool:
        """Reactivar una cita inactiva."""
        cita = self.obtener_cita(cita_id)
        if not cita:
            return False
        if cita.activo:
            return True
        cita.activo = True
        self.db.commit()
        return True

    def eliminar_cita_permanente(self, cita_id: UUID) -> bool:
        """Eliminar una cita permanentemente de la base de datos."""
        import logging
        try:
            cita = self.obtener_cita(cita_id)
            if not cita:
                raise ValueError(f"Cita con ID {cita_id} no encontrada")
            
            self.db.delete(cita)
            self.db.commit()
            
            logging.info(f"Cita {cita_id} eliminada permanentemente")
            return True
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error al eliminar cita permanentemente {cita_id}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError(f"Error al eliminar cita: {str(e)}")

    def eliminar_cita(self, cita_id: UUID) -> bool:
        """Eliminar una cita (soft delete) - mantiene compatibilidad."""
        return self.inactivar_cita(cita_id)
