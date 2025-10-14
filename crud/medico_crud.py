"""Operaciones CRUD para Medico."""

import re
from typing import List, Optional
from uuid import UUID

from entities.medico import Medico
from sqlalchemy.orm import Session


class MedicoCRUD:
    """CRUD para gestión de médicos."""

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

    def crear_medico(
        self,
        primer_nombre: str,
        apellido: str,
        fecha_nacimiento: str,
        especialidad: str,
        numero_licencia: str,
        telefono: str,
        direccion: str,
        id_usuario_creacion: UUID,
        segundo_nombre: str = None,
        consultorio: str = None,
        email: str = None,
    ) -> Medico:
        """
        Crear un nuevo médico con validaciones.

        Args:
            primer_nombre: Primer nombre del médico
            apellido: Apellido del médico
            fecha_nacimiento: Fecha de nacimiento (YYYY-MM-DD)
            especialidad: Especialidad médica
            numero_licencia: Número de licencia médica
            telefono: Número de teléfono
            direccion: Dirección de residencia
            id_usuario_creacion: UUID del usuario que crea
            segundo_nombre: Segundo nombre opcional
            consultorio: Número de consultorio opcional
            email: Email opcional

        Returns:
            Medico creado

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

        if not especialidad or len(especialidad.strip()) == 0:
            raise ValueError("La especialidad es obligatoria")

        if len(especialidad) > 100:
            raise ValueError("La especialidad no puede exceder 100 caracteres")

        if not numero_licencia or len(numero_licencia.strip()) == 0:
            raise ValueError("El número de licencia es obligatorio")

        if len(numero_licencia) > 50:
            raise ValueError("El número de licencia no puede exceder 50 caracteres")

        if self.obtener_medico_por_licencia(numero_licencia):
            raise ValueError("El número de licencia ya está registrado")

        if not telefono or not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        if not direccion or len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres")

        if len(direccion) > 500:
            raise ValueError("La dirección no puede exceder 500 caracteres")

        if email and not self._validar_email(email):
            raise ValueError("Email inválido")

        if email and self.obtener_medico_por_email(email):
            raise ValueError("El email ya está registrado")

        medico = Medico(
            primer_nombre=primer_nombre.strip(),
            segundo_nombre=segundo_nombre.strip() if segundo_nombre else None,
            apellido=apellido.strip(),
            fecha_nacimiento=fecha_nacimiento,
            especialidad=especialidad.strip(),
            numero_licencia=numero_licencia.strip(),
            consultorio=consultorio.strip() if consultorio else None,
            telefono=telefono.strip(),
            email=email.lower().strip() if email else None,
            direccion=direccion.strip(),
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(medico)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def obtener_medico(self, medico_id: UUID) -> Optional[Medico]:
        """
        Obtener un médico por ID.

        Args:
            medico_id: UUID del médico

        Returns:
            Medico encontrado o None
        """
        return self.db.query(Medico).filter(Medico.id == medico_id).first()

    def obtener_medico_por_email(self, email: str) -> Optional[Medico]:
        """
        Obtener un médico por email.

        Args:
            email: Email del médico

        Returns:
            Medico encontrado o None
        """
        return (
            self.db.query(Medico).filter(Medico.email == email.lower().strip()).first()
        )

    def obtener_medico_por_licencia(self, numero_licencia: str) -> Optional[Medico]:
        """
        Obtener un médico por número de licencia.

        Args:
            numero_licencia: Número de licencia

        Returns:
            Medico encontrado o None
        """
        return (
            self.db.query(Medico)
            .filter(Medico.numero_licencia == numero_licencia.strip())
            .first()
        )

    def obtener_medicos(self, skip: int = 0, limit: int = 100) -> List[Medico]:
        """
        Obtener lista de médicos con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de médicos
        """
        return self.db.query(Medico).offset(skip).limit(limit).all()

    def obtener_medicos_por_especialidad(self, especialidad: str) -> List[Medico]:
        """
        Obtener médicos por especialidad.

        Args:
            especialidad: Especialidad médica

        Returns:
            Lista de médicos de la especialidad
        """
        return (
            self.db.query(Medico)
            .filter(Medico.especialidad.contains(especialidad))
            .all()
        )

    def buscar_medicos_por_nombre(self, nombre: str) -> List[Medico]:
        """
        Buscar médicos por nombre.

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de médicos que coinciden
        """
        return (
            self.db.query(Medico)
            .filter(
                Medico.primer_nombre.contains(nombre)
                | Medico.segundo_nombre.contains(nombre)
                | Medico.apellido.contains(nombre)
            )
            .all()
        )

    def actualizar_medico(
        self, medico_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Medico]:
        """
        Actualizar un médico con validaciones.

        Args:
            medico_id: UUID del médico
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Medico actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        medico = self.obtener_medico(medico_id)
        if not medico:
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

        if "especialidad" in kwargs:
            especialidad = kwargs["especialidad"]
            if not especialidad or len(especialidad.strip()) == 0:
                raise ValueError("La especialidad es obligatoria")
            if len(especialidad) > 100:
                raise ValueError("La especialidad no puede exceder 100 caracteres")
            kwargs["especialidad"] = especialidad.strip()

        if "numero_licencia" in kwargs:
            licencia = kwargs["numero_licencia"]
            if not licencia or len(licencia.strip()) == 0:
                raise ValueError("El número de licencia es obligatorio")
            if len(licencia) > 50:
                raise ValueError("El número de licencia no puede exceder 50 caracteres")
            if (
                self.obtener_medico_por_licencia(licencia)
                and self.obtener_medico_por_licencia(licencia).id != medico_id
            ):
                raise ValueError("El número de licencia ya está registrado")
            kwargs["numero_licencia"] = licencia.strip()

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
                self.obtener_medico_por_email(email)
                and self.obtener_medico_por_email(email).id != medico_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        medico.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(medico, key):
                setattr(medico, key, value)
        self.db.commit()
        self.db.refresh(medico)
        return medico

    def eliminar_medico(self, medico_id: UUID) -> bool:
        """
        Eliminar un médico.

        Args:
            medico_id: UUID del médico

        Returns:
            True si se eliminó, False si no existe
        """
        try:
            medico = self.obtener_medico(medico_id)
            if medico:
                from entities.cita import Cita
                from entities.historial_entrada import HistorialEntrada
                from entities.hospitalizacion import Hospitalizacion

                citas = self.db.query(Cita).filter(Cita.medico_id == medico_id).count()
                hospitalizaciones = (
                    self.db.query(Hospitalizacion)
                    .filter(Hospitalizacion.medico_responsable_id == medico_id)
                    .count()
                )
                historiales = (
                    self.db.query(HistorialEntrada)
                    .filter(HistorialEntrada.medico_id == medico_id)
                    .count()
                )

                total_referencias = citas + hospitalizaciones + historiales
                if total_referencias > 0:
                    raise ValueError(
                        f"No se puede eliminar el médico porque tiene {total_referencias} referencia(s) en citas, hospitalizaciones o historiales"
                    )

                self.db.delete(medico)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e
