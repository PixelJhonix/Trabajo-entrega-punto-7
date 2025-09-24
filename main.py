"""Módulo principal para la gestión del sistema hospitalario.

Este módulo proporciona una interfaz de consola para registrar usuarios y profesionales,
gestionar citas, facturas y historiales médicos, y realizar operaciones como modificar
o eliminar datos. Utiliza SQLAlchemy para interactuar con la base de datos y Pydantic
para validar los datos de entrada.
"""

import json
from typing import List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import Base, Usuario, Profesional, Citas, Factura, HistorialMedico
from entities.usuario import UsuarioCreate, UsuarioUpdate
from entities.profesional import ProfesionalCreate
from entities.citas import CitasCreate
from entities.factura import FacturaCreate
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print("\n")
print("---------------BIENVENIDOS A HOSPITAL LOS ENA-NOS---------------")


def registrar_usuario():
    """Registra un nuevo usuario (paciente) en el sistema.

    Solicita los datos del usuario a través de la consola, valida la entrada con
    el modelo Pydantic UsuarioCreate y crea un nuevo usuario con un historial médico vacío.
    """
    nombre = input("Nombre del usuario: ")
    edad = int(input("Edad: "))
    diagnostico = input("Diagnóstico: ")
    necesita = input(
        "¿Necesita cita con doctor o servicios de enfermera? (doctor/enfermera): "
    )
    usuario_data = UsuarioCreate(
        nombre=nombre, edad=edad, diagnostico=diagnostico, necesita=necesita
    )
    with Session() as session:
        if session.query(Usuario).filter(Usuario.nombre == nombre).first():
            print("Usuario ya existe.")
            return
        usuario = Usuario(**usuario_data.model_dump())
        session.add(usuario)
        session.commit()
        historial = HistorialMedico(paciente=usuario, registros=[])
        session.add(historial)
        session.commit()
    print("Usuario registrado.")


def registrar_profesional():
    """Registra un nuevo profesional médico en el sistema.

    Solicita los datos del profesional a través de la consola, valida la entrada con
    el modelo Pydantic ProfesionalCreate y crea un nuevo profesional.
    """
    nombre = input("Nombre del profesional: ")
    categoria_profesional = input("Categoría (doctor/enfermera): ")
    profesional_data = ProfesionalCreate(
        nombre=nombre, categoria_profesional=categoria_profesional
    )
    with Session() as session:
        if session.query(Profesional).filter(Profesional.nombre == nombre).first():
            print("Profesional ya existe.")
            return
        profesional = Profesional(**profesional_data.model_dump())
        session.add(profesional)
        session.commit()
    print("Profesional registrado.")


def agendar_cita():
    """Agenda una nueva cita médica.

    Solicita los datos de la cita (usuario, profesional y fecha) a través de la consola,
    valida la entrada con el modelo Pydantic CitasCreate y registra la cita en la base de datos,
    actualizando también el historial médico del usuario.
    """
    usuario_nombre = input("Nombre del usuario: ")
    profesional_nombre = input("Nombre del profesional: ")
    fecha = input("Fecha (YYYY-MM-DD): ")
    cita_data = CitasCreate(
        usuario_nombre=usuario_nombre,
        profesional_nombre=profesional_nombre,
        fecha=fecha,
    )
    with Session() as session:
        usuario = (
            session.query(Usuario).filter(Usuario.nombre == usuario_nombre).first()
        )
        if not usuario:
            print("Usuario no encontrado.")
            return
        profesional = (
            session.query(Profesional)
            .filter(Profesional.nombre == profesional_nombre)
            .first()
        )
        if not profesional:
            print("Profesional no encontrado.")
            return
        cita = Citas(usuario=usuario, profesional=profesional, fecha=cita_data.fecha)
        session.add(cita)
        historial = usuario.historial
        if historial:
            historial.registros.append(
                f"Cita agendada con {profesional_nombre} el {fecha}"
            )
        session.commit()
    print("Cita agendada.")


def modificar_dato_usuario():
    """Modifica los datos de un usuario existente.

    Solicita el nombre del usuario y el campo a modificar (nombre, edad, diagnóstico o necesita),
    valida la entrada con el modelo Pydantic UsuarioUpdate y actualiza los datos en la base de datos.
    """
    nombre = input("Nombre del usuario a modificar: ")
    with Session() as session:
        usuario = session.query(Usuario).filter(Usuario.nombre == nombre).first()
        if not usuario:
            print("Usuario no encontrado.")
            return
        print("¿Qué desea modificar? (nombre/edad/diagnostico/necesita)")
        campo = input()
        update_data = {}
        if campo == "nombre":
            update_data["nombre"] = input("Nuevo nombre: ")
        elif campo == "edad":
            update_data["edad"] = int(input("Nueva edad: "))
        elif campo == "diagnostico":
            update_data["diagnostico"] = input("Nuevo diagnóstico: ")
        elif campo == "necesita":
            update_data["necesita"] = input("Nuevo necesita: ")
        else:
            print("Campo inválido.")
            return
        usuario_update = UsuarioUpdate(**update_data)
        for key, value in usuario_update.model_dump(exclude_unset=True).items():
            setattr(usuario, key, value)
        session.commit()
    print("Dato modificado.")


