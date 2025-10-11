"""Operaciones CRUD para Usuario."""

from typing import List, Optional
from uuid import UUID

from auth.security import PasswordManager
from entities.usuario import Usuario
from sqlalchemy.orm import Session


class UsuarioCRUD:
    """CRUD para gestión de usuarios."""

    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(
        self,
        nombre: str,
        nombre_usuario: str,
        email: str,
        contraseña: str,
        id_usuario_creacion: UUID,
        telefono: str = None,
        es_admin: bool = False,
    ) -> Usuario:
        """
        Crear un nuevo usuario con validaciones.

        Args:
            nombre: Nombre completo del usuario
            nombre_usuario: Nombre de usuario único
            email: Email único del usuario
            contraseña: Contraseña en texto plano
            id_usuario_creacion: UUID del usuario que crea
            telefono: Teléfono del usuario (opcional)
            es_admin: Si es administrador

        Returns:
            Usuario creado

        Raises:
            ValueError: Si los datos no son válidos
        """
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

        # Validar fortaleza de contraseña
        es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
        if not es_valida:
            raise ValueError(mensaje)

        # Verificar unicidad de nombre_usuario
        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        # Verificar unicidad de email
        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        # Hash de la contraseña
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

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """
        Obtener un usuario por ID.

        Args:
            usuario_id: UUID del usuario

        Returns:
            Usuario encontrado o None
        """
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_nombre_usuario(
        self, nombre_usuario: str
    ) -> Optional[Usuario]:
        """
        Obtener un usuario por nombre de usuario.

        Args:
            nombre_usuario: Nombre de usuario

        Returns:
            Usuario encontrado o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower().strip())
            .first()
        )

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtener un usuario por email.

        Args:
            email: Email del usuario

        Returns:
            Usuario encontrado o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Obtener lista de usuarios con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de usuarios
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def buscar_usuarios_por_nombre(self, nombre: str) -> List[Usuario]:
        """
        Buscar usuarios por nombre.

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de usuarios que coinciden
        """
        search_pattern = f"%{nombre.lower()}%"
        return self.db.query(Usuario).filter(Usuario.nombre.ilike(search_pattern)).all()

    def actualizar_usuario(
        self, usuario_id: UUID, id_usuario_edicion: UUID, **kwargs
    ) -> Optional[Usuario]:
        """
        Actualizar un usuario con validaciones.

        Args:
            usuario_id: UUID del usuario
            id_usuario_edicion: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Usuario actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
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
            # Verificar unicidad del nombre_usuario, excluyendo al propio usuario
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
            # Verificar unicidad del email, excluyendo al propio usuario
            existing_usuario = self.obtener_usuario_por_email(email)
            if existing_usuario and existing_usuario.id != usuario_id:
                raise ValueError("El email ya está registrado por otro usuario")
            kwargs["email"] = email.strip().lower()

        if "contraseña" in kwargs:
            contraseña = kwargs["contraseña"]
            if not contraseña or len(contraseña.strip()) == 0:
                raise ValueError("La contraseña es obligatoria")
            # Validar fortaleza de contraseña
            es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
            if not es_valida:
                raise ValueError(mensaje)
            # Hash de la contraseña
            kwargs["contraseña_hash"] = PasswordManager.hash_password(contraseña)
            del kwargs["contraseña"]  # Eliminar la contraseña en texto plano

        if "telefono" in kwargs and kwargs["telefono"]:
            telefono = kwargs["telefono"]
            if len(telefono) > 20:
                raise ValueError("El teléfono no puede exceder 20 caracteres")
            kwargs["telefono"] = telefono.strip()
        elif "telefono" in kwargs and not kwargs["telefono"]:
            kwargs["telefono"] = None  # Permitir borrar el teléfono

        usuario.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """
        Eliminar un usuario.

        Args:
            usuario_id: UUID del usuario

        Returns:
            True si se eliminó, False si no existe
        """
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def cambiar_estado_usuario(
        self, usuario_id: UUID, activo: bool, id_usuario_edicion: UUID
    ) -> Optional[Usuario]:
        """
        Cambiar el estado activo/inactivo de un usuario.

        Args:
            usuario_id: UUID del usuario
            activo: Nuevo estado
            id_usuario_edicion: UUID del usuario que hace el cambio

        Returns:
            Usuario actualizado o None
        """
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
        """
        Autenticar un usuario con nombre de usuario/email y contraseña.

        Args:
            nombre_usuario: Nombre de usuario o email
            contraseña: Contraseña en texto plano

        Returns:
            Usuario autenticado o None
        """
        # Buscar por nombre de usuario o email
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_usuario_por_email(nombre_usuario)

        if not usuario or not usuario.activo:
            return None

        # Verificar contraseña
        if PasswordManager.verify_password(contraseña, usuario.contraseña_hash):
            return usuario

        return None

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """
        Obtener el usuario administrador por defecto.

        Returns:
            Usuario admin por defecto o None
        """
        return (
            self.db.query(Usuario)
            .filter(
                Usuario.nombre_usuario == "admin",
                Usuario.email == "admin@system.com",
                Usuario.es_admin == True,
            )
            .first()
        )

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """
        Obtener todos los usuarios administradores.

        Returns:
            Lista de usuarios administradores
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.es_admin == True, Usuario.activo == True)
            .all()
        )

    def es_admin(self, usuario_id: UUID) -> bool:
        """
        Verificar si un usuario es administrador.

        Args:
            usuario_id: UUID del usuario

        Returns:
            True si es administrador, False en caso contrario
        """
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False
