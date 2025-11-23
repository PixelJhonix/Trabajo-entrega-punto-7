from typing import List, Optional
from uuid import UUID

from entities.enfermera import Enfermera
from sqlalchemy.orm import Session


class EnfermeraCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_enfermera(
        self,
        nombre: str,
        apellido: str,
        email: str,
        numero_licencia: str,
        turno: str,
        id_usuario_creacion: Optional[UUID] = None,
        telefono: Optional[str] = None,
    ) -> Enfermera:
        """Crear una nueva enfermera."""
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        if not apellido or len(apellido.strip()) == 0:
            raise ValueError("El apellido es obligatorio")
        if not email or len(email.strip()) == 0:
            raise ValueError("El email es obligatorio")
        if not numero_licencia or len(numero_licencia.strip()) == 0:
            raise ValueError("El número de licencia es obligatorio")
        if not turno or len(turno.strip()) == 0:
            raise ValueError("El turno es obligatorio")

        if self.obtener_enfermera_por_email(email):
            raise ValueError("El email ya está registrado")
        if self.obtener_enfermera_por_licencia(numero_licencia):
            raise ValueError("El número de licencia ya está registrado")

        enfermera = Enfermera(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            email=email.lower().strip(),
            telefono=telefono.strip() if telefono else None,
            numero_licencia=numero_licencia.strip(),
            turno=turno.strip(),
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(enfermera)
        self.db.commit()
        self.db.refresh(enfermera)
        return enfermera

    def obtener_enfermeras(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[Enfermera]:
        """Obtener todas las enfermeras con opción de incluir inactivas."""
        query = self.db.query(Enfermera)
        if not include_inactive:
            query = query.filter(Enfermera.activo == True)
        return query.offset(skip).limit(limit).all()

    def obtener_enfermera(self, enfermera_id: UUID) -> Optional[Enfermera]:
        """Obtener una enfermera por ID."""
        return self.db.query(Enfermera).filter(Enfermera.id == enfermera_id).first()

    def obtener_enfermera_por_email(self, email: str) -> Optional[Enfermera]:
        """Obtener una enfermera por email."""
        return self.db.query(Enfermera).filter(Enfermera.email == email.lower()).first()

    def obtener_enfermera_por_licencia(
        self, numero_licencia: str
    ) -> Optional[Enfermera]:
        """Obtener una enfermera por número de licencia."""
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.numero_licencia == numero_licencia)
            .first()
        )

    def obtener_enfermeras_por_turno(self, turno: str) -> List[Enfermera]:
        """Obtener enfermeras por turno."""
        return (
            self.db.query(Enfermera)
            .filter(Enfermera.turno == turno, Enfermera.activo == True)
            .all()
        )

    def buscar_enfermeras_por_nombre(self, nombre: str) -> List[Enfermera]:
        """Buscar enfermeras por nombre."""
        return (
            self.db.query(Enfermera)
            .filter(
                Enfermera.nombre.ilike(f"%{nombre}%"),
                Enfermera.activo == True,
            )
            .all()
        )

    def actualizar_enfermera(
        self, enfermera_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Enfermera]:
        """Actualizar una enfermera."""
        enfermera = self.obtener_enfermera(enfermera_id)
        if not enfermera:
            return None

        if "nombre" in kwargs and kwargs["nombre"]:
            if len(kwargs["nombre"].strip()) == 0:
                raise ValueError("El nombre no puede estar vacío")
            kwargs["nombre"] = kwargs["nombre"].strip()

        if "apellido" in kwargs and kwargs["apellido"]:
            if len(kwargs["apellido"].strip()) == 0:
                raise ValueError("El apellido no puede estar vacío")
            kwargs["apellido"] = kwargs["apellido"].strip()

        if "email" in kwargs and kwargs["email"]:
            email = kwargs["email"].lower().strip()
            if len(email) == 0:
                raise ValueError("El email no puede estar vacío")
            existing = self.obtener_enfermera_por_email(email)
            if existing and existing.id != enfermera_id:
                raise ValueError("El email ya está registrado por otra enfermera")
            kwargs["email"] = email

        if "numero_licencia" in kwargs and kwargs["numero_licencia"]:
            licencia = kwargs["numero_licencia"].strip()
            if len(licencia) == 0:
                raise ValueError("El número de licencia no puede estar vacío")
            existing = self.obtener_enfermera_por_licencia(licencia)
            if existing and existing.id != enfermera_id:
                raise ValueError(
                    "El número de licencia ya está registrado por otra enfermera"
                )
            kwargs["numero_licencia"] = licencia

        if "turno" in kwargs and kwargs["turno"]:
            if len(kwargs["turno"].strip()) == 0:
                raise ValueError("El turno no puede estar vacío")
            kwargs["turno"] = kwargs["turno"].strip()

        for key, value in kwargs.items():
            if hasattr(enfermera, key):
                setattr(enfermera, key, value)

        if id_usuario_edicion:
            enfermera.id_usuario_edicion = id_usuario_edicion

        self.db.commit()
        self.db.refresh(enfermera)
        return enfermera

    def eliminar_enfermera(self, enfermera_id: UUID) -> bool:
        """Eliminar una enfermera (soft delete)."""
        enfermera = self.obtener_enfermera(enfermera_id)
        if not enfermera:
            return False

        if not enfermera.activo:
            return False

        enfermera.activo = False
        self.db.commit()
        self.db.refresh(enfermera)
        return True