def modificar_dato_profesional():
    """Modifica los datos de un profesional existente.

    Solicita el nombre del profesional y el campo a modificar (nombre o categoría profesional),
    valida la entrada y actualiza los datos en la base de datos.
    """
    nombre = input("Nombre del profesional a modificar: ")
    with Session() as session:
        profesional = (
            session.query(Profesional).filter(Profesional.nombre == nombre).first()
        )
        if not profesional:
            print("Profesional no encontrado.")
            return
        print("¿Qué desea modificar? (nombre/categoria_profesional)")
        campo = input()
        if campo == "nombre":
            profesional.nombre = input("Nuevo nombre: ")
        elif campo == "categoria_profesional":
            categoria = input("Nueva categoría (doctor/enfermera): ")
            profesional_data = ProfesionalCreate(
                nombre=profesional.nombre, categoria_profesional=categoria
            )
            profesional.categoria_profesional = profesional_data.categoria_profesional
        else:
            print("Campo inválido.")
            return
        session.commit()
    print("Dato modificado.")


def eliminar_usuario():
    """Elimina un usuario de la base de datos.

    Solicita el nombre del usuario y elimina el registro correspondiente junto con sus datos asociados.
    """
    nombre = input("Nombre del usuario a eliminar: ")
    with Session() as session:
        usuario = session.query(Usuario).filter(Usuario.nombre == nombre).first()
        if not usuario:
            print("Usuario no encontrado.")
            return
        session.delete(usuario)
        session.commit()
    print("Usuario eliminado.")


def eliminar_profesional():
    """Elimina un profesional de la base de datos.

    Solicita el nombre del profesional y elimina el registro correspondiente junto con sus datos asociados.
    """
    nombre = input("Nombre del profesional a eliminar: ")
    with Session() as session:
        profesional = (
            session.query(Profesional).filter(Profesional.nombre == nombre).first()
        )
        if not profesional:
            print("Profesional no encontrado.")
            return
        session.delete(profesional)
        session.commit()
    print("Profesional eliminado.")


def mostrar_registros():
    """Muestra todos los registros de usuarios, profesionales, citas, historiales y facturas.

    Consulta y muestra todos los datos almacenados en la base de datos.
    """
    with Session() as session:
        print("Usuarios:")
        for u in session.query(Usuario).all():
            print(u)
        print("Profesionales:")
        for p in session.query(Profesional).all():
            print(p)
        print("Citas:")
        for c in session.query(Citas).all():
            print(c)
        print("Historiales:")
        for h in session.query(HistorialMedico).all():
            print(h)
        print("Facturas:")
        for f in session.query(Factura).all():
            print(f)


def generar_factura():
    """Genera una nueva factura para un usuario.

    Solicita los datos de la factura a través de la consola, valida la entrada con
    el modelo Pydantic FacturaCreate y registra la factura en la base de datos.
    """
    usuario_nombre = input("Nombre del usuario: ")
    descripcion = input("Descripción de cobros: ")
    monto = float(input("Monto: "))
    factura_data = FacturaCreate(
        usuario_nombre=usuario_nombre, descripcion=descripcion, monto=monto
    )
    with Session() as session:
        usuario = (
            session.query(Usuario).filter(Usuario.nombre == usuario_nombre).first()
        )
        if not usuario:
            print("Usuario no encontrado.")
            return
        factura = Factura(
            usuario=usuario,
            descripcion=factura_data.descripcion,
            monto=factura_data.monto,
        )
        session.add(factura)
        historial = usuario.historial
        if historial:
            historial.registros.append(f"Factura generada: {descripcion} por {monto}")
        session.commit()
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
            modificar_dato_profesional()
        elif opcion == "5":
            eliminar_usuario()
        elif opcion == "6":
            eliminar_profesional()
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
            with Session() as session:
                Citas.ver_citas_paciente(nombre, session)
        elif opcion == "3":
            nombre = input("Nombre del médico: ")
            with Session() as session:
                Citas.ver_citas_medico(nombre, session)
        elif opcion == "4":
            fecha = input("Fecha (YYYY-MM-DD): ")
            with Session() as session:
                Citas.ver_citas_fecha(fecha, session)
        elif opcion == "5":
            usuario_nombre = input("Nombre del usuario: ")
            profesional_nombre = input("Nombre del profesional: ")
            fecha = input("Fecha (YYYY-MM-DD): ")
            with Session() as session:
                Citas.cancelar_cita(usuario_nombre, profesional_nombre, fecha, session)
                usuario = (
                    session.query(Usuario)
                    .filter(Usuario.nombre == usuario_nombre)
                    .first()
                )
                if usuario and usuario.historial:
                    usuario.historial.registros.append(
                        f"Cita cancelada con {profesional_nombre} el {fecha}"
                    )
                    session.commit()
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
            with Session() as session:
                for f in session.query(Factura).all():
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
            with Session() as session:
                usuario = (
                    session.query(Usuario).filter(Usuario.nombre == nombre).first()
                )
                if usuario and usuario.historial:
                    usuario.historial.mostrar_historial()
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
            with Session() as session:
                usuarios = session.query(Usuario).all()
                profesionales = session.query(Profesional).all()
                submenu_registro(usuarios, profesionales, profesionales)
        elif opcion == "2":
            with Session() as session:
                usuarios = session.query(Usuario).all()
                profesionales = session.query(Profesional).all()
                submenu_citas(usuarios, profesionales)
        elif opcion == "3":
            with Session() as session:
                usuarios = session.query(Usuario).all()
                profesionales = session.query(Profesional).all()
                submenu_facturas(usuarios, profesionales, profesionales)
        elif opcion == "4":
            with Session() as session:
                usuarios = session.query(Usuario).all()
                profesionales = session.query(Profesional).all()
                submenu_Historial_Medico(usuarios, profesionales)
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    menu_principal()
