import math

ESTADO_ELIMINADA = "Eliminada"
ESTADOS_ENTREGADA = ("Calificado", "Subido")
CALIFICACION_APROBADA = "A"


def es_entregada(row):
    return row["estado"] in ESTADOS_ENTREGADA


def es_calificada(row):
    return row["calificacion"] in ("A", "D")


def total_actividades(rows):
    return sum(1 for r in rows if r["estado"] != ESTADO_ELIMINADA)


def total_eliminadas(rows):
    return sum(1 for r in rows if r["estado"] == ESTADO_ELIMINADA)


def total_entregadas(rows):
    return sum(1 for r in rows if es_entregada(r))


def total_calificadas(rows):
    return sum(1 for r in rows if es_entregada(r) and es_calificada(r))


def total_a_entregar(rows):
    return sum(1 for r in rows if r["estado"] == "No Entregado")


def promedio_aprobacion(rows):
    entregadas = [r for r in rows if es_entregada(r)]
    if not entregadas:
        return 0.0
    aprobadas = sum(1 for r in entregadas if r["calificacion"] == CALIFICACION_APROBADA)
    return round(aprobadas / len(entregadas) * 100, 2)


def porcentaje_entregadas(rows):
    base = total_actividades(rows)
    if base == 0:
        return 0.0
    return round(total_entregadas(rows) / base * 100, 2)


def faltantes_para_porcentaje(rows, porcentaje):
    entregadas = total_entregadas(rows)
    total = total_actividades(rows)
    if total == 0:
        return 0
    faltantes_exactos = porcentaje * total / 100 - entregadas
    if faltantes_exactos <= 0:
        return 0
    return math.floor(faltantes_exactos + 0.5)
