# 🧭 Guía de uso (Postman y consola)

Todos los endpoints de la API con comandos exactos y resultados esperados.

---

## ▶️ Antes de empezar

Levanta el servidor desde la carpeta `app/`:

```powershell
python -m uvicorn app.main:app --reload --port 8001
```

| Recurso | URL |
|:---|:---|
| URL base | `http://127.0.0.1:8001` |
| Swagger (probar desde el navegador) | <http://127.0.0.1:8001/docs> |
| ReDoc | <http://127.0.0.1:8001/redoc> |

> 💡 En **Swagger** puedes probar todo sin escribir comandos: despliega un endpoint, pulsa **Try it out**, llena los campos y **Execute**.

> 📊 Los resultados mostrados abajo corresponden a la base de ejemplo (130 actividades). Los tuyos pueden variar según tu migración.

---

## 📈 Endpoints de cálculo (GET)

### `GET /api/resumen`

Todos los cálculos en una sola respuesta.

**Consola:**

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/resumen
```

**Postman:** método `GET`, URL `http://127.0.0.1:8001/api/resumen`, **Send**.

**Resultado esperado:**

```json
{
  "promedio_aprobacion": 91.55,
  "porcentaje_entregadas": 54.62,
  "total_entregadas": 71,
  "total_calificadas": 65,
  "total_a_entregar": 59,
  "total_eliminadas": 12,
  "total_actividades": 130
}
```

---

### `GET /api/porcentaje-entregadas`

Porcentaje de actividades entregadas sobre el total del curso (sin contar eliminadas).

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/porcentaje-entregadas
```

```json
{"porcentaje_entregadas": 54.62}
```

---

### `GET /api/promedio-aprobacion`

Porcentaje de aprobación sobre las actividades entregadas (cuántas tienen `A`).

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/promedio-aprobacion
```

```json
{"promedio_aprobacion": 91.55}
```

---

### Totales simples

| Endpoint | Descripción | Resultado esperado |
|:---|:---|:---|
| `/api/total-entregadas` | Actividades entregadas | `{"total_entregadas": 71}` |
| `/api/total-calificadas` | Entregadas con nota | `{"total_calificadas": 65}` |
| `/api/total-a-entregar` | Faltan por entregar | `{"total_a_entregar": 59}` |
| `/api/total-eliminadas` | Marcadas como eliminadas | `{"total_eliminadas": 12}` |
| `/api/total-actividades` | Total del curso (sin eliminadas) | `{"total_actividades": 130}` |

Ejemplo:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/total-actividades
```

```json
{"total_actividades": 130}
```

---

### `GET /api/faltantes-para-porcentaje?porcentaje=55`

Cuántas actividades faltan por entregar para alcanzar un porcentaje objetivo (0–100).

```powershell
Invoke-RestMethod "http://127.0.0.1:8001/api/faltantes-para-porcentaje?porcentaje=55"
```

```json
{"porcentaje_objetivo": 55.0, "faltantes_por_entregar": 1}
```

Con la base actual (71 entregadas de 130):

| Objetivo | Resultado |
|:---:|:---|
| `50` | `{"faltantes_por_entregar": 0}` |
| `55` | `{"faltantes_por_entregar": 1}` |
| `60` | `{"faltantes_por_entregar": 7}` |
| `65` | `{"faltantes_por_entregar": 14}` |
| `100` | `{"faltantes_por_entregar": 59}` |

---

## 🔎 Búsqueda (GET)

### `GET /api/buscar?nombre=Infograf`

Busca actividades por nombre (coincidencia parcial, no distingue mayúsculas). Devuelve `id`, `actividad`, `calificacion` y `estado`.

```powershell
Invoke-RestMethod "http://127.0.0.1:8001/api/buscar?nombre=Infograf"
```

```json
{
  "resultados": [
    {"id": 1, "actividad": "Evidencia Infografía. AA1-EV01", "calificacion": "A", "estado": "Calificado"},
    {"id": 70, "actividad": "Evidencia Infografía - Plan de higiene y gasto calórico GA6-230101507-AA2-EV01", "calificacion": "A", "estado": "Calificado"},
    {"id": 126, "actividad": "Evidencia Infografía procesos de desarrollo del software. GA11-220501098-AA1-EV01", "calificacion": "-", "estado": "No Entregado"},
    {"id": 137, "actividad": "Evidencia Infografía sobre la huelga. GA11-210201501-AA2-EV04", "calificacion": "-", "estado": "No Entregado"}
  ]
}
```

### `GET /api/buscar?fase=Fase 1`

Lista las actividades de una fase.

```powershell
Invoke-RestMethod "http://127.0.0.1:8001/api/buscar?fase=Fase 1"
```

```json
{
  "resultados": [
    {"id": 6, "actividad": "Evidencia Identificación de procesos organizacionales. GA1-220501092-AA1-EV02", "calificacion": "A", "estado": "Calificado"},
    {"id": 7, "actividad": "Evidencia Formulación del proyecto de software. GA1-220501092-AA3-EV02", "calificacion": "A", "estado": "Calificado"}
  ]
}
```

> También se pueden combinar: `?nombre=Infograf&fase=Fase 3`. Si no envías ninguno, responde **422**.

> 💡 **Para saber el `id` de una actividad**, primero búscala por nombre o fase; el campo `id` es el que usarás en los endpoints `POST`.

---

## ✍️ Gestión de actividades (POST)

> ⚠️ Estos endpoints **modifican** la base de datos.

### `POST /api/actividades/{id}/subir`

Marca una actividad como subida (entregada, pendiente de calificación).

**Consola:**

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8001/api/actividades/43/subir
```

