"""Capa CRUD para operaciones de base de datos."""

from .paciente_crud import PacienteCRUD
from .medico_crud import MedicoCRUD
from .enfermera_crud import EnfermeraCRUD
from .cita_crud import CitaCRUD
from .hospitalizacion_crud import HospitalizacionCRUD
from .factura_crud import FacturaCRUD
from .factura_detalle_crud import FacturaDetalleCRUD
from .historial_medico_crud import HistorialMedicoCRUD
from .historial_entrada_crud import HistorialEntradaCRUD
from .usuario_crud import UsuarioCRUD

__all__ = [
    "PacienteCRUD",
    "MedicoCRUD",
    "EnfermeraCRUD",
    "CitaCRUD",
    "HospitalizacionCRUD",
    "FacturaCRUD",
    "FacturaDetalleCRUD",
    "HistorialMedicoCRUD",
    "HistorialEntradaCRUD",
    "UsuarioCRUD",
]
