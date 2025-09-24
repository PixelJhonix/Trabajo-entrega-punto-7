# Sistema de Gestión Hospitalaria - Hospital Los Enanos

## Descripción

Sistema de gestión hospitalaria desarrollado en Python que implementa un sistema de registro y gestión de pacientes, profesionales (médicos y enfermeras), citas, facturas e historiales médicos. Este proyecto utiliza conceptos avanzados de Programación Orientada a Objetos (POO) como herencia, encapsulación y polimorfismo, integrados con una base de datos PostgreSQL en Neon mediante SQLAlchemy y validación de datos con Pydantic.

## Características Principales

- **Registro de Personas**: Gestión unificada de pacientes, médicos y enfermeras.
- **Gestión de Citas**: Agendamiento, visualización y cancelación de citas.
- **Facturación**: Generación y visualización de facturas para pacientes.
- **Historial Médico**: Registro y visualización de historiales médicos.
- **Herencia de Clases**: Estructura jerárquica con modelos SQLAlchemy.
- **Encapsulación**: Uso de relaciones entre entidades para mantener integridad de datos.
- **Polimorfismo**: Representación personalizada de entidades en salidas (e.g., `__repr__`).
- **Interfaz de Consola**: Menú interactivo para todas las funcionalidades.
- **Validación de Datos**: Uso de Pydantic para asegurar datos correctos.

## Instalación

### Prerrequisitos

- **Python 3.8+** instalado en tu sistema.
- **Git** para clonar el repositorio.
- **Editor de código** (VS Code, PyCharm, Cursor, etc.).

### Extensiones Recomendadas para VS Code/Cursor

- **Python** (Microsoft)
- **Pylance** (Microsoft)
- **Python Indent** (Kevin Rose)
- **Python Docstring Generator** (Nils Werner)
- **GitLens** (Eric Amodio)

## Clonar el Repositorio

```bash
# Clonar desde GitHub
git clone https://github.com/PixelJhonix/Trabajo-entrega-punto-7.git

# Navegar al directorio del proyecto
cd Trabajo-entrega-punto-7
```

## Configuración

### 1. Crear entorno virtual (Recomendado)

```bash
# Crear entorno virtual
py -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install sqlalchemy psycopg2-binary pydantic python-dotenv
```
tambien esta el archivo (requirements.txt) y los ejecutas en la consola :)

### 3. Configurar la base de datos

