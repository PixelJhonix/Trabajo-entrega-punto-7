"""Menú interactivo para gestión de historiales médicos."""

import os
from uuid import UUID
from sqlalchemy.orm import Session
from crud.historial_medico_crud import HistorialMedicoCRUD
from crud.historial_entrada_crud import HistorialEntradaCRUD
from crud.paciente_crud import PacienteCRUD
from crud.medico_crud import MedicoCRUD
from auth.auth_service import AuthService


class HistorialMenu:
    """Menú para gestión de historiales médicos."""

    def __init__(self, db: Session, auth_service: AuthService):
        self.db = db
        self.auth_service = auth_service
        self.historial_crud = HistorialMedicoCRUD(db)
        self.entrada_crud = HistorialEntradaCRUD(db)
        self.paciente_crud = PacienteCRUD(db)
        self.medico_crud = MedicoCRUD(db)

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_titulo(self):
        """Mostrar título del menú."""
        print("LICENCIA GESTIÓN DE HISTORIALES MÉDICOS")
        print("-" * 40)

    def mostrar_menu(self):
        """Mostrar menú principal de historiales."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("1. LICENCIA Gestión de Historiales")
                print("2. NOTAS Gestión de Entradas")
                print("0. VOLVER Volver al Menú Principal")

                opcion = input("\n-> Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.menu_historiales()
                elif opcion == "2":
                    self.menu_entradas()
                else:
                    print("ERROR Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\nADIOS Regresando al menú principal...")
                break
            except Exception as e:
                print(f"ERROR Error: {e}")
                input("Presione Enter para continuar...")

    def menu_historiales(self):
        """Menú de gestión de historiales."""
        while True:
            try:
                self.limpiar_pantalla()
                print("LICENCIA GESTIÓN DE HISTORIALES")
                print("-" * 30)
                print("1. + Crear Historial")
                print("2. DIAGNOSTICO Buscar Historial")
                print("3. LICENCIA Listar Historiales")
                print("4. EDITAR Actualizar Historial")
                print("5. ELIMINAR Eliminar Historial")
                print("0. VOLVER Volver")

                opcion = input("\n-> Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.crear_historial()
                elif opcion == "2":
                    self.buscar_historial()
                elif opcion == "3":
                    self.listar_historiales()
                elif opcion == "4":
                    self.actualizar_historial()
                elif opcion == "5":
                    self.eliminar_historial()
                else:
                    print("ERROR Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\nADIOS Regresando...")
                break
            except Exception as e:
                print(f"ERROR Error: {e}")
                input("Presione Enter para continuar...")

    def menu_entradas(self):
        """Menú de gestión de entradas."""
        while True:
            try:
                self.limpiar_pantalla()
                print("NOTAS GESTIÓN DE ENTRADAS")
                print("-" * 30)
                print("1. + Agregar Entrada")
                print("2. DIAGNOSTICO Buscar Entrada")
                print("3. LICENCIA Listar Entradas")
                print("4. EDITAR Actualizar Entrada")
                print("5. ELIMINAR Eliminar Entrada")
                print("0. VOLVER Volver")

                opcion = input("\n-> Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.agregar_entrada()
                elif opcion == "2":
                    self.buscar_entrada()
                elif opcion == "3":
                    self.listar_entradas()
                elif opcion == "4":
                    self.actualizar_entrada()
                elif opcion == "5":
                    self.eliminar_entrada()
                else:
                    print("ERROR Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\nADIOS Regresando...")
                break
            except Exception as e:
                print(f"ERROR Error: {e}")
                input("Presione Enter para continuar...")

    def crear_historial(self):
        """Crear un nuevo historial médico."""
        try:
            self.limpiar_pantalla()
            print("LICENCIA CREAR HISTORIAL MÉDICO")
            print("-" * 30)

            paciente_id = input("ID ID del paciente: ").strip()
            paciente = self.paciente_crud.obtener_paciente(UUID(paciente_id))
            if not paciente:
                print("ERROR Paciente no encontrado")
                return

            print(f"USUARIO Paciente: {paciente.primer_nombre} {paciente.apellido}")

            numero_historial = input("LICENCIA Número de historial: ").strip()
            fecha_apertura = input("FECHA Fecha de apertura (YYYY-MM-DD): ").strip()

            historial = self.historial_crud.crear_historial(
                paciente_id=paciente.id,
                numero_historial=numero_historial,
                fecha_apertura=fecha_apertura,
                id_usuario_creacion=self.auth_service.get_current_user().id,
            )

            print(f"\nOK Historial creado exitosamente!")
            print(f"ID ID: {historial.id}")
            print(f"LICENCIA Número: {historial.numero_historial}")
            print(f"USUARIO Paciente: {paciente.primer_nombre} {paciente.apellido}")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def buscar_historial(self):
        """Buscar un historial médico."""
        try:
            self.limpiar_pantalla()
            print("DIAGNOSTICO BUSCAR HISTORIAL")
            print("-" * 25)

            historial_id = input("ID Ingrese ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if historial:
                self.mostrar_historial(historial)
            else:
                print("ERROR Historial no encontrado")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def listar_historiales(self):
        """Listar todos los historiales."""
        try:
            self.limpiar_pantalla()
            print("LICENCIA LISTAR HISTORIALES")
            print("-" * 25)

            historiales = self.historial_crud.obtener_historiales()
            if historiales:
                print(f"\nLICENCIA Total de historiales: {len(historiales)}")
                for historial in historiales:
                    self.mostrar_historial_resumen(historial)
            else:
                print("ERROR No hay historiales registrados")

        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def actualizar_historial(self):
        """Actualizar un historial médico."""
        try:
            self.limpiar_pantalla()
            print("EDITAR ACTUALIZAR HISTORIAL")
            print("-" * 30)

            historial_id = input("ID Ingrese ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if not historial:
                print("ERROR Historial no encontrado")
                return

            print(f"\nLICENCIA Historial actual:")
            self.mostrar_historial(historial)

            print("\nEDITAR Ingrese nuevos datos (deje en blanco para mantener el actual):")

            numero_historial = input(
                f"LICENCIA Número de historial [{historial.numero_historial}]: "
            ).strip()
            fecha_apertura = input(
                f"FECHA Fecha de apertura [{historial.fecha_apertura}]: "
            ).strip()
            estado = input(f"ESTADO Estado [{historial.estado}]: ").strip()

            kwargs = {}
            if numero_historial:
                kwargs["numero_historial"] = numero_historial
            if fecha_apertura:
                kwargs["fecha_apertura"] = fecha_apertura
            if estado:
                kwargs["estado"] = estado

            if kwargs:
                historial_actualizado = self.historial_crud.actualizar_historial(
                    historial.id, self.auth_service.get_current_user().id, **kwargs
                )
                print(f"\nOK Historial actualizado exitosamente!")
                self.mostrar_historial(historial_actualizado)
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def eliminar_historial(self):
        """Eliminar un historial médico."""
        try:
            self.limpiar_pantalla()
            print("ELIMINAR ELIMINAR HISTORIAL")
            print("-" * 25)

            historial_id = input("ID Ingrese ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if not historial:
                print("ERROR Historial no encontrado")
                return

            print(f"\nLICENCIA Historial a eliminar:")
            self.mostrar_historial(historial)

            confirmacion = (
                input("\nADVERTENCIA ¿Está seguro de eliminar este historial? (s/N): ")
                .strip()
                .lower()
            )
            if confirmacion == "s":
                if self.historial_crud.eliminar_historial(historial.id):
                    print("OK Historial eliminado exitosamente!")
                else:
                    print("ERROR Error al eliminar el historial")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def agregar_entrada(self):
        """Agregar una entrada al historial."""
        try:
            self.limpiar_pantalla()
            print("NOTAS AGREGAR ENTRADA AL HISTORIAL")
            print("-" * 35)

            historial_id = input("ID ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if not historial:
                print("ERROR Historial no encontrado")
                return

            medico_id = input("DOCTOR ID del médico: ").strip()
            medico = self.medico_crud.obtener_medico(UUID(medico_id))
            if not medico:
                print("ERROR Médico no encontrado")
                return

            print(f"LICENCIA Historial: {historial.numero_historial}")
            print(f"DOCTOR Médico: Dr. {medico.primer_nombre} {medico.apellido}")

            diagnostico = input("DIAGNOSTICO Diagnóstico: ").strip()
            tratamiento = input("TRATAMIENTO Tratamiento: ").strip()
            fecha_registro = input("FECHA Fecha de registro (YYYY-MM-DD): ").strip()
            cita_id = input("FECHA ID de cita (opcional): ").strip() or None
            notas = input("NOTAS Notas adicionales (opcional): ").strip() or None
            firma_digital = input("FIRMA Firma digital (opcional): ").strip() or None

            entrada = self.entrada_crud.crear_entrada(
                historial_id=historial.id,
                medico_id=medico.id,
                diagnostico=diagnostico,
                tratamiento=tratamiento,
                fecha_registro=fecha_registro,
                id_usuario_creacion=self.auth_service.get_current_user().id,
                cita_id=UUID(cita_id) if cita_id else None,
                notas=notas,
                firma_digital=firma_digital,
            )

            print(f"\nOK Entrada agregada exitosamente!")
            print(f"ID ID: {entrada.id}")
            print(f"DIAGNOSTICO Diagnóstico: {entrada.diagnostico}")
            print(f"FECHA Fecha: {entrada.fecha_registro}")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def buscar_entrada(self):
        """Buscar una entrada del historial."""
        try:
            self.limpiar_pantalla()
            print("DIAGNOSTICO BUSCAR ENTRADA")
            print("-" * 25)

            entrada_id = input("ID Ingrese ID de la entrada: ").strip()
            entrada = self.entrada_crud.obtener_entrada(UUID(entrada_id))
            if entrada:
                self.mostrar_entrada(entrada)
            else:
                print("ERROR Entrada no encontrada")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def listar_entradas(self):
        """Listar todas las entradas."""
        try:
            self.limpiar_pantalla()
            print("NOTAS LISTAR ENTRADAS")
            print("-" * 25)

            entradas = self.entrada_crud.obtener_entradas()
            if entradas:
                print(f"\nNOTAS Total de entradas: {len(entradas)}")
                for entrada in entradas:
                    self.mostrar_entrada_resumen(entrada)
            else:
                print("ERROR No hay entradas registradas")

        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def actualizar_entrada(self):
        """Actualizar una entrada del historial."""
        try:
            self.limpiar_pantalla()
            print("EDITAR ACTUALIZAR ENTRADA")
            print("-" * 30)

            entrada_id = input("ID Ingrese ID de la entrada: ").strip()
            entrada = self.entrada_crud.obtener_entrada(UUID(entrada_id))
            if not entrada:
                print("ERROR Entrada no encontrada")
                return

            print(f"\nNOTAS Entrada actual:")
            self.mostrar_entrada(entrada)

            print("\nEDITAR Ingrese nuevos datos (deje en blanco para mantener el actual):")

            diagnostico = input(f"DIAGNOSTICO Diagnóstico [{entrada.diagnostico}]: ").strip()
            tratamiento = input(f"TRATAMIENTO Tratamiento [{entrada.tratamiento}]: ").strip()
            fecha_registro = input(
                f"FECHA Fecha de registro [{entrada.fecha_registro}]: "
            ).strip()
            notas = input(f"NOTAS Notas [{entrada.notas or 'N/A'}]: ").strip()
            firma_digital = input(
                f"FIRMA Firma digital [{entrada.firma_digital or 'N/A'}]: "
            ).strip()

            kwargs = {}
            if diagnostico:
                kwargs["diagnostico"] = diagnostico
            if tratamiento:
                kwargs["tratamiento"] = tratamiento
            if fecha_registro:
                kwargs["fecha_registro"] = fecha_registro
            if notas:
                kwargs["notas"] = notas
            if firma_digital:
                kwargs["firma_digital"] = firma_digital

            if kwargs:
                entrada_actualizada = self.entrada_crud.actualizar_entrada(
                    entrada.id, self.auth_service.get_current_user().id, **kwargs
                )
                print(f"\nOK Entrada actualizada exitosamente!")
                self.mostrar_entrada(entrada_actualizada)
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def eliminar_entrada(self):
        """Eliminar una entrada del historial."""
        try:
            self.limpiar_pantalla()
            print("ELIMINAR ELIMINAR ENTRADA")
            print("-" * 25)

            entrada_id = input("ID Ingrese ID de la entrada: ").strip()
            entrada = self.entrada_crud.obtener_entrada(UUID(entrada_id))
            if not entrada:
                print("ERROR Entrada no encontrada")
                return

            print(f"\nNOTAS Entrada a eliminar:")
            self.mostrar_entrada(entrada)

            confirmacion = (
                input("\nADVERTENCIA ¿Está seguro de eliminar esta entrada? (s/N): ")
                .strip()
                .lower()
            )
            if confirmacion == "s":
                if self.entrada_crud.eliminar_entrada(entrada.id):
                    print("OK Entrada eliminada exitosamente!")
                else:
                    print("ERROR Error al eliminar la entrada")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"ERROR Error de validación: {e}")
        except Exception as e:
            print(f"ERROR Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def mostrar_historial(self, historial):
        """Mostrar información completa de un historial."""
        print(f"\nLICENCIA INFORMACIÓN DEL HISTORIAL")
        print("-" * 35)
        print(f"ID ID: {historial.id}")
        print(f"LICENCIA Número: {historial.numero_historial}")
        print(f"USUARIO Paciente ID: {historial.paciente_id}")
        print(f"FECHA Fecha de apertura: {historial.fecha_apertura}")
        print(f"ESTADO Estado: {historial.estado}")
        print(f"FECHA Creado: {historial.created_at}")

    def mostrar_historial_resumen(self, historial):
        """Mostrar resumen de un historial."""
        print(
            f"ID {historial.id} | LICENCIA {historial.numero_historial} | USUARIO {historial.paciente_id} | ESTADO {historial.estado}"
        )

    def mostrar_entrada(self, entrada):
        """Mostrar información completa de una entrada."""
        print(f"\nNOTAS INFORMACIÓN DE LA ENTRADA")
        print("-" * 35)
        print(f"ID ID: {entrada.id}")
        print(f"LICENCIA Historial ID: {entrada.historial_id}")
        print(f"DOCTOR Médico ID: {entrada.medico_id}")
        print(f"DIAGNOSTICO Diagnóstico: {entrada.diagnostico}")
        print(f"TRATAMIENTO Tratamiento: {entrada.tratamiento}")
        print(f"FECHA Fecha de registro: {entrada.fecha_registro}")
        print(f"NOTAS Notas: {entrada.notas or 'N/A'}")
        print(f"FIRMA Firma digital: {entrada.firma_digital or 'N/A'}")
        print(f"FECHA Creado: {entrada.created_at}")

    def mostrar_entrada_resumen(self, entrada):
        """Mostrar resumen de una entrada."""
        print(
            f"ID {entrada.id} | DIAGNOSTICO {entrada.diagnostico[:50]}... | FECHA {entrada.fecha_registro}"
        )
