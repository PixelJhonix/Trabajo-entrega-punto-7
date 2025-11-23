from typing import List, Optional
from uuid import UUID

from entities.historial_entrada import HistorialEntrada
from sqlalchemy.orm import Session


class HistorialEntradaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_entrada(
        self,
        fecha_consulta,
        diagnostico: str,
        historial_medico_id: UUID,
        medico_id: UUID,
        id_usuario_creacion: Optional[UUID] = None,
        tratamiento: str = None,
        observaciones: str = None,
    ) -> HistorialEntrada:
        """Crear una nueva entrada del historial."""
        from entities.historial_medico import HistorialMedico
        from entities.medico import Medico

        historial = (
            self.db.query(HistorialMedico)
            .filter(HistorialMedico.id == historial_medico_id)
            .first()
        )
        if not historial:
            raise ValueError("El historial médico especificado no existe")

        medico = self.db.query(Medico).filter(Medico.id == medico_id).first()
        if not medico:
            raise ValueError("El médico especificado no existe")

        if not diagnostico or len(diagnostico.strip()) == 0:
            raise ValueError("El diagnóstico es obligatorio")
        if len(diagnostico) > 500:
            raise ValueError("El diagnóstico no puede exceder 500 caracteres")

        entrada = HistorialEntrada(
            fecha_consulta=fecha_consulta,
            diagnostico=diagnostico.strip(),
            historial_medico_id=historial_medico_id,
            medico_id=medico_id,
            tratamiento=tratamiento.strip() if tratamiento else None,
            observaciones=observaciones.strip() if observaciones else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(entrada)
        self.db.commit()
        self.db.refresh(entrada)
        return entrada

    def obtener_entradas(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[HistorialEntrada]:
        """Obtener todas las entradas del historial con opción de incluir inactivas."""
        query = self.db.query(HistorialEntrada)
        if not include_inactive:
            query = query.filter(HistorialEntrada.activo == True)
        return query.offset(skip).limit(limit).all()

    def obtener_entrada(self, entrada_id: UUID) -> Optional[HistorialEntrada]:
        """Obtener una entrada del historial por ID."""
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.id == entrada_id)
            .first()
        )

    def obtener_entradas_por_historial(
        self, historial_id: UUID
    ) -> List[HistorialEntrada]:
        """Obtener entradas por historial médico."""
        return (
            self.db.query(HistorialEntrada)
            .filter(
                HistorialEntrada.historial_medico_id == historial_id,
                HistorialEntrada.activo == True,
            )
            .all()
        )

    def obtener_entradas_por_medico(self, medico_id: UUID) -> List[HistorialEntrada]:
        """Obtener entradas por médico."""
        return (
            self.db.query(HistorialEntrada)
            .filter(
                HistorialEntrada.medico_id == medico_id, HistorialEntrada.activo == True
            )
            .all()
        )

    def buscar_entradas_por_diagnostico(
        self, diagnostico: str
    ) -> List[HistorialEntrada]:
        """Buscar entradas por diagnóstico."""
        return (
            self.db.query(HistorialEntrada)
            .filter(
                HistorialEntrada.diagnostico.ilike(f"%{diagnostico}%"),
                HistorialEntrada.activo == True,
            )
            .all()
        )

    def actualizar_entrada(
        self, entrada_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[HistorialEntrada]:
        """Actualizar una entrada del historial."""
        entrada = self.obtener_entrada(entrada_id)
        if entrada:
            for key, value in kwargs.items():
                if hasattr(entrada, key):
                    setattr(entrada, key, value)
            if id_usuario_edicion:
                entrada.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(entrada)
        return entrada

    def eliminar_entrada(self, entrada_id: UUID) -> bool:
        """Eliminar una entrada del historial (soft delete)."""
        entrada = self.obtener_entrada(entrada_id)
        if entrada:
            entrada.activo = False
            self.db.commit()
            return True
        return False
