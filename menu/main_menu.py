"""Menú principal del sistema hospitalario."""

import os
from uuid import UUID
from database.config import SessionLocal
from auth.auth_service import AuthService
from menu.paciente_menu import PacienteMenu
from menu.medico_menu import MedicoMenu
from menu.enfermera_menu import EnfermeraMenu
from menu.cita_menu import CitaMenu
from menu.hospitalizacion_menu import HospitalizacionMenu
from menu.factura_menu import FacturaMenu
from menu.historial_menu import HistorialMenu
from menu.usuario_menu import UsuarioMenu


class MainMenu:
    """Menú principal del sistema."""

    def __init__(self):
        self.db = SessionLocal()
        self.auth_service = AuthService(self.db)
        self.usuario_actual = None
        self.paciente_menu = PacienteMenu(self.db, self.auth_service)
        self.medico_menu = MedicoMenu(self.db, self.auth_service)
        self.enfermera_menu = EnfermeraMenu(self.db, self.auth_service)
        self.cita_menu = CitaMenu(self.db, self.auth_service)
        self.hospitalizacion_menu = HospitalizacionMenu(self.db, self.auth_service)
        self.factura_menu = FacturaMenu(self.db, self.auth_service)
        self.historial_menu = HistorialMenu(self.db, self.auth_service)
        self.usuario_menu = UsuarioMenu(self.db, self.auth_service)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del sistema."""
        print("=" * 60)
        print("SISTEMA DE GESTION HOSPITALARIA")
        print("=" * 60)

    def login(self) -> bool:
        """
        Proceso de login del usuario.

        Returns:
            True si el login es exitoso
        """
        self.limpiar_pantalla()
        self.mostrar_titulo()
        print("\nINICIAR SESION")
        print("-" * 30)

        intentos = 0
        max_intentos = 3

        while intentos < max_intentos:
            try:
                nombre_usuario = input("Usuario o Email: ").strip()
                contraseña = input("Contraseña: ").strip()

                if not nombre_usuario or not contraseña:
                    print("ERROR: Usuario y contraseña son obligatorios")
                    intentos += 1
                    continue

                self.usuario_actual = self.auth_service.autenticar_usuario(
                    nombre_usuario, contraseña
                )

                if self.usuario_actual:
                    print(f"\nBIENVENIDO, {self.usuario_actual.nombre}!")
                    if self.usuario_actual.es_admin:
                        print("ACCESO DE ADMINISTRADOR")
                    return True
                else:
                    intentos += 1
                    print(
                        f"ERROR: Credenciales invalidas. Intentos restantes: {max_intentos - intentos}"
                    )

            except KeyboardInterrupt:
                print("\n\nHASTA LUEGO!")
                return False
            except Exception as e:
                print(f"ERROR: {e}")
                intentos += 1

        print("\nERROR: Demasiados intentos fallidos. Acceso denegado.")
        return False

    def mostrar_menu_principal(self):
        """Mostrar menú principal."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print(f"\nUsuario: {self.usuario_actual.nombre}")
                if self.usuario_actual.es_admin:
                    print("ADMINISTRADOR")
                print("\nMENU PRINCIPAL")
                print("-" * 30)
                print("1. Gestion de Pacientes")
                print("2. Gestion de Medicos")
                print("3. Gestion de Enfermeras")
                print("4. Gestion de Citas")
                print("5. Gestion de Hospitalizaciones")
                print("6. Gestion de Facturas")
                print("7. Historiales Medicos")
                if self.usuario_actual.es_admin:
                    print("8. Gestion de Usuarios")
                print("0. Salir")

                opcion = input("\nSeleccione una opcion: ").strip()

                if opcion == "0":
                    print("\nHASTA LUEGO!")
                    break
                elif opcion == "1":
                    self.paciente_menu.mostrar_menu()
                elif opcion == "2":
                    self.medico_menu.mostrar_menu()
                elif opcion == "3":
                    self.enfermera_menu.mostrar_menu()
                elif opcion == "4":
                    self.cita_menu.mostrar_menu()
                elif opcion == "5":
                    self.hospitalizacion_menu.mostrar_menu()
                elif opcion == "6":
                    self.factura_menu.mostrar_menu()
                elif opcion == "7":
                    self.historial_menu.mostrar_menu()
                elif opcion == "8" and self.usuario_actual.es_admin:
                    self.usuario_menu.mostrar_menu()
                else:
                    print("ERROR: Opcion invalida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\nHASTA LUEGO!")
                break
            except Exception as e:
                print(f"ERROR: {e}")
                input("Presione Enter para continuar...")

    def inicializar_sistema(self):
        """Inicializar el sistema y crear admin por defecto."""
        try:
            # Crear admin por defecto
            self.auth_service.crear_admin_por_defecto()
            print("Sistema inicializado correctamente")
        except Exception as e:
            print(f"ADVERTENCIA: {e}")

    def ejecutar(self):
        """Ejecutar el sistema principal."""
        try:
            self.inicializar_sistema()

            if self.login():
                self.mostrar_menu_principal()
        except Exception as e:
            print(f"ERROR CRITICO: {e}")
        finally:
            self.db.close()


def main():
    """Función principal para ejecutar el sistema."""
    sistema = MainMenu()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
