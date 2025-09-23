# Main.py
# Este es el archivo principal donde se registra los datos y corre el sistema.
# Permite modificar datos, eliminar usuarios, mostrar registros y volver al menú.

import json
import os
from typing import List, Optional
from Profesional import Profesional
from Usuario import Usuario
import Citas
import Factura
import Historial_Medico

print("\n")
print("---------------BIENVENIDOS A HOSPITAL LOS ENA-NOS---------------")

# Almacenamiento en memoria (puede guardarse en archivos JSON para persistencia)
usuarios: List[Usuario] = []
profesionales: List[Profesional] = []
citas: List[Citas.Citas] = []
historiales: List[Historial_Medico.HistorialMedico] = []
facturas: List[Factura.Factura] = []


# Funciones para guardar y cargar datos (persistencia simple)
def guardar_datos():
    with open("datos.json", "w") as f:
        json.dump(
            {
                "usuarios": [u.__dict__ for u in usuarios],
                "profesionales": [p.__dict__ for p in profesionales],
                "citas": [c.__dict__ for c in citas],
                "historiales": [h.__dict__ for h in historiales],
                "facturas": [f.__dict__ for f in facturas],
            },
            f,
        )


def cargar_datos():
    global usuarios, profesionales, citas, historiales, facturas
    if os.path.exists("datos.json"):
        with open("datos.json", "r") as f:
            data = json.load(f)
            usuarios = [Usuario(**u) for u in data["usuarios"]]
            profesionales = [Profesional(**p) for p in data["profesionales"]]
            citas = [Citas(**c) for c in data["citas"]]
            historiales = [
                Historial_Medico.HistorialMedico(**h) for h in data["historiales"]
            ]
            facturas = [Factura(**f) for f in data["facturas"]]


def registrar_usuario():
    nombre = input("Nombre del usuario: ")
    edad = int(input("Edad: "))
    diagnostico = input("Diagnóstico: ")
    necesita = input(
        "¿Necesita cita con doctor o servicios de enfermera? (doctor/enfermera): "
    )
    usuario = Usuario(nombre, edad, diagnostico, necesita)
    usuarios.append(usuario)
    historial = Historial_Medico.HistorialMedico(usuario.nombre, [])
    historiales.append(historial)
    guardar_datos()
    print("Usuario registrado.")


def registrar_profesional():
    nombre = input("Nombre del profesional: ")
    categoria_profesional = input("Categoría (doctor/enfermera): ")
    profesional = Profesional(nombre, categoria_profesional)
    profesionales.append(profesional)
    guardar_datos()
    print("Profesional registrado.")


