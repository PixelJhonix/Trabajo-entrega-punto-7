from typing import List, Optional
from uuid import UUID

from entities.historial_medico import HistorialMedico
from sqlalchemy.orm import Session


class HistorialMedicoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_historial(
        self,
        numero_historial: str,
        paciente_id: UUID,
        id_usuario_creacion: Optional[UUID] = None,
        notas_generales: str = None,
    ) -> HistorialMedico:
        """Crear un nuevo historial médico."""
        from entities.paciente import Paciente

        paciente = self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise ValueError("El paciente especificado no existe")

        if not numero_historial or len(numero_historial.strip()) == 0:
            raise ValueError("El número de historial es obligatorio")

        historial_existente = self.obtener_historial_por_numero(numero_historial)
        if historial_existente:
            raise ValueError("El número de historial ya está registrado")

        historial_paciente = self.obtener_historial_por_paciente(paciente_id)
        if historial_paciente and historial_paciente.activo:
            raise ValueError("El paciente ya tiene un historial médico activo")

        historial = HistorialMedico(
            numero_historial=numero_historial.strip(),
            paciente_id=paciente_id,
            notas_generales=notas_generales.strip() if notas_generales else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(historial)
        self.db.commit()
        self.db.refresh(historial)
        return historial

    def obtener_historiales(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[HistorialMedico]:
        """Obtener todos los historiales médicos con opción de incluir inactivos."""
        query = self.db.query(HistorialMedico)
        if not include_inactive:
            query = query.filter(HistorialMedico.activo == True)
        return query.offset(skip).limit(limit).all()

    def obtener_historial(self, historial_id: UUID) -> Optional[HistorialMedico]:
        """Obtener un historial médico por ID."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.id == historial_id)
            .first()
        )

    def obtener_historial_por_numero(
        self, numero_historial: str
    ) -> Optional[HistorialMedico]:
        """Obtener un historial médico por número."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.numero_historial == numero_historial)
            .first()
        )

    def obtener_historial_por_paciente(
        self, paciente_id: UUID
    ) -> Optional[HistorialMedico]:
        """Obtener historial médico por paciente."""
        return (
            self.db.query(HistorialMedico)
            .filter(
                HistorialMedico.paciente_id == paciente_id,
                HistorialMedico.activo == True,
            )
            .first()
        )

    def obtener_historiales_por_estado(self, estado: str) -> List[HistorialMedico]:
        """Obtener historiales médicos por estado."""
        return (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.estado == estado, HistorialMedico.activo == True)
            .all()
        )

    def buscar_historiales_por_numero(self, numero: str) -> List[HistorialMedico]:
        """Buscar historiales médicos por número (búsqueda parcial)."""
        return (
            self.db.query(HistorialMedico)
            .filter(
                HistorialMedico.numero_historial.ilike(f"%{numero}%"),
                HistorialMedico.activo == True,
            )
            .all()
        )

    def actualizar_historial(
        self, historial_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[HistorialMedico]:
        """Actualizar un historial médico."""
        historial = self.obtener_historial(historial_id)
        if historial:
            for key, value in kwargs.items():
                if hasattr(historial, key):
                    setattr(historial, key, value)
            if id_usuario_edicion:
                historial.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(historial)
        return historial

    def cerrar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[HistorialMedico]:
        """Cerrar un historial médico."""
        return self.actualizar_historial(
            historial_id, id_usuario_edicion, estado="cerrado"
        )

    def archivar_historial(
        self, historial_id: UUID, id_usuario_edicion: UUID
    ) -> Optional[HistorialMedico]:
        """Archivar un historial médico."""
        return self.actualizar_historial(
            historial_id, id_usuario_edicion, estado="archivado"
        )

    def eliminar_historial(self, historial_id: UUID) -> bool:
        """Eliminar un historial médico (soft delete)."""
        historial = self.obtener_historial(historial_id)
        if historial:
            historial.activo = False
            self.db.commit()
            return True
        return False
