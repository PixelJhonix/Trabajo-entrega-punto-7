"""Operaciones CRUD para Enfermera."""

import re
from typing import List, Optional
from uuid import UUID

from entities.enfermera import Enfermera
from sqlalchemy.orm import Session


class EnfermeraCRUD:
    """CRUD para gestión de enfermeras."""

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

    def _validar_turno(self, turno: str) -> bool:
        """Validar turno de trabajo."""
        turnos_validos = ["Mañana", "Tarde", "Noche"]
        return turno in turnos_validos

    def crear_enfermera(
        self,
        primer_nombre: str,
        apellido: str,
        fecha_nacimiento: str,
        numero_licencia: str,
        turno: str,
        telefono: str,
        direccion: str,
        id_usuario_creacion: UUID,
        segundo_nombre: str = None,
        especialidad: str = None,
        email: str = None,
    ) -> Enfermera:
        """
        Crear una nueva enfermera con validaciones.

        Args:
            primer_nombre: Primer nombre de la enfermera
            apellido: Apellido de la enfermera
            fecha_nacimiento: Fecha de nacimiento (YYYY-MM-DD)
            numero_licencia: Número de licencia de enfermería
            turno: Turno de trabajo (Mañana, Tarde, Noche)
            telefono: Número de teléfono
            direccion: Dirección de residencia
            id_usuario_creacion: UUID del usuario que crea
            segundo_nombre: Segundo nombre opcional
            especialidad: Especialidad opcional
            email: Email opcional

        Returns:
            Enfermera creada

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

        if not numero_licencia or len(numero_licencia.strip()) == 0:
            raise ValueError("El número de licencia es obligatorio")

        if len(numero_licencia) > 50:
            raise ValueError("El número de licencia no puede exceder 50 caracteres")

        if self.obtener_enfermera_por_licencia(numero_licencia):
            raise ValueError("El número de licencia ya está registrado")

        if not turno or not self._validar_turno(turno):
            raise ValueError("El turno debe ser: Mañana, Tarde o Noche")

        if not telefono or not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        if not direccion or len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres")

        if len(direccion) > 500:
            raise ValueError("La dirección no puede exceder 500 caracteres")

        if email and not self._validar_email(email):
            raise ValueError("Email inválido")

        if email and self.obtener_enfermera_por_email(email):
            raise ValueError("El email ya está registrado")

        enfermera = Enfermera(
            primer_nombre=primer_nombre.strip(),
            segundo_nombre=segundo_nombre.strip() if segundo_nombre else None,
            apellido=apellido.strip(),
            fecha_nacimiento=fecha_nacimiento,
            especialidad=especialidad.strip() if especialidad else None,
            numero_licencia=numero_licencia.strip(),
            turno=turno.strip(),
            telefono=telefono.strip(),
            email=email.lower().strip() if email else None,
            direccion=direccion.strip(),
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(enfermera)
        self.db.commit()
        self.db.refresh(enfermera)
        return enfermera

    def obtener_enfermera(self, enfermera_id: UUID) -> Optional[Enfermera]:
        """
        Obtener una enfermera por ID.

        Args:
            enfermera_id: UUID de la enfermera

        Returns:
            Enfermera encontrada o None
        """
        return self.db.query(Enfermera).filter(Enfermera.id == enfermera_id).first()

    def obtener_enfermera_por_email(self, email: str) -> Optional[Enfermera]:
        """
        Obtener una enfermera por email.

        Args:
            email: Email de la enfermera

        Returns:
            Enfermera encontrada o None
        """
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.email == email.lower().strip())
            .first()
        )

    def obtener_enfermera_por_licencia(
        self, numero_licencia: str
    ) -> Optional[Enfermera]:
        """
        Obtener una enfermera por número de licencia.

        Args:
            numero_licencia: Número de licencia

        Returns:
            Enfermera encontrada o None
        """
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.numero_licencia == numero_licencia.strip())
            .first()
        )

    def obtener_enfermeras(self, skip: int = 0, limit: int = 100) -> List[Enfermera]:
        """
        Obtener lista de enfermeras con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de enfermeras
        """
        return self.db.query(Enfermera).offset(skip).limit(limit).all()

    def obtener_enfermeras_por_turno(self, turno: str) -> List[Enfermera]:
        """
        Obtener enfermeras por turno.

        Args:
            turno: Turno de trabajo

        Returns:
            Lista de enfermeras del turno
        """
        return self.db.query(Enfermera).filter(Enfermera.turno == turno).all()

    def buscar_enfermeras_por_nombre(self, nombre: str) -> List[Enfermera]:
        """
        Buscar enfermeras por nombre.

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de enfermeras que coinciden
        """
        return (
            self.db.query(Enfermera)
            .filter(
                Enfermera.primer_nombre.contains(nombre)
                | Enfermera.segundo_nombre.contains(nombre)
                | Enfermera.apellido.contains(nombre)
            )
            .all()
        )

    def actualizar_enfermera(
        self, enfermera_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Enfermera]:
        """
        Actualizar una enfermera con validaciones.

        Args:
            enfermera_id: UUID de la enfermera
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Enfermera actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        enfermera = self.obtener_enfermera(enfermera_id)
        if not enfermera:
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

        if "numero_licencia" in kwargs:
            licencia = kwargs["numero_licencia"]
            if not licencia or len(licencia.strip()) == 0:
                raise ValueError("El número de licencia es obligatorio")
            if len(licencia) > 50:
                raise ValueError("El número de licencia no puede exceder 50 caracteres")
            if (
                self.obtener_enfermera_por_licencia(licencia)
                and self.obtener_enfermera_por_licencia(licencia).id != enfermera_id
            ):
                raise ValueError("El número de licencia ya está registrado")
            kwargs["numero_licencia"] = licencia.strip()

        if "turno" in kwargs:
            turno = kwargs["turno"]
            if not turno or not self._validar_turno(turno):
                raise ValueError("El turno debe ser: Mañana, Tarde o Noche")
            kwargs["turno"] = turno.strip()

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
                self.obtener_enfermera_por_email(email)
                and self.obtener_enfermera_por_email(email).id != enfermera_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        enfermera.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(enfermera, key):
                setattr(enfermera, key, value)
        self.db.commit()
        self.db.refresh(enfermera)
        return enfermera

    def eliminar_enfermera(self, enfermera_id: UUID) -> bool:
        """
        Eliminar una enfermera.

        Args:
            enfermera_id: UUID de la enfermera

        Returns:
            True si se eliminó, False si no existe
        """
        try:
            enfermera = self.obtener_enfermera(enfermera_id)
            if enfermera:
                # Verificar si hay hospitalizaciones que referencian a esta enfermera
                from entities.hospitalizacion import Hospitalizacion

                hospitalizaciones = (
                    self.db.query(Hospitalizacion)
                    .filter(Hospitalizacion.enfermera_asignada_id == enfermera_id)
                    .count()
                )

                if hospitalizaciones > 0:
                    raise ValueError(
                        f"No se puede eliminar la enfermera porque tiene {hospitalizaciones} hospitalización(es) asignada(s)"
                    )

                self.db.delete(enfermera)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e
