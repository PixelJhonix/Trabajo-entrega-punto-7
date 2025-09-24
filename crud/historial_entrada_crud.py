"""Operaciones CRUD para HistorialEntrada."""

from typing import List, Optional
from uuid import UUID

from entities.historial_entrada import HistorialEntrada
from sqlalchemy.orm import Session


class HistorialEntradaCRUD:
    """CRUD para gestión de entradas de historial médico."""

    def __init__(self, db: Session):
        self.db = db

    def crear_entrada(
        self,
        historial_id: UUID,
        medico_id: UUID,
        diagnostico: str,
        tratamiento: str,
        fecha_registro: str,
        id_usuario_creacion: UUID,
        cita_id: UUID = None,
        notas: str = None,
        firma_digital: str = None,
    ) -> HistorialEntrada:
        """
        Crear una nueva entrada de historial.

        Args:
            historial_id: UUID del historial médico
            medico_id: UUID del médico
            diagnostico: Diagnóstico establecido
            tratamiento: Tratamiento prescrito
            fecha_registro: Fecha del registro (YYYY-MM-DD)
            id_usuario_creacion: UUID del usuario que crea
            cita_id: UUID de la cita (opcional)
            notas: Notas adicionales (opcional)
            firma_digital: Firma digital del médico (opcional)

        Returns:
            HistorialEntrada creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not diagnostico or len(diagnostico.strip()) == 0:
            raise ValueError("El diagnóstico es obligatorio")

        if not tratamiento or len(tratamiento.strip()) == 0:
            raise ValueError("El tratamiento es obligatorio")

        if not fecha_registro:
            raise ValueError("La fecha de registro es obligatoria")

        # Validar fecha
        try:
            from datetime import datetime

            datetime.strptime(fecha_registro, "%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener el formato YYYY-MM-DD")

        entrada = HistorialEntrada(
            historial_id=historial_id,
            medico_id=medico_id,
            cita_id=cita_id,
            diagnostico=diagnostico.strip(),
            tratamiento=tratamiento.strip(),
            notas=notas.strip() if notas else None,
            fecha_registro=fecha_registro,
            firma_digital=firma_digital.strip() if firma_digital else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(entrada)
        self.db.commit()
        self.db.refresh(entrada)
        return entrada

    def obtener_entrada(self, entrada_id: UUID) -> Optional[HistorialEntrada]:
        """
        Obtener una entrada por ID.

        Args:
            entrada_id: UUID de la entrada

        Returns:
            HistorialEntrada encontrada o None
        """
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.id == entrada_id)
            .first()
        )

    def obtener_entradas_por_historial(
        self, historial_id: UUID
    ) -> List[HistorialEntrada]:
        """
        Obtener todas las entradas de un historial.

        Args:
            historial_id: UUID del historial

        Returns:
            Lista de entradas
        """
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.historial_id == historial_id)
            .order_by(HistorialEntrada.fecha_registro.desc())
            .all()
        )

    def obtener_entradas_por_medico(self, medico_id: UUID) -> List[HistorialEntrada]:
        """
        Obtener todas las entradas de un médico.

        Args:
            medico_id: UUID del médico

        Returns:
            Lista de entradas
        """
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.medico_id == medico_id)
            .order_by(HistorialEntrada.fecha_registro.desc())
            .all()
        )

    def obtener_entradas(
        self, skip: int = 0, limit: int = 100
    ) -> List[HistorialEntrada]:
        """
        Obtener lista de entradas con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de entradas
        """
        return (
            self.db.query(HistorialEntrada)
            .order_by(HistorialEntrada.fecha_registro.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def buscar_entradas_por_diagnostico(
        self, diagnostico: str
    ) -> List[HistorialEntrada]:
        """
        Buscar entradas por diagnóstico.

        Args:
            diagnostico: Texto a buscar en el diagnóstico

        Returns:
            Lista de entradas que coinciden
        """
        search_pattern = f"%{diagnostico.lower()}%"
        return (
            self.db.query(HistorialEntrada)
            .filter(HistorialEntrada.diagnostico.ilike(search_pattern))
            .order_by(HistorialEntrada.fecha_registro.desc())
            .all()
        )

    def actualizar_entrada(
        self, entrada_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[HistorialEntrada]:
        """
        Actualizar una entrada.

        Args:
            entrada_id: UUID de la entrada
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            HistorialEntrada actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        entrada = self.obtener_entrada(entrada_id)
        if not entrada:
            return None

        if "diagnostico" in kwargs:
            diagnostico = kwargs["diagnostico"]
            if not diagnostico or len(diagnostico.strip()) == 0:
                raise ValueError("El diagnóstico es obligatorio")
            kwargs["diagnostico"] = diagnostico.strip()

        if "tratamiento" in kwargs:
            tratamiento = kwargs["tratamiento"]
            if not tratamiento or len(tratamiento.strip()) == 0:
                raise ValueError("El tratamiento es obligatorio")
            kwargs["tratamiento"] = tratamiento.strip()

        if "fecha_registro" in kwargs:
            fecha_registro = kwargs["fecha_registro"]
            if not fecha_registro:
                raise ValueError("La fecha de registro es obligatoria")
            try:
                from datetime import datetime

                datetime.strptime(fecha_registro, "%Y-%m-%d")
            except ValueError:
                raise ValueError("La fecha debe tener el formato YYYY-MM-DD")

        if "notas" in kwargs and kwargs["notas"]:
            kwargs["notas"] = kwargs["notas"].strip()
        elif "notas" in kwargs and not kwargs["notas"]:
            kwargs["notas"] = None

        if "firma_digital" in kwargs and kwargs["firma_digital"]:
            kwargs["firma_digital"] = kwargs["firma_digital"].strip()
        elif "firma_digital" in kwargs and not kwargs["firma_digital"]:
            kwargs["firma_digital"] = None

        entrada.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(entrada, key):
                setattr(entrada, key, value)
        self.db.commit()
        self.db.refresh(entrada)
        return entrada

    def eliminar_entrada(self, entrada_id: UUID) -> bool:
        """
        Eliminar una entrada.

        Args:
            entrada_id: UUID de la entrada

        Returns:
            True si se eliminó, False si no existe
        """
        entrada = self.obtener_entrada(entrada_id)
        if entrada:
            self.db.delete(entrada)
            self.db.commit()
            return True
        return False