- Crea un proyecto en Neon (https://neon.tech).

- Obtén la conexión string (e.g., `postgresql://user:password@host/dbname`).

- Crea un archivo `.env` en el directorio raíz con:

  ```
  DATABASE_URL=postgresql://[user]:[password]@[host]/[dbname]
  ```

## Ejecutar el Proyecto

```bash
# Ejecutar el sistema hospitalario
py main.py
```

## Estructura del Proyecto

```
hospital-los-enanos/
├── main.py                 # Archivo principal con menú y lógica
├── database/
│   ├── __init__.py
│   ├── config.py
├── entities/
│   ├── __init__.py         # Importaciones de entidades
│   ├── base.py             # Base SQLAlchemy
│   ├── usuario.py          # Modelo de Usuario
│   ├── profesional.py      # Modelo de Profesional
│   ├── citas.py            # Modelo de Citas
│   ├── factura.py          # Modelo de Factura
│   ├── historial_medico.py # Modelo de Historial Médico
├── migrations/
│   ├── versions/
│   ├── env.py 
├── .env                    # Configuración de la base de datos
├── alembic.ini
├── requirements.txt
├── test_connection.txt
└── README.md               # Este archivo
```

## Arquitectura del Sistema

### Entidades Principales

#### Usuario

- **Atributos**: `id` (UUID), `nombre`, `edad`, `diagnostico`, `necesita`.
- **Relaciones**: `historial`, `citas`, `facturas`.

#### Profesional

- **Atributos**: `id` (UUID), `nombre`, `categoria_profesional`.
- **Relaciones**: `citas`.

#### Citas

- **Atributos**: `id` (UUID), `usuario_id`, `profesional_id`, `fecha` (DateTime).
- **Relaciones**: `usuario`, `profesional`.

#### Factura

- **Atributos**: `id` (UUID), `usuario_id`, `descripcion`, `monto`.
- **Relaciones**: `usuario`.

#### HistorialMedico

- **Atributos**: `id` (UUID), `paciente_id`, `registros` (JSON).
- **Relaciones**: `paciente`.

## Uso del Sistema

### Menú Principal

1. **Registrarse**: Accede al submenú de registro.
   - Registrar Usuario
   - Registrar Profesional
   - Editar Usuario
   - Editar Profesional
   - Eliminar Usuario
   - Eliminar Profesional
   - Mostrar Registros
   - Volver
2. **Citas**: Accede al submenú de citas.
   - Agendar Cita
   - Ver Citas por Paciente
   - Ver Citas por Médico
   - Ver Citas por Fecha
   - Cancelar Cita
   - Volver
3. **Facturas**: Accede al submenú de facturas.
   - Generar Factura
   - Ver Facturas
   - Volver
4. **Ver Historial Médico**: Accede al submenú de historial.
   - Ver Historial por Paciente
   - Volver
5. **Salir**

### Ejemplo de Uso

```python
# Registro de usuario:
# Nombre del usuario: Juan Pérez
# Edad: 25
# Diagnóstico: Gripe
# ¿Necesita cita con doctor o servicios de enfermera? (doctor/enfermera): doctor

# Agendar cita:
# Nombre del usuario: Juan Pérez
# Nombre del profesional: Dr. Gómez
# Fecha (YYYY-MM-DD): 2025-09-24
```

## Conceptos POO Implementados

### 1. Herencia

- Modelos SQLAlchemy heredan de `Base` para compartir estructura de base de datos.

### 2. Encapsulación

- Uso de relaciones SQLAlchemy para mantener integridad de datos entre entidades.

### 3. Polimorfismo

- Método `__repr__` personalizado para cada entidad.

### 4. Métodos de Clase

- Funciones como `ver_citas_paciente` en `Citas` para operaciones específicas.

## Desarrollo

### Flujo de trabajo Git

```bash
# 1. Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios y commits
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 3. Subir cambios
git push origin feature/nueva-funcionalidad

# 4. Crear Pull Request en GitHub
```

### Estándares de código

- **PEP 8** para estilo de código Python.
- **Mensajes de commit** descriptivos.
- **Documentación** en funciones y clases.

## Solución de Problemas

### Error común: "Python no se reconoce"

```bash
# Verificar instalación de Python
py --version

# Si no funciona, probar:
python --version
python3 --version
```

### Error: "No se encuentra el módulo sqlalchemy"

```bash
# Instalar dependencias faltantes
pip install sqlalchemy psycopg2-binary pydantic python-dotenv
```

### Error de conexión a la base de datos

```bash
# Verifica el archivo .env
# Asegúrate de que DATABASE_URL sea correcto
```

## Próximas Funcionalidades

- [ ] Interfaz gráfica (GUI).

- [ ] Notificaciones de citas.

- [ ] Reportes de facturación.

- [ ] Gestión de inventario médico.

## Contribuir

1. **Fork** el proyecto.
2. **Clone** tu fork.
3. **Crea** una rama para tu feature.
4. **Commit** tus cambios.
5. **Push** a tu rama.
6. **Crea** un Pull Request.

## Licencia

Este proyecto está bajo la Licencia ITM - ver el archivo LICENSE.md para detalles.  (EJEMPLO DE LICENCIA)

## Autores

- **@Miguel1820** 
- **@PixelJhonix** 

## Agradecimientos

- Profe Alejandro Salgar - Guia del Proyecto

## Contactos

- **Email's**: cortazar1820@gmail.com, ...
- **GitHub's**: @Miguel1820, @PixelJhonix

---