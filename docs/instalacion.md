# 🚀 Instalación

Guía paso a paso para dejar el proyecto listo en tu computador (Windows).

---

## 1. Requisitos previos

| Requisito | Versión | Cómo verificar |
|:---|:---:|:---|
| 🐍 Python | 3.10 o superior | `python --version` |
| 📦 pip | incluido con Python | `pip --version` |
| 🐙 Git *(opcional)* | cualquiera | `git --version` |

> Si `python --version` no funciona, instala Python desde <https://www.python.org/downloads/> y marca la casilla **"Add Python to PATH"**.

---

## 2. Obtener el proyecto

**Opción A — Clonar con Git (recomendado):**

```powershell
git clone https://github.com/miguejpaezb/api-calificaciones-adso.git
cd api-calificaciones-adso
```

**Opción B — Descargar ZIP:**

1. En GitHub pulsa el botón verde **Code → Download ZIP**.
2. Descomprime el archivo.
3. Abre una terminal dentro de la carpeta descomprimida.

---

## 3. Ubicarse en la carpeta `app/`

Todos los comandos de aquí en adelante se ejecutan desde la carpeta `app/`:

```powershell
cd app
```

> 📁 La estructura debe quedar así: `CALIFICACIONES\app\app\main.py`, `CALIFICACIONES\app\migrar.py`, etc.

---

## 4. Crear un entorno virtual *(opcional pero recomendado)*

Aísla las dependencias del proyecto del resto de tu sistema.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea el script de activación, ejecuta una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

## 5. Instalar dependencias

```powershell
pip install -r requirements.txt
```

Esto instala:

- `fastapi==0.141.1`
- `uvicorn[standard]==0.52.3`
- `beautifulsoup4==4.15.0`

---

## 6. Verificar la instalación

```powershell
python -c "import fastapi, uvicorn, bs4; print('OK')"
```

Debe imprimir:

```text
OK
```

---

## 7. Siguiente paso

👉 Continúa con la [**Migración de datos**](migracion-datos.md) para cargar las calificaciones y luego [**levantar el servidor**](configuracion.md#-ejecutar-el-servidor).

---

## 🛠️ Problemas comunes

| Problema | Solución |
|:---|:---|
| `python no se reconoce como un comando` | Reinstala Python marcando **Add Python to PATH**. |
| `pip no se reconoce` | Usa `python -m pip install -r requirements.txt`. |
| `No module named fastapi` | Asegúrate de haber activado el entorno virtual y ejecutado el paso 5. |
| Error de permisos al activar el venv | Ejecuta el comando `Set-ExecutionPolicy` del paso 4. |
