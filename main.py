""" 7. Hospital / Clínica
 Pacientes, médicos, enfermeras. 
 Operaciones: agendar cita, registrar diagnóstico, emitir factura. """

print("---------------BIENVENIDOS A HOSPITAL LOS ENANOS---------------")

# ==========================================
# CLASE PADRE - PERSONA
# ==========================================

class Persona:
    """Clase padre para todas las personas del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str):
        self._nombre = nombre
        self._fecha_nac = fecha_nac
        self._telefono = telefono
        self._direccion = direccion
    
    def mostrardatos(self) -> None:
        """Muestra todos los datos de la persona"""
        print(f"Nombre: {self._nombre}")
        print(f"Fecha de nacimiento: {self._fecha_nac}")
        print(f"Teléfono: {self._telefono}")
        print(f"Dirección: {self._direccion}")


# ==========================================
# CLASE HIJA - PACIENTE
# ==========================================

class Paciente(Persona):
    """Clase para pacientes del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._tipo = "Paciente"
    
    def mostrardatos(self) -> None:
        """Muestra datos del paciente"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()


# ==========================================
# CLASE HIJA - MEDICO
# ==========================================

class Medico(Persona):
    """Clase para médicos del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, especialidad: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._especialidad = especialidad
        self._tipo = "Médico"
    
    def mostrardatos(self) -> None:
        """Muestra datos del médico"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Especialidad: {self._especialidad}")


# ==========================================
# CLASE HIJA - ENFERMERA
# ==========================================

class Enfermera(Persona):
    """Clase para enfermeras del hospital"""
    
    def __init__(self, nombre: str, fecha_nac: str, telefono: str, direccion: str, turno: str):
        super().__init__(nombre, fecha_nac, telefono, direccion)
        self._turno = turno
        self._tipo = "Enfermera"
    
    def mostrardatos(self) -> None:
        """Muestra datos de la enfermera"""
        print(f"--- {self._tipo.upper()} ---")
        super().mostrardatos()
        print(f"Turno: {self._turno}")


# ==========================================
# FUNCIONES DE REGISTRO
# ==========================================

def registrar_paciente():
    """Función para registrar un nuevo paciente"""
    print("\n--- REGISTRAR NUEVO PACIENTE ---")
    
    nombre = input("Nombre: ")
    fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    
    paciente = Paciente(nombre, fecha_nac, telefono, direccion)
    print("✅ Paciente registrado exitosamente!")
    return paciente


def registrar_medico():
    """Función para registrar un nuevo médico"""
    print("\n--- REGISTRAR NUEVO MÉDICO ---")
    
    nombre = input("Nombre: ")
    fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    especialidad = input("Especialidad: ")
    
    medico = Medico(nombre, fecha_nac, telefono, direccion, especialidad)
    print("✅ Médico registrado exitosamente!")
    return medico


def registrar_enfermera():
    """Función para registrar una nueva enfermera"""
    print("\n--- REGISTRAR NUEVA ENFERMERA ---")
    
    nombre = input("Nombre: ")
    fecha_nac = input("Fecha de nacimiento (dd/mm/yyyy): ")
    telefono = input("Teléfono: ")
    direccion = input("Dirección: ")
    turno = input("Turno (Mañana/Tarde/Noche): ")
    
    enfermera = Enfermera(nombre, fecha_nac, telefono, direccion, turno)
    print("✅ Enfermera registrada exitosamente!")
    return enfermera


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


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

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
            paciente = registrar_paciente()
            pacientes.append(paciente)
        elif opcion == "2":
            medico = registrar_medico()
            medicos.append(medico)
        elif opcion == "3":
            enfermera = registrar_enfermera()
            enfermeras.append(enfermera)
        elif opcion == "4":
            mostrar_todos(pacientes, medicos, enfermeras)
        elif opcion == "0":
            print("¡Gracias por usar el sistema!")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")


# ==========================================
# EJECUTAR EL PROGRAMA
# ==========================================

if __name__ == "__main__":
    main()




