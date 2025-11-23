Backend - Sistema Hospitalario

API REST desarrollada con FastAPI para gestión hospitalaria.

## Requisitos

- Python 3.8+
- PostgreSQL (Neon Cloud)

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
```

## Ejecución

```bash
python main.py
```

La API estará disponible en `http://localhost:8000`

Documentación: `http://localhost:8000/docs`

## Estructura

```
BACK/
├── apis/          Endpoints de la API
├── crud/          Operaciones de base de datos
├── entities/       Modelos SQLAlchemy
├── schemas.py     Esquemas Pydantic
├── database/       Configuración de BD
└── main.py         Aplicación principal
```

## Entidades y Relaciones

### Usuario
Entidad que representa un usuario del sistema con permisos de administración.
- **Relaciones**: No tiene relaciones directas con otras entidades
- **Campos clave**: nombre_usuario (único), email (único), es_admin
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### Paciente
Entidad que representa un paciente del hospital.
- **Relaciones**: 
  - Uno a muchos con Cita
  - Uno a muchos con Hospitalizacion
  - Uno a muchos con Factura
  - Uno a muchos con HistorialMedico
- **Campos clave**: email (único), fecha_nacimiento
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### Medico
Entidad que representa un médico del hospital.
- **Relaciones**:
  - Uno a muchos con Cita
  - Uno a muchos con Hospitalizacion
  - Uno a muchos con HistorialEntrada
- **Campos clave**: email (único), numero_licencia (único), especialidad
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### Enfermera
Entidad que representa una enfermera del hospital.
- **Relaciones**:
  - Uno a muchos con Hospitalizacion
- **Campos clave**: email (único), numero_licencia (único), turno
- **Estados de turno**: mañana, tarde, noche
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### Cita
Entidad que representa una cita médica.
- **Relaciones**:
  - Muchos a uno con Paciente
  - Muchos a uno con Medico
- **Campos clave**: fecha_cita, motivo, estado
- **Estados**: programada, completada, cancelada
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### Hospitalizacion
Entidad que representa una hospitalización de un paciente.
- **Relaciones**:
  - Muchos a uno con Paciente
  - Muchos a uno con Medico
  - Muchos a uno con Enfermera (opcional)
- **Campos clave**: fecha_ingreso, numero_habitacion, estado
- **Estados**: activa, completada, cancelada
- **Reglas de negocio**: 
  - Una habitación no puede estar ocupada por múltiples hospitalizaciones activas simultáneamente
  - La fecha_salida es opcional y se establece cuando la hospitalización se completa
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### HistorialMedico
Entidad que representa el historial médico de un paciente.
- **Relaciones**:
  - Muchos a uno con Paciente
  - Uno a muchos con HistorialEntrada
- **Campos clave**: numero_historial (único), estado
- **Estados**: abierto, cerrado, archivado
- **Reglas de negocio**: 
  - Un paciente solo puede tener un historial médico activo a la vez
  - El número de historial debe ser único
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### HistorialEntrada
Entidad que representa una entrada en el historial médico.
- **Relaciones**:
  - Muchos a uno con HistorialMedico
  - Muchos a uno con Medico
- **Campos clave**: fecha_consulta, diagnostico, tratamiento, observaciones
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### Factura
Entidad que representa una factura de servicios médicos.
- **Relaciones**:
  - Muchos a uno con Paciente
  - Uno a muchos con FacturaDetalle
- **Campos clave**: numero_factura (único), fecha_emision, fecha_vencimiento, estado
- **Estados**: pendiente, pagada, vencida, cancelada
- **Reglas de negocio**:
  - El número de factura debe ser único
  - Los montos (subtotal, impuestos, total) no pueden ser negativos
  - El total debe ser igual a subtotal + impuestos
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

### FacturaDetalle
Entidad que representa un detalle de línea en una factura.
- **Relaciones**:
  - Muchos a uno con Factura
- **Campos clave**: descripcion, cantidad, precio_unitario, subtotal
- **Reglas de negocio**:
  - La cantidad debe ser mayor a cero
  - Los precios no pueden ser negativos
  - El subtotal debe ser igual a cantidad * precio_unitario
- **Auditoría**: fecha_creacion, fecha_actualizacion, id_usuario_creacion, id_usuario_edicion

## Lógica de Negocio

### Validaciones Comunes

1. **Email**: Debe tener formato válido y ser único por entidad
2. **Teléfono**: Opcional, máximo 20 caracteres, formato flexible
3. **Campos de texto**: No pueden estar vacíos (solo espacios), tienen límites de longitud
4. **Soft Delete**: Todas las entidades usan soft delete (campo `activo`), no se eliminan físicamente
5. **Auditoría**: Todas las entidades registran quién y cuándo las creó/modificó

### Reglas de Negocio Específicas

#### Citas
- El paciente y médico deben existir antes de crear la cita
- El motivo es obligatorio y no puede exceder 255 caracteres
- Las citas pueden tener notas opcionales

#### Hospitalizaciones
- El paciente y médico deben existir
- La enfermera es opcional pero si se proporciona debe existir
- El número de habitación no puede estar ocupado por otra hospitalización activa
- El motivo es obligatorio y no puede exceder 255 caracteres

#### Historiales Médicos
- Un paciente solo puede tener un historial médico activo
- El número de historial debe ser único en el sistema
- El número de historial es obligatorio

#### Facturas
- El número de factura debe ser único
- Los montos no pueden ser negativos
- El total debe calcularse correctamente (subtotal + impuestos)
- Una factura puede tener múltiples detalles

#### FacturaDetalle
- La factura padre debe existir
- La descripción es obligatoria
- La cantidad debe ser mayor a cero
- Los precios no pueden ser negativos

