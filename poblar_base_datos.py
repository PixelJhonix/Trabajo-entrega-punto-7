"""Script para poblar la base de datos con datos de prueba realistas."""

import random
from datetime import date, time, timedelta
from decimal import Decimal
from uuid import uuid4

from database.config import SessionLocal, create_tables
from auth.security import get_password_hash
from crud.usuario_crud import UsuarioCRUD
from crud.paciente_crud import PacienteCRUD
from crud.medico_crud import MedicoCRUD
from crud.enfermera_crud import EnfermeraCRUD
from crud.cita_crud import CitaCRUD
from crud.hospitalizacion_crud import HospitalizacionCRUD
from crud.factura_crud import FacturaCRUD
from crud.factura_detalle_crud import FacturaDetalleCRUD
from crud.historial_medico_crud import HistorialMedicoCRUD
from crud.historial_entrada_crud import HistorialEntradaCRUD


def poblar_base_datos():
    """Poblar la base de datos con datos de prueba realistas."""
    print("=== POBLANDO BASE DE DATOS ===")

    # Crear tablas si no existen
    create_tables()
    print("Base de datos inicializada")

    db = SessionLocal()

    try:
        # Crear CRUDs
        usuario_crud = UsuarioCRUD(db)
        paciente_crud = PacienteCRUD(db)
        medico_crud = MedicoCRUD(db)
        enfermera_crud = EnfermeraCRUD(db)
        cita_crud = CitaCRUD(db)
        hospitalizacion_crud = HospitalizacionCRUD(db)
        factura_crud = FacturaCRUD(db)
        factura_detalle_crud = FacturaDetalleCRUD(db)
        historial_medico_crud = HistorialMedicoCRUD(db)
        historial_entrada_crud = HistorialEntradaCRUD(db)

        # 1. Crear administrador
        print("Creando administrador...")
        admin_id = uuid4()
        admin = usuario_crud.crear_usuario(
            id=admin_id,
            nombre="Dr. Carlos Mendoza",
            nombre_usuario="admin",
            email="admin@hospital.com",
            contraseña=get_password_hash("admin123"),
            telefono="+57 300 123 4567",
            es_admin=True,
            id_usuario_creacion=admin_id,
        )
        print(f"Administrador creado: {admin.nombre}")

        # 2. Crear usuarios adicionales
        print("Creando usuarios adicionales...")
        usuarios_data = [
            {
                "nombre": "María Elena Rodríguez",
                "nombre_usuario": "mrodriguez",
                "email": "maria.rodriguez@hospital.com",
                "telefono": "+57 300 234 5678",
                "es_admin": False,
            },
            {
                "nombre": "José Antonio Silva",
                "nombre_usuario": "jsilva",
                "email": "jose.silva@hospital.com",
                "telefono": "+57 300 345 6789",
                "es_admin": False,
            },
            {
                "nombre": "Ana Patricia López",
                "nombre_usuario": "alopez",
                "email": "ana.lopez@hospital.com",
                "telefono": "+57 300 456 7890",
                "es_admin": False,
            },
        ]

        usuarios = [admin]
        for user_data in usuarios_data:
            usuario = usuario_crud.crear_usuario(
                nombre=user_data["nombre"],
                nombre_usuario=user_data["nombre_usuario"],
                email=user_data["email"],
                contraseña=get_password_hash("password123"),
                telefono=user_data["telefono"],
                es_admin=user_data["es_admin"],
                id_usuario_creacion=admin_id,
            )
            usuarios.append(usuario)
        print(f"Usuarios creados: {len(usuarios)}")

        # 3. Crear médicos
        print("Creando médicos...")
        medicos_data = [
            {
                "primer_nombre": "Alejandro",
                "segundo_nombre": "Carlos",
                "apellido": "García",
                "fecha_nacimiento": date(1975, 3, 15),
                "especialidad": "Cardiología",
                "numero_licencia": "MED-001234",
                "consultorio": "A-101",
                "telefono": "+57 300 111 1111",
                "email": "alejandro.garcia@hospital.com",
                "direccion": "Calle 100 #15-20, Bogotá",
            },
            {
                "primer_nombre": "Isabel",
                "segundo_nombre": "María",
                "apellido": "Fernández",
                "fecha_nacimiento": date(1980, 7, 22),
                "especialidad": "Pediatría",
                "numero_licencia": "MED-001235",
                "consultorio": "B-205",
                "telefono": "+57 300 222 2222",
                "email": "isabel.fernandez@hospital.com",
                "direccion": "Carrera 15 #85-30, Bogotá",
            },
            {
                "primer_nombre": "Roberto",
                "apellido": "Martínez",
                "fecha_nacimiento": date(1972, 11, 8),
                "especialidad": "Neurología",
                "numero_licencia": "MED-001236",
                "consultorio": "C-301",
                "telefono": "+57 300 333 3333",
                "email": "roberto.martinez@hospital.com",
                "direccion": "Avenida 68 #25-40, Bogotá",
            },
            {
                "primer_nombre": "Carmen",
                "segundo_nombre": "Elena",
                "apellido": "Vargas",
                "fecha_nacimiento": date(1978, 5, 12),
                "especialidad": "Ginecología",
                "numero_licencia": "MED-001237",
                "consultorio": "D-401",
                "telefono": "+57 300 444 4444",
                "email": "carmen.vargas@hospital.com",
                "direccion": "Calle 80 #12-15, Bogotá",
            },
            {
                "primer_nombre": "Diego",
                "apellido": "Ramírez",
                "fecha_nacimiento": date(1983, 9, 30),
                "especialidad": "Ortopedia",
                "numero_licencia": "MED-001238",
                "consultorio": "E-501",
                "telefono": "+57 300 555 5555",
                "email": "diego.ramirez@hospital.com",
                "direccion": "Carrera 7 #32-10, Bogotá",
            },
        ]

        medicos = []
        for med_data in medicos_data:
            medico = medico_crud.crear_medico(
                primer_nombre=med_data["primer_nombre"],
                apellido=med_data["apellido"],
                fecha_nacimiento=med_data["fecha_nacimiento"],
                especialidad=med_data["especialidad"],
                numero_licencia=med_data["numero_licencia"],
                telefono=med_data["telefono"],
                direccion=med_data["direccion"],
                id_usuario_creacion=admin_id,
                segundo_nombre=med_data.get("segundo_nombre"),
                consultorio=med_data.get("consultorio"),
                email=med_data.get("email"),
            )
            medicos.append(medico)
        print(f"Médicos creados: {len(medicos)}")

        # 4. Crear enfermeras
        print("Creando enfermeras...")
        enfermeras_data = [
            {
                "primer_nombre": "Sandra",
                "apellido": "Jiménez",
                "fecha_nacimiento": date(1985, 2, 14),
                "especialidad": "Cuidados Intensivos",
                "numero_licencia": "ENF-001001",
                "turno": "Mañana",
                "telefono": "+57 300 666 6666",
                "email": "sandra.jimenez@hospital.com",
                "direccion": "Calle 50 #25-30, Bogotá",
            },
            {
                "primer_nombre": "Luis",
                "segundo_nombre": "Alberto",
                "apellido": "Torres",
                "fecha_nacimiento": date(1987, 8, 25),
                "especialidad": "Emergencias",
                "numero_licencia": "ENF-001002",
                "turno": "Tarde",
                "telefono": "+57 300 777 7777",
                "email": "luis.torres@hospital.com",
                "direccion": "Carrera 30 #45-20, Bogotá",
            },
            {
                "primer_nombre": "Patricia",
                "apellido": "Herrera",
                "fecha_nacimiento": date(1982, 12, 3),
                "especialidad": "Quirófanos",
                "numero_licencia": "ENF-001003",
                "turno": "Noche",
                "telefono": "+57 300 888 8888",
                "email": "patricia.herrera@hospital.com",
                "direccion": "Avenida 19 #80-15, Bogotá",
            },
            {
                "primer_nombre": "Miguel",
                "apellido": "Castro",
                "fecha_nacimiento": date(1990, 4, 18),
                "especialidad": "Pediatría",
                "numero_licencia": "ENF-001004",
                "turno": "Mañana",
                "telefono": "+57 300 999 9999",
                "email": "miguel.castro@hospital.com",
                "direccion": "Calle 127 #15-45, Bogotá",
            },
        ]

        enfermeras = []
        for enf_data in enfermeras_data:
            enfermera = enfermera_crud.crear_enfermera(
                primer_nombre=enf_data["primer_nombre"],
                apellido=enf_data["apellido"],
                fecha_nacimiento=enf_data["fecha_nacimiento"],
                numero_licencia=enf_data["numero_licencia"],
                turno=enf_data["turno"],
                telefono=enf_data["telefono"],
                direccion=enf_data["direccion"],
                id_usuario_creacion=admin_id,
                segundo_nombre=enf_data.get("segundo_nombre"),
                especialidad=enf_data.get("especialidad"),
                email=enf_data.get("email"),
            )
            enfermeras.append(enfermera)
        print(f"Enfermeras creadas: {len(enfermeras)}")

        # 5. Crear pacientes
        print("Creando pacientes...")
        pacientes_data = [
            {
                "primer_nombre": "María",
                "segundo_nombre": "Isabel",
                "apellido": "González",
                "fecha_nacimiento": date(1985, 6, 10),
                "telefono": "+57 300 100 1001",
                "email": "maria.gonzalez@email.com",
                "direccion": "Calle 85 #15-25, Bogotá",
            },
            {
                "primer_nombre": "Carlos",
                "apellido": "Mendoza",
                "fecha_nacimiento": date(1978, 3, 22),
                "telefono": "+57 300 100 1002",
                "email": "carlos.mendoza@email.com",
                "direccion": "Carrera 50 #25-40, Bogotá",
            },
            {
                "primer_nombre": "Ana",
                "segundo_nombre": "Patricia",
                "apellido": "Ruiz",
                "fecha_nacimiento": date(1992, 11, 5),
                "telefono": "+57 300 100 1003",
                "email": "ana.ruiz@email.com",
                "direccion": "Avenida 68 #30-15, Bogotá",
            },
            {
                "primer_nombre": "José",
                "segundo_nombre": "Antonio",
                "apellido": "Herrera",
                "fecha_nacimiento": date(1965, 8, 18),
                "telefono": "+57 300 100 1004",
                "email": "jose.herrera@email.com",
                "direccion": "Calle 100 #50-20, Bogotá",
            },
            {
                "primer_nombre": "Laura",
                "apellido": "Vargas",
                "fecha_nacimiento": date(1988, 1, 12),
                "telefono": "+57 300 100 1005",
                "email": "laura.vargas@email.com",
                "direccion": "Carrera 15 #80-30, Bogotá",
            },
            {
                "primer_nombre": "Roberto",
                "apellido": "Silva",
                "fecha_nacimiento": date(1975, 9, 28),
                "telefono": "+57 300 100 1006",
                "email": "roberto.silva@email.com",
                "direccion": "Calle 127 #25-10, Bogotá",
            },
            {
                "primer_nombre": "Carmen",
                "segundo_nombre": "Elena",
                "apellido": "Morales",
                "fecha_nacimiento": date(1990, 4, 15),
                "telefono": "+57 300 100 1007",
                "email": "carmen.morales@email.com",
                "direccion": "Avenida 19 #45-25, Bogotá",
            },
            {
                "primer_nombre": "Diego",
                "apellido": "Castro",
                "fecha_nacimiento": date(1983, 12, 8),
                "telefono": "+57 300 100 1008",
                "email": "diego.castro@email.com",
                "direccion": "Carrera 7 #100-15, Bogotá",
            },
        ]

        pacientes = []
        for pac_data in pacientes_data:
            paciente = paciente_crud.crear_paciente(
                primer_nombre=pac_data["primer_nombre"],
                apellido=pac_data["apellido"],
                fecha_nacimiento=pac_data["fecha_nacimiento"],
                telefono=pac_data["telefono"],
                direccion=pac_data["direccion"],
                id_usuario_creacion=admin_id,
                segundo_nombre=pac_data.get("segundo_nombre"),
                email=pac_data.get("email"),
            )
            pacientes.append(paciente)
        print(f"Pacientes creados: {len(pacientes)}")

        # 6. Crear citas
        print("Creando citas...")
        motivos = [
            "Consulta general",
            "Control de presión arterial",
            "Revisión de resultados de laboratorio",
            "Dolor de cabeza persistente",
            "Control prenatal",
            "Revisión post-operatoria",
            "Consulta por ansiedad",
            "Control de diabetes",
            "Dolor en el pecho",
            "Revisión de medicación",
        ]

        estados = ["Agendada", "Completada", "Cancelada"]
        citas = []

        for i in range(15):
            paciente = random.choice(pacientes)
            medico = random.choice(medicos)
            fecha = date.today() + timedelta(days=random.randint(-30, 30))
            hora = time(random.randint(8, 17), random.choice([0, 15, 30, 45]))

            cita = cita_crud.crear_cita(
                paciente_id=paciente.id,
                medico_id=medico.id,
                fecha=fecha,
                hora=hora,
                motivo=random.choice(motivos),
                estado=random.choice(estados),
                observaciones=f"Observaciones para cita {i+1}",
                id_usuario_creacion=admin_id,
            )
            citas.append(cita)
        print(f"Citas creadas: {len(citas)}")

        # 7. Crear hospitalizaciones
        print("Creando hospitalizaciones...")
        tipos_cuidado = ["Intensivo", "Intermedio", "Básico", "Observación"]
        tipos_habitacion = ["Individual", "Doble", "Suite"]
        estados_hosp = ["Activa", "Completada", "Cancelada"]

        hospitalizaciones = []
        for i in range(8):
            paciente = random.choice(pacientes)
            medico = random.choice(medicos)
            enfermera = random.choice(enfermeras) if random.random() > 0.3 else None

            fecha_inicio = date.today() - timedelta(days=random.randint(1, 15))
            fecha_fin = (
                fecha_inicio + timedelta(days=random.randint(1, 10))
                if random.random() > 0.4
                else None
            )

            hosp = hospitalizacion_crud.crear_hospitalizacion(
                paciente_id=paciente.id,
                medico_responsable_id=medico.id,
                tipo_cuidado=random.choice(tipos_cuidado),
                descripcion=f"Hospitalización por {random.choice(['cirugía', 'tratamiento médico', 'observación', 'recuperación'])}",
                numero_habitacion=f"{random.randint(100, 999)}",
                tipo_habitacion=random.choice(tipos_habitacion),
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=random.choice(estados_hosp),
                id_usuario_creacion=admin_id,
                enfermera_asignada_id=enfermera.id if enfermera else None,
            )
            hospitalizaciones.append(hosp)
        print(f"Hospitalizaciones creadas: {len(hospitalizaciones)}")

        # 8. Crear facturas
        print("Creando facturas...")
        metodos_pago = ["Efectivo", "Tarjeta de crédito", "Transferencia", "Cheque"]
        estados_factura = ["Pendiente", "Pagada", "Vencida"]

        facturas = []
        for i in range(10):
            paciente = random.choice(pacientes)
            fecha_emision = date.today() - timedelta(days=random.randint(1, 30))
            fecha_limite = fecha_emision + timedelta(days=30)
            total = Decimal(str(random.uniform(50000, 500000)))

            factura = factura_crud.crear_factura(
                paciente_id=paciente.id,
                numero_factura=f"FAC-{str(i+1).zfill(6)}",
                fecha_emision=fecha_emision,
                fecha_limite_pago=fecha_limite,
                total=total,
                estado=random.choice(estados_factura),
                metodo_pago=(
                    random.choice(metodos_pago) if random.random() > 0.5 else None
                ),
                id_usuario_creacion=admin_id,
            )
            facturas.append(factura)
        print(f"Facturas creadas: {len(facturas)}")

        # 9. Crear detalles de factura
        print("Creando detalles de factura...")
        servicios = [
            "Consulta médica general",
            "Consulta especializada",
            "Examen de laboratorio",
            "Radiografía",
            "Ecografía",
            "Cirugía menor",
            "Hospitalización por día",
            "Medicamentos",
            "Terapia física",
            "Procedimiento diagnóstico",
        ]

        detalles_creados = 0
        for factura in facturas:
            num_detalles = random.randint(1, 4)
            for j in range(num_detalles):
                servicio = random.choice(servicios)
                cantidad = random.randint(1, 3)
                precio_unitario = Decimal(str(random.uniform(10000, 100000)))
                subtotal = precio_unitario * cantidad

                # Asociar con cita o hospitalización si existe
                cita_relacionada = (
                    random.choice(citas) if citas and random.random() > 0.5 else None
                )
                hosp_relacionada = (
                    random.choice(hospitalizaciones)
                    if hospitalizaciones and random.random() > 0.5
                    else None
                )

                detalle = factura_detalle_crud.crear_factura_detalle(  # noqa: F841
                    factura_id=factura.id,
                    descripcion=servicio,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    subtotal=subtotal,
                    id_usuario_creacion=admin_id,
                    cita_id=cita_relacionada.id if cita_relacionada else None,
                    hospitalizacion_id=(
                        hosp_relacionada.id if hosp_relacionada else None
                    ),
                )
                detalles_creados += 1
        print(f"Detalles de factura creados: {detalles_creados}")

        # 10. Crear historiales médicos
        print("Creando historiales médicos...")
        historiales = []
        for paciente in pacientes:
            historial = historial_medico_crud.crear_historial_medico(
                paciente_id=paciente.id,
                numero_historial=f"HIST-{str(paciente.id)[:8].upper()}",
                fecha_apertura=date.today() - timedelta(days=random.randint(1, 365)),
                estado="Activo",
                id_usuario_creacion=admin_id,
            )
            historiales.append(historial)
        print(f"Historiales médicos creados: {len(historiales)}")

        # 11. Crear entradas de historial
        print("Creando entradas de historial...")
        diagnosticos = [
            "Hipertensión arterial",
            "Diabetes tipo 2",
            "Gripe común",
            "Migraña",
            "Ansiedad generalizada",
            "Artritis reumatoide",
            "Bronquitis aguda",
            "Gastritis",
            "Depresión",
            "Asma bronquial",
        ]

        tratamientos = [
            "Reposo y medicación",
            "Terapia física",
            "Control dietético",
            "Medicación oral",
            "Terapia psicológica",
            "Cirugía ambulatoria",
            "Hospitalización",
            "Seguimiento mensual",
            "Cambio de estilo de vida",
            "Tratamiento preventivo",
        ]

        entradas_creadas = 0
        for historial in historiales:
            num_entradas = random.randint(1, 5)
            for j in range(num_entradas):
                medico = random.choice(medicos)
                cita_relacionada = (
                    random.choice(citas) if citas and random.random() > 0.3 else None
                )

                entrada = historial_entrada_crud.crear_historial_entrada(  # noqa: F841
                    historial_id=historial.id,
                    medico_id=medico.id,
                    diagnostico=random.choice(diagnosticos),
                    tratamiento=random.choice(tratamientos),
                    notas=f"Notas médicas para entrada {j+1} del historial {historial.numero_historial}",
                    fecha_registro=date.today() - timedelta(days=random.randint(1, 90)),
                    firma_digital=f"Dr. {medico.primer_nombre} {medico.apellido}",
                    id_usuario_creacion=admin_id,
                    cita_id=cita_relacionada.id if cita_relacionada else None,
                )
                entradas_creadas += 1
        print(f"Entradas de historial creadas: {entradas_creadas}")

        print("\n=== BASE DE DATOS POBLADA EXITOSAMENTE ===")
        print(f"Usuarios: {len(usuarios)}")
        print(f"Médicos: {len(medicos)}")
        print(f"Enfermeras: {len(enfermeras)}")
        print(f"Pacientes: {len(pacientes)}")
        print(f"Citas: {len(citas)}")
        print(f"Hospitalizaciones: {len(hospitalizaciones)}")
        print(f"Facturas: {len(facturas)}")
        print(f"Detalles de factura: {detalles_creados}")
        print(f"Historiales médicos: {len(historiales)}")
        print(f"Entradas de historial: {entradas_creadas}")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    poblar_base_datos()
