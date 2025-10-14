"""
Sistema de gestión hospitalaria con ORM SQLAlchemy y Neon PostgreSQL
API REST con FastAPI - Sin interfaz de consola
"""

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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(paciente.router)
app.include_router(medico.router)
app.include_router(enfermera.router)
app.include_router(cita.router)
app.include_router(hospitalizacion.router)
app.include_router(historial_medico.router)
app.include_router(historial_entrada.router)
app.include_router(factura.router)
app.include_router(factura_detalle.router)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación."""
    print("Iniciando Sistema de Gestión Hospitalaria...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz con información de la API."""
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
            "historiales_entrada": "/historiales-entrada",
            "facturas": "/facturas",
            "facturas_detalle": "/facturas-detalle",
        },
    }


def main():
    """Función principal para ejecutar el servidor."""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
