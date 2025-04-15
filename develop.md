# Instalación de desarrollo

## Requirements

```bash
sudo apt intsall libsqlite3-mod-spatialite
```

## Instalar pyenv

- URL: (pyenv/pyenv)[https://github.com/pyenv/pyenv]

```bash
curl https://pyenv.run | bash
```

## python 3.11.11

> To use geodjango and support spatialite on python sqlite with need to compile python in this way

```bash
PYTHON_CONFIGURE_OPTS="--enable-loadable-sqlite-extensions --enable-optimizations" \
LDFLAGS="-L/usr/local/opt/sqlite/lib" \
CPPFLAGS="-I/usr/local/opt/sqlite/include" \
pyenv install 3.11.11
pyenv shell 3.11.11
```

## Entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalar las dependencias

```bash
pip install --upgrade pip
pip install -r requirements-dev.txt
pre-commit install
```

### Errores posibles

- **import _tkinter # If this fails your Python may not be configured for Tk**: solución `sudo apt install python3-tk tk-dev`
- **./manage.py migrate: Error al intentar correr las migraciones.**Solucion:Es necesario ejecutar: `sudo  apt-get install -y gdal-bin`
- **Error de dependencias de xmlsec**: `sudo apt-get install libxmlsec1 libxmlsec1-dev`

## Correr el proyecto

```bash
cd eventol
./manage.py migrate

mkdir -p ../eventol/static
mkdir -p ../eventol/front/eventol/static
./manage.py collectstatic --noinput

./manage.py createsuperuser
./manage.py runserver 0.0.0.0:8000
```

## Precommit con linter y formatter

En el proyecto se utiliza [ruff](https://docs.astral.sh/ruff/) con [pre-commit](https://pre-commit.com/) para poder chequear formato antes de commitear. Los errores que peudan se corrigiran solos y los que no, se informaran y se sugieren posibles soluciones.
Para profundizar se puede chequear los archivos de configuracion `.pre-commit-config.yaml` y `pyproject.toml`
