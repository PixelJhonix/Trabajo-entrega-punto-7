"""
Script simple para probar importaciones
"""


def test_imports():
    """Probar que todas las entidades se pueden importar"""
    print("🧪 Probando importaciones...")

    try:
        # Probar importaciones individuales
        from entities.paciente import Paciente

        print("✅ Paciente importado")

        from entities.medico import Medico

        print("✅ Medico importado")

        from entities.enfermera import Enfermera

        print("✅ Enfermera importada")

        from entities.cita import Cita

        print("✅ Cita importada")

        from entities.hospitalizacion import Hospitalizacion

        print("✅ Hospitalizacion importada")

        from entities.factura import Factura

        print("✅ Factura importada")

        from entities.factura_detalle import FacturaDetalle

        print("✅ FacturaDetalle importada")

        from entities.historial_medico import HistorialMedico

        print("✅ HistorialMedico importado")

        from entities.historial_entrada import HistorialEntrada

        print("✅ HistorialEntrada importada")

        # Probar importación desde __init__.py
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

        print("✅ Todas las entidades importadas desde __init__.py")

        # Probar que se pueden instanciar (sin guardar en BD)
        paciente = Paciente(
            primer_nombre="Juan",
            apellido="Pérez",
            fecha_nacimiento="1990-05-15",
            telefono="+57 300 123 4567",
            direccion="Calle 123 #45-67, Bogotá",
        )
        print(f"✅ Paciente instanciado: {paciente}")

        medico = Medico(
            primer_nombre="Carlos",
            apellido="García",
            fecha_nacimiento="1985-03-20",
            especialidad="Cardiología",
            numero_licencia="MED-12345",
            telefono="+57 300 987 6543",
            direccion="Calle 456 #78-90, Bogotá",
        )
        print(f"✅ Medico instanciado: {medico}")

        print("\n🎉 ¡Todas las pruebas de importación exitosas!")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_imports()
