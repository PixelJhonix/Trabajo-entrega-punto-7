# Sistema de Gestion Hospitalaria

Sistema completo de gestion hospitalaria desarrollado con Python, SQLAlchemy ORM y PostgreSQL (Neon). Implementa una arquitectura en capas siguiendo principios SOLID y patrones de diseño establecidos.

## Arquitectura del Sistema

### Capas Implementadas

#### 1. Capa de Entidades (ORM) - `entities/`
- **Responsabilidad**: Definir modelos de datos y relaciones
- **Tecnologia**: SQLAlchemy ORM
- **Entidades**: Usuario, Paciente, Medico, Enfermera, Cita, Hospitalizacion, Factura, HistorialMedico

#### 2. Capa de Acceso a Datos (CRUD) - `crud/`
- **Responsabilidad**: Lógica de negocio y operaciones de base de datos
- **Patron**: Repository Pattern
- **Funcionalidades**: Create, Read, Update, Delete para todas las entidades

#### 3. Capa de Presentacion (UI) - `menu/`
- **Responsabilidad**: Interfaz de usuario y navegacion
- **Patron**: MVC (Model-View-Controller)
- **Funcionalidades**: Menus interactivos, formularios, validaciones de entrada

#### 4. Capa de Autenticacion - `auth/`
- **Responsabilidad**: Seguridad y autenticacion
- **Funcionalidades**: Hash de contraseñas, gestion de sesiones, control de acceso

#### 5. Capa de Configuracion - `database/`
- **Responsabilidad**: Configuracion de base de datos
- **Funcionalidades**: Conexion a PostgreSQL, configuracion de sesiones

## Principios de Diseño Aplicados

### Single Responsibility Principle (SRP)
- Cada clase tiene una sola responsabilidad
- Separacion clara entre logica de negocio y presentacion
- Facil mantenimiento y testing

### Open/Closed Principle (OCP)
- Fácil extension sin modificacion de codigo existente
- Nuevas entidades se pueden agregar sin afectar las existentes

### Dependency Inversion Principle (DIP)
- Las capas superiores dependen de abstracciones
- Bajo acoplamiento entre componentes

## Estructura del Proyecto

```
Trabajo-entrega-punto-7/
├── entities/           # Capa ORM - Modelos de datos
│   ├── usuario.py
│   ├── paciente.py
│   ├── medico.py
│   └── ...
├── crud/              # Capa CRUD - Logica de negocio
│   ├── usuario_crud.py
│   ├── paciente_crud.py
│   ├── medico_crud.py
│   └── ...
├── menu/              # Capa UI - Interfaz de usuario
│   ├── main_menu.py
│   ├── paciente_menu.py
│   ├── medico_menu.py
│   └── ...
├── auth/              # Capa de Autenticacion
│   ├── security.py
│   └── auth_service.py
├── database/          # Capa de Configuracion
│   └── config.py
├── migrations/        # Migraciones de base de datos
├── main.py           # Punto de entrada
└── requirements.txt  # Dependencias
```

## Entidades del Sistema

### 1. Usuario
- **Proposito**: Autenticacion y auditoria
- **Campos**: nombre, nombre_usuario, email, contraseña_hash, es_admin, activo
- **Relaciones**: Referenciado por todas las entidades para auditoria

### 2. Paciente
- **Proposito**: Gestion de pacientes
- **Campos**: primer_nombre, apellido, fecha_nacimiento, telefono, email, direccion
- **Relaciones**: Uno a muchos con Cita, Hospitalizacion, Factura, HistorialMedico

### 3. Medico
- **Proposito**: Gestion de medicos
- **Campos**: primer_nombre, apellido, especialidad, numero_licencia, consultorio
- **Relaciones**: Uno a muchos con Cita, Hospitalizacion, HistorialEntrada

### 4. Enfermera
- **Proposito**: Gestion de enfermeras
- **Campos**: primer_nombre, apellido, especialidad, numero_licencia, turno
- **Relaciones**: Uno a muchos con Hospitalizacion

### 5. Cita
- **Proposito**: Agendamiento de consultas
- **Campos**: fecha, hora, motivo, estado, observaciones
- **Relaciones**: Muchos a uno con Paciente y Medico

### 6. Hospitalizacion
- **Proposito**: Gestion de internaciones
- **Campos**: tipo_cuidado, descripcion, numero_habitacion, fecha_inicio, fecha_fin
- **Relaciones**: Muchos a uno con Paciente, Medico, Enfermera

### 7. Factura
- **Proposito**: Sistema de facturacion
- **Campos**: numero_factura, fecha_emision, total, estado, metodo_pago
- **Relaciones**: Muchos a uno con Paciente, uno a muchos con FacturaDetalle

### 8. FacturaDetalle
- **Proposito**: Detalles de servicios facturados
- **Campos**: descripcion, cantidad, precio_unitario, subtotal
- **Relaciones**: Muchos a uno con Factura, Cita, Hospitalizacion

### 9. HistorialMedico
- **Proposito**: Historial clinico de pacientes
- **Campos**: numero_historial, fecha_apertura, estado
- **Relaciones**: Uno a uno con Paciente, uno a muchos con HistorialEntrada

### 10. HistorialEntrada
- **Proposito**: Entradas del historial medico
- **Campos**: diagnostico, tratamiento, notas, fecha_registro, firma_digital
- **Relaciones**: Muchos a uno con HistorialMedico, Medico, Cita

## Sistema de Auditoria

