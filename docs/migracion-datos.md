# 📥 Migración de datos (Zajuna → SQLite)

Este proceso toma el reporte de calificaciones de **Zajuna** en formato HTML y lo convierte en la base de datos local `app/data/calificaciones.db`.

> ⚠️ La base **no viene incluida** en el repositorio. Cada compañero debe generarla con estos pasos.

---

## 1. Guardar el reporte desde Zajuna

1. Inicia sesión en **Zajuna** y entra al curso *Análisis y Desarrollo de Software*.
2. Abre la página de **Calificaciones / Notas** del curso.
3. Presiona **`Ctrl + S`** para guardar la página.
4. En el tipo de guardado elige **"Página web, completa"** y guarda.
   - Se generará un archivo `.html` y una carpeta `..._files` con los recursos.

> 💡 El script solo necesita el archivo **`.html`**. La carpeta `_files` puedes moverla también o dejarla; no afecta la migración.

---

## 2. Mover el HTML a la carpeta del proyecto

Mueve el archivo `.html` a la **raíz del proyecto**, es decir, **fuera** de la carpeta `app/`:

```text
CALIFICACIONES/
├── app/
│   ├── app/
│   ├── data/                      ← aquí se creará calificaciones.db
│   ├── migrar.py
│   └── ...
├── Usuario _ ... _ Zajuna.html    ← 📄 el HTML va aquí (fuera de app/)
└── README.md
```

---

## 3. Ejecutar la migración

Abre una terminal **dentro de la carpeta `app/`** y ejecuta el script:

```powershell
python migrar.py "..\Usuario _ ANALISIS Y DESARROLLO DE SOFTWARE. (3134556) _ Zajuna.html" --hasta "GA7-220501096-AA1-EV01"
```

> ✏️ Cambia el nombre del `.html` por el tuyo y ajusta el código de `--hasta` (ver abajo).

Cuando pregunte, escribe **`s`** y presiona Enter:

```text
¿Escribir los datos en la base de datos? [s/N]: s
```

### Resultado esperado (ejemplo)

```text
Corte: 'GA7-220501096-AA1-EV01' -> Evidencia Informe técnico de plan de trabajo para construcción de software GA7-220501096-AA1-EV01

Total de actividades: 142
Por estado:
  Calificado: 65
  Eliminada: 12
  No Entregado: 59
  Subido: 6
Por fase:
  Fase 1 Análisis: 21
  ...
Backup creado: C:\...\CALIFICACIONES\app\data\calificaciones.bak-20260823-111449.db
Migración completada.
```

Al terminar, la base queda en:

```text
app\data\calificaciones.db
```

---

## 4. ¿Qué significa `--hasta`?

Es el **código de la última evidencia que ya entregaste**. El script marca automáticamente:

| Situación de la actividad | Estado asignado |
|:---|:---|
| Tiene nota `A` o `D` | `Calificado` |
| Sin nota (`-`) y está **antes o en** el corte | `Eliminada` |
| Sin nota (`-`) y está **después** del corte | `No Entregado` |

> 🔎 Si omites `--hasta`, el script usa **automáticamente la última actividad con calificación** como corte.
> El código **no distingue mayúsculas/minúsculas** (`ga7-...` = `GA7-...`).

---

## 5. Parámetros del script

| Parámetro | Descripción |
|:---|:---|
| `html` | Ruta del archivo HTML de Zajuna (obligatorio). |
| `--hasta CODIGO` | Código de la última evidencia entregada. |
| `--db RUTA` | Base de datos destino (por defecto `app/data/calificaciones.db`). |
| `--dry-run` | Muestra el resumen **sin escribir** nada (prueba segura). |
| `-y`, `--yes` | Omite la confirmación. |
| `--no-backup` | No crea copia de seguridad de la base. |

---

## 6. Probar antes de escribir (recomendado)

```powershell
python migrar.py "..\reporte-zajuna.html" --hasta "GA7-220501096-AA1-EV01" --dry-run
```

Revisa el resumen y, si todo está bien, repite el comando sin `--dry-run`.

---

## 7. Marcar un rango de actividades como eliminadas

Después de migrar puede que necesites excluir un conjunto de actividades. Tienes dos opciones:

### Opción A — Script `eliminar_rango.py` (recomendado)

Marca como `Eliminada` todas las actividades cuyo **id** esté entre `desde` y `hasta`:

```powershell
python eliminar_rango.py 10 25
```

- Muestra primero el listado y pide confirmación.
- Crea un backup automático antes de escribir.
- Para omitir la confirmación: `python eliminar_rango.py 10 25 -y`

### Opción B — Con la API (servidor encendido)

```powershell
10..25 | ForEach-Object {
  Invoke-RestMethod -Method Post "http://127.0.0.1:8001/api/actividades/$_/eliminar"
}
```

> 👉 Más formas de gestionar actividades (Postman, SQL) en la [**Guía de uso**](guia-api.md#-marcar-un-rango-como-eliminada).

---

## ✅ Siguiente paso

Ya tienes los datos cargados. Ahora [**levanta el servidor**](configuracion.md#-ejecutar-el-servidor) y consulta la [**Guía de uso**](guia-api.md).
