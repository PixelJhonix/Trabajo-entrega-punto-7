from typing import List
from uuid import UUID

from crud.medico_crud import MedicoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from schemas import MedicoCreate, MedicoResponse, MedicoUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/medicos", tags=["medicos"])


@router.get("/", response_model=List[MedicoResponse])
async def obtener_medicos(
    skip: int = Query(0, ge=0),
    limit: int = Query(1000, ge=1, le=1000),
    include_inactive: bool = Query(False, description="Incluir médicos inactivos"),
    nombre: str = Query(None, description="Filtrar por nombre (búsqueda parcial)"),
    especialidad: str = Query(None, description="Filtrar por especialidad (búsqueda parcial)"),
    activo: bool = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db)
):
    """Obtener todos los médicos con paginación, opción de incluir inactivos y filtros de búsqueda."""
    try:
        medico_crud = MedicoCRUD(db)
        medicos = medico_crud.obtener_medicos(
            skip=skip, 
            limit=limit, 
            include_inactive=include_inactive,
            nombre=nombre,
            especialidad=especialidad,
            activo=activo
        )
        if not medicos:
            return []
        return medicos
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        import traceback

        error_detail = f"Error al obtener médicos: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
        )


@router.get("/{medico_id}", response_model=MedicoResponse)
async def obtener_medico(medico_id: UUID, db: Session = Depends(get_db)):
    """Obtener un médico por ID."""
    try:
        medico_crud = MedicoCRUD(db)
        medico = medico_crud.obtener_medico(medico_id)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener médico: {str(e)}",
        )


@router.get("/email/{email}", response_model=MedicoResponse)
async def obtener_medico_por_email(email: str, db: Session = Depends(get_db)):
    """Obtener un médico por email."""
    try:
        medico_crud = MedicoCRUD(db)
        medico = medico_crud.obtener_medico_por_email(email)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener médico: {str(e)}",
        )


@router.get("/licencia/{numero_licencia}", response_model=MedicoResponse)
async def obtener_medico_por_licencia(
    numero_licencia: str, db: Session = Depends(get_db)
):
    """Obtener un médico por número de licencia."""
    try:
        medico_crud = MedicoCRUD(db)
        medico = medico_crud.obtener_medico_por_licencia(numero_licencia)
        if not medico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )
        return medico
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener médico: {str(e)}",
        )


@router.get("/especialidad/{especialidad}", response_model=List[MedicoResponse])
async def obtener_medicos_por_especialidad(
    especialidad: str, db: Session = Depends(get_db)
):
    """Obtener médicos por especialidad."""
    try:
        medico_crud = MedicoCRUD(db)
        medicos = medico_crud.obtener_medicos_por_especialidad(especialidad)
        return medicos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener médicos por especialidad: {str(e)}",
        )


@router.get("/buscar/{nombre}", response_model=List[MedicoResponse])
async def buscar_medicos_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Buscar médicos por nombre (búsqueda parcial)."""
    try:
        medico_crud = MedicoCRUD(db)
        medicos = medico_crud.buscar_medicos_por_nombre(nombre)
        return medicos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar médicos: {str(e)}",
        )


@router.post("/", response_model=MedicoResponse, status_code=status.HTTP_201_CREATED)
async def crear_medico(medico_data: MedicoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo médico."""
    try:
        medico_crud = MedicoCRUD(db)
        medico = medico_crud.crear_medico(
            nombre=medico_data.nombre,
            apellido=medico_data.apellido,
            fecha_nacimiento=medico_data.fecha_nacimiento,
            especialidad=medico_data.especialidad,
            numero_licencia=medico_data.numero_licencia,
            consultorio=medico_data.consultorio,
            telefono=medico_data.telefono,
            direccion=medico_data.direccion,
            id_usuario_creacion=(
                medico_data.id_usuario_creacion
                if medico_data.id_usuario_creacion
                else None
            ),
            email=medico_data.email,
        )
        return medico
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear médico: {str(e)}",
        )


@router.put("/{medico_id}", response_model=MedicoResponse)
async def actualizar_medico(
    medico_id: UUID, medico_data: MedicoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un médico existente."""
    try:
        medico_crud = MedicoCRUD(db)

        medico_existente = medico_crud.obtener_medico(medico_id)
        if not medico_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in medico_data.dict(exclude={"id_usuario_edicion"}).items()
            if v is not None
        }

        if not campos_actualizacion and not medico_data.id_usuario_edicion:
            return medico_existente

        medico_actualizado = medico_crud.actualizar_medico(
            medico_id,
            medico_data.id_usuario_edicion if medico_data.id_usuario_edicion else None,
            **campos_actualizacion,
        )
        return medico_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar médico: {str(e)}",
        )


@router.patch(
    "/{medico_id}/inactivar", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def inactivar_medico(medico_id: UUID, db: Session = Depends(get_db)):
    """Inactivar un médico (soft delete)."""
    try:
        medico_crud = MedicoCRUD(db)
        medico_existente = medico_crud.obtener_medico(medico_id)
        if not medico_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )
        inactivado = medico_crud.inactivar_medico(medico_id)
        if inactivado:
            return RespuestaAPI(mensaje="Médico inactivado exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al inactivar médico",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al inactivar médico: {str(e)}",
        )


@router.patch(
    "/{medico_id}/reactivar", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def reactivar_medico(medico_id: UUID, db: Session = Depends(get_db)):
    """Reactivar un médico inactivo."""
    try:
        medico_crud = MedicoCRUD(db)
        medico_existente = medico_crud.obtener_medico(medico_id)
        if not medico_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )
        reactivado = medico_crud.reactivar_medico(medico_id)
        if reactivado:
            return RespuestaAPI(mensaje="Médico reactivado exitosamente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al reactivar médico",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar médico: {str(e)}",
        )


@router.delete(
    "/{medico_id}", response_model=RespuestaAPI, status_code=status.HTTP_200_OK
)
async def eliminar_medico_permanente(medico_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un médico permanentemente de la base de datos."""
    try:
        medico_crud = MedicoCRUD(db)
        medico_existente = medico_crud.obtener_medico(medico_id)
        if not medico_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Médico no encontrado"
            )
        eliminado = medico_crud.eliminar_medico_permanente(medico_id)
        if eliminado:
            return RespuestaAPI(mensaje="Médico eliminado permanentemente", success=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar médico",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar médico: {str(e)}",
        )
