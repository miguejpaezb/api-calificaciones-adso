from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .db import get_all_rows, get_actividad, update_estado, update_calificacion, buscar_actividades
from . import services

app = FastAPI(
    title="API Calificaciones",
    description="Cálculos sobre las calificaciones del curso ANALISIS Y DESARROLLO DE SOFTWARE",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CalificarRequest(BaseModel):
    calificacion: Literal["A", "D", "-"]
    retroalimentacion: str | None = None


def rows():
    return get_all_rows()


def require_actividad(activity_id):
    actividad = get_actividad(activity_id)
    if not actividad:
        raise HTTPException(status_code=404, detail=f"Actividad con id {activity_id} no encontrada")
    return actividad


@app.post("/api/actividades/{activity_id}/subir")
def marcar_subida(activity_id: int):
    require_actividad(activity_id)
    update_estado(activity_id, "Subido")
    return {"id": activity_id, "estado": "Subido"}


@app.post("/api/actividades/{activity_id}/calificar")
def marcar_calificada(activity_id: int, body: CalificarRequest):
    require_actividad(activity_id)
    update_calificacion(activity_id, body.calificacion, body.retroalimentacion)
    return {"id": activity_id, "estado": "Calificado", "calificacion": body.calificacion}


@app.post("/api/actividades/{activity_id}/eliminar")
def marcar_eliminada(activity_id: int):
    require_actividad(activity_id)
    update_estado(activity_id, "Eliminada")
    return {"id": activity_id, "estado": "Eliminada"}


@app.get("/api/buscar")
def buscar(
    nombre: str | None = Query(None, description="Nombre de la actividad a buscar"),
    fase: str | None = Query(None, description="Nombre de la fase cuyas actividades se listan"),
):
    if not nombre and not fase:
        raise HTTPException(status_code=422, detail="Debe enviar al menos 'nombre' o 'fase'")
    return {"resultados": buscar_actividades(nombre, fase)}


@app.get("/")
def root():
    return {
        "app": "API Calificaciones",
        "endpoints": [
            "/api/promedio-aprobacion",
            "/api/porcentaje-entregadas",
            "/api/total-entregadas",
            "/api/total-calificadas",
            "/api/total-a-entregar",
            "/api/total-eliminadas",
            "/api/total-actividades",
            "/api/faltantes-para-porcentaje?porcentaje=55",
            "/api/buscar?nombre=Infografía",
            "/api/buscar?fase=Fase 1 Análisis",
            "POST /api/actividades/{id}/subir",
            "POST /api/actividades/{id}/calificar  (body: calificacion, retroalimentacion opcional)",
            "POST /api/actividades/{id}/eliminar",
            "/api/resumen",
        ],
    }


@app.get("/api/promedio-aprobacion")
def get_promedio_aprobacion():
    return {"promedio_aprobacion": services.promedio_aprobacion(rows())}


@app.get("/api/porcentaje-entregadas")
def get_porcentaje_entregadas():
    return {"porcentaje_entregadas": services.porcentaje_entregadas(rows())}


@app.get("/api/total-entregadas")
def get_total_entregadas():
    return {"total_entregadas": services.total_entregadas(rows())}


@app.get("/api/total-calificadas")
def get_total_calificadas():
    return {"total_calificadas": services.total_calificadas(rows())}


@app.get("/api/total-a-entregar")
def get_total_a_entregar():
    return {"total_a_entregar": services.total_a_entregar(rows())}


@app.get("/api/total-eliminadas")
def get_total_eliminadas():
    return {"total_eliminadas": services.total_eliminadas(rows())}


@app.get("/api/total-actividades")
def get_total_actividades():
    return {"total_actividades": services.total_actividades(rows())}


@app.get("/api/faltantes-para-porcentaje")
def get_faltantes_para_porcentaje(
    porcentaje: float = Query(..., ge=0, le=100, description="Porcentaje objetivo de actividades entregadas")
):
    data = rows()
    return {
        "porcentaje_objetivo": porcentaje,
        "faltantes_por_entregar": services.faltantes_para_porcentaje(data, porcentaje),
    }


@app.get("/api/resumen")
def get_resumen():
    data = rows()
    return {
        "promedio_aprobacion": services.promedio_aprobacion(data),
        "porcentaje_entregadas": services.porcentaje_entregadas(data),
        "total_entregadas": services.total_entregadas(data),
        "total_calificadas": services.total_calificadas(data),
        "total_a_entregar": services.total_a_entregar(data),
        "total_eliminadas": services.total_eliminadas(data),
        "total_actividades": services.total_actividades(data),
    }
