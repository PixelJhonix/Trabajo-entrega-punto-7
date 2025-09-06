""" 7. Hospital / Clínica
 Pacientes, médicos, enfermeras. 
 Operaciones: agendar cita, registrar diagnóstico, emitir factura. """

from paciente import Paciente
from medico import Medico
from enfermera import Enfermera
from typing import List
from pydantic import BaseModel, ValidationError, conint

print("---------------BIENVENIDOS A HOSPITAL LOS ENA-NOS---------------")

class SeleccionIndice(BaseModel):
    idx: conint(ge=1)

def mostrar_todos(pacientes, medicos, enfermeras):
    """Función para mostrar todas las personas registradas"""
    print("\n--- LISTADO COMPLETO ---")
    
    if pacientes:
        print(f"\nPACIENTES ({len(pacientes)}):")
        for paciente in pacientes:
            paciente.mostrar_datos()
            print("-" * 30)
    
    if medicos:
        print(f"\nMÉDICOS ({len(medicos)}):")
        for medico in medicos:
            medico.mostrar_datos()
            print("-" * 30)
    
    if enfermeras:
        print(f"\nENFERMERAS ({len(enfermeras)}):")
        for enfermera in enfermeras:
            enfermera.mostrar_datos()
            print("-" * 30)

def registrar_persona(pacientes, medicos, enfermeras):
    """Función para registrar nuevas personas"""
    print("\n--- REGISTRAR NUEVA PERSONA ---")
    print("1. Registrar Paciente")
    print("2. Registrar Médico")
    print("3. Registrar Enfermera")
    
    opcion = input("Seleccione tipo de persona: ")
    
    if opcion == "1":
        paciente = Paciente.registrar()
        pacientes.append(paciente)
        print("Paciente registrado exitosamente!")
    elif opcion == "2":
        medico = Medico.registrar()
        medicos.append(medico)
        print("Médico registrado exitosamente!")
    elif opcion == "3":
        enfermera = Enfermera.registrar()
        enfermeras.append(enfermera)
        print("Enfermera registrada exitosamente!")
    else:
        print("Opción no válida")

def editar_persona(pacientes, medicos, enfermeras):
    """Función para editar personas existentes"""
    print("\n--- EDITAR PERSONA ---")
    print("1. Editar Paciente")
    print("2. Editar Médico")
    print("3. Editar Enfermera")
    
    opcion = input("Seleccione tipo de persona: ")
    
    if opcion == "1":
        editar_paciente(pacientes)
    elif opcion == "2":
        editar_medico(medicos)
    elif opcion == "3":
        editar_enfermera(enfermeras)
    else:
        print("Opción no válida")

def validar_indice(entrada: str, maximo: int) -> int:
    """Valida que la entrada sea un índice válido"""
    if not entrada.isdigit():
        return -1
    
    idx = int(entrada) - 1
    if idx < 0 or idx >= maximo:
        return -1
    
    return idx

def editar_paciente(pacientes):
    """Función para editar un paciente específico"""
    if not pacientes:
        print("No hay pacientes registrados")
        return
    
    print("\nPACIENTES DISPONIBLES:")
    for i, paciente in enumerate(pacientes, 1):
        print(f"{i}. {paciente._nombre}")
    
    entrada = input("Seleccione paciente a editar (número): ")
    idx = validar_indice(entrada, len(pacientes))
    
    if idx == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(pacientes))
        return
        
    paciente = pacientes[idx]
    print(f"\nEditando paciente: {paciente._nombre}")
    
    nuevo_nombre = input(f"Nuevo nombre ({paciente._nombre}): ") or paciente._nombre
    nueva_fecha = input(f"Nueva fecha ({paciente._fecha_nac}): ") or paciente._fecha_nac
    nuevo_telefono = input(f"Nuevo teléfono ({paciente._telefono}): ") or paciente._telefono
    nueva_direccion = input(f"Nueva dirección ({paciente._direccion}): ") or paciente._direccion
    
    paciente._nombre = nuevo_nombre
    paciente._fecha_nac = nueva_fecha
    paciente._telefono = nuevo_telefono
    paciente._direccion = nueva_direccion
    
    print("Paciente actualizado exitosamente")