def agendar_cita():
    usuario_nombre = input("Nombre del usuario: ")
    profesional_nombre = input("Nombre del profesional: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    cita = Citas(usuario_nombre, profesional_nombre, fecha)
    citas.append(cita)
    # Actualizar historial
    for h in historiales:
        if h.paciente == usuario_nombre:
            h.registros.append(f"Cita agendada con {profesional_nombre} el {fecha}")
    guardar_datos()
    print("Cita agendada.")


def modificar_dato_usuario():
    nombre = input("Nombre del usuario a modificar: ")
    for u in usuarios:
        if u.nombre == nombre:
            print("¿Qué desea modificar? (nombre/edad/diagnostico/necesita)")
            campo = input()
            if campo == "nombre":
                u.nombre = input("Nuevo nombre: ")
            elif campo == "edad":
                u.edad = int(input("Nueva edad: "))
            elif campo == "diagnostico":
                u.diagnostico = input("Nuevo diagnóstico: ")
            elif campo == "necesita":
                u.necesita = input("Nuevo necesita: ")
            guardar_datos()
            print("Dato modificado.")
            return
    print("Usuario no encontrado.")


def eliminar_usuario():
    nombre = input("Nombre del usuario a eliminar: ")
    global usuarios, historiales, citas, facturas
    usuarios = [u for u in usuarios if u.nombre != nombre]
    historiales = [h for h in historiales if h.paciente != nombre]
    citas = [c for c in citas if c.usuario != nombre]
    facturas = [f for f in facturas if f.usuario != nombre]
    guardar_datos()
    print("Usuario eliminado.")


def mostrar_registros():
    print("Usuarios:")
    for u in usuarios:
        print(u.__dict__)
    print("Profesionales:")
    for p in profesionales:
        print(p.__dict__)
    print("Citas:")
    for c in citas:
        print(c.__dict__)
    print("Historiales:")
    for h in historiales:
        print(h.__dict__)
    print("Facturas:")
    for f in facturas:
        print(f.__dict__)


def generar_factura():
    usuario_nombre = input("Nombre del usuario: ")
    descripcion = input("Descripción de cobros: ")
    monto = float(input("Monto: "))
    factura = Factura(usuario_nombre, descripcion, monto)
    facturas.append(factura)
    # Actualizar historial
    for h in historiales:
        if h.paciente == usuario_nombre:
            h.registros.append(f"Factura generada: {descripcion} por {monto}")
    guardar_datos()
    print("Factura generada.")


def submenu_registro(
    pacientes: List[Usuario], medicos: List[Profesional], enfermeras: List[Profesional]
) -> None:
    """Submenú para registrar usuarios y profesionales"""
    while True:
        print("\n" + "=" * 40)
        print("        SUBMENÚ DE REGISTRO")
        print("=" * 40)
        print("1. Registrar Usuario")
        print("2. Registrar Profesional")
        print("3. Editar Usuario")
        print("4. Editar Profesional")
        print("5. Eliminar Usuario")
        print("6. Eliminar Profesional")
        print("7. Mostrar Registros")
        print("0. Volver al Menú Principal")
        print("=" * 40)

        opcion: str = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            registrar_profesional()
        elif opcion == "3":
            modificar_dato_usuario()
        elif opcion == "4":
            print(
                "Funcionalidad de editar profesional no implementada."
            )  # modificar_dato_profesional() FALTA AGREGARLA
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "6":
            print(
                "Funcionalidad de eliminar profesional no implementada."
            )  # eliminar_profesional() FALTA AGREGARLA
        elif opcion == "7":
            mostrar_registros()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")


def submenu_citas(pacientes: List[Usuario], medicos: List[Profesional]) -> None:
    """Submenú para manejar citas"""
    while True:
        print("\n" + "=" * 40)
        print("          SUBMENÚ DE CITAS")
        print("=" * 40)
        print("1. Agendar Cita")
        print("2. Ver Citas por Paciente")
        print("3. Ver Citas por Médico")
        print("4. Ver Citas por Fecha")
        print("5. Cancelar Cita")
        print("0. Volver al Menú Principal")
        print("=" * 40)

        opcion: str = input("Seleccione una opción: ")

        if opcion == "1":
            agendar_cita()
        elif opcion == "2":
            nombre = input("Nombre del paciente: ")
            Citas.Citas.ver_citas_paciente(nombre, citas)
        elif opcion == "3":
            nombre = input("Nombre del médico: ")
            Citas.Citas.ver_citas_medico(nombre, citas)
        elif opcion == "4":
            fecha = input("Fecha (YYYY-MM-DD): ")
            Citas.Citas.ver_citas_fecha(fecha, citas)
        elif opcion == "5":
            usuario_nombre = input("Nombre del usuario: ")
            profesional_nombre = input("Nombre del profesional: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            Citas.Citas.cancelar_cita(usuario_nombre, profesional_nombre, fecha, citas)
            # Actualizar historial
            for h in historiales:
                if h.paciente == usuario_nombre:
                    h.registros.append(
                        f"Cita cancelada con {profesional_nombre} el {fecha}"
                    )
            guardar_datos()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")


def submenu_facturas(
    pacientes: List[Usuario], medicos: List[Profesional], enfermeras: List[Profesional]
) -> None:
    """Submenú para manejar facturas"""
    while True:
        print("\n" + "=" * 40)
        print("         SUBMENÚ DE FACTURAS")
        print("=" * 40)
        print("1. Generar Factura")
        print("2. Ver Facturas")
        print("0. Volver al Menú Principal")
        print("=" * 40)

        opcion: str = input("Seleccione una opción: ")

        if opcion == "1":
            generar_factura()
        elif opcion == "2":
            for f in facturas:
                f.mostrar_factura()
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")


def submenu_Historial_Medico(
    pacientes: List[Usuario], medicos: List[Profesional]
) -> None:
    """Submenú para ver historial médico"""
    while True:
        print("\n" + "=" * 40)
        print("      SUBMENÚ DE HISTORIAL MÉDICO")
        print("=" * 40)
        print("1. Ver Historial por Paciente")
        print("0. Volver al Menú Principal")
        print("=" * 40)

        opcion: str = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del paciente: ")
            for h in historiales:
                if h.paciente == nombre:
                    h.mostrar_historial()
                    break
            else:
                print("Historial no encontrado.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

        input("\nPresione Enter para continuar...")


def menu_principal():
    """Función principal del sistema"""
    print("       ¡Bienvenido al Sistema de Registro Hospitalario!")

    cargar_datos()
    while True:
        print("\n" + "=" * 40)
        print("        MENÚ PRINCIPAL")
        print("=" * 40)
        print("1. Registrarse")
        print("2. Citas")
        print("3. Facturas")
        print("4. Ver Historial Médico")
        print("0. Salir")
        print("=" * 40)

        opcion: str = input("Seleccione una opción: ")

        if opcion == "1":
            submenu_registro(usuarios, profesionales, profesionales)
        elif opcion == "2":
            submenu_citas(usuarios, profesionales)
        elif opcion == "3":
            submenu_facturas(usuarios, profesionales, profesionales)
        elif opcion == "4":
            submenu_Historial_Medico(usuarios, profesionales)
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_principal()
