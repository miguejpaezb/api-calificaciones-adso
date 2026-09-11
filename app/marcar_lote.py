"""Marca actividades como 'Subido' o 'Eliminada' en lote usando códigos completos.

Uso:
    python marcar_lote.py subido --codigos "GA5-220501095-AA1-EV04,GA5-220501095-AA1-EV05"
    python marcar_lote.py eliminada --archivo codigos.txt
    python marcar_lote.py subido --codigos "..." -y --no-backup

Solo acepta códigos con el formato completo (ej. GA5-220501095-AA1-EV04).
Si un código no cumple el formato o no se encuentra, deberá marcarse de forma manual.
"""
import argparse
import os
import sys


def leer_codigos(args):
    codigos = []
    if args.codigos:
        codigos.extend(args.codigos.split(","))
    if args.archivo:
        try:
            with open(args.archivo, encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if linea and not linea.startswith("#"):
                        codigos.append(linea)
        except FileNotFoundError:
            print(f"Error: no existe el archivo {args.archivo}", file=sys.stderr)
            sys.exit(1)
    return codigos


def main():
    parser = argparse.ArgumentParser(
        prog="marcar_lote",
        description="Marca en lote actividades como Subido o Eliminada usando códigos completos.",
    )
    parser.add_argument("estado", choices=["subido", "eliminada"], help="Estado a aplicar")
    parser.add_argument("--codigos", help="Códigos separados por coma")
    parser.add_argument("--archivo", help="Archivo .txt con un código por línea")
    parser.add_argument("--db", help="Ruta de la base de datos destino")
    parser.add_argument("--no-backup", action="store_true", help="No crea copia de seguridad")
    parser.add_argument("-y", "--yes", action="store_true", help="Salta la confirmación")
    args = parser.parse_args()

    codigos = leer_codigos(args)
    if not codigos:
        print("Error: debes indicar --codigos o --archivo.", file=sys.stderr)
        sys.exit(1)

    if args.db:
        os.environ["CALIFICACIONES_DB"] = os.path.abspath(args.db)

    from app import db

    estado = "Subido" if args.estado == "subido" else "Eliminada"

    validos, invalidos = db.validar_codigos(codigos)
    if invalidos:
        print(
            "Revisa estos códigos, no tienen el formato completo "
            "(ej. GA5-220501095-AA1-EV04):",
            file=sys.stderr,
        )
        for codigo in invalidos:
            print(f"  - {codigo}", file=sys.stderr)
        print("Corrígelos o márcalos de forma manual.", file=sys.stderr)
        sys.exit(1)

    if not args.yes:
        resp = input(
            f"\n¿Marcar como {estado} las actividades de {len(validos)} código(s)? [s/N]: "
        ).strip().lower()
        if resp not in ("s", "si", "sí", "y", "yes"):
            print("Cancelado.")
            return

    if not args.no_backup:
        backup = db.hacer_backup()
        if backup:
            print(f"Backup creado: {backup}")

    detalle, no_encontradas, ambiguas = db.marcar_por_codigos(validos, estado)

    print(f"\nEstado aplicado: {estado}")
    print(f"Actualizadas: {len(detalle)}")
    for d in detalle:
        print(f"  [{d['id']}] {d['codigo']} -> {d['actividad'][:70]}")
    if no_encontradas:
        print("No encontradas (revisa el código):")
        for codigo in no_encontradas:
            print(f"  - {codigo}")
    if ambiguas:
        print("Ambigüedades (hazlo de forma manual):")
        for a in ambiguas:
            print(f"  - {a['codigo']} -> ids {a['ids']}")
    if no_encontradas or ambiguas:
        print("\nLos códigos anteriores deben revisarse o marcarse de forma manual.")


if __name__ == "__main__":
    main()
