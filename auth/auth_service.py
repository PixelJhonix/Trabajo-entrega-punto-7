"""Servicio de autenticación."""

import re
from typing import Optional
from uuid import UUID

from entities.usuario import Usuario
from .security import PasswordManager
from sqlalchemy.orm import Session


class AuthService:
    """Servicio de autenticación y gestión de usuarios."""

    def __init__(self, db: Session):
        self.db = db
        self.usuario_actual: Optional[Usuario] = None

    def _validar_email(self, email: str) -> bool:
        """Validar formato de email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """Validar formato de teléfono."""
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def _validar_nombre_usuario(self, nombre_usuario: str) -> bool:
        """Validar formato de nombre de usuario."""
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return re.match(pattern, nombre_usuario) is not None

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
            nombre: Nombre del usuario
            nombre_usuario: Nombre de usuario único
            email: Email válido y único
            contraseña: Contraseña segura
            id_usuario_creacion: UUID del usuario que crea
            telefono: Teléfono opcional
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

        if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
            raise ValueError(
                "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
            )

        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")

        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        if not contraseña:
            raise ValueError("La contraseña es obligatoria")

        es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
        if not es_valida:
            raise ValueError(f"Contraseña inválida: {mensaje}")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        contraseña_hash = PasswordManager.hash_password(contraseña)

        usuario = Usuario(
            nombre=nombre.strip(),
            nombre_usuario=nombre_usuario.strip().lower(),
            email=email.lower().strip(),
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

    def autenticar_usuario(
        self, nombre_usuario: str, contraseña: str
    ) -> Optional[Usuario]:
        """
        Autenticar un usuario con nombre de usuario y contraseña.

        Args:
            nombre_usuario: Nombre de usuario o email
            contraseña: Contraseña en texto plano

        Returns:
            Usuario autenticado o None si las credenciales son inválidas
        """
        # Buscar por nombre de usuario o email
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_usuario_por_email(nombre_usuario)

        if not usuario or not usuario.activo:
            return None

        if PasswordManager.verify_password(contraseña, usuario.contraseña_hash):
            return usuario

        return None

    def cambiar_contraseña(
        self, usuario_id: UUID, contraseña_actual: str, nueva_contraseña: str
    ) -> bool:
        """
        Cambiar la contraseña de un usuario.

        Args:
            usuario_id: UUID del usuario
            contraseña_actual: Contraseña actual
            nueva_contraseña: Nueva contraseña

        Returns:
            True si se cambió exitosamente, False en caso contrario

        Raises:
            ValueError: Si la contraseña actual es incorrecta o la nueva es inválida
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False

        if not PasswordManager.verify_password(
            contraseña_actual, usuario.contraseña_hash
        ):
            raise ValueError("La contraseña actual es incorrecta")

        es_valida, mensaje = PasswordManager.validate_password_strength(
            nueva_contraseña
        )
        if not es_valida:
            raise ValueError(f"Nueva contraseña inválida: {mensaje}")

        usuario.contraseña_hash = PasswordManager.hash_password(nueva_contraseña)
        self.db.commit()
        return True

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> list[Usuario]:
        """
        Obtener lista de usuarios con paginación.

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de usuarios
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()

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

    def crear_admin_por_defecto(self) -> Usuario:
        """
        Crear usuario administrador por defecto.

        Returns:
            Usuario administrador creado
        """
        admin_existente = (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@hospital.com", Usuario.es_admin == True)
            .first()
        )

        if admin_existente:
            return admin_existente

        contraseña_hash = PasswordManager.hash_password("admin123")

        admin = Usuario(
            nombre="Administrador del Sistema",
            nombre_usuario="admin",
            email="admin@hospital.com",
            contraseña_hash=contraseña_hash,
            es_admin=True,
            id_usuario_creacion=UUID("00000000-0000-0000-0000-000000000000"),
        )
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    def autenticar_usuario(
        self, identificador: str, contraseña: str
    ) -> Optional[Usuario]:
        """
        Autentica un usuario usando nombre de usuario o email y contraseña.

        Args:
            identificador: Nombre de usuario o email.
            contraseña: Contraseña en texto plano.

        Returns:
            El objeto Usuario si la autenticación es exitosa, None en caso contrario.
        """
        usuario = self.obtener_usuario_por_nombre_usuario(identificador)
        if not usuario:
            usuario = self.obtener_usuario_por_email(identificador)

        if (
            usuario
            and usuario.activo
            and PasswordManager.verify_password(contraseña, usuario.contraseña_hash)
        ):
            self.usuario_actual = usuario
            return usuario
        return None

    def logout(self):
        """
        Cierra la sesión del usuario actual.
        """
        self.usuario_actual = None

    def get_current_user(self) -> Optional[Usuario]:
        """
        Obtiene el usuario actualmente autenticado.
        """
        return self.usuario_actual

    def is_admin(self) -> bool:
        """
        Verifica si el usuario actual es administrador.
        """
        return self.usuario_actual and self.usuario_actual.es_admin
