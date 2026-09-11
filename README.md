<div align="center">

# 🎓 API Calificaciones

**Consulta, migra y gestiona las calificaciones del curso _Análisis y Desarrollo de Software_ (Zajuna · SENA) desde una API REST.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.52-499848?style=for-the-badge&logo=gunicorn&logoColor=white)](https://www.uvicorn.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.15-4B8BBE?style=for-the-badge&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

## 📌 ¿Qué hace?

- 📥 **Migra** el reporte de calificaciones de Zajuna (HTML) a una base de datos SQLite.
- 📊 **Calcula** porcentaje de entregas, aprobación, faltantes y totales del curso.
- 🔎 **Busca** actividades por nombre o por fase.
- ✍️ **Actualiza** actividades: subir, calificar (A / D / -) o marcar como eliminada.
- 🗑️ **Marca rangos completos** de actividades como eliminadas en un solo comando.

> La base de datos se guarda en `app/data/calificaciones.db`. **No se sube a GitHub**: cada compañero la genera ejecutando la migración.

---

## 🧰 Tecnologías

| Tecnología | Versión | Rol en el proyecto |
|:---|:---:|:---|
| 🐍 **Python** | 3.10+ | Lenguaje base del backend |
| ⚡ **FastAPI** | 0.141.1 | Framework de la API REST |
| 🚀 **Uvicorn** | 0.52.3 | Servidor ASGI que ejecuta la app |
| 🗄️ **SQLite** | 3 | Base de datos local (archivo `.db`) |
| 🍲 **BeautifulSoup4** | 4.15.0 | Lee y extrae la tabla del HTML de Zajuna |

---

## ⚡ Inicio rápido

```powershell
# 1. Instalar dependencias (desde la carpeta app/)
pip install -r requirements.txt

# 2. Migrar las calificaciones desde el HTML de Zajuna
python migrar.py "..\reporte-zajuna.html" --hasta "GA7-220501096-AA1-EV01"

# 3. Levantar el servidor
python -m uvicorn app.main:app --reload --port 8001
```

Luego abre 👉 **http://127.0.0.1:8001/docs** (Swagger) o **http://127.0.0.1:8001/redoc**.

> El paso a paso completo está en la documentación 👇

---

## 📚 Documentación

| Documento | Contenido |
|:---|:---|
| 🚀 [**Instalación**](docs/instalacion.md) | Requisitos, clonar el proyecto y dependencias |
| 📥 [**Migración de datos**](docs/migracion-datos.md) | Guardar el HTML de Zajuna e importarlo a la base |
| ⚙️ [**Configuración**](docs/configuracion.md) | Ruta de la base, puerto, variables de entorno |
| 🧭 [**Guía de uso**](docs/guia-api.md) | Todos los endpoints con **Postman** y **consola** |
| 🐙 [**Publicar en GitHub**](docs/publicar-github.md) | Subir el proyecto y compartirlo con tus compañeros |

---

## 🗂️ Estructura del proyecto

```text
CALIFICACIONES/
├── app/                      # Código del sistema
│   ├── app/                  # Paquete FastAPI
│   │   ├── main.py           # Endpoints de la API
│   │   ├── db.py             # Conexión y consultas SQLite
│   │   ├── parser.py         # Lee el HTML de Zajuna
│   │   └── services.py       # Cálculos de totales y porcentajes
│   ├── data/                 # 💾 Bases de datos (se ignora en Git)
│   ├── migrar.py             # Script de migración HTML → SQLite
│   ├── eliminar_rango.py     # Marca un rango de ids como Eliminada
│   ├── marcar_lote.py        # Marca por código en lote (Subido/Eliminada)
│   └── requirements.txt      # Dependencias
├── docs/                     # 📚 Documentación detallada
├── README.md                 # Este archivo
├── LICENSE                   # Licencia MIT
└── .gitignore
```

---

## 🔌 Endpoints principales

| Método | Endpoint | Descripción |
|:---:|:---|:---|
| `GET` | `/api/resumen` | Todos los cálculos en una sola respuesta |
| `GET` | `/api/porcentaje-entregadas` | % de actividades entregadas |
| `GET` | `/api/promedio-aprobacion` | % de aprobación sobre lo entregado |
| `GET` | `/api/faltantes-para-porcentaje?porcentaje=55` | Cuántas faltan para un objetivo |
| `GET` | `/api/buscar?nombre=Infografía` | Busca actividades por nombre |
| `GET` | `/api/buscar?fase=Fase 1` | Lista actividades de una fase |
| `POST` | `/api/actividades/{id}/subir` | Marca una actividad como subida |
| `POST` | `/api/actividades/{id}/calificar` | Califica (A / D / -) |
| `POST` | `/api/actividades/{id}/eliminar` | Marca una actividad como eliminada |
| `POST` | `/api/actividades/lote` | Marca varias como `Subido`/`Eliminada` por código |

👉 Detalle, ejemplos y resultados esperados en la [**Guía de uso**](docs/guia-api.md).

---

## 🏷️ Estados de una actividad

| Estado | Significado |
|:---|:---|
| `Calificado` | Entregada y con nota (A o D) |
| `Subido` | Entregada, pendiente de calificación |
| `No Entregado` | Falta por entregar |
| `Eliminada` | Fuera del curso (no cuenta en los cálculos) |

---

## 🚀 Reto: constrúyele tu propia interfaz

La API ya está lista para que la consumas. **No hay restricciones**: usa el lenguaje, framework o plataforma que quieras. La idea es que la lleves más allá y la conectes a algo visual o útil.

Algunas ideas (pero puedes inventar la tuya):

- 📱 **App móvil** — Flutter, React Native, Kotlin, Swift...
- 🌐 **Web** — React, Vue, Angular, Svelte o HTML + JS puro...
- 🖥️ **Escritorio** — Electron, Tauri, .NET, Python (Tkinter/Qt)...
- ⌨️ **CLI** — un comando que consulte tu progreso...
- 🤖 **Otras** — bot de Discord/Telegram, dashboard, hoja de cálculo, widget...

> ✅ El CORS ya está abierto (`allow_origins=["*"]`), así que puedes conectarte sin configurar nada extra.
> Solo necesitas la URL base `http://127.0.0.1:8001` y los endpoints de la [**Guía de uso**](docs/guia-api.md).

**Ideas de funcionalidades:** dashboard de progreso, calculadora de "cuánto me falta para el 60%", gráficos por fase, recordatorios de entregas pendientes, comparador con tus compañeros...

---

## 👤 Autor

**Miguel Páez** · [@miguejpaezb](https://github.com/miguejpaezb)

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

<div align="center">

Hecho con 🧡 para el programa **Análisis y Desarrollo de Software** · SENA

</div>
