"""Módulo de menús interactivos."""

from .cita_menu import CitaMenu
from .factura_menu import FacturaMenu
from .hospitalizacion_menu import HospitalizacionMenu
from .main_menu import MainMenu
from .medico_menu import MedicoMenu
from .paciente_menu import PacienteMenu

__all__ = [
    "MainMenu",
    "PacienteMenu",
    "MedicoMenu",
    "CitaMenu",
    "HospitalizacionMenu",
    "FacturaMenu",
]
