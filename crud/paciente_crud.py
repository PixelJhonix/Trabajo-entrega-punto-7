import re
from typing import List, Optional
from uuid import UUID

from entities.paciente import Paciente
from sqlalchemy.orm import Session


class PacienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def _validar_email(self, email: str) -> bool:
        """Validar formato de email."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def _validar_telefono(self, telefono: str) -> bool:
        """Validar formato de teléfono."""
        if not telefono:
            return True
        pattern = r"^[0-9+\-\s()]+$"
        return bool(re.match(pattern, telefono)) and len(telefono) <= 20

    def crear_paciente(
        self,
        nombre: str,
        apellido: str,
        email: str,
        fecha_nacimiento,
        id_usuario_creacion: Optional[UUID] = None,
        telefono: Optional[str] = None,
        direccion: Optional[str] = None,
    ) -> Paciente:
        """Crear un nuevo paciente."""
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not apellido or len(apellido.strip()) == 0:
            raise ValueError("El apellido es obligatorio")
        if len(apellido) > 100:
            raise ValueError("El apellido no puede exceder 100 caracteres")

        if not fecha_nacimiento:
            raise ValueError("La fecha de nacimiento es obligatoria")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        if direccion and len(direccion.strip()) < 3:
            raise ValueError("La dirección debe tener al menos 3 caracteres")
        if direccion and len(direccion) > 255:
            raise ValueError("La dirección no puede exceder 255 caracteres")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")

        if self.obtener_paciente_por_email(email):
            raise ValueError("El email ya está registrado")

        paciente = Paciente(
            nombre=nombre.strip(),
            apellido=apellido.strip(),
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono.strip() if telefono else None,
            email=email.lower().strip(),
            direccion=direccion.strip() if direccion else None,
            id_usuario_creacion=id_usuario_creacion,
        )
        self.db.add(paciente)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

    def obtener_pacientes(
        self, 
        skip: int = 0, 
        limit: int = 1000, 
        include_inactive: bool = False,
        nombre: Optional[str] = None,
        activo: Optional[bool] = None
    ) -> List[Paciente]:
        """Obtener todos los pacientes con opción de incluir inactivos y filtros de búsqueda."""
        try:
            query = self.db.query(Paciente)
            if not include_inactive:
                query = query.filter(Paciente.activo == True)
            
            if activo is not None:
                query = query.filter(Paciente.activo == activo)
            
            if nombre:
                query = query.filter(
                    (Paciente.nombre.ilike(f"%{nombre}%")) | 
                    (Paciente.apellido.ilike(f"%{nombre}%"))
                )
            
            pacientes = query.offset(skip).limit(limit).all()
            return pacientes if pacientes else []
        except Exception as e:
            self.db.rollback()
            import logging

            logging.error(f"Error al obtener pacientes: {str(e)}")
            raise ValueError(f"Error al obtener pacientes: {str(e)}")

    def obtener_paciente(self, paciente_id: UUID) -> Optional[Paciente]:
        """Obtener un paciente por ID."""
        return self.db.query(Paciente).filter(Paciente.id == paciente_id).first()

    def obtener_paciente_por_email(self, email: str) -> Optional[Paciente]:
        """Obtener un paciente por email."""
        return self.db.query(Paciente).filter(Paciente.email == email.lower()).first()

    def buscar_pacientes_por_nombre(self, nombre: str) -> List[Paciente]:
        """Buscar pacientes por nombre."""
        return (
            self.db.query(Paciente)
            .filter(
                Paciente.nombre.ilike(f"%{nombre}%"),
                Paciente.activo,
            )
            .all()
        )

    def actualizar_paciente(
        self, paciente_id: UUID, id_usuario_edicion: Optional[UUID] = None, **kwargs
    ) -> Optional[Paciente]:
        """Actualizar un paciente."""
        paciente = self.obtener_paciente(paciente_id)
        if not paciente:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "apellido" in kwargs:
            apellido = kwargs["apellido"]
            if not apellido or len(apellido.strip()) == 0:
                raise ValueError("El apellido es obligatorio")
            if len(apellido) > 100:
                raise ValueError("El apellido no puede exceder 100 caracteres")
            kwargs["apellido"] = apellido.strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            telefono = kwargs["telefono"]
            if not self._validar_telefono(telefono):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = telefono.strip()

        if "direccion" in kwargs and kwargs["direccion"]:
            direccion = kwargs["direccion"]
            if len(direccion.strip()) < 3:
                raise ValueError("La dirección debe tener al menos 3 caracteres")
            if len(direccion) > 255:
                raise ValueError("La dirección no puede exceder 255 caracteres")
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

        if id_usuario_edicion:
            paciente.id_usuario_edicion = id_usuario_edicion

        for key, value in kwargs.items():
            if hasattr(paciente, key):
                setattr(paciente, key, value)
        self.db.commit()
        self.db.refresh(paciente)
        return paciente

    def inactivar_paciente(self, paciente_id: UUID) -> bool:
        """Inactivar un paciente (soft delete)."""
        try:
            paciente = self.obtener_paciente(paciente_id)
            if not paciente:
                return False
            if not paciente.activo:
                return True
            paciente.activo = False
            self.db.commit()
            self.db.refresh(paciente)
            return True
        except Exception as e:
            self.db.rollback()
            import logging
            logging.error(f"Error al inactivar paciente {paciente_id}: {str(e)}")
            raise ValueError(f"Error al inactivar paciente: {str(e)}")

    def reactivar_paciente(self, paciente_id: UUID) -> bool:
        """Reactivar un paciente inactivo."""
        try:
            paciente = self.obtener_paciente(paciente_id)
            if not paciente:
                return False
            if paciente.activo:
                return True
            paciente.activo = True
            self.db.commit()
            self.db.refresh(paciente)
            return True
        except Exception as e:
            self.db.rollback()
            import logging
            logging.error(f"Error al reactivar paciente {paciente_id}: {str(e)}")
            raise ValueError(f"Error al reactivar paciente: {str(e)}")

    def eliminar_paciente_permanente(self, paciente_id: UUID) -> bool:
        """Eliminar un paciente permanentemente de la base de datos."""
        import logging
        from sqlalchemy import text
        try:
            paciente = self.obtener_paciente(paciente_id)
            if not paciente:
                raise ValueError(f"Paciente con ID {paciente_id} no encontrado")

            # Actualizar referencias de id_usuario_creacion e id_usuario_edicion
            tablas_usuario = ['tbl_pacientes', 'tbl_medicos', 'tbl_enfermeras', 'tbl_citas', 
                             'tbl_hospitalizaciones', 'tbl_facturas', 'tbl_historiales_medicos', 
                             'tbl_historiales_entradas', 'tbl_facturas_detalles']
            
            for tabla in tablas_usuario:
                try:
                    self.db.execute(
                        text(f"UPDATE {tabla} SET id_usuario_creacion = NULL WHERE id_usuario_creacion = :paciente_id"),
                        {"paciente_id": str(paciente_id)}
                    )
                    self.db.execute(
                        text(f"UPDATE {tabla} SET id_usuario_edicion = NULL WHERE id_usuario_edicion = :paciente_id"),
                        {"paciente_id": str(paciente_id)}
                    )
                except Exception as e:
                    logging.warning(f"Error al actualizar referencias de usuario en {tabla}: {str(e)}")
                    continue

            # Eliminar o inactivar registros relacionados que tienen ForeignKey NOT NULL
            # Citas: eliminar permanentemente las citas del paciente
            from entities.cita import Cita
            citas = self.db.query(Cita).filter(Cita.paciente_id == paciente_id).all()
            for cita in citas:
                self.db.delete(cita)

            # Hospitalizaciones: eliminar permanentemente las hospitalizaciones del paciente
            from entities.hospitalizacion import Hospitalizacion
            hospitalizaciones = self.db.query(Hospitalizacion).filter(Hospitalizacion.paciente_id == paciente_id).all()
            for hosp in hospitalizaciones:
                self.db.delete(hosp)

            # Facturas: eliminar permanentemente las facturas del paciente
            from entities.factura import Factura
            facturas = self.db.query(Factura).filter(Factura.paciente_id == paciente_id).all()
            for factura in facturas:
                # Primero eliminar los detalles de factura
                from entities.factura_detalle import FacturaDetalle
                detalles = self.db.query(FacturaDetalle).filter(FacturaDetalle.factura_id == factura.id).all()
                for detalle in detalles:
                    self.db.delete(detalle)
                self.db.delete(factura)

            # Historiales Médicos: eliminar permanentemente los historiales del paciente
            from entities.historial_medico import HistorialMedico
            historiales = self.db.query(HistorialMedico).filter(HistorialMedico.paciente_id == paciente_id).all()
            for hist in historiales:
                # Primero eliminar las entradas del historial
                from entities.historial_entrada import HistorialEntrada
                entradas = self.db.query(HistorialEntrada).filter(HistorialEntrada.historial_medico_id == hist.id).all()
                for entrada in entradas:
                    self.db.delete(entrada)
                self.db.delete(hist)

            # Commit de las eliminaciones relacionadas
            self.db.commit()

            # Eliminar el paciente
            self.db.delete(paciente)
            self.db.commit()
            
            logging.info(f"Paciente {paciente_id} eliminado permanentemente")
            return True
        except Exception as e:
            self.db.rollback()
            logging.error(f"Error al eliminar paciente permanentemente {paciente_id}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            raise ValueError(f"Error al eliminar paciente: {str(e)}")

    def eliminar_paciente(self, paciente_id: UUID) -> bool:
        """Eliminar un paciente (soft delete) - mantiene compatibilidad."""
        return self.inactivar_paciente(paciente_id)
