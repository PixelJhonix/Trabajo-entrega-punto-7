from typing import List
from uuid import UUID

from crud.usuario_crud import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import (
    RespuestaAPI,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from sqlalchemy.orm import Session
from utils.error_handler import APIErrorHandler

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
async def obtener_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir usuarios inactivos"),
    email: str = Query(None, description="Filtrar por email (búsqueda parcial)"),
    nombre: str = Query(None, description="Filtrar por nombre (búsqueda parcial)"),
    activo: bool = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los usuarios con paginación, opción de incluir inactivos y filtros de búsqueda."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuarios = usuario_crud.obtener_usuarios(
            skip=skip, 
            limit=limit, 
            include_inactive=include_inactive,
            email=email,
            nombre=nombre,
            activo=activo
        )
        if not usuarios:
            return []
        return usuarios
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/email/{email}", response_model=UsuarioResponse)
async def obtener_usuario_por_email(email: str, db: Session = Depends(get_db)):
    """Obtener un usuario por email."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario_por_email(email)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.get("/username/{nombre_usuario}", response_model=UsuarioResponse)
async def obtener_usuario_por_nombre_usuario(
    nombre_usuario: str, db: Session = Depends(get_db)
):
    """Obtener un usuario por nombre de usuario."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.get("/admin/lista", response_model=List[UsuarioResponse])
async def obtener_usuarios_admin(db: Session = Depends(get_db)):
    """Obtener todos los usuarios administradores."""
    try:
        usuario_crud = UsuarioCRUD(db)
        admins = usuario_crud.obtener_usuarios_admin()
        return admins
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener administradores: {str(e)}",
        )


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.crear_usuario(
            nombre=usuario_data.nombre,
            nombre_usuario=usuario_data.nombre_usuario,
            email=usuario_data.email,
            contraseña=usuario_data.contraseña,
            id_usuario_creacion=(
                usuario_data.id_usuario_creacion
                if usuario_data.id_usuario_creacion
                else None
            ),
            telefono=usuario_data.telefono,
            es_admin=usuario_data.es_admin,
        )
        return usuario
    except ValueError as e:
        error_message = str(e)
        if "nombre de usuario ya está registrado" in error_message:
            raise APIErrorHandler.duplicate_error(
                "usuario", "nombre de usuario", usuario_data.nombre_usuario
            )
        elif "email ya está registrado" in error_message:
            raise APIErrorHandler.duplicate_error(
                "usuario", "email", usuario_data.email
            )
        elif "contraseña" in error_message.lower():
            raise APIErrorHandler.validation_error(error_message, "contraseña")
        elif "nombre" in error_message.lower():
            raise APIErrorHandler.validation_error(error_message, "nombre")
        elif "email" in error_message.lower():
            raise APIErrorHandler.validation_error(error_message, "email")
        else:
            raise APIErrorHandler.validation_error(error_message)
    except Exception as e:
        raise APIErrorHandler.server_error("crear usuario", str(e))


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: UUID, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)
):
    """Actualizar un usuario existente."""
    try:
        usuario_crud = UsuarioCRUD(db)

        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise APIErrorHandler.not_found_error("Usuario", str(usuario_id))

        campos_actualizacion = {
            k: v
            for k, v in usuario_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not usuario_data.id_usuario_edicion:
            return usuario_existente

        usuario_actualizado = usuario_crud.actualizar_usuario(
            usuario_id,
            (
                usuario_data.id_usuario_edicion
                if usuario_data.id_usuario_edicion
                else None
            ),
            **campos_actualizacion,
        )
        return usuario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        error_message = str(e)
        if "nombre de usuario ya está registrado" in error_message:
            raise APIErrorHandler.duplicate_error(
                "usuario", "nombre de usuario", usuario_data.nombre_usuario
            )
        elif "email ya está registrado" in error_message:
            raise APIErrorHandler.duplicate_error(
                "usuario", "email", usuario_data.email
            )
        else:
            raise APIErrorHandler.validation_error(error_message)
    except Exception as e:
        raise APIErrorHandler.server_error("actualizar usuario", str(e))


@router.patch(
    "/{usuario_id}/inactivar", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def inactivar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Inactivar un usuario (soft delete)."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        inactivado = usuario_crud.inactivar_usuario(usuario_id)
        if inactivado:
            return RespuestaAPI(mensaje="Usuario inactivado exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al inactivar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al inactivar usuario: {str(e)}",
        )


@router.patch(
    "/{usuario_id}/reactivar", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def reactivar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un usuario inactivo."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario_existente = usuario_crud.obtener_usuario(usuario_id)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        reactivado = usuario_crud.reactivar_usuario(usuario_id)
        if reactivado:
            return RespuestaAPI(mensaje="Usuario reactivado exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al reactivar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar usuario: {str(e)}",
        )


@router.delete(
    "/{usuario_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_usuario_permanente(usuario_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un usuario permanentemente de la base de datos."""
    import traceback
    import logging
    try:
        usuario_crud = UsuarioCRUD(db)
        # Verificar que el usuario existe (sin filtrar por activo)
        from entities.usuario import Usuario
        usuario_existente = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        
        logging.info(f"Intentando eliminar usuario permanentemente: {usuario_id}")
        eliminado = usuario_crud.eliminar_usuario_permanente(usuario_id)
        
        if eliminado:
            logging.info(f"Usuario {usuario_id} eliminado exitosamente")
            return RespuestaAPI(mensaje="Usuario eliminado permanentemente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario: el método retornó False",
            )
    except HTTPException:
        raise
    except ValueError as e:
        # Errores de validación del CRUD
        error_detail = f"Error al eliminar usuario: {str(e)}"
        logging.error(error_detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )
    except Exception as e:
        # Cualquier otro error
        error_detail = f"Error al eliminar usuario: {str(e)}"
        traceback_str = traceback.format_exc()
        logging.error(f"{error_detail}\n{traceback_str}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
        )


@router.get("/{usuario_id}/es-admin", response_model=RespuestaAPI)
async def verificar_es_admin(usuario_id: UUID, db: Session = Depends(get_db)):
    """Verificar si un usuario es administrador."""
    try:
        usuario_crud = UsuarioCRUD(db)
        es_admin = usuario_crud.es_admin(usuario_id)
        return RespuestaAPI(
            mensaje=f"El usuario {'es' if es_admin else 'no es'} administrador",
            success=True,
            datos={"es_admin": es_admin},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar administrador: {str(e)}",
        )


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Obtener un usuario por ID."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.patch("/{usuario_id}/desactivar", response_model=UsuarioResponse)
async def desactivar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    """Desactivar un usuario (soft delete)."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.cambiar_estado_usuario(usuario_id, False, usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al desactivar usuario: {str(e)}",
        )
