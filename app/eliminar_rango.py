"""Marca como 'Eliminada' todas las actividades cuyo id esté dentro de un rango.

Uso:
    python eliminar_rango.py <desde> <hasta> [--db RUTA] [--no-backup] [-y]

Ejemplo:
    python eliminar_rango.py 10 25
"""
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="eliminar_rango",
        description="Marca como 'Eliminada' las actividades cuyo id esté en el rango indicado.",
    )
    parser.add_argument("desde", type=int, help="Id inicial del rango (incluido)")
    parser.add_argument("hasta", type=int, help="Id final del rango (incluido)")
    parser.add_argument("--db", help="Ruta de la base de datos destino (default: app/data/calificaciones.db)")
    parser.add_argument("--no-backup", action="store_true", help="No crea copia de seguridad de la base")
    parser.add_argument("-y", "--yes", action="store_true", help="Salta la confirmación")
    args = parser.parse_args()

    if args.desde > args.hasta:
        print("Error: 'desde' no puede ser mayor que 'hasta'.", file=sys.stderr)
        sys.exit(1)

    if args.db:
        os.environ["CALIFICACIONES_DB"] = os.path.abspath(args.db)

    from app import db

    conn = db.get_connection()
    try:
        filas = conn.execute(
            "SELECT id, actividad, estado FROM calificaciones WHERE id BETWEEN ? AND ? ORDER BY id",
            (args.desde, args.hasta),
        ).fetchall()

        if not filas:
            print("No se encontraron actividades en ese rango.")
            return

        print(f"Rango {args.desde}-{args.hasta}: {len(filas)} actividad(es)")
        for r in filas:
            print(f"  [{r['id']}] {r['estado']:<12} {r['actividad']}")

        if not args.yes:
            resp = input("\n¿Marcar TODAS como Eliminada? [s/N]: ").strip().lower()
            if resp not in ("s", "si", "sí", "y", "yes"):
                print("Cancelado.")
                return

        if not args.no_backup:
            backup = db.hacer_backup()
            if backup:
                print(f"Backup creado: {backup}")

        cur = conn.execute(
            "UPDATE calificaciones SET estado = 'Eliminada' WHERE id BETWEEN ? AND ?",
            (args.desde, args.hasta),
        )
        conn.commit()
        print(f"Listo: {cur.rowcount} actividad(es) marcada(s) como Eliminada.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
