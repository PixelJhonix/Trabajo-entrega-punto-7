"""
Script de prueba para verificar las entidades ORM
"""

from database.config import create_tables, engine
from entities import (
    Paciente,
    Medico,
    Enfermera,
    Cita,
    Hospitalizacion,
    Factura,
    FacturaDetalle,
    HistorialMedico,
    HistorialEntrada,
)


def test_entities():
    """Probar que las entidades se pueden importar y crear"""
    print("🏥 Probando entidades del Sistema Hospitalario...")

    try:
        # Crear las tablas
        print("📋 Creando tablas en la base de datos...")
        create_tables()
        print("✅ Tablas creadas exitosamente")

        # Verificar que las entidades se pueden instanciar
        print("\n👤 Probando entidad Paciente...")
        paciente = Paciente(
            primer_nombre="Juan",
            apellido="Pérez",
            fecha_nacimiento="1990-05-15",
            telefono="+57 300 123 4567",
            email="juan.perez@email.com",
            direccion="Calle 123 #45-67, Bogotá",
        )
        print(f"✅ Paciente creado: {paciente}")

        print("\n👨‍⚕️ Probando entidad Medico...")
        medico = Medico(
            primer_nombre="Carlos",
            apellido="García",
            fecha_nacimiento="1985-03-20",
            especialidad="Cardiología",
            numero_licencia="MED-12345",
            consultorio="101",
            telefono="+57 300 987 6543",
            email="dr.garcia@hospital.com",
            direccion="Calle 456 #78-90, Bogotá",
        )
        print(f"✅ Médico creado: {medico}")

        print("\n👩‍⚕️ Probando entidad Enfermera...")
        enfermera = Enfermera(
            primer_nombre="María",
            apellido="López",
            fecha_nacimiento="1992-08-10",
            especialidad="Cuidados Intensivos",
            numero_licencia="ENF-67890",
            turno="Mañana",
            telefono="+57 300 555 1234",
            email="maria.lopez@hospital.com",
            direccion="Calle 789 #12-34, Bogotá",
        )
        print(f"✅ Enfermera creada: {enfermera}")

        print("\n📅 Probando entidad Cita...")
        cita = Cita(
            paciente_id=paciente.id,
            medico_id=medico.id,
            fecha="2024-01-15",
            hora="10:30:00",
            motivo="Consulta de rutina",
            estado="Agendada",
        )
        print(f"✅ Cita creada: {cita}")

        print("\n🏥 Probando entidad Hospitalizacion...")
        hospitalizacion = Hospitalizacion(
            paciente_id=paciente.id,
            medico_responsable_id=medico.id,
            enfermera_asignada_id=enfermera.id,
            tipo_cuidado="Intensivo",
            descripcion="Hospitalización por complicaciones cardíacas",
            numero_habitacion="ICU-101",
            tipo_habitacion="Individual",
            fecha_inicio="2024-01-10",
            estado="Activa",
        )
        print(f"✅ Hospitalización creada: {hospitalizacion}")

        print("\n💵 Probando entidad Factura...")
        factura = Factura(
            paciente_id=paciente.id,
            numero_factura="FAC-2024-001",
            fecha_emision="2024-01-15",
            fecha_limite_pago="2024-02-15",
            total=150000.00,
            estado="Pendiente",
        )
        print(f"✅ Factura creada: {factura}")

        print("\n📋 Probando entidad FacturaDetalle...")
        factura_detalle = FacturaDetalle(
            factura_id=factura.id,
            cita_id=cita.id,
            descripcion="Consulta médica especializada",
            cantidad=1,
            precio_unitario=150000.00,
            subtotal=150000.00,
        )
        print(f"✅ Detalle de factura creado: {factura_detalle}")

        print("\n📋 Probando entidad HistorialMedico...")
        historial = HistorialMedico(
            paciente_id=paciente.id,
            numero_historial="HIST-2024-001",
            fecha_apertura="2024-01-01",
            estado="Activo",
        )
        print(f"✅ Historial médico creado: {historial}")

        print("\n📝 Probando entidad HistorialEntrada...")
        entrada = HistorialEntrada(
            historial_id=historial.id,
            medico_id=medico.id,
            cita_id=cita.id,
            diagnostico="Hipertensión arterial",
            tratamiento="Medicamentos antihipertensivos",
            notas="Paciente requiere seguimiento mensual",
            fecha_registro="2024-01-15",
        )
        print(f"✅ Entrada de historial creada: {entrada}")

        print("\n🎉 ¡Todas las entidades funcionan correctamente!")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


if __name__ == "__main__":
    test_entities()
