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
        print("📋 GESTIÓN DE HISTORIALES MÉDICOS")
        print("-" * 40)

    def mostrar_menu(self):
        """Mostrar menú principal de historiales."""
        while True:
            try:
                self.limpiar_pantalla()
                self.mostrar_titulo()
                print("1. 📋 Gestión de Historiales")
                print("2. 📝 Gestión de Entradas")
                print("0. 🔙 Volver al Menú Principal")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

                if opcion == "0":
                    break
                elif opcion == "1":
                    self.menu_historiales()
                elif opcion == "2":
                    self.menu_entradas()
                else:
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\n👋 Regresando al menú principal...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def menu_historiales(self):
        """Menú de gestión de historiales."""
        while True:
            try:
                self.limpiar_pantalla()
                print("📋 GESTIÓN DE HISTORIALES")
                print("-" * 30)
                print("1. ➕ Crear Historial")
                print("2. 🔍 Buscar Historial")
                print("3. 📋 Listar Historiales")
                print("4. ✏️ Actualizar Historial")
                print("5. 🗑️ Eliminar Historial")
                print("0. 🔙 Volver")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

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
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\n👋 Regresando...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def menu_entradas(self):
        """Menú de gestión de entradas."""
        while True:
            try:
                self.limpiar_pantalla()
                print("📝 GESTIÓN DE ENTRADAS")
                print("-" * 30)
                print("1. ➕ Agregar Entrada")
                print("2. 🔍 Buscar Entrada")
                print("3. 📋 Listar Entradas")
                print("4. ✏️ Actualizar Entrada")
                print("5. 🗑️ Eliminar Entrada")
                print("0. 🔙 Volver")

                opcion = input("\n🔹 Seleccione una opción: ").strip()

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
                    print("❌ Opción inválida. Presione Enter para continuar...")
                    input()

            except KeyboardInterrupt:
                print("\n\n👋 Regresando...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("Presione Enter para continuar...")

    def crear_historial(self):
        """Crear un nuevo historial médico."""
        try:
            self.limpiar_pantalla()
            print("📋 CREAR HISTORIAL MÉDICO")
            print("-" * 30)

            paciente_id = input("🆔 ID del paciente: ").strip()
            paciente = self.paciente_crud.obtener_paciente(UUID(paciente_id))
            if not paciente:
                print("❌ Paciente no encontrado")
                return

            print(f"👤 Paciente: {paciente.primer_nombre} {paciente.apellido}")

            numero_historial = input("📋 Número de historial: ").strip()
            fecha_apertura = input("📅 Fecha de apertura (YYYY-MM-DD): ").strip()

            historial = self.historial_crud.crear_historial(
                paciente_id=paciente.id,
                numero_historial=numero_historial,
                fecha_apertura=fecha_apertura,
                id_usuario_creacion=self.auth_service.get_current_user().id,
            )

            print(f"\n✅ Historial creado exitosamente!")
            print(f"🆔 ID: {historial.id}")
            print(f"📋 Número: {historial.numero_historial}")
            print(f"👤 Paciente: {paciente.primer_nombre} {paciente.apellido}")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def buscar_historial(self):
        """Buscar un historial médico."""
        try:
            self.limpiar_pantalla()
            print("🔍 BUSCAR HISTORIAL")
            print("-" * 25)

            historial_id = input("🆔 Ingrese ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if historial:
                self.mostrar_historial(historial)
            else:
                print("❌ Historial no encontrado")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def listar_historiales(self):
        """Listar todos los historiales."""
        try:
            self.limpiar_pantalla()
            print("📋 LISTAR HISTORIALES")
            print("-" * 25)

            historiales = self.historial_crud.obtener_historiales()
            if historiales:
                print(f"\n📋 Total de historiales: {len(historiales)}")
                for historial in historiales:
                    self.mostrar_historial_resumen(historial)
            else:
                print("❌ No hay historiales registrados")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def actualizar_historial(self):
        """Actualizar un historial médico."""
        try:
            self.limpiar_pantalla()
            print("✏️ ACTUALIZAR HISTORIAL")
            print("-" * 30)

            historial_id = input("🆔 Ingrese ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if not historial:
                print("❌ Historial no encontrado")
                return

            print(f"\n📋 Historial actual:")
            self.mostrar_historial(historial)

            print("\n✏️ Ingrese nuevos datos (deje en blanco para mantener el actual):")

            numero_historial = input(f"📋 Número de historial [{historial.numero_historial}]: ").strip()
            fecha_apertura = input(f"📅 Fecha de apertura [{historial.fecha_apertura}]: ").strip()
            estado = input(f"📊 Estado [{historial.estado}]: ").strip()

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
                print(f"\n✅ Historial actualizado exitosamente!")
                self.mostrar_historial(historial_actualizado)
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def eliminar_historial(self):
        """Eliminar un historial médico."""
        try:
            self.limpiar_pantalla()
            print("🗑️ ELIMINAR HISTORIAL")
            print("-" * 25)

            historial_id = input("🆔 Ingrese ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if not historial:
                print("❌ Historial no encontrado")
                return

            print(f"\n📋 Historial a eliminar:")
            self.mostrar_historial(historial)

            confirmacion = input("\n⚠️ ¿Está seguro de eliminar este historial? (s/N): ").strip().lower()
            if confirmacion == "s":
                if self.historial_crud.eliminar_historial(historial.id):
                    print("✅ Historial eliminado exitosamente!")
                else:
                    print("❌ Error al eliminar el historial")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def agregar_entrada(self):
        """Agregar una entrada al historial."""
        try:
            self.limpiar_pantalla()
            print("📝 AGREGAR ENTRADA AL HISTORIAL")
            print("-" * 35)

            historial_id = input("🆔 ID del historial: ").strip()
            historial = self.historial_crud.obtener_historial(UUID(historial_id))
            if not historial:
                print("❌ Historial no encontrado")
                return

            medico_id = input("👨‍⚕️ ID del médico: ").strip()
            medico = self.medico_crud.obtener_medico(UUID(medico_id))
            if not medico:
                print("❌ Médico no encontrado")
                return

            print(f"📋 Historial: {historial.numero_historial}")
            print(f"👨‍⚕️ Médico: Dr. {medico.primer_nombre} {medico.apellido}")

            diagnostico = input("🔍 Diagnóstico: ").strip()
            tratamiento = input("💊 Tratamiento: ").strip()
            fecha_registro = input("📅 Fecha de registro (YYYY-MM-DD): ").strip()
            cita_id = input("📅 ID de cita (opcional): ").strip() or None
            notas = input("📝 Notas adicionales (opcional): ").strip() or None
            firma_digital = input("✍️ Firma digital (opcional): ").strip() or None

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

            print(f"\n✅ Entrada agregada exitosamente!")
            print(f"🆔 ID: {entrada.id}")
            print(f"🔍 Diagnóstico: {entrada.diagnostico}")
            print(f"📅 Fecha: {entrada.fecha_registro}")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def buscar_entrada(self):
        """Buscar una entrada del historial."""
        try:
            self.limpiar_pantalla()
            print("🔍 BUSCAR ENTRADA")
            print("-" * 25)

            entrada_id = input("🆔 Ingrese ID de la entrada: ").strip()
            entrada = self.entrada_crud.obtener_entrada(UUID(entrada_id))
            if entrada:
                self.mostrar_entrada(entrada)
            else:
                print("❌ Entrada no encontrada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def listar_entradas(self):
        """Listar todas las entradas."""
        try:
            self.limpiar_pantalla()
            print("📝 LISTAR ENTRADAS")
            print("-" * 25)

            entradas = self.entrada_crud.obtener_entradas()
            if entradas:
                print(f"\n📝 Total de entradas: {len(entradas)}")
                for entrada in entradas:
                    self.mostrar_entrada_resumen(entrada)
            else:
                print("❌ No hay entradas registradas")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def actualizar_entrada(self):
        """Actualizar una entrada del historial."""
        try:
            self.limpiar_pantalla()
            print("✏️ ACTUALIZAR ENTRADA")
            print("-" * 30)

            entrada_id = input("🆔 Ingrese ID de la entrada: ").strip()
            entrada = self.entrada_crud.obtener_entrada(UUID(entrada_id))
            if not entrada:
                print("❌ Entrada no encontrada")
                return

            print(f"\n📝 Entrada actual:")
            self.mostrar_entrada(entrada)

            print("\n✏️ Ingrese nuevos datos (deje en blanco para mantener el actual):")

            diagnostico = input(f"🔍 Diagnóstico [{entrada.diagnostico}]: ").strip()
            tratamiento = input(f"💊 Tratamiento [{entrada.tratamiento}]: ").strip()
            fecha_registro = input(f"📅 Fecha de registro [{entrada.fecha_registro}]: ").strip()
            notas = input(f"📝 Notas [{entrada.notas or 'N/A'}]: ").strip()
            firma_digital = input(f"✍️ Firma digital [{entrada.firma_digital or 'N/A'}]: ").strip()

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
                print(f"\n✅ Entrada actualizada exitosamente!")
                self.mostrar_entrada(entrada_actualizada)
            else:
                print("ℹ️ No se realizaron cambios")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def eliminar_entrada(self):
        """Eliminar una entrada del historial."""
        try:
            self.limpiar_pantalla()
            print("🗑️ ELIMINAR ENTRADA")
            print("-" * 25)

            entrada_id = input("🆔 Ingrese ID de la entrada: ").strip()
            entrada = self.entrada_crud.obtener_entrada(UUID(entrada_id))
            if not entrada:
                print("❌ Entrada no encontrada")
                return

            print(f"\n📝 Entrada a eliminar:")
            self.mostrar_entrada(entrada)

            confirmacion = input("\n⚠️ ¿Está seguro de eliminar esta entrada? (s/N): ").strip().lower()
            if confirmacion == "s":
                if self.entrada_crud.eliminar_entrada(entrada.id):
                    print("✅ Entrada eliminada exitosamente!")
                else:
                    print("❌ Error al eliminar la entrada")
            else:
                print("ℹ️ Operación cancelada")

        except ValueError as e:
            print(f"❌ Error de validación: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            input("\nPresione Enter para continuar...")

    def mostrar_historial(self, historial):
        """Mostrar información completa de un historial."""
        print(f"\n📋 INFORMACIÓN DEL HISTORIAL")
        print("-" * 35)
        print(f"🆔 ID: {historial.id}")
        print(f"📋 Número: {historial.numero_historial}")
        print(f"👤 Paciente ID: {historial.paciente_id}")
        print(f"📅 Fecha de apertura: {historial.fecha_apertura}")
        print(f"📊 Estado: {historial.estado}")
        print(f"📅 Creado: {historial.created_at}")

    def mostrar_historial_resumen(self, historial):
        """Mostrar resumen de un historial."""
        print(f"🆔 {historial.id} | 📋 {historial.numero_historial} | 👤 {historial.paciente_id} | 📊 {historial.estado}")

    def mostrar_entrada(self, entrada):
        """Mostrar información completa de una entrada."""
        print(f"\n📝 INFORMACIÓN DE LA ENTRADA")
        print("-" * 35)
        print(f"🆔 ID: {entrada.id}")
        print(f"📋 Historial ID: {entrada.historial_id}")
        print(f"👨‍⚕️ Médico ID: {entrada.medico_id}")
        print(f"🔍 Diagnóstico: {entrada.diagnostico}")
        print(f"💊 Tratamiento: {entrada.tratamiento}")
        print(f"📅 Fecha de registro: {entrada.fecha_registro}")
        print(f"📝 Notas: {entrada.notas or 'N/A'}")
        print(f"✍️ Firma digital: {entrada.firma_digital or 'N/A'}")
        print(f"📅 Creado: {entrada.created_at}")

    def mostrar_entrada_resumen(self, entrada):
        """Mostrar resumen de una entrada."""
        print(f"🆔 {entrada.id} | 🔍 {entrada.diagnostico[:50]}... | 📅 {entrada.fecha_registro}")
