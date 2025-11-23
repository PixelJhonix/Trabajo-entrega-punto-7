from typing import List, Optional
from uuid import UUID

from auth.security import PasswordManager
from entities.usuario import Usuario
from sqlalchemy.orm import Session


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(
        self,
        nombre: str,
        nombre_usuario: str,
        email: str,
        contraseña: str,
        id_usuario_creacion: Optional[UUID] = None,
        telefono: Optional[str] = None,
        es_admin: bool = False,
    ) -> Usuario:
        """Crea un nuevo usuario con validaciones."""
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not nombre_usuario or len(nombre_usuario.strip()) == 0:
            raise ValueError("El nombre de usuario es obligatorio")
        if len(nombre_usuario) > 50:
            raise ValueError("El nombre de usuario no puede exceder 50 caracteres")

        if not email or len(email.strip()) == 0:
            raise ValueError("El email es obligatorio")
        if len(email) > 150:
            raise ValueError("El email no puede exceder 150 caracteres")

        if not contraseña or len(contraseña.strip()) == 0:
            raise ValueError("La contraseña es obligatoria")

        es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
        if not es_valida:
            raise ValueError(mensaje)

        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        contraseña_hash = PasswordManager.hash_password(contraseña)

        usuario = Usuario(
            nombre=nombre.strip(),
            nombre_usuario=nombre_usuario.strip().lower(),
            email=email.strip().lower(),
            contraseña_hash=contraseña_hash,
            telefono=telefono.strip() if telefono else None,
            es_admin=es_admin,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuarios(
        self, skip: int = 0, limit: int = 1000, include_inactive: bool = False
    ) -> List[Usuario]:
        """Obtener todos los usuarios con opción de incluir inactivos."""
        query = self.db.query(Usuario)
        if not include_inactive:
            query = query.filter(Usuario.activo == True)
        return query.offset(skip).limit(limit).all()

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """Obtener un usuario por ID."""
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Obtener un usuario por email."""
        return self.db.query(Usuario).filter(Usuario.email == email.lower()).first()

    def obtener_usuario_por_nombre_usuario(
        self, nombre_usuario: str
    ) -> Optional[Usuario]:
        """Obtener un usuario por nombre de usuario."""
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower())
            .first()
        )

    def actualizar_usuario(
        self, usuario_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Usuario]:
        """Actualizar un usuario."""
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "nombre_usuario" in kwargs:
            nombre_usuario = kwargs["nombre_usuario"]
            if not nombre_usuario or len(nombre_usuario.strip()) == 0:
                raise ValueError("El nombre de usuario es obligatorio")
            if len(nombre_usuario) > 50:
                raise ValueError("El nombre de usuario no puede exceder 50 caracteres")
            existing_usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
            if existing_usuario and existing_usuario.id != usuario_id:
                raise ValueError(
                    "El nombre de usuario ya está registrado por otro usuario"
                )
            kwargs["nombre_usuario"] = nombre_usuario.strip().lower()

        if "email" in kwargs:
            email = kwargs["email"]
            if not email or len(email.strip()) == 0:
                raise ValueError("El email es obligatorio")
            if len(email) > 150:
                raise ValueError("El email no puede exceder 150 caracteres")
            existing_usuario = self.obtener_usuario_por_email(email)
            if existing_usuario and existing_usuario.id != usuario_id:
                raise ValueError("El email ya está registrado por otro usuario")
            kwargs["email"] = email.strip().lower()

        if "contraseña" in kwargs:
            contraseña = kwargs["contraseña"]
            if not contraseña or len(contraseña.strip()) == 0:
                raise ValueError("La contraseña es obligatoria")
            es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
            if not es_valida:
                raise ValueError(mensaje)
            kwargs["contraseña_hash"] = PasswordManager.hash_password(contraseña)
            del kwargs["contraseña"]

        if "telefono" in kwargs and kwargs["telefono"]:
            telefono = kwargs["telefono"]
            if len(telefono) > 20:
                raise ValueError("El teléfono no puede exceder 20 caracteres")
            kwargs["telefono"] = telefono.strip()
        elif "telefono" in kwargs and not kwargs["telefono"]:
            kwargs["telefono"] = None

        if id_usuario_edicion:
            usuario.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """Eliminar un usuario (soft delete)."""
        try:
            usuario = self.obtener_usuario(usuario_id)
            if not usuario:
                return False

            if not usuario.activo:
                return True

            usuario.activo = False
            self.db.commit()
            self.db.refresh(usuario)
            return True
        except Exception as e:
            self.db.rollback()
            raise e

    def cambiar_estado_usuario(
        self, usuario_id: UUID, activo: bool, id_usuario_edicion: UUID
    ) -> Optional[Usuario]:
        """Cambiar el estado activo/inactivo de un usuario."""
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            usuario.activo = activo
            usuario.id_usuario_edicion = id_usuario_edicion
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def autenticar_usuario(
        self, nombre_usuario: str, contraseña: str
    ) -> Optional[Usuario]:
        """Autenticar un usuario por nombre de usuario o email."""
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_usuario_por_email(nombre_usuario)

        if not usuario or not usuario.activo:
            return None

        if PasswordManager.verify_password(contraseña, usuario.contraseña_hash):
            return usuario

        return None

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """Obtener todos los usuarios administradores."""
        return (
            self.db.query(Usuario)
            .filter(Usuario.es_admin == True, Usuario.activo == True)
            .all()
        )

    def es_admin(self, usuario_id: UUID) -> bool:
        """Verificar si un usuario es administrador."""
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False
