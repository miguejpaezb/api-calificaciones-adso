import re
from pathlib import Path

from bs4 import BeautifulSoup


def clean_text(s):
    s = s.replace("\xa0", " ")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def parse_grade_html(ruta_html):
    """Extrae las actividades de una tabla de calificaciones de Zajuna/Moodle.

    Devuelve una lista de dicts con: fase, tipo, actividad, calificacion, retroalimentacion.
    """
    path = Path(ruta_html)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo HTML: {path}")

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    table = soup.find("table", class_="user-grade")
    if table is None:
        raise ValueError("No se encontró la tabla de calificaciones (class 'user-grade') en el HTML")

    rows = []
    current_fase = None

    for tr in table.find_all("tr"):
        th = tr.find("th", recursive=False)
        tds = tr.find_all("td", recursive=False)

        if th is not None:
            thcls = th.get("class") or []
            if "category" in thcls and "item" not in thcls:
                span = th.select_one(".category-content > span")
                if span:
                    current_fase = clean_text(span.get_text())
                continue
            if "categoryitem" in thcls:
                continue

        if th is None:
            continue

        thcls = th.get("class") or []
        if "item" not in thcls:
            continue

        tipo_span = th.find("span", class_="dimmed_text")
        tipo = clean_text(tipo_span.get_text()) if tipo_span else ""

        a = th.find("a", class_="gradeitemheader")
        nombre = clean_text(a.get_text()) if a else ""

        actividad = f"{tipo} {nombre}".strip()

        grado_td = None
        feedback_td = None
        for td in tds:
            tdcls = td.get("class") or []
            if "column-lettergrade" in tdcls:
                grado_td = td
            elif "column-feedback" in tdcls:
                feedback_td = td

        calificacion = clean_text(grado_td.get_text()) if grado_td else ""
        retro = clean_text(feedback_td.get_text()) if feedback_td else ""

        if not actividad:
            continue

        rows.append(
            {
                "fase": current_fase,
                "tipo": tipo,
                "actividad": actividad,
                "calificacion": calificacion,
                "retroalimentacion": retro,
            }
        )

    return rows