def editar_medico(medicos):
    """Función para editar un médico específico"""
    if not medicos:
        print("No hay médicos registrados")
        return
    
    print("\nMÉDICOS DISPONIBLES:")
    for i, medico in enumerate(medicos, 1):
        print(f"{i}. Dr. {medico._nombre} - {medico._especialidad}")
    
    entrada = input("Seleccione médico a editar (número): ")
    idx = validar_indice(entrada, len(medicos))
    
    if idx == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(medicos))
        return
        
    medico = medicos[idx]
    print(f"\nEditando médico: Dr. {medico._nombre}")
    
    nuevo_nombre = input(f"Nuevo nombre ({medico._nombre}): ") or medico._nombre
    nueva_fecha = input(f"Nueva fecha ({medico._fecha_nac}): ") or medico._fecha_nac
    nuevo_telefono = input(f"Nuevo teléfono ({medico._telefono}): ") or medico._telefono
    nueva_direccion = input(f"Nueva dirección ({medico._direccion}): ") or medico._direccion
    nueva_especialidad = input(f"Nueva especialidad ({medico._especialidad}): ") or medico._especialidad
    
    medico._nombre = nuevo_nombre
    medico._fecha_nac = nueva_fecha
    medico._telefono = nuevo_telefono
    medico._direccion = nueva_direccion
    medico._especialidad = nueva_especialidad
    
    print("Médico actualizado exitosamente")

def editar_enfermera(enfermeras):
    """Función para editar una enfermera específica"""
    if not enfermeras:
        print("No hay enfermeras registradas")
        return
    
    print("\nENFERMERAS DISPONIBLES:")
    for i, enfermera in enumerate(enfermeras, 1):
        print(f"{i}. {enfermera._nombre} - {enfermera._turno}")
    
    entrada = input("Seleccione enfermera a editar (número): ")
    idx = validar_indice(entrada, len(enfermeras))
    
    if idx == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(enfermeras))
        return
        
    enfermera = enfermeras[idx]
    print(f"\nEditando enfermera: {enfermera._nombre}")
    
    nuevo_nombre = input(f"Nuevo nombre ({enfermera._nombre}): ") or enfermera._nombre
    nueva_fecha = input(f"Nueva fecha ({enfermera._fecha_nac}): ") or enfermera._fecha_nac
    nuevo_telefono = input(f"Nuevo teléfono ({enfermera._telefono}): ") or enfermera._telefono
    nueva_direccion = input(f"Nueva dirección ({enfermera._direccion}): ") or enfermera._direccion
    nuevo_turno = input(f"Nuevo turno ({enfermera._turno}): ") or enfermera._turno
    
    enfermera._nombre = nuevo_nombre
    enfermera._fecha_nac = nueva_fecha
    enfermera._telefono = nuevo_telefono
    enfermera._direccion = nueva_direccion
    enfermera._turno = nuevo_turno
    
    print("Enfermera actualizada exitosamente")

def eliminar_persona(pacientes, medicos, enfermeras):
    """Función para eliminar personas"""
    print("\n--- ELIMINAR PERSONA ---")
    print("1. Eliminar Paciente")
    print("2. Eliminar Médico")
    print("3. Eliminar Enfermera")
    
    opcion = input("Seleccione tipo de persona: ")
    
    if opcion == "1":
        eliminar_paciente(pacientes)
    elif opcion == "2":
        eliminar_medico(medicos)
    elif opcion == "3":
        eliminar_enfermera(enfermeras)
    else:
        print("Opción no válida")

def eliminar_paciente(pacientes):
    """Función para eliminar un paciente específico"""
    if not pacientes:
        print("No hay pacientes registrados")
        return
    
    print("\nPACIENTES DISPONIBLES:")
    for i, paciente in enumerate(pacientes, 1):
        print(f"{i}. {paciente._nombre}")
    
    entrada = input("Seleccione paciente a eliminar (número): ")
    idx = validar_indice(entrada, len(pacientes))
    
    if idx == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(pacientes))
        return
        
    paciente = pacientes[idx]
    confirmacion = input(f"¿Está seguro de eliminar a {paciente._nombre}? (s/n): ")
    
    if confirmacion.lower() == 's':
        pacientes.pop(idx)
        print("Paciente eliminado exitosamente")
    else:
        print("Operación cancelada")

