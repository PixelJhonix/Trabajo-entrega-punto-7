# Sistema Hospitalario - Hospital Los Enanos

Sistema de gestión hospitalaria desarrollado en Python con programación orientada a objetos y validaciones robustas usando Pydantic.

## Descripción

Sistema completo para la gestión de un centro médico que permite administrar:
- **Pacientes**: Registro y gestión de información personal
- **Médicos**: Gestión con especialidades y funcionalidades médicas
- **Enfermeras**: Administración con turnos de trabajo
- **Citas**: Agendamiento y gestión de citas médicas
- **Diagnósticos**: Registro de diagnósticos médicos
- **Facturas**: Emisión de facturas por servicios

## Características Principales

### Gestión de Personas
- Registro, edición y eliminación de pacientes, médicos y enfermeras
- Validación completa de datos usando Pydantic
- Interfaz de usuario intuitiva con menús interactivos

### Gestión de Citas
- Agendamiento de citas entre médicos y pacientes
- Verificación automática de disponibilidad de horarios
- Validación de conflictos de horario
- Estados de cita (Agendada, Cancelada, Completada)

### Registro de Diagnósticos
- Los médicos pueden registrar diagnósticos completos
- Incluye síntomas, diagnóstico, tratamiento y observaciones
- Historial completo por paciente y médico

### Emisión de Facturas
- Facturas por consultas médicas y servicios de enfermería
- Números de factura únicos generados automáticamente
- Validaciones de montos y fechas

## Requisitos del Sistema

- **Python**: 3.8 o superior
- **Dependencias**: pydantic

## Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd sistema-hospitalario
```

2. **Instalar dependencias**
```bash
pip install pydantic
```

3. **Ejecutar el sistema**
```bash
python main.py
```

## Estructura del Proyecto

```
sistema-hospitalario/
├── main.py                 # Sistema principal con menús interactivos
├── persona.py              # Clase base abstracta para todas las personas
├── paciente.py             # Clase para gestión de pacientes
├── medico.py               # Clase para gestión de médicos
├── enfermera.py            # Clase para gestión de enfermeras
├── cita.py                 # Clase para gestión de citas médicas
├── schemas.py              # Esquemas de validación con Pydantic
└── README.md               # Documentación del proyecto
```

## Arquitectura del Software

### Diagrama de Clases

```
Persona (Abstracta)
├── Paciente
│   ├── _citas: List[Cita]
│   ├── _diagnosticos: List[Diagnostico]
│   └── _facturas: List[Factura]
├── Medico
│   ├── _especialidad: str
│   ├── _citas: List[Cita]
│   ├── _diagnosticos: List[Diagnostico]
│   └── _facturas: List[Factura]
└── Enfermera
    ├── _turno: str
    └── _facturas: List[Factura]

Cita
├── paciente: Paciente
├── medico: Medico
├── fecha: str
├── hora: str
└── motivo: str

Diagnostico
├── paciente: Paciente
├── medico: Medico
├── sintomas: str
├── diagnostico: str
└── tratamiento: str

Factura
├── paciente: Paciente
├── profesional: Union[Medico, Enfermera]
├── concepto: str
├── monto: float
└── tipo_servicio: TipoServicio
```

## Uso del Sistema

### Menú Principal
```
========================================
         MENÚ PRINCIPAL
========================================
1. Registro
2. Citas
3. Facturas
4. Diagnóstico
0. Salir
========================================
```

### Funcionalidades Disponibles

#### 1. Registro
- Registrar Paciente, Médico o Enfermera
- Editar información de personas registradas
- Eliminar registros
- Mostrar todos los registros

#### 2. Citas
- Agendar citas entre médicos y pacientes
- Ver citas por paciente o médico
- Cancelar citas
- Consultar citas por fecha

#### 3. Facturas
- Emitir facturas por consultas médicas
- Emitir facturas por servicios de enfermería
- Ver facturas por paciente
- Generar reportes de facturación

#### 4. Diagnóstico
- Registrar diagnósticos médicos
- Ver historial de diagnósticos
- Buscar diagnósticos por paciente o médico

## Validaciones Implementadas

### Datos Personales
- **Nombres**: Solo letras, espacios, puntos, guiones y apóstrofes
- **Fechas**: Formato dd/mm/yyyy con validación de fechas futuras
- **Teléfonos**: Formato válido con regex (7-15 dígitos)
- **Direcciones**: Mínimos y máximos para todos los campos

### Datos Médicos
- **Síntomas**: Mínimo 10, máximo 500 caracteres
- **Diagnóstico**: Mínimo 5, máximo 200 caracteres
- **Tratamiento**: Mínimo 10, máximo 500 caracteres
- **Montos**: Positivos, máximo 2 decimales, límite superior

### Horarios y Citas
- **Horas**: Formato HH:MM, horario laboral 8:00-17:00
- **Fechas de cita**: Deben ser futuras
- **Conflictos**: Verificación automática de disponibilidad

## Ejemplos de Uso

### Registrar un Paciente
```
--- REGISTRAR NUEVO PACIENTE ---
Nombre: María José García
Fecha de nacimiento (dd/mm/yyyy): 15/03/1990
Teléfono: 555-1234
Dirección: Calle Principal 123
```

### Registrar un Médico
```
--- REGISTRAR NUEVO MÉDICO ---
Nombre: Dr. Juan Carlos López
Fecha de nacimiento (dd/mm/yyyy): 20/07/1975
Teléfono: 555-5678
Dirección: Av. Médica 456
Especialidad: Cardiología
```

### Agendar una Cita
```
--- AGENDAR CITA DESDE SISTEMA ---
PACIENTES DISPONIBLES:
1. María José García

MÉDICOS DISPONIBLES:
1. Dr. Juan Carlos López - Cardiología

Fecha (dd/mm/yyyy): 20/12/2024
Hora (HH:MM): 14:30
Motivo de la consulta: Consulta de control cardiológico
```

## Características Técnicas

### Programación Orientada a Objetos
- **Herencia**: Todas las personas heredan de la clase base `Persona`
- **Encapsulación**: Atributos privados con métodos públicos
- **Polimorfismo**: Métodos comunes implementados específicamente
- **Composición**: Relaciones entre objetos (citas, diagnósticos, facturas)

### Validaciones Robustas
- **Pydantic**: Para modelos de datos y validación de esquemas
- **Expresiones regulares**: Para validación de formatos
- **Validaciones de negocio**: Horarios, fechas, montos
- **Mensajes de error claros**: En español con ejemplos

### Sin Try-Except
- **Validaciones simples**: Usando `if/else` y validaciones directas
- **Manejo de errores**: Con retorno de tuplas `(bool, str)`
- **Código limpio**: Sin bloques try-except innecesarios

## Información del Proyecto

**Desarrollado para**: [NOMBRE DEL CURSO/ASIGNATURA]
**Estudiante**: [NOMBRE DEL ESTUDIANTE]
**Fecha de entrega**: [FECHA]
**Versión de Python**: [VERSIÓN]

## Comandos de Verificación

```bash
# Verificar que todo funciona correctamente
python -c "from schemas import PacienteIn; print('Esquemas cargados correctamente')"
python -c "from paciente import Paciente; print('Clases cargadas correctamente')"
python -c "from pydantic import ValidationError; print('Pydantic disponible')"
```

---

**Sistema Hospitalario - Hospital Los Enanos**
*Desarrollado con Python y Pydantic*
