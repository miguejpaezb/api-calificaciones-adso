# ⚙️ Configuración

Ajustes de la base de datos, el servidor y las dependencias.

---

## 💾 Ubicación de la base de datos

Por defecto la base se guarda dentro de `app/`, en una carpeta exclusiva para bases de datos:

```text
CALIFICACIONES/app/data/calificaciones.db
```

La carpeta `data/` se crea automáticamente si no existe.

> 🚫 Tanto la base como sus respaldos están en `.gitignore`: **no se suben a GitHub**.

### Usar otra base de datos

Puedes apuntar a otro archivo con la variable de entorno `CALIFICACIONES_DB`:

```powershell
$env:CALIFICACIONES_DB = "C:\ruta\otra.db"
python -m uvicorn app.main:app --reload --port 8001
```

O con los scripts de migración/eliminación mediante `--db`:

```powershell
python migrar.py "..\reporte.html" --db "C:\ruta\otra.db"
python eliminar_rango.py 10 25 --db "C:\ruta\otra.db"
```

---

## ▶️ Ejecutar el servidor

Desde la carpeta `app/`:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

| Opción | Descripción |
|:---|:---|
| `--reload` | Reinicia el servidor al guardar cambios (útil en desarrollo). |
| `--port 8001` | Puerto del servidor. Cámbialo si está ocupado (el `8000` suele estarlo). |

Una vez iniciado:

| Recurso | URL |
|:---|:---|
| API | <http://127.0.0.1:8001> |
| Swagger (interactivo) | <http://127.0.0.1:8001/docs> |
| ReDoc (alternativo) | <http://127.0.0.1:8001/redoc> |

Para detener el servidor: **`Ctrl + C`**.

---

## 🌐 CORS

La API permite peticiones desde cualquier origen (`allow_origins=["*"]`), lo que facilita probarla desde un frontend local o desde Postman.

---

## 🗄️ Estructura de la tabla `calificaciones`

| Columna | Tipo | Descripción |
|:---|:---|:---|
| `id` | INTEGER (PK) | Identificador de la actividad |
| `fase` | TEXT | Fase del curso a la que pertenece |
| `tipo` | TEXT | Tipo (Evidencia, Foro, Prueba de Conocimiento...) |
| `actividad` | TEXT (NOT NULL) | Nombre completo de la actividad |
| `calificacion` | TEXT | `A`, `D` o `-` (validado con CHECK) |
| `retroalimentacion` | TEXT | Comentario del instructor |
| `estado` | TEXT | `Subido`, `Calificado`, `No Entregado` o `Eliminada` |

---

## 📦 Dependencias

```text
fastapi==0.141.1
uvicorn[standard]==0.52.3
beautifulsoup4==4.15.0
```

Para reinstalarlas:

```powershell
pip install -r requirements.txt
```

---

## 🔁 Flujo de trabajo típico

```text
1. Migrar HTML de Zajuna      →  python migrar.py ...
2. (Opcional) Ajustar rangos  →  python eliminar_rango.py 10 25
3. Levantar el servidor       →  python -m uvicorn app.main:app --reload --port 8001
4. Consultar / gestionar      →  Swagger, Postman o consola
```