def eliminar_medico(medicos):
    """Función para eliminar un médico específico"""
    if not medicos:
        print("No hay médicos registrados")
        return
    
    print("\nMÉDICOS DISPONIBLES:")
    for i, medico in enumerate(medicos, 1):
        print(f"{i}. Dr. {medico._nombre} - {medico._especialidad}")
    
    entrada = input("Seleccione médico a eliminar (número): ")
    idx = validar_indice(entrada, len(medicos))
    
    if idx == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(medicos))
        return
        
    medico = medicos[idx]
    confirmacion = input(f"¿Está seguro de eliminar al Dr. {medico._nombre}? (s/n): ")
    
    if confirmacion.lower() == 's':
        medicos.pop(idx)
        print("Médico eliminado exitosamente")
    else:
        print("Operación cancelada")

def eliminar_enfermera(enfermeras):
    """Función para eliminar una enfermera específica"""
    if not enfermeras:
        print("No hay enfermeras registradas")
        return
    
    print("\nENFERMERAS DISPONIBLES:")
    for i, enfermera in enumerate(enfermeras, 1):
        print(f"{i}. {enfermera._nombre} - {enfermera._turno}")
    
    entrada = input("Seleccione enfermera a eliminar (número): ")
    idx = validar_indice(entrada, len(enfermeras))
    
    if idx == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(enfermeras))
        return
        
    enfermera = enfermeras[idx]
    confirmacion = input(f"¿Está seguro de eliminar a {enfermera._nombre}? (s/n): ")
    
    if confirmacion.lower() == 's':
        enfermeras.pop(idx)
        print("Enfermera eliminada exitosamente")
    else:
        print("Operación cancelada")

def submenu_registro(pacientes, medicos, enfermeras):
    """Submenú para gestionar registros de personas"""
    while True:
        print("\n" + "="*40)
        print("        REGISTRO")
        print("="*40)
        print("1. Registrar")
        print("2. Editar")
        print("3. Eliminar")
        print("4. Mostrar Todos los Registros")
        print("0. Volver al Menú Principal")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_persona(pacientes, medicos, enfermeras)
        elif opcion == "2":
            editar_persona(pacientes, medicos, enfermeras)
        elif opcion == "3":
            eliminar_persona(pacientes, medicos, enfermeras)
        elif opcion == "4":
            mostrar_todos(pacientes, medicos, enfermeras)
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

def submenu_citas(pacientes, medicos):
    """Submenú para gestionar citas médicas"""
    while True:
        print("\n" + "="*40)
        print("        CITAS")
        print("="*40)
        print("1. Agendar Cita")
        print("2. Ver Citas de Paciente")
        print("3. Ver Citas de Médico")
        print("4. Ver Citas por Fecha")
        print("5. Cancelar Cita")
        print("0. Volver al Menú Principal")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agendar_cita_sistema(pacientes, medicos)
        elif opcion == "2":
            print("Función en desarrollo...")
        elif opcion == "3":
            print("Función en desarrollo...")
        elif opcion == "4":
            print("Función en desarrollo...")
        elif opcion == "5":
            print("Función en desarrollo...")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

def submenu_facturas(pacientes, medicos, enfermeras):
    """Submenú para gestionar facturación"""
    while True:
        print("\n" + "="*40)
        print("        FACTURAS")
        print("="*40)
        print("1. Emitir Factura por Consulta")
        print("2. Emitir Factura por Servicio de Enfermería")
        print("3. Ver Facturas de Paciente")
        print("4. Ver Facturas por Fecha")
        print("5. Generar Reporte de Facturación")
        print("0. Volver al Menú Principal")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("Función en desarrollo...")
        elif opcion == "2":
            print("Función en desarrollo...")
        elif opcion == "3":
            print("Función en desarrollo...")
        elif opcion == "4":
            print("Función en desarrollo...")
        elif opcion == "5":
            print("Función en desarrollo...")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

