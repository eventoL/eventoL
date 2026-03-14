# Instalación de desarrollo

Guía para instalar y ejecutar **Eventol** en un entorno de desarrollo usando **uv**.
---

# Requisitos del sistema

El proyecto usa **GeoDjango** con **SpatiaLite**, por lo que requiere algunas librerías del sistema.

## Linux (Ubuntu / Debian)

```bash
sudo apt update

sudo apt install -y \
    libsqlite3-mod-spatialite \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    libxmlsec1 \
    libxmlsec1-dev
```

## Linux (Arch / Manjaro)

```bash
sudo pacman -S \
    libspatialite \
    gdal \
    geos \
    proj \
    xmlsec
```

## MacOS (Homebrew)

```bash
brew install spatialite gdal geos proj xmlsec
```

## Windows

En Windows la forma más sencilla es instalar **OSGeo4W**.

1. Descargar el instalador
   https://trac.osgeo.org/osgeo4w/

2. Instalar los paquetes:

* gdal
* geos
* proj
* spatialite

---

# Instalar uv

Linux / MacOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verificar instalación:

```bash
uv --version
```

---

# Instalar Python 3.11 con uv

uv puede descargar versiones de Python automáticamente.

```bash
uv python install 3.11
```

Verificar:

```bash
uv python list
```

---

# Crear el entorno virtual

Desde el directorio del proyecto:

```bash
uv venv --python 3.11
```

Activar entorno:

Linux / MacOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Verificar versión:

```bash
python --version
```

Debe mostrar algo similar a:

```
Python 3.11.x
```

---

# Instalar dependencias Python

```bash
uv sync --extra dev
```

Esto instalará todas las dependencias definidas en `pyproject.toml`.

---

# Configurar base de datos espacial (SpatiaLite)

Antes de correr las migraciones es necesario inicializar los metadatos espaciales:

```bash
python manage.py shell -c "import django;django.db.connection.cursor().execute('SELECT InitSpatialMetaData(1);')"
```

---

# Ejecutar migraciones

```bash
python manage.py migrate
```

---

# Crear superusuario

```bash
python manage.py createsuperuser
```

---

# Ejecutar servidor de desarrollo

```bash
python manage.py runserver 0.0.0.0:8000
```

El sitio estará disponible en:

```
http://127.0.0.1:8000
```

---

# Pre-commit (lint y formatter)

El proyecto utiliza **ruff** junto con **pre-commit** para verificar formato y estilo antes de cada commit.

Instalar hooks:

```bash
pre-commit install
```

Los errores que puedan corregirse automáticamente se arreglarán solos; los restantes serán reportados con sugerencias.

Para más detalles ver:

* `.pre-commit-config.yaml`
* `pyproject.toml`

---

# Problemas comunes

## GDAL no encontrado

Verificar instalación:

```bash
gdalinfo --version
```

Si Django no detecta la librería, agregar en `settings.py`:

Linux:

```python
GDAL_LIBRARY_PATH = "/usr/lib/libgdal.so"
```

MacOS:

```python
GDAL_LIBRARY_PATH = "/opt/homebrew/lib/libgdal.dylib"
```

Windows:

```python
GDAL_LIBRARY_PATH = r"C:\OSGeo4W\bin\gdalXXX.dll"
```

---

## Error con Tkinter

```
import _tkinter # If this fails your Python may not be configured for Tk
```

Solución (Ubuntu / Debian):

```bash
sudo apt install python3-tk tk-dev
```

---

## Error con xmlsec

Instalar dependencias:

Ubuntu / Debian:

```bash
sudo apt install libxmlsec1 libxmlsec1-dev
```

Arch / Manjaro:

```bash
sudo pacman -S xmlsec
```

MacOS:

```bash
brew install xmlsec
```

---

## Reinstalar el entorno

Si hay problemas con dependencias:

```bash
rm -rf .venv

uv venv --python 3.11

source .venv/bin/activate

uv sync
```

