# Sistema de Gestión Hospitalaria - API FastAPI

## Descripción

Sistema de gestión hospitalaria desarrollado con FastAPI, SQLAlchemy y PostgreSQL. Proporciona una API REST completa para la gestión de usuarios, pacientes, médicos, enfermeras, citas, hospitalizaciones, facturas e historiales médicos.

## Características Principales

- **API REST completa** con FastAPI
- **Base de datos PostgreSQL** con SQLAlchemy ORM
- **Autenticación JWT** para seguridad
- **Documentación automática** con Swagger UI
- **Validación de datos** con Pydantic
- **Manejo de errores** estructurado
- **Códigos de estado HTTP** correctos
- **Soft delete** para preservar datos
- **Relaciones entre entidades** bien definidas

## Instalación

### Prerrequisitos

- Python 3.11+
- PostgreSQL (o usar Neon como servicio en la nube)
- Git

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Trabajo-entrega-punto-7
```

### 2. Crear entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/nombre_db
```

### 5. Ejecutar migraciones (opcional)

```bash
alembic upgrade head
```

## Ejecutar el Proyecto

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Estructura del Proyecto

```
Trabajo-entrega-punto-7/
├── apis/                    # Endpoints de la API
│   ├── auth.py             # Autenticación
│   ├── usuario.py          # Gestión de usuarios
│   ├── paciente.py         # Gestión de pacientes
│   ├── medico.py           # Gestión de médicos
│   ├── enfermera.py        # Gestión de enfermeras
│   ├── cita.py             # Gestión de citas
│   ├── hospitalizacion.py  # Gestión de hospitalizaciones
│   ├── factura.py          # Gestión de facturas
│   ├── factura_detalle.py  # Detalles de facturas
│   ├── historial_medico.py # Historiales médicos
│   └── historial_entrada.py # Entradas del historial
├── crud/                   # Operaciones de base de datos
├── entities/               # Modelos SQLAlchemy
├── schemas/                # Modelos Pydantic
├── database/               # Configuración de BD
├── auth/                   # Sistema de autenticación
├── utils/                  # Utilidades
├── main.py                 # Aplicación principal
└── requirements.txt        # Dependencias
```

## Entidades del Sistema

### Usuario
- Gestión de usuarios del sistema
- Autenticación y autorización
- Roles de administrador

### Paciente
- Información personal y médica
- Historial médico asociado

### Médico
- Especialidades médicas
- Número de licencia
- Citas y hospitalizaciones

### Enfermera
- Turnos de trabajo
- Número de licencia
- Asignación a hospitalizaciones

### Cita
- Programación de consultas
- Estados: programada, completada, cancelada
- Relación con paciente y médico

### Hospitalización
- Ingreso y egreso de pacientes
- Habitaciones asignadas
- Estados: activa, completada, cancelada

### Factura
- Facturación de servicios
- Estados: pendiente, pagada, vencida, cancelada
- Detalles de servicios

### Historial Médico
- Registro médico del paciente
- Entradas de consultas
- Estados: abierto, cerrado, archivado

## Endpoints Principales

### Autenticación
- `POST /auth/login` - Iniciar sesión
- `POST /auth/crear-admin` - Crear administrador
- `GET /auth/estado` - Estado del sistema

### Usuarios
- `GET /usuarios/` - Listar usuarios
- `POST /usuarios/` - Crear usuario
- `GET /usuarios/{id}` - Obtener usuario
- `PUT /usuarios/{id}` - Actualizar usuario
- `DELETE /usuarios/{id}` - Eliminar usuario

### Pacientes
- `GET /pacientes/` - Listar pacientes
- `POST /pacientes/` - Crear paciente
- `GET /pacientes/{id}` - Obtener paciente
- `PUT /pacientes/{id}` - Actualizar paciente
- `DELETE /pacientes/{id}` - Eliminar paciente

### Y más endpoints para cada entidad...

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **PostgreSQL**: Base de datos relacional
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **Alembic**: Migraciones de base de datos
- **JWT**: Autenticación basada en tokens

## Desarrollo

### Estándares de código

- **Docstrings** para documentación
- **Type hints** para tipado
- **Black** para formateo de código
- **Pydantic** para validación
- **HTTP status codes** correctos

### Flujo de trabajo

1. Crear rama para nueva funcionalidad
2. Implementar cambios
3. Probar endpoints
4. Hacer commit
5. Crear Pull Request

## Contribuir

1. Fork el proyecto
2. Crear rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autores

- [Tu nombre] - Desarrollo inicial

## Contacto

Para preguntas o sugerencias, contacta a [tu-email@ejemplo.com]