def submenu_diagnostico(pacientes, medicos):
    """Submenú para registrar diagnósticos médicos"""
    while True:
        print("\n" + "="*40)
        print("        DIAGNÓSTICO")
        print("="*40)
        print("1. Registrar Diagnóstico")
        print("2. Ver Historial de Diagnósticos")
        print("3. Buscar Diagnósticos por Paciente")
        print("4. Buscar Diagnósticos por Médico")
        print("5. Actualizar Diagnóstico")
        print("0. Volver al Menú Principal")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            print("Función en desarrollo...")
        elif opcion == "2":
            print("Función en desarrollo...")
        elif opcion == "3":
            print("Función en desarrollo...")
        elif opcion == "4":
            print("Función en desarrollo...")
        elif opcion == "5":
            print("Función en desarrollo...")
        elif opcion == "0":
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

def agendar_cita_sistema(pacientes, medicos):
    """Función para agendar citas desde el sistema"""
    if not pacientes:
        print("No hay pacientes registrados")
        return
    if not medicos:
        print("No hay médicos registrados")
        return
    
    print("\n--- AGENDAR CITA DESDE SISTEMA ---")
    
    print("PACIENTES DISPONIBLES:")
    for i, paciente in enumerate(pacientes, 1):
        print(f"{i}. {paciente._nombre}")
    
    entrada_paciente = input("Seleccione paciente (número): ")
    idx_paciente = validar_indice(entrada_paciente, len(pacientes))
    
    if idx_paciente == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(pacientes))
        return
    
    paciente = pacientes[idx_paciente]
    
    print("\nMÉDICOS DISPONIBLES:")
    for i, medico in enumerate(medicos, 1):
        print(f"{i}. Dr. {medico._nombre} - {medico._especialidad}")
    
    entrada_medico = input("Seleccione médico (número): ")
    idx_medico = validar_indice(entrada_medico, len(medicos))
    
    if idx_medico == -1:
        print("Error: Debe ingresar un número válido entre 1 y", len(medicos))
        return
    
    medico = medicos[idx_medico]
    
    fecha = input("Fecha (dd/mm/yyyy): ")
    hora = input("Hora (HH:MM): ")
    motivo = input("Motivo de la consulta: ")
    
    from schemas import validar_campo_fecha_servicio, validar_campo_hora, validar_campo_motivo
    
    es_valido_fecha, mensaje_fecha = validar_campo_fecha_servicio(fecha)
    if not es_valido_fecha:
        print(f"Error en fecha: {mensaje_fecha}")
        return
    
    es_valido_hora, mensaje_hora = validar_campo_hora(hora)
    if not es_valido_hora:
        print(f"Error en hora: {mensaje_hora}")
        return
    
    es_valido_motivo, mensaje_motivo = validar_campo_motivo(motivo)
    if not es_valido_motivo:
        print(f"Error en motivo: {mensaje_motivo}")
        return
    
    cita = medico.agendar_cita_paciente(paciente, fecha, hora, motivo)
    print("Cita agendada exitosamente")
    cita.mostrar_cita()

def main():
    """Función principal del sistema"""
    print("¡Bienvenido al Sistema de Registro Hospitalario!")
    
    pacientes: List[Paciente] = []
    medicos: List[Medico] = []
    enfermeras: List['Enfermera'] = []
    
    while True:
        print("\n" + "="*40)
        print("        MENÚ PRINCIPAL")
        print("="*40)
        print("1. Registro")
        print("2. Citas")
        print("3. Facturas")
        print("4. Diagnóstico")
        print("0. Salir")
        print("="*40)
        
        opcion: str = input("Seleccione una opción: ")
        
        if opcion == "1":
            submenu_registro(pacientes, medicos, enfermeras)
        elif opcion == "2":
            submenu_citas(pacientes, medicos)
        elif opcion == "3":
            submenu_facturas(pacientes, medicos, enfermeras)
        elif opcion == "4":
            submenu_diagnostico(pacientes, medicos)
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()




