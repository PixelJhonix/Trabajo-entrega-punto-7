"""
Sistema de gestión hospitalaria
API REST con FastAPI
"""

import os
import socket
import uvicorn
from apis import (
    auth,
    cita,
    enfermera,
    factura,
    factura_detalle,
    historial_entrada,
    historial_medico,
    hospitalizacion,
    medico,
    paciente,
    usuario,
)
from database.config import create_tables
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Sistema de Gestión Hospitalaria",
    description="API REST para gestión de hospital con pacientes, médicos, enfermeras, citas, hospitalizaciones, facturas e historiales médicos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(usuario.router, prefix="/api")
app.include_router(paciente.router, prefix="/api")
app.include_router(medico.router, prefix="/api")
app.include_router(enfermera.router, prefix="/api")
app.include_router(cita.router, prefix="/api")
app.include_router(hospitalizacion.router, prefix="/api")
app.include_router(historial_medico.router, prefix="/api")
app.include_router(historial_entrada.router, prefix="/api")
app.include_router(factura.router, prefix="/api")
app.include_router(factura_detalle.router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador personalizado para errores de validación de Pydantic."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.on_event("startup")
async def startup_event():
    """Inicio de la aplicación"""
    print("Iniciando sistema...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo.")
    print("Documentación: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz"""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión Hospitalaria",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autenticacion": "/auth",
            "usuarios": "/usuarios",
            "pacientes": "/pacientes",
            "medicos": "/medicos",
            "enfermeras": "/enfermeras",
            "citas": "/citas",
            "hospitalizaciones": "/hospitalizaciones",
            "historiales_medicos": "/historiales-medicos",
            "historiales_entrada": "/historial-entradas",
            "facturas": "/facturas",
            "facturas_detalle": "/factura-detalles",
        },
    }


def is_port_available(host: str, port: int) -> bool:
    """Verifica si un puerto está disponible"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def main():
    """Obtener puerto de variable de entorno o usar 8000 por defecto"""
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    if not isinstance(port, int) or port < 1 or port > 65535:
        print(f"ERROR: Puerto inválido: {port}")
        print("El puerto debe ser un número entre 1 y 65535")
        return

    if not is_port_available(host, port):
        print(f"ERROR: El puerto {port} ya está en uso")
        print(
            f"Por favor, detén el proceso que está usando el puerto {port} o usa otro puerto"
        )
        print(f"Para usar otro puerto, establece la variable de entorno PORT:")
        print(f"  Windows: $env:PORT=8001")
        print(f"  Linux/Mac: export PORT=8001")
        return

    print(f"Iniciando servidor en {host}:{port}...")
    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            reload=False,
            log_level="info",
        )
    except OSError as e:
        if e.errno == 10048:
            print(f"ERROR: No se puede iniciar el servidor en el puerto {port}")
            print(f"El puerto {port} está siendo usado por otro proceso")
            print(f"Para solucionarlo:")
            print(f"  1. Detén el proceso que está usando el puerto {port}")
            print(
                f"  2. O usa otro puerto estableciendo PORT=8001 (o el que prefieras)"
            )
        else:
            print(f"ERROR al iniciar el servidor: {e}")


if __name__ == "__main__":
    main()
