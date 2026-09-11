import os
import re
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

CODIGO_RE = re.compile(r"^GA\d+-\d+-AA\d+-EV\d+$", re.IGNORECASE)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = Path(
    os.environ.get("CALIFICACIONES_DB", str(DATA_DIR / "calificaciones.db"))
)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_all_rows():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM calificaciones").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_actividad(activity_id):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM calificaciones WHERE id = ?", (activity_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_estado(activity_id, estado):
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE calificaciones SET estado = ? WHERE id = ?", (estado, activity_id)
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def update_calificacion(activity_id, calificacion, retroalimentacion):
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE calificaciones SET estado = 'Calificado', calificacion = ?, retroalimentacion = ? WHERE id = ?",
            (calificacion, retroalimentacion, activity_id),
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def buscar_actividades(nombre=None, fase=None):
    conn = get_connection()
    try:
        query = "SELECT id, actividad, calificacion, estado FROM calificaciones WHERE 1 = 1"
        params = []
        if nombre:
            query += " AND actividad COLLATE NOCASE LIKE ?"
            params.append(f"%{nombre}%")
        if fase:
            query += " AND fase COLLATE NOCASE LIKE ?"
            params.append(f"%{fase}%")
        rows = conn.execute(query + " ORDER BY id", params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def validar_codigos(codigos):
    """Normaliza, deduplica y valida códigos completos (ej. GA5-220501095-AA1-EV04).

    Devuelve (validos, invalidos): listas de códigos en mayúsculas y sin duplicados.
    """
    validos = []
    invalidos = []
    for codigo in codigos:
        normalizado = codigo.strip().upper()
        if not normalizado or normalizado in validos or normalizado in invalidos:
            continue
        if CODIGO_RE.match(normalizado):
            validos.append(normalizado)
        else:
            invalidos.append(normalizado)
    return validos, invalidos


def marcar_por_codigos(codigos, estado):
    """Marca como `estado` las actividades cuyo texto contenga cada código.

    Devuelve (detalle, no_encontradas, ambiguas):
    - detalle: [{"codigo", "id", "actividad"}]
    - no_encontradas: [codigo, ...]
    - ambiguas: [{"codigo", "ids": [...]}]
    """
    conn = get_connection()
    try:
        rows = conn.execute("SELECT id, actividad FROM calificaciones").fetchall()
        detalle = []
        no_encontradas = []
        ambiguas = []
        ids = []
        for codigo in codigos:
            coincidencias = [r for r in rows if codigo in (r["actividad"] or "").upper()]
            if not coincidencias:
                no_encontradas.append(codigo)
            elif len(coincidencias) > 1:
                ambiguas.append({"codigo": codigo, "ids": [r["id"] for r in coincidencias]})
            else:
                fila = coincidencias[0]
                ids.append(fila["id"])
                detalle.append({"codigo": codigo, "id": fila["id"], "actividad": fila["actividad"]})
        if ids:
            conn.executemany(
                "UPDATE calificaciones SET estado = ? WHERE id = ?",
                [(estado, i) for i in ids],
            )
            conn.commit()
        return detalle, no_encontradas, ambiguas
    finally:
        conn.close()


def hacer_backup():
    if not DB_PATH.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = DB_PATH.with_name(f"{DB_PATH.stem}.bak-{timestamp}{DB_PATH.suffix}")
    shutil.copy2(DB_PATH, backup)
    return backup


def reemplazar_calificaciones(rows):
    conn = get_connection()
    try:
        conn.execute("DROP TABLE IF EXISTS calificaciones")
        conn.execute(
            """
            CREATE TABLE calificaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fase TEXT,
                tipo TEXT,
                actividad TEXT NOT NULL,
                calificacion TEXT CHECK (calificacion IN ('A', 'D', '-')),
                retroalimentacion TEXT,
                estado TEXT CHECK (estado IN ('Subido', 'Calificado', 'No Entregado', 'Eliminada'))
            )
            """
        )
        conn.executemany(
            "INSERT INTO calificaciones (fase, tipo, actividad, calificacion, retroalimentacion, estado) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            [
                (r["fase"], r["tipo"], r["actividad"], r["calificacion"], r["retroalimentacion"], r["estado"])
                for r in rows
            ],
        )
        conn.commit()
    finally:
        conn.close()
