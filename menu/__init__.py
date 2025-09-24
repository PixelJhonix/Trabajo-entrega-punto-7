"""Módulo de menús interactivos."""

from .main_menu import MainMenu
from .paciente_menu import PacienteMenu
from .medico_menu import MedicoMenu
from .cita_menu import CitaMenu
from .hospitalizacion_menu import HospitalizacionMenu
from .factura_menu import FacturaMenu

__all__ = [
    "MainMenu",
    "PacienteMenu",
    "MedicoMenu",
    "CitaMenu",
    "HospitalizacionMenu",
    "FacturaMenu",
]
