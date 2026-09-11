"""Migra un HTML de calificaciones de Zajuna/Moodle a la base de datos SQLite.

Uso:
    python migrar.py <archivo.html> [--hasta CODIGO] [--db RUTA] [--dry-run] [-y] [--no-backup]

--hasta: código de la última evidencia entregada (ej. GA7-220501096-AA3-EV01).
         Si se omite, se detecta automáticamente la última actividad con calificación.
         La comparación ignora mayúsculas/minúsculas (ga7-... == GA7-...).
"""
import argparse
import os
import sys


def normalizar(texto):
    return texto.strip().upper()


def calcular_estado(calificacion, idx, corte):
    if calificacion in ("A", "D"):
        return "Calificado"
    if calificacion == "-":
        return "Eliminada" if idx <= corte else "No Entregado"
    return "Subido"


def main():
    parser = argparse.ArgumentParser(
        prog="migrar",
        description="Migra un HTML de calificaciones a la base de datos.",
    )
    parser.add_argument("html", help="Ruta del archivo HTML de calificaciones")
    parser.add_argument(
        "--hasta",
        help="Código de la última evidencia entregada (ej. GA7-220501096-AA3-EV01). "
        "Si se omite, se usa la última actividad con calificación.",
    )
    parser.add_argument("--db", help="Ruta de la base de datos destino (default: calificaciones.db)")
    parser.add_argument("--dry-run", action="store_true", help="Muestra el resumen sin escribir nada")
    parser.add_argument("-y", "--yes", action="store_true", help="Salta la confirmación")
    parser.add_argument("--no-backup", action="store_true", help="No crea copia de seguridad de la base")
    args = parser.parse_args()

    if args.db:
        os.environ["CALIFICACIONES_DB"] = os.path.abspath(args.db)

    from app.parser import parse_grade_html
    from app import db

    try:
        filas = parse_grade_html(args.html)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not filas:
        print("Error: no se encontraron actividades en el HTML", file=sys.stderr)
        sys.exit(1)

    if args.hasta:
        objetivo = normalizar(args.hasta)
        coincidencias = [i for i, r in enumerate(filas) if objetivo in normalizar(r["actividad"])]
        if not coincidencias:
            print(f"Error: no se encontró ninguna actividad con el código '{args.hasta}'", file=sys.stderr)
            sys.exit(1)
        if len(coincidencias) > 1:
            print("Error: el código coincide con varias actividades:", file=sys.stderr)
            for i in coincidencias:
                print(f"  {i + 1}. {filas[i]['actividad']}", file=sys.stderr)
            print("Usa un código más específico.", file=sys.stderr)
            sys.exit(1)
        corte = coincidencias[0]
        print(f"Corte: '{args.hasta}' -> {filas[corte]['actividad']}")
    else:
        calificadas = [i for i, r in enumerate(filas) if r["calificacion"] in ("A", "D")]
        if not calificadas:
            print("Error: no hay actividades con calificación para detectar el corte", file=sys.stderr)
            sys.exit(1)
        corte = max(calificadas)
        print(f"Corte automático (última calificada): {filas[corte]['actividad']}")

    for idx, r in enumerate(filas):
        r["estado"] = calcular_estado(r["calificacion"], idx, corte)

    from collections import Counter

    por_estado = Counter(r["estado"] for r in filas)
    por_fase = Counter(r["fase"] for r in filas)

    print()
    print(f"Total de actividades: {len(filas)}")
    print("Por estado:")
    for estado, n in por_estado.items():
        print(f"  {estado}: {n}")
    print("Por fase:")
    for fase, n in por_fase.items():
        print(f"  {fase or '(sin fase)'}: {n}")

    if args.dry_run:
        print("\n[dry-run] No se escribió nada en la base de datos.")
        return

    if not args.yes:
        resp = input("\n¿Escribir los datos en la base de datos? [s/N]: ").strip().lower()
        if resp not in ("s", "si", "sí", "y", "yes"):
            print("Cancelado.")
            return

    if not args.no_backup:
        backup = db.hacer_backup()
        if backup:
            print(f"Backup creado: {backup}")

    db.reemplazar_calificaciones(filas)
    print("Migración completada.")


if __name__ == "__main__":
    main()