### Campos de Auditoria Implementados
- **id_usuario_creacion**: UUID del usuario que creo el registro
- **id_usuario_edicion**: UUID del usuario que edito el registro
- **created_at**: Fecha y hora de creacion (automatica)
- **updated_at**: Fecha y hora de ultima actualizacion (automatica)

### Beneficios de la Auditoria
- **Trazabilidad**: Saber quien hizo que y cuando
- **Cumplimiento**: Regulaciones medicas y legales
- **Seguridad**: Control de acceso y modificaciones
- **Auditoria**: Revision de cambios y modificaciones

## Instalacion y Configuracion

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
Crear archivo `.env` basado en `.env.example`:
```env
DATABASE_URL="postgresql://usuario:password@host:port/database?sslmode=require"
```

### 3. Ejecutar Migraciones
```bash
alembic upgrade head
```

### 4. Ejecutar el Sistema
```bash
python main.py
```

### Credenciales por Defecto
- **Usuario**: `admin`
- **Email**: `admin@system.com`
- **Contraseña**: `admin123`

## Funcionalidades Implementadas

### Sistema de Autenticacion
- Login seguro con hash de contraseñas
- Gestion de sesiones
- Control de acceso por roles
- Usuario administrador por defecto

### Gestion de Pacientes
- Registrar nuevo paciente
- Buscar paciente (ID, email, nombre)
- Listar todos los pacientes
- Actualizar informacion
- Eliminar paciente

### Gestion de Medicos
- Registrar nuevo medico
- Buscar medico (ID, email, nombre, especialidad)
- Listar todos los medicos
- Actualizar informacion
- Eliminar medico

### Gestion de Enfermeras
- Registrar nueva enfermera
- Buscar enfermera (ID, email, nombre, turno)
- Listar todas las enfermeras
- Actualizar informacion
- Eliminar enfermera

### Gestion de Citas
- Agendar nueva cita
- Buscar cita por ID
- Listar todas las citas
- Actualizar cita
- Cancelar cita
- Completar cita

### Gestion de Hospitalizaciones
- Registrar nueva hospitalizacion
- Buscar hospitalizacion
- Listar hospitalizaciones
- Actualizar hospitalizacion
- Completar hospitalizacion
- Cancelar hospitalizacion

### Gestion de Facturas
- Crear nueva factura
- Buscar factura (ID, numero)
- Listar todas las facturas
- Actualizar factura
- Marcar como pagada
- Cancelar factura

### Gestion de Historiales Medicos
- Crear historial medico
- Buscar historial
- Listar historiales
- Actualizar historial
- Eliminar historial
- Agregar entradas al historial

### Gestion de Usuarios (Solo Administradores)
- Crear nuevo usuario
- Buscar usuario
- Listar usuarios
- Actualizar usuario
- Eliminar usuario
- Cambiar estado de usuario

## Cumplimiento de Requerimientos del Examen

### Base de datos y entidades (20%)
- **10 entidades** implementadas con UUID
- **Relaciones** bien definidas entre entidades
- **Migraciones** configuradas con Alembic
- **PostgreSQL** como base de datos principal

### Columnas de autoria (15%)
- **id_usuario_creacion** en todas las tablas
- **id_usuario_edicion** en todas las tablas
- **fecha_creacion** (created_at) automatica
- **fecha_actualizacion** (updated_at) automatica

### Estilo y formato del codigo (10%)
- **Black Formatter** aplicado a todo el codigo
- **Sin comentarios #** - solo docstrings
- **Codigo limpio** y bien estructurado
- **Sin emojis** - interfaz profesional

### ORM con SQLAlchemy (20%)
- **SQLAlchemy 2.0** implementado completamente
- **Modelos ORM** para todas las entidades
- **Relaciones** bidireccionales configuradas
- **Validaciones** a nivel de base de datos

### Interfaz de interaccion (20%)
- **Menu interactivo** completo y funcional
- **Sistema de login** con autenticacion
- **Navegacion** intuitiva entre modulos
- **Validaciones** en tiempo real

### Logica de negocio (15%)
- **CRUD completo** para todas las entidades
- **Validaciones** de negocio implementadas
- **Reglas** especificas del dominio hospitalario
- **Operaciones** complejas (citas, hospitalizaciones, facturas)

### Documentacion (Obligatorio)
- **README.md** completo y detallado
- **Estructura** del proyecto documentada
- **Instrucciones** de ejecucion claras
- **Logica de negocio** explicada

## Instrucciones de Uso

1. **Ejecutar el sistema**: `python main.py`
2. **Login inicial**: Usuario `admin`, Contraseña `admin123`
3. **Navegar**: Usar los menus para acceder a cada modulo
4. **Operaciones**: Seguir las instrucciones en pantalla
5. **Salir**: Seleccionar opcion 0 en cualquier menu

## Tecnologias Utilizadas

- **Python 3.x**: Lenguaje principal
- **SQLAlchemy 2.0**: ORM para base de datos
- **PostgreSQL**: Base de datos relacional
- **Neon**: Servicio de base de datos en la nube
- **Alembic**: Migraciones de base de datos
- **Pydantic**: Validacion de datos
- **Black**: Formateo de codigo
- **python-dotenv**: Gestion de variables de entorno

## Patrones de Diseño Implementados

- **Repository Pattern**: En la capa CRUD
- **MVC (Model-View-Controller)**: Separacion de responsabilidades
- **Dependency Injection**: Inyeccion de dependencias
- **Factory Pattern**: Creacion de objetos
- **Observer Pattern**: Notificaciones y eventos

---

**Desarrollado para el examen de Programacion de Software - Arquitectura en Capas**