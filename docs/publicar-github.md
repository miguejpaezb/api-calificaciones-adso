# 🐙 Publicar en GitHub y compartir

Pasos para subir el proyecto y pasárselo a tus compañeros.

---

## 1. Crear el repositorio en GitHub

1. Entra a <https://github.com> e inicia sesión.
2. Pulsa **New repository**.
3. Nombre del repositorio: `api-calificaciones-adso`.
4. Déjalo **público** (o privado e invita a tus compañeros).
5. **No** marques "Add a README" ni ".gitignore" (ya los tenemos).
6. Pulsa **Create repository** y **copia la URL** que aparece (termina en `.git`).

---

## 2. Configurar Git (solo la primera vez)

```powershell
git config --global user.name "Miguel Páez"
git config --global user.email "mjpb.learn@gmail.com"
```

---

## 3. Inicializar y subir el proyecto

Desde la **raíz del proyecto** (`CALIFICACIONES/`):

```powershell
git init
git add .
git commit -m "feat: API de calificaciones con FastAPI y SQLite"
git branch -M main
git remote add origin https://github.com/miguejpaezb/api-calificaciones-adso.git
git push -u origin main
```

> 💡 Si usas SSH, el remoto sería `git@github.com:miguejpaezb/api-calificaciones-adso.git`.

Cuando pida credenciales, se abrirá el navegador para iniciar sesión en GitHub.

---

## 4. Verificar

Recarga la página del repositorio. Deben aparecer:

```text
✅ README.md
✅ LICENSE
✅ docs/
✅ app/
✅ .gitignore
```

### ¿Qué NO se sube?

Gracias al `.gitignore`, quedan fuera:

- 🗄️ `app/data/*.db` (la base de datos)
- 🧾 Los respaldos `.bak-*.db`
- 📄 El HTML y la carpeta `_files` de Zajuna
- 🧹 `__pycache__/` y entornos virtuales

> Por eso cada compañero debe **migrar sus propios datos** siguiendo la [guía de migración](migracion-datos.md).

---

## 5. About, topics y licencia

En la página del repositorio, pulsa el engranaje ⚙️ junto a **About** (columna derecha) y completa:

**Description:**

```text
API REST en FastAPI + SQLite para migrar, consultar y gestionar las calificaciones del curso Análisis y Desarrollo de Software (Zajuna · SENA) desde un reporte HTML.
```

**Topics** (pégalos separados por coma):

```text
fastapi, python, sqlite, rest-api, uvicorn, beautifulsoup, zajuna, sena, adso, calificaciones, moodle, educational-project
```

**Licencia:** el archivo [`LICENSE`](../LICENSE) (MIT) ya está en la raíz, GitHub lo detecta automáticamente y muestra el badge **MIT license** en el About.

> Opcional: en **Settings → General → Social preview** sube una captura de `/docs` (Swagger).

---

## 6. Compartir con tus compañeros

Envíales el enlace:

```text
https://github.com/miguejpaezb/api-calificaciones-adso
```

Ellos deben:

1. **Clonar** o descargar el ZIP:

   ```powershell
   git clone https://github.com/miguejpaezb/api-calificaciones-adso.git
   cd api-calificaciones-adso
   ```

2. Seguir la [**Instalación**](instalacion.md).
3. Seguir la [**Migración de datos**](migracion-datos.md) con **su propio** HTML de Zajuna.
4. [**Levantar el servidor**](configuracion.md#-ejecutar-el-servidor) y usar la [**Guía de uso**](guia-api.md).

---

## 7. Actualizar el repositorio más adelante

Cada vez que hagas cambios:

```powershell
git add .
git commit -m "descripción del cambio"
git push
```

Tus compañeros los reciben con:

```powershell
git pull
```

---

## 🛠️ Problemas comunes

| Problema | Solución |
|:---|:---|
| `remote origin already exists` | `git remote set-url origin https://github.com/miguejpaezb/api-calificaciones-adso.git` |
| `failed to push ... rejected` | Ejecuta `git pull --rebase origin main` y vuelve a hacer `git push`. |
| Pide usuario y contraseña | Usa un **Personal Access Token** como contraseña o instala [GitHub CLI](https://cli.github.com/). |
| Se subió la base de datos por error | `git rm --cached app/data/calificaciones.db` y confirma que esté en `.gitignore`. |
