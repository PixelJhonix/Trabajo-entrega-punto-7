"""
Script de pruebas automatizadas para verificar el sistema
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    """Verificar que todas las importaciones funcionan"""
    print("=" * 50)
    print("TEST 1: Verificando importaciones...")
    print("=" * 50)

    errors = []

    try:
        from entities.usuario import Usuario

        print("✓ Usuario importado correctamente")
    except Exception as e:
        errors.append(f"Usuario: {str(e)}")
        print(f"✗ Error importando Usuario: {str(e)}")

    try:
        from entities.paciente import Paciente

        print("✓ Paciente importado correctamente")
    except Exception as e:
        errors.append(f"Paciente: {str(e)}")
        print(f"✗ Error importando Paciente: {str(e)}")

    try:
        from entities.medico import Medico

        print("✓ Medico importado correctamente")
    except Exception as e:
        errors.append(f"Medico: {str(e)}")
        print(f"✗ Error importando Medico: {str(e)}")

    try:
        from entities.enfermera import Enfermera

        print("✓ Enfermera importada correctamente")
    except Exception as e:
        errors.append(f"Enfermera: {str(e)}")
        print(f"✗ Error importando Enfermera: {str(e)}")

    try:
        from entities.cita import Cita

        print("✓ Cita importada correctamente")
    except Exception as e:
        errors.append(f"Cita: {str(e)}")
        print(f"✗ Error importando Cita: {str(e)}")

    try:
        from entities.hospitalizacion import Hospitalizacion

        print("✓ Hospitalizacion importada correctamente")
    except Exception as e:
        errors.append(f"Hospitalizacion: {str(e)}")
        print(f"✗ Error importando Hospitalizacion: {str(e)}")

    try:
        from entities.factura import Factura

        print("✓ Factura importada correctamente")
    except Exception as e:
        errors.append(f"Factura: {str(e)}")
        print(f"✗ Error importando Factura: {str(e)}")

    try:
        from entities.factura_detalle import FacturaDetalle

        print("✓ FacturaDetalle importada correctamente")
    except Exception as e:
        errors.append(f"FacturaDetalle: {str(e)}")
        print(f"✗ Error importando FacturaDetalle: {str(e)}")

    try:
        from entities.historial_medico import HistorialMedico

        print("✓ HistorialMedico importado correctamente")
    except Exception as e:
        errors.append(f"HistorialMedico: {str(e)}")
        print(f"✗ Error importando HistorialMedico: {str(e)}")

    try:
        from entities.historial_entrada import HistorialEntrada

        print("✓ HistorialEntrada importado correctamente")
    except Exception as e:
        errors.append(f"HistorialEntrada: {str(e)}")
        print(f"✗ Error importando HistorialEntrada: {str(e)}")

    return errors


def test_entities():
    """Verificar que las entidades tienen los campos correctos"""
    print("\n" + "=" * 50)
    print("TEST 2: Verificando estructura de entidades...")
    print("=" * 50)

    errors = []

    try:
        from entities.medico import Medico

        # Verificar que no tenga primer_nombre o segundo_nombre
        if hasattr(Medico, "primer_nombre") or hasattr(Medico, "segundo_nombre"):
            errors.append(
                "Medico tiene campos primer_nombre o segundo_nombre (debería tener nombre y apellido)"
            )
            print("✗ Medico tiene campos incorrectos")
        else:
            if hasattr(Medico, "nombre") and hasattr(Medico, "apellido"):
                print("✓ Medico tiene nombre y apellido correctamente")
            else:
                errors.append("Medico no tiene nombre o apellido")
                print("✗ Medico no tiene nombre o apellido")
    except Exception as e:
        errors.append(f"Error verificando Medico: {str(e)}")
        print(f"✗ Error: {str(e)}")

    return errors


def test_cruds():
    """Verificar que los CRUDs se pueden instanciar"""
    print("\n" + "=" * 50)
    print("TEST 3: Verificando CRUDs...")
    print("=" * 50)

    errors = []

    cruds = [
        "usuario_crud",
        "paciente_crud",
        "medico_crud",
        "enfermera_crud",
        "cita_crud",
        "hospitalizacion_crud",
        "factura_crud",
        "factura_detalle_crud",
        "historial_medico_crud",
        "historial_entrada_crud",
    ]

    for crud_name in cruds:
        try:
            module = __import__(f"crud.{crud_name}", fromlist=[crud_name])
            crud_class = getattr(
                module, crud_name.replace("_crud", "").title().replace("_", "") + "CRUD"
            )
            print(f"✓ {crud_name} importado correctamente")
        except Exception as e:
            errors.append(f"{crud_name}: {str(e)}")
            print(f"✗ Error importando {crud_name}: {str(e)}")

    return errors


def test_schemas():
    """Verificar que los schemas se pueden importar"""
    print("\n" + "=" * 50)
    print("TEST 4: Verificando schemas...")
    print("=" * 50)

    errors = []

    try:
        from schemas import (
            UsuarioBase,
            UsuarioCreate,
            UsuarioResponse,
            PacienteBase,
            PacienteCreate,
            PacienteResponse,
            MedicoBase,
            MedicoCreate,
            MedicoResponse,
            EnfermeraBase,
            EnfermeraCreate,
            EnfermeraResponse,
        )

        print("✓ Schemas principales importados correctamente")
    except Exception as e:
        errors.append(f"Schemas: {str(e)}")
        print(f"✗ Error importando schemas: {str(e)}")

    # Verificar que MedicoBase no tenga primer_nombre
    try:
        from schemas import MedicoBase

        if hasattr(MedicoBase, "primer_nombre") or hasattr(
            MedicoBase, "segundo_nombre"
        ):
            errors.append("MedicoBase tiene campos primer_nombre o segundo_nombre")
            print("✗ MedicoBase tiene campos incorrectos")
        else:
            print("✓ MedicoBase tiene estructura correcta")
    except Exception as e:
        errors.append(f"Error verificando MedicoBase: {str(e)}")
        print(f"✗ Error: {str(e)}")

    return errors


def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "=" * 50)
    print("PRUEBAS DEL SISTEMA HOSPITALARIO")
    print("=" * 50 + "\n")

    all_errors = []

    # Ejecutar pruebas
    all_errors.extend(test_imports())
    all_errors.extend(test_entities())
    all_errors.extend(test_cruds())
    all_errors.extend(test_schemas())

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN")
    print("=" * 50)

    if not all_errors:
        print("\n✓ TODAS LAS PRUEBAS PASARON")
        print("El sistema está listo para usar.")
        return 0
    else:
        print(f"\n✗ SE ENCONTRARON {len(all_errors)} ERROR(ES):")
        for error in all_errors:
            print(f"  - {error}")
        return 1


if __name__ == "__main__":
    exit(main())
