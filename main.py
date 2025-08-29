""" 7. Hospital / Clínica
 Pacientes, médicos, enfermeras. 
 Operaciones: agendar cita, registrar diagnóstico, emitir factura. """

from paciente import Paciente
from medico import Medico
from enfermera import Enfermera

print("---------------BIENVENIDOS A HOSPITAL LOS ENANOS---------------")

def mostrar_todos(pacientes, medicos, enfermeras):
    """Función para mostrar todas las personas registradas"""
    print("\n--- LISTADO COMPLETO ---")
    
    if pacientes:
        print(f"\n📋 PACIENTES ({len(pacientes)}):")
        for paciente in pacientes:
            paciente.mostrardatos()
            print("-" * 30)
    
    if medicos:
        print(f"\n👨‍⚕️ MÉDICOS ({len(medicos)}):")
        for medico in medicos:
            medico.mostrardatos()
            print("-" * 30)
    
    if enfermeras:
        print(f"\n👩‍⚕️ ENFERMERAS ({len(enfermeras)}):")
        for enfermera in enfermeras:
            enfermera.mostrardatos()
            print("-" * 30)

def main():
    """Función principal del sistema"""
    print("¡Bienvenido al Sistema de Registro Hospitalario!")
    
    # Listas para almacenar los registros
    pacientes = []
    medicos = []
    enfermeras = []
    
    while True:
        print("\n" + "="*40)
        print("        MENÚ PRINCIPAL")
        print("="*40)
        print("1. Registrar Paciente")
        print("2. Registrar Médico")
        print("3. Registrar Enfermera")
        print("4. Mostrar Todos los Registros")
        print("0. Salir")
        print("="*40)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            paciente = Paciente.registrar()  # ← Usar método de clase
            pacientes.append(paciente)
            print("✅ Paciente registrado exitosamente!")
        elif opcion == "2":
            medico = Medico.registrar()      # ← Usar método de clase
            medicos.append(medico)
            print("✅ Médico registrado exitosamente!")
        elif opcion == "3":
            enfermera = Enfermera.registrar() # ← Usar método de clase
            enfermeras.append(enfermera)
            print("✅ Enfermera registrada exitosamente!")
        elif opcion == "4":
            mostrar_todos(pacientes, medicos, enfermeras)
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()




