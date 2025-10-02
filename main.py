"""Sistema de Gestión Hospitalaria - Punto de entrada principal."""

from menu.main_menu import MainMenu


def main():
    """Ejecutar el sistema."""
    sistema = MainMenu()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