**Postman:**

1. Nueva petición → método **POST**.
2. URL: `http://127.0.0.1:8001/api/actividades/43/subir`
3. **Send** (sin body).

**Resultado esperado:**

```json
{"id": 43, "estado": "Subido"}
```

---

### `POST /api/actividades/{id}/calificar`

Marca una actividad como calificada. Requiere `calificacion` (`A`, `D` o `-`) y acepta `retroalimentacion` opcional.

**Consola:**

```powershell
$body = @{ calificacion = "A"; retroalimentacion = "Bien hecho" } | ConvertTo-Json
Invoke-RestMethod -Method Post http://127.0.0.1:8001/api/actividades/43/calificar `
  -ContentType "application/json" -Body $body
```

Sin retroalimentación:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8001/api/actividades/44/calificar `
  -ContentType "application/json" -Body '{"calificacion":"D"}'
```

**Postman:**

1. Método **POST**, URL `http://127.0.0.1:8001/api/actividades/43/calificar`.
2. Pestaña **Body → raw → JSON**.
3. Pega:

   ```json
   {"calificacion": "A", "retroalimentacion": "Bien hecho"}
   ```

4. **Send**.

**Resultado esperado:**

```json
{"id": 43, "estado": "Calificado", "calificacion": "A"}
```

---

### `POST /api/actividades/{id}/eliminar`

Marca una actividad como eliminada (queda fuera de los cálculos del curso).

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8001/api/actividades/45/eliminar
```

```json
{"id": 45, "estado": "Eliminada"}
```

---

## 🗑️ Marcar un rango como eliminada

Para marcar de una sola vez las actividades con `id` entre **x** e **y**.

### Opción A — Script `eliminar_rango.py` (recomendado)

Desde `app/`:

```powershell
python eliminar_rango.py 10 25
```

Salida:

```text
Rango 10-25: 16 actividad(es)
  [10] Calificado   Evidencia Taller sobre metodologías...
  ...
Backup creado: ...\app\data\calificaciones.bak-20260910-120000.db
Listo: 16 actividad(es) marcada(s) como Eliminada.
```

Opciones: `-y` (sin confirmar) y `--db RUTA` (otra base).

### Opción B — Con la API (servidor encendido)

```powershell
10..25 | ForEach-Object {
  Invoke-RestMethod -Method Post "http://127.0.0.1:8001/api/actividades/$_/eliminar"
}
```

Cada petición responde: `{"id": <n>, "estado": "Eliminada"}`.

### Opción C — Directo en la base (SQL)

Desde `app/`, pega este bloque completo en la terminal:

```powershell
@'
from app import db
c = db.get_connection()
cur = c.execute("UPDATE calificaciones SET estado='Eliminada' WHERE id BETWEEN 10 AND 25")
c.commit()
print("Eliminadas:", cur.rowcount)
c.close()
'@ | python -
```

Salida esperada:

```text
Eliminadas: 16
```

---

## 🏷️ Estados posibles

| Estado | Significado |
|:---|:---|
| `Subido` | Entregada, pendiente de calificación |
| `Calificado` | Entregada y calificada (A o D) |
| `No Entregado` | Falta por entregar |
| `Eliminada` | Fuera del curso (no se cuenta en los cálculos) |

---

## 🚨 Códigos de error

| Código | Cuándo ocurre | Ejemplo de respuesta |
|:---:|:---|:---|
| `404` | El `id` de la actividad no existe | `{"detail": "Actividad con id 999 no encontrada"}` |
| `422` | Faltan parámetros o calificación inválida | `{"detail": "Debe enviar al menos 'nombre' o 'fase'"}` |

---

## 🧪 Ejercicio rápido de prueba

```powershell
# 1. Ver el resumen actual
Invoke-RestMethod http://127.0.0.1:8001/api/resumen

# 2. Buscar una actividad y quedarte con su id
Invoke-RestMethod "http://127.0.0.1:8001/api/buscar?nombre=Infograf"

# 3. Subirla y ver el cambio
Invoke-RestMethod -Method Post http://127.0.0.1:8001/api/actividades/1/subir

# 4. Volver a ver el resumen (las entregas aumentaron)
Invoke-RestMethod http://127.0.0.1:8001/api/resumen
```