## Ejemplos de Uso de la API

### Autenticación

```bash
# Login
POST /api/auth/login
{
  "nombre_usuario": "admin",
  "contraseña": "password123"
}

# Respuesta
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### Crear un Paciente

```bash
POST /api/pacientes
Authorization: Bearer {token}
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan.perez@email.com",
  "telefono": "+1234567890",
  "fecha_nacimiento": "1990-01-15",
  "direccion": "Calle Principal 123"
}

# Respuesta
{
  "id": "uuid-del-paciente",
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan.perez@email.com",
  "activo": true,
  "fecha_creacion": "2024-01-15T10:30:00Z",
  ...
}
```

### Crear una Cita

```bash
POST /api/citas
Authorization: Bearer {token}
{
  "fecha_cita": "2024-02-01T10:00:00Z",
  "motivo": "Consulta general",
  "paciente_id": "uuid-del-paciente",
  "medico_id": "uuid-del-medico",
  "notas": "Primera consulta"
}

# Respuesta
{
  "id": "uuid-de-la-cita",
  "fecha_cita": "2024-02-01T10:00:00Z",
  "estado": "programada",
  "activo": true,
  ...
}
```

### Listar Pacientes con Paginación

```bash
GET /api/pacientes?skip=0&limit=1000
Authorization: Bearer {token}

# Respuesta
[
  {
    "id": "uuid-1",
    "nombre": "Juan",
    "apellido": "Pérez",
    ...
  },
  {
    "id": "uuid-2",
    "nombre": "María",
    "apellido": "González",
    ...
  }
]
```

### Actualizar un Médico

```bash
PUT /api/medicos/{medico_id}
Authorization: Bearer {token}
{
  "especialidad": "Cardiología",
  "consultorio": "101",
  "id_usuario_edicion": "uuid-del-usuario"
}

# Respuesta
{
  "id": "uuid-del-medico",
  "nombre": "Dr. Carlos",
  "apellido": "Rodríguez",
  "especialidad": "Cardiología",
  "consultorio": "101",
  ...
}
```

### Eliminar (Soft Delete) una Cita

```bash
DELETE /api/citas/{cita_id}
Authorization: Bearer {token}

# Respuesta
{
  "mensaje": "Cita eliminada exitosamente",
  "success": true
}
```

### Crear una Hospitalización

```bash
POST /api/hospitalizaciones
Authorization: Bearer {token}
{
  "fecha_ingreso": "2024-01-20T08:00:00Z",
  "motivo": "Cirugía programada",
  "numero_habitacion": "201",
  "paciente_id": "uuid-del-paciente",
  "medico_id": "uuid-del-medico",
  "enfermera_id": "uuid-de-enfermera",
  "notas": "Paciente estable"
}

# Respuesta
{
  "id": "uuid-de-hospitalizacion",
  "estado": "activa",
  "numero_habitacion": "201",
  ...
}
```

### Crear una Factura con Detalles

```bash
# Primero crear la factura
POST /api/facturas
Authorization: Bearer {token}
{
  "numero_factura": "FAC-2024-001",
  "fecha_emision": "2024-01-15T00:00:00Z",
  "fecha_vencimiento": "2024-02-15T00:00:00Z",
  "subtotal": 500.00,
  "impuestos": 50.00,
  "total": 550.00,
  "paciente_id": "uuid-del-paciente"
}

# Luego crear los detalles
POST /api/factura-detalles
Authorization: Bearer {token}
{
  "descripcion": "Consulta médica",
  "cantidad": 1,
  "precio_unitario": 300.00,
  "subtotal": 300.00,
  "factura_id": "uuid-de-factura"
}

POST /api/factura-detalles
Authorization: Bearer {token}
{
  "descripcion": "Análisis de laboratorio",
  "cantidad": 2,
  "precio_unitario": 100.00,
  "subtotal": 200.00,
  "factura_id": "uuid-de-factura"
}
```

## Estados y Transiciones

### Estados de Cita
- **programada**: Cita creada y pendiente
- **completada**: Cita realizada exitosamente
- **cancelada**: Cita cancelada

### Estados de Hospitalización
- **activa**: Paciente actualmente hospitalizado
- **completada**: Paciente dado de alta
- **cancelada**: Hospitalización cancelada

### Estados de Factura
- **pendiente**: Factura emitida, pendiente de pago
- **pagada**: Factura pagada completamente
- **vencida**: Factura con fecha de vencimiento pasada
- **cancelada**: Factura cancelada

### Estados de Historial Médico
- **abierto**: Historial activo y en uso
- **cerrado**: Historial cerrado pero disponible
- **archivado**: Historial archivado

## Endpoints Disponibles

- `/api/auth/*` - Autenticación y autorización
- `/api/usuarios/*` - Gestión de usuarios
- `/api/pacientes/*` - Gestión de pacientes
- `/api/medicos/*` - Gestión de médicos
- `/api/enfermeras/*` - Gestión de enfermeras
- `/api/citas/*` - Gestión de citas
- `/api/hospitalizaciones/*` - Gestión de hospitalizaciones
- `/api/historiales-medicos/*` - Gestión de historiales médicos
- `/api/historial-entradas/*` - Gestión de entradas de historial
- `/api/facturas/*` - Gestión de facturas
- `/api/factura-detalles/*` - Gestión de detalles de factura

Todos los endpoints DELETE devuelven `HTTP 200 OK` con un objeto `RespuestaAPI`.

Todos los endpoints GET de listado soportan paginación con parámetros `skip` (default: 0) y `limit` (default: 1000).
