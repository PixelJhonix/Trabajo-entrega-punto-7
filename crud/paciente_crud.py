"""Operaciones CRUD para Paciente."""

import re
from typing import List, Optional
from uuid import UUID

from entities.paciente import Paciente
from sqlalchemy.orm import Session


class PacienteCRUD:
    """CRUD para gestión de pacientes."""

    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        """Validar formato de email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """Validar formato de teléfono."""
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def crear_paciente(
        self,
        primer_nombre: str,
        apellido: str,
        fecha_nacimiento: str,
        telefono: str,
        direccion: str,
        id_usuario_creacion: UUID,
        segundo_nombre: str = None,
        email: str = None,
    ) -> Paciente:
        """
        Crear un nuevo paciente con validaciones.

        Args:
            primer_nombre: Primer nombre del paciente
            apellido: Apellido del paciente
            fecha_nacimiento: Fecha de nacimiento (YYYY-MM-DD)
            telefono: Número de teléfono
            direccion: Dirección de residencia
            id_usuario_creacion: UUID del usuario que crea
            segundo_nombre: Segundo nombre opcional
            email: Email opcional

        Returns:
            Paciente creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not primer_nombre or len(primer_nombre.strip()) == 0:
            raise ValueError("El primer nombre es obligatorio")

        if len(primer_nombre) > 100:
            raise ValueError("El primer nombre no puede exceder 100 caracteres")

        if not apellido or len(apellido.strip()) == 0:
            raise ValueError("El apellido es obligatorio")

        if len(apellido) > 100:
            raise ValueError("El apellido no puede exceder 100 caracteres")

        if not fecha_nacimiento:
            raise ValueError("La fecha de nacimiento es obligatoria")

        if not telefono or not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        if not direccion or len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres")

        if len(direccion) > 500:
            raise ValueError("La dirección no puede exceder 500 caracteres")

        if email and not self._validar_email(email):
            raise ValueError("Email inválido")

        if email and self.obtener_paciente_por_email(email):
            raise ValueError("El email ya está registrado")

        paciente = Paciente(
            primer_nombre=primer_nombre.strip(),
            segundo_nombre=segundo_nombre.strip() if segundo_nombre else None,
            apellido=apellido.strip(),
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono.strip(),
            email=email.lower().strip() if email else None,
            direccion=direccion.strip(),
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

    def obtener_paciente(self, paciente_id: UUID) -> Optional[Paciente]:
        """
        Obtener un paciente por ID.

        Args:
            paciente_id: UUID del paciente

        Returns:
            Paciente encontrado o None
        """
        return self.db.query(Paciente).filter(Paciente.id == paciente_id).first()

    def obtener_paciente_por_email(self, email: str) -> Optional[Paciente]:
        """
        Obtener un paciente por email.

        Args:
            email: Email del paciente

        Returns:
            Paciente encontrado o None
        """
        return (
            self.db.query(Paciente)
            .filter(Paciente.email == email.lower().strip())
            .first()
        )

    def obtener_pacientes(self, skip: int = 0, limit: int = 100) -> List[Paciente]:
        """
        Obtener lista de pacientes con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de pacientes
        """
        return self.db.query(Paciente).offset(skip).limit(limit).all()

    def buscar_pacientes_por_nombre(self, nombre: str) -> List[Paciente]:
        """
        Buscar pacientes por nombre.

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de pacientes que coinciden
        """
        return (
            self.db.query(Paciente)
            .filter(
                Paciente.primer_nombre.contains(nombre)
                | Paciente.segundo_nombre.contains(nombre)
                | Paciente.apellido.contains(nombre)
            )
            .all()
        )

    def actualizar_paciente(
        self, paciente_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Paciente]:
        """
        Actualizar un paciente con validaciones.

        Args:
            paciente_id: UUID del paciente
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Paciente actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        paciente = self.obtener_paciente(paciente_id)
        if not paciente:
            return None

        if "primer_nombre" in kwargs:
            nombre = kwargs["primer_nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El primer nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El primer nombre no puede exceder 100 caracteres")
            kwargs["primer_nombre"] = nombre.strip()

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not apellido or len(apellido.strip()) == 0:
                raise ValueError("El apellido es obligatorio")
            if len(apellido) > 100:
                raise ValueError("El apellido no puede exceder 100 caracteres")
            kwargs["apellido"] = apellido.strip()

        if "telefono" in kwargs:
            telefono = kwargs["telefono"]
            if not telefono or not self._validar_telefono(telefono):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = telefono.strip()

        if "direccion" in kwargs:
            direccion = kwargs["direccion"]
            if not direccion or len(direccion.strip()) < 3:
                raise ValueError("La dirección debe tener al menos 3 caracteres")
            if len(direccion) > 500:
                raise ValueError("La dirección no puede exceder 500 caracteres")
            kwargs["direccion"] = direccion.strip()

        if "email" in kwargs and kwargs["email"]:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_paciente_por_email(email)
                and self.obtener_paciente_por_email(email).id != paciente_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        paciente.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(paciente, key):
                setattr(paciente, key, value)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

    def eliminar_paciente(self, paciente_id: UUID) -> bool:
        """
        Eliminar un paciente.

        Args:
            paciente_id: UUID del paciente

        Returns:
            True si se eliminó, False si no existe
        """
        try:
            paciente = self.obtener_paciente(paciente_id)
            if paciente:
                # Verificar si hay referencias a este paciente
                from entities.cita import Cita
                from entities.factura import Factura
                from entities.historial_medico import HistorialMedico
                from entities.hospitalizacion import Hospitalizacion

                citas = (
                    self.db.query(Cita).filter(Cita.paciente_id == paciente_id).count()
                )
                hospitalizaciones = (
                    self.db.query(Hospitalizacion)
                    .filter(Hospitalizacion.paciente_id == paciente_id)
                    .count()
                )
                facturas = (
                    self.db.query(Factura)
                    .filter(Factura.paciente_id == paciente_id)
                    .count()
                )
                historiales = (
                    self.db.query(HistorialMedico)
                    .filter(HistorialMedico.paciente_id == paciente_id)
                    .count()
                )

                total_referencias = citas + hospitalizaciones + facturas + historiales
                if total_referencias > 0:
                    raise ValueError(
                        f"No se puede eliminar el paciente porque tiene {total_referencias} referencia(s) en citas, hospitalizaciones, facturas o historiales"
                    )

                self.db.delete(paciente)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e
